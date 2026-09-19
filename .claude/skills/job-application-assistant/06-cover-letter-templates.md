# Cover Letter Templates and Tailoring Guide

**Authoritative source:** your school or the career guide's own guide, saved under `documents/references/`, if you have one. The rules below are the common core of those guides.

## Builder: DOCX in the resume house style (matches CV)

The cover letter uses the **same** Times New Roman setup as the CV, with the **same header**. Use the same header on both the cover letter and the résumé for a cohesive, polished look.

**Output file:** `cover_letters/<Your Name> - <Company> Cover Letter.docx`, rendered to PDF with LibreOffice (`soffice --headless --convert-to pdf`) and inspected from a `pdftoppm` PNG.
**Builder:** a per-company Node script `cover_letters/build_<company>_cl.js`, written with the `docx` library and copied from the most recent `cover_letters/build_*_cl.js`. The resume builders share `cv/build_epsilon_lib.js`; the cover-letter scripts carry the same header constants (Times New Roman, name 20pt, contact line 11pt in the canonical order leading with `<City, ST>`, thin black bottom rule) so the two headers render identically.
**Margins:** 0.6in left and right, 0.45in top and bottom, the resume's exact margins. Do not widen them (CLAUDE.md House Style Spec).
**Do not generate LaTeX.** The workflow is DOCX only; the legacy LaTeX cover-letter template and its class file are retired and are not in the tree.

## Document Structure

Header (centered name, centered contact line, then the thin black horizontal rule), followed by:

- [Month Day, Year]
- [Recipient: Recruiter name / "Hiring Team" / "Recruiting Team"]
- Dear [Hiring Team / Recipient Name],
- [Opening paragraph: state role, why writing, how learned of position, 2-3 sentences on interest in org]
- [Middle paragraph 1: most relevant experience, quantified outcome, transferable lesson]
- [Middle paragraph 2: second relevant experience or skill cluster, with named tools]
- [Closing paragraph: thanks for consideration, requests opportunity to discuss]
- Sincerely,
- <Your Name>

## Cover Letter Rules

| Rule | Value |
|------|-------|
| Header | **Must match CV exactly** |
| Length | 1 page, **3-5 paragraphs** |
| Format | Business letter |
| Tone | Detailed, tailored, concise; does not need to fill the page |
| Salutation | Named recruiter if known, else "Recruiting Team" or "Hiring Manager"; **avoid "To whom it may concern"** |
| Body content | 2-3 selected experiences (not all CV bullets), go *deeper* than CV bullets |
| Signature | **No contact info** (already in the header) |
| Personal pronouns | Allowed (cover letters use first person naturally) |

## Four-Paragraph Spine

### Opening paragraph (introduce yourself)

State role + why writing + how you learned about it + 2-3 sentences on interest in the organization. End with a sentence that "grabs the reviewer's attention and encourages them to continue reading."

Example pattern:
> I am writing to apply for the [Role] at [Company]. The intersection of [theme A], [theme B], and [theme C] is the exact intersection I have been preparing for, and I would be excited to contribute that work at [Company].

### Middle paragraph 1: Differentiator

Lead with the most relevant experience for this role. Quantify the outcome. State the transferable lesson.

Do not repeat the résumé. Select two or three experiences that show the positive impact of the relevant skills.

### Middle paragraph 2: Bridge (technical + ops/business if applicable)

Connect a second experience or skill cluster to specific requirements from the posting. Name the specific tools used.

Optional: combine this into Middle 1 if the role is narrowly technical (quant, AI research) and the second experience is structurally similar.

### Closing paragraph (express thanks and request to discuss)

Express interest in the environment or specific aspect of the role. Single closing sentence: "Thank you for considering my application. I would welcome the opportunity to discuss how I can contribute to the team."

## Tailoring Guidelines

### Salutation

- Known recruiter: "Dear [First Last],", preferred
- Team-level: "Dear [Company Name] Hiring Team," or "Dear Recruiting Team,"
- Generic: "Dear Hiring Manager," (use only when no other option available)
- **Never:** "To whom it may concern,"

### Length

