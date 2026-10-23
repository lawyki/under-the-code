# under-the-code — STATE

**OWNER CALLS DECIDED 2026-10-23 under the owner's delegation ("take the best option ... knowing the book's goal"; "reword for honesty on the legal / privacy"): 37 of 45 applied or kept (the Aleph One quote by the owner's own choice) on branch `owner-calls`, verified (blind retest, Gate 1 identical to `main`, clip 0, pass25 all pass), ledger `UNDER.md` §4af, decisions `docs/audit/decisions/owner-calls.md`. Not deployed: merging `owner-calls` into `main` and pushing waits for the owner's word (it also carries 3fd4774, the Go-deeper video guide). Still the owner's: Chapter 3's seven remaining calls (Claude's safety filter stops work on those figures), the marks-sync wording, the privacy notice's legal facts, and the read.** Before that: prose and figures frozen 1.0-rc2 (2026-10-17), deployed 2026-10-23 (merge fda8ce0); the book is still being built. Tagged `v1.0-rc2` at 92ed9f0; `v1.0-rc1` was 2026-10-15.

**Pass 31 at:** figure finalization (`docs/pass-31-brief.md`, ledger `UNDER.md` §4ag), branch `figures-final` from `owner-calls`, started 2026-10-23. Phase 0: both tracks open (author: contact sheets, prose subtraction, intents, kept-originals table; separate gate builder: tooling, frozen gate). Progress ticked in `docs/todo.md`, "Figure finalization". Nothing reaches `main` without the owner's word.

The resume header for this repo. `BRIDGE.md` is the architect charter;
`UNDER.md` §4 is the pass ledger; `README.md` says what the repo is.

**Pre-read audit, 2026-10-15 → 2026-10-17: DONE.** Every chapter, the Bridge and the outside-the-chapters findings decided, retested blind, gated and committed one chapter per commit on branch `pre-read-audit`; ledger `UNDER.md` §4ae; decisions `docs/audit/decisions/`; owner calls `docs/audit/owner-calls.md`. The outside fixes and Chapter 1 were deployed to the site 2026-10-17 ("deploy"), the rest 2026-10-23 (owner: "full yes, deploy"; merge fda8ce0 on `main`); the book is still being built.

**Pre-read audit, how it ran (owner, 2026-10-15: "verify the passes ... so I come back as little as possible"; ultracode on):** two workflows, both finished: round 1 (`book-audit`, run `wf_ba79ebb9-6bf`) and outside the sections (`book-audit-outside`, run `wf_f7f446b6-2cb`). Findings in `docs/audit/round1/` and `docs/audit/outside.json`. Every confirmed fix was written, retested, gated and committed per chapter (§4ae); tagged v1.0-rc2.

**Pass 29/30 at:** Pass 29 (language pass under law 4) DONE 2026-10-15. Pass 30 (every picture holds) DONE 2026-10-15, ledger `UNDER.md` §4ad: the shared pause control; intended messages for every figure, hero and the cover committed before any reader ran; Gate 2 with blind readers (figures 199 of 204 pass after two repair rounds, heroes and cover 17 of 20, icons all); Gate 1 at zero on every redrawn figure, hero and icon in Chromium and WebKit at every width, in the page and in fullscreen, in the still and at every sampled frame, except three findings left as owner calls; every page at zero in every `clip.mjs` mode, 31 containers that scroll on purpose listed (`UNDER.md` §5). Two Sonnet 5.5 verifications of every figure before and after. Owner calls: `docs/pass-30-owner-calls.md`; the owner's read starts at `docs/owner-read-map.md`. Then THE CLOSE (tag v1.0-rc1, 2026-10-15; §4ad).

**Pass 29 calibration (2026-10-11, cold reader `docs/pass-29-cold-reader.md` v1, Opus 5.5; record `docs/pass-29-calibration.json`):** planted gap (ch1-context-p4's definition of Turing's device removed) logged on the first try, as the reader's first point. Real runs: **ch1-context 10 search points, ch16-lockfree 4** (both under the 15-point floor). Its fact doubts (Turing "built" the Bombe; "historians estimate" two years and fourteen million lives for Bombe and Colossus alone; the Church–Turing thesis stated as fact; the halting framing credited to 1936; ch16-lockfree-p3 on x86 store order and coherence as a cause of reordering) go to the Part I and Part V fact gates, not to the count.

