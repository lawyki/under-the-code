# Chapter 3 · decisions

Round 1: `docs/audit/round1/ch3.json` (69: 50 confirmed, 19 owner) and part-1.json items 1, 5, 6, 19, 23, 24 and 26 (1-based). Numbers below are the 0-based indexes in ch3.json. Figs 3.7 to 3.11 are kept originals and the Aleph One pull-quote is owner-chosen: their findings, and those on the kept figures' captions, are in `owner-calls.md` (Chapter 3), nothing changed.

## Applied (own wording where the judge's wording did not fit)
- 0 · Fig 3.1 strip: why 6 bytes, not 7 (rax has a shorter form with no register byte). Checked: `add rax, imm32` is REX.W 05 id, six bytes (felixcloutier.com/x86/add).
- 1, 56 · ch3-registers-p2: "arguments (the values handed to it when it is called)".
- 2, 24, 61 · Fig 3.6: main's top slot is now "caller's rbp, saved" and the next "main's variables" (main's `push rbp` runs before any locals exist, so the saved rbp sits higher); only add's slot says "main's rbp, saved". Desc and generator in step.
- 3 · ch3-overflow-p3: one sentence says Fig 3.7 lists the lowest address at the top, so there the copy runs down the page (the figure stays as drawn).
- 4 · ch3-overflow-p5: "(In Fig 3.7 the A's stand where that code would go.)"
- 6 · ch3-defenses-p8: why whole functions were a limit: one at a time, and on x86-64 a plain return cannot put system()'s argument in RDI (Fig 3.4). The pop-rdi gadget is then the answer.
- 7, 26 · heading "Return-Oriented Programming, and defence four".
- 8, 34, part-1 26 · the arms race in order: p5 dates software non-executable stacks for Linux to 1997 (Solar Designer's patch, answered by return-to-libc the same year) and AMD's NX bit to 2003; p6 says ASLR (PaX, 2001) came two years before the NX bit reached x86 hardware. Fig 3.11's own order is an owner call.
- 18, 58, 29, part-1 5 · ch3-isa-p1: the 8086's instruction set "its descendants have extended but never replaced" (64-bit mode drops AAA, DAA, segment push/pop and turns INC/DEC 40–4F into REX prefixes; felixcloutier.com/x86/aaa); the "Not X. Y." reveal and the triplet gone; ISA is "the instruction set architecture (ISA) of Chapter 1", no longer taught as new.
- 19 · "runs most PCs and most servers" (Arm PCs are about 13% of shipments, 2025).
- 57 · ARM "licensed to chip designers such as Apple and Qualcomm" (§4g row 646 kept: chip designers, not handset makers), so the phone claim is made once.
- 20, 48 · RCX cell: "The `rep` prefix and the `loop` instruction take their count from RCX" (Intel SDM vol. 2, REP, LOOP).
- 21, 42, part-1 1 · ch3-call-p6: "a plain `ret` does not check it", pointing ahead to Section 06's hardware that does; the duplicate "ret jumps there instead" cut from Fig 3.6's strip.
- 22 · ch3-overflow-p10: the unsourced "majority of critical CVEs" sentence cut; the CVE gloss moves to the sourced 70% sentence.
- 27 · Fig 3.6 strip: call pushes "the address of the next instruction in main (its `pop rbp`)"; "main+19" and "Neither function sees the handoff" gone.
- 28, 50, part-1 19 · ch3-registers-p4: RIP is "the instruction pointer, x86's name for Chapter 1's program counter"; the aphorism closer cut.
- 30, part-1 6 · registers-p2 names the calling convention (Section 04) where it first describes it; call-p2 now says "the calling convention" (key term kept there, so the glossary home does not move) (ABI still expanded in call-p2, where the glossary takes its "System V AMD64 ABI" entry).
- 31 · Fig 3.6 caption names the picture: "The stack and RIP through one call of add, from call to ret."
- 32 · ch3-stack-p4 ends "Data that must outlive the call goes on the heap instead (Fig 3.5)"; the caption keeps the heap's definition.
- 33 · ch3-defenses-p3 no longer repeats p2 (the compiler's check); kept captions' duplication is an owner call.
- 35 · "ten percent of the computers then connected to the network".
- 36 · "a program that runs whatever commands are typed into it".
- 37, 62 · "One register, five names" (label, title, caption, generator).
- 43 · Fig 3.2 caption names the picture: three Intel lines, six ARM lines, which line becomes which.
- 44, part-1 5 · ch3-isa-p7's closing restatement of binary incompatibility cut (the fourth telling).
- 45 · Fig 3.1: the caption's "meaningless" sentence cut; the drawn line and desc now say "other chips read these bits differently" (p7 is right that the bits mean different things elsewhere; "nothing" was wrong).
- 46, part-1 23 · the stack is "a last-in-first-out region", not a buffer.
- 47 · RSP row: "Moves as values go on and come off the stack (next section)"; RBP row: "Lets a function find its own values at fixed distances"; one "next section" removed from registers-p2.
- 49 · RBP row: "Base Pointer (the frame pointer)".
- 51, 55 · ch3-defenses-p6: libc glossed where the argument needs it ("the C library (libc, the ready-made code every C program loads)"); the shell is not defined a second time.
- 52 · Blaster cut (an unexplained fourth example); "rather than an overflow".
- 53 · ch3-defenses-p8: the repeated "short fragments of existing code" collapsed.
- 54 · Fig 3.5 strip: "the MMU from Chapter 1, opened up in the Bridge".
- 59 · hero lead: one sentence, no triplet or intensifiers.
- 60 · era "1972 → present" (C, 1972, is the chapter's earliest date).
- part-1 24 · "ARM Pointer Authentication (PAC)", the name the kept figures use.
- Pending note from the handoff: the Ch3 hero's title id is now its own (svgt-part1-ch3-hero); Fig 3.2 keeps svgt-part1-30.

## Owner calls (owner-calls.md, Chapter 3)
- 5, 16, 41, 64 (Fig 3.7, 11 → 10 unused bytes); 9, 13, 39, 63 (Fig 3.10's chain); 10, 14, 67 (Fig 3.10 caption, "code" → "data"); 11, 15, 40, 65, 17, 25, 68 (Fig 3.9); 12 (Aleph One quote, fact H); 23, 38, 66 (Fig 3.11).

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch3-newcomer.json`, `ch3-expert.json`

Applied (one revision):
- ch3-registers-p2 (expert): "The chapter uses six registers" was false (Fig 3.4 and the table name more); now "Six of them matter most here".
- ch3-overflow-p1 (newcomer): "daemon" was never defined; now "fingerd, a UNIX background program that answered queries about a machine's users".

## Checks
- `build:glossary` (only the scanned count moved; the System V AMD64 ABI entry kept by leaving the "(application binary interface)" cue in call-p2), `build:sections` (timestamp only, restored), `check:dashes` clean; anchor ids outside SVGs unchanged.
- Gate 1 on Figs 3.1, 3.2, 3.3, 3.5, 3.6: still with fullscreen 0/60 (Chromium) and 0/60 (WebKit); motion with fullscreen 0/240 (Chromium); motion 0/120 (WebKit); hero-ch3 0/4 (overlay scrollbars, as for Chapter 2).
- clip (part-1): 0 findings. pass25: see RESUME.md.
