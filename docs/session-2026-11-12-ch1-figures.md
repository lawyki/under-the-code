# Session 2026-11-12 · Chapter 1 figures, round four

Owner: "perfect Part I (or the chapter) ... then you hopefully understand what went wrong and what is the level of human intuition that worked." No per-figure notes this time; the author looked at every Chapter 1 figure at every step and judged them as a learner.

## What was wrong, in one line each

The praised figures (1.1, 1.2, 1.7) show a thing the reader recognises, in which one cause visibly produces one effect. The ones that kept coming back did neither:

| Fig | Was | Why it failed |
|---|---|---|
| 1.3 | tube and transistor, each with a lamp on a pole | nothing tied the unfamiliar tube to anything known; the lamps read as street lights |
| 1.4 | a schematic | notation only an engineer reads; the sentence it illustrates ("flipped by electricity instead of a finger") was not in the picture |
| 1.5 | static cross-section, plus and minus signs | nothing caused anything: no pull, no flow |
| 1.6 | two numbers and an arrow | text, not a picture |
| 1.9 | four words on a wheel | named the steps without showing what any of them does |

## Now

| Fig | Now |
|---|---|
| 1.3 | A light bulb, a vacuum tube and a transistor to scale on a centimetre rule. Bulb and tube glow and give off heat; then both are dark with broken filaments; the transistor does not change. The reader's own knowledge of bulbs does the teaching. |
| 1.4 | The same lamp loop twice. Left: a finger pushes a lever shut. Right: the lever is a transistor and the finger is a small signal into its base. Both lamps light together; current runs as moving dashes. |
| 1.5 | Electrons are blue dots, holes red pluses. Gate on: gold plus charges fill the gate, the holes sink, electrons line up under it. Then electrons stream down the source lead, across the bridge and up the drain. |
| 1.6 | A zoom. 2,300 dots fill the square (1971). Every twenty years the whole picture shrinks into one gold tile of a 32 × 32 grid, with a magnifier callout showing the picture it holds: 1991, 2011. 2024 is twelve of the 2011 squares. |
| 1.9 | One real instruction, the bytes 01 D8 at address 0x0A, followed through the machine: copied from memory into the CPU, read as add eax, ebx, 5 and 3 into the ALU, 8 back into eax, program counter on to 0x0C. The hexadecimal addresses the prose promises are in the figure again. |

Unchanged: 1.1, 1.2, 1.7, 1.8, 1.10 to 1.15 (looked at; each shows a mechanism). 1.15 is the weakest left: a labelled list with bars.

## Checked
- Every changed figure looked at, at every step, at 1440 and 375 px.
- Gate 1 (`tests/pass28/figs.local.mjs`, still and motion, with fullscreen, Chromium): 0 fails on the five. `clip` on part-1: 0. `check:dashes` clean. Anchor ids unchanged. Glossary unchanged.
- Blind reader (Haiku, phone screenshots only, no prose): 1.3, 1.4 and 1.9 mostly clear; 1.5 and 1.6 unclear on the first try. Fixed from its points: 1.5 names its two charges and shows the flow with one arrow; 1.6 gained the magnifier callout and the ×1,024 and ×12 tags; 1.4's finger redrawn.
- The generators are in `scripts/figs/ch1/` (`plate.py` holds the helpers; `fig_1_N.py` rewrites its card in `public/part-1.html`).

## Round five (same day, after the owner looked at round four)

Owner: 1.3 "really good work"; 1.4 "really bad ... clipping issues ... not understandable ... way worse"; the rest "pretty good"; 1.5 "should be interactable, this sort of game of a transistor"; the four-step loop should run somewhere "embedded to the paper", not as a figure; then make 1.9 more understandable.

| What | Now |
|---|---|
| 1.4 | One lamp loop, not two. A whole hand (finger, fist, closed cuff) pushes a lever across the gap and the lamp lights. Then the transistor can of Fig 1.3 sits in the same gap, dark; a small signal arrives on its base and the lamp lights again. Three steps: off, finger, signal. |
| 1.5 | The reader drives it. A slider under the picture sets the gate voltage, 0 to 1.5 V. Charge gathers on the gate, the holes under it sink, electrons come in from both wells; at 0.7 V the two rows meet, electrons stream round a loop with a battery and a lamp, and the lamp brightens with the voltage. It sweeps once by itself when first seen, then waits. `public/live-figures.js` (an `<svg data-live="mosfet">`), `.fig-live` in `book.css`. |
| the loop | A small running picture in the text of section 04, after the intro line: four stations on a track, a dot going round, the nearest word lit. No card, caption or controls (`scripts/figs/ch1/loop_inline.py`, `.text-loop`). |
| 1.9 | The program counter is a named box in the CPU holding the address, with a pointer up to that address in memory; it changes to 0x0C at writeback. The two earlier instructions say what they did ("put 5 in eax", "put 3 in ebx"), which is why the registers hold 5 and 3. "registers" and "ALU" are named. |

Why round four's 1.4 failed: two half-size circuits side by side made every part small, and the "finger" was a stub nobody could read as a hand. One circuit at full size, one thing changing at a time, reads.

Checked: every state at 1440 and 375 px; Gate 1 still and motion with fullscreen, Chromium: 0 fails on 1.3, 1.4, 1.5, 1.6, 1.9; `clip` part-1 (Chromium and WebKit): 0; dashes clean; anchors and glossary unchanged. Fig 1.5 driven in Chromium and WebKit: the sweep runs once, keys and drag work, under reduced motion it answers the slider in still states with no sweep. pass25 `invariants` on part-1: only the known tab-stop count (its baseline predates the figure controls; the slider adds one stop). Blind reader (Haiku): all four "mostly clear"; from its points the hand's cuff was closed (two loose lines read as cut off) and the loop's lit word now follows the dot.

`book.css` is now `?v=20261112a` on every page.
