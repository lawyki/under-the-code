# Pass 31 · gate calibration (gate builder's record)

Brief: `docs/pass-31-brief.md` sections 6, 7 (gate builder track), 10, 11, 15. Status: **development set done, not frozen.**
The freeze (judge prompt hash final, recorded here) and the sealed validation (section 10) come later and are not part of this record.

The gate builder never saw the sealed material: commit 93aae05 (Fig 1.1 v3) was not checked out, shown, diffed or rendered, and nothing under `docs/pass-31-sealed/` was read. The only Fig 1.1 versions used are the three below.

## 1. Tooling

| Command | File | What it does |
|---|---|---|
| (library) | `scripts/figs/figlib.py` | `text(role="label"\|"object")` writes `data-role`; `obj()` wraps glyphs with their shape in `<g data-obj="1">`; `Timeline` exports its beat times. Byte-neutral for untagged scripts (verified 2026-10-24, section 5). |
| `python3 scripts/figs/build_into.py <public dir> <script.py>...` | `scripts/figs/build_into.py` | Runs figure scripts against any `public/` tree (redirects every `open()` under the main checkout's `public/`), one process per script. |
| `node tests/pass30/bare.mjs ... --no-text` | `tests/pass30/bare.mjs` | The SVG alone at a SMIL time; `--no-text` removes every `<text>` first. |
| `npm run fig:sheet` | `tests/pass31/sheet.mjs` | Contact sheets per chapter, 375 px, t=0, Fig 1.1 v4 and Fig 1.2 Enigma pinned. |
| `npm run fig:check -- <part>` | `tests/pass31/check.mjs` | Mechanical checks: Gate 1 (Pass 28 tools), label cap, 11 px floor, taught-yet, t=0 empty band, `<desc>`, caption, strip, dashes, anchors. |
| `npm run fig:gate -- <id> --intent=... --job=...` | `tests/pass31/gate.mjs`, `tests/pass31/prompts.mjs` | The gate (section 2). |
| `npm run fig:dev -- [--runs=3] [--label=...]` | `tests/pass31/dev.mjs` | The development set: builds v1, v2, v4 into scratch trees and runs the gate on each, three times. |

Outputs (renders, packets, every tester reply, verdicts) go to `tests/pass31/out/` (gitignored).

## 2. The gate

`npm run fig:gate -- <fig-id> --intent="<intent sentence>" --job="function|real thing|two-part" [--tree=<public dir>] [--rc2-tree=<dir> | --rc2-rev=v1.0-rc2 | --no-pairwise] [--order=random|cand-first|rc2-first] [--criteria=...] [--author]`

- **Renders** (bare.mjs, Chromium, 375 px, dsf 2): 12 frames at k/12 of the cycle, k = 0..11 (frame 1 is the t=0 still, the reduced-motion view); the same 12 frames with `--no-text`; for pairwise, the rc2 version's 12 frames. The rc2 version defaults to the `v1.0-rc2` tag's part page with this tree's assets.
- **Judge packet**: the book's prose up to the figure (every earlier part whole, then this part up to the card), with every figure card (label, picture, caption, strip), every other `<svg>`, scripts, styles and navigation removed. The figure's caption, strip, `<title>`, `<desc>` and intent are never in it.
- **Testers**: each is a fresh headless session, `claude -p --model claude-sonnet-5-5 --safe-mode --restricted --tools "" --strict-mcp-config --no-session-persistence`, run in an empty sandbox directory, with stream-json input holding only its prompt and images. Unreadable replies are retried up to three times.
- **Criteria** (the verdict names the first failed one in this order):
  1. `taught` (mechanical): every `<text>` token is a number or sign, a term `known-terms.mjs` lists before the section (or the section teaches before the card), or an everyday word (`lib.mjs taughtYet`, brief section 15).
  2. `judge`: (a) the judge describes the 12 frames; (b) the scorer compares that description with the intent for the job.
  3. `hedge`: (c) a separate checker reads the judge's description for hedges on what changes, why, or the result.
  4. `still`: (d) the t=0 still alone, described and scored.
  5. `stripped`: (e) the text-stripped strip, described and scored for what moves and what causes what.
  6. `pairwise`: (f) candidate against rc2, both orders in every run, the first order random unless `--order` is given. It fails only when rc2 is judged better in both orders. Byte-identical frames skip the call (SAME).
- **Verdict**: `<out>/verdict.json` (every reply) and one JSON line on stdout: `{"id","pass","failed","failed_all"}`. With `--author` the line is `{"id","pass","failed"}` only (brief section 6: the author learns pass or fail and the criterion name).

## 3. Intent used for Fig 1.1

From `docs/pass-30-figures.md`, row `fig-1-1`, job **function**:

> A Turing machine's head reads one tape cell at a time and follows two rules: on a mark, move right; on an empty cell, write a mark and stop. Starting from three tally marks it walks past them and writes a fourth, so these two rules alone compute 3 + 1 = 4.

## 4. Development set

| Version | Commit | Owner verdict (brief section 4) | Expected |
|---|---|---|---|
| v1 | `4392ca0` | rejected: binary, jargon | FAIL |
| v2 | `c18836c` | rejected: unexplained state labels | FAIL |
| v4 | `2a9ece9` | approved (the current figure; also the `v1.0-rc2` figure: same script blob `b89c298`) | PASS |

Each version is built by `dev.mjs`: a copy of this worktree's `public/`, then that commit's own `fig_1_1.py` and `figlib.py` run through `build_into.py`. The v4 build differs from the deployed v4 card only in two outline rects (the deployed page carries a later hand smoothing fix); the pairwise test therefore compares built v4 with deployed v4 and answers SAME or CANDIDATE, never RC2.

The rc2 version for pairwise is the `v1.0-rc2` tag (Fig 1.1 there is v4), so v1 and v2 are compared against the approved figure.

## 5. Verification of the committed pieces (2026-10-24)

- **figlib regression.** All 204 `scripts/figs/fig_*.py` run through `build_into.py` into this worktree's `public/`: 203 build, `fig_18_6.py` stops on its own caption assertion (pre-existing). `git diff --stat public/` is **not** empty (parts 1 to 5, about 4,000 lines), but the same scripts run with the figlib of `figures-final` (before 7a74c35) produce byte-identical output for all five parts. So the figlib change is byte-neutral; the diff is pre-existing drift between the scripts and the committed pages (hand fixes applied to the HTML after the scripts, for example the outline rects of Fig 1.1). `public/` restored afterwards; the main checkout's `public/` was checked unchanged (md5 of its HTML before and after).
- **`npm run fig:sheet`**: 19 of 19 sheets written; ch1 sheet inspected (v4 and Enigma pinned, 15 figures).
- **`npm run fig:check -- part-1`** (gate1 full, 41 min): runs to the end. 1 of 47 figures clean (Fig 1.1 v4); Fig 1.2 Enigma fails only `cap` (its key and lamp letters are untagged, so they count as labels until tagged `object`, and `at_bar` is still empty). Part checks: dashes clean, anchors 283 of 283, clip and smooth clean; Gate 1 figs 60 of 1,128 and figs-motion 144 of 4,224 failing rows (the Pass 30 findings). The security chapters' rows were not opened.

## 6. Prompt attempts (tuned on v1, v2, v4 only)

| Attempt | Prompt hash (sha256 of prompts.mjs) | Change before the run | Result |
|---|---|---|---|
| try0 | `06f7a5e0...` | the previous builder's prompts, unchanged | 1 run each: v1 FAIL, v2 FAIL, v4 FAIL on `hedge` (three "unsure" side doubts: the loop restart, card timing, where the head rests) |
| try1 | `cf151473...` | judge and still: "unsure" limited to the main idea, side details (timing, loop restart, layout, colours, resting place) named as out; "unexplained" reworded to words whose meaning had to be guessed; hedge checker: side details named as not counting | 8 of 9: v4 run 1 FAIL on `judge` ("carried by the picture": the result line "3 + 1 = 4" read as text-only) and `hedge` ("where the + 1 sits") |
| try2 | `21f1b713...` | scorer test 3: a short result line stating what the drawn change amounts to is the bar's "result stated", not a fail; new scorer test 5 "few words" (more than 8 text pieces in one panel fails), from the bar in brief section 4 and law 3; hedge: a doubt counts only when it leaves the main idea open or contradicts it | 8 of 9: v4 run 1 FAIL on `judge` ("one scene, shown once": the judge called the result line a repeat of the strokes) |
| try3 | `a0f294c1...` | judge "repeated" and scorer test 4: a label or a short result line is not a repeat; a rules table or a replay is | 8 of 9: v4 run 2 FAIL on `hedge` ("whether the stop is shown or only implied", counted although "result" states the stop) |
| try4 | `34003118...` (current) | hedge checker rewritten as two steps: first the plain statements of changes, cause, result; then each candidate hedge marked counts / does not count (doubts about how something is shown, or what a number stands for beyond a plainly stated result, do not count) | **9 of 9** |
| try5-repeat | `34003118...` (unchanged) | none: a repeat of try4 to see it hold | **9 of 9** |

Full hashes: try0 `06f7a5e0114173fdf23f8e3c49c40d0ea211e11d796076d75bf9bbe8ca82bf03`, try1 `cf1514737285ad78ff4bc37ee562ccf0e01e296ec2b93ddb2b0e94426376ad69`, try2 `21f1b713e9801ef08c0a16c7c9b96a43ea90893cad4f5b06dcab29c399947e40`, try3 `a0f294c18345d3fc46ff23a95ddbdc47d83c93f7de47ebf47a69a152030fe211`, try4 and try5 `34003118f82c53f72d68946d1b000b580f7f6490d8f9c46ede31fdc338a6c7d8` (the prompts.mjs committed with this file; not frozen).

## 7. Every development run (try1 to try5; try0 is in section 6)

Order: the first pairwise order of the run (both orders are asked in every run). Pairwise: each reply's verdict in the order asked.

| Attempt | Version | Run | Order | Expected | Got | Failed criteria | Pairwise |
|---|---|---|---|---|---|---|---|
| try1 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try1 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try1 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try1 | v2 | 1 | cand-first | FAIL | FAIL | judge, hedge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try1 | v2 | 2 | rc2-first | FAIL | FAIL | judge, hedge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try1 | v2 | 3 | random | FAIL | FAIL | judge, hedge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try1 | v4 | 1 | cand-first | PASS | FAIL | judge, hedge | candidate A: SAME; rc2 A: CANDIDATE |
| try1 | v4 | 2 | rc2-first | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: SAME |
| try1 | v4 | 3 | random | PASS | PASS | none | candidate A: SAME; rc2 A: CANDIDATE |
| try2 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try2 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try2 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try2 | v2 | 1 | cand-first | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try2 | v2 | 2 | rc2-first | FAIL | FAIL | judge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try2 | v2 | 3 | random | FAIL | FAIL | judge, hedge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try2 | v4 | 1 | cand-first | PASS | FAIL | judge | candidate A: SAME; rc2 A: CANDIDATE |
| try2 | v4 | 2 | rc2-first | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: CANDIDATE |
| try2 | v4 | 3 | random | PASS | PASS | none | candidate A: CANDIDATE; rc2 A: CANDIDATE |
| try3 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try3 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try3 | v1 | 3 | random | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try3 | v2 | 1 | cand-first | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try3 | v2 | 2 | rc2-first | FAIL | FAIL | judge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try3 | v2 | 3 | random | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try3 | v4 | 1 | cand-first | PASS | PASS | none | candidate A: SAME; rc2 A: CANDIDATE |
| try3 | v4 | 2 | rc2-first | PASS | FAIL | hedge | rc2 A: CANDIDATE; candidate A: SAME |
| try3 | v4 | 3 | random | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: SAME |
| try4 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try4 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try4 | v1 | 3 | random | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try4 | v2 | 1 | cand-first | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try4 | v2 | 2 | rc2-first | FAIL | FAIL | judge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try4 | v2 | 3 | random | FAIL | FAIL | judge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try4 | v4 | 1 | cand-first | PASS | PASS | none | candidate A: SAME; rc2 A: CANDIDATE |
| try4 | v4 | 2 | rc2-first | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: CANDIDATE |
| try4 | v4 | 3 | random | PASS | PASS | none | candidate A: SAME; rc2 A: CANDIDATE |
| try5-repeat | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | candidate A: RC2; rc2 A: RC2 |
| try5-repeat | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try5-repeat | v1 | 3 | random | FAIL | FAIL | taught, judge, still, stripped, pairwise | rc2 A: RC2; candidate A: RC2 |
| try5-repeat | v2 | 1 | cand-first | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try5-repeat | v2 | 2 | rc2-first | FAIL | FAIL | judge, pairwise | rc2 A: RC2; candidate A: RC2 |
| try5-repeat | v2 | 3 | random | FAIL | FAIL | judge, pairwise | candidate A: RC2; rc2 A: RC2 |
| try5-repeat | v4 | 1 | cand-first | PASS | PASS | none | candidate A: SAME; rc2 A: CANDIDATE |
| try5-repeat | v4 | 2 | rc2-first | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: SAME |
| try5-repeat | v4 | 3 | random | PASS | PASS | none | rc2 A: CANDIDATE; candidate A: SAME |

Failed judge sub-tests in try4 and try5 (12 runs of v1 and v2): v1 always fails `mechanism` (a binary carry machine, not the intent's tally machine), `few words` (10 to 16 text pieces) and `one scene, shown once` (the rules table), often `unexplained` and `carried by the picture`; v1 also fails `taught` (the `_` blank symbol), `still` and `stripped` every time. v2 always fails `one scene, shown once` (the five-row step-by-step replay), sometimes `few words` (13 to 16 pieces); its `mechanism`, `still` and `stripped` pass. Pairwise: rc2 (v4) was judged better than v1 and v2 in all 60 replies.

## 8. Known limits

- **v2 is caught by one sub-test.** Its owner reason (unexplained state labels, "head · adding", "while adding") is not caught by `unexplained` in any run: the judge works the labels out from the rules. v2 fails single-figure criteria only through `one scene, shown once` (its replay). Under validation (no pairwise), a figure with unexplained labels but one clean scene could pass.
- **The hedge check fired on no development figure in try4 and try5.** The dev set has no figure that is right but uncertain, so its strictness is untested; it fired on v1 and v2 in try1 and try2 and falsely on v4 in try0, try1 and try3.
- **"few words" is the scorer's call on the judge's own count** (`text_pieces`), and it is inconsistent across runs for v2 (14 pieces passed twice: the scorer counted per panel). The mechanical label cap lives in `fig:check`, not the gate.
- **The scorer sees the intent**, so `mechanism` fails a figure that teaches a different example (v1's binary counter) even if it were clear. That is the brief's design (the gate tests the intent), but it makes `mechanism` depend on the intent sentence's wording.
- **Small sample.** Six correct runs of the final prompts per version (try4 and try5); the false-fail rate of v4 before try4 was 1 in 3 per attempt, each time a different cause.
- **Model use.** The CLI reports `claude-haiku-5-5` beside `claude-sonnet-5-5` in each session's usage (the CLI's own side calls); the replies are Sonnet 5.5's.
- **Rendering** is Chromium only; WebKit is not used by the gate.
- **Gate 1 run time.** `fig:check -- part-1` with `--gate1=full` runs `figs.mjs --fullscreen` over the whole part and took 41 minutes on 2026-10-24; use `--fig=` or `--gate1=quick` while iterating.

## 9. Full prompt texts (tests/pass31/prompts.mjs, sha256 `34003118f82c53f72d68946d1b000b580f7f6490d8f9c46ede31fdc338a6c7d8`)

Every tester gets `SYSTEM` as its system prompt and one user message. `JUDGE`, `STILL`, `STRIPPED` and `PAIRWISE` are followed by the frames, each preceded by a line `Frame k of 12 (t = ... s of a ... s loop):` (pairwise: `Version A, Frame k ...`). `SCORER` and `HEDGE` get text only.

```js
// Pass 31 gate prompts (tests/pass31/gate.mjs). The full text is reproduced in docs/pass-31-calibration.md, with its
// hash. The author never reads this file (brief section 6: the author learns only pass or fail and the criterion name).
// Every tester is a fresh Sonnet 5.5 session with no tools: it sees only what its message holds.

export const SYSTEM = `You help test the figures of a book about how computers work. You only look and report what you see and understand. You never suggest changes, never advise, never vote on anything but the question asked. Answer with exactly one JSON object and nothing else.`;

const BOOK = packet => `THE BOOK SO FAR (everything you have read before the figure; figures that came earlier are left out):
<<<
${packet}
>>>`;

// (a) the judge: 12 frames, the prose up to the figure
export const JUDGE = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure: an animated picture, shown as 12 frames captured at equal steps through one loop of its animation. Frame 1 is the start of the loop; after frame 12 the loop starts again at frame 1. The figure has no caption and no explanation: you have only the picture and the text you have read.

Describe what the figure shows and teaches, from the frames and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The 12 frames follow. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words: the things in the picture and where they are",
 "panels": ["one entry per separate picture inside the figure, saying what it is. A key, a rule card, a label or a result line that belongs to a scene is part of that scene. A separate panel is its own picture: a second scene, a table, a list of steps, a replay of steps, a timeline, a block of text"],
 "changes": "what changes from frame to frame, in order",
 "cause": "what makes each change happen, as the picture shows it",
 "result": "where it ends up: the result the figure arrives at",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never shows it happening or drawn; \\"none\\" if none",
 "repeated": "anything the figure shows twice in different forms, for example a scene and also a step-by-step replay of the same steps, or the same rules written out again as a table. A label naming a drawn thing, or a short result line saying what the scene arrives at, is not a repeat; \\"none\\" if none",
 "unexplained": ["each word, label, symbol, number or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave out anything the picture or the text makes plain; leave the list empty if there is none"],
 "unsure": ["each doubt you still have, after looking at every frame, about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (the exact timing of the animation, the loop starting again, layout, colours, where something rests at the end). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (d) the t=0-only judge: the reduced-motion still
export const STILL = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as a reader who has turned animation off sees it: one still picture that does not move. The figure has no caption and no explanation: you have only this picture and the text you have read.

Describe what the figure shows and teaches, from the still and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The still follows. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words",
 "panels": ["one entry per separate picture inside the figure (a key, rule card, label or result line belongs to its scene)"],
 "changes": "what the still shows changing, happening or having happened: the process it depicts",
 "cause": "what makes it happen, as the picture shows it",
 "result": "the result the figure shows or states",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "unexplained": ["each word, label, symbol, number or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave out anything the picture or the text makes plain; leave the list empty if there is none"],
 "unsure": ["each doubt you still have about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (layout, colours, where something rests). Leave the list empty if you have none"]
}`;

// (e) the text-stripped judge: the same 12 frames with every <text> removed
export const STRIPPED = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as 12 frames captured at equal steps through one loop of its animation (frame 1 is the start; after frame 12 it starts again). Every word, letter and number has been removed from the picture: only shapes, marks, colours and their motion are left. There is no caption.

Say what the picture shows by its shapes and motion alone, using the text you have read only to name things. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The 12 frames follow. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn: the shapes and what they seem to stand for",
 "moves": "what moves or changes, frame by frame",
 "cause": "what causes what: which thing acts, and what happens to which other thing as a result",
 "result": "where it ends up",
 "unsure": ["each doubt you still have about what moves, what causes what, or the result after looking at every frame. Leave out doubts you resolved; leave the list empty if you have none"]
}`;

// (b) the scorer: the judge's description against the intent sentence, for the figure's job
const JOBS = {
  'function': `The figure's job is "function": it shows how something works. The bar for this job (the book owner's approved reference) is one calm scene, the core function, few labels, motion that is the mechanism, and the result stated.`,
  'real thing': `The figure's job is "real thing": it shows a real object or machine as it really is, so the reader sees the real thing and what happens inside it. For this job the description must recognise the object the intent names and see in it what the intent says happens.`,
  'two-part': `The figure's job is "two-part": one panel shows the real thing and the other shows its function, in one figure. Two panels are expected; each must do its job.`,
};
const RUBRIC = {
  judge: job => `Score the description against the intent. PASS only if every test below passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: the same thing changes, for the same cause, with the same result. Paraphrase is fine and extra correct detail is fine. It fails if what changes, why, or the result is missing, vague or wrong, or if the description gives a different mechanism, a different representation or a different example than the intent names.
2. unexplained: nothing listed in "unexplained" shows that the reader could not get what changes, why, or the result. An item the description itself resolves elsewhere (in "changes", "cause" or "result"), or one about decoration or a side detail, does not count.
${job === 'real thing' ? `3. object: the description recognises the real object or scene the intent names, drawn as itself (not as boxes and labels standing for it).` : `3. carried by the picture: the mechanism is shown happening or drawn, not only written. It fails if "read_only" names a part of the mechanism (what changes, why, or the result) that the picture never shows. A short result line that states what the drawn change amounts to (for example a sum) is part of this bar ("the result stated") and does not fail the test, as long as the change it sums up is shown happening.
5. few words: the picture uses few words. It fails if "text_pieces" is more than 8 for one panel, or if the words, not the picture, carry the mechanism.
4. one scene, shown once: ${job === 'two-part' ? 'at most two panels, and' : 'one panel only (the scene, with its own rule cards, keys and result line), and'} "repeated" is "none". It fails if the figure adds a separate table, list of steps, replay or block of text beside the scene, or shows the same steps twice. A short result line that states what the scene arrives at is not a repeat, even when "repeated" names it.`}`,
  still: () => `This description comes from the still alone, the frame a reader with animation turned off sees. A still cannot move, so the change may be shown by drawn states, arrows, a before and after, drawn rules, or a stated result, and the reader may have to work the motion out. Score it against the intent: a reader who works out, from what is drawn, the same change, cause and result as the intent passes, even when the reader says the change is implied rather than seen. PASS only if both tests pass; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: what changes, why, and the result, as the intent says. Paraphrase is fine. It fails if any of the three is missing, vague or wrong, or a different mechanism is given.
2. unexplained: nothing listed in "unexplained" shows that the reader could not get what changes, why, or the result. An item the description itself resolves elsewhere, or one about a side detail, does not count.`,
  stripped: () => `This description comes from the 12 frames with every word, letter and number removed: only shapes and motion were left. Score whether the picture still shows what moves and what causes what, as the intent says. Words and numbers are not expected. PASS only if both tests pass; otherwise FAIL.
1. what moves: the description names the thing that moves or changes and how, consistent with the intent.
2. what causes what: the description says which thing acts and what happens because of it, consistent with the intent's cause. It fails if the description can say only that things move, appear or light up, without what causes what, or if it gives a different mechanism.`,
};
export const SCORER = ({ kind, job, intent, description }) => `You score one blind reader's description of a figure in a book about how computers work. The reader saw the figure (and the book's text before it) but never saw the figure's intended message, which only you see.

${JOBS[job]}

THE INTENT (what the figure must get across):
"${intent}"

THE READER'S DESCRIPTION (JSON):
${JSON.stringify(description, null, 1)}

${RUBRIC[kind](job)}

Answer with one JSON object, nothing else:
{"tests": {"<test name>": {"pass": true, "why": "one sentence"}}, "verdict": "PASS or FAIL"}`;

