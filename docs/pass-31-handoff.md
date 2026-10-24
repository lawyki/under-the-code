# Pass 31 · handoff (stopped 2026-10-24 on the owner's word)

The owner stopped the work on 2026-10-24 ("Stop it. Only write everything about the progress that was made, and instructions and everything so it can be continued exactly"). The 15-minute heartbeat loop is cancelled and the gate's background run is stopped. This file is the complete state; it is enough to continue without the old conversation. Restart nothing until the owner says to continue.

## 1. Read first, in this order

1. This file.
2. `docs/pass-31-brief.md`: the pass's rules. Sections 4 (jobs), 7 (takeaway, content, knows, subtraction, the seen-loss test, the convergence rule and stop rule, the development set), 10 (gate and validation), 11 (Phase 2 per figure), 12 (cuts, merges, anchors), 15 (taught-yet), 16 (READY), 17 (done), 18 (laws and exceptions).
3. `UNDER.md` §4ag: the pass log. The last three entries are "Repairs, round 5", "Repairs, round 6" and "Phase 0 under the stop rule".
4. `docs/todo.md`, section "Figure finalization": the checklist, ticked only when committed and verified.
5. `STATE.md`, the "Pass 31 at:" line.

## 2. Where everything is

| What | Where | State |
|---|---|---|
| Author worktree | `.claude/worktrees/figures-final` (branch `figures-final`) | `24477bd`, pushed; clean apart from untracked `node_modules` |
| Gate worktree | `.claude/worktrees/figures-final-gate` (branch `figures-final-gate`) | local `19040ce`, NOT pushed (origin at `982670b`); clean |
| Main checkout | `/Users/yki/Documents/github/atheric/under-the-code` (branch `main`) | `3fd4774`, untouched by Pass 31. Its two untracked files, `docs/figure-finalization-plan.md` and `docs/pass-31-brief.md`, belong there: leave them |
| Calibration page (owner) | https://claude.ai/artifact/FycKg4RsbcLdCqjT2xQgkk | version 10, private, shows the 12 cut candidates; sources in `scripts/pass31-author/calib/` |
| Verifier peer session | `under-the-code-e2` (cross-session; `ListAgents`, `SendMessage`) | running its targeted check of `24477bd` (task `wuq24i5rs`), see section 3 |
| Author tools | `scripts/pass31-author/` | see section 8 |
| Gate review reports | `scripts/pass31-author/gate-reviews/` | the reviews of `c50f7e1`, `1984b89`, `982670b` (counts and code locations only) |

Pushing `main` deploys the live site: never without the owner's word. Pushing `figures-final` or `figures-final-gate` only makes previews.

## 3. Phase 0 (the ledger): closed under the stop rule, one check pending

What happened: six repair rounds, each verified by session e2. The convergence rule (brief §7 exit) said Phase 0 ends when an e2 verification finds no high and no medium class-A defect; after round 6 it still did (66 confirmed), so the stop rule applied. Commit `24477bd` is that stop-rule step:

- Facts fixed (facts block at any severity): 9.2 ("four sites' computers", SRI was not a university), 12.1 ("no script could change the page"), 5.11 (the drawn waves), 3.1's citation rewrite (whole clause), 11.12's content (only the leaf names a host), 18.2's content (verdict text moved out) and gap (Linux 1991). A fact must-fix closes only as "Applied".
- §7's new-fact clause ("reversing an earlier verified keep needs a new fact, not a reapplied rule") applied: 17 rows that were verified keeps through round 4 and were cut in round 5 by a reapplied rule returned to keep (3.1, 3.3, 5.1, 5.10, 5.11, 9.2, 9.9, 11.2, 11.5, 12.2, 12.4, 14.1, 14.2, 14.10, 14.13, 18.1, 18.2). Each starts with its round-4 subtraction and carries a "Phase 2 inputs: possible cut" note that keeps the round-5 cut record (gap, citations, aliases).
- Every remaining class-A medium is one labelled "Must-fix before <event>:" item on its row; lows and class B are "Phase 2 inputs" notes.

Pending: e2's targeted verification of `24477bd` (`wuq24i5rs`, resumed after a session-limit death). Its result is sent to this session's address by message. If it finds no fact error and no new class-A medium, Phase 0 is closed: tick in `docs/todo.md` the items "Repairs, round 3" to "Repairs, round 6" and "Phase 0 under the stop rule", commit, push. If it finds a fact, fix it (close "Applied"), and send e2 the rows to re-check. If the message never arrives, ask e2 (`SendMessage` to `under-the-code-e2`) for the result of `wuq24i5rs`.

