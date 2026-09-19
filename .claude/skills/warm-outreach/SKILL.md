# Warm Outreach

**name:** warm-outreach
**description:** For a company where the user already has an internship, an offer, an open application, or a target role, this skill figures out who they should reach out to (school or former-employer alumni first, then recruiters, then the hiring team), drafts a personalized LinkedIn connection note for each, shows them the list for approval, and then, only after they approve, sends the connection requests with notes via Chrome. Use it whenever the user wants to network into a company, get a referral, "reach out to people at [company]", "connect with someone at [company]", "find a warm intro", "who should I message at [company]?", or follow up on a role they already applied to. Trigger it even when they name only a company and a goal (e.g. "I applied to <company> for a summer internship, help me get a referral"). For finding new roles use the daily-opportunities-tracker skill instead.
**allowed-tools:** Read, Write, Edit, Glob, Grep, WebSearch, AskUserQuestion, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__list_connected_browsers, mcp__claude-in-chrome__select_browser

---

## What this skill is for

Referrals and warm intros come from people, not portals. When the user already has a foothold at a company, applied, interviewing, offer in hand, or just decided it's a target, this skill finds the right people to talk to and gets the outreach out the door. It does the research and drafting, then sends after a single approval checkpoint.

Two ground rules:
- **Never use Apollo or any sales/CRM connector.** This is the user's personal networking, separate from their work tools. Find people only through LinkedIn (via Claude in Chrome) or public web search.
- **Sending requires the user's explicit go.** You draft and stage everything, show it to them, and send connection requests only after they say yes in that run. This is not bureaucratic caution: connection requests can't be unsent, mass-blasting risks their account, and a clumsy note to a recruiter or alum reflects on them personally. The approval step is the whole reason this is safe to automate.

## Inputs

The user should name the **company** (and ideally the **role/term**, e.g. "<company>, Summer 2027 SWE intern"). If they don't:
- Check `job_search_tracker.csv` and the most recent `opportunities/digest-*.md` for companies they have applied to or shortlisted, and ask which one they mean.
- If still unclear, ask them directly, don't guess.

## Working folder and context

The repo root is the `ai-job-search` folder. Read first:
- `.claude/skills/job-application-assistant/01-candidate-profile.md` (Part 1): candidate profile, so messages are specific and accurate. The outreach rules themselves are in `01-outreach-rules.md` beside this file; read it first.
- `.claude/skills/job-application-assistant/03-writing-style.md`: the voice for the notes (no em-dashes, no clichés, warm and specific).
- Your university or career center's networking guide, if you have one, saved under `documents/references/`. Its networking section is the outreach playbook for this skill (see Step 3).
- `documents/playbook/index.md`: saved advice. Read the `outreach-cold`, `outreach-warm`, and `referrals` claims that fit this target before drafting.
- `documents/private/stated-beliefs.md`: the canonical opinions file and the main source of **specific openers**. Match an entry's topic against the target's domain and lead with the idea, not the fact that the user watched a video. **Every entry is in play, including Raw.** Verbatim, Approved, and Paraphrase entries can be drafted from directly. A **Raw** entry that fits the target is surfaced to the user with a request to develop it on the spot, not skipped; once they expand it, draft from what they said. Never write their opinion for them. When an entry cites a media-library file, quote third parties only from that file's "Exact quotes" section, attributed to the original speaker; everything else is paraphrase.
- `documents/library/index.md`: the media library behind those citations. **Never repeat a number an item's fact-check table flagged** as unverified, imprecise, or wrong; where the beliefs entry names a banned number, that ban travels with the belief. A wrong statistic in a founder's inbox is the most expensive kind, and several saved items are vendor marketing whose headline numbers did not hold up. A beliefs or library hook is one option, not a requirement: a firsthand problem the user hit in the target's own product still beats a secondhand idea, and for short-list startup targets the built proposal (Step 3) outranks both.
- `outreach_tracker.csv`: people already contacted (columns: `date,company,role,contact_name,contact_title,school_alum,linkedin_url,status,notes`). Never double-contact someone already in here for the same company.

## Step 1, Confirm the target and connect to Chrome

Confirm the company/role. Then connect to the user's logged-in browser by following the **Browser Selection Protocol in `documents/portals/browser-selection.md`**. If that file records a default device for this user, select it directly instead of asking again. Verify LinkedIn is logged in before doing any real work. If the browser isn't connected or LinkedIn isn't logged in, stop and tell them, this skill needs their session.

## Step 2, Find who to reach out to

Find **2–4 people** at the company using LinkedIn (read public profiles only; do not connect or message yet). Priority order, warmest first:
1. **Alumni of the user's school** at the company, via LinkedIn's school alumni filter or the school-alumni panel on the company's job postings and people pages. A shared-school intro is usually the strongest angle.
2. **Recruiters / university recruiting / talent** for the relevant org or role.
3. **The hiring manager or a team member** on the function the user applied to.

For each person capture: name, title, whether they are a school alum, and their LinkedIn profile URL. Skip anyone already in `outreach_tracker.csv` for this company. Favor people who are 2nd-degree connections or share a group/background, they're likelier to accept.

### Step 2b, Triage every contact into a tier (required)

The user's binding constraint is calendar time, not message volume. They work multiple concurrent roles and cannot coffee-chat everyone. Assign each person a tier before drafting, and carry the tier into the approval table. See the Contact triage rules in `CLAUDE.md` for the canonical version.

