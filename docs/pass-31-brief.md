# PASS 31 BRIEF: figure finalization (every figure designed, one at a time)

Written 2026-10-23. Status: **running since 2026-10-23** (started by the owner's figure-finalization heartbeat). Runs on branch `figures-final`, cut from `owner-calls` (the owner calls decided 2026-10-23, `UNDER.md` §4af, not yet deployed); `main` stays at 1.0-rc2 until the owner says deploy. Ledger: `UNDER.md` §4ag, opened by the first Phase 0 commit. Progress: `docs/todo.md`, "Figure finalization".

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

- **Two jobs a figure can do** (the owner's two-part rule): show **the real thing** (Fig 1.2 Enigma, praised because it draws the real machine) or show **the function** (Fig 1.1 v4, approved: one calm scene, the core function, about five labels, motion that is the mechanism, the result stated). A two-part figure does both, in two panels of one card. Every intent sentence names the job, and the gate tests only that job.
- **Why Enigma is good** is written in one sentence in Phase 0, before any gate runs. Enigma's Pass 30 reader could not say what the machine was for; under its "real thing" job that is not a failure.
- **Owner verdicts on record:** v4 approved; v1 `4392ca0` (binary, jargon), v2 `c18836c` (unexplained state labels), v3 `93aae05` (~30 text pieces) rejected; Enigma praised. All are Part I. Parts II to V have no owner verdict yet (section 9).

## 5. What stands from the first verdict, and what changes

Stands:
- contact sheets; one exemplar per part from an empty script, with its plate rules;
- the intent sentence first; several genuinely different concepts per figure, each from an empty script;
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

- **Author.** One agent (Opus 5.5) designs every figure and writes every changed sentence. It learns from the gate only pass or fail and the name of the failed criterion, never the judge prompts.
- **Gate builder.** A separate agent builds and tunes the gate harness. It never sees the sealed items, and sees validation results as counts only.
- **Testers** (fresh blind subagents, Sonnet 5.5, never editing or advising):
  - the judge, who describes the figure from its frames;
  - the scorer, who compares that description with the intent sentence;
  - the prose reader, who reads a chapter's prose only and writes what each figure there must show;
  - the fact checker, who checks every number, name and date in a figure against §4g and the section prose.
- **Sealing is procedural, and that is stated on the READY page.** The repo is public and everything runs in one model family. Sealed material (v3's renders and results, the owner's taps) sits in `docs/pass-31-sealed/`, which is gitignored and never pushed. Only the validation run reads it; the gate builder and the judge prompts never get it; every read is logged in the ledger. The author does see the taps arrive and v3 exists in git history, so the seal guards the gate's tuning, not the author's knowledge.

## 7. Phase 0 · survey and tools (two tracks in parallel)

**Author track:**
- Branch `figures-final` from `owner-calls` (rebase onto `origin/main` once `owner-calls` is deployed). Add `docs/pass-31-sealed/` to `.gitignore` before anything is sealed. Open `UNDER.md` §4ag and STATE.md's "Pass 31 at:" line.
- Contact sheets per chapter at 375 px, with v4 and Enigma pinned (`npm run fig:sheet`).
- **Prose subtraction, chapter by chapter.** Delete each figure, reread its paragraph, write down what is lost.
  - Nothing lost: the figure is cut (section 12).
  - Two figures that each half-carry one idea: they merge into one two-part figure.
  - The record of each decision goes in the ledger.
- **One intent sentence per remaining figure**, tagged "real thing" or "function": "[what] [changes] because [cause], so [result]. The newcomer already knows [an everyday thing or an earlier figure]." The prose reader reads the chapter and writes what each figure must show; where it asks for more than the intent, the author raises the intent. This stops modest intents passing easily.
- The Enigma sentence (section 4).
- The kept-originals table: 18 rows, each with its errors from `docs/audit/owner-calls.md` and one recommended action (literal fix, concept-level redraw, or cut).

**Gate builder track:**
- `figlib`: a `role` keyword on `text()` that writes `data-role="label"` or `data-role="object"` on the `<text>`, and an `obj()` group helper (section 15); `Timeline` exports its beat times. Existing scripts keep building untagged; tags are added as each figure comes up.
- `bare.mjs`: a `--no-text` option that removes every `<text>` before capture.
- `tests/pass31/gate.mjs` (`npm run fig:gate -- <id>`):
  - renders a strip of 12 frames sampled evenly across the cycle, plus the t=0 still, with `bare.mjs`;
  - renders the same strip with `--no-text`;
  - builds the judge packet with the book's prose up to the figure (every earlier section, and the paragraphs before the figure in its own section), never the caption or strip;
  - runs the judge, the scorer and the hedge check;
  - runs the pairwise comparison with the figure's rc2 version.
- `tests/pass31/check.mjs` (`npm run fig:check -- <part>`): Gate 1 as in Pass 30 (`figs.mjs`, `clip.mjs`, `smooth.mjs`), the label cap, the 11 px floor, the taught-yet token check (section 15), t=0 with no empty band taller than a quarter of the plate, `<desc>` present, caption at most two sentences, strip at most 150 words, dashes, anchors.
- `tests/pass31/sheet.mjs` (`npm run fig:sheet`). Scripts added to `package.json`.
- **Development set:** v1 and v2 must fail, v4 must pass, each three times with the order swapped on pairwise tasks. v3 stays sealed. The Go deeper black slab is left out (it is a UI component, not a figure). Video is used only if a judge is shown to read it.
- The judge prompt is frozen and its hash written to `docs/pass-31-calibration.md`.

**Exit:** the gate frozen; the cut list with its evidence; the ledger `docs/pass-31-ledger.tsv` with one row per figure: id, part, job, bin, intent, knows, subtraction record, concepts tried and why rejected, chosen and why, gate result, failed criterion, date, commit, status.

## 8. Phase 1 · exemplars

- The hardest figure in each of the five parts, chosen by the author from the sheets, from an empty script, with three concepts.
- **One page of plate rules per part** in `docs/pass-31-plates.md`: grid, type, three motion verbs drawn from the part's motif, and how its recurring things are drawn (for example, Greenbar's register, Chart Room's packet). These are written rules, never shared drawing code, so each figure is still designed by hand.
- **Exit:** all five exemplars clear Gate 1, the fact checker and the frozen gate's mechanical checks. They go through the judge after validation (section 10), before Phase 2; an exemplar that fails is redone from a new concept.

## 9. Owner touchpoint 1 · the calibration page (one page, about 15 minutes, sent once)

One claude.ai page that records his taps:
- **Line one, in plain words:** "This reverses your 2026-10-11 call on the kept originals. Reply yes to apply the table below. Silence keeps your call."
- **The kept-originals table:** 18 rows, each with its errors and one action.
  - The literal error fixes are open audit owner calls (`docs/audit/owner-calls.md`), which he delegated on 2026-10-23 ("take the best option"). They are applied under that delegation, logged, and shown here, except where the safety filter blocks them; a literal fix is not a redraw.
  - Fig 3.10: the recommendation is a concept-level replacement. He can write "human illustrator" instead, or make the literal fixes himself (the exact list is on the row).
- **The five exemplars,** before and after, each with yes or no.
- **The current contact sheets:** he taps the 3 best and the 3 worst figures per part, giving 30 sealed labels.
- **Cut counts per chapter.** Silence means go, because a cut can be undone.
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
- The gate builder sees counts only. If the run fails, a fresh builder gets one more attempt. If that fails too, Phase 2 does not start, and STATE.md says why under BLOCKED ON TIGER.
- **The gate stays frozen** from here on. Only a failed validation or a drift-check false pass (section 14) reopens it, and any rebuilt gate is validated again on the sealed set before it judges.
- **Final bins:**
  - A Part I figure that passes the gate unchanged is **at bar**. It keeps its drawing, skips the pairwise test and is exempt from the label cap.
  - A figure in Parts II to V is at bar only if it also already meets its part's plate rules.
  - **Redraw:** the concept passes but the plate is wrong. It skips the three-concept step and is drawn new on the plate from its existing concept.
  - **Redesign:** everything else; a new concept through the full loop.
- Tapped figures never become reference figures. Only owner-validated figures are references.

## 11. Phase 2 · chapters

- **Order:** Part I, then Parts II to V and their chapters in book order, so the prose the judge sees before each figure is already final. Inside a chapter, the worst figure first. One chapter per commit; mid-chapter work goes on `figures-final-wip` and is squashed.
- **Per figure:**
  1. The intent sentence from Phase 0, raised if the prose reader asked for more.
  2. Three genuinely different concepts as stills, beside v4, Enigma and the part's exemplar. The author picks one and writes in the ledger why, and why the others lost.
  3. An empty script on the plate rules. The old script stays in git.
  4. Within the label cap; motion only where motion is the mechanism, in the part's motion verbs; t=0 complete, result included; caption at most two sentences, naming the picture.
  5. How-it-works strip at most 150 words, walking the beats, at most one sentence of detail or history.
  6. `<desc>` written from the intent sentence and the beats; `<title>` names the figure.
- **The gate passes a figure when:**
  - the judge's description of the 12-frame strip gives the mechanism in the intent sentence, for the figure's job;
  - the t=0 still alone gives it too;
  - the text-stripped strip still shows what moves and what causes what;
  - there is no hedge on what changes, why, or the result;
  - it beats its rc2 version (a check that it got no worse, not the bar; merged figures and redraws skip it);
  - the fact checker passes it and `fig:check` is clean.
- **Identity is judged per chapter, not per figure.** Comparing a figure with its part's exemplar sets unlike ideas side by side (the first session's reviews 1 and 2). Instead, each chapter's sheet is set beside the exemplar and a blind tester judges whether it reads as one identity.
- **On failure:**
  - each failure means the next concept, never a patch, never an added label;
  - after three failed concepts the figure goes on the **hard list**, which gets one more round of three concepts when the part is finished;
  - if it still fails, the better of the rc2 figure and the best new attempt ships, and READY names it **below bar**. The fact check and the audit's known errors cannot be waived: whichever ships has its facts fixed in place first;
  - a failed figure is never cut; only the subtraction record can cut.
- **Prose.** Words removed from a figure do not move into the prose by default. A sentence is added only where the subtraction record shows a gap, in the same commit. Every sentence citing a changed figure is re-read; the glossary is rebuilt after any prose edit.
- **Every chapter commit includes the figures-only retell.** A blind judge sees only that chapter's figures, in order, and retells the chapter. A gap is fixed in the chapter before the commit.

## 12. Cuts, merges and anchors

- **Figures are never renumbered.**
  - **Cut:** a gap stays in the numbering, visible to the reader; that is the price of the anchor law. The figure id (where it is an anchor) and its caption's paragraph id get `ANCHOR_ALIASES` entries pointing at the nearest surviving paragraph. Every "Fig N.M" citation of it is rewritten in the same commit.
  - **Merge:** the merged figure keeps the lower number and id. The higher figure's anchors are aliased the same way, and its citations are rewritten in the same commit.
  - **Verified live:** a stored reading position on a cut or merged id lands on its alias target. Surviving anchors stay at zero pixel delta. `ANCHOR_ALIASES` lives in `public/book.js`, so its `?v=` is bumped.
- Ids are never reused. §4g entries keyed by figure number stay valid.
- Every cut carries its subtraction record in the ledger. READY shows the cut counts per chapter.

## 13. Kept originals, heroes, cover, open calls

- **With his yes:** each kept original is rebuilt from an empty script under Phase 2's loop, in its chapter, with its audit errors fixed in the drawing, the strip and the prose.
- **Without it:** his call stands. The delegated literal fixes are applied where the filter allows; the figure otherwise stays as it is, is exempt from the label cap, the 11 px floor and the caption check (as in Pass 30), and is listed on READY with what remains wrong. Fig 11.7's eight-sentence caption is one of these.
- **Figs 3.7 and 3.10 under the safety filter:** one concept-level attempt each, one session at most, with no addresses, payloads or working chain. If the filter blocks it, never reword to get past. The figure takes the path he chose on the page (human illustrator, his own literal fixes, or a cut with aliases), and READY lists it.
- **Fig 18.6's caption is owner text:** typeset, never rewritten, and exempt from the caption check.
- **The 7 Pass 30 figure calls** were decided on `owner-calls` (§4af: Figs 6.6, 6.9 accepted, 12.3 option b; heroes Ch1 and Ch3 labelled, Ch12 and the cover accepted). This pass starts from those results; a redesign still goes through the full loop.
- **Heroes and the cover** come after Part V, through the same gate, on their parts' plate rules.
- **Audit owner calls.** Decided on `owner-calls` (§4af), except Chapter 3's figures and captions, which are decided in this pass under the delegation where the safety filter allows. This branch rebases onto `origin/main` once `owner-calls` is deployed.

## 14. Drift and continuity

- **Drift check:** after each part, the sealed set runs again. Any false pass stops the work; the builder rebuilds the gate, and that part is judged again.
- **Session open:** read this brief, STATE.md, the ledger and `git log`; rebase onto `origin/main`; run `fig:check` on the last finished chapter; take the next open row.
- **Session close:** end on a chapter commit (or push the wip branch), update the ledger and STATE.md's "Pass 31 at:" line, push.
- **Branch rule:** rebase onto `origin/main` at every session start and before every chapter commit. A conflict inside a figure card is resolved by re-running its script; a prose conflict keeps `main`'s text and re-applies this pass's change. Bump the `?v=` on a part's CSS and JS links when either changes. Nothing reaches `main` without the owner's word.

## 15. Where this brief changed the council's wording, and why

- **The cap counts labels, not glyphs.** The council kept "at most 8 `<text>`". Enigma, the owner's praised reference, has 26 `<text>` elements, most of them key and lamp letters, and only 6 of 204 current figures have 8 or fewer. So `text()` takes a `role`:
  - `object` text is free: glyphs inside a drawn object, in an `obj()` group that also holds a shape, at most 6 characters per element (a key letter, "€100", a counter's value). Longer text counts as a label whatever its tag.
  - `label` text (names, notes, legends, instructions) is capped at 8 per panel. Legends have at most two entries. Any repair that raises the label count is rejected.
  - At-bar figures are exempt from the cap.
- **The text-stripped test removes every `<text>`,** as the council wrote, so it needs no tags and also runs on untagged rc2 versions.
- **No per-figure comparison with the exemplar.** The council's verdict had "not judged weaker than its part's exemplar"; the first session's own reviews showed that compares unlike ideas, so identity is judged per chapter sheet (section 11).
- **Taught-yet is also checked mechanically.** A judge cannot forget what it knows, so besides seeing the prose up to the figure, every label and object token must be a number or arithmetic sign, a term `known-terms.mjs` lists before the figure's section (run with `--out` to a scratch path), or an everyday word (in `/usr/share/dict/words`, not a glossary term anywhere in the book, not an all-capitals abbreviation of two or more letters). EAX, CGNAT, IHL and "/22" fail.
- **Captions are anchors too,** so every cut and merge aliases the caption paragraph id as well as the figure id.
- **The strips carry more words than the drawings** (15,983 against 13,145), so they get the 150-word limit and the same checks.
- **`<desc>` is what screen readers read,** so it is rewritten with every changed figure.
- **12 frames, not video,** because the judge reads images.

## 16. Owner touchpoint 2 · READY

One page:
- a before/after sheet per part;
- cut counts per chapter;
- the below-bar list;
- kept originals whose errors remain because his silence kept them;
- the gate's validation result, and any part identity he did not confirm;
- the request for his deploy word.

Then his full read, from `docs/owner-read-map.md`.

## 17. Done

- Every remaining figure has a complete ledger row and has passed the validated gate (with a clean final drift check), the label cap (at-bar and kept figures exempt) and the fact checker, or is on the below-bar list with its facts fixed.
- No known error remains, except in kept originals his silence preserved, and those are listed.
- Every chapter's retell has passed. A blind tester judges each part's final sheet as one identity, against its exemplar.
- Anchors identical or aliased; all figure citations correct; glossary rebuilt; `check:dashes` clean; `tests/pass25` at its recorded baseline.
- **No gate declares this pass done.** It is done when his full read sends back no figure. Wording keeps "still being built" until then.

## 18. Rules carried over

- The four laws in `CLAUDE.md` and `docs/working-laws.md`, with three stated exceptions for figures, on the owner's 2026-10-23 instruction ("as many token / time it needs"):
  - law 6's per-chapter recipe is replaced by this pass's gate;
  - law 2's "no gate loops" is set aside for the concept loop, while its core holds: one author writes, testers only describe, blind, and never edit, advise or vote;
  - law 4's "no owner review in the loop" allows the one calibration page, which the first session's problem statement allowed ("one small calibration sample at the start").
  Law 5 holds: section 9 bounds a late answer to one chapter.
- §4g is law; a new fact only with its source opened.
- Anchor ids never change; migrations go through `ANCHOR_ALIASES`, verified live.
- Pushing `main` deploys: only on the owner's word.
- Never ask the owner questions mid-work beyond the one calibration page; owner calls go to STATE.md's BLOCKED ON TIGER and work continues.
- Safety: concept level for attack figures, the defence or the idea; never hunt for wording that gets past the filter.
