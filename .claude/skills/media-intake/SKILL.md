# Media Intake

**name:** media-intake
**description:** the user drops a link (or file) to a podcast, article, video, paper, or talk they found interesting. This skill pulls the transcript or full text, distills the insights worth keeping, treats the save itself as the user agreeing with the piece, and saves it all to the media library so future application answers and interview prep can draw on real things they actually consumed. Trigger on: "save this", "add this to my library", "interesting podcast/article/video", "log this episode", "I listened to / read / watched X", or any pasted media link with a comment that they found it worthwhile.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__list_connected_browsers, mcp__claude-in-chrome__select_browser

---

## Why this exists

The answer-writing spec (08-application-answers.md) requires a real, recent reference plus the user's take for insight/worldview prompts, and interviews reward being conversant in what's actually happening in AI, markets, and policy. Today that knowledge evaporates unless the user happens to remember it under pressure. This skill is the catch basin: anything they save goes in, on the understanding that saving it means they agree with it, and it comes back out exactly when a prompt or interviewer asks "what have you been reading/listening to lately?"

## Storage

- **Library folder:** `documents/library/`, one file per item: `YYYY-MM-DD - <short-slug>.md` (date = intake date).
- **Index:** `documents/library/index.md`, one table row per item (date, title, type, themes, comment?, file), where "comment?" is `saved` when the endorsement rests on the save alone and `commented` when the user gave words of their own. Newest first. Update it on every intake; this is what other workflows scan.

## The intake flow

1. **Identify the item.** From the link or file: title, creator/author/show, publish date (verify via the page or a quick search; don't guess), type (podcast / video / article / paper / talk / thread).
2. **Get the words.**
   - **Article / paper / blog post:** WebFetch the text. If the fetch returns a shell or a paywall, open it in Chrome and use get_page_text. Save the key passages, not necessarily the whole text.
   - **YouTube / video:** open the video page in Chrome, expand the description, open the Transcript panel (More → Show transcript), and read it via get_page_text or read_page. If no transcript exists, fall back to the description plus a web search for a written summary or coverage, and mark the file "no transcript available, insights from secondary sources".
   - **Podcast:** check the episode's show-notes page for an official transcript; else search "<show> <episode> transcript" (many are on the show site, Podscribe, or fan wikis); else use detailed show notes / coverage, marked as secondary.
   - **Verbatim discipline:** in the saved file, distinguish **exact quotes** (safe to quote in an essay, with speaker attribution) from **paraphrase** (must never be presented as a quote). This feeds the never-fabricate-a-quote rule downstream.
3. **Distill.** Write the insight section: the 3-7 ideas actually worth keeping, each concrete enough to reuse (a claim, a framework, a number with its source, a contrarian position, a story told in the piece). Name the people who said what. Skip throat-clearing summary; capture what the user would want to bring up in a conversation.
4. **Treat the save as the endorsement.** the user saving something means its message resonates with them (their directive, 2026-08-19). Do not ask them to react to each item; across a batch of twenty that is overkill. Record the save as agreement with the item's main argument and keep going:
   - The item file's **The user's position** section states what they are on record as agreeing with on the strength of the save, and says plainly that no separate comment was given.
   - A **Raw**-tier entry goes in `documents/private/stated-beliefs.md` with a citation back to the item file. Raw is the right tier: the idea is fully in play and should surface whenever it fits a prompt, but the elaboration has to come from them, so a draft built on it asks them to phrase it before it ships.
   - If they do comment, their comment outranks the save. Record it close to verbatim in the same section and upgrade the beliefs entry to Verbatim or Paraphrase.
   - A save endorses the message, not every factual claim inside it. Fact-check flags still get raised and still get recorded.

   **Ask them only when the save alone cannot settle it.** Three cases: the item contradicts a belief already on file in `stated-beliefs.md`; a draft is about to quote them as holding the position rather than merely raising it; or the item is one they sent without saving, where there is no save to read intent from. Collect these in one round at the end of a batch instead of interrupting each item.

5. **Tag themes** from their real interest map so retrieval works: `ai-evals`, `agents`, `legal-tech`, `voice-ai`, `startups/0-to-1`, `vc/markets`, `geopolitics`, `ai-policy`, `defense`, `climate`, `health`, `journalism/debate`, `career`, `other`. Multiple tags fine.
6. **Update the index** and give the user a 3-5 line digest of the piece in chat (this is the stay-well-informed part), plus one line on what was saved.

## Per-item file template

```
# <Title>
- Source: <URL>
- Creator/speakers: 
- Published: <date> | Saved: <date>
- Type: podcast | video | article | paper | talk
- Themes: 
- Transcript: full | partial | none (secondary sources)

## Insights (attributed; paraphrase unless quoted)
- 

## Exact quotes (verbatim only, safe to cite)
> "..." (<speaker>)

## The user's position
(What the save puts them on record as agreeing with, in one or two lines, plus "Saved without comment" or their words close to verbatim if they gave any.)

## Might be useful for
(prompt types or interview topics this maps to, e.g. insight/worldview, "what excites you about AI", eval-methodology talking point)
```

## Retrieval (for the other workflows)

When drafting an insight/worldview answer or prepping an interview, scan `documents/private/stated-beliefs.md` first (it holds every take with provenance and cites the library files), then follow citations into `documents/library/` for exact quotes and fact-check flags. Every item in the library is one they chose to keep, so its argument can be used as a position they hold. What still may not happen is printing an elaboration they never gave: use the idea, and ask them to phrase it before a draft quotes them on it.

## Rules

- Follow CLAUDE.md's Global Writing Rules (no em-dashes).
- Never invent or clean up a quote; if the transcript is garbled, paraphrase and mark it as paraphrase.
- The user's take is theirs; record it, don't improve it.
- Batch intake is the normal case, not the exception. Twenty saved items means twenty files and zero interruptions; the only questions that go back to them are the ones step 4 lists.
