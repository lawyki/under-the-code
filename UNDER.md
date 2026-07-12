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
  is fully testable without mail.
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

## 6. Prioritized improvement backlog (later passes — needs owner sign-off)

**P0 — owner action (pass 3 leftover)**
0. **Enable Cloudflare Email Sending for atheric.eu** so magic-link mail
   actually delivers: Workers Paid plan → dashboard Email → Email Sending →
   enable for the zone + add its DNS records (or `npx wrangler email sending
   enable atheric.eu` once the account has access — the API currently returns
   Unauthorized 2036, i.e. plan/beta gating). Then create an API token with
   Email Sending permission and store it:
   `npx wrangler pages secret put EMAIL_API_TOKEN --project-name under-the-code`.
   Everything else (code, D1, CF_ACCOUNT_ID var) is already deployed;
   `/api/auth/request` returns 503 `delivery_unavailable` until this is done.
   Then: request a link on `/account` with a real address and complete one
   live email round-trip.

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
