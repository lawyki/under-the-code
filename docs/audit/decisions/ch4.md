# Chapter 4 · decisions

Round 1: `docs/audit/round1/ch4.json` (73: 72 confirmed, 1 owner) and part-2.json items 1, 5, 9, 11, 15, 16, 17, 18 (Ch4 half), 23 (1-based). Numbers below are the 0-based indexes in ch4.json.

## Applied (own wording where the judge's wording did not fit)
- 0 · ch4-anatomy-p5: how a Ring 3 driver reaches its device (the kernel maps just its own device registers into it and passes on its interrupts as messages).
- 1, 62 · Fig 4.2 strip: "IPC" not used before Section 05 defines it; the microkernel's parts "send their requests as messages through the kernel".
- 2, 61 · Fig 4.3 caption and Load bullet: why the symbol table (a separately built module cannot know where the kernel's functions sit; the table pairs each name with its address); commands set as code. The caption's closing slogan dropped to keep it to two sentences.
- 3, 44, part-2 5 · O(log N) glossed once at first use, in the CFS table row ("one more step each time the number of processes doubles, written O(log N)"); Fig 4.4's strip says "a few dozen steps at most"; the chapter summary keeps "O(log N) steps".
- 4 · ch4-scheduling-p5: what the red-black tree buys (each step rules out about half; recolouring and turning a few nodes keep branches level).
- 5 · Fig 4.5 strip: what "wait" and "first run after" count.
- 6 · MLFQ "approximates SJF … when short jobs mix with long ones"; the strip says why it looks like round robin here (every job is CPU-bound).
- 7 · ch4-vm-p15: the kernel's own note that the read-only pages are really writable, so the fault copies instead of ending the process.
- 8 · ch4-vm-p17: why the write reached the file (the kernel did the write for the attacker and, after the discard, looked the page up again and found the file's own page).
- 9 · ch4-vm-p10: the never-used page is a minor fault (a fresh page of zeros, no disk read).
- 10, 28, 36, 42 · ch4-fs-p6 opens on Chapter 1's creed instead of teaching it again; "Most" kernel-managed resources; the keyboard is "one of the /dev/input/event* files"; the network bullet cut; p7 says what a read does on a file with no data blocks.
- 11, 43 · the socket parenthetical in ch4-fs-p7 cut (sockets are taught in Section 05).
- 12, 22 · ch4-fs-p9: the journal holds the filesystem's own bookkeeping (inodes, the free list, directories), and by default ext4 writes file contents before the commit (data=ordered; docs.kernel.org/admin-guide/ext4.html). §4g's Fig 4.13 row (not every write twice) now holds in the prose too. Fig 4.13's strip says "the free list", as the figure does.
- 13 · ch4-fs-p11: why a copy-on-write change climbs to a new root (blocks hang in a tree; each parent holds the changed address).
- 14 · Fig 4.17 caption: when "the next return from the kernel" comes (the end of its next system call or timer interrupt).
- 15, 51, part-2 15 · Fig 4.15 caption names the picture (cat at one pointer, grep at the other) and drops "locks"; "The lineage" cut; "Two descriptors" uses cat and grep, not standard input and output before p6.
- 16 · Fig 4.17 strip: "handles or ignores every other signal" (not "trapped").
- 17 · ch4-security-p8: a mount namespace is "its own tree of files from / down, unpacked from a container image".
- 18 · ch4-security-p15: how a verifier can prove termination after Chapter 1's Turing: it accepts only programs simple enough to prove.
- 19 · Fig 4.20 strip: "The network" in words the reader has (a virtual network card joined by a virtual cable), pointing to Part III.
- 20 · Dirty COW: "at least nine years"; Fig 4.11 reads "2005 a fix, undone within days" and "2007 2.6.22: oldest kernel listed", the bar "nine years or more, in every kernel" (commits 4ceb5db9757a, f33ea7f404e5, 19be0eaffa3a; the dirtycow wiki's "since around 2.6.22").
- 21, 41, part-2 11 · ch4-scheduling-p2: "Many early personal-computer systems were cooperative, the model the Bridge described" (CTSS, 1961, was preemptive); p3 says the timer is the Bridge's, not a new idea. Both ids kept.
- 23 · ch4-anatomy-p2: the kernel "stays in memory, in charge of the machine" (the §4g glossary row: resident, not always running).
- 24, part-2 9 · EEVDF's deadline is virtual, set by the slice a task asks for, and it gives no real-time guarantee (docs.kernel.org/scheduler/sched-eevdf.html); p12 names CFS and EEVDF together.
- 25, 45 · ch4-scheduling-p10: M/M/1 needs random service times too; ρ = λ/μ derived, so the 20 and 100 follow; "four points more load". Fig 4.6's strip in step.
- 26 · Little's Law: "20 inside on average".
- 27 · mmap: "some databases (LMDB) and search engines (Lucene)" (Crotty, Leis, Pavlo, CIDR 2022).
- 29 · Dijkstra's semaphore "set out in" the 1965 note (invented 1962–63, EWD-35).
- 30 · Fig 4.20 caption: "A PID namespace is a translation table, not a copy".
- 31 · Fig 4.20 strip: clone() starts a new process; unshare() moves the caller (unshare(2)).
- 32 · "roughly 30 million lines of code".
- 33, 68 · SJF row: non-preemptive, as Fig 4.5 draws it.
- 34, 65 · Fig 4.4's first frame reads "scheduler picks 3.2", not "idle".
- 35 · ch4-fs-p1: the filesystem groups sectors into blocks, typically 4 KiB (so Fig 4.12's five blocks for 18,400 bytes check).
- 37 · Fig 4.18 strip: sem_wait() and sem_post() "use" atomic instructions.
- 38 · ch4-security-p3: root needs a bug to enter Ring 0 only where the kernel walls it off (lockdown; kernel_lockdown(7)).
- 39 · Fig 4.21 strip: io.max and pids.max are further files.
- 40 (owner), part-2 1 · Section 03 no longer teaches the hardware again: p2 points at the MMU of Fig BR.4 (its glossary entry now homes in Chapter 1, ch1-memory); p7 and p8 keep only what the kernel must manage (the miss, the switch). p3 to p5 and Fig 4.8 stay: p4 holds the book's only derivation of 512 GiB. The larger cut the owner verdict allows is not needed after this; recorded in owner-calls.md.
- part-2 16 · binary units in Section 03 (4 KiB, 256 TiB, 512 GiB), as the Bridge writes them.
- 46, 70 · Fig 4.1 caption names the thread and the bottom row; Linux "in most servers, phones and supercomputers" (drawn row "Linux: servers, phones"; desc in step).
- 47 · hero lead without fragments, triplet or reveal.
- 48 · ch4-security-p17: the two halves of the contrast in two sentences.
- 49, part-2 23 · Fig 4.13 caption names the two drawn outcomes; "The lineage" cut.
- 50, 72 · Fig 4.4 caption names the values drawn.
- 52 · Fig 4.16's "The philosophy" bullet cut (the pull-quote follows).
- 53 · Fig 4.19 caption ends before restating p11.
- 54 · Fig 4.7's "Hard real time" bullet cut.
- 55 · Fig 4.22's "A second guard" cut; caption names programs A and B.
- 56 · ch4-ipc-p2: "The kernel offers eight mechanisms:".
- 57 · ch4-ipc-p1 without the anaphoric triplet or "pipelines".
- 58 · "A semaphore is a counter changed atomically, in one step that nothing can interrupt."
- 59 · "indexes" in Fig 4.8's caption and desc.
- 60, part-2 17 · "filesystem" throughout Fig 4.2.
- 63 · metadata glossed in ch4-fs-p8.
- 64 · Fig 4.4's last frame redrawn: six processes, and 13.0 goes back in as a new leaf under 17.2 with nothing else moving (a valid red-black insertion); 8.1 is lit as the new leftmost.
- 66 · Fig 4.21: after the kill, batch's CPU, "wants" outline and memory bars stay at zero until the loop wraps.
- 67 · Fig 4.2: the monolithic counter turns 2 when the request crosses back, not a second early.
- 69 · Fig 4.5: the one-unit round-robin slot carries its D.
- 71 · Fig 4.17 caption: SIGKILL ends the process "at that same point", instead of diverting it.
- part-2 18 · "Usenet" in ch4-anatomy-p6 (Chapter 7's half with Chapter 7).

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch4-newcomer.json`, `ch4-expert.json`

Applied (one revision):
- Fig 4.4 (expert): the runner climbed from 3.2 to 13.0, past every other process, against the rule that the least-served runs. The values are now 3.2, 8.1, 8.4, 8.6, 17.2, 19.8; the runner ends at 8.9, a little past the others, and goes back in after 8.6 as a new leaf (still nothing else moves); caption and desc in step.
- Fig 4.3 caption (newcomer): three sentences; now two (insmod and rmmod together).
- ch4-scheduling-p5 (newcomer): "recolours or turns" named a colouring the book never draws; now "rearranges a few nodes".
- Fig 4.11 (newcomer): "a fix for this race, undone" and "2.6.22: oldest in the advisories".
- ch4-vm-p17 (newcomer): why the kernel did the write (it went through /proc/self/mem, a file through which the kernel writes into a process's own memory for it).
- Chapter 4 summary (expert): C is "the language of Linux and most production kernels", not every one (XNU's IOKit is C++; Linux now takes Rust).

Fixed after Gate 1:
- Fig 4.3 caption was three sentences at 60+ words; now two (54 words): insmod and rmmod together, then the symbol-table lookup and the init function in Ring 0.
- Fig 4.16: the five connector lines were below 3:1 against the card (pre-existing); stroke now at 0.55 opacity.
- Fig 4.4: the new leaf's lead circle had a fill that failed contrast in motion; it is drawn as an outline.

## Owner calls (owner-calls.md, Chapter 4)
- 40 (Section 03 teaching the MMU again): done in the text as far as the author's call reaches; the larger cut is recorded as an option.

## Checks
- `build:glossary`: the Memory Management Unit entry now homes in Chapter 1 (ch1-memory), where the book first teaches it; no entry added or lost. `build:sections` timestamp only, restored. `check:dashes` clean. Anchor ids outside SVGs unchanged.
- Gate 1 on the 18 changed figures: still with fullscreen 14/216 (Chromium) before the fixes above, then 0/36 on Figs 4.3, 4.4, 4.16; 0/216 (WebKit). Motion with fullscreen 60/864 (Chromium) before the fixes, then 0/144 on those three; motion 0/432 (WebKit). hero-ch4 0/4.
- clip (part-2): 0 findings in 12 runs. pass25: see RESUME.md.
