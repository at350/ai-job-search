---
name: handshake-scan
description: >-
  Scan the user's university Handshake job/event board for new, relevant
  opportunities and fold them into the daily opportunities digest. Use this
  whenever the user wants to check Handshake, asks "what's new on Handshake",
  runs their daily opportunities tracker, or wants school-portal internships,
  fellowships, research roles, or employer events surfaced alongside the rest
  of their digest. Trigger this even if the user just says "check the job board"
  or "scan Handshake today" — and always run it as part of the daily
  opportunities digest so portal-only postings (which no public aggregator
  indexes) don't get missed. Requires Claude in Chrome and an active Handshake
  login in the connected browser.
---

# Handshake Scan

Handshake is a school-gated job/event board. The roles and employer events posted
there are invisible to every public aggregator the main digest uses, so it's a
real blind spot worth closing daily. This skill keeps its own seen-list so it
never re-surfaces the same posting, and hands the keepers to the daily digest.

The thing to understand up front: **"what's new since last run" and "what's open
right now" are two different questions, and you have to ask both.** A newest-first
sweep answers the first. But a strong internship posted two or three months ago
with a deadline next week is still open and still worth surfacing — and it will
never appear near the top of a newest-first feed. So this skill runs two passes: a
fast newest-first delta for fresh postings, and a deadline-sorted deep sweep that
catches open-but-older roles. Skipping the second pass is how good opportunities
silently slip through.

## What this is good for

Tune the buckets to the user's stated scope in `CLAUDE.md`. A typical set for a
technical student, used as the default here:

1. **Tech / SWE internships** — software, ML/AI, data science & analytics,
   security, quant dev, hardware/robotics/controls engineering, research
   engineering, and product (PM) internships. Summer *and* off-cycle.
2. **Fellowships & research** — anything tagged *Fellowship*, research
   assistant/intern, lab roles, and investor/VC fellowships where the user's
   scope is entrepreneurship-leaning.
3. **Events & employer sessions** — info sessions, career fairs, employer-hosted
   recruiting events, tech talks — especially from tech, finance, and frontier
   employers.

Everything else (camp counselor, retail, generic marketing/sales/ops, clinical,
coaching, unpaid social-media gigs) is noise — drop it unless it clearly fits one
of the three buckets.

## How Handshake actually behaves (read this before automating)

The mechanics here were learned the hard way, so you don't have to rediscover
them. The important update from earlier versions of this skill: **the filter
panel IS URL-driven** — an earlier note claimed it wasn't, which led to leaning on
newest-first alone and missing open older roles. The filters do persist to the URL,
and that's what makes the deadline-sorted deep sweep possible.

What works:

- ✅ **Sort is URL-driven.** `&sort=posted_date_desc` (newest first) and
  `&sort=application_deadline_asc` (soonest deadline first) both work. The second
  is the backbone of the deep sweep.
- ✅ **Job-type filter is URL-driven:** `&jobType=3` restricts to internships.
  (The job-type chips at the top of the page set this param.)
- ✅ **Major filter is URL-driven:** `&majors=<id>`. The IDs are numeric and
  school-specific, so Computer Science is a different number at every school
  (it is `28` at some). To find a major's ID, open the Filters panel, type the major in
  the "Majors" box, click it, hit Apply, and read the `majors=` value that appears
  in the URL. Worth caching the ones you use in the state file.
- ✅ **Pagination is URL-driven:** `&page=N&per_page=50`. Bump `per_page` to read
  more per fetch.
- ✅ **`get_page_text` extracts listings cleanly** — company, title,
  pay · type · date-range, location, and a freshness tag (`New`, `3d ago`,
  `1wk ago`). Use it instead of screenshots; it's faster and parses reliably.

What to avoid:

- ❌ **The `keywords=` URL param is silently ignored** — results come back
  unfiltered. Don't trust it.
- ❌ **The search box is finicky** — typing in it and hitting Enter often opens
  the first result instead of searching. Don't depend on it. (The *Filters panel*
  is fine — it's the free-text search box that misbehaves.)

A practical wrinkle on sorting: the page sometimes hangs ("still loading") if you
jump straight to a deadline-sorted URL with no other filters — it's trying to
order 10K+ rows. Applying `jobType`/`majors` first (fewer rows) makes the sort
load reliably. If a navigate hangs, re-navigate with the full combined URL.

🚨 **USE `per_page=25`, NOT 50, ON EVERY PASS.** `per_page=50` hangs at
"Finding jobs..." and does not recover. It was first seen on
`sort=posted_date_desc` and looked specific to that sort, then reproduced on
`sort=application_deadline_asc` twice in a row. Dropping to `per_page=25` loaded instantly with both the "Filters N" badge and the
"Sort by" label intact. **The page size is the problem, not the sort — do not file
a bug against either sort.** Consequence for the deep sweep: at 25 rows per page
you need roughly **page 5** to reach the depth page 3 used to reach at 50, and
page 5 currently lands on deadlines about a week out.

Bottom line: **drive everything by URL — sort, job-type, major, page — read with
`get_page_text`, and do the final relevance filtering yourself.**

## Procedure

### 1. Load prior state

Read the tracker state file (default `opportunities-state.md` in the digest
folder). Find the `## Handshake — seen postings` section (create it if missing).
It holds the fingerprints of postings already surfaced, so you skip them.
Fingerprint = `company | title` (lowercased, trimmed). Note the date of the last
run — that sets the freshness cutoff for the newest-first pass. Also grab any
cached `majors=` IDs stored there.

