# mymind Intake (automated media library and playbook intake)

**name:** mymind-intake
**description:** Automated daily sweep of the user's mymind (their second-brain app, connected via MCP) that finds new saves relevant to the job search, pulls transcripts and full text via the AnyAPI MCP, and files each item through the existing `media-intake` and `advice-intake` skills. Trigger on: the daily scheduled run, "process my mymind saves", "run the intake", "sweep my mymind", or the user mentioning they saved things in mymind that should be in the library or playbook.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, AskUserQuestion, mcp__mymind__search, mcp__mymind__get_objects, mcp__mymind__list_spaces, mcp__mymind__edit_object, mcp__AnyAPI__search_apis, mcp__AnyAPI__get_api, mcp__AnyAPI__quote_api, mcp__AnyAPI__run_api, mcp__AnyAPI__read_result, mcp__AnyAPI__get_balance

---

## What this skill is

`media-intake` and `advice-intake` define WHAT gets saved and HOW it is filed. This skill automates WHERE the items come from and HOW their content gets fetched without a browser. It discovers new mymind saves, fetches the words via AnyAPI, then hands each item to the parent skill's flow. **Read both parent SKILL.md files every run and follow their storage formats, templates, and rules exactly. Do not restate or reinvent them here.**

A save in mymind is a save. The 2026-08-19 save-as-endorsement directive applies unchanged: The user saving an item means its message resonates with them. Batch mode, no interruptions, questions collected at the end (or, unattended, written to the pending-review file).

## Files this skill owns

- **State:** `documents/intake/intake-state.md`. Holds (a) the processed-ID ledger: one line per mymind object ever handled, with date, disposition (`library` / `playbook` / `both` / `tracker` / `skip` / `failed`), and the repo file it produced; (b) the query battery (see Discovery) with each query's last-known total; (c) the last-run date. IDs are tiny; never prune the ledger.
- **Run report:** `documents/intake/reports/intake-YYYY-MM-DD.md`. What was filed, skipped, and failed, with one line each, plus API spend. This is the record the user reads.
- **Pending review:** `documents/intake/PENDING-REVIEW.md`. Only what genuinely needs a decision from the user. Append, dated. The user clears it in any session; the entry is then removed. **The bar is narrow and was narrowed by the user in a past run after a run over-filled it. See "What does and does not go to pending review" below.**

The parent skills own everything under `documents/library/` and `documents/playbook/`, plus the beliefs file. Write those exactly per their specs.

## What does and does not go to pending review

A past run put six entries in the file. The user cut it to two. Their corrections are now the standing rule.

**Goes to pending review:**
- A proposed CLAUDE.md edit. Still never applied by a run.
- **A conflict between a saved piece of advice and one of the user's own rules.** That is the case worth their attention, because one of the two has to give.
- An item that contradicts something already on file in `stated-beliefs.md`.
- An item whose content could not be retrieved, once the routes in "Fetching the words" have actually been tried and named.

**Does NOT go to pending review:**
- **Conflicts between two sources.** the user's words: "It's fine if sources conflict. It's fine for ambiguity to exist in this world. It's not something that you necessarily need to flag if it's just sources." Record both positions in the item files and move on. Do not ask them to arbitrate between two strangers on the internet.
- **An unverified number.** Flag it in the file's fact-check section as unverified and stop. CLAUDE.md already bars repeating a number flagged as unverified, so that flag is the entire mechanism. Do not invent a separate "do not print" ban on top of it, and do not ask the user to ratify one. They called that an overstep, and they were right: it duplicated a rule they had already approved and handed a decision back to them for no reason. Fact-check findings against a primary source are different and stay in the file as findings.
- Routine coverage, tooling, or battery notes. Those belong in the run report.

The test: does this require a choice only the user can make? If not, it goes in the run report.

**Answered questions do not come back.** When the user declines a rule proposal, record the ruling and their reason in the source file and do not re-propose it when another source arrives. Declined in a past run: open-source contribution as a verifiable credential, saved three times, agreed with as a claim, refused as a CLAUDE.md rule because the repository is not only for applying to jobs.

