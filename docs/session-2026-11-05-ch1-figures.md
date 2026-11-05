# Session 2026-11-05 · Chapter 1 figures, redrawn as learning figures

Owner's verdict on the first redraw: too much text, most figures not understandable; Chapter 2's gates (Fig 2.3) are the bar. Chapter 1 only.

## What changed
Each figure now shows one idea in the standard teaching form for its topic, with words only where a picture cannot carry them.

| Fig | Before (owner) | Now |
|---|---|---|
| 1.1 | sized badly | drawn larger; rule cards no longer clip |
| 1.2 | pretty good | four labels cut; result row moved up |
| 1.3 | no one could understand it | two identical lamp circuits on one signal: a big glowing tube, a tiny transistor |
| 1.4 | good, could be better | a real switch drives the base: thin loop for the small current, thick loop for the large one |
| 1.5 | too much, too much text | one cross-section: electrons gather under the gate, current flows, the lamp lights |
| 1.6 | a stat is enough | a stat: 2,300 (1971) to 28,000,000,000 (2024); no animation |
| 1.7 | closest to good | unchanged |
| 1.8 | too much going on | memory, one bus, the CPU; instructions and numbers travel the bus as tokens |
| 1.9 | bad | the fetch, decode, execute, writeback wheel, with the program counter stepping through memory |
| 1.10 | bad | one instruction; each word joined to its own bits by colour |
| 1.11 | bad | the pipeline staircase (cycles across, instructions down), 9 cycles against 25 |
| 1.12 | bad | a fork: the guessed road runs, is undone, one cache cell stays lit |
| 1.13 | mid | the "idle" label cut |
| 1.14 | not reviewed | concentric protection rings with one door in the kernel ring |
| 1.15 | not reviewed | the "bigger" label cut |

Captions are one short sentence. "How it works" strips were changed only where they described something no longer drawn.

## Checked
- Every figure looked at frame by frame at 1440 and 375 px.
- A cold reader (an agent that had not read the book) saw only the screenshots: 5 clear, 9 unclear. Its concrete points were fixed (labels for the signal, the electrons and holes, the door; the zero bytes cut from 1.10; "your cards" restored in 1.13).
- Step buttons: the behaviour test and the project's figure-step tests pass. `check:dashes` clean. Glossary rebuilt. Anchors unchanged (one internal clip-path id inside the old 1.12 is gone).
- Web search and page fetching were blocked in this session; the forms used are the standard textbook ones.