**Pass 29 Part I done (2026-10-11; ledger UNDER.md §4ac).** 24 sections through the per-section method and two repair rounds: ch2-gates repaired to zero search points, none already teaching at the first read, 23 with open points; 22 facts corrected (§4g); verified by Sonnet 5.5 (77 findings: 24 fixed in the text, the rest fixed in the glossary or ledger, queued for Pass 30, or listed as owner calls). Part I raised more owner calls than the brief allows per part (its hard stop), listed in `docs/pass-29-owner-calls.md`. Samples page for the owner: https://claude.ai/artifact/6g2HHNNv15C9uWhhTtJQiS (one addition, one cut, one list turned into argument).

**Pass 29 budget** (`node scripts/count-prose.mjs`; section prose, Passes 28 and 29 together; ceiling = 02f486b × 1.05, rounded down). The script reproduces §4aa's 02f486b counts exactly in all five parts, so no calibration differences.

| Part | 02f486b | Ceiling | Pass 28 close (7d56482) | Headroom |
|---|---|---|---|---|
| I | 12,095 | 12,699 | 12,098 (after law 4 and the Part I close: 12,807) | −108 |
| II | 10,891 | 11,435 | 10,898 (after law 4: 10,867) | 568 |
| III | 14,012 | 14,712 | 14,066 (after law 4: 14,597) | 115 |
| IV | 9,761 | 10,249 | 9,811 (after law 4: 10,883) | −634 |
| V | 6,181 | 6,490 | 6,187 (after law 4: 6,735) | −245 |

Not enforced since the owner's "No restrictions for now until I say so" (2026-10-15, §4ac). On `main` at eb7fe95, after the pre-read audit: I 13,089 (−390), II 11,396 (39), III 15,577 (−865), IV 11,562 (−1,313), V 6,820 (−330).

**Pass 30 tools** (built 2026-10-11; each reviewed by an independent agent and fixed): `tests/pass28/figs.mjs` (`--kind=figs|heroes|cover|icons|all`, widths 320 to 1440, `--motion` at 0/25/50/75 % of each cycle, `--fullscreen` at the fitted viewBox scale, contrast at 1440 from pixels: text 4.5, named marks 3 on the worse paint, icons 3, unrounded; helper `tests/pass30/contrast.mjs`; skips only from `docs/pass-30-exceptions.json`; a run that measures nothing exits 2), `tests/pass30/bare.mjs` (the svg alone, any selector, `--frames`, cover at its end state, collision-guarded output), `tests/pass28/clip.mjs` (adds 360, `--textsize=200` from 768 up, `--spacing` per WCAG F104, a `scroll` finding for any overflowing scroll container not listed in the exceptions, scroll-driven reveals cancelled so headings are measured, `--state=open` for closed details). For Gate 1 (done, §4ad): the first plain sweep's 250 scroll findings were fixed or listed (31 containers that scroll on purpose, `docs/pass-30-exceptions.json`, §5); every redrawn figure reached zero (Figs 14.3 and 14.6 since the pre-read audit). Known limit: the 200 % run scales rem/em text only (px-sized labels, captions, code, tables and chapter navs are not exercised).

**Paragraph id form** (checked 2026-10-11 against `book.js` `/-p\d+$/`, `tests/pass25/lib.mjs` `PARA_RE`, `traces.mjs`, `ui.mjs`, `build-sections.js`, `build-glossary.js`): `<section id>-p<N>`. A new paragraph takes N = one more than the highest N the section has ever used (current ids, `ANCHOR_ALIASES` keys, git history), so it never reuses an id; ids then run out of numeric order in the page, which nothing relies on (the code reads DOM order). Never run `scripts/add-anchor-ids.js` for this: it fills gaps from 1 and would reuse merged-away ids.

**Go deeper videos (owner request, 2026-10-12):** optional outside videos beside the text, never part of it (`public/deeper.js`, styles at the end of `book.css`, rules in README "Go deeper videos"). First one: Veritasium's Enigma video beside ch1-context-p8 (redesigned the same day after the owner rejected the first: now a margin note on wide screens, a small pill on phones, a dark viewer like the fullscreen figures). Nothing loads from Google before play (verified in Chromium at 1440, 900 and 375 px); the privacy notice (`/account#privacy`), README and LICENSE carry the embed and licence lines. Section prose, anchors and glossary unchanged. The site has no on-page licence notice; the licence line is in README and LICENSE.

