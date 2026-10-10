# under-the-code — STATE

The resume header for this repo. `BRIDGE.md` is the architect charter;
`UNDER.md` §4 is the pass ledger; `README.md` says what the repo is.

## WHERE WE ARE

**READY.** Pass 19 — the book-wide closing sweep — completed 2026-08-09
(ledger `UNDER.md` §4s) and declared the book prose-ready for the owner's
complete read. The language pass is complete across all five parts and
independently verified in all five — Part II's audit (Pass-15 verification)
landed 2026-08-10 in parallel with the read: 20 surgical fact fixes, three
fabricated-or-recast quotes replaced with verbatim sourced ones, every §4o
load-bearing correction reconfirmed, ledger under §4o. The coverage table is
now uniform. Its top owner flag is closed: a ratified one-word micro-pass on
2026-08-10 replaced `requestz` with `request` in the Ch7 pickle coda (the
documented Sonatype-2022 typosquat, 404 on PyPI; `requestz` is a real,
legitimate package) — the coda is otherwise untouched. The sweep before it
executed every ruled worklist item (fig 15.2 geometry re-laid; Ch15 →
"Attack and Defence" with the defence-spelling strays in part-1/part-3
brought along; the Diffie–Hellman en-dash migration with its glossary-key
merge; the house spelling convention ratified book-wide and recorded in
`UNDER.md` §5), ran the closing audits clean (cross-part consistency read —
four fact-class cross-reference breaks found and fixed; 462 hrefs + 519
glossary refs, 0 broken; figure sweeps 0 new findings against a
HEAD-identical baseline; full §7 harness 100/100; docs registries
realigned), and confirmed live parity after push. Anchor-id sets
byte-identical in all five parts (354/346/380/228/189).

**Pass 20 — figure-truth, Part II — landed 2026-08-17** (ledger `UNDER.md`
§4t, commit `cff08e3`): the Pass-15 verification's four flagged geometry
defects fixed and live — fig 6.1's "C++ released" marker moved from the
1995 tick to the 1985 tick (x=310, from the timeline's own mapping);
fig 4.5's RR and MLFQ lanes redrawn as legal traces of the figure's own
workload (13-slice RR ending t=26; MLFQ with every slice queue-labelled;
the 8.75/7.75 avg-wait labels recomputed and standing); fig 7.6's
BINARY_MULTIPLY line contained (rect 160→186). Anchors 346 byte-identical,
glossary 519 ±0, §7 spot-check 4/4, live parity confirmed. One new
punch-list flag: fig 7.6's eval-loop line overhangs its rect ~50 px/side
(pre-existing, same class).

**Pass 23 — the book-arc read — landed 2026-08-17** (ledger `UNDER.md`
§4w): the report-only whole-book pedagogy audit, one continuous Fable read
cover→glossary plus two blind mid-book entrants (Part III, Part V). Zero
edits to any book file. **Verdict: the arc holds** — the synthesis is
earned (Ch15's six-pattern unification and Ch18's trace cash the cover's
exact promises; the four disciplines are handed over three times), the
part-identity micro-arcs complete (position fixes → landfall, redactions
→ zero, listing lines → EOF, "Quorum reached · 5 of 5"), and "open any
part to begin" is true. Seven ranked findings for the punch list, top
three: Ch16 §03's memory-ordering peak leans on store buffers (taught
nowhere) and cache coherence (taught three sections later); Ch1's
locality-thread promise ("same equation, all the way up the stack") is
never picked up by name in Parts II–IV; the "What you now understand"
codas stop at Ch4, leaving Ch14/Ch16 without consolidation and Ch18's
title-echo unprimed. Full ranked list with locations and one-line
directions in §4w.

**Pass 25 — Place and Marks — landed 2026-10-09** (ledger `UNDER.md` §4y):
the saved place is now where the reader was *reading* (skims, look-ups,
pop-ups and fullscreen figures no longer move it; detours are remembered and
undoable), shown as a seamless 2 px cue on the bar that widens under the mouse
and can be dragged or set by hand from the place button; sections can be
marked in five colours per volume (glyph + texture, one hue family per slot,
all ≥ 3.05:1, colour-blind-checked — min ΔE 11.4 — with glyph and texture carrying the meaning), listed book-wide under "Your marks" on the
account page. Server-side marks ship **switched off** (`MARKS_SYNC = "0"`)
until the owner approves the privacy wording; place sync for signed-in
readers is unchanged meanwhile. Migration 0002 is applied in production.
**Verified 2026-10-10 by Sonnet 5.5** (§4y "Verification of Pass 25"): the
tracking model holds; 40 findings held — two HIGH (marks lost at sign-out
while sync is off; the place bar and menu clipped on short screens) — all
fixed and re-tested.