Ledger numbers at `24477bd` (`docs/pass-31-ledger.tsv`, 222 rows, 15 columns read by header):

- 157 keep; 12 cut candidates: 1.10, 4.1, 5.2, 6.2, 7.2, 8.12, 11.1, 13.1, 17.11, 18.3, 18.4, 18.5 (the twelve that were candidates in every round); 9 merged cards: eight pending pairs 1.3+1.4, 2.7+2.8, 5.4+5.5, 6.3+6.4, 7.8+7.9, 8.5+8.6, 16.8+16.9, 17.7+17.8 (the higher row holds the takeaway and every durable decision) and 13.6, already merged with 13.5 on the page; 35 held (the security figures, never touched).
- Takeaway freeze: sha256 `a79eb924ee197aa5bbfe860f1b43d4c97ffe368cb3dba7ad7fdf7d9182130a23`. Reproduce with `python3 scripts/pass31-freeze.py` (serialization in the script and in brief §7). The Phase 2 keep-direction re-test must run on this frozen content.
- Open "Must-fix before" items on 20 rows: the 12 cut candidates (each re-tested in the keep direction at its chapter commit, before the cut is executed; a failure reverts it to keep, and the re-test makes no new cut), 9.2, 14.1, 18.4, 6.2, 11.1, and the five exemplars (1.5, 4.8, 10.3, 13.6, 17.6: recheck under the READY gate freeze, with a fact check and a newcomer read of their labels). Find them with `grep -n "Must-fix before" docs/pass-31-ledger.tsv`.
- "Phase 2 inputs: possible cut" notes: 47 from the round-6 blind keep panel (not acted on, see section 6), 17 on the returned keeps, 1 on 4.3. They are declined by default at Phase 2 step 1 unless a new fact reopens one, under §7's two-verdict rule.

## 4. The gate (`figures-final-gate`): not READY yet, code for the fourth review committed but not frozen

Freeze history (each with an independent review; all reports counts-only):

| Freeze | Fingerprint | Review |
|---|---|---|
| `43ff49c` | `4095d1aa` | superseded |
| `ef9b704` | `bb136e09` | NOT READY (7 defects) |
| `c50f7e1` | `327aba6a` | NOT READY (H1, H2, 11 false flags) |
| `1984b89` | `69bbef92` | NOT READY (A high, B to D medium, E to I low) |
| `982670b` | `d3513427` | NOT READY: D1 high (plain mentions place glossary and key-term abbreviations such as TLS, TCP, UDP, HTTP, IP, DNS, RSA before their teaching paragraph: 19 untaught tokens at 12 figures), D2 medium (-ed, -ing, -ly forms of multi-word terms escape), D3 to D10 low. Report: `scripts/pass31-author/gate-reviews/review-982670b.md` |

`19040ce` (local, unpushed) is the fix stage's code for D1 to D10, written before the run was stopped. It is not frozen, the development set has not been rerun on it, and it has not been reviewed.

The run that was stopped: workflow `wf_96a0d94b-9d0`, script `~/.claude/projects/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/workflows/scripts/pass31-gate-followup-3-wf_96a0d94b-9d0.js`. In the same session it resumes with `Workflow({scriptPath: <that path>, resumeFromRunId: 'wf_96a0d94b-9d0'})` (finished stages replay from cache). In a new session, start a fresh gate-builder agent instead, with these instructions:

1. Work only in the gate worktree; never read `tests/pass31/prompts.mjs`'s text in a report, `docs/pass-31-sealed/`, or commit `93aae05`; report counts, hashes, commit ids and file:line only; `prompts.mjs` stays byte-identical (`781262c1`); prompt revisions allowed: zero.
2. Check that `19040ce` fixes D1 to D10 of `review-982670b.md` with tests, including a must-fail regression test for each of D1's 19 tokens at its figure (and a pass at the first figure after its teaching paragraph). D1 is fixed as brief §15 says: a taught abbreviation is listed only at the paragraph that teaches it.
3. Rerun the development set under the 2-of-3 decision rule (v1, v2 and every decoy fail every evaluation; v4 and Enigma pass every evaluation; zero false passes at decision level). If the bar holds, re-freeze (calibration section 20: fingerprint, every file hash, the validation command with `--ledger=<figures-final>/docs/pass-31-ledger.tsv`), commit, push `figures-final-gate`.
4. An independent review of that freeze (review 3 of this loop). READY bar, agreed with e2: READY means no high and no medium defect; a low is fixed where cheap or logged in the calibration record as a known limit; facts about the gate's own behaviour (a true positive that passes, an unmarked partial verdict, an unhashed input that changes a verdict) are never low.
5. Stop path, agreed with e2: if review 3 is NOT READY, one fresh builder fixes and re-freezes, and review 4 judges that freeze; there is no fix 4. If review 4 is NOT READY, put the gate under BLOCKED ON TIGER in `STATE.md` with its open items; Phase 1b and Phase 2 do not start.

