Under the Code 1.0: Pass 29 (the book teaches) and Pass 30 (every picture holds)

THE GOAL AND THE FINISH LINE

This prompt finishes the book. Two passes run in order, then the book is
frozen for the owner's read. Done means all of this is true, committed and
live:
- Pass 29: every section of Parts I to V has been read by the cold reader
  and is repaired, recorded as "already teaches", or listed as an owner
  call; every part verified.
- Pass 30: every figure, chapter hero, the cover and every icon passes Gate 1
  (measured layout) and Gate 2 (the picture speaks for itself), or is listed
  as an owner call; the 18 kept-original figures take Gate 1 only.
- The book is tagged v1.0 if no owner call raised by Pass 29 or 30 is open,
  or v1.0-rc1 otherwise, and STATE.md opens with the line for the tag actually
  cut (see THE CLOSE).
Then stop. Open no new pass, audit or loop without an owner instruction.

The book is close to done. Both passes repair what fails and leave the rest
alone. "Already at bar, left as-is" is the expected verdict for most
sections and most figures, and it is recorded, not apologised for.

Scale, so you can plan: about 116 sections at 5 to 8 agent calls each in
Pass 29, and about 240 pictures in Pass 30. Work one part per session.

BEFORE STARTING

1. Save this prompt as docs/pass-29-30-brief.md and commit it. It must
   survive across sessions. Add to STATE.md a line "Pass 29/30 at:
   <pass, part, section or figure, step>" and keep it current. Every later
   session reads docs/pass-29-30-brief.md and STATE.md first, continues from
   that line, and never repeats a finished step.
2. Confirm Pass 28 is closed (commit 7d56482, "Pass 28 closed"): in
   docs/pass-28-figures.md every row starts with "done" or reads "kept:
   original", and none is "todo", "held" or "deferred". Confirm the Pass 28
   loop or schedule is stopped and git is clean (untracked scratch folders
   such as shots4/ and .kilo/ are not yours; leave them and do not commit
   them). If any of this fails, stop and say so. Then write two lists at the
   top of docs/pass-30-figures.md and commit:
   - "Security figures (concept level)": every figure that the git history
     of docs/pass-28-figures.md (git log -p) ever marked "deferred:
     conceptual pass" or "held: owner decision" and that now reads "done".
   - "Kept original": the 18 figures that read "kept: original" (3.7 to
     3.11, BR.3, 10.10, 10.11, 11.7, 12.9, 12.10, 13.10, 15.2, 15.3, 15.4,
     15.6, 15.8, 15.9). The owner settled these on 2026-10-11.
3. Read CLAUDE.md (the three laws), BRIDGE.md, UNDER.md §4g (fact ledger),
   §4w (arc devices), §4aa (Pass 27), §4ab (Pass 28) and §5 (known
   non-defects), docs/pass-27-brief.md (its lists of what gets cut and what
   does not still apply) and docs/pass-28-brief.md ("The standard").
4. Confirm the agents you will use can search and fetch the web. If they
   cannot, the teacher only proposes additions with the claim to be sourced,
   and this orchestrating session sources them before they are applied.
