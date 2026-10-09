# Pass 25 — privacy wording for owner approval (marks sync)

Server-side marks and the "set it yourself" flag ship **switched off**
(`MARKS_SYNC = "0"` in `wrangler.toml`). Until this wording is approved,
signed-in readers keep exactly today's sync (one reading position), and
section marks stay on the device like a signed-out reader's. The privacy
notice on `/account` stays accurate as it is.

On approval: apply the four replacements below to `public/account.html`, set
`MARKS_SYNC = "1"`, apply migration `0002_marks.sql` to production if it is not
there yet, push. Nothing else changes.

The 180-day tombstone purge the retention line promises already runs inside
every `/api/marks` request (review H13), so the copy is true from the moment
it is published.

## 1 · Intro paragraph (privacy notice, first paragraph)

**Now:**
> Reading progress for signed-out readers lives in your browser's localStorage
> and never leaves your device. An account adds exactly one thing — the same
> reading position, stored server-side so it can follow you between devices.

**Proposed:**
> Reading progress **and section marks** for signed-out readers live in your
> browser's localStorage and never leave your device. An account adds **two
> things: the same reading position, and any sections you mark**, stored
> server-side so they can follow you between devices.

## 2 · "What is stored" (the reading-position clause)

**Now:**
> …and one reading position — which part of the book, a paragraph anchor, an
> offset within it, chapter and section titles, and when it was last updated.

**Proposed:**
> …and one reading position — which part of the book, a paragraph anchor, an
> offset within it, chapter and section titles, **whether you set it yourself,**
> and when it was last updated. **The sections you mark: which section, the
> colour you chose, and when you last changed it.**

## 3 · Retention (append to the bullet)

> **Marks stay until you remove them. A removed mark leaves a short note (which
> section, and when) so your other devices remove it too; the note is erased
> after 180 days.**

## 4 · Deletion (the bullet, and the button's status text)

**Bullet:** "…removes your email, password, passkeys, sessions and position
**and marks** immediately and completely…"

**Button status** ("This removes your email, password, passkeys, sessions and
reading position immediately.") → "…sessions, reading position **and marks**
immediately."

## Notes for the owner

- The place record also carries technical fields when the flag is on: a
  random per-tab tag and a counter, so a slow network can't make an older save
  land after a newer one (review H4) — they identify a browser tab for one
  visit, not a person; the paragraph the labels name (another paragraph
  anchor, already covered by "a paragraph anchor"); and whether the place is in
  the part's last section. The wording above doesn't name them; say if you
  want a clause.
- UI strings already shipped (not privacy copy): `Set to where I’m reading`,
  `Go to saved place`, `Mark this section`, `Back to before the detour`,
  `Let the book track`, `Place set · Undo`, `SAVED ON THIS DEVICE`, `SYNCED`,
  `SAVED HERE · SYNC PAUSED`, `Reading sync · sign in`.
