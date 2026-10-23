# The Bridge · decisions

Round 1: `docs/audit/round1/chBridge.json` (52: 44 confirmed, 8 owner) and the remaining part-1.json items 2, 7, 9, 10, 11, 14, 20, 21, 22, 27 (1-based). Numbers below are the 0-based indexes in chBridge.json. Fig BR.3 is a kept original: its findings, and those on its caption (chBridge-trap-p5), are in `owner-calls.md` (the Bridge), nothing changed.

## Applied (own wording where the judge's wording did not fit)
- 0, 24 · chBridge-mode-p8: "raise the bit" read backwards against CPL 00/11; now "No program can switch the CPU into Ring 0 itself: only a trap does … And SYSRET, the way back to Ring 3, faults outside Ring 0: only the kernel moves the bit, in either direction" (felixcloutier.com/x86/sysret: #GP if CPL ≠ 0).
- 1 · chBridge-trap-p6: why a faked `int 14` does harm: the handler would act on the address of some earlier fault, because a real page fault records the address that failed and `int 14` records nothing.
- 5 · chBridge-mmu-p2: where 512 GiB comes from: 48-bit addresses, 2^36 pages, 8 bytes an entry (2^39 bytes).
- 6, 34, part-1 10 · chBridge-timer-p4 in two sentences, with the residual tick on a NO_HZ_FULL core ("a slow trickle remains, so the kernel can still take back a stuck task"; docs.kernel.org/timers/no_hz: a 1 Hz residual tick); Fig BR.6's "Tickless" strip item cut (it repeated p4).
- 7, 35 · chBridge-io-p2: "(MMIO)" and "(DMA)" at first use.
- 11, 17 · chBridge-mode-p6: "IRET or SYSRET on x86-64" (Linux enters its first user process through the IRET path, ret_from_fork; SYSRET is the fast return from a system call).
- 12, 19, 37, 46 · Fig BR.4: 0x7fff_a3c5_0010 was 16 pages above 0x7fff_a3c4_0010, not the next page, and Fig BR.5's "a3c4 → a200" were not page numbers. The addresses are now 0x7fff_fa3c_4010, 0x7fff_fa3c_5010 and 0x4a20_0010, so "the next page up" is true and BR.5's labels are the real last four digits of page and frame (0x7fffa3c4 → 0x4a200); the offset stays 0x010. §4g row 615 and the generator follow.
- 47 · Fig BR.4's still (reduced motion) showed only the store, so the offset note pointed at nothing. Both CPU lines now stay on screen (the inactive one at 0.55), and the RAM box shows the load's 0x4a20_0010 in the still and during the load; "not reached" shows only during the store.
- 50 · Fig BR.4: level 3 now fills gold on the load's walk like the other levels.
- 13, 20 · Fig BR.7: the network card's registers move to 0xD000_0000 (store at 0xD000_0018), so the frame buffer is no longer 1 MiB.
- 15, 18, 51 · Fig BR.1 strip: "#GP … the program gets no result" (a #GP does push an error code for the handler; Intel SDM vol. 3A, interrupt 13).
- 16, 21 · chBridge-synthesis-p6: "every time-slice switch" (a device interrupt that wakes a task can also force a switch).
- 23, part-1 20 · h3 "System calls, exceptions, interrupts: three kinds of trap".
- 25 · Fig BR.2 caption names the picture (Ring 3 left, Ring 0 right, the registers below) and keeps the timing.
- 26 · Fig BR.8 caption names the three drawn steps.
- 27 · Fig BR.9 caption: no garden path, no restatement of p2.
- 28 · Fig BR.1 caption names the picture.
- 29 · Fig BR.6 caption: "it" no longer points at the kernel; no repeat of p1.
- 30 · Fig BR.5 caption: the TLB is not glossed a third time.
- 31, part-1 7 · chBridge-mmu-p1: "the MMU of Chapter 1, the small piece of silicon between the CPU and the RAM" (not introduced as new).
- 32, part-1 9 · Fig BR.5 strip: "Keeping it true" cut (mmu-p7 says it); "Tags" names the PCID.
- 33, part-1 11 · Fig BR.8 strip: "Queues" (io-p4) and "The IOMMU" (io-p6) cut; "Scattered buffers" stays.
- 48 · Fig BR.8 drew no queue, so it reread as the kernel handing the command to the SSD (§4g row 616). The RAM box now carries "· command queue" and step 1 reads "1  command queued, doorbell rung" (the lighter repair; no new motion).
- 49 · Fig BR.6: the labels A, B, C, while (1), A sit inside the clip, so each appears with its slice instead of floating ahead.
- 36, part-1 21 · section title "The only way into the kernel" (sections.json and the glossary's section titles follow).
- 38 · "The diagram below maps the chain." cut.
- 39 · chBridge-io-p1: no four-verb list; the CPU no longer "types".
- 40 · chBridge-timer-p5: "fair turns for every program" in place of time-sharing, fairness and deadline scheduling.
- 41 · Fig BR.7 caption: "the physical address space", not "physical memory".
- 42 · "several gigabytes a second".
- 43 · chBridge-timer-p2: "One circuit does, the hardware timer: a counter …" (the verb no longer waits 17 words; the glossary's "hardware timer" cue is kept).
- part-1 2 · Fig BR.2 strip: the system-call argument registers named (RDI, RSI, RDX, R10, R8, R9; R10 in place of RCX, which SYSCALL overwrites).
- part-1 22 · Fig BR.6 strip: "the timer in each core's interrupt controller (the local APIC on x86; on ARM, the generic timer)".
- 14 · Fig BR.6's "Tickless" item, which gave both NO_HZ modes the purpose of saving power, is cut with 34.
- Pending note from the handoff: Figs BR.1 and BR.2 now have their own title ids (svgt-part1-br-1, -br-2); Figs 3.9 and 3.10 keep -39 and -40. No duplicate SVG ids are left in part-1.

## Owner calls (owner-calls.md, the Bridge)
- 2, 8, 22, 44 (Fig BR.3's SOURCE box draws SYSCALL as an IDT source); 4, 9 (vectors 32 and 33 with Linux handler names); 3, 10, 45 (the caption's "any trap"). part-1 14 and 27 are Chapter 3 figures and are listed there.

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/chBridge-newcomer.json`, `chBridge-expert.json`

Applied (one revision):
- chBridge-timer-p4 (expert): the residual tick of a NO_HZ_FULL core is housekeeping, not a way to take back a stuck task; with one task there is nothing to share, and the full tick returns as soon as a second task is ready. The paragraph now says that (it also answers round 1's question about a stuck lone task).
- Fig BR.8 (newcomer): one label named both the buffer and the queue; the queue is now its own small box beside the buffer's title.

Gate 1 leftovers fixed: Fig BR.7's caption had grown to 62 words ("the physical address space"), now 60; Fig BR.4's lit level fills at 0.35 read 2.07:1 in WebKit, so all eight highlight fills are now 0.55 (3.4:1, white text on them 5.4:1).

## Checks
- `build:glossary` (section titles follow the new h2; "hardware timer" kept by the "One circuit does, the hardware timer:" cue), `build:sections` (the new section title), `check:dashes` clean; anchor ids outside SVGs unchanged; no duplicate SVG ids left in part-1.
- Gate 1 on Figs BR.1, BR.2, BR.4 to BR.9: all four runs 0 failures after the fixes above (BR.4, BR.7, BR.8 re-run: still+fs 0/36 Chromium and WebKit, motion+fs 0/144 Chromium, motion 0/72 WebKit).
- clip (part-1): 0 findings. pass25: see RESUME.md.
