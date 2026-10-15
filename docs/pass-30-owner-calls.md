# Pass 30 · owner calls

Raised 2026-10-15 by Pass 30 (`docs/pass-29-30-brief.md`); ledger `UNDER.md` §4ad. Each entry: what is still open, the options, the recommended option, and a screenshot of the figure as it stands (375 px, the still a reader with reduced motion sees; heroes and the cover at 1440 px). None of these blocks the work; open calls decide the tag (v1.0-rc1 while any is open).

## A. Gate 2: pictures still failing after two repair rounds

Method: a fresh blind reader (Sonnet 5.5) described each figure from bare captures at 375 px, three frames for an animation, knowing only the book's terms up to that figure; a scorer compared the description with the intended message committed before any reader ran; a fail counted only when a second fresh reader also failed it. 110 figures failed round 1; repair round 1 (labels and marks) brought 82 through; repair round 2 (keys, plain notes, retimed animations) brought 23 of the remaining 28 through. Five are left. In all five the reader got the mechanism; what fails is notation the figure shows and the book never teaches.

- **Fig BR.7, the physical address map** (`docs/pass-30-shots/fig-br-7.png`). Readers cannot read the addresses (0xFEE0_0380: hexadecimal, which no section teaches), and still flag "firmware", "interrupt router" and "frame buffer". This is the same gap as the Pass 29 call on hex in ch1-cpu. Options: (a) teach hex once, in ch1-cpu, as that call proposes (four bits per digit, 0 to 9 then A to F, 0x marks such a number), which closes this figure and the book's other hex; (b) write the addresses in decimal or as "about 4 GiB" landmarks; (c) leave as is. Recommended: (a).
- **Fig 6.6, qsort against std::sort** (`docs/pass-30-shots/fig-6-6.png`). Readers follow the race (five steps against two, the count runs 2 against 5) but flag C++ notation: `v.begin()`, `v.end()`, the dot and the empty brackets. Options: (a) accept: the figure shows the two calls exactly as written, and the section teaches what they do; (b) replace the code lines with plain words ("sort v with qsort", "sort v with std::sort"). Recommended: (a).
- **Fig 6.9, three eras of C++** (`docs/pass-30-shots/fig-6-9.png`). Readers get the message (the same task, shorter each era) but flag `begin`, `fold_left`, the colon in `int x : v` and the braces in `plus{}`, even with a plain gloss under each snippet. Options: (a) accept: the point is what real code looked like in each era; (b) cut the snippets to their first line and let the glosses carry the rest. Recommended: (a).
- **Fig 10.3, TCP's states** (`docs/pass-30-shots/fig-10-3.png`). Readers follow the walk but flag the state names the section prose never introduces (FIN, CLOSE_WAIT, LAST_ACK, CLOSING, SYN_RCVD) and "max segment lifetime"; a key under the figure glosses three of them. Options: (a) add two sentences to ch10-handshake on how a connection closes (each side sends FIN, the other acknowledges; the side that closes second passes through CLOSE_WAIT and LAST_ACK), so the names are met before the figure; (b) accept with the key. Recommended: (a).
- **Fig 12.3, the event loop** (`docs/pass-30-shots/fig-12-3.png`). Readers get the whole mechanism (1 2 printed, the promise callback before the timer, output 1 2 3 4) but flag `console.log`, `setTimeout` and the call notation, even with a comment on each line. Options: (a) accept: the section teaches the event loop on exactly this code; (b) name setTimeout and console.log once in the section prose. Recommended: (b), one clause.

### Chapter heroes still failing after two repair rounds

Same method, at 1440 px (heroes render only on wide screens), against the intended messages in `docs/pass-30-figures.md`. Round 1 of the readers: 2 of 20 passed (Ch9, Ch16). Repair round 1 (labels and marks: abbreviations spelled out, hex and mnemonics replaced by plain words, keys added, the Ch10 handshake retimed so the three messages run in turn instead of all at once, the Ch14 curve redrawn true to y² = x³ + 7 with the third meeting point and the reflection labelled, the Ch15 attacks each stopped at a named ring): 10 more passed. Repair round 2 (Ch2 redrawn as the formula's own circuit, the Bridge's five pieces each given their job, Ch10's numbers tied to resending lost packets, the cover's motifs labelled): 5 more passed. Three are left; in each the reader got the promise and flagged one mark.

- **Hero Ch1, the machine** (`docs/pass-30-shots/heroes/hero-ch1.png`). The dashed line from the CPU core to the kernel is read as "attached, but not wired like the others", and readers cannot tell what it stands for. Options: (a) label it ("the software that runs the machine", not a wire); (b) drop the line and set the kernel under the core with its own caption; (c) accept. Recommended: (a).
- **Hero Ch3, the stack** (`docs/pass-30-shots/heroes/hero-ch3.png`). Readers get the stack growing down and the traffic to the registers, but cannot tie "high address / low address" to anything (nothing says memory positions are numbered) and cannot tell what the "stack top" register holds. Options: (a) a one-line key ("memory places are numbered; each new call takes lower numbers") and a pointer from "stack top" to the helper box; (b) accept. Recommended: (a).
- **Hero Ch12, JavaScript** (`docs/pass-30-shots/heroes/hero-ch12.png`). Every word now reads (the notes beside the code are repeated back correctly); the curly braces, the largest mark, read as decoration. Options: (a) a small label on the braces ("a block of code"); (b) accept: the braces are the chapter's emblem, not a mark to decode. Recommended: (b).

