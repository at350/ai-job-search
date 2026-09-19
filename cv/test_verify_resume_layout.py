#!/usr/bin/env python3
"""Regression tests for blocking resume structure checks."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from cv.verify_resume_layout import (
    Line,
    Word,
    normalize_artifact_text,
    verify_artifact_pair,
    verify_bullet_impact,
    verify_bullet_sentence_form,
    verify_content_structure,
    verify_docx_layout,
    verify_extracted_text,
    verify_font_table,
    verify_no_bullet_links,
    verify_orphans,
    verify_role_section_assignments,
    verify_skills_density,
)


def make_line(text: str, y: float, x: float = 50, block: int = 0) -> Line:
    words = [
        Word(token, x + index * 10, x + index * 10 + 8)
        for index, token in enumerate(text.split())
    ]
    return Line(text, x, x + max(len(text), 1) * 5, y, y + 10, words, block)


MARKER_X = 61.3
TEXT_X = 79.3


def make_bullet_line(text: str, y: float, *, opens: bool, block: int = 0) -> Line:
    """Build one rendered bullet line.

    `opens` marks the line that carries the bullet marker. Continuation lines
    sit at the hanging indent. Every line here shares one block index on
    purpose: that is what pdftotext actually emits for a run of bullets, and
    it is the condition the old block_index grouping could not see through.
    """
    words: list[Word] = []
    if opens:
        words.append(Word("\u25cf", MARKER_X, MARKER_X + 6))
    for index, token in enumerate(text.split()):
        x = TEXT_X + index * 10
        words.append(Word(token, x, x + 8))
    rendered = f"\u25cf {text}" if opens else text
    xmin = MARKER_X if opens else TEXT_X
    return Line(rendered, xmin, xmin + max(len(rendered), 1) * 5, y, y + 10, words, block)


def write_layout_fixture(
    path: Path,
    *,
    after: str = "0",
    line: str = "240",
    line_rule: str = "auto",
    before: str = "72",
    marker_font: str = "Times New Roman",
    marker_size: str = "22",
    bullet_after: str = "20",
    final_bullet_after: str = "120",
    bullet_line: str = "250",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = f"""\
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:pPr><w:spacing w:after="{after}" w:before="{before}" w:line="{line}" w:lineRule="{line_rule}"/></w:pPr><w:r><w:t>Your Name</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Normal"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr><w:spacing w:after="{bullet_after}" w:line="{bullet_line}" w:lineRule="auto"/><w:ind w:left="720" w:hanging="360"/></w:pPr><w:r><w:t>Built a verified system</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Normal"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr><w:spacing w:after="{final_bullet_after}" w:line="{bullet_line}" w:lineRule="auto"/><w:ind w:left="720" w:hanging="360"/></w:pPr><w:r><w:t>Shipped the final result</w:t></w:r></w:p>
  </w:body>
</w:document>
"""
    styles = """\
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal"><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
</w:styles>
"""
    numbering = f"""\
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="3">
    <w:lvl w:ilvl="0">
      <w:numFmt w:val="bullet"/><w:lvlText w:val="●"/><w:suff w:val="tab"/>
      <w:rPr><w:rFonts w:ascii="{marker_font}" w:hAnsi="{marker_font}" w:eastAsia="{marker_font}" w:cs="{marker_font}"/><w:sz w:val="{marker_size}"/></w:rPr>
      <w:pPr><w:tabs><w:tab w:val="left" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="2"><w:abstractNumId w:val="3"/></w:num>
