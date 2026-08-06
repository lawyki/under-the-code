# under-the-code — agent entry point

*Under the Code* — a unified theory of how computers actually work. Five parts,
eighteen chapters plus the Bridge, ~93,000 words, 242 inline-SVG figures.
Published at **under.atheric.eu** under CC BY-NC 4.0.

## Read in this order

1. `README.md` — what the book is, the repo layout, how it develops and deploys.
2. `UNDER.md` — the survey and quality log. It is the working baseline: what the
   site is, what was defective, what each pass fixed, and what remains. The pass
   ledger is §4a–§4q; read §4q for where the language pass stands.
3. `STATE.md` — where we are · what's next · blocked on Tiger.

> Operating model: `atheric-studios/estate/OPERATING-MODEL.md` — read before
> starting a session.

## Invariants — do not violate these before you have read further

- **No framework, no bundler, no build step** for the pages. The tooling is
  `scripts/build-glossary.js` and `scripts/add-anchor-ids.js`, nothing more.
- **Zero third-party requests.** Fonts are self-hosted; the privacy notice
  depends on that staying true.
- **`UNDER.md` §4g's fact corrections are law.** Do not re-open a corrected fact
  without a primary source.
- **`UNDER.md` §5 lists deliberate choices that look like defects.** Read it
  before "fixing" anything.
- **The pass sequence stops for owner review between parts** — the gate rhythm.
  Part V does not open until Tiger has read Pass 17.
- Verification protocol is `UNDER.md` §7: both engines, 1440 + 375, zero console
  errors, zero external requests, no horizontal scroll.
- Owner decisions live in `STATE.md` § BLOCKED ON TIGER and nowhere else.
