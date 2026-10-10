# PASS 28 BRIEF: figures (law 3: the picture carries it)

Authored by the bridge, 2026-10-10, from the owner's instruction: "almost
every single icon is somehow clipping… too much text and too little imagery.
The point of icons is not more text columns, but vision… visual animated
icons." ("Icons" here means the book's figures.) Runs after Pass 27. **Starts
with a three-figure pilot, published for the owner; the work then continues
figure by figure without waiting (owner, 2026-10-10: "instantly continue…
set up a loop"), and the owner can stop or redirect it at any figure.** Each
part gets a Sonnet 5.5 verification when its figures are done.

## The owner's example (2026-10-10, fig 1.2 Enigma)

"Literally so much potential to be so perfect: it could visualize it in an
extremely good way, but the huge amount of text and the ambiguity of the
details makes it really hard to see what is going on… You can always put
(compacted and meaningful) text into drop columns or hover-over explainers,
but the image should be good enough to talk as such, not needing a huge
paragraph of text with it. It's a pattern on almost all of the icons."

So, for every figure:
- **The image explains itself.** A reader who reads no words sees the
  mechanism (for Enigma: one key, the current's path through three stepping
  rotors and back via the reflector, a different lamp each press).
- **No ambiguous detail.** Every mark drawn means something the reader can
  read; decorative lines that look like data go.
- **Text is layered, not stacked.** At most a short title and the labels that
  name things. Anything more becomes a compact explainer the reader opens: a
  hover/focus explainer on a part of the drawing, or a drop-down "how it
  works" strip, keyboard- and touch-accessible, closed by default.
- **The long caption paragraph goes.** What it taught moves into the
  drawing, the explainer, or the prose (law 2 decides which).
- **Handcrafted one by one and tested** at 320 / 375 / 1440 in Chromium and
  WebKit before the next figure starts. A loop keeps the work going across
  sessions until all 222 are done.

## What was measured (2026-10-10)

- 222 figures hold ~21,200 words of text (~95 per figure; 5,100 `<text>`
  elements), close to a quarter of the book's prose.
- At 375 px a figure renders as a thin band with 4–5 px labels; some labels
  collide (fig 1.10: "what the CPU sees" over "immediate value"). The old
  sweeps only tested text escaping the frame, so they passed.
- Captions run to 100+ words in a mono column and carry the explanation the
  drawing should.

## The standard (every figure)

1. **Legible at 375 px**: no label renders below 11 CSS px; the figure is
   designed for the phone first (a tall layout where needed), not a desktop
   drawing scaled down.
2. **Nothing clipped or overlapping**, measured: every text box inside its
   shape and the viewBox, no two text boxes intersecting, at 320 / 375 / 768 /
   1440, Chromium and WebKit.
3. **Words only where a word is the thing** (a register name, a value, an axis
   unit). Target ≤ 12 labels; sentences never live inside a drawing.
4. **Motion shows the mechanism** (the packet moving, the bit flipping, the
   lock contended), SMIL or CSS, paused off-screen (existing pauser), static
   and complete under reduced motion.
5. **Caption ≤ 2 sentences**; the explanation moves to the prose (or is cut
   under law 2).
6. Each volume's figure grammar stays (Part I gold home grammar, II Greenbar,
   III Chart Room, IV Strongroom, V Quorum), as do figure numbering, `fig-*`
   ids, `role="img"` with a descriptive `<title>`, and the fullscreen view.

## Pilot (first session)

Three figures in three different idioms, chosen for how badly they fail
today: one dense text-diagram (fig 1.10, assembly to binary), one process
over time (a protocol or scheduler figure), one structure (a memory or
network map). For each: the redesign, before/after screenshots at 375 and
1440, the reduced-motion still, and a short note on what moved into the
prose. Published as a page for the owner. The owner's verdict sets the
pattern for the other 219.

## Verification per part

Automated overlap/size sweep at four widths in two engines (must be zero),
figure-by-figure screenshots read by a verifier, reduced motion, print,
fullscreen, `npm run check:dashes`, anchors unchanged (`fig-*` ids stay).

## Priority and the final gate (owner, 2026-10-10)

"It can take eternity, no restrictions on this: it's the most important aspect
of the book. The text needs to be great, but the icons are the thing that
finalize it." No time box, no batching: one figure at a time, each finished
and tested before the next.

**Last, after every figure is done: the no-clipping verification and the
smoothness check, book-wide.**
- No clipping anywhere: every page, every element (figures, labels, tabs,
  chips, the place bar, the menu, tooltips, tables, code blocks, headings),
  at 320 / 375 / 768 / 1024 / 1440, Chromium and WebKit, and in the
  fullscreen figure view. Measured, not eyeballed: text boxes inside their
  containers, no overlaps, no horizontal overflow, nothing cut by
  `overflow: hidden`. Zero findings is the bar.
- The UI is smooth: scrolling and figure animations hold 60 fps under a 4×
  CPU throttle with no long tasks, no layout shift, transitions on
  transform/opacity only, reduced motion respected.
