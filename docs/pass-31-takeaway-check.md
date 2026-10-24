# Pass 31 · takeaway check (2026-10-24, rerun after repair round 2)

The 186 takeaways (ledger column `intent`; held rows and Fig 13.6, merged into Fig 13.5, have none to check) after repair round 2: every one at most 20 words and at most two numbers, each opening with its job. They were run through `taughtYet` from `tests/pass31/lib.mjs` **as frozen at `dd51d25`** (blob `e444aa1`), with known-terms from `node scripts/known-terms.mjs --out=<scratch>` on `figures-final` (116 sections, 488 terms). The run is the checker's full output, not a hand search; the runner is a dozen lines that call `knownTerms`, `taughtBefore`, `packet` and `taughtYet` for each figure. Result: 8 figures flagged with lowercase tokens, 15 with all-capitals tokens only. Each flag was then looked up in the prose before its figure (paragraphs only, captions and cards excluded). Every one is taught there, so the flags are the checker's, not the wording's. They go to the gate builder's follow-up (`docs/todo.md`, Phase 0 repairs).

Corrections to the first version of this file (session e2's second verification): AL and AX (Fig 3.3) and API (Fig 17.3) were wrongly listed as taught; they are not, so both takeaways were reworded without them. Figs 1.6 (log scale), 1.14 (Ring 0, Ring 3, system call) and 10.8 were reworded so that no term is first taught in the figure's own caption.

All-capitals tokens, each taught before the figure:

| Token | Figures | Taught first in |
|---|---|---|
| CPU | 1.8, 3.1, BR.1, BR.3, BR.6, BR.8, 4.4, 4.21 | ch1-vonneumann-p3 |
| ARM | 3.2 | ch1-cpu-p4 |
| EAX | 3.3 | ch1-cpu-p5 (mov eax, 5) |
| RAX | 3.3 | ch3-registers-p2 |
| RIP | 3.6 | ch3-registers-p2 |
| SYSCALL | BR.2 | chBridge-trap-p2 |
| VM | 4.19 | ch4-security (the paragraph before the card: "lightweight VMs", "a virtual machine") |
| DB2, SQL (Server) | 13.1 | ch13-codd-p6 |
| GPU | 16.6 | ch16-gpu-p1 |

Lowercase tokens flagged although the prose teaches them first:

| Figure | Token | Why the checker flags it | Taught first in |
|---|---|---|---|
| 1.10 | mov, eax | not on its word list | ch1-cpu-p5 |
| 1.10 | bytes | inflection | ch1-cpu-p2 (byte) |
| 1.10 | register | glossary term known-terms does not list | ch1-vonneumann-p4 |
| 7.4, 7.5, 12.6 | thread | glossary term known-terms does not list | ch7-gil-p1 |
| 8.4 | bandwidth | not on its word list | ch8-shannon-p8 |
| 8.12 | TCP, IP's, OSI's | possessives; known-terms gap | ch8-layers-p2 (OSI), p3 (TCP/IP) |
| 12.1 | applet | not on its word list | ch12-browser-p2 |
| 12.3 | microtask | not on its word list | ch12-loop-p2 |

Reworded in this rerun because the flag was real: Fig 6.9 (C++23 is taught nowhere before the figure), Fig 9.2 ("began", an irregular form the checker cannot reduce) and Fig 18.6 ("Chapter 1's", notation).

## Exemplar drafts (2026-10-24)

`fig:check` on the five Phase 1 drafts: Figs 1.5, 13.5 and 17.6 pass every check. Figs 4.8 and 10.3 fail taught-yet on all-capitals tokens only, each taught before the figure: CR3 (chBridge-mode-p4) and TCP's state names SYN_SENT, SYN_RCVD, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, LAST_ACK, TIME_WAIT and the segment SYN-ACK (ch10-handshake-p1 and p3).
