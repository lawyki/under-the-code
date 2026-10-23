# Pass 31 · takeaway check (2026-10-24)

The 187 takeaways (ledger column `intent`) after the split: every one at most 20 words and at most two numbers, each opening with its job. They were run through `tests/pass31/lib.mjs` `taughtYet` as it stands, with known-terms from `scripts/known-terms.mjs --out`. Takeaways that used a term the reader meets only later were reworded (trap before Fig BR.2, DNS and TLS at Fig 11.3, heap at Fig 3.5). The flags left are the checker's, not the wording's. They go to the gate builder's follow-up (`docs/todo.md`, Phase 0 repairs).

All-capitals abbreviations the prose teaches before the figure, flagged only for being in capitals (14 figures): CPU (Figs 1.8, BR.1, BR.3, BR.6, BR.8, 4.4, 4.21), ARM (3.2), AL, AX, EAX, RAX (3.3), SYSCALL (BR.2), VM (4.19), SQL (13.3), GPU (16.6), API (17.3).

Terms flagged as untaught although the prose teaches them first (the paragraph that first uses each, found by search):

| Figure | Token | Taught first in |
|---|---|---|
| 1.10 | mov eax | ch1-cpu-p5 |
| 1.10 | byte | ch1-cpu-p2 |
| 3.1 | register | ch1-vonneumann-p4 |
| 7.4, 7.5 | thread | ch7-gil-p1 |
| 8.4, 10.8 | bandwidth | ch8-shannon-p8 |
| 8.12 | TCP/IP | ch8-layers-p3 |
| 8.12 | OSI | ch8-layers-p2 |
| 12.1 | applet | ch12-browser-p2 |
| 12.3 | microtask | ch12-loop-p2 |
| 12.6 | thread | ch7-gil-p1 |

Everyday words missing from the checker's word list: inflections (lowest, became, rewritten) and plain nouns (database).
