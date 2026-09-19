# Interview Content Library

**Workflow lives elsewhere.** How an interview gets prepared, what artifacts get built, and how the loop closes afterward are all specified in `.claude/skills/interview-prep/SKILL.md`. That skill is the process. This file is the content it draws on: the durable, cross-company material that does not change from one interview to the next.

Keep the two separate. When something is true about the user regardless of employer, it belongs here. When it is a step in preparing for one specific interview, it belongs in the skill.

## What to read before using this file

| File | What it holds |
|---|---|
| `documents/private/approved-answers.md` | Answers the user already approved, keyed by company and prompt type. Reuse the wording rather than rewriting it. |
| `documents/private/essay-context.md` | The real anecdotes and a themes index that works as a STAR lookup. |
| `documents/private/stated-beliefs.md` | Every position the user holds, with a provenance tier (Verbatim, Approved, Paraphrase, Raw) and a source. The canonical file for worldview and opinion questions; where an entry cites a media-library file, read that file for exact quotes and fact-check flags first. |
| `documents/playbook/index.md` | Advice claims tagged `interview-behavioral`, `interview-technical`, `negotiation`. Apply CONTEXT claims as judgment. CLAUDE.md wins on conflict. |
| `documents/library/index.md` | Media the user actually consumed, for "what have you been following lately". Only rows where the Take column says Yes. |
| `interviews/` | Every prior interview. Reuse what worked, drill what stumped. |
| `01-candidate-profile.md` | The canonical facts. Every number below traces to it. |

## Story bank

Empty until it is filled from the candidate profile. Every figure here must be confirmed in that profile. Do not add a number to this table that is not confirmed there, and do not vary a number's form between documents; a figure that shifts between tellings is one the user cannot say with confidence.

Add one row per durable story, using the columns below. Aim for coverage rather than volume: a measurable technical win, a system the user architected rather than contributed to, a customer or stakeholder story, a leadership-at-scale story, a research story, a hands-on build, and a failure with a real cost.

| Story | Numbers | Best used for | Boundary |
|---|---|---|---|
| `<short label>` | `<confirmed figures, in the exact form they are said aloud>` | `<the question types this story answers>` | `<what not to claim: scope, seniority, authorship, or detail to hold back unless asked>` |

The Boundary column is the one that gets skipped and the one that matters. It is where you record that a role was an internship, that a result was influenced rather than owned, that a contribution was shared with teammates, or that a technical detail should be held back unless the interviewer asks for it.

**Recurring personal narratives** live in `documents/private/essay-context.md` with a themes index. Pull from there rather than restating them here. One caution: a personal-hardship story used as a generic opener does not distinguish one employer from another, and using it that way weakens it.

## Recurring tough questions

Real guidance where the answer is settled. Where it is not, the question is marked open rather than filled with a placeholder, because an unfilled placeholder in a prep document is worse than a visible gap.

**"Why are you doing so many things at once?"** Near certain for anyone carrying concurrent roles. Answer it directly rather than defensively: name the layer of the problem each role covers and the convergence between them, rather than promising to narrow later.

**"You do not have X."** Acknowledge it in one sentence, do not apologize, and bridge to the nearest real thing plus what they did about the gap. The bridge has to be honest; adjacent technology is not the same as the thing asked for, and claiming otherwise is caught immediately.

**"What is your biggest weakness?"** Pick a real one the user is already acting on, and lead with the action. A weakness with no concrete narrowing underway reads as a rehearsed non-answer.

**"Where do you see yourself in five years?"** Open until the user answers it. Leave it visibly open rather than filling it with a placeholder.

**"Walk me through your graduation timeline."** Answer with the year presented on that application and nothing else. Check `facts.md` for which one was submitted, and do not volunteer an alternative the packet does not claim.

**"Why this company?"** Never generic, and never a compliment in place of a reason. Name one real distinguishing trait a competitor could not claim, specific enough to survive a follow-up. If the trait would apply equally to their nearest competitor, the answer has failed. Close on what they bring back to it, which is the move most candidates skip.

**"Tell me about a failure."** Use a real one with a real cost, where evidence proved the user wrong and the work changed as a result. A failure with no cost and no change is not an answer.

**"Tell me about a disagreement."** Competitive argument is not the same as disagreeing with a colleague, so prefer a story where the work materially changed because someone pushed back on it.

## Questions to ask

Pick two, tuned to who is in the room. A question that could be asked of any company is a wasted turn.

**A hiring manager or someone on the team:** how they will know they are doing well three months in (asks for the measure, not a description, and three months is roughly a whole internship); what tends to trip up new people; what the first six months would actually look like; the biggest thing slowing the team down right now; how work gets from idea to production; where this role's decisions stop and someone else's begin.

**In a final round with a hiring manager,** asking whether they have any hesitations they could address is permitted, because at that point they hold a real opinion and the objection may still be fixable. Never ask it at a recruiter screen or an early round, where the honest answer does not come and the question spends a slot for nothing.

**A recruiter:** the process and timeline; who else they would meet; what distinguishes people who do well in this program.

**A senior engineer or researcher:** what they would change about the current stack; how they decide what not to build; what surprised them about the problem after joining.

**Always close by confirming next steps and timeline.** It is part of the interview and it is the part most often skipped.

## Delivery basics

- Answer first, then support it. Both a human skimming and a transcript parser reward the shape.
- Numerals, named tools, named institutions. Specificity is what makes a claim checkable, and checkable is what makes it credible.
- Silence for a few seconds before answering is fine and reads as considered.
- Ask for clarification on a vague question rather than answering a nearby one.
- Match length to format: roughly 90 seconds for a recorded behavioral answer, shorter in conversation where the interviewer can follow up.
