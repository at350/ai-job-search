# Handshake seen-list format

This block lives inside the tracker's `opportunities-state.md`. It's how the scan
remembers what it already showed the user, so the same posting never appears
twice. Keep it append-only (prune entries older than ~60 days occasionally so it
doesn't grow forever — postings expire well before then).

```markdown
## Handshake — seen postings
*Append-only fingerprint log. Fingerprint = `company | title` lowercased. Used to
dedupe the daily Handshake scan. Last scanned: YYYY-MM-DD.*

| First seen | Fingerprint | Bucket | Deadline noted |
|---|---|---|---|
| 2026-06-05 | dropzone robotics \| computer vision & perception engineering intern | Tech | rolling |
| 2026-06-05 | 1752vc \| venture capital fellow — summer 2026 | Fellowship | unconfirmed |
```

## Notes

- The "Last scanned" date is the freshness cutoff for the **newest-first delta**
  pass. Walk that feed only until postings predate it. (The deadline-sorted deep
  sweep doesn't use this cutoff — it's bounded by how far out deadlines go, ~3–4
  weeks.)
- Bucket is one of: `Tech`, `Fellowship`, `Event`.
- If a posting reappears with a *changed* deadline (e.g. extended), it's fine to
  re-surface it once with a "(deadline updated)" note and refresh the row.

## Cached major IDs (for the deadline-sorted deep sweep)

The `majors=<id>` URL param is school-specific. Cache the ones you've looked up so
future runs don't have to rediscover them. Keep a small block like:

```markdown
### Handshake major IDs (this user's portal)
| Major | majors= ID |
|---|---|
| Computer Science | 28 |
```

To find a new one: open the Filters panel → type the major in the "Majors" box →
click it → Apply → read the `majors=` value from the resulting URL.