- Hard 1-page limit
- Detailed, tailored, concise storytelling is what an employer wants to see. The letter does not need to fill a whole page.
- Word budget: **250-350 words of body text**. Going above 350 risks overflow.

### Bullet Lists (avoid by default)

Career-guide example letters use straight paragraphs, not bullet lists. **Default to paragraphs.**

If a bullet list is truly clearer for a specific role:
- 3-5 bullets max
- Use bold category labels

### Header consistency

The rendered header on the cover letter and CV must match, not merely name the same contact fields. The canonical header is Times New Roman, with the user's name in 20-point regular weight and the contact line in 11-point regular weight. The email remains black plain text. LinkedIn and GitHub are blue and underlined. Both lines are centered using the same 0.6-inch side margins. The cover-letter header ends with a 0.4-point horizontal rule spanning the full text width.

Any change to one header means updating the other. After generating both PDFs, run the blocking parity check:

```bash
python3 cv/verify_application_header.py "cv/<Your Name> - <Company>.pdf" "cover_letters/<Your Name> - <Company> Cover Letter.pdf"
```

The check must pass on font family, font size, weight, text, width, centering, vertical position, and the required horizontal rule before review or upload.

## Patterns Observed in Past Applications

Empty until the user has approved cover letters to learn from. As they accumulate, record here the spine that keeps working (opening shape, differentiator paragraph, cross-functional bridge paragraph, leadership-scale paragraph, closing shape), the **reusable building blocks** with a note to rotate them rather than repeat them inside one hiring ecosystem, and **what to vary per company**: the opener's framing phrase, the single shipped example in the bridge paragraph, and which experience leads for each role family.

### AI tooling references

Per the `CLAUDE.md` rule, when mentioning agentic coding or AI tooling, **name the specific agent that actually fits the project and the employer**, never a generic phrase like "AI coding agents." Default to the tool the user genuinely used most for that work. **Do not name a competitor's tool on an application to that competitor**; pick the neutral or matching option instead. The shape that works: *"I used <agent> as a coding agent to rapidly prototype the system, generate evaluation scripts, and automate experimentation across large batches of prompts."*

### What to vary per company

- The framing phrase in the opener
- The single shipped example in the bridge paragraph
- Which experience leads, chosen by role family

## Build-and-Inspect Loop (MANDATORY)

1. Run the builder (`node cover_letters/build_<company>_cl.js` with `CODEX_NODE_MODULES` set), then render the DOCX to PDF with LibreOffice
2. Page count must be exactly 1
3. Read the PDF via the Read tool (or the `pdftoppm` PNG at 100% zoom), visually inspect:
   - `cv/verify_application_header.py` passes against the exact CV PDF
   - Header matches CV visually, including weight, font, size, contact colors, underlines, spacing, and the required full-width rule
   - Date, recipient, salutation correctly formatted
   - Paragraphs have clear breaks
   - No bullet lists unless intentional
   - Closing block ("Sincerely," + "<Your Name>") fits on page 1 with visible white space below
   - No orphaned words (a lone trailing word on its own line) and no em-dashes

### Common pitfalls

**Problem: body spills to page 2**
1. Trim the middle paragraphs (combine sentences, drop weakest example)
2. Combine thanks + closing into one paragraph
3. Never widen or narrow the margins; they are fixed at the resume's 0.6in / 0.45in

**Problem: thanks-paragraph or signature on page 2**
- Almost always means the body is 50-100 words too long. Trim the body; do not squeeze the paragraph spacing around the signature.

## Submission Guidelines

- Submit only the documents the employer requests
- Export as PDF (the LibreOffice render of the DOCX)
- Name files clearly: "<Your Name> - CV.pdf" and "<Your Name> - Cover Letter.pdf"
- Follow all employer instructions regarding anonymity or specific materials
- **Generate a cover letter only when a cover-letter field exists on the form, the posting asks for one, or the user requests one** (CLAUDE.md: "Cover letter only if needed, do NOT generate by default"). Career-guide advice to submit an optional letter anyway does not override this; an optional field with no request from the user stays empty.
