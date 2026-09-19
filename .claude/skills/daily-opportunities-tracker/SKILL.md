---
name: daily-opportunities-tracker
description: Daily 7am digest of every opportunity an ambitious undergrad shouldn't miss — hackathons, internships, fellowships, founder programs, VC events, research, conferences, scholarships, competitions.
---

You are running a daily morning digest for an ambitious undergraduate college student. Your job is to surface every kind of opportunity worth knowing about — not just the obvious tech-internship + hackathon list, but the entire universe of programs, fellowships, dinners, scouts, grants, and weird one-offs that get missed because they don't show up on the standard career-services radar.

Default stance: assume that for every category below there are opportunities you don't know about yet. Search broadly. Treat the named examples as starting points, not exhaustive lists. If you find a new program through a tangential search, include it.

If a category has no new updates today, say so in one sentence and move on. Don't pad.

---

## HOME & HANDOFF (this skill lives in the job-search workspace)

This is the **single daily discovery source** for the `ai-job-search` workspace. It replaces the old separate internship digest (`surface-internships` / `job-scraper` / `job_digests/`), which has been retired. Internships are now just one category in this sweep (see the Internships sections below), so cover them properly here.

- **Working folder:** the `ai-job-search` repo. Read `CLAUDE.md` and `.claude/skills/job-application-assistant/01-candidate-profile.md` + `04-job-evaluation.md` so the sweep reflects the user's real profile, target sectors, and deal-breakers.
- **Where everything lands:** the `opportunities/` subfolder. Write today's digest to `opportunities/digest-YYYY-MM-DD.md` and keep the running memory in `opportunities/opportunities-state.md`. Do NOT use the outputs scratch folder (it gets wiped).
- **The handoff:** the digest feeds the apply pipeline. When the user picks items to pursue, they applie through the pipeline in `CLAUDE.md` (tailor resume -> review -> auto-apply -> log to `job_search_tracker.csv`). Keep digest items concrete enough to act on: name, what it is, deadline, link.

---

## OPERATING DISCIPLINE (read first)

These rules fix the failure modes that make a daily digest stale or untrustworthy.

0. **🚨 PREFLIGHT — READ BEFORE YOU ACT. Do this first, every run, no exceptions.**

   **Why this rule exists (2026-08-14).** That run produced three separate failures and every one had the same cause: the answer was already written down in this repo, and the run acted before reading it. Specifically — (a) **SWElist was skipped entirely** because the Gmail sweep queried only the LinkedIn senders, even though SWElist had been a documented standing source in the state file since 8/13; (b) **Handshake was scanned with invented URL params** (`job_type_names[]=Internship`, `sort_by=`) when both `.claude/skills/handshake-scan/SKILL.md` and the state file's `## Handshake — SCAN METHOD` section already documented the working ones (`jobType=3`, `sort=`) — and rule 6 below had *already* said to invoke the skill rather than hand-search; (c) the run then **reported the sweep as "broken and needing a redesign,"** a false bug report that would have sent someone rewriting a working feature. None of this was a search-coverage problem. It was a reading problem.

   **The preflight, in order:**
   1. **Read `opportunities/opportunities-state.md` — the whole head of the file, not just the dedup rules.** It contains the targeting block, the suppress gate, the dedup/snooze rules, the **Handshake SCAN METHOD section (URLs, param IDs, browser registry)**, and the **email-source seen-lists, which are the authoritative list of which inboxes to sweep**.
   2. **Read the SKILL.md of every sub-skill you intend to invoke** — today that means `handshake-scan`. Do not reconstruct its URLs, selectors, or method from memory.
   3. **Enumerate your sources from the state file, not from this file's prose.** This file goes stale between edits; the state file is updated every run. If the state file documents a standing source this file does not mention, **the state file wins** and you sweep it anyway.
   4. **Read the newest `opportunities/runlogs/runlog-*.md`** for its recommended opening moves and unresolved corrections. Read only the newest one; older run logs are history.
   5. **When you find yourself inventing a URL, a parameter, a selector, or a query — stop.** That is the signal you skipped step 1 or 2. Go read.

   **Corollary — never file a bug report against a working feature.** Before writing "X is broken / ignored / needs a redesign" into a digest or the state file, you must have (a) read the documented method for X and (b) tried it exactly as written. A tool returning plausible output for wrong input is not evidence of a bug; see rule 0B.

0B. **🚨 SILENT FAILURE — plausible output is not proof of success.** The Handshake job feed accepts unrecognised parameters **without erroring and returns a full, normal-looking page of unfiltered results.** A wrong param therefore looks exactly like a successful scan. On 2026-08-14 this produced an entire "Internship" digest section that was never filtered to internships — it merely looked intern-heavy because relevance ranking uses the user's career interests. It was caught only because adding a working sort surfaced Video Editor and Math Teacher rows.

   **So confirm the filter took effect on the rendered page, not from the fact that results appeared.** On Handshake, check that the **"Filters N" badge** and the **"Sort by" label** read what you asked for. Generalise this: for every filtered source, find the on-page element that *echoes your filter back to you* and read it. If a source offers no such echo, say so in the coverage log rather than assuming.

1. **Verify every deadline on the official source before listing it.** Search results and aggregators routinely show closed programs as if they're open. Before you put a date in the digest, confirm it on the program's own page (or a citation dated within the last ~30 days). If you can't confirm, write "deadline unconfirmed — verify" rather than stating one.

