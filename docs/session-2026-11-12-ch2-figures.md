# Chapter 2 figures · 2026-11-12

Owner, after Chapter 1: "move to the next part ... those were pretty good already ... they still can be improved, probably ... don't ruin anything that's already good ... think for yourself."

## How the work was chosen

Every Part I figure was screenshotted at each of its steps (375 and 1440 px) and read blind by a small model; a second, stronger reader then checked every claim against the images and threw out what was not there (about three in four). I looked at each figure myself and changed only where the picture really failed, or where the reader's own hand could be the cause. Verdicts are in the workflow journal; most figures came back "leave as it is" and were left.

## Changed

| Fig | Was | Now |
|---|---|---|
| 2.1 | Two gauges, three thresholds, a noise arrow, two rows of five digits on each side, two steps ("way too complex"). A first redraw as two boxes with dots and readings was still wrong ("way too much text and isn't visible what it even represents"). | Five lamps, the lamp of Figs 1.3 to 1.5: two (dark, bright) and three (dark, half, bright), all flickering by the same amount. Off and on stay plain; the half-lit lamp keeps looking like its neighbours. The only text is the digit under each lamp. |
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

## 2026-11-13 · simplify

Owner on the lamps: "Looks really good, now just simplify most of them. You don't need to repeat in text what the figure is already saying."

| Fig | Now |
|---|---|
| 2.2 | The four-case strip and the two gold lines of words are gone: the reader's two presses are the cases. Circles, circuit, the two names. |
| 2.3, 2.4 | The row of cases drawn under the picture repeated the step buttons: gone. So are "A and B", "A or B", "not A" beside gates already named. |
| 2.6 | The row of cases is gone. Still the densest figure of the chapter (five gate symbols). |
| 2.9 | Redrawn. Eight ones; the check reads −1, the copy reads 255; a red line runs out of the buffer. Was a column of text in three numbered steps. |
| 2.10 | Redrawn. Sign, exponent and mantissa as three plain values; the point slides two places through 1 1 0 1; the place values appear; +6.5. One example, no steps. |
| 2.11 | Redrawn as a ruler whose ticks are the only numbers a double can hold near 0.3. "0.3" sits on a tick; "0.1 + 0.2" lands between two and is moved up to the next, 0.30000000000000004. |
| 2.12 | Redrawn as one scene: the Scud, the box where the radar looks, an hour counter. The box slides away as the hours run to 100; a bracket reads 570 m. |
| titles | The third clause, which restated the picture, is cut from every title in the chapter. |
| captions | Each now says what the picture cannot (2.1: "Each lamp is a voltage level; the flicker is noise.") or a few words. |

"How it works" keeps the audited facts; only words that named removed parts were changed. Gate 1 still and motion with fullscreen (Chromium): 0 fails on all twelve; clip 0.
