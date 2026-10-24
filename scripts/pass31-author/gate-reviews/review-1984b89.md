NOT READY

The harness refused the write to /private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/scratchpad/review18/REPORT-1.md (subagents may not write report files), so the report exists only here. The probes are in /private/tmp/claude-501/-Users-yki-Documents-github-atheric-under-the-code/1dfe6b29-505f-40e7-92c1-fd17c52389c5/scratchpad/review18/probes/.

# Review of the 1984b89 freeze (calibration section 18, combined 69bbef92)

**Trees:**
- clean `git archive` exports of 1984b89 (frozen), c50f7e1 (before) and e2df9cf (void attempt);
- a copy of figures-final's public/ (2c6c6109, branch at 929b930);
- the gate worktree's public/;
- review17's copy efc8b9dd;
- the nine dev trees.

**Held material:** every probe read held-stripped HTML (lib.mjs heldStripped) and located held material by id only. No held card, caption, strip or paragraph was read or printed. I did not touch commit 93aae05 or docs/pass-31-sealed/, and opened no tester input or prompt text.

## Defects

### A. High: abbreviations are credited by mentions in pointer and teaser sentences, and by mentions of abbreviations taught only in held material

- **Where:** scripts/known-terms.mjs:335-349 places an abbreviation at its first writing, with no pointer exclusion and no held-only rule. tests/pass31/lib.mjs:264 then credits every placed abbreviation.
- **Pointer exclusion is partial:** it exists only for the emphasis cue (known-terms.mjs:275-289). The builder's item 3 says pointer sentences do not teach; for abbreviations they still do.
- **Current label affected:** fig-8-12, token DNS, label "HTTP, DNS, SSH". It passes taught-yet.
  - Before Chapter 8, DNS is written only at ch4-ipc-p15, a teaser naming Part III's content. That is H5's class, but H5 was fixed only for p.part-tagline.
  - The same paragraph also places ARPANET and HTTP. Brief section 15 names HTTP and DNS as abbreviations "listed at the paragraph that teaches them".
- **Held clause bypassed:** these are glossary terms in glossary.noMention (taught nowhere, or only in held material), yet they are credited as abbreviations:
  - **ASLR**, from fig-2-1. It is placed at ch1-memory-p11, the very sentence known-terms.mjs:50 cites as teaching nothing.
  - **CFI**, from fig-br-1. New this round, via Chapter 3's closing list. It failed under c50f7e1.
  - **HTTPS**, from fig-11-1. New this round, via Chapter 11's lead. It failed under c50f7e1.
- **SBOM**, from fig-18-trace (not a noMention glossary term; first written in held Chapter 15). New this round, via the plural rule. It is placed at ch17-microservices-p7, a sentence pointing to Chapter 15.
- **Older cases of the same class:** CVE, US, GCHQ and CA are first written in held material and credited by later mentions.
- **Fix:**
  - skip a writing whose sentence matches POINTS;
  - do not place a noMention abbreviation, or one first written in held material, except through a gloss cue.
- **Tests:**
  - must fail: DNS at fig-8-12, ASLR at fig-2-1, CFI at fig-br-1, HTTPS at fig-11-1, SBOM at fig-18-trace;
  - must pass: DNS after its teaching paragraph; DEP from fig-2-1.
- **For e2 or the owner:** at fig-8-12, TCP and UDP are also credited, from a bare mention at ch4-ipc-p14. This is the documented first-writing limit, but it departs from brief section 15's wording.

### B. Medium: the new definition cues treat any line break in the HTML source as a sentence start

