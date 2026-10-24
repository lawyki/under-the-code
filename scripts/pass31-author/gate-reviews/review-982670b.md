NOT READY

**REPORT-2.md was not written.** The harness blocked writing a report file from this subagent, so the full report is below. Save it to `/private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/scratchpad/review18/REPORT-2.md` if it needs to be there.

# Review of the 982670b freeze (section 19, combined d3513427...)

The freeze reproduces and its record is consistent. A to H are fixed and tested. Every item of review17's "Required before READY", and every H and false-flag row, is fixed with tests that fail on c50f7e1's code. Not ready because of one high finding (D1): glossary and key-term abbreviations are still credited by a plain mention that comes before their teaching point. This passes 19 untaught tokens at 12 current non-held figures. There is also one medium hole (D2) and eight low findings.

Rules: I did not open or read 93aae05 or docs/pass-31-sealed/. Every probe read held-stripped HTML (`lib.mjs heldStripped`). Every sentence quoted below comes from a non-held paragraph. Nothing was written into figures-final, the main checkout or the gate worktree.

Trees and code used:
- Clean exports of 982670b, 1984b89 and c50f7e1, in r2/frozen, r2/b1984 and r2/c50.
- A byte copy of figures-final/public, tree c8f8fd5e, the same tree as section 19.5, in r2/live.
- The builder's copies 2c6c6109 and 78c5584a, review17's efc8b9dd, and the gate's own public/ (1bc591c9).

## 1. Earlier items: fixed, with tests

**Tests on the frozen code**
- `fig:taught-test`: 284 of 284 cases hold on every tree:
  - the gate's public/
  - c8f8fd5e
  - 2c6c6109
  - 78c5584a
  - efc8b9dd
- `fig:packet-test --ledger`: 17 of 17 on the gate tree, c8f8fd5e, 2c6c6109 and efc8b9dd.
- `fig:frozen-test`: 25 of 25.

**The new tests on old code**
- `taught.test.mjs` on c50f7e1's code: 95 of 284 cases fail. On 1984b89's code: 36 fail. Both match section 19.1.
- The cases that fail on c50f7e1 include every review17 row:
  - H1: redis at fig-4-20, subnet and unmap at fig-1-1.
  - H2: RAM's, OS's, ARM's, DRAMs, DRAM's, FIFOs, FIFO's, BIOSs, NULLs, ENIACs, ram's, os's and Mac's at fig-1-1.
  - H3: Ethernet at fig-8-2 and fig-8-7.
  - H4: los at fig-4-13.
  - H5: Baran, Cerf, Kahn, Berners-Lee and Eich at fig-8-1.
  - The 11 false flags:
    - diffie hellman at fig-11-10, 11-11, 11-13 and 14-1
    - sha 256 at fig-11-9, 14-2, 14-13 and 18-6
    - oct, aug, apr and ch
    - ERROR at fig-4-16
    - etcd at fig-17-5 and 17-8
    - virtual machine and VM at fig-4-19
  - The placement class:
    - page fault and page table at fig-2-1, BR.3, BR.4 and BR.5
    - mutex at fig-4-18 and 6-5
    - control plane at fig-17-3 and 17-10
    - JSON at fig-11-15 and 12-1
  - The table-row tokens: HDD, RDX, RCX, rbx, FCFS, SJF, MLFQ and FIFO.
- The old must-fail rows have become must-pass: SHA-256 at fig-18-6 and Diffie–Hellman at fig-11-11.
- `frozen.test.mjs` on 1984b89's code: 10 of 25 checks fail, with lib.mjs's missing `exemptProblems` export stubbed. The failing checks are the gate1-off marks, single on the author's line, the `--single --author` refusal, and 7 exempt checks. On c50f7e1's code the suite stops before it finishes, and c50f7e1's check.mjs has no `--expect-hash` at all.

