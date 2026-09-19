#!/usr/bin/env python3
"""Load the candidate identity the document verifiers check against.

The identity lives in `cv/candidate.json` so no name, email, phone, or school is
hard-coded in a script. `/setup` writes that file by copying `candidate.example.json`
and filling it in; it is git-ignored so a real identity never enters history. The
example file is the fallback, so the verifiers and their tests run on a fresh clone.
Point `CANDIDATE_PROFILE` at another path to verify a different person's packet.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

REQUIRED_FIELDS = (
    "name",
    "location",
    "email",
    "phone",
    "linkedin",
    "linkedin_url",
    "github",
    "github_url",
    "school",
)

_HERE = Path(__file__).resolve().parent
DEFAULT_PATH = _HERE / "candidate.json"
EXAMPLE_PATH = _HERE / "candidate.example.json"


def load_profile(path: str | os.PathLike[str] | None = None) -> dict:
    explicit = path or os.environ.get("CANDIDATE_PROFILE")
    if explicit:
        profile_path = Path(explicit)
    else:
        profile_path = DEFAULT_PATH if DEFAULT_PATH.is_file() else EXAMPLE_PATH
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise SystemExit(
            f"Candidate profile not found at {profile_path}. Run /setup, or copy "
            "cv/candidate.example.json to cv/candidate.json and fill it in."
        ) from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"Candidate profile at {profile_path} is not valid JSON: {error}") from error

    missing = [field for field in REQUIRED_FIELDS if not str(data.get(field, "")).strip()]
    if missing:
        raise SystemExit(
            f"Candidate profile at {profile_path} is missing: {', '.join(missing)}"
        )
    profile = {field: str(data[field]).strip() for field in REQUIRED_FIELDS}
    profile["pinned_sections"] = data.get("pinned_sections") or {}
    return profile


def contact_line(profile: dict[str, str]) -> str:
    """The canonical contact line, in the order the house style fixes."""
    return "  //  ".join(
        (
            profile["location"],
            profile["email"],
            profile["phone"],
            profile["linkedin"],
            profile["github"],
        )
    )
