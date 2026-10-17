# Pre-read audit · resume note

Full picture first: `docs/audit/HANDOFF.md` (every run, every findings file, the method, the rules). This note is the running progress.

All work is on branch `pre-read-audit` (pushed to GitHub, not merged). `main` is the live site and stays untouched: never push, merge, rebase onto or tag `main` from this work. Push only to `pre-read-audit` (from a worktree: `git push origin HEAD:pre-read-audit`).

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

## Next
- Chapter 2 (`ch2.json` 54, part-1.json items 12, 13, 16, 17, 25 counted 1-based). Decisions drafted in `docs/audit/decisions/ch2.md`.
- Then ch3 (+ part-1 items 1, 5, 6, 19, 23, 24, 26; owner items for Figs 3.7 to 3.11 and the Aleph One quote), chBridge (+ the rest of part-1), ch4–ch7 (+ part-2), ch8–ch12 (+ part-3), ch13–ch15 (+ part-4), ch16–ch18 (+ part-5).

## Pending
- Owner calls: `docs/audit/owner-calls.md` (privacy notice EU wording so far).
- Duplicate SVG title ids still present: svgt-part1-30 (Ch3 hero and Fig 3.2), -39 and -40 (Figs 3.9/3.10, kept-original, against BR.1/BR.2): fix with Ch3 and the Bridge.
