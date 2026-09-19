# Resume Evidence and Submission Audit

This is a mandatory blocking workflow for every tailored resume. It exists to prevent a resume from being accurate and keyword-matched while still omitting the user's strongest evidence, using generic labels, or contradicting the application form or transcript.

Do not waive a gate because a deadline is close. Do not call a resume final, optimized, maximized, verified, or ready to submit until Gate 0 and Gates A, B, and C pass. Passing page count or layout checks alone is not Gate B.

## Gate 0: Perfect benchmark and benchmark-fit the user resume, before clarification

For every job application, first build a complete one-page resume showing what the strongest plausible top candidate would submit for that exact posting.

**Federal exception:** a resume for a federal application through USAJOBS is built to the two-page federal limit instead of one, with month-and-year dates and hours per week on every work entry, and is verified with `cv/verify_resume_layout.py --pages 2`; every other gate here is unchanged. Source and the verbatim requirement: `documents/playbook/2026-09-01 - usajobs-federal-resume-requirements.md`.

Rules:

- This gate is unconditional. The user does not need to ask for a perfect resume.
- Research the full posting first, then build the benchmark before drafting or editing the user's real resume.
- Present the entire benchmark resume first. Do not interleave corrections, caveats, or evidence warnings inside the first presentation.
- Visibly label the artifact and filename `DO NOT SUBMIT - HYPOTHETICAL BENCHMARK`.
- The benchmark should optimize role selection, bullet order, X-Y-Z evidence, skills coverage, ATS language, and one-page density for the exact posting. Do not weaken it to match the current evidence files.
- Plausible hypothetical metrics, tasks, responsibilities, and tools may appear in this benchmark as reference placeholders. They are not claims about the user and must never be treated as approved evidence merely because they appeared in the benchmark.
- Never upload, attach, or submit a benchmark. Any file whose name or contents contain `DO NOT SUBMIT` or `HYPOTHETICAL BENCHMARK` is categorically ineligible for upload.

### Required benchmark-fit the user resume

Immediately after showing the complete benchmark, build and show a complete one-page the user-specific resume that fits the benchmark as closely as plausibly possible. The benchmark is the default design target for role selection, section order, bullet emphasis, skills coverage, ATS language, and page density. Because the user's evidence bank may be incomplete, this first the user-specific draft may introduce plausible new metrics, technologies, responsibilities, scope, and outcomes as claim hypotheses. Do not pause for clarification questions or present the correction map between the benchmark and this the user-specific resume.

Rules:

- Search the master bullet bank, approved-claims ledger, candidate profile, project evidence, and other permitted application materials first. Use the strongest existing evidence wherever it already supports the benchmark signal.
- Match the benchmark's strategy and strength by default. When the existing files do not fully support a strong benchmark signal, write the strongest plausible the user-specific claim for the closest real role or project instead of silently omitting the signal.
- For Gate 0 hypothesis generation, default every unresolved high-value posting signal that plausibly maps to a real the user role or project to **YES**. Supply reasonable, specific metrics, tools, scope, responsibilities, causal relationships, and outcomes in polished bullet form, then mark every invented element `NEW CLAIM - UNVERIFIED`. Do not defer a role-critical signal as an omission, a later question, or a vague placeholder merely because the evidence bank is incomplete. Known confirmed falsehoods remain excluded.
- Plausible claim hypotheses may include new numbers, technologies, responsibilities, causal relationships, scale, and outcomes that are reasonable for the user's documented role but are not yet confirmed. Write them in polished resume form so the user can evaluate the strongest version, then track every one as `NEW CLAIM - UNVERIFIED` in the companion correction map.
- Save this artifact separately as `cv/<Your Name> - <Company> - Benchmark-Fit Draft - DO NOT SUBMIT.docx` and a matching PDF. Visibly label the document `DO NOT SUBMIT - UNVERIFIED CLAIMS`. It must never overwrite or share the production filename.
- The companion map must identify each unverified claim, the role or project it belongs to, why it is plausible, the exact confirmation needed, and its final disposition as `CONFIRMED`, `CORRECTED`, or `REJECTED`.
- The companion map must also record a direct confirmation source for every final disposition. Acceptable provenance is a dated direct response from the user that addresses the exact claim or a uniquely identified approved-bullets entry. An agent-authored report, correction map, or status label is not provenance.
- Previously approved evidence stays approved and should not be re-asked. It covers a new hypothesis only when it explicitly supports every added number, tool, responsibility, causal link, scope, and outcome. Ask only about the genuinely new details.
- Record the SHA-256 of the benchmark-fit draft in the companion map. Run `python3 cv/verify_gate0_provenance.py <companion-map> --draft <benchmark-fit-draft>` before Gate A or Gate B can pass. Any unresolved row, missing confirmation source, or draft-hash mismatch is blocking.
- Creating or changing a benchmark-fit draft invalidates Gate A, Gate B, and any prior exact-PDF approval, including when the filename stays the same. A fast path for an existing posting requires a passing provenance check and a production PDF whose SHA-256 matches the user's approved hash.
- The existence of an `UNCHECKED` item does not block building or showing this first complete the user-specific resume. It blocks calling the resume final, passing Gate A, seeking exact-file approval, uploading, or submitting until the item is resolved, removed, or honestly classified.
- The first the user-specific resume is a complete benchmark-fit draft, not a loose outline, evidence table, or partial set of bullets.
- Only after both complete resumes have been built, rendered, visually inspected, and shown in full should the correction map and targeted clarification questions begin. Do not return to the user between the benchmark and benchmark-fit draft.

