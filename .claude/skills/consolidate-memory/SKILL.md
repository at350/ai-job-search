# Consolidate Memory

**name:** consolidate-memory
**description:** Monthly maintenance pass over the job-search workspace's memory files: fold the approved-bullets ledger into the master bullet bank, prune and promote learned voice notes, clean dead rows out of the opportunities state file, archive old digests, and check the two profile files for drift. Trigger on: "consolidate memory", "clean up memory", "merge the ledger", "monthly maintenance". Runs on a monthly schedule and on demand.
**allowed-tools:** Read, Write, Edit, Glob, Grep, AskUserQuestion

---

## Why this exists

The workspace's learning loops only append. Without a periodic fold-in, the ledgers, voice notes, and state file grow until they bury the signal. This skill is the digest step: merge what's proven, prune what's stale, and keep every file at working size.

## The pass (run in order)

1. **Fold the approved-bullets ledger into the master bank.**
   - Read `documents/cv/approved-bullets.md`. For every entry with status `new`, add the bullet to the matching role in the master bullet bank (`documents/cv/MASTER Bullet Bank.docx`), rebuilt with a `docx` build script per the House Style Spec.
   - Mark each folded entry `merged-into-bank (YYYY-MM-DD)` in the ledger and note at the top of the ledger what was merged this pass. Do not delete ledger entries; they are the provenance record.
   - Entries marked "captured via experience-capture, rough form" go into the bank only if they are concrete enough to be a real bullet option; otherwise leave them pending with a note.
2. **Groom the learned voice notes** in `.claude/skills/job-application-assistant/03-writing-style.md` ("Learned from Approvals"):
   - Promote any "signal (seen once)" note that has since appeared a second time to "confirmed".
   - Merge duplicate or overlapping notes into one.
   - Flag notes older than 6 months that never got a second sighting; ask the user before deleting anything, since these encode their taste.
3. **Clean the opportunities state file** (`opportunities/opportunities-state.md`):
   - Remove struck-through/dead rows (applied, closed, expired) from the Open Now table; the tracker CSV already records the outcome.
   - Remove snooze-table rows whose resurface date has passed (per the file's own rule).
   - Verify the "Last updated" date and any deadline that has already passed.
   - **Rot check on the daily tracker's named lists:** if the month's digests or state file marked any named program dead, discontinued, or renamed, update the corresponding entry in `.claude/skills/daily-opportunities-tracker/SKILL.md` so the sweep stops searching for corpses.
4. **Archive old digests:** move `opportunities/digest-*.md` older than 30 days into `opportunities/archive/`.
5. **Groom the media library** (`documents/library/`): confirm `index.md` matches the files on disk, and list any items still marked "take: not captured yet"; ask the user for quick takes on the ones worth keeping (a one-liner each is enough) and update the files.
6. **Drift check on the two profile files:** diff the core facts (status/class standing, target windows, coursework taken vs upcoming, roles and dates, skills) between CLAUDE.md's Candidate Profile and `.claude/skills/job-application-assistant/01-candidate-profile.md`. CLAUDE.md is canonical; fix the other file, and flag anything where CLAUDE.md itself looks outdated (e.g. class standing after a term ends, a role that ended) for the user to confirm.
7. **Receipt.** End with a short summary: N bullets folded, N notes promoted/merged, N state rows cleared, N digests archived, takes collected, drift found or none. If any step needed a judgment call the user should know about, list it in one line each.

## Rules

- Follow CLAUDE.md's Global Writing Rules (no em-dashes, concise, plain).
- Never delete information that exists nowhere else; archive or mark it instead.
- Anything ambiguous (a bullet that might be a NEW CLAIM variant, a voice note the user might still want) gets asked about, not silently dropped.
