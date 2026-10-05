# Pass 25 — adversarial review of the spec (workflow output, 2026-10-05)

# Pass 25 "Place and Marks": adversarial review

**Checked in the source (2026-10-05):**
- `book.js:347,384-448,457-518,535,541-578,600-623,686-690,958-968`, `book.css:31-57,92,101,288-302,1199-1206,1215-1229`, the per-part tokens, `position.js`, `_lib.js`, `auth/delete.js`, `account.html:139-145,250,260`, `schema.sql`, `_headers`.
- Contrast was recomputed independently (session scratch script, not kept). The palette claim of ≥3.05:1 against the bar, the chapter nav and the page holds for all 25 slots.

## HIGH

**H1 [eng/reader] Labels and readout name the wrong paragraph.**
- **Scenario:**
  - A commit stores `snapshot()` at line 56, which sits under the stuck chapter nav (48–107). That is about 290px above L at 1440×900 and about 220px at 375×667.
  - The readout `¶7`, the `place-btn` name, the index resume card and the other-device chip all read `section`, `sectionLabel` and `sectionTitle` from that record. So they name content above what the reader is reading. Near the top of a section they name the previous section.
  - `setPlace` makes it worse. With virtual scrollY = anchorTop − L, setting §04 ¶1 stores the last paragraph of §03, and the resume card then says §03.
  - "Promote: C = K" and "End of page: K = last paragraph" cannot be expressed in the line-56 encoding at all.
- **Fix:**
  - Keep `anchor` and `fraction` at line 56, so restore stays pixel-exact.
  - Compute every label from K, the paragraph at the attention line, and store it in the existing label fields (the whitelist already passes them).
  - Draw the readout, the mark and the button name from K.
  - Unit test: a place set at §04 ¶1 makes the resume card say §04.

**H2 [reader] A detour gets promoted too easily, which breaks requirement 1.**
- **Scenario:** at ch6, the reader follows a tooltip link to part-1 ch2, reads for 40 s and closes the laptop. 25 s plus 300 chars promotes the detour, and `R_prev` lived only in `sessionStorage`. Tomorrow the book resumes in Part I. Find-in-page lookups and going back via the chapter nav fail the same way. The goBack trace only covers the happy path.
- **Fix:**
  - Use asymmetric thresholds. Excursions that are cross-part, started by an in-book link, or go backward use the pin-release bar: ≥3 min and ≥5 paragraphs within budget, or reading past the end of the excursion's section.
  - Keep 25 s only for direct arrivals (index shelf, typed URL). Tell them apart with a `detour` flag set in `sessionStorage` on in-book link clicks.
  - Keep `R_prev` in localStorage for 24 h (local only), and offer "Back to before the detour" in the place bar.
  - Add a trace: detour, read 40 s, close, reopen, expect C0.

**H3 [eng] Multiple tabs and the hide beacon overwrite each other.**
- **Scenario:**
  - Every tab keeps its own C, and `pagehide`/`hidden` beacon C unconditionally.
  - Switching away from a stale tab B (part-1) sends B's old place over A's real one. Every tab switch also bumps `updated_at`, which raises false "other device" chips.
- **Fix:**
  - Beacon only when C has changed since the last `r.ok` (a dirty flag).
  - Add a `storage` listener that adopts a newer C written by another tab.
  - Re-read localStorage on `pageshow` and on `visible`.

**H4 [eng] Sync writes can race.**
- **Scenario:**
  - A 400 ms commit timer or the 2 s POST debounce scheduled before `setPlace` can fire after it and overwrite the pin.
  - POST(set) and POST(undo) can arrive out of order. The server is last-write-wins by arrival with no monotonic check (`position.js:55-58`).
  - SYNCED can light up from the ack of an older POST.
- **Fix:**
  - `setPlace` and Undo cancel all pending timers.
  - Send one POST at a time through a latest-wins queue.
  - The client sends `seq`, and the server rejects anything older than the stored `seq`.
  - The mark turns solid only when the ack's `seq` equals the current one.

**H5 [reader/a11y] PAUSED can freeze tracking indefinitely.**
- **Scenario:**
  - Glossary terms have `tabindex=0` and show the tooltip on `focus` (`book.js:958,968`). Nothing hides the tooltip on scroll.
  - A keyboard reader who focused a term and then scrolls with the arrow keys keeps the tooltip "open", so tracking stays paused.
  - Wheel scrolling with a parked mouse keeps opening tips through mouseenter after 160 ms.
  - A place bar or popover left open on mobile pauses tracking the same way.
- **Fix:**
  - Overlays pause only the accrual of reading time. Steps are never discarded.
  - Hide the tooltip on scroll.
  - Close the place bar and the popover on any scroll of more than 0.5B, or after 30 s idle.

