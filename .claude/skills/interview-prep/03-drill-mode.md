# Drill Mode

Scored practice. Claude plays the interviewer, the user answers, Claude scores the answer against a rubric and names one thing to fix, then the user re-takes. The rubric generalizes the 10-point scale from the FTI PRVI prep, which is the only place in the repo where practice was ever actually scored.

**This is preparation, never live.** Drill mode runs before an interview, on original questions Claude writes. It never runs during one, and it never uses questions recovered from a live assessment.

## Starting a drill

Ask three things, briefly, then start:

1. Which interview, or general practice if there is none scheduled
2. How long they have
3. Text or spoken

If a prep folder exists, pull the questions from its ranked question bank, hardest tier first. If not, build a set from the role and the memory files.

**Spoken drills are worth more than typed ones** for anything that will be delivered out loud, because the failure modes are different: typing hides filler words, pace, and the habit of restarting a sentence. When the user is typing, score the content and say plainly that delivery went unscored.

## The loop

One question at a time. Never a list.

1. Ask the question exactly as an interviewer would, with no preamble and no hints.
2. Wait for the whole answer. Do not coach mid-answer.
3. Score it. Show the rubric line by line, the total, and the single highest-value fix.
4. If the score is below 8, ask for a re-take of that same question.
5. Stop after two clean takes. Past that, delivery gets worse rather than better, because it starts sounding rehearsed.

Between questions, say nothing beyond the score and the fix. Encouragement between every answer makes the scores meaningless and makes a real weakness harder to hear.

## The rubric

Ten points, five dimensions, two points each. Score honestly. A 6 that names the real problem is more useful than an 8 that protects their mood, and they cannot fix what does not get flagged.

| Dimension | 2 points | 1 point | 0 points |
|---|---|---|---|
| **Answers the question** | Addresses what was actually asked, in the first sentence | Addresses it eventually, after setup | Answers a nearby question instead |
| **Specific evidence** | Named tools, named institutions, real numbers | Some specificity, some generic phrasing | Category labels and adjectives |
| **Structure** | Clear shape, listener always knows where they are | Shape present but wanders once | No discernible structure |
| **Length and pace** | Within the target window, steady | Over or under by up to 25 percent | Well outside the window, or rushed |
| **Ties back** | Ends on relevance to this role, unforced | Relevance implied | Ends on the anecdote, no connection made |

**The target window, when the format does not set one.** Live behavioral answers run **30 to 90 seconds**. Under 30 and the answer has no evidence in it; over 90 and the interviewer is waiting for the point. The Length and pace row above already scores against a window, and until now no default was written down anywhere, so "concise" was being judged by feel. Where a format publishes its own clock, that clock wins: recorded one-way answers stay on the 100 to 110 second beat in step 7 of `SKILL.md`, and a case or technical walkthrough runs to its own structure. State the window at the top of the drill so the user knows what they are being scored against.

**Two automatic caps, applied after scoring:**

- Any claim crossing the do-not-claim list in `facts.md` caps the answer at 4, regardless of quality. Say which claim and what the defensible version is. This is the failure that costs offers, so it does not get graded on a curve.
- Any number that disagrees with the `## Numbers` block caps the answer at 6. Consistency is the whole point of that table.

## Feedback shape

Three lines, always in this order. Longer than that and the fix gets lost.

```
8/10. Rubric: 2 / 1 / 2 / 2 / 1
Strongest: the headline metric landed in the first fifteen seconds.
Fix: you never said why 90 percent mattered. Add "which took expert review
from 120 hours to 12" and stop there.
```

Name one fix. When there are three problems, name the one whose repair improves the answer most, and hold the others for the next take.

## Question selection

Weight toward what is uncomfortable, not what is polished.

- Every question from the near-certain tier
- Every question that stumped them in a past interview, from the logs in `interviews/`
- The known-hard recurring ones: the multi-role allocation question, a real weakness, a failure, the graduation-timeline question, and "why this company"
- One curveball per session, unannounced

**"Why this company" gets drilled every session.** It is the most predictable question in any interview and the one most often answered with a compliment instead of a reason. Score it hard on specificity: if the distinguishing trait named would survive being applied to a competitor, it fails the specificity line and the answer caps at 6.

## Closing a session

Report, in a few lines:

- Questions drilled and the score trend
- The two weakest answers and what specifically to fix
- Any answer that scored 9 or 10, which goes to `documents/private/approved-answers.md` after the user confirms the wording
- Anything they said that is a new fact, which goes to `documents/private/essay-context.md`

Then tell them what got saved in one line.
