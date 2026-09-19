# Search Plan: the portal & query directory

This is the operational backbone of the daily sweep. The main `SKILL.md` lists *what kinds* of opportunities to look for; this file lists *exactly where and how to look*, with copy-pasteable URL patterns and query templates.

Why this file exists: the failure mode of a daily research digest is doing a handful of generic web searches, finding the same well-indexed programs every time, and missing the long tail of roles that live on individual company boards no aggregator has crawled yet. A precise, repeatable search plan is what turns "I searched the web" into real coverage. Work through the tiers below. Tier 0, Tier 1 and Tier 2 are the per-run floor (see the Coverage Contract in SKILL.md); Tiers 3-4 rotate.

## Contents
0. Tier 0, Read the board as JSON (do this before any HTML fetch)
1. Tier 1, Direct ATS search (highest leverage, often skipped)
2. Tier 2, Live aggregators & trackers
3. Tier 3, Startup & VC-portfolio job boards
4. Tier 4, Category-specific aggregators
5. Query template bank
6. How to read results (what counts as a real hit)

---

## Tier 0: read the board as JSON before you fetch any posting page (standing rule)

Greenhouse, Lever, and Ashby each publish every company's entire job board as public JSON. No key, no login, no browser. Once a `site:` search in Tier 1 hands you a company slug, stop fetching individual posting pages and pull the whole board instead. One request returns every open role at that company with the full description text, the location, whether it is on-site, and usually the pay band.

| ATS | URL pattern | Where the slug comes from |
|---|---|---|
| **Ashby** | `https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true` | `jobs.ashbyhq.com/<org>/<uuid>` |
| **Greenhouse** | `https://boards-api.greenhouse.io/v1/boards/<org>/jobs?content=true` | `job-boards.greenhouse.io/<org>/jobs/<id>` |
| **Lever** | `https://api.lever.co/v0/postings/<org>?mode=json` | `jobs.lever.co/<org>/<uuid>` |

All three verified working in a past run (Ashby against NationGraph, Greenhouse against `eventsandinterns`, Lever against `palantir`).

**The fields that answer the questions this digest keeps failing to answer:**

- **Ashby:** `title`, `location`, `workplaceType` (`OnSite` / `Remote` / `Hybrid`), `employmentType`, `isListed`, `publishedAt`, `compensation.compensationTierSummary`, and `descriptionPlain`, which is the entire posting as plain text with the class-year gate in it.
- **Lever:** `text` (title), `categories.location`, `categories.commitment`, `categories.team`, `workplaceType`, `country`, `createdAt`, `hostedUrl`, `applyUrl`, `descriptionPlain`.
- **Greenhouse:** `title`, `location.name`, `absolute_url`, `first_published`, `updated_at`, `metadata` (often carries the compensation fields), and the full posting body in `content` when `?content=true` is set.

**Three things this settles.**

1. **The Ashby JavaScript wall is gone.** A posting page at `jobs.ashbyhq.com/<org>/<uuid>` returns an empty shell, which is why this file's Ashby entries sat unread for weeks and why run after run concluded "needs a logged-in browser pass, cannot be resolved by more searching." That conclusion was wrong. **Do not write "gate unread" for an Ashby, Greenhouse, or Lever role until the JSON has been tried.**
2. **Closed detection becomes exact, with one weakening.** A dead requisition is simply absent from the array. That is stronger than the older heuristics in `opportunities-state.md` (the `meta-description` teaser read, and "a dead Ashby req returns the page title `Jobs`"); keep those only for boards with no JSON. Note that a **wrong org slug returns HTTP 404**, which means "check the slug", not "this company has no openings". ⚠️ **Weakened 2026-08-26: on Greenhouse, absence from the array is NOT by itself proof of closure**, because large boards can exceed the fetch ceiling and truncate. Confirm a Greenhouse closure against the single-job endpoint before recording it.

**Size limits, and they are asymmetric between the three ATSes (2026-08-25, extended 2026-08-26).**

- **Greenhouse:** on a board with many reqs, skip the full-board call and go straight to the single-job endpoint from the `site:` hit, e.g. `.../<org>/jobs/<id>`. ATOMS's full board returned 94,823 characters and blew the fetch ceiling while the single job returned in full.
- 🚨 **Lever is the opposite and the Greenhouse habit will silently fail here. The single-posting endpoint `https://api.lever.co/v0/postings/<org>/<id>` returns an EMPTY BODY**, verified against both `plus-2` and `actian`, with and without `?mode=json`, while the org-level list endpoint for the same slug returned full data. **On Lever, page the org list; there is no working single-job fallback.** A very large Lever board (Shield AI, 117,738 chars) may be unrecoverable by any route.
- 🚨 **Ashby has no escape hatch either: the single-posting endpoint `/job-board/<org>/<postingId>` returns an EMPTY BODY**, so only the whole-board endpoint works. Large Ashby boards (71k–116k chars) arrive as one unsplittable JSON line and must be read with a bounded `Grep -o`. 🆕 **2026-08-27: `web_fetch` truncates at roughly 108,000 characters and silently cuts the JSON array mid-way, so absence from a truncated Ashby or Greenhouse array is NOT closure** (Notion returned only 7 of its jobs this way). **Two escapes.** (a) On Ashby the complete untruncated array is embedded in the posting page at `window.__appData.jobBoard.jobPostings` and can be read with `javascript_tool` in Chrome; that defeated the truncation on Cohere (145 postings) and Meshy (21). (b) The **individual Ashby posting page's `meta-description` is fully server-rendered** and carries the job text, though Circleback, Quadrillion, Georgian and Rilla set a custom SEO description that hides it and need the board API instead. ⚠️ `Grep -o` silently omits any match longer than roughly 200 characters, so keep the windows small. Note the persisted **`.json`** wrapper escapes the payload (patterns must be written `\\"title\\":\\"...`) while persisted **`.txt`** files are unescaped and take plain `"title":"..."`.