## B. Kept-original figures: Gate 1 findings, reported, not repaired

The 18 kept-original figures are the owner's decision and are not edited (brief). Gate 1 still measured them (final run, Chromium and WebKit, 320 to 1440 px; contrast at 1440 px); these findings stand and do not block v1.0. Every one is "kept original, small on a phone": its smallest label at 375 px is far below the 11 px floor the redrawn figures meet. Screenshots: the figures as they are on the page.

| Figure | Smallest label at 375 px | Text under 4.5:1 (lowest) | Named marks under 3:1 (lowest) | Layout |
|---|---|---|---|---|
| fig-3-7 | 4 px | 10 (2.66) | 10 (1.02) | one label spills out of its box ("A A A …") |
| fig-3-8 | 3.5 px | 15 (3.27) | 13 (1.06) | the serif caption line overlaps the two check boxes |
| fig-3-9 | 4 px | 10 (2.67) | 22 (1.04) | clean |
| fig-3-10 | 3.5 px | 17 (3.74) | 12 (1.0) | clean |
| fig-3-11 | 4 px | 9 (2.67) | 7 (1.85) | clean |
| fig-br-3 | 3.5 px | 15 (2.71) | 13 (1.0) | clean |
| fig-10-10 | 3.5 px | 4 (3.82) | 11 (1.32) | clean |
| fig-10-11 | 4 px | 3 (3.82) | 7 (1.04) | clean |
| fig-11-7 | 4 px | 4 (3.17) | 5 (1.04) | clean |
| fig-12-9 | 4 px | 3 (4.4) | 3 (1.13) | clean |
| fig-12-10 | 4 px | 3 (4.33) | 2 (1.13) | clean |
| fig-13-10 | 4.5 px | 4 (2.69) | 4 (1.04) | the heading "QUERY THE DATABASE ACTUALLY EXECUTES" spills out of its box |
| fig-15-2 | 4 px | 0 | 6 (1.06) | clean |
| fig-15-3 | 4 px | 3 (2.45) | 7 (1.04) | clean |
| fig-15-4 | 4 px | 0 | 4 (1.05) | clean |
| fig-15-6 | 4 px | 0 | 6 (1.02) | clean |
| fig-15-8 | 4.5 px | 0 | 6 (1.06) | clean |
| fig-15-9 | 4 px | 0 | 7 (1.06) | in fullscreen at 1024 and 1440 px, "root web server · over-permissioned IAM" spills out of its box |

Also left as they are (Pass 29 handover, `UNDER.md` §4ac): captions that use terms the section never explains, Fig 10.10 and 10.11 (MSS, "tuple"), 11.7, 12.9 (template engines, OWASP) and 12.10 (Trusted Types). Four kept originals still carry errors the corrected prose contradicts (`docs/pass-29-part1-open.md`, §4g): Fig 3.7 ("+ 11 unused bytes" should be 10), Fig 3.9 ("~16 bits of randomness" against its own caption's 28 to 32), Fig 3.10 (system()'s argument in RSI, which should be RDI; the caption says DEP marks code non-executable, where it marks data pages), Fig BR.3 (SYSCALL drawn as an IDT source; timer and keyboard vectors; already in STATE.md, BLOCKED ON TIGER). The verifier also flagged, unchanged from before: Fig 3.9 (the Run 3 ".text" label struck by its frame), Fig 15.2 (the "Rust in kernel" stem crosses the 2026 label), Fig 15.3 (the Alice-Bob line runs through "attacker"), Fig 15.6 (step 1 text grazes the internal DB box).

Options: (a) accept them as kept (recommended: the owner chose to keep them); (b) allow a typography-only pass (sizes, spacing, contrast) that keeps every drawing as it is.

## C. Gate 1: findings left open

Gate 1 reached zero on every redrawn figure, every hero and every icon in both engines at every width, in the page and in fullscreen, in the still and at every sampled frame, except these. The first two are believed false; the third is an owner call.

- **Fig 14.3, adjacent birthdays** (`docs/pass-30-shots/fig-14-3.png`). Three people in the 23 have birthdays on neighbouring days, so their 3 px ticks overlap by 2 px; the tool measures each tick against the next one (same colour, ratio near 1). Nothing is lost: identical marks abut, and a shared day is the salmon mark. Believed false. Options: (a) accept; (b) draw a 1 px gap between ticks that touch. Recommended: (a).
- **Fig 14.6, the pictures under ECB and CBC** (`docs/pass-30-shots/fig-14-6.png`). The three small images are drawn as columns of grey pixels; neighbouring pixels of a picture are close in tone by nature, so each column fails 3:1 against the next. The panel frames pass. Believed false: the comparison is between the three panels, not between pixels. Options: (a) accept; (b) redraw the images with fewer, more contrasting tones. Recommended: (a).
- **The cover** (`docs/pass-30-shots/heroes/cover.png`). Two kinds of finding remain. The five volume cards are tinted panels close to the page colour (fills 1.0 to 1.2:1, with the glow and aurora gradients); their frames now pass 3:1 and carry the edges. And during the cover's one-time entrance (about 1.5 s, before it settles), the numerals and motifs pass through half-faded frames that fail. Options: (a) accept: the cards are drawn by their frames and the entrance plays once; (b) deepen each card's tint until it holds 3:1 against the page (a visible change to the five part identities) and make the entrance a cut. Recommended: (a).
