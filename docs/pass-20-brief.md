# PASS 20 BRIEF — figure-truth pass, Part II (ledger §4t)

Authored by the bridge, 2026-08-17. Owner-ratified: the four geometry
defects flagged by the Pass-15 verification (§4o, flag item 4). Sanctioned
geometry — the 16.8/CAP/15.2 licence class and discipline. **Model: Fable.**
Scope: `public/part-2.html`, these four figures, nothing else. The owner is
reading the book; anchors are sacred and no prose changes.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu); approved editorial plan. Read first: `CLAUDE.md`,
`BRIDGE.md`, `UNDER.md` §4o's Pass-15 verification sub-entry (your flag
source), §4g, §5, `STATE.md`.

## The four fixes

1. **fig 6.1 — the "C++ released" marker sits on the 1995 tick** (x=540;
   1985 ≈ x=312 per the flag). This is a fact error drawn spatially.
   Recompute the correct x from the timeline's own tick mapping — do not
   trust the flag's estimate blindly (verify before fix) — and move the
   marker group intact. Check no neighbour label collides at the new
   position.
2. **fig 4.5 — the MLFQ lane is not a legal trace as drawn**: C arrives at
   t=2 and is undrawn until t=17. Redraw the lane as a legal MLFQ schedule
   of the figure's own workload. **Criticial coupling:** the Pass-15
   verification just corrected this figure's average-wait labels to
   8.75/7.75 *from the drawn workload* — if the legal trace changes any
   completion time, recompute the averages and update the labels so the
   figure stays self-consistent. Show the arithmetic in the ledger.
3. **fig 4.5 — the RR lane draws 14 uniform slices = 28 units against 26
   units of work.** Redraw to exactly the workload (13 slices, or a final
   short slice — whichever the figure's grammar supports). Same
   recompute-the-averages coupling as item 2; the two lane fixes land
   together as one self-consistent figure.
4. **fig 7.6 — the BINARY_MULTIPLY line overhangs its rect ~8 px/side**
   (font already reduced to 7 by the micro-pass class). Contain it: widen
   the rect if the layout allows, or re-anchor; keep the §5(d) code
   register spelling.

## Discipline

Pass-2 lesson on every touched figure: bbox-vs-viewBox + text-vs-rect +
screenshots in Chromium **and** WebKit, dark + light, SMIL sampled if
animated. Captions and a11y `<title>`s re-read against the redrawn
figures — a caption describing the old illegal trace is a defect too.
Anchors byte-identical (346). Glossary regenerated, expect 519 ±0 (figure
text can feed the extractor — diff it). §7 spot-check part-2 both engines
at 1440 + 375. Push, confirm, live parity on all four figures.

Ledger: **`UNDER.md` §4t**, house shape, arithmetic shown. Update
`STATE.md`. Flag anything new to the punch list; fix nothing beyond the
four items.
