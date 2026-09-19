# Artifact Specs

Canonical anatomy for the three interview artifacts. Use these exact section names. The point of a fixed vocabulary is that the user can open any prep from any month and find the same thing in the same place, and that a section can be scanned for without guessing which of six synonyms that document happened to pick.

## Folder and file naming

```
interviews/YYYY-MM-DD - <Company> <assessment or round>/
  facts.md
  full-prep.md
  desk-sheet.md
  format-research.md (optional, when format research is substantial)
  log.md (written after the interview)
  practice/ (optional, for runnable practice files)
```

The date is the interview or deadline date, not the date of writing. Use the employer's own name for the assessment ("PRVI", "Virtual Job Tryout", "HireVue"), not a generic label.

Loose files already in `interviews/` stay where they are. Do not retrofit them; the naming convention applies going forward.

## Fixed vocabulary

Without a fixed vocabulary the same idea picks up several names across artifacts. These are the names.

| Idea | Use this | Never these |
|---|---|---|
| The decision up front | `## The answer first` | Bottom line, Summary, TL;DR |
| Employer-confirmed detail | **Confirmed** | Verified, Certain, Known |
| Candidate accounts and third-party reports | **Reported** | Best available, Strong signal, Historical, Likely |
| What the user may not claim | `## Boundaries` | Red lines, Landmines, Truth boundary, Technology boundary, Traits that would contradict |
| Agreement with the submitted packet | `## Packet consistency` | Application commitments, Application consistency rules, Submitted-resume consistency |

Do not number top-level sections. Numbering in one prep and not the others makes cross-document reference harder rather than easier.

---

## facts.md

Two to four thousand characters. The single source of truth. Written first, before any research or answer writing. Every number, name, date, and claim boundary in the other two files traces back to a line here.

This file is a build-time input, not something the user reads on the day. The desk sheet is the artifact for that.

```
# <Company> <assessment> - facts
Prepared <date> for: <role>, requisition <id>
Application submitted: <date> | Interview or deadline: <date and time, with timezone>

## Logistics
Platform, link, window, personal deadline (set earlier than the real one),
account email, attire, support contact, accommodations contact,
named human if the invitation names one.
Add one line on whether the employer permits notes during the interview,
quoting them where they say. Nothing more than a line.

## Format
One line per detail, each tagged Confirmed or Reported. Never blended.
Where reported accounts disagree, say so and state which version to plan for.

## Packet consistency
What is on the exact submitted PDF: roles, dates, metrics, graduation year
presented, GPA as submitted, file name and SHA-256 where known.
Then what is true but absent from that page, and the right way to handle
a question that would otherwise walk into it.

## Boundaries
The do-not-claim list. Named technologies, responsibilities, scope, and
traits that are not defensible. One line each, with what to say instead
where a substitute exists.

Scoped to this packet, and it does not leave this folder. Written against
the exact submitted PDF, not against the bullet bank, and never copied into
the ledger, the application profile, the Candidate Profile, approved-answers,
or stated-beliefs. It expires with the interview; the next one is written
from its own packet.

## Numbers
Every figure that may be spoken, in the exact form used elsewhere in the repo.
This is the anti-drift table; a number that appears here appears nowhere else
in a different form.

## Unverified
Anything researched but not confirmed. Kept visible rather than dropped.
```

---

## full-prep.md

Fifteen to fifty thousand characters. Length scales with how much of the assessment is spoken answers rather than demonstrated skill; a coding test's full prep is legitimately a third the size of a recorded behavioral set's.

Section order, with the optional ones marked:

```
# <Company> <assessment> full prep
Prepared <date> for: <role>, requisition, submission date, deadline,
graduation year presented, location preferences submitted.

## The answer first
The decision, not a summary. What must happen, by when, and what the single
biggest risk is. If there is a logistics table, it goes here.

## Format
Confirmed and Reported, in that order, never blended. Platform mechanics to
button level where the platform is scored. What the scoring model actually
measures, researched rather than assumed.

## What they are measuring
Built from the posting's responsibilities block per workflow step 5, not from
a generic competency list. One row per responsibility: the responsibility as
written, the competency it tests, the story attached, and the signal strength.
A responsibility with no story attached stays in the table marked as a prep
gap rather than being dropped. For a multi-discipline role, keep one row per
discipline as well, including the rows where the user is genuinely weak.
Where no written posting exists, say so here in one line.

## Your positioning in one sentence
A blockquote. Always present, always exactly one sentence.

## Company facts you can use
Hard-verified only, with the rationing rule stated: one is enough, two is
showing off. Include what must not be said, such as a title nobody publicly
holds. Cite sources inline.

## Packet consistency
Quoted from facts.md, not restated in different words.

## Boundaries
Quoted from facts.md. Where a trap exists, a two-column do-not-say and
say-instead table.

## Question bank
Derived from the responsibility rows above, then ranked: near certain, likely,
possible. Likelihood follows how much of the posting a question covers. Then
an explicit not-expected list so preparation stops somewhere.

## Answers
The largest block. Storage grade chosen per the workflow step 7 rule.
Each answer followed by why it works, its guardrail, and its 60-second
compression where the format is timed.

## Story bank
Table: story, numbers, best used for, boundary. One line each.

## Flash cards (technical and case assessments only)
## Practice set (optional; original scenarios only, labeled as such)
## Rehearsal plan
Timeboxed, sized to the assessment, one block at a time.

## Day-of checklist
Before opening the link. During. Between modules if there is more than one.
If something breaks.

## Afterward
The write-back list from workflow step 11, named explicitly.

## Sources
A terminal list of URLs. Always present, even when links also appear inline.

## Unverified
Quoted from facts.md.
```

---

## desk-sheet.md

Three to six thousand characters, targeting one printed page. Built by compressing the full prep at 6:1 to 12:1. Every sentence of prose is deleted. What survives is decisions, numbers, prohibitions, and lookups.

```
# <Company> <assessment> desk sheet

## Logistics
Time, link, window, deadline, account, attire, support contact.

## Positioning
The one sentence, verbatim from the full prep.

## Answer shape
One line. The beat structure for this format.

## Question to story
A lookup table. Question type in the left column, story and its headline
number in the right.

## Numbers
The figures, bare.

## Boundaries
The do-not-claim list, bare.

## Questions to ask (live conversations only, pick two)
## Close (live conversations only)
## Final checks
The last routine before starting.
```

For a live conversation, the desk sheet carries the named interviewer, the meeting link, the two questions to ask, and the thank-you plan; the async formats carry none of those and carry platform mechanics instead.

## Rendering to PDF

A desk sheet meant to be printed can be rendered with reportlab as a single color-coded letter page. Keep the first build script under `interviews/` and generalize from it rather than writing a new one each time, and only build a PDF when the user says they want one on paper.