**Defects A to H, as section 19.1 says**
- **A:** the pointer, never-by-mention and part-number rules. Of the abbreviations placed by a plain writing in a sentence that the whole-sentence POINTS matches, I read all 9:
  - MEM, `ch1-cpu-p7`
  - RSP, `ch3-registers-p2`
  - AMD64, `ch3-call-p2`
  - SIGSEGV, `ch4-vm-p12`
  - DSL, `ch8-encoding-p6`
  - GET, `ch10-modern-p6`
  - ES2015, `ch12-loop-p4`
  - DH, `ch14-publickey-p6`
  - CAP, `ch17-cap-p1`

  I agree with the builder on each of them.
- **B, C, E, F, G and H:** verified by test and by reading the code.
- **D:** `--single --author` exits 2.

## 2. Defects

### D1 (high): a plain mention places glossary and key-term abbreviations before their teaching point

- **Where:** `scripts/known-terms.mjs:459-460`. A plain writing (`by: 'writing'`) places every abbreviation that is not restricted. `tests/pass31/lib.mjs:266-267` then adds that placement to `known`, ahead of the term's glossary or key-term teaching point.
- **Placing writings on c8f8fd5e.** I read every one of them, and none glosses its term:

  | Token | Placed at | The writing | Taught at |
  |---|---|---|---|
  | TLS | `ch2-float-p12` | "from a Python list to a TLS handshake to a neural network" | `ch11-tls-p1`, key-term |
  | TCP, UDP | `ch4-ipc-p14` | "using TCP or UDP" | `ch10-why-p1`, key-term; `ch10-udp-p1` |
  | HTTP | `ch7-types-p3` | "an HTTP response" | `ch10-modern-p6` |
  | IP | `ch8-ethernet-p8` | "subsequent packets to that IP" | `ch9-ip-p1` |
  | DNS | `ch10-hero-lead` | "For voice and DNS that's fine." | `ch11-dns-p1`, key-term |
  | RSA | `ch11-crypto-p2` | "a 2048-bit RSA key" | `ch14-publickey-p4`, key-term |

  The IP writing is the sentence right after "IP addresses, which we'll meet in Chapter 9", which the pointer rule skipped. The pointer test is per sentence, so the next mention places IP anyway.
- **Effect.** A plain writing never places an abbreviation that is a glossary or key-term entry. Glosses still place.

  Measured on c8f8fd5e with that rule:
  - 19 tokens start failing at 12 non-held figures:
    - fig-8-9 ip
    - fig-8-11 tls, tcp, ip
    - fig-8-12 tcp, ip, http, udp
    - fig-9-2 tcp, ip
    - fig-9-4 tcp
    - fig-10-1 dns
    - fig-10-9 tls
    - fig-11-3 dns, tls
    - fig-11-8 rsa
    - fig-11-10 tls
    - fig-11-13 rsa
    - fig-14-1 rsa
  - Failing figures go from 124 to 126 and failing tokens from 465 to 484.
  - No token stops failing.
  - Figs 1.1 and 1.2, the development set, are unaffected.
- **Why high:**
  - Brief section 15 says abbreviations "the prose teaches (CPU, RAM, TCP, IP, HTTP, DNS) are listed at the paragraph that teaches them".
  - The frozen gate's own section 18 rule credits a key-term-marked name only where it is taught. Under that rule JavaScript fails at fig-5-11: before the card it is written only in a list at `ch2-float` and in a pointer sentence at `ch4-security-p16`. TLS, TCP, DNS and RSA are key-term-marked too, yet the abbreviation route credits them by mention.
  - The previous review left the first-writing limit for session e2 or the owner, naming only TCP and UDP at fig-8-12, DNS and HTTP. New here: TLS (credited for 102 figures from a Part I aside), IP right after a pointer sentence, RSA, the inconsistency with the key-term rule, and the 12-figure count.
- **Fix:** in known-terms, let a plain writing place only an abbreviation that is no glossary or key-term entry (`terms.has(norm(t))` false). An entry is placed at its teaching point, or at a writing that glosses it (`abbrCue`). Tests: each of the 19 tokens fails at its figure above and passes at the first figure after its teaching paragraph. Re-freeze and rerun the development set. If the owner keeps the limit instead, brief section 15's wording must change and READY must list it.

