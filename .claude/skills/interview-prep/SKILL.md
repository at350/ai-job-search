# Interview Prep

**name:** interview-prep
**description:** Prepares the user for a specific interview or assessment end to end: researches the employer, the role, and the exact assessment format, reconciles what they actually submitted, builds a per-interview facts file plus a full prep document plus a one-page desk sheet, runs scored practice drills, and closes the loop afterward by logging the interview and feeding the answers that worked back into memory. Use this whenever the user has an interview, phone screen, HireVue, Virtual Job Tryout, coding assessment, case, superday, or recruiter call coming up, or says "prep me for X", "I have an interview at X", "what should I expect from this assessment", "quiz me", "run a mock interview", "drill me on behaviorals", or mentions an interview invitation email. Also use it after an interview happens, to log it and update the tracker.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, Bash, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__list_connected_browsers, mcp__claude-in-chrome__select_browser

---

## Why this skill exists

Interview prep works, and it drifts. Run it a few times without a written spec and every run reinvents its own section names, its own confidence vocabulary, and its own idea of what gets produced, so artifacts in `interviews/` disagree with each other and every good invention (the ranked question bank, the practice scoring rubric, the executable practice files, the separate format-research pass) appears once and is never reused.

This file is that spec.

**Companion file for content:** `.claude/skills/job-application-assistant/07-interview-prep.md` holds the durable, cross-company material (story bank, recurring tough questions, questions to ask). This file holds the workflow. Content lives there, process lives here, and neither should restate the other.

## What gets produced

Three artifacts per interview, in a dated folder: `interviews/YYYY-MM-DD - <Company> <assessment or round>/`.

| File | Size | Purpose |
|---|---|---|
| `facts.md` | 2k to 4k | The single source of truth. Submitted packet, do-not-claim list, numbers, deadlines, format determination. Everything else derives from it. |
| `full-prep.md` | 15k to 50k | Research, answers, practice material, rehearsal plan. |
| `desk-sheet.md` | 3k to 6k | The last-mile page. Decisions, numbers, prohibitions, nothing else. |

Full anatomy and the canonical section order for each is in `01-artifact-specs.md`. Do not invent section names; that is the specific failure this spec exists to prevent.

**Scale by format, not by habit.** A 15-minute live recruiter call gets `facts.md` and `desk-sheet.md`; a full prep would go unread. A recorded assessment, a coding test, a case, or an onsite gets all three. When in doubt build all three, since the desk sheet is derived and cheap once the full prep exists.

**Derivation is one-directional.** `facts.md` is written first and is the only place a submitted fact, a metric, or a do-not-claim boundary is stated. The other two quote it. When a fact changes, it changes in `facts.md` and the other two get rebuilt. Artifacts drift precisely when the same facts are separately maintained in two files.

## The workflow

### 1. Establish what the interview actually is

Read the invitation email as the primary source; it is more reliable than anything on the web. Extract the employer's exact assessment name, the platform, the window, the deadline to the minute in the user's own timezone, the support and accommodations contact, and whether a human is named.

Then determine the format and record its evidence tier. Use exactly two tiers, and these words:

- **Confirmed** by the employer or the assessment platform, in writing, for this specific invitation.
- **Reported**, meaning candidate accounts, Glassdoor, coaching sites, or prior-year write-ups. Useful, not guaranteed.

Never blend them. When reported accounts disagree across years, say so and plan for the hardest version. When the format research is substantial, write it as its own dated file in the interview folder rather than burying it inside the prep document.

**Set the personal deadline earlier than the real one**, so a technical problem does not become a deadline problem.

### 2. Note the employer's notes and AI policy

One line in `facts.md`, quoting the employer where they state a policy: whether notes or reference material are permitted during this interview. That is all this needs to be. Do not restate it in the full prep or the desk sheet, and do not build a classification scheme around it.

Where an employer says nothing, assume notes are not expected and move on.

Claude's own standing constraints are in CLAUDE.md and apply whether or not they appear in a document: on-screen instructions always win, preparation does not open the live assessment link, Claude does not assist during a live or recorded assessment, and any practice question Claude writes is original rather than reconstructed from a real one.

### 3. Reconcile the submitted packet

Open the exact PDF that was uploaded, from `job_search_tracker.csv` or `cv/<Your Name> - <Company>.pdf`, and read it rather than reasoning from memory of the bank. Record in `facts.md`:

- Which roles, dates, and metrics are on that specific page, and which real experience is not on it
- The graduation year presented for this application, per the Default Selection Rule in CLAUDE.md
- The GPA as submitted, if a coarse form dropdown recorded something other than the real figure
- The account email used
- Any `PACKET DIFFERENCE` already logged for the application

