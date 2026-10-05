# Pass 25 — unified design spec (workflow output, 2026-10-05)

Binding together with `docs/pass-25-review.md`. Where they conflict, the review wins (see `docs/pass-25-brief.md`).


This spec merges five inputs: the wf-a6 Position Fix, the tracking verdict (B+), the interaction verdict (B), the verified palettes and the storage design.

**Checked in the source (2026-10-05):**
- `READING_LINE=56` (`book.js:347`)
- `keyOf *20` (`:535`)
- `sectionLabel` is the `.section-number` textContent (`:435-444`)
- The rail copies tab text (`:121`)
- `scrollToAnchor` uses `scrollTo` (`:461-463`)
- The chip uses smooth scroll (`:648`)
- The reduced-motion kill has no fill-mode (`book.css:1199-1206`)
- The `position.js:48-52` whitelist

This pass runs after Pass 22, which fixes the chapter-tab highlighting.

**Contradictions resolved**

| Topic | Ruling |
|---|---|
| `src` as `'a'/'p'` or `'auto'/'set'` | `'auto'/'set'`, because storage wins on data. Pinned means `src:'set'`. |
| Pin sync "needs Pass 24" | One whitelist line in `position.js`, in this pass. |
| 4 nav/ink swatches or 5 hexes | The verified 5-slot palettes are final, with one hex per slot. |
| Slots 1–4, 0–4 or 0–5 | `c ∈ 1..5`. "None" is a tombstone, not a slot. |
| Range marks (`b`) | Dropped. No UI creates them. |
| Marked dot: ring or margin glyph | The slot glyph (10px SVG) sits in the dot's own 6×6 slot. No glyph in the paragraph margin. |
| 4 textures | 5: solid, hatched, dotted, half, outline. |
| Part II easing: `steps(1)` or `steps(2)` | `steps(2, jump-none)`, as in `part-2.css:204`. |
| `.cue-sr` span or `place-btn` name | The `place-btn` name, which exists at every width. |
| Marks sync in Pass 24 or now | Now, as step 25c. It uses only `getSession`. |
| Decision 4 (detours) | The excursion model below. Still one reading position. |

## 1 Intent
- Save the place the reader actually read, not wherever the page is scrolled.
- Show it with one hairline.
- Hovering or tapping reveals the controls to correct the place and to colour-mark sections.
- At rest, nothing new appears next to the text.

## 2 Tracking model

**Geometry** (document pixels, from a cached table)
- `navB`: measured bottom of the chapter nav (about 107px).
- `B = max(200, innerHeight − navB)`.
- Attention line `L = navB + 0.3B`.
- `K`: the deepest anchor whose top is at or above `scrollY + L`.
- `C`: the committed place. It is the only thing that is saved, synced or drawn.

**Encoding is unchanged.** A commit stores `snapshot()` at line 56 for the scrollY of that moment. Restores stay pixel-exact (§4c) and old clients can still read the record. Memory also keeps `C.y = scrollY + L`.

**Burst:** scroll events less than 200 ms apart, momentum included. A burst ends on `scrollend` or after 250 ms without scroll events. Scrolls within 100 ms of an `innerHeight` change are ignored.

**A burst is seeking if any of these is true:**
1. **Skipped text:** the gap from the old viewport bottom to the new `scrollY + navB` is more than 0.25B and contains a `chN-*-pK` paragraph.
2. **Unexplained jump:** more than 0.5B with no wheel, touch, key or pointer input in the last 300 ms, and the book did not move the page itself. This covers find-in-page, text fragments and back/forward.
3. **Navigation:** `hashchange`, a click on `a[href*="#"]` (chapter nav, rail, tooltip link `:859`), Home or End.
4. **Budget overspent:**
   - The budget grows at 60 chars per second of reading time.
   - Its cap is the characters inside the band at the last commit, with a floor of 600. It starts at cap/2.
   - Text crossing `L` forward is subtracted.
   - Going below −cap/4 counts as seeking.
5. **Long move:** back more than 0.5B, or forward more than 1.5B.

Reading time counts only while the page is visible and no fullscreen figure, tooltip, place bar or popover is open. It stops 120 s after the last input.

