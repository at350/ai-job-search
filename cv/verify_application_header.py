#!/usr/bin/env python3
"""Verify that a cover-letter PDF header matches the exact resume PDF header."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from candidate_profile import contact_line, load_profile

import pdfplumber


@dataclass(frozen=True)
class HeaderLine:
    text: str
    font: str
    size: float
    x0: float
    x1: float
    top: float
    bottom: float

    @property
    def center(self) -> float:
        return (self.x0 + self.x1) / 2


def normalize_font(name: str) -> str:
    name = re.sub(r"^[A-Z]{6}\+", "", name)
    return re.sub(r"[^a-z0-9]", "", name.lower())


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def header_lines(path: Path) -> list[HeaderLine]:
    with pdfplumber.open(path) as document:
        if not document.pages:
            raise ValueError(f"PDF has no pages: {path}")
        page = document.pages[0]
        words = page.extract_words(extra_attrs=["fontname", "size"])

    header_words = [word for word in words if float(word["top"]) < 75]
    if not header_words:
        raise ValueError(f"No header text found above 75 points: {path}")

    grouped: list[list[dict]] = []
    for word in sorted(header_words, key=lambda item: (float(item["top"]), float(item["x0"]))):
        if not grouped or abs(float(word["top"]) - float(grouped[-1][0]["top"])) > 1.0:
            grouped.append([word])
        else:
            grouped[-1].append(word)

    lines: list[HeaderLine] = []
    for group in grouped[:2]:
        ordered = sorted(group, key=lambda item: float(item["x0"]))
        fonts = {normalize_font(str(item["fontname"])) for item in ordered}
        sizes = {round(float(item["size"]), 3) for item in ordered}
        if len(fonts) != 1:
            raise ValueError(f"Mixed fonts within a header line in {path}: {sorted(fonts)}")
        if max(sizes) - min(sizes) > 0.15:
            raise ValueError(f"Mixed sizes within a header line in {path}: {sorted(sizes)}")
        lines.append(
            HeaderLine(
                text=" ".join(str(item["text"]) for item in ordered),
                font=next(iter(fonts)),
                size=sum(float(item["size"]) for item in ordered) / len(ordered),
                x0=min(float(item["x0"]) for item in ordered),
                x1=max(float(item["x1"]) for item in ordered),
                top=min(float(item["top"]) for item in ordered),
                bottom=max(float(item["bottom"]) for item in ordered),
            )
        )
    if len(lines) != 2:
        raise ValueError(f"Expected two header lines in {path}, found {len(lines)}")
    return lines


def canonical_link_uris() -> set[str]:
    profile = load_profile()
    return {profile["linkedin_url"], profile["github_url"]}


def compare(resume: list[HeaderLine], cover: list[HeaderLine]) -> list[str]:
    errors: list[str] = []
    labels = ("name", "contact")
    profile = load_profile()
    expected_text = (
        normalize_text(profile["name"]),
        normalize_text(contact_line(profile)),
    )
    for index, label in enumerate(labels):
        resume_line = resume[index]
        cover_line = cover[index]
        for source, line in (("resume", resume_line), ("cover", cover_line)):
            if normalize_text(line.text) != expected_text[index]:
                errors.append(f"{source} {label} text differs from the canonical header: {line.text!r}")
        if resume_line.font != cover_line.font:
            errors.append(
                f"{label} font mismatch: resume={resume_line.font}, cover={cover_line.font}"
            )
        if abs(resume_line.size - cover_line.size) > 0.15:
            errors.append(
                f"{label} size mismatch: resume={resume_line.size:.2f}, cover={cover_line.size:.2f}"
            )
        if abs(resume_line.center - cover_line.center) > 1.0:
            errors.append(
                f"{label} centering mismatch: resume={resume_line.center:.2f}, cover={cover_line.center:.2f}"
            )
        if abs(resume_line.top - cover_line.top) > 1.0:
            errors.append(
                f"{label} vertical-position mismatch: resume={resume_line.top:.2f}, cover={cover_line.top:.2f}"
            )
        if abs(resume_line.x0 - cover_line.x0) > 2.0 or abs(resume_line.x1 - cover_line.x1) > 2.0:
            errors.append(
                f"{label} width mismatch: resume={resume_line.x0:.2f}-{resume_line.x1:.2f}, "
                f"cover={cover_line.x0:.2f}-{cover_line.x1:.2f}"
            )
    return errors


def cover_header_rule(path: Path, contact_bottom: float) -> dict | None:
    with pdfplumber.open(path) as document:
        page = document.pages[0]
        candidates = [
            line
            for line in page.lines
            if float(line.get("width", 0)) >= 520
            and 0.3 <= float(line.get("linewidth", 0)) <= 0.7
            and contact_bottom + 5 <= float(line.get("top", 0)) <= contact_bottom + 30
        ]
    if not candidates:
        return None
    return max(candidates, key=lambda line: float(line.get("width", 0)))


def link_underlines(path: Path) -> list[dict]:
    """Return the two visible header-link rules, ordered left to right."""
    with pdfplumber.open(path) as document:
        page = document.pages[0]
        links = [
            link
            for link in page.hyperlinks
            if link.get("uri") in canonical_link_uris()
        ]
        if len(links) != 2:
            raise ValueError(f"Expected two canonical header hyperlinks in {path}, found {len(links)}")

        rules: list[dict] = []
        for link in sorted(links, key=lambda item: float(item["x0"])):
            candidates = [
                line
                for line in page.lines
                if abs(float(line.get("x0", 0)) - float(link["x0"])) <= 1.0
                and abs(float(line.get("x1", 0)) - float(link["x1"])) <= 1.0
                and abs(float(line.get("top", 0)) - float(link["bottom"])) <= 3.0
                and 0.3 <= float(line.get("linewidth", 0)) <= 0.7
            ]
            if not candidates:
                raise ValueError(
                    f"Missing visible underline for header hyperlink {link.get('uri')} in {path}"
                )
            rules.append(min(candidates, key=lambda line: abs(float(line["top"]) - float(link["bottom"]))))
    return rules


def normalize_color(color: object) -> tuple[float, ...]:
    if isinstance(color, (int, float)):
        value = float(color)
        return (value, value, value)
    if isinstance(color, (tuple, list)):
        return tuple(float(value) for value in color)
    return ()


def compare_link_underlines(resume_pdf: Path, cover_pdf: Path) -> tuple[list[str], list[dict], list[dict]]:
    errors: list[str] = []
    resume_rules = link_underlines(resume_pdf)
    cover_rules = link_underlines(cover_pdf)

    if abs(float(cover_rules[0]["top"]) - float(cover_rules[1]["top"])) > 0.25:
        errors.append(
            "cover header link underlines are not baseline-aligned: "
            f"LinkedIn={float(cover_rules[0]['top']):.2f}, GitHub={float(cover_rules[1]['top']):.2f}"
        )

    for index, label in enumerate(("LinkedIn", "GitHub")):
        resume_rule = resume_rules[index]
        cover_rule = cover_rules[index]
        if abs(float(resume_rule["top"]) - float(cover_rule["top"])) > 1.25:
            errors.append(
                f"{label} underline vertical mismatch: "
                f"resume={float(resume_rule['top']):.2f}, cover={float(cover_rule['top']):.2f}"
            )
        if abs(float(resume_rule["linewidth"]) - float(cover_rule["linewidth"])) > 0.25:
            errors.append(
                f"{label} underline weight mismatch: "
                f"resume={float(resume_rule['linewidth']):.2f}, "
                f"cover={float(cover_rule['linewidth']):.2f}"
            )
        resume_color = normalize_color(resume_rule.get("stroking_color"))
        cover_color = normalize_color(cover_rule.get("stroking_color"))
        if len(resume_color) != len(cover_color) or any(
            abs(left - right) > 0.02 for left, right in zip(resume_color, cover_color)
        ):
            errors.append(
                f"{label} underline color mismatch: resume={resume_color}, cover={cover_color}"
            )
    return errors, resume_rules, cover_rules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare the first two rendered header lines of a resume and cover letter"
    )
    parser.add_argument("resume_pdf", type=Path)
    parser.add_argument("cover_letter_pdf", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        resume = header_lines(args.resume_pdf)
        cover = header_lines(args.cover_letter_pdf)
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1

    errors = compare(resume, cover)
    try:
        underline_errors, _, cover_underlines = compare_link_underlines(
            args.resume_pdf, args.cover_letter_pdf
        )
        errors.extend(underline_errors)
    except (OSError, ValueError) as error:
        errors.append(str(error))
        cover_underlines = []
    rule = cover_header_rule(args.cover_letter_pdf, cover[1].bottom)
    if rule is None:
        errors.append(
            "cover header is missing the required full-width 0.4-point horizontal rule"
        )
    else:
        if abs(float(rule["x0"]) - 43.2) > 1.0 or abs(float(rule["x1"]) - 568.8) > 1.0:
            errors.append(
                f"cover header rule width mismatch: {float(rule['x0']):.2f}-{float(rule['x1']):.2f}"
            )
    if errors:
        print("FAIL: application header mismatch")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: cover-letter header matches resume header")
    for label, resume_line, cover_line in zip(("name", "contact"), resume, cover):
        print(
            f"- {label}: font={resume_line.font}, size={resume_line.size:.2f}/{cover_line.size:.2f}, "
            f"top={resume_line.top:.2f}/{cover_line.top:.2f}, "
            f"center={resume_line.center:.2f}/{cover_line.center:.2f}"
        )
    if rule is not None:
        print(
            f"- rule: x={float(rule['x0']):.2f}-{float(rule['x1']):.2f}, "
            f"top={float(rule['top']):.2f}, weight={float(rule['linewidth']):.2f} pt"
        )
    if cover_underlines:
        print(
            "- link underlines: "
            f"top={float(cover_underlines[0]['top']):.2f}/{float(cover_underlines[1]['top']):.2f}, "
            f"weight={float(cover_underlines[0]['linewidth']):.2f}/"
            f"{float(cover_underlines[1]['linewidth']):.2f} pt, "
            f"color={normalize_color(cover_underlines[0].get('stroking_color'))}/"
            f"{normalize_color(cover_underlines[1].get('stroking_color'))}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
