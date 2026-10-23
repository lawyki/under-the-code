# under-the-code — STATE

**PROSE AND FIGURES FROZEN 1.0-rc2 (2026-10-17, after the pre-read audit). Open: the pre-read audit's owner calls (`docs/audit/owner-calls.md`, chapter by chapter) and the 12 from before (listed below). Next: the owner's read.** The 12: the eleven Pass 30 calls (`docs/pass-30-owner-calls.md` §A five figures and three heroes, §C three Gate 1 findings) and ch18-intersect-p3 from Pass 29 (owner text), each in BLOCKED ON TIGER. Start the read at `docs/owner-read-map.md`. Tagged `v1.0-rc2` on branch `pre-read-audit` (not merged; `main` and the live site carry only the outside fixes and Chapter 1); `v1.0-rc1` was 2026-10-15.

The resume header for this repo. `BRIDGE.md` is the architect charter;
`UNDER.md` §4 is the pass ledger; `README.md` says what the repo is.

**Pre-read audit, 2026-10-15 → 2026-10-17: DONE.** Every chapter, the Bridge and the outside-the-chapters findings decided, retested blind, gated and committed one chapter per commit on branch `pre-read-audit`; ledger `UNDER.md` §4ae; decisions `docs/audit/decisions/`; owner calls `docs/audit/owner-calls.md`. The outside fixes and Chapter 1 are live (deployed 2026-10-17, "deploy"); the rest goes live when the owner says so.

**Pre-read audit at (owner, 2026-10-15: "verify the passes ... so I come back as little as possible"; ultracode on):** two audit workflows running. Round 1 (`book-audit`, run `wf_ba79ebb9-6bf`): a newcomer reader per section (116), a fact checker, a craft/laws reader and a figure checker per chapter (19 each), a consistency reader per part (5), every finding judged by a Sonnet 5.5 skeptic. Outside the sections (`book-audit-outside`, run `wf_f7f446b6-2cb`): part openers, chapter leads, the cover and account pages, all 478 glossary entries, every cross-reference. Judged findings are copied to `docs/audit/` as they land (one JSON per chapter or batch: confirmed and owner verdicts with the fix). Next: I write every confirmed fix myself, chapter by chapter (working laws), one blind newcomer and one expert reader over each chapter's changed paragraphs, one revision; glossary regenerated; Gate 1 on any changed figure; tests; commit per chapter; ledger §4ae; tag v1.0-rc2. Progress is ticked in `docs/todo.md` ("Pre-read audit").

**Pass 29/30 at:** Pass 29 (language pass under law 4) DONE 2026-10-15. Pass 30 (every picture holds) DONE 2026-10-15, ledger `UNDER.md` §4ad: the shared pause control; intended messages for every figure, hero and the cover committed before any reader ran; Gate 2 with blind readers (figures 199 of 204 pass after two repair rounds, heroes and cover 17 of 20, icons all); Gate 1 at zero on every redrawn figure, hero and icon in Chromium and WebKit at every width, in the page and in fullscreen, in the still and at every sampled frame, except three findings left as owner calls; every page at zero in every `clip.mjs` mode, 31 containers that scroll on purpose listed (`UNDER.md` §5). Two Sonnet 5.5 verifications of every figure before and after. Owner calls: `docs/pass-30-owner-calls.md`; the owner's read starts at `docs/owner-read-map.md`. Then THE CLOSE (tag v1.0-rc1, freeze line above).

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

**Pass 30 tools** (built 2026-10-11; each reviewed by an independent agent and fixed): `tests/pass28/figs.mjs` (`--kind=figs|heroes|cover|icons|all`, widths 320 to 1440, `--motion` at 0/25/50/75 % of each cycle, `--fullscreen` at the fitted viewBox scale, contrast at 1440 from pixels: text 4.5, named marks 3 on the worse paint, icons 3, unrounded; helper `tests/pass30/contrast.mjs`; skips only from `docs/pass-30-exceptions.json`; a run that measures nothing exits 2), `tests/pass30/bare.mjs` (the svg alone, any selector, `--frames`, cover at its end state, collision-guarded output), `tests/pass28/clip.mjs` (adds 360, `--textsize=200` from 768 up, `--spacing` per WCAG F104, a `scroll` finding for any overflowing scroll container not listed in the exceptions, scroll-driven reveals cancelled so headings are measured, `--state=open` for closed details). For Gate 1: the plain clip sweep now reports 250 scroll findings (chapter navs, code blocks, wide tables), each to be listed with a §5 entry or fixed; contrast already fails on some redrawn figures (fig 1.2 at 1440: text min 2.7, 23 named marks); known limit: the 200 % run scales rem/em text only, so px-sized labels, captions, code, tables and chapter navs are not exercised by it (record beside the Gate 1 results).