Then write the **do-not-claim list**: technologies, responsibilities, and scope that are not defensible, named explicitly. This is the single highest-value block in the whole prep, and it is what keeps an answer from wandering somewhere the resume cannot back up.

**The list is scoped to this packet and stays in this folder.** It answers "what can the exact submitted PDF support in this conversation," not "what is the user unable to do." Write it against that page, not against the bank. It is never copied into `documents/cv/approved-bullets.md`, `documents/private/application-profile.md`, the Candidate Profile in CLAUDE.md, `documents/private/approved-answers.md`, or `documents/private/stated-beliefs.md`, and a later interview's `facts.md` is written from that interview's own packet rather than inherited from this one. A boundary that outlives its packet has become durable memory, which the Learning Loop forbids. A stale boundary ("AWS is keyword-level only", written days before the user confirmed real AWS work) is exactly what this rule prevents. When the post-interview log runs, what feeds back into the memory files is the confirmations: answers that worked, new facts, new opinions. The boundaries stay here and die with the folder.

Also flag the reverse trap: something true and strong that is absent from the submitted resume. If a current role is not on the page, "tell me about your most recent role" has a right answer and a wrong one.

### 4. Read the memory files before writing a single answer

All six, every time. The old prep artifacts declared these inputs and then never actually cited them, which is how the same story got re-derived from scratch seven times.

| File | What to take from it |
|---|---|
| `documents/private/approved-answers.md` | Answers the user already approved. Reuse the wording; do not rewrite what they have signed off on. |
| `documents/private/essay-context.md` | The user's real anecdotes, the ones with names and stakes in them. Its themes index is a STAR lookup. |
| `documents/private/stated-beliefs.md` | Every position the user holds, with a provenance tier (Verbatim, Approved, Paraphrase, Raw) and a source. The canonical file for worldview, "what do you think about X", and industry-opinion questions. Where an entry cites a media-library file, read that file for exact quotes and fact-check flags before quoting a third party or printing a number. |
| `documents/playbook/index.md` | Claims tagged `interview-behavioral`, `interview-technical`, and `negotiation`. Apply CONTEXT claims as judgment. CLAUDE.md still wins on conflict. |
| `documents/library/index.md` | A real recent thing the user consumed, for "what have you been following lately" and for a current-market observation. Only items where the Take column says Yes. |
| `interviews/` | Every prior interview at this company, and every prior interview in this format. Reuse what worked, drill what stumped. |

### 5. Predict the questions from the posting before writing any answer

Behavioral questions are not random. They are written against the competencies the role needs, and the role states those competencies in its own responsibilities block. Prep built from a generic question list guesses at that; prep built from the posting reads it.

Pull the responsibilities or duties block from the posting the user actually applied to. This is the same block Gate A already parses on the resume side, under whichever heading that employer used ("In this role, you will", "What you'll do", "Responsibilities", "Your impact", or no heading at all), so on most applications the extraction is already done and only needs to be carried across.

Then, for each responsibility:

1. Name the competency it tests (ownership, communication, execution under ambiguity, working with others, taking direction, technical depth).
2. Attach a story from the bank that can carry it, drawn from the memory files read in step 4.
3. Write the two or three behavioral questions that responsibility implies.

Three rules for the mapping:

- **Prefer breadth of coverage when choosing stories.** A story that answers four responsibilities is worth more than a story that answers one, because it survives whatever order the interviewer asks in. Reuse is the goal; a new story per question is a sign the mapping was skipped.
- **A responsibility with no story attached is a prep gap and gets recorded as one**, the same way an unevidenced requirement is recorded on the resume side. Do not paper over it with a story that does not actually fit, and do not let it disappear silently.
- **Nothing enters the map that the do-not-claim list forbids.** Step 3 runs first for this reason.

This map is what feeds `## What they are measuring` and the ranked `## Question bank` in the full prep. Where no written posting exists (a recruiter chat, a research conversation, an unstructured founder call), say so in `facts.md` and fall back to the format playbook and prior interviews.

### 6. Research the employer, then ration it

Gather more than will be used, then keep a short block of hard-verified facts with a stated limit. One fact is enough, two is showing off. What earns a place is a fact that shapes an answer, not a fact that proves research happened.

Verify anything checkable before it enters the document, and fence off what could not be verified. Naming a title that does not exist is worse than naming nothing. Keep a running list of unverified items rather than silently dropping them.

For the "why this company" answer specifically: name one real distinguishing trait a competitor could not claim, specific enough to survive a follow-up question. "They have a tech edge" fails. Naming the platform and what it does passes.

### 7. Write the answers at the right grade

Match the storage grade to the format rather than defaulting to scripts:

