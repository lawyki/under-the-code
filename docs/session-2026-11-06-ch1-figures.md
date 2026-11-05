# Session 2026-11-06 · Chapter 1 figures, round two

Owner on the 2026-11-05 redraw: "better but not yet there"; 1.3 still makes no sense, 1.4 got worse, 1.5 very bad. Fix every earlier ask at once, check your own screenshots for layout and sense, Chapter 1 only.

| Fig | Now |
|---|---|
| 1.3 | Two lamp loops on one signal: a big glass tube with its heater always glowing and heat rising, beside a small transistor symbol. At signal 1 both loops carry current; electrons cross inside the tube. Signal button moved below the labels. |
| 1.4 | Back to the layout the owner liked before 2026-11-05 (input pill on the base, no extra battery or switch), with a thick loop that turns gold and carries moving current at 0.7 V. |
| 1.5 | One clean cross-section: wells with electrons, holes in the body, oxide and gate. At 1 V the gate turns gold, holes under it are pushed down, a row of electrons bridges the wells, the lamp lights. Legend removed. |
| 1.8 | Moving instruction tokens widened so "store C" no longer clips. |
| 1.12 | Three steps (guess, check, trace): the guessed road runs and loads a cache cell; then a red cross and green tick show the verdict and the wrong road is struck out; the filled cache cell stays, ringed red. Caption cut to one sentence. |
| 1.13 | A one-hour timeline in two rows: you (cards at 9:00, a long wait, printout at 10:00) over the machine (four stacks, idle gaps hatched), your ten minutes joined across both rows. |
| 1.14 | Rings with a wide door at the top. Direct: the program heads for the hardware and is stopped at the kernel ring. System call: it goes to the door, the kernel carries the request in, the hardware lights. Caption shortened. |

Unchanged: 1.1, 1.2, 1.6, 1.7, 1.9, 1.10, 1.11, 1.15.

## Checked
- Every changed figure screenshotted at 1440 and 375 px at each step and looked at; clipped label in 1.13 and the cramped signal pill in 1.3 fixed.
- Blind reader (Sonnet 5.5, screenshots only): all six redrawn figures "mostly clear" (the previous round's reader found 9 of 14 unclear); its door and intent points on 1.14 fixed.
- Anchor ids unchanged (one pattern id added inside 1.13). No em dashes added. Glossary unchanged.
- Web search was blocked in this session; the forms are the standard textbook ones (NPN switch with lamp in the collector loop, n-channel MOSFET cross-section with inversion channel, Gantt timeline, protection rings with a gate).
- `npm run check:dashes` fails to start on Windows (path bug in the script); checked by grep instead.
