# PASS 18 BRIEF — the language pass, Part V (Ch16–18)

Authored by the bridge, 2026-08-06, under the amended gate rhythm (`BRIDGE.md`
§1): this is the last part of the language pass; it is followed by Pass 19
(independent verification) and the READY declaration, not by a per-part owner
read.

**Context for the session running this:** *Under the Code* is the owner's own
published book (under.atheric.eu, CC BY-NC 4.0); this is an approved editorial
plan executed on the author's behalf. The chapters cover distributed systems
and security material in an educational register — the work is editorial, on
existing published text. Model: **Fable.** If the session drops to a weaker
model mid-part, stop at the next ledger; do not squeeze the part into a budget
that will not hold it.

## Read first, in this order

1. `CLAUDE.md`, then `BRIDGE.md` — the laws, especially anchor-ID law and §4g.
2. `UNDER.md` §4n–§4q — the four prior language-pass ledgers and their two
   verification entries. The method, the declines, and the failure modes all
   live there.
3. `UNDER.md` §4g and §5 — the fact ledger (law) and the known non-defects
   (do not "fix" blindly).
4. `STATE.md`.

## The brief

**Scope: `part-5.html` (Ch16–18) only.** One pass is one part. Cross-part
inconsistencies you find are **flagged in the ledger for Pass 19, not chased**
— unless the fix lives entirely on the Part V side.

**The bar — Part IV's recalibration, ratified by the owner: pedagogy first,
facts second.** A passage that is factually impeccable and pedagogically inert
has failed. Mechanism carried in prose, cause to effect, felt rather than
named. The register bar is the Ch7 pickle-as-interpreter coda (part-2); when
unsure whether a passage holds, compare it to that. Judge every section as a
reader who wants to be gripped, and re-read every clearance once against
"would I enjoy reading this?" before declining a flag.

**Surgical, not wholesale.** Parts II–IV found the prose already at bar in
most places; only passages that *list* where they should *run* get re-carried.
"Already at bar, left as-is" is a valid and frequent verdict. Rewriting good
prose to prove effort is a failure.

**Method (the shape every prior pass used; the final gate is not optional):**

1. Deep read of all of Part V as a student who must understand it.
2. Independent per-chapter/per-section reader agents (pedagogy lens,
   web-enabled), then an **adversarial defense pass** — the target list is
   what *survives* defense, not what was first flagged.
3. Rewrites.
4. A 3-lens **confirmation gate** (facts / internal consistency / voice) over
   the full diff. This gate has caught self-introduced errors in every single
   prior pass — expect it to catch yours.
5. **Verify before fix**, throughout: every flagged fact is independently
   recomputed or checked against primary sources; conflicts are flagged, not
   guessed. Audits carry their own errors.

## Part V specifics

- **Do not touch:** the chapter heroes; the Quorum identity layer (`part-5.css`
  — constellation openers, `.qm-quorum` closer caption and its pass-5 z-order
  fix, violet/teal grammar, `#bca8ff` strip accent); the Phase-2 closer stamp
  `ch17-microservices-p6` ("Ask what the abstraction still charges."); chapter
  order; the thesis set and authorship line (owner-authored, never yours).
- **§4g terrain that lives in or beside Part V** — corrections that must
  survive in substance: ZooKeeper runs **ZAB**, not Raft (fig 17.8 + 17.5
  caption); the Paxos-lore direction (the 1998 TOCS paper IS the parable);
  CAP/FLP and quorum-intersection mechanisms (verified sound in pass 2);
  "at most a few dozen error-corrected logical qubits"; Lambda "meters the
  bill in milliseconds"; fig 18.2 "172 years"; the "two hundred and
  thirty-five" figure-count prose. Re-introducing a corrected error is a
  failed pass regardless of how well it reads.
- **Figure edits:** §4g-precedented **text labels only**, each matched to its
  corrected caption and its a11y `<title>`; no SVG geometry.
- **Anchor-ID law:** the part-5 anchor set is byte-identical across the pass
  (verify against HEAD; last recorded count 189), or migrates through
  `ANCHOR_ALIASES` at `book.js scrollToAnchor`, functionally verified at zero
  pixel delta in both engines. Reading positions are user data.
- **Glossary:** regenerate after the prose settles (`npm run build:glossary`);
  expect count **520, no entry added or removed** unless deliberate and named.
  Known extractor gotchas: em-dash clipping, junk entries from broken term
  cues — reflow the prose or extend `SKIP_WORDS` (precedents: `gab`, the
  instruction-cycle verbs, `system v amd64 abi`, the pass-17 security terms).
  Check the diff of definitions, not just the count.
- **British spelling** (artefact, not artifact). House voice throughout.

## Verification (repeat the §7 protocol)

Local against the Cloudflare-mimicking server (extensionless 200, `.html`
308), **Chromium and WebKit**, 1440 + 375, on part-5 / index / glossary:
0 console errors, 0 external requests, 0 page h-scroll, `.book-nav` 48 px,
fonts loaded, internal anchors resolve. Screenshot-review every touched
passage in both engines, dark and light. Then push, and **confirm live
parity** — corrected strings verified on the live page, live `glossary.json`
count checked.

## Close-out (all of it, no exceptions)

The ledger entry is the record; the chat report is a convenience. Write
`UNDER.md` **§4r** in the house shape: what changed and why, what was already
at bar, what was **declined** (with reasons — the next session must be able to
not-"fix" them blindly), fact corrections in the verified-how/outcome table
form, invariants (anchor set, glossary, §4g), verification results, commit
sha. Update `STATE.md` (Pass 18 done; Pass 19 next). Push, confirm the push
landed, and record live parity in the ledger. Flag anything Pass 19 should
carry — cross-part stitches, uncertain declines, anything you cleared but
would want a second read on.
