# PASS 31 BRIEF: figure finalization (every figure designed, one at a time)

Written 2026-10-23. Status: **running since 2026-10-23** (started by the owner's figure-finalization heartbeat). Runs on branch `figures-final`, cut from `owner-calls` (the owner calls decided 2026-10-23, `UNDER.md` §4af, not yet deployed); `main` stays at 1.0-rc2 until the owner says deploy. Ledger: `docs/pass-31-ledger.tsv`; pass log: `UNDER.md` §4ag, opened by the first Phase 0 commit. Progress: `docs/todo.md`, "Figure finalization".

**Where the plan comes from.** On the owner's instruction ("use the data that was produced on the first query"), the plan is built from the complete record of the first council session on this problem (the framed problem, five advisor analyses, five peer reviews, the verdict), re-examined by a third council round that read that record whole. The round found that the first verdict's own record falsified its gate, and that it had dropped good ideas raised by single advisors (the prose subtraction test, held-out validation, the owner's explicit word on reversing his decisions). The facts in section 3 were measured in the repo the same day. Section 15 lists where a measured fact forced a change to the council's wording.

## 1. The owner's instruction (2026-10-23)

"Can we create a full figure finalization project. The most important thing is that each needs to be self-explanatory, easy to fucking read and understand, good quality and follow the style of the PART, and the book. Subtly animated, etc etc etc things ... It can take as many token / time it needs, literally."

Quality sets the cost. There is no token or time cap. Volume without quality is still a failure (working law 6).

## 2. Why Passes 28 and 30 fell short

- **Pace.** Pass 28 redrew 204 of 222 figures in about two days.
- **Gates that measured describability.** Pass 30's Gate 2 asked a blind reader for the gist from three stills. Labels carry a gist, so most of its 110 first-round failures were "repaired" by adding labels, keys and glosses; 199 of 204 then passed.
- **The AI judge has a recorded false pass on the reference figure.** Fig 1.1 v3 (`93aae05`) passed an AI teach-back test that v1 and v2 failed. The owner rejected it.
- **Identity was a recolour.** Pass 4 rewrote SVG colour literals and the mono font. No figure was ever designed in its part's identity.
- **Done was declared on gates.** Working law 1 says gates are hygiene and never make anything done.

## 3. Facts (measured 2026-10-23)

- **Inventory.** 222 figures: 204 built by `scripts/figs/fig_X_Y.py` on `figlib.py` (`Timeline` for SMIL, `text()`, part palettes, `splice()` writes the card into `public/part-N.html`); 18 kept originals (hand-written SVG, no script). 210 animate. Plus 18 chapter heroes and the cover. A card holds a label line, the SVG, a caption paragraph and a closed "How it works" strip.
- **Text.** `<text>` per redrawn figure: median 21 (quartiles 16 / 21 / 29, max 124); only 6 of 204 have 8 or fewer. Fig 1.1 v4: 4 elements, 10 words. Fig 1.2 Enigma: 26 elements, most of them key, rotor and lamp letters. Words: 13,145 in SVGs, 15,983 in How-it-works strips (median ~77; Fig 1.1 v4's 148 was accepted).
- **The look today** (contact sheets of all 222 at 375 px, t=0). One vocabulary everywhere: rounded rectangles of monospaced labels on a dark plate, joined by thin lines. Parts differ only in palette and mono font. Several figures are text in a frame (4.1, 9.2, 13.1, 15.1, 15.5). The strongest draw a real object or scene (1.1, 1.2, 1.3, 1.5, 1.7, 9.3, 16.6).
- **Kept originals.** All 18 are unreadable at 375 px. Many carried errors the pre-read audit listed with exact fixes (`docs/audit/owner-calls.md`). On `owner-calls` (2026-10-23, under the owner's delegation) the literal fixes are applied to Figs BR.3, 10.10, 10.11, 11.7, 12.9, 12.10, 13.10, 15.2, 15.4, 15.6, 15.8 and 15.9; Chapter 3's (Figs 3.7 to 3.11 and their captions) remain open, Fig 3.10 with five errors. Claude's safety filter stopped a Fig 3.7 redesign on 2026-10-11 and blocks Fig 3.10 (noted 2026-10-23), including its literal fixes.
- **Motion and reduced motion.** Reduced-motion readers see every SVG paused at t=0; `figlib` already treats t=0 as the story moment. A Claude judge reads images, not video. `tests/pass30/bare.mjs` renders the SVG alone at any SMIL time (`--times`, `--frames`) and width, in Chromium or WebKit, from any tree (`FIG_ROOT`).
- **Screen readers.** All 222 SVGs are `role="img"` with `aria-labelledby` on `<title>` and `<desc>`; 204 have a `<desc>` (the 18 without are the kept originals). Screen readers read those, not the inner `<text>`.
- **Anchors.** Figure ids matching `fig-N-M` (letter suffix allowed) and caption paragraph ids (e.g. `ch3-defenses-p10`) are reading-position anchors stored per reader. Bridge ids (`fig-br-N`) and `fig-18-trace` do not match the pattern, so for those only the caption id is an anchor. Prose cites figures by number in 54 places.
- **Terms taught.** `scripts/known-terms.mjs` lists, per section in reading order, the terms taught before it.

## 4. The bar

- **Two jobs a figure can do** (the owner's two-part rule): show **the real thing** (Fig 1.2 Enigma, praised because it draws the real machine) or show **the function** (Fig 1.1 v4, approved: one calm scene, the core function, about five labels, motion that is the mechanism, the result stated). A two-part figure does both, in two panels of one card; its takeaway names the function, and its real-thing panel is required by its content and must pass the label cap, taught-yet, Gate 1, the fact checker and a hedge-free judge description, but is not scored. **Real thing** means the figure draws a physical object, machine or place as it looks (Enigma's rotors, a vacuum tube, ENIAC's cabinets); text in a frame, a table, a timeline or a schematic is never a real thing (amended 2026-10-24). Every takeaway names the job, and the gate tests only that job.
- **Why Enigma is good** is written in one sentence in Phase 0, before any gate runs. Enigma's Pass 30 reader could not say what the machine was for; under its "real thing" job that is not a failure.
- **Owner verdicts on record:** v4 approved; v1 `4392ca0` (binary, jargon), v2 `c18836c` (unexplained state labels), v3 `93aae05` (~30 text pieces) rejected; Enigma praised. All are Part I. Parts II to V have no owner verdict yet (section 9).

## 5. What stands from the first verdict, and what changes

Stands:
- contact sheets; one exemplar per part from an empty script, with its plate rules;
- the takeaway first; several genuinely different concepts per figure, each from an empty script;
- a label cap, with any repair that raises the count rejected (section 15 says what is counted);
- a failed gate means a new concept, never a patch;
- one chapter per commit, with prose edits, the fact-ledger check, byte-identical or aliased anchors, `check:dashes` and a glossary rebuild;
- the judge sees the book's prose up to the figure, never the caption; a hedge fails; the reduced-motion still must teach alone; the text-stripped test;
- no exhibit framing, no book-wide lexicon, no reading mode or share cards.

Changes:
- the gate is validated on sealed owner labels before it judges anything, and a separate agent builds it;
- cutting moves to the start, with prose evidence; a failed figure never becomes a cut;
- bins for Parts II to V wait for their exemplars;
- silence never reverses an owner decision;
- done is the owner's read, not a gate result.

## 6. Roles

- **Author.** One agent (Opus 5.5) designs every figure and writes every changed sentence. It learns from the gate only pass or fail and the name of the failed criterion, never the judge prompts; it may run the gate's mechanical checks (fig:check, taught-yet), which hold no prompt. That rule is procedural, not technical: the prompts sit on the branch `figures-final-gate`, in the same repository as the author's branch `figures-final`, so the author does not open them, and every exposure is logged in `UNDER.md` §4ag (three so far, all 2026-10-24: two lines of the hedge prompt, seen while checking the builder's progress; a workflow notification summarising the builder's review, which named carve-outs in `prompts.mjs` with line references; and the first follow-up's report and commit messages, which said in a sentence each what its real-thing prompt revisions changed). READY says so.
- **Gate builder.** A separate agent builds and tunes the gate harness. It never sees the sealed items, and sees validation results as counts only.
- **Testers** (fresh blind subagents, Sonnet 5.5, never editing or advising):
  - the judge, who describes the figure from its frames;
  - the scorer, who compares that description with the takeaway only (never the content);
  - the prose reader, who reads a chapter's prose only and writes what each figure there must show;
  - the fact checker, who checks every number, name and date in a figure against §4g and the section prose (and the opened source for a new fact, section 18); the content column lists what to check, and a disagreement is settled by §4g and the prose, never by the content;
  - the newcomer reader, who reads a takeaway or label against the prose before the card and says whether any plain word carries a technical sense not yet taught (its reads are logged in `docs/pass-31-takeaway-check.md`).
- **The seen-loss panel** (section 7; fresh blind subagents): a keep advocate, a cut advocate and a judge, who see the figure, its content cell, the blind prose reader's ask and the prose, never the author's record, with three skeptics on any cut ruling. It decides only whether a cut may go ahead; it never writes a sentence or draws a figure.
- **Sealing is procedural, and that is stated on the READY page.** The repo is public and everything runs in one model family. Sealed material (v3's renders and results, the owner's taps) sits in `docs/pass-31-sealed/`, which is gitignored and never pushed. Only the validation run reads it; the gate builder and the judge prompts never get it; every read is logged in `UNDER.md` §4ag. The author does see the taps arrive and v3 exists in git history, so the seal guards the gate's tuning, not the author's knowledge.

## 7. Phase 0 · survey and tools (two tracks in parallel)

**Author track:**
- Branch `figures-final` from `owner-calls` (rebase onto `origin/main` once `owner-calls` is deployed). Add `docs/pass-31-sealed/` to `.gitignore` before anything is sealed. Open `UNDER.md` §4ag and STATE.md's "Pass 31 at:" line.
- Contact sheets per chapter at 375 px, with v4 and Enigma pinned (`npm run fig:sheet`).
- **Prose subtraction, chapter by chapter.** Delete each figure, reread its paragraph, write down what is lost.
  - Nothing lost: the figure is cut (section 12). The seen-loss test judges what the reader loses if the card goes, never a takeaway written in the same round; the takeaways, and the content cells of the cut candidates, are frozen (one hash over every row's id and takeaway and every cut candidate's content, computed by `scripts/pass31-freeze.py`: every data row in file order, held rows included, one line per row, the id and the takeaway joined by a tab, then a tab and the content when the status starts with "cut candidate", lines joined by one newline with none after the last, sha256 of the UTF-8 text; logged in §4ag) before any subtraction runs, and the keep-direction re-test runs on that frozen content, before Phase 2 step 1 re-derives it. The prose stating the same facts does not make a figure redundant. A figure is a loss to cut when it shows something happening (a cause and its effect, a rule at work, a structure doing something) that the prose only tells; it is judged on the current figure together with its content cell and the blind ask, so a figure drawn today as text is judged on the mechanism they name, and its subtraction names that mechanism. A figure that shows nothing happening (a dated list, a lineage, a table of names, a notation, the shape of a text) carries no mechanism and may be cut when the prose holds its facts. A cut needs two agreeing verdicts: the author's, and a blind panel's (a keep advocate who must name something the figure shows happening that the prose only tells, a cut advocate and a judge, who see the figure, its content cell, the blind prose reader's ask and the prose, never the author's record), with at least two of three skeptics upholding a cut; a weaker case is logged on the row as "Phase 2 inputs: possible cut" and not acted on. Reversing an earlier verified keep needs a new fact, not a reapplied rule. Every cut candidate is re-tested this way, in the keep direction only, at its chapter's Phase 2 commit before the cut is executed: a cut that fails reverts to keep, and the re-test makes no new cut (the round-5 and round-6 panels both asked whether words could carry the figure, so neither counts as the blind verdict). Two drawings keep for what they are: a figure that teaches symbols later kept figures draw and no prose can teach (the gate symbols of Fig 2.3), and a chart whose shape is a law at work (a doubling as a straight line on a tenfold scale, a curve like entropy's). A kept original, a figure the owner accepted, or a card holding owner text (Fig 18.6's caption, section 13) keeps on his call. (Amended in round 5, after the pre-commit checks found the test applied to the cut list only; and in round 6, after session e2 found the round-5 form circular, since the author's own takeaway decided the loss, and after a blind panel that asked whether words could carry each figure swung 43 keeps to cut.)
  - Two figures that each half-carry one idea: they merge into one card (a merged card), but only if the two halves share one mechanism; otherwise both stay, or one is cut.
  - The record of each decision goes in the ledger.
- **One intent per remaining figure, in two parts** (amended 2026-10-24 after session e2's verification: a long intent rewards text-heavy figures, since the scorer grades against it).
  - The **takeaway** (ledger column `intent`): at most 20 words counting its opening job words, one mechanism, at most two numbers, every token passing taught-yet, opening with its job ("Function:" or "Real thing:"). "[what] [changes] because [cause], so [result]." It states the mechanism the figure draws (what changes, and why), not only the result, and is checked against the drawing and the section prose. A term first taught in the figure's own caption, labels or strip is not taught: the judge never sees them. The scorer grades only this.
  - The **content** (column `content`): the names, numbers and fields the figure, its strip, the prose and the fact checker need. Phase 0's content is a starting point: Phase 2 step 1 re-derives it in full from the figure, its caption, its strip and the section prose. A decision the redraw must keep (what to drop, what must survive) therefore goes in the subtraction column, which Phase 2 does not re-derive (or is appended to the chosen column, from which Phase 2 never deletes).
  - **Knows** (column `knows`): what the newcomer already knows, an everyday thing or an earlier figure that will survive (never a later figure, a cut candidate, a held figure, or the lower half of a merge). The higher half of a merge may be cited, because the merged card keeps its number and id; the lower half's row never cites its own partner. A cited paragraph id is allowed only once it has been checked to say what knows claims.
  - The prose reader reads the chapter and writes what each figure must show. Its asks go to the content, or are declined with a reason; an ask showing the takeaway is too modest raises the takeaway. `docs/pass-31-prose-readers.tsv` records each ask and its disposition: Phase 0 recorded the raises, and Phase 2 step 1 records, figure by figure, whether the ask went to the content or was declined and why. ("The ledger" in this brief means `docs/pass-31-ledger.tsv`; `UNDER.md` §4ag is the pass log.) This stops modest takeaways passing easily.
- The Enigma sentence (section 4).
- The kept-originals table: 18 rows, each with its errors from `docs/audit/owner-calls.md` and one recommended action (literal fix, concept-level redraw, cut, or held: no attempt in this pass, listed for the owner).

**Gate builder track:**
- `figlib`: a `role` keyword on `text()` that writes `data-role="label"` or `data-role="object"` on the `<text>`, and an `obj()` group helper (section 15); `Timeline` exports its beat times. Existing scripts keep building untagged; tags are added as each figure comes up.
- `bare.mjs`: a `--no-text` option that removes every `<text>` before capture.
- `tests/pass31/gate.mjs` (`npm run fig:gate -- <id>`):
  - renders a strip of 12 frames sampled evenly across the cycle, plus the t=0 still, with `bare.mjs`;
  - renders the same strip with `--no-text`;
  - builds the judge packet with the book's prose up to the figure (every earlier section, and the paragraphs before the figure in its own section), leaving out held material (the held figures' cards and captions, Chapter 15, the sections ch3-overflow and ch3-defenses, every section whose only figures are held, found by structure (ch9-security, ch10-attacks, ch12-security, ch13-injection, ch14-hashing), and the held paragraphs), with a test that no held id reaches a packet, never the caption or strip; every other tester (the prose reader, the newcomer reader, the fact checker, the seen-loss panel) leaves held material out too, and the list of held ids, sections and paragraphs is `tests/pass31/held-strip.json` on the gate branch;
  - runs the judge, the scorer and the hedge check;
  - runs the pairwise comparison with the figure's rc2 version.
- `tests/pass31/check.mjs` (`npm run fig:check -- <part>`): Gate 1 as in Pass 30 (`figs.mjs`, `clip.mjs`, `smooth.mjs`), the label cap, the 11 px floor, the taught-yet token check (section 15), t=0 with no empty band taller than a quarter of the plate, `<desc>` present, caption at most two sentences, strip at most 150 words, dashes, anchors.
- `tests/pass31/sheet.mjs` (`npm run fig:sheet`). Scripts added to `package.json`.
- **Development set:** v1 and v2 must fail and v4 must pass, Fig 1.2 Enigma must pass under its job "real thing", and every decoy must fail (a decoy is a figure built to fail one criterion: a block-schematic Enigma, a frozen Enigma, a figure with no drawn cause, a text-heavy one; the calibration record lists them), each in three independent evaluations, with the order swapped on pairwise tasks. The bar is decisions, not runs: each evaluation is one decision, which passes when at least two of its three complete runs pass, and zero false passes means no figure that should fail passes a decision in any of its three evaluations (a decoy that passes one evaluation of three is a false pass). v3 stays sealed. The Go deeper black slab is left out (it is a UI component, not a figure). Video is used only if a judge is shown to read it.
- The judge prompt is frozen and its hash written to `docs/pass-31-calibration.md`.

**Exit (convergence rule, agreed with session e2, 2026-10-24):** Phase 0 is done when one independent verification by session e2 finds no high and no medium defect in class A: facts against §4g and the prose, every takeaway (newcomer read, fidelity to the drawing, mechanism stated), structure (cuts, merges, aliases, where decisions live), the brief's consistency, and the exemplars under the frozen gate's mechanical checks (section 8's exit; their judge run stays after validation). That verification grades severity (high: misleads the gate, cuts wrongly or ships a false fact; medium: weakens the spec); the author may decline a finding with a logged reason, never re-grade it; a decline is logged in §4ag and settles the finding unless the next verification rejects it. Facts block at any severity. Low class-A findings other than facts, and every class-B finding (content completeness, record wording that Phase 2 step 1 re-derives) become "Phase 2 inputs" notes in the subtraction or chosen column. If the verification after round 6 still finds a class-A high or medium, the ledger stops churning and Phase 0 exits: every open class-A finding, facts included, becomes a must-fix item on its row (facts still block, so a fact item is fixed before its chapter's gate), every brief-level one is fixed in the brief before Phase 1b or listed on READY, and READY says so. A brief-level item is fixed in the brief before Phase 1b, or listed on READY. Also at exit: the gate frozen; the cut list with its evidence; the ledger `docs/pass-31-ledger.tsv` with one row per figure: id, part, job, bin, intent (the takeaway), content, knows, subtraction record (naming the paragraphs reread), concepts tried and why rejected, chosen and why, gate result, failed criterion, date, commit, status.

## 8. Phase 1 · exemplars

- The hardest figure in each of the five parts, chosen by the author from the sheets, from an empty script, with three concepts.
- **One page of plate rules per part** in `docs/pass-31-plates.md`: grid, type, three motion verbs drawn from the part's motif, and how its recurring things are drawn (for example, Greenbar's register, Chart Room's packet). These are written rules, never shared drawing code, so each figure is still designed by hand.
- At least one exemplar is a merged card, since nine merged cards will use that form: Part IV's, Figs 13.5 and 13.6 (the failure, then the log). A merged card carries one takeaway, one job and one mechanism, on the higher half's row (written in Phase 0, so Phase 2 does not grade a merged card against half its idea); its two panels show that mechanism in two parts (the failure, then the cure; the parts, then the function), and the gate scores it as one figure. Part IV's exemplar comes from Chapter 13 or 14, because Chapter 15 is held (amended 2026-10-24).
- **Exit:** all five exemplars clear Gate 1, the fact checker and the frozen gate's mechanical checks. They go through the judge after validation (section 10), before Phase 2; an exemplar that fails is redone from a new concept.

## 9. Owner touchpoint 1 · the calibration page (one page, about 15 minutes, sent once)

One claude.ai page that records his taps:
- **Line one, in plain words:** "This reverses your 2026-10-11 call for Fig BR.3, the one kept original not held. Reply yes to apply its row. Silence keeps your call; the other 17 are in the held block."
- **The kept-originals table:** Fig BR.3's row, with its errors and its action; the 17 held kept originals appear once, in the held-figures block below.
  - The literal error fixes are open audit owner calls (`docs/audit/owner-calls.md`), which he delegated on 2026-10-23 ("take the best option"). They are applied under that delegation, logged, and shown here; a literal fix is not a redraw. Held figures get no attempt: any literal fixes still open in them (Chapter 3's) stay open and are listed on READY.
  - Fig 3.10 is held, like 16 other kept originals: no attempt in this pass. Its options are those of the held figures below; its five errors stay listed with the Chapter 3 calls in `docs/audit/owner-calls.md`, and its row in `docs/pass-31-kept-originals.md` points there.
- **The five exemplars,** before and after, each with yes or no.
- **The held figures** (35, status `held` in the ledger: the attack and security figures Claude's safety filter blocks), each with his options: edit it himself, have it redrawn by another route, keep it, or have it cut (with aliases).
- **The current contact sheets:** he taps the 3 best and the 3 worst figures per part, giving 30 sealed labels. The tap sheets leave the held figures out.
- **Every cut candidate with its one-line reason and a Keep button, and the counts per chapter.** Silence means go, because a cut can be undone, and every cut is re-tested in the keep direction before it is made (section 7); the page says so, and says how the list has changed since he last saw it.
- **What silence does.** Only reversible steps go ahead.
  - An unanswered exemplar goes ahead, and READY marks that part's identity "not confirmed by owner".
  - If he taps nothing, the gate is validated on one held-out item (v3). That is weak, and READY says so in those words.
  - If he rejects an exemplar, it is redone from a new concept and shown once more, because he replied.
  - **When answers stop counting as calibration:** the page's answers shape a part's plate until Part I is committed (Part I alone takes many sessions, so no Part II to V figure is designed before then). After that point an unanswered exemplar is final for the pass, and a later rejection goes to the READY punch list, not back into the loop. A wrong direction then costs at most one chapter (working law 5).
- **Work never waits for the page.** While it is up, the author drafts Chapter 1's concepts. The validation run (section 10) takes the taps that have arrived when those drafts are ready; this timing is deliberate. Taps arriving later join the sealed set for the drift checks.

## 10. Phase 1b · validation (one sealed run), then the final bins

- Run the frozen gate on v3 plus the owner's taps, using its single-figure criteria only: the 12-frame description, the t=0 still, the text-stripped strip, the hedge rule and taught-yet (section 11). The pairwise test does not run here, because a tapped figure is its own rc2 version.
- **It passes if:**
  - v3 fails and v4 passes;
  - every tapped-worst figure fails;
  - at least half of the tapped-best figures pass.
- **Zero false passes is the bar.** False passes are what failed twice; a strict gate costs only tokens.
- **Before validation,** a gate builder's attempt has at most three prompt revisions. Any change to a gate file reruns the development set (section 7, under the gate's rule that a figure's decision is two passing runs out of three) and re-freezes with a new fingerprint, and every gate run first checks its files against the frozen fingerprint. A checker false flag is fixed in the checker, with regression tests for the true positives it must still catch, never by a per-figure exemption; an everyday word that matches a glossary term keeps failing in the gate; on a Phase 0 takeaway, a logged newcomer read decides whether the word stays (its plain sense is the one meant) or is reworded.
- The gate builder sees counts only. If the run fails, a fresh builder gets one more attempt. If that fails too, Phase 2 does not start, and STATE.md says why under BLOCKED ON TIGER.
- **The gate stays frozen** from here on. Only a failed validation or a drift-check false pass (section 14) reopens it, and any rebuilt gate is validated again on the sealed set before it judges.
- **Final bins:**
  - A Part I figure that passes the gate unchanged is **at bar**, unless an open "Phase 2 inputs:" note or must-fix item on its row needs a change to the drawing; then it is not at bar until that is applied. At bar, it keeps its drawing, skips the pairwise test and is exempt from the label cap.
  - A figure in Parts II to V is at bar only if it also already meets its part's plate rules.
  - **Redraw:** the concept passes but the plate is wrong. It skips the three-concept step and is drawn new on the plate from its existing concept.
  - **Redesign:** everything else; a new concept through the full loop.
- Tapped figures never become reference figures. Only owner-validated figures are references.

## 11. Phase 2 · chapters

- **Order:** Part I, then Parts II to V and their chapters in book order, so the prose the judge sees before each figure is already final. Inside a chapter, the worst figure first. One chapter per commit; mid-chapter work goes on `figures-final-wip` and is squashed.
- **Per figure:**
  1. The takeaway from Phase 0 (for a merged card, the higher row's), raised only where a prose reader's ask showed it too modest (section 7), and the ask's disposition recorded in `docs/pass-31-prose-readers.tsv`; the content re-derived in full from the figure, its caption, its strip and the section prose; and every "Phase 2 inputs:" note and every "Must-fix before <event>:" item on the row (the higher row for a merged card) is applied, or declined with the reason in chosen, before the gate runs; an item is closed on the row with "Applied <date or commit>" or "Declined: <reason>". A "Phase 2 inputs: possible cut" note is never applied: it is declined by default under section 7, and the decline is logged in chosen.
  2. Three genuinely different concepts as stills, beside v4, Enigma and the part's exemplar. The author picks one and writes in the ledger why, and why the others lost.
  3. An empty script on the plate rules. The old script stays in git.
  4. Within the label cap; motion only where motion is the mechanism, in the part's motion verbs; t=0 complete, result included; caption at most two sentences, naming the picture.
  5. How-it-works strip at most 150 words, walking the beats, at most one sentence of detail or history.
  6. `<desc>` written from the takeaway and the beats; `<title>` names the figure.
- **The gate passes a figure when:**
  - the judge's description of the 12-frame strip gives the mechanism in the takeaway, for the figure's job;
  - the t=0 still alone gives it too;
  - the text-stripped strip still shows what moves and what causes what;
  - there is no hedge on what changes, why, or the result;
  - it beats its rc2 version (a check that it got no worse, not the bar; merged figures and redraws skip it);
  - the fact checker passes it and `fig:check` is clean;
  - no "Must-fix before" item is open on its row (each closed with "Applied" or "Declined");
  - a real-thing panel in a function card gets its own hedge-free judge description of what it shows (checked, not scored, section 4);
  - a newcomer read of the takeaway and every label is logged (section 15).
- **Identity is judged per chapter, not per figure.** Comparing a figure with its part's exemplar sets unlike ideas side by side (the first session's reviews 1 and 2). Instead, each chapter's sheet is set beside the exemplar and a blind tester judges whether it reads as one identity.
- **On failure:**
  - each failure means the next concept, never a patch, never an added label;
  - after three failed concepts the figure goes on the **hard list**, which gets one more round of three concepts when the part is finished;
  - if it still fails, the better of the rc2 figure and the best new attempt ships, and READY names it **below bar**. The fact check and the audit's known errors cannot be waived: whichever ships has its facts fixed in place first;
  - a failed figure is never cut; only the subtraction record can cut.
- **Prose.** Words removed from a figure do not move into the prose by default. A sentence is added only where the subtraction record shows a gap, in the same commit. Every sentence citing a changed figure is re-read; the glossary is rebuilt after any prose edit.
- **Every chapter commit includes the figures-only retell.** A blind judge sees only that chapter's figures, in order, and retells the chapter. Held figures are left out; the judge is told one sits there. A gap is fixed in the chapter before the commit; a gap that sits at a held figure is listed for the owner instead.

## 12. Cuts, merges and anchors

- **Figures are never renumbered.**
  - **Cut:** a cut candidate is re-tested in the keep direction at its chapter's commit, before it is executed (section 7), and his Keep taps win. A gap stays in the numbering, visible to the reader; that is the price of the anchor law. The cut row records its alias targets now, and its prose reader's ask is dispositioned in `docs/pass-31-prose-readers.tsv` (carried by a paragraph, or declined with the reason). The figure id (where it is an anchor) and its caption's paragraph id get `ANCHOR_ALIASES` entries pointing at the nearest surviving paragraph. Every "Fig N.M" citation of it is rewritten in the same commit.
  - **Merge:** only halves that share one mechanism merge (section 7). The merged figure keeps the HIGHER half's number, id and slot, after every paragraph between the two halves, so its drawing uses only what is taught before it, and its caption keeps the higher half's caption id. The lower half's figure id and caption id are aliased to the paragraph just before its old slot, so a stored reading position resumes before text the reader has not read; no alias points at an id that is itself aliased (`book.js` follows one hop), and a check confirms every alias target exists on its page. Citations of the lower number are rewritten to the higher in the same commit; the gap in the numbering is visible, as for a cut. Every durable decision for a merged card (labels, wording, rejected concepts) sits on the higher row, which Phase 2 reads. The lower half's ledger row keeps its records, with the alias note in its subtraction column, and its prose reader's ask is dispositioned on the merged card's content; its status reads "merged into" the higher id, its takeaway cell says "Merged into Fig N.M" with no takeaway of its own, and the ledger checks skip it. Until Phase 2 applies a merge, both rows read "merge candidate with" the other: the higher row holds the merged card's one takeaway and every durable decision, the lower row's takeaway is only a record of its half (not scored; the takeaway checks count it apart), and its prose reader's ask is dispositioned at the higher row's Phase 2 step 1, on the merged card's content.
  - **Held material:** this pass edits nothing inside a held figure's card or caption, or in the held sections (ch3-overflow, ch3-defenses, Chapter 15, and every section whose only figures are held, found by structure (ch9-security, ch10-attacks, ch12-security, ch13-injection, ch14-hashing)) and held paragraphs. A cut or merge whose citation sits there goes ahead, and the stale citation is listed on READY for the owner (none at present: Fig 3.4, the one such case, is now a keep). A held figure is cut only on his order (section 13), with aliases and citations handled as for any cut.
  - **Verified live:** a stored reading position on a cut or merged id lands on its alias target. Surviving anchors stay at zero pixel delta. `ANCHOR_ALIASES` lives in `public/book.js`, so its `?v=` is bumped.
- Ids are never reused. §4g entries keyed by figure number stay valid.
- Every cut carries its subtraction record in the ledger. READY shows the cut counts per chapter.

## 13. Kept originals, heroes, cover, open calls

- **With his yes:** each kept original that is not held (Fig BR.3) is rebuilt from an empty script under Phase 2's loop, in its chapter, with its audit errors fixed in the drawing, the strip and the prose.
- **Without it:** his call stands. The delegated literal fixes are applied to the kept originals that are not held (Fig BR.3); the figure otherwise stays as it is, is exempt from the label cap, the 11 px floor and the caption check (as in Pass 30), and is listed on READY with what remains wrong.
- **Held figures (standing rule, 2026-10-24):** the safety filter stopped work on the attack and security figures three times on 2026-10-23, so this pass makes no attempt on any held figure, Figs 3.7 and 3.10 included, and never rewords to get past the filter. A held figure stays as it is (Fig 11.7's eight-sentence caption included) unless he edits it, has it redrawn by another route, or asks for a cut (with aliases). READY lists each with its status. Of the 18 kept originals, 17 are held; only Fig BR.3 goes through the loop.
- **Fig 18.6's caption is owner text:** typeset, never rewritten, and exempt from the caption check.
- **The 7 Pass 30 figure calls** were decided on `owner-calls` (§4af: Figs 6.6, 6.9 accepted, 12.3 option b; heroes Ch1 and Ch3 labelled, Ch12 and the cover accepted). This pass starts from those results; a redesign still goes through the full loop.
- **Heroes and the cover** come after Part V, through the same gate, on their parts' plate rules. Chapter 15's hero is held: no attempt; it is listed with the held figures.
- **Audit owner calls.** Decided on `owner-calls` (§4af), except Figs 3.7 to 3.11 and their captions, which are held: no attempt in this pass, listed on READY. This branch rebases onto `origin/main` once `owner-calls` is deployed.

## 14. Drift and continuity

- **Drift check:** after each part, the sealed set runs again. Any false pass stops the work; the builder rebuilds the gate, and that part is judged again. One rebuild per drift failure, by a fresh builder; a second failure goes to BLOCKED ON TIGER, as in section 10.
- **Session open:** read this brief, STATE.md, the ledger and `git log`; rebase onto `origin/main`; run `fig:check` on the last finished chapter; take the next open row.
- **Session close:** end on a chapter commit (or push the wip branch), update the ledger and STATE.md's "Pass 31 at:" line, push.
- **Branch rule:** rebase onto `origin/main` at every session start and before every chapter commit. A conflict inside a figure card is resolved by re-running its script; a prose conflict keeps `main`'s text and re-applies this pass's change. Bump the `?v=` on a part's CSS and JS links when either changes. Nothing reaches `main` without the owner's word.

## 15. Where this brief changed the council's wording, and why

- **The cap counts labels, not glyphs.** The council kept "at most 8 `<text>`". Enigma, the owner's praised reference, has 26 `<text>` elements, most of them key and lamp letters, and only 6 of 204 current figures have 8 or fewer. So `text()` takes a `role`:
  - `object` text is free: glyphs inside a drawn object, in an `obj()` group that also holds a shape, at most 6 characters per element (a key letter, "€100", a counter's value). Longer text counts as a label whatever its tag.
  - `label` text (names, notes, legends, instructions) is capped at 8 per panel. A panel is a `<g data-panel>` group showing one state or one view of the scene; a card has at most two, and a card drawn with more counts as one panel for the cap. Legends have at most two entries. Any repair that raises the label count is rejected.
  - At-bar figures are exempt from the cap.
- **The text-stripped test removes every `<text>`,** as the council wrote, so it needs no tags and also runs on untagged rc2 versions.
- **No per-figure comparison with the exemplar.** The council's verdict had "not judged weaker than its part's exemplar"; the first session's own reviews showed that compares unlike ideas, so identity is judged per chapter sheet (section 11).
- **Taught-yet is also checked mechanically.** A judge cannot forget what it knows, so besides seeing the prose up to the figure, every label and object token must be a number or arithmetic sign, a term the book's prose teaches before the card (known-terms for earlier sections, and the paragraphs before the card in its own section) (known-terms leaves out held material too: a term taught only there is untaught for later figures) (run with `--out` to a scratch path), or an everyday word (on the common-word list or in `/usr/share/dict/words`, and not a glossary term anywhere in the book; a token of three letters or fewer whose capital form is an abbreviation the book uses, such as ax, al, ram, os or lan, must be taught, since the dictionary holds it). Because a dictionary word can carry a technical sense (bucket, port, edge, node), every takeaway and label also gets a newcomer read, logged in `docs/pass-31-takeaway-check.md`. Inflections of a passing word pass (adds, added, adding). A term first taught in the figure's own caption, labels or strip does not count as taught. Teaching happens in the chapters' prose: their paragraphs (lead paragraphs included) and list items, and a table row that expands or defines the term (a row that only lists it, with values, does not); headings, section labels, chapter previews, part taglines and anything inside a card never teach. A plural or possessive of an abbreviation (DRAMs, RAM's) is judged as the abbreviation, and a prefix comes off a token only when what remains is a word as written (upload, rewrite), never to turn a name or an abbreviation into everyday words (redis is not re plus dis). An all-capitals token passes when its lowercase form is on the common-word list (AND, THE) or when known-terms lists it as taught before the figure; abbreviations the prose teaches (CPU, RAM, TCP, IP, HTTP, DNS) are listed at the paragraph that teaches them. No per-figure exemptions. An abbreviation the prose never teaches before the figure (CGNAT, IHL) fails, and so does notation such as "/22". The check in force is the gate branch's frozen `tests/pass31/lib.mjs` (the newest freeze whose independent review says READY) with its common-word list, which keeps the dictionary for lowercase words except the short abbreviations above; the older copy on `figures-final` is replaced when the frozen gate is brought over. (Amended 2026-10-24: session e2 found the old all-capitals rule failing 166 of 222 figures on noise; amended again the same day after its second verification found the dictionary clause gameable; and a third time in round 4, to state the dictionary rule as the frozen gate applies it, with the newcomer read beside it; in round 5, after the review of the `c50f7e1` freeze, to say where teaching happens, how plural and possessive abbreviations and prefixes are judged, and which sections are held by structure.)
- **Captions are anchors too,** so every cut and merge aliases the caption paragraph id as well as the figure id.
- **The strips carry more words than the drawings** (15,983 against 13,145), so they get the 150-word limit and the same checks.
- **`<desc>` is what screen readers read,** so it is rewritten with every changed figure.
- **12 frames, not video,** because the judge reads images.

## 16. Owner touchpoint 2 · READY

One page:
- a before/after sheet per part;
- cut counts per chapter;
- the below-bar list;
- the held figures, each with its status (kept as is, edited by him, redrawn elsewhere, or cut on his order), and the open literal fixes in them;
- the stale figure citations left inside held material by cuts and merges (section 12);
- the seal stated as procedural, every exposure of a judge prompt to the author (§4ag), and the gate's attempt count: prompt revisions per freeze, validation runs and drift rebuilds;
- kept originals whose errors remain because his silence kept them;
- kept figures whose strip or caption points into held material (Figs 8.9 and 14.12 in their strips, Fig 18.1.5 in its caption, all pointing to Chapter 15);
- the brief-level items carried under the convergence rule (section 7), each with its status;
- the ledger items carried as must-fix-before-gate under the convergence rule (section 7), each with its status;
- the gate's validation result, and any part identity he did not confirm;
- the request for his deploy word.

Then his full read, from `docs/owner-read-map.md`.

## 17. Done

- **Held figures** are exempt from the gate, the retell and the identity check; they count as listed, not passed (amended 2026-10-24).
- Every remaining figure that is not held has a complete ledger row and has passed the validated gate (with a clean final drift check), the label cap (at-bar and kept figures exempt) and the fact checker, or is on the below-bar list with its facts fixed; Fig BR.3, if his silence keeps it as drawn, is listed as kept instead.
- No known error remains, except in kept originals his silence preserved and in held figures; both are listed with their errors.
- Every chapter's retell has passed (Chapter 15, held whole, has none). A blind tester judges each part's final sheet as one identity, against its exemplar; Part IV's sheet holds Chapters 13 and 14.
- Anchors identical or aliased; all figure citations correct, except citations inside held material, which are listed on READY; glossary rebuilt; `check:dashes` clean; `tests/pass25` at its recorded baseline.
- **No gate declares this pass done.** It is done when his full read sends back no figure that is not held; a held figure he sends back stays a held item for him, not a loop figure, and does not hold the pass open; Fig BR.3, if his silence keeps it as drawn, is listed on READY as kept, not as below bar. Wording keeps "still being built" until then.

## 18. Rules carried over

- The four laws in `CLAUDE.md` and `docs/working-laws.md`, with four stated exceptions for figures, on the owner's 2026-10-23 instruction ("as many token / time it needs"):
  - law 6's per-chapter recipe is replaced by this pass's gate;
  - law 2's "no gate loops" is set aside for the concept loop, while its core holds: one author writes, testers only describe, blind, and never edit, advise or vote;
  - law 2's "testers never advise or vote" is also set aside for the seen-loss panel (section 6), which argues and votes only on whether a cut may go ahead and never writes or draws;
  - law 4's "no owner review in the loop" allows the one calibration page, which the first session's problem statement allowed ("one small calibration sample at the start").
  Law 5 holds: section 9 bounds a late answer to one chapter.
- §4g is law; a new fact only with its source opened.
- Anchor ids never change; migrations go through `ANCHOR_ALIASES`, verified live.
- Pushing `main` deploys: only on the owner's word.
- Never ask the owner questions mid-work beyond the one calibration page; owner calls go to STATE.md's BLOCKED ON TIGER and work continues.
- Safety: held figures get no attempt (section 13); any literal fixes still open in them (Chapter 3's) stay open and are listed on READY. Never hunt for wording that gets past the filter.
