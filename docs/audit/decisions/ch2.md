# Chapter 2 · decisions

Round 1: `docs/audit/round1/ch2.json` (54 confirmed) and part-1.json items 12, 13, 16, 17 and 25 (1-based). Numbers below are the 0-based indexes in ch2.json.

## Applied (own wording where the judge's wording did not fit)
- 0 · ch2-gates-p2: NOT is now two transistors taking turns, so it is clear why the output is 0 or 1 and never fought over (the judge's first option; no resistor model).
- 1, 8, 24, 45 · Fig 2.3 strip: the outputs are named in words, as drawn; the symbol key is gone (the truth tables above carry ·, + and ¬).
- 2 · ch2-gates-p10: the NAND-built OR worked through De Morgan's first law in one sentence.
- 3 · ch2-twos-p8: which patterns are negative (top bit 1, half of them), and the 8-bit range.
- 4 · Fig 2.9 strip: widening keeps −1, which is all ones at any width; size_t is 64 bits on a 64-bit machine.
- 5, 26, 49, part-1 12 · Fig 2.10: one place for each idea. The never-stored leading 1 moves into ch2-float-p4, before the figure that draws "1."; the bias stays in ch2-float-p6; the caption names the picture; the strip keeps only new facts (range, digits).
- 6, 21, 23 · code comments: 0.1 is rounded to the nearest double (here up), not cut off; the first comment says the printout is the stored double in decimal.
- 7, 9, 15, 42 · ch2-boole-p1: Latin from a local bookseller, Greek, French and German taught himself, his own school at nineteen, publishing by twenty-five. Checked: MacTutor, Boole ("receive instruction in Latin from a local bookseller"; "teach himself French and German"; "In 1834 he opened his own school in Lincoln although he was only 19"); first paper in the Cambridge Mathematical Journal, 1840 (aged 24).
- 10, 36 · ch2-float-p3: IEEE expanded; "each computer maker had its own format".
- 11, 22 · ch2-float-p1: C dropped from the list (its default printf shows 0.3).
- 12, 18, 29, part-1 13 · ch2-gates-p3 (Fig 2.3 caption): "any circuit can be built from", and the caption names the picture instead of repeating the truth tables.
- 13, 20, 51 · Fig 2.11: the drawn line reads "repeats forever, so a double rounds it"; the desc says the double keeps its leading 1 and the next 52 bits.
- 14, 17, 33, part-1 17 · "De Morgan's laws".
- 16 · Fig 2.2 strip: the circles are Venn's later picture (1880); Boole worked in symbols.
- 19 · ch2-arithmetic-p7 points at Fig 1.8, the one Chapter 1 figure with an ALU.
- 25, 27, 28, 30, 31 · captions of Figs 2.1, 2.6, 2.4, 2.7 and 2.9 name their pictures instead of retelling the paragraph above.
- 32 · ¬ is defined in the NOT table's heading; the sentence tacked onto ch2-gates-p2 is gone.
- 34, 46 · Fig 2.8 readouts: true minus signs, and 0 with no sign.
- 35 · Fig 2.3 strip points at Fig 1.5 (the field-effect transistor).
- 37 (and 36) · glossary homes: "Boolean algebra" → ch2-boole, "IEEE" → ch2-float.
- 38 · ch2-twos-p10: the buffer sentence untangled (buffer was defined in ch1-memory-p11).
- 39 · ch2-float-p11: the Patriot sentence split; the Scud killed the soldiers, not the failure. §4g row kept (timing error, 0.1 chopped in fixed point, radar looked in the wrong place).
- 40 · ch2-binary-p2: the overlapping triplet gone.
- 41 · coda: "actually", "really", "actually" dropped. Three words only; the coda stays whole (§4w).
- 43, part-1 25 · Fig 2.8 strip: the sentence repeating ch2-twos-p8 cut.
- 44 · two's-complement steps: full stops consistent.
- 47 · Chapter 2 hero: the circuit computed A·B + ¬A·B = B. Now XOR, A·¬B + ¬A·B, the recipe of ch2-boole-p10, with a NOT on B in the top row; with A = 1, B = 0 the output is 1.
- 48 · Fig 2.1: "threshold" moved clear of the rising edge.
- 50 · Fig 2.11: the red sum dot appears at the tie instead of sliding in from the left.
- 52 · hero tagline: "two states, the easiest to tell apart" (the chapter says ternary is possible).
- 53 · the hero's title id is its own (svgt-part1-ch2-hero), so Fig 2.1 is announced by its own title. The Ch3 hero and Figs BR.1 and BR.2 clash too; they are fixed with their chapters (Figs 3.9 and 3.10 are kept-original and keep their ids).
- part-1 16 · "Section 02" capitalised.

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch2-newcomer.json`, `ch2-expert.json`

Applied (one revision):
- ch2-float-p4 and Fig 2.10 (newcomer): the word "mantissa" named both 6.5 and the stored digits after the point. The paragraph now says the 52 stored bits are only the digits after the point and that Fig 2.10 writes the whole value as 1.mantissa; the figure's readouts say "1.mantissa = 1.101 (binary)" and "1.mantissa = 1.1 (binary)".
- Fig 2.1 strip (expert): "Engineering, not mathematics, decided it." cut (an aphorism after the point was made).
- Fig 2.1 (expert): the reading cursor was one line from the top box to the bottom row, so it crossed the TERNARY heading and the digit row. It is now two segments, one inside each wire's box, on the same timing.

Gate 1 leftover (pre-existing, also at dc2ebbd): Fig 2.3 in fullscreen, the neutral output wires measured 1.19 to 1.66:1 against the gold lit wire drawn over them. Fixed as in Fig 1.12: each neutral output wire is hidden while its gold one shows (the input wires already worked this way).

## Checks (cloud session, Linux; Playwright 1.61.1, Chromium 149, WebKit 26.5)
- `build:glossary` (no change but the timestamp), `build:sections` (timestamp only, restored), `check:dashes` clean; anchor ids outside SVGs unchanged against dc2ebbd.
- Gate 1 on Figs 2.1, 2.2, 2.3, 2.4, 2.6, 2.7, 2.8, 2.9, 2.10, 2.11: still with fullscreen 0/120 (Chromium) and 0/120 (WebKit); motion with fullscreen 0/480 (Chromium); motion 0/240 (WebKit, cards only); hero-ch2 0/4. Run with Chromium's overlay scrollbars (`--enable-features=OverlayScrollbar`), as on a phone or a Mac: with Linux's classic scrollbar, `scrollbar-gutter: stable` takes 15 px off a 360 px viewport and every 13 px label in the book (Chapter 1's included) reads 10.7 px; that is the test machine, not a reader's phone.
- clip (part-1, both engines, four widths): 0 findings. pass25: invariants 812/0 (after `git fetch --unshallow`, so the d1bbb42 baseline exists), parity 40/0, marks 106/0, ui 120/0, traces 231/2. The two trace failures (a CDP flick classed EXCURSION, long tasks of 50 to 82 ms under 4× CPU throttle) fail identically on dc2ebbd in this container, so they are the container's timing, not this chapter.
