# CV Templates and Tailoring Guide

## Formatting authority: CLAUDE.md House Style Spec and the DOCX builder

The **House Style Spec in `10-house-style.md` is the complete formatting specification**: font, sizes, centered header, education layout, section order, Skills shape, one-line role headers, bullet marker and geometry, the 2-rendered-line bullet cap, spacing, margins (0.6in left/right, 0.45in top/bottom), and the no-LaTeX rule. This file does not restate it; where anything here differs from CLAUDE.md, CLAUDE.md wins.

Build every resume as a `.docx` with a per-company Node script `cv/build_<company>.js` that uses the shared library `cv/build_epsilon_lib.js` (`header`, `heading`, `eduSchool`, `eduDegree`, `skill`, `roleLine`, `bullet(text, { final: true })` on the last bullet of each entry, `warningBanner` for non-submittable drafts, `write`). Copy the closest prior builder as the starting point and recheck every fact on it, starting with the GPA line, before rendering. Keep one builder as the current visual authority and label its output DO NOT SUBMIT if it exists only to demonstrate format. Render the DOCX with LibreOffice into a task-local directory, copy the exact PDF back to `cv/`, and run `cv/verify_resume_layout.py <pdf> --docx <docx>`; it enforces the spacing, marker, geometry, font, orphan, Skills-density, bullet-count, and reading-order rules. **Do not generate LaTeX.** The legacy `.tex` templates and compile loops are retired.

**When the page will not fit, cut content or cut an entry** (CLAUDE.md). Do not combine unrelated projects, do not compress an entry into a line, do not drop the Languages line to save space, and never shrink margins or spacing. Cut by the Relevance-Weighted Cutting rules at the end of this file.

**Authoritative external source:** your school or career center's own résumé guide, saved under `documents/references/` and named in `03-writing-style.md`. Most of them say the same thing about templates: avoid them, because they are overused, hard to customize, and often upload badly to employer portals. The house style is exactly that clean, ATS-friendly, plain-serif document. When in doubt, defer to the House Style Spec first, then the guide.

## Career-guide rules not restated in the House Style Spec

Every bullet follows the X-Y-Z shape in the House Style Spec (result, honest measure or artifact, method). The common career-guide formula, action verb + task + purpose/result, is the same idea at a lower resolution:

- *Bad:* "I worked as a server at the Main Street Café"
- *Good:* "Coordinated dinner service for fast-paced restaurant that served up to 500 customers a night"

Use a career-guide action verb list: Analytical (Analyzed, Conducted, Designed, Evaluated, Modeled, Solved, Synthesized…), Communication (Authored, Collaborated, Presented…), Leadership (Led, Managed, Spearheaded, Streamlined…), Quantitative (Allocated, Budgeted, Forecasted, Reduced…), Technical (Constructed, Designed, Developed, Engineered, Programmed, Prototyped…).

## Profile Statements / Summary

**A summary statement at the top is usually not required.** For a student or early-career candidate the Education and Skills sections do that job, and most career guides reserve a "Professional Summary" for experienced candidates. Default to **no summary paragraph**: go straight from header to Education.

If a specific recruiter pipeline expects a summary (rare for undergrads), keep it to 2-3 lines max.

## Section-by-Section Tailoring

### Education
- School name, location, degree, and expected graduation date in the exact three-line layout the House Style Spec gives; never print a graduation year without applying the Default Selection Rule in CLAUDE.md and naming the branch that fired
- GPA on its own italic line (`GPA: X.XX/4.0`), taken from the candidate profile
- **Coursework line: omit by default.** Include a short, role-relevant line only when it is really necessary (a finance, quant, or named-major gate where the user lacks direct experience and the coursework supplies a needed signal). Never annotate courses with letter grades

### Skills (technical roles only, placed after Education)
- Technical/language only. **No** "communication," "leadership," "teamwork."
- Suggested sub-categories: Programming, Quantitative & ML, Systems, Languages. The `Languages:` line is printed whenever a language the user speaks is plausibly valuable to that employer (regional footprint, global scope, bilingual users), per the House Style Spec; it is not dropped to save space
- List proficiency level if helpful (advanced, proficient, intermediate, beginner)