</w:numbering>
"""
    with ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)
        archive.writestr("word/numbering.xml", numbering)


class OrphanScanTests(unittest.TestCase):
    def test_rejects_orphan_on_a_non_final_bullet_in_one_block(self) -> None:
        """Regression for the 2026-08-09 CCI Full-Stack miss.

        Four bullets share one pdftotext block. The orphan is on the first
        bullet, so grouping by block_index only ever inspected the fourth.
        """
        lines = [
            make_bullet_line("Scaled a voice-agent workspace on Google", 10, opens=True),
            make_bullet_line("Cloud", 22, opens=False),
            make_bullet_line("Cut voice-relay latency in half by", 34, opens=True),
            make_bullet_line("streaming over async Python and WebSockets", 46, opens=False),
        ]
        errors: list[str] = []
        verify_orphans(lines, errors)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("Cloud", errors[0])

    def test_rejects_orphan_on_the_final_bullet(self) -> None:
        lines = [
            make_bullet_line("Parsed and normalized 2 million quotes", 10, opens=True),
            make_bullet_line("with a Java market-data adapter feeding that risk", 22, opens=False),
            make_bullet_line("engine", 34, opens=False),
        ]
        errors: list[str] = []
        verify_orphans(lines, errors)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("engine", errors[0])

    def test_accepts_wrapped_bullets_with_no_lone_trailing_word(self) -> None:
        lines = [
            make_bullet_line("Scaled a voice-agent workspace on Google Cloud from", 10, opens=True),
            make_bullet_line("0 to 500 paid daily active users", 22, opens=False),
            make_bullet_line("Cut voice-relay latency in half by", 34, opens=True),
            make_bullet_line("streaming over async Python and WebSockets", 46, opens=False),
        ]
        errors: list[str] = []
        verify_orphans(lines, errors)
        self.assertEqual(errors, [])

    def test_single_line_bullets_are_never_orphans(self) -> None:
        lines = [
            make_bullet_line("Won 3 sponsor tracks at HackPrinceton", 10, opens=True),
            make_bullet_line("Placed 3rd of 70 projects at WildHacks", 22, opens=True),
        ]
        errors: list[str] = []
        verify_orphans(lines, errors)
        self.assertEqual(errors, [])


    def test_ignores_right_aligned_date_column_fragments(self) -> None:
        """A bare year at the right tab stop is a column artifact, not an orphan."""
        role = make_line("GRPO Post-Training | Llama 3.2 1B, Hugging Face TRL, PyTorch", 10, x=43.3)
        date = Line("2026", 543.3, 565.3, 10, 20, [Word("2026", 543.3, 565.3)], 0)
        body = make_line("Trained a policy on a 1B parameter model", 22, x=43.3)
        # The centered contact line ends past the date tab stop, which is why an
        # exact right-edge match was not enough.
        header = Line("github.com/your-handle", 300.0, 567.9, 0, 8, [Word("github.com/your-handle", 300.0, 567.9)], 1)
        errors: list[str] = []
        verify_orphans([header, role, date, body], errors)
        self.assertEqual(errors, [])

    def test_still_flags_a_left_margin_wrapped_orphan(self) -> None:
        """The coursework-line case: a real wrapped orphan at the left margin."""
        lines = [
            make_line("Relevant coursework: Probability, Statistics, Data Management and", 10, x=43.3),
            make_line("Processing", 22, x=43.3),
            Line("2026", 543.3, 565.3, 10, 20, [Word("2026", 543.3, 565.3)], 0),
        ]
        errors: list[str] = []
        verify_orphans(lines, errors)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("Processing", errors[0])


class ContentStructureTests(unittest.TestCase):
    def test_accepts_standalone_honors_section(self) -> None:
        errors: list[str] = []
        verify_content_structure([make_line("HONORS", 10)], errors)
        self.assertEqual(errors, [])

    def test_rejects_one_bullet_entry(self) -> None:
        lines = [
            make_line("State University | Undergraduate Researcher", 20),
            make_line("July 2024 - August 2024", 20, 400),
            make_line("● Improved SNN training", 30),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertTrue(any("has 1 bullet(s)" in error for error in errors))

    def test_accepts_two_bullet_entry_without_honors(self) -> None:
        lines = [
            make_line("State University | Undergraduate Researcher", 20),
            make_line("July 2024 - August 2024", 20, 400),
            make_line("● Improved SNN training", 30),
            make_line("● Presented results", 40),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertEqual(errors, [])

    def test_rejects_role_header_wrapped_after_pipe(self) -> None:
        lines = [
            make_line(
                "Research Institute for Collaborative Intelligence and "
                "Partner Medical Center | Machine Learning",
                20,
            ),
            make_line("Researcher, Computational Pathology", 32),
            make_line("June 2026 - Present", 32, 400),
            make_line("● Tuned a slide-level classifier", 42),
            make_line("● Documented ablation results", 52),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertTrue(any("wraps" in error for error in errors), errors)

    def test_rejects_role_header_wrapped_before_pipe(self) -> None:
        lines = [
            make_line("Research Institute for Collaborative Intelligence", 20),
            make_line(
                "and Partner Medical Center | Machine Learning Researcher",
                32,
            ),
            make_line("June 2026 - Present", 32, 400),
            make_line("● Tuned a slide-level classifier", 42),
            make_line("● Documented ablation results", 52),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertTrue(any("wraps" in error for error in errors), errors)

    def test_accepts_complete_role_header_and_date_on_one_line(self) -> None:
        lines = [
            make_line(
                "Partner Medical Center, Research Cohort | "
                "Machine Learning Researcher",
                20,
            ),
            make_line("June 2026 - Present", 20, 400),
            make_line("● Tuned a slide-level classifier", 30),
            make_line("● Documented ablation results", 40),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertEqual(errors, [])

    def test_does_not_mistake_indented_markerless_bullet_for_role_wrap(self) -> None:
        lines = [
            make_line("Example Studios | Founding Intern", 20, x=50),
            make_line("April 2026 - Present", 20, x=400),
            make_line("Scaled a production voice system", 32, x=66),
            make_line("Shipped a verified evaluation suite", 44, x=66),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertFalse(any("Role header wraps" in error for error in errors), errors)

    def test_accepts_two_bullet_project_with_single_month_date(self) -> None:
        lines = [
            make_line("GreenChain (HackPrinceton) | Agentic Developer", 20),
            make_line("May 2026", 20, 400),
            make_line("● Built an agent swarm", 30),
            make_line("● Won three sponsor tracks", 40),
        ]
        errors: list[str] = []
        verify_content_structure(lines, errors)
        self.assertEqual(errors, [])

    def test_rejects_generic_project_label(self) -> None:
        errors: list[str] = []
        verify_content_structure(
            [make_line("AI Hackathon Projects | Developer", 10)],
            errors,
        )
        self.assertTrue(any("Generic label detected" in error for error in errors))

    def test_accepts_tailored_experience_section(self) -> None:
        errors: list[str] = []
        verify_content_structure([make_line("ENGINEERING EXPERIENCE", 10)], errors)
        self.assertEqual(errors, [])

    def test_accepts_professional_experience_section(self) -> None:
        errors: list[str] = []
        verify_content_structure(
            [make_line("PROFESSIONAL EXPERIENCE", 10)],
            errors,
        )
        self.assertEqual(errors, [])

    def test_rejects_seven_rendered_skills_lines(self) -> None:
        lines = [make_line("SKILLS", 10)]
        lines.extend(
            make_line(f"Category {index}: Skill", 20 + index * 10)
            for index in range(1, 8)
        )
        lines.append(make_line("ENGINEERING EXPERIENCE", 100))
        errors: list[str] = []
        verify_skills_density(lines, errors)
        self.assertTrue(
            any("uses 7 rendered lines" in error for error in errors)
        )

    def test_accepts_four_categories_across_six_lines(self) -> None:
        lines = [
            make_line("SKILLS", 10),
            make_line("Programming: Python, C++", 20),
            make_line("GPU: CUDA, NCCL", 30),
            make_line("continued GPU skills", 40),
            make_line("Systems: Linux, Docker", 50),
            make_line("continued systems skills", 60),
            make_line("Engineering: Git, CI", 70),
            make_line("ENGINEERING EXPERIENCE", 80),
        ]
        errors: list[str] = []
        result = verify_skills_density(lines, errors)
        self.assertEqual(result, (4, 6))
        self.assertEqual(errors, [])

    def test_rejects_lone_word_orphan_in_skills_section(self) -> None:
        lines = [
            make_line("SKILLS", 10),
            make_line("Business Intelligence: Power BI, Tableau, KPI", 20),
            make_line("dashboards", 30),
            make_line("PROFESSIONAL EXPERIENCE", 40),
        ]
        errors: list[str] = []
        result = verify_skills_density(lines, errors)
        self.assertEqual(result, (1, 2))
        self.assertTrue(
            any("Lone-word orphan in Skills section" in error for error in errors),
            errors,
        )

    def test_accepts_one_category_skills_section_for_gate_b_review(self) -> None:
        lines = [
            make_line("SKILLS", 10),
            make_line("Programming: Python, C++", 20),
            make_line("AWARDS", 30),
            make_line("NSDA National Champion", 40),
        ]
        errors: list[str] = []
        result = verify_skills_density(lines, errors)
        self.assertEqual(result, (1, 1))
        self.assertEqual(errors, [])

    def test_rejects_missing_skills_without_explicit_exception(self) -> None:
        errors: list[str] = []
        result = verify_skills_density([make_line("EDUCATION", 10)], errors)
        self.assertEqual(result, (0, 0))
        self.assertTrue(any("No Skills section" in error for error in errors), errors)

    def test_accepts_missing_skills_with_explicit_exception(self) -> None:
        errors: list[str] = []
        result = verify_skills_density(
            [make_line("EDUCATION", 10)],
            errors,
            allow_missing=True,
        )
        self.assertEqual(result, (0, 0))
        self.assertEqual(errors, [])

    def test_rejects_analysis_bullet_without_downstream_impact(self) -> None:
        errors: list[str] = []
        verify_bullet_impact(
            "● Identified 2 adjacent markets after reviewing 30 competitors\n",
            errors,
        )
        self.assertTrue(any("lacks downstream impact" in error for error in errors))

    def test_rejects_improved_bullet_when_lead_verb_is_only_impact_signal(self) -> None:
        errors: list[str] = []
        verify_bullet_impact(
            "● Improved evaluation criteria through 4 feedback rounds with 3 engineers\n",
            errors,
        )
        self.assertTrue(any("lacks downstream impact" in error for error in errors))

    def test_accepts_analysis_bullet_with_downstream_impact(self) -> None:
        errors: list[str] = []
        verify_bullet_impact(
            "● Identified the highest-return channel, prompting founders to reallocate half of campaign spend\n",
            errors,
        )
        self.assertEqual(errors, [])

    PINNED = {"Example Corp": ["Professional Experience", "Work History"]}

    def test_rejects_pinned_employer_under_the_wrong_section(self) -> None:
        lines = [
            make_line("RESEARCH", 10),
            make_line("Example Corp Technology Team | Research Fellow", 20),
        ]
        errors: list[str] = []
        verify_role_section_assignments(lines, errors, pinned_sections=self.PINNED)
        self.assertTrue(any("Example Corp must appear" in e for e in errors))

    def test_accepts_pinned_employer_under_an_allowed_section(self) -> None:
        lines = [
            make_line("PROFESSIONAL EXPERIENCE", 10),
            make_line("Example Corp Technology Team | Research Fellow", 20),
        ]
        errors: list[str] = []
        verify_role_section_assignments(lines, errors, pinned_sections=self.PINNED)
        self.assertEqual(errors, [])

    def test_no_pinned_sections_means_no_constraint(self) -> None:
        lines = [
            make_line("RESEARCH", 10),
            make_line("Example Corp Technology Team | Research Fellow", 20),
        ]
        errors: list[str] = []
        verify_role_section_assignments(lines, errors, pinned_sections={})
        self.assertEqual(errors, [])


class FontOutputTests(unittest.TestCase):
    def test_accepts_embedded_liberation_serif_fallback(self) -> None:
        font_output = """\
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+LiberationSerif               TrueType          WinAnsi          yes yes yes    120  0
CAAAAA+LiberationSerif-Bold          TrueType          WinAnsi          yes yes yes    115  0
"""
        errors: list[str] = []
        families = verify_font_table(font_output, errors)
        self.assertEqual(
            families,
            ["LiberationSerif", "LiberationSerif-Bold"],
        )
        self.assertEqual(errors, [])

    def test_rejects_unapproved_rendered_body_font(self) -> None:
        font_output = """\
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+ArialMT                       TrueType          WinAnsi          yes yes yes    120  0
"""
        errors: list[str] = []
        verify_font_table(font_output, errors)
        self.assertTrue(any("Unexpected rendered font family" in e for e in errors))
        self.assertTrue(any("No approved rendered body font" in e for e in errors))

    def test_rejects_missing_embedding_or_unicode_mapping(self) -> None:
        font_output = """\
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+TimesNewRomanPSMT             TrueType          WinAnsi          no  no  no     120  0
"""
        errors: list[str] = []
        verify_font_table(font_output, errors)
        self.assertTrue(any("is not embedded" in e for e in errors))
        self.assertTrue(any("has no Unicode mapping" in e for e in errors))

    def test_rejects_dedicated_symbol_font(self) -> None:
        font_output = """\
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+TimesNewRomanPSMT             TrueType          WinAnsi          yes yes yes    120  0
CAAAAA+NotoSansSymbols               TrueType          WinAnsi          yes yes yes    115  0
"""
        errors: list[str] = []
        verify_font_table(font_output, errors)
        self.assertTrue(any("Dedicated symbol fonts are forbidden" in e for e in errors))


class DocxSourceTests(unittest.TestCase):
    def test_normalizes_bullet_and_wrapped_hyphen_for_pair_comparison(self) -> None:
        docx_text = "Cut 30-day retention loss"
        pdf_text = "● Cut 30-\nday retention loss"
        self.assertEqual(
            normalize_artifact_text(docx_text),
            normalize_artifact_text(pdf_text),
        )

    def test_accepts_explicit_single_spaced_body_font_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx)
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertEqual(errors, [])

    def test_rejects_inter_bullet_paragraph_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, bullet_after="40")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(
                any(
                    "must set paragraph spacing after to 20 twips" in e
                    for e in errors
                ),
                errors,
            )

    def test_rejects_final_bullet_without_the_6pt_role_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, final_bullet_after="0")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(
                any(
                    "must set paragraph spacing after to 120 twips" in e
                    for e in errors
                ),
                errors,
            )

    def test_rejects_bullet_without_slightly_looser_line_spacing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, bullet_line="240")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(
                any("250-twip bullet line spacing" in e for e in errors),
                errors,
            )

    def test_rejects_non_bullet_paragraph_carrying_bullet_spacing(self) -> None:
        """Only final bullets get 6pt; a stray gap elsewhere is still a failure."""
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, after="80", before="72")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(
                any("spacing after to 0" in e for e in errors),
                errors,
            )

    def test_rejects_loose_paragraph_spacing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, after="120", line="480", before="200")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(any("spacing after to 0" in e for e in errors))
            self.assertTrue(any("single line spacing of 240" in e for e in errors))
            self.assertTrue(any("maximum is 180" in e for e in errors))

    def test_rejects_symbol_font_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cv" / "Your Name - Example.docx"
            write_layout_fixture(docx, marker_font="Noto Sans Symbols")
            errors: list[str] = []
            verify_docx_layout(docx, errors)
            self.assertTrue(any("must use Times New Roman" in e for e in errors))

    def test_rejects_stale_or_mismatched_artifact_pair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cv_dir = root / "cv"
            cv_dir.mkdir()
            docx = cv_dir / "Your Name - Example.docx"
            pdf = root / "Your Name - Wrong.pdf"
            docx.write_bytes(b"docx")
            pdf.write_bytes(b"pdf")
            os.utime(pdf, (1, 1))
            os.utime(docx, (2, 2))
            errors: list[str] = []
            verify_artifact_pair(pdf, docx, errors)
            self.assertTrue(any("one directory" in e for e in errors))
            self.assertTrue(any("same artifact" in e for e in errors))
            self.assertTrue(any("may be stale" in e for e in errors))


class ExtractedReadingOrderTests(unittest.TestCase):
    VALID_TEXT = """\
