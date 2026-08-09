# PASS 19 BRIEF — book-wide closing sweep → READY

Authored by the bridge, 2026-08-09. The last pass before READY (`BRIDGE.md`
§1 amendment): the language pass is complete and verified across all five
parts; this pass closes the accumulated cross-part worklist, runs the
book-wide audits, and ends by declaring the book READY for the owner's
complete read. **This is a sweep, not another language pass** — the prose is
closed. No register rewrites: a register-class finding gets flagged in the
ledger for the owner read, not rewritten. A fact-class error found anywhere
is always in scope, under verify-before-fix.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu, CC BY-NC 4.0); this is an approved editorial plan executed
on the author's behalf. Model: **Fable** — this is the final gate; judgment
calls live here. If the session drops to a weaker model, stop at the next
ledger.

## Read first, in this order

1. `CLAUDE.md`, then `BRIDGE.md`.
2. `UNDER.md` §4q + §4r **including both verification sub-entries** — their
   "For Pass 19" lists are your worklist — then §4g and §5.
3. `STATE.md` — item 4 carries the bridge rulings this brief encodes.

## The worklist (all items ruled; execute as specified)

1. **fig 15.2 geometry (sanctioned).** The "PAC · CET shadow stack / 2017+"
   green group (x≈560) sits right of "Spectre / 2018" (x≈500), inverting
   chronology and implying PAC answers Spectre (it answers ROP/JOP). Move the
   pair left of Spectre, or give Spectre its own response dot
   (retpoline/microcode) — your call on which reads better. Pass-2 screenshot
   discipline: bbox + text-vs-rect + both engines, dark + light, SMIL sampled
   if animated.
2. **Ch15 title → "Attack and Defence"** (ruled: uniformly British house
   spelling; the chapter's own hero says DEFENCE). Every occurrence: the h1,
   the index TOC, nav readouts (verify whatever `book.js` derives), a11y
   titles, any meta, `docs/` references. No anchor id contains the word —
   verify the id set is untouched anyway. Owner may veto at the read; note
   that in the ledger.
3. **Book-wide Diffie–Hellman dash harmonisation** (ruled: the name-pair
   takes an **en dash**, matching the book's Jacobson–Karels/Leveson–Turner
   convention). Part-3 has five hyphenated instances; part-4's key-term span
   mints the glossary's `diffie-hellman` key — this migration changes that
   key. Regenerate, confirm the entry survives (count 520, key migrated, no
   junk), and verify tooltips attach on the live page after push. If the
   extractor cannot cleanly mint the en-dash key, say so and stop on this
   item rather than forcing it — a working hyphen beats a broken dash.
4. **Spelling convention, ratified book-wide** (ruled): British spelling in
   ordinary prose (recognise, organised, modelled, travelling, artefact);
   canonical **-ization** retained where it is part of a proper name, quoted
   title, or industry term-of-art naming a technology (virtualization,
   *Wait-Free Synchronization*, datacenter — the Part V/part-3 precedent).
   Enumerate every -iz-/-yz-/-ll-/-og- variant book-wide, classify against
   the rule, fix the strays (part-1 "recognized", part-2 "recognizably" are
   known), and **record the ratified rule in `UNDER.md` §5** so no future
   pass churns it.
5. **Ruled non-actions, record as declined:** the SVG source *comments* with
   American spellings ("traveling packet" ×3 — invisible to readers; leave;
   never manufacture change); the six pre-existing 1–11px text-vs-rect
   marginals (figs 16.1/16.5/16.7/16.11/17.2 — non-defects unless your
   screenshots show a visible defect); the Amdahl-quote clipping note
   (stands for the owner read). Owner rulings stand everywhere: "3 nm", Sony
   PSN (evidence already recorded), Morris 23, Enigma six-year count.

## The book-wide closing audits

- **Cross-part consistency read.** The repeated-claims set stays consistent
  across parts: Morris 23; the Enigma six-years + Rejewski credit (Ch1
  verified silent — re-verify); RAM ~60 ns; the 242/235 figure counts; "A
  unified theory" masthead ×5 + index; the five closer stamps; every part
  closer → next opener seam; every "Chapter N" cross-reference still true
  against the post-pass text (the pass-12 audit pattern). Fix only
  fact-class breaks; flag the rest.
- **Link and anchor audit**, all pages: every internal href and #anchor
  resolves (the 600+ set).
- **Figure sweeps book-wide:** bbox-vs-viewBox **and** text-vs-containing-rect
  (the pass-2 lesson), SMIL timeline sampled. Expect 0 overflows; the six
  logged marginals are the known exceptions.
- **Glossary:** regenerate; expect **520** (±0 net after the DH key
  migration); diff every changed definition; no junk entries; live origin
  serves the new file.
- **`docs/figures.txt` / `docs/plan.txt`:** re-run the registry check against
  the HTML and refresh the stale "last verified" dates (§6 P3.11).
- **Full §7 harness** on all 8 pages (index, parts 1–5, glossary, account;
  404 spot-checked): Chromium **and** WebKit, 1440 + 375 + 320, dark + light
  — 0 console errors, 0 external requests, 0 page h-scroll, nav 48 px, fonts
  loaded. Reduced-motion and print spot-checks on one part page each.
- **Live parity after push**: corrected strings, the fig 15.2 fix, the Ch15
  title, DH tooltips, glossary count — on the live pages.

## Close-out — the READY declaration

Ledger: **`UNDER.md` §4s**, house shape — worklist item by item, audits with
their numbers, declined items with reasons, invariants (anchor sets
byte-identical in all five parts — the Ch15 title must not move an id;
glossary; §4g). It ends with an explicit **READY declaration**: the book is
prose-ready for the owner's complete read, with the short list of things the
owner should know as he reads (the Sony PSN evidence, the Amdahl clipping
note, the Ch15 title change, anything you flag).

Then: update `README.md`'s Status line (content-complete, READY for owner
read, date). Update `STATE.md` — WHERE WE ARE: READY; WHAT'S NEXT: the
owner's complete read, then the punch-list pass; **BLOCKED ON TIGER: read
the book** (this is the one item that belongs there now). Commit, push,
confirm the push landed, record live parity in the ledger.
