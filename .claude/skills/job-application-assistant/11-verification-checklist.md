<!-- Moved verbatim out of CLAUDE.md on 2026-09-04. Run this checklist at pipeline step 7 (Verify). Items appended at the end came from AGENTS.md and are Codex-flavoured variants of the same checks. -->

# Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

**Authoritative source:** your school or the career guide's own guide, saved under `documents/references/`, if you have one. The rules below are the common core of those guides.

### Factual accuracy

- [ ] Mandatory job-specific perfect benchmark produced and shown in full before the real resume; benchmark file visibly marked `DO NOT SUBMIT - HYPOTHETICAL BENCHMARK`

- [ ] Complete benchmark-fit the user resume built and shown immediately after the benchmark, before clarification questions; artifact has a distinct filename and is visibly marked `DO NOT SUBMIT - UNVERIFIED CLAIMS`

- [ ] Every plausible metric, technology, responsibility, scope, causal relationship, or outcome introduced in the benchmark-fit draft is tracked as `NEW CLAIM - UNVERIFIED` and later confirmed, corrected, or rejected

- [ ] Line-by-line benchmark correction map completed after both resumes were shown; no benchmark placeholder entered the real resume without confirmation

- [ ] Gate A evidence map completed after the first the user draft; no high-value row remains `UNCHECKED` before exact-file approval or upload

- [ ] Every bullet has an explicit X, Y, and Z with a cited ledger/profile/project source; a technology list or action verb alone does not count as Y

- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements

- [ ] Job titles, dates, company names, and locations are correct

- [ ] Specific institutions, projects, clients, publications, datasets, and awards replace generic labels wherever the real name is known

- [ ] Contact details are correct

