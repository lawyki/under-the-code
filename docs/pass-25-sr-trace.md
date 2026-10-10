# Pass 25 — manual screen-reader trace (for the owner)

Written by the Sonnet 5.5 verification (2026-10-10); items it flagged as
defects are fixed (marked ✓). Run on `/part-2`, fresh profile, signed out.
About ten minutes per reader. Report anything that differs.

## VoiceOver — macOS Safari (System Settings › Keyboard › Keyboard navigation ON), then iPhone

1. Load /part-2 and wait 10 s. Expect silence: nothing like "Place set" or
   "Marked" on load or while you scroll.
2. VO+Right into the top bar: "Under the Code, link", then the readout button
   ("PART II OF V … Reading place, collapsed, button"), then "Account". The
   description ("No saved place yet. Saved on this device.") follows after a
   pause.
3. VO+Space on the place button → "expanded". Move to "Close the place bar",
   then the slider: "Reading line, by paragraph, slider, §01 …, paragraph N of
   12". Up/Down change the paragraph and speak the new value. Note whether §
   and ¶ are spoken sensibly.
4. On the slider press Return → one announcement, "Place set: Chapter 4,
   section 01 …, paragraph N of M." Spoken once only ✓.
5. Move to "Mark this section" (it says "collapsed" ✓) and press VO+Space → a
   menu "Mark section 01 …" with "None, radio button, selected", "P3 amber",
   "Ribbon red" … Arrow down, VO+Space on "Ribbon red" → "Marked §01 …: Ribbon
   red." and focus back on "Mark this section". Reopen: "Ribbon red" is
   selected.
6. Escape in the menu (closes it, focus back on the button), Escape again
   (closes the bar, focus on the place button). The page does not jump back
   after a committed Set ✓.
7. VO+Right through the chapter tabs: "01 — Anatomy, link, Marked Ribbon red"
   on the marked tab only.
8. Move through a section heading: no "Mark section" button in the reading
   order, and no stray "Marked …" text left at the end of the page ✓.
9. iPhone: rotate to landscape, open "Mark this section", and reach every
   colour (the menu scrolls) ✓.

## NVDA — Chrome or Firefox on Windows

1. Browse mode, read the page with NVDA+Down for 30 s from the top: no
   unsolicited "Place set", no skipped paragraph.
2. Tab from the title: the place button, then "Account". Enter → "expanded".
   Tab → "Close the place bar", then "Reading line, by paragraph, slider".
   Right/Left speak the paragraph change; Enter → "Place set".
3. Tab to "Mark this section", Enter (switch to focus mode if NVDA doesn't).
   Down reads each radio item with its state; Enter selects it and "Marked
   §01 …" is spoken; Esc closes and returns focus. NVDA must not be left stuck
   in focus mode.
4. Windows High Contrast (Aero or Night sky): open the bar and the menu; the
   selected menu item is visibly marked ✓ and all buttons keep their borders.
5. Zoom to 400 % on a 1280 px window: "Mark this section" and every menu
   colour stay reachable (bar and menu scroll) ✓.

Note: Safari without Full Keyboard Access skips buttons on Tab (site-wide,
not this pass) — use Option+Tab or turn Full Keyboard Access on.
