# Application Short-Answer Workflow

The repeatable loop for writing first-person application answers: hackathons, fellowships, scholarships, club apps, "why us" prompts, personal essays, and any free-text question on a form. This is the answer-writing analog of the Resume Tailoring Workflow. The goal is writing that sounds like the user and uses their real material, not resume bullets rewritten as prose and not generic AI filler.

## Sources of truth (read these every time, before drafting)

1. `03-writing-style.md` - voice, the three first-person registers, signature moves, what to avoid.
2. `documents/private/essay-context.md` - the STAR and anecdote library: the user's real stories, the people in them, and the builds worth retelling. This is where the real material lives. Use it, and keep it growing.
3. `01-candidate-profile.md` and the CLAUDE.md profile - facts, skills, dates.
4. `documents/private/approved-answers.md` - the reusable answers/chunks the user has approved before, tagged by prompt type. Pull a prior phrasing when the current prompt matches.
5. `03-writing-style.md`, "Learned from Approvals" section - patterns from what the user approves and how they edit, appended to the style guide over time. Read it so the voice matches what they have actually signed off on.
6. `documents/cv/approved-bullets.md` and the master bullet bank - approved phrasings and the full skill set (including every skill the user has confirmed, named precisely).
7. `documents/library/index.md` - the media library (podcasts, articles, videos the user actually consumed, with insights and their take, saved by the `media-intake` skill). **For "insight/worldview" or "what excites you" prompts, scan this FIRST**: prefer recent, on-theme items where their take is captured. Quote only from the "Exact quotes" section of an item's file; everything else is paraphrase.
8. **the user, for anything the files can't hold.** If the library has nothing that fits, or the best item lacks their take, ask them for 1-2 real, recent inputs (a paper, a podcast take, a video doc) and their actual opinion, then save them to the library via `media-intake` so they're on file next time. Never invent a quote, paper, statistic, or anecdote. If a specific (a prize name, a metric) isn't in the files, ask.

## The loop

1. **Read every prompt and its character/word limit.** Name what it actually asks (background, a team story, a project, motivation, etc.).
2. **Pick the register** per `03-writing-style.md`: casual/energetic for hackathons and tech clubs; polished essay for fellowships and reflective prompts; professional/structured for finance and pre-professional clubs. Do not over-formalize a fun prompt.
3. **Anchor each answer in a real, specific story** from `essay-context.md`. Match the strongest true story to the prompt, and rotate so the same story does not lead every answer. If the file is empty, ask the user for the story instead of inventing one.
4. **Draft in first person, story then lesson then forward application.** Concrete specifics, real numbers, the user's actual opinions and edge. Surface real technical depth by name. Do not rehash resume bullets in sentence form.
5. **For insight/worldview prompts, weave in the real recent reference the user gave** plus their take. This is where they stand out; do not skip it.
6. **Run the `humanizer` skill** on every drafted answer. Kill the tells: rule-of-three lists, tidy parallel structure, slogan closers ("...that way now", "...is where I like to live" if overused), "this one's personal", even mid-length cadence, copula avoidance, manufactured vulnerability.
7. **Check limits programmatically** (count characters; iterate to fit).
8. **Review gate with the user.** Flag any NEW CLAIM before it ships.
9. **Learn from the approval (auto, then tell the user).** When the user approves an answer, or edits it and then approves, update the answer memories automatically and report in one line what was saved so they can veto it:
   - **Reusable answer or chunk** → append to `documents/private/approved-answers.md`, tagged by prompt type.
   - **New narrative-ready personal material** the answer revealed, such as an anecdote, relationship, identity, value, or turning point (not already on file) → add it to `documents/private/essay-context.md` so the anecdote library grows. Current role status belongs in the candidate profiles, raw capture history belongs in `documents/private/experience-log.md`, and assistant operating instructions belong in `AGENTS.md` or the relevant skill.
   - **A style/voice pattern** (something they cut, an opener they rewrote, a rhythm they smoothed, or what an approved-as-is draft did well) → log it in the "Learned from Approvals" section of `03-writing-style.md`. If the user edited the draft, diff their version against it and record the change as the pattern. Promote a pattern to "confirmed" once it has shown up twice.
   - Any resume-style factual **NEW CLAIM** (a tool, metric, or role detail) still goes to `documents/cv/approved-bullets.md` as before.
10. **Re-run the learning audit after submission.** Approval-time updates are not the final closeout because later form choices, resume edits, packet differences, and submission outcomes can add reusable information. After direct submission confirmation and before reporting success, compare the exact submitted packet and the full interaction against the approved-answer ledger, essay context, writing-style memory, approved bullet bank, candidate profile, application profile, application record, and `job_search_tracker.csv`. Save every missing item. If nothing changed, explicitly report that the audit ran and found nothing new.

## Anti-patterns

- Resume bullets rewritten as prose. The answer must be a story, not a list of accomplishments.
- Generic motivation with no personal stake. Anchor "why I care" in a true story, never abstract passion.
- AI-smooth cadence and rule-of-three. Vary sentence length; let one idea run long and the next be short.
- Omitting the real differentiators. Whatever the user has actually won, published, or shipped belongs in the answer; keep that list current in the candidate profile.
- Underselling the technical skill set. Name the real tools and methods instead of flattening them into a category label.
- Inventing specifics. Ask the user for prize names, metrics, and recent references instead of guessing.
