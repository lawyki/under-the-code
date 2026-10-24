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

Phase 0, author track (the security figures are held: Claude's safety filter, STATE.md BLOCKED ON TIGER)
- [x] Branch `figures-final` (from `owner-calls`), `docs/pass-31-sealed/` gitignored, ledger §4ag and STATE "Pass 31 at:" opened
- [x] Contact sheets per chapter at 375 px, v4 and Enigma pinned (19 sheets, `npm run fig:sheet`; output gitignored)
- [x] Why Enigma is good, in one sentence (§4ag)
- [x] Prose subtraction, Part I (Ch1, Ch2, Ch3, the Bridge): 47 rows, 3 merge candidates, 2 cut candidates, 7 held
- [x] Prose subtraction, Part II (Ch4 to Ch7): 51 rows, 4 merge pairs, 2 cut candidates, 3 held
- [x] Prose subtraction, Part III (Ch8 to Ch12): 61 rows, 2 merge pairs, 2 cut candidates, 10 held
- [x] Prose subtraction, Part IV (Ch13 to Ch15): 34 rows, 1 merge pair (13.5+13.6), 0 cut candidates, 15 held (Ch15 whole, Ch13's query-safety section, Figs 14.3, 14.4, 14.6)
- [x] Prose subtraction, Part V (Ch16 to Ch18): 29 rows, 2 merge pairs (16.8+16.9, 17.7+17.8), 3 cut candidates (18.1, 18.3, 18.4), none held (Chapter 16 names Spectre only in prose, ch16-numa-p4). Ledger now has all 222 figures once: 35 held
- [x] Intent sentence per remaining figure (job tagged), raised where the blind prose reader asks for more: 187 intents (every figure not held, cut candidates included); 8 blind Sonnet 5.5 prose readers (`docs/pass-31-prose-readers.tsv`); 32 intents raised; asks for a different figure, or for expert depth, left out (law 4)
- [x] Kept-originals table (18 rows, errors and one action each): `docs/pass-31-kept-originals.md`; BR.3 redrawn in Phase 2, the 17 security originals held for the owner (fixes on `owner-calls` checked against `main`)
- [x] Ledger `docs/pass-31-ledger.tsv`, one row per figure: 222 rows; job, intent, knows and the subtraction record filled for the 187 open figures, 35 held; bin waits for Phase 1b (brief §10), the concept and gate columns for Phase 2

Phase 0, gate builder track (a separate agent; v3 sealed)
- [ ] `figlib`: `role` on `text()`, `obj()` groups, `Timeline` beat times
- [ ] `bare.mjs --no-text`
- [ ] `tests/pass31/sheet.mjs`, `check.mjs`, `gate.mjs` and their npm scripts
- [ ] Development set: v1 and v2 fail, v4 passes, three times each, order swapped
- [ ] Judge prompt frozen, hash in `docs/pass-31-calibration.md`

Phase 0 repairs (verification by session e2, 2026-10-24: "safe, but not ready for Phase 1"; no gate freeze and no exemplar ticked until these land)
- [x] Subtraction, Parts II to V, redone row by row: each row names the paragraphs reread and what the reader loses; the 12 weak keeps (1.13, 4.3, 5.2, 6.9, 7.2, 9.9, 12.1, 13.1, 14.1, 17.11, 18.2, 18.5) resolved: nine became cut candidates, 1.13, 14.1 and 17.11 stay with the reason
- [x] "knows" fixed where it cites a later figure or a cut or merge candidate (10.9, 3.1, 3.3, 6.9, 7.2, 18-trace, 18.6)
- [x] Intent split: `intent` becomes the takeaway (at most 20 words, one mechanism, at most two numbers, taught tokens, names the job); the new `content` column holds the names, numbers and fields; reader asks go to content or are declined with a reason; taught-yet record in `docs/pass-31-takeaway-check.md`
- [x] "Real thing" defined (draws a physical object, machine or place as it looks); 4.1, 9.2, 13.1, 17.8, 18.5 retagged
- [x] Brief amended: held status (§9, §13, §16, §17); §6's prompt rule stated as procedural; one exemplar a two-part merge card; the ledger's takeaway and content columns
- [x] Repairs, round 2 (e2's second verification at `7876daa`: 150 confirmed findings): 64 takeaways restate the drawn mechanism; caption-only terms count as untaught; content fixes on 9 rows, re-derived in full at Phase 2 step 1; 20 knows cells checked against their paragraphs; all 37 open Part I records redone and 59 in Parts II to V rewritten after reading every paragraph not under the hold; 11 status changes (ten merge pairs left); merged cards sit at the higher half's slot; brief §5 to §18 amended; Figs 1.5 and 13.5 exemplar fixes; taught-yet rerun pinned to `dd51d25`; calibration page sections 3 and 5 republished
- [ ] Gate builder follow-up (a fresh builder after the running one): an all-capitals token passes when its lowercase form does; taught abbreviations listed at the paragraph that teaches them; Enigma a must-pass under "real thing", three runs; development set rerun with the takeaway form; both forms logged
- [ ] Housekeeping: `figures-final` pushed; `figures-final-gate` pushed once its builder commits; §4ag records that the author wrote every subtraction row and the hedge-prompt glimpse

Phase 1 and the owner's calibration page
- [ ] Five exemplars (one per part, three concepts each) and `docs/pass-31-plates.md` (drafts done: Figs 1.5, 4.8, 10.3, 13.5 with 13.6 merged, 17.6; Gate 1, clip and the fact checker clean; plates written. Ticked when the frozen gate's mechanical checks pass)
- [x] Calibration page published (kept-originals table, exemplars, 3 best and 3 worst per part): https://claude.ai/artifact/FycKg4RsbcLdCqjT2xQgkk (2026-10-24; private to the owner; answers in its db collection `answers`, copied to `docs/pass-31-sealed/` when read)
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