**Two mirrors that recover req text when the employer's own tenant is unreadable (banked 2026-08-26).**

- **`careers.nsbe.org`** carries full verbatim requisition text for large employers. This is what cracked BNY's class-year gate after its Workday tenant returned an empty body across several runs.
- **`indeed.com/viewjob?jk=<id>`** is a reliable server-rendered mirror for **federal and intelligence-community postings**. This is what produced the NSA SPORT eligibility text after `cgo.corporategray.com` returned HTTP 200 with a completely empty body.

**`web_fetch` quirks worth knowing before you burn calls on them.**

- 🚨 **The dedup cache is keyed on the exact URL string, and a bare `?` appended to the URL bypasses it.** A lane can receive *"Already fetched … Ns ago in this session"* for a URL it has never fetched, including in a fresh subagent context. Appending `?` returns the full page. This is cleaner than the older "drop the `en-US` segment" workaround.
- ⚠️ **Several hosts return an empty body for `application/json` responses** (Microsoft's `gcsservices` and Eightfold job APIs, NVIDIA's Workday CXS, Lockheed's Eightfold API) while serving HTML fine. This does **not** apply to the three Tier 0 endpoints above, which work. Expect Eightfold and Workday JSON APIs specifically to need the Chrome browser tools instead.
3. **Location and workplace type are one field each, so read them first.** A role that is on-site outside the continental US is dead on a standing deal-breaker no matter what the graduation gate says. NationGraph's Winter 2027 SWE req was carried in the state file as "gate unread" from 8/04 to 8/21, across at least four runs and three digests, while the API returned Toronto, `OnSite`, and CA$6,000-8,000 per month in a single request. The location killed it, not the class year.

🚨 **THE GREENHOUSE AND LEVER ORG-LEVEL BOARDS SILENTLY UNDERCOUNT (standing rule, four companies confirmed).** `boards/thenuclearcompany/jobs` returned 33 jobs with **none of its intern reqs** and nothing updated after 2026-06-17; `boards/dvtrading/jobs` returned 58 jobs and **omitted both 2027 intern reqs**; `boards/ctccampusboard/jobs` returned `{"jobs":[],"meta":{"total":0}}` because the board is flagged *"External, Not Advertised."* **In all three cases the single-job endpoint `/jobs/<id>` returned full live content.** Lever does the same: `api.lever.co/v0/postings/belvederetrading?mode=json` returned 7 postings, all Full-Time and no interns, while three Belvedere intern postings were live at public `jobs.lever.co` URLs. **So absence from a Greenhouse or Lever org array proves nothing.** Confirm against the single-job endpoint on Greenhouse, or the public HTML posting page on Lever, before recording any closure.

🚨 **THE WORKDAY CXS ENDPOINT IS GET-ABLE AND IGNORES THE LOCATION SEGMENT (standing rule, and this is the single most reusable finding of that run).** Pattern: `https://<tenant>/wday/cxs/<tenant>/<site>/job/<ANY-string>/<Title-slug>_<ReqId>`. It returns the **full JSON posting**: verbatim gate text, pay band, every location, the close date, and a **`similarJobs` array that surfaces sibling requisitions for free** (that is how Blackstone's Cybersecurity req 45023 was discovered from 45021). The **title slug is still required** and a wrong slug returns empty; the location segment can be anything. This turns any known Workday job URL into a cheap, reliable re-check. 🚨 **SUPERSEDED IN PART, 2026-09-11: WORKDAY *CAN* BE ENUMERATED, FROM INSIDE THE BROWSER PANE.** The GET note below stands, but the "no Workday tenant can be searched" limitation does not. **Park a browser tab on the tenant's own origin, then issue a same-origin `POST` to `https://<tenant>/wday/cxs/<tenant-name>/<site>/jobs`** with body `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"<query>"}`. It returns `total` plus a `jobPostings` array carrying each title and the `externalPath` that holds the requisition ID. Proven on seven tenants in one session: `troweprice/troweprice`, `thehartford/Careers_External` and `Careers_Restricted`, `pwc/US_Entry_Level_Careers`, `gilead/gileadcareers`, `capitalone/Capital_One`, `mastercard/Campus`, `intel/External`. 🚨 **AND THE COUNT IT RETURNS IS NOT ALWAYS A FILTERED COUNT (standing rule, found the same hour the POST started working).** On `labcorp.wd1` a `searchText` of `Intern Data Science` returned **`total: 1584` with titles like Phlebotomist and Specimen Processor**, which is the whole board. On `fiserv.wd5` a `searchText` of `Intern` returned `total: 212` against a 399-job board, with Director and CNC Machinist in the first ten results. Other tenants filter correctly (T. Rowe Price 10, GE HealthCare 14, Autodesk 41). **So a Workday POST count is evidence only when the returned titles actually match the query. The safe method, and the one to use for any closure claim, is to page the whole board with an empty `searchText` and filter titles client-side.** That is what proved Fiserv has no intern requisition at all.

⚠️ **The site name matters and is often not `Careers`.** The Hartford runs two sites and neither is `Careers`; a wrong site silently redirects to Workday's own `invalid-url` page, which reads like a bot block. ⚠️ Cross-origin `POST` is refused, so navigate to the tenant first. ⚠️ A tenant can freeze the renderer; a 45-second timeout is a retry, not a finding.

⚠️ **It does NOT solve enumeration**: Workday's `/wday/cxs/.../jobs` *search* endpoint is **POST-only**, so no Workday tenant can be searched from a GET-only fetcher. That single limitation blocked ~30 verification-backlog rows in a past run and needs a rendering browser, not more fetching.

⭐ **BANK OF AMERICA PUBLISHES ITS ENTIRE CAMPUS BOARD AS PUBLIC RSS (standing rule).** Programmes: `https://bankcampuscareers.tal.net/vx/mobile-0/candidate/jobboard/vacancy/1/feed` · Events: `.../vacancy/2/feed`. Fully fetchable, with per-programme closing dates, cities and line of business. It is how the **absence** of a 2027 sophomore req was established as evidence rather than a guess, and it is the best early-warning source for the whole BofA campus family.

⭐ **WORKABLE HAS A PUBLIC JSON API that defeats its client-side shell (standing rule):** `https://apply.workable.com/api/v2/accounts/<subdomain>/jobs/<shortcode>` returns `location`, `locations`, `workplace`, `description`, `requirements` and `published`.

🚨 **LEVER: PAGE THE PUBLIC HTML BOARD, NOT THE ORG JSON (standing rule, superseding the earlier advice to page the org list).** `api.lever.co/v0/postings/<org>?mode=json` blows the fetch ceiling on any real board (Belvedere returned 107,191 characters, and **86,698 even with `&limit=5&skip=0`**), and the saved payload is one unsplittable line. ✅ **The public board `https://jobs.lever.co/<org>` renders every posting with title, commitment, workplace type and location in a few kB, and supports `?commitment=Intern` filtering.** That is what finally read Shield AI's 117,738-character board after two runs of failure. Use it as the standing Lever surface.

⚠️ **GREENHOUSE: DROP `?content=true` ON MID-SIZE BOARDS (standing rule).** The bare `https://boards-api.greenhouse.io/v1/boards/<org>/jobs` endpoint is compact and returns id, title, location, `first_published` and `application_deadline`, which is enough to triage; then fetch `/jobs/<id>` for the full text. `?content=true` returned 70,569 characters for a 33-job board and 94,823 for another.

🚨 **PHENOM AND FINDLY "NO RESULTS" PAGES ARE NOT NO-RESULTS PAGES, and they nearly produced four false closures in a past run.** TJX, Lowe's, O'Reilly and Thermo Fisher all rendered `No results for "${pageStateData.searchKeyword}"` — that **literal unevaluated template token** proves the page never hydrated. Home Depot's Findly shell has the same signature, printing a hardcoded "0 Live Results" plus one placeholder card for *every* query, and Costco's Phenom `/api/jobs` endpoint **silently ignores `keyword`** and returns default warehouse jobs. **Never score any of these as zero.**

⚠️ **`web_fetch` rejects URLs longer than roughly 200 characters** (observed 2026-08-28). Compose long Workday URLs with that in mind.

⚠️ **Levels.fyi is dead for the 2027 cycle (standing rule), not merely unreadable.** Its internships table is client-rendered **and its season selector tops out at Summer 2026**, so no 2027 data exists on the page at all. Deprioritise it in the Tier 2 rotation until a 2027 season appears.

⭐ **EngRadar (`https://engradar.com`) promoted to a Tier 2 source 2026-08-27 and first swept 2026-08-28.** Its homepage and `/entry-level-tech-jobs` view server-render; `/search?q=...` is client-side and returns an empty body. Honest yield note: the entry-level view is dominated by full-time junior roles and non-US listings, so it is a low-yield source for 2027 interns.

🚨 **THE ESCAPE HAS A PRECONDITION AND IT IS THE CALLING PAGE'S CSP (standing rule, after it cost two attempts to find).** The tab you park on governs the fetch. **`raw.githubusercontent.com` serves `Content-Security-Policy: default-src 'none'`, so parking a tab there and fetching from it ALWAYS fails with `TypeError: Failed to fetch`** — which reads exactly like the source being unreachable. **Park on `https://example.com` first, then `fetch()` the raw URL and filter in-page; GitHub sends `Access-Control-Allow-Origin: *`.** Doing this broke a five-run SimplifyJobs truncation streak and a four-run 80,000 Hours failure streak in the same call. 80,000 Hours additionally renders fine under plain browser navigation; `web_fetch` was never the right tool for it.

🚨 **THE WEBSEARCH QUOTA (200) AND THE BROWSER PANE ARE SHARED ACROSS PARALLEL SUBAGENTS (standing rule).** One lane can exhaust the quota in its first sector and silently bind every later lane, and parked tabs get hijacked mid-task. **Lead each lane with direct board fetches rather than WebSearch, pass `tabId` explicitly on every browser call, and re-check `location.href` inside any JS payload.** A lane that hits the wall must name its unreached targets rather than inferring closures from an unrun search.

⭐ **THE STANDING ESCAPE FROM TRUNCATION AND PROVENANCE REFUSALS (standing rule).** When `web_fetch` truncates a board, refuses an origin, or returns an empty body, **run `fetch()` from inside the browser pane via `javascript_tool`, with the tab parked on the API's own origin**. That bypasses both the provenance allowlist and the roughly 108,000-character ceiling, and it lets a large board be filtered in-page instead of downloaded. Greenhouse, Ashby and Lever all answer cross-origin from any of the three, so one parked tab reads all three. It cleared six long-running blockers in three tool calls. ⚠️ Workable and `philips.wd3` CXS still refuse cross-origin. **Two sources that have failed for four and five consecutive runs, 80,000 Hours and SimplifyJobs, have never been tried this way and should be.**

🚨 **A CLOSURE CLAIMED FROM A BOARD ENUMERATION MUST NAME THE SLUG IT ENUMERATED (standing rule, after a real false closure).** A lane reported Tower Research as having no student internship "on a full first-party board enumeration"; `towerresearchcapital` in fact returns 86 jobs with 11 intern requisitions. The claim could not be checked because the slug was never stated. **State the slug and the job count with every closure.**

**Cost note:** one JSON pull covers a company's whole board, so this is cheaper than the per-posting fetches it replaces. Pull the board for every ATS company a run touches, not only the ones already flagged unread.

---

## Tier 1: Direct ATS search (do this every run)

Most companies post on a hosted applicant-tracking system (ATS) long before the role shows up on LinkedIn or a GitHub tracker. You can search across *all* companies on a given ATS with a search engine's `site:` operator. This is the single best way to find roles early, and it is the part most runs skip. Run each of these and read the first 2-3 pages of results.

**Greenhouse** (used by most mid-to-late startups and many funds):
- `site:job-boards.greenhouse.io "Summer 2027" intern`
- `site:boards.greenhouse.io "2027" (intern OR internship) (engineer OR "machine learning" OR data OR research)`
- Then read each hit's whole board with Tier 0: `https://boards-api.greenhouse.io/v1/boards/<org>/jobs?content=true`

**Lever:**
- `site:jobs.lever.co "2027" intern`
- `site:jobs.lever.co (internship OR intern) ("machine learning" OR "AI" OR research)`
- Then read each hit's whole board with Tier 0: `https://api.lever.co/v0/postings/<org>?mode=json`

**Ashby** (common at newer AI startups, Cursor, many YC cos):
- `site:jobs.ashbyhq.com intern 2027`
- `site:jobs.ashbyhq.com (internship OR "early career") (AI OR ML OR research OR engineer)`
- **The posting pages are JavaScript shells and will not read. Always go to Tier 0:** `https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true`

**Workday** (big tech / enterprise; URLs vary, but the pattern works):
- `site:myworkdayjobs.com "Summer 2027" intern software`
- `"2027 summer intern" (software OR "machine learning") site:myworkdayjobs.com`

⭐ **Workday renders the full posting text into the `meta-description` tag**, which returns verbatim class-year gates at zero search cost. Known suppressors: Capital One, Salesforce, PwC, Fiserv.

🚨 **THE UNPOSTED-STUB TEST HAS TWO FAILURE MODES AND BOTH PRODUCE FALSE CLOSURES. Read this before recording any Workday req as closed.** A req that returns a bare stub carrying only `meta-image` / `og:url` / `og:type` *looks* closed. Before believing it:

1. **Insert the `en-US` path segment** (`/en-US/<Tenant>/job/...`). Capital One's Data Analyst req stubbed without it and returned the full posting with it. (Added 2026-08-25.)
2. 🆕 **Try the location-less canonical slug.** Humana's Summer 2027 req stubbed at `.../en-US/Humana_External_Career_Site/job/**Remote-Nationwide**/…_R-424692` — `en-US` was already present — and returned the complete posting at `…_R-424692-1` with no location segment. **A guessed or wrong location segment stubs out a fully live req.** So a stub means *"wrong URL OR unposted"*, never *"closed"* on its own. (Added 2026-08-26, after this nearly killed the best F500 req of that day.)

⚠️ **Two further false-negative shapes that are NOT closures:** the **company-blurb substitution**, where a tenant renders a generic corporate blurb into `meta-description` instead of the posting body (GE Vernova), and the **empty-body client-side render** (BNY, Truist, Uber's Oracle CX, CCC). Neither is evidence of closure. Separately, **P&G's Phenom `search-results` page renders zero server-side results** and returns the raw unsubstituted template literal `"${pageStateData.searchKeyword}"`, so P&G's inventory cannot be enumerated by fetch at all; individual req URLs do render.

**Rippling / SmartRecruiters / Workable** (rotate one per run):
- `site:jobs.rippling.com intern 2027`
- `site:jobs.smartrecruiters.com 2027 intern (AI OR data OR engineer)`

Tip: swap the season each run (`"Summer 2027"`, `"Winter 2027"`, `"Fall 2026"` for academic-year-aware ones), and swap the role keyword (`"machine learning"`, `"applied AI"`, `quant`, `data scientist`, `"forward deployed"`, `product`). One ATS x one season x one role keyword is one search; budget roughly 6-10 of these per run.

---

## Tier 2: Live aggregators & trackers (do this every run)

These are crawled or community-maintained, so they refresh on their own. Hit the GitHub trackers and HN thread every run; rotate the rest.

**GitHub internship trackers** (read the raw README, which is the actual list):
- SimplifyJobs Summer 2027: `https://github.com/SimplifyJobs/Summer2027-Internships` (raw: `https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/README.md`). 🚨 **The branch is `dev`. There is NO `main` branch on this repo** — every file resolves to `blob/dev/...`, and an earlier instruction here to "try `main` first" was wrong and cost three runs. Confirmed readable on the `dev` path three consecutive runs (8/24, 8/25, 8/26). ⚠️ The file is ~1 MB and `web_fetch` truncates it at roughly 70k characters / 858 lines; because the table is sorted newest-first the truncated head **is** the 0–3 day delta, so nothing time-relevant is lost, but anything older than ~4 days will not be seen. ⚠️ The table is HTML `<tr>/<td>`, not markdown pipes, so grep on `<td>` rather than `^\|`.
- **speedyapply 2027 AI/ML (RUN THIS FIRST, highest yield):** `https://github.com/speedyapply/2027-AI-College-Jobs` (raw: `https://raw.githubusercontent.com/speedyapply/2027-AI-College-Jobs/main/README.md`)
- speedyapply 2027 SWE: `https://github.com/speedyapply/2027-SWE-College-Jobs` (raw: `https://raw.githubusercontent.com/speedyapply/2027-SWE-College-Jobs/main/README.md`)
- **Internship Radar 2027 (not a repo, server-rendered, per-row eligibility tags):** `https://internship-radar-2027.yuxhuang.com/`. ⚠️ **The site has moved to `https://earlycareerradar.com/summer-internships`; the old URL 302s there cleanly.** Only ~40 of ~345 rows are server-rendered; the rest are client-side past the fold. Harvest the per-row eligibility tags from the readable head, since that field ("3rd year", "Undergraduate — year not stated", "Graduate student", "No sponsorship") is what decides whether a req is worth an application and no other board carries it.
- Student-run quant tracker, e.g. `https://github.com/<org>/<year>QuantInternships` (raw: `https://raw.githubusercontent.com/<org>/<year>QuantInternships/main/README.md`); find the current one by searching GitHub for `<year>QuantInternships`
- Dropped 2026-08-13: `vanshb03/Summer2027-Internships`, dead for this cycle (last push 2026-05-23; `OFFSEASON_README.md` is titled "Spring & Fall 2026" and has no row newer than May 22). Do not re-add without checking it has resumed.
- Note: early in a cycle these repos may still be mostly the prior year, so check the dates rather than assuming freshness.
- **Check the cycle year in the URL, not just that the fetch succeeded.** Both `speedyapply/2026-SWE-College-Jobs` and the 2027 repo are live, so a stale reference returns last year's roles with no error. Same trap on any repo whose name carries a year.

**Hacker News "Who is Hiring?"** (first weekday of each month; indexed by no aggregator):
- `https://hnhiring.com/` (current month), filter for "intern" and remote
- Algolia search within the monthly thread: `https://hn.algolia.com/?query=intern&type=comment`

**Other aggregators (rotate ~2-3 per run):**
- 80,000 Hours job board: `https://jobs.80000hours.org/`, high-signal AI/policy/research roles + fellowships
- aisafety.training: `https://www.aisafety.training/`, the single best AI-safety/alignment deadline board
- 🚨 **John Gannon's VC job board, URL CORRECTED 2026-08-27.** `https://www.johngannonblog.com/vc-jobs/` **301-redirects to `/vc-careers/vc-jobs-archive/`, a hand-maintained archive whose newest entry is dated 6/30/15** and which carries zero current listings. The live board is `https://www.johngannonblog.com/venture-capital-internship/`, and it is a **JavaScript widget** that returns *"Your browser does not support JavaScript, or it is disabled. JavaScript must be enabled in order to view listings."* to a fetcher. **Needs a real browser; do not record it as swept from a fetch.**
- Levels.fyi internship leaderboard: `https://www.levels.fyi/internships/`
- ColorStack / Rewriting the Code opportunity boards
- The Forage (virtual experience programs): `https://www.theforage.com/`
- ProFellow: `https://www.profellow.com/`, fellowship deadline database
- 🚨 **Devpost, USE THE JSON API, NOT THE PAGE (standing rule).** `https://devpost.com/hackathons` renders its tiles client-side and returns nothing to a fetcher, which is why this source sat unread for at least four runs. ✅ `https://devpost.com/api/hackathons?status[]=open&order_by=recently_added` returns the full listing with first-party start and end dates, prize pools and themes, 9 per page. One call replaced four runs of failure.
- 🚨 **MLH, THE DOMAIN CHANGED (standing rule).** `mlh.io/seasons/2027/events` 302s to `https://www.mlh.com/seasons/2027/events`, which server-renders the WHOLE season schedule. ⭐ **One fetch yields ~31 dated US in-person events, so make it the FIRST move of the hackathon lane** and spend the by-name budget on the self-hosted marquee events MLH does not carry.
- ETHGlobal: `https://ethglobal.com/events`, travel-covered crypto hackathons

---

## Tier 3: Startup & VC-portfolio job boards (rotate, ~3-4 per run)

This is the richest vein for the early-stage AI roles that match the candidate's profile, and almost nothing here is indexed by the generic trackers. Most VC firms run a shared "talent network" job board across their whole portfolio (frequently powered by Getro or Consider), so one board surfaces dozens of vetted startups at once.

**General startup boards:**
- Wellfound (formerly AngelList Talent): `https://wellfound.com/jobs`, filter Internship + remote/role
- 🚨 **Y Combinator, USE THE MIRROR, NOT WORK AT A STARTUP (confirmed 2026-08-27).** `workatastartup.com` returns **HTTP 200 with a zero-byte body** on `/companies?jobType=intern`, `/internships`, `/events/<id>/lookbook` and every individual `/jobs/<id>`, and **the bare-`?` cache-bypass does NOT fix it.** ✅ **Every WaaS posting is mirrored at `https://www.ycombinator.com/companies/<slug>/jobs`, which server-renders in full including the monthly pay band and the `School year:` gate.** That mirror is strictly better data than the WaaS page and produced CTGT, three Dedalus reqs and Abundant in a past run. ⚠️ Do not trust `ycombinator.com/jobs/role/software-engineer/intern`: it **silently ignores the `/intern` path segment** and returns full-time roles only.
- Built In: `https://builtin.com/jobs/internships`

**VC-portfolio talent boards** (each is a single board spanning that firm's portfolio, rotate through them):
- a16z: `https://portfoliojobs.a16z.com/jobs`
- Sequoia: `https://jobs.sequoiacap.com/jobs`
- General Catalyst: `https://jobs.generalcatalyst.com/`
- Greylock: `https://jobs.greylock.com/`
- Bessemer (BVP): `https://jobs.bvp.com/`
- Lightspeed: `https://jobs.lsvp.com/`
- Index Ventures: `https://jobs.indexventures.com/jobs`
- Founders Fund / Khosla / Thrive / Benchmark, search `"<firm> portfolio jobs"` to find the current board URL.

Query template for these: open the board, filter to Internship + Engineering/Data/Research, and read role + dates. When a board has no internship filter, search the page for `2027` and `intern`.

---

## Tier 3B: Fortune 500 mid-tier direct sweep (rotate one sector/run; all five in the Aug–Nov wave)

The F500 mid-tier (retail/CPG, healthcare/pharma, industrials, energy, insurers, non-bulge finance) posts large Summer-2027 tech/data internship programs mostly Aug–Nov, and no aggregator indexes them well. Hit them by name on their own ATS. See SKILL.md Category 2A for the full sector rosters. Query shapes:
- `<company> "Summer 2027" (data scientist OR "machine learning" OR software) intern`
- `site:myworkdayjobs.com "Summer 2027" intern (data OR "machine learning" OR analytics) <company>`
- `<company> 2027 technology internship apply`
Standing filters: present the graduation year these programs sort on, per the Default Selection Rule in `CLAUDE.md`; **defense primes (Boeing, Lockheed, RTX, Northrop, GD, L3Harris) are citizenship/clearance-gated**, so check the candidate profile's work-authorization line and verify any clearance, export-control, or facility-access requirement separately.

---

## Tier 4: Category-specific aggregators (rotate, tie to the daily rotation slice)

Match these to whichever named-program category the run is rotating through that day (see the rotation discipline in SKILL.md):
- **AI fellowships / safety:** aisafety.training, 80,000 Hours, GovAI openings page, EA Forum opportunities.
- **Founder / builder:** firm pages directly (Z Fellows, Emergent Ventures, EF, Neo, Contrary, South Park Commons), plus Sifted for EU.
- **VC scouts / fellows:** Dorm Room Fund, Contrary, firm "fellows" pages.
- **Quant / trading:** firm career pages (Jane Street, Citadel, Five Rings, HRT, Optiver, SIG, IMC, Aquatic) plus their direct ATS.
- **Research / REU:** nsf.gov REU search, DOE SULI, NASA, lab pages.
- **Conferences / affinity:** GHC/AnitaB, Tapia, SHPE, NSBE, ColorStack, RTC, SEO, MLT.
- **APM / product:** APMList.com.
- **Aerospace:** Brooke Owens, Matthew Isakowitz, Patti Grace Smith, Zed Factor pages.

---

## Query template bank

Reusable shapes. Replace the bracketed parts each run.

**Season-specific internships (use quoted phrase, engines ignore unquoted years):**
- `"Summer 2027" [role] internship application open`
- `"Winter 2027" [AI OR ML OR data OR quant] intern`

**Discovery (find programs you don't know yet):**
- `new [AI fellowship OR founder program OR VC scout] 2026 application open undergraduate`
- `[city] tech week 2026 student events schedule`
- `[firm] sophomore [insight OR diversity] program 2027 application`

**LinkedIn quoted-phrase** (needs the user's logged-in browser via Claude in Chrome; read-only, scroll the lazy-loaded results pane and read cards from screenshots):
- `https://www.linkedin.com/jobs/search/?keywords=%22Summer%202027%22&f_E=1&f_F=eng%2Cit&sortBy=DD`
- Repeat with `keywords=%22Winter%202027%22`. `f_E=1` = internship level; `f_F=eng,it` = Engineering + IT.

**Handshake** (school portal): handled by the separate `handshake-scan` skill, do not hand-search it. See its scan-method notes in `opportunities/opportunities-state.md`.

---

## How to read results (what counts as a real hit)

- A "hit" is a specific, actionable opportunity: a named program/role with an apply path and a deadline (or an honest "rolling"/"unconfirmed, verify"). A blog post *about* internships is not a hit.
- **Read location and workplace type before the class-year gate.** Both are single fields in the Tier 0 JSON. An on-site role outside the continental US is dead on a deal-breaker regardless of the gate, so checking it first is the cheapest disqualification available.
- Verify every deadline on the official source before listing it (search results lag reality, so closed programs often still show as open). See OPERATING DISCIPLINE rule 1 in SKILL.md.
- Dedupe against `opportunities/opportunities-state.md`, `opportunities/closed-this-cycle.md` and `job_search_tracker.csv` before listing, per the dedup rule in the state file.
- When a search returns only already-known items, that is still a useful result: it means coverage of that source is current. Log it in the run's coverage log (see SKILL.md) rather than silently dropping it.


---

## Pipeline traps that delete live rows (standing rule)

These are not search problems. They are ways a correctly-found, genuinely open opportunity disappears between the state file and `OPEN-LIST.md`.

- 🚨 **`verify_open_list.py`'s CLOSED detector matches the bare phrase `not eligible`.** So quoting an employer's sponsorship sentence verbatim — `This role is not eligible for candidates requiring VISA sponsorship`, which is *good* news for a candidate who needs no sponsorship — classifies the row as closed and drops it from the rendered list. **Paraphrase sponsorship and eligibility sentences in the What/why column instead of quoting them.**
- 🚨 **The same detector matches `not yet open`.** Never write that phrase to mean "the gate has not been read". Write **`gate not read by this run`**. Six rows were silently classified closed this way in a past run.
- ⚠️ **The detector also matches `already ended`, `deadline passed`, `next cycle`, `now closed` and `ineligible`.** Any of these appearing inside a quotation has the same effect as the row asserting them about itself.
- ⭐ **The durable fix is code, not care: make the CLOSED detector skip text inside backticks.** A quoted employer gate is evidence about the employer's rules, never about whether the requisition is live.
- 🚨 **When a gate read corrects a date, change the Deadline column, not only the Verified? note.** `OPEN-LIST.md` and the Deadline radar are generated from the Deadline column, so a row whose note disagrees with its own column will publish the wrong date indefinitely. This happened to Contrary for four days.
- 🚨 **A removal filter must match on the requisition or programme identifier, never on a name that can appear in another row's prose.** On 2026-09-12 a filter keyed on the string `Z Fellows` swept the Thiel Fellowship row, because Thiel's What/why still carries the shared context of a combined row split in a past run and names Z Fellows inside it. Z Fellows resolved that run; Thiel did not, and the two are unrelated. This was the second time in two runs that a filter matched text a row merely mentions rather than text that identifies it.

---

## Method findings standing rule

- 🚨 **`jobs.lever.co` PUBLIC HTML DOES NOT ANSWER CROSS-ORIGIN FROM `example.com`, THOUGH THE LEVER API DOES.** This narrows the 2026-09-11 standing escape, which says Greenhouse, Ashby and Lever all answer from one parked tab. **That is true of the three JSON APIs, not of Lever's rendered board.** Every `fetch()` against `jobs.lever.co` from a tab parked on example.com threw `TypeError: Failed to fetch`. The workaround that does work is navigating the tab directly to the posting. Consequence: a Lever closure confirmed only by org-array enumeration has no HTML positive control, and should say so.
- ⚠️ **Ashby's `api.ashbyhq.com/posting-api/job-board/<org>` returns an EMPTY BODY to `web_fetch`** and must go through the browser pane. A 404 from that endpoint means the slug is wrong or the org is not on Ashby; it never means the board is empty.
- 🚨 **A LONG RUN OUTLIVES THE EMAIL SEND WINDOW THAT USUALLY BOUNDS IT.** Six run logs recorded "LinkedIn sends at 16:23Z and this run fired earlier, so LinkedIn is a structural zero." That held only because those runs were short. On 2026-09-14 a nine-lane fan-out kept the run alive past 16:23Z and that day's alert arrived mid-run. **Re-query the email sources at the END of a long run as well as the start, or at least re-query once the run has crossed 16:23Z.**
- ⚠️ **a16z's board header string `798 companies. 16,822 jobs.` makes a naive `(\d+) jobs` regex return `822`.** Read the count that sits under `Clear filters` instead. Its list is virtualised, so only ~15 rows exist in the DOM at a time and scrolling replaces them rather than appending. Counts in a past run: a16z 307 internships, Sequoia 272, Lightspeed 408, Bessemer 81.
- ⚠️ **General Catalyst's working filter parameter is `?q=`, re-confirmed 2026-09-14**; `?searchQuery=` is the one that silently drops. Getro paginates rather than virtualising, so a single read gets page one only. There is no visible filter chip and the search input's `.value` reads empty, so the row count against the unfiltered ~20,000 baseline is the only available proof the filter took.
- ⚠️ **Built In is `unsearched` for tech internships, not empty.** `/jobs/internships` renders but carries no function filter; both `/jobs/dev-engineering/internships` and `/jobs/internships?search=engineer` silently drop the internship filter and return senior full-time roles, with the `All Filters` badge falling from `1` to blank. Use the on-page function control instead of a URL path or query.
- ⚠️ **Y Combinator is `unsearched` for internships and two further paths fail silently.** `ycombinator.com/jobs?jobType=intern` and `ycombinator.com/companies?jobType=intern` both return the unfiltered default with no filter chip. The `ycombinator.com/companies/<slug>/jobs` mirror does server-render, but it needs a slug list and no working YC-side filter exists to produce one.
- ⚠️ **SmartRecruiters company IDs are frequently wrong and a wrong ID returns `totalFound: 0`, which reads exactly like an empty board.** 28 of 36 IDs returned zero in a past run. None of those is a closure finding.
- ⚠️ **Phenom empty responses are a hydration failure, never a no-results page**, re-confirmed on Cone Health, whose `/api/jobs` and `/api/apply/v2/jobs` both returned empty.
- ⚠️ **The quant firms and the sophomore programmes gate on mutually exclusive graduation windows.** Optiver, IMC, SIG, AQR, Belvedere, Point72 and Balyasny converge on roughly December 2027 through July 2028, which selects the earlier graduation year. Sophomore and insight programmes such as Goldman's Emerging Leaders Series and Blackstone Future Leaders select the later one. Surface that as one decision about which year to present, not as many separate ones.
- ⚠️ **Several named trading competitions have no standalone public application page at all** — Jane Street ETC and Estimathon, SIG Trading Game, HRT Algo Engineering Challenge, D.E. Shaw Quant Challenge, Optiver Trading Challenge, Bloomberg Coding Challenge. Entry is through campus recruiting, prior events, or an internship requisition. **Stop tasking these as lookups; that is a structural answer, not a coverage gap.**
- ⚠️ **Blueprint (MIT) is high-school-only**, and **Goldman Sachs's Engineering Hackathon and Walmart's Sparkathon are both India-only**, gated to Indian engineering colleges. All three should come off the named-hackathon rotation for a US undergraduate.

## Method findings standing rule

- 🚨 **CORS behaviour is a per-host property, not a general rule.** Greenhouse, Ashby and Lever all answer cross-origin `fetch()` from a tab parked on `https://example.com`. **Workable's `apply.workable.com/api/v2` REFUSES it** and must go through `web_fetch`; **Devpost's `/api/hackathons` also refuses it** and must go through `web_fetch`. Workday `/wday/cxs/` endpoints refuse cross-origin and need the tab parked on the tenant's own origin.
- ⭐ **The example.com to raw.githubusercontent.com route defeats the SimplifyJobs truncation completely.** All 1,577 `<tr>` rows parsed in-page on the first try, against a `web_fetch` that truncates the same file immediately. The precondition recorded in a past run is confirmed: park on `example.com`, never on `raw.githubusercontent.com`.
- 🚨 **A PER-LANE NUMERIC WEBSEARCH BUDGET IS THE FIX FOR THE SHARED 200-CALL QUOTA.** The prose warning was already in every brief in a past run and one lane still exhausted the quota in its first sector. Adding an explicit "budget at most N calls; lead with direct board fetches" to each brief kept all eight lanes well inside it in a past run. **Write the number into every lane brief.**
- ⚠️ **Wrap every batched browser fetch in try/catch.** `browser_batch` aborts on the first thrown error, so one unhandled bad slug kills the rest of the batch. Returning the error as a string keeps the remaining actions running and roughly tripled one lane's throughput.
- ⚠️ **ETHGlobal now overflows `web_fetch`'s token ceiling** and needs the in-page `fetch()` route with client-side filtering. Low priority: two remaining events, both outside the continental US.
- ⚠️ **Bank of America's public campus RSS is EMEA-only**, correcting the 2026-08-28 entry above that promoted it as the best early-warning source for the whole BofA campus family. All 55 entries on `vacancy/1/feed` are European or Dubai. US campus technology roles need another route.
- **Getro boards filter on `?q=`. Consider boards filter on `?internshipOnly=true`.** General Catalyst is Getro and silently drops `?searchQuery=`, returning all 20,024 rows. a16z, Sequoia, Bessemer and Lightspeed are Consider and echo the internship chip on the page.
- 🚨 **Wellfound's internship filter drops silently to a logged-out landing page** with no filter chip and no result list. Zero rows there is `unsearched`, never `empty`.
- ⭐ **Read the `__NEXT_DATA__` payload rather than the rendered page on any Next.js careers site.** Contrary's programme data lives there and carries the authoritative `open` boolean; three reads of its rendered page produced three different deadlines, none of which appears in the payload.