**H6 [a11y] Screen-reader and magnifier reading is classed as seeking.**
- **Scenario:** in browse mode, VoiceOver and NVDA send no key events to the page, and "read all" scrolls about one screen at a time with no input. Rule 2 (more than 0.5B, unexplained) turns every page turn into an EXCURSION. C then trails behind, caught up only by repeated 25 s promotions.
- **Fix:**
  - Count `focusin`, `selectionchange` and caret moves as input.
  - Apply rule 2 only to jumps over 1.25B.
  - Add manual VoiceOver and NVDA traces.

**H7 [a11y/reader] Section dots add tab stops and screen-reader noise.**
- **Scenario:** there are 19–30 sections per part (verified: 24/24/30/19/19), not about 40. Even so, each heading is now preceded by "Mark section 03 …: none, button, collapsed", in browse mode and in Tab order, on top of the glossary tab stops that already exist. That is an interruption under the Law of Invisible Software.
- **Fix:**
  - Give `mark-dot` `tabindex=-1` and `aria-hidden`, and run axe `aria-hidden-focus`.
  - Add "Mark this section" (the section holding K) to the place bar. `place-btn` then stays the single keyboard and screen-reader entry point.

**H8 [reader] The readout cap contradicts the readout strings.**
- **Scenario:** the cap is 28 chars, but:
  - `CH 4 · §03 · ¶7 · SAVED ON THIS DEVICE` is 38
  - `… · SAVED HERE · SYNC PAUSED` is 41
  - `CH Bridge · §01 · ¶12 · SYNCED` is 30

  Clipping between 621 and 960px is guaranteed.
- **Fix:** the readout shows the location only. Sync state goes on the mark shape, in the `place-btn` name and in the place bar.

**H9 [reader] Flicker at the edge of vision.**
- **Scenario:** a commit lands 400 ms after every step and rewrites the readout. The mark then goes hollow until the POST ack about 2 s later. So the nav text and the mark change every few seconds while the reader reads.
- **Fix:**
  - Sync state shows the health of the connection, not each ack: the mark stays solid while the last POST succeeded and the backlog is under 10 s.
  - It drops to paused only after 2 consecutive failures.
  - The readout text changes only on a section change, or at most every 10 s.

**H10 [reader] Mark colours change meaning between volumes.**
- **Scenario:**
  - Slot 2 is red in I and II, magenta in III and purple in IV (`#7d5188`).
  - Slot 4 is green or teal everywhere except II, where it is grey (`#616462`).
  - Slot 5 is purple in I and II, grey in III and IV, and green in V.

  A reader's own code ("red = re-read", "green = got it") breaks from one volume to the next.
- **Fix:** keep one hue family per slot across all five volumes (1 amber, 2 red, 3 blue, 4 green, 5 violet or neutral). Vary only the tint, name and glyph per volume.

**H11 [eng] A removed mark comes back.**
- **Scenario:** a mark synced earlier is removed while the reader is signed out. Under the spec it is deleted outright, so the server copy returns on the next sign-in.
- **Fix:** delete outright only if the mark was never synced. Otherwise write a local tombstone.

**H12 [privacy] Shared devices and account switching.**
- **Scenario:** logout (`account.html:250`) clears no storage. When user B then signs in, "Signing in uploads local marks" pushes user A's marks into B's account.
- **Fix:**
  - Store the owner id returned by GET marks alongside the local marks.
  - Upload only marks that have no owner, made while signed out.
  - On logout, clear the synced marks and position, or offer to.

**H13 [privacy] Nothing performs the 180-day purge.**
- **Scenario:** Pages Functions have no cron, yet the privacy copy promises the purge.
- **Fix:** run an indexed delete of tombstones older than 180 days (LIMIT 100) inside every marks request, or deploy a Worker cron. Only then publish the copy.

## MEDIUM

1. **Marks trust the client clock.** `t` comes from the client and is clamped only upward. A phone running 10 min slow cannot remove a mark set on the laptop. The tie rules also differ: the server keeps the existing row, the client takes the higher `c`. **Fix:** the server assigns `t = max(now, old.t+1)`, the client adopts the server's `t`, and both sides use one tie rule.
2. **The cursor can skip rows.** `seen_at > since` at millisecond resolution misses rows written in the same ms as the cursor. **Fix:** use a monotonic version or rowid as the cursor.
3. **`x` and `d` are never defined.** POST accepts only `c` 1–5, so a tombstone cannot be sent. **Fix:** define x = deleted (0/1) and d = unsynced. "Set d on every local mark" after account deletion would re-upload everything on the next sign-in; state whether that is intended.
4. **Local unsynced place vs newer remote.** If local C changed offline after `sa` and the remote is newer, the adoption logic (`book.js:606-609`) overwrites local C. **Fix:** never adopt over a local place that hasn't synced yet; show the chip instead. A missing `sa` counts as unsynced.
5. **No-hash restore fights the browser.** On reload or back/forward, the browser restores its own scroll position, then the book jumps to C, for example in the middle of an excursion. **Fix:** restore only when the navigation type is `navigate`.
6. **Rotation, zoom and reflow are unhandled.** They can register as a step. **Fix:**
   - A change of width or DPR enters SETTLING and re-pins to C.
   - A change of `innerHeight` alone recomputes B and L and takes no step.
