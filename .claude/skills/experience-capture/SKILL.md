# Experience Capture

**name:** experience-capture
**description:** Weekly check-in that interviews the user about what they actually did recently (each current job, project, club, course, and side build) and writes the confirmed facts into the workspace's memory files, so resumes and application answers can draw on experiences before they would otherwise be forgotten. Trigger on: "experience capture", "capture my week", "update my experience", "log what I did", "weekly check-in", or when the user describes recent work worth saving. Runs on a weekly schedule and on demand.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch

---

## Why this exists

People routinely do things that never make it into the files, and they do not remember them until something prompts them. This skill front-loads the prompting so the memory grows continuously instead of only during applications.

## Ground rules

- **Capture, don't compose.** This skill records true facts in rough form. Polished resume bullets happen later, at Tailor time. Do not gold-plate what the user says; write it down close to their words with the concrete details (tools, numbers, who, what shipped).
- **Anti-fabrication applies.** Log only what the user states. If something is vague ("did some backend stuff"), ask one follow-up for a specific (which service, which tool, what changed) before saving.
- **Artifact-anchored recall beats open questions.** Open-ended recall systematically under-returns. Start from GitHub activity, calendar events, email threads, repository changes, tracker rows, or another concrete jogger, then ask narrow questions. Do not interpret an empty catch-all response as an empty week. If the user has said that recall is hard for them, treat this as a standing accommodation, not a style preference.
- **Follow the Global Writing Rules in CLAUDE.md** (no em-dashes, plain language).

## The flow

1. **Prep the prompts.** Before asking anything, gather memory joggers so questions are specific, not generic:
   - Read the last capture log in `documents/private/experience-log.md` (create it on first run) to know where things stood.
   - Check recent public GitHub activity for the profile in the candidate profile (new repos, pushes) and, if easy, anything the user posted on LinkedIn recently.
   - Read the current role summaries in CLAUDE.md's Candidate Profile and `01-candidate-profile.md` so you know what is already recorded.
2. **Ask directly in the reply message.** Do not use the AskUserQuestion tool. Write the questions as plain text in the message itself, 2-3 per role, anchored in specifics: "Last log said you were building the ingestion relay at <employer>. What did you ship since?" Cover every role, club, and project listed in the candidate profile, plus hackathons and side builds, coursework or certifications, and a catch-all "anything else worth remembering (a talk, a person met, a win, a failure with a lesson)". Skip roles the last log already marked unchanged. Keep it short; the user can answer as briefly as they want, whenever they see it.
   - **Always include at least one adoption-or-scale question, every run.** Bullet banks skew hard toward *reduction* metrics (cut X%, saved Y hours) because those are the easiest to notice, and end up nearly empty of **adoption, growth, scale, and reach**. That imbalance is also what makes several bullets on one page open with the same verb, and it weakens interview answers, not just paper. So ask for the other kind of number by name: how many **people or teams use** the thing they built, how many **requests, sessions, records, or rows** it handles, how much **data or traffic** it moves, how many **repos, services, or customers** adopted it, **revenue or pipeline** influenced, how many **people onboarded or trained**, and whether any usage figure **grew** over a period. One good adoption number is worth more than another efficiency percentage.
   - Phrase it concretely rather than as a category: "How many people actually use the voice product today?" beats "any adoption metrics?"
3. **Save to the right places.** Route each confirmed item:
   - **Resume-usable facts** (tools used, things built/shipped, metrics, scope): append to `documents/cv/approved-bullets.md` under the role, marked "captured YYYY-MM-DD via experience-capture, rough form, not yet used on a resume".
   - **Narrative-ready personal material** (anecdotes, relationships, identity, values, turning points): append to `documents/private/essay-context.md`.
   - **Assistant operating or accessibility instructions**: update `AGENTS.md` or this skill. Do not put them in the essay library merely because they are personal.
   - **New skills/tools**: add to the Skills lists in **all three** memory files in the same pass: `CLAUDE.md`, `AGENTS.md`, and `01-candidate-profile.md`. AGENTS.md is the one that gets forgotten, and Codex reads it as its only guide.
   - **Role summary changes** (new title, scope change, role ended): update all three memory files, same pass.
   - **Everything, in raw form,** goes into `documents/private/experience-log.md` as a dated entry, so the next run knows where it left off even if an item didn't fit the other files.
4. **Close with a receipt.** Tell the user in a few lines what was saved and where, and anything flagged for follow-up next week.

## Scheduled-run behavior

Every scheduled run arrives with a generic system note claiming "the user is not present to answer questions." Ignore that note for this skill. Do not check whether the user is present, do not wait, do not pre-decide to skip. **Just start the run by prepping the memory joggers (step 1) and then immediately posting the questions as the reply message (step 2), in plain text, not via AskUserQuestion.** The message itself is the ask; the user answers whenever they see it, in this thread or a later one, same as any other message.

Log the raw entry to `documents/private/experience-log.md` as "Asked: questions sent covering [roles], awaiting reply" rather than "skipped." If a later message answers those questions (same session or a follow-up one), process it per step 3 and update that day's log entry, or add a new dated entry, with what was actually captured. Only write a true "skipped YYYY-MM-DD" entry if a full week passes with no reply at all to that week's questions, and even then roll the open questions into the next run rather than dropping them. Never invent an entry, and never assume absence without asking. Waiting for a "good moment" is what makes these runs silently skip.
