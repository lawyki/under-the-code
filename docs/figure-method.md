# Figure method (Part I first; owner, 2026-11-04)

The owner's law: the card already has its "How it works" strip, so the picture and the caption must not carry text as well. "It is really easy for an AI to write text and almost, seemingly, impossible to use visual figures. Even the figures are mostly text after probably 7 passes on them." Part I is made right first; the method below then goes to Parts II to V.

## The rules

1. **The picture carries the mechanism.** If a label explains, the drawing has failed: draw the thing instead (an arrow, a colour, a position, a size, a motion, an icon).
2. **Labels are names, never sentences.** No verbs and no result lines in the SVG. A label names a thing the reader cannot recognise from its shape (a register's name, a year, a value). Aim at six labels or fewer.
3. **The caption is one sentence** of 16 words or fewer, telling the eye where to look. It never explains how; that is the strip's job.
4. **The strip holds the detail:** the steps, the numbers, the history, the caveats. At most 150 words.
5. **Colour is a word.** One colour per role, the same in every figure of the part (Part I: gold is what acts or is on, blue is data or charge, red is what blocks or fails, green is what holds or passes), so it never needs a legend.
6. **Motion is the explanation.** What changes moves; the steps under the figure let the reader stop on each moment, so no text has to narrate the sequence.
7. **Nothing is said twice.** Not by the picture and the caption, not by the caption and the strip, not by the figure and the prose beside it.

## What works (record as it is learned)

- *Steps instead of narration (2026-11-04).* Named step buttons ("0 V | 0.7 V", "press 1 | 2 | 3") replace the "first this, then that" sentences: the reader holds each moment.
- *A thick loop and a thin wire (Fig 1.3).* Line weight says "large current" and "small signal" without the words.
- *Current moving the way the symbol's arrow points (Fig 1.4).* A picture that contradicts its own symbol reads as wrong, however good the caption.
- *Counts on the axis, not on the plot (Fig 1.6).* Labels on lines and dots read as clipping.
- *Owner-praised figures (1.1, 1.2, 1.7)* are scenes: a real object or one calm mechanism, very few words.

- *Start from what the reader already knows (2026-11-12).* A vacuum tube means nothing to a newcomer; a light bulb beside it says hot, fragile and short-lived without a word (Fig 1.3). A finger on a switch is the transistor's whole idea (Fig 1.4).
- *The same picture, one thing changed, one after the other (Fig 1.4).* One lamp loop: first a finger closes the gap, then a transistor sits in the same gap and a signal does the finger's job. In time, not side by side (see What fails).
- *Follow one real thing through (Fig 1.9).* One instruction's actual bytes moving through the machine teach the four steps; four step names on a wheel do not.
- *Zoom for big numbers (Fig 1.6).* Each step shrinks the whole previous picture into one tile, with a magnifier callout saying so.
- *Cause, then effect, as separate steps (Fig 1.5).* Charge appears on the gate; electrons gather; only then does current run.

- *Let the reader's hand be the cause (2026-11-12).* Where one quantity controls the picture (a gate voltage), give it a slider and let the picture answer; a threshold found by one's own hand is remembered (Fig 1.5, `live-figures.js`). One control, the value shown in the picture where the eye is, one sweep by itself so the reader sees what the control does.
- *A loop can live in the text.* A small always-running picture on the paper, with no card or controls, carries "this repeats" better than a full figure (section 04 of Chapter 1).

## What fails

- Result lines inside the figure ("code and data: one memory, one bus"): the caption, or the picture itself, already says it.
- Legends, when one colour rule would do.
- Explanatory sub-labels under names ("off limits to the program", "page → physical").
- Labels placed on gridlines, wires or dots.
- Symbols a newcomer has not been taught, used as the picture itself (a circuit schematic, plus and minus signs with no name).
- Step names arranged in a shape (a wheel of four words): a list in disguise.
- A dark fill behind a named shape: Gate 1 judges every fill, so shapes are outlines and moving tokens are solid colour.
- Two small pictures side by side. Halving a circuit to show it twice makes every part too small to read on a phone and the stand-in marks (a stub for a finger) stop being recognisable. One picture, full size, changed in time (Fig 1.4, round four to five).