Then create a line-by-line correction map:

| Benchmark claim or skill | Closest real role or project | Source | Status | Correction needed | Draft disposition |
| --- | --- | --- | --- | --- | --- |

- Use only `CONFIRMED`, `UNMEASURED`, `TRUE GAP`, or `UNCHECKED` in the Status column. For claims introduced in the benchmark-fit draft, record the final Draft disposition as `CONFIRMED AS WRITTEN`, `CORRECTED`, or `REJECTED` after clarification.
- Ask 2-4 targeted questions per round for high-value `UNCHECKED` items. The user's files often under-document work, so investigate before marking a `TRUE GAP`.

- **🚨 ASK WHAT THE USER DID, NOT WHICH TOOL THEY USED.** A question that names a product can only be answered yes or no, so a `no` ends the thread and the hypothesis dies with nothing learned. A question about the work itself keeps the evidence. **Ask about the activity, the artifact, the person on the other end, or the outcome, in the words they would use to describe their own day.** Not `did you use <tool>` but `how did that get updated and reviewed`. Not `is there a data catalog` but `if a new collaborator needed to find the right table, what did they look at`. A question about a storage format is worth nothing at all, because the format is invisible to the person doing the work and no honest answer can come from them. **A posting term that names an implementation detail the user would have no reason to notice is not a Gate 0 hypothesis; it is a TRUE GAP, and it should be recorded as one without a question.** This does not weaken the rule that a posting's named terms are the first source of hypotheses: it changes the wording of the question, not whether the hypothesis is written.
- Benchmark ideas may transfer into the separately labeled benchmark-fit the user draft as `NEW CLAIM - UNVERIFIED` hypotheses. Nothing unverified may transfer into the production resume. Confirmed new facts enter the Learning Loop.

## First-reader mode, decide during research

Choose and record one mode for the application before Gate A:

- `RECRUITER-FIRST` means the first reader is a generalist screen: centralized recruiting, campus hiring, a broad multi-team requisition, or a recruiter matching to teams later. `TECHNICAL-READER` means an engineer, founder, researcher, or specialist team reads the resume first. **Which one applies is decided only by the DEFAULT SELECTION RULE below**; walk its tests in order and stop at the first that fires. When uncertain, choose `TECHNICAL-READER`.

**🚨 A REQUIREMENT THE POSTING NAMES BY NAME MUST BECOME A GATE 0 HYPOTHESIS, NEVER A BARE SKILLS KEYWORD.** When the posting names a specific tool, document type, or qualification and no confirmed evidence exists, write the strongest plausible bullet for it in the benchmark-fit draft and track it as `NEW CLAIM - UNVERIFIED`, exactly as for any other gap. Do not put the term in Skills and plan to disclose it at the review gate. **The failure mode:** the posting names a plain requirement such as `Word` or `Excel`, every hypothesis gets written for the impressive technical requirements, and the plain one lands in Skills unbacked and surfaces only as a Gate B disclosure. One question usually produces a real artifact and a shippable bullet instead. **The posting's own named terms are the first place hypotheses come from, ahead of the discipline list.**

### DEFAULT SELECTION RULE for first-reader mode

Stop re-deriving this per application. **Walk the tests in order and stop at the first one that fires.** Name the firing test and the deciding evidence in the review-gate report. The user can always override.

