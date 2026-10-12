# Under the Code

A unified theory of how computers actually work — five parts, eighteen chapters, ~93,000 words, 242 inline-SVG figures (222 diagram cards + 19 chapter heroes + the cover).

Published at **[under.atheric.eu](https://under.atheric.eu)**.

By [Yki Lähteenmäki](https://github.com/lawyki). Published by [Atheric](https://atheric.eu) (YDT Holdings Oy, operating from Helsinki).

## Repo layout

```
public/          ← the static site · what the domain serves
  index.html
  part-1.html ... part-5.html
  book.css, book.js
  part-2.css ... part-5.css ← per-volume identity layers
  fonts.css, fonts-part2..5.css, fonts/ ← self-hosted webfonts (no third-party requests)
  glossary.html, glossary.json
  sections.json  ← section labels for the account page's "Your marks" (npm run build:sections)
  account.html   ← sign-in + privacy notice (/account)
  og-image.svg, og-image.png
  robots.txt, sitemap.xml, 404.html, _headers
functions/       ← Cloudflare Pages Functions · the account/position API (/api/*)
schema.sql       ← D1 schema: users, sessions, login tokens, reading positions (+ migrations/: accounts v2, section marks)
wrangler.toml    ← Pages + D1 bindings
scripts/         ← build tooling (not served)
  build-glossary.js
docs/            ← internal design docs (not served)
  plan.txt
  figures.txt
legacy/          ← prior drafts, kept for reference
```

## Develop

```bash
# Serve public/ on http://localhost:8000 for local preview
npm run serve

# Re-extract the auto-glossary from the part-N.html files
npm run build:glossary

# Rebuild the section-label map after any heading edit
npm run build:sections
```

The book itself is a static site — no framework, no bundler. Everything in `public/` is plain HTML + CSS + JS that a browser parses directly. Alongside it runs one small optional service: the account/position API in `functions/`, deployed as Cloudflare Pages Functions against a D1 database.

## Reading positions & accounts

Signed out, your reading position — and any sections you mark — is kept in the browser's `localStorage` only — it never leaves the device. The place is the paragraph you were *reading*: skims, look-ups and detours don't move it, and you can set it by hand from the place button on the bar (Pass 25, `UNDER.md` §4y; `?utc-debug` on a part page shows the tracker). Signing in (a password; the email is used only to confirm the account and to recover it — passkeys follow at the domain move) stores that same single position server-side in D1 so it can follow you between devices. What is stored, why, and for how long is disclosed in the privacy notice at [/account#privacy](https://under.atheric.eu/account#privacy).

## Go deeper videos

Optional outside videos sit beside the text, never in it: the book must teach on its own. Each is an `<aside class="deeper">` placed just before the paragraph it belongs to, on a page that loads `deeper.js` after `book.js`. On wide screens it is a note in the right margin beside that paragraph; narrower, a small pill at the bottom right while the paragraph is on screen. Either opens a viewer with the play button. Without script it is one quiet line. `data-art` picks a small drawing for the picture (`enigma`; none gives a plain dark card). Copy the Enigma aside in `part-1.html` (ch1-context) and change the data:

- `data-yt`: the 11-character video id, no start time. `data-length`: the length, e.g. `47:41`.
- `.deeper-about` says in one line what it shows, using only what the video itself states; `.deeper-title` links the watch URL, `.deeper-channel` the creator's channel.
- Use no `<p>` or `<li>` inside the aside (they would count as section prose) and no `ch…`/`fig-…` ids (anchor law).

Rules (EU copyright and privacy):

- Only the creator's own upload on their official channel; never a re-upload or mirror. Check the channel and that embedding is allowed (the oEmbed endpoint answers 401 when it is not; then set `data-embed="off"` and only the plain link shows).
- Never download, re-host, crop or edit a video, its thumbnail or its audio.
- Nothing loads from Google before the click: the placeholder is drawn locally (no `i.ytimg.com` thumbnail); play inserts the player from `www.youtube-nocookie.com/embed/<id>`. The credit (*"Title" by Creator*, channel linked), the cookie note and the "Watch on YouTube" link always show. If a Content-Security-Policy is ever added to the pages, include `frame-src https://www.youtube-nocookie.com`.
- Never imply the creator endorses or works with the book. The videos are outside the book's licence (below); the privacy notice at `/account#privacy` covers the embeds.

## Deploy

Production is **Cloudflare Pages**: pushes to `main` deploy `public/` as the site and `functions/` as the `/api/*` account service (bindings in `wrangler.toml`; apply `schema.sql` to the D1 database once).

The book alone — everything except accounts — is still a plain static artifact. `public/` can be served from any static host (Netlify, Vercel, GitHub Pages, nginx via `rsync -av --delete public/ user@host:/var/www/under.atheric.eu/`); without the functions the book works fully (positions stay in `localStorage`); only the optional sign-in stops working.

## Regenerate og-image.png

The committed `og-image.png` is rendered from `og-image.svg` in headless Chromium at 1200×630 (2× device scale) with the repo's self-hosted fonts, so Playfair Display and DM Mono render exactly as on the site. To regenerate after changing the SVG: serve `public/`, open the SVG in a page that loads `fonts.css`, and screenshot at 1200×630 — or use `rsvg-convert -w 1200 -h 630 public/og-image.svg -o public/og-image.png` if you have the fonts installed system-wide.

## License

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You are free to share and adapt the material non-commercially, with attribution. Commercial use requires permission. © MMXXVI · Yki Lähteenmäki / YDT Holdings Oy.

Embedded and linked third-party videos belong to their creators and are not covered by this licence.

## Status

Content-complete — **READY for the owner's complete read** (Pass 19, the
book-wide closing sweep, 2026-08-09; ledger in `UNDER.md` §4s). Last
updated 2026-08-09.
