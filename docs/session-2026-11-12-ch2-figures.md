# Chapter 2 figures · 2026-11-12

Owner, after Chapter 1: "move to the next part ... those were pretty good already ... they still can be improved, probably ... don't ruin anything that's already good ... think for yourself."

## How the work was chosen

Every Part I figure was screenshotted at each of its steps (375 and 1440 px) and read blind by a small model; a second, stronger reader then checked every claim against the images and threw out what was not there (about three in four). I looked at each figure myself and changed only where the picture really failed, or where the reader's own hand could be the cause. Verdicts are in the workflow journal; most figures came back "leave as it is" and were left.

## Changed

| Fig | Was | Now |
|---|---|---|
| 2.1 | Two steps; the read row showed ternary's wrong +1 even while the level was nowhere near a threshold. | A noise slider. Both levels shake by the same amount; ternary's 0 is read as +1 (red) only while its level is over the threshold; binary's never is. The arrow is as long as the noise. |
| 2.2 | A loop through the four cases. | The reader works Shannon's two switches. Each press opens or closes one; the lamp lights only with both closed, and Boole's circles light with them. The press-here mark sits on the first switch not yet tried. |
| 2.5 | A loop. | Waits unsolved with the mark on the first adder; one press lets the carry ripple once and the answer stays. The line "carries ripple right to left" went: the caption says it. |
| 2.7 | "ninth bit" stood under nothing in the first two steps. | The label appears with the bit. |
| 2.9 | A nine-second loop with no way to hold a moment. | Three step buttons: the check, read as unsigned, the copy. "no, so on" is "no: it passes". |
| 2.10 | Nothing tied the stored mantissa to the digits in the boxes. | The mantissa's digits are gold like their field, the hidden leading 1 sits in a dashed box, the exponent line gives its result (= 2, = −1). |
| 2.11 | The rule over 5.6 × 10⁻¹⁷ touched nothing; its exponent rendered at about 7 px. | A bracket from the stored 0.3 to the rounded sum; the exponent at label size. |
| 2.12 | "0.34 s" stood while the error was still 0; "window" stayed put while its box moved. | The readout shows when the error gets there; the label moves with the box. |

Left as they are: 2.3, 2.4, 2.6, 2.8 (each shows its mechanism and has its steps).

## New in `public/live-figures.js`

`data-live="switches"` (parts with `data-when="A&B"`, levers with `data-turn`, press areas with `data-sw`), `data-live="noise"`, and for press figures `data-rest` (the waiting moment) and `data-hold="end"` (stay on the result). One `slider()` makes every slider row. WebKit forgets a moment set before the page's load event, so a press figure sets its waiting moment again after load.

## Checked

Gate 1 still and motion with fullscreen (Chromium): 0 fails on 2.1, 2.2, 2.5, 2.7, 2.9, 2.10, 2.11, 2.12. `clip` part-1 (Chromium and WebKit): 0. The three reader-driven figures driven by touch in Chromium and WebKit, with and without reduced motion. Dashes clean, anchors unchanged.
