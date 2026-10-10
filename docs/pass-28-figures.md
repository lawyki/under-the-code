# Pass 28 · the figure ledger

Every figure, in book order. One at a time, each finished and tested before the next (docs/pass-28-brief.md).
Generator per figure: `scripts/figs/fig_<n>.py`. Gate per figure: `node tests/pass28/figs.mjs --part=<part> --fig=<id> --times=<frames>` (0 fail, Chromium + WebKit, 320 to 1440) and a look at 360/375 and 1440, fullscreen included.
Before = the 2026-10-10 baseline at 375 px (smallest label, caption words).

| # | Part | Figure | Before | Status |
|---|---|---|---|---|
| 1 | 1 | `fig-1-1` Fig 1.1 · A Turing machine · adding one | 2.6 px · cap 90 | done 2026-10-10 |
| 2 | 1 | `fig-1-2` Fig 1.2 · Enigma · one key, a different lamp every press | 2.6 px · cap 99 | done (pilot, 2026-10-10) |
| 3 | 1 | `fig-1-3` Fig 1.3 · The replacement · the same switch, without the fire | 2.2 px · cap 98 | done 2026-10-10 |
| 4 | 1 | `fig-1-4` Fig 1.4 · Transistor as a switch · base off, base on | 3.5 px · cap 61 | done 2026-10-10 |
| 5 | 1 | `fig-1-5` Fig 1.5 · Inside the switch · a field-effect transistor in cross-section | 2.9 px · cap 168 | done 2026-10-10 |
| 6 | 1 | `fig-1-6` Fig 1.6 · Moore's Law · transistors per chip, 1971 to 2024 | 2.9 px · cap 71 | done 2026-10-10 |
| 7 | 1 | `fig-1-7` Fig 1.7 · ENIAC and the Apple M4 · the same job, 79 years apart | 2.6 px · cap 71 | done 2026-10-10 |
| 8 | 1 | `fig-1-8` Fig 1.8 · Von Neumann architecture · one memory, one bus | 2.2 px · cap 74 | done 2026-10-10 |
| 9 | 1 | `fig-1-9` Fig 1.9 · The instruction cycle · fetch, decode, execute, writeback | 2.2 px · cap 47 | done 2026-10-10 |
| 10 | 1 | `fig-1-10` Fig 1.10 · From assembly to binary · one instruction decoded | 2.6 px · cap 97 | done (pilot, 2026-10-10) |
| 11 | 1 | `fig-1-11` Fig 1.11 · Pipelined execution · five instructions, five stages | 2.9 px · cap 93 | done 2026-10-10 |
| 12 | 1 | `fig-1-12` Fig 1.12 · Speculative execution · the CPU guesses, then checks | 2.6 px · cap 107 | done 2026-10-10 |
| 13 | 1 | `fig-1-13` Fig 1.13 · Running a program in 1955 · one job, one user, one machine | 2.2 px · cap 64 | done 2026-10-10 |
| 14 | 1 | `fig-1-14` Fig 1.14 · Protection rings · user programs, the kernel, the hardware | 3.1 px · cap 99 | done 2026-10-10 |
| 15 | 1 | `fig-1-15` Fig 1.15 · The hierarchy of forgetting · bigger and slower at every step | 2.6 px · cap 76 | done (pilot, 2026-10-10) |
| 16 | 1 | `fig-2-1` Fig 2.1 · Why binary survives noise · one threshold against two | 3 px · cap 42 | done 2026-10-10 |
| 17 | 1 | `fig-2-2` Fig 2.2 · Boole's algebra · Shannon's switches · the same AND | 2.6 px · cap 96 | done 2026-10-10 |
| 18 | 1 | `fig-2-3` Fig 2.3 · The three fundamental gates · AND, OR, NOT | 3.2 px · cap 51 | done 2026-10-10 |
| 19 | 1 | `fig-2-4` Fig 2.4 · Everything from NAND · NOT, AND and OR built from one gate | 2.9 px · cap 60 | done 2026-10-10 |
| 20 | 1 | `fig-2-5` Fig 2.5 · Adding 5 + 3 in binary · a ripple-carry adder | 2.6 px · cap 49 | done 2026-10-10 |
| 21 | 1 | `fig-2-6` Fig 2.6 · Inside a full adder · two half adders and an OR | 2.2 px · cap 78 | done 2026-10-10 |
| 22 | 1 | `fig-2-7` Fig 2.7 · Computing 7 − 5 = 2 with two's complement | 3.5 px · cap 51 | done 2026-10-10 |
| 23 | 1 | `fig-2-8` Fig 2.8 · The two's-complement wheel · where addition wraps | 2.6 px · cap 122 | done 2026-10-10 |
| 24 | 1 | `fig-2-9` Fig 2.9 · How a signed overflow becomes a buffer overflow | 2.9 px · cap 126 | done 2026-10-10 |
| 25 | 1 | `fig-2-10` Fig 2.10 · IEEE 754 double precision · sign, exponent, mantissa | 2.6 px · cap 63 | done 2026-10-10 |
| 26 | 1 | `fig-2-11` Fig 2.11 · 0.1 + 0.2 in binary · where the famous error lives | 2.9 px · cap 122 | done 2026-10-10 |
| 27 | 1 | `fig-2-12` Fig 2.12 · The Patriot missile · a clock that lost a third of a second | 2.6 px · cap 135 | done 2026-10-10 |
| 28 | 1 | `fig-3-1` Fig 3.1 · Same operation · three ISAs · three encodings | 2.2 px · cap 106 | done 2026-10-10 |
| 29 | 1 | `fig-3-2` Fig 3.2 · Rosetta 2 · an Intel app, translated once for an ARM chip | 2.2 px · cap 173 | done 2026-10-10 |
| 30 | 1 | `fig-3-3` Fig 3.3 · The x86-64 register file · one register, four names | 2.1 px · cap 122 | done 2026-10-10 |
| 31 | 1 | `fig-3-4` Fig 3.4 · System V calling convention · which register holds which argument | 2.4 px · cap 103 | done 2026-10-10 |
| 32 | 1 | `fig-3-5` Fig 3.5 · A process's virtual address space | 2.6 px · cap 50 | done 2026-10-10 |
| 33 | 1 | `fig-3-6` Fig 3.6 · The stack during a function call | 2.9 px · cap 58 | done 2026-10-10 |
| 34 | 1 | `fig-3-7` Fig 3.7 · Stack frame of greet(): normal vs overflow | 2.6 px · cap 57 | held: owner decision |
| 35 | 1 | `fig-3-8` Fig 3.8 · The stack canary · a tripwire between buffer and return address | 2.2 px · cap 110 | held: owner decision |
| 36 | 1 | `fig-3-9` Fig 3.9 · ASLR · the same binary, three random load layouts | 2.6 px · cap 122 | held: owner decision |
| 37 | 1 | `fig-3-10` Fig 3.10 · Return-Oriented Programming · arbitrary computation from existing code | 2.2 px · cap 137 | held: owner decision |
| 38 | 1 | `fig-3-11` Fig 3.11 · The arms race, in one diagram | 2.6 px · cap 53 | held: owner decision |
| 39 | 1 | `fig-br-1` Fig BR.1 · The privilege bit · two worlds, one chip | 2.6 px · cap 95 | done 2026-10-10 |
| 40 | 1 | `fig-br-2` Fig BR.2 · The trap mechanism · one round trip across the boundary | 2.2 px · cap 124 | done 2026-10-10 |
| 41 | 1 | `fig-br-3` Fig BR.3 · The interrupt descriptor table · 256 doors into the kernel | 2.2 px · cap 66 | held: owner decision |
| 42 | 1 | `fig-br-4` Fig BR.4 · The MMU · silicon between the CPU and the RAM | 2.1 px · cap 146 | todo |
| 43 | 1 | `fig-br-5` Fig BR.5 · The TLB · why the walk usually doesn't happen | 2.2 px · cap 65 | todo |
| 44 | 1 | `fig-br-6` Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back | 2.2 px · cap 97 | todo |
| 45 | 1 | `fig-br-7` Fig BR.7 · The physical address space · devices among the RAM | 2.2 px · cap 130 | todo |
| 46 | 1 | `fig-br-8` Fig BR.8 · Direct memory access · the device writes RAM by itself | 2.2 px · cap 113 | todo |
| 47 | 1 | `fig-br-9` Fig BR.9 · Hardware features → kernel → abstractions | 2.2 px · cap 112 | todo |
| 48 | 2 | `fig-4-1` Fig 4.1 · The Tanenbaum–Torvalds debate, January 1992 | 2.5 px · cap 118 | todo |
| 49 | 2 | `fig-4-2` Fig 4.2 · Monolithic vs microkernel | 2.5 px · cap 57 | todo |
| 50 | 2 | `fig-4-3` Fig 4.3 · A kernel module loading at runtime | 2.2 px · cap 120 | todo |
| 51 | 2 | `fig-4-4` Fig 4.4 · CFS chooses the leftmost node of a red-black tree | 2.5 px · cap 67 | todo |
| 52 | 2 | `fig-4-5` Fig 4.5 · Four schedulers, one workload | 2.5 px · cap 136 | todo |
| 53 | 2 | `fig-4-6` Fig 4.6 · L = λ · W and the cliff at full utilisation | 2.5 px · cap 112 | todo |
| 54 | 2 | `fig-4-7` Fig 4.7 · A periodic task and the deadline it must meet | 2.5 px · cap 120 | todo |
| 55 | 2 | `fig-4-8` Fig 4.8 · x86-64 four-level page table walk | 2.5 px · cap 67 | todo |
| 56 | 2 | `fig-4-9` Fig 4.9 · A page fault, decision tree | 2.5 px · cap 129 | todo |
| 57 | 2 | `fig-4-10` Fig 4.10 · Fork, then write: when shared pages diverge | 2.5 px · cap 123 | todo |
| 58 | 2 | `fig-4-11` Fig 4.11 · Dirty COW: the race that broke Linux | 2.5 px · cap 163 | todo |
| 59 | 2 | `fig-4-12` Fig 4.12 · Filename → inode → data blocks | 2.5 px · cap 56 | todo |
| 60 | 2 | `fig-4-13` Fig 4.13 · Journaling: write your intent before doing it | 2.5 px · cap 139 | todo |
| 61 | 2 | `fig-4-14` Fig 4.14 · Copy-on-write filesystem: never overwrite, just re-point | 2.2 px · cap 155 | todo |
| 62 | 2 | `fig-4-15` Fig 4.15 · A pipe is a kernel ring buffer with two ends | 2.5 px · cap 89 | todo |
| 63 | 2 | `fig-4-16` Fig 4.16 · The UNIX philosophy, in five processes | 2.2 px · cap 111 | todo |
| 64 | 2 | `fig-4-17` Fig 4.17 · A signal arrives mid-execution | 2.9 px · cap 148 | todo |
| 65 | 2 | `fig-4-18` Fig 4.18 · Two processes, one region, one gate | 2.2 px · cap 126 | todo |
| 66 | 2 | `fig-4-19` Fig 4.19 · VMs vs containers | 2.5 px · cap 60 | todo |
| 67 | 2 | `fig-4-20` Fig 4.20 · Namespaces: each container sees its own world | 2.5 px · cap 121 | todo |
| 68 | 2 | `fig-4-21` Fig 4.21 · Cgroups: quotas as taps on the resource flow | 2.5 px · cap 132 | todo |
| 69 | 2 | `fig-4-22` Fig 4.22 · eBPF: untrusted code in the kernel, made safe by proof | 2.5 px · cap 135 | todo |
| 70 | 2 | `fig-5-1` Fig 5.1 · One C source, many targets | 2.2 px · cap 74 | todo |
| 71 | 2 | `fig-5-2` Fig 5.2 · UNIX's rewrite, in time | 2.2 px · cap 75 | todo |
| 72 | 2 | `fig-5-3` Fig 5.3 · PDP-7 to PDP-11 · the machines that shaped C | 2.2 px · cap 190 | todo |
| 73 | 2 | `fig-5-4` Fig 5.4 · A pointer walks down memory | 2.5 px · cap 86 | todo |
| 74 | 2 | `fig-5-5` Fig 5.5 · a[i] ≡ *(a + i) | 2.5 px · cap 76 | todo |
| 75 | 2 | `fig-5-6` Fig 5.6 · The heap, as a free list | 2.5 px · cap 90 | todo |
| 76 | 2 | `fig-5-7` Fig 5.7 · Leak vs use-after-free | 2.5 px · cap 107 | todo |
| 77 | 2 | `fig-5-8` Fig 5.8 · How "trust the programmer" deletes your bug check | 2.9 px · cap 99 | todo |
| 78 | 2 | `fig-5-9` Fig 5.9 · A NULL dereference, traced | 2.5 px · cap 96 | todo |
| 79 | 2 | `fig-5-10` Fig 5.10 · Where C still runs in 2026 | 2.2 px · cap 121 | todo |
| 80 | 2 | `fig-5-11` Fig 5.11 · The C family tree · half a century of descendants | 2.2 px · cap 159 | todo |
| 81 | 2 | `fig-6-1` Fig 6.1 · The 1980s software crisis, in one chart | 2.5 px · cap 89 | todo |
| 82 | 2 | `fig-6-2` Fig 6.2 · C++, in time | 2.5 px · cap 90 | todo |
| 83 | 2 | `fig-6-3` Fig 6.3 · A class, an object, and a vtable | 2.5 px · cap 105 | todo |
| 84 | 2 | `fig-6-4` Fig 6.4 · Inheritance: same vptr slot, different function | 2.5 px · cap 94 | todo |
| 85 | 2 | `fig-6-5` Fig 6.5 · RAII: scope acquires, scope releases | 2.9 px · cap 125 | todo |
| 86 | 2 | `fig-6-6` Fig 6.6 · qsort vs std::sort, same algorithm, different cost | 2.5 px · cap 119 | todo |
| 87 | 2 | `fig-6-7` Fig 6.7 · Three pointer flavours, three ownership semantics | 2.5 px · cap 106 | todo |
| 88 | 2 | `fig-6-8` Fig 6.8 · A move is "I'm done with this, take it" | 2.5 px · cap 98 | todo |
| 89 | 2 | `fig-6-9` Fig 6.9 · C++ standards · the language eating its own complexity | 2.5 px · cap 149 | todo |
| 90 | 2 | `fig-7-1` Fig 7.1 · The two pipelines, side by side | 2.2 px · cap 84 | todo |
| 91 | 2 | `fig-7-2` Fig 7.2 · Python's slow conquest | 2.5 px · cap 93 | todo |
| 92 | 2 | `fig-7-3` Fig 7.3 · Duck typing: behaviour, not lineage | 2.5 px · cap 128 | todo |
| 93 | 2 | `fig-7-4` Fig 7.4 · Two Python threads, one GIL | 2.5 px · cap 99 | todo |
| 94 | 2 | `fig-7-5` Fig 7.5 · asyncio: cooperative scheduling on one thread | 2.5 px · cap 127 | todo |
| 95 | 2 | `fig-7-6` Fig 7.6 · CPython's pipeline, in detail | 2.2 px · cap 91 | todo |
| 96 | 2 | `fig-7-7` Fig 7.7 · Why Python is slow (and why nobody minds) | 2.9 px · cap 142 | todo |
| 97 | 2 | `fig-7-8` Fig 7.8 · How NumPy actually does work | 2.5 px · cap 103 | todo |
| 98 | 2 | `fig-7-9` Fig 7.9 · The same matmul, two ways | 2.5 px · cap 100 | todo |
| 99 | 3 | `fig-8-1` Fig 8.1 · One signal, two scales | 2.2 px · cap 88 | todo |
| 100 | 3 | `fig-8-2` Fig 8.2 · Three substrates, one job | 2.2 px · cap 110 | todo |
| 101 | 3 | `fig-8-3` Fig 8.3 · Entropy of a binary source as p varies | 2.5 px · cap 138 | todo |
| 102 | 3 | `fig-8-4` Fig 8.4 · Channel capacity as a function of SNR | 2.5 px · cap 166 | todo |
| 103 | 3 | `fig-8-5` Fig 8.5 · Manchester: every bit is a transition | 2.5 px · cap 127 | todo |
| 104 | 3 | `fig-8-6` Fig 8.6 · Same bits, two waveforms | 2.5 px · cap 122 | todo |
| 105 | 3 | `fig-8-7` Fig 8.7 · Three ways to ride bits on a carrier | 2.5 px · cap 115 | todo |
| 106 | 3 | `fig-8-8` Fig 8.8 · Two stations collide; both back off | 2.5 px · cap 139 | todo |
| 107 | 3 | `fig-8-9` Fig 8.9 · A MAC address, and the ARP cache that resolves it | 2.5 px · cap 157 | todo |
| 108 | 3 | `fig-8-10` Fig 8.10 · Hub vs switch: broadcast vs learned | 2.2 px · cap 137 | todo |
| 109 | 3 | `fig-8-11` Fig 8.11 · The OSI seven-layer cake | 3.2 px · cap 118 | todo |
| 110 | 3 | `fig-8-12` Fig 8.12 · OSI vs TCP/IP, side by side | 2.5 px · cap 108 | todo |
| 111 | 3 | `fig-9-1` Fig 9.1 · One call, two architectures | 2.5 px · cap 122 | todo |
| 112 | 3 | `fig-9-2` Fig 9.2 · The first internet | 2.2 px · cap 121 | todo |
| 113 | 3 | `fig-9-3` Fig 9.3 · Baran 1964: three architectural shapes | 2.5 px · cap 118 | todo |
| 114 | 3 | `fig-9-4` Fig 9.4 · The IPv4 header, byte by byte | 2.2 px · cap 153 | todo |
| 115 | 3 | `fig-9-5` Fig 9.5 · A 4 KB packet, fragmented onto a 1500-byte link | 2.2 px · cap 149 | todo |
| 116 | 3 | `fig-9-6` Fig 9.6 · BGP path-vector announcements | 2.2 px · cap 131 | todo |
| 117 | 3 | `fig-9-7` Fig 9.7 · The internet's tier hierarchy | 2.5 px · cap 161 | todo |
| 118 | 3 | `fig-9-8` Fig 9.8 · IPv4 ran out, then CGNAT papered over it | 2.5 px · cap 125 | todo |
| 119 | 3 | `fig-9-9` Fig 9.9 · The shape of an IPv4 vs an IPv6 address | 2.5 px · cap 120 | todo |
| 120 | 3 | `fig-9-10` Fig 9.10 · IP spoofing: a forged source field | 2.5 px · cap 134 | todo |
| 121 | 3 | `fig-9-11` Fig 9.11 · Pakistan/YouTube, 24 February 2008 | 2.2 px · cap 149 | todo |
| 122 | 3 | `fig-9-12` Fig 9.12 · A route leak: traffic takes the wrong door | 2.5 px · cap 148 | todo |
| 123 | 3 | `fig-10-1` Fig 10.1 · UDP: eight bytes, no state, no apologies | 2.2 px · cap 100 | todo |
| 124 | 3 | `fig-10-2` Fig 10.2 · The three-way handshake, in time | 2.5 px · cap 116 | todo |
| 125 | 3 | `fig-10-3` Fig 10.3 · TCP's state machine | 2.2 px · cap 112 | todo |
| 126 | 3 | `fig-10-4` Fig 10.4 · The sliding window | 2.5 px · cap 105 | todo |
| 127 | 3 | `fig-10-5` Fig 10.5 · The TCP sawtooth | 2.5 px · cap 109 | todo |
| 128 | 3 | `fig-10-6` Fig 10.6 · AIMD's fairness, in phase space | 2.2 px · cap 135 | todo |
| 129 | 3 | `fig-10-7` Fig 10.7 · CUBIC vs Reno: same loss, different recovery | 2.5 px · cap 105 | todo |
| 130 | 3 | `fig-10-8` Fig 10.8 · BBR aims for the bandwidth-delay product | 2.9 px · cap 140 | todo |
| 131 | 3 | `fig-10-9` Fig 10.9 · TCP+TLS+HTTP vs QUIC: the same job, two stacks | 2.5 px · cap 146 | todo |
| 132 | 3 | `fig-10-10` Fig 10.10 · SYN flood: half-open connections fill the table | 2.2 px · cap 129 | todo |
| 133 | 3 | `fig-10-11` Fig 10.11 · SYN cookies: the state goes into the wire | 2.5 px · cap 143 | todo |
| 134 | 3 | `fig-11-1` Fig 11.1 · March 1989 to August 1991 · a quiet two and a half years | 2.2 px · cap 105 | todo |
| 135 | 3 | `fig-11-2` Fig 11.2 · A complete HTTP exchange · request and response, byte for byte | 2.5 px · cap 98 | todo |
| 136 | 3 | `fig-11-3` Fig 11.3 · One curl, fully traced | 2.5 px · cap 96 | todo |
| 137 | 3 | `fig-11-4` Fig 11.4 · HTTP methods · what they promise, what caches and clients assume | 2.5 px · cap 111 | todo |
| 138 | 3 | `fig-11-5` Fig 11.5 · The DNS namespace · a tree, read right to left | 2.2 px · cap 119 | todo |
| 139 | 3 | `fig-11-6` Fig 11.6 · Recursive resolution · four servers, four questions, one answer | 2.2 px · cap 74 | todo |
| 140 | 3 | `fig-11-7` Fig 11.7 · Cache poisoning · the attacker races the real answer | 2.5 px · cap 152 | todo |
| 141 | 3 | `fig-11-8` Fig 11.8 · One-way function · easy forward, infeasible backward | 2.9 px · cap 101 | todo |
| 142 | 3 | `fig-11-9` Fig 11.9 · SHA-256 avalanche · one bit changed, all 256 bits scrambled | 2.5 px · cap 143 | todo |
| 143 | 3 | `fig-11-10` Fig 11.10 · Symmetric vs asymmetric · the same secret · or two halves of one | 2.5 px · cap 94 | todo |
| 144 | 3 | `fig-11-11` Fig 11.11 · TLS 1.3 · one round trip from "hello" to encrypted data | 2.5 px · cap 142 | todo |
| 145 | 3 | `fig-11-12` Fig 11.12 · The certificate chain · why your browser trusts a stranger | 2.5 px · cap 152 | todo |
| 146 | 3 | `fig-11-13` Fig 11.13 · Forward secrecy · stealing the long-term key tomorrow does not unlock yesterday | 2.2 px · cap 162 | todo |
| 147 | 3 | `fig-11-14` Fig 11.14 · HTTP/1.1 vs HTTP/2 · serial vs multiplexed on the same TCP connection | 1.9 px · cap 126 | todo |
| 148 | 3 | `fig-11-15` Fig 11.15 · HTTP/3 over QUIC · escaping TCP at the protocol layer | 2.5 px · cap 167 | todo |
| 149 | 3 | `fig-12-1` Fig 12.1 · The web of 1994–95 · static documents and a tab-out to Java | 2.5 px · cap 97 | todo |
| 150 | 3 | `fig-12-2` Fig 12.2 · May 1995 to ECMAScript 2026 · the slow legitimisation | 2.5 px · cap 110 | todo |
| 151 | 3 | `fig-12-3` Fig 12.3 · The event loop · stack, microtasks, macrotasks, render | 2.5 px · cap 105 | todo |
| 152 | 3 | `fig-12-4` Fig 12.4 · The same fetch · three eras of async syntax | 2.9 px · cap 92 | todo |
| 153 | 3 | `fig-12-5` Fig 12.5 · V8 · from source to optimised native code, with a feedback loop | 2.2 px · cap 138 | todo |
| 154 | 3 | `fig-12-6` Fig 12.6 · Node.js · V8 + libuv + a JavaScript stdlib | 2.5 px · cap 124 | todo |
| 155 | 3 | `fig-12-7` Fig 12.7 · Critical rendering path · five stages, one ~16 ms frame | 2.5 px · cap 100 | todo |
| 156 | 3 | `fig-12-8` Fig 12.8 · Same-origin policy · scheme + host + port must all match | 2.5 px · cap 99 | todo |
| 157 | 3 | `fig-12-9` Fig 12.9 · XSS · three ways for attacker code to run with your origin's privileges | 2.5 px · cap 134 | todo |
| 158 | 3 | `fig-12-10` Fig 12.10 · CSRF · the cookie attaches to the cross-site request unless we add a token | 2.5 px · cap 137 | todo |
| 159 | 3 | `fig-12-11` Fig 12.11 · CSP · the server tells the browser which scripts to trust, the browser refuses the rest | 2.9 px · cap 133 | todo |
| 160 | 4 | `fig-13-1` Fig 13.1 · Codd 1970 to PostgreSQL 18 · two lineages, fifty years | 2.5 px · cap 91 | todo |
| 161 | 4 | `fig-13-2` Fig 13.2 · Three operators · selection, projection, join | 2.5 px · cap 113 | todo |
| 162 | 4 | `fig-13-3` Fig 13.3 · Same query, three forms · SQL → relational algebra → execution plan | 2.5 px · cap 121 | todo |
| 163 | 4 | `fig-13-4` Fig 13.4 · Nested-loop · hash · merge: three ways to do the same join | 2.5 px · cap 115 | todo |
| 164 | 4 | `fig-13-5` Fig 13.5 · A bank transfer · what each ACID letter actually guarantees | 2.5 px · cap 102 | todo |
| 165 | 4 | `fig-13-6` Fig 13.6 · Write-ahead log · log first, mutate later, replay on crash | 2.5 px · cap 126 | todo |
| 166 | 4 | `fig-13-7` Fig 13.7 · The four isolation levels · what each one permits | 2.9 px · cap 145 | todo |
| 167 | 4 | `fig-13-8` Fig 13.8 · A B+ tree · range scan walks the leaves left to right | 2.9 px · cap 145 | todo |
| 168 | 4 | `fig-13-9` Fig 13.9 · B-tree vs hash index · which one wins which workload | 2.9 px · cap 131 | todo |
| 169 | 4 | `fig-13-10` Fig 13.10 · SQL injection · a single quote turns a SELECT into a tautology | 2.9 px · cap 162 | todo |
| 170 | 4 | `fig-13-11` Fig 13.11 · Parameterised queries · code and data on separate wires | 2.5 px · cap 121 | todo |
| 171 | 4 | `fig-14-1` Fig 14.1 · Two thousand years of cryptography in one strip | 2.5 px · cap 117 | todo |
| 172 | 4 | `fig-14-2` Fig 14.2 · The four one-way functions cryptography is built on | 2.5 px · cap 240 | todo |
| 173 | 4 | `fig-14-3` Fig 14.3 · Three hash properties · three different attacks | 2.5 px · cap 146 | todo |
| 174 | 4 | `fig-14-4` Fig 14.4 · Password storage · plaintext to hash to salted hash to slow KDF | 2.9 px · cap 129 | todo |
| 175 | 4 | `fig-14-5` Fig 14.5 · One AES round · four steps on a 4×4 byte grid | 2.2 px · cap 127 | todo |
| 176 | 4 | `fig-14-6` Fig 14.6 · ECB's famous failure · structure leaks through | 2.9 px · cap 142 | todo |
| 177 | 4 | `fig-14-7` Fig 14.7 · Diffie–Hellman with actual numbers · g=5, p=23 | 2.5 px · cap 129 | todo |
| 178 | 4 | `fig-14-8` Fig 14.8 · RSA worked through · p=17, q=23 | 2.5 px · cap 139 | todo |
| 179 | 4 | `fig-14-9` Fig 14.9 · Point addition on an elliptic curve · geometric picture | 2.9 px · cap 120 | todo |
| 180 | 4 | `fig-14-10` Fig 14.10 · Equivalent security · ECC keys are dramatically smaller | 2.9 px · cap 132 | todo |
| 181 | 4 | `fig-14-11` Fig 14.11 · TLS 1.3 handshake at cryptographic depth | 2.5 px · cap 141 | todo |
| 182 | 4 | `fig-14-12` Fig 14.12 · Digital signatures and Certificate Transparency · Merkle trees keep CAs honest | 2.2 px · cap 137 | todo |
| 183 | 4 | `fig-14-13` Fig 14.13 · Post-quantum migration · the algorithms that survive Shor | 2.9 px · cap 129 | todo |
| 184 | 4 | `fig-15-1` Fig 15.1 · STRIDE · the six classes of threat to enumerate | 2.5 px · cap 129 | todo |
| 185 | 4 | `fig-15-2` Fig 15.2 · The arms race continued · Fig 3.11 extended through 2026 | 2.5 px · cap 140 | todo |
| 186 | 4 | `fig-15-3` Fig 15.3 · Man-in-the-middle · with and without TLS | 2.5 px · cap 132 | todo |
| 187 | 4 | `fig-15-4` Fig 15.4 · ARP spoofing · poisoning the address-resolution cache | 2.5 px · cap 137 | todo |
| 188 | 4 | `fig-15-5` Fig 15.5 · SQL injection defence in depth · five layers, each independent | 2.5 px · cap 122 | todo |
| 189 | 4 | `fig-15-6` Fig 15.6 · SSRF · the server makes the request the attacker can't | 2.5 px · cap 134 | todo |
| 190 | 4 | `fig-15-7` Fig 15.7 · Five generations of defence · firewall → IDS → SIEM → EDR → zero trust | 2.5 px · cap 124 | todo |
| 191 | 4 | `fig-15-8` Fig 15.8 · Stuxnet · four zero-days, a USB jump, sabotage of physical machines | 2.9 px · cap 158 | todo |
| 192 | 4 | `fig-15-9` Fig 15.9 · The attack-pattern map · every specific exploit reduces to a few patterns | 2.5 px · cap 141 | todo |
| 193 | 4 | `fig-15-10` Fig 15.10 · The security ecosystem · learning, working, meeting | 2.5 px · cap 150 | todo |
| 194 | 5 | `fig-16-1` Fig 16.1 · Threads vs processes · the same parallelism, two isolation models | 2.5 px · cap 150 | todo |
| 195 | 5 | `fig-16-2` Fig 16.2 · The classic race · two threads, one counter, lost updates | 2.9 px · cap 122 | todo |
| 196 | 5 | `fig-16-3` Fig 16.3 · Mutex protects · deadlock is the new failure mode | 2.5 px · cap 144 | todo |
| 197 | 5 | `fig-16-4` Fig 16.4 · Compare-and-swap · the atomic primitive everything else is built on | 2.5 px · cap 115 | todo |
| 198 | 5 | `fig-16-5` Fig 16.5 · Memory orderings · four levels, four guarantees, four costs | 2.9 px · cap 134 | todo |
| 199 | 5 | `fig-16-6` Fig 16.6 · CPU vs GPU · few clever cores vs thousands of simple ones | 1.9 px · cap 148 | todo |
| 200 | 5 | `fig-16-7` Fig 16.7 · The CUDA hierarchy · thread → warp → block → grid | 2.5 px · cap 185 | todo |
| 201 | 5 | `fig-16-8` Fig 16.8 · Amdahl's law · the ceiling that won't move | 2.5 px · cap 128 | todo |
| 202 | 5 | `fig-16-9` Fig 16.9 · Amdahl vs Gustafson · same hardware, different question | 2.5 px · cap 129 | todo |
| 203 | 5 | `fig-16-10` Fig 16.10 · NUMA · two sockets, two memories, asymmetric latency | 2.5 px · cap 141 | todo |
| 204 | 5 | `fig-16-11` Fig 16.11 · MESI · how four cores keep one cache line consistent | 2.5 px · cap 155 | todo |
| 205 | 5 | `fig-17-1` Fig 17.1 · Type 1 vs Type 2 hypervisors · bare metal vs hosted | 2.5 px · cap 193 | todo |
| 206 | 5 | `fig-17-2` Fig 17.2 · Docker image layers · copy-on-write filesystems for software distribution | 2.5 px · cap 161 | todo |
| 207 | 5 | `fig-17-3` Fig 17.3 · Kubernetes architecture · control plane + workers | 2.2 px · cap 136 | todo |
| 208 | 5 | `fig-17-4` Fig 17.4 · The reconcile loop · observe, diff, act, repeat | 2.5 px · cap 125 | todo |
| 209 | 5 | `fig-17-5` Fig 17.5 · Raft · leader election and log replication | 2.5 px · cap 157 | todo |
| 210 | 5 | `fig-17-6` Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure | 2.5 px · cap 136 | todo |
| 211 | 5 | `fig-17-7` Fig 17.7 · CAP triangle · pick two when the network splits | 2.5 px · cap 143 | todo |
| 212 | 5 | `fig-17-8` Fig 17.8 · CAP in production · which database picked which corner | 2.2 px · cap 171 | todo |
| 213 | 5 | `fig-17-9` Fig 17.9 · Monolith vs microservices · same business logic, different deployment | 2.2 px · cap 137 | todo |
| 214 | 5 | `fig-17-10` Fig 17.10 · Service mesh and the sidecar · how microservices actually talk in 2026 | 2.2 px · cap 216 | todo |
| 215 | 5 | `fig-17-11` Fig 17.11 · The architectural pendulum · same problems, different costumes | 2.9 px · cap 129 | todo |
| 216 | 5 | `fig-18-1` Fig 18.1 · The full stack · sand to web service · math at every layer | 3.5 px · cap 154 | todo |
| 217 | 5 | `fig-18-trace` Fig 18.1.5 · The trace · what happens when you press Enter on google.com | 1.5 px · cap 190 | todo |
| 218 | 5 | `fig-18-2` Fig 18.2 · The civilization timeline · seven moments that made the rest possible | 2.9 px · cap 135 | todo |
| 219 | 5 | `fig-18-3` Fig 18.3 · Three things the next decade will change | 2.5 px · cap 168 | todo |
| 220 | 5 | `fig-18-4` Fig 18.4 · CS intersections · the disciplines that now run on the substrate | 2.2 px · cap 143 | todo |
| 221 | 5 | `fig-18-5` Fig 18.5 · The reading list · grouped by part of this book | 2.5 px · cap 160 | todo |
| 222 | 5 | `fig-18-6` Fig 18.6 · The closing zoom-out · the inverse of where <a href="part-1#ch1">Chapter 1</a> began | 2.2 px · cap 156 | todo |
