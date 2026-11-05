# Session 2026-11-04 (second round) · lag-free scrolling, figure steps

Branch `smooth-part1`. The agent may not push to `main`; merging it to `main` on GitHub puts it live.

## 1 · Lag (sitewide fix)
**Cause, measured:** the animated figures. Each one that runs repaints on every frame, and that cost lands on scroll. Two more pictures animated without control: the chapter heroes (Parts I, III, IV, V) and the cover ran off screen too, for as long as the page was open.

**Fix:** while the page scrolls, the pictures on screen hold still. They run on from the same moment 160 ms after the scroll stops. Every animated picture (figures, heroes, cover) now runs only while on screen.

**Result** (Part I, wheel scroll top to bottom, share of frames dropped):

| Browser engine | Before | After | Engine floor (no script, no animation) |
|---|---|---|---|
| Chrome, desktop (4x slower CPU) | 3.3 % | 0.5 % | 0.2 % |
| Chrome, phone (4x slower CPU) | 4.4 % | 0.1 to 0.7 % | 0.1 % |
| Safari's engine, desktop | 11.0 % | 4.9 to 5.2 % | 5.6 % |
| Safari's engine, phone | 17.9 % | 6.5 to 7.0 % | 6.5 to 6.9 % |

Both engines are now at their floor: what is left is the engine itself, not the site. A still screen with figures running drops no frames in Chrome. (Safari's engine slows its own frame clock when nothing changes, so its still-screen numbers are not lag.)

## 2 · Pausing (Part I figures)
The figure keeps running when the mouse is on the picture. It stops only when the mouse is on the row of step buttons, and runs on from there when the mouse leaves the row.

## 3 · Smarter buttons (Part I figures)
- The "run" button is gone.
- With a mouse, the buttons are hidden until the pointer is on the figure. Their space stays reserved, so nothing jumps.
- The lit button follows the animation: it shows which step the figure is in now.
- A press glides to that moment by the shortest way round the loop (before, it could rewind through several loops).
- Keyboard: a step in focus holds the figure; leaving the row lets it run on.
- Touch (no hover): the buttons always show. Tap a step to hold it there; tap the lit step again to let it run. A tap on the picture goes to the next step.
- Reduced motion: figures stay still; the steps still work.

## Verified
- A new check of all of the above, in Chrome and Safari's engine: all pass.
- The project's interface tests: 107 of 108 pass. The one failure (the place bar's sync test in Safari's engine) also fails without this change, on this Windows machine.
- `check:dashes` clean.
- Invariant checks: the only failures are the tab-stop count against the old baseline `d1bbb42`. They also fail on Parts II to V, which this change does not touch, because the fullscreen buttons were removed earlier today; that baseline needs refreshing. The Safari-engine half of that run crashed on this machine.
- `?v=` raised to `20261104d` on every page, so browsers fetch the new script and styles.
- Not checked: real iPhone and Mac Safari (only Safari's engine on Windows was available).

## Files
`public/book.js` (first module; the pauser), `public/book.css` (figure steps), `tests/pass25/ui.mjs` (the figure-step test follows the new behaviour), the `?v=` tag on every page.
