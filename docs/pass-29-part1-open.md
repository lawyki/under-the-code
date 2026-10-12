# Part I · what is still open (audit 2026-10-12)

The 114 owner-call items in `docs/pass-29-owner-calls.md` were checked against the live text after the law-4 rewrite. Four auditors (one per chapter) did the check and four skeptics re-checked every verdict. Result: 68 fixed, 6 obsolete (the sentence is gone), 40 still open. The 40 include duplicates; the distinct items are below. Raw result: workflow wf_f1c1fc38-398.

## Prose (law-4 work; Chapter 3 carries most of it)

- ch1-transistor-p7: nothing says where the gate's electrons come from (the n-type source and drain).
- ch1-transistor-p8 (Fig 1.5 caption): "its field reaches through the insulator", but a field is never explained.
- ch1-kernel-p8: what reading a running program "like a file" means is still unexplained.
- ch1-memory-p10: nothing says how a page sent to disk comes back when it is touched (the page fault). Also, the memory table's RAM row "~100 cycles (~60 ns)" contradicts its own 0.3 ns per cycle.
- ch2-boole h3: "the most consequential paper of the 20th century" claims more than the source (Goldstine: "one of the most important master's theses ever written").
- ch2-twos-p10: the case never says where the −1 comes from (attacker input, or a length sum that wrapped).
- ch2-arithmetic-p7: the italic closer is still there.
- ch3-isa-p2: the licensing clause ("licensed to the chip designers behind nearly every phone") is missing. The Android fix landed but is not in §4g.
- ch3-isa-p7: "hot code" is not glossed.
- ch3-isa-p5 and Fig 3.2: only the middle line's split into ARM lines is explained at the figure.
- ch3-registers-p2: push and pop are named before ch3-stack-p3 says what they do. The rewrite also cut the only definition of "volatile", which Fig 3.4 still uses.
- ch3-registers table: the RIP row omits interrupts and exceptions; the RBX row says "historically pointed to data segments".
- ch3-stack-p3: "the one data structure the ISA understands" is wrong (x87 register stack; page-table walks). ch3-stack-p1: "By convention" growth direction (push decrements RSP in hardware; only the placement is convention).
- ch3-stack-p2: the heap's purpose, as distinct from the stack, is never said.
- ch3-stack-p4: no reason is given for saving the caller's registers, and since the rewrite no reason appears anywhere in the chapter.
- ch3-overflow-p5: reads as if the attack works today (add: stacks were then executable; DEP changed that).
- ch3-overflow-p8: "array" is never defined, and buffer[16] is never called one.
- ch3-overflow-p9: "runtime" and "managed runtime" are never defined; "cannot occur" is not scoped to ordinary safe code.
- ch3-defenses-p8: never says what ROP adds over return-to-libc. It also credits ROP with beating ASLR, against the §4g ch3-defenses-p9 row (Shacham 2007 beat W⊕X).
- Glossary "Boolean algebra" and "truth values": both still credit Boole with the modern inclusive-OR algebra (Jevons; contradicts ch2-boole-p5).

## Figures (Pass 30 work)

- Fig 1.6: Epyc, a four-die package, is plotted as "per chip"; the desc says "until about 2015".
- Fig 2.2 strip: credits Shannon with closed = 1, open = 0 (he used hindrance, the other way round).
- Fig 2.9: its title calls a sign-conversion bug an overflow (§4g ch2-twos).
- Fig 2.11: the caption promises a marker where the exact sum falls, but the SVG has none.
- Fig 3.1: "immediate" is never defined; the 7-byte line should be the 6-byte short form.
- Fig 3.2 strip: uses threads and memory order, never introduced.
- Fig 3.3 strip: "every" arithmetic instruction sets flags (not all do). Fig 3.4 strip: says large struct arguments go by hidden pointer (System V copies them onto the stack).
- Fig 3.6: return address main+5 should be main+19 (call at main+0x0e).
- Fig 3.7 (kept original): "+ 11 unused bytes" should be 10; no slot is marked as the payload.
- Fig 3.9 (kept original): "~16 bits of randomness" contradicts its own caption (28–32 bits).
- Fig 3.10 (kept original): system()'s argument goes in RSI (should be RDI), as a literal string; the caption says DEP marks code non-executable (it marks data pages).
- Fig BR.3 (kept original): draws SYSCALL as an IDT source; timer at vector 32, keyboard at 33 (§4g rows 528, 614); the caption says "When any trap fires".
- Fig BR.9 strip: "One level down" uses hypervisor and nested page tables, which Part I never teaches.
- Fig 1.5 "3 nm": owner-ruled; open only if the owner re-rules.

## Not Pass 29

- Every other Part I figure still needs its Pass 30 check (only Fig 1.1 is done).
- tests/pass25 invariants: 12 failures from the Go-deeper feature (see STATE.md).