### D2 (medium): multi-word glossary terms escape in -ed, -ing and -ly forms

- **Where:** `tests/pass31/lib.mjs:328` and `:330` accept only `(s|es)?` after a multi-word term. The file's own rule (lines 140 to 145) says "not a glossary term (single or multi-word, in any inflection)".
- **Evidence:**
  - At fig-1-1, these pass while "page fault" fails: "page faulting", "hard-linked", "buffer overflowing", "system calling", "virtual addressing".
  - At fig-4-11, "hard-linked" and "hard linking" pass while "hard link" fails. It is taught at `ch4-fs-p4`, after that card.
  - c50f7e1's code behaves the same.
  - None of the 186 non-held figures' labels has such a form today.
- **Fix:** let the last word of a multi-word term take the plain endings `stems()` strips (s, es, d, ed, ing, er, ers, ly), in both the match and the removal. Tests: those forms at fig-1-1 and fig-4-11 must fail, and pass after their teaching paragraphs.

### D3 (low): author-form options that change what is judged reach the author unmarked

- **Where:** `tests/pass31/gate.mjs:168-177` and `:96-97`.
- **`--rc2-tree` and `--rc2-rev`:** either one sets the pairwise baseline with no mark on the author's line, and verdict.json does not record the source. I ran `--rc2-tree=<the candidate's own tree>` at fig-1-5: pairwise passed as SAME, with no tester call.
- **`--intent`, `--intent-file` and `--job`:** these override the ledger's takeaway in the author's form. Only verdict.json records it (`intent_source`).
- **Fix:** refuse these options with `--author`, since Phase 2 judges against the ledger and v1.0-rc2. Alternatively, print `rc2` and `intent_source` on every output line and record the rc2 source in verdict.json. Add tests to frozen.test.

### D4 (low): the naming cue's list guard

- **Where:** `scripts/known-terms.mjs:197` checks only that the clause before has four words or more. A list whose items are that long therefore reads as naming.
- **Evidence:** CDN is placed at `ch11-dns-p3` by naming ("a hosting company, a corporate IT department, a CDN."). No teaching point moves today: CDN would be placed by its plain writing anyway, and no glossary term is placed this way.
- **Fix:** reject the cue when the clause before itself opens after ", a|an|the", which is a list, as LIST does. Add a synthetic test with four-word list items.

### D5 (low): unhashed inputs that change verdicts

- **The gate's public/ (1bc591c9):**
  - Validation judges items without a rev on it (`tests/pass31/validate.mjs:62`).
  - Every development and validation tree is copied from it (`dev.mjs:102`, `:115`; `validate.mjs:66`), and so is the default rc2 tree (`gate.mjs:174`).
  - It is not in the fingerprint, and no verdict records a hash of the tree.
- **Cached trees:** `dev.mjs:114` and `validate.mjs:65` reuse them, so the hashed `build_into.py` need not be what built them. The v1, v2 and v4 trees date from 2026-10-23T23:07Z. That is after the last change to `build_into.py` and public/, so today they agree with their inputs.
- **`scripts/check-dashes.mjs`:** used by `check.mjs:162` when the gate's own tree is the one checked.
- **Fix:** hash public/ (or record a tree hash in every verdict and in reads.log), rebuild or hash cached trees, and hash check-dashes.mjs.

### D6 (low): case forms of abbreviations of four letters or more

- **The mention route:** read_file passes by mention through the section 16 rule (`lib.mjs:400`) at 154 figures where READ_FILE fails, because READ_FILE's only writing, at `chBridge-trap-p1`, is a pointer sentence. That route bypasses rule A.
- **Dictionary forms:** where their capitals fail, these pass as everyday words (`lib.mjs:396`): dram, fifo, bios, eniac, null and grub. That is by the brief's letter, which limits the short-abbreviation rule to three letters or fewer.
- **Labels:** no current label is affected.
- **Fix:** judge a token whose capitals form is in known-terms' `capitals` as that abbreviation, in any case, unless the token is COMMON or the prose writes it in that very case. As a minimum, apply this to the mention route.

### D7 (low, by the brief's letter): prefix compounds that are technical terms

- **Where:** `lib.mjs:193` and `:216`.
- **Evidence:** at fig-1-1 these pass through the prefix rule only: prefetch, prefetching, preemption, subnetting, subnetted, overcommit, reboot, subshell, unpickle, unmarshal. In each, what remains is a dictionary word. preemptive, a glossary term, fails.
- **Fix:** none in the checker without contradicting brief section 15 (upload). Rely on the logged newcomer read, and list this class for session e2 or the owner.

### D8 (low): mechanism entries credited as names by a mention

- **Where:** the name rule in `scripts/known-terms.mjs` (`isName`) lists Paxos, AddRoundKey and NaN as names. None is key-term-marked, so a mention credits them:
  - Paxos is mentioned in the `ch17-consensus` lead and taught at `ch17-consensus-p1`.
  - AddRoundKey is listed at `ch14-symmetric-p1` and taught at `ch14-symmetric-p2`.
- No current label falls in those windows. This is the same class as H3.
- **Fix:** exclude an entry whose glossary section teaches it as a method or step, or require a key-term or glossary teaching point for every name that is not a person or place.

### D9 (low): an environment variable lifts the author-form refusals

- **Where:** `gate.mjs:77`.
- **Evidence:** with `P31_GATE_DECISION_RUN=1` set, `--single --author --criteria=taught` ran (exit 0). The marks are still printed (`partial`, `single`), so no unmarked verdict results.
- **Fix:** have each decision pass its runs a per-decision nonce in place of the constant.

### D10 (low, logged in section 19.6): at_bar is free data

- **Where:** `check.mjs:64` and `lib.mjs:504`. Any figure id listed in at_bar is exempt from the label cap, with no evidence. The line prints "(exempt: cap)".
- **Fix:** accept an at_bar id only with a passing decision verdict under the frozen fingerprint for that figure's current svg hash.

### I (low, open, author side): figures-final's own fig:check is unfrozen

- figures-final's own fig:check runs `check.mjs` a53d8115, `lib.mjs` 170d6eaa and `known-terms.mjs` df5a945e, and it has no refusal.
- Brief section 15 says this copy is replaced when the frozen gate is brought over. Until then, the mechanical check in force is the gate worktree's, run with `--tree` and `--expect-hash`.

## 3. Over-strictness: tokens that newly fail

On c8f8fd5e, c50f7e1's code against the frozen code, I reproduced section 19.5 exactly:
- Failing figures go from 128 to 124, and failing tokens from 500 to 465.
- 4 tokens start failing and 39 stop.
- Against 1984b89's code: 124 to 124 figures, 472 to 465 tokens. 2 start (dns, CA) and 9 stop.

The 4 tokens that start failing are all true positives (0 false flags):

| Figure | Token | Where it is written and taught |
|---|---|---|
| fig-4-20 | redis | First written at `ch13-indexes-p3`, after the card. |
| fig-5-11 | javascript | Before the card, only in a list at `ch2-float` and in a pointer sentence at `ch4-security-p16`. Taught at `ch11-modern-p1`; a key-term-marked name. |
| fig-8-12 | dns | Before the card, only in the Part III teaser at `ch4-ipc-p15`. Taught at `ch11-dns-p1`. |
| fig-14-12 | CA | Never expanded outside held material. Its non-held writings at `ch14-tls-pqc-p3` and `p4` are plain. "Certificate authority" is taught in words at `ch11-tls-p4`, so the label can say that. |

Placements the 39 stops depend on:
- ID at fig-9-5 now passes from `ch4-security-p8` ("process IDs (…)", the parenthesis cue). Section 18 added the plural to CAPS; a plain writing would place it there anyway.
- C++ is placed at `ch5-survives-p1` by the possessive apposition, which is a gloss.

## 4. Exemptions, prompts, frozen-file check

- **No per-figure exemption for taught-yet: PASS.** The only figure ids in the judging code are KEPT_ORIGINALS (`lib.mjs:496`), the 18 kept originals. common-words.txt adds only the month abbreviations and "ch".
- **prompts.mjs: PASS.** It is byte-identical, 781262c1, at 355c41f, c50f7e1, 1984b89, 8a8f784 and 982670b. All 7 prompt hashes match section 14.7.
- **Frozen-file check: PASS.** It sits at `gate.mjs:108`, `dev.mjs:39`, `validate.mjs:35` and `check.mjs:49`. Each runs before anything is judged, refuses a missing or wrong hash with exit 2, and has no bypass flag. Each single run checks its fingerprint again, and the decision cross-checks the runs at `gate.mjs:149`. No module that the hashed files import is left unhashed.
- **Partial verdicts:** marked on every author line for `--criteria`, `--single`, `--no-pairwise` and `--gate1` quick or off. D3's options are the exception.
- **Unhashed inputs:** D5.

## 5. Freeze record: consistent

- **Fingerprint:** it reproduces from a clean export of 982670b: combined `d3513427330802364831f85ee336653913b3e78fe0df9979844a543637c1f3eb`. All 20 file hashes match table 19.4.
  - 4 files changed since 1984b89: gate.mjs, lib.mjs, known-terms.mjs, check.mjs.
  - 16 are byte-identical.
  - The unhashed files are as recorded: dev.mjs 857a1372, taught.test.mjs 21ed7fa6, packet.test.mjs a4c89c1a, frozen.test.mjs 0cdfdeaa, sheet.mjs 7d35e20b, exempt.json 7a78bd18.
- **C:** both rows of section 18.4 are corrected and marked. places.mjs is 198a4b32 and taught.test.mjs is ffa8095f; I checked both against 1984b89's own files.
- **Development set run** (`summary.json` and the run folders):
  - 27 evaluations, 54 runs, 1,167 tester calls, 0 errors.
  - Every evaluation and every run carries d3513427.
  - Run stamps are 12:01:04Z to 12:10:56Z. That is after 8a8f784 (12:00:36Z) and before 982670b (12:40:48Z).
  - All 27 rows of table 19.3 match the outputs, including the hedge and pairwise columns. Every decision follows the 2-of-3 rule.
  - Criteria failed per item match section 19.3, and runs per item match the summary.
  - The ledger copy is d863dab9, with 223 rows, 35 of them held.
- **The 9 development trees:** packets and taught-yet results are identical under 1984b89's code and the frozen code.
- **Branch:** 982670b is pushed.
- **Commit messages:** they follow the reporting rule.
- **Exemplars:** I reran the frozen fig:check on c8f8fd5e with gate1 full and `--expect-hash`.
  - fig-1-5, fig-4-8, fig-10-3, fig-13-6 and fig-17-6 all PASS; 0 of 40 figure checks failed.
  - Labels per panel are 6 and 4; 8; 8 and 8; 5 and 8; 4 and 5, as in section 19.5.
  - Gate 1 is 120 rows clean on each.
  - Part-5 `gate1:smooth` had 1 finding, the load-dependent result section 19.5 logs.
  - The anchors check failed only because my export is no git repository. It is not a gate finding.

## Required before READY

1. Fix D1 in known-terms, with the 19 regression tests. Or record the owner's decision to keep the first-writing limit and amend brief section 15.
2. Fix D2, with tests.
3. Fix or log D3 to D10. D3 and D5 are the gate-integrity ones.
4. Re-freeze with a new fingerprint and rerun the development set.

Probe scripts are in `/private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/scratchpad/review18/r2/probes/`:
- why.mjs
- caseforms.mjs
- glossforms.mjs
- multiinfl.mjs
- window.mjs
- cmpkt.mjs
- fails.mjs
- diff.mjs
- where.mjs
- one.mjs
- navli.mjs
- devtt.mjs
- record.mjs
- table.mjs

The instrumented copies are in `/private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/scratchpad/review18/r2/instr/`. The D1 ablation is `ABL_GLOSS=1`, and the per-writing log is `KTLOG`.