After a READY freeze (agreed with e2; brief §9 and §10):

- The development-set rerun is part of the freeze. Then the sealed validation (v3, and whatever owner taps exist on the calibration page; v3 alone if he tapped nothing, and READY then calls the gate weak in those words), zero false passes, run by a gate-side agent that sees counts only. It never waits on the owner and is not listed under BLOCKED ON TIGER. Record on READY how many taps it used and the total prompt-revision count.
- Then recheck the five exemplars under the READY freeze (see section 7), run taught-yet on every takeaway under the READY `lib.mjs`, update `docs/pass-31-takeaway-check.md`, and tick in `docs/todo.md`: "Development set", "Judge prompt frozen", then "Five exemplars" (after the rechecks, fact checks and label newcomer reads), then "Validation run".

Under `982670b`'s code (provisional, its review said NOT READY): all five exemplars passed every mechanical check (labels per panel 1.5: 6 and 4; 4.8: 8; 10.3: 8 and 8; 13.6: 5 and 8; 17.6: 4 and 5), and taught-yet flagged 0 of the takeaways.

## 5. Phase 1 exemplars (drafts done, not ticked)

Figs 1.5 (Part I), 4.8 (Part II), 10.3 (Part III, redesigned in round 6 as two states: the opening, then the closing; each segment a packet box with its name inside), 13.6 (Part IV, the merged card), 17.6 (Part V). Scripts in `scripts/figs/` (`fig_1_5.py`, `fig_4_8.py`, `fig_10_3.py`, `fig_13_5.py` builds 13.6, `fig_17_6.py`). Plate rules: `docs/pass-31-plates.md`. Each carries its recheck must-fix in its chosen cell.

Run the gate's check on an exemplar (from the gate worktree, against figures-final's tree):

```
cd .claude/worktrees/figures-final-gate
HASH=$(git log -1 --format=%s | grep -o 'fingerprint [0-9a-f]*' | cut -d' ' -f2)   # only on a freeze commit
node tests/pass31/check.mjs <part 1-5> --fig=<fig-id> --tree=<abs path>/figures-final/public --gate1=full --expect-hash=$HASH --json=<scratch>.json
```

`check.mjs` refuses (exit 2) when the worktree's files do not match the fingerprint; never run it while a gate builder is editing.

## 6. What round 6 decided about cuts (do not undo)

- The seen-loss test (brief §7) judges what the reader loses if the card goes: the current figure, its content cell and the blind prose reader's ask, never a takeaway written in the same round. The prose stating the same facts does not make a figure redundant. A figure that shows nothing happening (a dated list, a lineage, a table of names, a notation, the shape of a text) may be cut when the prose holds its facts. A cut needs two agreeing verdicts: the author's and a blind panel's (keep advocate who must name something the figure shows happening that the prose only tells, cut advocate, judge; three skeptics on any cut, at least two upholding). Reversing a verified keep needs a new fact.
- A blind panel that asked "does the figure carry anything the prose cannot?" swung 43 keeps to cut; e2's own round-5 panel had asked the same question. Neither counts as the blind verdict; none of those rows was acted on. Never ask a panel whether words could carry a figure: words can carry any fact.
- The seen-loss panel is law 2's fourth stated exception (brief §18, roles in §6).

## 7. Phase 2 (not started)

Brief §11, chapter by chapter, one chapter per commit. At step 1 for each figure: the takeaway from the ledger (higher row for a merged card), every "Must-fix before" item and every "Phase 2 inputs:" note applied or declined with the reason in chosen (a fact item only "Applied"), "possible cut" notes declined by default. Before a cut is executed at its chapter commit: the keep-direction re-test on the frozen content (freeze `a79eb924` must reproduce), aliases in `public/book.js` `ANCHOR_ALIASES` (bump `?v=`), every "Fig N.M" citation rewritten, the gap sentences added. Build figures only with `python3 scripts/figs/build_into.py "$PWD/public" scripts/figs/fig_X.py` (the scripts otherwise write into the main checkout); after any build, check `git -C /Users/yki/Documents/github/atheric/under-the-code status` is unchanged.