**Paragraph id form** (checked 2026-10-11 against `book.js` `/-p\d+$/`, `tests/pass25/lib.mjs` `PARA_RE`, `traces.mjs`, `ui.mjs`, `build-sections.js`, `build-glossary.js`): `<section id>-p<N>`. A new paragraph takes N = one more than the highest N the section has ever used (current ids, `ANCHOR_ALIASES` keys, git history), so it never reuses an id; ids then run out of numeric order in the page, which nothing relies on (the code reads DOM order). Never run `scripts/add-anchor-ids.js` for this: it fills gaps from 1 and would reuse merged-away ids.

**Go deeper videos (owner request, 2026-10-12):** optional outside videos beside the text, never part of it (`public/deeper.js`, styles at the end of `book.css`, rules in README "Go deeper videos"). First one: Veritasium's Enigma video beside ch1-context-p8 (redesigned the same day after the owner rejected the first: now a margin note on wide screens, a small pill on phones, a dark viewer like the fullscreen figures). Nothing loads from Google before play (verified in Chromium at 1440, 900 and 375 px); the privacy notice (`/account#privacy`), README and LICENSE carry the embed and licence lines. Section prose, anchors and glossary unchanged. The site has no on-page licence notice; the licence line is in README and LICENSE.

## WHERE WE ARE

**READY.** Pass 19 — the book-wide closing sweep — completed 2026-08-09
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

The book: five parts, 18 chapters plus the Bridge interlude, ~93k words,
242 figures, glossary at **519** terms (the Diffie–Hellman duplicate row
merged in Pass 19 — see §4s item 3). Five volume identities live; magic-link
accounts and exact reading-position sync live; the §4g fact ledger survives
in substance throughout.

## WHAT'S NEXT — the to-do list (in order)

**For the Go-deeper (video) work, not Pass 29 (2026-10-12):** `tests/pass25` invariants fail 12 checks, all on Part I and all from Go deeper: the injected id `deeper-viewer-title` needs the `utc-` prefix, and the new tab stops (`button.deeper-note` on desktop, `button.deeper-pill` on phones) need adding to the tab-stop baseline (or the test told about them). Everything else passes.

1. **Marks sync on** once the owner approves `docs/pass-25-copy.md`: apply
   its five replacements in `public/account.html`, set `MARKS_SYNC = "1"`,
   push.
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
   §4w arc dossier's seven ranked findings (Ch16 §03 scaffolding, the
   locality thread, the coda instrument, the integer-overflow and De Morgan
   promises, the Ch14 primer callback, the Ch17 §02 revisit gloss), fig
   7.6's eval-loop line overhang (Pass 20), the open §4o register flags (two
   Part II hero-lead overclaims) and §4s register flags, the default-blue
   "Chapter 15" link in Part I's Spectre/Meltdown insight strip (§4y).

**Model (owner ruling 2026-10-05, BRIDGE §5):** every pass runs on Opus 5.5;
each is followed by an independent Sonnet 5.5 verification.

**Done:** Pass 25 place and marks + its Sonnet 5.5 verification (§4y; 40
findings held, all fixed or recorded)  · Pass 23 book-arc read (§4w) · Pass 24 accounts v2 (§4x) · Pass 21
icons (§4u) · Pass 22 tabs + touch tooltips (§4v) · Sonnet verification of
21/22/24 with fixes · open-redirect fix · saved-title spacing fix · account
bookmark in the bar (all 2026-10-05 → 10-09). Owner's two old accounts
deleted at his request 2026-10-09 (backup in `~/under-the-code-backups/`);
the live database is empty and ready for fresh sign-ups.

## BLOCKED ON TIGER

Owner decisions and actions live here and nowhere else. If it is not on
this list, it is not blocking.