2. **Keep state across runs (don't re-surface dead programs).** Maintain a running file — `opportunities/opportunities-state.md` in the `ai-job-search` repo (the persistent folder that also holds the `digest-YYYY-MM-DD.md` files — NOT the outputs scratch folder, which gets wiped between sessions). If you don't see it there, create it. It has three lists: **(a) Open now** (program + verified deadline), **(b) Closed this cycle** (program + when it reopens, so you skip it until then; since 2026-09-12 the rows live in `opportunities/closed-this-cycle.md` and the state file keeps only the heading), **(c) Opening soon** (program + expected open month). At the start of each run, read this file, and read `closed-this-cycle.md` for dedup. Only feature a program as "new" if it actually changed since the last run. Update the file at the end of each run. This is what turns a daily digest into a real tracker instead of the same list every morning.

3. **You can't search every named program daily — rotate.** This file lists hundreds of programs. Hitting all of them every day is impossible and wasteful. Instead: every run, (a) check the live aggregators below, (b) run the discovery searches, (c) chase anything in your "Opening soon" state list whose window is near, and (d) rotate through a different ~20% of the named-program backlog each day so the full list gets covered weekly. Always fully search anything flagged urgent or opening within ~3 weeks.

4. **Calibrate to the calendar.** Hard deadlines cluster in Jan–May and Sept–Nov. June–August is mostly rolling programs + live summer events. Don't force "new drops" that aren't there — a thin day is a real result. Say so. **One seasonal exception worth holding in mind: marquee collegiate hackathons open their fall application windows in mid-June → October** (e.g., HackMIT historically opens apps in early-mid June for a September event). A "quiet summer day" is exactly when these quietly open, so don't let the slow-season framing lull the hackathon check — see the named-hackathon floor item in rule 7.

5. **Scope is global, not just US.** Most of this list is US-centric. Each run, include at least one discovery pass for non-US programs (EU/UK/Canada/Asia) — see Category 2R.

6. **Scan Handshake every run via the `handshake-scan` skill. 🚨 INVOKE THE SKILL — DO NOT HAND-ROLL URLs.**

   **On 2026-08-14 this instruction was already present and was violated anyway**, with the run inventing `job_type_names[]=Internship&sort_by=application_deadline_asc` instead of reading `.claude/skills/handshake-scan/SKILL.md`, which documents the working URLs. Because wrong params fail silently (rule 0B), the result looked fine and was written into the digest as a real finding, and the working deadline sweep was then falsely reported as broken. **If you are composing a Handshake URL by hand, you have already made the mistake.**

   **Verified-working URLs (also in the handshake-scan skill and the state file — confirmed end to end 2026-08-14):**
   - Newest-first delta: `https://<school>.joinhandshake.com/job-search?per_page=25&sort=posted_date_desc&page=N`
   - Deadline-sorted deep sweep: `https://<school>.joinhandshake.com/job-search?jobType=3&majors=<cs-id>&sort=application_deadline_asc&per_page=25&page=N`; page 1 is mostly expired/unpaid noise, deadlines advance ~1 week per page, so **walk to at least page 4–5** to reach the live 3–6 week window.
   - Param IDs: `jobType=3` Internship · `jobType=7` Fellowship · `majors=<id>` per major, school-specific. **`sort=`, never `sort_by=`. `jobType=`, never `job_type_names[]=`.**
   - **Confirm on the rendered page** that the "Filters N" badge and "Sort by" label match the request before trusting a single row (rule 0B).

6-legacy. **Original rule text.** Handshake is the user's university job/event portal — its postings are invisible to every public aggregator above, so it's a real blind spot. Each run, invoke the `handshake-scan` skill: it runs TWO passes — (a) a newest-first delta for freshly posted roles, and (b) a deadline-sorted deep sweep (`jobType`/`majors`/`application_deadline_asc`) that catches still-open roles posted weeks-to-months ago, which the newest-first pass alone misses — plus a Fellowship job-type sweep. It filters to the user's buckets (tech/SWE internships, fellowships & research, employer events), enriches deadlines, dedupes against the seen-list in the state file, and folds keepers into today's digest under `## Handshake (school portal)`. It needs Claude in Chrome connected and an active Handshake login; if the browser isn't available, note that Handshake couldn't be scanned this run and continue with the rest of the digest rather than failing. Don't duplicate its work by hand-searching Handshake — just run the skill.

6B. **Scan the connected Gmail for ALL standing email job sources every run — not just LinkedIn.**

   🚨 **This rule was LinkedIn-only until 2026-08-14, and that is exactly how SWElist got skipped.** SWElist was added as a standing source on 8/13, recorded in the state file, and then missed the very next day because the Gmail step named only the LinkedIn senders. **The authoritative list of email sources is the set of `— seen-list` sections in `opportunities-state.md`, not the list below.** Read those section headings during preflight and sweep every source you find, including ones added after this file was last edited.

   **Standing sources as of 2026-08-14 (sweep ALL of them; add to the state file when a new one appears):**
   - **LinkedIn job alerts** — `from:(jobalerts-noreply@linkedin.com OR jobs-listings@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d`
   - **SWElist daily digest** — `from:noreply@swelist.com newer_than:2d`. Arrives daily at the user's school address. Signal-to-noise is roughly **1 in 5**: single employers flood it (SAM ×3, Bank of China ×3, ByteDance ×3 in one edition), and it does not filter by season, geography or degree level. Read it fast and filter hard. Every posting routes through `simplify.jobs/p/<uuid>`, so **gates must be read on the real employer posting.** ⚠️ Its footer still links the stale `Summer2026-Internships` repo — the email is current, that link is not.
   - Run one combined query per run where possible, and **state each source separately in the coverage log** so a skipped source is visible.

6B-legacy. **LinkedIn specifics.** the user has LinkedIn job alerts that arrive by email — another personalized source no public aggregator sees (LinkedIn tailors them to their searches/profile). If a Gmail connector is connected, sweep it each run.
   - **Which inbox.** Record in the state file which address the Gmail connector is authenticated to, and whether another address forwards into it. Caution: don't infer the connected account from a message's `toRecipients`, because forwarded mail keeps the *original* recipient. If LinkedIn alert volume looks low, that's usually just genuine volume, not a plumbing problem — but sanity-check that forwarding is still active and note it in the coverage log rather than reporting an empty source as if dead.
   - **How to query.** Use the Gmail connector thread search with: `from:(jobalerts-noreply@linkedin.com OR jobs-listings@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d` (widen `newer_than` to cover the gap since the last run). Each alert subject is role + company (e.g. "AI Builder Intern at Scale AI"); `get_thread` (FULL_CONTENT) to pull the specific roles and apply links from the body.
   - **What to do with hits.** Filter to the user's buckets and deal-breakers like the rest of the sweep, dedupe against `opportunities-state.md`, `closed-this-cycle.md` and `job_search_tracker.csv`, **verify the role is still open on the actual posting before listing it** (alert emails lag and often point to filled roles), and fold keepers into the digest under `## LinkedIn job alerts (email)`. Keep a seen-list of alerted roles in the state file so the same alert is not re-surfaced.
   - If no Gmail connector is connected, note that in one line and continue — do not fail the run.

6C. **Sweep the SWElist daily email digest every run, in the same pass as rule 6B.** `noreply@swelist.com` sends the user a daily internship digest. It is a second personalized email source, and like the LinkedIn alerts it is not replaceable by any public aggregator, so it gets swept alongside them rather than instead of them. **Added as a standing source 2026-08-13 at the user's prompting.** It had been recorded only in `opportunities-state.md`, which meant it was swept only when a run happened to notice the note; this rule is what makes it instructed rather than rediscovered.
   - **Which inbox.** Same inbox as rule 6B. The same forwarding caveat applies: do not infer the connected account from `toRecipients`.
   - **How to query.** Gmail connector thread search with `from:noreply@swelist.com newer_than:2d` (widen `newer_than` to cover the gap since the last run). Use `get_thread` (FULL_CONTENT) to pull the listing bodies.
   - **Calibrate at roughly 1-in-5 signal, and filter hard.** The first read in a past run carried 54 postings and produced 7 real keepers. Two structural reasons, both of which recur: single employers flood the feed (Mapjects posted 7 legacy-stack listings in one edition, RRS Group 4), and the digest does not filter by season, geography, or degree level, so Fall-2026 reqs, Toronto roles, and Master's or PhD gates all arrive unlabeled. Read it fast, drop hard, and do not let volume inflate the keeper count.
   - **Every link routes through `simplify.jobs/p/<uuid>`, not the employer's own board.** Links are indirect, so the gate, season, location, and deadline must be read on the real posting before an item reaches the digest. This is also why SWElist is **not** a substitute for the SimplifyJobs 2027 GitHub tracker in Tier 2: its own footer points at `SimplifyJobs/Summer2026-Internships`, which is last cycle's repo.
   - **Known noise clusters to skip on sight:** Mapjects (legacy-stack listings, Oracle DBA, PHP, Drupal, Java, C# ASP.NET), RRS Group ("Placement Year" is a UK convention and the employer could not be pinned down).
   - **What to do with hits.** Filter to the user's buckets and deal-breakers, dedupe against `opportunities-state.md`, `closed-this-cycle.md` and `job_search_tracker.csv`, verify each keeper on the employer's real posting, and fold keepers into the digest under `## SWElist daily digest (email)`. Keep a seen-list in the state file so the same listing is not re-surfaced. **Company-level suppression is not function-level suppression:** keep a req at a company the user already applied to when it is a different function from the ones already submitted.
   - If no Gmail connector is connected, note that in one line and continue; do not fail the run.

7. **Meet the coverage contract, and log what you actually checked.** This is the rule that keeps a run honest. The hard failure mode of this digest is doing a few generic searches, finding the same well-indexed programs, and calling it done. A vague instruction to "search broadly" can't prevent that, because a lazy run and a thorough run look identical from the outside. The fix is to make coverage concrete and auditable.

   The full portal and query directory lives in `references/search-plan.md`. Read it every run; it has the exact URL patterns and query templates. The per-run **floor** (the minimum, not the target) is:
   - **Tier 0, Read the board as JSON (standing rule):** for every Greenhouse, Lever, or Ashby company the run touches, pull the whole board as public JSON rather than fetching posting pages. `api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true`, `boards-api.greenhouse.io/v1/boards/<org>/jobs?content=true`, `api.lever.co/v0/postings/<org>?mode=json`. No key, no login, no browser, one request per company. It returns the full posting text, the location, the workplace type, and usually the pay. **This is a floor item because its absence cost real coverage:** Ashby posting pages are JavaScript shells, so runs kept writing "gate unread, needs a logged-in browser pass" and a dozen Ashby companies sat unresolved for weeks. **Never record an Ashby, Greenhouse, or Lever role as "gate unread" without trying the JSON.** Full field lists and the closed-detection rule are in Tier 0 of `references/search-plan.md`.
   - **Tier 1, Direct ATS search:** at least 6 `site:` searches across Greenhouse, Lever, Ashby, and Workday (vary the season and role keyword). This is the highest-leverage tier and the one runs skip most, because it surfaces roles before any tracker indexes them. The `site:` search's job is to hand you the company slug; Tier 0 then reads the board.
   - **Tier 2, Live aggregators:** the GitHub 2027 trackers and the HN "Who is Hiring?" thread every run, plus 2-3 rotating aggregators from the list.
   - **Tier 3, Startup and VC-portfolio boards:** at least 3, rotating (Wellfound, YC Work at a Startup, and one VC portfolio board such as a16z, Sequoia, or General Catalyst). This is where the early-stage AI roles that fit the user live.
   - **Discovery searches:** at least 5 broad queries aimed at surfacing programs not already on the named lists.
   - **Fortune 500 mid-tier rotation (year-round, weighted Aug–Nov):** the named lists in this skill lean tech/quant/startup and under-cover the Fortune 500 mid-tier — big retail/CPG data-science programs, healthcare/pharma AI-ML, industrials/aerospace, energy, insurers, and the non-bulge finance names. These run large structured Summer-2027 internship programs that mostly open **August through November**, and they were a real blind spot until a manual sweep in a past run surfaced ~a dozen live roles (Chevron, Intuitive Surgical, BofA, GE Vernova, Morgan Stanley, Wells Fargo, UPS, Labcorp, etc.) plus a large pre-open watch list. Each run, rotate through **one F500 sector** (finance/insurance · tech/telecom/media · retail/CPG · healthcare/pharma · industrials/defense/energy/auto) so the whole 500 gets covered weekly. In the **Aug–Nov opening wave, hit ALL five sectors every run** (this is when the volume drops). See Category 2A for the sector rosters. Two standing filters: (a) present the graduation year these programs sort on, per the Default Selection Rule in `CLAUDE.md`, since they screen on time-to-conversion; (b) **defense primes (Boeing, Lockheed, RTX, Northrop, General Dynamics, L3Harris) are US-citizenship/clearance-gated**, so check the candidate profile for work authorization before listing them and verify any clearance-specific requirement separately.
   - **Named marquee collegiate hackathons (mid-June → October):** during this window, directly check the application status of the top travel-covered school hackathons by name — HackMIT, HackHarvard, PennApps, HackPrinceton, Hack the North, CalHacks, TreeHacks, MHacks, HackGT, and the rest of the Category 1 list. **This is its own floor item because these events do NOT appear on Devpost, MLH, or any aggregator — they announce application openings only on their own (JavaScript-rendered) sites and X/Twitter accounts.** Searching `site:devpost.com` or the MLH season page will never surface them. A real example of the failure: in a past run the sweep leaned on Devpost/MLH/ETHGlobal and missed HackMIT opening applications that very day. Search each by name (`"HackMIT 2026" applications open`, `HackHarvard 2026 apply`, etc.); if a site is JS-only and unreadable, say so and fall back to the org's X account or last year's timing rather than silently dropping it.
   - **Handshake:** via the skill (rule 6).
   - **Gmail / LinkedIn alerts:** via the connector (rule 6B), when connected.
   - **Gmail / SWElist daily digest:** via the connector (rule 6C), when connected. Same pass as the LinkedIn alerts, separate query and separate digest section.

   At the end of every run, write the **Coverage log** into the run-log file `opportunities/runlogs/runlog-YYYY-MM-DD.md` (format in OUTPUT FORMAT) — never into the digest — recording which sources you actually hit and which you skipped. The point is not bureaucracy. A visible, honest record of "I checked these 14 sources, skipped these 3, and here is why" is the only thing that makes a thin day distinguishable from a lazy day, and it tells the user exactly where to poke around themselves. If you fall short of the floor (rate limits, time, a tool was down), say so in the log rather than hiding it.

8. **Keep the state file lean — prune every run (this is what stops context bloat).** `opportunities-state.md` is loaded into context on every scheduled run, so unbounded append-only lists are the real long-term risk, not the snooze list. Each run, before writing, do a quick compaction so the file holds *live* data only:
   - **Expired snoozes:** delete any row in the Snoozed table whose resurface date/condition has passed (the role becomes eligible to reappear).
   - **Closed/expired roles:** remove them from the Open Now table and from the seen-lists — once a posting is closed there is nothing left to dedupe against.
   - **Age out seen-list fingerprints older than ~4 months:** those postings are long gone; their fingerprints no longer earn their keep. (Handshake + LinkedIn seen-lists are the fastest-growing; prune them hardest.)
   - **Rotation log:** keep ~the last 10-14 daily entries; older ones can be compressed to a one-line-per-week summary or dropped.
   - The goal: the "must-read every run" head of the file (targeting, dedup/snooze rules, Open Now, Opening Soon, active snoozes) stays small and stable no matter how many months this has been running. If the file is clearly ballooning anyway, say so in the coverage log and flag that a deeper consolidation pass is due (the `consolidate-memory` skill can do it).

8A. **The automation owns the verification backlog. The user never reviews it manually.** `opportunities/verification-backlog.md` is pipeline work, not a user task and not a graveyard. Every daily run must process at least 25 candidate opportunities from it, starting with recent internships, fellowships, and items with a named employer or official-looking link. Split cluster rows into individual opportunities, find the official posting, and assign each candidate to exactly one outcome: Open Now, Opening Soon, Closed This Cycle, ineligible with a recorded reason, suppressed by the application tracker, or still blocked with a precise verification failure and retry condition. Remove resolved candidates from the backlog in the same run. If fewer than 25 can be processed because of tool failure or a genuinely smaller queue, record the exact count and reason in the run log. New discoveries should be verified and written atomically during the run whenever possible, rather than added as another cluster. A daily run that only adds leads while leaving the backlog untouched has failed.


9. **🚨 TWO OUTPUTS, STRICT SEPARATION — the digest is for the user, the run log is for the pipeline.** Added 2026-08-24 because digests had grown past 10,000 words, more than half operational telemetry (lane counts, filter echoes, browser IDs, method findings, notes to the next run). That buried the action layer and made the daily read useless. The digest carries jobs, programs, events and deadlines ONLY, under a hard 800-word cap; the full open backlog is rendered for the user in `opportunities/OPEN-LIST.md` (refreshed each run); every operational sentence goes to `opportunities/runlogs/runlog-YYYY-MM-DD.md`. Durable findings get edited into their permanent home (search-plan, sub-skill, state file) at the moment of discovery instead of being restated in every digest. Full spec in OUTPUT FORMAT. Before saving the digest, check it against the template and the word cap — a run that ships an over-cap or off-template digest has failed, even if its sweep was perfect.

---

## CORE INSTRUCTION: Search laterally, not just narrowly

**Fan out.** Every run, fire a wide spread of web searches across the categories and aggregators — many queries, issued in parallel batches, breadth over depth. The goal is broad coverage so nothing slips through, not a deep dive on any one item. (This is the opposite of the `deep-research` skill, which goes narrow-and-deep on a single question; save that for when you want to drill into one specific lead, not for the daily sweep.)

For each category, run BOTH:
1. **Named searches** — query the specific programs listed below.
2. **Discovery searches** — broad queries designed to surface programs you haven't heard of. Examples:
   - "new AI fellowship 2026 undergraduate applications"
   - "founder fellowship just launched application open"
   - "sophomore insight program 2027 [bank/firm]"
   - "[city] tech week 2026 student events"
   - "VC scout program undergraduate 2026"
   - "AI safety summer program 2026"
   - "summer research program undergraduate computer science open"

Also check aggregator sources every run. The authoritative, copy-pasteable version of this list (with exact URL patterns, the direct-ATS-search technique, and query templates) is `references/search-plan.md` — open it and work the tiers. The quick list below is a reminder, not a substitute:
- **Pitt CSC / SimplifyJobs Summer 2027 Internships** GitHub: `github.com/SimplifyJobs/Summer2027-Internships`
- **speedyapply/2027-AI-College-Jobs** GitHub repo — the AI/ML-specific sibling of the SWE repo, updated daily. **Promoted to standing source 2026-08-13; run it FIRST.** Repeatedly the single highest-yield source in the digests (245 live US AI internships in a past run) and it was being rediscovered run by run instead of being listed here
- **speedyapply/2027-SWE-College-Jobs** GitHub repo (note the `2027`; `2026-SWE-College-Jobs` is last cycle's repo and is still live, so pointing at it returns stale roles without erroring)
- **Internship Radar 2027**: `https://internship-radar-2027.yuxhuang.com/` — **standing rule.** Not a GitHub repo. Server-rendered so it is fetchable without a browser, refreshed daily around 7:30 AM PT from 18 sources, and it is the **only board carrying a per-row student-eligibility tag** ("3rd year", "Undergraduate — year not stated", "Graduate student"), which is the field that decides whether a req is worth an application. Independent project by Yu Huang; verify eligibility and deadlines on the employer page
- **A student-maintained quant internship GitHub tracker** (search GitHub for the current season's `<year>QuantInternships` repo; several student groups maintain one) — **standing rule.** Summer 2027 quant, maintained by a university fintech club. Covers Optiver, Citadel and Citadel Securities, Jane Street, HRT, IMC, SIG, DRW, Five Rings, Walleye and Quantic, broken out by QT / QR / QD / SWE / FPGA
- ~~**vanshb03/Summer2027-Internships**~~ — dropped 2026-08-13, dead for this cycle. Last push 2026-05-23; the main README description still reads "Summer 2026" and `OFFSEASON_README.md` is titled "Spring & Fall 2026" with no row newer than May 22. Do not re-add without checking it has resumed
- **ColorStack** opportunities feed
- **Rewriting the Code (RTC)** opportunities board
- **Codepath Tech Fellows** posts
- **MLH** (mlh.io) season schedule
- **Devpost** trending hackathons
- **Cracked Engineers / Yo Pickle / @cracked_dev** style Twitter alerts
- **Levels.fyi** internship leaderboard
- **AngelList Talent / Wellfound** (early-stage startup intern roles)
- **Built In** newsletters
- **The Forage** (virtual experiences/PA programs)
- **aisafety.training** — single best deadline aggregator for AI safety/alignment programs (covers MATS, Anthropic, GovAI, ARENA, MARS, etc. in one place)
- **80,000 Hours job board** — high-signal roles + fellowships, frequently updated
- **John Gannon's VC job board** — VC analyst/scout/intern roles
- **Hacker News "Who is Hiring" monthly thread** (first weekday of each month) — dense with startup roles, indexed by no aggregator
- **ProFellow** — broad fellowship deadline database
- **Atom Grants / OpportunityDesk** — grant & fellowship deadline trackers
- **ETHGlobal** (ethglobal.com) — travel-covered, cash-prize crypto/web3 hackathons
- **Sifted** — European startup news (for EU founder/builder programs that don't index well in US search)
- **Direct ATS search** — `site:` queries across Greenhouse, Lever, Ashby, Workday (see Tier 1 of `references/search-plan.md`), then the public board JSON for each company found (Tier 0 of the same file); the best way to catch roles before any tracker indexes them
- **YC Work at a Startup** (`workatastartup.com`) and **VC-portfolio talent boards** (a16z, Sequoia, General Catalyst, Greylock, Bessemer, etc.); one board spans a whole portfolio of vetted early-stage startups (see Tier 3 of the search plan)

---

## EXECUTION MODEL: parallel fan-out (preferred when subagents are available)

A single agent doing 30+ searches has to skim and drop most results to stay inside its context window, so coverage quietly degrades exactly when you need it most. The fix is to fan the work out across subagents. Each one gets its own fresh context, so it can actually read full result pages instead of truncating, and they run concurrently so wall-clock stays reasonable. This is the preferred way to run the sweep whenever the environment has a subagent/Task tool. If subagents are not available, fall back to the serial model: work the tiers in `references/search-plan.md` yourself, in parallel search batches, still meeting the coverage contract.

**The owner of this workspace has asked for maximum thoroughness on the daily run and explicitly does not care how long it takes or how many tokens it costs.** So when fanning out, err toward more lanes and deeper reading, not fewer. A 10-30 minute run is fine and expected.

**Architecture: one orchestrator, several search lanes.**

The orchestrator (the main run) spawns the lane subagents in a single batch so they run concurrently, then does the work that must stay centralized. Spawn roughly these lanes, each pointed at the matching part of `references/search-plan.md`:
1. **ATS lane A**: Greenhouse + Lever `site:` searches (vary season and role keyword), then the Tier 0 board JSON for every company those searches surface.
2. **ATS lane B**: Ashby + Workday + Rippling/SmartRecruiters/Workable. **Ashby posting pages do not render, so this lane reads Ashby entirely through the Tier 0 JSON API**; a `site:` hit here is a slug to look up, not a page to fetch.
3. **Aggregators lane**: GitHub 2027 trackers, HN "Who is Hiring," 80,000 Hours, aisafety.training, Levels.fyi, ProFellow, John Gannon.
4. **Startup & VC-portfolio boards lane**: Wellfound, YC Work at a Startup, Built In, and the VC portfolio boards.
5. **Discovery lane**: broad "new program" queries plus status-verification of the known open/closing cluster.
6. **Named-2027 programs lane**: Big Tech, quant, APM, research/REU, aerospace, international timelines.

Split or add lanes freely (for example, two ATS lanes as above) to go deeper. Each lane subagent gets, in its prompt: a compact candidate profile and targeting, the deal-breakers (so it can drop bad-fit roles itself), today's date, the relevant search-plan slice, and a strict output contract.

**What each lane subagent must return** (and must NOT do): return findings only as its final message, and do not write any files (the orchestrator owns all writes). For each opportunity: org/program, a short description, the apply link, the deadline tagged `[VERIFIED on official page: DATE]` or `[UNCONFIRMED]`, and a one-line fit note. Prefix Summer/Winter 2027 internships with the 2027 flag. Include a short "confirmed closed, skip" list and a note of which sources were unreadable (JS-gated/blocked) so coverage stays auditable. **Before calling any Ashby, Greenhouse, or Lever source unreadable, try its Tier 0 board JSON and say in the note that you did.** A JS-gated posting page on those three ATSes is not an unreadable source; it is a source read the wrong way.

**What the orchestrator must keep centralized** (do not delegate these):
- **Dedup** against `opportunities/opportunities-state.md`, `opportunities/closed-this-cycle.md` and `job_search_tracker.csv` per the dedup + snooze rules in the state file. Key points: suppress only CSV rows with status **`applied`** or later — **`drafted` does NOT suppress** (re-surface drafted roles tagged "⏳ in progress — finish it"). Honor the **Snoozed / revisit later** table: hide a snoozed role only until its resurface date/condition passes, then it reappears (a "not interested" is a timed snooze, never a permanent delete).
- **Verification** of every deadline that will appear in the digest. Subagents *discover* deadlines; the orchestrator *confirms* them on the official page before they are stated as fact. This is where correctness is enforced, so it cannot be spread across lanes.
- **Writing** the digest, the coverage log, and the state-file update.

**Stays in the main thread, never a subagent: Handshake.** It is tied to the user's logged-in Chrome session, so a detached subagent cannot reach it. Run `handshake-scan` from the orchestrator (see rule 6). Likewise, the VC-portfolio boards and Wellfound are JavaScript-gated: subagents can only read them via search snippets, so when individual postings matter, the orchestrator should do a logged-in Claude-in-Chrome pass.

**🚨 LANE-COMPLETION ACCOUNTING (standing rule — a lane died silently and its whole category went uncovered).** On that run the named-hackathon lane was terminated mid-flight by an API error (the host machine slept) and returned nothing. The run noticed, but only wrote "re-run tomorrow" — so a **required floor item silently produced zero coverage on the day it mattered**, during the exact mid-June→October window when those events open. That is a worse outcome than a thin day, because the digest still looked complete.

**The rule: a lane that does not return is not a footnote, it is an incomplete run.**
1. **Count lanes out and lanes back.** Before writing the digest, explicitly reconcile: N spawned, M returned, and name every lane that did not.
2. **Re-launch any lane that died, in the same run.** A dead lane is retried once immediately. Subagent failures here are usually transient (API error, host sleep), not deterministic — the 8/14 hackathon lane re-ran successfully the same day and produced the single best hackathon find of the week.
3. **If a re-launched lane dies again, narrow it and retry once more** (split it in half, or drop to the highest-value half of its target list) rather than abandoning the category.
4. **Only after two failures may a category be reported as uncovered** — and then it must be flagged at the TOP of the digest as a coverage gap, not buried in the appendix, and written into the state file's rotation log as a floor miss.
5. **Never let a dead lane be represented by carryover items.** If the hackathon lane dies, the Hackathons section says "NOT CHECKED", it does not quietly list yesterday's still-open events as though they were today's sweep.

**Coverage log under fan-out:** record that the run fanned out, how many lanes, and the per-lane yield, in the same Coverage log format (see OUTPUT FORMAT). The contract from rule 7 still applies; fan-out is how you exceed it, not a reason to skip the accounting.

---

## CATEGORY 1: Collegiate Hackathons

Major undergraduate hackathons, with emphasis on those that offer travel reimbursement.

> **Why this category needs *named* searches, not aggregator scans.** The big collegiate hackathons run their own application portals and announce on their own sites + X/Twitter. They are not posted to Devpost, MLH, or any other aggregator the rest of this skill leans on, so a Devpost/MLH-only pass will report "no new hackathons" on the exact day HackMIT opens. The general lesson, which applies beyond hackathons: an opportunity that *hosts its own front door* is invisible to aggregators that only index opportunities submitted to them. Whenever a category's marquee items self-host (collegiate hackathons here; you'll see the same with some fellowships and founder programs), you have to go knock on each door by name. For hackathons specifically, work the named list below by name during the mid-June→October window (rule 7 floor), and note that their sites are usually JavaScript-rendered — if a fetch returns an empty shell, check the org's X account or fall back to last year's timing rather than dropping the item.

Named hackathons:
- HackMIT, Blueprint (MIT)
- HackHarvard, Hack@Brown / HackBrown
- TreeHacks (Stanford)
- PennApps (UPenn)
- HackPrinceton
- MHacks (Michigan)
- HackGT, Hacklytics (Georgia Tech)
- HackIllinois
- HackNC, HackDuke
- Hack the North (Waterloo)
- YHack (Yale)
- HackNYU
- CalHacks, Berkeley AI Hackathon (UC Berkeley)
- SpartaHack (Michigan State)
- HackDavis (UC Davis)
- The user's own school hackathon
- HackCMU, TartanHacks, ScottyLabs (Carnegie Mellon)
- Bitcamp (Maryland)
- HooHacks (UVA)
- HackUTD (UT Dallas), HackTX (UT Austin), TreeHacks-style at other schools
- LA Hacks (UCLA), SB Hacks (UCSB), SD Hacks (UCSD)
- DubHacks (UW)
- DandyHacks (Notre Dame), BoilerMake (Purdue), HackIowa
- Hoya Hacks (Georgetown), Bitcamp, HackUMass

Discovery queries:
- "MLH 2026-2027 season schedule"
- "hackathon fall 2026 travel reimbursement undergraduate"
- "AI hackathon 2026 cash prize undergraduate"

## CATEGORY 1B: Company-Hosted Hackathons & Coding Challenges

Often higher signal than school hackathons because they're recruiting funnels:
- **JPMorgan Code for Good** (sophomore-friendly recruiting hackathon)
- **Goldman Sachs Engineering Hackathon / Code Cup**
- **Citadel Datathon, Citadel Terminal Live, Citadel Trading Competition**
- **Jane Street Electronic Trading Challenge (ETC), Estimathon**
- **IMC Prosperity** (annual large-scale trading game)
- **Optiver Trading Challenge**, **SIG Trading Game**, **HRT Algo Engineering Challenge**
- **Two Sigma Hackathon / Halite / Battlecode-style competitions**
- **D.E. Shaw Quant Challenge**
- **Bloomberg Coding Challenge, Bloomberg Hackathon**
- **Capital One Software Engineering Summit / Hackathon**
- **Microsoft Imagine Cup**
- **Google Solution Challenge, Google Code Jam alternatives, Google Hash Code (check if reinstated)**
- **Apple Swift Student Challenge**
- **Meta Hacker Cup**
- **Amazon AWS DeepRacer**, AWS GameDay, Re:Invent challenges
- **NVIDIA AI Hackathons, GTC student events**
- **Walmart Sparkathon**
- **AT&T Hackathon, T-Mobile Tech Experience**
- **Visa Everywhere Initiative**
- **Mastercard Innovation Challenge**
- **OpenAI / Anthropic / Cohere community hackathons** (often weekend-only, announced on Discord/X)
- **Scale AI competitions**
- **xAI / Perplexity / Replit / Vercel / Cursor hackathons** (frequent, AI-startup hosted)
- **Buildspace S-cohorts / Nights & Weekends**
- **YC AI Startup School hackathon**

**Crypto / web3 hackathons** (travel + lodging often covered, large cash/token prizes, very student-friendly):
- **ETHGlobal** events (ETHDenver, ETHNYC, ETHGlobal Online, etc.) — the flagship circuit
- **a16z crypto CSX / Crypto Startup School**
- **Solana / Colosseum hackathons**
- **Encode Club hackathons**
- **Chainlink / Devfolio-hosted hackathons**

Discovery queries:
- "company hackathon 2026 undergraduate cash prize"
- "AI startup hackathon weekend SF NYC 2026"
- "trading firm competition 2026 undergraduate"
- "ETHGlobal hackathon 2026 travel stipend"

---

## CATEGORY 2: 2027 Summer Internship Deadlines

**Big Tech:** Google, Meta, Apple, Amazon, Microsoft, Netflix, Salesforce, Adobe, Nvidia, Intel, AMD, Qualcomm, Broadcom, Databricks, Snowflake, Stripe, Plaid, Block (Square), Figma, Notion, Airtable, Canva, Linear, Rippling, Brex, Ramp, Mercury, Scale AI, OpenAI, Anthropic, Cohere, Mistral, Perplexity, xAI, Hugging Face, Palantir, Anduril, Shield AI, Saronic, SpaceX, Tesla, Cloudflare, Crowdstrike, Datadog, Hashicorp, MongoDB, Elastic, Roblox, Unity, Epic Games, Riot, Discord, Spotify, Pinterest, Reddit, Coinbase, Robinhood, DoorDash, Instacart, Uber, Airbnb, Lyft, Twilio, Atlassian, Asana, Zoom, ServiceNow, Workday, Oracle, IBM, Yelp

**Top Consulting:** McKinsey, BCG, Bain, Deloitte (S&O, Monitor), Accenture (Strategy, Song), Oliver Wyman, A.T. Kearney, L.E.K., Roland Berger, EY-Parthenon, Strategy& (PwC), ZS Associates, Putnam Associates, Analysis Group, Cornerstone Research, Charles River Associates, Bridgespan, Dalberg, FTI Consulting, Alvarez & Marsal, AlixPartners

**Investment Banking & Finance:** Goldman Sachs, JP Morgan, Morgan Stanley, Citi, BofA, Barclays, Wells Fargo, Deutsche Bank, UBS, Credit Suisse / UBS, HSBC, Jefferies, Lazard, Evercore, Centerview, PJT Partners, Moelis, Houlihan Lokey, Guggenheim, Perella Weinberg, Greenhill, Qatalyst, Allen & Co, Raine Group, LionTree

**Private Equity / Growth Equity:** Blackstone, KKR, Apollo, Carlyle, Bain Capital, TPG, Warburg Pincus, Silver Lake, Vista, Thoma Bravo, General Atlantic, Insight Partners, TA Associates, Summit Partners, Advent, EQT, Brookfield, Ares

**Hedge Funds / Quant Trading:** Citadel, Citadel Securities, Jane Street, Two Sigma, D.E. Shaw, Point72, Bridgewater, Millennium, Balyasny, ExodusPoint, Schonfeld, HRT, Jump Trading, IMC, Optiver, SIG, Tower Research, Five Rings, Akuna, DRW, Belvedere, Headlands, Old Mission, Quadrature, Aquatic, Cubist, Voloridge, Squarepoint, AQR

**Unicorn / High-growth startups:** Search broadly — anything YC, Sequoia, a16z, Founders Fund, Thrive, Khosla, Index, Lightspeed, Greylock, Benchmark, Accel-backed at Series A+

**Defense / Frontier:** Anduril, Shield AI, Saronic, Helsing, ARX Robotics, Hadrian, Rocket Lab, Astranis, Capella Space, Vannevar Labs

**Climate / Bio / Hardware:** Commonwealth Fusion, Helion, TerraPower, Boom Supersonic, Joby, Archer, Boston Dynamics, Figure, 1X, Sanctuary AI

For each, note: company + role (SWE, PM, analyst, quant, etc.) + open/close date + link.

**Internship discovery technique (folded in from the retired `surface-internships` skill).** Don't rely only on the named list above — actively hunt new postings each run:
- **LinkedIn ignores the year in loose keyword searches.** Searching `summer 2027 intern` just returns generic recent posts. To find season-specific roles, search the **exact quoted phrase** and let filters narrow: `https://www.linkedin.com/jobs/search/?keywords=%22Summer%202027%22&f_E=1&sortBy=DD` (the quoted `"Summer 2027"` is what matches; `f_E=1` = internship level). Add `&f_F=eng%2Cit` (Engineering + IT) to cut through the accounting/tax noise and surface SWE/AI roles. Repeat for `"Winter 2027"`. Use Claude in Chrome on the user's logged-in session, read-only; the list is lazy-loaded, so scroll the results pane and read cards from screenshots (`get_page_text` only returns the open posting's detail pane, and DOM scrapes get blocked).
- **Aggregators** for internships specifically: the SimplifyJobs / Pitt CSC Summer 2027 GitHub list, `speedyapply/2027-SWE-College-Jobs`, and company career portals directly (early in a cycle, portals carry 2027 roles before LinkedIn or the trackers do).
- **Targeting:** prioritize Winter 2027 + Summer 2027 AI/ML, data, applied-ML, AI-eval, vertical-AI, and AI-adjacent product/strategy roles in the user's target sectors. Drop Summer 2026 (too late) and flag on-site Fall/Winter roles as academic-year logistics conflicts. Dedupe against `opportunities/opportunities-state.md` and `job_search_tracker.csv` (already-applied) before listing.

---

## CATEGORY 2A: Fortune 500 Mid-Tier Internships (the sector this skill used to miss)

Added 2026-07-28 after a manual F500 sweep found ~a dozen live roles the daily run had never surfaced. Category 2 above covers big tech, quant, IB, PE, consulting, and defense/frontier. This category covers the REST of the Fortune 500 — the large, non-tech-sector employers that run substantial technology/data-science/ML/analytics internship programs and recruit an Industrial-Engineering + AI profile well. Rotate one sector per run year-round; hit all five every run in the **Aug–Nov opening wave** (see coverage-contract rule 7).

**Method:** for each name, check the official careers page / ATS for a LIVE Summer-2027 (or Winter-2027) technology, data-science, ML/AI, analytics, or operations-research intern req. Use ATS `site:` searches (`<company> "Summer 2027" data scientist intern`, `site:myworkdayjobs.com "2027" intern (data OR "machine learning") <company>`). Verify the posting is live and read its grad-window/class-year language before listing. Skip generic finance/accounting/store/clinical roles — keep the technology/data/AI tracks.

**Sector rosters:**
1. **Finance & insurance (non-bulge / corporate-tech tracks):** JPMorgan, Bank of America, Wells Fargo, Citi, US Bancorp, PNC, Truist, Capital One, American Express, Discover, Synchrony, Charles Schwab, Fidelity, State Street, BNY Mellon, Mastercard, Visa, PayPal, Fiserv, FIS, Global Payments, Liberty Mutual, Nationwide, MetLife, Prudential, USAA, Progressive, Allstate, Travelers, Chubb, AIG. (Bulge-bracket IB desks live in Category 2; here the target is their **Technology / Data & Analytics** tracks.)
2. **Tech / telecom / media (non-FAANG F500):** Oracle, IBM, Cisco, Intel, Qualcomm, AMD, Broadcom, HP, HPE, Dell, Texas Instruments, Micron, Applied Materials, Adobe, Intuit, ServiceNow, Workday, Palo Alto Networks, CrowdStrike, Western Digital, Motorola Solutions, Comcast, AT&T, Verizon, T-Mobile, Charter, Disney, Netflix, Warner Bros Discovery, Paramount, Fox, EA, Uber, DoorDash, Airbnb, eBay, Expedia.
3. **Retail / consumer / CPG:** Walmart, Costco, Target, Home Depot, Lowe's, Kroger (84.51°), Walgreens, CVS, Best Buy, TJX, Albertsons, McDonald's, Starbucks, Chipotle, PepsiCo, Coca-Cola, P&G, Nike, Mondelez, General Mills, Kraft Heinz, Colgate, Kimberly-Clark, Estée Lauder, AutoZone, O'Reilly, Genuine Parts, Ulta. (Best-matched DS programs: 84.51°/Kroger, Target, Coca-Cola, PepsiCo, General Mills — IE-friendly — Home Depot, AutoZone.)
4. **Healthcare / pharma / biotech:** UnitedHealth/Optum, CVS/Aetna, McKesson, Cencora, Cardinal Health, Cigna/Evernorth, Elevance, Centene, Humana, HCA, Pfizer, J&J, Merck, AbbVie, Eli Lilly, BMS, Amgen, Gilead, Thermo Fisher, Danaher, Abbott, Regeneron, Vertex, Moderna, Biogen, GE HealthCare, Stryker, Boston Scientific, Intuitive Surgical, Labcorp, Quest. (Best fits for their imaging/ML research: Intuitive Surgical, Boston Scientific, GE HealthCare, Amgen, Gilead, Labcorp — several DS reqs are Master's-gated, read per posting.)
5. **Industrials / aerospace-defense / energy / auto / logistics:** Boeing, Lockheed Martin, RTX, Northrop Grumman, General Dynamics, L3Harris, GE Aerospace, GE Vernova, Honeywell, 3M, Emerson, John Deere, Cummins, PACCAR, Parker Hannifin, ITW, Eaton, Rockwell Automation, GM, Ford, Tesla, Stellantis, ExxonMobil, Chevron, ConocoPhillips, Marathon, Phillips 66, Valero, Duke Energy, Southern Company, NextEra, Dominion, SLB, Halliburton, Union Pacific, UPS, FedEx. (Check the candidate profile: an engineering degree or hands-on hardware and CAD experience also fits the operations-research and mechanical or fabrication intern reqs here.)

**Two standing filters for this whole category:**
- **Present the earlier graduation year where the user has two honest options.** These are large structured programs with return-offer pipelines; they sort on time-to-conversion, so the later date disqualifies at most of them (per the Default Selection Rule in `CLAUDE.md`). Exceptions that accept the later year exist and are worth noting in the state file as you find them.
- **Citizenship gate on defense primes.** Boeing, Lockheed, RTX, Northrop, General Dynamics, L3Harris — plus some auto self-driving / ITAR roles — require US citizenship or clearance. Check the work-authorization line in the candidate profile before listing one of these. Verify any separate clearance, export-control, or facility-access requirement before listing a role as actionable.

Discovery queries:
- "<company> Summer 2027 data science internship apply"
- "Fortune 500 2027 summer technology internship application open"
- `site:myworkdayjobs.com "Summer 2027" intern (data OR "machine learning" OR analytics)`

---

## CATEGORY 2B: Diversity, Insight & Sophomore-Specific Programs

These run on completely different timelines and many undergrads miss them. Often the easiest path into a banked top-tier offer.

**Banking sophomore / diversity programs:**
- Goldman Sachs Engineering Possibilities, GS Sophomore Insight, GS Markets Insight, GS Spring Programme
- JPMorgan Sophomore Edge, Winning Women, Advancing Black Pathways, Launching Leaders, Code for Good
- Morgan Stanley Early Insights, Sophomore Insights, Richard B. Fisher Scholarship, Beat the Streets
- Citi Sophomore Leadership Program, HSI/HBCU Innovation Lab, Citi Bracelet
- BofA Merrill Multicultural Sales Program (MMSP), Lazard Diversity Symposium, Lazard Women's Insight
- Deutsche Bank dbAchieve, dbWomen
- Barclays SEED, Barclays Spring Internship
- UBS Discover, UBS Future Female Leaders
- Wells Fargo Diversity programs
- Jefferies Sophomore Insight
- Evercore Sophomore Diversity Day, Evercore Women's Insights
- Centerview Sophomore Diversity Program
- Houlihan Lokey Diversity Symposium
- PJT Sophomore Insight
- Moelis Sophomore Engagement
- Lazard MAE program

**Big Tech sophomore / pre-internship:**
- Google ASDI (Associate Software Developer Intern; **renamed from STEP, so search "ASDI" because "STEP" returns stale listings**), Google CSSI, BOLD, Tech Exchange, computeRR
- Meta Above & Beyond Computer Science (AlphaB & B), Meta Summer Academy. **Meta University is closed; do not spend a sweep looking for a 2027 cycle.** Kept named here so it is not re-added
- Apple Pathways, Apple WWDC Scholars
- Amazon Future Engineer, Amazon Propel
- **Microsoft Explore** (the flagship first- and second-year software program, and the one this category most often missed), Microsoft New Technologists, Microsoft Discovery Program, Microsoft TEALS
- Roblox Tech Sandbox
- Bloomberg Sophomore Insights, Bloomberg Diversity Programs
- NVIDIA AI Foundations programs
- LinkedIn CARES, LinkedIn REACH

**Consulting sophomore / diversity:**
- McKinsey Sophomore Summer Business Analyst, McKinsey FCG (First-Generation College Graduates), McKinsey Diversity Connect
- BCG Sophomore Summer Associate, BCG Unlock, BCG Pride@BCG
- Bain Sophomore Summer Associate, Bain Building Entrepreneurial Leaders, Bain ADVANCE
- Deloitte Discovery Internship
- Accenture Student Leadership Conference
- Oliver Wyman Diversity Programs, OW Women's Connections Workshop

**Other notable:**
- Booz Allen Hamilton Summer Games
- Capital One Tech Internship, Capital One Power Day
- BlackRock Future Leaders, BlackRock Pathways
- Citadel Discover, Citadel Trading Discovery
- Two Sigma Diversity Fellowship
- Jane Street Academy of Math and Programming (AMP), Jane Street SPARK, Jane Street INSIGHT, Jane Street FOCUS
- DRW Spring Programs
- HRT Women in Trading & Tech
- SIG Discover Symposium
- IMC Insights / Future Trader programs

Discovery queries:
- "[bank/firm name] sophomore insight 2027 application"
- "diversity sophomore program tech 2026 application open"
- "spring week 2027 banking application"

**Timing, and why this category needs its own autumn sweep.** These open earlier than general internship cycles and close before them, so a sweep timed to the main season finds them already shut. Run a dedicated pass in autumn against the named programs above rather than relying on the daily sweep to surface them, because aggregators that filter on the word "internship" do not index most of them. **The user's eligibility is finite:** they started in September 2025, so the summer 2027 cycle is the last one where the underclassmen-only programs in this category accept them. Treat a missed deadline here as costing a year rather than a week. (Added 2026-08-20 from `documents/playbook/2026-08-13 - itsellagonzales-underclassmen-programs.md`.)

---

## CATEGORY 2C: AI Fellowships, Research & Safety Programs

Often weekly stipends, mentorship, sometimes lead to roles at top labs. **Start here: aisafety.training aggregates most of these deadlines.**

- **Anthropic Fellows Program** (AI safety research)
- **MATS (ML Alignment & Theory Scholars)** — twice yearly
- **SERI MATS** (older variant)
- **ARENA (Alignment Research Engineer Accelerator)** — London
- **MARS (CAIS Mentorship for Alignment Research Students)**
- **PIBBSS Fellowship**
- **GovAI Summer Fellowship** (Oxford)
- **Constellation Fellowship / Constellation Visiting Researcher**
- **Astra Fellowship**
- **Pivotal Research Fellowship**
- **Apart Research / Apart Lab**
- **OpenPhil Career Development & Transition Funding, OpenPhil Undergrad Scholarship**
- **METR Fellowship**
- **Future of Life Institute fellowships**
- **80,000 Hours career calls / advising**
- **DeepMind Scholarship, DeepMind PhD Fellowship**
- **Google PhD Fellowship, Google Research Mentorship**
- **Cohere For AI Scholars**
- **OpenAI Researcher Access Program**
- **IAPS (Institute for AI Policy and Strategy) Fellowship** — undergrad-eligible AI policy
- **Flow Research Fellowship** — AI-native / open-source builder cohorts
- **NeurIPS, ICML, ICLR student travel awards & DEI scholarships**
- **Eric & Wendy Schmidt AI in Science Postdoctoral**
- **Schmidt Futures Rise, Schmidt Sciences Fellowship**
- **Vitalik-funded grant programs (Optimism RPGF, Gitcoin)**
- **Stanford HAI student grants**
- **EA / 80k aligned funding (Long Term Future Fund, EA Funds)**
- **Effective Ventures Foundation grants**

Discovery queries:
- "new AI fellowship 2026 applications open"
- "AI safety summer program undergraduate 2026"
- "ML research fellowship 2026 stipend"

---

## CATEGORY 2D: Founder / Builder Programs

Frequently overlooked even though many run rolling and pay $5–$100k:

- **Y Combinator** (S26 and W27 batches; check timing)
- **Z Fellows** (1-week dinners + $10k for builders)
- **Pioneer** (online tournament, prize + grant)
- **Emergent Ventures** (Mercatus / Tyler Cowen) — rolling
- **Thiel Fellowship** (annual, $250k for under-22 founders dropping out)
- **1517 Fund Medici Project**, **1517 MEDICI scholarships**
- **South Park Commons Fellowship**
- **Neo Scholars**
- **Sequoia Arc**
- **a16z Talent x Opportunity (TxO)**, **a16z Open Source AI Grant**, **a16z American Dynamism Fellowship**
- **Stripe Press / Stripe Press summer program**
- **Mercor Fellowship**, **Mercor Build**
- **Founders Inc Fellowship / F.inc Camp**
- **Antler Residency** (multiple cities)
- **Contrary Talent / Contrary Capital**, **Contrary Fellowship**
- **8VC Build**, **8VC Fellows**
- **General Catalyst Creation**, **GC Beacon**
- **Greylock Edge**
- **Replit Bounties, Replit Effect, Replit Fellowship**
- **Soma Capital Fellowship**, **Soma Capital Scout**
- **The Residency** (SF house-based program)
- **Lightcone Infrastructure programs**
- **Pillar VC Founder Internships**
- **Lux Capital Lab**
- **NFX Founder programs**
- **AI Grant** (Nat Friedman / Daniel Gross)
- **AI Tinkerers events / grants**
- **Atomic Studio Fellowship**
- **Susa Ventures Network Catalyst**
- **Khosla Ventures Fellows**
- **Greylock Hacker House**

Discovery queries:
- "founder fellowship 2026 undergraduate application open"
- "AI residency 2026 paid program"
- "builder grant 2026 student"

---

## CATEGORY 2E: VC Scout / Fellow / Student Investor Programs

Most undergrads have no idea these exist:

- **Dorm Room Fund (DRF)** — recruits each semester
- **Rough Draft Ventures (General Catalyst)** — undergrad investor program (now GC Venture Fellowship)
- **Sequoia Scouts**
- **Bain Capital Ventures Future Operators**
- **Bessemer Fellows**
- **First Round Graduate Fund / First Round Fast Track**
- **Lightspeed Summer Fellows / Lightspeed Scouts**
- **NEA Edison Scholars**
- **Kleiner Perkins Fellows**, **KP Engineering Fellows**, **KP Design Fellows**, **KP Product Fellows**
- **8VC Fellows**, **8VC Designer in Residence**
- **Contrary Network** (campus VC analyst program)
- **Soma Capital Scouts**
- **Pear VC PearX, Pear Garage**
- **Index Ventures Origins**
- **a16z Campus Connect**
- **General Catalyst Student Investor**
- **Floodgate Fellows**
- **Susa Ventures Network Catalyst**
- **Republic / AngelList Scout programs**

Discovery queries:
- "venture capital fellowship undergraduate 2026 application"
- "campus scout program VC 2026"
- "student investor program 2026 application"

---

## CATEGORY 2F: VC Events, Parties, Dinners & Summits

The undocumented but highly valuable layer of opportunity. Check Luma, Partiful, X (Twitter), and event calendars:

- **SF Tech Week, NYC Tech Week, LA Tech Week, London Tech Week, Boston Tech Week**
- **YC Demo Day** + adjacent founder dinners
- **YC AI Startup School**
- **Cerebral Valley AI Summit**
- **AI Engineer Summit / World's Fair**
- **HumanX**
- **SXSW** (Austin, March)
- **South Summit, Slush** (international)
- **TechCrunch Disrupt** (student scholarship tickets)
- **Web Summit** (Lisbon, student tickets)
- **DEF CON**, **Black Hat** (security)
- **Hack Club / Hack Summit**
- **Pioneer Summit**
- **Lightcone Infrastructure events**
- **a16z Speedrun events**
- **GitHub Universe**
- **NeurIPS / ICML / ICLR** social events
- **Y Combinator Founder Summer events**
- **Mercor builder dinners**
- **Z Fellows Friday dinners**
- **The Residency, Genesis, Tech Tree house events**
- **OpenAI / Anthropic / Cohere developer days**
- **Vercel Ship, Linear Mainline, Notion Make, Figma Config**
- **Stripe Sessions**
- **Various YC-backed startup Halloween / holiday parties** (announced last-minute on X / Luma)

Discovery queries:
- "SF tech week 2026 schedule events"
- "AI founder dinner 2026 luma"
- "tech week party invite undergraduate student"
- "VC event 2026 student scholarship"

---

## CATEGORY 2G: Research Programs (REUs, Industry Research, National Labs)

For students who might be PhD-curious or want a research stamp:

- **NSF REUs** (search by field on nsf.gov)
- **MIT MISTI, MIT SuperUROP, MIT UROP**
- **Caltech SURF**
- **Princeton SURP, Princeton Plasma Physics, PCTS**
- **Stanford UGVR, Stanford Bio-X, CURIS**
- **Harvard PRISE, Harvard REU**
- **NIST SURF**
- **HHMI Janelia Undergraduate Scholars**
- **Allen Institute** (Brain, Cell, Immunology) summer programs
- **DOE SULI** (Science Undergrad Lab Internship), **DOE CCI**
- **NASA / JPL Internship Program**
- **DARPA Forward / DARPA Riser**
- **DAAD RISE Germany**
- **Microsoft Research Internship, Microsoft Research Fellowship**
- **Google Research Internship, Google AI Residency**
- **IBM Research Internship**
- **Meta AI Residency / FAIR internship**
- **Adobe Research Internship**
- **NVIDIA Research Internship, NVIDIA Graduate Fellowship**
- **OpenAI Researcher Access**
- **DeepMind Research Internship**
- **Bell Labs Summer Research**
- **Cambridge, Oxford summer research bursaries**
- **Sandia, Los Alamos, Argonne, Berkeley Lab internships**
- **MITRE summer internship** (cleared work)
- **Mitsubishi Electric Research Labs (MERL)**

Discovery queries:
- "REU 2027 undergraduate research computer science application"
- "industry research internship 2027 undergraduate"
- "national lab summer 2027 internship"

---

## CATEGORY 2H: Conferences with Scholarships & Recruiting

Many fund travel + housing and double as job fairs:

- **Grace Hopper Celebration (GHC) — AnitaB.org**
- **Tapia Conference** (CMD-IT)
- **SHPE National Convention** (Society of Hispanic Professional Engineers)
- **NSBE National Convention** (Black Engineers)
- **oSTEM National Conference** (LGBTQ+ STEM)
- **Out for Undergrad (O4U)** — Tech, Engineering, Marketing, Business
- **Reaching Out MBA undergrad track**
- **Rewriting the Code conferences**
- **ColorStack convenings**
- **ACM-W conference travel scholarships**
- **NeurIPS, ICML, ICLR Diversity & Inclusion travel awards**
- **DEF CON Scholarships (HackerOne, EFF)**
- **DefCamp**, **CactusCon** (security regional)
- **AfroTech**
- **Latinx in AI workshops**
- **Black in AI workshops**
- **WiCS / Women in CS regional conferences**
- **HackCon (MLH organizer conference)**
- **GeekWire Summit**
- **TED, TEDx student programs**

Discovery queries:
- "Grace Hopper 2026 student scholarship application"
- "tech conference 2026 undergraduate travel grant"

---

## CATEGORY 2I: Trading / Quant / Math Competitions

- **IMC Prosperity**
- **Jane Street ETC, Estimathon, Real Estate Investment Trust**
- **Citadel Trading Competition, Datathon, Terminal Live**
- **Optiver Trading Challenge, Optiver Insight**
- **SIG Trading Game, SIG Quant Challenge**
- **HRT Algo Engineering Challenge**
- **DRW Trading Challenge**
- **Akuna Coding Challenge, Akuna Options 101**
- **Two Sigma Halite, Battlecode**
- **Putnam Mathematical Competition** (December)
- **ICPC (International Collegiate Programming Contest)**
- **Kaggle competitions**
- **Numerai**
- **AIcrowd, DrivenData, Zindi** (ML competition platforms)

## CATEGORY 2J: Case & Business Competitions

- **Bain Cup, Bain Build a Brand**
- **BCG Build Together / Strategy Cup**
- **McKinsey Forward, McKinsey Equip**
- **National Investment Banking Competition (NIBC)**
- **Wharton Investment Competition**
- **HKUST Business Case Competition**
- **Cornell Hospitality Case Competition**
- **HBS New Venture Competition**
- **Deloitte National Undergraduate Case Competition**
- **John Molson MBA International Case Competition** (undergrad version)
- **University of Chicago Booth Investment Banking Group case comp**
- **Wharton MUSE, Wharton Pricing Competition**
- **Wells Fargo Net Impact**

---

## CATEGORY 2K: Open Source & Maker Programs

- **Google Summer of Code (GSoC)**
- **MLH Fellowship**
- **Outreachy**
- **Linux Foundation Mentorship**
- **Rust Project mentorship**
- **CNCF Mentorship**
- **Buildspace S-cohorts, Nights & Weekends**
- **100Devs**
- **The Odin Project, Boot.dev community programs**

---

## CATEGORY 2L: Scholarships & Major Fellowships

- **Hertz Foundation Fellowship** (PhD STEM)
- **NSF GRFP** (juniors/seniors)
- **Goldwater Scholarship** (sophomore/junior)
- **Truman Scholarship** (junior)
- **Knight-Hennessy Scholars** (senior)
- **Rhodes, Marshall, Mitchell, Gates Cambridge, Schwarzman, Fulbright** (mostly seniors)
- **Beinecke Scholarship** (junior)
- **Udall Scholarship**
- **Astronaut Scholarship**
- **Hispanic Scholarship Fund, UNCF, APIA**
- **Jack Kent Cooke**
- **Davis Projects for Peace**
- **Critical Language Scholarship (CLS), Boren, Gilman, Fulbright UK Summer**
- **Schmidt Science Fellows, Schmidt Futures Rise**

---

## CATEGORY 2M: Government / Policy / National Security

- **White House Internship Program**
- **Congressional Internships** (House, Senate, committees)
- **State Department Student Internship Program**
- **State Dept Rangel & Pickering Fellowships** (diversity, foreign service pipeline)
- **DOE Pathways, DOD SMART Scholarship**
- **CIA Stokes Educational Scholarship, CIA Undergraduate Internship**
- **NSA Stokes, NSA Summer Programs (DSP, GenCyber)**
- **FBI Honors Internship**
- **Aspen Strategy Group, Aspen Tech Policy Hub**
- **Knight First Amendment Institute fellowships**
- **Truman National Security Project**
- **Coro Fellowship in Public Affairs**
- **New America Fellowships**
- **CSIS, RAND, Brookings, Hudson** internships

---

## CATEGORY 2N: Pre-Internship / Identity & Affinity Pipelines

Frequently the highest-leverage opportunities — often pay for travel + mentorship + guaranteed interviews:

- **Sponsors for Educational Opportunity (SEO)** — Career, Tech Developer
- **Management Leadership for Tomorrow (MLT) CP / Career Prep**
- **Code2040 Fellows**
- **ColorStack opportunities + Career Fairs**
- **Rewriting the Code (RTC) Fellowship + targeted programs**
- **Girls Who Invest (GWI)**
- **Greenwood Project**
- **Toigo Foundation MBA fellowship undergrad pipeline**
- **AKPsi, Smart Woman Securities** chapter recruiting
- **Codepath Tech Fellows, Codepath Cybersecurity / iOS / Web tracks**
- **Headstarter AI**
- **Out in Tech U**
- **Lesbians Who Tech, /dev/color**
- **Latinas in Tech Mentorship**
- **POSSE Foundation**
- **JumpStart, Year Up** (for community college / non-trad)

---

## CATEGORY 2O: Product Management / APM Programs

A major non-engineering path that this list historically under-covered. APM/RPM programs are prestigious, well-paid, and recruit on their own (often early-fall) timelines:

- **Google APM** (and STEP-equivalent for PM)
- **Meta RPM (Rotational Product Manager)**
- **Uber APM**, **Lyft APM**
- **DoorDash APM**, **Atlassian APM**, **Salesforce APM (Futureforce PM)**
- **Microsoft PM intern programs**
- **Yahoo APM**, **LinkedIn APM**, **Robinhood APM**, **Snap APM**
- **Twitch / Coda / Asana / Dropbox PM intern programs**
- **APMList.com** — community-maintained APM program directory (use as the aggregator)

Discovery queries:
- "APM program 2027 application open"
- "associate product manager new grad 2027 apply"
- "product management internship 2027 undergraduate"

---

## CATEGORY 2P: Aerospace & Space Fellowships

Prestige programs in aviation/space — paid, mentored, internship-placing, and almost always missed by general career services:

- **Brooke Owens Fellowship** — for women & gender-minority undergrads in aerospace; paid internship + mentorship + summit
- **Matthew Isakowitz Fellowship** — for junior/senior/grad students in commercial spaceflight; internship + mentor + summit
- **Patti Grace Smith Fellowship** — for Black undergraduates in aerospace; internship + mentorship
- **Zed Factor Fellowship** — broadening access to aerospace careers
- **NASA OSTEM internships, NASA Pathways**
- **AIAA scholarships**, **Astronaut Scholarship** (also in 2L)

Discovery queries:
- "Brooke Owens Fellowship 2027 application open"
- "Matthew Isakowitz Fellowship deadline"
- "aerospace undergraduate fellowship 2026 paid"

---

## CATEGORY 2Q: Standing Prizes & "Weird One-Offs"

Open, ongoing competitions with cash — exactly the under-the-radar bucket this digest is supposed to catch:

- **ARC Prize (ARC-AGI)** — large cash prize for progress on abstract reasoning benchmark
- **Vesuvius Challenge** — cash prizes for reading carbonized Herculaneum scrolls with ML
- **XPRIZE** competitions (various tracks)
- **Hutter Prize** (text compression)
- **Millennium / Clay Math problems** (long-shot, but real)
- **Kaggle "featured" competitions** with large purses
- **AI Mathematical Olympiad (AIMO) Prize**
- **Hackathon "grand challenge" tracks** with standing bounties (e.g., protocol/foundation bounties)

Discovery queries:
- "open AI prize competition 2026 cash"
- "research bounty 2026 student eligible"
- "new XPRIZE / benchmark prize launched 2026"

---

## CATEGORY 2R: International / Non-US Programs

Run at least one discovery pass here every day — the rest of this file skews heavily US:

- **Entrepreneur First (EF)** — global founder program (London, Bangalore, SF, etc.)
- **Antler** (already in 2D, but emphasize non-US cohorts)
- **Mitacs Globalink Research Internship** (Canada) — funded summer research for international undergrads
- **Amgen Scholars** (international host sites — Cambridge, ETH Zurich, Tokyo, etc.)
- **DAAD RISE** (Germany — also in 2G)
- **UK quant/finance spring weeks** (London desks of Citadel, Jane Street, Optiver, SIG, IMC)
- **Quant internships in Hong Kong / Singapore / Amsterdam**
- **Slush (Helsinki), South Summit, Web Summit, Slush'D** — European startup events with student tickets
- **Recurse Center** (NYC but globally relevant)
- **Tony Blair Institute, Schmidt-funded** international policy fellowships

Discovery queries:
- "Entrepreneur First cohort 2026 application"
- "Mitacs Globalink 2027 application"
- "European founder fellowship undergraduate 2026"
- "London spring week quant 2027"

---

## CATEGORY 2S: Bio / Health & Climate / Energy Programs

Depth beyond the company lists in Category 2, for students with a science bent:

**Bio / health:**
- **iGEM** (international synthetic biology competition)
- **Amgen Scholars** (US + international)
- **NIH IRTA / Summer Internship Program**
- **Fred Hutch, Broad Institute, Cold Spring Harbor** summer programs
- **Biosecurity fellowships** (e.g., NTI, Johns Hopkins Center for Health Security)
- **Nucleate** (student-run biotech venture program)

**Climate / energy:**
- **Activate Fellowship** (hard-tech / climate)
- **Breakthrough Energy Fellows**
- **Terra.do, Climatebase** fellowships/job board
- **Greentown Labs** programs
- **DOE clean-energy internships**, **ARPA-E**
- **Watt Club / climate founder communities**

Discovery queries:
- "synthetic biology competition 2026 undergraduate"
- "climate tech fellowship 2026 student"
- "biotech summer program undergraduate 2027"

---

## OUTPUT FORMAT — THREE FILES, STRICT SEPARATION

Every run writes **three files**. Do not merge them. The digest and the open list are for the user. The run log is for the pipeline.

**The one-sentence test that decides where a line goes:** if the line is about a job, program, event, or deadline, it goes in the digest. If it is about the pipeline — a tool, a browser, a query, a lane, a suppress-gate result, a clock, a filter echo, a prior run, a method finding — it goes in the run log. No exceptions. A digest that contains pipeline talk has failed the format contract, even if every fact in it is true.

### File 1 — `opportunities/digest-YYYY-MM-DD.md` (the brief)

**Hard caps: 800 words and 120 lines, total.** Count before you save. If the file is over the cap, cut detail from the bottom sections — never from Apply now. These caps are the contract; a 5,000-word digest is a failed run even if its content is good.

Template. Use these exact sections, in this order, and no other sections:

```
# Daily Opportunities Digest — [today's date]
[1-2 sentence orientation. If a missed run or a broken source CHANGES what the user
should do today, one plain sentence about it here — and that is the only place
pipeline reality may touch this file.]

## ✅ Apply now — ranked by FIT (max 6)
[THE decision layer. Open + eligible + strong fit. RANK BY FIT, not by deadline.
Per item, exactly this shape, no nested caveat stacks:
**Name** — what it is (<10 words). One line on why it fits. One line max for a
gate or date warning, only if it changes the decision. **closes <verified date>**
OR **rolling — do it soon**. One link.]

### 🔁 Rolling, high-fit (protected slot — max 4)
[Open, strong-fit, no closing date. One line each. If empty, one line.]

## ⏰ Deadline radar
[TABLE ONLY, soonest first, ⚠️ if ≤14 days. Only deadlines verified on the
official source; otherwise write "unconfirmed".
| Deadline | Item | Fit (Strong/Possible/Stretch) | Link |]

## 📅 Opening soon (watch list)
[From the state file, one line per program: name + expected open month + the one
prep step worth doing now. Max 10 lines.]

## 🆕 Also new today (max 10)
[One line each for new keepers that did not make Apply now. Name, <10-word
descriptor, date or "rolling", link. Everything else new goes into the state
file's Open Now table (and so into OPEN-LIST.md) — NOT here. The full per-source
sweep detail (Handshake / LinkedIn / SWElist keepers, drops, suppressions) lives
in the run log.]

📂 Full open backlog (N roles): [opportunities/OPEN-LIST.md] — refreshed today.
```

That is the whole file. **The digest contains NO coverage log, NO corrections section, NO method findings, NO lane or wave reports, NO per-source sections, NO suppress-gate output, NO notes addressed to the next run.** It does not re-list the standing open backlog; that lives in `opportunities/OPEN-LIST.md` (File 3), which the digest links to in one line.

Fit tiers and eligibility traps: a trap (wrong class year, term overrun, unpaid, wrong geography) means the item simply does not appear in the digest. Record the reason in the state file (so it is not re-derived) and, if newly discovered this run, one line in the run log.

### File 2 — `opportunities/OPEN-LIST.md` (the standing backlog, for the user to browse)

Refreshed every run: **fully rewritten from the state file's Open Now table, never appended.** One compact table row per still-open, un-applied, non-snoozed role — grouped by category, `⏳ drafted` items flagged first. Columns: Item · What/Why (short) · Deadline or "rolling" · Link. No prose paragraphs, no history, no telemetry. This file is how the user directive of 2026-06-07 (nothing open may silently disappear) is satisfied without re-listing the backlog inside the digest.

**🚨 BEFORE SHIPPING THIS FILE, RUN `python3 opportunities/verify_open_list.py` AND DO NOT SHIP ON A NON-ZERO EXIT (standing rule, after the user opened a session to apply to a program this file listed as open and that had closed months earlier).** The Harvard Kempner summer internship sat in OPEN-LIST under the heading *"every still-open, un-applied opportunity"* while its own page read verbatim *"This application is now closed."* and the 2026 program had already ENDED three days before. **Nothing overrode the status. The status was never read.**

**The mechanism, because it will recur in any positional generator:** the Open Now table's canonical header is **6 columns** (`Program | What / why | Category | Deadline | Verified? | Link`). The 2026-08-24 consolidation made the rationale a deliberate column, normalized the table, and moved clustered or unverified legacy leads to `opportunities/verification-backlog.md`. Every live row must represent one opportunity and carry one official link.

Two rules follow, and they are cheap:

1. **Write every Open Now row at exactly the six-column header's width.** Never add a local extra pipe. Never place multiple roles or multiple official links in one row. If a discovery cannot be split and verified in the same run, put it in `opportunities/verification-backlog.md` with a precise blocker and retry condition. Rule 8A requires the automation to process that backlog automatically.
2. **Filter on status, and make the filter visible.** A row whose state entry says closed, not yet open, opening soon, next cycle, or already ended is **not an open opportunity and does not belong in OPEN-LIST at all.** If a closed-but-worth-watching item should stay visible, it goes in a separate `## 🔒 Not open yet — check dates, do not apply` section with the reopen date in the Deadline column, never in the open tables. **A `CHECK ~JANUARY` note buried in the state file is not a substitute: OPEN-LIST is the file the user actually browses, so it is the file that has to be right.**


### File 3 — `opportunities/runlogs/runlog-YYYY-MM-DD.md` (the pipeline's record)

Everything operational goes here, with no length cap:

- **Coverage log** — the accountability record for the coverage contract (rule 7), including every REQUIRED line: preflight, lane completion, per-tier sources hit/skipped with reasons, Handshake filter-echo confirmation, each email source named separately with raw/keeper counts, suppress-gate stats, state-file compaction, shortfall.
- **Per-source sweep detail** — keepers, drops, suppressed items, noise clusters, raw counts per source.
- **Corrections and contradictions** — tracker rows to fix, reversed findings, stale-site traps, tool failures and workarounds.
- **Recommended opening moves for the next run** (max 5, ranked).

The next run's preflight reads the **latest run log only** (for the opening moves and any unresolved corrections). Older run logs are history, not instructions — never re-read or re-summarize them into a new digest.

### Where standing knowledge lives (write once, not daily)

A finding that must outlive the run gets ONE permanent home, edited at the moment of discovery — never carried forward from digest to digest:

- **Method findings, workarounds, standing instructions** (a working URL pattern, a fetch trick, a source's quirk, "date the digest from the inbox not the shell clock") → edit `references/search-plan.md`, the relevant sub-skill's SKILL.md, or the state file's method sections. Then one line in the run log saying what was edited and where.
- **Run-to-run state** (seen-lists, snoozes, open/closed/opening-soon, per-item kill reasons) → the state file, per rules 2 and 8.
- **Repo bugs** (e.g. a script needing a patch) → one line in the run log's corrections; the tracked fix belongs in the repo, not restated in prose every day.

**The tripwire: if the same warning or finding would appear in a second consecutive run's output, it belongs in a permanent home instead. Write it there and stop repeating it.**

At the end of the run, update `opportunities/opportunities-state.md` (open / closed-this-cycle / opening-soon) so tomorrow's digest builds on today's instead of repeating it.

Tone for the digest: direct, briefing-style. Assume the reader is sharp and short on time. The test: The user reads the whole digest in under three minutes and knows exactly what to do today.