- [ ] Header contact line leads with "<City, ST>" and matches the canonical order exactly (city // email // phone // LinkedIn // GitHub)

- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification

### Targeting

- [ ] Skills section is reordered to lead with the role's required stack

- [ ] Every listed skill maps to a bullet, project, coursework item, or approved evidence source

- [ ] Every role-critical skill shown only in Skills triggered an evidence search, resume rewrite, or targeted question; any final `KEYWORD ONLY` item is disclosed and is not counted as qualification coverage

- [ ] First-reader mode is recorded and applied: recruiter-readable purpose for qualifying large-enterprise pipelines, technical density preserved for startups, founder or engineer review, research teams, specialist teams, and uncertain cases

- [ ] For every `RECRUITER-FIRST` resume, make the exact-posting technical-term whitelist before production, then build the full term census from the extracted final-PDF text. Cover acronyms, vendor products, cloud services, frameworks, libraries, models, datasets, protocols, internal names, specialist shorthand, unfamiliar organizations, and every `KEYWORD ONLY` term. Stable standard terms may share a row only when each literal term, action, and justification is shown; every product/subproduct, unexplained acronym, unfamiliar proper noun, internal name, and keyword-only term gets its own row. Every item is marked `KEEP`, `GENERALIZE`, `EXPLAIN`, or `REMOVE`, with final wording shown. `GENERALIZE`, `EXPLAIN`, and `REMOVE` must change the rendered wording; a vendor prefix is not an explanation; a broad posting category does not license a specific product. A missing row, unsupported `KEEP`, or unchanged action blocks Gate B. Apply fixes in one batch, then run one 10-second top-third read and one first-clause-only bullet read.

- [ ] When a posting explicitly values collaboration, code review, mentorship, direction, feedback, or resolving issues, the resume contains a concrete confirmed example or the review report records the gap. **Scan the whole posting, especially the responsibilities/duties block (headed "In this role, you will," "What you'll do," "Responsibilities," or nothing at all), since that is where this language lives rather than in the qualifications list. Record `TRIGGERED` or `NOT TRIGGERED` and quote the deciding line from the posting at hand.**

- [ ] **WORKING-WITH-PEOPLE FLOOR on every `RECRUITER-FIRST` internship resume, whether or not the posting names it.** These reqs are screened by a generalist checking that the intern can be handed to a team without friction, so a posting that stays silent on this is not a posting that does not want it. The page must carry **at least one concrete confirmed example in each of the four rows below**, and one bullet may satisfy more than one row. Record which bullet covers which row, or record the gap. Under `TECHNICAL-READER` this stays conditional on the posting, per the 2026-08-01 rule.

  | Row | What must be shown | Where the evidence comes from |
  |---|---|---|
  | **A. Taking direction** | Working under someone else's brief or supervision, with the outcome | A supervised research cohort, a founder-set scope, a client brief, a manager-assigned project |
  | **B. Receiving criticism and changing the work** | The work materially changed *because of* feedback | Review iterations with named reviewers, a design rejected after user testing, a rewrite that followed a critique |
  | **C. Working with others** | Shared delivery with named mechanics, not co-presence | Pull-request review and CI, cross-functional releases, sprint planning and retrospectives, shared repositories |
  | **D. Explaining technical work to non-technical people** | A specialist result made legible to a non-specialist audience, with what it produced | A demo or deck a non-specialist acted on, stakeholder interviews turned into requirements, model limits explained to subject-matter experts |

  **Row D is the one most often missing and is not satisfied by the term census.** The census governs *how the resume is worded*; row D requires evidence that the user has actually done this translation work in the job. They are different requirements and both apply.

  **No soft-skill label ever satisfies any row.** "Works well with others", "accepts criticism well", "strong communicator", and "team player" remain banned outright. Only a concrete action with an outcome counts.

- [ ] **These four rows are checked per resume, not per bank.** Coverage across a set of production resumes is usually uneven, and a strong example living in `approved-bullets.md` does not mean it survived onto the page currently being built.

- [ ] Skills section fits within 4 categories and 6 rendered body lines, or the exception and cost are disclosed for the user's approval

- [ ] **Top-third keyword coverage.** List every must-have tool, skill, or qualification the posting names, then confirm on the RENDERED page that each one appears in the top third (Skills block plus the leading role's bullets). Name any that appear only below the fold and say why that is acceptable. Reviewers skim the top 20-30% and a human searches the applicant list by literal keyword, so a keyword buried at the bottom is worth less than the same keyword up top. This is placement, not stuffing: nothing gets added that is not already true and evidenced.

- [ ] Experience bullets are reframed to match the job requirements

- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)

- [ ] Nice-to-have requirements are highlighted where there is a match

- [ ] **Graduation year matches the Default Selection Rule** (Candidate Profile → Class standing), and the review gate names which branch fired. Large structured program = June 2028; startup / hackathon / research / fellowship = June 2029; explicit posting gate wins over both

### Career-guide résumé format rules

- [ ] **1 page** for undergrad (the user is undergrad, never 2 pages)

- [ ] **Font:** one of the commonly approved fonts: Arial, Book Antiqua, Calibri, Cambria, Centaur, Century Gothic, Garamond, Helvetica, Palatino Linotype, **Times New Roman**. Same font size throughout body.

- [ ] **Rendered font output:** `pdffonts` reports an embedded Unicode body font from the approved house family: Times New Roman, or the documented LibreOffice PDF fallback Liberation Serif. Any other body-font substitution is a failure

- [ ] **Font size:** 10-12pt body; 14-24pt name

- [ ] **Margins:** the usual guide range is 0.5-1.0 inch. House style is 0.6in left/right, 0.45in top/bottom (top/bottom is slightly under the career guide min, accepted for content density)

- [ ] **Alignment:** body Left-aligned (NOT justified); header (name + contact) centered

- [ ] **Bullets:** every experience has 2-5 bullets, never just 1; bullets are fragments with no trailing period

- [ ] **Project integrity:** every project entry represents one real project or one genuine established program block. No heading combines unrelated projects to save space, borrow a second bullet, or mask a date mismatch

- [ ] **Order:** Reverse chronological by **end date** (most recent first within each section)

- [ ] **Numerals:** Use 6 not "six", 30% not "thirty percent"

- [ ] **No personal pronouns**: no "I", "my", "our". Bullets start with action verbs (Built, Designed, Analyzed, Led, etc.)

- [ ] **No full sentences** in bullets, fragment form is the norm

- [ ] **No template look**, plain Times New Roman in the user's house style, not a fancy template

- [ ] **ATS-safe**, no tables, text boxes, multi-column layout, or info in headers/footers

### Section structure for technical roles

- [ ] **Skills section** placed near the top, **after Education and before Experience** (career-guide technical-role guidance)

- [ ] **Skills section contains technical/language skills ONLY**, not transferable skills like "communication" or "leadership", not honors

- [ ] **Skills section is deliberate:** include only relevant, evidence-backed hard skills. A one-category or one-line Skills section is allowed when the target explicitly values those hard skills and the line adds useful keyword coverage without generic filler. It triggers a verifier warning and requires a Gate B justification. For a nontechnical role whose posting names no hard-skill gate, omit Skills and run the verifier with `--allow-no-skills`; all role-critical evidence must still appear in bullets. Two to four coherent categories remain the normal shape for technical roles with broader stack requirements.

- [ ] **Honors/awards placement is intentional:** distinctions are folded into the related entry by default; any standalone Honors/Awards section is compact, non-duplicative, role-relevant, and justified in the Gate B review

- [ ] **Header centered**; education uses university (bold) + location (regular) on one line, degree+grad date on one line, GPA on its own line; coursework line omitted unless really necessary for the role

- [ ] **No per-class letter grades** (e.g., "(A)") next to any course in the resume or cover letter; only the cumulative GPA appears

- [ ] **GitHub / portfolio link** in the header (per career-guide technical-role guidance)

- [ ] **Bullet formula:** every bullet follows X-Y-Z: result or accomplishment first, strongest honest measure or concrete proof second, and named method last. Include specific proper nouns wherever true and relevant. Never invent a metric.

### Cover letter format rules

- [ ] **Same header as CV** for cohesive brand

- [ ] **3-5 paragraphs**, business letter format, 1 page

- [ ] **Salutation:** named recruiter if known, else "Recruiting Team" or "Hiring Manager". **Avoid "To whom it may concern"**

- [ ] **Opening paragraph:** introduce self, state why writing, how learned about position, 2-3 sentences on interest in org

- [ ] **Middle paragraphs:** 2-3 experiences (not all résumé bullets), with specific examples of skills the employer is seeking

- [ ] **Closing paragraph:** thank for consideration, request to discuss

- [ ] **No contact info in signature** (it's already in the header)

### Quality

- [ ] Document validates (run the docx skill's `validate.py`)

- [ ] No spelling or grammar errors

- [ ] No em-dashes (use commas, periods, or restructure)

- [ ] Agentic coding / AI tooling references name the specific agent that fits the project and employer (not a generic phrase), and avoid naming a competitor's tool on that competitor's application

- [ ] Tone consistent between resume and cover letter

- [ ] House Style Spec matched exactly (font, sizes, header rule, spacing, margins, right-tab dates)

### Adversarial recruiter audit (run before the review gate)
Everything above checks whether the document is correct. This step checks whether it is *persuasive*, by attacking it instead of proofreading it. Run it against the actual posting after the document passes the checks above, and report the findings to the user alongside the resume.

Read the finished resume back as a hostile reader and answer:

- [ ] **Missing keywords:** which terms appear in the posting but nowhere in the resume? For each, say whether the user has real experience that could honestly surface it (then surface it) or whether it is a true gap (then say so).

- [ ] **Red flags in a 10-second skim:** what would a recruiter notice and hold against them reading only the top third? Common ones: an unexplained gap, a title that undersells the actual scope, a lead bullet with no number, a stack mismatch with the posting.

- [ ] **Skipped sections:** which blocks would get skipped entirely on a first scroll, and why? Anything that would get skipped is either rewritten or cut, since a section nobody reads is costing line count on a one-page resume.

- [ ] **Weak bullet openers:** any bullet that fails to lead with the result, prove it with an honest measure or verifiable artifact, and name the method. Rewrite every bullet into X-Y-Z, and replace generic nouns with true specific technologies, workflows, frameworks, datasets, institutions, clients, or awards.

- [ ] **Page-value loss:** which current, confirmed outcome is stronger than material that made the page? Cut generic keywords, repeated stack lists, or older content before omitting stronger current evidence.

- [ ] **Generic labels:** which entries hide a known institution, project, client, publication, system, dataset, or award behind a category label? Replace each with the real proper noun.

- [ ] **Same-word repetition:** read the page as one document, not as a list of bullets. List every content word appearing 3+ times and every bullet lead verb repeating, then vary them. `cv/verify_resume_layout.py` emits these as `WARN lexical repetition` and every warning needs a disposition here. Domain nouns the posting itself uses may repeat; **lead verbs may not**. Changing a lead verb without touching facts, numbers, tools, or causality is not a new claim and needs no re-confirmation (see the Learning Loop). **Why this row exists:** the Western Digital draft used "Cut" 9 times and still passed Gate A, Gate B, this audit, and the layout verifier, because every gate checked bullets individually or the page geometrically and nothing read the page's language as a whole. The underlying cause is that nearly every confirmed metric in the bank is a *reduction*, so the bank's approved wordings independently converge on the same verb.

Rules for this step:

- **Do not produce a match score.** A number out of 100 looks empirical but no model knows what a given company's ATS does, so a score invents precision that does not exist. Name the specific findings instead.

- The point is to catch what the correctness checks cannot: a resume that is accurate, well-formatted, and still gets passed over.

### Exact packet consistency gate (MANDATORY before submission)
Complete Gate C in `.claude/skills/job-application-assistant/09-resume-evidence-audit.md` against the exact PDF attached to the application, every visible or serialized form field, and the submitted transcript.

- [ ] Resume, form, and transcript agree on employer/institution names, titles, dates, locations, degree, graduation year, GPA, metrics, and technologies

- [ ] Hackathon, class project, research, and startup relationships are described without inflated titles or omitted context

- [ ] Every intentional difference is listed for the user as a `PACKET DIFFERENCE` with its reason and risk

- [ ] the user's approval applies to this exact PDF and disclosed differences; later contradictory form edits require new approval

- [ ] Tracker records the exact uploaded resume path, account email, graduation year, and approved packet differences

- [ ] Submission remains blocked while any unexplained contradiction exists

### Compiled PDF verification (MANDATORY - never skip)
The.docx MUST be converted to PDF and visually inspected via the Read tool on the PDF output. "Looks fine in the source" is not acceptable. Build to a canonical path under `cv/`, render that exact DOCX into a fresh task-local directory, copy the exact reviewed PDF back to the matching canonical `cv/` filename, inspect font families and Unicode mappings with `pdffonts`, inspect logical extraction with `pdftotext -raw`, then render to PNG with `pdftoppm` for the visual check and run `cv/verify_resume_layout.py <rendered.pdf> --docx <source.docx>`. The verifier checks canonical path/name/freshness, normalized PDF-to-DOCX text identity, explicit 240-twip body and 250-twip bullet line spacing, marker font and geometry, page geometry, rendered font output, font embedding, Unicode mappings, and extracted reading order. Do not skip it in favor of eyeballing alone. Iterate until these all pass:

- [ ] **Resume is exactly 1 page**

- [ ] **Cover letter is exactly 1 page**, signature block fits with the body

- [ ] **No orphaned section headings**, a header must never sit alone at the bottom of a page with its content on the next

- [ ] **No orphaned words on ANY document:** scan every wrapped bullet and paragraph in the rendered PDF for a lone trailing word sitting on its own line (e.g. "conversations", "modes", "tools") and reword until each wrapped line carries at least two words. This applies to every resume and cover letter, not just hackathon applications. **`cv/verify_resume_layout.py` now catches these (fixed 2026-08-09).** The old scan grouped rendered lines by pdftotext's `block_index`, and pdftotext merges a whole run of consecutive bullets into one block, so it only ever inspected the *last* bullet of the run and every earlier bullet's orphan was invisible. It now regroups bullets geometrically (marker line opens a group, hanging-indent lines continue it) and ignores right-aligned date-column fragments. Two orphans on the CCI Full-Stack draft ("Cloud", "engine") were missed by the old version and are covered by regression tests in `cv/test_verify_resume_layout.py`. **Still check the rendered PNG as well;** the verifier is now a real gate, not a substitute for looking. Note also that the committed test suite had been failing (12 of 24 errors, `make_line` missing `block_index`) and was fixed in the same pass, so run `python3 -m unittest cv.test_verify_resume_layout` before trusting any verifier change

- [ ] Section rules have clear breathing room before the next line; nothing collides

- [ ] **No "I"/"my"/"our" in resume bullets** (programmatically check before declaring done)

- [ ] `cv/verify_resume_layout.py <pdf> --docx <docx>` reports PASS on the canonical pair, including source-path/freshness, paragraph-spacing, marker-font, per-entry bullet-count, rendered-font, font-embedding, Unicode-mapping, and extracted-reading-order checks

- [ ] **Extracted reading order passes:** `pdftotext -raw <pdf> -` returns selectable text in logical order from name and contact information through Education, Skills, and the experience sections, with no missing glyphs or reordered columns

- [ ] **Post-render content reconciliation passes:** list the 3 strongest omitted confirmed outcomes, or all if fewer, and explain why each loses to retained content. Restore stronger evidence before accepting unused space

- [ ] **Bottom density passes:** final content ends 28-72 points above the page bottom; no visibly empty lower quarter

- [ ] **Bullets pass in both PDF and Finder Quick Look:** marker is the solid circle `●` in Times New Roman at body size; no dedicated symbol font is embedded; one bullet-marker x-position, one text x-position, and every wrapped line aligns exactly under the first line's text

- [ ] **Dates pass:** each role uses a separate right tab and date run, every date stays on the role line, and every date ends at the same right edge

- [ ] **Reference comparison passes:** inspect side by side against a current approved resume at the same resolution for margins, section rhythm, bullet geometry, date alignment, and bottom-page density
