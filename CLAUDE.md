# under-the-code — agent entry point

*Under the Code* — a five-volume interactive computer-science book at
under.atheric.eu. Public, CC BY-NC 4.0. This file is the signpost; it decides
what you read next, nothing more.

> Operating model: `../estate/OPERATING-MODEL.md` (canonical name
> `atheric-studios/estate`; on this disk the sibling folder is `estate/`) —
> read before starting a session.

## Read in this order

1. `BRIDGE.md` — the architect charter. If you are the project's bridge chat,
   this is your founding document.
2. `README.md` — what the repo is and how it deploys.
3. `UNDER.md` — the spine. §4 is the pass ledger; read the most recent entries
   before doing anything.
4. `STATE.md` — where we are · what's next · blocked on Tiger.

## The three laws (owner, 2026-10-10)

Binding on every pass, every file a reader can see, every future edit.

1. **No em dashes, ever.** Not in prose, figures, captions, labels, tabs, UI
   strings, page titles, meta, the glossary or the mails. Rewrite the sentence
   with better language (a full stop, a colon, a comma, parentheses, a
   restructured clause); never swap in a look-alike. Section labels read
   "01 · Context". The en dash keeps its two jobs only: ranges (1950–1960) and
   name pairs (Diffie–Hellman). `npm run check:dashes` must pass.
2. **Every paragraph does a job.** It teaches, shows, or moves the reader to
   the next idea, once, in its strongest place. Restating, announcing ("it is
   important to note"), summarising what was just said, three examples where
   one works, and transitions that only fill space are cut or merged. Length
   costs an AI nothing and costs the reader everything.
3. **The picture carries it.** A figure shows the mechanism, it does not hold
   a text column. Readable at 375 px (no label below 11 CSS px rendered),
   nothing overlapping or clipped, as few words as the idea allows, motion
   where motion is the mechanism (reduced motion respected), a caption of at
   most two sentences. The explanation lives in the prose.

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