Your Name
City, ST // your.email@example.com // (555) 555-5555 // linkedin.com/in/your-handle // github.com/your-handle
EDUCATION
Your University City, ST
Bachelor of Science Expected June 2028
SKILLS
Programming: Python, TypeScript
RELEVANT EXPERIENCE
Example Company | Software Engineer April 2026 - Present
● Built a production system
"""

    def test_accepts_logical_extracted_reading_order(self) -> None:
        errors: list[str] = []
        verify_extracted_text(self.VALID_TEXT, errors)
        self.assertEqual(errors, [])

    def test_rejects_reordered_extracted_sections(self) -> None:
        reordered = self.VALID_TEXT.replace(
            "EDUCATION\nYour University City, ST\n"
            "Bachelor of Science Expected June 2028\nSKILLS",
            "SKILLS\nProgramming: Python, TypeScript\nEDUCATION\n"
            "Your University City, ST\n"
            "Bachelor of Science Expected June 2028",
        ).replace(
            "SKILLS\nProgramming: Python, TypeScript\nProgramming: Python, TypeScript",
            "SKILLS\nProgramming: Python, TypeScript",
        )
        errors: list[str] = []
        verify_extracted_text(reordered, errors)
        self.assertTrue(any("not logical" in e for e in errors))

    def test_rejects_missing_glyph_and_contact_token(self) -> None:
        broken = self.VALID_TEXT.replace("github.com/your-handle", "�")
        errors: list[str] = []
        verify_extracted_text(broken, errors)
        self.assertTrue(any("missing-glyph" in e for e in errors))
        self.assertTrue(any("GITHUB.COM/YOUR-HANDLE" in e for e in errors))


class BulletLinkTests(unittest.TestCase):
    def test_rejects_plaintext_repository_url_inside_bullet(self) -> None:
        text = """\