## WHERE WE ARE

**READY at Pass 19 (2026-08-09); the current status is the header of this file.** Pass 19, the book-wide closing sweep, completed 2026-08-09
(ledger `UNDER.md` §4s) and declared the book prose-ready for the owner's
complete read. The language pass is complete across all five parts and
independently verified in all five — Part II's audit (Pass-15 verification)
landed 2026-08-10 in parallel with the read: 20 surgical fact fixes, three
fabricated-or-recast quotes replaced with verbatim sourced ones, every §4o
load-bearing correction reconfirmed, ledger under §4o. The coverage table is
now uniform. Its top owner flag is closed: a ratified one-word micro-pass on
2026-08-10 replaced `requestz` with `request` in the Ch7 pickle coda (the
documented Sonatype-2022 typosquat, 404 on PyPI; `requestz` is a real,
legitimate package) — the coda is otherwise untouched. The sweep before it
executed every ruled worklist item (fig 15.2 geometry re-laid; Ch15 →
"Attack and Defence" with the defence-spelling strays in part-1/part-3
brought along; the Diffie–Hellman en-dash migration with its glossary-key
merge; the house spelling convention ratified book-wide and recorded in
`UNDER.md` §5), ran the closing audits clean (cross-part consistency read —
four fact-class cross-reference breaks found and fixed; 462 hrefs + 519
glossary refs, 0 broken; figure sweeps 0 new findings against a
HEAD-identical baseline; full §7 harness 100/100; docs registries
realigned), and confirmed live parity after push. Anchor-id sets
byte-identical in all five parts (354/346/380/228/189).

**Pass 20 — figure-truth, Part II — landed 2026-08-17** (ledger `UNDER.md`
§4t, commit `cff08e3`): the Pass-15 verification's four flagged geometry
defects fixed and live — fig 6.1's "C++ released" marker moved from the
1995 tick to the 1985 tick (x=310, from the timeline's own mapping);
fig 4.5's RR and MLFQ lanes redrawn as legal traces of the figure's own
workload (13-slice RR ending t=26; MLFQ with every slice queue-labelled;
the 8.75/7.75 avg-wait labels recomputed and standing); fig 7.6's
BINARY_MULTIPLY line contained (rect 160→186). Anchors 346 byte-identical,
glossary 519 ±0, §7 spot-check 4/4, live parity confirmed. One new
punch-list flag: fig 7.6's eval-loop line overhangs its rect ~50 px/side
(pre-existing, same class).

**Pass 23 — the book-arc read — landed 2026-08-17** (ledger `UNDER.md`
§4w): the report-only whole-book pedagogy audit, one continuous Fable read
cover→glossary plus two blind mid-book entrants (Part III, Part V). Zero
edits to any book file. **Verdict: the arc holds** — the synthesis is
earned (Ch15's six-pattern unification and Ch18's trace cash the cover's
exact promises; the four disciplines are handed over three times), the
part-identity micro-arcs complete (position fixes → landfall, redactions
→ zero, listing lines → EOF, "Quorum reached · 5 of 5"), and "open any
part to begin" is true. Seven ranked findings for the punch list, top
three: Ch16 §03's memory-ordering peak leans on store buffers (taught
nowhere) and cache coherence (taught three sections later); Ch1's
locality-thread promise ("same equation, all the way up the stack") is
never picked up by name in Parts II–IV; the "What you now understand"
codas stop at Ch4, leaving Ch14/Ch16 without consolidation and Ch18's
title-echo unprimed. Full ranked list with locations and one-line
directions in §4w.

**Pass 25 — Place and Marks — landed 2026-10-09** (ledger `UNDER.md` §4y):
the saved place is now where the reader was *reading* (skims, look-ups,
pop-ups and fullscreen figures no longer move it; detours are remembered and
undoable), shown as a seamless 2 px cue on the bar that widens under the mouse
and can be dragged or set by hand from the place button; sections can be
marked in five colours per volume (glyph + texture, one hue family per slot,
all ≥ 3.05:1, colour-blind-checked — min ΔE 11.4 — with glyph and texture carrying the meaning), listed book-wide under "Your marks" on the
account page. Server-side marks ship **switched off** (`MARKS_SYNC = "0"`)
until the owner approves the privacy wording; place sync for signed-in
readers is unchanged meanwhile. Migration 0002 is applied in production.
**Verified 2026-10-10 by Sonnet 5.5** (§4y "Verification of Pass 25"): the
tracking model holds; 40 findings held — two HIGH (marks lost at sign-out
while sync is off; the place bar and menu clipped on short screens) — all
fixed and re-tested.

