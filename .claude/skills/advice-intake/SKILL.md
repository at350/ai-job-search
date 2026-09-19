# Advice Intake

**name:** advice-intake
**description:** the user drops a link, screenshot, or pasted text containing professional advice (resume tactics, cold outreach and networking playbooks, interview and negotiation strategy, career positioning). This skill pulls the content, extracts the actual advice as discrete claims, judges how much weight each claim deserves, tags when it applies, and saves it to the playbook so the resume, cover letter, outreach, answer, and interview workflows can consult it while drafting. Trigger on: "save this advice", "add this to my playbook", "this resume tip", "good outreach advice", "remember this for interviews", a pasted LinkedIn/X post or short-form video about job searching, or any career-advice content the user shares or saves, since saving it is itself approval.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__list_connected_browsers, mcp__claude-in-chrome__select_browser

---

## Why this exists

`media-intake` handles ideas the user wants to be able to *talk about*. This skill handles advice that should change *how the work gets done*. They are different jobs and they retrieve differently: a podcast insight surfaces when an essay prompt asks about their worldview, whereas "cold emails should open with a specific hook, not a compliment" needs to surface at the moment an outreach message is being drafted, whether or not the user remembers they saved it.

Without this, good advice the user finds gets read once and evaporates, and the repo keeps drafting to whatever rules were written months ago.

## Storage

- **Playbook folder:** `documents/playbook/`, one file per source: `YYYY-MM-DD - <short-slug>.md` (date = intake date).
- **Index:** `documents/playbook/index.md`. One row per *claim*, not per source, because a single post often carries several separable pieces of advice with different applicability. Newest first. This is what other workflows scan.
- The playbook is tracked in git and committed along with the rest of the user's personal material; the repository being private is what keeps it private. Do not write passwords, API keys, or ID numbers into it. (Corrected 2026-08-09; this line previously claimed the folder was git-ignored, which it never was.)

## The intake flow

### 1. Get the content

- **Article / blog / newsletter:** WebFetch. If it returns a shell or paywall, open in Chrome and use `get_page_text`.
- **LinkedIn or X post:** these are JS-rendered and often gated. Go straight to Chrome, `navigate` then `get_page_text`. Capture the full post text plus the author's headline or bio, which matters for weighting (see step 3).
- **Short-form video (TikTok, Reels, Shorts):** open in Chrome and try captions or the transcript panel. Many have neither. Fall back in this order: on-screen text and the caption/description, then a web search for the creator saying the same thing in writing, then **ask the user what the video actually said**. Never reconstruct a claim from a thumbnail or a title. Mark the file `source fidelity: low` when the advice came from the user's summary rather than the source itself.
- **Screenshot or pasted text:** use it directly. Ask for the source and author if not obvious, since weighting depends on it.

### 2. Extract discrete claims

Break the content into separate, checkable pieces of advice. One post might yield three claims and a story. Each claim should be specific enough to act on. "Network more" is not a claim worth saving. "Ask for a 20 minute call with a specific agenda instead of open-ended coffee" is.

Drop the filler: hooks, engagement bait, self-promotion, and anything that restates a rule already in CLAUDE.md verbatim.

### 3. Weigh each claim

Advice quality varies enormously and the playbook is worthless if a growth-hacker take carries the same weight as a recruiter's. For each claim record:

- **Who said it and what standing they have.** A recruiter at a target company, a hiring manager, a career center, someone who has done the thing, or an anonymous content account. Do not inflate this. If you cannot establish standing, write "standing unknown".
- **Evidence type:** personal experience, data or study cited, secondhand, or assertion with nothing behind it.
- **How specific the applicability is.** Advice tuned to new-grad software hiring may be wrong for VC scout roles or defense primes.
- **Verify anything checkable.** If a claim asserts a fact about how a system works (an ATS behavior, a Workday quirk, what a recruiter screen filters on), do a quick search before recording it as true. Plenty of confident resume advice online is folklore. Record verified claims as verified and unverified ones as unverified; save both, but never let an unverified claim silently become a rule.

### 4. Classify each claim

Consider everything the user sends, but let the claim's nature decide whether it becomes a rule or stays as context.

- **RULE.** Crisp, generalizable, verified or credibly sourced, and it either sharpens or contradicts something already in CLAUDE.md. Propose a specific CLAUDE.md edit, quoting the current text and the proposed replacement. **Do not apply it without the user's approval.**
- **CONTEXT.** True and useful but situational, judgment-dependent, or narrower than a blanket rule. Lives in the playbook, gets read at draft time, and informs the draft without being mechanical. This is the default and most claims land here.
- **CONTESTED.** It conflicts with an existing CLAUDE.md rule, with a prior playbook claim, or with itself across sources. Record both positions and who holds each, flag it to the user, and do not act on it until they resolve it. Never silently overwrite a rule the user has already approved.
- **REJECTED.** Wrong, or wrong for the user specifically. Save it anyway with the reason, so the same bad advice does not get re-litigated in three months when they see it again.

