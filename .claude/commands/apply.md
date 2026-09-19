# /apply - Job Application Workflow

The job posting is provided as `$ARGUMENTS`, either a URL or pasted text.

This command is a thin entry point to the authoritative workflow. Read these files in order:

1. `CLAUDE.md` for the candidate profile, the Application Pipeline, and the deal-breakers
2. `.claude/skills/job-application-assistant/SKILL.md` for the operational summary and the reference-file map
3. `.claude/skills/job-application-assistant/09-resume-evidence-audit.md` for the mandatory benchmark-fit draft and Gates A, B, and C

Deliverables are a one-page DOCX source and the matching rendered PDF. The single exception is a federal application through USAJOBS, which is built to the two-page federal limit and verified with `--pages 2`.

## Required sequence

1. Fetch and read the live posting. Verify formal eligibility before tailoring anything.
2. Complete Gate 0. Build and show the full `DO NOT SUBMIT - HYPOTHETICAL BENCHMARK` resume first: the resume the perfect candidate for this exact posting would have.
3. Immediately build and show a complete one-page benchmark-fit candidate resume, using the benchmark as the default target for role selection, section order, bullet emphasis, skills coverage, ATS language, and density. Search the existing evidence first, then introduce plausible new metrics, technologies, responsibilities, scope, causal relationships, and outcomes for the candidate's **real** roles wherever the files appear incomplete. Write them as polished resume claims and track each as `NEW CLAIM - UNVERIFIED`. Save the artifact separately under `Benchmark-Fit Draft - DO NOT SUBMIT` and visibly label it `DO NOT SUBMIT - UNVERIFIED CLAIMS`. Do not ask clarification questions or present the correction map before this resume is complete and shown.
4. Complete Gate A after both resumes are shown. Build the correction and evidence maps, ask the user to confirm, correct, tone down, or reject every `NEW CLAIM - UNVERIFIED`, and revise the resume with their answers. `UNCHECKED` evidence blocks finalization and upload, not the required first complete draft.
5. Render the revised DOCX to PDF and complete Gate B on the exact PDF.
6. Run `cv/verify_resume_layout.py <pdf> --docx <docx>` on the exact canonical pair. A path, name, or freshness mismatch, a paragraph-spacing or bullet-font failure, a standalone Honors/Awards section that does not earn its space, any entry with fewer than 2 or more than 5 bullets, a bottom-density failure, or any other verifier failure blocks review.
7. Complete the post-render page-value reconciliation. List the 3 strongest omitted confirmed outcomes, or all of them if fewer, and explain why each loses to retained content. A one-page render alone is not success.
8. Present the exact PDF and the complete review-gate report. Label anything not checked as `NOT CHECKED`. Wait for the user to approve that exact PDF.
9. Do not upload a resume before approval. After approval, attach that exact PDF, complete Gate C against every form field and the transcript, disclose each `PACKET DIFFERENCE`, then obtain explicit approval for the final submit.
10. Log a submission only after direct confirmation from the portal. Save approved new claims through the Learning Loop.

## Hard epistemic rule for uploads

A file-chooser timeout or failed upload proves only that the attempt failed. State that a browser extension or file-upload permission is disabled only after directly inspecting the current setting. Otherwise report the observed failure and label any permission change as a troubleshooting suggestion.

## Output

Lead with the current outcome and any blocker. Never call a resume verified, final, optimized, maximized, or ready until the applicable evidence, content, visual, review, and packet-consistency gates have passed.