1. **A named human already routes the application → `TECHNICAL-READER`.** A referral into the team, a founder or engineer who invited the application, a hiring manager the user has spoken to, or a live process where they already passed a technical assessment. The generalist screen has been bypassed, so density is safe regardless of company size. This test outranks every test below it, including company size.
2. **The posting itself is written by and for engineers → `TECHNICAL-READER`.** The signal is the posting naming specific versions, architectures, internal systems, or tradeoffs ("gRPC", "PyTorch 2.x", "we run a monorepo", "you'll own the inference path"). A posting that can name its own stack that precisely was written by someone who will read the resume.
3. **The posting is written in generic competency language → `RECRUITER-FIRST`.** The signal is the inverse: broad requirement families with no versions or systems ("experience with cloud technologies", "strong programming fundamentals", "familiarity with machine learning"), boilerplate shared across many reqs at the same employer, or one requisition spanning several teams, locations, or class years. Vague posting language is direct evidence of a non-specialist writer and therefore a non-specialist first reader.
4. **Structured campus, early-careers, or rotational program at an employer over roughly 5,000 people → `RECRUITER-FIRST`.** Centralized recruiting owns the first pass and matches to teams later. Covers big tech early-careers portals, banks, consultancies, defense primes, and large public companies.
5. **Team size, where it is knowable → follow it.** A posting naming a specific team of roughly 20 or fewer, or a company under roughly 200 people, means the reader is almost certainly on that team: `TECHNICAL-READER`. A req that never names a team at a large employer means it is going into a pool: `RECRUITER-FIRST`.
6. **Anything unresolved → `TECHNICAL-READER`.** Uncertainty defaults to density. The asymmetry is deliberate: over-simplifying for an engineer loses the evidence that makes the user competitive, while a recruiter encountering one dense bullet still sees the surrounding plain-language results.

**Two standing cautions.**

- **Recording the mode is not applying it.** This failed once already (see CLAUDE.md, 2026-08-06). After the draft renders, re-read the top third as the actual first reader and name every term they would not know.
- **`RECRUITER-FIRST` never means removing a term the posting itself uses.** Under this mode, keep exact technical terms the posting names and generalize or explain technical terms it does not. A posting that says "RAG" has licensed "RAG".

The mode changes presentation, not truth or evidence standards:

- In `RECRUITER-FIRST`, each bullet used to cover a posting priority must let a nontechnical recruiter identify the technology, how it was used, and the business or user reason. Preserve the exact technical terms needed by the posting and hiring manager.
- In `TECHNICAL-READER`, preserve technical density, architecture, methods, scale, performance, and exact tools. Do not add lay explanations that displace stronger technical evidence. The result or purpose must still be clear under X-Y-Z.
- Decide per application, not permanently per company. A direct technical-team referral or founder-routed process can justify `TECHNICAL-READER` even at a larger employer. Record the evidence for the choice in the review-gate report.

### RECRUITER-FIRST language gate, blocking

`RECRUITER-FIRST` is a drafting constraint from the first production draft, not a label applied during final review. Start with the result, user, and plain-language function. Add technical specificity only where it helps the posting or materially strengthens the evidence.

Run this as a **single bounded gate**, not a second tailoring project:

1. Before drafting production, make a short whitelist of the exact technical terms the posting names. A broad family such as `cloud and AI technologies` licenses those categories, not every vendor product within them.
2. Start from the closest one or two approved recruiter-first resumes for the same function and reuse established plain-language variants and stable term decisions. Use targeted searches for missing evidence instead of rereading the whole evidence bank.
3. Build a provisional census from the production source before the final render. Common standard terms may share one row only when every literal term is listed and every term has the same action and justification. Every vendor product or subproduct, unexplained acronym, internal name, unfamiliar proper noun, and `KEYWORD ONLY` term gets its own row so grouping cannot hide it.
4. Review only the exceptions requiring judgment and apply all `GENERALIZE`, `EXPLAIN`, and `REMOVE` edits in one batch. Do not start a separate edit-render-review loop for each term.
5. Render the final production pair once, extract that PDF's text once, and reconcile the census against the exact rendered wording. Perform one 10-second top-third read and one first-clause-only read of every bullet, then run the mechanical verifier once. Rerun only if an actual failure or approved wording change changes the file.

The complete census stays in the application audit file. The user-facing review links that file and summarizes changed or disputed terms, unsupported `KEEP` decisions, and blockers rather than repeating every passing row in chat.

Before Gate B can pass, scan the entire rendered resume, not only the top third, for every term in these families:

- Acronyms and abbreviations
- Vendor products and cloud services
- Framework, library, model, dataset, protocol, and architecture names
- Internal system or workflow names
- Specialist research, legal, financial, sales, or engineering shorthand
- Lesser-known employers, clients, projects, conferences, publications, and awards

Record every found term in this mandatory table:

| Resume term | Plain-English meaning | Named by this posting? | Reader action | Final rendered wording |
| --- | --- | --- | --- | --- |

Use only `KEEP`, `GENERALIZE`, `EXPLAIN`, or `REMOVE` for `Reader action`:

