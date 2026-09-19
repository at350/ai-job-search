<p align="center">
  <img src="claude_animation.gif" alt="Claude Job Search Assistant" width="200">
</p>

# AI Job Search

An AI-powered job application framework built on [Claude Code](https://claude.com/claude-code). Fork it, fill in your profile, and let Claude evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

## What this is

A structured workflow that turns Claude Code into a full-stack job application assistant. The core workflow (self-profiling, fit evaluation, and the evidence-gated application pipeline) is **language- and country-agnostic**. The job portal search skills are built for the Danish market (Jobindex, Jobnet, Akademikernes Jobbank, etc.), but the pattern is designed to be swapped for your local job boards.

Every document is built as a `.docx`, rendered to PDF, and mechanically verified before you are asked to approve it. Nothing reaches an employer that a verifier has not read in its rendered form.

```
/setup          /scrape              /apply <url>
  |                |                     |
  v                v                     v
Fill in        Search job           Evaluate fit
your profile   portals              Score & recommend
  |                |                     |
  v                v                     v
Profile        Present matches      Benchmark -> your draft
files ready    with fit ratings     -> Gates A, B, C -> submit
```

The framework encodes career guidance best practices, including structured evaluation criteria, forward-looking cover letter framing, and optional salary benchmarking.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (CLI)
- Python 3.10+
- Node 18+ and `npm install` (the `docx` package builds every document)
- LibreOffice (`soffice`) to render DOCX to PDF, and `poppler-utils` for the PDF verifiers
- [Bun](https://bun.sh) (for the Danish job search CLI tools, optional)

## Quick start

### 1. Fork and clone

```bash
gh repo fork MadsLorentzen/ai-job-search --clone
cd ai-job-search
```

### 2. Install dependencies

```bash
npm install     # the docx package, used by every document builder
```

Optional, for the Danish job portal CLIs:

```bash
cd .agents/skills/jobbank-search/cli && bun install && cd ../../../..
cd .agents/skills/jobdanmark-search/cli && bun install && cd ../../../..
cd .agents/skills/jobindex-search/cli && bun install && cd ../../../..
cd .agents/skills/jobnet-search/cli && bun install && cd ../../../..
```

### 3. Set up your profile

```bash
claude
# Then inside Claude Code:
/setup
```

`/setup` offers three paths: read your `documents/` folder if you have one populated (CV PDF, LinkedIn export, diplomas, reference letters, past applications), import a single CV pasted in chat, or walk through an interview. It auto-detects what you have and asks. Documents-folder mode is idempotent and safe to re-run as you add more material; see `documents/README.md` for the layout.

### 4. Search for jobs

```bash
/scrape
```

This searches multiple job portals for positions matching your profile, deduplicates results, and presents them sorted by fit. Pick a match to run `/apply` on it directly.

### 5. Apply to a job

```bash
/apply https://jobindex.dk/job/1234567
```

If the URL can't be fetched (some job portals block automated access), you can paste the job description directly instead:

```bash
/apply <paste the full job description here>
```

This runs the full workflow: check the posting is live and you are eligible, build the benchmark and your benchmark-fit draft, reconcile every unverified claim with you, render and verify the PDF, then wait for your approval of that exact file before anything is uploaded.

## Other commands

`/setup`, `/scrape`, and `/apply` form the core workflow. Two more commands extend it once your profile is in place:

- **`/expand`** enriches your profile by scanning public sources you've already linked in it (GitHub repos, portfolio site, Kaggle, Google Scholar) and looking up syllabi for named courses and certifications. Discovered competencies are added to your profile with a source tag. Useful right after `/setup` to surface skills that documents alone don't make explicit.
- **`/upskill`** analyzes the gap between your profile and your tracked job postings (or a single posting via `/upskill <URL>`). Produces a prioritized heatmap of skill gaps and a learning plan with web-searched study resources and time estimates. Useful for career planning between applications.

`/reset` is also available, see [Starting over](#starting-over) below.

## Skills beyond the application itself

Skills are folders of instructions under `.claude/skills/`. Ask for one by name, or let the assistant pick it up from context.

| Skill | What it does |
|---|---|
| `daily-opportunities-tracker` | A daily digest of live opportunities: internships, fellowships, hackathons, research, competitions, events. Configure your sources and filters in its state file. |
| `handshake-scan` | Sweeps your university's Handshake board for postings no public aggregator indexes, and folds them into the digest. Needs a logged-in browser. |
| `warm-outreach` | Triage a contact, then draft a referral or networking message you actually approve before it is sent. |
| `interview-prep` | Facts file, full prep pack, one-page desk sheet, scored drills, and a post-interview log that feeds back into the profile. |
| `advice-intake`, `media-intake`, `mymind-intake` | Turn career advice, a talk or article, or your saved-content export into dated, indexed claims under `documents/playbook/` and `documents/library/`. |
| `experience-capture` | A regular pass that asks narrow, artifact-anchored questions and writes new evidence into your profile and bullet bank. |
| `consolidate-memory` | Periodic cleanup: merge duplicates, retire superseded facts, and keep each fact in exactly one home. |
| `humanizer` | Strips the tells of AI-generated writing from a draft. |
| `upskill` | Gap analysis between your profile and the postings you are tracking, with a study plan. |

None of these skills assist during a live or recorded assessment, and none send a message or submit an application without your explicit approval.

## File structure

```
ai-job-search/
├── CLAUDE.md                          # Profile, rules, and the application pipeline
├── .claude/
│   ├── commands/                      # /apply /setup /expand /reset
│   ├── hooks/brevity-gate.py          # Stop hook: caps chat replies at 120 words
│   ├── settings.json                  # Registers the hook
│   └── skills/
│       ├── job-application-assistant/ # Core application skill
│       │   ├── SKILL.md               # Operational summary and file map
│       │   ├── 01-candidate-profile.md through 07-interview-prep.md
│       │   ├── 08-application-answers.md   # Short-answer and essay workflow
│       │   ├── 09-resume-evidence-audit.md # Gate 0, Gate A, Gate B, Gate C
│       │   ├── 10-house-style.md           # The one home for formatting rules
│       │   └── 11-verification-checklist.md
│       ├── daily-opportunities-tracker/    # Daily digest of live opportunities
│       ├── handshake-scan/                 # University portal sweep
│       ├── warm-outreach/                  # Networking and referral messages
│       ├── interview-prep/                 # Facts file, drills, post-interview log
│       ├── advice-intake/ media-intake/ mymind-intake/  # Capture advice and saved material
│       ├── experience-capture/ consolidate-memory/      # Keep the profile current
│       ├── humanizer/ upskill/ job-scraper/
├── .codex/                            # Codex agent definitions
├── .agents/skills/                    # Job portal CLI tools (Denmark)
├── cv/
│   ├── build_epsilon_lib.js           # Shared docx-js helpers (house style)
│   ├── build_resume_example.js        # Format reference builder
│   ├── candidate.example.json         # Identity template; copy to candidate.json
│   ├── candidate_profile.py           # Loads that identity for the verifiers
│   ├── verify_resume_layout.py        # Gate B: the rendered PDF
│   ├── verify_gate0_provenance.py     # Gate A: claim provenance and hashes
│   ├── verify_application_header.py   # Resume and cover letter headers match
│   └── main_example.tex               # Legacy LaTeX template
├── cover_letters/                     # Legacy LaTeX class and fonts
├── documents/                         # Your material (git-ignored)
│   ├── cv/ linkedin/ diplomas/ references/ applications/
│   ├── private/                       # Approved answers, essay context, beliefs
│   ├── playbook/                      # Career advice you saved, with an index
│   ├── library/                       # Books, talks, and articles you captured
│   └── portals/                       # One file per applicant tracking system
├── opportunities/ interviews/ outreach/  # Workspace output (git-ignored)
├── salary_lookup.py                   # Salary benchmarking tool (BYO data)
├── job_search_tracker.csv             # Application tracking spreadsheet
└── SETUP.md                           # Detailed setup guide
```

## How `/apply` works

`/apply` runs an **evidence-gated pipeline**. Each gate blocks the next step.

1. **Liveness and eligibility.** Confirm the posting is open and that you formally qualify, before any tailoring.
2. **Gate 0, the benchmark.** Build the resume a perfect candidate for this exact posting would have, labeled `DO NOT SUBMIT - HYPOTHETICAL BENCHMARK`, then a complete benchmark-fit draft of your own resume against it. Anything the draft asserts that your files do not yet support is tracked as `NEW CLAIM - UNVERIFIED` and the artifact is labeled `DO NOT SUBMIT - UNVERIFIED CLAIMS`.
3. **Gate A, claim reconciliation.** You confirm, correct, tone down, or reject every unverified claim. `cv/verify_gate0_provenance.py` checks that each one carries a dated source and that the draft hash still matches.
4. **Gate B, the rendered document.** The DOCX renders to PDF and `cv/verify_resume_layout.py` reads the PDF: page count, embedded fonts, reading order, contact line, bullet shape and density, paragraph spacing, orphans, section structure, and that the PDF is the fresh partner of that DOCX.
5. **Page-value reconciliation.** The three strongest confirmed outcomes that did not make the page are named, with why each lost. A one-page render alone is not success.
6. **Approval.** You approve one exact PDF. Anything unchecked is labeled `NOT CHECKED`.
7. **Gate C, packet consistency.** The approved PDF is checked against every form field and any transcript, and each difference is disclosed before the Submit click, which needs its own approval.

All claims are traced to your own confirmed material. The system never fabricates skills, metrics, or experience.

### What makes this workflow different

- **The benchmark comes first.** Writing the ideal candidate's resume before your own turns tailoring into a gap analysis instead of a guess, and it exposes the claims you would have to invent to compete. Those claims are surfaced for you to rule on rather than quietly written in.
- **Verification reads the render, not the source.** "Looks fine in the `.docx`" is not a check. The verifier reads the PDF a recruiter would open, and a failure blocks the review gate.
- **Unverified content is labeled, not deleted.** Benchmark and benchmark-fit artifacts carry `DO NOT SUBMIT` in the filename and on the page, so a draft cannot be mistaken for a deliverable.
- **Memory is separated by kind.** Facts about you, approved bullet wording, form answers, portal mechanics, and application records each have exactly one home, so a correction lands in one place and is reused everywhere.
- **The loop closes after submission.** Approved new claims land in your bullet bank, portal lessons land in the portal file, and the tracker records the exact file and hash that was sent.

## Customization

### Which files to edit manually

If you prefer editing files directly instead of using `/setup`:

| File | What to change |
|------|---------------|
| `CLAUDE.md` | Your full profile (name, education, experience, skills, goals) |
| `01-candidate-profile.md` | Structured version of your CV data |
| `cv/candidate.json` | Name, contact line, and school the builders and verifiers use |
| `02-behavioral-profile.md` | Your behavioral assessment or self-assessment |
| `04-job-evaluation.md` | Skill match areas, career goals, motivation filters |
| `05-cv-templates.md` | Profile statement templates for different role types |
| `07-interview-prep.md` | Your STAR examples from actual experience |
| `search-queries.md` | Job search queries for your skills and location |

### Updating your search queries

As your priorities evolve, you can reconfigure just the job search without re-running the full profile setup:

```
/setup --section search
```

This re-runs the search configuration interview: which roles to target, which skills to search for, which locations, and which portals. It also suggests role types you may not have considered based on your profile.

### Document templates

Documents are built by Node scripts using the [`docx`](https://www.npmjs.com/package/docx) package. `cv/build_epsilon_lib.js` holds the house-style helpers (fonts, spacing, bullets, header) and `cv/build_resume_example.js` shows the shape of a builder. Change the formatting in one place, `10-house-style.md`, and update the helpers to match; the verifiers enforce what that file says.

The LaTeX templates (`cv/main_example.tex`, `cover_letters/cover.cls` with Lato/Raleway) are the earlier pipeline and still work, but the skills and verifiers target the DOCX pipeline.

### Job search tools

The four CLI tools in `.agents/skills/` are specific to the **Danish job market** (Jobbank, Jobdanmark, Jobindex, Jobnet). They demonstrate the pattern for building job portal integrations. If you're in a different country, you can build equivalent tools for your local job portals using the same structure.

### Salary benchmarking

The salary tool works with any salary data you provide (union statistics, Glassdoor exports, personal research, etc.). See `tools/README_SALARY_TOOL.md` for the expected format and setup. If you don't have salary data, the salary step is simply skipped.

### Starting over

To wipe your profile data and start fresh:

```
/reset profile    # clears skill files, preserves framework rules
/reset documents  # deletes files from documents/ folder
/reset all        # both
```

`/reset` shows exactly what will be deleted and requires you to type `RESET` to confirm. Nothing is deleted until you do.

## Tips for better results

### Profile depth matters

The single biggest factor in output quality is how much detail you put into your profile. A thin profile produces generic applications; a detailed one enables genuinely tailored results.

- **Role descriptions:** Don't just list job titles. Describe what you actually did in each position: specific projects, tools used, responsibilities, and measurable achievements. The more material you provide, the more precisely the system can reframe your experience for different roles.
- **Skills in context:** Instead of listing "Python" or "project management," describe how and where you applied them. "Built ML pipelines for customer churn prediction in Python using scikit-learn" gives the system far more to work with than "Python, machine learning."
- **All onboarding paths work:** Whether you point `/setup` at your `documents/` folder, paste a single CV, or walk through the interview, the principle is the same: richer input produces sharper output.

### Career path discovery

The framework supports two distinct modes of job searching:

- **Explicit targeting:** You know which roles or sectors you want. The system helps refine and prioritize based on fit.
- **Latent opportunity discovery:** By analyzing your full history (not just job titles, but the actual work you did), the system can surface career paths you haven't considered. Transferable skills that map to unexpected industries, patterns in what you enjoyed or excelled at, or emerging roles that combine your domain expertise with new technology.

To get the most from this, invest time during `/setup` in describing not just your experience, but what energized you, what drained you, and what you'd want more of. This context directly shapes how the system evaluates fit and which roles it surfaces during `/scrape`.

## Acknowledgements

- [Mikkel Krogholm](https://github.com/mikkelkrogsholm) ([skills repo](https://github.com/mikkelkrogsholm/skills)) for the job search CLI skills
- Built with [Claude Code](https://claude.com/claude-code) by [Anthropic](https://anthropic.com)

## License

MIT