| State | Rule |
|---|---|
| SETTLING | Load, restore, chip jump, bfcache `pageshow`, and 400 ms after fullscreen closes. Nothing is saved. Ends 1.5 s after the re-pin stops, or on input. |
| READING | A burst that is not seeking is a step. 400 ms after it, `C` becomes the snapshot. Going back up to 0.5B is a re-read and changes nothing. |
| EXCURSION(R=C) | Starts on any seeking burst. **Return:** `L` comes within ±max(0.5B, 80px) of R, with 0 writes. **Promote:** at least 25 s of reading plus at least 300 chars read forward within budget, or at least 90 s on one spot with input in the last 120 s. Then `C = K`. |
| PAUSED | Tab hidden, fullscreen, tooltip, place bar or popover open. Positions are measured again on resume. |
| PINNED | See §5. |

**Undo after a detour:** for 10 min after a promotion, one reading step at `R_prev` restores it, with 1 write.

**Moving between parts**
- Arriving on a part other than `C.part` starts an EXCURSION.
- **Exception, reading on:** if `C` is in the last section of the previous part, landing on the next part's opener counts as reading.
- Opening `C.part` with no hash restores `C` (fixes G4).
- A hash equal to `C.anchor`, or the `pending` handoff, restores. Any other hash counts as seeking.
- `{R, R_prev, K, dwell, budget}` live in `sessionStorage` only.

**Other rules**
- **End of page** (max scroll − 4px, in READING): `K` is the last paragraph whose top is visible.
- **First visit:** the first commit comes after 8 s of reading past the opener.
- **Hiding the tab:** `pagehide` and `hidden` send **C** by beacon, never the live scroll position.
- **Glossary page:** never tracks (`:352`).

## 3 The cue at rest

**The line**
- `span.reading-cue` (no id, `aria-hidden`) sits inside `.book-nav`: absolute, `left:0; right:0; bottom:0; height:2px`. Track `#1e1e1e`.
- `.cue-head` uses `scaleX(var(--cue-p))` with no transition. `p` is the chapter progress of `scrollY + L`.
- `.cue-tick` draws section boundaries in `rgba(255,255,255,.18)`.
- `.cue-mark` sits at `C.y`. It is 6px tall (y 42–48) with a 1px `#0a0a0a` gap around it.
  - If `C` is in another chapter or part, the mark docks at the end of the track facing it, at 60% opacity.
  - A pinned place gets a 1px halo at 40%.
- Marked sections show as 2px segments in the slot colour, with 1px gaps.

**Readout and motion**
- `.book-progress` is rewritten only on a commit, e.g. `CH 4 · §03 · ¶7 · SYNCED` (at most 28 chars). On an opener with no `C`, the static text returns and the cue fades.
- Chapter change: fade out 160ms, reset, fade in 200ms.
- Restore draw-in: the head grows from 0 to p over 480ms, once.

**Dots, tabs and rail**
- Marked section dot: the slot glyph, no pulse. Unmarked dot: keeps `livePulse`.
- Marked chapter tab: `.nav-item{position:relative}` plus `::before{position:absolute; inset:0 20px auto; height:2px}`. The bottom border still means "active".
- Marked rail tick: the slot colour.

| Sync | Mark | Readout |
|---|---|---|
| Saved locally, or signed out | hollow | `SAVED ON THIS DEVICE` |
| POST returned `r.ok` during this page load | solid | `SYNCED` |
| Offline, 5xx or 401 | hollow at 50% | `SAVED HERE · SYNC PAUSED` |

- A beacon never sets solid, and every page load starts hollow.
- Footer (`:688`): `Reading sync · on` only after a 200 GET; `Reading sync · sign in` on 401.

## 4 Hover and touch

**Mouse** (`(hover:hover) and (pointer:fine)`)
- `.cue-hit` is a strip at y 36–48, layered under `place-btn`.
- It opens after a 120 ms dwell, and only if the pointer moves slower than 0.5 px/ms.
- The track grows from 2 to 8px (`scaleY`, origin at the bottom).
- An unscaled layer of per-section segments fades in. Marked segments are textured by slot.
- The mark grows to 8px and shows a grab cursor.
- `.book-progress` previews the target.
- Clicking a segment jumps there instantly (counts as seeking). The empty track does nothing.
- It collapses 300 ms after the pointer leaves.

**Touch** (620px or narrower, or no hover)
- `button.place-btn` shows the mark glyph in a 44×48 area at 620px or narrower. Above that it wraps `.book-progress`.
- Tapping it opens `#utc-placebar`: 48px tall, fixed at `top:48px`, z-index 160. It slides in with `translateY` over the chapter nav and pushes nothing. Contents:
  - `[◀¶] [¶▶]` slider
  - `Set to where I'm reading`
  - `Go to saved place`
  - Close