// (c) the hedge check: the judge's description, read for hedges on what changes, why, or the result
export const HEDGE = description => `Below is a blind reader's description of an animated figure. Decide whether the reader hedges on the figure's main idea: what changes, what makes it change, or the result.

Work in two steps.
Step 1. Write down what the description states as plain fact about each of the three: "changes", "cause" and "result". If one of them is missing, vague, or itself hedged, that is a hedge.
Step 2. List every candidate hedge: each entry in "unsure"; each word such as "seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "unclear", "not sure", "could be"; each pair of alternatives ("either ... or", "whether ... or"); each question. For each candidate decide whether it counts:
- It COUNTS when it leaves open which thing changes, what makes it change, or what the result is, or when it offers an alternative that contradicts what step 1 found.
- It does NOT count when step 1 already states that point plainly and the candidate does not contradict it: a doubt about how the figure shows something (shown or only implied, drawn or written), about what a number or a line in the picture stands for beyond the stated result, or about what else the figure might mean.
- It does NOT count when it is about a side detail: colours, decoration, layout, the exact timing of the animation, the loop starting again, where something rests at the end.

THE DESCRIPTION (JSON):
${JSON.stringify(description, null, 1)}

Answer with one JSON object, nothing else:
{"stated": {"changes": "...", "cause": "...", "result": "..."}, "candidates": [{"quote": "the hedged words", "about": "what changes | why | result | side detail", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what changes | why | result"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;

// (f) the pairwise comparison: two versions for the same place, order given by the caller
export const PAIRWISE = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. Two different versions of that figure were made for this place, A and B. Each is shown as 12 frames captured at equal steps through one loop of its animation (frame 1 is the start). Neither has a caption.

Which version would a newcomer who has read only this text understand faster and more surely? Judge by the book's rules for figures: the picture carries the idea (it shows the mechanism, it does not hold a column of text); as few words as the idea allows; motion where motion is the mechanism; nothing a newcomer cannot yet read; everything shown once. Answer "SAME" if the differences would not change how quickly or surely a newcomer gets the idea.

${BOOK(packet)}

Version A's 12 frames come first, then version B's 12 frames. Then answer with one JSON object, nothing else:
{"better": "A or B or SAME", "why": "two sentences at most, naming the concrete difference"}`;
```

## 10. Not done yet

- Freeze: the judge prompt hash is not final; the freeze happens after review, before the sealed validation run.
- Validation (section 10 of the brief) is not run by the gate builder beyond counts.
