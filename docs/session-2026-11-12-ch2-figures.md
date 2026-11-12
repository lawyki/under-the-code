# Chapter 2 figures · 2026-11-12

Owner, after Chapter 1: "move to the next part ... those were pretty good already ... they still can be improved, probably ... don't ruin anything that's already good ... think for yourself."

## How the work was chosen

Every Part I figure was screenshotted at each of its steps (375 and 1440 px) and read blind by a small model; a second, stronger reader then checked every claim against the images and threw out what was not there (about three in four). I looked at each figure myself and changed only where the picture really failed, or where the reader's own hand could be the cause. Verdicts are in the workflow journal; most figures came back "leave as it is" and were left.

## Changed

| Fig | Was | Now |
|---|---|---|
| 2.1 | Two gauges, three thresholds, a noise arrow, two rows of five digits on each side, two steps. The owner, seeing it for the first time: "way too complex". | Redrawn to one look: two boxes (two levels, three levels), a dot in each shaken by the same noise, and one reading under each. The left stays "read as 0"; the right turns red, "read as 2", while its dot is over the line. No steps, no digit rows. |
| 2.2 | A loop through the four cases. | The reader works Shannon's two switches. Each press opens or closes one; the lamp lights only with both closed, and Boole's circles light with them. The press-here mark sits on the first switch not yet tried. |
| 2.5 | A loop. | Waits unsolved with the mark on the first adder; one press lets the carry ripple once and the answer stays. The line "carries ripple right to left" went: the caption says it. |
| 2.7 | "ninth bit" stood under nothing in the first two steps. | The label appears with the bit. |
| 2.9 | A nine-second loop with no way to hold a moment. | Three step buttons: the check, read as unsigned, the copy. "no, so on" is "no: it passes". |
| 2.10 | Nothing tied the stored mantissa to the digits in the boxes. | The mantissa's digits are gold like their field, the hidden leading 1 sits in a dashed box, the exponent line gives its result (= 2, = −1). |
| 2.11 | The rule over 5.6 × 10⁻¹⁷ touched nothing; its exponent rendered at about 7 px. | A bracket from the stored 0.3 to the rounded sum; the exponent at label size. |
| 2.12 | "0.34 s" stood while the error was still 0; "window" stayed put while its box moved. | The readout shows when the error gets there; the label moves with the box. |

Left as they are: 2.3, 2.4, 2.6, 2.8 (each shows its mechanism and has its steps).

## New in `public/live-figures.js`

`data-live="switches"` (parts with `data-when="A&B"`, levers with `data-turn`, press areas with `data-sw`), and for press figures `data-rest` (the waiting moment) and `data-hold="end"` (stay on the result). One `slider()` makes every slider row. WebKit forgets a moment set before the page's load event, so a press figure sets its waiting moment again after load.

## Checked

Gate 1 still and motion with fullscreen (Chromium): 0 fails on 2.1, 2.2, 2.5, 2.7, 2.9, 2.10, 2.11, 2.12. `clip` part-1 (Chromium and WebKit): 0. The reader-driven figures (2.2, 2.5) driven by touch in Chromium and WebKit, with and without reduced motion. Dashes clean, anchors unchanged.

## After the owner saw the set

"Almost all of them are much too complex. They should be figures, not entire games. They should be places to learn, not things TO learn." The scan's bar ("does it show its mechanism?") was the wrong one: most Pass 28 figures pass it and still take work to read. The bar from here is in `docs/figure-method.md` (one look, one idea). Fig 2.1 is the first redrawn to it; the rest of Part I is to be judged again on that test, figure by figure, with the owner seeing each.
