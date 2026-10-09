# PASS 25 BRIEF — Place and Marks: intelligent reading place, a cue you can correct, coloured section marks (ledger §4y)

Authored by the bridge, 2026-10-05. **Status: ratified by the owner
2026-10-05; runs after Pass 22** (its chapter-tab scroll-spy is this pass's
foundation, and the cue must agree with it). Model: Opus 5.5; Sonnet 5.5 verification after (BRIDGE §5). UI work — the
ui-ux-pro-max standards apply (transform/opacity motion, reduced motion,
≥3:1 non-text contrast, never colour-only meaning, 44px touch targets).

**Binding documents, in this order of precedence:**
1. This brief (owner rulings and bridge resolutions below).
2. `docs/pass-25-review.md` — the adversarial review. Every **HIGH** item
   (H1–H13) is a mandatory amendment. **MEDIUM** items are mandatory unless
   the pass finds a better route and records why in the ledger. LOW and
   "missing" items: do them where cheap and right.
3. `docs/pass-25-spec.md` — the unified design spec (tracking model, cue,
   hover/touch, set-my-place, section marks, palettes, data and sync,
   accessibility, motion, performance, invariants, verification). Where the
   spec and the review conflict, **the review wins**.

Both were produced by a 12-agent design workflow: two tracking models
(conservative-commit won), three interaction designs (section-native won,
with grafts), palettes built and independently re-verified for contrast and
colour-blindness, a storage design, one integrator, one three-lens
adversarial reviewer (reader / accessibility / engineering).

**Context:** *Under the Code* is the owner's own published book. Read first:
`CLAUDE.md`, `BRIDGE.md`, `UNDER.md` §2, §4c, §4d ("What invariant means"),
§4e, §4f, §5, §4v (Pass 22), `STATE.md`.

## Owner's intent (2026-10-05)

- Track the **real place the reader was reading**, not merely where the
  page is scrolled — skims, flings, look-ups in another part, pop-ups and
  fullscreen figures must not move it.
- The cue is **really seamless** at rest. Under the mouse it **widens a
  little**. The reader can **set the place themselves** when the tracker is
  wrong.
- The reader can **mark sections with different colours**.
- All of it in **the real design of each of the five volumes**, with a
  **custom marker palette per volume**. Per-volume colour on the cue:
  approved. Privacy-copy changes: owner approves at the pass.

## The shape in one paragraph

A 2px line on the bottom edge of the 48px nav shows chapter progress and a
small mark at the saved place (hollow = saved on this device, solid =
synced). The tracker commits a new place only from steady reading; anything
that looks like seeking becomes an excursion with a return point. Hovering
the line widens it to 8px with section segments and coloured marks; the
mark can be dragged to correct the place. Phones get a `place-btn` in the
nav that opens a slim place bar (nudge by paragraph, "Set to where I'm
reading", "Go to saved place", "Mark this section", "Back to before the
detour", "Let the book track"). Section marks: five colours per volume, each
with its own glyph and texture, shown on the section dot, the chapter tab
and the rail; synced for signed-in readers via a new `marks` table and
`/api/marks`.

## Bridge resolutions (binding)

1. **Palettes: one hue family per slot, tinted per volume** (review H10 vs
   the owner's "custom palette per volume"). Slot 1 amber, 2 red, 3 blue, 4
   green, 5 violet/neutral in every volume, so a reader's own colour code
   means the same thing everywhere; each volume keeps its own tint, names
   and glyphs. Re-derive the spec's table on this rule and re-verify:
   ≥3:1 on nav, chapter nav and page; CVD-distinguishable; Strongroom's red
   reads as wax/ink, never as an error.
2. **Labels come from the reading line, positions stay at line 56** (review
   H1). `anchor`/`fraction` keep today's meaning, so restores stay
   pixel-exact; every visible label and the resume card are computed from
   K, the paragraph the reader is actually on.
3. **Detours are hard to promote** (review H2). Cross-part, in-book-link and
   backward excursions need ≥3 min and ≥5 paragraphs, or reading past the
   end of the excursion's section. The 25 s rule applies only to direct
   arrivals. "Back to before the detour" lives in the place bar for 24 h.
4. **Drag stays on desktop** (the owner asked to set the place by hand at
   the mouse cue), but "Set to where I'm reading" is the main path
   everywhere, and paragraph ordinals come from the offset table, never
   from ids.
5. **Section dots are not tab stops** (review H7): `tabindex=-1`,
   `aria-hidden`; keyboard and screen-reader access goes through
   `place-btn` → place bar → "Mark this section". One new tab stop per page.
6. **The readout shows location only** (review H8/H9): sync state lives on
   the mark's shape, in `place-btn`'s name and in the place bar; the
   readout changes at most on a section change or every 10 s. Nothing
   flickers at the edge of vision.
7. **No discovery hints.** Under the Law of Invisible Software the cue
   explains itself on hover; no tooltip, banner or onboarding. The account
   page gains a short **"Your marks"** list (part · section · colour, link
   to each) — the book-wide overview the review found missing.
8. **One reading position stays** (decision 4 answered by the excursion
   model). The privacy notice still promises one position; it gains the
   marks sentences from spec §14, amended for H13 (the 180-day tombstone
   purge runs inside `/api/marks` requests — publish the copy only once
   that code exists).
9. **Domain move (~1 month):** signed-out readers' place and marks live in
   per-origin localStorage. Not this pass, but keep the stored formats
   versioned and portable so the move's hand-off is simple.

## Note added 2026-10-09 — the account mark shares the bar

Since this brief was written the bar gained an account mark (`.book-account`,
a bookmark at the right end of `.book-nav`; filled gold when signed in;
injected by `book.js`, `.book-nav.has-account` layout). The cue's
`place-btn` and readout must sit alongside it — place-btn immediately left of
the account mark at ≤620 px, the 2 px cue line under both — and the "synced"
state of the cue should not contradict the account mark's signed-in fill
(the mark reflects the hint cookie; the cue reflects the last real server
answer, which is the more truthful of the two: when they disagree, prefer
fixing the mark to follow the cue's knowledge of a 401).

## Invariants

Nav exactly 48.0px. Anchor set and `candidates()` count byte-identical;
injected elements carry no id matching the anchor regex (new ids use the
`utc-` prefix only). `READING_LINE` and the stored fraction's meaning
unchanged; `ANCHOR_ALIASES` honoured. Signed-out readers make zero API
calls. Zero third-party requests. Zero layout shift. Part IV body
untouched. The gold spine stays gold; per-volume colour lives only on the
cue, marks and existing per-part elements. No prose, no figures, no glossary
change.

## Verification & close-out

Everything in spec §13 **plus** the review's missing tests: `anchorAt` ↔
`computeAnchor` parity at 50 positions per part, out-of-order POSTs (`seq`),
multi-tab trace, tooltip-focus freeze, labels correct at section starts,
rotation/zoom, the detour-close-reopen trace, Tab-stop count, manual
VoiceOver + NVDA reading traces, forced-colors, print, reduced motion.
Chromium + WebKit; 1440, 375, 320; dark + light; all five volumes. Ship the
local-only `?utc-debug` overlay (state, budget, K, R; no network) so the
thresholds can be re-tuned after the owner's read. Preview first if the
D1 migration for `marks` runs against production. Push, live parity.

Ledger **`UNDER.md` §4y**: behaviour as shipped, thresholds as shipped,
the review items taken and any declined with reasons, palettes table with
measured ratios, invariants. Mark §6 P3.10 done. Update `STATE.md`.