- `KEEP` only when the posting names the exact term, it is a standard search term for this functional recruiter, or removing it would materially weaken a role-relevant qualification. State which reason applies.
- `GENERALIZE` a vendor-specific or niche implementation into the category a recruiter can route, while preserving the truthful function. Example: `Vertex AI Search ingestion pipeline` becomes `Google Cloud data pipeline` when the posting does not ask for Vertex AI Search.
- `EXPLAIN` a necessary proper noun or technical term in adjacent plain language. A lesser-known employer or project keeps its real name, then gets a short description in its first bullet.
- `REMOVE` implementation detail, internal shorthand, or an unfamiliar acronym that adds decoding cost without improving match strength. Replace an obscure venue acronym with the relevant proof, such as `peer-reviewed`, when the role does not value that venue.

These actions are operational, not labels:

- `GENERALIZE`, `EXPLAIN`, or `REMOVE` must change the final rendered wording. If the wording remains unchanged, the action has not been applied and Gate B fails.
- Prefixing a product with its vendor does not count as `EXPLAIN`. `Google Vertex AI Live` still requires a functional explanation or generalization when the posting does not name it.
- An unrequested `KEYWORD ONLY` term defaults to `REMOVE` unless the row gives a concrete ATS-search reason for `KEEP`. Being true or broadly related to the posting is not enough.
- A posting's broad category does not count as naming a specific product, framework, model, or service inside that category.

Additional requirements:

- Expand an acronym on first use unless the posting uses that acronym or it is a standard recruiter search term for the function.
- The opening clause of every bullet must make the result, user, or business purpose understandable before specialist detail appears.
- Read only the top third and then only the first clause of every bullet. If a nontechnical recruiter cannot answer what changed, for whom, or why it matters, the bullet fails.
- Exact posting keywords may stay in Skills for searchability, but an unexplained product name in a bullet does not become recruiter-friendly merely because it is technically accurate.
- `NONE` is allowed only when the table explicitly states that every scan family above was checked and no unfamiliar term remains. Silence is `NOT CHECKED` and blocks Gate B.

## Gate A: Evidence discovery and clarification, after the benchmark-fit draft

Audit the complete first-pass the user resume against the benchmark and build an evidence map for the actual posting:

| Posting priority | Ideal honest claim | Role or project | X: result | Y: measure or proof | Z: method | Source | Status | Rendered resume evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- Cover the posting's 3-5 highest-value requirements, every role or project likely to appear, and every `NEW CLAIM - UNVERIFIED` introduced in the benchmark-fit draft.
- `Y` must be an honest number or verifiable proof: users, latency, throughput, cost, test count, adoption, revenue, publication, award, shipped artifact, user test, design review, selection, customer outcome, or similar evidence.
- A technology list, action verb, or phrase such as "built," "worked on," "production," or "large-scale" is not a `Y`.
- If a high-value claim has no documented `Y`, ask the user a targeted question after showing the complete benchmark-fit the user resume. Ask 2-4 questions per round, then repeat if important evidence is still unchecked.
- If no valid metric exists, ask for the strongest verifiable artifact. Mark the row `UNMEASURED` only after this check, and use that artifact instead of inventing a number.
- Mark genuinely absent experience `TRUE GAP`. Never convert it into a vague skills keyword.
- **A `TRUE GAP` is transient and dies with this application.** It is a classification of one row of one posting's evidence map. It lives in this application's Gate A table, its Gate 0 companion map, and the spoken review-gate report, and nowhere else. **It is never copied into `documents/cv/approved-bullets.md`, `documents/private/application-profile.md`, the Candidate Profile in CLAUDE.md, `documents/private/approved-answers.md`, or `documents/private/stated-beliefs.md`**, and no new entry in those files may say `true gap`, `hold off claiming`, `do not claim`, or `remains unconfirmed`, dated or undated. A classification that outlives the application it was made for has become durable memory, which the Learning Loop forbids. What does get saved after the user approves is the confirmation: the corrected positive bullet, not the rejection that produced it.
- **Never carry a gap forward from a previous application.** Do not read an old companion map, or a legacy pre-2026-08-18 ledger entry, and treat it as settled. When the posting names something, run it through Gate A from scratch and ask the user. Approvals are the exception and stay approved; they are never re-asked.
- **Why this rule exists.** The ledger's 2026-07 aerospace entry read `no AWS, no Kubernetes, do not claim them`; Kubernetes was confirmed 2026-08-04 and AWS on 2026-08-14, so the ban outlived its own truth by weeks and nothing in the workflow was set up to notice. The 2026-08-16 fix was to date the ban, and an audit two days later found 739 stored negatives, 23 already false. Dating it did not help, so the negative is no longer stored at all.
- In `Rendered resume evidence`, use `BULLET`, `PROJECT`, `COURSEWORK`, `KEYWORD ONLY`, or `OMITTED`. This field must cause action:
  1. If a role-critical requirement the user has is `KEYWORD ONLY` or `OMITTED`, first search the approved evidence for a concrete use and rewrite or add an evidence-bearing bullet, project, or coursework line.
  2. If the underlying use is under-documented, ask a targeted question tied to the most likely role or project. The item remains `UNCHECKED` until the user answers or the claim is removed.
  3. After clarification, either surface the confirmed evidence or leave the item `KEYWORD ONLY`. `KEYWORD ONLY` may remain in Skills when the skill is confirmed, but it does not count as qualification coverage. Disclose it as an uncovered requirement in the review-gate report.
  4. Do not call a requirement addressed merely because its keyword appears in Skills or a private evidence file. The exact rendered resume controls this field.
