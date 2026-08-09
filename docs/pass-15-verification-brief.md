# PASS-15 VERIFICATION BRIEF — Part II (Ch4–7)

Authored by the bridge, 2026-08-09. The last coverage asymmetry: every other
part's language pass has had a full independent audit (14/16/17/18
verifications); Pass 15 never did, and its own adversarial defense was
partially degraded in-flight — six defense agents died on a session limit and
the executing model defended those batches itself. Every verification to date
has found real items in the clearance layer (~15, ~30, ~30, 22), and the Pass
19 sweep already caught two fact-class breaks in Ch5. You audit those
clearances now, **with licence to override**.

**This pass runs while the owner is reading the book.** The book is declared
READY (`UNDER.md` §4s) and live. That raises the bar on restraint: surgical
fact fixes only, zero register churn, and the anchor law is doubly sacred —
the owner's own reading position may be parked in part-2.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu, CC BY-NC 4.0); this is an approved editorial plan executed
on the author's behalf. Ch4–7 cover the kernel, C and UNIX, C++, and Python.
Model: **Fable.** If the session drops to a weaker model mid-part, stop at
the next ledger.

## Read first, in this order

1. `CLAUDE.md`, then `BRIDGE.md`.
2. `UNDER.md` §4o — the ledger you are auditing — then the §4n/§4p/§4q/§4r
   verification sub-entries (your method, four precedents), then **§4g and
   §5 — §5 now carries the Pass-19 ratified spelling rule and the
   Diffie–Hellman dash convention; both bind you.**
3. `UNDER.md` §4s — what the closing sweep already fixed in Part II (the two
   Ch5 "Recall from" breaks) and its register flags (see Constraints).
4. `STATE.md`.

## The brief

**Scope: `part-2.html` (Ch4–7).** Method — the standing verification pattern:

1. **Deep read of all of Part II by you** against the pedagogy-first bar.
   The bar itself lives in this part: **the Ch7 pickle coda is the book-wide
   register calibration standard — it is untouchable**, and so are the
   Phase-2 items (the Little's Law mechanism `ch4-scheduling-p10`, the Ch4
   closer stamp `ch4-security-p18`).
2. **Independent per-chapter fresh readers** (pedagogy lens, web-enabled),
   blind to §4o's verdicts.
3. **Every flag adjudicated against an adversarial defense** — the full
   defense Pass 15 only partially got.
4. **Re-verify the load-bearing §4o corrections against primary sources or
   by recomputation.** At minimum: both replacement Stroustrup quotes
   word-for-word against their documented sources (D&E 1994); WAL =
   Gray/System R, late 1970s; pipes conceived by McIlroy, built by Thompson;
   the scheduler-tick, major-vs-minor-fault, cgroups, CPU-quota, Firecracker,
   and eBPF scopings; CFS-and-EEVDF; PDP-7 minicomputer; the "after B"
   naming; K&R 2nd ed.; browser = C++; the 70% memory-safety scoping; Zig;
   OS/360 for Brooks; Simula's words vs ideas; modules = C++20; moved-from =
   unspecified; the Christmas-1989 seam; Dartmouth BASIC compile-and-go; Zen
   of Python = Tim Peters 1999; GIL 5 ms switch interval; the .pyc caching
   semantics; the bytecode/stack-machine lineage; the matmul figure's
   measured numbers (re-benchmark locally if feasible — the figures should
   still be self-consistent even if your machine differs).
5. **Re-judge the §4o re-carries** (the GIL lost-update race, UBSan as the
   optimizer's mirror, the MLFQ caption, the signals triad) against the
   pickle-coda bar, and **re-read the cleared spans** — the partially
   self-defended clearances are exactly what you are here for.
6. Fix what fails; your own confirmation gate over the diff (it has caught
   the verifier's own errors in all four precedents).

## Constraints

- Greenbar identity untouched — phosphor plates, banding, sprocket rails,
  the cumulative LISTING meta lines (ch4 `0001–0790` → ch7 `2414–3199`),
  the `EOF` closer. Heroes, chapter order, thesis set, authorship line
  untouched.
- **Pass 19's register flags for Part II are the owner's, not yours**: the
  "End of Part Two" closer label and its headline pattern are flagged for
  his read — do not act on them.
- **Figures: text labels only**, §4g-precedented, a11y titles matched. A
  genuine geometry defect gets flagged to the punch-list pass with
  coordinates — nothing is sanctioned here.
- **Anchor-ID law:** part-2 set byte-identical (verify against HEAD; last
  recorded 346) or `ANCHOR_ALIASES` migration verified at zero pixel delta —
  and prefer byte-identical; the owner is reading.
- **Glossary:** regenerate; the book-wide count is now **519** (§5, the
  Pass-19 Diffie–Hellman merge); expect 519, no entry added or removed
  unless deliberate and named; diff the definitions; extractor gotchas and
  SKIP_WORDS precedents apply; the `thompson` entry quirk is documented and
  stands.
- **Spelling per the §5 ratified rule** — British prose, retained classes
  (quoted titles, SQL keywords, terms-of-art, code registers, civilization);
  -or/-our outside scope; source comments exempt.

## Verification & close-out

The full §7 protocol: local CF-mimicking server, Chromium **and** WebKit,
1440 + 375, part-2 / index / glossary, dark + light — 0 console errors,
0 external requests, 0 h-scroll, nav 48 px, anchors resolve; screenshot every
touched passage in both engines; push; **confirm live parity** with corrected
strings on the live page.

Ledger: a **"### Pass-15 verification"** sub-entry under `UNDER.md` §4o, in
the house verification shape. Update `STATE.md` (the parallel-audit item
done; the coverage table now uniform). Record the commit sha and the
confirmed push. Anything register-class you find goes to the ledger as a
flag for the owner read — his punch list is the only pass that touches
register from here.
