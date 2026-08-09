# PASS-18 VERIFICATION BRIEF — Part V (Ch16–18)

Authored by the bridge, 2026-08-09. Second of the two verification passes that
stand in for the waived per-part owner reads (`BRIDGE.md` §1 amendment).
Runs **after** the Pass-17 verification has landed (one writing session per
repo at a time). **You have licence to override** the executing pass's
verdicts — they are evidence, not rulings.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu, CC BY-NC 4.0); this is an approved editorial plan executed
on the author's behalf. Ch16–18 cover concurrency, distributed systems, and
the book's synthesis. Model: **Fable.** If the session drops to a weaker model
mid-part, stop at the next ledger.

## Read first, in this order

1. `CLAUDE.md`, then `BRIDGE.md`.
2. `UNDER.md` §4r — the ledger you are auditing, including its "For Pass 19"
   list — then the §4n/§4p verification sub-entries (your method), the new
   Pass-17 verification sub-entry under §4q, then §4g and §5.
3. `STATE.md`.

## The brief

**Scope: `part-5.html` (Ch16–18)**, plus the two sanctioned figure-geometry
fixes below. Method — the 14/16 verification pattern:

1. **Deep read of all of Part V by you** against the pedagogy-first bar (the
   Ch7 pickle coda).
2. **Independent per-chapter fresh readers** (pedagogy lens, web-enabled),
   blind to §4r's verdicts.
3. **Every flag adjudicated against an adversarial defense**; expect to
   decline some of your own readers' flags.
4. **Re-verify the load-bearing §4r corrections against primary sources or by
   recomputation.** At minimum: the Knight Capital strip against SEC Release
   34-70694 (the stale-server/Power Peg mechanism, the rescue-vs-acquisition
   dates); CP/CMS vs VM/370; EC2 hourly→per-second; the verbatim Amdahl and
   Brewer quotes; Herlihy wait-free/lock-free; fig 18.2's "1 network · 1
   kernel" and Boole/Cork; Dynamo vs DynamoDB; the CUDA
   threads-within-a-block rescope; Docker/LXC/libcontainer; the Google 2B
   containers/week attribution; Lambda/Firecracker microVM reuse; the
   Spectre/Meltdown "mid-1990s" hedge; the quantum-optimisation and
   neuromorphic-efficiency hedges.
5. **Re-judge §4r's three re-carries** (ch16-lockfree-p3's release/acquire
   walk, ch17-consensus-p2's quorum-overlap witness, ch17-virt-p2's
   trap-and-emulate caption) **and the rewritten Knight strip** against the
   bar — §4r itself asks for this. Re-read the cleared spans.
6. Fix what fails; confirmation gate over your own diff.

**Sanctioned geometry fixes (bridge-authorised, 2026-08-09 — the one place
your figure licence exceeds text labels):**

- **fig 16.8** — the Amdahl speedup curves terminate *above* their own ceiling
  lines (p=0.95 ends ~y164 vs its 20× asymptote at y184; p=0.90 and p=0.50
  similar). Recompute the curve endpoints so each approaches its asymptote
  from below; the drawn math must not falsify the section's own equation.
- **fig 17.7 / 17.8** — the CAP spatial encoding: 17.7 parks "CA
  (impossible)" nearest the P vertex; 17.8's AP dot-cluster hugs the C–A side
  and the "CA edge" note sits at the centroid. Rework the positions so
  distance encodes meaning; labels/captions stay consistent with the §4r
  Dynamo corrections.

Apply the pass-2 lesson to every geometry edit: bbox-vs-viewBox sweep **plus**
text-vs-containing-rect scan **plus** screenshots of every touched figure,
both engines, dark + light, SMIL timeline sampled if animated. Metrics can be
satisfied while the defect remains.

**Known and settled — do not re-litigate:** "3 nm" (owner-ruled, twice
upheld); ch17-consensus-p9's DynamoDB (true of the service); the
ch17-virt-p2 "handful of its instructions" (the count is 17, Robin–Irvine
2000 — deliberately unnumbered; verify it reads well, do not number it);
fig 18.2's 1969/1976 sublabel tightness (pre-existing); the `thompson`
glossary quirk. Cross-part strays (part-1 "recognized", part-2
"recognizably") belong to the Pass 19 sweep, not you.

## Constraints

- Quorum identity untouched — constellation openers, `.qm-quorum` closer and
  its pass-5 z-order fix, violet/teal grammar, `#bca8ff` strip accent. Heroes,
  chapter order, the ch17-microservices-p6 stamp, thesis set and authorship
  line untouched.
- **Anchor-ID law:** part-5 set byte-identical (verify against HEAD; last
  recorded 189) or `ANCHOR_ALIASES` migration verified at zero pixel delta.
- **Glossary:** regenerate; expect 520 unless deliberate and named; diff the
  definitions; extractor gotchas and SKIP_WORDS precedents apply.
- British spelling; house voice.

## Verification & close-out

The full §7 protocol: local CF-mimicking server, Chromium **and** WebKit,
1440 + 375, part-5 / index / glossary, dark + light — 0 console errors,
0 external requests, 0 h-scroll, nav 48 px, anchors resolve; screenshot every
touched passage and **every touched figure** in both engines; push; **confirm
live parity** with corrected strings and both fixed figures on the live page.

Ledger: a **"### Pass-18 verification"** sub-entry under `UNDER.md` §4r, in
the house verification shape, with the geometry fixes documented per figure.
Update `STATE.md` (item 3 done; Pass 19 closing sweep next). Record the commit
sha and the confirmed push. Flag everything the Pass 19 sweep should carry —
it is the last pass before READY.