- **Recorded, one attempt, transcript-scored** (HireVue and similar): verbatim timed scripts on a published beat clock, roughly 100 to 110 seconds at 140 words per minute, each followed by why it works, its guardrail, and a 60-second compression.
- **Live conversation:** speaking outlines only. A script read aloud sounds like a script read aloud.
- **Practice-only material:** full prose is fine, labeled disposable, with an instruction to rebuild it in their own words.
- **Technical or case:** a named routine with numbered steps, plus flash cards, plus a timed explanation structure.

STAR is a tool, not a law. Forcing every prompt into STAR is a known failure mode. Use it for behavioral prompts and use the right shape for everything else.

**Close a behavioral answer on what changed afterward.** Context, action and result stop at what happened. Add a short final beat saying what the user learned or what they would do differently, which turns the answer into its own reply to "what would you do differently," a question interviewers ask often enough to prepare for. One or two sentences, and it has to be a real change in how they work rather than a lesson bolted on, since an invented one is audible. Skip it where the result already carries the learning, and skip it on a recorded format tight enough that the beat would push the answer past its clock. This is the difference between STAR and CARL, and it is an addition to the close rather than a replacement for the usual time split across the beats.

Build a **story bank table**, one line each: story, numbers, best used for, and boundary. Keep the numbers identical to how they appear elsewhere in the repo, since a figure that shifts between documents is a figure the user cannot say with confidence.

Rank the question bank by likelihood into near certain, likely, and possible, and state explicitly what is **not** expected, so preparation does not sprawl. The bank is built from the step 5 map, not from a generic list; likelihood follows how much of the posting a question covers.

### 8. Build the desk sheet by compression

Target 6:1 to 12:1 against the full prep. Delete every sentence of prose. What survives is decisions, numbers, prohibitions, the question-to-story lookup, and the closing routine. State at the top whether the sheet may be open, using the boundary decided in step 2 and the reason for it.

### 9. Rehearse, then drill

Write a timeboxed rehearsal plan sized to the assessment: 30 minutes for a short recorded set, 45 to 60 for a multi-module tryout, 90 for a coding test. Say what happens in each block.

Then offer the scored drill in `03-drill-mode.md`. This is the part that most improves outcomes and the part the user has had the least support on.

### 10. Verify before handing it over

- Every metric in all three artifacts matches `facts.md` and the submitted PDF
- No claim crosses the do-not-claim list
- The graduation year matches what was submitted
- Confirmed and reported are never blended
- Practice material is labeled original and not reconstructed
- No em-dashes anywhere, per the Global Writing Rules
- Every unverified item is flagged rather than quietly dropped
- Every responsibility in the posting has a story attached or is recorded as a prep gap

### 11. Close the loop afterward

This is the step that never gets done: prep artifacts pile up and post-interview logs do not. Treat that as a design problem, not a discipline problem: the blank page is the obstacle, so **Claude drafts the log and the user corrects it.**

When the user mentions an interview happened, or when a known interview date passes:

1. Draft `log.md` in the interview folder from the prep document, pre-filling the questions that were expected and the answers that were prepared, leaving what actually happened for them to correct. Record which predicted questions actually came up, since that is the only way to find out whether the step 5 mapping works. Ask two or three specific questions ("did the ranking module appear?", "which story did you use for the failure question?") rather than "how did it go".
2. Move what worked into `documents/private/approved-answers.md`, tagged with company, prompt type, and date.
3. Move anything that stumped them into the tough-questions list in `07-interview-prep.md`.
4. Save any new personal fact to `documents/private/essay-context.md`, any new or refined opinion to `documents/private/stated-beliefs.md`, and any new resume-grade claim to `documents/cv/approved-bullets.md`.
5. Update the row in `job_search_tracker.csv` to `interviewing` or the outcome, with a dated note recording the date and the questions actually received.
6. Run the `warm-outreach` skill (default yes, per the Application Pipeline). A live interview makes everyone at that company a Tier 1 contact under the CLAUDE.md triage rules, since the application is live and a conversation can still move it.
7. Tell the user in one line what was saved.

## Reference files

| File | Purpose |
|---|---|
| `01-artifact-specs.md` | Canonical section order and naming for the three artifacts, plus the fixed vocabulary |
| `02-format-playbooks.md` | Per-format handling: recorded video, virtual job tryout, coding assessment, live conversation, case, superday, recruiter screen |
| `03-drill-mode.md` | The scored practice drill and its rubric |

## Rules

- Follow CLAUDE.md's Global Writing Rules. No em-dashes, plain language, no slogan lines.
- CLAUDE.md outranks this file. The playbook informs it. Neither outranks a fact the user has confirmed about themselves.
- Never invent a metric, a company fact, an interviewer name, or a format detail. Flag the gap and ask.
- Never write an answer that the submitted resume cannot support.
- Never assist during a live or recorded assessment, and never build a document intended for use during one.