- For an internship or early-career posting that explicitly values teamwork, mentorship, agile work, code review, collaboration, receiving direction, or iteration on feedback, add a dedicated evidence-map row even if it falls outside the posting's top 3-5 technical requirements. If confirmed evidence exists, surface at least one concrete example in the production resume. If none exists, record the gap rather than listing a soft-skill claim.
- **🚨 WHERE TO SCAN FOR THIS TRIGGER: the responsibilities block, not the qualifications list.** Postings put tool and degree keywords under "Requirements" or "Desired Qualifications," and put the behavioral requirements in the duties block, whose heading varies: "In this role, you will," "What you'll do," "Responsibilities," "Your impact," "Day to day," or no heading at all. **Read the whole posting and decide the trigger from all of it.**
- **Language families that fire this row** (any one is enough; the words below are categories, not a checklist to string-match):
  - *Working with others:* collaborate, partner, consult, cross-functional, work alongside, team environment, stakeholders, peers
  - *Receiving input:* receive direction, take direction, coaching, feedback, mentorship, guidance, supervision, learn from
  - *Resolving friction:* resolve issues, escalate, raise concerns, align, negotiate, reconcile competing priorities
  - *Shared engineering process:* code review, pull requests, design reviews, pairing, standups, sprint planning, retrospectives
  - *Communicating outward:* present to, brief, report to, influence, build relationships, maintain contact with leaders
- **Record the decision in the Gate A map either way: `TRIGGERED` or `NOT TRIGGERED`, with the exact line quoted from the posting being worked on.** A row that is never evaluated is indistinguishable from a rule that does not exist, which is precisely how this rule failed once despite being written in three files.
- *Case note, 2026-08-06 (illustration only, not a template):* on a large-bank operations internship the trigger appeared four times in the duties block and zero times in Desired Qualifications, so a map built from the qualifications list alone missed a binding rule. Expect the split; do not expect the same wording.
- Ask the user to confirm, correct, tone down, or reject every `NEW CLAIM - UNVERIFIED`. Revise the the user resume after the clarification answers so it fits the benchmark as closely as the confirmed evidence supports.
- `UNCHECKED` evidence never blocks the required first complete the user-specific draft. Gate A cannot pass, and the resume cannot be approved, uploaded, or submitted, while a high-value row remains `UNCHECKED`.

## Gate B: Bullet and page-value audit, after drafting

Audit every proposed bullet in a table:

| Bullet ID | X | Y | Z | Evidence source | New claim? | Generic label? | Pass? |
| --- | --- | --- | --- | --- | --- | --- | --- |

Then audit posting coverage against the exact rendered resume:

| Posting priority | Rendered evidence | Action taken | Coverage result | Pass? |
| --- | --- | --- | --- | --- |

For every `RECRUITER-FIRST` resume, also include the completed full-document language table defined above. This table is mandatory even when the posting-coverage and bullet tables pass.

Rules:

