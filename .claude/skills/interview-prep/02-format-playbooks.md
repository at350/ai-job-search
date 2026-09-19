# Format Playbooks

What changes per assessment format. The workflow in `SKILL.md` is the same every time; what varies is the research target, the answer grade, the rehearsal, and whether notes are normally permitted.

Research the specific platform every time rather than assuming. Platforms change their scoring, and a rule that was true two years ago is exactly the kind of thing a candidate report will repeat long after it stopped being true.

---

## Recorded one-way video (HireVue, Modern Hire, Sparkhire, Paradox/Olivia)

**What it is.** A set of prompts, each with a short prep timer and a short recording window. Usually one attempt per question. Nobody is watching live.

**Research to button level.** The exact labels on the buttons, **the number of scored questions, the preparation timer, and the maximum recording length**, whether practice takes are unlimited and unsaved, how many retakes the employer enabled, what the status messages mean, and how long the window stays open. **Check any interview-question database the user has access to first** (campus career-prep portals often hold the exact question count and timer for a given employer). A prep written without them routinely plans the wrong number of answers at the wrong length. Get this from the platform's own help pages plus the invitation, not from candidate memory.

**Optimize the transcript AND the video. Both are read.** Any automated scoring layer works from language, that is, the transcript, so say the structural words out loud: "the situation was", "the actions I took were", "the outcome was". A human skimming a transcript and a model parsing one reward the same legibility. **But human reviewers watch the recording itself** — campus recruiting and the hiring team are not handed a text file — so physical setup and finishing cleanly matter too. A transcript parser does not notice a mid-sentence cut; a person watching does.

**🚨 Do not claim a vendor's published scoring behaviour applies to a different vendor.** HireVue removed facial analysis in 2020 and later dropped vocal-tone scoring. That is documented, and it is evidence about **HireVue only**. It is easy to cite it as settled fact about a different vendor's stage and then have to retract the claim. Name the vendor the employer actually uses, and file anything carried across from another vendor as **Reported**, never **Confirmed**.

**Answer grade:** verbatim timed scripts. Publish the beat clock in the document. Give every answer a 60-second compression, because the window is sometimes shorter than advertised.

**🚨 BUILD TO 70% OF THE RECORDING CAP, AT 115 WORDS A MINUTE.** This replaces the common "roughly 140 words per minute" advice, which overruns the timer.

Worked example of the failure: 245-word scripts timed at 85 to 108 seconds using **140 wpm**, against a **2:00** cap, get cut by the timer every time, because the real delivered rate is **110 to 120 wpm**. Speaking rate drops on camera, under a visible countdown, with no listener to react to. **140 wpm is a reading rate, not a recording rate.**

1. Compute length at **115 words a minute**, never 140.
2. Target **70% of the stated cap**, never 90%. For a 2:00 cap that is about **84 seconds, roughly 160 words**.
3. Land the result and its number by **50% of the cap**, so a cut costs nothing that is scored.
4. **Rehearse one answer against a real timer, measure the actual rate, and re-cut every script to it.** This step existed in the rehearsal plan and was skipped; running it would have caught the error before recording.
5. Write the closing tie-back as its own short sentence, never a subordinate clause, so it survives being dropped.

Example beat clock for a **2:00 cap**, targeting 1:24: headline 0:00-0:10, situation 0:10-0:25, three concrete actions 0:25-0:55, outcome with a number 0:55-1:10, tie back 1:10-1:24.

**Use practice mode deliberately.** Where practice takes are unlimited, unsaved, and invisible to the employer, that is free rehearsal on the real interface. Say so in the prep and budget time for it.

**Physical setup belongs in the prep:** camera at eye level, light in front, look at the lens rather than the preview window, business casual unless stated otherwise.

**Integrity:** usually closed. Even where notes are not prohibited, visibly reading a script off a second screen is obvious and reads badly. Bullet cues at eye level beside the lens are the most that should ever be suggested, and only when the employer's policy permits notes.

---

## Virtual job tryout and situational judgment (SHL, Pymetrics, and employer-branded tryouts)

**What it is.** Multiple modules of different kinds in one sitting: ranked situational judgment, a business case, factual work-history questions, forced-choice work-style items. Not a conversation, and it does not ask "why this company".

**No recording guidance is needed.** Replace it with a method per module:

