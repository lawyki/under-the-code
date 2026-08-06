# under-the-code — agent entry point

*Under the Code* — a five-volume interactive computer-science book at
under.atheric.eu. Public, CC BY-NC 4.0. This file is the signpost; it decides
what you read next, nothing more.

> Operating model: `atheric-studios/estate/OPERATING-MODEL.md` — read before
> starting a session.

## Read in this order

1. `BRIDGE.md` — the architect charter. If you are the project's bridge chat,
   this is your founding document.
2. `README.md` — what the repo is and how it deploys.
3. `UNDER.md` — the spine. §4 is the pass ledger; read the most recent entries
   before doing anything.
4. `STATE.md` — where we are · what's next · blocked on Tiger.

## Before you touch anything

- **The gate rhythm is law** (as amended 2026-08-06, `BRIDGE.md` §1): proposal
  → owner veto → per-part execution → ledger → next part, with the owner read
  moved to the end — the book is finalized, verified, declared READY, and Tiger
  reads it once in full. Nothing is declared READY on an unverified clearance.
- **`UNDER.md` §4g (the fact ledger) is law.** Re-introducing a corrected error
  is a failed pass regardless of how well it reads.
- **Anchor-ID law**: anchor sets stay byte-identical across a pass, or migrate
  through `ANCHOR_ALIASES` in `book.js scrollToAnchor`, verified live at zero
  pixel delta. Reading positions are user data.
- **Regenerate the glossary after any prose edit** (`npm run build:glossary`)
  and check the extractor's known gotchas: em-dash clipping, junk entries from
  term cues.
- **Pedagogy first, facts second.** The register bar is the Ch7 pickle coda.
  "Already at bar, left as-is" is a valid and frequent verdict — never
  manufacture change.
- Part IV's serif-on-cream body is deliberate Strongroom identity (§4d/§5).
  Do not "fix" it. Check `UNDER.md` §5 for the other known non-defects.
- The thesis set and the authorship line are owner-authored. Agents typeset
  them, never author them.