- Every bullet must have a defensible X, Y, and Z. If a bullet has no number, name the exact artifact or external proof serving as Y. An analysis finding is not downstream impact: bullets beginning with `identified`, `analyzed`, `researched`, `assessed`, `evaluated`, `reviewed`, `conducted`, `explored`, `investigated`, or `improved` (the list `cv/verify_resume_layout.py` enforces) must state the decision, adoption, launch, allocation, user result, time or cost change, revenue effect, or external recognition that followed.
- Every new metric, tool, responsibility, title, or outcome is a `NEW CLAIM` until the user confirms it.
- Use the real institution, employer, client, project, publication, dataset, system, or award wherever one exists. Labels such as "Independent Research," "AI Project," or "Startup" fail when a specific name is available.
- Prefer `Professional Experience` or `Work History` for employment, `Projects` for named builds, and `Research` for research roles. Do not force all three content types into Professional Experience. Clear tailored headings such as `Engineering Experience`, `Technical Experience`, `AI & Machine Learning Experience`, `Project Experience`, `Research Experience`, or `Relevant Experience` are allowed when they organize the evidence more accurately for the target role. Keep them plain-text, concise, recognizable, and truthful.
- A paid industry role with "Research" in its title appears under `Professional Experience` or `Work History`, never under `Research`. Record standing placement exceptions like this in the candidate profile.
- Fold each relevant distinction into the role, project, education entry, or activity that earned it by default. A compact standalone `HONORS`, `AWARDS`, `HONORS & AWARDS`, or equivalent section is allowed when a small number of unusually strong, role-relevant distinctions materially strengthens the page and would otherwise be hidden or distorted. Do not duplicate the same distinction elsewhere, and justify the section in the review-gate report.
- Every included experience, research role, project, and leadership entry must have 2-5 bullets. One bullet is a hard failure, including for an older role. Do not use age as a bullet-count heuristic. Choose bullet count from posting relevance and evidence strength.
- Skills must earn their space. Every listed skill must map to a bullet, project, coursework item, or approved evidence source. For every role-critical requirement the user has, Gate B must confirm that the exact rendered resume contains an evidence-bearing bullet, project, or coursework line. If it does not, the coverage result is `KEYWORD ONLY`, the requirement is not counted as addressed, and the review report must state what search, rewrite, or evidence question was attempted. A present Skills section may use 1 to 4 coherent categories and no more than 6 rendered body lines. **No rendered Skills line may contain only one word. A wrapped continuation such as `dashboards` or a stranded category label is a blocking orphan, even when the general paragraph orphan scan passes.** A one-category or one-line section is allowed only when it contains relevant, evidence-backed hard skills that add useful coverage for the target; the verifier warns and Gate B must justify retaining it. For a nontechnical role that names no hard-skill gate, omit Skills and run `cv/verify_resume_layout.py` with `--allow-no-skills`, then document the omission in the review report.
- Apply the selected first-reader mode. In `RECRUITER-FIRST`, a priority bullet fails when its technology is present but its use and business or user reason are not understandable without specialist inference. Gate B also fails when the full-document language table omits a specialized term, uses `KEEP` without one of the permitted reasons, or leaves an unfamiliar company or project without plain-language context. In `TECHNICAL-READER`, a bullet fails when unnecessary simplification removes role-relevant architecture, methods, scale, performance, or exact tools. Both modes retain X-Y-Z and exact truthful terminology.
- When the conditional internship collaboration row was triggered in Gate A and confirmed evidence exists, Gate B fails if the production resume omits all concrete evidence of collaboration, review, direction, or feedback. Do not satisfy this check with `team player`, `communication`, `accepts feedback`, or another unsupported soft-skill label.
- **WORKING-WITH-PEOPLE FLOOR on every `RECRUITER-FIRST` internship resume, whether or not the posting names it.** These reqs are screened by a generalist checking that the intern can be handed to a team without friction, so a posting that stays silent on this is not a posting that does not want it. The page must carry **at least one concrete confirmed example in each of the four rows below**, and one bullet may satisfy more than one row. Record which bullet covers which row, or record the gap. Under `TECHNICAL-READER` this stays conditional on the posting, per the triggered-row rule above.

  | Row | What must be shown | Where the evidence comes from |
  |---|---|---|
  | **A. Taking direction** | Working under someone else's brief or supervision, with the outcome | A supervised research cohort, a founder-set scope, a client brief, a manager-assigned project |
  | **B. Receiving criticism and changing the work** | The work materially changed *because of* feedback | Review iterations with named reviewers, a design rejected after user testing, a rewrite that followed a critique |
  | **C. Working with others** | Shared delivery with named mechanics, not co-presence | Pull-request review and CI, cross-functional releases, sprint planning and retrospectives, shared repositories |
  | **D. Explaining technical work to non-technical people** | A specialist result made legible to a non-specialist audience, with what it produced | A demo or deck a non-specialist acted on, stakeholder interviews turned into requirements, model limits explained to subject-matter experts |

  **Row D is the one most often missing and is not satisfied by the term census.** The census governs *how the resume is worded*; row D requires evidence that the user has actually done this translation work in the job. They are different requirements and both apply. **No soft-skill label ever satisfies any row.** "Works well with others", "accepts criticism well", "strong communicator", and "team player" remain banned outright. **These four rows are checked per resume, not per bank**: a strong example living in `approved-bullets.md` does not mean it survived onto the page currently being built.
