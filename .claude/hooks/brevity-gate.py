#!/usr/bin/env python3
"""Stop hook: block any reply to the user longer than the cap, and make Claude rewrite it.

Why this exists: a prose brevity rule in CLAUDE.md tends not to hold across long sessions.
A mechanical gate does. Adjust WORD_CAP and LINE_CAP to taste, or remove the hook from
.claude/settings.json if you prefer longer replies.

Reads the Stop hook payload from stdin, finds the last assistant message in the transcript,
counts words, and blocks with a rewrite instruction when over the cap. Runs once per turn:
if stop_hook_active is already set, it lets the rewrite through so it cannot loop.
"""
import json
import re
import sys

WORD_CAP = 120          # a review gate, a status report, or a handoff fits in this
LINE_CAP = 14           # tables and long bullet lists trip this even when word-light


def last_assistant_text(path):
    text = ""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "assistant":
                    continue
                msg = obj.get("message") or {}
                parts = msg.get("content") or []
                if isinstance(parts, str):
                    candidate = parts
                else:
                    candidate = "\n".join(
                        p.get("text", "") for p in parts
                        if isinstance(p, dict) and p.get("type") == "text"
                    )
                if candidate.strip():
                    text = candidate
    except OSError:
        return ""
    return text


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("stop_hook_active"):
        return 0  # this is already the rewrite; let it through
    text = last_assistant_text(payload.get("transcript_path", ""))
    if not text:
        return 0
    words = len(re.findall(r"\S+", text))
    lines = len([ln for ln in text.splitlines() if ln.strip()])
    has_table = bool(re.search(r"^\s*\|.*\|\s*$", text, re.M))
    problems = []
    if words > WORD_CAP:
        problems.append(f"{words} words, cap is {WORD_CAP}")
    if lines > LINE_CAP:
        problems.append(f"{lines} non-empty lines, cap is {LINE_CAP}")
    if has_table:
        problems.append("a markdown table, which is banned in chat")
    if not problems:
        return 0
    reason = (
        "BREVITY GATE: the reply you just wrote has " + "; ".join(problems) + ". "
        f"Rewrite it now, under {WORD_CAP} words and {LINE_CAP} lines, no table: one line of "
        "outcome, then only the items that need the user's decision, then one question. "
        "Anything longer belongs in a file with a one-line pointer in chat. "
        "Do not apologise for the length and do not explain the rewrite."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
