# Review of the c50f7e1 freeze (section 17): NOT READY

The seven section-16 defects are fixed and tested; the freeze record is consistent. Not ready: two classes of true positives still pass (H1, H2; redis at fig-4-20 in the book now); defect 4 only partly fixed; 11 of the 31 newly failing tokens are false flags, and two new must-fail tests lock false flags in.

Trees used: the builder's book copy efc8b9dd (review17/bookcopy); a snapshot of figures-final's live public/; an export of 9b1cec0; the gate's own public/.

## 1. The seven defects: fixed

- fig:taught-test 135 of 135 on all four trees; fig:packet-test 14 of 14 on the copy, the live tree and the gate's tree.
- c50f7e1's 122 label cases against ef9b704's code: 91 hold, 31 fail, exactly section 17's additions (defect 1: 9, 2: 9, 3: 10, 4: 2, 5: 1).
- Defect 6: the exemption check fails on ef9b704's files and holds on c50f7e1.
- Old probes on the new code: nonpara (strict) 91 before, 0 after; cmp: 186 figures, failing 123 before, 128 after; 5 pass to fail (4.5, 8.6, 9.2, 9.5, 10.7); 31 tokens start failing at 24 figures; 1 stops (javascript at 5.11). leak: a form is credited while untaught only through names (17 forms) and 4 plain inflections; no prefix, HTTPS, held-only or packet-mention leak. CAS, CSS, HTTPS, IDS, IIS fail where only their base is taught.
- Two new must-fail cases lock in false flags: tests/pass31/taught.test.mjs:145 (SHA-256 at fig-18-6) and :160 (Diffie–Hellman at fig-11-11).

## 2. Holes: true positives that pass on c50f7e1 (all also pass on ef9b704)

