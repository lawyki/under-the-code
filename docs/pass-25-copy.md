# Pass 25 — privacy wording for owner approval (marks sync)

Server-side marks and the "set it yourself" flag ship **switched off**
(`MARKS_SYNC = "0"` in `wrangler.toml`). Until this wording is approved,
signed-in readers keep exactly today's sync (one reading position), and
section marks stay on the device like a signed-out reader's. The privacy
notice on `/account` stays accurate as it is.

On approval: apply the five replacements below to `public/account.html`, set
`MARKS_SYNC = "1"`, push (migration `0002_marks.sql` is already applied in
production). Nothing else changes.

The 180-day purge of removal notes already runs inside `/api/marks` (every
save, and a read at most hourly; review H13), so the copy is true from the
moment it is published. Revised 2026-10-10 after the Sonnet 5.5 verification:
the wording now names every field the server stores once the flag is on.

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
> offset within it, chapter and section titles, **the paragraph you were
> reading, whether you set the place yourself, whether it is in the part's last
> section, and — so a slow connection can't save an older place over a newer
> one — a random tag for the open page and a save counter;** and when it was
> last updated. **The sections you mark: which section, the colour you chose,
> and when you last changed it.**

(The closing "Nothing else." of that bullet then stays true.)

## 3 · Retention (append to the bullet)

> **Marks stay until you remove them. A removed mark leaves a short note (which
> section, its last colour, and when) so your other devices remove it too; the
> note is erased after about 180 days.**

## 4 · "What it is for" (the bullet)

**Now:** "signing you in and putting you back at your paragraph. Nothing else."

**Proposed:** "signing you in, putting you back at your paragraph, **and keeping
your section marks the same on every device.** Nothing else."

## 5 · Deletion (the bullet, and the button's status text)

**Bullet:** "…removes your email, password, passkeys, sessions and position
**and marks** immediately and completely…"

**Button status** ("This removes your email, password, passkeys, sessions and
reading position immediately.") → "…sessions, reading position **and marks**
immediately."

## Notes for the owner

- The random page tag identifies an open browser tab for one visit, not a
  person; it exists only so two saves arriving out of order can't overwrite
  the newer one (review H4).
- Not stored on the server, so not in the copy: the account tag the server
  sends back (a short hash of the account id, computed on each request). Your
  browser keeps it beside your place and marks so a shared device can tell two
  accounts apart.
- UI strings already shipped (not privacy copy): `Set to where I’m reading`,
  `Go to saved place`, `Mark this section`, `Back to before the detour`,
  `Let the book track`, `Place set · Undo`, `SAVED ON THIS DEVICE`, `SYNCED`,
  `SAVED HERE · SYNC PAUSED`, `Reading sync · sign in`.
