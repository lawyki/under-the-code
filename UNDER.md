# UNDER.md — Survey & Quality Log

A systematic survey of *Under the Code* (under.atheric.eu), taken 2026-07-06 as the
first structured quality pass since the book was written. This file records what the
site is, how it is built, what is strong, what was defective, what was fixed in
pass 1, and what remains for later passes. It is the working baseline for future
improvement work.

---

## 1. What the book is

An interactive HTML book: **5 parts, 18 chapters + one Bridge interlude, ~93,000
words, 242 inline-SVG figures** (222 diagram cards + 19 chapter heroes + the cover
art). Every figure is hand-drawn inline SVG, most with SMIL animation. No framework,
no bundler, no build step for the pages themselves — the tooling is
`scripts/build-glossary.js` (extracts defined terms into `glossary.json`) and
`scripts/add-anchor-ids.js` (bakes stable paragraph anchor ids into the part
files, added in pass 3 for reading-position sync; idempotent, collision-safe).

Published by Atheric (atheric.eu) as one of two proof-of-work products; deployed on
Cloudflare Pages from `public/`, auto-deploy on push to `main`.

### Page inventory

| Page | Role | Size |
|---|---|---|
| `index.html` | Cover, part shelves, full 18-chapter TOC | 23 KB |
| `part-1.html` … `part-5.html` | The book itself (3–4–5–3–3 chapters per part) | 313–473 KB each |
| `glossary.html` | Auto-built alphabetical index (JS-rendered from `glossary.json`) | 1 KB shell |
| `account.html` | Sign-in / account / privacy notice (pass 3; noindex, robots-disallowed) | 12 KB |
| `404.html` | Self-contained error page (own inline CSS, no book.css) | 3 KB |
| `book.css` / `book.js` | Shared core stylesheet + single shared script | 52 KB / 26 KB |
| `part-2.css` … `part-5.css` | Per-part identity layers (pass 4): tokens + furniture over book.css | 8–10 KB each |
| `fonts-part2.css` … `fonts-part5.css` + `fonts/` | Per-part self-hosted identity faces (css2 mirrors, OFL) | 130–470 KB/part |
| `fonts.css` + `fonts/` | Self-hosted webfonts (added in pass 1) | 16 woff2, ~270 KB total |

## 2. Architecture

**There is no client-side routing.** `book.js` is not a router — each part is a
plain multi-anchor document; navigation is ordinary links + URL hashes
(`part-2.html#ch5`). `book.js` is five self-contained IIFEs:

1. **Figure fullscreen** — expand/close buttons injected on every
   `.diagram-card`/`.light-diagram`; View Transitions morph; "liquid rainbow"
   ambient layer while fullscreen (opacity-only GPU animation, pre-painted in DOM).
2. **Section progress rail** — desktop-only left rail, rebuilt per chapter from the
   `.chapter-nav` items via IntersectionObserver.
3. **SMIL pause/resume** — every figure's SVG animations are paused offscreen
   (IntersectionObserver, 300px margin) and forced on in fullscreen;
   `prefers-reduced-motion` pauses everything permanently.
4. **Reading progress + resume + cross-device sync** (rewritten in pass 3) —
   position = deepest stable element id at the reading line + fractional offset,
   never raw scrollY. localStorage always (90-day expiry, "Where you left off"
   card on the index); when signed in, mirrored to `/api/position` (debounced 2 s
   idle, sendBeacon on pagehide/visibilitychange). A server position newer than
   local surfaces as a quiet dismissible "on your other device" chip. Signed-out
   readers generate zero API traffic — the JS-readable `under_signedin` hint
   cookie gates every call.
5. **Glossary** — fetches `glossary.json`, attaches hover/focus tooltips to
   `<strong>/<em>/.key-term` occurrences everywhere except each term's first-use
   section, renders the glossary index page, adds the index-footer link.

The CSS is one file in a strict vocabulary: design tokens in `:root`, component
classes (`.diagram-card`, `.pull-quote`, `.insight-strip`, `.math-callout`,
`.summary-table`, `.timeline`, `.truth-table`, `.code-block`, `.memory-diagram`),
scroll-driven animations behind `@supports (animation-timeline: view())`, print
stylesheet, reduced-motion block.

### Design system

- **Palette**: near-black surfaces (`#0a0a0a`/`#111`/`#1a1a1a`) + warm paper
  (`#f5f0eb`/`#ede8e3`) + gold accent `#d4a853` (dim `#8a6a2a`); semantic
  blue/green/red for figure content only.
- **Type**: Playfair Display (display/serif voice), DM Sans 300 (body), DM Mono
  (labels, code, figure text). Consistent mono-smallcaps labelling idiom
  (10–11px, 0.1–0.35em tracking) everywhere.
- **Reading rhythm**: dark part-openers/heroes alternate with paper content
  sections; figures are dark islands inside paper; `.lead` drop-caps open chapters.
- **Motion**: SMIL inside figures; scroll-driven fade/underline flourishes;
  reveal-on-scroll for structural furniture only (prose is deliberately static).

## 3. Strengths (verified, keep)

- **Zero console errors** on all 8 pages, desktop and mobile viewports.
- **Zero broken links or anchors** — all 600+ internal hrefs (including deep
  cross-part references like `part-3.html#fig-11-12`) resolve; verified by script.
- **All 241 planned figures exist** — `docs/figures.txt` registry is 100% `[x]`,
  matches the HTML exactly; every SVG has a `viewBox`.
- **Disciplined CSS** — effectively no undefined classes in the HTML, no duplicate
  IDs, one shared stylesheet with a real token system.
- **Genuinely considered performance engineering**: SMIL paused offscreen, the
  fullscreen rainbow layer pre-painted + opacity-only, `contain` used deliberately,
  scroll-driven effects behind `@supports`.
- **Accessibility above static-site baseline**: `prefers-reduced-motion` honored in
  both CSS and JS (SMIL), keyboard/focus support on glossary terms, aria-labels on
  injected buttons, skip-safe print stylesheet.
- **Self-containment**: no analytics, no trackers, no CDN; state (progress,
  glossary cache) never leaves localStorage. As of pass 1, **zero third-party
  requests of any kind** (fonts now self-hosted).

## 4. Defects found & fixed in pass 1 (2026-07-06)

Objective breakage only; no restyling, no content changes.

| # | Defect | Fix |
|---|---|---|
| 1 | **Google Fonts loaded from fonts.googleapis.com/gstatic** on every page — the studio posture is zero third-party requests | Self-hosted: `fonts.css` mirrors the css2 payload (same families/weights/subsets/unicode-ranges → pixel-identical rendering); 16 woff2 files under `fonts/`; preloads for the five latin faces every page uses; all 8 pages switched. Playfair + DM Sans are variable fonts (one file per subset serves all weights); DM Mono is per-weight. |
| 2 | **Mobile horizontal page scroll** (375px and 320px) on parts 1–3 — wide `.summary-table`s (up to 618px), the ch4 `.memory-diagram`, and a long inline-`code` URL in ch11 pushed the whole page wide | `.summary-table` becomes a horizontal scroll container ≤768px; `.memory-diagram { overflow-x: auto }`; `code { overflow-wrap: anywhere }`; `.truth-table` given `max-width:100%; overflow-x:auto` as a guard. Verified: no page-level overflow at 1440/375/320 on any page. |
| 3 | **Fixed header height was unpinned** — `.book-nav` was padding-sized (real height 54px desktop; wrapped to 79–105px on phones) while `.chapter-nav { top:48px }` and `.part-opener { margin-top:48px }` assume 48px → sticky nav slid under the header and page tops were overlapped on mobile | `.book-nav` is now exactly `height:48px`, one line at every width: subtitle hidden ≤960px (new `.book-title-sub` span), part/chapter readout hidden ≤620px. Verified 48px at all three viewports. |
| 4 | **No way home** — no link to the cover anywhere on a part page (`.book-title` was a plain `<div>`) | Title is now `<a href="index.html">` (visually unchanged, `color:inherit`, no underline). |
| 5 | **Dead-end part endings** — every "End of Part N" section stopped with no affordance to continue; the `.next-btn` class existed in CSS but was used 0 times (unrealized design intent) | Each part's closing section now carries one `.next-btn`: parts 1–4 → next part, part 5 → back to the cover. |
| 6 | **`og-image.png` was broken** — the committed raster (macOS `qlmanage`) was mis-composed: title cropped off-canvas, white band at the bottom, wrong layout. This is what every social share showed | Re-rendered from `og-image.svg` in headless Chromium at 1200×630 @2× with the self-hosted fonts. Now matches the SVG exactly. |
| 7 | **Metadata inconsistencies** — README claimed "~210 figures" (actual: 242 incl. cover, as the cover itself states); `package.json` said `UNLICENSED` while the repo is CC BY-NC 4.0 | README count corrected with breakdown; `license: "CC-BY-NC-4.0"`. |
| 8 | **Index carried a `.liquid-bg` layer it can never use** (only fullscreen figures activate it; the index has none — glossary.html correctly ships without it) and its two infinite drift animations idled forever | Removed from `index.html`. |

## 4b. Defects found & fixed in pass 2 (2026-07-06)

Pass 2 was two-track: a pedagogical read of the whole book as a learner (defect
classes: incomplete explanations, missing connective tissue, figure defects) and
the register-neutral mechanical items from §6.

### Pedagogy — figures (the largest track)

A scripted sweep sampled every figure's SMIL timeline (0–12 s) and compared the
union content bbox against the `viewBox` on all 242 SVGs. **27 figures overflowed**
their frame; a per-element pass then named each offender. All fixed, and the sweep
now reports **0 overflows**. Two root causes dominated:

- **Broken SVG foreign content (3 figures: 15.7, 14.2, 18.5).** HTML `<span
  class="key-term">` / `<em>` had been used inside SVG `<text>`. HTML tags inside
  SVG text force the parser out of foreign-content mode, so roughly half of each of
  these figures was rendering as ghost HTML *below* the SVG. Replaced with plain
  text / SVG-native `<tspan font-style="italic">`. (A book-wide scan found only
  these; `<em>` in figs 14.2/18.5 was the same bug and was swept up too.)
- **Text/box overflow (23 figures).** Long caption/annotation lines and labels ran
  past the right or bottom edge and were clipped by the card. Fixed per figure:
  wrapped long lines, right-anchored or shortened labels, rescaled fig 5.10's bar
  row, extended `viewBox` height where the layout genuinely needed the room (2.8,
  2.12, 3.6, 15.1, 18.1), and flattened fig 14.11's message arrows off the text
  they were crossing.
- **Flash-at-origin (26 animated circles, book-wide).** Dots animated with
  `<animate attributeName="cx/cy">` but no base `cx`/`cy` rendered at the SVG origin
  (0,0) until their delayed `begin` fired. Added base coordinates (and `opacity="0"`
  where a delayed fade-in applies).
- **Invisible caption emphasis (CSS).** `p strong { color: var(--text-dark) }` and
  the default link color made `<strong>`/links inside dark `.diagram-caption`
  near-black on the dark card. Restated both for the dark ground, with
  `.light-diagram` overrides.

### Pedagogy — prose

The book's connective tissue is genuinely strong: every chapter closes with a
"What you now understand" / explicit "seam to Chapter N", and every part has an
opener + closer that states why the next layer exists. No missing-seam defects were
found. Two **incomplete-explanation** defects were — concepts whose *outcome* was
stated but whose load-bearing *mechanism* lived only in a figure caption or nowhere.
Both extended in the book's own narrative register (mechanism first, then anchor):

- **Ch2, two's complement (part-1).** "Subtraction is just addition… the bits work
  out — the carries cancel in exactly the right way" was the whole justification.
  Added the modular-arithmetic reason: negation is 2ⁿ − x, so a + (−b) = 2ⁿ + (a −
  b); the 2ⁿ is a 1 one place past the register's widest bit, it falls off the end,
  and a − b remains. The wheel figure (2.8) that follows is now the intuition anchor
  for a stated mechanism, not a substitute for one.
- **Ch14, Diffie–Hellman (part-4).** Prose asserted both parties "end up knowing the
  same secret" and Fig 14.7 shows both landing on 2, but the reason they *must*
  coincide — exponentiation commutes, (gᵃ)ᵇ = (gᵇ)ᵃ = g^ab — appeared nowhere.
  Added the one line of algebra plus why the eavesdropper's remaining step runs
  backward against the discrete-log asymmetry.

### Mechanical (§6 items)

| # | Item | Fix |
|---|---|---|
| 1 | **308 redirect chain** (§6 P3.12): every internal href used the `.html` form while Cloudflare serves extensionless, costing a 308 per navigation; canonicals pointed at `.html` while readers land extensionless | All internal hrefs, canonicals, `og:url`, and `sitemap.xml` locs rewritten extensionless (`/part-1`). `book.js` now strips `.html` wherever it derives the current page or builds a glossary/resume href — which also fixes a latent bug the 308 already caused: same-page glossary links rebuilt as `part-N.html#x` (full nav + redirect) instead of a bare in-page anchor. `build-glossary.js` stores the page ref extensionless. |
| 2 | **glossary.json re-fetched per page** (§6 P2.5) | `public/_headers` gives `glossary.json` `max-age=86400, stale-while-revalidate=604800`, so navigations within a day are served from cache with no network; the localStorage parse-cache (keyed by the `generated` stamp) still short-circuits parsing. Fonts get a 1-year immutable cache. glossary.json regenerated (stale since 2026-05-04): 516 terms, extensionless parts, definitions/sections refreshed to current HTML. |
| 3 | **Figure a11y** (§6 P1.1): 222 diagram SVGs had no `role`/`<title>` link | Every in-book figure already had a descriptive `<title>`; added `role="img"` + `aria-labelledby` (unique `<title>` id) to all 241 figure SVGs + the cover. Verified 0 unlabelled. |
| 4 | **No favicon** — every load logged a `/favicon.ico` 404 (a real console error the §7 exit claim missed) | Inline SVG data-URI favicon (gold "U" on near-black) on all 8 pages. Data URI = no request, so zero-third-party holds. |

### Pass-2 verification (2026-07-06, second model, same day)

An independent audit of the pass-2 commits. Verdicts on the prior work: the
mechanical track shipped correctly (extensionless hrefs/canonicals/sitemap,
`_headers` caching, a11y labelling all verified independently — a corrected
a11y scan that excludes the injected fullscreen-button icon SVGs reports 0
problems on all 241 figure SVGs); the two prose insertions targeted the right
gaps and were kept, with register corrections (both opened with the same
"not luck" move — a tell, the phrase appears nowhere else in the book; math
markup normalised to the book's `<em>` idiom; "meet in the middle" dropped
from the DH paragraph — loaded phrase one chapter before MITM attacks).

The figure track was sound but its **sweep had a blind spot**: it compared
content bboxes against the `viewBox` only, so text crossing the border of its
own *card inside the frame* passed. A text-vs-containing-rect scan plus
screenshots of all 45 touched figures found 13 more defective figures, all
fixed (commit `def7bc0`):

- **Fig 13.5** — the ACID table was drawn *on top of* both scenario panels,
  occluding their RECOVERY rows. Moved below; viewBox extended.
- **Fig BR.3** — IDT handler names crossed the table edge; row 128's cause
  and handler overlapped each other.
- **Fig 3.10** — bottom caption sat on both cards' bottoms; gadget comments
  overflowed. **Fig 4.13** — journal-entry lines ran ~40px past their boxes.
  **Fig 6.5** — the C error-path line overran the card. **Fig 11.12** —
  ROOT/INTERMEDIATE/LEAF sub-lines wider than their boxes. **Fig 12.11** —
  CSP verdicts crossed the row edge. One-line overflows in **15.1, 15.6,
  15.9, 15.10, 16.5, 16.11, 17.10**.
- **Fig 15.7** — the prior pass had shrunk the vendor labels to satisfy its
  viewBox sweep while they still crossed the row border by ~30px (a
  metric-satisfying fix, not an actual one). Labels moved to the title line,
  right-anchored at the card's inner edge.
- **Flash-at-origin, `animateMotion` variant** — the prior cx/cy fix missed
  delayed `animateMotion` dots (5 circles, figs 2.x gate/transistor + 9.11),
  which sit at the SVG origin until their first `begin`. Base `opacity="0"`.
- **Fig 4.11** — "madvise" lane label still clipped after the prior
  shortening; both thread labels moved above their lanes.
- **Fig 15.1** — "DDoS" as an *example of* denial-of-service is circular;
  now "resource exhaustion".

Prose hunts re-run independently: ten high-risk explanations sampled across
all parts (B-tree, SHA-256 rounds, AES modes, TCP/AIMD incl. Chiu–Jain,
Paxos/Raft quorum intersection, FLP, CAP, floats, GIL, DH) — mechanism
present in every one; all four part closers → openers verified. No further
incomplete-explanation or missing-seam defects; the pass-2 assessment of the
connective tissue stands.

**Lesson for future passes:** a bbox-vs-viewBox sweep is necessary but not
sufficient; pair it with a text-vs-containing-rect scan *and* screenshots of
every touched figure. Metrics can be satisfied while the defect remains.

## 4c. Pass 3 (2026-07-06): accounts + exact reading-position sync

Additive feature pass, not a defect pass. Goal: "continue reading" restores the
reader's exact position, every time, across devices. Signed-out experience is
byte-identical in behavior (verified: zero `/api` requests signed out).

### Position unit — what "exact" means

Anchor = **deepest stable element id at the reading line** (56 px, just under
the 48 px header) **+ fractional offset within that element**. Never raw
scrollY — it breaks across viewport widths and font settings. Granularity:
chapter (`ch7`) → section (`ch7-locks`) → paragraph/figure (`ch7-locks-p4`,
`fig-7-3`). Sections and figures already had ids; `scripts/add-anchor-ids.js`
baked **816 paragraph ids** into the five part files (literal text in the HTML,
so hand edits never renumber; re-runs only fill gaps, collision-checked).
Restores self-correct once after layout settles (late font reflow, smooth-scroll
tail), cancelled if the reader scrolls meanwhile — verified pixel-exact against
the stored fraction at 1440 and 375.

### Architecture (server)

- **Auth: self-hosted magic links.** `POST /api/auth/request` → one-time token
  (SHA-256 stored, 15 min TTL, ≤3 outstanding per address) → emailed link.
  `GET /api/auth/verify` renders a confirm page and does *not* consume (mail
  scanners prefetch GETs); the button `POST`s, consumes atomically
  (`DELETE … RETURNING`), sets a `__Host-` HttpOnly session cookie (180 d,
  hashed in D1) + the `under_signedin` hint. `/me`, `/logout`, `/delete`
  (full erasure: position, sessions, tokens, user row). No passwords, no OAuth,
  no third-party identity.
- **Storage: Cloudflare D1** (`under-book`, EEUR) — `users`, `login_tokens`,
  `sessions`, `positions` (one row per user). Schema in `schema.sql`.
- **Email: Cloudflare Email Sending via its REST API** — Cloudflare's native
  service; even the mail hop has no third-party provider. The `[[send_email]]`
  binding is Workers-only (Pages config validation rejects it — learned from a
  failed deploy), so the Function POSTs
  `accounts/{id}/email/sending/send` with an `EMAIL_API_TOKEN` Pages secret.
  **Owner action still required**: Workers Paid plan + enable Email Sending for
  `atheric.eu` (+ its DNS records) + set the secret. Until then
  `/api/auth/request` returns a clean 503 and the account page says delivery
  is unavailable; on localhost the API echoes the link (`devLink`) so the flow
  is fully testable without mail. *(Resolved: owner completed this and
  verified live delivery — see §6 P0, 2026-08-01.)*
- Pages Functions live in `functions/api/*`; `wrangler.toml` carries the
  bindings (`pages_build_output_dir = "public"`). `_lib.js` is not routed
  (verified 404).

### Client