- Tapping a section dot opens the mark popover. On coarse pointers, `::after` gives it a 44×44 hit area.
- No long-press anywhere.

## 5 Set my place

**Ways in:** drag the mark, use the place bar, or choose "Set my place here" in the popover. Clicking the docked mark goes to the saved place.

**Drag**
- `setPointerCapture`, 4px threshold.
- Snaps to the nearest paragraph using cached geometry.
- A 30% ghost stays at the old place. The page never scrolls.
- Esc cancels. Release commits.

**Slider:** the preview moves the ghost and the readout. The target paragraph gets `outline:1px dashed` in the accent at 40%, offset 6px. This changes no layout and leaves Part IV's font alone.

**`setPlace(anchor)`**
- Virtual scrollY = max(0, anchorTop − L).
- Stores the line-56 snapshot for that position with `src:'set'`.
- Saves locally and to the server at once.

**Confirm**
- The mark glides for 240ms and stays hollow until `r.ok`.
- The chip slot shows `Place set · §03 ¶4 [Undo]` for 6 s, paused on hover or focus.
- Undo restores the previous snapshot (kept in memory) in both stores.
- This toast takes priority over the other-device chip, which waits.

**Releasing a pin**
- Reading forward from within 1B of it (`src→'auto'`).
- At least 3 min and at least 5 paragraphs read within budget somewhere else.
- A new pin, or `Let the book track` in the place bar.
- Nothing else moves it, and there is no time limit.

## 6 Section marks
- **Shape:** `{part, a: section id, c}`, one mark per section.
- **The dot:**
  - Inject `button.mark-dot` as the first child of each `.section-number`. It holds no text, which keeps `sectionLabel` and the glossary scan clean.
  - Hide the old dot with `.has-dot::before{display:none}`. The button takes the same 6×6 flex slot.
  - Add `.mark-dot` to the `::before` selectors at `book.css:293`, `part-2.css:201` and `part-4.css:188`.
  - Without JS, the old dot stays.
- **Popover:**
  - `popover="auto"`, with a positioned div as fallback.
  - It sits on `#0a0a0a`, never on plates or dark cards.
  - Contents: a radiogroup of None plus the 5 colours (12px glyph and name), then "Set my place here".
  - Choosing a colour sets the mark and plays the part's motion. None removes it, with no toast.
- **Limits:** at most 250 live marks (409 `mark_limit`, shown once). Ids that can't be resolved are kept but hidden, and never rewritten.

## 7 Per-volume design and palettes

| Part | Strip | Saved mark | Fill | Set motion |
|---|---|---|---|---|
| I | plain, continuous | Gilt `#d4a853`, 1×6 notch | `#8a6a2a` | fade 160ms |
| II | 4px cells | Phosphor `#84ffb2`, 4×6 cursor, no blink | `#3fae7c` | `steps(2)` cut |
| III | route legs | Signal `#4fc4e6` "+", drawn open when hollow | `#2f9dc4` | scale .8→1, 160ms |
| IV | ledger rules above and below | Seal `#cf8d78` ring | `#946657` | stamp 1.12→1, once |
| V | capsules, 20ms stagger | 3 dots: 1 violet `#a08cff` = local, 3 teal `#4fd8c2` = synced, 1 lit + 2 dim = paused | `#7a68e0` | node stagger |

| Slot | I | II | III | IV | V |
|---|---|---|---|---|---|
| 1 solid | Sienna `#b27749` asterisk | P3 amber `#805c00` `>` | Route `#c36f16` arrowhead | Ochre `#8b5a03` tick | Candidate `#7b5e10` half node |
| 2 hatched | Madder `#aa3853` dagger | Ribbon red `#d35f51` `#` | Chart magenta `#a24389` diamond | Copying ink `#7d5188` redaction bar | Heartbeat `#b94065` zigzag |
| 3 dotted | Smalt `#787adf` double dagger | 3270 blue `#6680e2` `=` | Prussian `#5569ca` wave | Registry ink `#6d7bb9` double rule | Replica `#3f639a` double ring |
| 4 half | Verdigris `#008374` parallels | Carbon `#616462` `/` | Starboard `#2e7e4f` triangle | Verdigris `#068d85` lozenge | Follower `#0a9394` hollow ring |
| 5 outline | Murex `#725491` pilcrow | Magenta `#ad459b` `*` | Sounding `#7c8589` ring | Graphite `#64615e` tab corner | Commit `#6a8f3a` square |

