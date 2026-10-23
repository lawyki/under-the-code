# To do · Pass 29 and Pass 30 to v1.0 (owner, 2026-10-15: "Do them all, use a to do list")

Order follows `docs/pass-29-30-brief.md`. Ticked when committed and deployed to the site.

## Pass 29 · language pass under law 4

- [x] Part I rewritten (Ch1, Ch2, Ch3, the Bridge)
- [x] Part I open prose items closed (`docs/pass-29-part1-open.md`)
- [x] Part II rewritten (Ch4 to Ch7)
- [x] Part III rewritten (Ch8 to Ch12)
- [x] Part IV: Ch13
- [x] Part IV: Ch14
- [x] Part IV: Ch15
- [x] Part V: Ch16
- [x] Part V: Ch17
- [x] Part V: Ch18
- [x] Glossary check, book-wide (every entry authored, first uses deliberate)
- [x] Tests after Pass 29 (`tests/pass25`, dashes)

## Pass 30 · every picture holds

- [x] Shared pause and play control for animated figures (book.js, ui.mjs test)
- [x] Intended messages written and verified for every figure, committed before any describer runs
- [x] Describer calibration (planted untaught label in a Ch1 figure)
- [x] Part I: Gate 1 + Gate 2, repairs (incl. the 14 figure items in `docs/pass-29-part1-open.md`)
- [x] Part II: Gate 1 + Gate 2, repairs
- [x] Part III: Gate 1 + Gate 2, repairs (the locked captions are kept originals: reported in `docs/pass-30-owner-calls.md` §B)
- [x] Part IV: Gate 1 + Gate 2, repairs
- [x] Part V: Gate 1 + Gate 2, repairs
- [x] Heroes, cover, icons: Gate 1 + Gate 2
- [x] Frame drops on real devices (owner report)

## The close

- [x] Book-wide re-run: figs.mjs (--motion, --fullscreen), clip.mjs, smooth.mjs, tests/pass25
- [x] docs/owner-read-map.md
- [x] Tag v1.0 or v1.0-rc1 (v1.0-rc1: 12 owner calls open)
- [x] STATE.md freeze line

## Pre-read audit (owner, 2026-10-15: "verify the passes ... so I come back as little as possible")

- [x] Read: newcomer per section (116), facts, craft and figures per chapter (19 each), consistency per part (5)
- [x] Judge: every finding by a Sonnet 5.5 skeptic
- [x] Fix what is confirmed (one author), chapter by chapter, glossary regenerated after prose edits
- [x] Retest the fixes blind; Gate 1 on any changed figure; tests/pass25, check:dashes, clip
- [x] Ledger, owner calls, commit per chapter, push, tag


## After 1.0-rc2 (re-verified against `main` 2026-10-23)

Decision page for everything below marked "decide": https://claude.ai/artifact/NAF7n8U6uuQ3kwdb8gwA15

- [x] Re-verify every open owner call and STATE item against `main` (workflow `open-calls-verify`, Sonnet 5.5 skeptic on every closure): 43 open, not 49
- [x] STATE, owner calls, read map, RESUME, HANDOFF brought up to date (b2a0f1a)
- [x] Decision page rebuilt: 45 cards (36 audit, 7 Pass 30, marks wording, one "stays unless you object")
- [x] Owner delegated the calls (2026-10-23): 36 of 45 decided by the laws and the book's goal (`docs/audit/decisions/owner-calls.md`)
- [x] Applied on branch `owner-calls`, one chapter per commit; blind retest and one revision; Gate 1 identical to `main`; clip 0; pass25 all pass (§4af)
- [x] Privacy notice reworded for honesty, checked claim by claim against the code
- [ ] Deploy `owner-calls` (merge into `main`, push) on the owner's word
- [ ] Owner: Chapter 3's seven figure and caption calls (Claude's safety filter blocks them), the marks-sync wording (redraft first), the notice's legal facts (Business ID, address, legal bases)
- [ ] Owner does: create an account (first real mail test); VoiceOver check plus iPhone flick-scroll check (`docs/pass-25-sr-trace.md`)
- [ ] Owner reads the book, from `docs/owner-read-map.md`
- [ ] Punch-list pass after the read (STATE.md, WHAT'S NEXT item 6)
- [ ] Domain move and passkeys (owner's timing, ~early November); retire `/api/auth/request` after 2026-11-15

## Figure finalization (Pass 31, `docs/pass-31-brief.md`; ticked when committed and verified)

Phase 0, author track
- [x] Branch `figures-final` (from `owner-calls`), `docs/pass-31-sealed/` gitignored, ledger §4ag and STATE "Pass 31 at:" opened
- [ ] Contact sheets per chapter at 375 px, v4 and Enigma pinned
- [ ] Why Enigma is good, in one sentence
- [ ] Prose subtraction, Part I (Ch1, Ch2, Ch3, the Bridge)
- [ ] Prose subtraction, Part II (Ch4 to Ch7)
- [ ] Prose subtraction, Part III (Ch8 to Ch12)
- [ ] Prose subtraction, Part IV (Ch13 to Ch15)
- [ ] Prose subtraction, Part V (Ch16 to Ch18)
- [ ] Intent sentence per remaining figure (job tagged), raised where the blind prose reader asks for more
- [ ] Kept-originals table (18 rows, errors and one action each)
- [ ] Ledger `docs/pass-31-ledger.tsv`, one row per figure

Phase 0, gate builder track (a separate agent; v3 sealed)
- [ ] `figlib`: `role` on `text()`, `obj()` groups, `Timeline` beat times
- [ ] `bare.mjs --no-text`
- [ ] `tests/pass31/sheet.mjs`, `check.mjs`, `gate.mjs` and their npm scripts
- [ ] Development set: v1 and v2 fail, v4 passes, three times each, order swapped
- [ ] Judge prompt frozen, hash in `docs/pass-31-calibration.md`

Phase 1 and the owner's calibration page
- [ ] Five exemplars (one per part, three concepts each) and `docs/pass-31-plates.md`
- [ ] Calibration page published (kept-originals table, exemplars, 3 best and 3 worst per part)
- [ ] Validation run (Phase 1b) passed with zero false passes; final bins

Phase 2, chapters in book order (one commit each, retell included)
- [ ] Ch1
- [ ] Ch2
- [ ] Ch3
- [ ] The Bridge
- [ ] Drift check after Part I
- [ ] Ch4
- [ ] Ch5
- [ ] Ch6
- [ ] Ch7
- [ ] Drift check after Part II
- [ ] Ch8
- [ ] Ch9
- [ ] Ch10
- [ ] Ch11
- [ ] Ch12
- [ ] Drift check after Part III
- [ ] Ch13
- [ ] Ch14
- [ ] Ch15
- [ ] Drift check after Part IV
- [ ] Ch16
- [ ] Ch17
- [ ] Ch18
- [ ] Drift check after Part V
- [ ] Hard list: one more round of three concepts per part
- [ ] Heroes and the cover

Close
- [ ] READY page for the owner (before/after per part, cuts, below-bar list, validation result); deploy waits for his word