## 8. Tools (`scripts/pass31-author/`)

| Tool | Use |
|---|---|
| `taught-yet.mjs` | `node scripts/pass31-author/taught-yet.mjs <abs path to a gate lib.mjs> <kt.json> <takeaways.tsv>`; kt.json from the gate's `scripts/known-terms.mjs --public=<tree> --strip=<held-strip.json> --out=<path>`; takeaways.tsv is `id<TAB>takeaway` per non-held, non-merged-away row. Make the lib copy with `git archive <freeze> tests/pass31 scripts/known-terms.mjs`, then delete `tests/pass31/prompts.mjs` from the copy without opening it |
| `lint_knows.py` | knows cells never cite a cut candidate, a held figure, a later figure or a merge's lower half |
| `repairs.py` | regenerates `docs/pass-31-repairs.md` from git (edit its `rounds` list) |
| `cutinfo.py`, `cites.py` | a figure's slot, caption id and every "Fig N.M" citation (multi-whitespace safe; skips held material) |
| `shot.cjs`, `svgdiff.cjs` | render an SVG frame; pixel-compare two versions every 50 ms (playwright from `tests/pass25/node_modules`) |
| `calib/` | calibration page: `update3.py <calib dir> <figures-final dir>` refreshes `data.json` from the ledger, `build.py <calib dir>` writes `index.html`; republish with the Artifact tool to the URL in section 2 |
| `scripts/pass31-freeze.py` | the takeaway freeze hash |

Checks before any commit: `npm run -s check:dashes` (no em dashes anywhere a reader sees); takeaways at most 20 words counting the job words and at most two numbers; taught-yet; `lint_knows.py`; when `public/` changes, `tests/pass25` (`traces`, `parity`, `marks`, `ui`, `invariants`; the one known flaky failure is WebKit phone signed-in `/glossary`, which passes when rerun alone: `node invariants.mjs --browser=webkit --only=glossary`). Last results on `24477bd`'s tree: traces 229/0, parity 40/0, marks 106/0, UI 120/0, invariants 807/1 (that flake).

## 9. Hard rules and lessons

- Never deploy (push `main`) without the owner's word. The book is "still being built": never call it live or released.
- The seal: never check out, render or read commit `93aae05` or `docs/pass-31-sealed/`. The author never reads the judge prompts (`tests/pass31/prompts.mjs`, `docs/pass-31-calibration.md`).
- Held material (35 figures, Chapter 15, sections ch3-overflow, ch3-defenses, ch9-security, ch10-attacks, ch12-security, ch13-injection, ch14-hashing, and the paragraphs ch16-numa-p4, ch8-substrates-p5, ch1-cpu-p9 to p11, ch2-twos-p10 and p11): never drafted, analysed or quoted; every tester's input leaves it out; never reword to get past the safety filter.
- One author writes; agents only test, blind. Every takeaway rewritten after its last blind newcomer read gets another blind read before it counts (the 9.2 fact error came from skipping this).
- Never launch a Workflow with placeholder or empty `args`; paste the literal JSON.
- In shell heredocs, quote the delimiter (`<<'EOF'`) or backticks run as commands. A regex rename of a label can hit prose: check the hits.
- Do not change `public/` while a panel or check is reading it.
- Facts follow `UNDER.md` §4g; a new fact only with its source opened.
- Session limits kill background runs; resume a workflow with `resumeFromRunId`, and ask e2 to resume its runs.

## 10. Next steps, in order

1. Get e2's result for `wuq24i5rs` (Phase 0 check of `24477bd`); act on it as in section 3; tick the Phase 0 items when it confirms.
2. Gate: freeze `19040ce`'s code (dev set rerun) or have a fresh builder do so, then review 3 under the READY bar, then the stop path (section 4).
3. On a READY freeze: sealed validation (section 4), exemplar rechecks with fact checks and label newcomer reads, taught-yet on the takeaways; tick the gate, development-set, exemplar and validation items.
4. Phase 2, Part I first (Ch1, Ch2, Ch3, the Bridge), one chapter per commit, with the drift check after each part (brief §14).
5. READY page for the owner (brief §16); deploy only on his word.