### Professional Experience, Projects, and Research
- Reverse chronological by **end date**
- 2-5 bullets each
- Never combine unrelated projects merely to save a role line or satisfy the 2-bullet minimum. Use a shared entry only for a genuine established program block whose heading, role, and date range accurately apply to every included project. Otherwise keep separate 2-5 bullet entries or cut the weaker project.
- Expand opaque event and program brands into recruiter-readable names. Use `Yale Hackathon`, not `YHack`, on resumes unless the user explicitly requests the abbreviation for a specific audience.
- Bullet structure: action verb + task + purpose/result
- Quantify wherever possible (90%, 86%, $20k, 65-person, 1,000+)
- Mention the specific tools actually used (languages, libraries, platforms, methods)
- Prefer **Professional Experience** or **Work History** for employment, **Projects** for named builds, and **Research** for research roles. Do not force projects or research under Professional Experience. Clear tailored headings such as **Relevant Experience**, **Research Experience**, **Engineering Experience**, **Technical Experience**, or **Project Experience** are allowed when they organize the evidence more accurately for the target role.
- A paid industry role with "Research" in the title still belongs under **Professional Experience** or **Work History**, not under Research. Record per-role placement decisions like this in the candidate profile once the user settles them.

### Leadership
- 2-5 bullets per role; same action-verb structure
- Quantify scope (budget size, headcount, awards won)

### Honors
- Fold each relevant honor into the entry that earned it by default
- A compact standalone Honors or Awards section is allowed when it contains unusually strong, role-relevant distinctions, does not duplicate another entry, and earns its page space

### Interests (optional)
- Optional; include only if specific, authentic, and appropriate
- Include only when it is useful for the role and stronger evidence does not need the space
- If an application explicitly requires an Interests section, use that exact heading even when the section is one line. Do not rename it `Additional` or move an academic fact such as a minor into it merely to make the section look fuller. Keep academic facts in Education.

## Page Budget, Hard 1-Page Limit

| Section | Max budget |
|---------|-----------|
| Header | 2 lines (name + contact) |
| Education | 1 entry, 3-4 lines |
| Skills | Maximum 4 categories and 6 rendered lines (no bullet markers; bold category labels) |
| Most recent project / role | 3-4 bullets |
| Previous project / role | 2-5 bullets |
| Older role | 2-5 bullets or omit the role |
| Leadership | 1-2 entries, 2-5 bullets each |
| Honors | Fold into related entries by default; allow a compact standalone section when it is stronger and non-duplicative |

**If in doubt, cut rather than squeeze.** Clean readable spacing beats cramped content.

## Relevance-Weighted Cutting (when 2-page overflow happens)

Score each candidate line by:
1. **Relevance to THIS posting**, does it hit a named tool/keyword/responsibility?
2. **Uniqueness**, only place this claim appears?
3. **Narrative load**, does the cover letter lean on it?

Cut lowest-total-score first, regardless of section. Older "high-priority" sections lose to recent role bullets that don't match the posting.


## Reusable section shapes by role family

Empty until the user has verified resumes to learn from. Each time a resume passes Gate B, add one entry here so the next posting in the same family starts from a known-good shape instead of a blank page. Use this format:

- **Reusable section shape for `<ROLE FAMILY>` (`RECRUITER-FIRST` or `TECHNICAL-READER`, verified one page at NN pt bottom whitespace):** Education, with or without a coursework line and why -> Skills, how many categories across how many rendered lines, in order -> the experience sections in order with the bullet count per entry -> total bullets and entries. Then name **the two or three bullets that carry the page** and which stated qualification each one answers, the strongest evidence deliberately **omitted** and what it lost to, and the builder scripts under `cv/`.

Two things make these entries worth writing: the rendered bottom-whitespace figure, which tells the next run how much room the shape actually leaves, and the named omission, which stops a later run from re-litigating a decision that was already made on the merits.