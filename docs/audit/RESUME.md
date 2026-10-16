# Pre-read audit · resume note (paused 2026-10-16 at the owner's request)

All work so far is committed on branch `pre-read-audit` (pushed to GitHub, not merged; `main` is the live site and stays untouched until the audit is retested and gated). Never push or merge to `main`, never tag, from this branch until the owner's read is ready.

## Done (uncommitted)
- Outside-audit fixes (docs/audit/outside.json, 157 confirmed): cover, five part openers/leads/closers, account page
  (+ functions/api/auth/verify.js passkey branch), 85 glossary definitions (scripts/glossary-defs.json; builder now skips
  part-opener mentions and takes a `home` override), 25 cross-references. Blind retest done (docs/audit/outside-retest-result.json),
  one revision applied. clip.mjs 0 findings in 84 runs, tests/pass25 all pass, check:dashes clean, anchors unchanged.
- Chapter 1 round-1 fixes (docs/audit/round1/ch1.json, 54, plus part-1.json items 3, 4, 8, 15, 18): all prose, caption and
  strip edits applied; Figs 1.3, 1.5, 1.6, 1.7, 1.12, 1.13, 1.15 changed. Gate 1 (figs.mjs --motion) clean on those figures;
  --fullscreen leaves ONE failure: fig-1-12, the new neutral outline rect behind "wrong · ~5%" (stroke white@0.35) is named
  by the label "loaded data, still there" and measures 1.66:1 on the red fill in fullscreen. Fix that, rerun fullscreen.

## Next
1. Fix fig-1-12 fullscreen; blind retest of Chapter 1's changed paragraphs (newcomer + expert, Sonnet); one revision.
2. Commit each chapter on the branch as its retest passes. Then chapter by chapter through docs/audit/round1/*.json
   (1,325 confirmed or owner findings: ch2 54, ch3 69, chBridge 52, ch4 73 ... part-N consistency). Owner verdicts
   go to an owner-calls list; kept-original figures and owner text are never edited.
3. Open owner call from the outside audit: privacy notice "D1 database in the European Union" (DB has no EU
   jurisdiction; recreate with --jurisdiction=eu or reword). Not changed.
Tools: docs/audit/tools/el.py (print an element by id), apply.py (exact-once replace).
