# Pre-read audit · resume note

Full picture first: `docs/audit/HANDOFF.md` (every run, every findings file, the method, the rules). This note is the running progress.

All work is on branch `pre-read-audit` (pushed to GitHub, not merged). `main` is the live site and stays untouched: never push, merge, rebase onto or tag `main` from this work. Push only to `pre-read-audit` (from a worktree: `git push origin HEAD:pre-read-audit`). **Update 2026-10-23:** the owner said "full yes, deploy"; `pre-read-audit` is merged into `main` (fda8ce0) and deployed to the site; the book is still being built.

## Method per chapter (working laws)
1. Read the chapter's findings (`docs/audit/round1/<ch>.json`, plus the part-N.json items for it) and the whole chapter in `public/part-N.html`.
2. Decide each finding as author: apply (own wording), adjust, or reject with a one-line reason. Owner-only matters go to `docs/audit/owner-calls.md`. Record in `docs/audit/decisions/<ch>.md`.
3. Edit (`docs/audit/tools/el.py` prints an element by id; `apply.py` does exact-once replacements). Keep generator text in `scripts/figs/*.py` in step for text-only changes where the string exists (the generators already lagged the published SVGs before the audit; the page is the source of truth).
4. Blind retest: one newcomer and one expert reader (Sonnet), given only the changed passages, screenshots of changed figures and the page. Results in `docs/audit/retest/<ch>-*.json`. One revision.
5. Checks: `npm run build:glossary`, `npm run build:sections` (restore sections.json if only its timestamp moved), `npm run check:dashes`; anchors (book.js candidate ids outside SVGs) unchanged except new paragraphs, which take the next unused number; Gate 1 on changed figures (`tests/pass28/figs.mjs --fig=... --fullscreen`, and again with `--motion`), `node clip.mjs --pages=part-N`, `sh tests/pass25/run-all.sh`.
6. One commit per chapter, push, update this note.

## Done
- Outside the chapters (docs/audit/outside.json): commit 6a5f607.
- Chapter 1: round 1 in 6a5f607; fig-1-12 fullscreen contrast fixed; blind retest and one revision; checks green (Gate 1 0/192 still+fs and 0/768 motion+fs on the changed figures, clip 0, pass25 all pass). Commit "Pre-read audit: Chapter 1".

- Outside fixes and Chapter 1 are LIVE (owner: "deploy", 2026-10-17, commit 5cc3417 on `main`, merged back into this branch).
- Chapter 2: round 1 from `pre-read-audit-ch2-wip`; blind retest and one revision; Fig 2.3 fullscreen contrast fixed; checks green (`decisions/ch2.md` lists them). Commit "Pre-read audit: Chapter 2".

