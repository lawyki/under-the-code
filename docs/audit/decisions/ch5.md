# Chapter 5 · decisions

Round 1: `docs/audit/round1/ch5.json` (44 confirmed) and part-2.json items 2, 6, 7, 13, 14, 20 (1-based). Numbers below are the 0-based indexes in ch5.json.

## Applied (own wording where the judge's wording did not fit)
- 0 · Fig 5.1 strip: lea's brackets look like Fig 3.2's memory, but lea only works out the address and never reads it.
- 1 · Fig 5.3 strip: "extra instructions to pull it out of its word", not "shifting and masking" (never taught).
- 2 · ch5-malloc-p1: "heap memory", not "dynamic memory".
- 3 · ch5-malloc-p3: a chunk in use never moves (the program holds its address), so the allocator cannot slide chunks together.
- 4, 23, 24, 12, part-2 2, part-2 6 · ch5-ub-p5: the NULL path is Fig 4.9's invalid exit, told once; the crash is the operating system's doing, not C's; the optimiser may delete a later NULL check, which is why Linux builds with -fno-delete-null-pointer-checks. Fig 5.9's caption names the picture; its strip says a NULL access "that reaches the processor" traps.
- 5 · Fig 5.11 strip: what an object is, in half a sentence (Chapter 6 teaches it).
- 6, 16 · Fig 5.11 strip, third wave: Rust rules out use-after-free and data races at compile time and checks bounds as it runs (as ch3-overflow-p9 says); Go and Swift compile to machine code but manage memory.
- 7, 33 · ch5-survives-p6 names "his own creation, C++".
- 8, 26 · ch5-survives-p1 without the fragments, the aphorism and the TLS claim (BoringSSL, the TLS of Chrome and Android, is C++ since 2024); it hands over to Fig 5.10.
- 9 · Thompson "found a little-used PDP-7" (Ritchie 1979); no windowless room; section title "Two men, a spare minicomputer, four years."
- 10 · "By 1972 Ritchie had added types" (he began in 1971; Ritchie 1993).
- 11, 20 · Fig 5.1: "x86: 1 to 15 bytes · ARM64: 4 · RISC-V: 4 or 2"; caption and desc no longer call RISC-V fixed.
- 13 · ch5-portability-p6: C's types are the byte and "an integer of the machine's natural size" (today's int is 32 bits on 64-bit machines).
- 14 · ch5-bell-labs-p3: the space-travel game was rewritten for the bare PDP-7 first; the OS came after, for a better place to work (Ritchie 1979).
- 15, 18, 38 · Fig 5.4 caption: no "never the next byte"; it says the double pointer stops when the next double would leave the 32 bytes.
- 17 · Fig 5.3 strip: the repeat "Its bytes are what forced types" cut.
- 19 · Fig 5.5 caption names the rewrite drawn.
- 21 · Fig 5.7 caption names the two drawn stories.
- 22 · ch5-malloc-p1: "nothing in the language frees memory for you" (garbage collection is introduced in p7).
- 25 · ch5-ub-p8 without the "not X but Y" reveal or the aphorism.
- 27 · Fig 5.10 strip: "Why others lean on it" (the calling convention), not a third telling of the three properties.
- 28 · ch5-bell-labs-p2 without the triplet ("no machine to build it on and no approved project to build it in").
- 29 · Fig 5.5 strip: "undefined behaviour (Section 05)".
- 30 · ch5-pointers-p8 ends at the buffer overflow of Chapter 3.
- 31 · ch5-ub-p7 keeps only the sanitizer (the Linux flags live in Fig 5.8's strip).
- 32 · Fig 5.8 caption: "(UB in the figure)".
- 34 · Fig 5.11: the counter reads "year 1984" … and "to 2016" at rest.
- 35 · Fig 5.4: "= 0x118 (last double)", and the desc says why the double pointer stops.
- 36 · Fig 5.7: the early "p = malloc(64)" label, shown while the chunk was still free, removed.
- 37 · ch5-pointers-p5: arrays count from 0.
- 39 · Fig 5.4 strip: "the block in each pointer's track", not a bracket.
- 40, part-2 20 · Fig 5.1 strip: rdi/rsi, as drawn.
- 41 · Fig 5.2: the 1971 row dims like the others until the sweep reaches it.
- 42 · Fig 5.6: each size label, and the free tail's box, word and 176, appear with their chunk, so the allocation phase no longer shows chunks that do not exist yet.
- 43 · Fig 5.3 moved to follow the PDP-11 paragraph, before the K&R heading.
- part-2 7 · Fig 5.2's "Why C" bullet cut (p7 tells it); ch5-bell-labs-p5 drops the repeated 1970 date.
- part-2 13 · "on the PDP-11, 1 byte for a character and 2 for an integer".
- part-2 14 · Fig 5.2's "The book" bullet cut (p6 tells it).

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch5-newcomer.json`, `ch5-expert.json`

The expert found nothing. Applied from the newcomer (one revision):
- Fig 5.11 strip: "data races" and "ownership" were never explained; now "data races (two threads changing the same memory at once)" and "by giving every value one owner that the compiler tracks".
- Fig 5.7 strip: "the ownership rules" replaced by what they do (every value has one owner, which frees it; any use after that is rejected at compile time).

## Checks
- `build:glossary`: no entry added, lost or moved; the three Section 02 entries carry the new section title. `build:sections` carries the new h2 ("Two men, a spare minicomputer, four years."). `check:dashes` clean. Anchor ids outside SVGs unchanged.
- Gate 1 on Figs 5.1 to 5.11: still with fullscreen 0/132 (Chromium) and 0/132 (WebKit); motion with fullscreen 0/528 (Chromium); motion 0/264 (WebKit).
- clip (part-2): 0 findings in 12 runs. pass25: see RESUME.md.