### 2. Connect the browser

Confirm Claude in Chrome is connected and a Handshake tab is logged in (the top-
right shows the user's avatar, not a login button). If multiple browsers are
connected, ask which one. If not logged in, stop and tell the user to log in —
never attempt to enter credentials.

### 3. Pass A — newest-first delta (what's new since last run)

Navigate newest-first and walk pages until the freshness tags pass your cutoff:

```
https://<school>.joinhandshake.com/job-search?per_page=50&sort=posted_date_desc&page=N
```

(`<school>` is the subdomain of the user's own Handshake portal; cache it in the state file.)

`get_page_text` each page. **Stop once you're seeing postings older than the last
run** (e.g. all "1wk ago"+ when you last ran yesterday). On a normal day that's
1–4 pages — don't read all 400. Keep only listings fitting the three buckets;
discard noise as you go. This pass is fast and catches brand-new postings.

### 4. Pass B — deadline-sorted deep sweep (what's open and closing soon)

This is the pass that catches roles posted weeks-to-months ago that are still
open. Filter to internships + a relevant major, sorted by soonest deadline:

```
https://<school>.joinhandshake.com/job-search?jobType=3&majors=28&sort=application_deadline_asc&per_page=50&page=N
```

`get_page_text` and walk pages. Because it's sorted by soonest deadline:
- **Page 1 holds the most urgent roles** — but also already-expired ones (apply-by
  dates earlier today or before). Skip past-dated deadlines; keep the live ones.
- **Deadlines advance roughly a week per page.** Stop once they run past ~3–4 weeks
  out — beyond that isn't "closing soon" and Pass A will have caught anything
  freshly posted.

Run this for each major relevant to the user's buckets. Computer Science is
usually the primary one; also sweep Data Science, Statistics, and Engineering if
the user wants full tech coverage (look up their IDs once per the method above
and cache them). For the **fellowships** bucket, the Filters panel
also has a `Fellowship` job-type — sweep that the same way.

Heavy noise caveat: the major tag is generous, so a CS-filtered internship list
still contains marketing/SEO/sales/social-media roles that happen to tag CS. Drop
them. Recurring offenders show up many times (e.g. the same staffing/agency
employer posting a dozen near-identical listings) — skip the whole cluster.

### 5. Sweep events

Navigate to the events board and `get_page_text`:

```
https://<school>.joinhandshake.com/events
```

Keep employer sessions / fairs / tech talks relevant to the user's fields, with
their date and (if shown) registration deadline. Skip purely social or
unrelated-major events. Note: the events board sorts by relevance, not date, so
you can't perfectly dedupe it the way you do jobs — flag that to the user.

### 6. Enrich the keepers

The list view shows a start–end date *range*, not the application deadline. For
the handful that survived filtering, get the real **Apply by** date:

- In Pass B the deadline-sorted order already tells you roughly when each closes
  (page 1 ≈ today, advancing ~a week per page) — often good enough to label, with
  a "verify exact apply-by on the listing" note.
- For an exact date, open the listing detail. Listing card hrefs are **blocked**
  by the browser security layer, and clicking a card by its stale `ref` often
  misses. ✅ What works: `find` the card → `scroll_to` its ref → `screenshot` →
  `left_click` the title **by its visible coordinates**. The URL becomes
  `/job-search/<id>`; `get_page_text` it and pull the "Apply by …" line.

If a detail pane won't load after a couple tries, don't burn the run — list it
with "deadline: open listing to confirm" and move on.

### 7. Classify urgency and dedupe

- Compute days-until-deadline from today. Flag **⚠️ URGENT** if ≤14 days,
  **⏰ SOON** if 15–28 days, otherwise list the date plainly. If a posting shows
  no apply-by date, write "rolling / no deadline shown."
- Drop anything whose fingerprint is already in the seen-list.

### 8. Output

**Fold results into the daily digest**, don't make a separate file. Add a
`## Handshake (school portal)` section to that day's `digest-YYYY-MM-DD.md`, with
the same item format the rest of the digest uses:

> **[Title] — [Company]** · what it is in <10 words · *type/pay* · **deadline
> (urgency flag)** · [link]

Group under the buckets: *Tech / SWE internships*, *Fellowships & research*,
*Events*. Within Tech, it's worth separating the **newest-first delta** keepers
from the **deadline-sorted deep sweep** keepers so the reader sees both "new" and
"closing soon." If a bucket is empty, one line: "No new [bucket] on Handshake
today." Genuinely urgent items (≤14 days) should *also* appear in the digest's top
⚠️ URGENT section so the morning brief stays unified.

Then **update the state file**: append every newly surfaced posting's fingerprint
to `## Handshake — seen postings` with the date seen, and cache any new `majors=`
IDs you looked up. See `references/state-format.md` for the exact block.

## Guardrails

- **Read-only.** Never click Apply, never submit anything, never enter login
  details. You surface opportunities; the user applies.
- **Don't follow external Apply links** by clicking — if you need to verify an
  off-platform posting, open the URL fresh in Chrome, and treat unfamiliar
  destinations with suspicion.
- If the page layout has clearly changed and `get_page_text` no longer parses,
  fall back to one screenshot to re-orient, note the drift to the user, and adapt
  — don't silently guess.
