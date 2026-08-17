# PASS 21 BRIEF — the icon pass (§6 P1.2, ledger §4u)

Authored by the bridge, 2026-08-17. Owner-ratified: the P1 backlog's emoji
icons (⚡-class glyphs in `.insight-icon` / `.concept-icon`) become
hand-drawn inline SVG — the book's last non-SVG drawing surface goes
native, and the cross-platform rendering inconsistency dies. **Model:
Fable** — this is visual craft across five identities.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu); approved editorial plan. Read first: `CLAUDE.md`,
`BRIDGE.md`, `UNDER.md` §2 + §4d (the identity architecture and what
"invariant" means), §5, `STATE.md`.

## The brief

1. **Inventory first.** Enumerate every emoji-as-icon site across all five
   part files, the index, and glossary/account if any. Record the count
   and the distinct glyphs in the ledger before drawing anything.
2. **Design one icon set in the book's figure grammar** — stroke-drawn,
   mono-weight, sized to the current icon box — and let each volume's
   identity colour it: use `currentColor`/the part's accent token so the
   existing per-part CSS does the theming, not five hand-tinted sets.
   The icons must read as quotations from the book's own figures, not as
   an icon library. Restraint is the bar: if an emoji's meaning needs a
   complex drawing, simplify the metaphor rather than the stroke.
3. **Semantics:** decorative icons get `aria-hidden="true"` (the strip
   text carries the meaning). No new DOM depth beyond the swap; no JS; no
   animation (the strips are reading furniture, not figures).
4. **Invariants:** zero third-party requests; anchor sets byte-identical
   in every touched file; reduced-motion and print unaffected (check the
   print block renders the SVG icons acceptably or hides them as the
   emoji were); glossary 519 ±0.

## Verification & close-out

§7 on every touched page, Chromium **and** WebKit, 1440 + 375, dark +
light — the icons screenshot-reviewed in **both engines in every volume
identity** (this is the point of the pass: identical rendering
everywhere). Push, confirm, live parity.

Ledger: **`UNDER.md` §4u** — inventory, the design rationale in two
sentences, per-identity screenshots noted, invariants. Mark §6 P1.2 done.
Update `STATE.md`.
