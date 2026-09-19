#!/usr/bin/env python3
"""Fail fast on blocking resume layout and structural defects."""

from __future__ import annotations

import argparse
import re
import statistics
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from candidate_profile import load_profile


MONTHS = (
    "January|February|March|April|May|June|July|August|"
    "September|October|November|December"
)
# A full range carrying a year on both ends, e.g. "May 2026 - Present".
_FULL_RANGE = (
    rf"(?:{MONTHS})\s+\d{{4}}\s+[–-]\s+(?:(?:{MONTHS})\s+\d{{4}}|Present)"
)
# A same-year range that prints the year once, e.g. "June - August 2026".
_SHORT_RANGE = rf"(?:{MONTHS})\s+[–-]\s+(?:{MONTHS})\s+\d{{4}}"
# Federal-style resumes append average hours per week to the date column, e.g.
# "May 2026 - Present, 40 hrs/week". Federal reviewers use that figure to weigh
# how substantial a role was, so the date column has to carry it. Optional, so
# every existing one-page house-style resume still matches unchanged.
_HOURS = r"(?:,\s+\d{1,3}\s+hrs/week)?"
DATE_LINE = re.compile(
    rf"^(?:Expected\s+(?:{MONTHS})\s+\d{{4}}|{_FULL_RANGE}|{_SHORT_RANGE}){_HOURS}$"
)
ROLE_DATE_LINE = re.compile(
    rf"^(?:(?:{MONTHS})\s+\d{{4}}|{_FULL_RANGE}|{_SHORT_RANGE}){_HOURS}$"
)
YEAR_LINE = re.compile(r"^(?:19|20)\d{2}$")
BULLETS = {"•", "●"}
HANGING_TOLERANCE = 1.5
RIGHT_COLUMN_FRACTION = 0.6
EXPECTED_BULLET = "●"
DISALLOWED_GENERIC_LABELS = {
    "INDEPENDENT RESEARCH",
    "AI HACKATHON PROJECTS",
    "AI PROJECT",
    "STARTUP",
}
MAX_SKILL_CATEGORIES = 4
MAX_SKILL_LINES = 6
WEAK_ANALYSIS_LEADS = {
    "analyzed",
    "assessed",
    "conducted",
    "evaluated",
    "explored",
    "identified",
    "improved",
    "investigated",
    "researched",
    "reviewed",
}
DOWNSTREAM_IMPACT_RE = re.compile(
    r"\b(?:adopted|approved|booked|cut|doubled|grew|implemented|increased|"
    r"launched|leading|lowered|prompted|prompting|raised|reallocate|reallocated|reduced|resulting|"
    r"saved|secured|shipped|shortened|tripled|won)\b",
    re.IGNORECASE,
)
BULLET_URL_RE = re.compile(
    r"(?:https?://\S+|www\.\S+|(?:github|gitlab|bitbucket|devpost)\.com/\S+|"
    r"[a-z0-9-]+\.(?:com|io|ai|app|dev|tech|me)(?:/\S*)?)",
    re.IGNORECASE,
)
BULLET_SENTENCE_BREAK_RE = re.compile(r"[a-z0-9%)]\.\s+[A-Z]")
# Lexical repetition scan (WARN, not FAIL). Added 2026-08-09 after a draft
# shipped "Cut" nine times on one page. Every per-bullet gate passed; nothing
# was looking at the page's language as a whole.
REPETITION_WORD_LIMIT = 3
REPETITION_VERB_LIMIT = 2
REPETITION_STOPWORDS = {
    "a", "across", "after", "an", "and", "any", "are", "as", "at", "b", "be",
    "before", "both", "but", "by", "each", "every", "for", "from", "had", "has",
    "have", "how", "in", "into", "is", "it", "its", "no", "not", "of", "on",
    "one", "only", "or", "out", "over", "per", "s", "so", "than", "that", "the",
    "their", "them", "then", "there", "these", "they", "this", "through", "to",
    "under", "until", "up", "was", "were", "what", "when", "where", "which",
    "while", "who", "why", "with", "within", "without",
    # URL fragments from the header contact line, not resume prose
    "com", "edu", "http", "https", "net", "org", "www",
}
STANDARD_SECTION_HEADINGS = {
    "EDUCATION",
    "SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "WORK HISTORY",
    "EXPERIENCE",
    "RELEVANT EXPERIENCE",
    "ENGINEERING EXPERIENCE",
    "TECHNICAL EXPERIENCE",
    "AI & MACHINE LEARNING EXPERIENCE",
    "PROJECT EXPERIENCE",
    "PROJECTS",
    "RESEARCH",
    "RESEARCH EXPERIENCE",
    "LEADERSHIP",
    "HONORS",
    "AWARDS",
    "HONORS & AWARDS",
    "AWARDS & HONORS",
    "HONORS AND AWARDS",
    "AWARDS AND HONORS",
    "ACTIVITIES",
    "ACTIVITIES & COMMUNITY INVOLVEMENT",
    "ADDITIONAL INFORMATION",
}
APPROVED_BODY_FONT_MARKERS = {
    "timesnewroman",
    "liberationserif",
}
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
EXPECTED_BODY_FONT = "Times New Roman"
EXPECTED_BODY_SIZE = "22"
EXPECTED_LINE = "240"
EXPECTED_BULLET_LINE = "250"
MAX_PARAGRAPH_BEFORE = 180


@dataclass
class Word:
    text: str
    xmin: float
    xmax: float


@dataclass
class Line:
    text: str
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    words: list[Word]
    block_index: int


def run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_page_count(pdf_path: Path) -> int:
    info = run(["pdfinfo", str(pdf_path)])
    match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    if match is None:
        raise RuntimeError("Could not read the PDF page count")
    return int(match.group(1))


