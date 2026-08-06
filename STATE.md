# Under the Code — STATE

The resume header for this repo. `README.md` says what the book is and how it is
built; `UNDER.md` is the survey and quality log, and the pass ledger lives there.

## WHERE WE ARE

The book is written and live at **under.atheric.eu** — five parts, eighteen
chapters plus the Bridge interlude, ~93,000 words, 242 inline-SVG figures, a
520-term auto-glossary. Static `public/` on Cloudflare Pages; the only service
alongside it is the account/reading-position API in `functions/` on D1
(magic-link auth, position by anchor + fraction, never raw scrollY).

**The pedagogical language pass has completed Parts I–IV.** The chain, all
ledgered in `UNDER.md`:

- Pass 14 — Part I (§4n, 2026-08-01)
- Pass 15 — Part II, Ch4–7 (§4o, `6a94554`)
- Pass 16 — Part III, Ch8–12 (§4p, `c4c41ea`) + its verification audit
- **Pass 17 — Part IV, Ch13–15 (§4q, `e639b98`, 2026-08-03)**, ledger at
  `0b8081f`. Recalibrated to *pedagogy first, facts second*.

HEAD is `0b8081f`. The tree is clean; nothing is half-written.

**Part V is the one part remaining** — the last language pass in the sequence.

## WHAT'S NEXT

**Part V of the language pass.** The method is established and needs no new
design: per-section student-readers → adversarial defence pass → fact/voice
confirmation gate. Carry the Pass 17 recalibration (pedagogy first, facts
second) and Tiger's own reading notes into the brief.

It is **not** waiting on a Fable usage reset — an older note said so and was
wrong. It is waiting on the gate below, which is the design working as intended.

## BLOCKED ON TIGER

Owner decisions live here and nowhere else. If it is not on this list, it is not
blocking.

- **Owner review of Pass 17 (Part IV) before Part V opens.** `UNDER.md` §4q
  states the gate in its own words: *"STOP for owner review before Part V — the
  gate rhythm."* Every pass in this sequence stops for Tiger's read; this is the
  rhythm, not a stall. Nothing else is required to unblock Part V, and reading
  costs no model budget.
- **`UNDER.md` §6** — the prioritized improvement backlog for later passes,
  explicitly marked as needing owner sign-off. Not started, by design.

## Standing rules

- `UNDER.md` §4g's fact corrections are **law**. Do not re-open a corrected fact
  without a primary source.
- `UNDER.md` §5 lists deliberate choices that look like defects. Read it before
  "fixing" anything.
- `UNDER.md` §7 is the verification protocol — repeat it after any pass (both
  engines, 1440 + 375, zero external requests, zero console errors).
