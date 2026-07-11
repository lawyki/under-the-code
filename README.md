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
  account.html   ← sign-in + privacy notice (/account)
  og-image.svg, og-image.png
  robots.txt, sitemap.xml, 404.html, _headers
functions/       ← Cloudflare Pages Functions · the account/position API (/api/*)
schema.sql       ← D1 schema: users, sessions, login tokens, reading positions
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
```

The book itself is a static site — no framework, no bundler. Everything in `public/` is plain HTML + CSS + JS that a browser parses directly. Alongside it runs one small optional service: the account/position API in `functions/`, deployed as Cloudflare Pages Functions against a D1 database.

## Reading positions & accounts

Signed out, your reading position is kept in the browser's `localStorage` only — it never leaves the device. Signing in (one email, one magic link, no password) stores that same single position server-side in D1 so it can follow you between devices. What is stored, why, and for how long is disclosed in the privacy notice at [/account#privacy](https://under.atheric.eu/account#privacy).

## Deploy

Production is **Cloudflare Pages**: pushes to `main` deploy `public/` as the site and `functions/` as the `/api/*` account service (bindings in `wrangler.toml`; apply `schema.sql` to the D1 database once).

The book alone — everything except accounts — is still a plain static artifact. `public/` can be served from any static host (Netlify, Vercel, GitHub Pages, nginx via `rsync -av --delete public/ user@host:/var/www/under.atheric.eu/`); without the functions the book works fully (positions stay in `localStorage`); only the optional sign-in stops working.

## Regenerate og-image.png

The committed `og-image.png` is rendered from `og-image.svg` in headless Chromium at 1200×630 (2× device scale) with the repo's self-hosted fonts, so Playfair Display and DM Mono render exactly as on the site. To regenerate after changing the SVG: serve `public/`, open the SVG in a page that loads `fonts.css`, and screenshot at 1200×630 — or use `rsvg-convert -w 1200 -h 630 public/og-image.svg -o public/og-image.png` if you have the fonts installed system-wide.

## License

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You are free to share and adapt the material non-commercially, with attribution. Commercial use requires permission. © MMXXVI · Yki Lähteenmäki / YDT Holdings Oy.

## Status

Active — last updated 2026-07-11.