**Pass 26 — the dash law — landed 2026-10-10** (ledger `UNDER.md` §4z):
no em dash anywhere a reader sees (~2,860 rewritten, not swapped; enforced
by `npm run check:dashes`), verified by Sonnet 5.5 (20 findings fixed, one
old ARPANET fact corrected). Glossary 519 → 509 (eleven junk entries gone).
The three laws are in `CLAUDE.md`.

The book: five parts, 18 chapters plus the Bridge interlude, ~93k words,
242 figures, glossary at **519** terms (the Diffie–Hellman duplicate row
merged in Pass 19 — see §4s item 3). Five volume identities live; magic-link
accounts and exact reading-position sync live; the §4g fact ledger survives
in substance throughout.

## WHAT'S NEXT — the to-do list (in order)

1. **Marks sync on** once the owner approves `docs/pass-25-copy.md`: apply
   its five replacements in `public/account.html`, set `MARKS_SYNC = "1"`,
   push.
2. **Domain move** (~early November 2026, owner's timing): set
   `SITE_ORIGIN` (wrangler.toml), redirect old URLs with `#anchor` intact,
   hand signed-out readers' local place (and Pass 25 marks) across the
   origin change; then passkeys on — test a real passkey against production
   D1 first, `PASSKEYS_ENABLED = "1"`, `utc-passkeys` meta → `on` in
   `public/account.html`, account intro copy may mention passkeys again.
3. **Retire `/api/auth/request`** after 2026-11-15 (replace with a 410).
4. **Re-tune the Pass 25 thresholds** after the owner's read (`?utc-debug`
   on any part shows the tracker's state; constants in `book.js` `T`).
5. **Passes 27–28: laws 2 and 3** (owner 2026-10-10, `CLAUDE.md`): 27 the
   cut, DONE (§4aa: 11.2 % shorter, glossary authored);
   28 figures IN PROGRESS (§4ab; ledger `docs/pass-28-figures.md`, 26 of 222
   done, pilot published for the owner), every figure one by one, handcrafted and
   tested, kept going by a loop (`docs/pass-28-brief.md`, incl. the owner's
   fig 1.2 note: the image explains itself, text goes into explainers).
6. **The punch-list pass**, after Tiger's read: the read's findings, the
   §4w arc dossier's seven ranked findings (Ch16 §03 scaffolding, the
   locality thread, the coda instrument, the integer-overflow and De Morgan
   promises, the Ch14 primer callback, the Ch17 §02 revisit gloss), fig
   7.6's eval-loop line overhang (Pass 20), the open §4o register flags (two
   Part II hero-lead overclaims) and §4s register flags, the default-blue
   "Chapter 15" link in Part I's Spectre/Meltdown insight strip (§4y).

**Model (owner ruling 2026-10-05, BRIDGE §5):** every pass runs on Opus 5.5;
each is followed by an independent Sonnet 5.5 verification.

**Done:** Pass 25 place and marks + its Sonnet 5.5 verification (§4y; 40
findings held, all fixed or recorded)  · Pass 23 book-arc read (§4w) · Pass 24 accounts v2 (§4x) · Pass 21
icons (§4u) · Pass 22 tabs + touch tooltips (§4v) · Sonnet verification of
21/22/24 with fixes · open-redirect fix · saved-title spacing fix · account
bookmark in the bar (all 2026-10-05 → 10-09). Owner's two old accounts
deleted at his request 2026-10-09 (backup in `~/under-the-code-backups/`);
the live database is empty and ready for fresh sign-ups.

## BLOCKED ON TIGER

Owner decisions and actions live here and nowhere else. If it is not on
this list, it is not blocking.

- **Look at the figure pilot** (https://claude.ai/artifact/ADZTGFP5QqDEqq62E9Ebhn,
  three figures redrawn, before/after and live). One question: is this the
  direction for every figure? The work continues meanwhile; a change you ask
  for is applied to every figure already done.
- **Read the book.** The punch list waits on the complete read. Read-along
  notes: end of `UNDER.md` §4s.
- **Create your new account** at /account ("New here? Create an account")
  — the first real end-to-end email test of Pass 24. Report if the mail
  doesn't arrive.
- **Run the ten-minute screen-reader check** — `docs/pass-25-sr-trace.md`
  (VoiceOver on Mac/iPhone; NVDA if you have Windows). Report what differs.
- **Sign off the Pass 26 wording choices** (§4z "Owner sign-off list": the Zen
  of Python's own punctuation, the shortened Berners-Lee pull-quote, the
  epilogue ornament, quote attributions). Silence keeps them.
- **Sign off the Pass 27 epilogue trims** (§4aa Part V, "For the owner's
  sign-off": restatement cut from Ch18's math, trace, civilization, future,
  intersect, reading and final paragraphs; the book's closing paragraph and
  every changed claim were restored verbatim). Silence keeps them.
- **Approve the Pass 25 privacy wording** — `docs/pass-25-copy.md` (five
  short replacements on the account page). Until then marks stay on each
  device.
- **`.kilo/`** (another tool's folder, untracked in the repo): keep or delete.
