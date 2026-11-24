# Chapter 3 figures · 2026-11-12

Same method as Chapter 2 (`docs/session-2026-11-12-ch2-figures.md`): a blind screenshot read of every figure, each claim checked against the images, then by eye. Only confirmed faults were touched.

| Fig | Was | Now |
|---|---|---|
| 3.1 | The ARM64 and RISC-V opcode boxes were empty outlines while x86's showed 83. | Each shows its bits (100100010, 0010011). The "register" chip's frame clears its word. |
| 3.2 | "register w8" hung off the instruction column. | It sits under its box. |
| 3.4 | Two step moments fell while the next argument was already in flight (a stray d; a g over RDX). | Both moved to the settled moment just before (beats 4.6 and 7.3). |
| 3.6 | The dashed return line ran through the RSP mark. | It leaves the return box above the mark. |

Left as they are: 3.3, 3.5.

## Figs 3.7 to 3.11: owner ground, not touched

These five are kept originals. The scan's second reader, and my own look, agree they are the weakest figures in Part I on a phone: the whole drawing is scaled to about 40 %, so labels render at 4 to 6 px ("blocks reading" on 3.7, 3.8 and 3.9); in 3.8 the italic line is drawn over the text of both check boxes; 3.11's dates run 1998, 2003, 2001+, 2007. Their known content errors are in `docs/audit/owner-calls.md`. Redrawing them is the owner's call.

## Checked

Gate 1 still and motion with fullscreen (Chromium): 0 fails on 3.1, 3.2, 3.4, 3.6. Dashes clean, anchors unchanged.

## 2026-11-13 · simplify (Chapter 3 and the Bridge)

Owner: "now just simplify most of them. You don't need to repeat in text what the figure is already saying."

- **Fig 3.1**: the three colour chips above the picture repeated the three step buttons under it, and the hex under each row repeated the row. Both are gone; the figure is the three rows.
- **Titles** of 3.1 to 3.4 and BR.1 to BR.8 lose the clause that restated the picture.
- Captions here were already one short line each. Figs 3.7 to 3.11 (kept originals) are not touched.
- Still dense, not yet redrawn: 3.3, 3.4, 3.6, BR.2, BR.7, BR.9, and 2.6 in Chapter 2.

Gate 1 still and motion with fullscreen (Chromium): 0 fails on the eleven touched.

## 2026-11-20 · Figs 3.7 to 3.11 redrawn

Owner: "fix errors and simplify the one's. I have repeatedly only given two rules: understantable & simple." Summary and the list of what changed: `UNDER.md` §4ai. Generators: `scripts/figs/ch3/card.py` and `fig_3_7.py` to `fig_3_11.py`.

What the reviewers changed (blind readers, a second reader, two fact checks; twelve agents):
- 3.7, 3.8: the overwritten rows lost their names; the names now stand beside the rows as the A's take them.
- 3.8: called "the same overflow" while drawing forty A's against Fig 3.7's thirty-two; the description says forty. `__stack_chk_fail` cut from the strip (expert detail).
- 3.9: a dot where the attacker's line lands in launch 1; three unsourced entropy ranges replaced by the documented 28 bits.
- 3.10: the list ran down the page while every stack in the chapter has its first-used address lowest; it now climbs, with Fig 3.6's RSP mark. "add" became "add 1" to match the prose's "increment a counter". "forged" left the caption.
- 3.11: the 1988 note no longer reads as if fingerd was the worm's only way in.
Not acted on: the Morris "23" (owner ruling, `UNDER.md`); a baseline value beside "changed" in 3.8 (the "before" step shows it).

## 2026-11-24 · the five redone

Owner on the 2026-11-20 redraws: "worse design" (3.11), "DONT make THEM LOOK CHILDISH", "not understantable by anyone now and they look toys ... please fix it", and, when I said I would restore the old manner: "no you are not restoring them. You are fixing them." The redo and what it learned: `UNDER.md` §4ai and `docs/figure-method.md` ("Understandable comes first; simple is not cryptic", "Drawn for an adult"). The fragments in 3.10 run top to bottom again, headed "in order of use" (the reviewers' alternative to flipping the list). Deployed on his word the same day.
