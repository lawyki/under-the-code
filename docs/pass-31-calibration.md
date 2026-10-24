# Pass 31 · gate calibration (gate builder's record)

Brief: `docs/pass-31-brief.md` sections 3, 4, 6, 7 (gate builder track), 10, 11, 15. Status: **not frozen.** The gate was frozen on 2026-10-24 at `dd51d25` (section 11, combined fingerprint `3294111df0b4b9b81033d65b2424affad874452574d0894bd76076d31526185d`), reopened the same day before any validation for session e2's follow-up (section 13: taught-yet repairs, the takeaway read from the ledger by header, Enigma as a must-pass), and **not re-frozen**: the three prompt revisions the follow-up allowed were used without v4 and Enigma passing three of three (section 13.4). The configuration in the repo is the last one tried (try25, combined `9ba0dfc0709a7f4cb8d8ea4f618e5b976ecd8eea474fbb147729e3a43b4f6a87`). Total prompt attempts: **26** (try0 to try25, section 13.6). The sealed validation (brief section 10) is not part of this record: it runs later with `npm run fig:validate` and reports counts only.

The gate builder never saw the sealed material: commit 93aae05 (Fig 1.1 v3) was not checked out, shown, diffed or rendered, and nothing under `docs/pass-31-sealed/` was read or written. The validation runner was tested only on a scratch manifest in the builder's scratch directory, with v1, v4 and a decoy as stand-ins. The only Fig 1.1 versions used are v1, v2 and v4 below, plus decoys built from v4. No figure from the book's security chapters was opened.

## 1. Tooling

| Command | File | What it does |
|---|---|---|
| (library) | `scripts/figs/figlib.py` | `text(role="label"\|"object"\|"legend")` writes `data-role`; `obj()` wraps glyphs with their shape in `<g data-obj="1">`; `Timeline` exports its beat times. Byte-neutral for untagged scripts (section 5). `legend` added 2026-10-24 (review item 6). |
| `python3 scripts/figs/build_into.py <public dir> <script.py>...` | `scripts/figs/build_into.py` | Runs figure scripts against any `public/` tree (redirects every `open()` under the main checkout's `public/`), one process per script. |
| `node tests/pass30/bare.mjs ... --no-text` | `tests/pass30/bare.mjs` | The SVG alone at a SMIL time; `--no-text` removes every `<text>` first. |
| `npm run fig:sheet` | `tests/pass31/sheet.mjs` | Contact sheets per chapter, 375 px, t=0, Fig 1.1 v4 and Fig 1.2 Enigma pinned. |
| `npm run fig:check -- <part>` | `tests/pass31/check.mjs` | Mechanical checks per figure: Gate 1 rows attributed to the figure (new), label cap (tightened), legend entries (new), 11 px floor, taught-yet, t=0 empty band, `<desc>`, caption, strip; per part: dashes, anchors, each Gate 1 tool's summary. |
| `npm run fig:gate -- <id> [--ledger=...]` | `tests/pass31/gate.mjs`, `tests/pass31/prompts.mjs`, `tests/pass31/lib.mjs`, `tests/pass31/common-words.txt` | The gate (section 2). The takeaway and job come from the ledger by header name (section 13.1, item 4), or from `--intent` and `--job` for a figure outside it. |
| `npm run fig:dev -- [--runs=3] [--label=...] [--ledger=...]` | `tests/pass31/dev.mjs` | The development set: builds v1, v2, v4, the four decoys and Enigma (section 13.1, items 5 and 6) and runs the gate on each, three times, with the ledger's takeaways. |
| `npm run fig:taught-test` | `tests/pass31/taught.test.mjs` | The taught-yet rules on 19 fixed cases at real figure positions (section 13.1, item 7). |
| `npm run fig:hash` | `tests/pass31/hash.mjs` | The gate's fingerprint: sha256 of each prompt, of each file the gate runs, the model id, and the combined hash; the CLI version beside it. |
| `npm run fig:validate -- --expect-hash=<combined>` | `tests/pass31/validate.mjs` | The sealed validation: runs the frozen gate (no pairwise) on the items of `docs/pass-31-sealed/validation.json`, each scored against the ledger's takeaway (the manifest's intent only where the ledger has none), and prints counts only; everything else stays under `docs/pass-31-sealed/`. |

Outputs (renders, packets, every tester reply, verdicts) go to `tests/pass31/out/` (gitignored); validation outputs go to `docs/pass-31-sealed/` (gitignored).

## 2. The gate

`npm run fig:gate -- <fig-id> [--ledger=<docs/pass-31-ledger.tsv>] | [--intent="<takeaway>" --job="function|real thing|two-part"] [--tree=<public dir>] [--rc2-tree=<dir> | --rc2-rev=v1.0-rc2 | --no-pairwise] [--order=random|cand-first|rc2-first] [--criteria=...] [--expect-hash=<combined>] [--author]`

- **Renders** (bare.mjs, Chromium, 375 px, dsf 2): 12 frames at k/12 of the cycle, k = 0..11 (frame 1 is the t=0 still, the reduced-motion view); the same frames with `--no-text`; for pairwise, the rc2 version's frames. The rc2 version defaults to the `v1.0-rc2` tag's part page with this tree's assets. A figure that does not animate renders one frame: `judge` is then n/a (the still is the whole figure), the still and the one-frame text-stripped still carry the test, and pairwise compares one frame against twelve when needed. A figure missing from rc2 (a merge, a new figure) gets pairwise n/a.
- **Judge packet**: unchanged: the book's prose up to the figure, with every figure card (label, picture, caption, strip), every other `<svg>`, scripts, styles and navigation removed. Caption, strip, `<title>`, `<desc>` and intent are never in it.
- **Testers**: each is a fresh headless session, `claude -p --model claude-sonnet-5-5 --safe-mode --restricted --tools "" --strict-mcp-config --no-session-persistence`, run in a new empty directory under the system temp directory (outside any repo; removed afterwards), with stream-json input holding only its prompt and images. An unreadable reply or a failed spawn is retried (three attempts, 15 s and 30 s apart).
- **Describers** (round 1): the judge (12 frames), the still (t=0), the text-stripped judge, and the two pairwise orders. Each describer names `cause_drawn`, the drawn thing that shows the cause, or "none". The judge and the still list `unexplained_words` (each with its reason) and `unexplained_marks` separately.
- **Checks** (round 2): one scorer per description and one hedge check per description (judge, still, stripped), each asked **three times** in fresh sessions; the majority decides. The description is fixed, so the votes damp only the checker's noise in applying its rules.
- **Criteria** (the verdict names the first failed one in this order):
  1. `taught` (mechanical): every `<text>` token is a number or sign, a term `known-terms.mjs` lists before the section (or the section teaches before the card, or, for an all-capitals abbreviation, the prose paragraph that first uses it comes before the card), an everyday word, or a proper name from the glossary that the prose before the figure already uses (`lib.mjs taughtYet`, brief section 15; the rules as revised in section 13.1).
  2. `judge`: (a) the judge describes the 12 frames; (b) the scorer compares that description with the intent for the job: mechanism (with the cause drawn), unexplained (any unexplained word fails), carried by the picture, one scene shown once, few words.
  3. `hedge`: (c) the hedge check on the judge's, the still's and the text-stripped descriptions, each in its own scope (section 7, item 1). Any of the three failing fails `hedge`.
  4. `still`: (d) the t=0 still alone, described and scored (mechanism with the cause drawn, unexplained, few words).
  5. `stripped`: (e) the text-stripped strip, described and scored for what moves and what causes what, with a drawn cause.
  6. `pairwise`: (f) candidate against rc2, both orders in every run. It fails only when rc2 is judged better in both orders. Byte-identical frames skip the call (SAME).