Rewrote book.js IIFE #4 (see §2). Entry point is one quiet footer link on the
index ("Keep your place across devices →" → `/account`; swaps to "Reading
sync · on" when signed in). The offer is a dismissible bottom chip in the
book's grammar (mono eyebrow + serif italic link), never a modal, hidden in
print, inert under reduced-motion (global transition kill). Cross-page exact
restore hands the fraction through `sessionStorage` (resume card and
cross-part chip). Position writes are whitelisted server-side (part/anchor
regex, fraction 0–3, labels ≤200 chars, body ≤2 KB).

### Privacy

The book had no notice; it now does — `/account#privacy`: what is stored
(email, hashed session ids, one reading position), purpose (sign-in + resume,
nothing else), where (D1 in the EU, Cloudflare Email Sending), retention
(links 15 min, sessions 180 d, position until overwritten/deleted), deletion
(self-serve button + `hello@atheric.eu`), operator (YDT Holdings Oy). The
studio privacy page (atheric.eu/privacy) scopes itself to the studio site and
is not referenced by the book, so it needed no change. `/account` is noindex
(meta + `X-Robots-Tag`) and robots-disallowed along with `/api/`.

## 4d. Pass 4 (2026-07-06): the five-volume identity build

Owner-approved identity pass: each part becomes a complete distinct brand while
Part 1 keeps the original grammar unchanged. Four proposed identities (Greenbar,
Chart Room, Strongroom, Quorum) were approved as proposed and built one part per
sub-pass, each verified in Chromium **and** WebKit at 1440 + 375 (0 console
errors, 0 external requests, no page h-scroll, `.book-nav` 48px) before the next.

### Architecture

- **Identity layer per part**: `part-N.css` loaded *after* `book.css` redefines
  the design tokens (`--dark`, `--warm-*`, `--accent`, `--text-*`, `--sans`,
  `--mono`) and restyles reading furniture (openers, heroes, headings, leads,
  quotes, plates, code, tables, timelines, buttons). `book.css` is untouched —
  part-1, index, glossary, account render byte-identically from it.
- **Fonts**: `fonts-partN.css` + woff2 under `fonts/` — local css2 mirrors
  (latin + latin-ext, same unicode-ranges), pass-1 convention. Per part:
  II IBM Plex Mono/Sans · III Space Grotesk/Karla/Space Mono ·
  IV Fraunces/Spectral/Courier Prime · V Syne/Manrope/JetBrains Mono.
  All OFL, ~130–470 KB per part, each page loads only its own. Zero third-party
  holds.
- **Figure recolor**: scripted rewrite of the SVG color literals in each part
  file — the *identity* families only (gold `rgba(212,168,83,α)` + dim golds +
  neutral steel `rgba(180,200,220,α)` + dark panel hexes), **alphas preserved**;
  the semantic red/green/blue families are pedagogical grammar and were left
  untouched in all parts. SVG `font-family="DM Mono"` follows each part's mono;
  Playfair inside figures (the author's voice) stays everywhere.
- **Invariant spine** (explicitly re-pinned in every part css): the 48px black
  `.book-nav` (Playfair + DM Mono + gold em), glossary tooltips, fullscreen
  chrome, resume/sync chips, account/colophon — the gold thread that marks the
  five volumes as one curriculum. The index shelves now carry five spine
  stripes + numeral hues (I gold · II phosphor · III cyan · IV seal · V violet),
  home grammar otherwise.
- **What "invariant" means** (ratified pass 5): the invariant is *grammar and
  structure* — the spine thread above, the component vocabulary (`.diagram-card`,
  `.insight-strip`, `.pull-quote`, `.chapter-nav`, openers/heroes/leads),
  the pedagogical red/green/blue figure grammar, anchor ids, and the 48px nav.
  **Reading typography is per-identity, by design.** Each volume may set its own
  body face, accent, plate colour, and even reading model — Part IV's
  serif-on-cream ledger body (Fraunces/Spectral) is deliberate Strongroom
  identity, *not* a regression to be "fixed" back to the sans reading default.
  Restyle the surface freely per volume; never break the grammar underneath.

### The four identities and their motif-evolution schemes (cyclic, hand-set)

Every recurring motif returns across its part's chapters, never identically —
the design advances with the content. All variation is hand-placed (no
randomness). Auditable by grepping the literals below.

- **II — Greenbar** (the printed program listing; IBM Plex, phosphor terminal
  plates `$`-prompt labels + scanlines, listing paper with greenbar banding,
  sprocket rails beside the text column, discrete/stepped motion, block-cursor
  on opener/closer h1).
  *Evolution*: each hero's `LISTING` meta line advances a cumulative line-range
  and build command — ch4 `lines 0001–0790 · cc -c kernel.c` → ch5
  `0791–1608 · cc unix.c` → ch6 `1609–2413 · c++ objects.cc` → ch7
  `2414–3199 · python3 readable.py` (compiled → interpreted mirrors the
  content); the banding re-inks at every chapter head and fades to
  near-subliminal past the lead (owner mitigation); the closer prints
  `EOF · 3199 lines · 4 modules`.
- **III — Chart Room** (cable chart / blueprint; Space Grotesk/Karla/Space
  Mono, Prussian plates with 36px grids + surveyor's corner ticks, legend-box
  captions, continuous-flow motion — ambient dash drift on the route arc).
  *Evolution*: the part is a cable-laying voyage. `POSITION FIX` meta lines
  advance London → New York across ch8–ch12 (`51.51°N 0.09°W · 0 nm` →
  `40.71°N 74.01°W · 3,129 nm · landfall` — landfall at the browser chapter;
  runs recomputed in pass 7 so each leg is the true great-circle distance
  between successive fixes);
  the opener chart shows the route ahead with 1 of 5 waypoints lit, the closer
  the same route completed (all 5 + `LANDFALL`).
- **IV — Strongroom** (ledger + sealed dossier; Fraunces/Spectral serif body
  (approved)/Courier Prime, ledger stock with double-rule section margins,
  rubber-stamp part/chapter labels, double-framed dossier plates, lock-step
  motion — stamps land once on scroll entry).
  *Evolution*: the dossier declassifies as the reader learns. Stamp angles vary
  per chapter (ch13 −2° · ch14 +1.2° · ch15 −1°; closer tilts opposite the
  opener); each hero's redaction row loses bars — ch13 three bars
  (`§3 redactions remain`) → ch14 one → ch15 none
  (`nothing remains redacted` at Attack & Defense).
- **V — Quorum** (many machines as one; Syne/Manrope/JetBrains Mono,
  void-indigo constellation openers, violet + teal accents in phase, gradient
  display type at **headline scale only** (owner mitigation), 20px glass
  plates with a phase-offset status dot, phase-sync motion).
  *Evolution*: the constellation gains nodes as the curriculum completes — the
  opener draws the five *parts* as stars with I–IV lit and V hollow, breathing;
  `End of the Book` shows all five lit and fully meshed
  (`QUORUM REACHED · 5 OF 5`). `CLUSTER` meta lines zoom out
  `1 machine · 8 cores` → `10,000 machines · 3 regions` → `one curriculum ·
  five layers · one reader`; hero auroras phase-shift violet → teal across
  ch16–18.

### Pass-4 exit state (2026-07-06, LIVE at under.atheric.eu)

Deployed (commits cd40d88…f1ef465) and re-verified against production —
index + parts 2–5, Chromium + WebKit, 1440 + 375: 0 console errors, 0 external
requests, no h-scroll, nav 48px; all identity CSS/font assets serve 200.
Previously verified locally against the Cloudflare-mimicking server, Chromium + WebKit,
1440 + 375, per part and again for index/part-1/glossary/account/404:
0 console errors, 0 external requests, 0 page-level horizontal scroll,
nav 48px, all five part font sets confirmed loaded via `document.fonts`.
Reduced motion: all new animations are CSS (cursor blink, route drift, stamp
landing, constellation breathing) and die under the global reduced-motion
kill; SMIL handling unchanged. Print: banding/rails/arcs/constellations and
gradient text are explicitly reset in each part css print block.

## 4e. Pass 5 (2026-07-06): identity-friction fixes

Four confirmed friction findings from a read of the shipped identity build,
where the per-part identity layer collided with the spine text or fell below a
comfortable-read bar. Register-neutral repairs inside each volume's existing
idiom — no new design, no anchor-id changes. Each verified in Chromium **and**
WebKit at 1440 + 375, 0 console errors. The ratified typography principle is
recorded in §4d ("What invariant means"): Part IV's serif-on-cream body is
intentional and was **not** touched.

| # | Finding | Fix |
|---|---|---|
| 1 | **Fig 8.4 (Part III) three-element overprint** — the salmon "fibre" data-point label overprinted the green Shannon annotation *and* formula at the top-right of the SNR curve | Relocated only the fibre label into the open area just below its data point, with a short salmon leader to keep the association. Formula + annotation left in place; all three now legible. `part-3.html`. |
| 2 | **Part V end-of-book footer** — the full-bleed `.qm-const` mesh painted *over* the closer prose: the `QUORUM REACHED · 5 OF 5` chip overprinted "…security boundary", and the I–V node labels sat on the running text | **Z-order + clearance.** `.part-opener` is now `isolation: isolate`; the mesh is `z-index:0`, the spine text `z-index:1` — the identity layer can never sit above spine text again. The two SVG text layers (roman numerals + the QUORUM chip) were lifted out of the prose band: numerals dropped at the closer, and `QUORUM REACHED · 5 OF 5` re-set as a legible in-flow `.qm-quorum` caption above the button. The remaining 5-node mesh is dimmed to a true backdrop (lines .16→.10, dots .95→.5) so no bright node competes with prose. Top opener unchanged (verified). `part-5.html` + `part-5.css`. |
| 3 | **Section nav (`.chapter-nav`, all parts) clipped its last tab** with no scroll affordance — a hidden scrollbar (macOS/iOS) gave no hint the 6–7 section tabs scroll (always on mobile, on narrow desktop for 7-tab chapters) | A CSS fade at whichever edge has off-screen tabs, appearing **only** when actually scrollable and hiding at the scroll end. Horizontal inset moved from nav padding → item margins (`--nav-inset`) so the sticky `::before`/`::after` fades pin to the true edges; per-part `--nav-bg` colours the fade; a small `book.js` IIFE toggles `[data-navscroll~="more-left|more-right"]` from scroll/resize state. `book.css` + `book.js` + part-3/4/5 css (`--nav-bg`). Last tab is never clipped at scroll end. |
| 4 | **Takeaway strips (`.insight-strip`) accent under-contrast, Parts IV/V** — emphasis is weight-400, so colour is the only signal, and `--sr-seal` (~6.9:1) / `--qm-violet` (~6.8:1) read *dimmer* than the ~9.5:1 body, so the emphasised phrase de-emphasised itself | Lifted the strip accent to ~9:1 (matching the body): Part IV seal → `#e6a892`, Part V violet strong → `#bca8ff`. Strip-scoped (the `.insight-*` classes are strip-only); the global `--sr-seal` / `--qm-violet` tokens are unchanged. Parts II/III were already comfortable and left untouched. `part-4.css` + `part-5.css`. |

**Verification:** local Cloudflare-style server, Chromium + WebKit, 1440 + 375.
0 console errors on all pages; 0 page-level horizontal scroll; `.book-nav` 48px.
Fig 8.4, the Part V closer (both openers), and the nav fade (start/middle/end
scroll states, all five parts, per-part colour) were screenshot-reviewed in both
engines. Anchor-id sets verified byte-identical to HEAD in every edited HTML
(part-3 364, part-4 217, part-5 180). Not yet redeployed — confirm live parity
after push. The upcoming precision test (anchor-id / reading-position sync) can
proceed: no ids moved.

## 4f. Pass 6 (2026-07-07): reading-position restore polish

Two diagnostic-mechanical fixes from the precision-test findings. Existing
anchor ids and the /api/position contract are unchanged; both verified in
Chromium **and** WebKit at 1440 + 375 (0 console errors, 0 external requests,
0 page h-scroll, `.book-nav` 48px; restores exercised under
`prefers-reduced-motion` too).

1. **Post-restore layout nudge eliminated (`book.js` `scrollToAnchor`).** After
   the first apply, content above the anchor could still shift and the restore
   visibly settled ~1.2 s later. Root cause (measured, not the obvious one):
   *not* fallback→webfont width reflow. It is a **vertical-metrics** effect —
   display webfonts (worst: Space Grotesk, Part III) whose intrinsic line box is
   ~2.4 em reserve a tall box for **off-screen** headings, which collapses to the
   CSS `line-height` (1.15) ~120 ms *after* the heading is scrolled into view.
   `document.fonts.ready` does not cover this (the font is loaded; the off-screen
   box is stale), and a metric-matched fallback can't win the first paint (local
   faces load async too), so `size-adjust` is the wrong lever. Fix is
   font-agnostic: while an instant restore settles, a **ResizeObserver on
   `document.body`** (fires after layout, before paint) plus a short rAF loop
   re-pin the anchor to its exact offset, absorbing any shift above it in the
   same frame. Stops on reader input, when the position holds for 8 frames, or
   after 2.5 s. Result: Chromium lands pixel-exact with zero drift; WebKit lands
   exact with at most a sub-frame transient on Part III during load. The smooth
   path (sync chip) keeps its single post-`scrollend` re-apply.
2. **Chapter-hero sub-anchoring (`scripts/add-hero-anchor-ids.js`, + 57 baked
   ids across the 5 part files).** Parking inside a hero used to anchor to the
   whole `<section id="chN">` (tall, heterogeneous), so the stored fraction
   resolved to different content across viewports (~150 px). Each hero's three
   text blocks now carry their own id — `chN-hero-label`, `chN-hero-title`,
   `chN-hero-lead` — so a mid-hero position anchors to a short, text-homogeneous
   element and the fraction maps to the same words on every device. Verified:
   parking on the title restores the exact line 1440↔375 (h1 has hard `<br>`
   breaks); parking on the lead restores to within a line (paragraph-level, like
   any body paragraph). The script is idempotent, never collides with an existing
   id, and touches only the hero label/h1/subtitle — the 277/274/291/177/144
   existing paragraph/section/figure id sets are byte-identical to HEAD.

## 4g. Pass 7 (2026-07-11): fact-verification pass

A holistic audit had found the book's rigor two-tier: mechanism/math sound,
anecdote/attribution stratum carrying ~30 blemishes. Every audit item was
**independently re-verified** (recomputed for math, primary/registry sources
for facts) before any fix — the audit itself was treated as fallible.
Register-neutral corrections only; anchor-id sets verified byte-identical to
HEAD in all five parts. Ledger (item → verified-how → outcome):

### Tier 1 — broken figures

| Item | Verified how | Outcome |
|---|---|---|
| Fig 14.8 RSA worked example | Recomputed end-to-end (Python): 65³=274625; 274625 mod 391 = **143** (not 191); e=3 coprime to φ=352 ✓; d=235 ✓ (3·235≡1 mod 352); 143²³⁵ mod 391 = 65 ✓ | Fixed: c=143 in all three places; every number on the card now verifies by hand. Also fixed a pre-existing ENCRYPT/DECRYPT header overprint found in the render spot-check |
| Fig 17.8 + fig 17.5 caption "ZooKeeper runs Raft" | ZooKeeper's protocol is ZAB (predates Raft, 2014); etcd/Consul/CockroachDB/TiDB/Vault do run Raft | Fixed: caption now credits ZAB with the same leader-majority shape; fig 17.8 label "Raft / ZAB · config-store role" |

### Tier 2 — attributions & anecdotes (16)

| Item | Verified how | Outcome |
|---|---|---|
| 1988 congestion paper: Karels, not Floyd | SIGCOMM '88 byline: Van Jacobson (LBL) + Michael J. Karels (UC Berkeley CSRG); Floyd = RED 1993 | Fixed, with correct affiliations ("one at each end of the collapsed link") |
| Takedown/Cyberpunk swap | *Takedown* = Shimomura & Markoff book (1996); *Cyberpunk* = Hafner & Markoff **book** (1991); the film (*Track Down*, 2000) was based on *Takedown* | Fixed: "a book (Shimomura and Markoff's *Takedown*) and, later, a film based on it" |
| TJX 2007 vector | DOJ/Gonzalez record: WEP war-driving interception; Heartland 2008 is the SQLi case | Fixed: TJX moved to a parenthetical with its true WEP vector; MOVEit 2023 (CVE-2023-34362, SQLi) added to the injection list. **Removed** the "2023 major US municipal water utility" SQLi claim — no supporting evidence exists (2023 water incidents were default-credential PLC hacks). **Flag:** Sony PSN 2011 = SQLi is common lore, never officially confirmed by Sony; left in place — owner call |
| Paxos lore inversion | 1998 TOCS paper IS the parable (submitted 1990); *Paxos Made Simple* (2001) is the plain one | Fixed in both prose spots |
| "Apple OUI 00:1A:11" | IEEE registry (maclookup.app): 00:1A:11 = **Google**; 00:03:93 = Apple, Inc.; 00:0A:41 = Cisco ✓; B8:27:EB = Raspberry Pi Foundation ✓ | Fixed: Apple example now 00:03:93 |
| Dhahran date | GAO IMTEC-92-26: **25** February 1991 | Fixed (was 28 — the death toll, not the date) |
| Boole→electron gap | Boole d. 1864; Thomson's electron 1897 → 33 years | Fixed ("twenty" → "thirty-three") |
| C++ ANSI timeline | ANSI committee convened 1989; first standard C++98 (1998) | Fixed: "In 1989 ANSI convened a standards committee; the standard itself — C++98 — took nine more years" |
| C++ renamed 1983 | Name coined 1983 (Mascitti); book + Cfront release 1985 | Fixed: rename 1983, book/compiler 1985 |
| Simula 67 date | Simula 67 = 1967 (Dahl & Nygaard) | Fixed in prose + fig 6.2 tick (1965 → 1967) |
| Perl origin | Wall wrote Perl at Unisys (1987), not NASA (JPL came later) | Fixed fig 5.11: "Wall · Unisys · syntax" |
| Copper attenuation | Cat5e/6 insertion loss ≈ 22 dB per **100 m** at 100 MHz — book's "30 dB per kilometre" was ~10× low | Fixed: "about 22 dB per hundred metres at the ~100 MHz frequencies modern Ethernet uses" |
| BGP age "twenty-five years" | BGP born 1989 (RFC 1105) → ~37 by book frame | Fixed to age-proof "born in 1989" |
| Shellshock class | CVE-2014-6271 is bash parser injection, not memory-unsafety | Fixed fig 5.10 "price of C" chip → Stagefright 2015 (libstagefright memory corruption) |
| ECB-Tux attribution | First appeared as a Wikipedia illustration (2004, User:Lunkwill); Valsorda's essay (2013) re-popularised it | Fixed caption: "first made for a Wikipedia illustration in 2004, famously revisited by Filippo Valsorda in 2013" |
| LinkedIn/Adobe "plaintext" | LinkedIn 2012 = unsalted SHA-1; Adobe 2013 = reversible 3DES — neither plaintext | Fixed fig 14.4: Era 1 example now RockYou 2009 (32 M genuinely plaintext); LinkedIn 2012 moved to the unsalted-hash era; Adobe dropped |

### Tier 3 — stale against 2026 (5)

| Item | Verified how | Outcome |
|---|---|---|
| CFS → EEVDF | EEVDF is Linux's default since kernel 6.6 (2023) | Table row now "default 2007–2023"; prose sentence added explaining EEVDF (same vruntime ledger + explicit deadlines) |
| Namespaces count | 8 kinds since Linux 5.6 (time namespace, 2020) | Fixed: "eight kinds — … and (since Linux 5.6) time" |
| Lambda billing | 1 ms granularity since Dec 2020 (GCF still 100 ms) | Fixed to platform-safe "meters the bill in milliseconds of execution" |
| "logical qubits" in 2026 | 2026 machines: hundreds+ physical, at most a few dozen error-corrected logical | Fixed: "at most a few dozen error-corrected *logical* qubits, each built from many noisy physical ones" |
| gVisor ≠ microVM | gVisor = user-space kernel (syscall interception); Firecracker/Kata are the microVMs | Fixed insight strip: gVisor "attacks the same trade from the other side" |

### Tier 4 — internal inconsistencies (6)

| Item | Verified how | Outcome |
|---|---|---|
| "235 figures" vs "two hundred and forty" | Counted figure SVGs preceding fig-18-trace: 51+55+66+37+26 = **235** | Prose fixed to "two hundred and thirty-five"; caption's 235 was correct |
| RAM latency 100 ns vs 60 ns | Part-I table + math callout use 60 ns (and compute with it) | Ch1 prose unified to "about sixty nanoseconds" |
| CUBIC 2008 vs 2006 | Linux default since 2.6.19 (Nov 2006); the CUBIC paper is 2008 | Prose fixed to "(Linux's default since 2006)" — now matches the caption |
| Cover "A visual theory" vs mastheads "A unified theory" | All five mastheads + README + package.json say "unified"; only the index `<title>` said "visual" | Unified to **"A unified theory"** (majority). **Flag:** owner may prefer "visual" — one-line change in index.html if so |
| "Less than 150 years" (1854→2026) | 2026 − 1854 = 172 | Fixed fig 18.2 line: "172 years from beginning to here" |
| Part III position-fix arithmetic | Haversine great-circle legs between the five stated fixes: cumulative 1,183 / 1,819 / 2,480 / 3,129 nm | All four runs replaced (were 870/1,730/2,590/3,459); each leg now computes from the printed coordinates. part-3.css comment + §4d updated |

### Side effects & verification

- `glossary.json` regenerated (516 → 518 terms): stale extracts ("Sally
  Floyd", "hundred-millisecond", old C++/CUBIC definitions) refreshed; new
  EEVDF and *Paxos Made Simple* entries; a bogus `gab` term (the
  `<em>g<sup>ab</sup></em>` math markup in ch14) excluded via a SKIP_WORDS
  addition in `build-glossary.js`.
- Verification: Cloudflare-mimicking server (200 extensionless, 308 on
  `.html`), Chromium + WebKit at 1440 + 375, all 8 pages: **0 console
  errors, 0 external requests, 0 page h-scroll, nav 48 px**. All 11 touched
  figures screenshot-reviewed in both engines. Anchor-id sets byte-identical
  to HEAD in all five part files (355/346/379/226/189 ids).
- Explicitly untouched (out of scope per owner): Little's Law framing, GCM
  nonce caveat, ANSI-isolation critique, "3 nm", Bletchley estimate.

## 4h. Pass 8 (2026-07-11): cover hero remake — the exhibit

The cover hero predated the pass-4 identity build: it presented one brand
(gold arc, single voice) while the book had become a five-identity collection.
Remade so the cover is the shelf that exhibits the collection. Below-the-fold
content (shelves, TOC, footer), navigation, resume/account chips and anchor
ids untouched; title, tagline, eyebrow, meta line and BEGIN READING kept
verbatim (vertical rhythm tightened so the whole hero fits a 1440×900 fold).

- **The exhibit (≥880px)**: one hand-drawn SVG replaces the sand→civilization
  arc — the same transistor and globe terminals, but the gold thread now runs
  **through five volume panels**, each drawn verbatim from its part's shipped
  identity: I home grammar (Playfair italic numeral, gold radial), II Greenbar
  (`#0c120e`, 32px phosphor banding, IBM Plex Mono 600), III Chart Room
  (`#0d2740`, 26px grid, surveyor corner ticks, Space Grotesk), IV Strongroom
  (`#171008`, double-rule inner frame, −2° stamp box around a Fraunces
  numeral), V Quorum (`#0e0c1a`, violet/teal auroras + star specks, Syne 800
  numeral in the headline-scale gradient). Curation stays in the spine's
  voice: the thread, terminals, SAND/CIVILIZATION and per-panel chapter
  labels are gold + DM Mono. Each panel is an SVG `<a>` to its part
  (aria-label carries the meaning; hover/focus-visible lifts the volume and
  brightens its identity frame).
- **Motion (one-shot, settling)**: the thread draws once (CSS dashoffset,
  2s linear from 0.35s), a gold packet rides it once (SMIL `animateMotion`
  paced, `fill="freeze"`, fades out into the globe), and each volume's
  numeral+port ignites as the packet passes (CSS delays 0.59–2.07s computed
  from the path's arc-length fractions 0.121/0.306/0.491/0.675/0.861); the
  globe lights at arrival. Rest state fully calm. **Reduced motion**: book.js's
  SMIL pauser exits early on the index (no figures) and book.css's kill zeroes
  durations but *not delays*, so the hero carries its own block — packet
  hidden, exhibit animations removed; every base value is the composed lit
  state.
- **Below 880px**: the same shelf stacked — five full-width identity bars
  (simplified CSS textures of the same tokens) on a vertical gold thread rail,
  SAND above, CIVILIZATION below, identity beads at each bar.
- **Fonts**: index now links `fonts-part2–5.css` (the one page that exhibits
  every identity). Only faces actually drawn download: Fraunces, IBM Plex
  Mono 600, Space Grotesk, Syne (~134 KB, self-hosted, 1-year immutable
  cache); Karla/Manrope/Spectral/etc. are declared but never fetched.
  Museum labels reuse the already-loaded DM Mono.
- **Verified** (local, Chromium + WebKit, 1440/900/820/375/320): 0 console
  errors, 0 external requests, 0 h-scroll, **CLS 0.0000** at 1440/375/320;
  mid-animation frame, settled state, hover, keyboard focus (aria-labels
  announced, frame highlight), reduced-motion composure all
  screenshot-reviewed in both engines; resume card still injects after
  `.cover`; only the intended font files load.

**Iteration 2 (owner-approved direction, same day):** the exhibit became an
**ascending shelf** — the five volumes stand on one gold shelf line, each
taller than the last (I 214 → V 286 units, common baseline), and the thread
now *climbs* from a low transistor to a globe in orbit: "from silicon to the
cloud, one layer at a time" drawn literally. Chapter labels moved out of the
panels onto **museum placards under the shelf** (DM Mono gold, curator's
voice), so a hovered volume lifts off the shelf while its placard stays on
the wall. Each panel gained its part's signature motif, quoted from the
shipped identity furniture: II a **sprocket rail** (dots + dashed separator,
the greenbar continuous-form edge); III a dashed salmon **route arc**
(`--cr-route #e07a3f`) with one lit waypoint of three (the voyage ahead);
IV a **declassifying redaction row** (one solid bar, one hollow) above the
stamped numeral; V the **five-part constellation fully meshed** (violet/teal
nodes, the End-of-Book "quorum reached" state); I stays bare — restraint is
the home grammar. Port beads now **bloom once** (scale pop, `transform-box:
fill-box`) on the same arc-length clock as the ignitions (fractions
0.136/0.325/0.513/0.701/0.889, delays 0.72–2.23s on a 2s ride from 0.45s).
Mobile stack: bar heights ascend 58→78px (layers accumulate) and bar II
carries the sprocket rail as a CSS dot column. Full verification matrix
re-run, identical results (0/0/0, CLS 0 at 1440/375/320, reduced-motion
composed, hover/focus in both engines).

**Iteration 3 (owner direction: keep the panels, drop the terminals):** the
SAND transistor and CIVILIZATION globe are gone; the exhibit is now the five
volumes alone. The thread runs **bead to bead** — it starts at volume I's
port and ends at volume V's port (ports carry small convex offsets, +26/+32/
+34/+32/+26 from panel tops, so the climb gently accelerates instead of
being a rigid straight line). The packet spawns on bead I and settles into
bead V (1.5s paced ride from 0.45s; ignition delays 0.45/0.82/1.20/1.57/
1.95s at arc fractions 0/0.249/0.499/0.749/1). ViewBox cropped to the shelf
(962×346), render width 900px — the panels gain ~10% presence. Mobile: the
SAND/CIVILIZATION caps removed; the gold rail now spans exactly from bar I's
bead to bar V's bead. Full verification matrix re-run (Chromium + WebKit,
1440/900/820/375/320): 0 console errors, 0 external requests, 0 h-scroll,
CLS 0 at 1440/375/320, reduced-motion composed, hover/focus verified,
early-frame choreography intact.

## 4i. Pass 9 (2026-07-12): pedagogical items, Part II (Phase 2, pass 1 of 5)

First execution pass of the owner-approved pedagogical plan (survey delivered
2026-07-12; approved scope = surgical items, no chapter reordering). The pass
brief raised a chapter 6⇄7 sequence swap; queried against the written proposal
(which concluded the 18-chapter spine is sound) and the owner confirmed
**items only, no swap**. Three register-neutral prose edits in `part-2.html`,
all inside existing elements: anchor-id sets verified **byte-identical to
HEAD** in all five parts (355/346/379/226/189 ids) — no ID migration needed,
every stored `/api/position` anchor resolves unchanged.

| # | Item | Edit |
|---|---|---|
| 1 | §2D — Little's Law mechanism (`ch4-scheduling-p10`) | The wait-time explosion is now carried, not asserted: the only slack absorbing arrival bursts is the spare capacity μ − λ; as λ climbs toward μ, backlog compounds between bursts and W grows like 1/(μ − λ) — the hyperbola Fig 4.6 plots. All existing claims (95%→99% ≈ 10× latency) untouched; the pass-7 "Little's Law framing out of scope" decision is respected in substance — no prior claim altered, mechanism added. |
| 2 | T1 — Ch4 closer box (`ch4-security-p18`) | The "**The recurring pattern.**" stamp (5 near-identical instances book-wide: Ch4/10/11/14/17) varied at its first instance — recast as the question every layer answers ("What is less-trusted code allowed to do here — and what stops it?"). Body substance kept verbatim in spirit; remaining four instances get their own shapes in their parts' passes. |
| 3 | T2 — Ch7 sharp-edges coda (`ch7-datasci-p7`) | "Python's three sharp edges" (same enumerated-wounds template as Ch6's "Where C++ still bleeds") reframed around the single worked footgun: pickle as a stack-machine interpreter whose objects can execute on construction — mechanism now carried — with `eval`/`exec` and the `requestz` typosquat folded in as the same **data-as-code** property (pattern name preserved for the Ch15 tie). All three facts survive. Ch6's box deliberately keeps the enumerated shape; Ch5 verified to have no such coda (the proposal over-attributed) — no-op. |

Side effects: `glossary.json` regenerated — 518 terms, 0 added / 0 removed;
one definition (`exec`) refreshed to the new Ch7 sentence. Ledger §4g
untouched — no edit intersects any of the 29 corrections.

Verification (local, Cloudflare-mimicking server: extensionless 200, `.html`
308): Chromium + WebKit at 1440 + 375 on part-2 / index / glossary —
0 console errors, 0 external requests, 0 page h-scroll, `.book-nav` 48 px;
all three edited passages confirmed rendering. Live parity verified after
push (see below). Next pass per approved order: Part III (Ch8 Shannon–Hartley
intuition + T1 Ch10/Ch11) — awaiting owner review of this pass first.

## 4j. Pass 10 (2026-07-12): pedagogical items, Part III (Phase 2, pass 2 of 5)

Approved scope: §2A Shannon–Hartley intuition (Ch8) + T1 stamp variation
(Ch10, Ch11). Three edits in `part-3.html`.

| # | Item | Edit |
|---|---|---|
| 1 | §2A — Shannon–Hartley mechanism (new `ch8-shannon-p12`, inside the math callout between formula and theorem statement) | The formula's shape is now read off the physics: distinguishable levels ≈ √(1+SNR) (received range √(S+N) vs noise blur √N), log₂ of that = ½ · log₂(1+SNR) bits per pulse, × 2B pulses/sec (Nyquist 1928, no affiliation claimed) — halves cancel to C = B · log₂(1+SNR). Includes why the +1 (the measuring range contains the noise). Faithful to the sphere-packing proof shape; existing theorem/coding-history text untouched. |
| 2 | T1 — Ch10 closer box (`ch10-attacks-p9`) | Stamp "The recurring pattern." → "**State is the attack surface.**" (chapter thesis); first sentence deduplicated ("pays for each in kernel-side state that an attacker can force it to spend"); rest verbatim. |
| 3 | T1 — Ch11 closer box (`ch11-modern-p7`) | Stamp → "**Protocols earn their shape.**" (aphorism; the body's "earned their current shape" line now reads as payoff, not echo). Body verbatim. |

Stamp variety so far: Ch4 question · Ch10 thesis · Ch11 aphorism; Ch14/Ch17
remain for their parts' passes. Anchor ids: sets are strict supersets of HEAD
— 0 removed anywhere, exactly one added (`ch8-shannon-p12`, baked by
`add-anchor-ids.js`); no migration needed, all stored positions resolve.
`glossary.json` regenerated: 518 terms, 0 added/removed; `shannon` / `snr` /
`channel capacity` definitions refreshed around the new sentence. Ledger §4g
untouched. Verification: local Chromium + WebKit at 1440 + 375 on
part-3/index/glossary — 0 console errors, 0 external requests, 0 h-scroll,
nav 48 px; all three passages render. Live parity verified after push.
Next pass per approved order: Part IV (§2B RSA correctness, §2C isolation
enforcement, T1 Ch14) — awaiting owner review.

## 4k. Pass 11 (2026-07-12): pedagogical items, Part IV (Phase 2, pass 3 of 5)

Approved scope: §2B RSA correctness (Ch14), §2C isolation enforcement (Ch13),
T1 stamp variation (Ch14). Three edits in `part-4.html`.

| # | Item | Edit |
|---|---|---|
| 1 | §2B — RSA correctness (new `ch14-publickey-p7`, after the RSA prose ¶, before the Fig 14.8 card) | The caption's "follows from Euler's theorem… homework problem" gesture is now carried in prose, parallel to the pass-2 DH treatment: e·d ≡ 1 (mod φ(n)) ⇒ ed = 1+kφ(n); Euler gives m^φ(n) ≡ 1; so (m^e)^d = m·(m^φ(n))^k ≡ m. Closes with why the attacker's path back to d is factoring. "Eighteenth-century theorem" — no precise year claimed (Euler 1763 not verified to source). Nested-superscript rendering screenshot-checked at 1440 + 375, legible. |
| 2 | §2C — isolation enforcement (new `ch13-acid-p8`, closing the ch13-acid section after Fig 13.7) | The levels section said what each level *permits*, never how an engine *provides* it. Added the two families: pessimistic two-phase locking (shared/exclusive, hold to commit, conflicters wait) vs MVCC (version chains + snapshots; readers never block writers). Engine placement: PostgreSQL MVCC throughout (snapshot per statement / per transaction / SSI abort layer at Serializable), InnoDB = MVCC + next-key locks closing the phantom window. `MVCC` marked as a key-term → deliberate new glossary entry; "two-phase locking"/"snapshot" left unmarked to avoid glossary noise. |
| 3 | T1 — Ch14 closer box (`ch14-tls-pqc-p9`) | Stamp "The recurring pattern." → "**Every asymmetry has a half-life.**" Body verbatim (Caesar → RSA → ECC → lattices, migrate-before-it-fails). Stamp variety now: Ch4 question · Ch10 thesis · Ch11 aphorism · Ch14 metaphor; Ch17 remains. |

Anchor ids: strict supersets of HEAD — 0 removed anywhere, 2 added
(`ch14-publickey-p7`, `ch13-acid-p8`, baked by `add-anchor-ids.js`); no
migration, all stored positions resolve. `glossary.json`: 518 → **519**
(new `MVCC` entry, correctly attributed to ch13-acid first use; 0 removed).
Ledger §4g untouched — RSA edit is consistent with the pass-7 recomputed
Fig 14.8 numbers and touches none of them. Verification: local Chromium +
WebKit at 1440 + 375 on part-4/index/glossary — 0 console errors, 0 external
requests, 0 h-scroll, nav 48 px; all three passages render; both new
paragraphs screenshot-reviewed at both widths. Live parity verified after
push. Next pass per approved order: Part I (§2E Ch1 thinning — the only item
with an anchor-ID migration) — awaiting owner review.

## 4l. Pass 12 (2026-07-12): pedagogical items, Part I (Phase 2, pass 4 of 5)

Approved scope: §2E — Chapter 1 thinned to preview altitude. Ch1 previewed the
kernel/syscall/virtual-memory material at near-full depth, which the Bridge
(silicon view) and Ch4 (code view) then teach again — triple-telling. The
front/middle of Ch1 (Turing → transistor → Von Neumann → instruction cycle →
memory hierarchy/caching) is untouched; both figures (1.13, 1.14), both
insight strips, and all captions are untouched — **no figure removed, all
figure-count claims (242/235) remain true**. Net prose: −443 / +332 words.

| # | Edit | Detail |
|---|---|---|
| 1 | `ch1-kernel-p6` thinned in place (id kept) | The full syscall path walk (Python→fopen→syscall→state save→Ring 0 entry→permission check) compressed to name-the-mechanism + two-sided seam: silicon half → the Bridge, kernel half → Ch4. `<em>file descriptor</em>` kept. p7 ("It asked the kernel, the kernel decided") kept verbatim. |
| 2 | Syscall `code-block` removed (id-less — no anchor impact) | Its 7-step CPU-level walk is verbatim the Bridge's Fig BR.2 dispatch story. |
| 3 | UNIX ¶s merged: `ch1-kernel-p8` rewritten, `ch1-kernel-p9` **removed** | Everything-is-a-file creed + lineage compressed into one paragraph under p8's id, closing with seams to Ch4 (kernel as program) and Ch5 (the language). |
| 4 | `ch1-memory-p9` thinned in place (id kept) | Page-table/4KB/swap mechanics compressed to MMU-names-the-hardware + two-sided seam (Bridge walker/TLB/fault; Ch4 page-faults-as-features/mmap/COW). `ch1-memory-p8` (virtual-address fiction) and p10 (isolation/flexibility/protection) kept verbatim. |

**Anchor-ID migration (the first real one).** Exactly one id removed:
`ch1-kernel-p9`. `book.js` gains an `ANCHOR_ALIASES` map consulted in
`scrollToAnchor` — the single resolve point through which all three restore
paths flow (sessionStorage handoff, local restore, sync chip). A stored
position at the dead anchor resolves to `ch1-kernel-p8` with its fraction
preserved (drift bounded by one merged paragraph — same guarantee class as
pass-6 hero anchoring). Functionally tested in Chromium **and** WebKit:
seeded pending-offset at `ch1-kernel-p9` fraction 0.5 → restore lands with
p8 midpoint at the reading line, **0 px delta** in both engines. The line-606
proximity lookup is null-guarded (worst case: sync chip shows instead of
being suppressed — benign). Thinned-in-place paragraphs keep their ids, so
positions there survive without migration.

Cross-reference audit: every "Chapter 1 …" back-reference in all five parts
checked against the surviving prose — all still true (VM-as-fiction for the
Bridge/Ch4, registers/memory-hierarchy for Ch3/Ch13, privilege rings for
Ch15's Dirty COW context, speculation §04 for Ch16). No link targets the
removed id anywhere. `glossary.json`: 519 → 519 — gained `everything is a
file` (the reworded creed now extracts; section ch1-kernel), lost the plural
`page tables` (its defining sentence was the removed mechanics; the singular
`page table` entry, home ch4-vm, survives, and the plural's only marked
occurrence in the book is the new ch1 sentence itself). Ledger §4g untouched.

Verification: local Chromium + WebKit at 1440 + 375 on part-1/index/glossary
— 0 console errors, 0 external requests, 0 h-scroll, nav 48 px; all kept/new
passages render; removed id + code block confirmed absent; thinned section
flow screenshot-reviewed at 1440. Live parity + live migration restore
verified after push. Remaining pass: Part V (T1 Ch17) — awaiting owner
review.

## 4m. Pass 13 (2026-07-12): pedagogical items, Part V — Phase 2 complete

Final approved item: T1 stamp variation, Ch17. One edit in `part-5.html`
(`ch17-microservices-p6`): "The recurring pattern." → "**Ask what the
abstraction still charges.**" — an imperative, matching the box's cost
ledger; body verbatim. Zero "The recurring pattern." stamps now remain
book-wide; the five closers each carry their own rhetorical shape:

| Ch | Stamp | Shape |
|---|---|---|
| 4 | The question every layer answers. | question |
| 10 | State is the attack surface. | thesis |
| 11 | Protocols earn their shape. | aphorism |
| 14 | Every asymmetry has a half-life. | metaphor |
| 17 | Ask what the abstraction still charges. | imperative |

Anchor-id sets byte-identical to HEAD in all five parts; `glossary.json`
regenerated — byte-stable (519 terms, no entry changes). Ledger §4g
untouched. Verified local + live, Chromium + WebKit at 1440 + 375: 0 console
errors, 0 external requests, 0 h-scroll, nav 48 px.

**Phase 2 exit state.** All approved items from the 2026-07-12 pedagogical
survey are executed and live (passes 9–13, commits 6a4485c → this):
§2A Shannon–Hartley mechanism (Ch8) · §2B RSA correctness (Ch14) ·
§2C isolation enforcement (Ch13) · §2D Little's Law mechanism (Ch4) ·
§2E Ch1 thinned to preview altitude (with the `ch1-kernel-p9` →
`ch1-kernel-p8` ANCHOR_ALIASES migration in book.js, functionally verified
live in both engines) · T1 all five instances varied · T2 Ch7 reframed
(Ch6 deliberately kept enumerated; Ch5 had no such coda). Chapter order
unchanged throughout (a 6⇄7 swap raised in a pass brief was queried and
declined by the owner). The 29 §4g corrections survive in substance;
glossary net 518 → 519 (+`everything is a file`, +`MVCC`, −plural
`page tables`); no figure added or removed — all count claims hold.

## 4n. Pass 14 (2026-08-01): the language pass, Part I — mechanism carried in prose

First part of the book-wide **language pass** — the owner's final planned
transformation. The brief: across the book, prose too often *names* a mechanism
(or defers it to a figure caption) instead of running it cause-to-effect. This
pass shifts that at the sentence level, part by part, to the register of the
Ch7 pickle coda (pass 9): the mechanism carried in the prose, alive, facts
intact. Content is fixed — every fact, figure reference, and §4g correction
survives in substance; anchor ids preserved.

**Method.** Deep read of all of Part I (Ch1–3 + the Bridge) as a student who
must understand it, plus an independent judge workflow: 28 per-section
student-readers, then a 19-section adversarial *defense* pass whose only job was
to overturn weak flags (the target list is what survived defense, not what was
first flagged). Then rewrites, then a final fact/voice confirmation gate on
every rewritten passage — which caught and fixed one overstatement introduced in
flight (see item 15). Anchor-id set **byte-identical to HEAD** (354 ids); no
position-sync migration needed.

**Left alone (said so, per the brief).** The **Bridge interlude** is the
calibration standard end-to-end — the SYSCALL five-atomic-steps, the four-level
MMU walk from CR3, the TLB hit-rate argument, the three-step DMA story all run in
prose already; it was not touched. Also left verbatim: the chapter heroes; the
Turing-machine definition and universality (ch1-context p3/p5); Von Neumann
stored-program (ch1-vonneumann); the pipelining, out-of-order, and speculative
paragraphs (ch1-cpu p7–p9 already run their mechanisms); the memory-hierarchy
math-callout (locality + T_avg, exemplary); the pass-12 preview-altitude ch1
kernel/memory thinning (compression respected — only a *dropped* causal link was
restored, item 6); ch2-arithmetic (half/full adder already constructive); the
pass-2 two's-complement modular insertion; ch2-float layout/Patriot; all of
ch3-registers/stack/call/defenses (call/ret, canaries, DEP, ASLR, ROP each run
their mechanism). Roughly two-thirds of Part I's sections passed the bar
untouched — Part I is one of the book's strongest parts.

**Rewritten (18 passages, why):**

| # | Item | Change |
|---|---|---|
| 1 | Ch1 `ch1-cpu-p2` + caption `-p3` (**severe**) | The chapter titled "Fetch. Decode. Execute. Repeat." never ran the four stages in prose — they lived only in 8px SVG labels, and the caption duplicated the preview. p2 now defines the program counter and runs fetch→decode→execute→writeback cause-to-effect; the caption is de-duplicated to figure-specific guidance. |
| 2 | `ch1-context-p4` | The "extraordinary proof" was promised and never delivered (undecidability is taught nowhere in the book). Added the self-reference cash-out: a decider fed a program built to contradict its own verdict — the machine *was* the proof. |
| 3 | `ch1-context-p8` | "searched the key space mechanically" was a tautology. Now runs the Bombe's actual method: a crib, Enigma's no-letter-encrypts-to-itself flaw, and elimination by electrical contradiction — search by elimination, not exhaustion. Facts (158 quintillion keys, Colossus/Flowers/Lorenz) preserved. |
| 4 | `ch1-transistor-p7` | "Why semiconductors" answered with a definition + sand trivia. Now carries doping: donor/acceptor atoms seed electrons/holes, and why a *tunable in-between* conductivity is exactly what a switch needs. |
| 5 | `ch1-transistor-p8` (caption) | The field-effect "inverts" happened by fiat. Added the causal middle: the gate's charge reaches *across* the oxide as a field (not a current), pulling an inversion layer into being. |
| 6 | `ch1-kernel-p4` | The section's own question (idle CPU during I/O — can another program run?) was answered by name only, then pivoted to protection. Restored the dropped half: a program blocking on I/O is exactly when the kernel hands the CPU to a ready one. (Not the pass-12 compression — a dropped causal link.) |
| 7 | `ch1-memory-p11` (insight strip) | Canary/ASLR/DEP were a bare catalogue. Each now carries a one-clause cause (trip-wire before the return address; randomized target; non-executable data). Ch3 still delivers the full treatment — this makes the *preview* teach. |
| 8 | `ch2-binary-p3` | The climactic sentence was garbled ("a small drift will turn a 1 into a 0" read as a contradiction; "a 0 look like a 2" referenced a digit the balanced-ternary framing lacks) and contradicted its own caption. Rewritten to run the noise-margin mechanism: three levels in one voltage span → narrower bands → a drift binary shrugs off crosses a ternary boundary. |
| 9 | `ch2-boole-p3` | Boolean algebra was named but its operations never defined (deferred to the gates section three paragraphs on). Added the meanings of AND/OR/NOT and a Boolean law (A + A = A, A · A = A) — "same symbols, different rules." |
| 10 | `ch2-boole-p6` | "series = AND, parallel = OR" was asserted. Added the one-clause cause (series: current must pass through both; parallel: either path suffices) — the section's central Shannon click. |
| 11 | `ch2-gates-p4` | NAND universality was named ("functional completeness") with the construction wholly in the figure. Now runs it in prose: tie a NAND's inputs to get NOT (because A·A = A), double it for AND, De Morgan for OR. |
| 12 | `ch2-twos-p3` | "cannot use the same adder to subtract" was asserted. Now shows the signed-magnitude adder failing concretely: +5 (00000101) + −5 (10000101) → 10001010 = −10, not 0. |
| 13 | `ch2-float-p2` | The section's title question ("why 0.1 + 0.2 ≠ 0.3") bottomed out in an assertion. Added the cause: a binary fraction is a sum of powers of two, so it terminates only when the denominator is a power of two; 1/10 carries a factor of 5 that no stack of halves divides — and the reader can now predict which fractions are exact. |
| 14 | `ch2-float-p9` / `-p10` | Special values were a bit-pattern catalogue. p9 adds infinity's producers and the poison-value rationale (a bad result flows to the end to be spotted, not crashing at once); p10 resolves the "mathematically odd" NaN ≠ NaN by explaining *why* (a non-value can't equal anything) and turning it into the x != x detector. |
| 15 | `ch3-isa-p5` (Rosetta caption) — **accuracy** | The caption claimed x86 and ARM share a memory model; they do not (x86 = TSO, ARM = weakly ordered), which is precisely why Apple added a per-process hardware TSO mode to M-series. Corrected the stated cause; kept the real intuition (every x86 instruction has an equivalent ARM sequence, findable ahead of time). New §4g-class correction. |
| 16 | `ch3-isa-p6` | "RISC could clock faster because decode was simple" named the cause without running it. Now cashes Fig 3.1's variable-vs-fixed-width setup: variable length hides where the next instruction begins (serial decode); fixed 4-byte ARM sits at known boundaries (parallel decode, shorter tick). |
| 17 | `ch3-overflow-p9` | "memory-safe languages check bounds" named the check without its consequence, and overclaimed ("the central reason newer languages exist"). Now runs the consequence — an out-of-range access becomes a controlled panic *before* the write, so corruption becomes a crash and a crash is not code execution — and scopes the claim honestly (Rust's raison d'être; Java/Python/Go had other drivers). |
| 18 | `ch3-overflow-p10` | The Heartbleed clause introduced a new mechanism (over-*read*) and asserted its effect. Added the cause: the server trusted an attacker-supplied length and echoed that many bytes from its own memory, spilling whatever sat next to the buffer — including private keys. |

**Confirmation-gate fix.** The final fact pass flagged one overstatement I had
introduced in item 14: "any arithmetic that touches an infinity or a NaN
produces another infinity or NaN" is false for infinity (`1.0 / ∞ = 0.0`).
Rescoped the propagation claim to NaN (which is also the load-bearing half for
the p10 detector); infinity now merely "keeps the computation moving." No other
factual error survived the gate; 18/19 checked items were clean on first pass.

**Glossary.** Regenerated: net **+1** (`doping`, home ch1-transistor). Five
emphasis-markup artifacts from the rewrites were skip-listed in
`build-glossary.js` (matching the pass-7 `gab` precedent): the four
instruction-cycle stage verbs `fetch`/`decode`/`execute`/`writeback` (common
words that would fire CPU-cycle tooltips on every unrelated use book-wide — the
term `instruction cycle` itself remains) and `a a a` (the `A · A = A` Boolean-law
markup). No entry removed.

**Invariants held.** §4g corrections untouched (item 15 *adds* one, consistent
with the book's fact-rigor standard); figure grammar/counts/identities, chapter
order, zero-third-party, reduced-motion/print, and the five Phase-2 closer
stamps all unchanged. Anchor-id set byte-identical (354). No figure added or
removed.

**Verification.** Local (Cloudflare-mimicking server: extensionless 200, `.html`
308) Chromium **and** WebKit at 1440 + 375 on part-1/index/glossary — 0 console
errors, 0 external requests, 0 page h-scroll, `.book-nav` 48px. All 11 dark/
light edited passages screenshot-reviewed (math markup A·A=A, code fractions,
dark diagram-captions, insight strips all render). Internal anchors all resolve.
**Live parity confirmed** after push (commit `4abf0d0`): live part-1 passes the
full harness in both engines at both widths; canonical `glossary.json` serves
count 520 with `doping` (the count-519 first read was the documented 1-day
`stale-while-revalidate` edge cache, since revalidated). **STOP for owner review**
before Part II — the Phase-2 gate rhythm.

### Pass-14 verification (2026-08-01, second model, commit `081d2f8`)

Full audit of Pass 14 (which had been executed by a weaker model): all 18
rewrites re-judged against the Ch7 pickle-coda bar, the cleared two-thirds
re-read, both accuracy claims re-verified. Method mirrored the pass itself:
deep read plus an independent 13-agent workflow (6 author-voice judges over
the rewrites, 4 fresh readers over the cleared spans, 3 fact/figure
verifiers); every flag adjudicated by the verifying model, several declined.

**Rewrites: 12 of 18 kept verbatim** (2, 4, 5, 7, 9–13, 15, 17, 18 — the NaN
pair, the doping and field-effect passages, and the kernel-sharing close are
genuinely at the bar). **Six re-carried:**

| # | Item | Why |
|---|---|---|
| 1 | `ch1-cpu-p3` caption | "The diagonal hand-off" — Fig 1.9 contains no diagonal (four stages in one row, rectangular loop); "diagonal" is Fig 1.11's pipeline signature. → "The cycle never stops…" (p2 kept verbatim) |
| 3 | `ch1-context-p8` | **Fact:** "the day's rotor wiring" — rotor wiring was fixed at manufacture and known to Bletchley; the daily secrets were settings (the Bombe's chains were plugboard hypotheses per rotor position). → "the day's secret settings" |
| 6 | `ch1-kernel-p4` | "The trick that made sharing pay off is this:" — zero-content announcement scaffold. → "…is timing:" |
| 8 | `ch2-binary-p3` | "Here is the mechanism." — literal announcement, double wind-up on "that is where it lost." Cut; fused with a colon |
| 14 | `ch2-float-p9` | "and it does so for a reason:" scaffold + thesis stated twice ("Both keep the computation moving" repeated the opening). Cut both; sign-bit clause repositioned ("and the sign bit says which direction"). p10 kept verbatim |
| 16 | `ch3-isa-p6` | "recall from Fig 3.1 that an x86 add can run anywhere from two bytes to a dozen" — the figure shows one 7-byte add, no range. → figure cited for what it shows; range kept as prose fact (2 bytes `01 C8` — the book's own Fig 1.10 aside — to ~12 with REX+SIB+disp32+imm32) |

**Accuracy claims: both stand.** Rosetta/TSO — x86 TSO vs ARMv8 weak default
confirmed; M-series per-thread TSO mode (ACTLR_EL1, Asahi-documented) engaged
for translated code; caption scoped correctly. ∞→NaN rescope — verified
empirically at bit level: `1.0/∞ = 0.0` (infinity does not always propagate),
NaN propagates through all basic arithmetic, `x != x` is the standard test;
the rescope was the right call.

**Wrongly cleared, found & fixed (15 surgical edits).** Three fact-class:
`chBridge-mmu-p3` fault list had the U/S protection **inverted** ("U-tagged
page touched from kernel mode" is SMAP, never introduced; the promised case
in `chBridge-mode-p7` is an S-tagged page touched from *user* mode — fixed);
`chBridge-mode-p2` credited rings to "IBM and Intel" — rings are **Multics**
terminology (IBM used supervisor/problem state) — fixed; `ch1-context-p9`
caption's "daily reflector settings" (Wehrmacht reflector was fixed; keyspace
factors are rotor order × start positions × plugboard) — fixed, and its
now-stale Bombe clause re-aimed at the body's elimination mechanism. The
rest: caption/body duplication *created by pass 14 itself* (`ch2-binary-p4`,
`ch2-gates-p6` de-duplicated to figure-specific guidance; `ch1-cpu-p10`
verbatim 95%-sentence cut; `ch1-kernel-p2` caption no longer pre-asks and
pre-answers the section); mechanism gaps of the brief's exact class
(`ch2-arithmetic-p5` now runs two-half-adders+OR — the two carry-outs can
never both fire; `ch2-arithmetic-p9` caption trimmed of its p5/p6 echoes;
`ch3-isa-p7` now says how x86 escaped the decode penalty p6 proves — parse
once, serve hot code from the μop cache; `ch3-defenses-p9` CFI got its
mechanism clause; `ch3-stack-p3` tautology closer replaced — the stack is
the one data structure the ISA itself understands); and two consistency
stitches (`ch3-isa-p4` "on the fly" → "before they run", matching the AOT
caption beside it; `ch3-call-p2` back-references Fig 3.4 instead of
re-introducing the ABI as new; `ch3-isa-p1` "any consumer CPU" → "no
descendant has ever removed"; `ch2-twos-p7` caption's "magic" de-mystified
to match p6's own "not luck — arithmetic").

**Considered and declined** (deliberate layering or owner-call; do not
"fix" blindly): pre-existing caption self-containment (`ch1-transistor-p6`,
`ch1-memory-p3`, `ch1-cpu-p8`, `ch2-boole-p9`, `ch2-float-p11`/`-p12`
Patriot pairing, `ch3-defenses-p4`/`-p10`, `ch3-registers-p5` ABI caption);
Bridge reinforcement repetition (`chBridge-mmu-p6`, `-mode-p5`, `-timer-p3`,
`-io-p3` caption-carried MMIO, `-mode-p1` one-bit framing — the Bridge is
the calibration standard; its layering reads as intentional); `ch1-context-p5`
universality cash-out (the rules-as-data reveal is deliberately held for
Von Neumann two sections later); `ch2-boole-p10` circuit-vs-machine
overbreadth (inspirational register, owner-call); ch3-closer/Bridge-lead
12-word echo (reads as a deliberate bead-to-bead thread); "naval codes" vs
the 158 × 10¹⁸ Army-figure tension (pre-existing, "about" hedge in place).

**Invariants.** Anchor-id set byte-identical to HEAD (354). Glossary
regenerated twice: first regen dropped `full-adder`/`infinity` and minted a
junk `system v amd64 abi` entry (the edits had broken the builder's
term-cue patterns); prose adjusted, second regen restored **count 520 — no
entry added or removed**, 6 definitions refreshed and all improved (CFI now
carries its mechanism; both kernel entries carry "timing"; `full-adder`
constructive). §4g corrections untouched; this pass **adds four** §4g-class
corrections (U/S inversion, Multics rings, Enigma reflector, Bombe
settings). No figure added/removed; figure references now all match what
their figures draw.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308) and **live after push**, Chromium + WebKit at 1440 + 375 on
part-1/index/glossary — 0 console errors, 0 external requests, 0 h-scroll,
nav 48 px, fonts loaded, internal anchors resolve. 10 edited passages
screenshot-reviewed in both engines, dark + light (sup markup `2ⁿ`/`10³⁰⁸`,
code chips, captions all render). Live parity confirmed ~30 s after push;
live `glossary.json` serves count 520. **STOP for owner review** stands —
Parts II–V of the language pass remain.

## 4o. Pass 15 (2026-08-01): the language pass, Part II — Ch4–7 (commit `6a94554`)

Same brief, same bar (the Ch7 pickle coda — which lives in this part and was
untouched). **Method:** deep read of all of Part II, then a 12-reader /
per-batch adversarial-defense workflow (target = what survived defense) plus
3 fact agents; 6 defense agents died on a session limit mid-run and those
batches were defended by the executing model directly. Then rewrites, then a
3-lens confirmation gate (facts / internal-consistency / voice) over the full
diff — which caught **4 must-fix errors introduced in flight** (an
eBPF-vs-browser false equivalence; figure arithmetic that failed
self-division; a C++23 figure label contradicting its corrected caption; a
splice artifact) and 7 accepted nits. All fixed before commit.

**The finding of the pass: Part II's prose already holds the bar.** The
defense overturned most style flags (CFS "elegant idea" topic sentence,
caption self-containment across all four chapters, the Tanenbaum/Torvalds
caption resolution). Genuine language re-carries were few: the GIL's
lost-update race now runs cause-to-effect (both threads read 2, write 1 — an
object that should be dead lives forever; lose the increment instead and
Chapter 5's use-after-free arrives in a language that promised you'd never
see one); UBSan cast as the optimizer's mirror; the MLFQ caption made to
describe its own figure (A is demoted, not "interactive"); the signals triad
corrected to handle/ignore/default with SIGKILL/SIGSTOP as the uncatchable
pair (figure label matched).

**What Part II actually needed was a fact pass (~30 corrections, §4g-class):**

| Area | Corrections |
|---|---|
| Ch4 | Scheduler tick = on-core timer (was "chip on the motherboard", contradicting the Bridge); major faults ~1000× minor (was "tens of thousands", contradicting its own µs/ms figures); WAL = Gray, IBM System R, late 1970s (was "IBM, 1981" — Gray was at Tandem by 1981); commit-record atomicity "in practice" not "hardware guarantee"; WAFL "early 1990s", "first" dropped (Sprite LFS 1991); pipes conceived by McIlroy, **built by Thompson in an evening** (was "added by McIlroy"); IPC table chronology claim cut (contradicted signals caption); "same five syscalls incl. lseek work on all" → four, with the socket door noted; cgroups meter processes not file descriptors; CPU **quota** descheduling (was share/budget conflation); Firecracker = micro-VM wrapper not "VM-strengthened container"; eBPF unprivileged-load claim scoped (verifier + who-may-load); eBPF/browser forward-ref corrected to proof-up-front vs fenced-at-runtime (TLS dropped — not an instance); closer now says CFS *and EEVDF* (was contradicting the §4g EEVDF fix) |
| Ch5 | PDP-7 "mainframe" → minicomputer (contradicted its own section 3×); C named "after its predecessor's first letter" (B's first letter is B) → "the language that comes after B"; 1975-code-runs-unmodified softened (K&R dialect aged); Ritchie *and Thompson* rewrote UNIX; K&R "mostly unrevised" dropped (2nd ed. 1988 was an ANSI rewrite); "same source ran next year" → within five years (matched its own p4); BCPL "stack-based" dropped; 2⁶⁴ "more bytes than will ever exist" → than any machine will fill; heap "free list" wording made precise (and the term's definition kept — see glossary note); audio 48,000 samples/s not callbacks/s; browser is **C++** not "mostly C"; C++ near-superset (only Objective-C strict); 70% memory-safety stat scoped to Microsoft/Google codebases (matching Part I's phrasing); "dozens" of UB -f flags → handful; NULL-deref chain "takes a few microseconds" (was "time to read this sentence"); Zig is not memory-safe — third-wave taxonomy rewritten |
| Ch6 | **Both Stroustrup pull-quotes were unverifiable and are replaced with documented ones**: RAII section now carries "C makes it easy to shoot yourself in the foot…" ; modern-C++ section carries "Within C++, there is a much smaller and cleaner language struggling to get out" (D&E 1994 — which is that section's thesis). OS/360, not Multics, as Brooks's canonical case; defect-density "law" softened to the quadratic-interactions argument; Stroustrup's thesis = distributed systems, simulator in Simula; Simula words = class/object/virtual/this, ideas = inheritance/virtual methods (subclasses/virtual procedures); C++23 caption + timeline box fixed (modules are C++20; box now std::print); `operator==` vs `p.equals(q)` naming unified; RAII "break exits function" → loop; "eight cleanup paths" arithmetic dropped; "every modern feature built on RAII" scoped to the library; moved-from reads = unspecified value, not UB; move = three pointer assignments (caption matched to body); "nine-year pattern" → decade-scale; dangling "them" pronoun; Ch6→Ch7 seam now says Christmas 1989 (was "1990 in a hallway", contradicting Ch7) |
| Ch7 | **Dartmouth BASIC was a compile-and-go compiler** — the interpreted BASIC is the microcomputer ROM lineage, sentence rewritten; McCarthy "had written" not "had published" (CACM was 1960); **Zen of Python credited to Tim Peters, 1999** (was "van Rossum's design notes"; the p6 pull-quote was already correctly attributed); static-typing example fixed ("hand a string to a function that wants an integer" — string+int compiles fine in C/C++/Java); types-p1 payment ledger un-inverted; "ate every benchmark" → "the fast languages growing Python wrappers"; interpret-p3/p4 respect .pyc caching (translation cached, interpretation paid every run; only imports cached, `__main__` recompiled); **GIL switch interval = 5 ms** (was Python 2's "100 bytecodes"); GIL controversy "since the cores multiplied" (was "last decade", contradicting its own caption); asyncio scoped (nothing tears mid-operation; thread-per-connection cost, not the GIL, is the ceiling); PEP-703 caption de-duplicated; CPython bytecode "JVM later made famous, both inherited from older stack machines" (was "predating it by a year" — it's four, and p-code/Smalltalk predate both); **matmul figure renumbered to measured reality** (benchmarked locally: ~50 s pure Python on fast 3.14, 3.8 ms NumPy → figure now ~2 min / 0.012 s / ~10,000×, caption "four orders", all self-consistent); "numerical work is the slowest thing computers do well" → most cycle-hungry |

**Declined** (deliberate; do not "fix" blindly): caption self-containment
throughout (pipe, canary-class, smart-pointer, zero-cost captions);
"Windows is monolithic" (assert-then-refine, p8 carries the nuance);
"deserves its own paragraph" and "Here is one of the deeper revelations"
(content-bearing flourishes); "exactly two ways to mishandle malloc" (two
classes; the lead's three are instances); Ch5 "This is what kernel security
is about"-class lead closers. Pre-existing `thompson` glossary entry points
at a Stroustrup sentence (extractor quirk, predates this pass) — noted, not
chased.

**Invariants.** Anchor-id set byte-identical (346). Chapter order, heroes,
Phase-2 stamps (ch4-security-p18), pass-9 items (Little's Law mechanism,
pickle coda) untouched. Figure edits confined to four text labels, each
§4g-precedented (matmul numbers, C++23 box, signal-reactions strip — plus
the MLFQ caption describing the drawn schedule). Glossary regenerated:
**count 520, no entry added or removed** after reflowing three cues the
edits had broken (junk `default`/`os 360` averted, `timer interrupt`
restored); 6 definitions improved, including two that had been broken
fragments (`van rossum`, `inheritance`).

**Verification.** Local (CF-mimicking server) + **live after push**
(commit `6a94554`, live ~30 s later): Chromium + WebKit at 1440 + 375 on
part-2/index/glossary — 0 console errors, 0 external requests, 0 h-scroll,
nav 48 px, fonts loaded. 12 edited passages screenshot-reviewed in both
engines, dark + light. Live glossary serves 520 with `timer interrupt`
restored. **STOP for owner review before Part III** — the gate rhythm.
Remaining language-pass parts: III, IV, V.

### Pass-15 verification (2026-08-10)

Full Fable audit of Pass 15, whose clearances never had a second read and
whose in-flight defense was partially self-defended (brief:
`docs/pass-15-verification-brief.md`); run in parallel with the owner's read —
fact fixes only, zero register churn, anchors byte-identical. Method mirrored
the 14/16/17/18 pattern: deep read of all of Part II by the verifying model,
then a 17-agent workflow — 8 independent per-chapter fresh readers (student +
sceptic lens, web-enabled, blind to §4o), 4 primary-source verifiers over the
§4o correction list, an adversarial defense over every contested flag (4
defenders, one per chapter batch: 21 overturned, 8 conceded, 1 partial), and
a fact/consistency/voice confirmation gate over the diff. The first 12-agent
wave died whole on a session limit — the exact Pass-15 failure mode — and was
re-run complete after the reset; nothing was self-defended. The gate found no
verifier error (a first in five verifications), returning only cosmetic
notes; its second look ratified one post-gate banner iteration (below).

**The §4o load-bearing corrections: all stand.** Reconfirmed against primary
sources or recomputed: both replacement Stroustrup pull-quotes word-for-word
(foot quote per stroustrup.com/quotes.html; "smaller and cleaner language" =
D&E p. 207, 1994); WAL = Gray/System R late 1970s; pipes conceived by
McIlroy, built by Thompson in a night (McIlroy, *A Research UNIX Reader*);
scheduler tick = on-core APIC timer; major ≈1000× minor; commit-record "in
practice"; WAFL early 1990s; four-syscalls + socket door (POSIX read() on
sockets); cgroups / CPU-quota descheduling (CFS bandwidth-control docs);
Firecracker micro-VM; eBPF verifier + who-may-load; proof-up-front vs
fenced-at-runtime; CFS-and-EEVDF (6.6, 2023); PDP-7 minicomputer; "after B"
(Ritchie's "progression through the alphabet" account); no K&R-unrevised
claim remains; browser = C++ (every major engine); 70% scoped to MSRC 2019 /
Chromium; the kernel's exact -f flags in its Makefile; Zig not memory-safe;
OS/360 for Brooks; Stroustrup thesis = distributed systems, Simula
simulator; Simula words class/object/virtual/THIS vs ideas
(subclasses/virtual procedures); modules = C++20, std::print = C++23;
moved-from = valid-but-unspecified ([lib.types.movedfrom]); Christmas-1989
seam; ANSI committee Dec 1989 → C++98; Dartmouth compile-and-go misclaim
absent, ROM-BASIC lineage correct; McCarthy "had written"; Zen = Tim Peters
1999; GIL 5 ms; .pyc = imports cached, `__main__` recompiled;
bytecode/stack-machine lineage; asyncio and PEP-703 scopings; matmul figure
re-benchmarked locally (42.2 s pure Python / 0.0023 s NumPy on this machine;
the printed ~2 min / 0.012 s / ~10,000× is self-consistent to the digit).
**The four §4o re-carries hold the register** — blind readers, not knowing
they were re-carries, named the GIL lost-update race and the pickle coda
among the chapters' best passages; kept verbatim.

**Wrongly cleared, found & fixed (20 surgical edits).** Quote-class — the
§4o replacement class, a third instance inside its own chapter: fig 6.2's
"I wanted Simula's expressiveness and BCPL's efficiency, on a real machine,
for real systems" is attested nowhere → replaced with the verbatim HOPL-II
opening sentence ("C++ was designed to provide Simula's facilities for
program organization together with C's efficiency and flexibility for
systems programming" — *A History of C++*, 1993); fig 7.2's first-person van
Rossum naming quote was a recasting of the third-person Python FAQ →
replaced with his real first-person sentence from the *Programming Python*
foreword (1996; python.org/doc/essays/foreword), attribution updated;
fig 4.1's "microkernels have won the intellectual debate" was
paraphrase-in-quotes → the verbatim "the debate is essentially over.
Microkernels have won." Figure arithmetic (all recomputed): fig 4.5 avg
waits 8.5/7.0 → **8.75/7.75** (from the figure's own workload; the RR and
MLFQ lane sequences verified exact); fig 5.1 x86-64 "7 bytes" → **4**
(8D 04 37 C3, assembled twice independently); fig 5.6 malloc(150) fit its
own free 240 B chunk → **malloc(300)**; fig 6.9 banner "six standards" →
**seven** (98/03/11/14/17/20/23 drawn); fig 4.21 batch net 2 → **4 Gbps**
(the one column that broke the figure's own "fully accounted" invariant —
CPU/RAM/IO sum exactly). Fact-class: the inode table glossed ctime as
"created" → "changed" (POSIX st_ctime = status change; classic inodes store
no creation time); figs 5.2/5.3 "UNIX v1 · PDP-7 asm / 1971" → "UNIX ·
1969" (First Edition, Nov 1971, was PDP-11 assembly — the labels
contradicted fig 5.3's own caption); fig 4.3 "~30 million lines of C,
loaded once at boot" → "carved from ~30 million…" (the tree is not the boot
image — the label undercut the figure's own modules story); fig 5.7 banner
"EVERY MAJOR BROWSER CVE OF THE 2010S WAS ONE OF THESE TWO" (leaks are
never CVEs; UAF ≈ a third) → "UAF ALONE: A THIRD OF SEVERE BROWSER CVES" —
the render check found the old banner also physically interleaved with both
columns' bottom lines at HEAD (36×6 / 20×6 px), so the shorter true banner
clears them in both engines; fig 7.6 "BINARY_MUL" (an opcode that never
existed) → "BINARY_MULTIPLY" at font-size 7 (same footprint; sanctioned);
fig 7.8 "return view" → "return array" (np.dot allocates, and the label
contradicted its own caption); ch5-portability-p7 "B's wordless model" →
"word-only" (contradicted "word-oriented" two sentences up);
ch5-ub-p2 "The list is short" → "The core of the list is short" (C11 Annex
J.2 enumerates ~200 UB kinds); ch5-survives-p3 "the Android Bluetooth stack
moved" → "is moving" (partial migration); ch7-gil-p2's mid-word HTML break
rendered "single- threaded" → rewrapped.

**Considered and declined** (defense overturned with sources, or
documented; do not "fix" blindly): Dirty COW "patched it within hours" —
the fix commit's author date is 2016-10-13T20:07Z, the same day as the
07:45 UTC Red Hat report (the 18 Oct date is the embargo merge; verified
against the GitHub API directly); pipe dating stays 1973 (conflict of
primaries: Ritchie's Evolution paper says 1972, the V3 manual documenting
pipe(2) is Feb 1973 — flagged, not guessed); Steve Russell "transcribing
the paper" — attested in his Smithsonian oral history ("I'd been
hand-compiling all sorts of things like that for two or three months");
ceval.c "ten thousand lines" (generated_cases.c.h is #included at the
switch site: 3.13 ≈ 9.4k, 3.14 ≈ 16k); CPython "roughly one million lines
of C" (current trees measure 0.93–1.04M raw .c+.h lines); array decay as
PDP-11 idiom (Ritchie invented the decay rule for the PDP-11 retarget — the
flag had it backwards); "(seL4, QNX, the formally-verified ones)"
(enumeration, and p5 already scopes seL4 precisely); "pipes between every
pair" (neighbour idiom, figure disambiguates); SJF row + "lowest possible
average wait" (canonical Silberschatz claim, non-preemptive class); MLFQ
caption (the "demoted" stamp carries C's descent); "Until 1973 … assembly"
(generic self-scoped by p3's "the normal state"; MCP/Multics never left
their machines); fig 6.1 "had not evolved since 1973" (Ritchie: X3J11's one
important change was borrowed *from* C++); "1980s software crisis" phase
framing; "50,000 lines" era-scoped; moved-from "valid-but-empty"
(guaranteed for vector, the drawn case); fig 6.5 return-value asymmetry
(the exception path is the C++ error path, primed by p2/p3); modules
"obsoleted/replacing" (the parallel C++11 panel defines the idiom); "ANSI
ratifies" (ANSI approved the US edition, 27 July 1998); "Cox · NeXT ·
Apple" (lineage idiom, matches the tree's loose slot grammar); "C's first
child" (conception 1979); ~20 lines of C per NumPy op (the ufunc tutorial's
inner loop is literally 21 lines); "favor"/"behavior"/"math" (-or/-our
outside the §5 ruling; register is the owner's); fig 7.1
"tokenize/optimize" (§5(d) code registers); "Resource Acquisition Is
Initialisation" (Pass-19 ratified sweep); fig 5.9 "roughly 10 µs" label vs
"a few µs" caption (both order-correct, §4o wording deliberate).

**Flagged for the owner read (no edits — untouchables and register):**
1. **`requestz` in the pickle coda (`ch7-datasci-p7`)** — the named
   typosquat is a real, live, apparently legitimate PyPI package (author
   Han Zhichao, HTTP 200, benign metadata; verified twice independently);
   the sentence effectively labels a real maintainer's package malware.
   The coda is untouchable under this brief, so nothing was changed.
   **Ready one-word fix if you want it: `requestz` → `request`** — a
   documented malicious requests typosquat (Sonatype 2022 ransomware
   incident), currently 404 on PyPI, still one keystroke from `requests`.
2. ch7 hero lead "an order of magnitude of performance" understates the
   chapter's own numbers (~150× fig 7.7, ~10,000× fig 7.9); heroes are
   untouchable.
3. ch6 hero lead "By 1979, C was running million-line systems" —
   unverifiable (V7 ≈ 10⁵ lines; 5ESS is 1982+).
4. Geometry, punch-list class: fig 6.1's "C++ released" marker sits on the
   1995 tick (x=540; 1985 ≈ x=312); fig 4.5's MLFQ lane leaves C undrawn
   from its t=2 arrival until t=17 (not a legal MLFQ trace as drawn);
   fig 4.5's RR lane draws 14 uniform slices = 28 units against 26 of
   work; fig 7.6's BINARY_MULTIPLY line overhangs its rect ~8 px/side
   (pre-existing overhang class).
5. Register-class reader flags (punch-list): the fig 4.1 caption
   re-litigates the body's verdict; the fig 4.9 caption re-runs the fault
   taxonomy; fig 5.3's caption/banner/body triple the "portable PDP-11
   assembler" thesis; the fig 6.9 caption repeats the SVG's own closing
   lines; ch7-cpython-p2 retells the §01 switch sentence; "Inheritance is
   layout" promises layout, delivers dispatch; ch7's nav item 06 diverges
   from its section eyebrow; "Van Rossum 1989-91" hyphen. Pass 19's
   Part II flags (closer label / headline) stand untouched.

**Invariants.** Anchor-id set **byte-identical to HEAD (346)** — verified
after every edit block (sorted-set md5 unchanged). Glossary regenerated:
**count 519, no entry added or removed, zero definition changes** —
timestamp-only diff; the DH merge state and the `thompson` quirk stand.
Greenbar identity, heroes, LISTING lines, EOF closer, Phase-2 items
(Little's Law mechanism, the ch4-security-p18 stamp), the pickle coda,
thesis set and authorship line untouched. Figure edits: text labels only;
the single attribute change is one font-size 8→7 (BINARY_MULTIPLY, width
containment); no geometry moved.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308): Chromium **and** WebKit at 1440 + 375, dark + light, on
part-2/index/glossary — 24 page-checks: **0 console errors, 0 external
requests, 0 page h-scroll, nav 48 px** (index and glossary carry their own
headers by design), fonts loaded, all internal #anchors resolve. All 18
touched sites screenshot-captured in both engines, dark + light (76
shots); the width-sensitive labels (both replacement quotes, the
BINARY_MULTIPLY line, the carved-from label, the new fig 5.7 banner)
reviewed at zoom — the fig 5.7 banner now clears the lines the old one
crossed; zero viewBox overflows across all touched figures. **Live after
push** (commit `f9c399b`): all 18 corrected strings confirmed on the live
page ("avg wait: 8.75", "4 bytes", "malloc(300)", "seven standards",
"changed, modified, accessed", "net: 4 Gbps", "the debate is essentially",
"C++ was designed to provide Simula", "I chose Python as a working title",
"UNIX · 1969", "carved from ~30 million", "UAF ALONE", "BINARY_MULTIPLY",
"return array", "word-only", "The core of the list", "is moving", the
rewrapped "single-threaded" among them); origin glossary.json serves 519.

## 4p. Pass 16 (2026-08-02): the language pass, Part III — Ch8–12 (commit `c4c41ea`)

Same brief, same bar (the Ch7 pickle coda — Part II — untouched). **Method:**
deep read of all of Part III, then a 9-reader / per-batch adversarial-defense
Workflow plus 3 fact agents (target = what survived defense). Three agents
died mid-run on API 500s (ch8-b, ch9-b readers; ch8-ch9 facts) and were
recovered by `resumeFromRunId` (which re-ran them on Opus 4.8 — a second
independent set of eyes on those batches). Then rewrites, then a 3-lens
confirmation gate (facts / internal-consistency / voice) over the full diff —
which caught **2 must-fix figure/caption contradictions I introduced**
(handshake SVG still said "1.5 RTTS" after the caption was corrected to one
RTT; Shannon SVG marker still said "56k" after the caption moved to V.34) plus
6 nits. All fixed before commit.

**As with Part II, the prose already holds the bar** — the defense overturned
most style flags. The one genuine mechanism re-carry: **twisted-pair**
(ch8-substrates-p2) named "twisted to cancel interference" without running it;
now runs common-mode rejection cause-to-effect (receiver reads only the
difference; outside noise lands equally on both wires and subtracts to zero;
the twist keeps them balanced). Everything else was a **~40-item fact pass**
(Part III had never had Part I's §4g scrutiny):

| Ch | Corrections |
|---|---|
| 8 | Shannon's "Rubik's-cube proof" was a **joke song**, not a proof → replaced with his real juggling theorem; "lived to see the networked world" — he had **Alzheimer's** from the early 1990s → "gave the mathematics to a world he could no longer quite see"; the 56k-modem capacity example exceeded its own printed limit → **V.34 33.6k hugging the Shannon ceiling** (SVG marker + caption + the V.90 digital-downstream note); "slightly faster on fibre" → "about the same" (fibre ≈ copper propagation); **TEMPEST** direction fixed (Van Eck 1985, from across the street); **WEP** 1999 → shipped 1997, broken by 2001; Ethernet was **not Metcalfe's doctoral work** (his rejected thesis was the ALOHAnet analysis; Ethernet carried it to a wire); **Butler Lampson → Gary Starkweather** for the laser printer; PARC Ethernet **2.94 Mbps** vs the standardised **10BASE5 (DIX 1980)** — "original… late 1970s" split, and the Manchester-section "Original Ethernet (10 Mbps)" relabelled 10BASE5; the **"Networking is inter-galactic" pull-quote** was a fabricated Metcalfe/1973-whiteboard attribution → J.C.R. **Licklider's** real 1963 "Intergalactic Computer Network" memo; MAC-flooding "Mike Beekey 2000" → the documented **macof/dsniff** lineage |
| 9 | **ARPA** glossed as "Defense Advanced…" in a 1966 context → not yet DARPA (renamed 1972); "**six years** after the Cuban Missile Crisis" (1962→1969) → seven; **traceroute** "this is what bounds traceroute" (backwards) → the mechanism traceroute *exploits* (TTL 1, 2, 3… each hop announces itself); CGNAT wrongly credited with **IPv6↔IPv4 translation** (it is v4-to-v4) → native v6 where both ends speak it, CGNAT only where they don't |
| 10 | 1986 congestion collapse "a single 400-**metre** cable, lightly loaded" → Jacobson–Karels' **400 yards, three IMP hops** (dropped "lightly loaded" — it was congestion); handshake "**1.5 round trips** before a byte" → one full RTT (third ACK may carry data), SVG label matched; **CUBIC curve inverted** ("slowly then faster") → fast-after-loss, plateau near W_max, then accelerate above; QUIC migration "keeps its **TCP** connection alive — TCP could not" → **QUIC** connection (TCP tied to the four-tuple); random-ISN "retrofitted into every OS **within a year**" → RFC 1948 followed about a year after, stacks took the decade; **2·MSL** parenthetical fixed (2·MSL ≈ 60 s on Linux, not MSL); "**Two chapters** from now the stack is complete" → one (Ch11) |
| 11 | HTTP "**Forty years**" → three and a half decades; web server "**eighteen months**" after March 1989 → Christmas 1990; "existed for **nine months**" → seven; DNS "~360M names **deep** at its widest" → a handful of levels deep, ~360M **wide**; Kaminsky fix "minutes to **thousands of years**/**centuries**" (two magnitudes, neither right) → both to "years"; **ENQUIRE** framed as a lab-wide CERN database → Berners-Lee's own earlier program; SHA-256 "what **every Git commit** uses" → Git is SHA-1 (body + p5 caption); Merkle trees "**TLS certificates** use" → a blockchain/CT structure; AES "**roughly fifteen rounds**" → ten to fourteen; "~150 **organisations**" → ~150 root *certificates* held by a few dozen operators (p4 + p5); **forward secrecy backwards** — "store-now-decrypt-later only threatens current/future, not historical recordings" is exactly wrong (quantum recovers the ephemeral DH from a *recorded* handshake) → historical recordings ARE the threat; HTTP/2 push "**removed from the spec**" → deprecated in practice, still in RFC 9113; Dyn "manually reconfigured anycast; aftershocks a week" → three waves, redundant-NS lesson; QUIC share hedged "by volume" both places |
| 12 | Sun HotJava "**late 1994**" → publicly May 1995; "**eleven weeks**" (unsourced, contradicts April→September) → cut in body + caption; V8 "**four-stage pipeline**" vs its own "two-tier" caption → "tiered"; "originally interpreted by **SpiderMonkey**" → Mocha, soon rewritten as SpiderMonkey; **libuv** "added in 2009" → libev/libeio, unified as libuv in 2011 (matches p5); rendering "**five-stage pipeline**" (body listed six) → count dropped; DOM frameworks "pipeline runs once instead of fifty" → fewer mutations + no forced reflows; typeof-null "**leftover**" quote (unverifiable) → the real Mocha value-tagging cause; SameSite "**every major browser**" → Chrome/Edge only; CSP "sites without CSP are the exception" → softened |

**Declined** (defense overturned; deliberate): most caption/body overlap
(figure self-containment); the lossy-codecs-on-Shannon's-curve line (final
entropy-coding stage genuinely rides the bound); the Chiu–Jain AIMD glosses
(at altitude); "physics, mathematics, practitioner cleverness" (content-bearing);
Netscape-2.0-SOP dating; the ch9-security "twenty-three-year-old Morris" (22 at
release but universally reported as 23, and Part I's Ch3 already says 23 —
left consistent rather than split).

**Invariants.** Anchor-id set byte-identical (**380** — pass-10 added one to
the fact-verified 379). Chapter order, heroes, part taglines, and the three
prior-pass Phase-2 items (Shannon–Hartley mechanism ch8-shannon-p12, "State
is the attack surface" ch10-attacks-p9, "Protocols earn their shape"
ch11-modern-p7) untouched. Two SVG **text-label** edits only (handshake RTT,
modem name), each §4g-precedented and matched to its corrected caption.
Glossary regenerated: **count 520, no entry added or removed** — after
catching that an em-dash in the SpiderMonkey edit had minted a junk
`spidermonkey` entry (reworded to break the cue); 12 definitions refreshed,
all coherent. American "artifact" caught by the gate and returned to British
"artefact."

**Verification.** Local (CF-mimicking server) + **live after push** (commit
`c4c41ea`, live ~30 s later): Chromium + WebKit at 1440 + 375 on
part-3/index/glossary — 0 console errors, 0 external requests, 0 h-scroll,
nav 48 px, fonts loaded. Both touched figures + key rewrites screenshot-
reviewed in both engines, dark + light; live SVG labels confirmed
("ONE FULL RTT", "V.34 33.6k"). **STOP for owner review before Part IV** —
the gate rhythm. Remaining language-pass parts: IV, V.

### Pass-16 verification (2026-08-02, commit `17e904e`)

Full audit of Pass 16 (parts of which had been executed by a weaker model
after a session safeguard drop). Method mirrored the Pass-14 verification:
deep read of all of Part III by the verifying model, plus 5 independent
per-chapter fresh readers with web access; every flag adjudicated by the
verifying model against an adversarial defense; the listed load-bearing
corrections re-verified against primary sources or recomputed.

**The ~40 fact corrections: all stand.** Independently confirmed:
forward-secrecy direction (Shor on a *recorded* ECDHE handshake recovers the
ephemeral secret — historical recordings ARE the store-now-decrypt-later
threat; the mechanism, not just the claim, checks); Licklider's April 23,
1963 ARPA memo ("Members and Affiliates of the Intergalactic Computer
Network" — addressee line, "salutation" fair); Starkweather (SLOT 1971 at
PARC; Lampson/Rider built EARS's *character generator* — the old Lampson
attribution was indeed wrong); Metcalfe (Harvard rejection first, ALOHA
math added at PARC to the revision — confirmed); 1-RTT setup (recomputed:
client's first data byte leaves at exactly 1 RTT; SVG label verified live);
Shannon (Rubik's-cube piece was the song "A Rubric on Rubik Cubics" — the
old "proof of solving distance" was flatly wrong; juggling theorem real;
Alzheimer's signs from ~1985, diagnosed 1993 — "through the 1990s" holds);
V.34 33.6k (V.34+ 1996; caption math self-checks: 30 dB / 4 kHz → ≈40 kbps
ceiling vs 33.6k); CUBIC (concave-to-W_max-then-convex — the un-inversion is
correct). WEP 1997, macof/dsniff lineage, Dyn three waves, HotJava May 1995,
2·MSL ≈ 60 s Linux, RFC 1948 timing, Kaminsky "years" recompute — all check.
**The twisted-pair re-carry holds the register** (runs common-mode rejection
cause-to-effect, no announcement scaffolds) — kept verbatim.

**Wrongly cleared, found & fixed (~30 surgical edits + 2 re-carries):**
Five fact-class: `ch8-ethernet-p1` credited the radio analysis to the
*rejected* thesis (it was added after the rejection and rescued it —
contradicted p2's own timeline); `ch10-handshake-p1` "why three?" gave a
false reason ("two would not let the server pick its own starting sequence"
— it can pick in two; it can't get it *acknowledged*); `ch10-attacks-p7`
"weeks fingerprinting" — Shimomura's own tcpdump shows ~minutes of probing
on Christmas afternoon revealing the fixed +128,000 ISN stride; `ch11-tls-p2`
"mutually authenticated" (web TLS proves the server only); `ch12-hero-lead`
"runs in every database that speaks JSON" (JSON is data, not executable JS
— reworked to the object-literal-syntax-became-JSON truth). Two re-carries
of the brief's exact class: the **TLS 1.3 handshake now runs in prose**
(DH halves → shared secret → encrypted first reply → signature → transcript
hash; it had lived only in the fig 11.11 caption — Ch11's centerpiece), and
the **forced-reflow mechanism** in `ch12-dom-p3` (Pass 16's own rewrite
derived the slowdown from mutations; the real cause is interleaved layout
*reads* — offsetHeight between writes — forcing synchronous re-layout; the
dated innerHTML folk-claim dropped). Consistency/caption fixes: fig 12.1
"by 1994 … failed" contradicted Pass 16's own May-1995 HotJava correction
(→ mid-1995, label + a11y title matched); fig 12.7 label "~16 ms each" →
"one ~16 ms frame" (5×16 ms would be 12 fps — contradicted ch12-loop-p3);
DOM section now counts five stages consistently in h2, body, and caption;
fig 12.7 caption no longer re-runs *parse* on appendChild; fig 9.6 caption
"picks the shorter one" of two equal-length paths → policy picks (matches
its own figure); ARP caption's "switching contains spoofing" → switching
alone does not (port security / dynamic ARP inspection do); `ch9-ip-p3`
garbled "(since IPv4)"; SYN-cookie prose now runs verification correctly;
timeout vs triple-dup-ACK responses split correctly (halve vs reset-to-1);
"queues collapsed" → overflowed; 20 ms voice-gap premise carried;
longest-prefix-wins now runs in `ch9-security-p4` (the marquee YouTube
story's crux was fiat); one-clause v6 deadlock mechanism + RIR "years that
followed"; Ch8/Ch9 count stitch (billions of devices, *tens of* thousands
of networks — matched ch9-routing-p1); plus small date/wording precision
(Simonyi "soon to write", motorised pogo sticks, CERT "within weeks",
"young internet", QUIC in Chrome 2013→2017, "HTTP/2's share", BIND
maintainers, "a handful of people at CERN" for Aug 1991, Netscape brief
grammar ×2, V8 caption "two-tier core").

**Considered and declined** (do not "fix" blindly): Morris "23" (kept —
cross-part consistency, ledger-documented); Manchester caption convention
(matches its own figure's drawn "HIGH→LOW = 1" CONVENTION strip; body stays
agnostic); example.com's literal IP (rhetorical stand-in; any real IP goes
stale); chapter-meta div nesting ×5 (uniform across all chapters, renders
verified — identity structure); V8 four-tier reality beyond the "core"
soften (figure draws two tiers; body says "tiered"); ch10's HTTP/2-HOL
name-only mention (Ch11 runs it); `TCP`-only key-term span on "TCP
hijacking" (extractor quirk, pass-15 precedent); Kleinrock-1962 priority
framing (mainstream account); Pass 16's declines all re-checked and upheld.

**Invariants.** Anchor-id set byte-identical (380). Glossary regenerated:
**count 520, no entry added or removed** — first regen garbled `dom` and
front-truncated `rtt` (em-dash-heavy rewrites broke the extractor's
clipping, the documented pass-15/16 failure mode); prose reflowed, final
regen has 7 definitions refreshed, all coherent (`ethernet`/`xerox parc`
now carry the corrected thesis line, `congestion avoidance`/`rtt` the
corrected loss-signal sentence). §4g and all Pass-16 corrections survive in
substance. Two figure-label edits only (fig 12.1 date, fig 12.7 frame
budget), both §4g-precedented text labels with a11y titles matched; no SVG
geometry touched.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308): Chromium + WebKit at 1440 + 375 on part-3/index/glossary — 0 console
errors, 0 external requests, 0 h-scroll, nav 48 px, fonts loaded, part-3
anchors resolve. 14 edited passages screenshot-reviewed in both engines,
dark + light. **Live after push** (commit `17e904e`): marker strings and
both corrected labels confirmed on the live page. **STOP for owner review
before Part IV** stands — Parts IV–V remain, to run on the verifying-model
session; if a session drops off Fable mid-part, stop at the next ledger.

## 4q. Pass 17 (2026-08-03): the language pass, Part IV — Ch13–15 (commit `e639b98`)

Same brief, **recalibrated by the owner: pedagogy is the first goal** (the
book enjoyable, mechanisms *felt*, never a list wearing prose); facts are the
second job, not the first. Every section judged as a reader who wants to be
gripped, and each clearance re-read once against "would I enjoy reading this?"
before a flag was declined. **Method:** deep read of all of Part IV plus 3
independent per-chapter reader agents (pedagogy-lens, web-enabled), every flag
adjudicated against an adversarial defense; load-bearing facts recomputed or
checked against primary sources.

**Part IV holds the bar.** Ch13's bank-transfer/WAL/MVCC run, Ch14's
DH-commutativity and RSA-Euler spine (pass-11 §2B/§2C work) run, Ch15's
data-as-code unification is *performed* not asserted (ch15-culture-p1). The
pass is **four light pedagogical re-carries + a cluster of fact fixes** (Ch14,
the "math in depth" chapter, carried the most).

**Re-carries (the primary job):**
| # | Item | Change |
|---|---|---|
| 1 | `ch13-algebra-p3` | Six-operator roll-call (∪, −, ×, ρ) was four definition-strings. Now each buys a felt question — *difference* IS "the customers who never ordered"; *cross product* a firehose you bolt a selection onto to rebuild the join from parts. |
| 2 | `ch13-sql-p4` | Dead frame paragraph (added nothing its captions didn't) now runs the N×M cost that makes the three join strategies matter — a trillion row-comparisons on two million-row tables, minutes of work — so the reader feels *why* the optimiser's choice is load-bearing. |
| 3 | `ch14-ecc-p4` | "The pragmatic difference is mostly cultural" — a shrug where the story should land. Now runs the real split: secp256k1 (cheap, rigid, nothing-up-my-sleeve) vs Curve25519 (shaped so the fast path and the constant-time path are the same path). Same trapdoor, different thing each was hardened against. |
| 4 | `ch15-defense-p1` | Five-generation roll-call with parenthetical dates *asserted* "each was a response to the failure of the one before" and never showed one. Now runs the whole cascade cause-to-effect: firewall waves port 80 through → IDS has no signature for the new attack → SIEM sees only its slice of network logs → the evidence lives on the endpoint (EDR) → a decade of breaches says *inside* should confer no trust → zero trust. |

**Fact fixes (real errors still matter, Parts II–III proved it):**
| Ch | Corrections |
|---|---|
| 13 | **IMS "neither survived two decades"** — IBM still ships IMS in 2026; corrected to "neither would define the era that followed," IMS noted as niche survivor. **Selinger "most-cited paper in database history"** → "on query optimisation" (Codd out-cites it and is praised two sentences later — self-undercutting). **Projection-pushdown identity was false** — inner projections must retain the join key or the join degenerates to a cross product; corrected, sitting as it did directly above "the transformations are correct because the algebra is rigorous." B-tree **1970** not 1971 (SIGFIDET); Codd paper **eleven** pages not twelve (×2, pp. 377–387); "complete query language" → **relationally complete** (aggregation/recursion sit outside); great-grandparent; "in practice" ×2 dedupe. |
| 14 | **fig-14-2 "factoring 2048-bit takes weeks of supercomputer time"** — flatly false, contradicted the chapter's own "infeasible / age of the universe"; record is RSA-250 (829 bits, 2020, ~2,700 core-years). **PQC "all three based on lattices"** — SLH-DSA is *hash*-based (contradicted the same paragraph + fig-14-13); primer caption's "lattice-based replacements" matched. **fig-14-10 Cloudflare "saved petabytes of bandwidth"** — conflation of two posts; the real 2014 result is the private-key op ~9× cheaper. **RSA-vs-ECC key growth un-inverted** — RSA key grows ~cubically with the security level, not "cube root of attack work." **fig-14-3 "increasing order of attacker difficulty for a defender"** — garbled + backwards; reordered hardest→easiest with the 2¹²⁸/2²⁵⁶ bound. **DH "referees almost rejected as too speculative"** cut (unsourced; it was an *invited* paper). **OTP "eventually broken"** → provably unbreakable, foundered on key distribution. Ed25519 **2011** not 2005; SHA-3 **standardised 2015** (Keccak 2012); exponential-growth sentence fixed ("add a bit, work doubles; double the bits, it squares"); signature "decrypt with private key" scoped to RSA (ECDSA/Ed25519 noted); PGP source-as-speech precedent attributed to **Bernstein/Junger**, not the dropped case. |
| 15 | **Pwn2Own** funded by Trend Micro's **Zero Day Initiative** (not "vendors put bounties on their own products"). **Prompt injection dated 2022** (named/demonstrated Sept 2022). **Capital One** split into the $80M OCC fine (2020) + $190M class-action (2021), not "$190M direct cost." |

**Declined** (owner-settled or deliberate; upheld after the "would I enjoy
this?" re-read): **Sony PSN as SQLi** — pass-7 kept it as known-unconfirmed
lore, owner-aware through every gate since; not re-litigated (the caption's
scrupulous TJX carve-out sets a bar PSN doesn't meet, noted but left).
**Enigma "six years"** — consistent with Ch1's framing, a Ch1 question.
The **ch15-culture** CTF-category / red-blue-bounty / conference directory —
the most list-heavy stretch, but the hero explicitly promises an ecosystem
field-guide and the chapter's emotional close is the unification (performed)
plus the responsible-disclosure norm (run); intentional resource content, kept.
The **hashing three-property** list (fig-14-3 caption runs it with SHAttered).

**Invariants.** Anchor-id set byte-identical (**228**). Glossary **count 520,
no entry added or removed** — the re-carries bolded four real security-
generation terms (IDS, EDR, zero-trust, "relationally complete") whose auto-
extracted definitions were non-self-contained (they open with a parenthetical
date or back-reference); suppressed via `build-glossary.js` SKIP_WORDS (same
pattern as pass-14's `system v amd64 abi`) plus one math-annotation de-
emphasised. Also caught: the IMS insertion had polluted the `brittle` entry
(a `.)` before the term is not a clean sentence boundary for the extractor) —
de-parenthesised to restore it; `firewall`/`siem` definitions came out
*improved* (real definitions now, where before they were catalogue fragments).
Strongroom serif-on-cream reading stock untouched (deliberate identity, §4d/§5).

**Verification.** Local (CF-mimicking server: extensionless 200, `.html` 308):
Chromium + WebKit at 1440 + 375 on part-4/index/glossary — 0 console errors,
0 external requests, 0 h-scroll, nav 48 px, fonts loaded. 6 re-carries
screenshot-reviewed in both engines, dark + light — register holds, cream
stock intact, math (`y²=x³+7`) and σ/π/⨝ symbols render. **Live after push**
(commit `e639b98`): corrected passages confirmed on the live page. **STOP for
owner review before Part V** — the gate rhythm. Remaining language-pass part: V.

### Pass-17 verification (2026-08-09, commit `186cd32`)

Full Fable audit of Pass 17, whose clearances had never had a second read
(brief: `docs/pass-17-verification-brief.md`). Method mirrored the 14/16
pattern: deep read of all of Part IV by the verifying model, plus a 25-agent
workflow — 6 independent per-chapter fresh readers (student + sceptic lens,
web-enabled, blind to §4q), 4 primary-source verifiers over the load-bearing
corrections, an adversarial defense per flagged anchor (15 run: 7 conceded,
7 partial, 1 held) — 72 raw flags in 49 anchor groups, every one adjudicated
by the verifying model; all fixes gated through a fact-and-voice confirmation
agent over the diff, which caught the verifier's own error again ("two shapes
this chapter closes on" against the chapter's six-pattern close).

**The §4q load-bearing corrections: all stand.** Reconfirmed against primary
sources or recomputed: RSA-250 (829 bits, 2020, ~2,700 core-years); SLH-DSA
hash-based / ML-KEM+ML-DSA lattice (FIPS 205/203/204); fig-14-10 Cloudflare —
the 2014 post's own sentence says the private-key op is cheaper "by a factor
of 9.5x" (9516.8 vs 1001.8 signs/s recomputed), so "about 9×" is faithful;
RSA-vs-ECC growth (SP 800-57 Table 2; ECC exactly 2s — linear); fig-14-3
ordering coherent in labels, caption, and subtitle; fig-14-8 re-verified to
the digit; Ed25519 2011 (eprint 2011/368); SHA-3 2012/2015 (FIPS 202);
Bernstein/Junger; IMS alive (15.6 GA 2025); Selinger scoping (Codd 3,612 vs
Selinger 2,489 citations — the old superlative would have been false);
projection-pushdown recomputed under set semantics; B-tree 1970 SIGFIDET;
Codd pp. 377–387 = eleven; relationally-complete per Codd 1972; Pwn2Own =
ZDI-funded; prompt injection Sept 2022; Capital One $80M (OCC NR 2020-101)
+ $190M (Dec 2021); TJX WEP carve-out. **The four §4q re-carries hold the
register** — blind readers, not knowing they were re-carries, quoted two as
their chapters' best passages; kept verbatim (one caption echo trimmed,
below). All six blind readers: Part IV grips; at bar for the large majority.

**Wrongly cleared, found & fixed (~30 surgical edits).** Fact-class in prose:
`ch14-history-p1` Enigma — "six years before *Bletchley* broke it" fused the
Polish timeline with British credit (six years from 1926 military adoption
lands on Rejewski's December 1932 reconstruction; the Bombe is 1940); credit
re-aimed to Rejewski's team, "a break Bletchley industrialised with the
Bombe", the settled six-year *count* untouched, Ch1 cross-ref kept (part-1
verified silent on "six years" — the old decline rationale was hollow);
`ch14-history-p3` observer list Bletchley → Rejewski. `ch13-acid-p1` +
fig 13.5 "IBM's Jim Gray"/"IBM 1981" → Tandem (TR 81.3; Gray left IBM 1980).
`ch13-codd-p5` System R "begun in 1973" → 1974 (Chamberlin; the body
contradicted fig 13.1's correct 1974–1979 on the same page); Ellison's
"small consulting firm" employer clause cut. `ch13-codd-p6`/`p7` "IBM
Almaden" ×2 → San Jose (Almaden opened 1986; the figure had it right).
`ch14-history-p4` "ceased to be a munition in 2000" → off the US Munitions
List 1996 (EO 13026), rules liberalised 2000. `ch14-history-p6`
Cocks/Williamson "implemented" → worked out on paper, never deployed.
`ch15-mindset-p1` "Congressional Record" → Senate's published hearing record
(S. Hrg. 105-609). `ch13-codd-p8` the non-existent title → two
*Computerworld* pieces. `ch13-codd-p2` CODASYL was a committee, not a
database. `ch15-defense-p6` SolarWinds Fortune-500 moved from
malware-delivery claim to customer-roll fact; "(SLSA)" re-labelled signed
build provenance (SLSA, sigstore). Figure text labels (a11y titles matched,
zero geometry): fig 15.8 keyboard EoP CVE **2010-2549 → 2010-2743**
(MS10-073, NVD: demonstrated in the wild by Stuxnet) and "three machines per
host" → per USB drive (Symantec dossier); fig 15.2 "Google 2022" → **2020**;
fig 13.1 PostgreSQL 16 → **18** (GA 2025-09-25; the figure's other branch is
stamped 2026); fig 13.5 fsync listed as a hazard durability survives — cut;
fig 13.6 ARIES footer no longer claims PostgreSQL (redo-only WAL noted — the
§4g ZooKeeper/ZAB precedent class); fig 13.8 "~1 leaf per million rows" →
per few hundred matches (contradicted its own caption by ~10⁴); fig 13.9
index storage "of column data" → of the table; fig 13.10 "blind SQLi" on an
error-based payload → error-based (body's blind definition re-scoped to
timing/behaviour); fig 14.7 numbering gap ③→⑥ closed (⑥⑦ → ④⑤, both
panels); fig 14.8 "e = 3 (very common choice)" → "small, for legibility;
real RSA uses 65537" (contradicted its own caption); fig 14.3 MD5 cell
"2⁶⁴ · feasible 2004" → "broken 2004 · seconds today" (a birthday bound
masquerading as attack cost beside SHA-1's true 2⁶³); fig 14.13 Apple split
out (Cloudflare/Google hybrid TLS 2023; Apple's 2024 item is iMessage PQ3 —
Safari TLS PQC was not a 2023–24 fact); fig 15.4 attacker's forged MAC
de-collided from the body's real-gateway MAC, "first wins" → keeps-answering
(RFC 826 updates on later claims; matching one-liner in `ch15-network-p4`);
fig 15.9 side-channel FIX → "constant-time code · isolation" (constant-time
crypto does not fix Spectre); fig 15.10 → "Microsoft Bounty — top offers
reach seven figures" (BlueHat is the conference; million-dollar *payouts*
unsupported). Consistency/register: DBMS industry "fifty-billion" → hundred-
billion (Gartner ~$120B 2024); Pwn2Own "Vancouver and Toronto" → Berlin/
Cork/Tokyo; `ch14-tls-pqc-p3` verbatim-duplicated signature sentence cut;
`ch13-sql-p5` caption's EXPLAIN closer cut (verbatim echo of the §4q
re-carry's new close one screen up — the pass-14 self-created-duplication
class); `ch15-defense-p2` caption's Helsinki/Tokyo pair trimmed (the
re-carry p1 carries it); `ch13-acid-p2` aphorism un-crossed ("isolation
protects against concurrency; consistency is what the other three exist to
preserve"); `ch14-primer-p3` "four such operations are known" → four carry
this chapter, the lattice fifth stands behind them (was contradicted by
§06); `ch14-hashing-p3` BLAKE3-a-decade → the BLAKE family; `ch15-memory-p1`
/`p2` "thirty-five years" ×2 → nearly forty (h2 says forty; axis 1988→2026)
and "gotten" ×2 → grown; `ch15-memory-p4` PAC "a few transistors" → a corner
of each core; `ch15-network-p1` "detectable and reversible" → a detected lie
kills the connection; `ch15-web-p1` "most of those bugs are confused
deputies" → two of the six shapes (gate's wording); `ch15-culture-p7`
"empty" → pure data abstraction; Diffie–Hellman en dash in the TOC card and
fig 14.7 caption.

**Considered and declined** (do not "fix" blindly): **Sony PSN as SQLi** —
owner-ruled since pass 7; re-flagged high by two blind readers and conceded
by its own defense on the facts; left untouched per the ruling, with the
readers' evidence recorded for the owner read (vector never publicly
confirmed; the confirmed 2011 Sony SQLi is LulzSec/SonyPictures.com).
Enigma six-year *count* (settled; only the attribution was repaired). Caesar
"worked for a generation"/"contemporary cryptanalyst" (hedged narrative
compression). The six-operator set counting ⨝ (pedagogical set; the
paragraph itself derives join from × — formalism quibble). Caption
self-containment (`ch13-codd-p7`, `ch13-indexes-p5`, `ch14-tls-pqc-p8` — house
convention, pass-14 precedent) and the SolarWinds insight-strip double-tell
(display element, self-contained by design). Fig 14.11 "every byte
accounted for" vs the skipped Master Secret stage (teaching abstraction).
Fig 14.1 "3-rotor + plug" on the 1923 cell and "Bombe 1940" marker (era
compression; prose now carries the Polish credit). Fig 13.2 row-count/
distinct-note compression. `ch15-memory-p1` superlative + itinerary leads
(functional orientation). `ch14-publickey-p6` "RSA encryption takes
microseconds" (public-op, defensible). The `key-term` "Diffie-Hellman"
hyphen kept — it mints the glossary's `diffie-hellman` key, and part-3 has
five more hyphenated instances: book-wide dash sweep is Pass 19's.

**For Pass 19:** fig 15.2 *geometry* — the "PAC · CET shadow stack / 2017+"
green group (x≈560) sits right of "Spectre / 2018" (x≈500), inverting
chronology and implying PAC answers Spectre (it answers ROP/JOP); move the
pair left of Spectre or give Spectre its own response dot (retpoline/
microcode). Ch15 title "Attack and Defense" (American) vs the hero's own
"DEFENCE IN DEPTH" and uniformly British body — title/identity call for the
owner or the sweep. Book-wide Diffie–Hellman dash harmonisation (with the
glossary-key migration it implies).

**Invariants.** Anchor-id set byte-identical to HEAD (**228**). Glossary
regenerated (twice, once after the gate repair): **count 520, no entry added
or removed**; 6 definitions refreshed, all coherent (`pwn2own`/`ccc`/`black
hat` carry the new venues, `edr` the deduped SIEM sentence, `codasyl` the
committee correction, `hellman` the on-paper wording); no junk entries
minted. §4g and every §4q correction survive in substance.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308): Chromium + WebKit at 1440 + 375, dark + light, part-4/index/glossary —
24 page-checks: 0 console errors, 0 external requests, 0 h-scroll, nav
48 px, fonts loaded; all 39 internal #anchors resolve. 24 touched passages
screenshot-shot in both engines, dark + light (193 shots); the width-tight
labels (Stuxnet USB line, PQC deploy line, ARP ③, ARIES footer, Gray/Tandem,
fig 14.7 renumber) reviewed in both engines — all render inside their boxes.
**Live after push** (commit `186cd32`): corrected strings confirmed on the
live page.

## 4r. Pass 18 (2026-08-07): the language pass, Part V — Ch16–18 (commit `eb80d7a`)

Same brief, same bar (pedagogy first, facts second; the Ch7 pickle coda —
untouched). The last part of the language pass, run under the amended gate
rhythm (per-part owner reads waived; Pass 19 verification before READY).
**Method:** deep read of all of Part V, then a 13-agent Workflow — 7
per-section student-readers (pedagogy lens, web-enabled) plus 3 fact agents,
then a per-chapter adversarial defense (target = what survived: 27 of ~40 raw
flags; caption self-containment, insight-strip narrative form, and the ch18
"None of X; all of them Y" chapter cadence all overturned). Then rewrites,
then a 3-lens confirmation gate (facts / internal-consistency / voice) over
the full diff — which caught **2 must-fix errors I introduced** (the CUDA
caption's "blocks cannot coordinate at all" — cooperative groups and
global-memory atomics both falsify it; rescoped to *synchronise* — and Knight
Capital's Power Peg described as a "test routine" where SEC Release 34-70694
says real, discontinued order-routing functionality) plus a half-applied
quantum hedge and 4 accepted nits. Screenshot review then caught a third:
the widened fig-17.11 label collided with its neighbours (shortened; the
HEAD label already overlapped the 2026 label — net improvement). All fixed
before commit.

**Part V holds the bar** — Ch16's race/CAS/Therac spine, Ch17's control-loop,
FLP, and CAP treatments, Ch18's trace and synthesis all run and grip. The
pass is **three pedagogical re-carries + a fact cluster** (Ch17, the
systems-lore chapter, carried the most).

**Re-carries (the primary job):**
| # | Item | Change |
|---|---|---|
| 1 | `ch16-lockfree-p3` | The four-ordering roll-call near-duplicated fig 16.5's table and dangled "the releaser" before release was defined. Now runs release/acquire through the paragraph's own `x = 1; flag = true` broken example — the store carries the promise, the load demands it, `x` crosses with the flag; seq-cst above the pair, relaxed below. |
| 2 | `ch17-consensus-p2` | Paxos's value-adoption rule was bare procedure with correctness outsourced to a proof date. Added the quorum-overlap witness argument (any two majorities intersect, so a preparing proposer must meet — and carry forward — any chosen value), which also sets up the adjacent N/2+1 callout. |
| 3 | `ch17-virt-p2` (caption) | "Heroic software tricks… ran an order of magnitude slower" was doubly wrong: no cause for why trap-and-emulate failed, and the 10× belonged to naive emulation, not BT/PV (Xen SOSP 2003 within a few %; Adams–Agesen 2006). Now runs the sensitive-but-unprivileged-instructions mechanism, credits BT/PV as near-native, and lands VT-x. |

**Fact fixes (item → verified-how → outcome):**
| Item | Verified how | Outcome |
|---|---|---|
| Knight Capital mechanism inverted (`ch17-microservices-p8`) | SEC Release 34-70694: new RLP build repurposed a flag; the un-updated eighth server read it as "run Power Peg" (real router, discontinued 2003; fill-counting moved out 2005); rescue financing 6 Aug 2012 (~70% dilution); Getco deal agreed 19 Dec 2012 | Strip rewritten: the lethal path is the *stale* server's retired code — which is the one story that actually proves the strip's heterogeneous-deployment moral. "Acquired weeks later" → rescue within the week, acquisition agreed before year-end |
| CP/CMS 1968 "VM/370 sessions" (`ch17-virt-p1`) | VM/370 is the 1972 System/370 reimplementation; CP ran CMS in per-user virtual System/360s | "many isolated CMS sessions — each inside its own virtual System/360" (glossary `hypervisor` def de-anachronised too) |
| EC2 "pay by the hour … billed to the second" (`ch17-virt-p1`, `-p3`) | AWS: hourly at 2006 launch; per-second Oct 2017 | "by the hour at launch, by the second today"; p3 → "billed only for what you used" |
| Amdahl pull-quote (`ch16-amdahl-p5`) | AFIPS 1967 text: "parallel/sequential *processing rates*", not "performance" | Quote restored verbatim |
| "Both terms come from Herlihy 1991" (`ch16-lockfree-p1`) | pdftotext over the TOPLAS paper: "wait-free" ×75, "lock-free" ×0 (Herlihy's weaker term is "nonblocking") | "The stricter term comes from…" |
| fig 18.2 "2 networks · 1 kernel" (1969, ×3 sites) | ARPANET was one network (UCLA→SRI Oct 1969, four nodes by Dec — the book's own Ch9); UNIX is a kernel | "1 network · 1 kernel"; caption "one network of computers, one kernel"; roll-call "a network and a kernel". "172 years" untouched |
| Dynamo/DynamoDB conflation (fig 17.8 + both CAP captions) | The 2007 SOSP paper is Dynamo (internal, vector clocks); DynamoDB is the 2012 service, no exposed vector clocks; fig 17.7 already said Dynamo | Label → "Amazon Dynamo"; captions → Dynamo with descendants named; `ch17-consensus-p9`'s DynamoDB left (true of the service) |
| CUDA blocks "synchronise with each other" (`ch16-gpu-p4`) | Blocks share nothing and cannot barrier in the base model; threads within a block do | Caption rebound to threads-within-a-block; "separate blocks cannot, and may only communicate through slow global memory" |
| Docker "built on a Linux capability called LXC" (`ch17-containers-p1`) | LXC is a userspace runtime over the namespaces/cgroups the same paragraph back-references; replaced by libcontainer (0.9, 2014) | "initially driving the kernel's namespaces and cgroups through LXC, a userspace container runtime it soon replaced with its own"; in-sentence "image format" dup removed |
| "datacenters run billions [of containers] globally" | Unverifiable; the sourced figure is Google's 2B containers/week (Beda, GlueCon 2014) | "By 2014 Google alone was starting over two billion containers every week" |
| Lambda "every invocation in a dedicated microVM" (`ch17-containers-p3`) | Firecracker NSDI'20: microVM per execution environment, reused across invocations, never shared across functions/customers | "dedicated Firecracker microVMs — each reused across invocations, never shared between functions or customers" |
| Spectre/Meltdown "every modern CPU since 1995" (`ch16-numa-p4`) | 1995 is the Meltdown/Intel claim; Spectre pair-wide needs speculation | "essentially every fast CPU since the mid-1990s"; punchline "cache coherence is… a security boundary" → "the cache is… the most expensive side channel" (its own body's mechanism) |
| fig 17.3 "all of them watch etcd" | Contradicted its own caption and API-server box; only the API server talks to etcd | Bottom line → "all of them watch the API server" |
| Brewer quote "'two of three'" (`ch17-cap-p2`) | IEEE Computer 2012: "The '2 of 3' formulation" (rest verbatim) | Restored |
| Goroutines "get the best of both" (`ch16-threads-p2`) | Caption's own trade-frame defines "both" as free IPC + corruption-impossible; goroutines race | BEAM genuinely gets both (share-nothing); goroutines "get the cheapness but keep the shared memory — and the races" |
| Boole node "Lincolnshire" (fig 18.2) | Laws of Thought written from Queen's College Cork (professor since 1849); the figure's place column is place-of-work | Node → "Cork, Ireland"; the "Lincolnshire schoolteacher" epithet (person, not place-of-the-moment) deliberately kept in lead + roll-call |
| Torvalds "a Helsinki Usenet group" (`ch18-civilization-p2`) | comp.os.minix is worldwide; posted from Helsinki | "posted from Helsinki to a worldwide Usenet group" |
| Quantum optimisation "fundamentally can't" (`ch18-future-p1` + fig 18.3 caption) | Grover is quadratic (BBBV-optimal); QAOA advantage unestablished | Lead restructured (optimisation "a more speculative third"); caption hedged to match |
| Neuromorphic "~1000× efficient on NN" (fig 18.3 label) | NorthPole ~22–25×, Loihi 2 up to ~100×; ~1000× only for sparse event-driven cases — and the caption says "order-of-magnitude" | Label → "10–100× efficient on NN" |
| Reading list "every entry… at least a decade" | DDIA is 2017 — nine years | "nearly every entry… a decade or more" (lead + caption) |
| Copy-cost absolute (`ch16-threads-p1`) | SysV shm/mmap existed pre-threads | "with every message — or hand-manage an explicitly shared segment" |
| Therac "first… in history" (`ch16-races-p6`) | Standard account but unprovable as an absolute | "first known software-caused medical fatalities" |
| House spelling / consistency | — | "artefacts" (SolarWinds strip), "rasterises" ×2, "recognise" ×2; "without compression" (final-p2) → "without hand-waving" (contradicted reading-p1's own compression framing); four-move litany in `ch18-intersect-p3` aligned to final-p3 + the closer ("follow the math… name the historical decision"); `ch18-math-p1` "graph-theoretic protocol" → "quorum arithmetic" (matches fig 18.1 and Ch17's actual argument); fig 17.11 serverless sublabel → "Lambda (2014) · FaaS" |

**Declined** (deliberate; do not "fix" blindly): **fig 16.8's Amdahl curves
end above their own ceiling lines** (p=0.95 terminates ~y164 vs its 20×
asymptote at y184; p=0.90 and p=0.50 similar) and **the CAP figures' spatial
encoding** (fig 17.7 parks "CA (impossible)" nearest the P vertex; fig 17.8's
AP dot-cluster hugs the C–A side and the "CA edge" note sits at the centroid)
— both genuine, both declined under this brief's text-labels-only /
no-SVG-geometry constraint; **flagged to Pass 19** for an owner-sanctioned
geometry fix. Also declined: "3 nm" (§4g owner-ruled, twice re-flagged, twice
upheld); `ch17-consensus-p9` DynamoDB (true of the service; no paper/vector-
clock claim attached); fig 18.2's 1969/1976 sublabel tightness (pre-existing,
one char looser now); the trace's station accounting and the "235 figures"
caption/prose layering (defense overturned — documented self-containment);
Gustafson pre-spoiler resolved by trimming the math callout to its own label
("The ceiling, in one equation") and moving the key-term to p7 — fig 16.9
keeps the formula.

**Invariants.** Anchor-id set **byte-identical (189)**. Glossary **count 520,
no entry added or removed** — the ch17-cap-p4 Dynamo appositive would have
minted a fragment entry; suppressed via `build-glossary.js` SKIP_WORDS
(pass-17 precedent), and the em-dash appositive kept for the prose. Nine
definitions refreshed, all improved: `acquire`/`release`/`sequentially
consistent`/`memory ordering` are now real definitions (were fragments),
`cache coherence` now defines coherence via MESI (was a KPTI fragment —
`ch16-numa-p1` hosts the term), `hypervisor` de-anachronised, `gustafson s
law`/`ap systems`/`docker` coherent. §4g Part-V terrain survives in
substance: ZAB (fig 17.8 label + 17.5 caption), Paxos-lore direction
("submitted 1990, printed 1998, still in costume"), Lambda "meters the bill
in milliseconds", fig 18.2 "172 years", "two hundred and thirty-five"
figure-count prose. Heroes, Quorum identity (constellation openers,
`.qm-quorum` closer, violet/teal), the `ch17-microservices-p6` stamp, thesis
set and authorship line untouched. Figure edits: **text labels only** (fig
17.3 bottom line, fig 17.8 Dynamo, fig 17.11 sublabel, fig 18.2 ×4 text
sites, fig 18.3 efficiency label); no geometry.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308): Chromium **and** WebKit at 1440 + 375 on part-5/index/glossary, dark +
light — 0 console errors, 0 external requests, 0 page h-scroll, nav 48 px,
fonts loaded, all internal anchors resolve. All 29 touched passages
screenshot-captured in both engines, dark + light; key figures and re-carries
visually reviewed (Quorum violet/teal intact, code chips and math render).
**Live after push** (commit `eb80d7a`): 13 corrected strings confirmed on
live part-5 ("processing rates is wasted", "Amazon Dynamo", "run Power Peg",
"isolated CMS sessions", "watch the API server", "quorum arithmetic",
"2 of 3", "attested artefacts", "Cork, Ireland", "Lambda (2014) · FaaS",
"rasterises", "a network and a kernel", "the property called"); origin
`glossary.json` serves count 520 with the refreshed definitions (the plain
URL briefly serves the documented 1-day `stale-while-revalidate` edge cache,
the pass-14 precedent). **The language pass is complete, Parts I–V.** Next:
Pass 19 — independent Fable verification of Parts IV–V plus the book-wide
closing sweep, then READY.

**For Pass 19:** the two declined geometry defects above (fig 16.8 curve
endpoints; fig 17.7/17.8 spatial encoding); re-verify the Pass-18 rewrites
against the pickle-coda bar (especially the three re-carries and the Knight
strip); the "a handful of its instructions" clause in `ch17-virt-p2` (the
precise count is 17, Robin–Irvine 2000 — deliberately left unnumbered);
cross-part: part-1's stray "recognized" and part-2's "recognizably" (outside
this pass's scope); the pre-existing `thompson` glossary quirk stands.

### Pass-18 verification (2026-08-09)

Full Fable audit of Pass 18, whose clearances had never had a second read
(brief: `docs/pass-18-verification-brief.md`), plus the two bridge-sanctioned
figure-geometry fixes. Method mirrored the 14/16/17 pattern: deep read of all
of Part V by the verifying model, then a 15-agent workflow — 3 independent
per-chapter fresh readers (pedagogy lens, web-enabled, blind to §4r), 5
primary-source verifiers over the load-bearing corrections (44 claims), and
an adversarial defense over every reader flag (23 raised) — every flag
adjudicated by the verifying model; all fixes gated through a fact/
consistency/voice confirmation agent over the diff, which caught 2 more
(the EC2 edit sharpening a pre-existing VM-boot tension; a broken
preposition pair in the NUMA caption). The auditor re-read SEC Release
34-70694 itself for the Knight strip.

**The §4r load-bearing corrections: all stand.** Reconfirmed against primary
sources: the Knight strip against the SEC order clause by clause (repurposed
flag ¶13, seven-of-eight ¶15, stale-server Power Peg path ¶16, real router
discontinued 2003 / counting moved 2005 and thereby "inadvertently disabled"
¶14, 4M executions · 154 stocks · ~45 min ¶17; rescue 6 Aug ~70% dilution;
Getco agreed 19 Dec 2012); CP/CMS-in-virtual-System/360; EC2 hourly→per-second
(Oct 2017); Amdahl and Brewer pull quotes word-for-word against the 1967
facsimile and IEEE Computer 2012; Herlihy wait-free-only scoping (TOPLAS
1991); Lamport and Dijkstra quotes verbatim; Paxos 1989 (SRC RR-49) /
submitted 1990 / printed 1998 / PMS 2001 all simultaneously right; FLP 1985;
CAP 2000/2002; Raft 2014; Gustafson's formula recomputed as algebraically
identical to CACM 1988; fig 18.2's "1 network · 1 kernel", Boole/Cork, and
all seven timeline years; Dynamo-vs-DynamoDB descendant framing; the CUDA
threads-within-a-block rescope against the programming guide; Docker/LXC/
libcontainer; Google 2B/week; Lambda/Firecracker microVM reuse (NSDI'20);
Spectre "mid-1990s" hedge; quantum-optimisation and neuromorphic 10–100×
hedges; "nearly every entry" reading-list hedge. **The three re-carries and
the rewritten Knight strip hold the bar** — blind readers, not knowing they
were re-carries, independently named all four among their chapters' best
passages (`ch16-lockfree-p3`, `ch17-consensus-p2`, `ch17-virt-p2`,
`ch17-microservices-p8`); kept verbatim. All three chapters judged gripping
and at bar by their blind readers.

**Sanctioned geometry fixes (per figure, pass-2 screenshot discipline):**
- **fig 16.8** — all four Amdahl curves redrawn as polylines through
  S(N)=1/((1−p)+p/N) computed at the figure's own tick mapping (x: log-scaled
  ticks N=1/8/32/128/512/∞; y: piecewise per the drawn 1/5/10/20/40/80×
  labels), each ending exactly on its asymptote at the ∞ tick. Before: p=0.95
  ended ~y164 (≈23× on a 20× ceiling), p=0.90 at y237 (>10×), p=0.50 at y280
  (the 5× tick, on a 2× ceiling), and p=0.99 flattened at ≈75× under a 100×
  label. The dashed 20× ceiling moved y184→180 (the true tick), its label
  clear of it; every point spot-recomputed to 0.1px by the confirmation gate.
- **fig 17.7** — pair-labels now sit on their own edges: CP block along the
  C–P edge (diagonal stack tracking the edge slope), AP block centred inside
  the A–P bottom edge (equidistant from A and P, far from C), and "CA
  (impossible on real networks)" moved from the P-adjacent interior to
  *outside* the C–A edge it names — the impossible pair literally outside the
  feasible region. All positions computed against the edge equations; no text
  crosses the triangle boundary.
- **fig 17.8** — the AP dot-cluster translated from the C–A side to the
  lower-right interior along the A–P edge (same scatter shape, SMIL opacity
  animations untouched), "AP corner" label moved with it; the "CA edge:
  unreachable" note moved from the centroid to outside the C–A edge midpoint,
  indent echoing the edge slope. CP cluster already correct — untouched.

**Wrongly cleared, found & fixed (20 surgical edits + 2 gate catches).**
Fact-class: the **Part V opener's "sixty-four cores in your laptop"**
contradicted Ch16's own (correct) "eight to sixteen" → the scale-step now
runs 16 laptop / 64 cloud server / 10,000 machines a region (matches both
heroes); `ch16-numa-p2` "runtimes (Java, Go, .NET) have NUMA-aware
schedulers" — Go's runtime is affirmatively NUMA-oblivious (the 2014 Vyukov
design was never implemented) and Java/.NET awareness lives in the GC, not a
scheduler → "Java and .NET push the same awareness into their garbage
collectors"; `ch16-lockfree-p2` called `ldxr/stxr` "a single atomic
instruction" — it is an exclusive pair → "a single `cmpxchg` instruction on
x86; the `ldxr/stxr` exclusive pair on ARM"; `ch17-microservices-p3` routed
Linkerd through Envoy/xDS — Linkerd's own literature rejects both
(linkerd2-proxy, Destination API) → caption decoupled ("Istio and Consul
Connect drive Envoy through xDS… Linkerd runs its own lean Rust proxy
instead") and the fig 17.10 label de-xDS'd ("all pushed live to every
sidecar"); `ch17-virt-p3` **Dropbox** never scaled serverless-of-servers
(own metadata servers in colo from early on) → Instagram (entirely on AWS
until the Facebook era); Knight's "**lost $440 million**" was the superseded
initial company estimate — the controlling SEC order says "over $460
million" (Knight's own later filings ~$458M) → "over $460 million";
`ch16-races-p6` Therac "the targeting magnet" — no such component; the
mispositioned element was the turntable (Leveson–Turner) → "the turntable
that shapes the beam"; `ch17-microservices-p7` "Eighteen thousand customers…
installed" → "Nearly eighteen thousand" (the 8-K says "fewer than 18,000");
`ch18-civilization-p1` the web "to organise lab notes" — the 1989 proposal
is about CERN-wide information loss → "the lab's tangle of people, projects,
and documents". Precision/dating: EC2 "fresh VM in 60 seconds" → "in
minutes — today, in under one" (Amazon's own 2006 copy says minutes; the
gate then aligned `ch17-containers-p1` to "a minute or more"); Firecracker
"boot in 100 ms" → "about a tenth of a second" (the paper's figure is
<125 ms); Borg "since 2003" → "had by then been running internally for over
a decade" (no primary source attests 2003; EuroSys 2015 says only "more than
a decade"); "Netflix, Amazon, and Spotify all famously decomposed" → "had
all famously decomposed" (Amazon's decomposition predates 2014 by a decade);
"a typical CI/CD pipeline pushes only kilobytes" → "a well-layered… can push
just kilobytes" (best case, not typical); `ch18-future-p1` "problems
classical computers fundamentally can't" → "problems no classical computer
can attack efficiently" (hardness is unproven; the hedged structure kept);
`ch16-numa-p4` "permanent" → "lasting" (post-2018 silicon fixed Meltdown in
hardware; affected machines paid for life); `ch16-numa-p2` "inside
high-performance GPUs" → "of GPU servers… and of multi-GPU setups" (system
topology, not intra-GPU; prepositions parallel per the gate). Consistency/
voice: `ch17-k8s-p2` announced five components then enumerated seven → the
figure draws exactly five (API server, etcd, scheduler, controller manager,
kubelet); kube-proxy and the runtime subordinated ("supported by…"), the
count now honest; "traveling" → "travelling" (`ch18-trace-p5`), "modeled" →
"modelled" (`ch18-intersect-p2`).

**Considered and declined** (do not "fix" blindly): "3 nm" — re-flagged
high by a third consecutive blind reader; owner-ruled, upheld again.
`ch16-numa-p1` MESI body prose (the chapter's uniform body-introduces/
caption-runs architecture; fig 16.11's caption carries ping-pong and false
sharing). The Therac "first…fatalities were race conditions" plural — the
*first* deaths (Tyler, 1986) were the Datent race; the Yakima overflow death
came in 1987, so the sentence is strictly right. "$7 billion in positions"
(WSJ-reported intraday peak; the SEC's end-state gross is $6.65B — noted,
kept as the published peak figure). "Procurement" register in `ch17-cap-p4`
(the caption's second decision is precisely procurement; the figure's own
box says so). The "-ization" technical-name convention (virtualization,
Wait-Free Synchronization, datacenter — uniform across Part V, matching
vendor/paper names; part-3 precedent). The trace's Python station (Chapter
7's waypoint in an explicitly chapter-tour figure). "The kernel that runs
every cloud" (legacy-attribution sweep; Linux hosts on AWS/GCP, >60% of
Azure VM cores). The Amdahl pull quote is the verbatim *tail* of a longer
sentence, silently capitalised — standard quoting practice, noted for the
record. Kata Containers "2018" (1.0 date; announced Dec 2017). Six
pre-existing 1–11px text-vs-rect marginals in untouched figures (16.1,
16.5, 16.7, 16.11, 17.2 — invisible at render, logged only).

**Invariants.** Anchor-id set **byte-identical (189)** — verified against
HEAD after both the geometry and text edits. Glossary regenerated: **count
520, no entry added or removed** — the mesh-caption restructure initially
dropped the `control plane` entry (its parenthetical was the extractor's
definitional cue) and an appositive re-cue garbled the comma; final phrasing
keeps the parenthetical cue, and the entry's definition now carries the
corrected xDS scoping instead of the old falsehood. Six definitions
refreshed, all improved (`control plane`, `kubernetes` Borg dating,
`container`, `container runtime`, `docker`, `governance` "modelled"). §4g
and every §4r correction survive in substance. Quorum identity, heroes,
`.qm-quorum` closer, `#bca8ff` strip accent, `ch17-microservices-p6` stamp,
thesis set and authorship line untouched.

**Verification.** Local (CF-mimicking server: extensionless 200, `.html`
308): Chromium **and** WebKit at 1440 + 375, dark + light, on
part-5/index/glossary — 24 page-checks: **0 console errors, 0 external
requests, 0 page h-scroll, nav 48 px** (the glossary page's own header is
its own pass-2 design, no `.book-nav` — not a regression), fonts loaded,
all internal #anchors resolve (30/30). bbox-vs-viewBox sweep: **0 overflows
book-wide**. 96 screenshots: all 19 touched passages and all 4 touched
figures in both engines, dark + light, fig 17.8's SMIL timeline sampled
mid-cycle — the Amdahl curves approach their ceilings from below in both
engines, the CAP encodings read correctly, no label collisions. **Live
after push** (commit `42fe9d8`): all 22 corrected strings ("lost over $460
million", "Linkerd runs its own lean Rust proxy", "sixteen cores in your
laptop", "the turntable that shapes the beam", "Nearly eighteen thousand"
among them), all four curve endpoints and both CAP label positions, and
origin `glossary.json` count 520 with the corrected `control plane`
definition confirmed on the live page.

**For Pass 19 (additions to §4r's list):** the SVG source *comments* carry
American spellings ("traveling packet" ×3 — invisible to readers; normalise
or ignore); ratify the "-ization technical-name" convention book-wide while
running the "recognized"/"recognizably" strays; the six pre-existing
text-vs-rect marginals above are logged as non-defects unless the sweep
disagrees; the Amdahl-quote clipping note stands for the owner read.

## 4s. Pass 19 (2026-08-09): the book-wide closing sweep → READY

The last pass before READY, run under the amended gate rhythm (`BRIDGE.md` §1)
against the bridge-authored brief (`docs/pass-19-brief.md` — all five worklist
items pre-ruled). Model: Fable throughout. The prose was closed: register-class
findings are flagged below, not rewritten; fact-class errors were fixed under
verify-before-fix.

### The worklist

**1 · fig 15.2 geometry (sanctioned).** Took the "move the pair left of
Spectre" option: the PAC · CET group (green) and Spectre (red) swapped
positions — PAC · CET now at x=500 on the high label tier (stem 200→160,
labels y=150/138, the band free right of ROP), Spectre at x=560 on the below
tier (labels y=252/264/276, sublabel split "2018 · speculative" / "side
channel" to clear CFI's). The timeline now reads CFI 2015 → PAC·CET 2017+ →
Spectre 2018 → MTE 2023, and PAC · CET sits directly after the ROP/JOP attacks
it actually answers. HEAD-vs-working screenshots showed the old layout also
carried two same-row text collisions (Spectre-sub × MTE-sub at y=148; CFI-sub
× PAC-sub at y=264) — the swap removes both. A third, pre-existing overprint
the screenshots surfaced (ROP main label × JOP sublabel, x=332–351, baselines
2 px apart) was fixed in the same licence class by lifting ROP's label pair
one row (stem 200→148, labels y=138/126); every row was recomputed clear.
Its ASLR sublabel also took the item-4 spelling ("2003+ · randomisation").
The figure is static (no SMIL); shot in Chromium + WebKit, dark + light,
before and after; both sweeps clean; a11y title unchanged.

**2 · Ch15 title → "Attack and Defence".** Every occurrence: the h1
(`Attack and<br>Defence<br>`), the hero's a11y `<title>`, part-4's TOC card
title and its "Defence in depth." card text, the three meta descriptions
("attack and defence"), the chapter-nav item and section-number ("05 —
Defence systems"), the index chapter card, `docs/plan.txt`, and
`docs/figures.txt`. `book.js` derives nav readouts and stored-position labels
from the h1 at runtime, so no code changed; previously stored position labels
are user data and will show the old string until the next save (benign).
Contrary to the brief's premise, eight anchor ids *do* contain the word
(`ch15-defense`, `ch15-defense-p1…p6`, plus the `#ch15-defense` href) — all
held byte-identical, verified. **Scope extension under the ruling's own
"uniformly British house spelling" basis:** the audit found the claimed
uniformity false outside Ch15 — part-1's Chapter 3 was uniformly American
(nav item + section-number "06 — Defenses", four h3s "Defense one…four",
eleven prose defense/defences, fig 3.11's DEFENSE ×4 labels and its caption's
"broke the previous defense" — the very sentence fig 15.2's caption spells
"defence"), and part-3 carried four American figure labels (fig 11.7
"DEFENSE — randomise…", fig 12.9 "defense:" ×3). All fixed to British;
`ch3-defenses*` ids untouched; figs 3.11/11.7/12.9 screenshot-reviewed in
both engines. Owner may veto the title at the read — it is a per-site string
change to revert.

**3 · Diffie–Hellman en dash, book-wide.** Part-3's five hyphenated instances
(two prose, the fig 11.11 caption + its SVG line "Here is half of a
Diffie–Hellman…", the ephemeral-DH prose) and part-4's key-term span → en
dash, matching the book's Jacobson–Karels/Leveson–Turner convention. The two
SVG source comments (part-4, part-5) left per the item-5 class. **Glossary
key migration — what was actually found:** the shipped 520 contained a
shadowed *duplicate pair* — `diffie-hellman` (hyphen, minted by the key-term
span, home ch14-publickey, a weaker definition, serving **zero** tooltips
because its only wrapped occurrence was inside its own first-use section)
alongside `diffie hellman` (term "Diffie–Hellman", curated, home
ch14-primer, the good discrete-log definition, already serving the 17
en-dash occurrences). The glossary index page showed both rows side by side.
The migration merges them: **count 520 → 519, removed key `diffie-hellman`
only, nothing added, no junk**, the surviving definition byte-stable, and
one `cipher suite` definition picks up the en dash. The stop-if-broken guard
did **not** trigger — the extractor already mints the en-dash key cleanly
(the curated list carries 'Diffie–Hellman'; `book.js` normalises en dash
identically, proven by the pre-existing en-dash tooltips). Verified locally:
the migrated ch14-publickey span now carries a live tooltip (it previously
served nothing); the ch14-primer `<strong>` is the first-use anchor. The
brief's "count 520 ±0" rested on a single-entry premise; the −1 is the
duplicate healing, an improvement, and STATE/README now say 519. Noted, not
chased: `parameterized query` still sits in `curated_missing` (the book's
British `parameterised queries` entry exists; the American curated spelling
is a no-op line in the regen output).

**4 · Spelling convention, ratified and recorded (§5).** Enumerated every
-iz-/-yz-/-ll-/-og- variant book-wide (plus artefact and the defence
cluster), classified each against the rule, fixed the strays: **part-1** ×9
(mechanised, miniaturisation, optimisation, optimising, realisation, the
known "recognised", specialised ×2, popularised) plus the item-2 defence
cluster; **part-2** ×38 (initialises/initialisation/initialising, criticised,
optimise ×3 + the optimiser/optimisers/optimisations/optimising cluster ×10
incl. two headings, utilisation ×8 incl. the fig 4.6 label/caption/axis,
specialised, analysed, analyser, organised ×2, Synchronising, generalisation,
containerised, the known "unrecognisably", standardisation, realisation,
deserialise, tokeniser); **part-3** ×3 (utilisation ×2, utilise); **part-4**
×10 (Deserialisation h3, deserialisation ×4 prose + 2 figure labels,
authorisation figure label, parameterised TOC card, randomisation fig-15.2
label). The -ll- and -og-(catalog/dialog) families were already clean;
artefact uniform. **Retained** (recorded in §5): proper names and quoted
titles (ISO's full name, *Wait-Free Synchronization*, *Structured Computer
Organization*, *Computer Organization and Design*, UndefinedBehaviorSanitizer,
Baran's CENTRALIZED/DECENTRALIZED taxonomy labels, the Codd pull-quote's
"organized" ×2 — quotations are never respelled); standard keywords and
theory terms (SQL SERIALIZABLE/Serializable/serializable ×7); technology
names (virtualization/paravirtualization ×11, datacenter ×3, analog ×4, the
ASLR expansions ×2); code registers (CPython stage labels tokenize/optimize,
`deserialize()`); and **civilization/civilizational** (~30 sites — uniform,
owner-thesis vocabulary, deliberately left; owner call at the read). The
-or/-our family (behavior ×9, color, favor) is **outside** the ratified
scope and untouched.

**5 · Ruled non-actions, declined as ruled.** SVG source comments with
American spellings, enumerated for the record and left: "traveling" ×5
(part-3 ×1, part-4 ×1, part-5 ×3 — the ruling's "×3" was Part V's own
count), "Stylized" ×2, "Tokenizer" ×1, "utilization" ×1,
"Centralized/Decentralized" ×2, "SERIALIZABLE" ×1, "Defense" ×1, hyphenated
"Diffie-Hellman" ×2 — all invisible to readers. The six logged text-vs-rect
marginals: confirmed non-defects (see the sweep below — nothing
reader-visible). The Amdahl-quote clipping note stands for the owner read.
Owner rulings verified untouched: "3 nm" ×4, Sony PSN, Morris 23 ×3, the
Enigma six-year count.

### The book-wide closing audits

- **Cross-part consistency read** (4-agent Fable workflow: repeated claims /
  seams / Chapter-N cross-references ×2; ~140 cross-references and every
  repeated claim checked, all listed with verdicts). The core set is clean:
  Morris 23 (part-1 + part-3 agree), Enigma six-years only in part-4 with
  the Rejewski credit and part-1 verified silent, RAM 60 ns everywhere with
  the T_avg arithmetic recomputed, figure counts 242/235/222 all consistent,
  "A unified theory" masthead ×5 + index title ("A visual theory" appears
  nowhere), all five closer stamps present exactly once with zero "The
  recurring pattern." residue, all five closer→opener seams verified with
  their promised names present. **Four fact-class breaks found and fixed**
  (each verified at source before the fix): `ch5-malloc-p2` "Recall from
  Chapter 4" for the stack/heap split — Chapter 4 never mentions the heap;
  re-aimed at Chapter 3, whose fig 3.5 draws it (the `heap` glossary
  definition follows); `ch5-pointers-p2` "Recall from Chapter 1 that memory
  is a giant array of bytes" — Chapter 1 never states that model; now "To a
  C program, memory is…" (no false recall, fits the pointers context);
  `ch15-web-p2`'s "confused deputies (Chapter 11 §06 introduced the term
  obliquely)" — the term appears nowhere in part-3 and ch11 §06 is HTTP/2–3;
  the false parenthetical cut and the definition made a sentence ("A
  confused deputy is code that has authority…"), phrased to mint no glossary
  entry; `ch18-final-p6` "The book's first diagram showed a single
  transistor" — Fig 1.1 is the Turing machine; now "Chapter 1 drew a single
  transistor." And one fact-class hedge: the fig 1.2 caption's "It was the
  first time a machine was built specifically to think through a problem
  human minds could not" → "among the first machines" — Rejewski's bomba
  (1938) precedes the Bombe, the same Polish lineage part-4 now credits.
  **Flagged, not fixed (register-class, for the owner read):** part-2's
  closer label "End of Part Two" (all others use Roman numerals) and its
  headline "The kernel *and the languages*." breaking the "…is built."
  pattern of the other four closers — possibly Greenbar-deliberate, never
  ratified; the ASLR era labels 2001+ (fig 3.11) vs 2003+ (fig 15.2), both
  era hedges in context; Ch2's promise that Boolean algebra returns as
  "access control in security (Chapter 15)" lands only on least-privilege
  material with no Boolean framing; Ch1's Spectre "we will return to this in
  Chapter 15" is honoured at recap/caption level only; the index cover
  eyebrow "A Visual Computer Science Book" (a distinct design element, not
  the banned masthead string).
- **Link and anchor audit:** 462 internal hrefs + 519 glossary
  part/section references, all resolve; 0 broken. (Remaining flags are by
  design: data-URI favicons, canonical/og self-URLs, the `href="/"` home
  link, part-5's colophon externals, two JS template strings in
  account.html.)
- **Figure sweeps, book-wide** (both detectors first validated against a
  deliberately failing baseline): bbox-vs-viewBox with the SMIL timeline
  sampled 0–12 s — one pre-existing 3.2 px marginal (fig 1.4, present at
  HEAD), 0 new; text-vs-containing-rect under a stricter belonging
  heuristic than prior passes — 43 findings, **the finding set byte-identical
  to a HEAD-checkout sweep run under identical conditions** (fonts loaded,
  sequential), i.e. this pass introduced zero; the set contains the known
  six-marginal class, and the largest escapes were screenshot-adjudicated
  benign (annotation labels deliberately extending past background rects —
  fig 11.14's bar label, fig 9.6's AS-path list, fig 11.6/11.7 speech
  labels, fig 7.2/7.6/13.4 code-register lines). Decorative part-opener/hero
  SVGs are excluded by scope (deliberate bleed, not registry figures).
- **Glossary:** regenerated twice (after the worklist edits, after the
  consistency fixes) — **519**, the DH merge the only key change; 10
  definitions updated, every one a shadow of this pass's own edits
  (spelling ×8, DH dash, the corrected Chapter-3 recall in `heap`); no junk,
  no em-dash clipping.
- **`docs/figures.txt` / `docs/plan.txt`:** registry re-checked against the
  HTML — 19 heroes + 221 numbered cards + the trace = 241 in-book SVGs
  (+ cover = 242) reconcile exactly after fixing a real registry defect:
  the Ch 14 block still used the audit-era "14.0 math primer" numbering,
  leaving titles 14.2–14.12 systematically one behind the HTML ids; block
  realigned to 14.1–14.13. "Last verified" refreshed to 2026-08-09;
  plan.txt's 18 chapter titles verified against the HTML TOCs (18/18,
  including the new Ch15 title).
- **Full §7 harness:** 100 checks — 8 pages × Chromium + WebKit ×
  1440/375/320 × dark + light (96 page-checks) plus 404 spot-checks, all
  pass: **0 console errors, 0 external requests, 0 page h-scroll, nav
  48 px, fonts loaded**. Reduced-motion spot-check (part-4): SMIL paused on
  all sampled figures, console clean. Print spot-check (part-4): renders,
  console clean. After the consistency fixes, the four edited pages were
  re-checked in both engines (console, h-scroll, marker strings) — clean.
- **Live parity after push** (commit `1320be7`, deploy verified in single
  page snapshots after a brief propagation window): all 15 marker strings
  confirmed on the live pages ("05 — Defence systems", "Attack
  and<br>Defence", the hero a11y title, "A confused deputy is code…",
  "among the first machines", "06 — Defences", "2001+/2003+ ·
  randomisation", "To a C program, memory", "The optimiser", "full
  utilisation", "DEFENCE — randomise", part-3 "Diffie–Hellman", "Chapter 1
  drew a single transistor", the index card title); fig 15.2's swapped dot
  geometry and lifted ROP labels present in the live SVG; origin
  `glossary.json` serves **count 519** with keys
  `diffie`/`diffie hellman`/`hellman` and term "Diffie–Hellman" (the plain
  URL keeps its documented 1-day `stale-while-revalidate` edge window);
  live DH tooltip verified in **Chromium and WebKit** — the migrated
  ch14-publickey span attaches (`glossary-ref`) and shows the definition on
  hover, the ch14-primer first-use anchor set, 0 console errors on the live
  page in both engines.

### Invariants

Anchor-id sets **byte-identical to HEAD in all five parts
(354/346/380/228/189)** — verified after the worklist edits and again after
the consistency fixes; the Ch15 title change moved no id. §4g and every
later correction survive in substance (Morris, Enigma, RAM 60 ns, ZAB,
Paxos-lore, "172 years", figure-count prose re-verified by the audit; "3 nm"
and Sony PSN untouched). Glossary 519 as documented. Thesis set, authorship
line, the five identities, heroes, closer stamps, reduced-motion/print
grammar, zero-third-party: untouched and re-verified.

### READY — the declaration

**The book is prose-ready.** The language pass is complete and independently
verified across all five parts; the closing sweep's worklist is executed,
the book-wide audits are clean, and every invariant holds. *Under the Code*
is declared **READY for the owner's complete read.**

**Read-along notes for Tiger:**
1. **Sony PSN 2011 = SQLi** stays as ruled — known-unconfirmed lore; the
   blind-reader evidence is recorded in §4q's verification entry.
2. **The Amdahl pull quote** is the verbatim tail of a longer sentence,
   silently capitalised — standard quoting practice (§4r note).
3. **Ch15 is now "Attack and Defence"** (with part-1 Ch3 and two part-3
   figures brought to the same British spelling). Veto reverts a per-site
   string list, no ids.
4. **The glossary is 519**, not 520 — the Diffie–Hellman duplicate row
   merged (this entry, item 3). STATE and README now say 519.
5. **Spelling:** the ratified rule is recorded in §5. "Civilization/
   civilizational" was classified as your thesis vocabulary and left
   American throughout — flip it at the punch-list if you want
   "civilisation". The -or/-our family (behavior, color) was outside the
   ruling and untouched.
6. **Register flags from the consistency read** (yours to keep or change):
   part-2's closer label "End of Part Two" and its headline that breaks the
   "…is built." pattern; ASLR "2001+" vs "2003+" between the paired
   arms-race figures; Ch2's "access control (Chapter 15)" promise lands
   thinly; Ch1's Spectre promise returns at recap level.
7. **Five passages changed under fact rules this pass** — worth reading in
   place: `ch5-pointers-p2`, `ch5-malloc-p2` (both false "Recall from"
   references), `ch15-web-p2` (confused-deputy attribution),
   `ch18-final-p6` (first-diagram claim), fig 1.2's caption (Bombe
   priority hedged for Rejewski's bomba).
8. **fig 15.2** was re-laid per the sanction — worth a look at render.

## 5. Known non-defects / deliberate choices (do not "fix" blindly)

- `404.html` is intentionally self-contained (own CSS, reduced font set).
- The h2 "glass reveal" leaves a faint chromatic text-shadow at rest — intentional.
- `glossary.json` (248 KB) is fetched on every page; the localStorage cache only
  short-circuits parsing, not the network (the fetch itself learns the version).
  HTTP caching mitigates. Candidate for a version-stamped URL later, not breakage.
- The cover figure count (242) includes the cover art itself; `docs/figures.txt`
  tracks the 241 in-book SVGs.
- **Part IV reads in a serif body on cream ledger stock** (Fraunces/Spectral).
  This is deliberate Strongroom identity, ratified pass 5 — reading typography is
  per-volume (see §4d "What invariant means"). Not a regression to the sans
  reading default; do not "restore" it.
- **House spelling — ratified Pass 19 (2026-08-09), do not relitigate.**
  British **-ise/-yse/-ll-/-ogue** in ordinary prose (recognise, organised,
  modelled, travelling, artefact, defence, optimiser, utilisation,
  deserialisation). Canonical **-iz-/-og-** forms are RETAINED where the
  string is:
  (a) a **proper name or quoted title** — International Organization for
  Standardization, *Wait-Free Synchronization*, *Structured Computer
  Organization*, *Computer Organization and Design*,
  UndefinedBehaviorSanitizer, Baran's CENTRALIZED/DECENTRALIZED figure
  taxonomy, and any direct quotation (the Codd pull-quote's "organized" —
  quotations are never respelled);
  (b) a **standard's keyword or theory term** — SQL
  SERIALIZABLE/Serializable, serializable isolation/schedules;
  (c) an **industry term-of-art naming a technology** — virtualization,
  paravirtualization, datacenter, analog (signal domain / analog computing),
  the proper expansion "Address Space Layout Randomization";
  (d) **code, identifiers, and code-register figure labels** — always
  (`deserialize()`, the CPython stage labels tokenize/optimize);
  (e) **civilization / civilizational** — owner-thesis vocabulary, uniform
  book-wide, deliberately American; only the owner flips it.
  The **-or/-our family** (behavior, color, favor) is OUTSIDE this ruling's
  scope and follows the technical literature as-is. SVG/HTML **source
  comments are exempt** (invisible to readers; never churn them).
- **Diffie–Hellman takes an en dash** (the name-pair convention:
  Jacobson–Karels, Leveson–Turner). The glossary key is `diffie hellman`
  (en dash normalises to a space in both the extractor and book.js — they
  must stay in lockstep). Since Pass 19 the glossary counts **519** terms:
  the old hyphen key `diffie-hellman` was a shadowed duplicate row and was
  merged away, not lost.

## 6. Prioritized improvement backlog (later passes — needs owner sign-off)

**P0 — owner action (pass 3 leftover)**
0. ~~**Enable Cloudflare Email Sending for atheric.eu**~~ — **DONE**
   (owner-confirmed 2026-08-01): Email Sending enabled, `EMAIL_API_TOKEN`
   set, and a live magic-link email round-trip verified in production.
   No P0 items remain.

**P1 — reader-facing polish**
1. ~~**Figure a11y**~~ — DONE in pass 2. All 241 figure SVGs + the cover carry
   `role="img"` + `aria-labelledby` → their descriptive `<title>`.
2. **Emoji as icons** in `.insight-icon`/`.concept-icon` (⚡ etc.) — inconsistent
   cross-platform rendering; the book otherwise draws everything as SVG.
3. **Chapter-nav active state**: `.nav-item.active` styling exists but no scroll
   spy sets it on the horizontal chapter nav (the left rail has one); minor JS.
4. **Glossary tooltips on touch**: hover/focus only; tap works via `tabindex` but
   dismissal is awkward. Consider tap-toggle semantics.

**P2 — performance**
5. ~~Version-stamp `glossary.json` + long-cache headers~~ — DONE in pass 2 via the
   load-once route: `public/_headers` caches `glossary.json` for a day with
   `stale-while-revalidate`, so navigations within the window skip the network
   entirely; localStorage still short-circuits parsing. (A URL version stamp was not
   added — book.js is static and cannot know it without a build step; the header
   policy plus the `generated`-keyed localStorage cache achieve the same effect.)
6. Part pages are 313–473 KB HTML (largely SVG). Fine gzipped (~60–90 KB), but a
   figure-lazy-mount pass (template + IntersectionObserver) would cut initial DOM
   size (~5,000–6,000 nodes/page) if mobile INP ever becomes a concern.
7. Consider subsetting the self-hosted latin fonts to the book's glyph set (the
   main site did this; saves ~40%). Deliberately not done in pass 1 — unsubset
   files are byte-served exactly as Google's, so rendering risk is zero.

**P3 — structural nice-to-haves**
8. Dead CSS: `.bit-row`, `.process-flow`, `.concept-grid`, `.scale-shock`,
   `.chapter-end`, `.diagram-grid-2`, `.tall` are defined but unused (legacy of
   earlier drafts). Harmless; strip in a cleanup commit.
9. `glossary.html` lacks canonical/OG meta (all other pages have full sets).
10. A "part N of V" progress indicator exists in the header but there is no
    per-chapter progress bar; the rail covers desktop only.
11. `docs/plan.txt` / `docs/figures.txt` "last verified" dates are stale
    (2026-05-01); re-verify after content edits. (`glossary.json` itself was
    regenerated in pass 2 and is now current.)
12. ~~**Cloudflare Pages pretty-URLs**~~ — DONE in pass 2. Internal hrefs,
    canonicals, `og:url`, and sitemap are all extensionless; `book.js` normalises
    `.html` so both forms still work for returning visitors' stored progress.

## 7. Verification protocol used (repeat after any pass)

```bash
npm run serve                      # localhost:8000
# headless: console errors, page-level h-scroll, nav height, font status,
# external-request detector at 1440/375/320 on all 8 pages
# link audit: every href/#anchor across all pages resolves
```

Pass 1 exit state: 0 console errors, 0 external requests, 0 broken anchors,
0 pages with horizontal scroll at 320px+, header 48px at all widths, fonts
self-hosted and loading (`document.fonts` confirms Playfair 400/500/i400, DM Sans
300/400/500, DM Mono 300/400/500), live-site parity confirmed after deploy.

Pass 2 exit state (2026-07-06, verified locally at 1440 + 375 on all 8 pages):
0 console errors (favicon 404 closed), 0 external requests, 0 horizontal scroll;
418 internal links + anchors resolve; reduced-motion still honored; figure sweep
reports 0 of 242 SVGs overflowing; all 241 figures + cover carry `role="img"` +
`aria-labelledby`; glossary tooltips, glossary index (516 terms), and the resume
card all function with extensionless hrefs. Not yet redeployed — verify live-site
parity after push, and confirm the `_headers` `Cache-Control` is served by
Cloudflare (curl the response headers on `glossary.json`).

Pass-2 verification exit state (2026-07-06, after commit `def7bc0`): all of the
above re-verified locally against a server that mimics Cloudflare's extensionless
routing (200 on `/part-N`, 308 on `.html`), plus: text-vs-rect scan clean,
corrected a11y scan 0 findings, all 45 pass-2-touched figures screenshot-reviewed.
~~Still not deployed~~ — **deployed in pass 3** (pushed with the accounts work;
push permission was available this time). Live post-deploy checks all pass:
canonical is extensionless (`https://under.atheric.eu/part-2`), `.html` 308s to
extensionless, `glossary.json` serves `Cache-Control: public, max-age=86400,
stale-while-revalidate=604800`, and figs 13.5 / br-3 / 15.7 were
screenshot-checked live at 1440 and 375 (13.5's ACID table sits below the
scenario panels; no frame overflows).

### Pass-3 exit state (2026-07-06, live at under.atheric.eu)

Deployed as commits `3835e74` + `165795d` (first deploy failed on a
Pages-unsupported `send_email` binding; switched to the Email Sending REST
API). Production D1 `under-book` (EEUR) carries the schema; test rows removed
after verification (0 users at exit).

Live verification, two isolated browsers (Playwright contexts), both signed in
to the same account via minted magic links (email delivery awaits the P0 owner
step), at 1440×900 **and** 375×812 — all 21 checks pass, **0 console errors**:

- A reads to a mid-chapter paragraph (`ch5-bell-labs-p4` in part-2 at 1440;
  `ch11-http-p3` in part-3 at 375); the debounced save lands on the server
  with the anchor + fraction.
- B opens the same part → quiet "On your other device — Chapter N · §NN" chip;
  clicking it restores to the **exact stored fraction** (0.514→0.514,
  0.852→0.852 — well within one paragraph; the settle correction snaps out
  late font reflow).
- B's index resume card targets `part#anchor` and the exact offset survives
  the navigation (sessionStorage handoff).
- Signed-out regression: a fresh browser on a part page makes **zero `/api`
  requests**, saves anchored progress to localStorage as before, no layout or
  console changes; no horizontal scroll at 375 with the chip up.
- API sanity live: `/api/auth/me` 401 signed out; `/api/auth/request` 503
  `delivery_unavailable` (secret not yet set); GET verify page does not
  consume tokens; token reuse rejected; `/api/auth/delete` erases everything
  (curl-verified locally against the same code).