- **Where:** scripts/known-terms.mjs:146-147 (SENT matches `\n`), :157 (clauseBefore), :200 and :264 (rawBefore keeps textMap's newlines).
- **Effect:** "TERM is a/an/the" teaches TERM mid-sentence whenever TERM happens to start a source line.
- **Proof on a copy of the live tree:** I planted "…, and⏎safety is a concern; … as a⏎group is …" in ch1-context-p1.
  - safety and group were then placed at ch1-context-p1 as "prose gloss (definition)", and both passed at fig-1-3 and fig-5-11.
  - The same text on one line left both failing.
- **On the book today:** 2 of the 10 definition-cue hits are mid-sentence (cache coherence, processes). Neither moves a teaching point, so no current verdict changes.
- **Fix:** collapse whitespace inside each piece and join pieces with a non-whitespace separator.
- **Tests:** the two planted mid-sentence uses must fail; a control at a real sentence start must pass.

### C. Medium: two rows of the freeze record's hash table are stale

- **docs/pass-31-calibration.md:1322:** places.mjs is recorded as 18b42f9e…, which is e2df9cf's file. The frozen file is 198a4b32e74e2f5224b9628aedc7741d7c4770262ade056d4253ff12c6bf7641.
- **docs/pass-31-calibration.md:1327:** taught.test.mjs is recorded as 515b6443… (also e2df9cf's). The frozen file is ffa8095fd20e2771349a390292935ceb01ee3cdf35143398f35ac41d8f3d1c00.
- **Everything else matches:**
  - the other 19 fingerprint files;
  - dev.mjs, packet.test.mjs, frozen.test.mjs and sheet.mjs;
  - pass-31-exempt.json;
  - the combined hash.
- **Fix:** correct both rows.

### D. Medium: a single run reaches the author with no marker

- **Where:** tests/pass31/gate.mjs:75-77 and :87.
- **Problem:** `--single --author` without `--criteria` is accepted outside a decision. The author's line is the same `{id, pass, failed}` a decision prints, although the bar is 2 of 3 runs.
- **Fix:** refuse `--single` with `--author` unless IN_DECISION, or print `single: true` on that line.
- **Tests:** add the case to frozen.test.mjs.

### E. Low: C++ at fig-5-11 is a false flag (newly failing; also fails at fig-5-10)

- **Where it is taught:** ch5-survives-p1, between fig-5-9 and fig-5-10, glosses C++ with a possessive apposition.
- **Cause:** the forward apposition cue (known-terms.mjs:139-140) needs an article, while the reverse cue (OPENS_NP) accepts possessives.
- **Fix:** accept a possessive determiner, keeping the LIST and POINTER guards.
- **Tests:** C++ fails at fig-5-9 and passes at fig-5-10 and fig-5-11; plain-use regressions still hold.

### F. Low: DA at fig-8-9 is a hex byte, reported as an abbreviation (newly failing)

- **Where:** inside 9C:DA:C7. Its neighbours 9c and c7 fail as notation.
- **Why it matters:** hexadecimal is taught at ch1-cpu-p2, and MAC hex bytes at ch8-ethernet-p7. So DA, 9c and c7 (and HEXADECIMAL on the same figure, which already failed before this round) are false flags, or at least carry the wrong reason.
- **Fix:** judge hex groups in a colon-separated hex run as notation, taught once hexadecimal is; at minimum, report the reason correctly.

### G. Low: some partial results reach the author unmarked

- **--no-pairwise:** the caller chooses it, and the author's line shows no mark (gate.mjs:68, :87).
- **fig:check --gate1=off or quick:** per-figure PASS lines are unmarked (check.mjs:178); only the summary line names the mode (:184).
- **check.json:** it does not record the fingerprint (:182).
- **Fix:** mark these runs on every line, and write fp.combined into check.json.

### H. Low: docs/pass-31-exempt.json is unhashed (hash.mjs:16)

- **Problem:** its free lists label_cap.ids, floor.ids and caption.ids can exempt any figure (check.mjs:54-58).
- **Fix:** refuse ids outside at_bar ∪ kept ∪ {fig-18-6}.

### I. Low: figures-final's own fig:check is unfrozen

- **Problem:** it still runs check.mjs a53d8115, lib.mjs 170d6eaa and known-terms.mjs df5a945e, with no refusal.
- **Fix:** on the author's side, bring the frozen gate over or make that copy refuse.

## Checks that hold

### 1. Every review17 item is fixed and tested

- **Scope:** H1 to H5, the 11 false flags, Fig 4.19's virtual machine and VM, and the placement class.
- **fig:taught-test:**
  - 228 of 228 on the live copy, the gate tree and efc8b9dd;
  - with c50f7e1's code, 162 of 228, so 66 fail as recorded;
  - taught.test.mjs:145 and :160 are corrected.
- **fig:packet-test:** 17 of 17, also with the current ledger 0af7627a.
- **fig:frozen-test:** 12 of 12, run from the clean export.

### 2. Hole search: holes found are A and B

**Ablating each new rule over all non-held labels** (labels whose verdict depends on the rule):

| Rule | Labels affected |
|---|---|
| prefix | 0 |
| abbreviation plural/possessive branch | 0 |
| defining rows | 10 |
| emphasis | 4 |
| definition cues | 12 |
| chapter leads (JSON) | 1 |
| plural placement (VM, ID) | 2 |
| key-term names (javascript newly fails) | 1 |

**Other sweeps:**
- **Emphasis:** all 181 emphasis uses are term introductions.
- **Tables:** every non-held table row is classed correctly.
- **Abbreviation forms:** 379 capitals × 5 forms behave like the abbreviation; the one exception is HTTPs, which is stricter.
- **Short forms:** lower-case short forms fail before teaching, except when the prose writes that exact token (am, cap, Mac, mov).
- **Prefix:** 19 book words pass at fig-1-1 only through the prefix rule; none is a name or an abbreviation.
- **Glossary leaks:** names-route leaks fell from 51 to 30; other leaks went from 11 to 14 (the additions are Semaphores, a plural of a taught term).

### 3. Newly failing tokens (4)

| Token | Figure | Verdict |
|---|---|---|
| redis | fig-4-20 | True positive; first written at ch13-indexes-p4 |
| javascript | fig-5-11 | True positive by rule; explained at ch11-modern-p8 |
| c++ | fig-5-11 | False flag (E) |
| DA | fig-8-9 | See F |

### 4. Prompts, exemptions and frozen-file checks

- **Prompts:** prompts.mjs is byte-identical (781262c1…), and all 7 prompt hashes are as in section 14.7.
- **Exemptions:** taught-yet has no per-figure exemption.
- **Frozen-file checks:** gate.mjs, dev.mjs, validate.mjs and check.mjs all refuse without the hash, and every imported .mjs is hashed.
- **Gaps:** D, G and H.

### 5. The run outputs match the record, except C

- **Runs:**
  - 27 evaluations, 54 complete runs, 1,170 tester calls, 0 errors, 0 reruns;
  - all 81 verdicts report 69bbef92;
  - run stamps 10:25:11Z to 10:33:32Z, after 963c24e at 10:25:05Z;
  - freeze commit at 10:48:25Z.
- **Table 18.3:** 27 of 27 rows match.
- **Runs passed:**
  - v1: 0 of 6;
  - v2: 0 of 6;
  - v4: 6 of 6;
  - Enigma: 6 of 6;
  - decoys: 0 of 30.

  The failed-criterion counts match 18.3.
- **Ledger:** the run copy 84b4c1be has 35 held rows. The current ledger 0af7627a has the same held ids and the same takeaways for Fig 1.1 and Fig 1.2.
- **Fingerprint:** it reproduces from a clean export.
- **Book counts reproduced:**
  - live copy: failing figures 128 to 124, failing tokens 500 to 472, 4 tokens start and 32 stop;
  - gate tree: 131 to 127, and 508 to 480;
  - efc8b9dd: the same as the live copy.
- **Dev trees:** packets and taught-yet results are identical under both codes in 9 of 9 trees.
- **Exemplars (frozen fig:check, gate1 full):** fig-1-5, fig-4-8, fig-10-3, fig-13-6 and fig-17-6 all PASS, each with 120 Gate 1 rows clean. The anchors part check could not run in my export, which is not a git repository, so it was not verified.