Your Name
City, ST // github.com/your-handle
PROFESSIONAL EXPERIENCE
Example Company | Research Fellow
● Published the harness at github.com/your-handle/example-project for teammates
"""
        errors: list[str] = []
        verify_no_bullet_links(text, errors)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("github.com/your-handle/example-project", errors[0])

    def test_allows_general_github_profile_in_header(self) -> None:
        text = """\
Your Name
City, ST // github.com/your-handle
PROFESSIONAL EXPERIENCE
Example Company | Research Fellow
● Published an evaluation harness that other researchers ran as a reference
"""
        errors: list[str] = []
        verify_no_bullet_links(text, errors)
        self.assertEqual(errors, [])


class BulletSentenceFormTests(unittest.TestCase):
    def test_rejects_two_sentences_inside_one_bullet(self) -> None:
        text = """\
PROFESSIONAL EXPERIENCE
Example Company | Software Engineer
● Cut feature delivery from 5 days to 2. Coordinated release notes and issue triage
"""
        errors: list[str] = []
        verify_bullet_sentence_form(text, errors)
        self.assertTrue(any("more than one sentence" in error for error in errors))

    def test_rejects_trailing_period(self) -> None:
        text = """\
PROFESSIONAL EXPERIENCE
Example Company | Software Engineer
● Cut feature delivery from 5 days to 2.
"""
        errors: list[str] = []
        verify_bullet_sentence_form(text, errors)
        self.assertTrue(any("trailing period" in error for error in errors))

    def test_accepts_one_clause_with_decimal_and_abbreviation(self) -> None:
        text = """\
PROFESSIONAL EXPERIENCE
Example Company | Software Engineer
● Improved U.S. model accuracy by 2.5% while coordinating release notes
"""
        errors: list[str] = []
        verify_bullet_sentence_form(text, errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