## Discovery (how new saves are found)

**Hard facts about mymind search. Design around them; do not rediscover them:**

- No date sort and no date filter. `created:` is not a filter; it silently matches nothing.
- Results cap at 50. Above 50 the call returns `too_many_results` with the exact `total`.
- Valid `type:` filter values: `Video`, `Article`, `WebPage`, `Note`, `PDF`, `Image`, `Tweet`. Display types like `InstagramReel` and `YouTubeVideo` are NOT filterable; both live under `type:Video`.
- ⚠️ **`-tag:` exclusion applies AFTER the 50-result window.** Excluding a top-ranked item shrinks the page instead of backfilling it (verified: limit 3 with the top item tagged returned 2 results). So tags CANNOT make room in a query. Never use tag exclusion for dedup. Dedup happens against the state file's processed-ID ledger only.

**The method that works: an enumerable query battery.**

1. The battery lives in the state file. Every query in it must be *enumerable*: its `total` is 50 or less, so one call returns the complete slice. Baseline shape: `type:X && <topic term>` across the topic vocabulary below, for types Video, Article, WebPage, Tweet, PDF, Note.
2. Each run, execute every battery query with `limit: 50`. Collect all returned IDs. New items = IDs not in the processed ledger.
3. **Self-healing:** when a query returns `too_many_results`, split it into narrower `&&` slices until every slice is enumerable, replace the battery row, and record the change in the run report. Watch per-query totals for drift toward 50 and split early.
   **A newly added row gets a full diff on its first execution, not just a total (standing rule).** A past run added `type:Video && engineer`, recorded its total, and did not diff its IDs against the ledger; three in-scope saves sat unhandled until the next day found them. Recording a new row's total is not the same as processing it. Treat the first run of any new or re-split row as a backfill of that whole slice.
4. Run one semantic catch-all pass on top (`semantic: true`, a query like "career advice, job search tactics, AI industry commentary, startup building") and diff those IDs too. Best effort only.
5. **Known coverage limit, stated honestly:** an in-scope save matching none of the battery terms can be missed. The run report's footer must carry one line naming the battery size and this limit. When the user mentions an item that was missed, add the term that would have caught it to the vocabulary.

**Topic vocabulary (seed; grow it in the state file, never here):** career, job, internship, resume, interview, recruiter, hiring, outreach, networking, negotiation, startup, founder, vc, venture, ai, agent, llm, eval, machine learning, engineer, sales, gtm, marketing, product, growth, debate, journalism.

## Classification (per item, from title + mymind summary)

