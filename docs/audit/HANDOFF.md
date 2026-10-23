# Pre-read audit · full handoff

For any session (cloud or local) that continues the pre-read audit. Read this file whole, then `docs/audit/RESUME.md` (the running progress note), then work.

## Why this audit exists

The owner, 2026-10-15, after v1.0-rc1: "verify the passes ... go through the book in really careful detail ... and verify that the things the LLM console proposed are actually done well, with high quality ... so I would need to come back to you while reading the book as little as possible." Extra tokens granted; ultracode on (exhaustive, adversarially verified, token cost no constraint). His read is meant to be one pass; every finding left in the book is a return trip for him.

## What has already been run (all results are in this folder)

| Run | Agents | What it did | Result | Files |
|---|---|---|---|---|
| Book audit, round 1 | 260 | A newcomer reader per section (116, protocol `docs/pass-29-cold-reader.md`, packets from `scripts/section-packet.mjs`); per chapter a fact checker, a craft and laws reader and a figure checker (19 each); a consistency reader per part (5); then a Sonnet skeptic judged every finding (81 judges) | 2,005 findings judged: 1,240 confirmed, 85 owner, 680 rejected | `round1/<chapter or part>.json` (confirmed and owner only, with the judge's reason and fix); `raw/book-audit-judged.json` (every finding with its verdict, rejected ones included); `raw/book-audit-agents.json` (every agent's raw output by label) |
| Outside the chapters | 48 | Part openers, chapter leads and closers, cover, account and 404 pages (7 readers); all 478 glossary entries (12 batches); every cross-reference (5 readers); 24 skeptic judges | 226 judged: 182 confirmed, 2 owner, 42 rejected | `outside.json` (confirmed and owner); `raw/outside-audit-judged.json`, `raw/outside-audit-agents.json` |
| Retest of the outside fixes | 14 | One blind newcomer and one expert per page over every changed passage | One revision applied | `outside-retest-passages.json`, `outside-retest-result.json`, `raw/outside-retest-agents.json` |
| Retest of Chapter 1 | 2 | Blind newcomer and expert over the changed paragraphs and figures | One revision applied | `retest/ch1-newcomer.json`, `retest/ch1-expert.json` |

How to read `raw/book-audit-judged.json`: a list of `{chapter, judged: [{lens, items: [{n, id, kind, severity, quote, problem, fix, ...}], verdicts: [{n, verdict, reason, fix}]}]}`; match items to verdicts by `n` within the same lens. Lenses: newcomer, facts, craft, figures, consistency (consistency entries live under `part-1` to `part-5`). A rejected finding has its rejection reason; do not re-raise it unless you have new evidence.

## Where it stands

| Branch | Holds |
|---|---|
| `main` | The live site (Cloudflare Pages deploys every push to `main`). Since 2026-10-17 it carries the outside-the-chapters fixes and Chapter 1, deployed at the owner's word. Later chapters go live only when the owner says so. |
| `pre-read-audit` | All finished audit work: outside-the-chapters fixes (6a5f607), Chapter 1 (dc2ebbd), this handoff. |
| `pre-read-audit-ch2-wip` | Chapter 2 round-1 edits and `decisions/ch2.md`, unfinished: NOT retested, NOT gated, NOT checked. The run lost its connection during Chapter 2's retest. |

Done: outside the chapters (all five parts, cover, account page, glossary, cross-references) and Chapter 1. Everything else is open.

## What is left, in order

1. **Chapter 2**: merge `pre-read-audit-ch2-wip` into your working branch (or cherry-pick its one commit), read `decisions/ch2.md`, check the edits against `round1/ch2.json` and part-1.json items 12, 13, 16, 17, 25, finish any undecided ones, then the blind retest, one revision, all checks, commit "Pre-read audit: Chapter 2".
2. **Chapter 3** (`round1/ch3.json`, 69, plus part-1.json items 1, 5, 6, 19, 23, 24, 26; Figs 3.7 to 3.11 are kept originals: their findings are owner calls).
3. **The Bridge** (`round1/chBridge.json`, 52, plus the remaining part-1.json items; Fig BR.3 is a kept original).
4. **Part II**: ch4 (73), ch5 (44), ch6 (55), ch7 (55), plus `part-2.json` (23).
5. **Part III**: ch8 (64), ch9 (52), ch10 (70), ch11 (87), ch12 (88), plus `part-3.json` (29).
6. **Part IV**: ch13 (60), ch14 (75), ch15 (67), plus `part-4.json` (27). Serif-on-cream is Part IV's identity, not a defect.
7. **Part V**: ch16 (47), ch17 (82), ch18 (49), plus `part-5.json` (22).
8. **Close**: owner calls collected (`owner-calls.md`), ledger `UNDER.md` §4ae, STATE.md freeze line, `docs/todo.md` "Pre-read audit" ticked, owner read map refreshed (`docs/owner-read-map.md`), tag v1.0-rc2.

