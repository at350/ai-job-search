#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from verify_gate0_provenance import verify


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def map_text(draft_hash: str, rows: list[tuple[str, str, str]]) -> str:
    body = "\n".join(f"| {claim_id} | {status} | {source} |" for claim_id, status, source in rows)
    return (
        f"Benchmark-fit draft SHA-256: `{draft_hash}`\n\n"
        "| ID | Status | Direct confirmation source |\n"
        "| --- | --- | --- |\n"
        f"{body}\n"
    )


class Gate0ProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.draft = self.root / "draft.pdf"
        self.draft.write_bytes(b"draft-v1")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_map(self, rows: list[tuple[str, str, str]], draft_hash: str | None = None) -> Path:
        path = self.root / "map.md"
        path.write_text(map_text(draft_hash or digest(b"draft-v1"), rows), encoding="utf-8")
        return path

    def test_complete_provenance_and_matching_hashes_pass(self) -> None:
        companion_map = self.write_map(
            [
                ("A1", "CONFIRMED AS WRITTEN", "User direct response, 2026-08-01"),
                ("A2", "CORRECTED", "documents/cv/approved-bullets.md"),
                ("A3", "REJECTED", "User direct response, 2026-08-01"),
            ]
        )
        production = self.root / "production.pdf"
        production.write_bytes(b"production-v1")
        errors, counts, hashes = verify(
            companion_map,
            self.draft,
            production,
            digest(b"production-v1"),
        )
        self.assertEqual([], errors)
        self.assertEqual(1, counts["CONFIRMED AS WRITTEN"])
        self.assertEqual(digest(b"draft-v1"), hashes["draft"])

    def test_unresolved_claim_fails(self) -> None:
        companion_map = self.write_map([("A1", "UNCHECKED", "Not yet confirmed")])
        errors, counts, _ = verify(companion_map, self.draft)
        self.assertTrue(any("unresolved status" in error for error in errors))
        self.assertEqual(1, counts["UNRESOLVED"])

    def test_corrected_to_detail_counts_as_corrected(self) -> None:
        companion_map = self.write_map(
            [("A1", "CORRECTED TO 100,000 VIEWS", "User direct response, 2026-08-01")]
        )
        errors, counts, _ = verify(companion_map, self.draft)
        self.assertEqual([], errors)
        self.assertEqual(1, counts["CORRECTED"])

    def test_final_status_without_direct_source_fails(self) -> None:
        companion_map = self.write_map(
            [("A1", "CONFIRMED AS WRITTEN", "assistant correction report")]
        )
        errors, _, _ = verify(companion_map, self.draft)
        self.assertTrue(any("lacks a dated direct user response" in error for error in errors))

    def test_changed_draft_fails(self) -> None:
        companion_map = self.write_map(
            [("A1", "CONFIRMED AS WRITTEN", "User direct response, 2026-08-01")]
        )
        self.draft.write_bytes(b"draft-v2")
        errors, _, _ = verify(companion_map, self.draft)
        self.assertTrue(any("draft changed" in error for error in errors))

    def test_changed_production_pdf_fails(self) -> None:
        companion_map = self.write_map(
            [("A1", "CONFIRMED AS WRITTEN", "User direct response, 2026-08-01")]
        )
        production = self.root / "production.pdf"
        production.write_bytes(b"production-v2")
        errors, _, _ = verify(
            companion_map,
            self.draft,
            production,
            digest(b"production-v1"),
        )
        self.assertTrue(any("Production PDF hash mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
