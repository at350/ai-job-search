#!/usr/bin/env python3
"""Block resume finalization when Gate 0 claim provenance is incomplete."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


FINAL_STATUSES = {"CONFIRMED AS WRITTEN", "CORRECTED", "REJECTED"}
UNRESOLVED_STATUSES = {"", "UNCHECKED", "UNRESOLVED", "NEW CLAIM - UNVERIFIED"}
DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
HASH_RE = re.compile(r"Benchmark-fit draft SHA-256:\s*`?([0-9a-fA-F]{64})`?")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def find_claim_table(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = text.splitlines()
    for index, line in enumerate(lines[:-1]):
        headers = split_markdown_row(line)
        required = {"ID", "Status", "Direct confirmation source"}
        if not required.issubset(headers):
            continue
        if not is_separator(split_markdown_row(lines[index + 1])):
            continue
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.lstrip().startswith("|"):
                break
            cells = split_markdown_row(row_line)
            if len(cells) != len(headers):
                raise ValueError(
                    f"Malformed claim row: expected {len(headers)} columns, found {len(cells)}"
                )
            rows.append(dict(zip(headers, cells)))
        if not rows:
            raise ValueError("The claim-provenance table has no rows")
        return headers, rows
    raise ValueError(
        "No Markdown table with ID, Status, and Direct confirmation source columns was found"
    )


def source_is_direct(source: str) -> bool:
    normalized = source.lower()
    direct_response = "user direct response" in normalized and bool(DATE_RE.search(source))
    approved_ledger = "documents/cv/approved-bullets.md" in normalized
    return direct_response or approved_ledger


def verify(
    map_path: Path,
    draft_path: Path | None = None,
    production_pdf: Path | None = None,
    approved_pdf_sha256: str | None = None,
) -> tuple[list[str], Counter[str], dict[str, str]]:
    errors: list[str] = []
    counts: Counter[str] = Counter()
    hashes: dict[str, str] = {}

    if not map_path.is_file():
        return [f"Companion map not found: {map_path}"], counts, hashes

    text = map_path.read_text(encoding="utf-8")
    try:
        _, rows = find_claim_table(text)
    except ValueError as exc:
        return [str(exc)], counts, hashes

    for row in rows:
        claim_id = row["ID"] or "<missing ID>"
        raw_status = row["Status"].strip().upper()
        status = "CORRECTED" if raw_status.startswith("CORRECTED TO ") else raw_status
        source = row["Direct confirmation source"].strip()
        if status in FINAL_STATUSES:
            counts[status] += 1
            if not source_is_direct(source):
                errors.append(
                    f"{claim_id}: {status} lacks a dated direct user response or approved-ledger source"
                )
        elif status in UNRESOLVED_STATUSES:
            counts["UNRESOLVED"] += 1
            errors.append(f"{claim_id}: unresolved status {status or '<blank>'}")
        else:
            counts["UNRESOLVED"] += 1
            errors.append(f"{claim_id}: unsupported status {status}")

    if draft_path is not None:
        if not draft_path.is_file():
            errors.append(f"Benchmark-fit draft not found: {draft_path}")
        else:
            actual = sha256(draft_path)
            hashes["draft"] = actual
            match = HASH_RE.search(text)
            if not match:
                errors.append("Companion map is missing Benchmark-fit draft SHA-256 metadata")
            elif match.group(1).lower() != actual:
                errors.append(
                    "Benchmark-fit draft hash mismatch: the draft changed after the map was recorded"
                )

    if (production_pdf is None) != (approved_pdf_sha256 is None):
        errors.append(
            "Production fast-path verification requires both --production-pdf and --approved-pdf-sha256"
        )
    elif production_pdf is not None and approved_pdf_sha256 is not None:
        if not production_pdf.is_file():
            errors.append(f"Production PDF not found: {production_pdf}")
        elif not re.fullmatch(r"[0-9a-fA-F]{64}", approved_pdf_sha256):
            errors.append("Approved production PDF SHA-256 must contain exactly 64 hex characters")
        else:
            actual = sha256(production_pdf)
            hashes["production_pdf"] = actual
            if actual != approved_pdf_sha256.lower():
                errors.append(
                    "Production PDF hash mismatch: the file is not the exact PDF the user approved"
                )

    return errors, counts, hashes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify Gate 0 claim dispositions, confirmation provenance, and file hashes."
    )
    parser.add_argument("companion_map", type=Path)
    parser.add_argument("--draft", type=Path)
    parser.add_argument("--production-pdf", type=Path)
    parser.add_argument("--approved-pdf-sha256")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, counts, hashes = verify(
        args.companion_map,
        args.draft,
        args.production_pdf,
        args.approved_pdf_sha256,
    )
    summary = ", ".join(
        f"{label}={counts[label]}"
        for label in ("CONFIRMED AS WRITTEN", "CORRECTED", "REJECTED", "UNRESOLVED")
    )
    if errors:
        print(f"FAIL: Gate 0 provenance incomplete ({summary})")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: Gate 0 provenance complete ({summary})")
    for label, value in hashes.items():
        print(f"{label} SHA-256: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