- Run a post-render page-value reconciliation, not just a one-page check. Inspect the exact PDF's bottom density, then list the 3 strongest omitted confirmed outcomes, or all of them if fewer than 3, and state why each loses to content that remains. Generic keywords, repeated stack lists, and weak older content lose space before stronger relevant engineering or research evidence.
- If the PDF ends more than 72 points above the bottom edge, restore the strongest relevant approved evidence and render again. Unused space may not coexist with a compressed one-bullet role or stronger omitted evidence.
- Run `cv/verify_resume_layout.py <pdf> --docx <docx>` on the exact canonical pair, adding `--allow-no-skills` only under the documented nontechnical-role exception above. Any path or filename mismatch, PDF older than the DOCX, normalized PDF text that differs from the DOCX source, missing explicit single spacing, paragraph-before spacing above the house limit, dedicated bullet symbol font, generic role or project label, one-bullet entry, analysis-only impact failure, Skills-density failure, page-count failure, bottom-density failure, date-alignment failure, bullet-geometry failure, unexpected rendered font, unembedded font, missing Unicode mapping, or broken extracted reading order blocks Gate B.
- Do not describe the resume as optimized if the audit finds a stronger confirmed claim that is still omitted.

## Review and upload freeze

- Form fields may be prepared incrementally, but do not upload a resume until Gate B passes and the user has reviewed and approved the exact PDF intended for upload.
- Approval applies only to that exact PDF. A rebuild, renamed replacement with changed contents, or later edit requires a new review.
- **The same freeze covers approved free-text answers.** Once the user approves the wording of a comment, essay, or short-answer field, do not add, cut, reword, or "improve" a line, and do not do so because a newly discovered problem would be explained by an added line. Ask them first, quoting the exact change. A line added after approval can be true, well-intentioned, and still an unapproved edit.
- A file-chooser timeout or failed upload attempt proves only that the attempt failed. It does not prove that a browser extension or file-upload permission is disabled.
- State that a permission is disabled only after directly inspecting the current setting. Otherwise report the observed failure and label permission changes as troubleshooting suggestions, not a diagnosis.

## Gate C: Exact packet consistency, before submission

Compare the exact PDF selected for upload against every visible or serialized application field and the submitted transcript.

Check line by line:

- Name, contact email, phone, links, location
- Employer and institution names
- Titles and relationship to the work, including hackathon or class-project context
- Start and end dates, especially `Present` versus a paused or ended role
- Degree name, declared field, graduation year, GPA, and any difference from the transcript
- Metrics, technologies, locations, and work authorization
- Resume filename and file contents actually attached

Rules:

- The form may add detail, but it may not silently contradict or inflate the resume.
- Any intentional resume-form or resume-transcript difference must be shown to the user in a `PACKET DIFFERENCE` list with the reason and risk. Silence is not approval.
- Approval applies to the exact reviewed PDF and disclosed packet differences. It is not standing authorization for later form edits.
- Submission is blocked while an unexplained contradiction remains.
- After submission, record the exact uploaded resume path, account email, graduation year, and any approved packet differences in `job_search_tracker.csv`.

## Required review-gate report

Before asking the user to approve, provide:

1. Gate 0 benchmark path and confirmation that it was shown in full first
2. First benchmark-fit the user resume path, confirmation that it was visibly labeled `DO NOT SUBMIT - UNVERIFIED CLAIMS`, and confirmation that the complete resume was shown before clarification questions
3. Selected first-reader mode, evidence for the choice, and its bullet-audit result. For `RECRUITER-FIRST`, save the completed full-document term census with every `KEEP`, `GENERALIZE`, `EXPLAIN`, and `REMOVE` decision in the application audit file; in chat, link it and summarize every changed or disputed term, unsupported `KEEP`, and blocker.
4. Line-by-line benchmark correction map
5. Evidence gaps questioned and what was confirmed
6. Posting-coverage table from the exact rendered resume, including every `KEYWORD ONLY` or `OMITTED` requirement and the action taken
7. Remaining `TRUE GAP` or `UNMEASURED` items
8. Bullet audit failures corrected
9. Every `NEW CLAIM`, including the disposition of each claim introduced in the benchmark-fit draft as `CONFIRMED`, `CORRECTED`, or `REJECTED`
   - Include totals for `CONFIRMED AS WRITTEN`, `CORRECTED`, `REJECTED`, and `UNRESOLVED`, plus the provenance-checker result. Any unresolved count above zero blocks approval, upload, and submission.
10. Conditional internship collaboration decision, evidence selected, and rendered placement when triggered
11. Section and per-entry bullet-count result, plus the Honors/Awards placement decision and justification
12. Skills-density, bottom-density, and page-value result, including the strongest omitted-evidence comparison
13. `cv/verify_resume_layout.py <pdf> --docx <docx>` result for the exact canonical pair, including source path/name/freshness, paragraph spacing, marker font, rendered font families, and extracted reading order
14. Generic labels replaced with proper nouns
15. Expected packet differences, including transcript differences
16. Exact production PDF path that will be uploaded, plus confirmation that it is not the benchmark file

If any item has not been checked, say `NOT CHECKED` rather than implying the resume is final.

## Learning Loop verifier, blocking, after the memory writes

After the submission is logged and the memory files are updated, and **before the final report**, run:

```
python3 cv/verify_learning_loop.py
```