**Pass 26 — the dash law — landed 2026-10-10** (ledger `UNDER.md` §4z):
no em dash anywhere a reader sees (~2,860 rewritten, not swapped; enforced
by `npm run check:dashes`), verified by Sonnet 5.5 (20 findings fixed, one
old ARPANET fact corrected). Glossary 519 → 509 (eleven junk entries gone).
The three laws are in `CLAUDE.md`.

The book: five parts, 18 chapters plus the Bridge interlude, section prose 58,444 words (`node scripts/count-prose.mjs`, eb7fe95), 222 figures (18 kept original), glossary 484 entries (`public/glossary.json`). Five volume identities; accounts (password sign-in, email only to confirm and recover, passkeys off until the domain move) and exact reading-position sync; the §4g fact ledger survives in substance throughout.

## WHAT'S NEXT — the to-do list (in order)

Go-deeper test failures fixed 2026-10-15 (06eab33): viewer id `utc-deeper-viewer-title`, note and pill known tab stops; invariants 812/0.

1. **Marks sync on** once the owner approves `docs/pass-25-copy.md`: apply
   its five replacements in `public/account.html` (the first redrafted
   2026-10-23 against the intro the pre-read audit rewrote), set
   `MARKS_SYNC = "1"`, push.
2. **Domain move** (~early November 2026, owner's timing): set
   `SITE_ORIGIN` (wrangler.toml), redirect old URLs with `#anchor` intact,
   hand signed-out readers' local place (and Pass 25 marks) across the
   origin change; then passkeys on — test a real passkey against production
   D1 first, `PASSKEYS_ENABLED = "1"`, `utc-passkeys` meta → `on` in
   `public/account.html`, account intro copy may mention passkeys again.
3. **Retire `/api/auth/request`** after 2026-11-15 (replace with a 410).
4. **Re-tune the Pass 25 thresholds** after the owner's read (`?utc-debug`
   on any part shows the tracker's state; constants in `book.js` `T`).
5. **Passes 27–28: laws 2 and 3** (owner 2026-10-10, `CLAUDE.md`): 27 the
   cut, DONE (§4aa: 11.2 % shorter, glossary authored);
   28 figures DONE 2026-10-11 (§4ab; ledger `docs/pass-28-figures.md`: 204 of 222
   redrawn, 18 kept original (attack mechanics, resolved at the owner's request), fig 18.6's caption kept verbatim as the owner's closing claim; Parts I to V verified by Sonnet 5.5 and fixed; book-wide no-clipping and 60 fps checks at 0 findings, `tests/pass28/clip.mjs` and `smooth.mjs`), every figure one by one, handcrafted and
   tested, kept going by a loop (`docs/pass-28-brief.md`, incl. the owner's
   fig 1.2 note: the image explains itself, text goes into explainers).
6. **The punch-list pass**, after Tiger's read: the read's findings, the
   §4w arc dossier's seven ranked findings (Ch16 §03 scaffolding: store
   buffers glossed since Pass 29, recheck the rest; the locality thread, the
   coda instrument, the integer-overflow and De Morgan promises, the Ch14
   primer callback, the Ch17 §02 revisit gloss), the open §4o and §4s
   register flags, the default-blue "Chapter 16" link in Part I's
   Spectre/Meltdown strip (ch1-cpu-p11; no `.insight-text a` rule, §4y), the
   duplicate SVG title id `svgt-part2-1` (Ch4 hero and Fig 4.1), and the §6
   backlog items the owner approves.

**Model (owner ruling 2026-10-05, BRIDGE §5):** every pass runs on Opus 5.5;
each is followed by an independent Sonnet 5.5 verification.

**Done:** Pass 25 place and marks + its Sonnet 5.5 verification (§4y; 40
findings held, all fixed or recorded)  · Pass 23 book-arc read (§4w) · Pass 24 accounts v2 (§4x) · Pass 21
icons (§4u) · Pass 22 tabs + touch tooltips (§4v) · Sonnet verification of
21/22/24 with fixes · open-redirect fix · saved-title spacing fix · account
bookmark in the bar (all 2026-10-05 → 10-09). Owner's two old accounts
deleted at his request 2026-10-09 (backup: Google Drive → My Drive → _inbox →
mac → mac-cleanup-2026-10-15 → under-the-code-backups; the Mac copy went in
the 2026-10-15 cleanup). Pass 29 reader check: owner gave go without marks,
2026-10-11 (recall and precision tests not run).

## BLOCKED ON TIGER

Owner decisions and actions live here and nowhere else. If it is not on
this list, it is not blocking. Re-verified against `main` 2026-10-23
(workflow `open-calls-verify`; answered, superseded and duplicate items
removed, each removal checked by a Sonnet 5.5 skeptic).

**Deploy** (one word)

- **`owner-calls` → `main`**: the 36 decided calls, the honest privacy notice and the Go-deeper video guide (3fd4774). Say "deploy" and it is merged and pushed.

**Decide**

- **Pass 31 and the security figures**: Claude's safety filter stopped work on the book's attack and security figures three times on 2026-10-23, so Pass 31 leaves them as they are (Chapter 3's overflow and defence figures, Fig 1.12, Fig 2.9, the kept originals in Chapters 10 to 13, Chapter 15, the Spectre figures in Chapter 16). Edit them yourself, use another route, or keep them; every other figure goes through the pass.
- **Chapter 3's seven remaining calls** (`docs/audit/owner-calls.md`, Chapter 3; also on https://claude.ai/artifact/NAF7n8U6uuQ3kwdb8gwA15): Claude's safety filter stops work on those figures, so apply the recommended text yourself or keep them as they are.
- **Marks sync**: `docs/pass-25-copy.md` must first be redrafted against the new privacy notice; approval turns marks sync on.
- **The privacy notice's legal facts** only you have: YDT Holdings Oy's Business ID and address, the legal bases (account: contract; abuse limits and notices: legitimate interest?), the transfer basis for Cloudflare (a US company), whether hello@atheric.eu is read; and the colophon's © holder against LICENSE's, plus a CC BY-NC 4.0 line on the site (the colophon is your text).
- **Domain move**: your timing (WHAT'S NEXT item 2).

**Do** (needs you, not a decision)

- **Read the book**, starting at `docs/owner-read-map.md`. The punch list waits on the complete read. Older read-along notes: end of `UNDER.md` §4s.
- **Create your new account** at /account ("New here? Create an account"): the first real end-to-end email test of Pass 24. Report if the mail doesn't arrive.
- **Ten-minute screen-reader check**: `docs/pass-25-sr-trace.md` (VoiceOver on Mac/iPhone; NVDA if you have Windows). In the same sitting, on an iPhone: flick-scroll a part page hard and check the saved place does not jump (owed since Pass 25, §4y). Report what differs.

**Kept** (decided 2026-10-23 under your delegation: each stays as it is; say so if you want one changed)

- Pass 26 wording choices (§4z "Owner sign-off list": the Zen of Python's own punctuation, the shortened Berners-Lee pull-quote, the epilogue ornament, quote attributions, the Part V tagline order, the account notice and mails repunctuated).
- Pass 27 epilogue trims (§4aa Part V, "For the owner's sign-off").
- §4s read-along notes still open: the Amdahl pull-quote's silent capital, Chapter 15's title "Attack and Defence", the American "civilization".
- The cover's "A unified theory" (§4g flag: you may prefer "A visual theory").
- Found 2026-10-23, never listed before (`docs/audit/owner-calls.md`, "Found later"): Part II's closer as the audit changed it ("End of Part II", "The software layer is built."); the "3 nm" lines the audit corrected (your old ruling kept them); the account page wording the audit rewrote (you approved the earlier copy 2026-10-09); Figs 1.5 and 1.7's intended messages, revised with their fact fixes.
- The 18 kept-original figures stay as drawn (`docs/pass-30-owner-calls.md` §B; the alternative is a typography-only pass).
- `.kilo/agents/data.md`, `.claude/settings.json` and `shots4/`: tracked since your commit 7c2495b (a generic Kilo agent prompt and permission rules; no secrets).
- Permission rules for `.claude/settings.local.json` (your 2026-10-11 list): not written, not blocking while auto mode runs the work.