- **Verdict**: `<out>/verdict.json` (every reply, every vote, the gate's fingerprint) and one JSON line on stdout: `{"id","pass","failed","failed_all"}`; with `--author` only `{"id","pass","failed"}`. Exit 0 pass, 1 fail. A tool failure (render, CLI, unreadable replies after three attempts, a refused `--expect-hash`) gives `failed: "error"` and exit 2, never a criterion name.

## 3. Intent used for Fig 1.1

From try22 on (section 13), the takeaway in the ledger's column `intent`, read by header: "Function: the head walks right past each mark and marks the next blank, so three marks become four." (job **function**). Up to try21, the long intent from `docs/pass-30-figures.md`, row `fig-1-1`, job **function**:

> A Turing machine's head reads one tape cell at a time and follows two rules: on a mark, move right; on an empty cell, write a mark and stop. Starting from three tally marks it walks past them and writes a fourth, so these two rules alone compute 3 + 1 = 4.

## 4. Development set

| Item | Source | Verdict on record | Expected | Pairwise |
|---|---|---|---|---|
| v1 | `4392ca0` | owner: rejected (binary, jargon) | FAIL | against rc2 |
| v2 | `c18836c` | owner: rejected (unexplained state labels) | FAIL | against rc2 |
| v4 | `2a9ece9` | owner: approved (the current figure; also the `v1.0-rc2` figure: same script blob `b89c298`) | PASS | against rc2 |
| decoy1 | v4 tree, svg replaced | constructed: the mechanism written out as six lines of text beside a decorative moving dot (the review's decoy1) | FAIL | none (validation mode) |
| decoy2 | v4 tree, svg replaced | constructed: tape, three marks, a head that slides right and writes a fourth, labels TAPE, HEAD, "3 + 1 = 4", **no rule drawn** (the review's decoy2) | FAIL | none |
| decoy3 | v4 tree, one label changed | constructed: v4 with its head labelled "head · adding" (v2's unexplained state label on an otherwise approved scene) | FAIL | none |
| Enigma | this worktree's `public/`, Fig 1.2 as it stands | owner: praised (the real thing); a must-pass from session e2 on, job **real thing** (added in section 13) | PASS | against rc2 (byte-identical frames: SAME) |
| decoy4 | Enigma tree, svg replaced | constructed: Fig 1.2's takeaway as a block schematic, empty boxes KEY, ROTORS, REFLECTOR, LAMP joined by arrows, a counter and a lamp letter stepping (added in section 13) | FAIL | none |

v1, v2 and v4 are built by `dev.mjs` from a copy of this worktree's `public/` with each commit's own `fig_1_1.py` and `figlib.py` run through `build_into.py`. The built v4 differs from the deployed v4 card only in two outline rects (a later hand smoothing fix); pairwise therefore compares built v4 with deployed v4 and answers SAME or CANDIDATE (one RC2 in one order in try21, never both). The decoys are test fixtures made by `dev.mjs` (never book figures) and run without pairwise, as validation runs, so each must fail on its single-figure criteria alone. The owner never saw the decoys: their expected verdicts follow from the bar (decoy1 and decoy2), from the owner's stated reason for rejecting v2 (decoy3) and from the amended brief's "a schematic is never a real thing" (decoy4).

## 5. Verification

Of the committed pieces before the review (2026-10-24, unchanged):

- **figlib regression.** All 204 `scripts/figs/fig_*.py` run through `build_into.py` into this worktree's `public/`: 203 build, `fig_18_6.py` stops on its own caption assertion (pre-existing). `git diff --stat public/` is **not** empty (parts 1 to 5, about 4,000 lines), but the same scripts run with the figlib of `figures-final` (before 7a74c35) produce byte-identical output for all five parts, so the figlib change is byte-neutral and the diff is pre-existing drift between the scripts and the committed pages (hand fixes applied to the HTML after the scripts). The review confirmed this on 10 random non-security scripts. `public/` restored; the main checkout's `public/` unchanged. The `legend` role added on 2026-10-24 only extends the allowed values, so untagged output is unchanged.
- **`npm run fig:sheet`**: 19 of 19 sheets written; ch1 sheet inspected.
- **`npm run fig:check -- part-1`** (gate1 full, 41 min, before the review's changes): 1 of 47 figures clean (Fig 1.1 v4); Fig 1.2 Enigma fails only `cap`; dashes clean, anchors 283 of 283, clip and smooth clean; Gate 1 figs 60 of 1,128 and figs-motion 144 of 4,224 failing rows.

After the review's fixes (2026-10-24):

- **What a tester session receives.** A probe with the gate's exact flags asked the session to copy every context block it got. Run from inside the repo (the old sandbox), it received a userEmail block and an environment block whose working directory named the repo and the worktree (`.../under-the-code/.claude/worktrees/figures-final-gate/tests/pass31/out/...`) with the worktree notes; no git status, no commit subjects, no CLAUDE.md. Run from a temp directory (the new sandbox), it receives the userEmail block and an environment block with the temp path and "Is a git repository: false", nothing else. So try0 to try5 testers could see the book's repo and worktree names; try6 on could not. The userEmail block cannot be turned off without `--bare` (which needs an API key); it names the owner's address, not the book.
- **Tool errors.** A missing tree, a refused `--expect-hash` and (live, in try18) a CLI self-update mid-run (`spawn ENOENT`, `spawn ENOEXEC`) each gave `{"pass":false,"failed":"error"}` and exit 2; fig:dev counted those runs as ERROR, not FAIL. Spawn failures are now retried.
- **Static figures.** No figure in the development set is static, so the path was smoke-tested on a fixture: v4 with its four SMIL elements removed. Two runs completed without a crash (one frame, judge n/a, hedge on still and stripped, pairwise one frame against twelve).
- **Validation runner.** `fig:validate` on a scratch manifest (v1 as a stand-in v3, v4 built from `2a9ece9` by rev, decoy2 as a stand-in worst, the v4 tree as a stand-in best) printed one line, `HOLDS: v3 failed 1 of 1; v4 passed 1 of 1; tapped worst failed 1 of 1; tapped best passed 1 of 1; tool errors 0`, wrote its verdicts and `counts.json` under the scratch sealed dir and appended to its `reads.log`. With a wrong `--expect-hash` it refused (exit 2).
- **Label cap.** Unit cases: one key in its obj group is free; the review's 16 words in one obj group with a background rect now count 16 labels; object text nested below a non-obj group counts as a label; 20 labels in 20 panels count as 20 in one panel; three tagged legend entries fail the two-entry rule.
- **fig:check after the changes**: `--fig=fig-1-1,fig-1-2 --gate1=quick`: Fig 1.1 PASS (gate1 30 rows clean), Fig 1.2 FAIL on `cap` only (26 labels, untagged), 6 of 6 part checks clean. Chapters 1 and 2 (27 figures) with `--gate1=quick`: 1 of 27 clean (Fig 1.1); the other 26 fail the label cap (untagged text counts as labels, 11 to 70 per figure) and 19 of them also taught-yet (for example EAX, mov, ALU, 0x05); 6 of 6 part checks clean; Gate 1 quick had 0 failing rows (162 still, 648 motion), so the per-figure `gate1` check was exercised only on clean rows. Its failing branch restates figs.mjs's rules but has not met a failing row (the full run's 60 and 144 failing rows were at widths and fullscreen sizes the quick run skips).
- **Taught-yet.** "SHANNON" on Fig 2.2 now passes (the prose before the figure names Shannon); the same token with no prior mention still fails as a glossary term not yet taught. Fig 1.1 v4 clean.

## 6. Attempts before the review (try0 to try5; tuned on v1, v2, v4 only)

These ran the previous gate: one scorer and one hedge call per run, hedge on the judge only, testers in an empty directory inside the repo (so the working-directory path named the repo and worktree, section 5). Kept as the record of what was tried.

| Attempt | Prompt hash (sha256 of prompts.mjs) | Change before the run | Result |
|---|---|---|---|
| try0 | `06f7a5e0...` | the previous builder's prompts, unchanged | 1 run each: v1 FAIL, v2 FAIL, v4 FAIL on `hedge` (three "unsure" side doubts: the loop restart, card timing, where the head rests) |
| try1 | `cf151473...` | judge and still: "unsure" limited to the main idea, side details (timing, loop restart, layout, colours, resting place) named as out; "unexplained" reworded to words whose meaning had to be guessed; hedge checker: side details named as not counting | 8 of 9: v4 run 1 FAIL on `judge` ("carried by the picture": the result line "3 + 1 = 4" read as text-only) and `hedge` ("where the + 1 sits") |
| try2 | `21f1b713...` | scorer test 3: a short result line stating what the drawn change amounts to is the bar's "result stated", not a fail; new scorer test 5 "few words" (more than 8 text pieces in one panel fails), from the bar in brief section 4 and law 3; hedge: a doubt counts only when it leaves the main idea open or contradicts it | 8 of 9: v4 run 1 FAIL on `judge` ("one scene, shown once": the judge called the result line a repeat of the strokes) |
| try3 | `a0f294c1...` | judge "repeated" and scorer test 4: a label or a short result line is not a repeat; a rules table or a replay is | 8 of 9: v4 run 2 FAIL on `hedge` ("whether the stop is shown or only implied", counted although "result" states the stop) |
| try4 | `34003118...` | hedge checker rewritten as two steps: first the plain statements of changes, cause, result; then each candidate hedge marked counts / does not count (doubts about how something is shown, or what a number stands for beyond a plainly stated result, do not count) | **9 of 9** |
| try5-repeat | `34003118...` (unchanged) | none: a repeat of try4 to see it hold | **9 of 9** |

Full hashes: try0 `06f7a5e0114173fdf23f8e3c49c40d0ea211e11d796076d75bf9bbe8ca82bf03`, try1 `cf1514737285ad78ff4bc37ee562ccf0e01e296ec2b93ddb2b0e94426376ad69`, try2 `21f1b713e9801ef08c0a16c7c9b96a43ea90893cad4f5b06dcab29c399947e40`, try3 `a0f294c18345d3fc46ff23a95ddbdc47d83c93f7de47ebf47a69a152030fe211`, try4 and try5 `34003118f82c53f72d68946d1b000b580f7f6490d8f9c46ede31fdc338a6c7d8` (the prompts.mjs of commit 7ea7f76).

### Every run, try1 to try5 (try0 is in the table above)

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

## 7. The review (2026-10-24) and what was done

The independent review found the gate not ready to freeze. Each item, and what was done:

1. **The hedge criterion never fired and waved through hedges on the cause and the result.** *Fixed in part, rejected in part.* The hedge check now runs on all three descriptions (judge, still, text-stripped), each in its own scope, and reads only the fields about the mechanism (`changes`/`moves`, `cause`, `cause_drawn`, `result`, `teaches`, `unsure`; `unexplained_*` belong to the scorer). For the 12-frame judge the old carve-outs "how it is shown (shown or only implied)" and "what else the figure might mean" are gone. The review's "no carve-outs beyond colours, layout and loop restart" was run as try6: v4, the approved figure, failed all three runs on hedges ("whether 3 + 1 = 4 states the task or the result", "where the + 1 is on the tape", and on the still and the stripped strip doubts no still and no wordless picture can avoid). Kept, each for a stated reason:
   - the **meaning** of the end state (that marks stand for a number, whether a written sum is the task or the answer, which mark is the "+ 1") does not count as a hedge; the scorer's mechanism test scores the meaning, so it is not counted twice;
   - a doubt that **names the drawn thing that shows the point** and asks only whether it is meant that way does not count ("the head stays put with the stop card lit, but does it truly stop?"); holding still under a lit rule is a drawn stop. A doubt where nothing drawn shows the point still counts: that is the decoy2 case ("nothing shows what makes the head stop", "the rules are never drawn");
   - a doubt only whether there is **more than is drawn** (a hidden state) does not count while the drawn cause is stated plainly;
   - timing (a pause, a frame where nothing is lit, a frame caught between two positions, the order inside a step), colours, layout and the loop restart do not count;
   - **still**: doubts about what happens over time, what a rule's action produces, how the drawn rules are chosen step by step, whether the end state is reached, or whether the still shows the start or the end do not count (a still cannot move; the still's scorer tests whether the reader worked them out); a doubt about which drawn thing is the cause, or whether it is drawn at all, counts;
   - **text-stripped**: a narrow positive check; it counts only a doubt about which thing moves, or that nothing drawn shows why things move (no drawn cause named, or `cause_drawn` "none"). Doubts about which action a wordless rule stands for, or whether the drawn cause causes or only accompanies the change, do not count: the words that named the actions were removed, and the stripped scorer tests the drawn cause.
   With the frozen prompts the hedge fires: in try20 and try21 it failed v1 6 of 6, decoy1 6 of 6, decoy2 6 of 6, decoy3 4 of 6, v2 1 of 6, and v4 1 of 6 (a false fail, section 9).
2. **A figure with no cause drawn passed.** *Fixed.* Judge, still and stripped describers name `cause_drawn` (the drawn thing that acts, lights up, matches or points; "none" if the cause is only words, only from the text, or absent). The scorer fails `mechanism` when `cause_drawn` is "none", empty or only words, when `read_only`, `unsure` or `cause_drawn` say the rules, cause or result are not drawn, or when the cause comes only from the text or a guess; "carried by the picture" now needs the cause drawn ("things moving is not enough"); the stripped scorer needs a drawn shape that shows the cause. In try20 and try21 decoy2 failed judge `mechanism` 6 of 6, still `mechanism` 6 of 6 and stripped "what causes what" 4 of 6.
3. **Static figures crashed the gate.** *Fixed, one difference.* One frame: `judge` n/a, still, hedge (on still and stripped), taught and pairwise run; pairwise handles one frame on either side; a figure absent from rc2 gets pairwise n/a. The review proposed `stripped` n/a too; it runs instead on the one-frame text-stripped still (`STRIPPED(packet, 1)`), because a static figure whose cause lives only in its words would otherwise skip the text-stripped test. Untested on a real static figure (section 10).
4. **Tester sessions may carry repository context.** *Fixed and confirmed.* Testers run in `fs.mkdtempSync(os.tmpdir() + '/p31-tester-')`, removed after the run. What a session receives, before and after, is in section 5.
5. **Tool errors reported as figure failures.** *Fixed.* `failed: "error"`, exit 2, for render failures, CLI spawn failures, unreadable replies after three attempts and uncaught exceptions; retries back off 15 s and 30 s. Seen working live in try18.
6. **The label cap could be sidestepped.** *Fixed.* Object text is free only as a direct child of its `obj()` group with a shape (or a group holding a shape) as a direct sibling, at most two object texts per group (a group with more counts all of them as labels) and at most 6 characters; more than two `data-panel` groups count as one panel; `text(role="legend")` entries count as labels and at most two per panel. The two-entry legend rule applies only to tagged legends (untagged legend text still counts against the label cap).
7. **fig:check ignored Gate 1 failures per figure.** *Fixed.* A per-figure `gate1` check attributes the figure's own `figs.json` and `figs-motion.json` rows (overlap, outside, spill, caption words, text and named-mark contrast) with figs.mjs's own rules restated (kept in step by hand; the floor stays its own check).
8. **The freeze hash was too narrow.** *Fixed.* `npm run fig:hash` hashes each prompt as rendered with placeholders (system, judge, scorer, hedge, still, stripped, pairwise), each file the gate runs (`tests/pass31/{gate,prompts,lib,hash}.mjs`, `tests/pass30/bare.mjs`, `scripts/known-terms.mjs`) and the model id into one combined hash. The CLI version is recorded beside it, not in it: the CLI updates itself (it did during try18), which would otherwise make a frozen gate refuse to run. Every verdict carries the fingerprint; `--expect-hash` refuses a different gate.
9. **The record read better than the evidence.** *Fixed.* Three decoys are in the dev set; every attempt is listed below with what it changed, including that most changes after try6 loosened a rule to stop a v4 false fail; v2's owner reason is now measured on its own (section 9).
10. **No validation runner printing counts only.** *Fixed.* `npm run fig:validate` (section 1).
11. **Minor.** *Fixed.* A glossary entry that is a proper name ("Shannon") passes taught-yet once the prose before the figure uses the name; the scorer rubric numbers its tests in order.

## 8. Attempts after the review (try6 to try21)

Each attempt ran all six items three times (v1, v2, v4 with pairwise; decoys without). "Combined" is the gate fingerprint of section 11 (first 12 hex digits; every verdict carries it in full). Each change was tuned on these six items only.

| Attempt | Combined | Change before the run | v1, v2, v4 correct | Decoys correct | Where v4 failed |
|---|---|---|---|---|---|
| try6 | `efa38bd07771` | the review's fixes: `cause_drawn`; unexplained words (any listed word fails) and marks; hedge on all three descriptions with no carve-outs beyond side details; temp sandbox, static path, tool errors | 6 of 9 | 9 of 9 | every run: "head" and "write, stop" listed as unexplained words; hedges on the meaning of 3 + 1 = 4 and on what a still cannot show |
| try7 | `d744d113fa36` | words: one the text uses is plain; describers' `unsure` back to the main idea; hedge: the meaning of the end state is the scorer's | 6 of 9 | 9 of 9 | scorer: the "+ 1" not drawn; still hedges (what "write" writes); decoy3 slipped through the words test |
| try8 | `9c867a55a4ae` | words: a name for a state or mode counts even if guessable, drawn parts and plain actions do not; scorer: the result line also says what the marks count; still hedge scoped to the cause; stripped: timing out | 6 of 9 | 9 of 9 | hedge only ("whether it truly stops", what "write" writes) |
| try9 | `13de21428ad3` | hedge: a doubt naming its drawn evidence does not count; "more than is drawn" does not count | 7 of 9 | 9 of 9 | hedge (stripped); scorer ("stop" only in the card's word) |
| try10 | `84be92be7f7b` | holding still under a lit card is a drawn stop (hedge and scorer); stripped: "stops or holds" is a result | 7 of 9 | 9 of 9 | stripped hedge ("does the move come from the rule") |
| try11 | `16859edc2fd0` | stripped hedge: doubts about which action a wordless rule stands for do not count | 8 of 9 | 9 of 9 | stripped hedge |
| try12 | `83939b503d7b` | stripped hedge rewritten as a narrow positive check | 9 of 9 | 9 of 9 | none |
| try13-repeat | `83939b503d7b` | none | 8 of 9 | 8 of 9 | still hedge ("start, end or only the rules"); decoy3 passed once |
| try14 | `c6921ec30be8` | words: a word tagged onto a part to name its condition counts ("head · ready"); still: "start or end" out | 8 of 9 | 9 of 9 | still scorer counted a resolved mark |
| try15 | `35f6bd03f669` | scorer: judge only the two unexplained lists; a mark used the intent's way is resolved | 8 of 9 | 9 of 9 | the judge listed "head" as an unexplained word |
| try16 | `4492baec5e7c` | each unexplained word carries its reason; one exception: the text describes the thing and only its placement was unsure | 7 of 9 | 9 of 9 | judge hedge (a frame caught mid-slide); stripped hedge (cause or correlation) |
| try17-repeat | `4492baec5e7c` | none | 8 of 9 | 9 of 9 | still hedge (how the rules are chosen) |
| try18 | `56074fa63ee2` | timing: a frame between two positions; still: how rules are chosen step by step out; stripped: only "which thing moves" and "no drawn cause" count | 5 of 9 (3 ERROR) | 9 of 9 | three runs ERROR (the CLI updated itself mid-run); judge hedge counted against its rule |
| try19-repeat | `56074fa63ee2` | none | 8 of 9 | 9 of 9 | still scorer counted the resolved "+ 1" mark |
| try20 | `3294111df0b4` | prompts unchanged; each scorer and hedge check asked three times, majority decides; spawn failures retried | 8 of 9 | 9 of 9 | judge hedge, all three votes: the reader doubted "whether the head frame sliding between cells is the head moving or just the animation of the highlight" |
| try21-repeat | `3294111df0b4` | none | **9 of 9** | **9 of 9** | none |

Frozen: try20 and try21's configuration. The requirement (9 of 9) is met by try21; try20, with the same configuration, had one false fail of v4, recorded above and in section 10.

## 9. Runs of the frozen configuration (try20, try21)

Order: the first pairwise order of the run (both orders are asked in every run). Hedge in: the descriptions whose hedge check failed.

| Attempt | Item | Run | Order | Expected | Got | Failed criteria | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|
| try20 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | candidate A: RC2; rc2 A: RC2 |
| try20 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try20 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try20 | v2 | 1 | cand-first | FAIL | FAIL | judge, hedge, still, pairwise | judge | candidate A: RC2; rc2 A: RC2 |
| try20 | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try20 | v2 | 3 | random | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try20 | v4 | 1 | cand-first | PASS | PASS | none | none | candidate A: SAME; rc2 A: CANDIDATE |
| try20 | v4 | 2 | rc2-first | PASS | FAIL | hedge | judge | rc2 A: CANDIDATE; candidate A: SAME |
| try20 | v4 | 3 | random | PASS | PASS | none | none | candidate A: SAME; rc2 A: CANDIDATE |
| try20 | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try20 | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try20 | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try20 | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try20 | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try20 | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try20 | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |
| try20 | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |
| try20 | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try21-repeat | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | candidate A: RC2; rc2 A: RC2 |
| try21-repeat | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try21-repeat | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | still | candidate A: RC2; rc2 A: RC2 |
| try21-repeat | v2 | 1 | cand-first | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try21-repeat | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try21-repeat | v2 | 3 | random | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try21-repeat | v4 | 1 | cand-first | PASS | PASS | none | none | candidate A: SAME; rc2 A: CANDIDATE |
| try21-repeat | v4 | 2 | rc2-first | PASS | PASS | none | none | rc2 A: CANDIDATE; candidate A: SAME |
| try21-repeat | v4 | 3 | random | PASS | PASS | none | none | candidate A: RC2; rc2 A: CANDIDATE |
| try21-repeat | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try21-repeat | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try21-repeat | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try21-repeat | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try21-repeat | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try21-repeat | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try21-repeat | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try21-repeat | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |
| try21-repeat | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |

Sub-tests the scorers failed by majority in these 12 runs per item (6 for each of try20 and try21): v1 fails judge `mechanism` 6/6, `unexplained` 6/6, `one scene, shown once` 6/6, `few words` 6/6, still `mechanism` 6/6, stripped both tests 6/6, and `taught` every run. v2 fails judge `one scene, shown once` 6/6, `few words` 6/6 and **`unexplained` 5/6 (its owner reason: "adding" and "done" listed as unexplained state words)**, still `unexplained` 6/6 and `few words` 6/6; its mechanism passes. decoy1 fails judge `mechanism`, `unexplained`, `carried by the picture` 6/6, still `mechanism` 6/6, stripped both tests 6/6. decoy2 fails judge `mechanism` and `carried by the picture` 6/6, still `mechanism` 6/6, stripped "what causes what" 4/6. decoy3 fails judge `unexplained` 6/6 and still `unexplained` 6/6 ("adding"). v4 failed no scorer test in these runs. Pairwise: rc2 (v4) was judged better than v1 and v2 in all 24 replies.

Without pairwise (as the sealed validation runs), v1 and v2 still fail on their single-figure criteria in 12 of 12 runs.

## 10. Known limits

- **v4's false-fail rate is not zero.** With the frozen configuration v4 failed 1 of 6 runs (try20 run 2: one reader doubted whether the head frame sliding between cells is the head moving, and the three hedge votes counted it unanimously, a real doubt in that description rather than checker noise). With the same prompts before the votes (try18, try19) it failed 2 of 6 runs. The sealed validation needs v4 to pass in one run, so it carries roughly a one-in-six risk of failing on v4 alone; the brief allows a fresh builder one more attempt.
- **Tuned on one approved figure.** After try6 (which tightened: drawn cause, unexplained words, hedge on three descriptions, decoys), every change except the state-word rules (try8, try14) loosened a rule to stop a v4 false fail. The loosenings are the hedge exclusions listed in section 7, item 1, and the scorer's result-line clauses (the line also says what the marks count; a doubt about how it refers to the marks is not an unexplained mark). They are written generally but were found on Fig 1.1 only.
- **The hedge check is strict only where it is narrow.** It fires on figures that fail anyway (v1, the decoys) and once on v4; it has never met a figure that is right but uncertain, so its strictness there is unknown. Its exclusions (meaning, drawn evidence, more than drawn, the still's and the stripped strip's scopes) are judgement calls a figure could exploit, for example a stop shown by holding still under a vague card.
- **Unexplained words depend on the judge listing them.** decoy3 passed the words test in some runs before try14 (the judge read "adding" as plain); with the frozen prompts it was caught 6 of 6, v2's state words 5 of 6 in the judge and 6 of 6 in the still. A single state label could still slip through a run.
- **One description per view.** The votes damp the checkers; the judge, the still and the stripped reader each describe once, so one reader's doubt can fail a figure (try20).
- **Static figures** are tested only on a fixture (v4 with SMIL removed), and their text-stripped test runs on one frame, which the review proposed to skip.
- **Tester context.** Testers still receive the CLI's userEmail block and an environment block (temp path, no git); it cannot be removed without `--bare`. The CLI reports `claude-haiku-5-5` beside `claude-sonnet-5-5` in each session's usage (its own side calls); the replies are Sonnet 5.5's.
- **CLI version.** Recorded (2.1.310 at the freeze) but not in the combined hash, because the CLI updates itself; a new version could change tester behaviour without changing the hash. `fig:validate` records the version it ran with in `reads.log` and `counts.json`.
- **"few words"** is the scorer's call on the describer's own `text_pieces` count; the mechanical label cap lives in `fig:check`.
- **Legends** are checked only when tagged `legend`. **fig:check** restates figs.mjs's failure rules by hand for the per-figure `gate1` check; a change in figs.mjs must be copied. Its failing branch has not yet met a failing row (section 5).
- **The intent decides `mechanism`**, so the gate tests the intent sentence's wording as much as the figure (the brief's design).
- **Rendering** is Chromium only. The full `fig:check -- part-1` (41 min) was not re-run after the changes; chapters 1 and 2 were (quick Gate 1).
- **figlib literal regression check** still fails (pre-existing drift, section 5); unchanged.

## 11. Frozen (2026-10-24), then reopened

**Superseded.** This freeze was reopened for section 13 and not re-made; the values below are those of `dd51d25` and no longer match the code (taught-yet rules, ledger reading, real-thing prompts). The text as written at the freeze follows.

The gate is **frozen** as of 2026-10-24, at the configuration of try20 and try21. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. `npm run fig:hash` reproduces these values; run the validation as `npm run fig:validate -- --expect-hash=3294111df0b4b9b81033d65b2424affad874452574d0894bd76076d31526185d`.

SHA-256 of each judge prompt, rendered by `prompts.mjs frozenTexts()` with placeholder inputs (`{{PACKET}}`, `{{INTENT}}`, field placeholders); the scorer hash covers its 9 renderings (judge, still, stripped × function, real thing, two-part), the hedge hash its 3 (judge, still, stripped), the stripped hash its 12-frame and 1-frame forms, the pairwise hash its 4 frame-count forms:

| Prompt | SHA-256 (frozen 2026-10-24) |
|---|---|
| judge (12 frames) | `fd5e2c7a8461beb9dff9f129e4f7e5dc62398d55b8661b4fdc58109bef053b20` |
| scorer | `584de9d374a23abb29033a395855e4dab22c2bbe9b73c7e48788ee41cc36b2ba` |
| hedge | `1a95a6bb022667749b3bdcc77e9420bd83bb7018ebac7e4c69f6ab58006a9f13` |
| t=0 still | `87a0a088b55e0fed246c5438fc51cd259a7dad76a57c81369e414d8b6eef4a76` |
| text-stripped | `d9a1570d7e9cbd2c36257640055d1643717f3f8330bb53625f52717f9a75a2ab` |
| pairwise | `382b5b6a0f2f9ad0da3b1bc312745682cdd88f216c4bef7cb148acf4b2b1b50e` |
| system (every tester) | `32e914caf96b78905a2c020a696e70eb2c9b64c4c921574c0373d890eb223aeb` |

| File the gate runs | SHA-256 (frozen 2026-10-24) |
|---|---|
| `tests/pass31/gate.mjs` | `25c999f2d32a934602e4c2b531b14a6ab6275d2a60cb81e2612f4d3cc7b4409f` |
| `tests/pass31/prompts.mjs` | `529f80b39e3dad2377cbc1adf98f99bbcf9acab797d34e370131653acd85c149` |
| `tests/pass31/lib.mjs` | `827d041a3e3e5e84de95f6d073454fd0ca9d0a82d6fb11254c1bd595b1ef3c75` |
| `tests/pass31/hash.mjs` | `ed57f3a3346e4eba6aae1d238b7a80bcbe5ac10c34379033bd89e68770c08508` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `df5a945e7082e746e544d00bc3913094fc38480f10e08f62d71634011eff6cba` |

- Model: `claude-sonnet-5-5`; votes per scorer and hedge check: 3 (in `gate.mjs`).
- Combined fingerprint (prompts, files, model): `3294111df0b4b9b81033d65b2424affad874452574d0894bd76076d31526185d`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.

## 12. Full prompt texts (tests/pass31/prompts.mjs, sha256 `b54ca44c368332f631564fb7a7b6c46d7b4d6fb6533537fccaacb5177c0b6c57`, the try25 configuration; not frozen)

The frozen text of `dd51d25` (sha256 `529f80b3...`) is in git history. Every tester gets `SYSTEM` as its system prompt and one user message. `JUDGE`, `STILL`, `STRIPPED` and `PAIRWISE` are followed by the images: for 12 frames each is preceded by a line `Frame k of 12 (t = ... s of a ... s loop):` (pairwise: `Version A, Frame k ...`); a one-frame figure's image is preceded by `the still picture:`; the still tester's image by `The still:`. `SCORER` and `HEDGE` get text only.

```js
// Pass 31 gate prompts (tests/pass31/gate.mjs). The full text is reproduced in docs/pass-31-calibration.md, with the
// hash of every prompt (npm run fig:hash). The author never reads this file (brief section 6: the author learns only
// pass or fail and the criterion name). Every tester is a fresh Sonnet 5.5 session with no tools, run in an empty
// temporary directory outside the repo: it sees only what its message holds.

export const SYSTEM = `You help test the figures of a book about how computers work. You only look and report what you see and understand. You never suggest changes, never advise, never vote on anything but the question asked. Answer with exactly one JSON object and nothing else.`;

const BOOK = packet => `THE BOOK SO FAR (everything you have read before the figure; figures that came earlier are left out):
<<<
${packet}
>>>`;

// the fields every describer fills the same way
const CAUSE_DRAWN = `"cause_drawn": "what in the picture shows the cause: name the drawn thing (a shape, a card, a symbol, an arrow, a light) that you see act, light up, match or point when each change happens, and say what it shows. Write \\"none\\" if the picture shows things changing but nothing drawn shows why, if the cause is only written out in words, or if you know the cause only from the text you read before the figure"`;
const CAUSE_DRAWN_STILL = `"cause_drawn": "what in the picture shows the cause: name the drawn thing (a rule card, an arrow, a drawn state, a symbol, a shape) that shows why the change happens, and say what it shows. Write \\"none\\" if nothing drawn shows why, if the cause is only written out in words, or if you know the cause only from the text you read before the figure"`;
const UNEXPLAINED = `"unexplained_words": ["one entry per word or label written in letters in the picture whose meaning here you had to guess, written as the word, a colon, and why you could not place it: a word the text you read never uses, or a word used as the name of a state, a mode, a step or a setting that neither the picture nor the text says what it is, even if you could guess it from the rest of the picture. This includes a word tagged onto a part to say what it is doing or what condition it is in (for example "head · ready"), unless the picture or the text says what that condition is. Leave out a word naming a drawn part or object the text has described, and a plain everyday word for an action, even where the picture puts it somewhere you did not expect. Leave the list empty if every word is plain"],
 "unexplained_marks": ["each symbol, number, sign or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave the list empty if there is none"]`;

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
 ${CAUSE_DRAWN},
 "result": "where it ends up: the result the figure arrives at",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never shows it happening or drawn; \\"none\\" if none",
 "repeated": "anything the figure shows twice in different forms, for example a scene and also a step-by-step replay of the same steps, or the same rules written out again as a table. A label naming a drawn thing, or a short result line saying what the scene arrives at, is not a repeat; \\"none\\" if none",
 ${UNEXPLAINED},
 "unsure": ["each doubt you still have, after looking at every frame, about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (the exact timing of the animation, the loop starting again, layout, colours). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (d) the t=0-only judge: the reduced-motion still (also the whole test of a figure that does not animate)
export const STILL = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as a reader who has turned animation off sees it: one still picture that does not move. The figure has no caption and no explanation: you have only this picture and the text you have read.

Describe what the figure shows and teaches, from the still and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The still follows. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words",
 "panels": ["one entry per separate picture inside the figure (a key, rule card, label or result line belongs to its scene)"],
 "changes": "what the still shows changing, happening or having happened: the process it depicts, as you work it out from what is drawn",
 "cause": "what makes it happen, as the picture shows it",
 ${CAUSE_DRAWN_STILL},
 "result": "the result the figure shows or states",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never draws it; \\"none\\" if none",
 ${UNEXPLAINED},
 "unsure": ["each doubt you still have about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (layout, colours). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (e) the text-stripped judge: the same frames with every <text> removed (one frame for a figure that does not animate)
export const STRIPPED = (packet, n = 12) => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure ${n > 1 ? `as ${n} frames captured at equal steps through one loop of its animation (frame 1 is the start; after frame ${n} it starts again)` : 'as one still picture (the figure does not animate)'}. Every word, letter and number has been removed from the picture: only shapes, marks, colours${n > 1 ? ' and their motion' : ''} are left. There is no caption.

Say what the picture shows by its shapes${n > 1 ? ' and motion' : ''} alone, using the text you have read only to name things. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The ${n > 1 ? `${n} frames follow` : 'picture follows'}. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn: the shapes and what they seem to stand for",
 "moves": "${n > 1 ? 'what moves or changes, frame by frame' : 'what the shapes show moving, changing or happening (arrows, drawn states, before and after)'}",
 "cause": "what causes what: which thing acts, and what happens to which other thing as a result",
 ${CAUSE_DRAWN},
 "result": "where it ends up",
 "unsure": ["each doubt you still have about what moves, what causes what, or the result${n > 1 ? ' after looking at every frame' : ''}. Leave out doubts you resolved; leave the list empty if you have none"]
}`;

// (b) the scorer: a describer's description against the intent sentence, for the figure's job
const JOBS = {
  'function': `The figure's job is "function": it shows how something works. The bar for this job (the book owner's approved reference) is one calm scene, the core function, few labels, motion that is the mechanism, and the result stated.`,
  'real thing': `The figure's job is "real thing": it draws a real physical object, machine or place as it looks, its parts drawn with their own physical features (a wheel's contacts and wiring, round keys and lamps, a cabinet's front), even when the drawing is simplified or flattened; and the reader sees in it what the intent says happens. This job is judged on showing the real object as it looks and what visibly happens in it, not on explaining how or why it works: a reader who cannot say what the object is for, why it is built or wired as it is, or why it gives these particular values does not fail for that. Plain labelled boxes joined by arrows or lines standing for the parts, a table, a timeline or text in a frame is never a real thing.`,
  'two-part': `The figure's job is "two-part": one panel shows the real thing and the other shows its function, in one figure. Two panels are expected; each must do its job.`,
};
const DRAWN = `A thing that holds still while its matching rule card stays lit is shown stopping, even though the card's word names the stop. The cause counts only when the picture draws it: "cause_drawn" must name a drawn thing (a shape, card, symbol, arrow or light) that shows the intent's cause. It fails if "cause_drawn" is "none", empty, or names only written words; if "read_only", "unsure" or "cause_drawn" says the rules, the cause or the result is not drawn or not shown; or if the cause given comes only from the book's text before the figure or from the reader's own guess.`;
const DRAWN_STILL = `The cause counts only when the picture draws it: "cause_drawn" must name a drawn thing (a rule card, an arrow, a drawn state, a symbol) that shows the intent's cause. It fails if "cause_drawn" is "none", empty, or names only written words; if "read_only", "unsure" or "cause_drawn" says the rules or the cause are not drawn; or if the cause given comes only from the book's text before the figure or from the reader's own guess. A still cannot show the change happening, so the result may be worked out from the drawn rules and states or stated by a short result line.`;
const UNEXPLAINED_BASE = `unexplained: it fails if "unexplained_words" lists any word or label (a word the reader had to guess, or one naming something the text never introduced, fails even when the reader got the mechanism anyway; an entry that is only a number or a sign is judged as a mark). The one exception: an entry whose own reason says the text describes the thing the word names and the reader was unsure only where or how the picture places it does not count. It also fails if an entry in "unexplained_marks" shows that the reader could not get what changes, why, or the result. Judge only these two lists here (doubts in "unsure" are scored elsewhere). A mark the description itself uses in the intent's way in "changes", "cause" or "result" is resolved; so is a mark the description itself resolves elsewhere (for example strokes the reader took as counting marks and then used that way in "result"), one about decoration, or a doubt only about how a short result line refers to the drawn marks (whether it states the task or the answer, which mark is the "+ 1") when "result" matches the intent, does not count.`;
// a real thing is judged on showing the object as it looks: its parts' names, the letters on them, a legend and a short
// note on a part are part of that job (taught-yet still checks every token mechanically)
const UNEXPLAINED_TEST = job => job !== 'real thing' ? UNEXPLAINED_BASE : `${UNEXPLAINED_BASE} For this job (real thing), do not count, in either list, an entry for a word, letter or number that is part of drawing the object: a part's name (a key, a wheel, a lamp, a reflector, a cabinet), the letters or numbers written on a part (a key's letter, a wheel's position letter), a legend for the drawing's colours or lines, or a short note on the drawing saying what a part does or how the drawing simplifies the object. These do not count even when the reader had to guess them or the text never used them: naming the parts of the object as it looks is this job (a separate mechanical check makes sure every such word is an everyday word or taught before the figure). Count only a word tagged onto a part to name a state, mode or condition it is in that neither the picture nor the text explains (for example a part tagged "· ready").`;
const OBJECT = `object: the description recognises the real object or scene the intent names, its parts drawn with their own physical features (for example wheels with their rows of contacts and the wiring inside them, round keys and lamps). It fails only when the parts are plain boxes or labels with nothing of the part drawn in them (at most a name, a letter or a number), joined by arrows or lines, or when the figure is a table, a timeline or text in a frame. Parts drawn with their own detail pass even when the reader calls them boxes or the drawing a diagram.`;
// a real thing's cause is its part changing as drawn; how that change gives the result inside the object is function
const REAL_CAUSE = ` For this job (real thing), the cause is drawn when the part the intent names is drawn changing (it moves or steps, or its position letter or drawn state changes); how that change produces the result inside the object is not tested, so a reader who says nothing shows how it does so does not fail this test.`;
const RUBRIC = {
  judge: job => `Score the description against the intent. PASS only if every test below passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: the same thing changes, for the same cause, with the same result. Paraphrase is fine and extra correct detail is fine. It fails if what changes, why, or the result is missing, vague or wrong, or if the description gives a different mechanism, a different representation or a different example than the intent names. ${DRAWN}${job === 'real thing' ? REAL_CAUSE : ''}
2. ${UNEXPLAINED_TEST(job)}
${job === 'real thing' ? `3. ${OBJECT}` : `3. carried by the picture: the mechanism is shown happening or drawn, not only written. It fails if "read_only" names a part of the mechanism (what changes, why, or the result) that the picture never shows, or if the cause is not drawn (test 1). Things moving is not enough: the picture must show what makes them move. A short result line that states what the drawn change amounts to (for example a sum, which also says what the drawn marks count) is part of this bar ("the result stated") and does not fail the test, even when "read_only" names it, as long as the change it sums up is shown happening.
4. one scene, shown once: ${job === 'two-part' ? 'at most two panels, and' : 'one panel only (the scene, with its own rule cards, keys and result line), and'} "repeated" is "none". It fails if the figure adds a separate table, list of steps, replay or block of text beside the scene, or shows the same steps twice. A short result line that states what the scene arrives at is not a repeat, even when "repeated" names it.
5. few words: the picture uses few words. It fails if "text_pieces" is more than 8 for one panel, or if the words, not the picture, carry the mechanism.`}`,
  still: job => `This description comes from the still alone, the frame a reader with animation turned off sees (for a figure that does not animate, the whole figure). A still cannot move, so the change may be shown by drawn states, arrows, a before and after, drawn rules, or a stated result, and the reader may have to work the motion out. Score it against the intent: a reader who works out, from what is drawn, the same change, cause and result as the intent passes, even when the reader says the change is implied rather than seen. PASS only if every test passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: what changes, why, and the result, as the intent says. Paraphrase is fine. It fails if any of the three is missing, vague or wrong, or a different mechanism is given. ${DRAWN_STILL}${job === 'real thing' ? ` For this job (real thing) the change may also be shown on the drawn object by its parts' drawn states, a row of results, or a short note on the part that changes together with that part's drawn state (a still cannot move); such a note counts as drawn.${REAL_CAUSE}` : ''}
2. ${UNEXPLAINED_TEST(job)}
3. ${job === 'real thing' ? OBJECT : `few words: it fails if "text_pieces" is more than 8 for one panel.`}`,
  stripped: job => job === 'real thing' ? `This description comes from the figure with every word, letter and number removed (the letters on keys, wheels or dials too): only shapes (and, for an animated figure, their motion) were left. The figure's job is "real thing", so score whether the picture without its words still shows the real object and what changes in it, as the intent says. Names are not expected, and why the object behaves as it does is not tested for this job. PASS only if both tests pass; otherwise FAIL.
1. the object: the shapes the description gives can be matched to the parts of the object the intent names, drawn with their own features (for example panels with rows of contacts and crossing wires for wheels, circles for keys and lamps, cabinets), even when the reader cannot name them or calls them boxes. It fails only if the reader saw plain empty boxes with nothing of the part drawn in them, joined by arrows or lines, or text-like blocks.
2. what changes: the description names a drawn part that moves or changes, or a drawn result that changes from one press or step to the next (a different light, a path that takes a different route), consistent with the intent. It fails if it names nothing that changes, or only a change the intent does not name.` : `This description comes from the figure with every word, letter and number removed: only shapes (and, for an animated figure, their motion) were left. Score whether the picture still shows what moves and what causes what, as the intent says. Words and numbers are not expected. PASS only if both tests pass; otherwise FAIL.
1. what moves: the description names the thing that moves or changes and how, consistent with the intent.
2. what causes what: the description says which thing acts and what happens because of it, consistent with the intent's cause, and "cause_drawn" names a drawn shape that shows that cause (it lights up, matches, points or acts when the change happens). It fails if "cause_drawn" is "none" or empty, if the description can say only that things move, appear or light up without what causes what, if the cause given is only the reader's guess or comes only from the book's text, or if it gives a different mechanism.`,
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

// (c) the hedge check, on each description (12 frames, still, text-stripped), each in its own scope. It guards the
// events the reader saw: what changes, what makes it change, whether it stops, where it ends up. What the end state
// means (that marks stand for a number, that a line states the sum) is scored by the scorer's mechanism test.
const HEDGE_SCOPE = {
  judge: { what: 'what changes, what makes it change, or where it ends up', fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'],
    out: '' },
  still: { what: 'what makes the change happen (which drawn thing is the cause, and whether the rules or causes are drawn)', fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'],
    out: `\n- It is about what happens over time, what a rule's action produces (for example what "write" writes), how the drawn rules are chosen step by step, whether the end state is reached, or whether the still shows the start, the end or only the rules: the reader saw one still picture, which cannot move, and another test scores whether the reader worked those out. A doubt about which drawn thing causes the change, or whether the cause is drawn at all, still counts.` },
  stripped: { what: 'what moves, or whether any drawn thing causes it', fields: ['moves', 'cause', 'cause_drawn', 'result', 'unsure'] },
};
// The text-stripped reader lost every word that named an action or a result, so its check is narrow and positive: it
// counts only a doubt about which thing moves, or a doubt that anything drawn causes the change (the stripped scorer
// tests the drawn cause itself).
const HEDGE_STRIPPED = (d, job = 'function') => job === 'real thing' ? `Below is part of a blind reader's description of a figure from which every word, letter and number was removed. The figure draws a real object, and it is judged on showing that object as it looks, not on how or why it works. Decide whether the reader hedges on whether anything in it changes.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only when it says that nothing in the picture moves or changes, or that the reader cannot tell what the drawing shows at all.
Every other candidate does NOT count: doubts about which of the drawn things moves, or whether a change the reader sees is real or meant; why things move or change, what causes it, what the shapes or their parts stand for or are called (the words that named them were removed), what the object is for; timing (a pause, a frame where nothing is lit, a frame caught between two positions, the order inside a step); the result (where it ends up, whether it stops or holds still); the loop starting again; colours and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "nothing changes | cannot tell what is drawn | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "nothing changes | cannot tell what is drawn"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)` : `Below is part of a blind reader's description of a figure from which every word, letter and number was removed. Decide whether the reader hedges on what moves, or on whether any drawn thing causes it.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these two cases:
- it leaves open WHICH thing moves or changes (the reader cannot tell what moved, or offers two different things);
- it says that nothing drawn shows why things move or change: the reader names no drawn thing as the cause at all. "cause_drawn" being "none" or empty also counts.
Every other candidate does NOT count: doubts about which action a drawn rule stands for, whether a particular step comes from the drawn cause the reader named, or whether that drawn thing causes the change or only goes with it (the words that named the actions were removed, and another test scores the drawn cause); timing (a pause, a frame where nothing is lit, a frame caught between two positions, the order inside a step); the result (where it ends up, whether it stops or holds still, whether a mark is new); the loop starting again; colours and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "which thing moves | no drawn cause | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "which thing moves | no drawn cause"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
// a real thing is judged on showing the object as it looks, not on how or why it works (brief section 4)
const HEDGE_REAL_THING = (kind, d) => `Below is part of a blind reader's description of a figure${kind === 'still' ? ' seen as one still picture' : ''}. The figure draws a real object (a machine, a device, a place), and it is judged on showing that object as it looks and what visibly happens in it, not on explaining how or why it works. Decide whether the reader hedges on what the drawing shows, on whether anything in the object changes, or on the result it shows.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these three cases:
- it leaves open what the drawing shows: the reader cannot tell what object, or which kind of parts, is drawn;
- it leaves open whether anything in the object changes at all${kind === 'still' ? ' (or, for this still, whether the picture shows a change: drawn states, a row of results, a note on a part)' : ''};
- it leaves open whether the result the reader names changes (for example whether a different lamp lights for the same key), or offers two different results.
Every other candidate does NOT count, however it is worded: which of several parts moves, how far, or why the others stay still; why or how a part moves or gives the result it gives, including whether the drawn part is really what makes the result change; what a letter, mark or note on a part stands for; why the object is built or wired as it is, or what it is for; the order or timing of the results shown, a pause, a frame caught between two positions, the loop starting again; colours, layout and how the drawing is meant. (Another test scores whether the reader saw what the figure is meant to show.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what is drawn | whether it changes | the result | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what is drawn | whether it changes | the result"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
export const HEDGE = (kind, description, job = 'function') => {
  const S = HEDGE_SCOPE[kind];
  const d = Object.fromEntries(S.fields.filter(k => description[k] !== undefined).map(k => [k, description[k]]));
  if (kind === 'stripped') return HEDGE_STRIPPED(d, job);
  if (job === 'real thing') return HEDGE_REAL_THING(kind, d);
  return `Below is part of a blind reader's description of a figure. Decide whether the reader hedges on ${S.what}.

Every candidate below COUNTS as a hedge unless a rule further down says it does not:
- each entry in "unsure";
- each word such as "seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "I infer", "unclear", "not sure", "could be", in any field;
- each pair of alternatives ("either ... or", "whether ... or") and each question, in any field;
- a field about ${S.what} that is missing, empty or vague.
A candidate counts when it touches ${S.what} in any way: which thing changes or moves, how, what makes it, whether a drawn thing causes it, whether it stops, what the end state is, and whether any of these is shown or only implied. It does not matter that another field states the point plainly.
It does NOT count only in these cases:
- It is purely about colours, decoration, layout, the exact timing of the animation (a pause, a frame where nothing is lit, a frame caught between two positions, the order of events inside one step), or the loop starting again.
- It is only about what the end state or a mark, number or line means, not about what happens: for example whether marks stand for a number, whether a written sum states the task or the answer, or which mark is the "+ 1". (Another test scores the meaning.)
- The doubt itself, or "cause_drawn", names the drawn thing that shows the point, and the doubt asks only whether it is really meant that way: for example "the head stays put with the stop card lit, but does the machine truly stop?", or "the stroke appears one frame after the right card lights, so I take it that rule writes it". Holding still is a drawn way to show a stop: a doubt whether the thing truly stops or only holds still, when the description says it holds still while a card or rule stays lit, is of this kind, even when the word on the card is what names the stop. A doubt where nothing drawn shows the point (for example "nothing shows what makes the head stop", or "the rules are never drawn") still counts.
- It asks only whether there is more to the thing than is drawn (another part, a hidden state), while the description states the drawn cause plainly.${S.out || ''}

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what changes | why | end state | meaning | side detail", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what changes | why | end state"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
};

// (f) the pairwise comparison: two versions for the same place, order given by the caller
const seen = n => n > 1 ? `${n} frames captured at equal steps through one loop of its animation (frame 1 is the start)` : 'one still picture (it does not animate)';
export const PAIRWISE = (packet, nA = 12, nB = 12) => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. Two different versions of that figure were made for this place, A and B. Version A is shown as ${seen(nA)}; version B as ${seen(nB)}. Neither has a caption.

Which version would a newcomer who has read only this text understand faster and more surely? Judge by the book's rules for figures: the picture carries the idea (it shows the mechanism, it does not hold a column of text); as few words as the idea allows; motion where motion is the mechanism; nothing a newcomer cannot yet read; everything shown once. Answer "SAME" if the differences would not change how quickly or surely a newcomer gets the idea.

${BOOK(packet)}

Version A comes first, then version B. Then answer with one JSON object, nothing else:
{"better": "A or B or SAME", "why": "two sentences at most, naming the concrete difference"}`;

// the prompts as frozen: each rendered with placeholder inputs, for the hashes in docs/pass-31-calibration.md
export function frozenTexts() {
  const pk = '{{PACKET}}', desc = { '{{DESCRIPTION}}': '' };
  const jobs = Object.keys(JOBS);
  return {
    system: SYSTEM,
    judge: JUDGE(pk),
    scorer: ['judge', 'still', 'stripped'].flatMap(kind => jobs.map(job => SCORER({ kind, job, intent: '{{INTENT}}', description: desc }))).join('\n\u0000\n'),
    hedge: ['judge', 'still', 'stripped'].flatMap(k => jobs.map(job => HEDGE(k, Object.fromEntries(HEDGE_SCOPE[k].fields.map(f => [f, `{{${f}}}`])), job))).join('\n\u0000\n'),
    still: STILL(pk),
    stripped: [STRIPPED(pk, 12), STRIPPED(pk, 1)].join('\n\u0000\n'),
    pairwise: [PAIRWISE(pk, 12, 12), PAIRWISE(pk, 12, 1), PAIRWISE(pk, 1, 12), PAIRWISE(pk, 1, 1)].join('\n\u0000\n'),
  };
}
```

## 13. Follow-up (2026-10-24, session e2): the takeaway form, taught-yet repairs, Enigma. Not re-frozen

The gate frozen at `dd51d25` (fingerprint `3294111d`) was reopened, before any validation ran, for exactly the items of the author's Phase 0 repairs and session e2's verification (its systemic items 2 and 3 and the §15 findings). The cap set by session e2 against overfitting: at most **three prompt revisions** after the first rerun on the takeaway form and Enigma; code that is not prompt wording does not count. Every attempt is logged below, numbered on from try21. **The cap was reached without the bar** (v4 and Enigma did not pass three of three in the last attempt), so, as the cap requires, **the gate was not re-frozen**. The development set is a smoke test; only the sealed validation tests the gate.

### 13.1 What changed (code, not counted toward the cap)

1. **Taught-yet, all-capitals tokens** (`tests/pass31/lib.mjs` `taughtYet`, `scripts/known-terms.mjs`, new `tests/pass31/common-words.txt`). An all-capitals token passes when:
   - the prose before the figure teaches it: `known-terms.mjs` now lists every all-capitals token (two or more capitals; digits and underscores allowed, so CR3 and SYN_SENT stay whole) at the prose paragraph that first uses it (`abbreviations`: part, section, nearest id, offset). Prose is the section text with every figure card (label, picture, caption, strip), every other svg, scripts and styles taken out. A token passes when that paragraph comes before the card. `known-terms.mjs --public=<tree>` reads the tree the gate or check is run on, so offsets match;
   - its lowercase form is on the COMMON-word list: the 1,000 most frequent words of google-10000-english (Google Trillion Word Corpus), kept when the word or a plain inflection is a lowercase dictionary entry, plus 11 everyday words the dictionary predates (box, database, women, ...), minus words that double as abbreviations (al, id, am, re, ...; ax, arm, ram, mac, os, nat, lan, dos listed so a regenerated list keeps them out); 902 words. Below four letters only the exact form counts (DOS is not "do"s);
   - or (beyond the literal item, needed for Enigma, see 13.4) it is an everyday word set in capitals: four letters or more, a lowercase dictionary or COMMON entry, not a glossary term, and never written in capitals anywhere in the book's text outside figure cards (`known-terms.mjs` `capitals`), so it is not an abbreviation the book uses. LAMP, REFLECTOR, ROTORS pass this way; ARM, RAM, OS, MAC, LAN, CPU do not, since the book writes them in capitals.
   The old rules (a three-letter stop list, `/usr/share/dict/words` for four letters or more, the "(RAM)" spelled-out pattern) are gone. A proper name the prose already uses still passes (Shannon; LINUX for a name the prose spells Linux).
2. **Inflections.** `stems()` adds -est, -iest, -ier, doubled consonants, -en and -n participles (written, rewritten, taken, shown), an irregular-form table (became, began, held, ...) and plain prefixes (re-, un-, over-, ...). An inflection of a glossary term the figure has not taught fails like the term (kernels). The COMMON list also counts as everyday for lowercase tokens (database, databases).
3. **Own caption, label, strip.** Prose never includes a figure card, so a term first written in the figure's own caption, label or How-it-works strip is not taught for it. Multi-word glossary terms are now checked whole: "system call", "Ring 0", "Ring 3" fail before they are taught, although every word in them is a dictionary word (a hyphenated term needs its hyphen: "a-machine" is not "a machine"). Named ones (Bell Labs, von Neumann) pass once the prose uses them.
4. **The ledger, read by header.** `lib.mjs readLedger` reads `docs/pass-31-ledger.tsv` by column name, throws on a missing column or a repeated id, and returns the file's sha256; `ledgerTakeaway` gives column `intent` (the takeaway) and column `job`, and refuses a held row or an unknown job. `content` is never read by the gate (it is the fact checker's). `gate.mjs` takes `--ledger` (default `docs/pass-31-ledger.tsv`) or `--intent`/`--job`, never both, and records the ledger file and sha256 in every verdict; `dev.mjs` copies the ledger into the attempt folder and every run reads the copy; `validate.mjs` scores each sealed item against the ledger's takeaway and job (the manifest's own intent only where the ledger has none) and prints how many came from each. `check.mjs` reads no ledger. Tested with a ledger whose 15 columns were shuffled: all 222 rows read the same.
5. **Development set.** Every item's takeaway and job come from the ledger (`figures-final`'s working file, read only, copied per attempt). The takeaways used, identical in all four attempts (ledger sha256 `3309a269e395...` for try22 and try23, `e8396779dc93...` for try24 and try25; the author edited other rows in between): Fig 1.1 "Function: the head walks right past each mark and marks the next blank, so three marks become four." (job function); Fig 1.2 "Real thing: the rotors step before each press, so the same key lights a different lamp every time." (job real thing).
6. **Enigma and a real-thing decoy added.** `enigma`: Fig 1.2 as it stands (this worktree's `public/`, whose prose and card up to Fig 1.2 are byte-identical to `figures-final`'s), expected PASS. `decoy4`: Fig 1.2's takeaway drawn as a block schematic (empty boxes KEY, ROTORS, REFLECTOR, LAMP joined by arrows, a counter stepping 1, 2, 3, a lamp letter F, E, C), expected FAIL, because the amended brief says a schematic is never a real thing; it guards the real-thing loosenings below.
7. `npm run fig:taught-test` (`tests/pass31/taught.test.mjs`): 19 cases at real figure positions, 19 hold: the nine abbreviations fail at Fig 1.1; ARM, RAM, OS, CPU pass at Fig 3.2; AX and AL fail at Fig 3.3 (RAX passes); CR3 passes at Figs BR.4 and 4.8; the state names fail at Fig 10.2 and pass at Fig 10.3 (SYN_SENT to TIME_WAIT, SYN-ACK, ESTABLISHED, LISTEN; TCP, IP, HTTP, DNS); CGNAT fails at Fig 9.8 and IHL at Fig 9.4; THE MACHINE, TAPE, HEAD and Enigma's KEY, LAMP, ROTORS, REFLECTOR pass; lowest, became, rewritten, databases and seven more inflections pass; kernels fails; Ring 3, Ring 0 and system call fail at Fig 1.14; Figs 1.1 and 1.2 are clean.
8. Effect on the book (rc2 figures, this worktree's `public/`): 174 of 222 fail taught-yet (188 with the frozen rules); all-capitals flags 281 to 124, "not an everyday word" 685 to 572. The seven figures of `figures-final`'s `public/` that have drafts or references (Figs 1.1, 1.2, 1.5, 4.8, 10.3, 13.5, 17.6) are clean, including CR3 in Fig 4.8 and the state names in Fig 10.3.

### 13.2 Prompt revisions (the cap: three, all used)

Each revision changed only the **real-thing** renderings: every function and two-part rendering of every prompt is byte-identical from try22 to try25 (checked by rendering each prompt with each version), so v1, v2, v4 and decoys 1 to 3 ran one configuration in all four attempts.

- **Revision 1 (try23).** The amended brief's real thing: the job text (drawn as it looks, judged on showing the object and what visibly happens in it, not on how or why it works); the still's rubric job-aware (the object test instead of "few words", as the judge's rubric already was); a text-stripped rubric for real thing (the object without its words; what changes; no cause test); in the unexplained test, part names, letters on parts, legends and notes on the drawing do not count; in the hedge check, doubts about why the object is built or behaves as it does do not count (the hedge check now gets the job: a code change in `gate.mjs`).
- **Revision 2 (try24).** The object test by physical features (parts drawn with their own features, even simplified or flattened; revision 1's "a schematic of boxes is never a real thing" had made the scorer read Enigma's rotors as boxes); the unexplained exception restated without its "a setting still counts" clause (which caught the rotors' position letters); for real thing the cause is the named part drawn changing, how it produces the result is not tested; the real-thing hedge scope narrowed to what is drawn, whether anything changes and whether the result changes.
- **Revision 3 (try25).** The real-thing hedge as its own narrow check for the judge and the still (revision 2's rule sat as the last exclusion and the checker applied the general rule over it); the object test stated by what fails (plain boxes or labels with nothing of the part drawn in them, joined by arrows or lines).

### 13.3 Attempts

| Attempt | Combined | prompts.mjs | Change before the run | v1, v2, v4 correct | Decoys correct | Enigma passed | Where v4 or Enigma failed |
|---|---|---|---|---|---|---|---|
| try22 | `ec9797ed2dde` | `529f80b3` (frozen) | the code of 13.1 only; prompts as frozen | 7 of 9 | 12 of 12 | 0 of 3 | v4 run 2 judge unexplained ("write, stop"), run 3 still hedge ("whether the head moves from the left cell"). Enigma every run: judge unexplained (REFLECTOR, KEY · LAMP, out, back, "steps each press"), still few words (13 to 15 pieces) and unexplained, stripped "what causes what"; hedges on why only the first rotor steps and why the outputs are F, E, C |
| try23 | `b1d77d7f4d1e` | `fa1abceb` | revision 1 | 9 of 9 | 12 of 12 | 0 of 3 | Enigma: object (judge 2, still 3, stripped 2 of 3 runs: rotors read as boxes) and unexplained (judge and still 3 of 3) |
| try24 | `b858d961da67` | `55ab1a05` | revision 2 | 8 of 9 | 12 of 12 | 0 of 3 | v4 run 1 judge hedge (a pause in frame 5). Enigma every run: judge hedge ("why only the left rotor moves" counted under the general rule); run 3 also still object and hedge |
| try25 | `9ba0dfc0709a` | `b54ca44c` | revision 3 (the cap) | 7 of 9 | 12 of 12 | 1 of 3 | v4 runs 1 and 2 judge hedge ("whether the lit card causes each step or only shows which rule applies"; "why the write, stop card does not show what is written"). Enigma runs 1 and 2 still: mechanism (the stepping shown only by the note "steps each press") in run 1, unexplained ("KEY · LAMP", "steps") in run 2 |

Full fingerprints: try22 `ec9797ed2ddeca27ba960c3c5e52fd81a6ba57f711f1efb361f5db8aef8350a2`, try23 `b1d77d7f4d1ea71cb1aa72eb9de152755da54454f24dd815d7f6bdfeaa6b75b0`, try24 `b858d961da67229069f7cc759e528ac6e0a9ae362f25750383c6ee73dd8a215f`, try25 `9ba0dfc0709a7f4cb8d8ea4f618e5b976ecd8eea474fbb147729e3a43b4f6a87`. prompts.mjs sha256: try22 `529f80b39e3dad2377cbc1adf98f99bbcf9acab797d34e370131653acd85c149`, try23 `fa1abceb3e7def7c567250533c9c588ec4865259b4d5eb2563f7de7da96231d8`, try24 `55ab1a05087c85d3afe12d907ce48e194541ca9f5df23a1abaa0ddccdc340ff7`, try25 `b54ca44c368332f631564fb7a7b6c46d7b4d6fb6533537fccaacb5177c0b6c57`. CLI 2.1.310 throughout.

Sub-tests failed by majority, per attempt (runs of 3): v1 fails judge mechanism, unexplained, carried by the picture, one scene, few words, still mechanism, unexplained, few words, stripped both tests and `taught` in every run of every attempt. v2 fails judge unexplained, one scene, few words and still unexplained in every run; its mechanism passes. decoy1, decoy2 and decoy3 fail as in try20 and try21 (decoy3 on judge and still unexplained, "adding", 12 of 12). decoy4 fails judge mechanism 12 of 12 and, from try23 on, judge, still and stripped object 9 of 9: no revision let the schematic through. Enigma, try25: judge 3 of 3 passed; still mechanism failed 1 of 3 and unexplained 1 of 3; stripped and hedge passed 3 of 3. Pairwise: rc2 (v4) judged better than v1 and v2 in all 48 replies; Enigma's frames are byte-identical to its rc2 version (SAME, no call).

### 13.4 Result and what it means

- **Not re-frozen.** In try25, the configuration after the third revision: v1 and v2 failed 6 of 6, every decoy failed (12 of 12), v4 passed 1 of 3, Enigma passed 1 of 3. The cap's condition (v1 and v2 failing, v4 and Enigma passing, every decoy failing) is not met, so the builder stopped here.
- **v4.** Its configuration did not change in this follow-up, so try22 to try25 are 12 runs of it: 7 passed (try22 1, try23 3, try24 2, try25 1). The five failures: one unexplained word (the judge listed "write, stop") and four failed hedge checks, each carried by all three votes: a pause in a frame where nothing is lit, whether the lit card causes the step or only shows the rule, whether the still shows the head's start (three doubts of kinds the hedge rules exclude), and why the "write, stop" card does not show what is written. The describers and the hedge check never see the takeaway, and the scorer failed v4 once (the unexplained test, which does not depend on it), so the takeaway form does not explain the rate; the frozen gate's own record was 5 of 6 (try20, try21). Whether this is sample noise or a change in the tester model behind the same CLI version is not known.
- **Enigma.** The frozen gate failed it on everything a real thing is not judged on (unexplained part names, few words in the still, the stripped cause, doubts about why only one rotor steps). After the three revisions its judge, stripped and hedge criteria pass 3 of 3; the t=0 still fails 2 of 3 (the stepping it shows is a written note plus the rotors' position letters, and one reader still listed "KEY · LAMP" and "steps").
- **The literal item 1 and Enigma.** Item 1 lets an all-capitals token pass only when taught or on the COMMON list. Enigma's LAMP and REFLECTOR are neither (the prose before Fig 1.2 names only Enigma and its rotors; the reflector is first explained in Fig 1.2's own caption), so the literal rule fails the must-pass figure on `taught`. The rule kept here adds one route: an everyday word of four letters or more that the book never writes in capitals passes as that word. It keeps every abbreviation the book uses, and every token of three letters or fewer, under the teaching rule. This is the builder's reading; the alternative is to drop it, and then Enigma fails `taught` whatever the judge says.
- **Next step (the caller's call, not the builder's):** keep the gate open with these results; or accept a configuration below the bar; or have the author or the brief change what a real-thing still must show. The development set is a smoke test only; the sealed validation (brief section 10) has not run, and the §10 path (one fresh builder, then stop) applies only to a failed validation.

### 13.5 Known limits added by this follow-up

- The real-thing handling (revisions 1 to 3) was found on one real thing (Enigma) and checked against one decoy (decoy4). It is written generally (part names, legends and notes on a drawn object do not count as unexplained; how or why the object works is not tested or hedged), and each loosening applies only to the job "real thing", but no second real-thing figure has been run.
- "Taught" for an abbreviation is mechanical: the first prose paragraph that uses it (CPU at ch1-vonneumann-p3, TCP at ch4-ipc-p2). A first use that does not explain the term still counts as teaching; the judge's unexplained-words test is the backstop.
- Glossary placement is unchanged: terms the prose teaches before their glossary section (register, thread, bandwidth, byte; `docs/pass-31-takeaway-check.md`) still fail as untaught glossary terms.
- A multi-word glossary term written without its hyphen ("copy on write") is checked word by word only.
- The ledger is read from `figures-final`'s working file, which the author was editing during the attempts; each attempt copied it, and the takeaways used never changed.
- `fig:validate` with the ledger was run once on a scratch manifest (v1 as stand-in v3, v4; both takeaways from the ledger, read from `figures-final`'s working file): HOLDS, v3 failed 1 of 1, v4 passed 1 of 1, tool errors 0 (gate `9ba0dfc0`). Nothing under `docs/pass-31-sealed/` was read or written; commit 93aae05 was not touched.

### 13.6 Total attempt count (for the READY page)

**26 prompt attempts** on the development set: try0 to try21 before this follow-up (the frozen configuration was try20 and try21), and try22 to try25 here (one rerun on the takeaway form and Enigma, then the three revisions the cap allows). Each attempt ran every item three times.

### 13.7 Every run, try22 to try25

Order: the first pairwise order of the run (both orders are asked in every run). Hedge in: the descriptions whose hedge check failed.

| Attempt | Item | Run | Order | Expected | Got | Failed criteria | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|
| try22 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | still | candidate A: RC2; rc2 A: RC2 |
| try22 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try22 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | candidate A: RC2; rc2 A: RC2 |
| try22 | v2 | 1 | cand-first | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try22 | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try22 | v2 | 3 | random | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try22 | v4 | 1 | cand-first | PASS | PASS | none | none | candidate A: CANDIDATE; rc2 A: CANDIDATE |
| try22 | v4 | 2 | rc2-first | PASS | FAIL | judge | none | rc2 A: CANDIDATE; candidate A: SAME |
| try22 | v4 | 3 | random | PASS | FAIL | hedge | still | rc2 A: CANDIDATE; candidate A: SAME |
| try22 | Enigma | 1 | cand-first | PASS | FAIL | judge, hedge, still, stripped | judge, still | SAME (identical frames) |
| try22 | Enigma | 2 | rc2-first | PASS | FAIL | judge, hedge, still, stripped | judge, still | SAME (identical frames) |
| try22 | Enigma | 3 | random | PASS | FAIL | judge, hedge, still, stripped | judge | SAME (identical frames) |
| try22 | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try22 | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try22 | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, stripped | not run |
| try22 | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still, stripped | not run |
| try22 | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try22 | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try22 | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |
| try22 | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try22 | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge | not run |
| try22 | decoy4 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try22 | decoy4 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try22 | decoy4 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try23 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | stripped | candidate A: RC2; rc2 A: RC2 |
| try23 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try23 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | candidate A: RC2; rc2 A: RC2 |
| try23 | v2 | 1 | cand-first | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try23 | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try23 | v2 | 3 | random | FAIL | FAIL | judge, still, stripped, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try23 | v4 | 1 | cand-first | PASS | PASS | none | none | candidate A: SAME; rc2 A: CANDIDATE |
| try23 | v4 | 2 | rc2-first | PASS | PASS | none | none | rc2 A: CANDIDATE; candidate A: SAME |
| try23 | v4 | 3 | random | PASS | PASS | none | none | rc2 A: CANDIDATE; candidate A: SAME |
| try23 | Enigma | 1 | cand-first | PASS | FAIL | judge, hedge, still, stripped | judge, still | SAME (identical frames) |
| try23 | Enigma | 2 | rc2-first | PASS | FAIL | judge, hedge, still, stripped | judge, stripped | SAME (identical frames) |
| try23 | Enigma | 3 | random | PASS | FAIL | judge, still | none | SAME (identical frames) |
| try23 | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try23 | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, stripped | not run |
| try23 | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try23 | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try23 | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try23 | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still, stripped | not run |
| try23 | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try23 | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try23 | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try23 | decoy4 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try23 | decoy4 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try23 | decoy4 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, stripped | not run |
| try24 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, still, stripped, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try24 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still, stripped | rc2 A: RC2; candidate A: RC2 |
| try24 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try24 | v2 | 1 | cand-first | FAIL | FAIL | judge, hedge, still, pairwise | judge | candidate A: RC2; rc2 A: RC2 |
| try24 | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try24 | v2 | 3 | random | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try24 | v4 | 1 | cand-first | PASS | FAIL | hedge | judge | candidate A: SAME; rc2 A: CANDIDATE |
| try24 | v4 | 2 | rc2-first | PASS | PASS | none | none | rc2 A: CANDIDATE; candidate A: RC2 |
| try24 | v4 | 3 | random | PASS | PASS | none | none | rc2 A: CANDIDATE; candidate A: SAME |
| try24 | Enigma | 1 | cand-first | PASS | FAIL | hedge | judge | SAME (identical frames) |
| try24 | Enigma | 2 | rc2-first | PASS | FAIL | hedge | judge | SAME (identical frames) |
| try24 | Enigma | 3 | random | PASS | FAIL | hedge, still | judge, still | SAME (identical frames) |
| try24 | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try24 | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try24 | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try24 | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try24 | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try24 | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still | judge, still | not run |
| try24 | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try24 | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try24 | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try24 | decoy4 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try24 | decoy4 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try24 | decoy4 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try25 | v1 | 1 | cand-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | candidate A: RC2; rc2 A: RC2 |
| try25 | v1 | 2 | rc2-first | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge, still | rc2 A: RC2; candidate A: RC2 |
| try25 | v1 | 3 | random | FAIL | FAIL | taught, judge, hedge, still, stripped, pairwise | judge | candidate A: RC2; rc2 A: RC2 |
| try25 | v2 | 1 | cand-first | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try25 | v2 | 2 | rc2-first | FAIL | FAIL | judge, still, pairwise | none | rc2 A: RC2; candidate A: RC2 |
| try25 | v2 | 3 | random | FAIL | FAIL | judge, still, pairwise | none | candidate A: RC2; rc2 A: RC2 |
| try25 | v4 | 1 | cand-first | PASS | FAIL | hedge | judge | candidate A: SAME; rc2 A: CANDIDATE |
| try25 | v4 | 2 | rc2-first | PASS | FAIL | hedge | judge | rc2 A: CANDIDATE; candidate A: SAME |
| try25 | v4 | 3 | random | PASS | PASS | none | none | candidate A: SAME; rc2 A: CANDIDATE |
| try25 | Enigma | 1 | cand-first | PASS | FAIL | still | none | SAME (identical frames) |
| try25 | Enigma | 2 | rc2-first | PASS | FAIL | still | none | SAME (identical frames) |
| try25 | Enigma | 3 | random | PASS | PASS | none | none | SAME (identical frames) |
| try25 | decoy1 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try25 | decoy1 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try25 | decoy1 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still, stripped | not run |
| try25 | decoy2 | 1 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try25 | decoy2 | 2 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try25 | decoy2 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | judge, still | not run |
| try25 | decoy3 | 1 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try25 | decoy3 | 2 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try25 | decoy3 | 3 | no pairwise | FAIL | FAIL | judge, still | none | not run |
| try25 | decoy4 | 1 | no pairwise | FAIL | FAIL | judge, still, stripped | none | not run |
| try25 | decoy4 | 2 | no pairwise | FAIL | FAIL | judge, still, stripped | none | not run |
| try25 | decoy4 | 3 | no pairwise | FAIL | FAIL | judge, hedge, still, stripped | still | not run |
