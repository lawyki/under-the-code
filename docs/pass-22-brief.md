# PASS 22 BRIEF — the interaction pair (§6 P1.3 + P1.4, ledger §4v)

Authored by the bridge, 2026-08-17. Owner-ratified: the two remaining P1
items. **Model: Fable** (the tooltip work is interaction judgment; the
scroll-spy rides along). Both are `book.js`/`book.css` work — zero prose,
zero anchors, zero figures.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu); approved editorial plan. Read first: `CLAUDE.md`,
`BRIDGE.md`, `UNDER.md` §2 (the five IIFEs — your work extends #2 and #5),
§4e item 3 (the nav-fade pass — the precedent for touching this nav), §5,
`STATE.md`. The standing law that governs both features: **the Law of
Invisible Software** — remove a decision, remove an action, remove
waiting; every interaction must justify interrupting a reader.

## Item 1 — chapter-nav scroll-spy (P1.3)

`.nav-item.active` styling exists in CSS but nothing sets it on the
horizontal `.chapter-nav`. Extend the existing IntersectionObserver
machinery (the left rail already solves this problem — reuse its logic,
don't duplicate it) to set the active tab per section. When the active tab
is outside the scroll viewport of the nav, bring it into view *quietly*
(no smooth-scroll chase while the reader scrolls; respect
`prefers-reduced-motion`). Per-part identity styles the active state via
existing tokens — verify in all five volumes.

## Item 2 — glossary tooltips on touch (P1.4)

Today: hover/focus only; tap technically works via `tabindex` but
dismissal is awkward. Target: **tap toggles, tap-elsewhere or Esc or a
second tap dismisses, scroll does not kill it mid-read.** Desktop
hover/focus behaviour must be byte-identical — this pass adds a touch
path, it does not redesign the tooltip. No modal, no backdrop, no
positioning rewrite. First-use sections stay tooltip-free (the existing
rule). Keyboard and screen-reader behaviour must not regress.

## Verification & close-out

§7 on all touched pages, Chromium **and** WebKit, 1440 + 375, dark +
light, **plus touch emulation at 375 in both engines** (tap, tap-elsewhere,
Esc, scroll-with-tooltip-open, rotate). Scroll-spy verified in all five
volumes including a 7-tab chapter at narrow width (the §4e fade must still
work with the active state). 0 console errors, 0 external requests, no
jank on scroll (rAF/passive listeners; profile once). Push, confirm, live
parity.

Ledger: **`UNDER.md` §4v** — behaviour spec as shipped, the decisions
made and why they're invisible, invariants. Mark §6 P1.3 + P1.4 done.
Update `STATE.md`.