It scans the **added** lines of the durable memory files in `git diff` and fails on stored negatives: a rejected Gate 0 hypothesis, a missing tool, a number the user could not supply, or any positively-phrased instruction to ask again later. **A failure is blocking and the fix is deletion, not rewording.** The correct diff for a rejected hypothesis is empty; Gate A re-asks on its own next time, which is the intended behavior because the user builds constantly.

Gate 0 dispositions belong in that application's companion map and answer sheet, which expire with the application. They are never copied into the ledger.

Waive a line only for the three carve-outs in CLAUDE.md, by putting `learning-loop-ok: <reason>` on it.

**This exists because the prose rule failed on Crowe R-51782 (2026-08-25): three rejected hypotheses were written into `approved-bullets.md` as durable memory and the user caught it, not the process.**

## Conditional Rules Register (MANDATORY emit at the review gate)

**Why this exists.** On 2026-08-06 the collaboration RULE sat unfired on a Wells Fargo application even though it was written in CLAUDE.md, AGENTS.md, and this file. It did not fail because it was missing or because it was read and ignored. It failed because it is **conditional**, its trigger lived in a part of the posting that was never extracted, so the condition was never evaluated at all. A rule whose input is never gathered is indistinguishable from a rule that does not exist, and nothing in the output revealed the omission.

**The fix is an artifact, not another rule.** "Consider everything in the repo" is the right standard and it is not self-enforcing across a 500-line CLAUDE.md, an 800-line ledger, and an 86-row playbook. Every conditional rule below must be given an explicit disposition in the review-gate report **whether or not it fired**. A skipped check then shows up as a missing line instead of as silence.

Emit this block verbatim, one line per row, before asking the user to approve any resume:

| # | Conditional rule | Required disposition |
|---|---|---|
| 1 | First-reader mode | `RECRUITER-FIRST` or `TECHNICAL-READER`; for `RECRUITER-FIRST`, include the completed full-document term census and every `KEEP`, `GENERALIZE`, `EXPLAIN`, or `REMOVE` decision |
| 2 | Collaboration / direction / feedback trigger | `TRIGGERED` or `NOT TRIGGERED`, with the deciding line quoted from this posting, and the evidence used or the gap recorded |
| 3 | Graduation year | Which Default Selection Rule branch fired (1-4) and why |
| 4 | Top-third keyword coverage | Posting's named must-haves, and which appear below the fold |
| 5 | Skills-only coverage | Every `KEYWORD ONLY` item disclosed, confirmation none is role-critical, and the Skills shape justified: 2-4 categories, a justified warned one-line section, or a justified `--allow-no-skills` omission |
| 6 | Multiple reqs at one employer | Functional groups named, and which resume serves each |
| 7 | Honors placement | Folded into the earning entry, or standalone with the justification, and which of the two permitted formats |
| 8 | Company descriptor | All-or-none satisfied across lesser-known employers |
| 9 | Page fit | What was cut to reach one page, and the strongest omitted confirmed evidence |
| 10 | Coursework line | Omitted by default, or included with the role-specific reason |
| 11 | Working-with-people floor (rows A-D) | On every `RECRUITER-FIRST` internship resume: which rendered bullet covers each of rows A, B, C, and D, or the gap recorded per row; under `TECHNICAL-READER`, `NOT APPLICABLE` unless the collaboration trigger in row 2 fired |

**Rules for this register.** `NOT TRIGGERED` is a valid and common answer; the point is that it was evaluated. `NOT CHECKED` is permitted only when stated plainly, and it blocks upload. Do not mark a row satisfied by asserting the principle; cite the posting line, the file, or the rendered artifact that decided it. Add a row whenever a new conditional rule is approved.

## Retracted-claim rail, blocking at Gate B

```
python3 cv/verify_no_retracted_claims.py "<the exact production pdf>"
```

Run it on the rendered production PDF alongside `cv/verify_resume_layout.py`. **A hit is blocking and the resume may not be uploaded.** It carries the claims the user has stated are false about their own past, so it is an integrity rail under the CLAUDE.md carve-out, not a Learning Loop negative: it protects them from a fabricated award or a denied tool attribution reaching a page, and it suppresses nothing they can legitimately claim.

**Why it exists:** the user asked on 2026-08-25 for every retraction note to be deleted from `approved-bullets.md`, and they were. A scan then found **54 build scripts** still carrying `USACO Gold`, `PySpark`, or the dead `4 million shipment records` figure. Those scripts are what the Tailor step copies from when it starts from the closest prior resume, so the notes had been the only thing between them and a live page. The protection now lives on the rendered artifact instead of in prose. `python3 cv/verify_no_retracted_claims.py --scan-builders` lists the affected builders; they are the historical record of submitted resumes and are left unedited.
