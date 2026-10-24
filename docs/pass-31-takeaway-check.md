# Pass 31 · takeaway check (2026-10-24, rerun after repair round 3)

The 186 takeaways (ledger column `intent`; held rows and Fig 13.6, merged into Fig 13.5, have none) after repair round 3: every one at most 20 words counting its opening job words, at most two numbers, each opening with its job.

**The checker in force** is the gate's frozen taught-yet: `tests/pass31/lib.mjs` with `tests/pass31/common-words.txt` and `scripts/known-terms.mjs` as on `figures-final-gate` at the freeze commit `355c41f` (blobs `6d8b3ff`, `98aa9dc` and `97d99d2`, unchanged since `fd4c94e`). It was run on a scratch copy of those three files against `figures-final`'s `public/` (known-terms with `--public`: 116 sections, 488 terms, 371 abbreviations at their first prose paragraph). The runner calls `knownTerms`, `taughtBefore`, `packet` and `taughtYet` for each figure; its full output is below. The older copy of `lib.mjs` on `figures-final` (the dictionary rule) no longer decides anything.

Result: 14 figures flagged, no all-capitals flag. Each was looked up in the prose before its card (paragraphs only, captions and cards excluded). Every flag is the checker's, not the wording's: the term is taught before the card, or it is an everyday word that matches a glossary term by spelling. They go to the gate track as known false flags; no takeaway was reworded to dodge one.

| Figure | Token | Why the checker flags it | In fact |
|---|---|---|---|
| 1.10 | mov, bytes, register | known-terms places byte and register later | mov eax: ch1-cpu-p5; byte: ch1-cpu-p2; register: ch1-vonneumann-p4 |
| 3.4 | compilers | glossary first-use placed later | ch1-vonneumann-p3 |
| 4.19 | virtual machine, container's | taught earlier in the same section, which known-terms does not credit | ch4-security-p6 |
| 4.20 | container's | same | ch4-security-p6 |
| 4.21 | group's | everyday word matching a glossary term | everyday |
| 6.5 | releases | everyday word matching a glossary term (memory ordering) | everyday |
| 7.4, 7.5, 12.6 | thread | glossary first-use placed later | ch7-gil-p1 |
| 8.3 | toss | everyday word matching a glossary term | everyday |
| 8.4 | bandwidth | not on the word list | ch8-shannon-p8 |
| 9.9 | groups | everyday word matching a glossary term | everyday |
| 12.1 | applet | not on the word list | ch12-browser-p2 |
| 12.3 | microtask | not on the word list | ch12-loop-p2 |

Reworded in round 3 because a flag or a review was right: 5.3 ("pointers", first taught after the card), 4.19 ("VM" spelled out), BR.6 ("timer interrupts" read as the glossary term), 9.4 ("time to live"), 9.7 ("Tier 1s"), 17.1 ("sensitive"), 17.3 ("desired state", "watchers"), 6.4 ("call site"), 7.9 ("toll"); and, from round 2, 3.3 (AL, AX), 17.3 (API), 1.6, 1.14 and 10.8, all terms first met in the figure's own caption.

## Exemplar drafts (2026-10-24)

`fig:check` on the five Phase 1 drafts: Figs 1.5, 13.5 and 17.6 pass every check. Figs 4.8 and 10.3 fail taught-yet on all-capitals tokens only, each taught before the figure: CR3 (chBridge-mode-p4) and TCP's state names SYN_SENT, SYN_RCVD, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, LAST_ACK, TIME_WAIT and the segment SYN-ACK (ch10-handshake-p1 and p3).
