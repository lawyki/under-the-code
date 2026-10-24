# Pass 31 · gate calibration (gate builder's record)

Brief: `docs/pass-31-brief.md` sections 3, 4, 6, 7 (gate builder track), 10, 11, 15, amended by the author's decisions D1 to D3 of 2026-10-24 (section 14.1). Status: **frozen** (2026-10-24, after the review of the section 16 freeze, section 17: seven defects fixed in code), at the configuration of try26-review: combined fingerprint `327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`, the try26 prompts (unchanged), the gate's decision for a figure being **at least two of three independent complete runs pass** (section 14.2). Run the validation as `npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741` (the ledger is the author's file on `figures-final`; without it the run stops as incomplete; `fig:gate`, `fig:dev` and `fig:validate` refuse, exit 2, without the matching `--expect-hash`, section 16.3). History: frozen first at `dd51d25` (section 11, `3294111d...`), reopened before any validation for session e2's follow-up (section 13), which used its three prompt revisions without the bar (try25, `9ba0dfc0...`); the fresh builder (section 14) implemented D1 to D3, made one prompt revision (try26) and froze at `f8353940...`; the independent review of that freeze found five code defects, fixed in code only (section 15), and the bar held under `4095d1aa...` (try26-fix); the builder follow-up (section 16) changed code only and the bar held again under `bb136e09...` (try26-held); the review of that freeze found seven code defects, fixed in code only (section 17), and the bar held under `327aba6a...` (try26-review). Total prompt attempts: **27** (try0 to try26; try26-fix, try26-held and try26-review reran try26's prompts). The sealed validation (brief section 10) is not part of this record: it runs later with `npm run fig:validate` and reports counts only.

The gate builder never saw the sealed material: commit 93aae05 (Fig 1.1 v3) was not checked out, shown, diffed or rendered, and nothing under `docs/pass-31-sealed/` was read or written. No held figure's card, caption or strip and no held prose was opened (section 16). The validation runner was tested only on a scratch manifest in the builder's scratch directory, with v1, v4 and a decoy as stand-ins. The only Fig 1.1 versions used are v1, v2 and v4 below, plus decoys built from v4. No figure from the book's security chapters was opened.

## 1. Tooling

| Command | File | What it does |
|---|---|---|
| (library) | `scripts/figs/figlib.py` | `text(role="label"\|"object"\|"legend")` writes `data-role`; `obj()` wraps glyphs with their shape in `<g data-obj="1">`; `Timeline` exports its beat times. Byte-neutral for untagged scripts (section 5). `legend` added 2026-10-24 (review item 6). |
| `python3 scripts/figs/build_into.py <public dir> <script.py>...` | `scripts/figs/build_into.py` | Runs figure scripts against any `public/` tree (redirects every `open()` under the main checkout's `public/`), one process per script. |
| `node tests/pass30/bare.mjs ... --no-text` | `tests/pass30/bare.mjs` | The SVG alone at a SMIL time; `--no-text` removes every `<text>` first. |
| `npm run fig:sheet` | `tests/pass31/sheet.mjs` | Contact sheets per chapter, 375 px, t=0, Fig 1.1 v4 and Fig 1.2 Enigma pinned. |
| `npm run fig:check -- <part>` | `tests/pass31/check.mjs` | Mechanical checks per figure: Gate 1 rows attributed to the figure (new), label cap (tightened), legend entries (new), 11 px floor, taught-yet, t=0 empty band, `<desc>`, caption, strip; per part: dashes, anchors, each Gate 1 tool's summary. Exemptions only for the label cap, the floor and the caption check (section 17). |
| `npm run fig:gate -- <id> [--ledger=...]` | `tests/pass31/gate.mjs`, `tests/pass31/prompts.mjs`, `tests/pass31/lib.mjs`, `tests/pass31/common-words.txt` | The gate (section 2): one decision, at least two of three independent complete runs passing (section 14.2); `--single` is one complete run, the decision's building block. The takeaway and job come from the ledger by header name (section 13.1, item 4), or from `--intent` and `--job` for a figure outside it. |
| `npm run fig:dev -- [--runs=3] [--label=...] --ledger=...` | `tests/pass31/dev.mjs` | The development set: builds v1, v2, v4, the five decoys and Enigma (section 13.1, items 5 and 6; decoy5 from section 15) and runs the gate on each, three times (three evaluations, each one decision of two or three complete runs, from try26 on), with the ledger's takeaways. |
| `npm run fig:taught-test` | `tests/pass31/taught.test.mjs` | The taught-yet rules on fixed cases at real figure positions: 19 (section 13.1, item 7), 30 from section 15, 77 from section 16, 135 from section 17. |
| `npm run fig:packet-test` | `tests/pass31/packet.test.mjs`, `tests/pass31/held.mjs`, `tests/pass31/held-strip.json` | The held material out of every non-held judge packet, prose-token set and known-terms credit: the strip list against the tree, every packet built and searched, planted markers, controls (section 16.1); planted name markers never credited by mention (section 17). |
| `npm run fig:hash` | `tests/pass31/hash.mjs` | The gate's fingerprint: sha256 of each prompt, of each file the gate runs (from section 15 also `tests/pass31/validate.mjs`; from section 16 also `tests/pass31/held.mjs` and `tests/pass31/held-strip.json`; from section 17 also `tests/pass31/check.mjs`, `tests/pass31/band.py`, `tests/pass28/figs.mjs`, `tests/pass28/clip.mjs`, `tests/pass28/smooth.mjs`, `tests/pass30/contrast.mjs`), the model id, and the combined hash; the CLI version beside it. `fig:gate`, `fig:dev` and `fig:validate` compute it first and refuse (exit 2) unless `--expect-hash` equals it (section 16.3). |
| `npm run fig:validate -- --ledger=<figures-final>/docs/pass-31-ledger.tsv --expect-hash=<combined>` | `tests/pass31/validate.mjs` | The sealed validation: runs the frozen gate (no pairwise; each item one decision, section 14.2) on the items of `docs/pass-31-sealed/validation.json`, each scored against the ledger's takeaway (the manifest's intent and job only where the ledger has none), and prints counts only; everything else stays under `docs/pass-31-sealed/`. A missing or unreadable ledger, or a fallback item without a valid job, is incomplete (exit 2; section 15). |

Outputs (renders, packets, every tester reply, verdicts) go to `tests/pass31/out/` (gitignored); validation outputs go to `docs/pass-31-sealed/` (gitignored).

## 2. The gate

`npm run fig:gate -- <fig-id> [--ledger=<docs/pass-31-ledger.tsv>] | [--intent="<takeaway>" --job="function|real thing|two-part"] [--tree=<public dir>] [--rc2-tree=<dir> | --rc2-rev=v1.0-rc2 | --no-pairwise] [--order=random|cand-first|rc2-first] [--criteria=...] [--expect-hash=<combined>] [--author]`

- **Renders** (bare.mjs, Chromium, 375 px, dsf 2): 12 frames at k/12 of the cycle, k = 0..11 (frame 1 is the t=0 still, the reduced-motion view); the same frames with `--no-text`; for pairwise, the rc2 version's frames. The rc2 version defaults to the `v1.0-rc2` tag's part page with this tree's assets. A figure that does not animate renders one frame: `judge` is then n/a (the still is the whole figure), the still and the one-frame text-stripped still carry the test, and pairwise compares one frame against twelve when needed. Exception from section 15: for the job "real thing", whose still is not scored on the mechanism (D1), the still's description stands in for the judge's, scored and hedge-checked as the judge's. A figure missing from rc2 (a merge, a new figure) gets pairwise n/a.
- **Judge packet**: the book's prose up to the figure, with every figure card (label, picture, caption, strip), every other `<svg>`, scripts, styles and navigation removed, and (from section 16) the held material of `tests/pass31/held-strip.json` removed. Caption, strip, `<title>`, `<desc>` and intent are never in it.
- **Testers**: each is a fresh headless session, `claude -p --model claude-sonnet-5-5 --safe-mode --restricted --tools "" --strict-mcp-config --no-session-persistence`, run in a new empty directory under the system temp directory (outside any repo; removed afterwards), with stream-json input holding only its prompt and images. An unreadable reply or a failed spawn is retried (three attempts, 15 s and 30 s apart).
- **Describers** (round 1): the judge (12 frames), the still (t=0), the text-stripped judge, and the two pairwise orders. Each describer names `cause_drawn`, the drawn thing that shows the cause, or "none". The judge and the still list `unexplained_words` (each with its reason) and `unexplained_marks` separately.
- **Checks** (round 2): one scorer per description and one hedge check per description (judge, still, stripped), each asked **three times** in fresh sessions; the majority decides. The description is fixed, so the votes damp only the checker's noise in applying its rules.
- **Criteria** (the verdict names the first failed one in this order):
  1. `taught` (mechanical): every `<text>` token is a number or sign, a term `known-terms.mjs` lists before the section (or the section teaches before the card, or, for an all-capitals abbreviation, the prose paragraph that first uses it comes before the card), an everyday word, or a proper name from the glossary that the prose before the figure already uses (`lib.mjs taughtYet`, brief section 15; the rules as revised in sections 13.1, 15.1, 16.2 and 17.1: held material and figure cards teach nothing, known-terms places a term at its first prose gloss and reads paragraphs and list items only, a token that is neither a glossary term nor an everyday word passes when a paragraph or list item before the card writes it, and only an entry known-terms lists as a name is credited by being mentioned, in a paragraph or list item).
  2. `judge`: (a) the judge describes the 12 frames; (b) the scorer compares that description with the intent for the job: mechanism (with the cause drawn), unexplained (any unexplained word fails), carried by the picture, one scene shown once, few words.
  3. `hedge`: (c) the hedge check on the judge's, the still's and the text-stripped descriptions, each in its own scope (section 7, item 1). Any of the three failing fails `hedge`.
  4. `still`: (d) the t=0 still alone, described and scored (mechanism with the cause drawn, unexplained, few words).
  5. `stripped`: (e) the text-stripped strip, described and scored for what moves and what causes what, with a drawn cause.
  6. `pairwise`: (f) candidate against rc2, both orders in every run. It fails only when rc2 is judged better in both orders. Byte-identical frames skip the call (SAME).
- **Decision** (from section 14, the author's decision D3): the figure passes when at least two of three independent complete runs pass, each run everything in this section (fresh renders, fresh describers, fresh votes). Runs 1 and 2 run in parallel; run 3 is made only when they disagree, and decides. A run ending in a tool error is made again once; a second error makes the decision `error`. A failed decision names the criteria its failing runs failed, most often first. The rule applies to every figure the gate judges (fig:dev, fig:validate, Phase 2).
- **Verdict**: `<out>/verdict.json` (the decision, the rule and each run's result; each run's own `<out>/run-k/verdict.json` holds every reply, every vote and the gate's fingerprint) and one JSON line on stdout: `{"id","pass","failed","failed_all"}`; with `--author` only `{"id","pass","failed"}`. Exit 0 pass, 1 fail. A tool failure (render, CLI, unreadable replies after three attempts, a refused `--expect-hash`) gives `failed: "error"` and exit 2, never a criterion name.

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

## 12. Full prompt texts (tests/pass31/prompts.mjs, sha256 `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`, the try26 configuration; frozen 2026-10-24, sections 14 and 15)

The frozen text of `dd51d25` (sha256 `529f80b3...`) and the try25 text (`b54ca44c...`, commit `2428273`) are in git history. Every tester gets `SYSTEM` as its system prompt and one user message. `JUDGE`, `STILL`, `STRIPPED` and `PAIRWISE` are followed by the images: for 12 frames each is preceded by a line `Frame k of 12 (t = ... s of a ... s loop):` (pairwise: `Version A, Frame k ...`); a one-frame figure's image is preceded by `the still picture:`; the still tester's image by `The still:`. `SCORER` and `HEDGE` get text only.

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
// (from revision 1 of the follow-up, try26: a rule of its own, not the base rule with exceptions, which the scorer
// sometimes applied over them)
const UNEXPLAINED_REAL = `unexplained (real thing): this job draws the object as it looks, so the words, letters and numbers that are part of drawing it are expected: a part's name, or one label naming parts (a key, a wheel, a lamp, a reflector, a cabinet, or two part names on one label), the letters or numbers written on a part (a key's letter, a wheel's position letter), a legend for the drawing's colours or lines, and a short note on the drawing saying what a part does or how the drawing simplifies the object, with every word in that note. None of these counts, in either list, even when the reader had to guess it or the text never used it (a separate mechanical check makes sure every such word is an everyday word or taught before the figure). The test fails only if "unexplained_words" lists a word tagged onto a part to name a state, mode or condition it is in that neither the picture nor the text explains (for example a part tagged "· ready"), or if an entry in "unexplained_marks" shows that the reader could not tell what object is drawn. Judge only these two lists here (doubts in "unsure" are scored elsewhere).`;
const UNEXPLAINED_TEST = job => job !== 'real thing' ? UNEXPLAINED_BASE : UNEXPLAINED_REAL;
const OBJECT = `object: the description recognises the real object or scene the intent names, its parts drawn with their own physical features (for example wheels with their rows of contacts and the wiring inside them, round keys and lamps). It fails only when the parts are plain boxes or labels with nothing of the part drawn in them (at most a name, a letter or a number), joined by arrows or lines, or when the figure is a table, a timeline or text in a frame. Parts drawn with their own detail pass even when the reader calls them boxes or the drawing a diagram.`;
// the still of a real thing (author decision D1, 2026-10-24): it passes when it shows the real object as it looks, its
// parts identifiable; the mechanism is carried by the animation (the 12-frame judge) and is not tested on the still
const OBJECT_STILL = `${OBJECT} The parts must also be identifiable: the reader names them, or tells them apart by their own features.`;
// a real thing's cause is its part changing as drawn; how that change gives the result inside the object is function
const REAL_CAUSE = ` For this job (real thing), the cause is drawn when the part the intent names is drawn changing (it moves or steps, or its position letter or drawn state changes); how that change produces the result inside the object is not tested, so a reader who says nothing shows how it does so does not fail this test.`;
const RUBRIC = {
  judge: job => `Score the description against the intent. PASS only if every test below passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: the same thing changes, for the same cause, with the same result. Paraphrase is fine and extra correct detail is fine. It fails if what changes, why, or the result is missing, vague or wrong, or if the description gives a different mechanism, a different representation or a different example than the intent names. ${DRAWN}${job === 'real thing' ? REAL_CAUSE : ''}
2. ${UNEXPLAINED_TEST(job)}
${job === 'real thing' ? `3. ${OBJECT}` : `3. carried by the picture: the mechanism is shown happening or drawn, not only written. It fails if "read_only" names a part of the mechanism (what changes, why, or the result) that the picture never shows, or if the cause is not drawn (test 1). Things moving is not enough: the picture must show what makes them move. A short result line that states what the drawn change amounts to (for example a sum, which also says what the drawn marks count) is part of this bar ("the result stated") and does not fail the test, even when "read_only" names it, as long as the change it sums up is shown happening.
4. one scene, shown once: ${job === 'two-part' ? 'at most two panels, and' : 'one panel only (the scene, with its own rule cards, keys and result line), and'} "repeated" is "none". It fails if the figure adds a separate table, list of steps, replay or block of text beside the scene, or shows the same steps twice. A short result line that states what the scene arrives at is not a repeat, even when "repeated" names it.
5. few words: the picture uses few words. It fails if "text_pieces" is more than 8 for one panel, or if the words, not the picture, carry the mechanism.`}`,
  still: job => job === 'real thing' ? `This description comes from the still alone, the frame a reader with animation turned off sees (for a figure that does not animate, the whole figure). The figure's job is "real thing": its still passes when it shows the real object the intent names as it looks, its parts identifiable. The still does not have to show what changes, why, or the result: the animation carries that, and another test scores it on the frames. So do not score the intent's mechanism here: a reader who says the still shows no change, or who gets the change, its cause or the result wrong or not at all, does not fail for that. PASS only if both tests pass; otherwise FAIL.
1. ${OBJECT_STILL}
2. ${UNEXPLAINED_TEST(job)}` : `This description comes from the still alone, the frame a reader with animation turned off sees (for a figure that does not animate, the whole figure). A still cannot move, so the change may be shown by drawn states, arrows, a before and after, drawn rules, or a stated result, and the reader may have to work the motion out. Score it against the intent: a reader who works out, from what is drawn, the same change, cause and result as the intent passes, even when the reader says the change is implied rather than seen. PASS only if every test passes; otherwise FAIL.
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
  judge: { fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'] },
  still: { fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'] },
  stripped: { fields: ['moves', 'cause', 'cause_drawn', 'result', 'unsure'] },
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
// the still of a real thing (author decision D1): judged only on showing the object as it looks, its parts identifiable
const HEDGE_REAL_STILL = d => `Below is part of a blind reader's description of a figure seen as one still picture. The figure draws a real object (a machine, a device, a place), and its still is judged only on showing that object as it looks, its parts identifiable; what changes in the object is carried by the animation and tested elsewhere. Decide whether the reader hedges on what the drawing shows.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only when it leaves open what the drawing shows: the reader cannot tell what object is drawn, or what kind of parts it has (offers two different objects, or cannot say what the parts are).
Every other candidate does NOT count, however it is worded: whether anything changes, what changes, whether the still shows a change, which part moves, what the result is or whether it changes; why or how a part moves or gives its result; what a letter, mark or note on a part stands for; why the object is built or wired as it is, or what it is for; which moment the still shows; colours, layout and how the drawing is meant. (Another test scores whether the reader saw the object.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what is drawn | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what is drawn"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
// the function (and two-part) checks on the judge's and the still's descriptions (from revision 1 of the follow-up,
// try26: narrow positive checks, as the text-stripped check, instead of "counts unless an exclusion applies")
const HEDGE_FUNCTION = (kind, d) => kind === 'still' ? `Below is part of a blind reader's description of a figure seen as one still picture, which cannot move. Decide whether the reader hedges on what makes the change happen: which drawn thing is the cause, or whether the cause is drawn at all.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "I infer", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these cases:
- it says, or leaves open, that nothing drawn shows why the change happens: the reader names no drawn thing as the cause, or says the rules or the cause are not drawn, or are only written in words. "cause_drawn" being "none", empty or only words also counts;
- it offers two different drawn things as the cause, or cannot tell which drawn thing is the cause.
Every other candidate does NOT count, however it is worded: what happens over time; what a rule's action produces (for example what "write" writes); how the drawn rules are chosen step by step; whether the end state is reached; whether the still shows the start, the end or only the rules; whether the drawn cause the reader names truly causes the change, or only shows which rule applies or goes with it; what the end state, a mark, a number or a line means; whether there is more than is drawn; colours, decoration and layout. (The reader saw one still picture, and other tests score whether the reader worked out the change and the result.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "no drawn cause | which cause | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "no drawn cause | which cause"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)` : `Below is part of a blind reader's description of a figure shown as frames of its animation. Decide whether the reader hedges on what changes, what makes it change, or where it ends up.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "I infer", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these cases:
- what changes: it leaves open WHICH thing changes or moves, or whether anything changes (the reader cannot tell, or offers two different things);
- what makes it change: the reader names no drawn thing as the cause, says the rules or the cause are not drawn, or are only written in words, or offers two different drawn things as the cause. "cause_drawn" being "none", empty or only words also counts;
- where it ends up: the reader cannot say what the end state is, offers two different end states, or doubts that it stops while nothing drawn shows a stop (holding still while a rule card or light stays lit is a drawn stop);
- a field about these ("changes", "cause", "cause_drawn", "result") is missing, empty or vague.
Every other candidate does NOT count, however it is worded:
- a doubt that names the drawn thing that shows the point and asks only whether it is really meant that way, or whether it truly causes the change or only shows which rule applies or goes with it (for example "the head stays put with the stop card lit, but does the machine truly stop?");
- what the end state, a mark, a number or a line means (whether marks stand for a number, whether a written sum states the task or the answer, which mark is the "+ 1"): another test scores the meaning;
- how a drawn rule or card depicts its condition or its action (what it shows or leaves out), while the change itself is stated;
- whether there is more to the thing than is drawn (another part, a hidden state);
- timing: a pause, a frame where nothing is lit, a frame caught between two positions, the order of events inside one step; the loop starting again;
- colours, decoration and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what changes | why | end state | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what changes | why | end state"}], "hedged": true}
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
  if (job === 'real thing') return kind === 'still' ? HEDGE_REAL_STILL(d) : HEDGE_REAL_THING(kind, d);
  return HEDGE_FUNCTION(kind, d);
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

*Kept as the record. The fresh builder's section 14 continues from here and re-froze the gate; where 13 and 14 differ, 14 holds.*

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

## 14. The fresh builder (2026-10-24): the author's decisions D1 to D3, one prompt revision, frozen

*Kept as the record of try26. The review of this freeze and its five code fixes are in section 15, which re-froze the gate at `4095d1aa...`; where 14 and 15 differ (the fingerprint, the hashed files, validate.mjs, the validation command, the development set), 15 holds.*

The configuration left by section 13 (try25) was not frozen. A fresh builder (brief section 10's pattern: a single attempt) was given the author's decisions D1 to D3 (the owner delegated these calls; they amend the brief and are not prompt wording), a cap of **at most three prompt revisions** across build, review fixes and freeze, numbered from try26, and the bar below. It read sections 12 and 13 and the code first. It did not check out, render, diff or read commit 93aae05, read nothing under `docs/pass-31-sealed/` (the validation runner was tested on a scratch manifest in its scratch directory, section 14.2), opened no figure from the book's security chapters, and only read `figures-final`'s ledger and brief (the ledger is copied per attempt, as before). Of the three revisions it used **one**: the bar held after it, so the gate is frozen at try26.

**The bar** (all must hold under the final decision rule, three independent evaluations of each item): v1 and v2 fail every time; every decoy fails every time; v4 and Enigma pass every time.

### 14.1 The author's decisions (brief amendments)

- **D1. Real-thing still.** For a figure whose job is "real thing", the t=0 still passes when it shows the real object as it looks, its parts identifiable; it does not have to show the mechanism, which the strip's motion carries. The text-stripped strip for a real-thing figure passes when the object and what moves remain visible. (Brief section 4: Enigma's Pass 30 reader could not say what the machine was for, and under its real-thing job that is not a failure.)
- **D2. Taught-yet.** Section 13.1 item 1's route stays: an everyday word of four letters or more, set in capitals, passes when the book never writes it in capitals; every abbreviation the book uses and every token of three letters or fewer still needs teaching.
- **D3. Stability.** The gate's decision for a figure may aggregate independent complete gate runs, each run itself as before. Choosing and implementing the rule is code and does not count toward the cap; the rule applies to every figure the gate ever judges, validation included.

### 14.2 The decision rule (D3: code in `gate.mjs`, not counted toward the cap)

- **Rule: a figure passes when at least two of three independent complete runs pass.** Each run is the whole gate of section 2 (fresh renders, fresh describers, its own three votes per check, its own pairwise pair). Runs 1 and 2 run in parallel; run 3 is made only when they disagree, and decides, so the outcome is always the one all three runs would give. A run that ends in a tool error is made again once; a second error makes the decision `error` (exit 2), never a criterion name. A failed decision names the criteria its failing runs failed, most often first (ties in the gate's order). `fig:gate` makes a decision by default; `--single` makes one complete run (the decision's building block, never a verdict on a figure). `<out>/verdict.json` holds the rule, each run's result and the decision; each run's full record is in `<out>/run-k/verdict.json`. A run reporting a different fingerprint from the decision's is a tool error.
- **Why two of three.** The noise is in the describers: in try22 to try25 the function prompts were byte-identical and v4 passed 7 of 12 runs (try20 to try25: 12 of 18), with the failures spread over single readers' doubts. A majority vote damps false fails and false passes alike wherever a single run is right more often than not. "At least one of three" would have cut v4's false fails further but roughly triples the chance of a false pass on a borderline figure, against brief section 10's "zero false passes is the bar"; "three of five" costs more for little gain at the observed rates. The rule does not help a figure near even odds (section 14.8).
- **Where it applies.** `fig:validate` and `fig:dev` call `gate.mjs`, so every validation item is one decision and every development evaluation is one decision; Phase 2 runs `fig:gate`. The rule lives in `gate.mjs`, which the combined fingerprint hashes, so `--expect-hash` refuses any other rule.
- **`dev.mjs`** (not hashed): `--runs=3` now means three evaluations per item, each a decision (6 to 9 complete runs); the summary records every run and each item's complete runs passed. **`validate.mjs`** (not hashed): unchanged except its header comment.
- **Checks of the plumbing.** Taught-only decisions (`--criteria=taught`, no tester calls): v4 PASS (2 of 2 runs, exit 0), v1 FAIL on `taught` (0 of 2, exit 1). A forced tool error (an rc2 revision that does not exist): each run made again once, then `failed: "error"`, exit 2. A wrong `--expect-hash`: refused, exit 2. `fig:validate --expect-hash=f8353940...` on a scratch manifest in the builder's scratch directory (stand-ins only: v1 as v3, v4, decoy2 as a tapped worst; no tapped best): `HOLDS: v3 failed 1 of 1; v4 passed 1 of 1; tapped worst failed 1 of 1; tapped best passed 0 of 0; tool errors 0; takeaways from the ledger 3 of 3`, each item decided on two runs (v4 2 of 2 passed; the others 0 of 2). These stand-in runs are not part of the bar.
- **Cost.** A decision is two or three complete runs: about 46 to 69 tester calls for a figure with pairwise, 42 to 63 without.

### 14.3 D2: taught-yet unchanged

`tests/pass31/lib.mjs`, `tests/pass31/common-words.txt` and `scripts/known-terms.mjs` are as committed in `fd4c94e` (sha256 in section 14.7). `npm run fig:taught-test`: 19 of 19 cases hold at the freeze (Figs 1.1 and 1.2 clean; LAMP, REFLECTOR, ROTORS pass; ARM, RAM, OS, MAC, LAN, CPU fail until taught; AX, AL, DOS fail).

### 14.4 Revision 1 (try26), the only prompt revision

1. **D1, the real-thing still's scorer.** For the job "real thing" the still is scored on two tests: `object` (section 12's object test, plus "the parts must also be identifiable: the reader names them, or tells them apart by their own features") and `unexplained (real thing)` (item 3). The mechanism is not scored on a real thing's still: the rubric says the still does not have to show what changes, why or the result, and that a reader who says the still shows no change, or gets the change wrong, does not fail for that. The function and two-part still rubrics are unchanged.
2. **D1, the real-thing still's hedge check**: a check of its own that counts only a doubt about what object, or what kind of parts, is drawn; doubts about whether or what anything changes, the result, how parts work, what letters or notes stand for, which moment is shown, colours and layout do not count.
3. **The real-thing unexplained test** (judge and still) stated as a rule of its own instead of the base rule with exceptions: in try25 the still's scorer counted "KEY · LAMP" and "steps" (from the note "steps each press") under the base rule by two votes of three, although the exceptions named part names and notes. Now part names (or one label naming two parts), letters and numbers on parts, legends and short notes on the drawing, with every word in the note, do not count; the test fails only on a word tagged onto a part to name an unexplained state, mode or condition, or a mark entry showing the reader could not tell what object is drawn.
4. **The function (and two-part) hedge checks on the judge and the still** rewritten as narrow positive checks, as the text-stripped check has been since try12. Judge: a candidate counts only when it leaves open which thing changes (or whether anything does); names no drawn cause, says the cause is not drawn or only written, or offers two different drawn causes (`cause_drawn` "none", empty or only words counts); cannot say the end state, offers two, or doubts a stop that nothing drawn shows (holding still under a lit card is a drawn stop); or when a field about these is missing, empty or vague. Every other kind is listed as not counting: a doubt naming the drawn evidence and asking only whether it is meant that way or truly causes the change rather than showing which rule applies; the meaning of the end state, a mark or a line; how a drawn rule or card depicts its condition or action while the change itself is stated; more than is drawn; timing and the loop; colours, decoration, layout. Still: counts only a missing drawn cause or two different drawn causes; over-time questions, what a rule's action produces, start or end, whether the drawn cause truly causes, meaning, more than drawn, colours and layout do not count. Reason: four of v4's five false fails in try22 to try25 were hedge checks counting, with all three votes, doubts of kinds the old exclusions already named (a pause in a frame where nothing is lit; whether the lit card causes the step or only shows the rule; whether the still shows the head's start; why the "write, stop" card does not show what is written). The old check opened with "every candidate counts unless a rule further down says it does not" and "it does not matter that another field states the point plainly", and the checkers applied that over the exclusions.

Renderings checked against try25 by rendering every prompt with both texts: changed are the scorer for real thing (judge: item 3; still: items 1 and 3), the real-thing still hedge (item 2) and the function and two-part judge and still hedges (item 4). Unchanged: the system prompt, the judge, still, text-stripped and pairwise prompts, every function and two-part scorer, every text-stripped scorer, the real-thing judge hedge and every text-stripped hedge.

### 14.5 Attempts

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26 | `f8353940d3dc` | `781262c1` | revision 1 (section 14.4); the decision rule (section 14.2, code) | **9 of 9** | **12 of 12** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 7, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6 |

Full fingerprint: try26 `f8353940d3dc75c2877751a0b823751afbef5d15e231df28c0c8316cbb1dbd0a`; prompts.mjs `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`; gate.mjs `73632dbc8309386899113a2186ed4fd9ecb1a8b22d5eb9303c47e0778f59dee5`. Ledger (`figures-final`'s working file, copied into the attempt folder) sha256 `e8396779dc93c5f25f5f9a452a104d171babe1486872d5f32d57e358a02c2011`, the same file as try24 and try25: Fig 1.1 "Function: the head walks right past each mark and marks the next blank, so three marks become four." (function); Fig 1.2 "Real thing: the rotors step before each press, so the same key lights a different lamp every time." (real thing). CLI 2.1.310. 24 evaluations, 49 complete runs.

### 14.6 Every evaluation, try26

Evaluation: one gate decision. Order: the first pairwise order passed to each of its runs (both orders are asked in every run). Hedge in: per run, the descriptions whose hedge check failed (n/a where the run had no hedge result).

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26 | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26 | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26 | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26 | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26 | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26 | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26 | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26 | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: CANDIDATE |
| try26 | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26 | Enigma | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26 | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26 | Enigma | 3 | random | PASS | PASS | 2 of 3 | run 1 PASS; run 2 FAIL (still); run 3 PASS | run 1: none; run 2: none; run 3: none | run 1: SAME (identical frames); run 2: SAME (identical frames); run 3: SAME (identical frames) |
| try26 | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26 | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26 | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26 | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still) | run 1: judge, still; run 2: judge, still, stripped | not run |
| try26 | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still | not run |
| try26 | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still, stripped; run 2: judge, still | not run |
| try26 | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, hedge, still) | run 1: none; run 2: judge | not run |
| try26 | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26 | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26 | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26 | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: none; run 2: stripped | not run |
| try26 | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: none; run 2: stripped | not run |

Sub-tests the scorers failed by majority, per complete run (6 runs per item, 7 for Enigma): v1 fails judge mechanism, unexplained, carried by the picture, one scene, few words, still mechanism, unexplained, few words and stripped both tests 6 of 6, and `taught` every run. v2 fails judge one scene and few words 6 of 6, judge unexplained 5 of 6, still unexplained 6 of 6, still few words 4 of 6; its mechanism passes. decoy1 fails judge mechanism, unexplained and carried by the picture 6 of 6, still mechanism 6 of 6, still unexplained 5 of 6, stripped both tests 6 of 6. decoy2 fails still mechanism and unexplained 6 of 6, judge mechanism, unexplained and carried by the picture 5 of 6, stripped "what causes what" 2 of 6. decoy3 fails judge and still unexplained 6 of 6 ("adding"). decoy4 fails judge mechanism and object, still object, stripped object and "what changes" 6 of 6. Enigma failed one sub-test in one run: the still's object test (evaluation 3, run 2: two votes of three read the drawing as a schematic wiring diagram of labelled columns rather than a machine), which the decision absorbed (2 of 3 runs passed). v4 failed no criterion in any run. The hedge criterion failed in decoy1 every run (judge, still, stripped), decoy2 every run (judge and still), decoy3 in 1 of 6 runs and decoy4 in 2 of 6 (stripped); never in v1, v2, v4 or Enigma. Pairwise: rc2 (v4) was judged better than v1 and v2 in all 24 replies; v4 against its rc2 version gave SAME or CANDIDATE; Enigma's frames are byte-identical to its rc2 version (SAME, no call). Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6.

### 14.7 Frozen (2026-10-24), and the total attempt count

*Superseded by section 15.3 (fingerprint `4095d1aa...`): the values below are try26's.*

The bar holds at try26: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (12 of 12 decisions, 0 of 24 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3, 6 of 7 runs). The gate is **frozen** at this configuration. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. `npm run fig:hash` reproduces these values; run the validation as `npm run fig:validate -- --expect-hash=f8353940d3dc75c2877751a0b823751afbef5d15e231df28c0c8316cbb1dbd0a`.

SHA-256 of each judge prompt, rendered by `prompts.mjs frozenTexts()` with placeholder inputs (as in section 11: the scorer hash covers its 9 renderings, the hedge hash its 9 (judge, still, stripped × function, real thing, two-part), the stripped hash its 12-frame and 1-frame forms, the pairwise hash its 4 frame-count forms):

| Prompt | SHA-256 (frozen 2026-10-24, try26) |
|---|---|
| judge (12 frames) | `fd5e2c7a8461beb9dff9f129e4f7e5dc62398d55b8661b4fdc58109bef053b20` |
| scorer | `45189b5643f385c8fc8c49fa1520d667c3f55b3f871a07996b019a14a7ff6b92` |
| hedge | `5a558534d8e04f704e484ba14ff475c9c59fadd37994479a134ca2b4d33e2565` |
| t=0 still | `87a0a088b55e0fed246c5438fc51cd259a7dad76a57c81369e414d8b6eef4a76` |
| text-stripped | `d9a1570d7e9cbd2c36257640055d1643717f3f8330bb53625f52717f9a75a2ab` |
| pairwise | `382b5b6a0f2f9ad0da3b1bc312745682cdd88f216c4bef7cb148acf4b2b1b50e` |
| system (every tester) | `32e914caf96b78905a2c020a696e70eb2c9b64c4c921574c0373d890eb223aeb` |

| File the gate runs | SHA-256 (frozen 2026-10-24, try26) |
|---|---|
| `tests/pass31/gate.mjs` | `73632dbc8309386899113a2186ed4fd9ecb1a8b22d5eb9303c47e0778f59dee5` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `e434d7b23064fd6a9db5c5813c3fc7919b5cb3a9295063cfc0f7cfbdab008aee` |
| `tests/pass31/hash.mjs` | `9588a724f1afea94b2b0d1dd4226dedb87a3d65275dafbc80e059fb126a04748` |
| `tests/pass31/common-words.txt` | `f0d41e5dbd1733127522c760c9feedc586d92a1717bd6c1c7ccdb651ef46a25e` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `94fc69f6f64c2ba82a73eb79eb029febb26f98a68eafb8c6c26a6e0346663350` |

- Decision rule: at least 2 of 3 independent complete runs pass (in `gate.mjs`, section 14.2). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `f8353940d3dc75c2877751a0b823751afbef5d15e231df28c0c8316cbb1dbd0a`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.

**Total prompt attempts: 27** (for the READY page): try0 to try21 before session e2's follow-up (the first freeze was try20 and try21's configuration), try22 to try25 in the follow-up (one rerun, then three revisions), and try26 by the fresh builder (one revision of the three allowed). Each attempt ran every item three times; from try26 each of those three is a decision of two or three complete runs.

### 14.8 Known limits added by the fresh builder

- **The bar was measured once.** No repeat attempt followed try26: the cap and bar define the measurement as three evaluations of each item under the final rule (24 decisions, 49 complete runs). v4 passed 6 of 6 complete runs in try26 and 2 of 2 in the scratch validation test; with the previous hedge check it passed 12 of 18 (try20 to try25). Validation needs v4 to pass one decision.
- **The function hedge is narrower.** It now counts only open alternatives on what changes, the drawn cause or the end state, plus missing or vague fields. It still fails decoy1 and decoy2 every run, but no longer fires on v1 (0 of 6 runs; 10 of 12 in try22 to try25). v1 fails `taught`, `judge`, `still` and `stripped` every run, so no development verdict depends on the hedge; as a backstop for validation it is weaker than before. Like the earlier loosenings, the change was found on Fig 1.1.
- **D1 removes the mechanism from a real thing's still.** A reduced-motion reader of a real-thing figure is guaranteed the object, not what changes in it; that is the author's decision under brief section 4. The 12-frame judge still tests the mechanism for a real thing, and the text-stripped strip what changes.
- **Two of three helps only where a run is right more often than not.** A figure near even odds per run stays near even odds per decision, and a decision costs two to three times the tester calls of one run. Enigma's one failed run (the still's object test) shows a single reader can still read its drawing as a schematic.
- **Real-thing handling is still tuned on one real thing** (Enigma) and one real-thing decoy (decoy4); no second real-thing figure has been run.
- The other limits of sections 10 and 13.5 stand (tester context, CLI version outside the hash, Chromium only, unexplained words depending on the describer, the ledger read from `figures-final`'s working file).

## 15. The review of the try26 freeze (2026-10-24): five code fixes, rerun, frozen

*Section 14 stays as the record of try26; where 14 and 15 differ, 15 holds. Section 16 supersedes 15.3's fingerprint, file hashes and validation command.*

An independent review of the try26 freeze (commit `355c41f`, fingerprint `f8353940...`) reproduced the builder's record (fingerprint, file hashes, `summary.json`, taught-test 19 of 19, the ledger read by header, the D3 rule on stubbed runs) and reran the bar itself (13 items, 39 decisions, 79 complete runs, no pairwise): v1, v2, decoy2, decoy3 and six of its seven new decoys failed every decision and v4 and Enigma passed every decision, but the seventh, Fig 1.2 frozen at t=0 (not animated), passed 1 of 3 decisions. It returned **NOT READY** over three code defects and two small ones. The same builder fixed all five in code (commit `88dc4d1`). `tests/pass31/prompts.mjs` is unchanged (sha256 `781262c1...`, the try26 text, every prompt hash as in section 14.7), so the prompt revisions used stay at **1 of 3** and the prompt-attempt count at **27**. The fingerprint changed (gate.mjs, lib.mjs, hash.mjs, and validate.mjs added to it), so the bar was rerun under the new fingerprint (try26-fix) before the freeze. The builder did not check out, render, diff or read commit 93aae05, read nothing under `docs/pass-31-sealed/`, and only read `figures-final`'s ledger and brief.

### 15.1 The fixes (code, not counted toward the cap)

1. **A real thing that does not animate** (`tests/pass31/gate.mjs`). Before: a figure rendering one frame had `judge` n/a, and under D1 a real thing's still is not scored on the mechanism, so for a static real thing no criterion scored the takeaway's mechanism (the review's static Enigma, Fig 1.2 frozen at t=0, passed 1 of 3 decisions on the object alone). Now, for a figure that does not animate whose job is "real thing", the still's description stands in for the judge's: `judge` is the judge's scorer (the real-thing rubric, the rendering used for every animated real thing) applied to the still's description, and the hedge check adds the judge's real-thing scope on the same description (`failed_in` names it `judge`). The verdict marks both `stand_in: "still"`. Static function and two-part figures are unchanged (`judge` n/a; their still rubric already scores the mechanism). No prompt text changed: both renderings were already in use. The review's offline rescore of its 13 static descriptions with this scorer failed 13 of 13 (0 of 3 votes each). Guarded in the development set by **decoy5** (`tests/pass31/dev.mjs`): Fig 1.2 at its t=0 state, every animation removed and each animated opacity set to its first value, job "real thing", expected FAIL (it renders one frame, byte-identical to Enigma's t=0 still).
2. **Taught-yet, short abbreviations in lower or mixed case** (`tests/pass31/lib.mjs` `taughtYet`). Before: a lowercase or title-case token passed when `/usr/share/dict/words` held it (ax, al, arm, ram, mac, os, lan, dos and Ram, Arm, Mac, Os, Lan, Dos passed at Fig 1.1; rax at Fig 3.1, lo at Fig 8.5), and a known term took an s or es ending whatever its length (css passed as CS plus s at Fig 11.14). Now:
   - a token of two or three letters, not all capitals, fails as "an abbreviation not taught before the figure" when its capitalised form is one the book writes in capitals (`known-terms.mjs` `capitals`) or it is one of brief section 15's dictionary abbreviations (`SHORT_ABBR`: ax, al, arm, ram, nat, lan, dos, plus mac and os from the review), unless the token itself is on the COMMON list in exact form (add, get, put, not, in, it, as, at, us, or, and, out, net pass);
   - a plain s plural of a word of two or three letters that the book writes in capitals fails the same way (rams, macs, arms), unless that word is on the COMMON list (adds, puts, gets pass, as brief section 15 requires of inflections);
   - a taught term of two letters or fewer takes an s or es ending only when written as the abbreviation (IPs, PCs, OSes); css, ips keep their ending and are checked as tokens.
   The check runs after the glossary-term check and the all-capitals branch, before the everyday-word check, so the dictionary cannot make these tokens everyday. **Where this departs from the review's wording:** the review named common-words.txt's left-out list; that list also holds words left out because they are not English words (non, re, mar, san, de, en, la, st, york), and using it whole failed everyday text in the book (non-volatile at Figs 3.11 and 15.2, re- at Figs 4.1, 13.7 and 15.4, Mar at Fig 11.1, San at Fig 13.1, which flipped to a fail). `SHORT_ABBR` holds the abbreviations brief section 15 names; every other left-out word that the book writes in capitals (AM, CA, ID) is caught by `capitals`. A rule that no stem of one letter makes a token everyday (js, ms) was tried and dropped: it failed units and possessives across 16 figures (ms, ns, vs, A's), and js is caught anyway because the book writes JS.
   Effect on the book (every figure, the rc2 tree in this worktree's `public/`): 174 of 222 fail taught-yet with the try26 rules, 175 with these; one figure flips to a fail (fig-8-5, lo), none flips to a pass; the new failing tokens are rax (fig-3-1), al (fig-3-3), ast (fig-4-1), lo (fig-8-5), css (fig-11-14); no token stops failing. On `figures-final`'s `public/` (read only): 171 of 221 to 172, the same flip and the same five tokens; Figs 1.1 and 1.2 stay clean. `npm run fig:taught-test`: 30 cases, 30 hold (the 19 of section 13.1, plus: the eight abbreviations in lower and in title case fail at Fig 1.1; rams, macs, arms fail at Fig 1.1; add, adds, added, adding, puts, gets, not, non-volatile, re-read, Mar, 10 ms pass at Fig 1.1; ram, os, arm, rams, arms, CPUs, RAMs, OSes pass at Fig 3.2 once taught; IPs passes and ips fails at Fig 10.3; rax fails at Fig 3.1, css at Fig 11.14, lo at Fig 8.5, ast at Fig 4.1).
3. **Validation without the ledger** (`tests/pass31/validate.mjs`). Before: with no ledger at the default path (the gate branch keeps none) every item was silently scored against the manifest's own intent, a missing job defaulted to function, and the run still exited 0 or 1. Now a missing or unreadable ledger is incomplete (exit 2, nothing run, nothing logged), a manifest fallback item needs both an intent and a valid job (function, real thing, two-part) or the run is incomplete (exit 2), and the command names the ledger: `npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=<combined>` (the full command with the frozen hash is in section 15.3).
4. **validate.mjs in the fingerprint** (`tests/pass31/hash.mjs` `GATE_FILES`): the validation bars and the takeaway source can no longer change after the freeze without changing the combined hash, which `--expect-hash` refuses. `tests/pass31/dev.mjs` (the tuning harness, which judges no figure) stays outside it; its sha256 is recorded in section 15.3.
5. **A repeated header name in the ledger** (`lib.mjs readLedger`) now throws (gate exit 2, validation incomplete) instead of letting the last column win.

**Checks of the plumbing** (scratch only, no tester calls): `fig:validate` with `--ledger` pointing at a missing file, with no `--ledger` (no ledger in this worktree), with a manifest item outside the ledger that has an intent but no job, and with a ledger whose header names `intent` twice: each printed one "incomplete" line and exited 2, writing nothing; `fig:gate` with the twice-named ledger exited 2. The real ledger still reads (222 rows). Taught-only decisions (`fig:dev --criteria=taught`, every item, one evaluation): v1 FAIL on `taught` (0 of 2 runs), every other item PASS on `taught` (2 of 2), decoy5 rendered one frame and Enigma twelve.

### 15.2 The rerun: try26-fix (the try26 prompts, the fixed code)

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26-fix | `4095d1aa77eb` | `781262c1` (as try26) | review fixes 1 to 5 (section 15.1, code only) and decoy5 | **9 of 9** | **15 of 15** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 7, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6, decoy5 0 of 6 |

Full fingerprint `4095d1aa77eb8bb4dc4bcffd75a1540bdce7468e6c20c7e1cdfe9aa542840286` (every run reported it); ledger (`figures-final`'s committed working file at `832cb0d`, copied into the attempt folder) sha256 `cab20cf0c5d630b2a8bb2f1daf045005daa107b2c746cf0905505a33aceacc89`, a later file than try26's (`e8396779...`; the author edited other rows) with the same two takeaways: Fig 1.1 "Function: the head walks right past each mark and marks the next blank, so three marks become four." (function); Fig 1.2 "Real thing: the rotors step before each press, so the same key lights a different lamp every time." (real thing). CLI 2.1.310. 27 evaluations, 55 complete runs, 1,188 tester calls, no tool error, no run made again. Output: `tests/pass31/out/dev/try26-fix/summary.json` (with snapshots of the six scripts).

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26-fix | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-fix | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-fix | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-fix | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-fix | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-fix | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-fix | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-fix | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-fix | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-fix | Enigma | 1 | cand-first | PASS | PASS | 2 of 3 | run 1 PASS; run 2 FAIL (hedge); run 3 PASS | run 1: none; run 2: judge; run 3: none | run 1: SAME (identical frames); run 2: SAME (identical frames); run 3: SAME (identical frames) |
| try26-fix | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-fix | Enigma | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-fix | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, stripped | not run |
| try26-fix | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-fix | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-fix | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still | not run |
| try26-fix | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-fix | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still; run 2: judge, still, stripped | not run |
| try26-fix | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-fix | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-fix | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-fix | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: stripped; run 2: none | not run |
| try26-fix | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: none; run 2: stripped | not run |
| try26-fix | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-fix | decoy5 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |
| try26-fix | decoy5 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, stripped); run 2 FAIL (stripped) | run 1: judge; run 2: none | not run |
| try26-fix | decoy5 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |

Sub-tests the scorers failed by majority, per complete run (6 runs per item, 7 for Enigma): v1 fails judge mechanism, unexplained, carried by the picture, one scene and few words, still mechanism, unexplained and few words, stripped both tests 6 of 6, and `taught` every run. v2 fails judge one scene and few words 6 of 6, judge unexplained 5 of 6, still unexplained and few words 6 of 6; its mechanism passes. decoy1 fails judge mechanism, unexplained and carried by the picture, still mechanism and unexplained and stripped both tests 6 of 6. decoy2 fails judge mechanism and carried by the picture, still mechanism and unexplained 6 of 6, judge unexplained 4 of 6. decoy3 fails judge and still unexplained 6 of 6 ("adding"). decoy4 fails judge mechanism and object, still object, stripped object and what changes 6 of 6. **decoy5** fails stripped "what changes" 6 of 6 and the stand-in judge's mechanism 4 of 6: in the other two runs (evaluation 1 run 1, 3 votes of 3; evaluation 2 run 2, 2 of 3) the scorer took the note "steps each press" with the first rotor's position letter as the drawn cause; its still passes 6 of 6 (D1: the object). Enigma failed one check in one run: the judge-scope hedge (evaluation 1, run 2: two votes of three counted a doubt about the result), which the decision absorbed (2 of 3 runs). v4 failed no criterion in any run. Hedge failed in decoy1 and decoy2 every run, decoy4 2 of 6, decoy5 1 of 6, Enigma 1 of 7, never in v1, v2 or v4. Pairwise: rc2 (v4) judged better than v1 and v2 in all 24 replies; v4 against its rc2 version SAME or CANDIDATE; Enigma's frames byte-identical to rc2 (SAME, no call). Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6.

**Validation runner, scratch stand-ins only** (`fig:validate --sealed=<builder's scratch> --ledger=<figures-final ledger> --expect-hash=4095d1aa...`, manifest in the builder's scratch directory: v1 as v3, v4, decoy5 as a tapped worst, Enigma as a tapped best; nothing under `docs/pass-31-sealed/` read or written): `HOLDS: v3 failed 1 of 1; v4 passed 1 of 1; tapped worst failed 1 of 1; tapped best passed 1 of 1; tool errors 0; takeaways from the ledger 4 of 4` (exit 0), each item one decision of two runs (v4 and Enigma 2 of 2 passed, the others 0 of 2), every run at `4095d1aa...`. These stand-in runs are not part of the bar.

### 15.3 Frozen (2026-10-24), and the total attempt count

The bar holds under the fixed gate: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (15 of 15 decisions, 0 of 30 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3, 6 of 7 runs). The gate is **frozen** at this configuration, which replaces section 14.7's. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. `npm run fig:hash` reproduces these values. Run the validation as:

`npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=4095d1aa77eb8bb4dc4bcffd75a1540bdce7468e6c20c7e1cdfe9aa542840286`

(the ledger is the author's `docs/pass-31-ledger.tsv` on `figures-final`; the gate branch keeps none, and without `--ledger` the run stops as incomplete).

Prompt hashes: unchanged from section 14.7 (judge `fd5e2c7a...`, scorer `45189b56...`, hedge `5a558534...`, t=0 still `87a0a088...`, text-stripped `d9a1570d...`, pairwise `382b5b6a...`, system `32e914ca...`); the full text in section 12 is the frozen text.

| File the gate runs | SHA-256 (frozen 2026-10-24, try26-fix) |
|---|---|
| `tests/pass31/gate.mjs` | `4ef9614020c0eefe6fa7963e813f2a923cd88eca2c4d274c1bb8a0fc83cf2796` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `aeaadd7b15c757e090816edee42423d0ebd6f852afef0834998c6bc2567aed74` |
| `tests/pass31/hash.mjs` | `41efca3f4cc634dd57f1af2def1af32f457390f3bd372b91cbe5a1ebc5753715` |
| `tests/pass31/common-words.txt` | `f0d41e5dbd1733127522c760c9feedc586d92a1717bd6c1c7ccdb651ef46a25e` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `94fc69f6f64c2ba82a73eb79eb029febb26f98a68eafb8c6c26a6e0346663350` |
| `tests/pass31/validate.mjs` | `deb0103a56243a73f3cbcb124b41cf012f4097381a1373b7a2c75c8943ecfccd` |

- Not in the fingerprint (they judge no figure), recorded here: `tests/pass31/dev.mjs` `134dc7dee95b2a47faf9c8b5fb96d11bfb0223a2d0ee386581bde75065ae6657`, `tests/pass31/taught.test.mjs` `cc12e19c0ba588bc903c5f0565c42c28ce0484d3a87c0911f39c3e5c6e3bcdc8`.
- Decision rule: at least 2 of 3 independent complete runs pass (section 14.2, unchanged). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `4095d1aa77eb8bb4dc4bcffd75a1540bdce7468e6c20c7e1cdfe9aa542840286`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.

**Total prompt attempts: 27** (for the READY page), unchanged: try0 to try21 before session e2's follow-up, try22 to try25 in it, and try26 by the fresh builder, who used one of the three prompt revisions allowed. try26-fix reran try26's prompts, byte-identical, under the review's code fixes; it is a rerun of the bar, not a prompt attempt. Each attempt ran every item three times; from try26 each of those three is a decision of two or three complete runs.

### 15.4 Known limits added by the review fixes

- **A static real thing rests on two criteria that each miss sometimes.** On the static Enigma (decoy5 here; the review's enigma-static was built the same way) the stand-in judge failed 11 of 13 runs (4 of 6 here; 7 of 7 in the review's offline rescore of its runs), and in the 2 it passed the scorer accepted a written note beside a drawn position letter as the drawn cause; `stripped` failed 11 of 13 (6 of 6 here, 5 of 7 in the review: with its words gone the still shows no change). No run passed both, so every decision failed. A static real thing whose drawn states show the change without words would pass `stripped` and then rests on the stand-in judge alone. No static real thing that should pass has been run.
- **Static function and two-part figures are unchanged**: `judge` n/a, their still scored on the mechanism, the still's hedge in its narrow scope (section 14.4, item 4).
- **Taught-yet still uses `/usr/share/dict/words`** for lowercase words outside the new rule (four letters or more, and short words the book never writes in capitals and brief section 15 does not name). Brief section 15 says the dictionary is not used, because it holds ax, al, arm, ram, nat, lan and dos; those now fail in every case (section 15.1, item 2), but a lowercase dictionary word of four letters or more still passes as an everyday word even where the book writes it in capitals for something else (basic; the book writes BASIC). Replacing the dictionary with the COMMON list alone would fail ordinary words such as pin, bus, row, fan, tag, hop and sum, which are not among the 902.
- **A short taught term in lower case fails** (ips after IP is taught; os passes because the term itself is taught): strict, by design.
- The other limits of sections 10, 13.5 and 14.8 stand.

## 16. The builder follow-up (2026-10-24): held material out, taught-yet repairs, the frozen-file check; rerun; frozen

*Sections 14 and 15 stay as the record; where they differ from 16 (the fingerprint, the hashed files, the judge packet, the taught-yet rules, the validation command), 16 holds; section 17 replaces 16 where they differ.*

The follow-up asked for code only, with every change tested: the held material out of the judge packets and out of everything taught-yet credits (item 1), taught-yet false flags fixed in the checker and never by exemption (item 2), a required frozen-file check (item 3), the development set rerun under the D3 rule (item 4), and the frozen mechanical checks on the five Phase 1 exemplars (item 5). `tests/pass31/prompts.mjs` is byte-identical (sha256 `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`; every prompt hash as in section 14.7). Prompt revisions in this follow-up: **0** (the cap's count stays 1 of 3; total prompt attempts stay **27**). The builder did not check out, render, diff or read commit 93aae05, read nothing under `docs/pass-31-sealed/`, and opened no held figure's card, caption or strip and no held prose: the strip list was built from the ledger's `id` and `status` columns and from the tree's ids and section structure, and every check that touches held material prints counts and ids only. `figures-final`'s ledger and `public/` were read only (figures for item 5 rendered into this worktree's `tests/pass31/out/`).

### 16.1 Held material out of the judge packets (item 1)

- **The list** is data in one file, `tests/pass31/held-strip.json` (ids only):
  - `held_figures`: the 35 ledger rows with status "held" (`figures-final` ledger at `832cb0d`, sha256 `cab20cf0...`): Figs 1.12, 2.9, 3.7 to 3.11, 4.11, 5.7, 5.8, 9.10 to 9.12, 10.10, 10.11, 11.7, 12.8 to 12.11, 13.10, 13.11, 14.3, 14.4, 14.6 and 15.1 to 15.10. Each card goes whole: label, picture, caption, How-it-works strip.
  - `chapters`: `ch15`, the chapter element whole (its hero, navigation, every section and closing paragraphs), with the part opener's toc card that links to it.
  - `sections.named`: `ch3-overflow`, `ch3-defenses`. `sections.held_only`: every section whose only figures are held, found by structure (each section's figures against `held_figures`): the two named, plus `ch9-security`, `ch10-attacks`, `ch12-security`, `ch13-injection`, `ch14-hashing` and the six sections of Chapter 15 (13 in all, the same in both trees).
  - `paragraphs`: `ch16-numa-p4`, `ch8-substrates-p5`, `ch1-cpu-p9`, `ch1-cpu-p10`, `ch1-cpu-p11`, `ch2-twos-p10`, `ch2-twos-p11` (two of these ids are the captions of held cards).
  - A section with a held figure beside others (`ch1-cpu`, `ch2-twos`, `ch4-vm`, `ch5-malloc`, `ch5-ub`, `ch11-dns`, `ch14-symmetric`) loses the held card and any listed paragraph only.
- **Applied** by `tests/pass31/held.mjs` `stripHeld()`: every held card, every listed element from its start tag to its matching end tag (nesting of the same tag counted), and every toc card linking to a stripped chapter or section is blanked (offsets kept). `lib.mjs` reads every part through it for `packet()` (the judge packet), `priorTokens()` (item 2c) and the section text before a card; `scripts/known-terms.mjs --strip=tests/pass31/held-strip.json` reads the parts through it for `known`, `defines`, `defines_at`, key-terms, prose glosses and `abbreviations` (only `capitals`, which can only make the check stricter, still reads the whole book). `lib.mjs knownTerms()` refuses a known-terms file not made with this strip list (its sha256 is in the file), and the gate, `fig:check` and the tests run known-terms only through `lib.mjs runKnownTerms()`, which passes `--strip`.
- **Effect.** In this worktree's `public/`, 176 of 187 non-held packets change; the 11 before the first held material (Figs 1.1 to 1.11) are byte-identical, so the development set's packets (Figs 1.1 and 1.2) are unchanged. In known-terms, 97 glossary entries sit in a stripped section or are used in their section only inside held material, and 324 abbreviations have a first prose paragraph (371 without the strip).
- **Test:** `npm run fig:packet-test [-- --tree=<public dir>]` (`tests/pass31/packet.test.mjs`), 11 checks:
  - list: the 35 held figures and the 21 chapter, section and paragraph ids are in the tree; the 13 sections whose only figures are held are all listed; no listed paragraph sits inside a card that is not held; no strip zone cuts into a card that is not held;
  - packets: every non-held figure's packet is built (187 here, 186 in `figures-final`); of the 19,467 runs of eight words that only held material holds (a run the rest of the book also holds does not count), none is in any packet; control: with nothing stripped, the last non-held figure's packet holds 9,544 of them;
  - markers: a unique word, all-capitals token and key-term span planted in each of the 57 strip zones of a scratch copy of the tree reach no non-held packet or prose-token set, and known-terms `--strip` teaches none and lists none as an abbreviation; controls: with nothing stripped, 23 markers reach the last packet or its tokens, and known-terms without `--strip` lists 18 marker abbreviations and teaches 20 marker terms.
  11 of 11 hold on this worktree's `public/` and on `figures-final`'s `public/`.

### 16.2 Taught-yet (item 2), in the checker only

- **a. Same-section teaching.** known-terms now records, for each term first taught in a section, where the section's prose first teaches it (`by_section[].defines_at`, an offset in the part); `lib.mjs taughtBefore` credits it when that offset comes before the card (before: when its text stood anywhere in the section's text before the card). An inflection of a taught term passes like the term: a token one of whose stems is a taught single word of three letters or more, or a stem of five letters or more of one (pipelined after pipelining, registered after register); a taught term of two letters lends no stem (ips after IP still fails, section 15.1).
- **b. Glossary placement.** Why the four cases were placed late: `public/glossary.json` records not the first teaching but the first *marked* use (a key-term span, or `<em>`/`<strong>` before a definitional cue) and, for a curated term, the best-*scored* use (a section named after the term weighs 30, emphasis 60, a definitional window 25 to 50); the extractor also reads captions. So register (curated) sat at `ch3-registers`, compiler (curated) at `ch7-cpython`, byte at `ch2-binary` and thread at `ch16-threads`, though the prose glosses each in place earlier (`ch1-vonneumann-p4`, `ch1-vonneumann-p3`, `ch1-cpu-p2`, `ch7-gil-p1`). The rule now (`scripts/known-terms.mjs`): a term is first taught at the earliest of its glossary section (located at the first use in that section's prose), its first **prose gloss** (a paragraph or list item where the term or its plural is followed by a parenthesis that opens with a word, by ", which" or ", who", by ", or ACRONYM", by an apposition that is not one item of a list and does not point elsewhere, or is preceded by "called" or "known as"), and a key-term span. Teaching is in **prose only**: a use inside a figure card (label, picture, caption, strip) teaches nothing, since no judge sees it, so a glossary entry whose section writes the term only in a card (33 entries, CGNAT and IHL among them) and a key-term inside a card give no teaching point; such a term stays a glossary term, taught nowhere. 20 terms move earlier (in both trees), among them the four named; 128 marked terms are taught nowhere (held material only, cards only, or, for one, not found in its section).
- **c. Prose tokens.** A token that is neither a glossary term nor an everyday word passes when the same token, as written or in an inflection, stands in a paragraph or list item of the prose before the card (`lib.mjs priorTokens`: never a caption, label or strip, never held material). Prose is cut into tokens as labels are, so "css" is not in "/style.css" and "js" not in "Node.js". A short abbreviation in lower case (section 15.1, item 2) needs the token in exactly that case (mov after "mov eax, 5" at `ch1-cpu-p5`); an all-capitals token keeps its own rule (its first prose paragraph).
- **d. Everyday words that are glossary terms** (key, bucket, port, node, edge, release, group, toss, safety): no rule passes them. A glossary term not yet taught fails before the everyday-word and prose-token rules are reached, and the placement rule moves a teaching point only to a gloss, never to a plain use. safety fails at Figs 4.1, 4.2 and 5.11 (its first gloss is at `ch11-http-p8`), release and released at Fig 6.5, group and groups at Fig 9.9; a synthetic case makes the other six glossary terms and puts each in the prose before: all nine fail as glossary terms.
- **e. Tests:** `npm run fig:taught-test` now has **77** cases (the 30 of section 15, plus 47): 2a passes (doping and semiconductor at Fig 1.5, pipelining and pipelined at Fig 1.11, instruction set architecture at Fig 1.10, registered at Fig BR.1) and fails after the card (Figs 1.4, 1.10, 1.9, and mmap at Fig 4.8); 2b passes (register, registers, byte, bytes at Fig 1.10; compiler at Fig 3.4; thread, threads, threaded at Fig 7.4; thread at Fig 7.5) and the four placements by paragraph; 2c passes (bandwidth at Fig 8.4, applet at Fig 12.1, microtask(s) at Fig 12.3, speedup at Figs 16.8 and 16.9, int at Fig 5.1, mov at Figs 1.10, 3.2, 3.3) and fails before the prose writes them (Figs 1.9, 3.4, 8.3, 11.14, 13.2); 2d as above; 2e fails: EAX at Figs 1.8 and 1.9, mov and eax at Fig 1.9, CGNAT and IHL at Figs 9.8, 9.4, 9.9 and 18.6 (the book's last figure), AL and AX and al and ax at Fig 3.3, Ring 3, Ring 0 and system call at Fig 1.14 (its own caption), stur and ldur at Fig 3.2, execve at Fig 4.10 and vptr at Fig 6.3 (each only in the figure's own caption or strip), ax al arm ram mac os lan dos at Fig 1.1, rax at Fig 3.1, css at Fig 11.14, lo at Fig 8.5, js at Figs 11.14 and 12.1. 77 of 77 hold on this worktree's `public/` and on `figures-final`'s.
- **Effect on the book** (taught-yet on every non-held figure): `figures-final`'s `public/` 141 of 186 fail before, 123 after (18 figures flip to pass, none to fail; 127 failing tokens stop failing, 7 start: opcode at Figs 3.1, 7.7 and BR.3, taught only in a card; runtime at Fig 5.11, array at Fig 7.8, Helsinki at Fig 18.2 and OpenSSL at Fig 5.10, taught before only in held material). This worktree's `public/`: 144 of 187 before, 126 after (18 to pass, none to fail; 129 stop, the same 7 start). Figs 1.1 and 1.2 stay clean.

### 16.3 The frozen-file check (item 3)

`fig:gate`, `fig:dev` and `fig:validate` compute the gate's fingerprint (`tests/pass31/hash.mjs`) before anything else and refuse, exit 2, unless `--expect-hash=<combined>` is given and equals it: `gate.mjs` before rendering (each `--single` run of a decision checks again, and a run reporting another fingerprint is a tool error, as before); `dev.mjs` before building any tree; `validate.mjs` before reading the manifest or the ledger, writing nothing and logging nothing. The fingerprint now also hashes `tests/pass31/held.mjs` and `tests/pass31/held-strip.json`, so a change to the held list changes it (and needs a new freeze and a new validation). Checked: each of the three with no `--expect-hash` and with a wrong one exits 2 with a refusal line; with the right one each runs (`fig:dev --runs=1 --criteria=taught`, every item: v1 FAIL on `taught`, every other item PASS, as in section 15.1). `fig:check`, `fig:sheet` and the two test scripts are not gated (they judge no figure through the testers); their sha256 are recorded in section 16.5.

### 16.4 The rerun: try26-held (the try26 prompts, this follow-up's code)

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26-held | `bb136e09063d` | `781262c1` (as try26) | items 1 to 3 (sections 16.1 to 16.3, code only) | **9 of 9** | **15 of 15** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 6, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6, decoy5 0 of 6 |

`npm run fig:dev -- --runs=3 --label=try26-held --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=bb136e09063d5bfaddf67bf6e28db9c30294f104984b9d1be6921871fea177a2`. Every run reported fingerprint `bb136e09063d5bfaddf67bf6e28db9c30294f104984b9d1be6921871fea177a2`; the ledger (`figures-final`'s working file, copied into the attempt folder) sha256 `63247c12e1d80b661d076e2cae18ef03e92e4b32737448a763379ba3bc9e2e69`, with the same 35 held rows and the same two takeaways as section 15.2 (Fig 1.1, function; Fig 1.2, real thing). CLI 2.1.310. 27 evaluations, 54 complete runs (no third run was needed: every decision was 2 of 2 or 0 of 2), 1,168 tester calls, no tool error, no run made again. Output: `tests/pass31/out/dev/try26-held/summary.json`. The development set's packets and taught-yet results are the same as in try26-fix (section 16.1: Figs 1.1 and 1.2 come before all held material), so this rerun measures the gate's decisions under the new fingerprint, not the new rules; those are measured by `fig:taught-test` and `fig:packet-test`.

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26-held | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-held | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-held | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-held | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped, pairwise); run 2 FAIL (judge, hedge, still, stripped, pairwise) | run 1: none; run 2: judge | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-held | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-held | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: judge; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-held | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-held | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-held | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-held | Enigma | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-held | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-held | Enigma | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-held | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-held | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, stripped; run 2: judge, still, stripped | not run |
| try26-held | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, stripped | not run |
| try26-held | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still) | run 1: still; run 2: judge, still | not run |
| try26-held | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still) | run 1: judge, still; run 2: judge, still | not run |
| try26-held | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still, stripped | not run |
| try26-held | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-held | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-held | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-held | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: stripped; run 2: none | not run |
| try26-held | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: stripped; run 2: none | not run |
| try26-held | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-held | decoy5 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, stripped); run 2 FAIL (judge, stripped) | run 1: judge; run 2: none | not run |
| try26-held | decoy5 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge); run 2 FAIL (stripped) | run 1: none; run 2: none | not run |
| try26-held | decoy5 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |

Criteria failed per complete run (6 runs per item): v1 `taught`, `judge`, `still`, `stripped`, `pairwise` 6 of 6; v2 `judge`, `still`, `pairwise` 6 of 6, `stripped` 2, `hedge` 2; decoy1 `judge`, `hedge`, `still`, `stripped` 6 of 6; decoy2 `judge`, `hedge`, `still` 6 of 6, `stripped` 3; decoy3 `judge`, `still` 6 of 6; decoy4 `judge`, `still`, `stripped` 6 of 6, `hedge` 2; decoy5 `judge` 5, `stripped` 5, `hedge` 1 (every run failed at least one); v4 and Enigma none. Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6 and v4 passes 3 of 3.

### 16.5 Frozen (2026-10-24), and the total attempt count

The bar holds under this follow-up's code: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (15 of 15 decisions, 0 of 30 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3, 6 of 6 runs). The gate is **frozen** at this configuration, which replaces section 15.3's. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. A change to the held list (`tests/pass31/held-strip.json`) is a change to the gate: it changes the fingerprint, and the gate must be frozen again. `npm run fig:hash` reproduces these values. Run the validation as:

`npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=bb136e09063d5bfaddf67bf6e28db9c30294f104984b9d1be6921871fea177a2`

(the ledger is the author's `docs/pass-31-ledger.tsv` on `figures-final`; without `--ledger` the run stops as incomplete, and without `--expect-hash`, or with another, it refuses, exit 2). Every figure the gate judges in Phase 2 is judged as `npm run fig:gate -- <id> --ledger=<that ledger> --tree=<public dir> --expect-hash=bb136e09063d5bfaddf67bf6e28db9c30294f104984b9d1be6921871fea177a2`.

Prompt hashes: unchanged from section 14.7 (judge `fd5e2c7a...`, scorer `45189b56...`, hedge `5a558534...`, t=0 still `87a0a088...`, text-stripped `d9a1570d...`, pairwise `382b5b6a...`, system `32e914ca...`); the full text in section 12 is the frozen text.

| File the gate runs | SHA-256 (frozen 2026-10-24, try26-held) |
|---|---|
| `tests/pass31/gate.mjs` | `defc9144ba56c46d4b269dd40f93dec487916a28470a0f57c1fb1bbc558fc316` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `afc0be00662d4589ad90b39c4aa11701c94c538d72dfb6c3826c6ee1e3ef4e82` |
| `tests/pass31/hash.mjs` | `444a8ee69ecac4b9cb63732d4589f096f1a6eb5ed8009ce5faaadce7a89cbba7` |
| `tests/pass31/common-words.txt` | `f0d41e5dbd1733127522c760c9feedc586d92a1717bd6c1c7ccdb651ef46a25e` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `8d00b8c075280a10ca9201125dd577fb741f0bdcdc1fd5b71184714bc486129c` |
| `tests/pass31/validate.mjs` | `a0d3daac3ba92b313bf0d232022030ac921a304c02b37c7925b91c8ed89da921` |
| `tests/pass31/held.mjs` | `c5cb14af7a1f958ee4f56655f2f2f3d30dea3ceb697ee7b7a47ff56d2ca01cd1` |
| `tests/pass31/held-strip.json` | `a1d03dda6779c7c8c731c86da98cb7bd946896727abe6b4a55b6bd6d1ddeaf00` |

- Not in the fingerprint (they judge no figure through the testers), recorded here: `tests/pass31/check.mjs` `ce6dd1b404a52a3681afa0295db7a74e5f685ccd93f4e63b45b2b93c2d662e7d`, `tests/pass31/dev.mjs` `857a137268147545b36ba62b6ba15fecb0ab7ef4c53e9970b46b4e51cd3db6b1`, `tests/pass31/taught.test.mjs` `0b15bf339b30b8e91b91eaf2637d6870ffbbff7672e4f7cb8c6e68aa2b9b1fbc`, `tests/pass31/packet.test.mjs` `5ebfd2af0504993c69891b6c1a508740471e84b083f6baa72b99bbf250420b63`, `tests/pass31/sheet.mjs` `7d35e20b3bb881ef1b72edd5593dfb62775382a293d4af8080de329d85cb7c0a`.
- Decision rule: at least 2 of 3 independent complete runs pass (section 14.2, unchanged). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `bb136e09063d5bfaddf67bf6e28db9c30294f104984b9d1be6921871fea177a2`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.
- Code commit: `2a7d27c` (the files above); this record and the freeze: the commit that adds this section.

**Total prompt attempts: 27** (for the READY page), unchanged: try0 to try26 as in section 15.3. try26-held reran try26's prompts, byte-identical, under this follow-up's code; it is a rerun of the bar, not a prompt attempt. Prompt revisions: 1 of 3 (try26), none in this follow-up.

### 16.6 The frozen mechanical checks on the Phase 1 exemplars (item 5)

`npm run fig:check -- <part> --fig=<id> --tree=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/public --gate1=full` at `2a7d27c` (the frozen `lib.mjs` taught-yet with the held material stripped, the label cap with `MAX_PANELS` 2, Gate 1 full), on `figures-final`'s `public/` as it stood on 2026-10-24 (read only). Part IV's merged card is `fig-13-6` (it exists in `part-4.html`; `fig-13-5` does not).

| Figure | Result | Failed checks | Gate 1 rows | Part checks |
|---|---|---|---|---|
| `fig-1-5` | PASS | none | 120 clean | 6 of 6 |
| `fig-4-8` | FAIL | `cap` (33 labels in one panel; limit 8) | 120 clean | 6 of 6 |
| `fig-10-3` | FAIL | `cap` (16 labels; 3 panels, more than 2, counted as one) | 120 clean | 6 of 6 |
| `fig-13-6` | FAIL | `cap` (15 labels in its largest panel, 5 in the other) | 120 clean | 6 of 6 |
| `fig-17-6` | FAIL | `cap` (9 labels; 3 panels, more than 2, counted as one) | 120 clean | 6 of 6 |

Every other check (taught, desc, caption, strip, band, floor, gate1) passed on all five; none of the five is exempt (`docs/pass-31-exempt.json` lists no at-bar figure and none of them as kept).

### 16.7 Known limits added by this follow-up

- **A prose gloss is a pattern.** It misses glosses of other shapes (a colon, a sentence that defines without a cue) and can take an aside for a gloss ("Promises (standardised in ES2015, ...)" at `ch12-loop-p4`); it only ever moves a teaching point earlier when one of its patterns sits there. 20 terms moved, each checked by the builder against its (non-held) paragraph.
- **Teaching is in prose only.** A term the prose never writes outside a figure card (33 glossary entries, among them CGNAT, IHL, opcode, NAT, ICMP, TTL, MOSFET) is taught nowhere; an all-capitals one is still credited where a prose paragraph first writes it (`abbreviations`). This is stricter than sections 13 to 15, where a later figure was credited a term from an earlier figure's caption; three figures newly fail on opcode.
- **A use teaches a non-glossary token** (item 2c): bandwidth passes after any paragraph writes it, defined there or not; that is the rule as asked.
- **The held list is data frozen into the gate.** It mirrors the ledger's held rows at the freeze; when the author holds or releases a figure, or the held prose changes ids, the list, `fig:packet-test` and the fingerprint change together, and the gate is frozen and validated again. `fig:packet-test` fails when a section whose only figures are held is missing from the list or a listed id is missing from the tree.
- **The development set does not exercise the strip or the new taught-yet rules**: its packets precede all held material and its taught results are unchanged. They rest on `fig:taught-test` (77 cases) and `fig:packet-test` (11 checks), run on both trees.
- The other limits of sections 10, 13.5, 14.8 and 15.4 stand.

## 17. The review of the section 16 freeze (2026-10-24): seven defects and a note, fixed in code; rerun; frozen

*Sections 14 to 16 stay as the record; where they differ from 17 (the fingerprint, the hashed files, known-terms' teaching points, the taught-yet rules, the exemptions, the validation command), 17 holds.*

An independent review of the try26-held freeze (combined `bb136e09...`) reproduced its fingerprint, tests, frozen-file check, rerun and exemplar results, and found five ways taught-yet passed terms not yet taught, one per-figure exemption hook and gaps in the tests (verdict: not ready). Every fix is code. `tests/pass31/prompts.mjs` is byte-identical (sha256 `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`; every prompt hash as in section 14.7). Prompt revisions in this round: **0** (the cap's count stays 1 of 3; total prompt attempts stay **27**). The builder did not check out, render, diff or read commit 93aae05, read nothing under `docs/pass-31-sealed/`, and opened no held figure's card, caption or strip and no held prose: every probe that touches held material works by ids and section structure and prints counts and ids only. `figures-final`'s ledger and `public/` were read only. The author edited `figures-final`'s `public/` and ledger during this round, so the book counts below use a copy of its `public/` taken at `9b1cec0` (the five parts and `glossary.json` together: sha256 of their sha256 list `efc8b9dd...`); the tests were run on that copy, on `figures-final`'s live `public/` and on this worktree's `public/`.

### 17.1 The fixes (code, not counted toward the cap)

- **Defect 1, the name rules** (`tests/pass31/lib.mjs`, `scripts/known-terms.mjs`). Before: a multi-word glossary term with any capital, or a one-word entry opening with a capital, passed once the judge packet mentioned it, and the packet also holds headings, section labels, tables and the part openers' chapter previews. So terms taught only in held material (SQL injection, SYN flood, SHA-256), taught nowhere (Reno) or not yet taught (TLS handshake from Fig 3.1, IEEE 754 from Fig 1.1 through the Part I preview, CAP theorem, IP header) passed. Now:
  - a mention is tested against the prose before the card only: `lib.mjs priorTokens()` returns its plain text beside its tokens (paragraphs and list items, held material out, `<pre>` left out). `taughtYet` no longer takes the packet (it throws if one is passed), and `taughtContext` no longer builds it;
  - only an entry known-terms lists in the new `names` is credited by being mentioned. A name has a capital, no digit and no word in capitals; no en dash (the book joins a name pair with one for a named method: Diffie–Hellman); no possessive followed by a word (Amdahl's law); a capital opening every word but for the particles von, van, de, der, du, da, di, la, le (Turing machine, Boolean algebra, Shannon entropy name mechanisms); for several words, initials that are not an abbreviation the book writes (Translation Lookaside Buffer, Domain Name System); for one word, a capital then a lower-case letter, and the word, its singular and its plural never written in lower case in the book's paragraphs and list items, code left out (Signals, Promises, Consistency open sentences or list items as common nouns); and it is never taught nowhere or written in its section only inside held material. `lib.mjs knownTerms()` also drops any name in `taught_nowhere` or `strip.glossary_terms_only_in_held` (`glossary.noMention`) and matches the mention in the entry's written form (`glossary.forms`; before, the form was rebuilt from the lower-case key, so JavaScript was looked up as "Javascript"). The review's minimum (no word in capitals, no digit, never a term taught nowhere or only in held material) was extended because a probe of every glossary entry at every non-held figure still found Diffie–Hellman and Amdahl's law credited by mention, and the minimum leaves 90 entries name-shaped, among them technical terms in title case and capitalised common nouns; the rule here lists 40 names on the copy (people, organisations, papers and products), and on the copy the mention route credits only people, organisations and products;
  - the proper-name rule for a token that is no glossary term, and the LINUX rule, now match whole words in that prose: before, a truncation passed when the packet held a longer word beginning with it (Aug for August; also Apr, Oct, Manch, Eth, Ch, Comp, Crypto).
- **Defect 2, EAX** (`scripts/known-terms.mjs`, `lib.mjs`). Abbreviations are placed at the first paragraph or list item that writes them, with every `<pre>` block blanked: the code comment after `ch1-cpu-p5` no longer teaches EAX, which the book next writes in Fig 3.3's own caption and first in a paragraph at `ch3-call-p3`. The decision on `<code>` inside a paragraph: an all-capitals abbreviation in it counts, since it is the sentence's word (MOV CR3 at `chBridge-mode-p4`, "chooses which page tables the MMU uses"); for a short abbreviation in lower case, which taught-yet credits from the exact token in the prose (section 16.2 c), only a code span's first token counts (mov in "mov eax, 5", the instruction the sentence names), never its operands (eax there), which the sentence does not explain. EAX and eax fail at Figs 1.10, 2.5, 3.1 and 3.2 and pass from Fig 3.6; mov still passes at Figs 1.10, 3.2 and 3.3.
- **Defect 3, teaching only in paragraphs and list items** (`scripts/known-terms.mjs`). The glossary location, the key-term spans and the abbreviations now come from the same paragraph and list-item pieces as the prose glosses (a `<p>` or `<li>` outside every figure card, never a caption, `<pre>` blanked). Nothing else teaches: a figure card, a heading, a section label (`div.section-number`), a math label, a table cell, a code block, a part opener's chapter preview. **Tables, decided:** they do not teach. The book has 8 tables, 4 of them section summaries; a term or abbreviation first written in a cell is listed there, not explained (OS in Chapter 1's memory table, FCFS, SJF and MLFQ in Chapter 4's scheduling table); no table contains a paragraph or list item. A glossary entry whose section writes the term only outside its paragraphs is now listed by where it does: only in held material (checked first), only in a card, or the new `glossary_terms_only_outside_paragraphs` (heading, label, table cell, code block). On the copy: 93 terms keep their section but move to its first paragraph or list-item use, 4 become taught nowhere (2 written in their section only in a math label or a table cell; 2 only in figure cards, a heading or a code block), 307 abbreviations are placed (324 before; 270 stay, 37 move later, 17 go, none moves earlier). The review's probe of same-section and abbreviation credits taken from a place that is not a paragraph or list item: 91 before, **0** after.
- **Defect 4, prefixes** (`lib.mjs`). An inflection of a taught term is credited by plain endings only (`stems(part, false)`), as the review asked. Further, so that a prefixed word is neither credited nor flagged through the term inside it: a glossary term is matched by plain inflection only, and a stripped prefix makes a different word (subprocess is not process; SubBytes is not bytes), checked as a token of its own; the prefix never makes it an everyday word when what remains is a glossary term, and the prose-token rule (section 16.2 c) credits it only by its own plain inflections, never because the prose writes the term inside it. subprocess, subthreads, substack and unpipelined fail at Fig 17.6, as at `43ff49c`; SubBytes passes at Fig 14.5 (the prose before writes it; before this, the prefix made it the glossary term byte, so it failed).
- **Defect 5, HTTPS** (`lib.mjs`). A taught term takes no ending when the inflected form is an abbreviation of its own: one the book writes in capitals (known-terms `capitals`), or a glossary entry written in capitals. HTTPS fails at Fig 4.19 and passes from Fig 11.2 (first written in a paragraph at `ch11-http-p1`). The review's wording, "itself a glossary term or in the capitals list", is narrowed to entries written in capitals: lower-case entries that are plurals or inflections of another (Semaphores, Namespaces, callbacks, Promises, microservices, journaling) are the same word as their stem, and blocking them would flag a plural taught after its singular (callbacks at `ch12-loop-p2`, callback at `ch12-loop-p1`). On the copy, HTTPS is the only form the clause blocks.
- **Defect 6, the per-figure exemption hook** (`tests/pass31/check.mjs`, `docs/pass-31-exempt.json`). `check.mjs` takes exemptions only where the brief grants them (sections 10, 13, 15): the label cap (at-bar and kept figures), the floor and the caption check (kept figures; the caption of fig-18-6). The taught, desc, strip and band hooks are gone, their keys are gone from the exempt file, and a file with any other key is a refusal (exit 2). `check.mjs` and the tools it runs are now in the fingerprint, since a clean `fig:check` is part of the gate's pass (brief section 11): `tests/pass31/check.mjs`, `tests/pass31/band.py`, `tests/pass28/figs.mjs`, `tests/pass28/clip.mjs`, `tests/pass28/smooth.mjs`, `tests/pass30/contrast.mjs`. `docs/pass-31-exempt.json` is data (the author fills `at_bar` after validation) and stays outside it.
- **Defect 7, tests.** `npm run fig:taught-test`: **135** cases (the 77 of section 16; its two cases with OS are each split in two, OS now passing from Fig 3.5 and the other tokens still at Fig 3.2, 2 more; plus 56): defect 1, 17 (the four held-only or nowhere terms fail at fig-18-6; IEEE 754 at fig-1-1, TLS handshake at fig-3-1, CAP theorem at fig-16-1, IP header at fig-8-1 fail, and each passes after its teaching; Diffie–Hellman, Amdahl's law and Promises fail; Bell Labs, Shannon, Diffie and von Neumann pass once a paragraph writes them, and von Neumann fails at fig-1-1, where only a heading or preview does); defect 2, 11; defect 3, 15 (the review's eight must-fail rows, five passes after the first paragraph use, two table cases); defect 4, 4; defect 5, 3; synthetic name cases and the refused packet argument, 4; the `names` list against the rule, 1; the exemption file and `check.mjs`, 1. `npm run fig:packet-test`: **14** checks (the 11 of section 16, plus 3): two name-shaped markers in each of the 57 strip zones, each made a glossary entry of its zone's section in the scratch glossary: known-terms `--strip` lists none of the 114 as a name (control: 37 without `--strip`), and taught-yet fails every one at every non-held figure; control: a one-word and a two-word name planted in a paragraph before Fig 1.1 and taught at `ch18-final` pass at Fig 1.1, while a term with a word in capitals planted beside them fails. Both suites hold in full on this worktree's `public/`, on `figures-final`'s live `public/` and on the copy.
- **The review's note, partial criteria** (`tests/pass31/gate.mjs`). `--criteria` naming only some criteria now marks the verdict `partial` (in `verdict.json` and on stdout); an unknown criterion is refused; and `--criteria` with `--author` is refused (exit 2) outside a decision's own runs, so the author never receives a partial verdict.

### 17.2 Effect on the book (taught-yet on every non-held figure, `ef9b704` against this round's code)

- `figures-final` copy: 123 of 186 figures fail before, **128** after. 5 figures go from pass to fail (Figs 4.5, 8.6, 9.2, 9.5, 10.7), none from fail to pass. 31 failing tokens start, at 24 figures; 1 stops (JavaScript at Fig 5.11, now matched in its written form as a name a paragraph before writes).
- The 31 by cause: EAX and eax 5 (defect 2); 11 written before the card only in table cells, code blocks or figure cards (defect 3: HDD, RDX, RCX twice, rbx, FCFS, SJF, MLFQ, ERROR, ID, etcd); 7 no longer credited by mention (defect 1: Reno, SHA-256 twice, Diffie–Hellman three times, Promises); 8 truncations no longer credited by a longer word in the packet (Aug, Apr, Oct, Manch, Eth, Ch, Comp, Crypto).
- This worktree's `public/`: 126 of 187 before, 131 after; the same 31 start and the same 1 stops.
- Figs 1.1 and 1.2 stay clean. The development set's packets (sha256 per item) and taught-yet results are byte-identical under `ef9b704` and this code, in all nine of its trees.

### 17.3 The rerun: try26-review (the try26 prompts, this round's code)

A first attempt under the label try26-review (fingerprint `25a26f6c...`, code `e563dc5`) is **void**: the builder changed `tests/pass31/lib.mjs` while it ran (the completion of defect 4, commit `9d74d95`), so the frozen-file check refused 20 of its 27 evaluations as tool errors (exit 2) and its 7 finished decisions ran on mixed code. Its output is kept as `tests/pass31/out/dev/try26-review-void/`; nothing in it counts.

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26-review | `327aba6a0a00` | `781262c1` (as try26) | defects 1 to 7 and the note (section 17.1, code only) | **9 of 9** | **15 of 15** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 8, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6, decoy5 0 of 6 |

`npm run fig:dev -- --runs=3 --label=try26-review --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`, run with no file of the gate changed during it. Every run reported fingerprint `327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`; the ledger (`figures-final`'s working file, copied into the attempt folder) sha256 `dd6e94faa2eb0691233aead6ab49b2b5158bc041f8e59d71627107868492ccbd`, with the same 35 held rows and the same two takeaways as sections 15.2 and 16.4 (Fig 1.1, function; Fig 1.2, real thing). CLI 2.1.310. 27 evaluations, 56 complete runs (two Enigma evaluations needed a third run), 1,213 tester calls, no tool error, no run made again. Output: `tests/pass31/out/dev/try26-review/summary.json`. The development set's packets and taught-yet results are the same as in try26-held (section 17.2), so this rerun measures the gate's decisions under the new fingerprint; the new rules are measured by `fig:taught-test` and `fig:packet-test`.

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26-review | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, hedge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: stripped; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-review | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-review | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: RC2; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-review | Enigma | 1 | cand-first | PASS | PASS | 2 of 3 | run 1 PASS; run 2 FAIL (hedge); run 3 PASS | run 1: none; run 2: still; run 3: none | run 1: SAME (identical frames); run 2: SAME (identical frames); run 3: SAME (identical frames) |
| try26-review | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review | Enigma | 3 | random | PASS | PASS | 2 of 3 | run 1 PASS; run 2 FAIL (still); run 3 PASS | run 1: none; run 2: none; run 3: none | run 1: SAME (identical frames); run 2: SAME (identical frames); run 3: SAME (identical frames) |
| try26-review | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-review | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-review | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-review | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still) | run 1: judge, still, stripped; run 2: still | not run |
| try26-review | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: still; run 2: judge, still | not run |
| try26-review | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still | not run |
| try26-review | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-review | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: none; run 2: stripped | not run |
| try26-review | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-review | decoy5 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (stripped) | run 1: none; run 2: none | not run |
| try26-review | decoy5 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |
| try26-review | decoy5 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |

Criteria failed per complete run: v1 `taught`, `judge`, `still`, `stripped`, `pairwise` 6 of 6, `hedge` 1; v2 `judge`, `still`, `pairwise` 6 of 6; decoy1 `judge`, `hedge`, `still`, `stripped` 6 of 6; decoy2 `judge`, `hedge`, `still` 6 of 6, `stripped` 3; decoy3 `judge`, `still` 6 of 6; decoy4 `judge`, `still`, `stripped` 6 of 6, `hedge` 1; decoy5 `judge` 5, `stripped` 5 (every run failed at least one); v4 none; Enigma 2 of 8 runs failed, one on `hedge` and one on `still`, each in an evaluation that its third run decided as a pass. Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6 and v4 passes 3 of 3.

### 17.4 Frozen (2026-10-24), and the total attempt count

The bar holds under this round's code: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (15 of 15 decisions, 0 of 30 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3 decisions; 6 of 8 runs). The gate is **frozen** at this configuration, which replaces section 16.5's. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. A change to the held list, to `check.mjs` or to any tool it runs is a change to the gate: the fingerprint changes and the gate must be frozen again. `npm run fig:hash` reproduces these values. Run the validation as:

`npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`

(the ledger is the author's `docs/pass-31-ledger.tsv` on `figures-final`; without `--ledger` the run stops as incomplete, and without `--expect-hash`, or with another, it refuses, exit 2). Every figure the gate judges in Phase 2 is judged as `npm run fig:gate -- <id> --ledger=<that ledger> --tree=<public dir> --expect-hash=327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`, with `--author` and without `--criteria`.

Prompt hashes: unchanged from section 14.7 (judge `fd5e2c7a...`, scorer `45189b56...`, hedge `5a558534...`, t=0 still `87a0a088...`, text-stripped `d9a1570d...`, pairwise `382b5b6a...`, system `32e914ca...`); the full text in section 12 is the frozen text.

| File the gate runs | SHA-256 (frozen 2026-10-24, try26-review) |
|---|---|
| `tests/pass31/gate.mjs` | `6626fa55b57f00abaeff00ecf82f715e9d517ecf53f83ac5fef2dc24b1356fb7` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `b37ae5f5d5c72c7b3121a4487ee8dd2008e36597e63b1970c626a6e68fada37e` |
| `tests/pass31/hash.mjs` | `8af74d1442d1edd48b64b0618fc5012dc4fc0d982cf14af275f750c3a9b546c4` |
| `tests/pass31/common-words.txt` | `f0d41e5dbd1733127522c760c9feedc586d92a1717bd6c1c7ccdb651ef46a25e` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `740b8ab0542cec291f8e1bcc2edc6a6d21c3ac450fbdf518215505753ebea200` |
| `tests/pass31/validate.mjs` | `a0d3daac3ba92b313bf0d232022030ac921a304c02b37c7925b91c8ed89da921` |
| `tests/pass31/held.mjs` | `c5cb14af7a1f958ee4f56655f2f2f3d30dea3ceb697ee7b7a47ff56d2ca01cd1` |
| `tests/pass31/held-strip.json` | `a1d03dda6779c7c8c731c86da98cb7bd946896727abe6b4a55b6bd6d1ddeaf00` |
| `tests/pass31/check.mjs` | `4c57550ed74159f83db4780cfdc0e738e8bdc49574c130cbcbd5ef891b4c0780` |
| `tests/pass31/band.py` | `71cfffe78fc130b5a608b3fa1beb41e62be62ef58309602bfe78e85258795fdc` |
| `tests/pass28/figs.mjs` | `42591479a811a29afbd59b76d682ca795f1fd1669c28856eddfa1e47b35cffdd` |
| `tests/pass28/clip.mjs` | `25ea825b575245ff0b0353875c4b402e4e94907ae7e014f52f060c301c2ead67` |
| `tests/pass28/smooth.mjs` | `559d25fc2aa6c17b99866e8568da03adf57fe7119fdd4afa8c22de59566546e2` |
| `tests/pass30/contrast.mjs` | `0cc1eed5a34619ec88e61094e2f0e3037fb3a19ae9672bd2adabae00f56660e0` |

- Not in the fingerprint (they judge no figure), recorded here: `tests/pass31/dev.mjs` `857a137268147545b36ba62b6ba15fecb0ab7ef4c53e9970b46b4e51cd3db6b1`, `tests/pass31/taught.test.mjs` `4dd0e26998a07863bb87232ab8f0801496788dba5a505fad776b707b2781969e`, `tests/pass31/packet.test.mjs` `602106f34e54b7c16b8a72c6ce8add9e09bb2e282993f40f3fb053258309fe86`, `tests/pass31/sheet.mjs` `7d35e20b3bb881ef1b72edd5593dfb62775382a293d4af8080de329d85cb7c0a`; the exemption data `docs/pass-31-exempt.json` `7a78bd188067e6c4d24d384b11cfc7c7c2b6be9d255f2e20e48f5bfa952ceb52`.
- Decision rule: at least 2 of 3 independent complete runs pass (section 14.2, unchanged). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `327aba6a0a003dea3aa4ed3b1b757ca3de698508b3ff321e0529583bccb17741`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.
- Code commits: `e563dc5` and `9d74d95` (the files above); this record and the freeze: the commit that adds this section.

**Total prompt attempts: 27** (for the READY page), unchanged: try0 to try26 as in section 15.3. try26-review reran try26's prompts, byte-identical, under this round's code; it is a rerun of the bar, not a prompt attempt. Prompt revisions: 1 of 3 (try26), none in this round.

### 17.5 The frozen mechanical checks on the Phase 1 exemplars (item 5)

`npm run fig:check -- <part> --fig=<id> --tree=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/public --gate1=full` at `9d74d95` (this round's frozen `check.mjs` and `lib.mjs` taught-yet, the label cap with `MAX_PANELS` 2, Gate 1 full), on `figures-final`'s `public/` as it stood after the rerun (read only; `figures-final` at `6257b62` with the author's uncommitted edits of that moment; sha256 of the sha256 list of the five parts, `glossary.json` and `book.js`: `5892958a...`). Part IV's merged card is `fig-13-6` (it exists in `part-4.html`; `fig-13-5` does not). The author had redrawn Figs 10.3 and 17.6 since section 16.6.

| Figure | Result | Failed checks | Gate 1 rows | Part checks |
|---|---|---|---|---|
| `fig-1-5` | PASS | none | 120 clean | 6 of 6 |
| `fig-4-8` | FAIL | `cap` (33 labels in one panel; limit 8) | 120 clean | 6 of 6 |
| `fig-10-3` | PASS | none | 120 clean | 6 of 6 |
| `fig-13-6` | FAIL | `cap` (15 labels in its largest panel, 5 in the other) | 120 clean | 6 of 6 |
| `fig-17-6` | PASS | none | 120 clean | 6 of 6 |

Every other check (taught, desc, caption, strip, band, floor, gate1) passed on all five, taught-yet under this round's rules; none of the five is exempt.

### 17.6 Known limits added by this round

- **Names are a pattern.** A technical term in title case whose initials the book never writes as an abbreviation, or a one-word camel-case name of a mechanism (AddRoundKey, NaN), or an algorithm's proper name (Raft, Paxos), is listed as a name; it is credited only once a paragraph or list item before the card writes it, and the newcomer read stays beside it. A real name the book also writes in lower case outside code (Scheme beside scheme) is not a name and needs teaching.
- **A token made of two taught pieces passes** (Node.js once node and JS are taught): the known terms are taken out of the label before its tokens are checked, as in section 13.
- **Tables do not teach**, and neither do headings, section labels, math labels or code blocks; a term the book explains only in one of them is taught nowhere. On the copy that leaves 2 glossary entries in `glossary_terms_only_outside_paragraphs`.
- **Code in a paragraph:** an all-capitals abbreviation inside `<code>` counts where the paragraph writes it (MOV CR3), while a lower-case short abbreviation counts only as a code span's first token. The asymmetry is deliberate (section 17.1, defect 2).
- **Truncations fail** unless taught or everyday: month abbreviations not in the dictionary or the common-word list (Aug, Apr, Oct) are among the 8 tokens that newly fail; the common-word list was not changed.
- The other limits of sections 10, 13.5, 14.8, 15.4 and 16.7 stand.

## 18. The review of the section 17 freeze (2026-10-24): two holes, three low findings, eleven false flags and their placement class, teaching places, frozen-file gaps; fixed in code and data; rerun; frozen

*Sections 14 to 17 stay as the record; where they differ from 18 (the fingerprint, the hashed files, the teaching places, known-terms' cues and names, the taught-yet rules, the frozen-file check, the validation command), 18 holds.*

An independent review of the try26-review freeze (combined `327aba6a...`) reproduced it and found it not ready: two classes of true positives passed taught-yet (H1, H2), three low findings (H3 to H5), 11 of the 31 tokens that round 17 made fail were false flags (two of its must-fail tests locked them in), the same placement fault sat elsewhere (page fault, page table, mutex, control plane, JSON), `check.mjs` had no frozen-file check, `gate.mjs --single --author --criteria` printed a partial verdict without its marker, and three inputs that change verdicts were not hashed. Brief section 15 was amended the same day (round 5) to say where teaching happens, how plural and possessive abbreviations and prefixes are judged, and which sections are held by structure. Every fix is code or data. `tests/pass31/prompts.mjs` is byte-identical (sha256 `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`; every prompt hash as in section 14.7). Prompt revisions in this round: **0** (the cap's count stays 1 of 3; total prompt attempts stay **27**). The builder did not check out, render, diff or read commit 93aae05 and read nothing under `docs/pass-31-sealed/`. Held material: every probe works by ids and section structure and blanks held material (`lib.mjs heldStripped`) before it prints any text, with one exception, logged here by id only: an early survey of the paragraphs that sit outside the sections printed the first 90 characters of each, and one of them was `ch15-hero-lead`, Chapter 15's chapter lead (held with its chapter). No held card, caption or strip was opened. `figures-final`'s ledger and `public/` were read only; the book counts below use a copy of `figures-final`'s `public/` (sha256 of the sha256 list of the five parts, `glossary.json` and `book.js`: `2c6c6109...`), taken twice during this round with the same hash, and `figures-final`'s ledger at sha256 `84b4c1be...` for the tests and the rerun (35 held rows; at the freeze `0af7627a...`, with the same 35 held ids, on which `fig:packet-test` holds too).

### 18.1 The fixes (code and data, not counted toward the cap)

- **Teaching places** (new `tests/pass31/places.mjs`, read by `scripts/known-terms.mjs` for every teaching point and by `lib.mjs priorTokens()` for the prose before a card, so the two never disagree; brief section 15 as amended). A place that teaches is a `<p>` or `<li>` outside every figure card (section paragraphs and leads, chapter leads `p.chapter-subtitle`, insight and timeline paragraphs, chapter closings, list items), never a caption and never a part tagline (`p.part-tagline`, H5); or the first cell of a table row that expands or defines its term: the cell glosses itself with a parenthesis that opens with a lower-case word (HDD (spinning disk)), or the row's second cell is a definition (a phrase closed by a colon or a full stop and followed by more words, "Counter: used for loop counts and shift amounts", "First-come, first-served. Run processes in arrival order ..."; or a sentence of four words or more closed by a full stop). Only that first cell teaches: the row's other cells, a header row and a row whose other cells are values teach nothing (Chapter 1's memory table: SATA in "SATA bus", OS in "OS kernel", NVMe in "SSD (NVMe)", L2 in "L2 Cache"; SIGKILL in the Signal row's description). On the copy, of the 8 tables, the four truth tables teach nothing and the other four have rows that define their head: Chapter 1's memory table 1 of 7 body rows (HDD), Chapter 3's register table 7 of 8, Chapter 4's scheduling table 6 of 6, its IPC table 8 of 8. Section 17.1's decision that tables do not teach is replaced: its reason ("listed there, not explained") was wrong for those three tables, which expand or define each term. Section 17's requirement that an abbreviation sit inside a section is dropped, since chapter leads and closings are a chapter's paragraphs (JSON is written only in Chapter 12's lead); such a placement is recorded with the next section, and a record never names a held element (the nearest id is read with held material blanked).
- **H1, prefixes** (`lib.mjs stems()`). A prefix comes off only when what remains, as written, is an everyday word of four letters or more (a lower-case dictionary entry or a COMMON word), after the token's own plain endings and never through the remainder's stems: uploads (load), rewrote (wrote), overwritten (written) pass; redis at Fig 4.20 (re + dis), subnet and unmap fail.
- **H2, plurals, possessives and compounds** (`lib.mjs taughtYet`). A plural or possessive of an all-capitals piece is judged as the abbreviation (DRAMs, DRAM's, OSes, RAM's: the trailing s, es, 's or ’s comes off before the capitals test, and the stem is tested, so DRAMs fails where DRAM fails and passes where DRAM is taught); a lower-case possessive is judged as the short abbreviation (ram's as ram). Each piece of a compound now keeps the case the label writes: tokens are matched to their originals in order, after dashes and hyphens are made spaces, so DRAM in DRAM-only and SYN in SYN-ACK are judged as abbreviations (before, a hyphen or colon lost the case, and DRAM-based passed as the dictionary word dram).
- **H3, names** (`scripts/known-terms.mjs`). A term marked with a key-term span anywhere outside the figure cards is a concept the book teaches, never a name a mention credits (held material included, so the rule only ever makes the check stricter). Ethernet, JavaScript, Kubernetes and Raft leave the names list (40 to 36 on the copy); Ethernet fails at Figs 8.2 and 8.7 and passes from Fig 8.8; JavaScript, taught at `ch11-modern-p1`, fails at Fig 5.11 again (section 17.2's one stop) and passes from Fig 11.14.
- **H4, "los"** (`lib.mjs inPrior`). The prose's plural teaches a short abbreviation's singular only when that singular does not itself end in s: loss no longer credits los at Fig 4.13.
- **H5, part taglines** (`places.mjs`). Part II's end-of-part teaser no longer credits Baran, Cerf, Kahn, Berners-Lee and Eich from Fig 8.1; each passes from the first figure after a paragraph writes it.
- **The eleven false flags**, each fixed in the checker, none by listing a figure:

| Token | Figures | Where it is taught | Fix |
|---|---|---|---|
| diffie hellman | 11.11, 11.13, 14.1 | `ch11-crypto-p7` (between 11.9 and 11.10) | a parenthesised number between a term and its cue is skipped ("Diffie–Hellman (1976), which is key agreement") |
| sha 256 | 14.2, 14.13 | `ch11-crypto-p4` (between 11.8 and 11.9) | definitional sentence: the sentence opens with the term (after A or An at most) and goes on "is", "are" plus "a", "an" or "the" ("SHA-256 is the workhorse") |
| oct; aug, apr; ch | 9.2; 11.1; 11.1, 18-trace | everyday shorthand | `common-words.txt` gains jan, feb, apr, jun, jul, aug, sep, sept, oct, nov and ch; mar stays out (as the list's header says; MAR in capitals must be taught), and so does dec (the book writes DEC, the company) |
| ERROR | 4.16 | on the COMMON list | an all-capitals piece is judged by its letters (^ERROR as ERROR); ^EAX still fails |
| etcd | 17.8 | `ch17-consensus-p1` (between 17.4 and 17.5) | reverse apposition: a noun phrase opening its clause with an article or a possessive, then ", TERM," and a verb ('Kubernetes' "source of truth", etcd, runs'); a list item is not one |

  Fig 4.19's virtual machine and VM, false flags that predate section 17, are fixed too: a generic definition (a term of two words or more opens the sentence after A or An and a verb in -s follows: "A virtual machine imitates an entire computer", at `ch4-security-p6`; never a one-word term, whose everyday sense reads the same), and an all-capitals token with a plural ending in lower case is recorded as its singular (VMs at `ch4-security-p6` places VM there, not at `ch4-security-p11`). Both pass from Fig 4.19 and fail at Fig 4.18. Round 17's two must-fail tests are corrected: `taught.test.mjs:145` drops SHA-256 (no longer taught only in held material), and the Diffie–Hellman case moves from Fig 11.11, after its teaching, to Fig 11.9, before it.
- **The same placement class**, fixed the same way: emphasis (a term written whole inside `<em>` or `<strong>` in a teaching place, the book's mark for a term it introduces, unless the sentence holding it points to a chapter, section, part or figure number) places page table at `ch1-memory-p9` and page fault at `ch1-memory-p10` (pass from Fig 2.1, fail at Fig 1.15; pass at BR.3, BR.4, BR.5); naming apposition (a clause of four words or more, then ", a TERM" closed by ";" or ".") places mutex at `ch4-ipc-p12` (pass from Fig 4.18 and at 6.5, fail at 4.17); a modifier gloss (a term of two words or more written as the modifier of one noun that a parenthesis glosses, "control-plane components (the parts that decide what should run where)") places control plane at `ch17-k8s-p1` (pass at 17.3 and 17.10, fail at 17.2); JSON is placed at `ch12-hero-lead` (pass at 12.1 in capitals and lower case, fail at 11.15).
- **Every new cue against plain use.** On the copy this round's rules move 17 teaching points and nothing else: by the skipped number, the five cues and emphasis, the 8 fixed terms above, privilege escalation (`ch1-kernel-p10`, "In a privilege escalation attack, a malicious program running in Ring 3 gains ...", emphasised) and closure (`ch12-eich-p2`, emphasised after its description) earlier by chapters, and microservices to its emphasised use in the same paragraph; by the defining table rows of Chapter 4, CFS, pipe, shared memory, semaphore and socket earlier inside their sections; and by the part-tagline rule, C++ later (from Part II's tagline to `ch6-stroustrup-p3`, its glossary place). safety, release and group still fail at their book figures, and a synthetic tree plants plain uses of safety, release, group, key, bucket, port, node and edge before Fig 1.1, each made a glossary entry of `ch18-final`, in forms that sit next to every cue (a definite or bare subject before "is", "A key opens the lock", a list ending ", a bucket.", a parenthesis after another noun, emphasis in a sentence that names a chapter): all eight fail at Fig 1.1 as glossary terms not yet taught. One control sentence per new cue, for planted terms, teaches each.
- **Abbreviation placement on the copy**: 320 placed (307 before). Plurals placed as their singular: VM, ID (`ch11-dns-p7` to `ch4-security-p8`), PC (`ch11-bernerslee-p2` to `ch3-isa-p2`), and LKM, IMP, SBOM newly. Chapter leads and closings: JSON newly, HTTPS (`ch11-http-p1` to Chapter 11's lead), SYN (`ch10-handshake-p1` to Chapter 10's lead), AI (`ch18-future-p1` to Chapter 17's lead), TLS (`ch4-ipc-p15` to Chapter 2's closing), CFI newly (Chapter 3's closing). Defining rows: HDD, RBX, RCX, RDX, FCFS, SJF, MLFQ, FIFO newly; CFS to the table after `ch4-scheduling-p4`. `capitals` gains IMP, LKM, PLC, SBOM (379).
- **The frozen-file check in `check.mjs`** (item 4): `fig:check` computes the fingerprint first and refuses (exit 2, nothing checked) unless `--expect-hash` is given and equals it, the same refusal as `gate.mjs`, `dev.mjs` and `validate.mjs`.
- **The partial-verdict gap** (`gate.mjs`): `--criteria` with `--author` is refused with `--single` too, except in a decision's own runs (the decision starts each with `P31_GATE_DECISION_RUN=1` and reads its `verdict.json`); and the author's output line of a partial run carries `partial`.
- **The fingerprint** (`hash.mjs`) adds `tests/pass31/places.mjs`, `/usr/share/dict/words` (hashed by its absolute path; on this Mac a link to `web2`), `docs/pass-30-exceptions.json` and `scripts/figs/build_into.py`: 20 files.
- **held_only, exactly** (item 5, `packet.test.mjs`): the ledger's held ids (rows with status "held", read by header name) are exactly `held_figures`, and `sections.held_only` is exactly the set of sections whose figures in the tree are all held by the ledger (13 on every tree: the five the brief now names by structure, ch3-overflow and ch3-defenses, and Chapter 15's six); controls show the comparison catches a held figure made not held and a section added that is not held-only. The gate branch keeps no ledger, so the check needs `--ledger` and fails without it.
- **Tests.** `npm run fig:taught-test`: **228** cases (section 17's 135 with its two corrected cases and without its scheduling case, now among the table cases: 134; plus 94): H1 3, H2 5, H3 5, H4 1, H5 5; the false flags 23 and the placement class 13 (each the figure just before its teaching and the first figure after, and the figures the review named); teaching places 15 (defining rows both ways, value rows, a description cell); placements and sources of the 8 fixed terms 8, of 10 abbreviations 10, SATA and SIGKILL not placed by a table cell 1; no name marked with a key-term span 1; the synthetic tree 4 (plain uses of the eight everyday words fail; one control per cue passes; emphasis in a pointer sentence, a part tagline's gloss and a value row's term fail; abbreviations of an expanding row and of rows defined by a phrase and by a sentence pass, those of a two-word cell, a value row, a header row, a description cell and a part tagline fail). Run against `c50f7e1`'s code, 66 of the 228 fail, so each new rule is exercised. `npm run fig:packet-test -- --ledger=<figures-final's ledger>`: **17** checks (the 14 of section 17, plus the ledger's held ids, held_only exactly, and its controls). New `npm run fig:frozen-test`: **12** checks (the four new hashed inputs at their files' sha256; every module a hashed file imports is hashed, a third-party package under `node_modules` excepted; `fig:check` refuses with no hash and a wrong one and runs with the frozen one; `fig:dev` refuses both ways; `gate.mjs` refuses `--criteria` with `--author`, with and without `--single`, outside a decision; a decision's own partial run prints `partial` on the author's line). All three suites hold in full on this worktree's `public/`, on the copy of `figures-final`'s `public/` and on the review's copy (`efc8b9dd`). The development set's packets and taught-yet results are identical under `c50f7e1`'s code and this round's, in all nine of its trees.

### 18.2 Effect on the book (taught-yet on every non-held figure, `c50f7e1` against this round's code; item 7)

- Copy of `figures-final`'s `public/` (`2c6c6109...`): 186 non-held figures; failing figures 128 before, **124** after; failing tokens 500 before, **472** after. No figure goes from pass to fail; 4 go from fail to pass (Figs 4.5, 9.2, 9.5, 17.10).
- 4 tokens start failing, at 3 figures: redis (Fig 4.20; H1); C++ (Fig 5.11: Part II's tagline no longer teaches it, its glossary place is `ch6-stroustrup-p3`) and JavaScript (Fig 5.11; H3); DA (Fig 8.9: the byte in "9C:DA:C7" keeps its capitals now, where 9C and C7 already fail as notation).
- 32 stop, at 25 figures: the 11 false flags (diffie hellman at 11.11, 11.13 and 14.1; sha 256 at 14.2 and 14.13; oct at 9.2; aug, apr and ch at 11.1; ch at 18-trace; ERROR at 4.16; etcd at 17.8); Fig 4.19's virtual machine and VM; the placement class (page fault at BR.3 and BR.4; page table at BR.4 and BR.5; mutex at 6.5; control plane at 17.3 and 17.10; JSON at 12.2); the defining table rows (HDD at 1.15; RDX and RCX at 3.4; rbx at BR.1; RCX at BR.2; FCFS, SJF and MLFQ at 4.5); ID at 9.5 (placed where the prose first writes IDs, `ch4-security-p8`); Shape* at 6.4 (the label "print(Shape* s)" keeps its capital and the prose before writes Shape). No token changes only its case.
- This worktree's `public/`: 187 non-held figures, failing 131 before and 127 after, tokens 508 and 480; the same 4 start and the same 32 stop.
- Figs 1.1 and 1.2 stay clean, and the development set's packets and taught-yet results are unchanged in all nine trees (section 18.1).

### 18.3 The rerun: try26-review18 (the try26 prompts, this round's code)

A first attempt under the label try26-review18 (fingerprint `505661de...`, code `e2df9cf`) is **void**: the builder stopped it after its first three evaluations had started and before any finished, having found that a table row whose second cell is one full sentence did not teach (Chapter 4's Semaphore and Shared memory rows); the rule was completed in `963c24e` and the set rerun from the start. Its folder is kept as `tests/pass31/out/dev/try26-review18-void/`; nothing in it counts.

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26-review18 | `69bbef92cf73` | `781262c1` (as try26) | H1 to H5, the false flags and their placement class, teaching places, frozen-file gaps (section 18.1, code and data only) | **9 of 9** | **15 of 15** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 6, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6, decoy5 0 of 6 |

`npm run fig:dev -- --runs=3 --label=try26-review18 --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`, run with no file of the gate changed during it, after commit `963c24e` (10:25:05Z; run stamps 10:25:11Z to 10:33:32Z). Every run reported fingerprint `69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`; the ledger (`figures-final`'s working file, copied into the attempt folder) sha256 `84b4c1bea7199304ef636100d65582eecbbc2d19b926fb30d46ae9e263e5f1b9`, 35 held rows, the same two takeaways as sections 15.2 to 17.3 (Fig 1.1, function; Fig 1.2, real thing). The author's ledger moved on during this round (sha256 `0af7627a...` at the freeze): the same 35 held ids and the same two takeaways and jobs. CLI 2.1.310. 27 evaluations, 54 complete runs (no evaluation needed a third run), 1,170 tester calls, no tool error, no run made again. Output: `tests/pass31/out/dev/try26-review18/summary.json`.

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26-review18 | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review18 | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, hedge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: stripped; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review18 | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review18 | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review18 | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review18 | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review18 | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: CANDIDATE, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-review18 | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-review18 | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-review18 | Enigma | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review18 | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review18 | Enigma | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review18 | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-review18 | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, stripped | not run |
| try26-review18 | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, stripped; run 2: judge, still, stripped | not run |
| try26-review18 | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still, stripped; run 2: judge, still | not run |
| try26-review18 | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still | not run |
| try26-review18 | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (hedge, still) | run 1: judge, still; run 2: judge, still | not run |
| try26-review18 | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review18 | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review18 | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review18 | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-review18 | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: none; run 2: stripped | not run |
| try26-review18 | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-review18 | decoy5 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, stripped); run 2 FAIL (judge, stripped) | run 1: judge; run 2: none | not run |
| try26-review18 | decoy5 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |
| try26-review18 | decoy5 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge) | run 1: none; run 2: none | not run |

Criteria failed per complete run: v1 `taught`, `judge`, `still`, `stripped`, `pairwise` 6 of 6, `hedge` 1; v2 `judge`, `still`, `pairwise` 6 of 6; decoy1 `judge`, `hedge`, `still`, `stripped` 6 of 6; decoy2 `hedge`, `still` 6 of 6, `judge` 5, `stripped` 1; decoy3 `judge`, `still` 6 of 6; decoy4 `judge`, `still`, `stripped` 6 of 6, `hedge` 1; decoy5 `judge` 6 of 6, `stripped` 5, `hedge` 1; v4 none; Enigma none (6 of 6 runs passed). Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6 and v4 passes 3 of 3.

### 18.4 Frozen (2026-10-24), and the total attempt count

The bar holds under this round's code: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (15 of 15 decisions, 0 of 30 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3 decisions, 6 of 6 runs); no false pass at decision level. The gate is **frozen** at this configuration, which replaces section 17.4's. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. A change to the held list, to `places.mjs`, to `check.mjs` or any tool it runs, to `docs/pass-30-exceptions.json`, to `scripts/figs/build_into.py`, or to the system dictionary is a change to the gate: the fingerprint changes and the gate must be frozen again. `npm run fig:hash` reproduces these values. Run the validation as:

`npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`

(the ledger is the author's `docs/pass-31-ledger.tsv` on `figures-final`; without `--ledger` the run stops as incomplete, and without `--expect-hash`, or with another, it refuses, exit 2). Every figure the gate judges in Phase 2 is judged as `npm run fig:gate -- <id> --ledger=<that ledger> --tree=<public dir> --expect-hash=69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`, with `--author` and without `--criteria`; its mechanical check as `npm run fig:check -- <part> --fig=<id> --tree=<public dir> --expect-hash=69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`.

Prompt hashes: unchanged from section 14.7 (judge `fd5e2c7a...`, scorer `45189b56...`, hedge `5a558534...`, t=0 still `87a0a088...`, text-stripped `d9a1570d...`, pairwise `382b5b6a...`, system `32e914ca...`); the full text in section 12 is the frozen text.

| File the gate runs | SHA-256 (frozen 2026-10-24, try26-review18) |
|---|---|
| `tests/pass31/gate.mjs` | `63e7708bc226aa44217829dfcb5d0034aee5be800d771c7844a2ca5d316d98fc` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `1db162957b4a8af951d249b7582759ad502dceeafccbac24b4c75bddc989313a` |
| `tests/pass31/hash.mjs` | `ba7aa2ae09dba3f96848bb381e9daadda49a6f2903cb5ac6fd9fcda400dd3158` |
| `tests/pass31/common-words.txt` | `c1cc82a7993f92335e915283dfbe9078e39427bc7c96fd015df6766284d6873d` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `ad6b19836d5b1f698b3bb65a4477173cadf792ce6f90654a2dedc2f7dc84e582` |
| `tests/pass31/validate.mjs` | `a0d3daac3ba92b313bf0d232022030ac921a304c02b37c7925b91c8ed89da921` |
| `tests/pass31/held.mjs` | `c5cb14af7a1f958ee4f56655f2f2f3d30dea3ceb697ee7b7a47ff56d2ca01cd1` |
| `tests/pass31/held-strip.json` | `a1d03dda6779c7c8c731c86da98cb7bd946896727abe6b4a55b6bd6d1ddeaf00` |
| `tests/pass31/check.mjs` | `89bef2163a47f0e42df911f586702fed7f3521705d7a10f062377c4428e2b047` |
| `tests/pass31/band.py` | `71cfffe78fc130b5a608b3fa1beb41e62be62ef58309602bfe78e85258795fdc` |
| `tests/pass28/figs.mjs` | `42591479a811a29afbd59b76d682ca795f1fd1669c28856eddfa1e47b35cffdd` |
| `tests/pass28/clip.mjs` | `25ea825b575245ff0b0353875c4b402e4e94907ae7e014f52f060c301c2ead67` |
| `tests/pass28/smooth.mjs` | `559d25fc2aa6c17b99866e8568da03adf57fe7119fdd4afa8c22de59566546e2` |
| `tests/pass30/contrast.mjs` | `0cc1eed5a34619ec88e61094e2f0e3037fb3a19ae9672bd2adabae00f56660e0` |
| `tests/pass31/places.mjs` | `198a4b32e74e2f5224b9628aedc7741d7c4770262ade056d4253ff12c6bf7641` (corrected in section 19: this row first recorded `e2df9cf`'s file, `18b42f9e...`; the combined fingerprint was computed with the frozen file) |
| `/usr/share/dict/words` | `be41ad97963bf8dabedd5871d5d691596175269d540956b0f9965a885c2bbab9` |
| `docs/pass-30-exceptions.json` | `e1766e4c87edd36c43ef077b7650f36151338684592afd766da5ea9c49a27dc2` |
| `scripts/figs/build_into.py` | `4dffffaa7e23a1900ef3342e00ffeb2b42e960b9500e95d549d88380c13c4443` |

- Not in the fingerprint (they judge no figure), recorded here: `tests/pass31/dev.mjs` `857a137268147545b36ba62b6ba15fecb0ab7ef4c53e9970b46b4e51cd3db6b1` (unchanged), `tests/pass31/taught.test.mjs` `ffa8095fd20e2771349a390292935ceb01ee3cdf35143398f35ac41d8f3d1c00` (corrected in section 19: first recorded as `e2df9cf`'s file, `515b6443...`), `tests/pass31/packet.test.mjs` `a4c89c1a33580d090bee9d581ddb8251cdfe734d2bd732e18b3ac60afc082566`, `tests/pass31/frozen.test.mjs` `0b11a323024038cdd5936b31cab96ee7459c170bf8b7b476f222ea46c0f979a8`, `tests/pass31/sheet.mjs` `7d35e20b3bb881ef1b72edd5593dfb62775382a293d4af8080de329d85cb7c0a`; the exemption data `docs/pass-31-exempt.json` `7a78bd188067e6c4d24d384b11cfc7c7c2b6be9d255f2e20e48f5bfa952ceb52`; the third-party renderer playwright 1.61.1 (under `tests/pass25/node_modules`).
- Decision rule: at least 2 of 3 independent complete runs pass (section 14.2, unchanged). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.
- Code commits: `e2df9cf` and `963c24e` (the files above); this record and the freeze: the commit that adds this section.

**Total prompt attempts: 27** (for the READY page), unchanged: try0 to try26 as in section 15.3. try26-review18 reran try26's prompts, byte-identical, under this round's code; it is a rerun of the bar, not a prompt attempt. Prompt revisions: 1 of 3 (try26), none in this round.

### 18.5 The frozen mechanical checks on the Phase 1 exemplars (item 7)

`npm run fig:check -- <part> --fig=<id> --tree=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/public --gate1=full --expect-hash=69bbef92cf736e77c0d75c41f1c6e98bcb7751c39213a116459dc509eefdbc6c`, after the rerun, with the frozen code (the frozen-file check passed on each), on `figures-final`'s `public/` read only (`figures-final` at `929b930`, clean; the same `2c6c6109...` tree as the counts above, before and after the five runs).

| Figure | Result | Failed checks | Labels per panel (cap 8) | Gate 1 rows | Part checks |
|---|---|---|---|---|---|
| `fig-1-5` | PASS | none | 6 and 4 | 120 clean | 6 of 6 |
| `fig-4-8` | PASS | none | 8 (one panel) | 120 clean | 6 of 6 |
| `fig-10-3` | PASS | none | 8 and 8 | 120 clean | 6 of 6 |
| `fig-13-6` | PASS | none | 5 and 8 | 120 clean | 6 of 6 |
| `fig-17-6` | PASS | none | 4 and 5 | 120 clean | 6 of 6 |

Every check (cap, taught, desc, caption, strip, band, floor, gate1) passed on all five, taught-yet under this round's rules; none of the five is exempt. Part IV's anchors check reports 2 ids missing against `main`, both aliased (pass). Failed check counts: 0 of 40.

### 18.6 Known limits added by this round

- **Definitions are read by their form, not their meaning.** The five new cues, the skipped number and emphasis credit a term where the sentence has a definition's shape; on the copy they move 11 teaching points (section 18.1), each read and found a definition in place, and nothing else. A plain-use sentence of the same shape ("A bucket is a pail") would still teach the glossary term; the generic cue is limited to terms of two words or more for that reason, the definitional cue needs "is" or "are" plus an article, and the newcomer read stays beside the check.
- **Abbreviations are placed at their first writing in a teaching place**, as before; with chapter leads and closings counted as the chapters' paragraphs (brief section 15), a mention there places one (TLS in Chapter 2's closing, from a phrase that names it; AI in Chapter 17's lead).
- **Table rows** teach only through their first cell and only when the second cell is a definition by form (a phrase closed by a colon or a full stop, then words; or a sentence of four words or more): a defining row written as a bare noun phrase does not teach, and a row whose description names other terms never teaches those.
- **Lower-case forms of longer abbreviations** that are dictionary words (dram, bios) pass as everyday words, since brief section 15 limits the rule to three letters or fewer; an all-capitals word whose lower-case form inflects a COMMON word passes, and so do its plural and possessive (CLOSING, CLOSINGs: section 13's rule, judged as the abbreviation).
- **Month and chapter abbreviations**: Dec fails (the book writes DEC, the company); MAR in capitals fails; mar, may and sept are dictionary words.
- **The dictionary is hashed by its absolute path**: a system update that changes it, or another machine, changes the fingerprint, and the gate refuses until it is frozen again. Third-party packages (playwright) are not hashed, as the CLI is not.
- **A key-term span in held material** also keeps a term off the names list (only stricter); on the copy every one of the four terms dropped is marked outside held material.
- **packet-test's ledger check needs the author's ledger** (`--ledger`): the gate branch keeps none, and without it the check fails.
- The other limits of sections 10, 13.5, 14.8, 15.4, 16.7 and 17.6 stand, except 17.6's "Tables do not teach" (replaced by section 18.1) and "Truncations fail" for month abbreviations (now on the COMMON list).

## 19. The review of the section 18 freeze (2026-10-24): abbreviations credited by pointer and held-only mentions, line breaks read as sentence starts, two stale record rows, an unmarked single run, five low findings; fixed in code and data; rerun; frozen

*Sections 14 to 18 stay as the record; where they differ from 19 (the fingerprint and the hashed files' hashes, known-terms' abbreviation placement and apposition cue, the taught-yet rules for hexadecimal runs and words set in capitals, `gate.mjs`'s refusals and marks, `check.mjs`'s marks and exemption check, the validation command), 19 holds. (The builder's item list asks for "a new calibration section 18"; section 18 exists, so this is section 19.)*

An independent review of the try26-review18 freeze (combined `69bbef92...`) reproduced it (the fingerprint from a clean export, 27 of 27 rows of table 18.3, `fig:taught-test` 228 of 228, `fig:packet-test` 17 of 17, `fig:frozen-test` 12 of 12) and found it not ready: one high finding (A), three medium (B, C, D) and five low (E to I). Every fix is code or data. `tests/pass31/prompts.mjs` is byte-identical (sha256 `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54`; every prompt hash as in section 14.7). Prompt revisions in this round: **0** (the cap's count stays 1 of 3; total prompt attempts stay **27**). The builder did not check out, render, diff or read commit 93aae05 and read nothing under `docs/pass-31-sealed/`. Held material: every probe read held-stripped HTML (`lib.mjs heldStripped`) and located held material by id and offset; one probe reported, per abbreviation, only whether its first writing in a teaching place lies inside held material (yes or no, never text), which the new rule needs; no held card, caption, strip or paragraph was read or printed. `figures-final`'s ledger and `public/` were read only. Trees: the section 18 copy of `figures-final`'s `public/` (`2c6c6109...`, the counts below unless named), a copy taken at the start of this round (`78c5584a...`: `figures-final` at `929b930` with the author's uncommitted edits to `part-3.html`), the review's copy `efc8b9dd` and this worktree's `public/`.

### 19.1 The fixes (code and data, not counted toward the cap)

- **A, abbreviations credited by pointer and held-only mentions** (`scripts/known-terms.mjs`). A writing in a teaching place places an abbreviation only when it glosses it, or when it is a plain writing and neither of these holds:
  - *its sentence points elsewhere*: `POINTS` (a chapter, section, part or figure number, or §), read on the sentence (from the piece start or the last . ! ? followed by a space; a decimal point ends nothing) less every parenthesis that does not hold the writing, and less every figure number of the writing's own chapter (a chapter lead's or closing's chapter is its nearest id's). So the Part III teaser at `ch4-ipc-p15` ("Part III opens up what happens between write and read: ARPANET, packet switching, TCP, DNS, TLS, HTTP") and `ch17-microservices-p7` ("Chapter 15's answers (SBOMs, ...)") place nothing;
  - *the abbreviation is never credited by a mention*: a glossary term taught nowhere or written in its section only inside held material (the set `lib.mjs` reads as `glossary.noMention`: ASLR, CFI, HTTPS), or one the book first writes inside held material (its first writing in a teaching place, read with held material in, lies in a held zone, decided by offset; nothing of it is written out: CVE, CA, SBOM).

  A gloss of an abbreviation is any prose-gloss cue on that writing (a parenthesis that opens with a word, ", which", ", or ACRONYM", an apposition, "called" or "known as", the five definitional forms of section 18), its expansion before it (the abbreviation alone in a parenthesis after a word, "main memory (RAM)", "interrupt request (IRQ)", "time to live (TTL)", or after ", or "), or the generic form for an abbreviation (it opens the sentence and a verb in -s follows, "SQL tells it what you want": section 18 kept that form to terms of two words or more because a one-word term reads in its everyday sense, which an abbreviation in capitals lacks). A roman numeral written as a part's number ("Part II's kernel chapter", "Parts II and III") is placed where it is written: it is the book's own numbering. Each record now says how it was placed (`by`: writing, gloss (cue) or part number); `lib.mjs` reads only part and offset, as before.

  The review proposed skipping every writing whose whole sentence matches `POINTS`. Measured on the copy, that alone makes 10 tokens fail that their sentence teaches: MEM at Fig 1.11 ("Fig 1.11 adds a fifth stage, MEM, for reading or writing data in memory"), SIGSEGV at Figs 4.9 and 5.9 ("a SIGSEGV signal (Section 05 covers signals), which by default ends the program"), DH at Fig 14.10 ("forward secrecy (Chapter 11, Section 05): each session uses ephemeral DH values"), ES2015 at Fig 12.4 ("Promises (standardised in ES2015, Fig 12.2)"), II, III and IV at Fig 18.5 (the parts' numbers), and, with the held-only rule, SQL at Fig 13.1 (Chapter 13's lead). The asides, the same-chapter figures, the part numbers and the generic form are the four refinements that keep these, each measured in section 19.2. Read the other way: 9 abbreviations are still placed by a plain writing in a sentence that the whole-sentence `POINTS` matches (MEM, RSP, AMD64, SIGSEGV, DSL, GET, ES2015, DH, CAP), and each sentence was read: the pointer is an aside in parentheses or a figure of the same chapter, and the sentence teaches the term or (DSL, in "Radio, DSL and cable modems ... like those of Fig 8.6") writes it as the first-writing limit allows.

  Abbreviation placements that change on the copy (15, ids only): ASLR (`ch1-memory-p11`), CFI (`ch3-call-p6`), READ_FILE (`chBridge-trap-p1`), CVE (`ch4-vm-p17`), US (`ch9-arpanet-p3`), HTTPS (`ch11-hero-lead`), CA (`ch14-tls-pqc-p3`), SPHINCS (`ch14-tls-pqc-p7`) and SBOM (`ch17-microservices-p7`) are no longer placed; ARPANET moves from `ch4-ipc-p15` to `ch9-hero-lead`, DNS to `ch10-hero-lead`, HTTP to `ch7-types-p3`, SQL from `ch7-datasci-p7` to `ch13-hero-lead`, QUIC from `ch10-udp-p1` to `ch10-modern-p6`, CAP from `ch16-numa-p5` to `ch17-cap-p1`; GCHQ stays at `ch14-history-p6`, now by its gloss (fix E). In labels on non-held figures this makes DNS fail at Fig 8.12 and CA fail at Fig 14.12 (first written in held material; the prose before the card writes it only without a gloss: a true positive by rule, as the review asked); ASLR, CFI, HTTPS, CVE and SBOM are in no non-held label, so synthetic labels test them. HTTPS now also fails at Fig 11.2 and HTTP at Fig 4.19, so two section 17 cases change (`taught.test.mjs`, defect 5). Unchanged, as the review leaves it for session e2 or the owner: TCP and UDP at Fig 8.12 are credited from a bare mention at `ch4-ipc-p14` (the first-writing limit, section 18.6), and so are DNS from Chapter 10's lead and HTTP from `ch7-types-p3`.
- **B, line breaks read as sentence starts** (`scripts/known-terms.mjs`). Each teaching piece's text has every run of whitespace made one space (the run keeps its first character's offset) and is trimmed; pieces are joined with a separator that is not whitespace (U+001E), so no cue, term or sentence start reads across two pieces or across a line break in the HTML source, and the definitional forms' sentence start (`SENT`) and `clauseBefore` use that separator, never a newline. On the copy the definitional cue no longer fires at the two mid-sentence uses the review found (cache coherence, processes); no teaching point moves. The emphasis rule now takes the first character at or after the emphasis's content (a tag right inside `<em>` is a space the collapse merges), so its 181 emphasised uses are unchanged.
- **C, two stale rows in section 18.4** (`docs/pass-31-calibration.md`): `tests/pass31/places.mjs` is `198a4b32e74e2f5224b9628aedc7741d7c4770262ade056d4253ff12c6bf7641` and `tests/pass31/taught.test.mjs` `ffa8095fd20e2771349a390292935ceb01ee3cdf35143398f35ac41d8f3d1c00` (both rows had recorded `e2df9cf`'s files; the combined `69bbef92...` was computed with the frozen files). Corrected in place, marked as corrected.
- **D, a single run reached the author unmarked** (`tests/pass31/gate.mjs`). `--single` with `--author` is refused (exit 2) outside a decision's own runs whatever the criteria, so the author gets only decisions (2 of 3 runs); every output line of a single run, and its verdict, says `single`.
- **E, the possessive apposition** (`scripts/known-terms.mjs`). The apposition cue accepts a possessive noun as its determiner, as the reverse cue's `OPENS_NP` does, with the list and pointer guards extended to it: C++ is placed at `ch5-survives-p1` ("in C++, C's best-known descendant."), and GCHQ at `ch14-history-p6` is placed by its gloss ("GCHQ, Britain's signals-intelligence agency"). On the copy one teaching point moves (C++, from `ch6-stroustrup-p3`).
- **F, hexadecimal groups** (`tests/pass31/lib.mjs`). A run of three or more two-character hexadecimal groups joined by colons or by hyphens, holding a digit and a letter A to F (a MAC address, B8:27:EB:9C:DA:C7), is notation judged whole: it passes once the prose before the card writes "hexadecimal" (`ch1-cpu-p2`, between Figs 1.8 and 1.9) and fails otherwise as one token, "hexadecimal notation not taught before the figure"; its groups are never judged as words or abbreviations (DA, 9C). A word of four letters or more set in capitals, which the book never writes in capitals and which is no glossary term, passes once the prose before the card writes it in lower case, as section 16 passes the lower-case token: HEXADECIMAL at Fig 8.9, and on the copy also FILESYSTEM at Fig 4.13 and DESCRIPTOR at Fig BR.3; COMMIT, which the book writes in capitals, still fails.
- **G, partial results unmarked** (`tests/pass31/gate.mjs`, `tests/pass31/check.mjs`). A gate run with `--no-pairwise` says `no_pairwise` on every output line, the author's included, and in its verdict; `fig:check` with `--gate1=quick` or `off` ends every figure line and part line with `[partial: gate1 <mode>]`, and `check.json` records the mode and the fingerprint the run was checked against.
- **H, the exemption file** (`tests/pass31/lib.mjs exemptProblems`, applied by `check.mjs` before anything is checked, exit 2 on a breach). `docs/pass-31-exempt.json` stays unhashed (the author fills `at_bar` after validation), and frozen code holds it to the brief's grants: `kept` only ever names the 18 kept originals (one may leave the list, none may join it); `label_cap.ids` only at-bar or kept figures; `floor.ids` only kept ones; `caption.ids` only kept ones and fig-18-6; every id a figure id; no other key (section 17).
- **I, `figures-final`'s own `fig:check` is unfrozen: not fixed here.** Making that copy refuse, or bringing the frozen mechanical check over, is a change on `figures-final`, which the gate builder does not write. Until the author's side does it, the frozen mechanical check is this worktree's, run with `--tree=<figures-final>/public` and `--expect-hash` (section 19.4).
- **Tests.** `npm run fig:taught-test`: **284** cases (228, with section 17's two HTTP and HTTPS cases changed as above, plus 56): A 26 label cases (DNS at Fig 8.12, ASLR at Fig 2.1, CFI at Fig BR.1, HTTPS at Fig 11.1 and the book's last figure, SBOM at Fig 18-trace, CVE, CA, GCHQ before its gloss must fail; DNS from Chapter 10 and after `ch11-dns-p1`, DEP from Fig 2.1, GCHQ from Fig 14.2, and the glosses, asides, same-chapter figures, part numbers and generic form of the measurement above must pass, each beside the figure before its place), 2 for HTTP and HTTPS at Fig 7.3, 12 placements with their `by`, 1 for the six abbreviations never placed, 1 synthetic (a pointer sentence's mention and a noMention term's mention place nothing, their expansions do); B 1 synthetic ("and⏎safety is a", "as a⏎group is a" in the source fail; a control after a real sentence end passes); E 3 label cases (C++ fails at Fig 5.9, passes at Figs 5.10 and 5.11), its placement, and synthetic plain uses in a possessive list and a possessive pointer that must fail beside a possessive control that must pass; F 9 label cases (the MAC runs and HEXADECIMAL at Fig 8.9 pass, fail at Fig 1.8 and pass at Fig 1.9; a lone DA fails; a time is numbers; FILESYSTEM and DESCRIPTOR pass, COMMIT and an unwritten FILESYSTEM fail). Run against `1984b89`'s code, 36 of the 284 fail; against `c50f7e1`'s, 95. `npm run fig:packet-test -- --ledger=<figures-final's ledger>`: **17** of 17. `npm run fig:frozen-test`: **25** checks (12, plus 13: the `--gate1=off` marks on every line and `check.json`'s fingerprint 1; `single` and `no_pairwise` on a decision's own run's author line, and the refusal of `--single --author` with the full criteria 2; `exemptProblems` on the file as it stands, on eight variants, and its place in `check.mjs` before any check 10). `fig:taught-test` and `fig:packet-test` hold in full on this worktree's `public/`, on the copies `2c6c6109`, `78c5584a` and `c8f8fd5e` (taken for section 19.5) and on `efc8b9dd`, and `fig:frozen-test` on this worktree. The development set's packets and taught-yet results are identical under `1984b89`'s code and this round's in all nine of its trees.

### 19.2 Effect on the book (taught-yet on every non-held figure; item 7)

- Copy `2c6c6109...` (186 non-held figures), `1984b89`'s code against this round's: failing figures 124 before, **124** after; failing tokens 472 before, **465** after. One figure goes from pass to fail (Fig 8.12), one from fail to pass (Fig 8.9). 2 tokens start failing: dns at Fig 8.12 (A: written before Chapter 10 only in the Part III teaser) and CA at Fig 14.12 (A: first written in held material, never glossed). 9 stop: DESCRIPTOR at BR.3 and FILESYSTEM at 4.13 (F, the word in capitals), c++ at 5.11 (E), HEXADECIMAL, 9c, DA, c7, 8c and 1f at 8.9 (F).
- The same copy, `c50f7e1`'s code (the freeze before section 18) against this round's: 128 to **124** figures, 500 to **465** tokens; 4 start (redis at 4.20, javascript at 5.11, dns at 8.12, CA at 14.12; section 18.2's c++ and DA no longer start), 39 stop (section 18.2's 32, plus DESCRIPTOR at BR.3, FILESYSTEM at 4.13, and HEXADECIMAL, 9c, c7, 8c and 1f at 8.9; section 19.5 lists them).
- The copies `78c5584a` and `efc8b9dd` change exactly as `2c6c6109`; this worktree's `public/` (187 non-held figures): 127 to 127 and 480 to 473 against `1984b89`, 131 to 127 and 508 to 473 against `c50f7e1`, the same tokens.
- Each new rule, ablated alone over every non-held label of the copy (the labels whose verdict depends on it): the pointer rule 1 (dns at 8.12); the never-by-mention rule 1 (CA at 14.12); asides out of the pointer test 3 (SIGSEGV at 4.9 and 5.9, DH at 14.10); same-chapter figures 2 (MEM at 1.11, ES2015 at 12.4); part numbers 3 (II, III, IV at 18.5); the expansion and the abbreviation's generic form 3 (IRQ at BR.8, SQL at 13.1 in capitals and in "SQL/DS"); the possessive apposition 1 (c++ at 5.11); hexadecimal runs 5 (8.9); the word in capitals 3 (DESCRIPTOR, FILESYSTEM, HEXADECIMAL). B moves no teaching point (above).
- Figs 1.1 and 1.2 stay clean, and the development set's packets and taught-yet results are unchanged in all nine trees.

### 19.3 The rerun: try26-review19 (the try26 prompts, this round's code)

| Attempt | Combined | prompts.mjs | Change before the run | Decisions: v1, v2, v4 correct | Decoys correct | Enigma passed | Complete runs passed |
|---|---|---|---|---|---|---|---|
| try26-review19 | `d35134273308` | `781262c1` (as try26) | A to H (section 19.1, code and data only) | **9 of 9** | **15 of 15** | **3 of 3** | v1 0 of 6, v2 0 of 6, v4 6 of 6, Enigma 6 of 6, decoy1 0 of 6, decoy2 0 of 6, decoy3 0 of 6, decoy4 0 of 6, decoy5 0 of 6 |

`npm run fig:dev -- --runs=3 --label=try26-review19 --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`, run with no file of the gate changed during it, after commit `8a8f784` (12:00:36Z; run stamps 12:01:04Z to 12:10:56Z). Every run reported fingerprint `d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`; the ledger (`figures-final`'s working file, copied into the attempt folder) sha256 `d863dab904de0faf8cb7f49fbcc637499964fde1bb8953fe09d94dcde3b552f3`, 35 held rows, the same held ids and the same two takeaways and jobs as section 18.3's copy `84b4c1be...` (Fig 1.1, function; Fig 1.2, real thing; compared by equality, not printed). CLI 2.1.310. 27 evaluations, 54 complete runs (no evaluation needed a third run), 1,167 tester calls, no tool error, no run made again. Output: `tests/pass31/out/dev/try26-review19/summary.json`.

| Attempt | Item | Evaluation | Order | Expected | Got | Runs passed | Runs | Hedge in | Pairwise |
|---|---|---|---|---|---|---|---|---|---|
| try26-review19 | v1 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, hedge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: judge; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review19 | v1 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review19 | v1 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (taught, judge, still, stripped, pairwise); run 2 FAIL (taught, judge, still, stripped, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review19 | v2 | 1 | cand-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: candidate A: RC2, rc2 A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review19 | v2 | 2 | rc2-first | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: rc2 A: RC2, candidate A: RC2 |
| try26-review19 | v2 | 3 | random | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, pairwise); run 2 FAIL (judge, still, pairwise) | run 1: none; run 2: none | run 1: rc2 A: RC2, candidate A: RC2; run 2: candidate A: RC2, rc2 A: RC2 |
| try26-review19 | v4 | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: CANDIDATE, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-review19 | v4 | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: rc2 A: CANDIDATE, candidate A: SAME; run 2: rc2 A: CANDIDATE, candidate A: SAME |
| try26-review19 | v4 | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: candidate A: SAME, rc2 A: CANDIDATE; run 2: candidate A: SAME, rc2 A: CANDIDATE |
| try26-review19 | Enigma | 1 | cand-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review19 | Enigma | 2 | rc2-first | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review19 | Enigma | 3 | random | PASS | PASS | 2 of 2 | run 1 PASS; run 2 PASS | run 1: none; run 2: none | run 1: SAME (identical frames); run 2: SAME (identical frames) |
| try26-review19 | decoy1 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still, stripped; run 2: judge, still, stripped | not run |
| try26-review19 | decoy1 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, stripped; run 2: judge, still, stripped | not run |
| try26-review19 | decoy1 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, stripped; run 2: judge, stripped | not run |
| try26-review19 | decoy2 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still, stripped; run 2: judge, still | not run |
| try26-review19 | decoy2 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still) | run 1: judge, still; run 2: judge, still | not run |
| try26-review19 | decoy2 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still); run 2 FAIL (judge, hedge, still, stripped) | run 1: judge, still; run 2: judge, still | not run |
| try26-review19 | decoy3 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review19 | decoy3 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review19 | decoy3 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still); run 2 FAIL (judge, still) | run 1: none; run 2: none | not run |
| try26-review19 | decoy4 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: stripped; run 2: none | not run |
| try26-review19 | decoy4 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: none; run 2: none | not run |
| try26-review19 | decoy4 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, still, stripped); run 2 FAIL (judge, still, stripped) | run 1: stripped; run 2: none | not run |
| try26-review19 | decoy5 | 1 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, hedge, stripped); run 2 FAIL (judge, stripped) | run 1: judge; run 2: none | not run |
| try26-review19 | decoy5 | 2 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (judge, stripped) | run 1: none; run 2: none | not run |
| try26-review19 | decoy5 | 3 | no pairwise | FAIL | FAIL | 0 of 2 | run 1 FAIL (judge, stripped); run 2 FAIL (still, stripped) | run 1: none; run 2: none | not run |

Criteria failed per complete run: v1 `taught`, `judge`, `still`, `stripped`, `pairwise` 6 of 6, `hedge` 1; v2 `judge`, `still`, `pairwise` 6 of 6; decoy1 `judge`, `hedge`, `still`, `stripped` 6 of 6; decoy2 `judge`, `hedge`, `still` 6 of 6, `stripped` 1; decoy3 `judge`, `still` 6 of 6; decoy4 `judge`, `still`, `stripped` 6 of 6, `hedge` 2; decoy5 `stripped` 6 of 6, `judge` 5, `hedge` 1, `still` 1; v4 none; Enigma none (6 of 6 runs passed). Without pairwise (as validation runs), the v1 and v2 decisions fail on their single-figure criteria 6 of 6 and v4 passes 3 of 3.

### 19.4 Frozen (2026-10-24), and the total attempt count

The bar holds under this round's code: v1 and v2 failed every evaluation (6 of 6 decisions, 0 of 12 complete runs passed), every decoy failed every evaluation (15 of 15 decisions, 0 of 30 runs), v4 passed every evaluation (3 of 3, 6 of 6 runs) and Enigma passed every evaluation (3 of 3 decisions, 6 of 6 runs); no false pass at decision level. The gate is **frozen** at this configuration, which replaces section 18.4's. From here only a failed validation or a drift-check false pass reopens it (brief sections 10 and 14), and a rebuilt gate is validated again on the sealed set before it judges. A change to any file below, to the held list or to the system dictionary is a change to the gate: the fingerprint changes and the gate must be frozen again. `npm run fig:hash` reproduces these values. Run the validation as:

`npm run fig:validate -- --ledger=/Users/yki/Documents/github/atheric/under-the-code/.claude/worktrees/figures-final/docs/pass-31-ledger.tsv --expect-hash=d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`

(the ledger is the author's `docs/pass-31-ledger.tsv` on `figures-final`; without `--ledger` the run stops as incomplete, and without `--expect-hash`, or with another, it refuses, exit 2). Every figure the gate judges in Phase 2 is judged as `npm run fig:gate -- <id> --ledger=<that ledger> --tree=<public dir> --expect-hash=d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`, with `--author`, without `--criteria` and without `--single` (both refused with `--author`; a run without the pairwise test, as for a merged figure or a redraw, says `no_pairwise` on its line); its mechanical check as `npm run fig:check -- <part> --fig=<id> --tree=<public dir> --expect-hash=d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb` (Gate 1 full: a quick or off run marks every line partial).

Prompt hashes: unchanged from section 14.7 (judge `fd5e2c7a...`, scorer `45189b56...`, hedge `5a558534...`, t=0 still `87a0a088...`, text-stripped `d9a1570d...`, pairwise `382b5b6a...`, system `32e914ca...`); the full text in section 12 is the frozen text.

| File the gate runs | SHA-256 (frozen 2026-10-24, try26-review19) |
|---|---|
| `tests/pass31/gate.mjs` | `cd65247117b91feab0e2dd6950b1601cbfc70f77f7e677e2f4a801b8ed244f57` |
| `tests/pass31/prompts.mjs` | `781262c1da6c9a90545f9f8ea84cf6ae0853e181e55adb732ff5ac7aead3bb54` |
| `tests/pass31/lib.mjs` | `f42845deadb5a8293d98327bf3f0db4c6f9cf5fd3248ed7650ef5a6ab53e82df` |
| `tests/pass31/hash.mjs` | `ba7aa2ae09dba3f96848bb381e9daadda49a6f2903cb5ac6fd9fcda400dd3158` |
| `tests/pass31/common-words.txt` | `c1cc82a7993f92335e915283dfbe9078e39427bc7c96fd015df6766284d6873d` |
| `tests/pass30/bare.mjs` | `4a50e955f415b658a21c00d8fe012ca24aa0849bcf35b21fe8a7e181d263f281` |
| `scripts/known-terms.mjs` | `5c5a616e8925a858e2b052b270450bd4f8ad2ac9a23d53cb5eb9328ed4b5e7e7` |
| `tests/pass31/validate.mjs` | `a0d3daac3ba92b313bf0d232022030ac921a304c02b37c7925b91c8ed89da921` |
| `tests/pass31/held.mjs` | `c5cb14af7a1f958ee4f56655f2f2f3d30dea3ceb697ee7b7a47ff56d2ca01cd1` |
| `tests/pass31/held-strip.json` | `a1d03dda6779c7c8c731c86da98cb7bd946896727abe6b4a55b6bd6d1ddeaf00` |
| `tests/pass31/check.mjs` | `c50598b18dfc700115a3b003769254cb7077343e87ddddeb5079020ed530d98e` |
| `tests/pass31/band.py` | `71cfffe78fc130b5a608b3fa1beb41e62be62ef58309602bfe78e85258795fdc` |
| `tests/pass28/figs.mjs` | `42591479a811a29afbd59b76d682ca795f1fd1669c28856eddfa1e47b35cffdd` |
| `tests/pass28/clip.mjs` | `25ea825b575245ff0b0353875c4b402e4e94907ae7e014f52f060c301c2ead67` |
| `tests/pass28/smooth.mjs` | `559d25fc2aa6c17b99866e8568da03adf57fe7119fdd4afa8c22de59566546e2` |
| `tests/pass30/contrast.mjs` | `0cc1eed5a34619ec88e61094e2f0e3037fb3a19ae9672bd2adabae00f56660e0` |
| `tests/pass31/places.mjs` | `198a4b32e74e2f5224b9628aedc7741d7c4770262ade056d4253ff12c6bf7641` |
| `/usr/share/dict/words` | `be41ad97963bf8dabedd5871d5d691596175269d540956b0f9965a885c2bbab9` |
| `docs/pass-30-exceptions.json` | `e1766e4c87edd36c43ef077b7650f36151338684592afd766da5ea9c49a27dc2` |
| `scripts/figs/build_into.py` | `4dffffaa7e23a1900ef3342e00ffeb2b42e960b9500e95d549d88380c13c4443` |

- Changed since section 18.4: `gate.mjs`, `lib.mjs`, `scripts/known-terms.mjs`, `check.mjs`; the other 16 files are byte-identical.
- Not in the fingerprint (they judge no figure), recorded here: `tests/pass31/dev.mjs` `857a137268147545b36ba62b6ba15fecb0ab7ef4c53e9970b46b4e51cd3db6b1` (unchanged), `tests/pass31/taught.test.mjs` `21ed7fa65f3b3051c70acb7327275f964038c3b2fa98215397bdbad1635dbb77`, `tests/pass31/packet.test.mjs` `a4c89c1a33580d090bee9d581ddb8251cdfe734d2bd732e18b3ac60afc082566` (unchanged), `tests/pass31/frozen.test.mjs` `0cdfdeaad9591f5dfe4c42be071442bab88fc7abc2576b59c9abbb9fc9bf8383`, `tests/pass31/sheet.mjs` `7d35e20b3bb881ef1b72edd5593dfb62775382a293d4af8080de329d85cb7c0a` (unchanged); the exemption data `docs/pass-31-exempt.json` `7a78bd188067e6c4d24d384b11cfc7c7c2b6be9d255f2e20e48f5bfa952ceb52` (unchanged; held to its grants by `lib.mjs exemptProblems`, section 19.1 H); the third-party renderer playwright 1.61.1 (under `tests/pass25/node_modules`).
- Decision rule: at least 2 of 3 independent complete runs pass (section 14.2, unchanged). Votes per scorer and hedge check within a run: 3. Model: `claude-sonnet-5-5`.
- Combined fingerprint (prompts, files, model): `d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`.
- CLI at the freeze (recorded, not hashed): `2.1.310 (Claude Code)`.
- Code commit: `8a8f784` (the files above); this record and the freeze: the commit that adds this section.

**Total prompt attempts: 27** (for the READY page), unchanged: try0 to try26 as in section 15.3. try26-review19 reran try26's prompts, byte-identical, under this round's code; it is a rerun of the bar, not a prompt attempt. Prompt revisions: 1 of 3 (try26), none in this round.

### 19.5 The frozen mechanical checks on the Phase 1 exemplars, and taught-yet on `figures-final` (item 7)

`npm run fig:check -- <part> --fig=<id> --tree=<tree> --gate1=full --expect-hash=d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`, after the rerun, with the frozen code (the frozen-file check passed on each). The author was editing `figures-final`'s `public/` during this round (`figures-final` at `929b930`, uncommitted edits to `part-1.html` and `part-3.html`): a first pass on `figures-final/public` itself saw the tree change from `c675ab16` to `c8f8fd5e` during it, so the five were run again on a byte copy taken right after (`c8f8fd5e`, unchanged before and after the runs), and that pass is the record. Both passes gave the same figure results.

| Figure | Result | Failed checks | Labels per panel (cap 8) | Gate 1 rows | Part checks |
|---|---|---|---|---|---|
| `fig-1-5` | PASS | none | 6 and 4 | 120 clean | 6 of 6 |
| `fig-4-8` | PASS | none | 8 (one panel) | 120 clean | 6 of 6 |
| `fig-10-3` | PASS | none | 8 and 8 | 120 clean | 6 of 6 |
| `fig-13-6` | PASS | none | 5 and 8 | 120 clean | 6 of 6 |
| `fig-17-6` | PASS | none | 4 and 5 | 120 clean | 5 of 6 (smooth), then 6 of 6 |

Every figure check (cap, taught, desc, caption, strip, band, floor, gate1) passed on all five, taught-yet under this round's rules; none of the five is exempt; failed figure checks: 0 of 40. Part IV's anchors check reports 2 ids missing against `main`, both aliased (pass). Part V's page-level `gate1:smooth` check found 1 finding in both passes (dropped frames while scrolling at 1440 px, 7.8%; the page is byte-identical to the one that passed in section 18.5) and none on a third run of the same check (4%): the load-dependent measure `UNDER.md` §4ag already logs for Part V; the figure checks are unaffected.

Taught-yet over every non-held figure of the copy `c8f8fd5e` (186), `c50f7e1`'s code (before) against the frozen code (after): failing figures 128 before, **124** after; failing tokens 500 before, **465** after. One figure goes from pass to fail (Fig 8.12); 5 go from fail to pass (Figs 4.5, 8.9, 9.2, 9.5, 17.10).
- Tokens that start failing (4, at 4 figures): fig-4-20 `redis`; fig-5-11 `javascript`; fig-8-12 `dns`; fig-14-12 `CA`.
- Tokens that stop failing (39, at 27 figures): fig-1-15 `HDD`; fig-3-4 `RDX`, `RCX`; fig-br-1 `rbx`; fig-br-2 `RCX`; fig-br-3 `DESCRIPTOR`, `page fault`; fig-br-4 `page table`, `page fault`; fig-br-5 `page table`; fig-4-5 `FCFS`, `SJF`, `MLFQ`; fig-4-13 `FILESYSTEM`; fig-4-16 `ERROR`; fig-4-19 `virtual machine`, `VM`; fig-6-4 `shape*`; fig-6-5 `mutex`; fig-8-9 `HEXADECIMAL`, `9c`, `c7`, `8c`, `1f`; fig-9-2 `oct`; fig-9-5 `ID`; fig-11-1 `ch`, `aug`, `apr`; fig-11-11, fig-11-13, fig-14-1 `diffie hellman`; fig-12-2 `JSON`; fig-14-2, fig-14-13 `sha 256`; fig-17-3 `control plane`; fig-17-8 `etcd`; fig-17-10 `control plane`; fig-18-trace `ch`.
- Against `1984b89`'s code on the same copy: 124 to 124 figures, 472 to 465 tokens; start fig-8-12 `dns`, fig-14-12 `CA`; stop fig-br-3 `DESCRIPTOR`, fig-4-13 `FILESYSTEM`, fig-5-11 `c++`, fig-8-9 `HEXADECIMAL`, `9c`, `DA`, `c7`, `8c`, `1f`.

### 19.6 Known limits added by this round

- **Pointers are read by form.** A sentence points elsewhere when it names a chapter, section, part, § or a figure of another chapter outside the parentheses that do not hold the writing; a teaser without a number ("the next part covers DNS") is not caught, an aside that cites another place does not make its sentence a pointer, and a sentence that brings in a figure of its own chapter is read as the teaching that figure goes with. On the copy every abbreviation placed by a plain writing in a sentence the whole-sentence `POINTS` matches (9) was read (section 19.1).
- **"First written in held material" is decided by the first writing in a teaching place**, held material included, by offset; a token written first in a held card or caption is not restricted by it (cards never teach). Such an abbreviation, and a glossary term never credited by a mention, is placed only through a gloss outside held material.
- **The first-writing limit stands** for every other abbreviation (section 18.6): a plain writing in a sentence that does not point elsewhere places it (TCP and UDP at `ch4-ipc-p14`, DNS in Chapter 10's lead, HTTP at `ch7-types-p3`), as the review leaves for session e2 or the owner.
- **An abbreviation's generic form** ("SQL tells it what you want") is read as a gloss by its shape; a sentence that opens with an abbreviation and a verb in -s is credited as one.
- **Hexadecimal runs** need three or more two-character groups with one separator, a digit and a letter A to F; a run of digits only stays numbers (10:25:11), and a lone group is judged as a token.
- **A word set in capitals** passes once the prose before the card writes it in lower case, unless the book writes it in capitals (COMMIT) or it is a glossary term.
- **`at_bar`** stays free data (any figure id) and exempts the label cap only (brief section 10); the other lists are held to their grants.
- **Finding I is open**: `figures-final`'s own `fig:check` runs that branch's unfrozen copy until the author's side makes it refuse or brings the frozen check over.
- The other limits of sections 10, 13.5, 14.8, 15.4, 16.7, 17.6 and 18.6 stand.