- **Tier 1, live call.** The hiring manager, someone on the specific team, or the recruiter who owns the req. Also anyone at a company where the user already passed an assessment or interview. **Cap Tier 1 at 1-2 people per week across all companies**, so check recent `outreach_tracker.csv` rows before assigning another one. Only Tier 1 messages may propose a call.
- **Tier 2, asynchronous first.** Alumni at large companies applied to cold, anyone whose title does not touch the req, any speculative contact. Default to a short message with a specific question or a direct referral ask, answerable at their keyboard. The user may attach a booking link and name a concrete window when they have something worth a call, but the message must stand on its own without one, so a keyboard reply is always a complete answer. Do not open a scheduling thread, and never hold a slot on a Tier 2 contact's calendar; a held slot is a Tier 1 move. A Tier 2 call that gets booked comes out of the same 1 to 2 weekly Tier 1 slots.
- **Tier 3, skip.** Large centralized campus pipelines where nobody reachable touches the decision. Do not draft a message; list the person as skipped with the reason.

If a run produces more than 2 Tier 1 contacts, present them ranked and let the user pick which get the call ask; the rest drop to Tier 2.

## Step 3, Draft a connection note for each

Follow `03-writing-style.md` and, where you have one, the career center networking framework in `documents/references/`. A good outreach message covers: who you are (brief intro), how you found them, what you have in common, why you're reaching out and what you hope to learn, and one light specific ask. Treat it as connecting and learning, not asking for a job, and don't ask for a referral in a first message; it follows naturally once they know you. For each person write a **connection-request note under 300 characters** (LinkedIn's limit) that:
- Is specific to the person and the role/company (not a template). If a media-library item matches their domain, the idea from it is a strong opener; in 300 characters that means one clause of the idea plus why it connects to their work, with no citation apparatus.
- Names the tie if they are a school alum (use the school's own shorthand for its alumni) or shares a concrete reason for reaching out.
- **Matches the ask to the tier.** Tier 1 may ask for a 20-minute call. Tier 2 is asynchronous first: it asks one specific question or asks directly for a referral, may carry a booking link only if the message stands alone without it, and never holds a slot on the contact's calendar ("I applied to [role] and completed the assessment. Would you be open to referring me, or pointing me to whoever owns that req?"). The direct Tier 2 ask is a deliberate exception to the standard career center advice against asking for a referral in a first message, which assumes unlimited time to build the relationship first.
- Closes with the easy out that still routes, so a no returns a name: "if this doesn't fall under your team, I'd appreciate any direction on who might be best to connect with."
- Sounds like the user wrote it: warm, brief, and in their register. Where it fits, name the tooling they actually build with.

**Founder branch.** When the target is a founder or senior operator at a seed or YC-stage startup who reads their own inbox, the first message is **under 240 characters** with **exactly three beats**: who the user is, what they built that is relevant to them, and why they believe in what they are building. The longer format stays for recruiters and larger companies. The draft must read as the user's, not as generic AI output, and gets an extra pass for template smell before sending. For a small number of high-priority short-list targets (YC companies, a16z-backed or similar early-stage portfolio companies, Series A through B startups), **build something for them instead of describing past work**: a short written proposal naming a concrete problem the user noticed in their product plus a specific fix. It costs hours per target, so it is a short-list tactic and never the default, and the analysis has to actually be good. A founder who reads their own inbox is also the one reader type where a funny or strange opener is allowed; the substance underneath still names something specific and ends on one clear ask, and it never invents a shared history or a fact. See the Networking and Outreach Rules in CLAUDE.md for the canonical wording.

Optionally draft a short follow-up message to send if they accept, but the connection note is the thing that gets sent in Step 5.

**Optional reference:** `reference/3-touch-networking.md` holds David Fano's 3-Touch Networking System (connect with a specific note, add value with no ask 3 to 7 days later, then ask for insight rather than a job). Reach for it when the user is building a relationship over weeks with someone they have no existing tie to, or when a first note landed but there's no natural reason to ask for anything yet. Skip it for the normal case of a single well-aimed note to a school alum. Its "70% of jobs come from networking" stat is unsourced; do not repeat it without verifying.

## Step 4, Show the list and get approval (required checkpoint)

Present a compact table to the user: Name · Title · School alum? · **Tier** · why this person · the exact connection note. State the running Tier 1 count for the week and flag anyone dropped to Tier 2 or skipped as Tier 3, with the reason. Ask them to approve, edit, or drop individual entries. **Do not proceed to send until they give a clear go.** If they edit notes, use their versions.

## Step 5, Send the approved connection requests

Only for the people the user approved, and only after their go: in Chrome, for each profile, open it, click **Connect**, choose **Add a note**, paste the approved note, and **Send**. Go one at a time, keep to a sane volume in a session (LinkedIn limits noted invitations), and if a profile only offers "Follow" or routes through "More", handle it gracefully or skip and tell the user. Never send anything that wasn't in the approved list.

## Step 6, Log and wrap up

- Append each person to `outreach_tracker.csv` with `status` = `sent` (or `skipped`/`failed` with a note in the notes column). **Record the assigned tier in the notes column** (e.g. `tier 1 - hiring manager`) so the next run can count recent Tier 1 asks against the weekly cap.
- Give the user a one-line summary: e.g. "Sent 3 connection requests at <company> (2 alumni, 1 recruiter); 1 skipped (no Connect button), logged in outreach_tracker.csv." Remind them you'll follow up when they accept if they want the follow-up messages sent.