- Chapter 3: round 1, blind retest, one revision; Figs 3.1, 3.3, 3.6 relabelled; the hero's own title id. Owner calls for Figs 3.7 to 3.11, their captions and the Aleph One quote. Checks green except the two container traces (pass25 on 6e63b69: invariants 812/0, parity 40/0, marks 106/0, ui 120/0, traces 231/2). Commit "Pre-read audit: Chapter 3".
- The Bridge: round 1, blind retest, one revision; Figs BR.4, BR.6, BR.7, BR.8 corrected; BR.1 and BR.2 have their own title ids (no duplicate SVG ids left in Part I). Owner calls for Fig BR.3 and its caption. Gate 1 and clip green. Commit "Pre-read audit: the Bridge" (pass25 on 2f771c5: as for Chapter 3).
- Chapter 4: round 1, blind retest, one revision (Fig 4.4's values redrawn); Figs 4.3, 4.4, 4.16 fixed after Gate 1. Owner call recorded for the Section 03 MMU verdict. Gate 1 and clip green. Commit "Pre-read audit: Chapter 4" (58ddc46).
- Chapter 8: round 1, blind retest, one revision; three captions trimmed after Gate 1; two glossary side effects fixed in the text. Gate 1 and clip green. Commit "Pre-read audit: Chapter 8" (4db5004).
- Chapter 5: round 1, blind retest, one revision. Gate 1 and clip green. Commit 700eb9f.
- Chapter 13: round 1, blind retest, one revision; Figs 13.3, 13.5, 13.6, 13.11 fixed after Gate 1 (merged label, neutral waiting pills, the σ fade made a cut). Two §4g rows. Owner calls for Fig 13.10. Commit 437ad38.
- Chapter 9: round 1, blind retest, one revision; Figs 9.6, 9.8, 9.12 fixed after Gate 1; a curated Flags definition and the NAT entry kept. Commit 09a469a.
- Chapter 6: round 1, blind retest, one revision; pre-existing crowding in Figs 6.5, 6.6, 6.9 fixed. Commit 4582f54.
- Chapter 14 (2502963), Chapter 10 (dfbdec9), Chapter 7 (b0f02e8), Chapter 16 (4175fb6), Chapter 15 (c655f00), Chapter 17 (ae60b58), Chapter 11 (9f0f39d), Chapter 12 (6b840ea), Chapter 18 (b337f1f): each round 1, blind retest, one revision where the readers found something (Chapters 12 and 15 none; Chapter 18 only the owner's Fig 18.6 caption), Gate 1 fixes re-gated to zero, clip and glossary green. Details in each `decisions/<ch>.md`.
- pass25 on b337f1f: invariants 812/0, marks 106/0, ui 120/0; traces 231/2 (the two container timing checks); parity 39/1: one of the 50 sampled positions in part-4 lands within a few pixels of Chapter 13's hero top, where the live reading-line anchor names `ch13-hero-label` and the cached table names `ch13` (fractions 0.032 and 0.004). It comes and goes with page length (also at 437ad38 in Chromium 375, absent at 700eb9f and 2502963), so it is a near-tie the sampling hits, not a moved anchor; anchor ids are unchanged. Left for a `book.js` tie rule if wanted, not changed here (anchor law).
- Close: owner calls collected (`owner-calls.md`), ledger `UNDER.md` §4ae, STATE.md freeze line (1.0-rc2), `docs/todo.md` ticked, owner read map refreshed, tag `v1.0-rc2` on `pre-read-audit`.

## Next
- The pre-read audit is done. Nothing goes live until the owner says "deploy" (merge `pre-read-audit` into `main` then); the owner's read starts at `docs/owner-read-map.md`. Done 2026-10-23: the owner said "full yes, deploy"; merged at fda8ce0 and deployed to the site (the book is still being built); tag `v1.0-rc2` (92ed9f0) pushed the same day.
- Scratch scripts of this run lived in /home/user/sp (not in the repo): `<ch>_apply.py` per chapter, `gate2.sh`, `glcheck.sh`, `prep.sh`, `mk.py`. Gate 1 at 360 px in Chromium rounds glyph advances to whole pixels, so a label that clears its neighbour in WebKit can crowd it there.

## Running the checks in a cloud container (Linux)
- `git fetch --unshallow origin` first: pass25's invariants read their baseline from commit d1bbb42, which a shallow clone lacks (it then compares the page with itself and reports 30 false tab-stop failures).
- `npm ci` at the root (check:dashes needs esbuild); `cd tests/pass25 && npm i --no-save playwright`; browsers with `PLAYWRIGHT_BROWSERS_PATH=<dir> npx playwright install --with-deps chromium webkit`, and export the same variable for every run.
- Run Chromium with overlay scrollbars (`--enable-features=OverlayScrollbar`, as phones and Macs have): Linux's classic scrollbar plus `scrollbar-gutter: stable` takes 15 px off the viewport and fails every 13 px label at 360 px. The session used uncommitted copies `tests/pass28/figs.local.mjs` and `clip.local.mjs` that differ from the originals only in that launch argument.
- traces.mjs fails two timing checks (a CDP flick, long tasks over 50 ms under 4× throttle) in the container on dc2ebbd too: the container, not the book.

## Pending
- Owner calls: `docs/audit/owner-calls.md` (privacy notice EU wording so far).