- **H1 (high).** A stripped prefix still makes an everyday word when the remainder is not a glossary term. lib.mjs:183 (a remainder of 3 letters is enough), :206, :326-327, :336. Book: fig-4-20, token redis (4 texts), passes as re+dis; no non-held paragraph before the card writes it. At fig-1-1, subnet and unmap also pass. Fix: remainder at least 4 letters, and a dictionary or COMMON word as written, not through its stems. Test: redis at fig-4-20, subnet and unmap at fig-1-1 fail; upload, subsystem, unpaid, rewrite still pass.
- **H2 (high).** Possessive and plural forms escape the abbreviation rules. lib.mjs:317-319 (caps false when the token ends in a lower-case s or 's); :347 (the short-abbreviation branch needs letters only, so an apostrophe skips it); :336. At fig-1-1, RAM's, OS's and ARM's pass (brief section 15's own examples). DRAMs, DRAM's, FIFOs, FIFO's, BIOSs, NULLs and ENIACs pass while DRAM, FIFO, BIOS, NULL and ENIAC fail. No current label affected (375 capitals x 5 forms x 186 figures probed). Fix: strip a trailing s, es, 's or ’s before the caps test and the short-abbreviation test, and judge the stem as the abbreviation. Test: these forms fail at fig-1-1; RAM's and OS's pass at fig-3-5.
- **H3 (low).** known-terms.mjs:287-298 lists Ethernet as a name, so a mention credits it at Figs 8.2 to 8.7, before ch8-ethernet-p1 teaches it. No current label.
- **H4 (low).** lib.mjs:274: the orig + 's' check lets loss credit the token los from fig-4-13. Fix: skip it when orig already ends in s.
- **H5 (low).** lib.mjs:96-108 reads p.part-tagline, so part-2's end-of-part teaser credits Baran, Cerf, Kahn, Berners-Lee and Eich from fig-8-1. No current label.
- Checked clean: multi-word terms split across <text> elements 0; tokens credited only by a <code> operand: 1 figure (6.7: unique_ptr, weak_ptr), correct; credit from a place that is not a paragraph or list item: 0.

## 3. Over-strictness

5 figures pass to fail: 9.2 is a false flag (oct); 4.5, 8.6, 9.5, 10.7 true positives by the rules.

31 newly failing tokens: 20 true positives, 11 false flags.

True positives (20): EAX/eax (5: fig-1-10 x2, fig-3-2, fig-3-3 x2); written before the card only in table cells (8: HDD 1.15, RDX 3.4, RCX 3.4, rbx BR.1, RCX BR.2, FCFS, SJF and MLFQ 4.5), true only by the paragraph rule, and calibration 17.1's reason "listed there, not explained" is factually wrong for the ch1-memory, ch3-registers and ch4-scheduling tables, which expand or define each one; truncations (4: manch 8.6, eth 8.11, comp and crypto 18.5); by rule (3: ID 9.5 under the short-abbreviation rule, its first paragraph ch11-dns-p7; reno 10.7, named only inside a list in ch10-modern-p1, taught nowhere; promises 12.2).

False flags (11):

| Token | Figures | Where it is taught / why it fails | Fix |
|---|---|---|---|
| diffie hellman | 11.11, 11.13, 14.1 | Taught at ch11-crypto-p7 (between 11.9 and 11.10). The glossary places it at ch14-publickey. known-terms.mjs:107-113 misses the gloss because a parenthesised year sits between the term and ", which" (the parenthesis cue needs a letter). | Skip a leading parenthesised number before testing the cues. Test: passes from 11.10, fails at 11.9. Correct taught.test.mjs:160. |
| sha 256 | 14.2, 14.13 | Taught at ch11-crypto-p4 (between 11.8 and 11.9). Its glossary section ch14-hashing is stripped, so it is listed held-only (known-terms.mjs:186) and lands in noMention (lib.mjs:229). No cue matches a sentence-initial "TERM is" definition. | Add a definitional-sentence cue, with plain-use regressions (safety, release, group still fail). Test: passes from 11.9, fails at 11.8. Drop SHA-256 from taught.test.mjs:145. |
| oct; aug, apr | 9.2; 11.1 | Month abbreviations. mar passes only because it is a dictionary word. | Add month abbreviations to common-words.txt. |
| ch | 18-trace | Chapter abbreviation. | COMMON list. |
| ERROR | 4.16 | The label is grep ^ERROR. ERROR alone passes (on COMMON); the caret is kept by lib.mjs:92-93 and tested unstripped at :340, and the failure is reported as an abbreviation. | Test the letters-only form at :340. |
| etcd | 17.8 | Moderate confidence. ch17-consensus-p1 (between 17.4 and 17.5) introduces it with an apposition; known-terms has it as taught nowhere. | A cue for ", TERM," after a noun phrase. |

Fig 4.19, "virtual machine": a false flag; the case is right and the rule is wrong. ch4-security-p6, in the figure's own section and before the card, defines it ("A virtual machine imitates an entire computer, kernel and all"); the glossary assigns the entry to ch17-virt, where it is placed; no key-term span; no cue in known-terms.mjs:107-114 matches a definitional clause; it already failed on ef9b704. Same figure, VM: also a false flag: ch4-security-p6 writes the plural; CAPS (known-terms.mjs:255) does not match a capitals run followed by s, so VM is placed at ch4-security-p11, after the card; a label VMs would pass, which is inconsistent. Fix: let CAPS take an optional trailing s and record the singular.

The same placement class causes false flags elsewhere: page fault BR.3, BR.4 (taught at ch1-memory-p10); page table BR.4, BR.5 (ch1-memory-p9); mutex 6.5 (ch4-ipc-p12); control plane 17.3, 17.10 (ch17-k8s-p1); JSON never placed, because it is written only in a chapter lead (known-terms.mjs:265); lower-case json passes from 12.1.

Brief deviation: held-strip.json sections.held_only strips 5 sections the brief does not hold: ch9-security, ch10-attacks, ch12-security, ch13-injection, ch14-hashing. 44 of the 97 held-only glossary entries sit in them.

## 4. Exemptions, prompts, frozen-file check

- No per-figure exemption for taught-yet: PASS. prompts.mjs byte-identical: PASS (781262c1...). Frozen-file check in gate.mjs:92-94, dev.mjs:37-39, validate.mjs:33-35: PASS, no bypass flag; gate.mjs:135 cross-checks each run's fingerprint.
- Gaps: (a) check.mjs has no frozen-file check (:33-57), though it is hashed and a clean fig:check is part of the gate's pass; figures-final has its own older, unfrozen check.mjs (a53d8115), lib.mjs (170d6eaa) and known-terms.mjs (df5a945e) that run with no refusal. Fix: the same refusal as gate.mjs:92-94. (b) gate.mjs:73 refuses --criteria with --author only when --single is absent; with --single --author --criteria the author's output line (gate.mjs:83) carries no partial marker. Fix: refuse unless the run comes from the decision loop, or print the partial marker. (c) (low) Three unhashed inputs can change verdicts: /usr/share/dict/words (lib.mjs:162-163); docs/pass-30-exceptions.json, per-figure Gate 1 skips (check.mjs:118-125, figs.mjs:42-44, clip.mjs:27); scripts/figs/build_into.py (validate.mjs:72, dev.mjs:121).

## 5. Freeze record: consistent

summary.json agrees with the record (27 decisions; complete runs v1 0/6, v2 0/6, v4 6/6, Enigma 6/8, each decoy 0/6; 56 runs, 1,213 tester calls); all 83 verdicts carry 327aba6a; run stamps 08:30:03Z to 08:40:03Z, after e563dc5 and 9d74d95; section 17.3's 27 rows match with 0 mismatches; ledger copy dd6e94fa, its 35 held rows match held-strip.json; the void attempt kept separately in try26-review-void and not counted; fingerprint reproduces from a clean archive; all 16 file hashes and 7 prompt hashes as in 17.4; the dev set's packets and taught-yet results identical under ef9b704 and c50f7e1 code in all 9 trees; the 5 exemplar check outputs match 17.5.

## Required before READY

1. Fix H1 and H2, with tests.
2. Fix the 11 false flags in the checker, or log a reason for keeping each one. Correct taught.test.mjs:145 and :160.
3. Add the frozen-file check to check.mjs, and close the --single partial-verdict gap.
4. Re-freeze with a new fingerprint and rerun the development set.

Probe scripts in this folder: oldcases.mjs, cmp2.mjs, ctx.mjs, leak2.mjs, abbrleak.mjs, codeop.mjs, mentioned.mjs, routes.mjs, split.mjs, devtt.mjs, nonpara-new.mjs, nonpara-old.mjs, instr/.