- Every colour is at least 3.05:1 on the bar, the chapter nav and the page.
- The smallest colour difference under colour-blindness simulation is ΔE 11.3.
- Glyphs are SVG, at least 10px.
- The spine stays gold.

## 8 Data and sync

**Local storage**
- `under-the-code:progress` gains `v:2`, `src` and `sa` (the POST's `updated_at`, kept locally only).
- It is written on every change of `C`, in 1% steps. The 90-day expiry stays.
- `under-the-code:marks` = `{v:1, cursor, m:{"part|a":{c,t,x,d}}}`, with no expiry. When signed out, removing a mark deletes it outright.

**Position endpoint**
- Add one line: `if (body.src==='auto'||body.src==='set') clean.src = body.src;`.
- POST 2 s after `C` changes, with the 5% dedupe.
- The chip compares `remote.updated_at` with `sa`, so both times come from the server clock.

**Marks**
- Table: `marks(user_id → users ON DELETE CASCADE, part, a, c, t, x DEFAULT 0, seen_at, PK(user_id,part,a))`, plus an index on `(user_id, seen_at)`.
- `functions/api/marks.js`, built on `sameOrigin` and `getSession`:
  - `GET ?since=` returns rows with `seen_at > since`, plus a new cursor.
  - `POST {v:1, ops:[{part,a,c,t,x}]}`: at most 50 ops and 8 KB, regex-checked, `c` 1–5, `t` clamped to at most now + 5 s, upsert `WHERE excluded.t > marks.t`.
- Merge: last write wins on `t`; a tie goes to the higher `c`.
- Tombstones are purged after 180 days.
- Signing in uploads local marks with their original `t`.
- Traffic: one GET per part load; POSTs debounced 1 s, with a `pagehide` flush. Every call is gated by the sign-in cookie.

**Account deletion**
- Add `DELETE FROM marks` to the batch in `auth/delete.js`, and update its header comment and `account.html:260`.
- The client resets `cursor` and sets `d` on every local mark.

## 9 Accessibility
- **`place-btn`:**
  - The only new Tab stop in the nav.
  - `aria-expanded`, `aria-controls="utc-placebar"`.
  - Name, e.g. "Reading place: Chapter 4, section 03, paragraph 4, synced". It updates only on a commit.
- **Place bar:** `role="group"`, not modal.
- **Slider:**
  - `aria-valuetext` like "§03 Von Neumann, paragraph 4 of 9".
  - ←/→ move one paragraph, PgUp/PgDn one section, Home/End the chapter's start and end.
  - Enter commits. Esc reverts and returns focus.
- **`mark-dot`:** `aria-label="Mark section 03 Von Neumann: none"`, `aria-haspopup`, `aria-expanded`.
- **Marked tabs:** `aria-describedby` points to hidden spans. Tab text never changes.
- **General:**
  - One polite live region, used only after the reader's own action.
  - No single-key shortcuts.
  - Decorative layers are `aria-hidden`.
  - Focus rings are 2px in the part's accent.
  - New ids use only the `utc-` prefix.
  - No `strong`/`em` in injected UI (`:926`).
- **`forced-colors: active`:** track 1px `CanvasText`, head `Highlight`, mark and glyphs `CanvasText`. Shapes carry the meaning.

## 10 Motion, reduced motion, print, fullscreen

**Motion tokens** (transform and opacity only)
- Widen 180ms `cubic-bezier(.2,.7,.2,1)`; unwiden 140ms ease-in.
- Segments 160ms, starting after 40ms.
- Popover 160ms in, 120ms out, `translateY(4px→0)`.
- `--cue-move` 240ms. Hollow to solid 180ms.

**Reduced motion**
- `.mark-dot:not(.is-marked){opacity:.35}`.
- Stamp, stagger, glide and draw-in become instant. The head still tracks.
- Remove the JS smooth scroll (`:648`).
- Re-read the preference on `matchMedia` change.

**Hash jumps under the chapter nav (G5):** `section.section, section.section p[id], section.section [id^="fig-"]{scroll-margin-top:116px}`.

**Print:** hide `.reading-cue, .place-bar, [popover]`. Marked dots print as static glyphs.

**Fullscreen:** hide the cue and the place bar, and pause tracking. Esc closes the popover first.

## 11 Performance
- Offset table `{top, bottom, isPara, chars}` for the 153–307 anchors per part. It is built in one rAF on load, on `fonts.ready`, and from the body ResizeObserver (debounced 150ms).
- The passive scroll listener stores only `scrollY` and `now()`. One rAF writes `--cue-p`.
- Binary search only at the end of a burst.
- `getBoundingClientRect` only at a commit.
- One `setTimeout`, no intervals.
- Input listeners store timestamps only.

## 12 Invariants
- Nav exactly 48.0px.
- Anchor set and `candidates()` count unchanged.
- `READING_LINE` and the meaning of the stored fraction unchanged.
- Aliases honoured.
- One reading position.
- Signed-out readers make 0 API calls.
- 0 third-party requests.
- 0 layout shift.
- Part IV body untouched.
- Spine stays gold.

## 13 Verification

**Setup**
- Playwright ≥1.45 as a dev dependency (confirm the version on install), with `page.clock`, `npm run serve`, `page.route` stubs and the cookie `under_signedin=1`.
- Chromium and WebKit at 1440×900, 375×667 and 320×568.
- Every trace starts from `part-1#ch1-kernel-p2` (C0).
- Node unit tests for the budget and skipped-text rules.

**Traces**

| Trace | Expected |
|---|---|
| Wheel +120 every 8 s | Advances each step |
| PageDown every 45 s, ×4 | 4 commits |
| PageDown every 2 s, ×8 | Moves at most 1 screen |
| +4000 in 300ms, then idle | C0, 0 writes |
| Then reading | Promoted at about 25 s |
| Fling 3B and back | 0 writes |
| Scrollbar drag; scripted `scrollTo`; fullscreen for 60 s | C0 |
| Chapter-nav click, then reading | C0, then promoted |
| Tooltip link to part-3, then `goBack()` | C0 |
| Open part-3 directly, read 40 s | part-3 |
| Undo to `R_prev` | 1 write |
| Tab hidden during an excursion | Beacon sends C0 |
| Pin | Held, then `set→auto` |
| Read to the end of the page | Last paragraph |
| 1400px figure | READING |
| Open with no hash | Pixel-exact restore |
| Reduced motion and 568×320 | Identical results |
| 4× CPU fling | 0 rect reads, no task over 50ms |

- **Chromium only:** a CDP flick of 0.4B counts as reading; 4B counts as seeking.
- **iPhone:** check momentum by hand.

**UI checks**
- The slow-hover gate.
- 0 rect reads during a drag.
- Esc paths and slider keys.
- Popover dismiss and the fallback.
- 44px touch targets.
- Undo in both stores.
- Solid only after a 200.
- Footer text on 401.

**Marks checks:** sync between two contexts, tombstones, the tie rule, 409 at mark 251, account deletion, aliases.

**Every run**
- `node final.mjs`.
- Forced-colors emulation.
- Print preview.
- 0 console errors, 0 horizontal scroll.
- Readout not clipped at 621, 960, 1100 and 1440.

## 14 Owner copy to approve (privacy changes)
- **Intro:** "Reading progress **and section marks** for signed-out readers live in your browser's localStorage and never leave your device. An account adds **two things: the same reading position, and any sections you mark**, stored server-side so they can follow you between devices."
- **What is stored:** "…chapter and section titles, **whether you set it yourself,** and when it was last updated. **The sections you mark: which section, the colour you chose, and when you last changed it.** That is the whole database."
- **Retention:** "**Marks stay until you remove them. A removed mark leaves a short note (which section, and when) so your other devices remove it too; the note is erased after 180 days.**"
- **Deletion,** also in `account.html:260`: "…removes your email, sessions, position **and marks** immediately and completely."
- **UI strings:** `Set to where I'm reading`, `Go to saved place`, `Let the book track`, `Place set · [Undo]`, `SAVED ON THIS DEVICE`, `SYNCED`, `SAVED HERE · SYNC PAUSED`, `Reading sync · sign in`.

## 15 Open risks
1. The thresholds are tuned on paper only. Keep them as constants and re-tune after the owner reads.
2. iOS momentum and `scrollend` support vary, so the 250ms fallback must hold.
3. An old cached `book.js` drops `src`, so a pin is lost until the cache refreshes.
4. A pin puts the paragraph exactly at `L` only on the viewport where it was set. Other viewports land within 0.3B.
5. The domain move in about a month: localStorage belongs to one origin, so signed-out readers lose their place and marks unless a small `#handoff=` fragment pass ships before the move.
6. Pass 24 must keep `getSession` stable for `marks.js`.
7. The mark dots add about 40 Tab stops per part. Check with VoiceOver and NVDA.