## Method per chapter (working laws, `docs/working-laws.md`)

1. Read the chapter's findings file and the whole chapter in `public/part-N.html`.
2. Decide each finding as the author: apply in your own wording (the judge's fix is a suggestion), adjust, or reject with a one-line reason. Findings can be wrong: verify facts against primary sources and against the book's own text elsewhere. "Already at bar, left as-is" is a valid verdict; never manufacture change. Record every decision in `decisions/<chapter>.md` (see `decisions/ch1.md` for the form).
3. Write every edit yourself: one author writes, agents only test. Tools: `tools/el.py <page> <id>` prints an element's source; `tools/apply.py` does exact-once replacements. Keep the figure generators in `scripts/figs/*.py` in step for text changes where the string exists (the page is the source of truth).
4. Blind retest: one newcomer and one expert reader (Sonnet), given only the changed passages, screenshots of changed figures and the page, never your reasons. Save to `retest/<chapter>-newcomer.json` and `-expert.json`. Apply one revision.
5. Checks: `npm run build:glossary`; `npm run build:sections` (restore sections.json if only its timestamp moved); `npm run check:dashes` (must be clean); anchor ids unchanged (new paragraphs take the next unused number; never renumber; aliases only through `ANCHOR_ALIASES` in `public/book.js`); bump `?v=` on any CSS or JS change; Gate 1 on every changed figure (`cd tests/pass28 && node figs.mjs --kind=figs --part=part-N --fig=<ids> --fullscreen`, and again with `--motion`), layout (`node clip.mjs --pages=part-N`), `sh tests/pass25/run-all.sh`. These need Playwright with Chromium and WebKit (`npm i --no-save playwright && npx playwright install --with-deps chromium webkit`). If browsers cannot run, write "Gate 1 pending: <ids>" for that chapter in RESUME.md; never skip silently.
6. One commit per chapter, push to `pre-read-audit`, update RESUME.md.

## Rules that are never broken

- The four laws (CLAUDE.md): no em dashes anywhere (the en dash only for ranges and name pairs); every paragraph does a job; the picture carries it (labels at least 11 CSS px at 375 px, captions at most two sentences that name the picture, motion respects reduced motion); teach at the right depth (`docs/pass-29-language-law.md`).
- No AI-style prose: clipped dramatic fragments, "Not X. Y." reveals, reflexive triplets, aphorism closers, announcing sentences.
- `UNDER.md` §4g is law: a corrected error must never come back. §5 lists known non-defects.
- Never edit: the thesis set, the authorship line ("one person's study journal, built out with claude"), owner epigraphs and pull-quotes, the colophon, Ch18's closing note, Fig 18.6's caption, and the 18 kept-original figures (fig-3-7, 3-8, 3-9, 3-10, 3-11, fig-br-3, 10-10, 10-11, 11-7, 12-9, 12-10, 13-10, 15-2, 15-3, 15-4, 15-6, 15-8, 15-9). The §4w arc devices (the six-pattern unification, the four disciplines, the part micro-arcs, the "What you now understand" codas) stay whole: fix a false fact inside one minimally, never cut one. Findings that need any of these, and every "owner" verdict, go to `owner-calls.md`.
- Never ask the owner what to do next; do the agreed next step.
- Never commit `.claude/`, `.kilo/`, `shots4/` or `node_modules/`.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Pending notes

- Duplicate SVG title ids: svgt-part1-30 (Ch3 hero and Fig 3.2), -39 and -40 (Figs 3.9 and 3.10, kept originals, against BR.1 and BR.2): fix with Ch3 and the Bridge (renaming an id inside a kept original is markup, not drawing).
- Owner calls so far: `owner-calls.md` (the privacy notice's EU wording, plus Chapter 1's).