### 5. Tag applicability

Two tag sets, both required, because retrieval depends on them.

**Stage** (when this advice should surface): `resume`, `cover-letter`, `short-answers`, `outreach-cold`, `outreach-warm`, `referrals`, `interview-behavioral`, `interview-technical`, `negotiation`, `positioning`, `job-search-ops`.

**Conditions** (when it does and does not apply): role type, company stage, industry, seniority, and anything else that scopes it. Write "general" only when it really is. Example: "applies to startups under 50 people; probably wrong for Workday portals at large primes".

### 6. Close the loop with the user

**A save is an endorsement.** the user saving a piece of advice means its message resonates with them (their directive, 2026-08-19). Do not ask them to react to each source; across a batch that is overkill. What a save does **not** do is settle whether a claim is true or whether it should govern the repo's drafting. Standing, evidence, and verification in step 3 are still assessed on the merits, and a claim that fails them is still recorded as CONTESTED or REJECTED with the reason, however clearly they endorsed the source. Endorsement tells you the idea appeals to them; the weighing tells you what it is worth.

So:

- **CONTEXT claims** need nothing from them. Save, tag, index, done.
- **REJECTED claims** need nothing from them either, but the digest names them, because they liked the source and deserves to see where it was wrong.
- **RULE claims** still wait. Show them the proposed CLAUDE.md edit, quoting the current text and the replacement, and do not apply it. A save says they agree with the creator, not that they have approved rewriting their own rules.
- **CONTESTED claims** still wait, for the same reason: the save cannot tell you which side of a conflict they land on.

Give them one digest per batch rather than one per source: what was saved, what became a rule proposal, what is contested, and anything that could not be retrieved. If a video's content could not be retrieved, ask them for the gist rather than guessing.

## Per-item file template

```
# <Title or first line of the post>
- Source: <URL>
- Author: <name> | Standing: <role, or "unknown">
- Published: <date> | Saved: <date>
- Type: post | article | video | newsletter | talk | screenshot
- Source fidelity: full text | partial | low (from the user's summary)

## Claims

### Claim 1: <one-line statement of the advice>
- Classification: RULE | CONTEXT | CONTESTED | REJECTED
- Stage: <tags>
- Conditions: <when it applies and when it does not>
- Evidence: <experience | data | secondhand | assertion>, <detail>
- Verified: yes (how) | no | not checkable
- Notes: <nuance, caveats, conflicts with existing rules>

### Claim 2: ...

## Exact quotes (verbatim only)
> "..." (<author>)

## The user's position
(Saved by the user, which stands as agreement with the source's message. Add their words close to verbatim if they gave any, and note where their endorsement of the source does not extend to a specific claim below.)

## Proposed rule changes
(any CLAUDE.md edits proposed from this source, with approval status and date)
```

## Index format

`documents/playbook/index.md` holds a table, newest first:

| Date | Claim (one line) | Stage | Class | Conditions | Verified | Source file |

## Retrieval (for the other workflows)

Before drafting, scan `documents/playbook/index.md` and read the claims whose **Stage** matches what is being written and whose **Conditions** fit the company and role at hand:

- Building a tailored resume, `resume` claims
- Writing a cover letter or short answers, `cover-letter` and `short-answers`
- The `warm-outreach` skill, `outreach-cold`, `outreach-warm`, `referrals`
- Interview prep, `interview-behavioral`, `interview-technical`, `negotiation`
- Strategy conversations, `positioning`, `job-search-ops`

Apply CONTEXT claims as judgment, not as checkboxes. Skip REJECTED. If a CONTESTED claim is directly relevant to what is being drafted, raise it with the user rather than picking a side. Where playbook advice conflicts with CLAUDE.md, **CLAUDE.md wins** until the user approves a change.

## Rules

- Follow CLAUDE.md's Global Writing Rules (no em-dashes, plain concise language).
- Never invent a claim, a statistic, an author, or a credential. If the source could not be read, say so and ask.
- Never quietly edit CLAUDE.md from this skill. Rule changes are proposed and wait for approval.
- Advice from a stranger on the internet does not outrank something the user has confirmed about themselves or a rule they have already approved.
- Batch intake is the normal case. Twenty saved sources means twenty files and one digest at the end, not twenty conversations.
