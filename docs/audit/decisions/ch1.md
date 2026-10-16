# Chapter 1 · decisions

Round 1 (`docs/audit/round1/ch1.json`, 54 confirmed, plus part-1.json items 3, 4, 8, 15 and 18, counted 1-based): every finding applied in commit 6a5f607 in the author's own wording (each finding's element differs from 46543fb; finding 41 landed in the memory table, not in ch1-memory-p1). Figs 1.3, 1.5, 1.6, 1.7, 1.12, 1.13 and 1.15 redrawn or relabelled.

Gate 1 leftover: fig-1-12 in fullscreen, the neutral outline behind "wrong · ~5%" measured 1.66:1 against the red highlight. Fixed by hiding the neutral rect while the red one shows (same keyTimes, inverse values).

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch1-newcomer.json`, `ch1-expert.json`

Applied (one revision):
- fig-1-5 strip: "Every modern CPU is a stack of these about 3 nanometres wide" was false ("3 nm" is a process name; no feature is 3 nm). Now "A modern CPU holds billions of them, each a few tens of nanometres across" (agrees with ch1-transistor-p16's flu-virus width). ch1-transistor-p16's "3-nanometre process" stays: it names the process.
- ch1-transistor-p6 (Fig 1.4 caption) was three sentences; now two.
- ch1-transistor-p7 split: doping stays in p7, the field-effect transistor and the gate move to a new paragraph ch1-transistor-p18 (next unused number; one anchor added, none removed).
- ch1-transistor-p11: "(every second one is labelled)", since the labels sit two gridlines apart.
- fig-1-7 strip: the red flashes show only while the figure plays; the strip says so.
- fig-1-2: the left column is both key and lamp; its header now says "KEY · LAMP".
- ch1-cpu-p3 (Fig 1.9 caption) says why the counter goes 0, 5, 8 (five-byte and three-byte instructions); the strip's repeat of it trimmed.
- ch1-cpu-p10: Spectre and Meltdown pointed forward to the box that explains them.
- ch1-cpu-p11: the attack told in steps (read the byte, load the location it numbers, time all 256).
- ch1-kernel-p5: "a request to the kernel called a system call" (the term is defined in the next subsection).
- ch1-kernel-p8: process defined plainly; Chapter 5's language named (C).
- ch1-memory-p2: the caches hide the gap to RAM, not the SSD gap (both readers).
- ch1-memory-p7: one clause on what the working set model says.
- ch1-memory-p10: the page-fault sentence moved after the three-item list.
- ch1-memory-p11: DEP named where it is used.

Rejected:
- ch1-transistor-p7 (now p18) sand and oxide (expert, L): true at the book's depth; the classic MOSFET's oxide is silicon dioxide, and today's high-k stacks still sit on a silicon dioxide layer. Adding hafnium would be expert detail (law 4).
- ch1-transistor-p5, p1, p16, fig-1-3, vonneumann-p6, cpu-p5, cpu-p9, fig-1-13, fig-1-14, fig-1-15 (newcomer, L): each is answered within a sentence or two by the text around it, or by the next section; left as is.