- **PLAYBOOK** (route to `advice-intake`): the item tells the user how to do the job search better. Test from the parent skill: it should change *how the work gets done*.
- **LIBRARY** (route to `media-intake`): ideas, commentary, stories, technical or market takes. Test: The user would want to *talk about* it.
- **BOTH** (rare): file the advice claims in the playbook and the worldview substance in the library, one source file each per the parent specs.
- **TRACKER** (route to the opportunities pipeline; lane approved by the user 2026-08-25): the save is a *target*, not an idea or advice — a job post, careers page, program or fellowship listing, conference, grant, or hiring announcement. Append one row to `opportunities/verification-backlog.md` in its table format (`| Lead | Reason | Prior state line | Link |`, prior-state column = `mymind`, reason = "Saved in the user's mymind; live status and eligibility not verified."), using the item's source URL. Tag the mymind object `claude-tracker`; ledger disposition `tracker` with the backlog path. The daily tracker owns verification from there; this skill NEVER marks a target verified, live, or eligible, and never writes to the tracker's other files. A save whose only content is a person (a recruiter's profile with no named role or program) is a contact, not a target: SKIP it.

  **Targets named inside an item also go to the backlog.** The lane is no longer only for saves that *are* a target. When a reel, video, post, or article the user saves about jobs *names* an opportunity, that opportunity gets its own backlog row even though the item itself files to the playbook or the library. Their words: anything from reels and other media that they save about jobs should get added to the backlog. So a reel of career advice that happens to name four fellowships produces one playbook file and four backlog rows, and the ledger disposition stays `playbook` (or `library`) with the backlog path noted after it. The mymind tag stays the intake tag; do not add `claude-tracker` to an item that filed as advice.

  **What counts as a target, and what does not.** A target is a named thing you apply to: a program, fellowship, scholarship, grant, conference, accelerator, a company that is hiring, or a specific role. A tool, job board, community, or Discord named as a way to *find* work (Forage, RippleMatch, Simplify, a careers Discord) is not a target; it stays in the playbook as advice. Where a listed name is ambiguous, add the row. Row format is unchanged, the reason line says the name came from a saved item rather than from a listing the user opened, and nothing is ever marked verified here. Group a run's seeded rows under one dated heading so the user can strike the batch in one line.
- **SKIP:** design inspiration, aesthetics, shopping, personal, tools-to-try with no career relevance. One line in the run report; no files. The user's "Design Inspiration" and "Website Builders" spaces are skip territory by default.

When unsure between SKIP and either intake lane, lean toward intake; a wrongly-skipped save is invisible, a wrongly-filed one is one line in the report the user can veto.

## Fetching the words (AnyAPI, no browser needed)

Wallet check first: `get_balance`. Below $1.00, fetch only the free routes (WebFetch) and flag the rest as `failed: wallet low` in the report and pending-review. **Per-run spend cap: $1.00.** Beyond it, stop fetching, carry the remainder to the next run, and say so in the report.

| Source (from the item's URL) | Route | Cost, approx |
|---|---|---|
| YouTube | `run_api` sku `youtube.video_transcript_full`, input `{"url": ...}` | $0.003 |
| Instagram reel/video | `run_api` sku `instagram.reel_transcript`, input `{"url": ...}` (returns caption + transcript; slow, p50 ~37s) | $0.031 |
| TikTok | sku `tiktok.video_transcript`, fallback `tiktok.video_transcript_full` | $0.002-0.018 |
| LinkedIn post | sku `linkedin.post`; video posts add `linkedin.post_transcript` | $0.001-0.002 |
| X / Twitter | sku `twitter.article` for long-form; otherwise search the catalog for the tweet-by-URL sku | $0.001 |
| Article / blog / webpage | WebFetch first (free). Shell or paywall: sku `web.scrape` (markdown out) | $0.0007 |
| Podcast page | WebFetch the show notes; else per media-intake's podcast fallback chain | free |

Mechanics: transcripts SKUs are `heavy` — pass `fields`, `jq`, or `max_items` to trim, and `read_result` to re-slice a paid result instead of re-running. `quote_api` validates input without charging. Latency p99 runs to ~47s on reels; set patience, not retries. Never let a paraphrase into an "Exact quotes" section; the reel caption is quotable, recognition output of names and jargon is not (check `isAutoGenerated` / `isAiGenerated`).

### Extraction discipline (standing rule after wasting $0.062)

**A wrong field path returns null, not an error, so it is indistinguishable from an empty source.** On 2026-08-25 a run passed a guessed `jq` filter to `instagram.reel_transcript`, read four nulls, reported to the user that Instagram transcripts come back empty, and proposed dropping reels from the pipeline. The transcripts were there in full the whole time. Three rules follow, in order:

1. **Never write a `jq` or `fields` filter from memory or assumption. Call `get_api` for the SKU first.** It is free, it charges nothing, it takes one call, and it prints the exact output schema. Do this even when the paths look obvious. The schemas below cover the common SKUs; anything not listed gets a `get_api` call before the first paid run.
2. **`items >= 1` with all-null extracted fields means the filter is wrong, not that the source is empty.** A genuinely empty result reports `found: false`, or returns the record with an empty string in the text field. Never conclude "no transcript available", never mark a file `source fidelity: low`, and never report a source-side failure to the user on the strength of nulls alone.
3. **When output looks wrong, `read_result` before paying again.** It re-slices the cached paid result for free with any filter, but **only for about 15 minutes**. Re-slice immediately, in the same turn. After the cache expires the only way back is paying twice for the same data, which is exactly what happened.

**Confirmed output shapes (verified against `get_api`, 2026-08-25):**

| SKU | Envelope | The field you actually want |
|---|---|---|
| `youtube.video_transcript_full` | `{found, data: {...}}` | `data.transcript` (full joined text). Also `data.segments[].text` with `startSeconds`/`endSeconds`, plus `data.channel`, `data.title`, `data.durationSeconds`, `data.isAutoGenerated`, `data.isAiGenerated` |
| `instagram.reel_transcript` | `{found, data: {items: [{...}]}}` | `data.items[0].text` (full transcript) and `data.items[0].caption`. Note the extra `items` array. Also `ownerUsername`, `durationSeconds`, `segments[]` |
| `twitter.tweet` | `{found, data: {...}}` | `data.text` (the post body). Also `data.authorId`, `data.createdUtc` (epoch SECONDS, not ms), `data.likes`, `data.views`, and `data.media[]` with `type`, `url`, `videoUrl`. **Verified against `get_api` 2026-09-01.** ⚠️ A post whose substance is in attached screenshots returns only its headline in `data.text`; check `data.media` before concluding the post is thin, and there is still no image-to-text route in the catalog |

Both nest everything under `data`. Neither exposes a top-level `.transcript` or `.caption`, which is the exact mistake that was made. Add a row here whenever a new SKU is used for the first time.

**Reporting rule.** Cost honesty covers mistakes, not just spend. When a run wastes money, the run report says so in the spend line and explains what went wrong, rather than quietly absorbing it.

## Writeback to mymind (markers, not filters)

After handling an item, `edit_object` with `addTags` exactly one of: `claude-library`, `claude-playbook`, `claude-tracker`, `claude-skip` (BOTH gets both intake tags). These are human-visible markers so the user sees state inside mymind. They are NOT used by discovery (see the window fact above). Never delete a mymind object, never edit its title, summary, or notes, never move it between spaces.

## Unattended discipline (scheduled runs)

- Never edit CLAUDE.md. RULE proposals go to pending-review with the exact quoted current text and proposed replacement, per `advice-intake`.
- Never resolve a CONTESTED claim; record both sides and queue it.
- Beliefs entries stay **Raw** tier with a citation, per `media-intake`. Upgrades require the user's words.
- Never fabricate a quote, author, statistic, or credential. An unreadable item is queued, not guessed.
- Commit nothing to git; write files only.
- If the mymind or AnyAPI tools are absent from the session (connector not attached to a headless run), write a one-line report saying which tool was missing and stop. Do not fall back to guessing content.

## Run shape

1. Read parent skills, state file, `documents/playbook/index.md`, `documents/library/index.md`, `documents/private/stated-beliefs.md` (contradiction checks need it).
2. `get_balance`. Execute the battery + semantic pass. Diff against the ledger.
3. Classify each new item. Fetch content by the table. File via the parent flows. Tag the mymind object. Append the ledger line.
4. Write the run report; append pending-review items; update battery totals and last-run date.
5. Interactive runs: give the user the parent skills' batch digest in chat. Scheduled runs: the report file is the digest; keep the completion summary to counts and the strongest one or two items.

## Rules

- Global Writing Rules apply (no em-dashes, plain language).
- Batch is normal: twenty items means twenty files, one report, zero interruptions.
- Cost honesty: the report states actual spend per run, from `run_api` results, and the remaining balance, **including money wasted on mistakes**.
- **Never guess an AnyAPI field path.** `get_api` first, `read_result` before re-running, and all-null fields mean a bad filter rather than an empty source. See Extraction discipline above. This rule exists because breaking it cost real money and produced a false report to the user.
- This skill discovers and fetches. The moment filing logic here disagrees with a parent skill, the parent skill wins; fix the drift by editing this file, not by improvising in the run.
