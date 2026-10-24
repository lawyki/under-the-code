# Pass 31 · takeaway check (2026-10-24, rerun for repair round 4)

The 186 takeaways (ledger column `intent`; held rows and Fig 13.5, merged into Fig 13.6, have none) after repair round 4: every one at most 20 words counting its job words, at most two numbers, each opening with its job.

**The checker in force** is the gate's taught-yet as frozen at `43ff49c` (fingerprint `4095d1aa`): `tests/pass31/lib.mjs` (blob `e7190db`), `tests/pass31/common-words.txt` and `scripts/known-terms.mjs`, run on a scratch copy against `figures-final`'s `public/` (known-terms with `--public`: 116 sections, 488 terms, 371 abbreviations at their first prose paragraph). The runner calls `knownTerms`, `taughtBefore`, `packet` and `taughtYet` per figure. Lowercase words pass on the common-word list or the dictionary, except tokens of three letters or fewer whose capital form is an abbreviation (brief section 15). A second gate follow-up (code only) is fixing the checker gaps below in the checker itself; this file is rerun on its freeze.

Result: 12 figures flagged, no all-capitals flag. Every flag was looked up in the prose before its card (paragraphs only, never captions or cards).

| Figure | Token | Why the checker flags it | In fact | Fix |
|---|---|---|---|---|
| 1.10 | mov, bytes, register | mov written lowercase; byte and register placed later by known-terms | mov eax: ch1-cpu-p5; byte: ch1-cpu-p2; register: ch1-vonneumann-p4 | checker (follow-up 2) |
| 3.4 | compilers | glossary first-use placed later | ch1-vonneumann-p3 | checker |
| 4.19, 4.20, 4.21 | virtual machine, container | taught earlier in the same section | ch4-security-p6 | checker |
| 5.3 | pointer, int | taught earlier in the same section | ch5-bell-labs-p5, ch5-portability-p7 | checker |
| 7.4, 7.5, 12.6 | thread | glossary first-use placed later | ch7-gil-p1 | checker |
| 9.9 | groups | everyday word matching a glossary term | plain sense: the card writes the address in groups of hex digits | newcomer read: stays |
| 12.1 | applet | not a glossary term, met in prose before the card | ch12-browser-p2 | checker |
| 12.3 | microtask | same | ch12-loop-p2 | checker |

## Newcomer reads

A newcomer read asks whether a plain word in a takeaway carries a technical sense the prose has not taught by then. Round 4's pre-commit check (`wf_ae34022e-546`, read-only Sonnet reviewers with two skeptics per finding) read every changed takeaway; its confirmed and split findings were reworded: 2.3 ("symbol", a word first met in the caption, now "gate"), 5.11 ("braces"), 16.10 ("link"), 13.6 ("redoes", "undoes", now p4's "replays" and "rolls back"), 8.4 (a "limit" read as a ceiling), 11.1 (a cause the prose before the card does not give). Earlier rounds reworded 13.4 ("bucket", "keys"), 8.10 ("port"), 8.5 and 8.6 ("edge", now "transition"), 4.4 ("node"), 9.4 ("time to live", then "counts it down"), 17.1 ("sensitive") and 17.3 ("desired state", "watchers"). Kept with their plain sense: 9.9 "groups"; 2.8 "wrap" and "wheel" (the card draws the wheel; knows gives a clock face).

## Exemplar drafts (2026-10-24)

The first run used the older `fig:check` on `figures-final`: Figs 1.5, 13.5 (now 13.6) and 17.6 passed every check; Figs 4.8 and 10.3 failed taught-yet on all-capitals tokens the prose teaches before them (CR3, chBridge-mode-p4 and chBridge-mmu-p4; TCP's state names and SYN-ACK, ch10-handshake-p1 and p3). That checker no longer decides. The frozen gate's mechanical checks on the five drafts are run by the second gate follow-up and recorded here on its freeze. Figs 10.3 and 17.6 had three panels each, which the two-panel cap fails; both were regrouped into two panels on 2026-10-24 (no label renamed or reboxed), and Fig 13.6's stamps now use p4's words.