- **Pre-read audit owner calls (2026-10-17): `docs/audit/owner-calls.md`.** Each with what, options and a recommendation, chapter by chapter: kept-original figures that now disagree with corrected prose (BR.3, 10.11, 11.7, 12.9, 12.10, 13.10, Chapter 3's and Chapter 15's attack figures), owner text (ch18-intersect-p3, the closing note's fragments, Fig 18.6's caption), and the account page's legal wording.
- **Pass 30 owner calls (11, 2026-10-15): `docs/pass-30-owner-calls.md`, each with a screenshot.** §A: five figures still failing Gate 2 after two repair rounds (BR.7 hexadecimal, 6.6 and 6.9 C++ notation, 10.3 TCP state names, 12.3 setTimeout and console.log) and three chapter heroes (Ch1 the dashed kernel link, Ch3 addresses and the stack-top register, Ch12 the braces); §C: Fig 14.3 and Fig 14.6 (Gate 1 findings believed false) and the cover (tinted cards, one-time entrance). Options: rule on each / let the next session apply every "recommended" option / accept all as they are. Recommended: the second (most are one label or one clause; two need a prose clause, BR.7 and 10.3).
- **ch18-intersect-p3, owner text (Pass 29 Part V, 2026-10-15).** The passage carrying the four moves (resolve into layers, follow the math, locate the security boundary, name the historical decision) is the book's claim about itself, so it was left as written. Two blind-reader findings: "market microstructure" and "distributed-ledger" are never taught; the sentence ending "a computational one they are trying to solve without the vocabulary" is hard to parse. Options: "how a market matches buyers and sellers ... a shared-ledger system (a blockchain, say)" and "whether they can recognise that a problem in their own field is a computational one, even when nobody has given them the words for it" / leave. Recommended: the rewrites.
- **Pass 29 Part I owner calls (more than the brief's 10 per part, so Pass 29 stopped after Part I).** Each, one line with question, options and recommended option: https://github.com/lawyki/under-the-code/blob/main/docs/pass-29-owner-calls.md (A: from the per-section method; B: verification findings left; C: kept-original figures). Options: rule on them / let the next session apply every "recommended" / keep the cap and leave them. Recommended: let the next session apply the recommended fixes for facts (section B) and decide the rest when you read.
- **Fig BR.3, kept original, contradicts §4g (verification H).** Its rows "SYSCALL or int 0x80" and "32 · timer (LAPIC)" repeat two corrected errors beside the corrected prose. Options: redraw those rows / accept. Recommended: redraw. Link: docs/pass-29-owner-calls.md, section C.
- **Pass 29 reader check (answered).** Read Chapter 1 §01 and Chapter 16 §03 at https://claude.ai/artifact/N35mfA7FsjTxboSLryWMxu as a newcomer would, and mark every place you had to stop and wonder (select the words, press Mark; a note is optional). Options: write go when you have marked / write go with no marks if nothing stopped you. Recommended: the first; the cold reader is compared against your marks before it touches Part I. Your answer: go. Owner gave go without marks, 2026-10-11; recall and precision tests not run.
- **Permission rules (not blocking).** The owner's 2026-10-11 list of `permissions.allow` rules for `.claude/settings.local.json` (node, npm, npx, git, python3, curl, cp, mv, mkdir, touch, chmod, sort, awk, tee, `pkill -f serve.mjs`, lsof; Edit, Write, Read, WebSearch, WebFetch, Artifact, ArtifactData, ArtifactComments, Workflow, Agent, Skill, ToolSearch, Monitor, ScheduleWakeup) was not written: Claude Code's auto-mode safety check refuses an agent editing its own permissions. Options: add them yourself (or run `/permissions`) / leave as is. Recommended: leave as is while auto mode runs the work; add them if prompts start to stall it.
- **Look at the figure pilot** (https://claude.ai/artifact/ADZTGFP5QqDEqq62E9Ebhn,
  three figures redrawn, before/after and live). One question: is this the
  direction for every figure? The work continues meanwhile; a change you ask
  for is applied to every figure already done.
- **Pass 28, Chapter 3's attack figures** (3.7 to 3.11): a redesign of 3.7 was
  stopped by a safety filter. Redraw them conceptually (the defences, without
  exploit mechanics) or keep the current ones?
- **Read the book.** The punch list waits on the complete read. Read-along
  notes: end of `UNDER.md` §4s.
- **Create your new account** at /account ("New here? Create an account")
  — the first real end-to-end email test of Pass 24. Report if the mail
  doesn't arrive.
- **Run the ten-minute screen-reader check** — `docs/pass-25-sr-trace.md`
  (VoiceOver on Mac/iPhone; NVDA if you have Windows). Report what differs.
- **Sign off the Pass 26 wording choices** (§4z "Owner sign-off list": the Zen
  of Python's own punctuation, the shortened Berners-Lee pull-quote, the
  epilogue ornament, quote attributions). Silence keeps them.
- **Sign off the Pass 27 epilogue trims** (§4aa Part V, "For the owner's
  sign-off": restatement cut from Ch18's math, trace, civilization, future,
  intersect, reading and final paragraphs; the book's closing paragraph and
  every changed claim were restored verbatim). Silence keeps them.
- **Approve the Pass 25 privacy wording** — `docs/pass-25-copy.md` (five
  short replacements on the account page). Until then marks stay on each
  device.
- **`.kilo/`** (another tool's folder, untracked in the repo): keep or delete.