def normalize_font_name(font_name: str) -> str:
    family_name = font_name.split("+", 1)[-1]
    return re.sub(r"[^a-z0-9]", "", family_name.lower())


def parse_pdffonts(font_output: str) -> list[tuple[str, str, str]]:
    fonts: list[tuple[str, str, str]] = []
    for raw_line in font_output.splitlines():
        match = re.search(
            r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$",
            raw_line,
        )
        if match is None:
            continue
        font_name = raw_line.split()[0]
        embedded, _, unicode_mapping = match.groups()
        fonts.append((font_name, embedded, unicode_mapping))
    return fonts


def verify_font_table(font_output: str, errors: list[str]) -> list[str]:
    fonts = parse_pdffonts(font_output)
    if not fonts:
        errors.append("No rendered PDF fonts were detected")
        return []

    detected_families: list[str] = []
    approved_body_detected = False
    for font_name, embedded, unicode_mapping in fonts:
        family = font_name.split("+", 1)[-1]
        normalized = normalize_font_name(font_name)
        if family not in detected_families:
            detected_families.append(family)

        if any(marker in normalized for marker in APPROVED_BODY_FONT_MARKERS):
            approved_body_detected = True
        else:
            errors.append(
                f"Unexpected rendered font family '{family}'; expected Times New "
                "Roman or the documented Liberation Serif fallback. Dedicated "
                "symbol fonts are forbidden because they can inflate bullet line boxes"
            )

        if embedded != "yes":
            errors.append(f"Rendered font '{family}' is not embedded")
        if unicode_mapping != "yes":
            errors.append(f"Rendered font '{family}' has no Unicode mapping")

    if not approved_body_detected:
        errors.append(
            "No approved rendered body font was detected; expected Times New Roman "
            "or the documented Liberation Serif fallback"
        )
    return detected_families


def verify_pdf_fonts(pdf_path: Path, errors: list[str]) -> list[str]:
    return verify_font_table(run(["pdffonts", str(pdf_path)]), errors)


def xml_attr(node: ET.Element | None, name: str) -> str | None:
    if node is None:
        return None
    return node.attrib.get(f"{W}{name}")


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(
        node.text or "" for node in paragraph.findall(f".//{W}t")
    ).strip()