7. **`navB` must be a constant.** "Measured bottom" changes when the chapter nav isn't stuck (heroes, openers). **Fix:** use 48 + the chapter nav's `offsetHeight`.
8. **The hover strip catches parked cursors.** A stationary pointer passes the speed gate. **Fix:** open only on mouse movement inside the strip; close on scroll or wheel until the next pointermove.
9. **Resting marks look like the progress fill.** Slot vs fill contrast is only 1.08–2.2:1 (Part I verdigris vs fill 1.08, Part III Route vs fill 1.20). **Fix:** at rest show only the head and the saved mark. Show segments only when the line widens.
10. **Part I can't show hollow.** A 1px notch cannot be hollow, and the 6px "+" is marginal. **Fix:** make it a 3×6 notch.
11. **Readout contrast.** `.book-progress` is 10px at `rgba(255,255,255,.4)`, which is 3.77:1. That fails 1.4.3 now that it carries state. **Fix:** raise the alpha to ≥.5 (about 5.3:1).
12. **Label in Name (2.5.3).** The visible readout ("CH 4 · §03") is not contained in the accessible name ("Reading place: Chapter 4…"). **Fix:** start the name with the visible text and move the rest to `aria-describedby`.
13. **The Undo toast is timed and never focused (2.2.1).** **Fix:** keep Undo in the place bar until the next commit.
14. **Arrow keys in the radiogroup write marks.** Arrowing through it sets up to 5 marks and plays 5 motions. **Fix:** use `menuitemradio` items that commit on Enter, and specify focus on open and on close.
15. **Drag and the slider are blind.** Paragraphs carry no visible numbers, and the page doesn't scroll during a drag. The ¶ number taken from the id is wrong: `ch1-kernel-p10` follows `p8`, verified. **Fix:**
    - "Set to where I'm reading" is the main path, with an outline flash.
    - The nudge buttons scroll the target into view (counted as SETTLING).
    - Take ordinals from the offset table.
    - Consider dropping drag.
16. **Popovers don't follow the page.** A top-layer popover is fixed while the dot scrolls away. **Fix:** close it on scroll.
17. **Esc has no single owner.** The document handler exits fullscreen (`book.js:332`), and popover dismiss, slider revert and drag cancel all listen for Esc. **Fix:** one handler stack where each checks `defaultPrevented`.
18. **`snapshot()` reads live rects.** A virtual scrollY needs a new pure `anchorAt(y)` that copies `computeAnchor`'s containing/above/cap logic. **Fix:** write it, plus a parity test at 50 positions per part.
19. **A 401 keeps every call firing.** **Fix:** clear the JS hint cookie (`under_signedin=; Max-Age=0; Path=/; Secure`) and stop calls. Say "sign in" only in the footer and the place bar.
20. **Pins across devices are undefined.** Another device's tracking silently overwrites a pin, and a device that adopts a remote `src:'set'` has no PINNED state. **Fix:** define this, so that adopting a remote pin enters PINNED.

## LOW

- **Mark geometry:** `.book-nav` has a 1px bottom border, so with `bottom:0` the line sits at y 45–47 and the mark at 41–47, not 42–48. Decide whether to use `bottom:-1px`.
- **The 250-mark cap can never be reached:** the book has 116 sections in total. The 409 path and its test go untested.
- **Risk 3 is mostly about open tabs, not caches.** `_headers` sets no cache rule for `book.js`, so Pages revalidates it.
- **`:926` is really `book.js:931`.** Add `.place-bar` and `[popover]` to that exclusion list defensively.
- **The reduced-motion `opacity:.35`** changes how unmarked dots look today.
- **"Marked chapter tab" is really a section tab.**
- **"One setTimeout"** is unrealistic with about 8 timers. Specify one deadline queue.
- **Opening `C.part` from the index shelf now lands mid-part.** That is intended, but it surprises a reader who wants the opener.

## Missing from the spec

- **Unspecified behaviour:**
  - Multiple tabs.
  - Reload and bfcache.
  - Rotation and zoom.
  - Logout and account switching.
  - A purge mechanism.
  - The local-vs-remote rule.
  - Labels taken from K.
  - What the readout shows when C is in another part.
  - Disabling "Go to saved place" when the reader is already there.
  - The place bar's DOM position (right after `place-btn`, for Tab order).
  - Migrating v1 records (no `v` means `src:'auto'`).
- **Tests:**
  - An `anchorAt`/`computeAnchor` parity test.
  - Out-of-order POSTs.
  - A multi-tab trace.
  - The tooltip-focus freeze.
  - Label correctness at section starts.
  - A rotation trace.
  - Manual screen-reader traces.
  - A count of Tab stops.
- **Tuning:** a local-only `?utc-debug` overlay showing state, budget, K and R, with zero network. Thresholds tuned on paper need this for the owner's re-tune.
- **Owner decisions:**
  - Discoverability of marks (zero hints vs one line in the colophon).
  - Any overview of marks across the book (none exists; marks are visible only inside the current chapter).