5. Build and commit the tools before any edit. Every Playwright import
   resolves from tests/pass25/node_modules, never from an npx cache path;
   fix every script in tests/pass28 (figs, shot, fsshot, clip, smooth) and
   tests/pass25/alias.mjs the same way.
   - scripts/count-prose.mjs: section-prose words per section and per part.
     Run at commit 02f486b it must reproduce §4aa's per-part counts (I
     12,095; II 10,891; III 14,012; IV 9,761; V 6,181; total 52,940), using
     §4aa's per-section tables to calibrate. If after that any part still
     differs by more than 0.5 %, record the differences in STATE.md and use
     the script's own 02f486b counts as the baseline. Then run it at the current HEAD (the
     Pass 28 close) and write to STATE.md, per part: the 02f486b count, its
     5% ceiling, the current count, and the headroom left.
   - scripts/known-terms.mjs: for each section in reading order, the terms
     the book has taught before it, from public/glossary.json (each entry's
     first-use part and section) plus key-term spans of earlier sections.
     Commit its output as docs/pass-29-known-terms.json. Both passes read
     this file.
   - Extend tests/pass28/figs.mjs: selectors for .chapter-hero-visual,
     .cover-exhibit-svg and the icon SVGs; default widths 320, 360, 375, 768,
     1024, 1440; a --motion run without reducedMotion that samples each
     animated figure at 0, 25, 50 and 75 % of its cycle (every animation in
     the book repeats indefinitely, so a figure's cycle is the largest
     begin plus dur among its animate elements); a --fullscreen mode for
     elements that have the figure fullscreen control; a contrast check
     (below).
   - tests/pass30/bare.mjs: a screenshot of the <svg> element alone, for any
     selector (figure, hero, cover, icon), at a given SMIL time, with the
     figure number, <title>, <desc>, caption, the "How it works" strip and
     surrounding prose excluded, and the SVG's own text intact.
   - Extend tests/pass28/clip.mjs (Pass 28's book-wide clipping sweep):
     add 360 px to its widths, a 200 % text-size run (root font-size set
     to 200 %, at 768 px and wider; WCAG 1.4.4) and the WCAG 1.4.12
     text-spacing override on page text.
   - Exceptions file: docs/pass-30-exceptions.json lists, by id, the only
     checks a gate may skip: the 11 px label floor and the caption length
     for the 18 kept-original figures, the caption length of fig 18.6, and any container that
     scrolls on purpose (added only as Gate 1 below allows). The gates read
     this file; nothing else is skipped.

FOR BOTH PASSES

Facts. UNDER.md §4g is law: re-introducing a corrected error fails the pass.
Every fact, date, name, number or quote either pass adds (in prose, a <desc>,
a caption or a label) is checked against a reliable source (primary
documents, standards, papers, reputable histories) by web search or fetch
before it is written, and the URL or citation goes into the ledger beside
it. Nothing is asserted from memory. If it cannot be sourced it is not
added; the gap becomes an owner call.

Owner calls. Each goes into STATE.md under BLOCKED ON TIGER as one line:
the question, the options, the recommended option, and a link. The agent
never decides an owner call itself. If one part produces more than 10 owner
calls, finish that part, stop and report; do not start the next.

Pages for the owner are published as claude.ai artifacts, the way the Pass
28 figure pilot was, with the link added to BLOCKED ON TIGER.

Ledger entries stay short: per part, a table and the findings, no essays.
Commit per part, push, check the live site.

PASS 29: THE BOOK TEACHES

The bar. A reader who holds this book and nothing else can follow
everything it says without stopping to look something up. That reader is a
curious adult with school mathematics and everyday use of a computer and a
phone. They know what a file, a website and an app are; they do not know
what a register, a packet or a hash is until the book tells them.

What the research says, and what it asks of the edit. Each rule is here
because the evidence supports it; none is a licence to add.
- Teach from what the reader already has (Ausubel 1968: "The most important
  single factor influencing learning is what the learner already knows").
  Where a section depends on an earlier idea the reader may not connect, a
  clause names it. Not a paragraph, and not where the link is already plain.
- Make the links explicit for the novice, and stop there (McNamara, Kintsch,
  Songer and Kintsch 1996; Kalyuga, Ayres, Chandler and Sweller 2003).
  Readers new to a subject need the "because" and the step an expert skips;
  the same help can hurt readers who already have the idea. So write the
  missing step once, where it is first needed, and never explain twice what
  the book has already explained.
- Tie the new to the given (Clark and Haviland 1977). What a sentence treats
  as known must point to one thing the reader really has; usually that means
  opening with the known and ending with the new. A paragraph starts where
  the last one left off and hands the reader to the next. Ideas are joined by
  reasoning (because, so, which is why), not stacked as items. Bullets and
  tables stay only where the content really is a set.
- Spare the reader's working memory (cognitive load theory, Sweller 1988;
  Mayer's pre-training principle: a mechanism is learned better when the
  names of its parts are already known). A term is defined before a
  mechanism leans on it; a sentence does not ask the reader to hold a new
  definition, an analogy and a formula at once.
- Cut what does not teach (Mayer's coherence principle; Harp and Mayer 1998:
  interesting but irrelevant details lower recall and transfer). A story
  stays when the history explains why the thing is the way it is (the
  constraint, the failure that forced the fix, the trade-off); stories are
  understood and remembered better than exposition (Willingham 2004), which
  is why a teaching story is protected. Colour that teaches nothing goes.
- Say it once. Where a caption and the prose beside it explain the same
  thing, the prose keeps it and the caption names the picture.
- Show it working only when description fails (Sweller and Cooper 1985;
  Fyfe, McNeil, Son and Goldstone 2014). Where the cold reader cannot follow
  a mechanism from its description, one concrete example with real values
  goes in, concrete first and notation last. Not otherwise.
- An analogy maps relations and is then cashed out (Gentner 1983). Give the
  analogy, then the literal mechanism exactly, then where the analogy stops
  being true. An analogy never cashed out is a search point.
These describe how understanding builds, not a template. A book where every
section opens with a story and ends with a moral reads as machine-made. Keep
each section's entry when it works.

How much may change. This is a repair pass, not a rewrite.
- No part may end more than 5% longer than its section prose at the Pass 27
  close (commit 02f486b), measured by scripts/count-prose.mjs. This budget
  covers Passes 28 and 29 together.
- In a part already at or over its ceiling, every edit is net-zero within
  its section: an addition is paid for by a cut in the same section. A
  search point that cannot be closed that way is an owner call.
- Edits are local: a sentence, a clause, a paragraph. A section where the
  repair would touch more than a quarter of its paragraphs is an owner call,
  not a rewrite.
- Where a section cannot be taught from zero within that budget, make it
  shallower (state the result, drop the detail the baseline reader cannot
  carry) rather than grow it, or record an owner call.
- Every addition closes a search point the cold reader logged. Nothing is
  added unprompted.

Never touch. The thesis set, the authorship line, owner epigraphs and
pull-quotes stay verbatim; agents typeset them, never author them. The §4w
arc devices stay whole (the six-pattern unification, the four disciplines,
the part-identity micro-arcs, the "What you now understand" codas). Each
volume keeps its register, Part IV's Strongroom serif voice included; the
register bar is the Ch7 pickle coda. Fig 18.6's caption is the owner's
closing claim and stays verbatim. Pass 29 changes no SVG. Every figure
mark the prose names keeps its name.

AI style is a defect, as much as padding. No clipped dramatic fragments, no
"Not X. Y." reveals, no reflexive triplets, no aphorism closers, no
rhetorical questions standing in for explanation, no "this is where it gets
interesting", no stacked hedges, no sameness of shape from section to
section. Never an em dash (law 1; npm run check:dashes must pass); the en
dash only for ranges and name pairs.

Anchors. Removed or merged paragraph ids migrate through ANCHOR_ALIASES in
public/book.js, verified at zero pixel delta (tests/pass25/alias.mjs,
Chromium and WebKit, 375 and 1440). New paragraphs get new ids that never
renumber or reuse an existing id, and existing ids never move to different
content. Confirm the id form against public/book.js,
scripts/build-sections.js, scripts/build-glossary.js and the tests/pass25
suites before the first insertion, and record it.

The cold reader is an expert pretending to be a novice, so it is
calibrated before it is trusted.
1. Planted gap: on a copy of Ch1's opening section (ch1-context), remove one
   definition the section relies on. The cold reader must log that gap. If it does not, tighten its
   instructions and repeat; after three failed tries, stop: it is an owner
   call.
2. Run the cold reader on ch1-context and Ch16 §03 (ch16-lockfree) and
   record both counts in STATE.md.
3. Publish a page for the owner with those two sections and no markings,
   and stop. The owner marks every place they had to stop and wonder, then
   writes "go" in STATE.md. Compare. Recall: the cold reader must have found
   at least two thirds of the owner's marks. Precision: a Sonnet 5.5 agent
   judges each cold-reader point the owner did not mark as needed or
   unneeded for the baseline reader; at most a third may be unneeded. If
   either test fails, retune the cold reader and compare again; after two
   retunes, the reader floor is an owner call before Part I. If either
   section logged more than 15 search points, the reader floor is an owner
   call before Part I is touched.

Method, per section, one part per session:
1. Cold reader. It reads the section as the baseline reader who has read
   the book up to here and nothing else. Its known terms are that section's
   entry in docs/pass-29-known-terms.json; a term defined earlier in plain
   prose also counts as known. Anything else it must mark as a term it would
   have to look up, even if it knows it. It logs every search point: a place
   where the argument depends on a term or step the reader could not explain
   back from earlier pages. A term named only in passing, which the argument
   does not rely on, is not one. Kinds: a term relied on before it is
   explained, a skipped step, an analogy never cashed out, a jump in
   reasoning, a list that does not connect, a mechanism that cannot be
   followed from its description, and a step an old caption taught (at
   commit 664e794) that neither the redrawn figure (with its "How it works"
   strip) nor the prose carries now.
2. Teacher. Closes each logged point in the book's voice, by the rules
   above, and cuts what only repeats. Each change names the point it closes;
   each added fact carries its source.
3. Advocate. Argues from the student's side against every cut that loses an
   explanation and against every addition the section did not need.
   Analogies, stories and examples are protected unless another passage
   already does the same job better.
4. Fact and voice gate. Facts, numbers, names, cross-references and figure
   references survive; glossary first-use sites survive or move earlier on
   purpose, recorded. Every addition is sourced. The prose reads as one
   author with none of the AI tells.
5. Cold reader again on the result. The section passes at zero search
   points. At most two repair rounds; anything still open is an owner call.

Per part: apply; aliases verified; npm run build:glossary and npm run
build:sections; npm run check:dashes; the tests/pass25 suites (baseline at
the Pass 28 close: invariants 812/0, traces 229/0, marks 106/0, UI 93/0,
parity 39/40, the one known sub-pixel case ch8-layers-p5; no new
failures);
scripts/count-prose.mjs within the budget. Then the Sonnet 5.5
verification: it compares every section with its text before Pass 27
(commit 664e794) and names any lost explanation, any new AI style, any
unsourced or mis-sourced addition, opening at least one cited source per
section. A removed passage counts as lost explanation only if it was the
sole place a term or step was taught; restatement the cut removed stays
removed. Fix or record every finding. After Part I, publish three
before-and-after samples for the owner (one cut, one addition, one list
turned into argument) and continue; the owner can redirect at any section.

Close of Pass 29: every term the pass newly defines gets an authored
one-sentence entry in scripts/glossary-defs.json (at most 30 words, the Pass
27 rules); regenerate public/glossary.json and docs/pass-29-known-terms.json,
and verify that no term lacks a definition and no first-use site points at
the wrong section. Ledger §4ac.

PASS 30: EVERY PICTURE HOLDS

Scope: all 222 figures (204 redrawn by Pass 28, 18 kept original), the 19
chapter heroes, the cover,
the 17 insight-strip icons (Pass 21) and every interface icon (place bar,
menu, account mark). Pass 28's standard (docs/pass-28-brief.md, "The
standard") is the bar. Pass 28 already measured its figures clean; this
pass re-measures every picture after the prose is final, adds the test
Pass 28 did not run (Gate 2, the picture speaks for itself), and repairs
only what fails. A picture that passes is not touched.

Kept-original figures. The 18 figures on the "Kept original" list are the
owner's decision and are not redrawn or edited. Gate 1 still checks them
for clipping, overlap and text outside the viewBox, and those must be zero;
the 11 px label floor, the caption length and Gate 2 do not apply to them,
and Pass 29 leaves their captions as they are. A finding on one of them is
not repaired: it is reported to the owner with a screenshot and does not
block v1.0. They are recorded by id in UNDER.md §5 and in the owner read map
as "kept original, small on a phone".

Heroes and the cover. Chapter heroes are hidden at 768 px and below, and the
cover SVG below 880 px (where the cover is the .exh-stack, which clip.mjs
covers). Gate 1 measures them only at widths where they render, and Gate 2
captures them at 1440 px. The cover's animation plays once: it is captured
at its end state and needs no pause control.

What may change. SVG, figure <title> labels, <desc>, captions and labels,
and the CSS and public/book.js needed to clear a Gate 1 finding or build the
pause control. No section prose and no other page text. A figure that cannot
pass without a prose change or a new figure is an owner call. A redraw keeps
every mark the prose names, under the same name.

Security figures. The figures Pass 28 drew at the level of concepts (the
"Security figures (concept level)" list in docs/pass-30-figures.md) stay
at that level: their intended message
is the defence or the idea, and no repair moves them toward attack
mechanics.

What the research says about pictures.
- A diagram earns its place by making relations visible at a glance, so the
  reader finds by looking what text would make them search for (Larkin and
  Simon 1987).
- Nothing extraneous (Mayer's coherence principle): every mark means
  something the reader can read. Labels sit next to what they name (spatial
  contiguity), and the eye is led to what matters (signaling).
- Motion only where the mechanism is change over time, slow and clear
  enough to follow (Tversky, Morrison and Bétrancourt 2002: animation helps
  only when it is congruent with the idea and can be apprehended; often a
  good still does as well). Readers learn better when they control the pace
  (Mayer's segmenting principle), so animations can be paused.

Gate 1, measured layout. Zero findings is the bar.
- Every picture, at 320, 360, 375, 768, 1024 and 1440 px, Chromium and
  WebKit, in the page, in the fullscreen view where it has one, in the
  reduced-motion still and at every sampled animation frame: no label below
  11 CSS px from 360 px up (at 320, unclipped and not overlapping, as
  figs.mjs already rules); no text outside its shape or the viewBox; no two
  text boxes overlapping or crowded.
- Every page and every element (labels, tabs, chips, the place bar, the
  menu, tooltips, tables, code blocks, headings), at the same widths and
  engines, plus the 200 % text-size run (768 px and wider) and the
  text-spacing run of tests/pass28/clip.mjs: no horizontal page scroll, no text cut by
  overflow: hidden, nothing clipped.
- Contrast (WCAG 2.2): text at least 4.5:1 (1.4.3); every stroke and fill
  of a mark that a label or the <desc> names at least 3:1 against what
  touches it (1.4.11); other marks are listed, not failed. Icons are
  held to 3:1 too as a house rule, so they read on every volume's
  background.
- Motion: every animation in the five parts repeats indefinitely, so every
  animated figure falls under WCAG 2.2.2. Build one shared pause and play
  control in public/book.js, in the existing figure chrome,
  keyboard-reachable, its state kept for the page, covered by
  tests/pass25/ui.mjs. No per-figure markup. The off-screen pauser stays, but it never unpauses
  a figure the reader paused, in the page or in fullscreen; ui.mjs tests
  that.
  Under prefers-reduced-motion every figure shows a complete, meaningful
  still.
- Every figure keeps role="img", its short <title> label and a <desc> that
  states the mechanism (WCAG 1.1.1), as Pass 28 set them. Decorative icons
  stay aria-hidden.
- Never loosen a threshold, widen a tolerance or add an exemption in the
  test scripts to reach zero. Skips live only in
  docs/pass-30-exceptions.json: the kept-original label floor and caption
  length, fig 18.6's caption length, and a container that scrolls on purpose (a code block, a
  wide table), each also entered in UNDER.md §5 with its measured value and
  reason and reviewed by the Sonnet verifier. A finding believed false is
  an owner call with a screenshot.

Gate 2, the picture speaks for itself. Loosely modelled on ISO 9186-1:2014
(comprehension testing of graphical symbols): show the picture without its
explanatory text to someone who has not seen it, ask what it means, and
compare the answer with what it is meant to mean.
- Intended messages first. For each picture the intended message is its
  <desc>: the specific parts, the mechanism, and its key cause and effect, in
  one or two sentences (for a security figure, the defence or idea). Where a
  <desc> is missing or vague, an agent writes it from the prose around the
  figure. A Sonnet 5.5 verifier checks every intended message against the
  prose. Then all are stored in docs/pass-30-figures.md and committed before
  any describer runs. After that commit, changing an intended message is an
  owner call. The agents that wrote them never score.
- Calibrate the describer. Give one fresh describer a Ch1 figure in which
  one label is swapped for a term the book has not yet taught. It must flag
  that mark as uninterpretable. If it does not, tighten its instructions
  and repeat; after three failed tries, stop: it is an owner call.
- Describe. One fresh vision-capable describer per chapter sees that
  chapter's pictures as a batch, captured with tests/pass30/bare.mjs at 375
  px (an animated figure as three frames in order). It never sees the same
  chapter twice. It is told: you know school mathematics, everyday computer
  use, the terms this book has taught before this point, and the terms the
  picture's own section teaches (supplied next to each screenshot: the
  entry in docs/pass-29-known-terms.json for the section that contains the
  picture, plus the terms that section defines); mark any mark you could
  read only with outside technical knowledge as uninterpretable. For a term
  the picture's own section teaches, judge only whether the picture shows
  the role the section gives it. For each picture it
  writes, in at most three sentences, what it shows and what changes, and
  lists any mark it cannot interpret.
- Score. One scorer per part compares each description with the intended
  message. Pass when the mechanism and its key cause and effect are named
  and no mark is uninterpretable. A fail counts only when a second fresh
  describer also fails it. The first repair is the labels and marks; a
  redraw to the Pass 28 standard happens only if that repair fails. Two
  rounds at most; a picture still failing is an owner call.
- Icons. Insight-strip icons: the describer sees each icon alone and picks
  its meaning from the list of all strip concepts; pass when it picks the
  right one. Interface icons: the describer names the action from the icon
  alone. A fail is redrawn in the Pass 21 grammar (24-unit grid, 1.5
  stroke, currentColor) and re-tested.
- Heroes and the cover are tested the same way against the chapter's or the
  book's promise.

Per part: Gate 1 and Gate 2 for every picture in the part, fixes, re-run
to zero (Gate 1 repairs: two rounds at most; anything still failing is an
owner call with a screenshot), npm run check:dashes, anchors and fig-* ids unchanged, then the
Sonnet 5.5 verification: it reads each repaired picture's before and after
screenshots and its test record, and opens five passing pictures per part to
confirm the pass was honest. Ledger §4ad: per picture, the intended message,
the describer's words, the verdict and what changed.

THE CLOSE

When Pass 29's glossary check and Pass 30's last part are committed and
live, re-run book-wide: tests/pass28/figs.mjs (with --motion and
--fullscreen), tests/pass28/clip.mjs, tests/pass28/smooth.mjs and the
tests/pass25 suites. If anything fails, repair it once; anything still
failing is an owner call. Then:
1. Publish docs/owner-read-map.md: per part, the section-prose count against
   its 02f486b ceiling, the five largest Pass 29 edits before and after with
   the search point each closed, the sections that needed two repair rounds,
   every Gate 2 fail and near-miss with its screenshot, every hero, and
   every open owner call, each with a link. The owner's read starts where
   the book is weakest.
2. Tag v1.0 if no owner call raised by Pass 29 or 30 is open; otherwise tag
   v1.0-rc1. Standing items already in BLOCKED ON TIGER (the owner's read,
   sign-offs, earlier passes) do not decide the tag, and this session never
   removes them. The 18 kept-original figures are settled and do not block
   v1.0.
3. Write at the top of STATE.md either "PROSE AND FIGURES FROZEN 1.0.
   Next: the owner's read." or "PROSE AND FIGURES FROZEN 1.0-rc1. Open: <n>
   owner calls (listed below). Next: the owner's
   decisions, then the owner's read." Then stop.