def normalize_artifact_text(text: str) -> str:
    text = text.replace(EXPECTED_BULLET, " ")
    text = re.sub(r"-\s+", "-", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_docx_text(docx_path: Path) -> str:
    with ZipFile(docx_path) as archive:
        parts = sorted(
            name
            for name in archive.namelist()
            if re.fullmatch(r"word/header\d+\.xml", name)
        )
        parts.append("word/document.xml")
        paragraphs: list[str] = []
        for part in parts:
            root = ET.fromstring(archive.read(part))
            for paragraph in root.findall(f".//{W}p"):
                text = paragraph_text(paragraph)
                if text:
                    paragraphs.append(text)
        return "\n".join(paragraphs)


def verify_docx_pdf_text_match(
    pdf_path: Path,
    docx_path: Path,
    errors: list[str],
) -> None:
    try:
        docx_text = normalize_artifact_text(extract_docx_text(docx_path))
    except (BadZipFile, ET.ParseError, KeyError) as exc:
        errors.append(f"DOCX text could not be extracted for pair verification: {exc}")
        return
    pdf_text = normalize_artifact_text(
        run(["pdftotext", "-raw", str(pdf_path), "-"])
    )
    if docx_text != pdf_text:
        errors.append(
            "PDF text does not exactly match the canonical DOCX source; the pair "
            "may be stale or may come from different builds"
        )


# Density rule (see the House Style Spec and
# cv/PLAN - house-style-density-update-2026-08-31.md): ordinary bullets carry
# 1pt (20 twips) after, and the final bullet of each entry carries 6pt (120
# twips) after to separate entries. Wrapped bullet text keeps the slightly
# looser 1.04 line spacing (250/240). Section headers carry 8pt (160 twips)
# before and 2pt (40 twips) after the bottom rule.
BULLET_SPACING_AFTER = "20"
FINAL_BULLET_SPACING_AFTER = "120"
HEADING_SPACING_AFTER = "40"


def verify_spacing_node(
    spacing: ET.Element | None,
    label: str,
    errors: list[str],
    *,
    check_before: bool = True,
    is_bullet: bool = False,
    is_final_bullet: bool = False,
    is_heading: bool = False,
) -> None:
    if spacing is None:
        errors.append(f"{label} has no explicit paragraph spacing")
        return
    expected_after = (
        FINAL_BULLET_SPACING_AFTER
        if is_final_bullet
        else BULLET_SPACING_AFTER
        if is_bullet
        else HEADING_SPACING_AFTER
        if is_heading
        else "0"
    )
    if xml_attr(spacing, "after") != expected_after:
        if is_bullet:
            errors.append(
                f"{label} is a bullet and must set paragraph spacing after to "
                f"{expected_after} twips "
                f"({'6pt final-bullet gap' if is_final_bullet else '1pt inter-bullet gap'})"
            )
        elif is_heading:
            errors.append(
                f"{label} is a section header and must set paragraph spacing "
                f"after to {HEADING_SPACING_AFTER} twips (2pt gap under the rule)"
            )
        else:
            errors.append(f"{label} must set paragraph spacing after to 0")
    expected_line = EXPECTED_BULLET_LINE if is_bullet else EXPECTED_LINE
    if xml_attr(spacing, "line") != expected_line:
        if is_bullet:
            errors.append(
                f"{label} must use the approved 250-twip bullet line spacing"
            )
        else:
            errors.append(f"{label} must use single line spacing of 240 twips")
    if xml_attr(spacing, "lineRule") != "auto":
        errors.append(f"{label} must use lineRule=auto")
    if check_before:
        before = xml_attr(spacing, "before") or "0"
        try:
            before_value = int(before)
        except ValueError:
            errors.append(f"{label} has invalid spacing before value '{before}'")
        else:
            if before_value > MAX_PARAGRAPH_BEFORE:
                errors.append(
                    f"{label} uses {before_value} twips before spacing; maximum is "
                    f"{MAX_PARAGRAPH_BEFORE}"
                )


def verify_artifact_pair(
    pdf_path: Path,
    docx_path: Path,
    errors: list[str],
) -> None:
    if pdf_path.parent != docx_path.parent:
        errors.append("PDF and DOCX must be the exact canonical pair in one directory")
    if pdf_path.stem != docx_path.stem:
        errors.append("PDF and DOCX filenames do not identify the same artifact")
    if docx_path.parent.name != "cv":
        errors.append("Canonical resume DOCX and PDF must both be under cv/")
    if pdf_path.exists() and docx_path.exists():
        if pdf_path.stat().st_mtime_ns < docx_path.stat().st_mtime_ns:
            errors.append("PDF is older than its DOCX source and may be stale")


def verify_docx_layout(docx_path: Path, errors: list[str]) -> None:
    try:
        with ZipFile(docx_path) as archive:
            required = {
                "word/document.xml",
                "word/styles.xml",
                "word/numbering.xml",
            }
            missing = required.difference(archive.namelist())
            if missing:
                errors.append(
                    "DOCX is missing required layout parts: " + ", ".join(sorted(missing))
                )
                return
            document = ET.fromstring(archive.read("word/document.xml"))
            styles = ET.fromstring(archive.read("word/styles.xml"))
            numbering = ET.fromstring(archive.read("word/numbering.xml"))
    except (BadZipFile, ET.ParseError) as exc:
        errors.append(f"DOCX source could not be parsed: {exc}")
        return

    default_spacing = styles.find(
        f".//{W}docDefaults/{W}pPrDefault/{W}pPr/{W}spacing"
    )
    verify_spacing_node(
        default_spacing,
        "DOCX default paragraph style",
        errors,
        check_before=False,
    )

    normal_style = None
    for style in styles.findall(f".//{W}style"):
        if xml_attr(style, "styleId") == "Normal":
            normal_style = style
            break
    normal_spacing = (
        None
        if normal_style is None
        else normal_style.find(f"./{W}pPr/{W}spacing")
    )
    verify_spacing_node(
        normal_spacing,
        "DOCX Normal paragraph style",
        errors,
        check_before=False,
    )

    body_paragraphs = document.findall(f".//{W}body/{W}p")
    for index, paragraph in enumerate(body_paragraphs, start=1):
        text = paragraph_text(paragraph)
        if not text:
            continue
        spacing = paragraph.find(f"./{W}pPr/{W}spacing")
        label = f"DOCX paragraph {index} ('{text[:32]}')"
        is_bullet = paragraph.find(f"./{W}pPr/{W}numPr/{W}numId") is not None
        is_heading = (
            not is_bullet
            and paragraph.find(f"./{W}pPr/{W}pBdr/{W}bottom") is not None
        )
        next_is_bullet = False
        if is_bullet:
            for next_paragraph in body_paragraphs[index:]:
                if not paragraph_text(next_paragraph):
                    continue
                next_is_bullet = (
                    next_paragraph.find(f"./{W}pPr/{W}numPr/{W}numId") is not None
                )
                break
        verify_spacing_node(
            spacing,
            label,
            errors,
            is_bullet=is_bullet,
            is_final_bullet=is_bullet and not next_is_bullet,
            is_heading=is_heading,
        )

    used_num_ids = {
        xml_attr(node, "val")
        for node in document.findall(f".//{W}body/{W}p/{W}pPr/{W}numPr/{W}numId")
        if xml_attr(node, "val") is not None
    }
    num_to_abstract: dict[str, str] = {}
    for num in numbering.findall(f".//{W}num"):
        num_id = xml_attr(num, "numId")
        abstract = num.find(f"./{W}abstractNumId")
        abstract_id = xml_attr(abstract, "val")
        if num_id is not None and abstract_id is not None:
            num_to_abstract[num_id] = abstract_id

    abstract_by_id = {
        xml_attr(node, "abstractNumId"): node
        for node in numbering.findall(f".//{W}abstractNum")
        if xml_attr(node, "abstractNumId") is not None
    }

    checked_bullet = False
    for num_id in used_num_ids:
        abstract = abstract_by_id.get(num_to_abstract.get(num_id, ""))
        if abstract is None:
            continue
        level = None
        for candidate in abstract.findall(f"./{W}lvl"):
            if xml_attr(candidate, "ilvl") == "0":
                level = candidate
                break
        if level is None:
            continue
        marker = xml_attr(level.find(f"./{W}lvlText"), "val")
        if marker != EXPECTED_BULLET:
            continue
        checked_bullet = True
        suffix = xml_attr(level.find(f"./{W}suff"), "val")
        if suffix != "tab":
            errors.append("DOCX bullet marker must use a tab suffix")
        fonts = level.find(f"./{W}rPr/{W}rFonts")
        marker_fonts = {
            xml_attr(fonts, name)
            for name in ("ascii", "hAnsi", "eastAsia", "cs")
            if xml_attr(fonts, name) is not None
        }
        if marker_fonts != {EXPECTED_BODY_FONT}:
            errors.append(
                "DOCX bullet marker must use Times New Roman, not a dedicated "
                f"symbol font; found {sorted(marker_fonts)}"
            )
        if xml_attr(level.find(f"./{W}rPr/{W}sz"), "val") != EXPECTED_BODY_SIZE:
            errors.append("DOCX bullet marker must use the 11 pt body size")
        indent = level.find(f"./{W}pPr/{W}ind")
        if xml_attr(indent, "left") != "720" or xml_attr(indent, "hanging") != "360":
            errors.append("DOCX bullet numbering indent must be left 720, hanging 360")
        tab = level.find(f"./{W}pPr/{W}tabs/{W}tab")
        if xml_attr(tab, "pos") != "720":
            errors.append("DOCX bullet numbering tab stop must be 720 twips")

    if used_num_ids and not checked_bullet:
        errors.append("DOCX uses numbered paragraphs but no valid solid-circle bullet definition")


def normalized_text_lines(extracted_text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", line.strip()).upper()
        for line in extracted_text.replace("\f", "\n").splitlines()
        if line.strip()
    ]


def is_experience_heading(normalized: str) -> bool:
    return (
        normalized.endswith("EXPERIENCE")
        or normalized in {"PROJECTS", "RESEARCH", "LEADERSHIP"}
    )


def is_section_heading(normalized: str) -> bool:
    return normalized in STANDARD_SECTION_HEADINGS or is_experience_heading(normalized)


def verify_extracted_text(
    extracted_text: str,
    errors: list[str],
    *,
    allow_missing_skills: bool = False,
    profile: dict[str, str] | None = None,
) -> None:
    profile = profile or load_profile()
    if not extracted_text.strip():
        errors.append("PDF text extraction returned no selectable text")
        return
    if "\ufffd" in extracted_text:
        errors.append("Extracted PDF text contains missing-glyph replacement characters")

    lines = normalized_text_lines(extracted_text)

    def find_line(predicate, start: int = 0) -> int | None:
        for index in range(start, len(lines)):
            if predicate(lines[index]):
                return index
        return None

    name_index = find_line(lambda line: line == profile["name"].upper())
    contact_index = find_line(
        lambda line: profile["email"].upper() in line,
        0 if name_index is None else name_index + 1,
    )
    education_index = find_line(lambda line: line == "EDUCATION")
    school_index = find_line(lambda line: profile["school"].upper() in line)
    skills_index = find_line(lambda line: line == "SKILLS")
    experience_index = find_line(is_experience_heading)

    required_positions = [
        ("name", name_index),
        ("contact line", contact_index),
        ("Education heading", education_index),
        (profile["school"], school_index),
        ("experience section", experience_index),
    ]
    if not allow_missing_skills:
        required_positions.append(("Skills heading", skills_index))
    for label, position in required_positions:
        if position is None:
            errors.append(f"Extracted reading order is missing the {label}")

    if all(position is not None for _, position in required_positions):
        base_order_is_logical = (
            name_index < contact_index < education_index < school_index
            and experience_index > school_index
        )
        skills_order_is_logical = skills_index is None or skills_index > school_index
        if not (base_order_is_logical and skills_order_is_logical):
            errors.append(
                "Extracted reading order is not logical: expected name, contact, "
                f"Education, {profile['school']}, then experience and any Skills section"
            )

    uppercase_text = extracted_text.upper()
    for contact_token in (
        profile["location"].upper(),
        profile["phone"].upper(),
        profile["linkedin"].upper(),
        profile["github"].upper(),
    ):
        if contact_token not in uppercase_text:
            errors.append(
                f"Extracted contact information is missing '{contact_token}'"
            )

    if EXPECTED_BULLET not in extracted_text:
        errors.append(
            f"Extracted PDF text is missing the expected '{EXPECTED_BULLET}' bullets"
        )


def verify_extracted_reading_order(
    pdf_path: Path,
    errors: list[str],
    *,
    allow_missing_skills: bool = False,
    profile: dict[str, str] | None = None,
) -> None:
    extracted_text = run(["pdftotext", "-raw", str(pdf_path), "-"])
    verify_extracted_text(
        extracted_text,
        errors,
        allow_missing_skills=allow_missing_skills,
        profile=profile,
    )


def bullet_bodies(extracted_text: str) -> list[str]:
    bodies: list[str] = []
    current: list[str] = []
    for raw_line in extracted_text.replace("\f", "\n").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line[0] in BULLETS:
            if current:
                bodies.append(" ".join(current))
            current = [line[1:].strip()]
        elif current and " | " not in line and not is_section_heading(
            re.sub(r"\s+", " ", line).upper()
        ):
            current.append(line)
        elif current:
            bodies.append(" ".join(current))
            current = []
    if current:
        bodies.append(" ".join(current))
    return bodies


def verify_bullet_impact(extracted_text: str, errors: list[str]) -> None:
    """Reject analysis bullets that stop at a finding without a consequence."""
    for body in bullet_bodies(extracted_text):
        lead_match = re.match(r"[A-Za-z][A-Za-z'-]*", body)
        if not lead_match:
            continue
        lead = lead_match.group(0).lower()
        # Search only after the lead verb. Searching the whole bullet allowed
        # "Improved ..." to satisfy its own impact check even when the rest of
        # the bullet named only activity, reviewers, and elapsed sprints.
        remainder = body[lead_match.end():]
        if lead in WEAK_ANALYSIS_LEADS and not DOWNSTREAM_IMPACT_RE.search(remainder):
            errors.append(
                "Analysis bullet lacks downstream impact beyond the finding: "
                f"'{body}'"
            )


def verify_no_bullet_links(extracted_text: str, errors: list[str]) -> None:
    """Reject printed or clickable project URLs inside resume bullets.

    The standard GitHub profile remains allowed in the contact header. Project
    and repository links belong in dedicated portal fields, never in resume
    body text (house style).
    """
    for body in bullet_bodies(extracted_text):
        match = BULLET_URL_RE.search(body)
        if match:
            errors.append(
                "Project or repository URL detected inside a resume bullet: "
                f"'{match.group(0)}'. Keep only the general GitHub profile in "
                "the standard header and use dedicated portal link fields"
            )


def verify_bullet_sentence_form(extracted_text: str, errors: list[str]) -> None:
    """Require every resume bullet to remain one sentence or clause."""
    for body in bullet_bodies(extracted_text):
        if body.endswith("."):
            errors.append(
                "Resume bullet has a trailing period; bullets must be fragments: "
                f"'{body}'"
            )
        if BULLET_SENTENCE_BREAK_RE.search(body):
            errors.append(
                "Resume bullet contains more than one sentence; combine it into "
                f"one recruiter-scannable clause: '{body}'"
            )


def verify_pdf_bullet_impact(pdf_path: Path, errors: list[str]) -> None:
    extracted_text = run(["pdftotext", "-raw", str(pdf_path), "-"])
    verify_bullet_impact(extracted_text, errors)


def verify_pdf_bullet_links(pdf_path: Path, errors: list[str]) -> None:
    extracted_text = run(["pdftotext", "-raw", str(pdf_path), "-"])
    verify_no_bullet_links(extracted_text, errors)


def verify_pdf_bullet_sentence_form(pdf_path: Path, errors: list[str]) -> None:
    extracted_text = run(["pdftotext", "-raw", str(pdf_path), "-"])
    verify_bullet_sentence_form(extracted_text, errors)


def scan_lexical_repetition(pdf_path: Path) -> list[str]:
    """Page-level language scan. Returns WARN strings; never blocks a PASS.

    Two per-bullet-invisible failure modes this catches:
      1. A content word repeated across the page.
      2. The same lead verb opening several bullets, which happens because
         approved ledger bullets each individually start with the most natural
         verb for a reduction metric.
    """
    extracted_text = run(["pdftotext", "-raw", str(pdf_path), "-"])
    warnings: list[str] = []

    words: list[str] = []
    lead_verbs: list[str] = []
    for raw_line in extracted_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        is_bullet = line[0] in BULLETS
        if is_bullet:
            body = line[1:].strip()
            first = re.match(r"[A-Za-z][A-Za-z'-]*", body)
            if first:
                lead_verbs.append(first.group(0).lower())
        for token in re.findall(r"[A-Za-z][A-Za-z'-]+", line):
            lowered = token.lower()
            if lowered in REPETITION_STOPWORDS or len(lowered) < 3:
                continue
            # Skip proper nouns mid-sentence (technologies, institutions,
            # employers); repeating those is usually correct and intentional.
            if token[0].isupper() and token is not line.split()[0]:
                continue
            words.append(lowered)

    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    overused = sorted(
        ((w, c) for w, c in counts.items() if c >= REPETITION_WORD_LIMIT),
        key=lambda pair: (-pair[1], pair[0]),
    )
    if overused:
        rendered = ", ".join(f"{word} x{count}" for word, count in overused)
        warnings.append(f"Repeated content words ({rendered})")

    verb_counts: dict[str, int] = {}
    for verb in lead_verbs:
        verb_counts[verb] = verb_counts.get(verb, 0) + 1
    repeated_verbs = sorted(
        ((v, c) for v, c in verb_counts.items() if c > REPETITION_VERB_LIMIT),
        key=lambda pair: (-pair[1], pair[0]),
    )
    if repeated_verbs:
        rendered = ", ".join(f"{verb} x{count}" for verb, count in repeated_verbs)
        warnings.append(f"Repeated bullet lead verbs ({rendered})")

    return warnings


def parse_bbox(pdf_path: Path, expected_pages: int = 1) -> tuple[float, float, list[Line]]:
    with tempfile.TemporaryDirectory(prefix="resume-layout-") as tmp_dir:
        bbox_path = Path(tmp_dir) / "resume.xml"
        run(["pdftotext", "-bbox-layout", str(pdf_path), str(bbox_path)])
        root = ET.parse(bbox_path).getroot()

    namespace = {"x": "http://www.w3.org/1999/xhtml"}
    pages = root.findall(".//x:page", namespace)
    if len(pages) != expected_pages:
        raise RuntimeError(
            f"Expected {expected_pages} bbox page(s), found {len(pages)}"
        )

    # Multi-page documents are flattened into one continuous coordinate space by
    # offsetting each page's y coordinates by the cumulative height of the pages
    # above it. Bottom-whitespace therefore measures the LAST page, which is the
    # only page whose trailing whitespace is meaningful, and the x-based date and
    # bullet checks are unaffected. block_index stays globally unique so the
    # geometric bullet regrouping cannot merge across a page break.
    width = float(pages[0].attrib["width"])
    total_height = 0.0
    lines: list[Line] = []
    block_index = 0

    for page in pages:
        y_offset = total_height
        page_height = float(page.attrib["height"])
        total_height += page_height

        for block_node in page.findall(".//x:block", namespace):
            block_index += 1
            for line_node in block_node.findall("./x:line", namespace):
                words: list[Word] = []
                for word_node in line_node.findall("./x:word", namespace):
                    words.append(
                        Word(
                            text="".join(word_node.itertext()),
                            xmin=float(word_node.attrib["xMin"]),
                            xmax=float(word_node.attrib["xMax"]),
                        )
                    )
                if not words:
                    continue
                lines.append(
                    Line(
                        text=" ".join(word.text for word in words),
                        xmin=float(line_node.attrib["xMin"]),
                        xmax=float(line_node.attrib["xMax"]),
                        ymin=float(line_node.attrib["yMin"]) + y_offset,
                        ymax=float(line_node.attrib["yMax"]) + y_offset,
                        words=words,
                        block_index=block_index,
                    )
                )

    lines.sort(key=lambda line: (round(line.ymin, 2), line.xmin))
    return width, total_height, lines


def verify_bottom_density(height: float, lines: list[Line], errors: list[str]) -> float:
    bottom_whitespace = height - max(line.ymax for line in lines)
    if bottom_whitespace > 72:
        errors.append(
            f"Bottom whitespace is {bottom_whitespace:.1f} pt, above the 72 pt limit"
        )
    if bottom_whitespace < 28:
        errors.append(
            f"Bottom whitespace is {bottom_whitespace:.1f} pt, below the 28 pt safety margin"
        )
    return bottom_whitespace


def verify_dates(width: float, lines: list[Line], errors: list[str]) -> list[float]:
    date_lines = [line for line in lines if DATE_LINE.fullmatch(line.text)]
    if not date_lines:
        errors.append("No right-aligned date lines were detected")
        return []

    target = statistics.median(line.xmax for line in date_lines)
    right_aligned_years = [
        line
        for line in lines
        if YEAR_LINE.fullmatch(line.text)
        and line.xmin > width * 0.75
        and abs(line.xmax - target) <= 1.5
    ]
    aligned_lines = date_lines + right_aligned_years
    right_edges = [line.xmax for line in aligned_lines]
    target = statistics.median(right_edges)
    if target < width - 52:
        errors.append(
            f"Date right edge is {target:.1f} pt, too far from the page boundary"
        )

    for line in aligned_lines:
        if abs(line.xmax - target) > 1.5:
            errors.append(
                f"Date is not right-aligned: '{line.text}' ends at {line.xmax:.1f} pt "
                f"instead of {target:.1f} pt"
            )
    return right_edges


def verify_bullets(lines: list[Line], errors: list[str]) -> tuple[list[float], list[float]]:
    marker_positions: list[float] = []
    text_positions: list[float] = []
    date_edges = [line.xmax for line in lines if DATE_LINE.fullmatch(line.text)]
    date_edge_target = statistics.median(date_edges) if date_edges else None

    for index, line in enumerate(lines):
        if line.words[0].text not in BULLETS:
            continue
        if line.words[0].text != EXPECTED_BULLET:
            errors.append(
                f"Wrong bullet marker '{line.words[0].text}'; expected '{EXPECTED_BULLET}'"
            )
        marker_positions.append(line.words[0].xmin)
        text_line_index = index
        if len(line.words) >= 2:
            text_start = line.words[1].xmin
        else:
            text_start = None
            nearby_indices = [
                candidate_index
                for candidate_index in (index - 2, index - 1, index + 1, index + 2)
                if 0 <= candidate_index < len(lines)
            ]
            for candidate_index in nearby_indices:
                candidate = lines[candidate_index]
                if candidate.words[0].text in BULLETS:
                    continue
                vertical_overlap = min(line.ymax, candidate.ymax) - max(
                    line.ymin, candidate.ymin
                )
                if vertical_overlap >= 0 and candidate.xmin > line.xmax + 5:
                    text_start = candidate.words[0].xmin
                    text_line_index = candidate_index
                    break
            if text_start is None:
                errors.append(f"Bullet has no text at y={line.ymin:.1f}")
                marker_positions.pop()
                continue

        text_positions.append(text_start)

        rendered_lines = 1
        next_index = max(index, text_line_index) + 1
        while next_index < len(lines):
            following = lines[next_index]
            if following.words[0].text in BULLETS:
                break
            if DATE_LINE.fullmatch(following.text):
                next_index += 1
                continue
            if (
                date_edge_target is not None
                and YEAR_LINE.fullmatch(following.text)
                and abs(following.xmax - date_edge_target) <= 1.5
                and abs(following.ymin - lines[text_line_index].ymin) <= 1.5
            ):
                next_index += 1
                continue
            if following.xmin < text_start - 1.5:
                break
            if abs(following.xmin - text_start) > 1.5:
                errors.append(
                    f"Wrapped bullet line is misaligned at y={following.ymin:.1f}: "
                    f"{following.xmin:.1f} pt instead of {text_start:.1f} pt"
                )
            rendered_lines += 1
            next_index += 1

        # Density rule: a bullet may render at
        # most 2 lines. Cut words or split the bullet, never squeeze spacing.
        if rendered_lines > 2:
            snippet = lines[text_line_index].text[:48]
            errors.append(
                f"Bullet renders {rendered_lines} lines; the maximum is 2 "
                f"(house style density rule): '{snippet}'"
            )

    if not marker_positions:
        errors.append("No real bullet markers were detected")
        return marker_positions, text_positions

    if max(marker_positions) - min(marker_positions) > 1.0:
        errors.append("Bullet markers do not share one left position")
    if max(text_positions) - min(text_positions) > 1.0:
        errors.append("Bullet text does not share one hanging-indent position")

    return marker_positions, text_positions


def is_marker_line(line: Line) -> bool:
    return bool(line.words) and line.words[0].text in BULLETS


def is_date_column_fragment(line: Line, right_edge: float) -> bool:
    """A right-aligned date that pdftotext emits as its own bbox line.

    Role lines put the date at a right tab stop, and -bbox-layout reports it
    as a separate line inside the same block. It is a column artifact, not a
    wrapped word, so reporting it as a lone-word orphan is a false positive.

    The test is positional rather than an exact right-edge match: the centered
    header contact line routinely extends a couple of points past the date tab
    stop, so `right_edge` is not the tab stop. Any date sitting in the right
    portion of the page is a column fragment, while a genuinely wrapped date
    lands at the left margin or the bullet hanging indent.
    """
    if not (DATE_LINE.fullmatch(line.text) or YEAR_LINE.fullmatch(line.text)):
        return False
    return line.xmin >= right_edge * RIGHT_COLUMN_FRACTION


def group_rendered_paragraphs(lines: list[Line]) -> list[list[Line]]:
    """Regroup rendered lines into logical paragraphs.

    pdftotext's -bbox-layout blocks routinely merge a whole run of consecutive
    bullets into a single block. Grouping on block_index alone therefore only
    ever exposes the last bullet in the run, and every earlier bullet's final
    line is hidden inside the block where its orphan goes unreported. That is
    how the 2026-08-09 CCI Full-Stack draft passed the orphan scan while
    rendering 'Cloud' and 'engine' alone on their own lines.

    Bullets are regrouped geometrically instead: a line carrying a bullet
    marker opens a group, and any later line sitting at that bullet's
    hanging-indent position continues it. A following bullet's marker sits at
    the marker position rather than the hanging indent, so runs never merge.
    Non-bullet paragraphs keep the block_index grouping, which is correct for
    them.
    """
    ordered = sorted(lines, key=lambda line: (line.ymin, line.xmin))
    groups: list[list[Line]] = []
    non_bullet: dict[int, list[Line]] = {}
    current: list[Line] | None = None
    hanging: float | None = None

    for line in ordered:
        if is_marker_line(line):
            current = [line]
            groups.append(current)
            hanging = line.words[1].xmin if len(line.words) > 1 else None
            continue
        if (
            current is not None
            and hanging is not None
            and abs(line.xmin - hanging) <= HANGING_TOLERANCE
        ):
            current.append(line)
            continue
        current = None
        hanging = None
        non_bullet.setdefault(line.block_index, []).append(line)

    groups.extend(non_bullet.values())
    return groups


def verify_orphans(lines: list[Line], errors: list[str]) -> None:
    right_edge = max((line.xmax for line in lines), default=0.0)
    scannable = [
        line for line in lines if not is_date_column_fragment(line, right_edge)
    ]
    for group in group_rendered_paragraphs(scannable):
        if len(group) < 2:
            continue
        if all(
            line.text in BULLETS
            or DATE_LINE.fullmatch(line.text)
            or YEAR_LINE.fullmatch(line.text)
            for line in group
        ):
            continue
        final_line = group[-1]
        if len(final_line.words) == 1:
            errors.append(
                f"Lone-word orphan '{final_line.text}' at y={final_line.ymin:.1f}"
            )


def verify_content_structure(lines: list[Line], errors: list[str]) -> None:
    for line in lines:
        normalized = re.sub(r"\s+", " ", line.text.strip()).upper()
        for generic_label in DISALLOWED_GENERIC_LABELS:
            if normalized == generic_label or normalized.startswith(
                f"{generic_label} |"
            ):
                errors.append(
                    f"Generic label detected: '{line.text}'. "
                    "Use the real institution, employer, or project name"
                )

    role_dates = [line for line in lines if ROLE_DATE_LINE.fullmatch(line.text)]
    for index, date_line in enumerate(role_dates):
        next_y = (
            role_dates[index + 1].ymin
            if index + 1 < len(role_dates)
            else float("inf")
        )
        bullet_count = sum(
            1
            for line in lines
            if date_line.ymin < line.ymin < next_y
            and line.words[0].text in BULLETS
        )
        same_row = [
            line
            for line in lines
            if abs(line.ymin - date_line.ymin) <= 1.5
            and line.xmin < date_line.xmin
            and not DATE_LINE.fullmatch(line.text)
        ]
        same_row.sort(key=lambda line: line.xmin)
        role_label = " ".join(line.text for line in same_row) or date_line.text

        # A right-aligned date can still look correct when the role header has
        # wrapped. The old verifier therefore passed a visibly broken NASA
        # entry whose organization sat on one line and whose role plus date sat
        # on the next. Require the complete ``Organization | Role`` structure
        # on the date row, then reject any adjacent left-margin continuation.
        if "|" not in role_label:
            errors.append(
                f"Role header wraps before the date row near '{role_label}'; "
                "the organization, role, and date must render on one physical line"
            )
        else:
            role_margin = min(line.xmin for line in same_row)
            adjacent_left_fragments = [
                line
                for line in lines
                if 1.5 < abs(line.ymin - date_line.ymin) <= 14.5
                and abs(line.xmin - role_margin) <= 3.0
                and line.words
                and line.words[0].text not in BULLETS
                and not DATE_LINE.fullmatch(line.text)
                and not is_section_heading(
                    re.sub(r"\s+", " ", line.text.strip()).upper()
                )
            ]
            if adjacent_left_fragments:
                fragment = min(
                    adjacent_left_fragments,
                    key=lambda line: abs(line.ymin - date_line.ymin),
                )
                errors.append(
                    f"Role header wraps onto an adjacent line near "
                    f"'{fragment.text}'; the organization, role, and date "
                    "must render on one physical line"
                )
        if bullet_count < 2 or bullet_count > 5:
            errors.append(
                f"Entry '{role_label}' has {bullet_count} bullet(s); expected 2-5"
            )


def verify_skills_density(
    lines: list[Line],
    errors: list[str],
    *,
    allow_missing: bool = False,
) -> tuple[int, int]:
    normalized_lines = [
        re.sub(r"\s+", " ", line.text.strip()).upper() for line in lines
    ]
    try:
        start = normalized_lines.index("SKILLS") + 1
    except ValueError:
        if not allow_missing:
            errors.append("No Skills section was detected")
        return 0, 0

    end = len(lines)
    for index in range(start, len(lines)):
        text = normalized_lines[index]
        if is_section_heading(text) and text != "SKILLS":
            end = index
            break

    skill_lines = lines[start:end]
    rendered_line_count = len(skill_lines)
    category_count = sum(
        1
        for line in skill_lines
        if re.match(r"^[A-Za-z][A-Za-z &/+.-]*:", line.text)
    )

    # A wrapped Skills paragraph may be split into separate bbox blocks, so the
    # general paragraph-based orphan scan cannot reliably associate its final
    # line with the category line above it. Check the rendered Skills section
    # directly and hard-block every single-word line, including a category
    # label stranded without its content. Added after the Vertiv Planning
    # Analytics draft rendered "dashboards" alone while the general orphan scan
    # incorrectly passed.
    for line in skill_lines:
        if len(line.words) == 1:
            errors.append(
                f"Lone-word orphan in Skills section: '{line.text}' "
                f"at y={line.ymin:.1f}"
            )

    if category_count > MAX_SKILL_CATEGORIES:
        errors.append(
            f"Skills section has {category_count} categories; "
            f"maximum is {MAX_SKILL_CATEGORIES}"
        )
    if rendered_line_count > MAX_SKILL_LINES:
        errors.append(
            f"Skills section uses {rendered_line_count} rendered lines; "
            f"maximum is {MAX_SKILL_LINES}"
        )
    return category_count, rendered_line_count


def verify_role_section_assignments(
    lines: list[Line],
    errors: list[str],
    *,
    pinned_sections: dict[str, list[str]] | None = None,
) -> None:
    """Block a role that drifted out of the section it has to stay in.

    A role whose framing depends on where it sits, such as an employment role a
    reader must not mistake for a project, is pinned in `candidate.json` under
    `pinned_sections`: employer name -> the section headings it may appear under.
    """
    if pinned_sections is None:
        pinned_sections = load_profile().get("pinned_sections", {})
    if not pinned_sections:
        return
    pinned = {
        employer.upper(): {heading.upper() for heading in headings}
        for employer, headings in pinned_sections.items()
    }
    current_section: str | None = None
    for line in lines:
        normalized = re.sub(r"\s+", " ", line.text.strip()).upper()
        if is_section_heading(normalized):
            current_section = normalized
            continue
        for employer, allowed in pinned.items():
            if employer in normalized and current_section not in allowed:
                errors.append(
                    f"{employer.title()} must appear under "
                    + " or ".join(sorted(heading.title() for heading in allowed))
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument(
        "--docx",
        type=Path,
        help=(
            "Canonical DOCX source for the exact PDF. When supplied, verifies "
            "path, filename, freshness, approved paragraph spacing, and bullet OOXML."
        ),
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help=(
            "Expected page count. Defaults to 1, the house-style undergraduate "
            "resume. Use 2 only for a federal application whose posting states a "
            "two-page limit and asks for full employment history, and record the "
            "reason in the Gate B report."
        ),
    )
    parser.add_argument(
        "--allow-no-skills",
        action="store_true",
        help=(
            "Allow a deliberately omitted Skills section for a nontechnical role. "
            "A present Skills section may use 1 to 4 coherent categories; one category triggers a warning."
        ),
    )
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        parser.error(f"File not found: {pdf_path}")

    docx_path: Path | None = None
    if args.docx is not None:
        docx_path = args.docx.resolve()
        if not docx_path.exists():
            parser.error(f"File not found: {docx_path}")

    errors: list[str] = []
    if docx_path is not None:
        verify_artifact_pair(pdf_path, docx_path, errors)
        verify_docx_layout(docx_path, errors)
        verify_docx_pdf_text_match(pdf_path, docx_path, errors)
    if args.pages < 1 or args.pages > 2:
        parser.error("--pages must be 1 or 2")
    page_count = parse_page_count(pdf_path)
    if page_count != args.pages:
        errors.append(f"Resume is {page_count} pages instead of {args.pages}")

    font_families = verify_pdf_fonts(pdf_path, errors)
    verify_extracted_reading_order(
        pdf_path,
        errors,
        allow_missing_skills=args.allow_no_skills,
    )
    verify_pdf_bullet_impact(pdf_path, errors)
    verify_pdf_bullet_links(pdf_path, errors)
    verify_pdf_bullet_sentence_form(pdf_path, errors)
    width, height, lines = parse_bbox(pdf_path, expected_pages=args.pages)
    bottom_whitespace = verify_bottom_density(height, lines, errors)
    date_edges = verify_dates(width, lines, errors)
    marker_positions, text_positions = verify_bullets(lines, errors)
    verify_orphans(lines, errors)
    verify_content_structure(lines, errors)
    skill_categories, skill_lines = verify_skills_density(
        lines,
        errors,
        allow_missing=args.allow_no_skills,
    )
    verify_role_section_assignments(lines, errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"- Pages: {page_count}")
    print(
        f"- Bottom whitespace: {bottom_whitespace:.1f} pt "
        f"({bottom_whitespace / 72:.2f} in)"
    )
    print(
        f"- Bullet marker/text positions: "
        f"{statistics.median(marker_positions):.1f} / "
        f"{statistics.median(text_positions):.1f} pt"
    )
    print(
        f"- Right-aligned dates: {len(date_edges)} rows ending at "
        f"{statistics.median(date_edges):.1f} pt"
    )
    if skill_categories == 0 and args.allow_no_skills:
        print("- Skills section: deliberately omitted under --allow-no-skills")
    else:
        print(
            f"- Skills density: {skill_categories} categories across "
            f"{skill_lines} rendered lines"
        )
        if skill_categories == 1:
            print(
                "- WARN Skills section has one category; Gate B must justify "
                "its target relevance and evidence-backed keyword value"
            )
    print("- Bullet impact scan: no analysis-only bullets detected")
    print("- Project-link scan: no URLs detected inside bullets")
    print("- Bullet sentence-form scan: one clause per bullet, no trailing periods")
    print("- Lone-word orphan scan: none detected")
    repetition_warnings = scan_lexical_repetition(pdf_path)
    if repetition_warnings:
        for warning in repetition_warnings:
            print(f"- WARN lexical repetition: {warning}")
        print(
            "  Disposition each at Gate B. Changing a bullet's lead verb without "
            "touching facts, numbers, tools, or causality is not a new claim."
        )
    else:
        print("- Lexical repetition scan: none detected")
    print(f"- Rendered font families: {', '.join(font_families)}")
    print("- Extracted reading order: logical and complete")
    if docx_path is not None:
        print(
            "- DOCX/PDF pair: canonical, current, house-spacing compliant, "
            "and source-verified"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