- **Ranking items:** score each option against the dimensions the employer says it values, then rank. Write the scoring method down so it is applied consistently rather than by feel.
- **Business case:** a fixed number of passes over the material, with a stated goal per pass, so time does not disappear into rereading.
- **Factual and work-history items:** answer from the submitted packet, not from the fullest version of the truth. These are cross-checked against the application.
- **Self-ratings:** do not build a profile where every positive statement gets the maximum. It reads as invalid and some instruments flag it directly.
- **Forced choice:** build a truthful compass first, a table of the dimensions and where the user actually sits, then answer from it. Consistency across items is what is being measured.

**Answer grade:** original practice scenarios with an answer key, plus a calibration exercise. Label the practice as original and not reproduced from the assessment.

**Integrity:** closed, and these instruments often say so explicitly. Do not photograph, copy, or distribute items, during or after.

---

## Coding and technical assessment

**What it is.** Timed problems, sometimes on a proctored platform, sometimes with a follow-up explanation.

**Research the scorecard,** not just the topics. A shared rubric across functions plus a per-function emphasis is common, and knowing which one applies changes what to practice.

**Answer grade:** not answers at all. Build a named routine with numbered steps, run it every time. Restate the contract, name the edge cases, pick the pattern, write it, test it against the cases named up front, then state complexity and failure behavior. Add a recall sheet for the language and a clue-to-pattern lookup for the desk sheet.

**Study order when preparation time is short.** Six patterns cover most of what actually gets asked: hash maps, recursion, depth-first and breadth-first search, binary search, sliding window, and heaps. Work those before dynamic programming, which is discussed far more than it is asked. Build the clue-to-pattern lookup over these six first. **Where the user keeps failing tree, graph, or backtracking problems, treat recursion as the cause rather than the topic they are failing**, and study that instead of the surface topic. The language recall sheet should carry the traps that produce silent wrong answers rather than errors, which in Python are floor division rounding down instead of toward zero, negative modulo differing from Java and C++, list multiplication aliasing rows in a grid, and `heapq` being min-heap only.

**Write runnable practice**, with contracts in docstrings and solutions in a separate file so the practice is real. Keep one worked example folder under `interviews/` as the pattern. Head every practice file with a line saying it is preparation material and not a live or leaked assessment.

**Prepare the explanation separately.** A three-minute walkthrough with fixed beats, since being able to rebuild and explain the solution is frequently the actual test.

**Integrity:** closed, and the strictest of any format. Do not paste a solution the user cannot rebuild and explain. Between multiple assessments, do not review or discuss the live questions with anyone, Claude included.

---

## Live conversation: recruiter screen, hiring manager, behavioral round

**What it is.** A human, usually 15 to 45 minutes, usually with a named interviewer.

**Research the person, lightly.** Their role, how long they have been there, what they own. Enough to ask a question that lands. Do not build a dossier.

**Answer grade:** speaking outlines, never scripts. Beats, not sentences. A script read aloud in a conversation is worse than a rough answer delivered naturally.

**The desk sheet carries what the async formats do not:** the interviewer's name, the meeting link and password, two questions to ask, an explicit close, and the thank-you plan with its deadline.

**Prepare the close.** Confirming next steps and timeline is part of the interview, and it is the part most often skipped.

**Integrity:** notes are usually permitted and rarely mentioned. Where permitted, the desk sheet sits beside the camera rather than on the screen below it. Claude still does not participate in the call.

---

## Case interview

**What it is.** A business problem worked aloud with the interviewer, usually consulting or strategy.

**Answer grade:** a structure, plus practice cases. The structure has to be visible to the interviewer, since the process is what is scored and a correct answer arrived at invisibly scores badly.

**Practice with numbers said out loud.** Mental arithmetic under observation is a separate skill from arithmetic, and it is where most of the avoidable loss happens.

**Integrity:** closed. Notes on paper are expected and usually encouraged; that is the candidate's own scratch work, not reference material.

---

## Superday and multi-round onsite

**What it is.** Several back-to-back rounds, often mixed formats, sometimes with a lunch that is also an evaluation.

**Build one facts file and one desk sheet for the day**, plus a per-round section in the full prep. Do not build three parallel sets; the packet, the boundaries, and the numbers are shared and must not drift between rounds.

**Plan for repetition.** The same story will be asked for twice by different interviewers who compare notes afterward. Keep the facts identical and vary nothing that matters.

**Track who asked what** during the day, for the log and the thank-you notes, which should be individualized per interviewer.

---

## When the format is genuinely unknown

Say so in `facts.md` rather than guessing. Prepare for the most demanding plausible version, list what would change under each alternative, and tell the user which single question to the recruiter would resolve it. Asking a recruiter what format to expect is normal and costs nothing.
