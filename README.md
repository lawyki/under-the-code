# Under the Code

A unified theory of how computers actually work — five parts, eighteen chapters, ~93,000 words, 242 inline-SVG figures (222 diagram cards + 19 chapter heroes + the cover).

Published at **[under.atheric.eu](https://under.atheric.eu)**.

By [Yki Lähteenmäki](https://github.com/lawyki). Published by [Atheric](https://atheric.eu) (YTD Holdings Oy, Helsinki).

## Repo layout

```
public/          ← deploy this directory · the only thing the domain serves
  index.html
  part-1.html ... part-5.html
  book.css, book.js
  fonts.css, fonts/ ← self-hosted webfonts (no third-party requests)
  glossary.html, glossary.json
  og-image.svg, og-image.png
  robots.txt, sitemap.xml, 404.html
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

The book is a static site — no framework, no bundler, no Node runtime in production. Everything is plain HTML + CSS + JS that a browser parses directly.

## Deploy

The `public/` directory is the publishable artifact. Any of:

**Cloudflare Pages / Netlify / Vercel** — connect the repo, set publish directory to `public/`, deploy on push. Zero config.

**GitHub Pages** — set the publish source to `public/` (or move contents to `docs/` if your fork prefers that convention).

**rsync / scp to a VPS** — `rsync -av --delete public/ user@host:/var/www/under.atheric.eu/`. Point nginx at the deployed directory.

## Regenerate og-image.png

The committed `og-image.png` is rendered from `og-image.svg` in headless Chromium at 1200×630 (2× device scale) with the repo's self-hosted fonts, so Playfair Display and DM Mono render exactly as on the site. To regenerate after changing the SVG: serve `public/`, open the SVG in a page that loads `fonts.css`, and screenshot at 1200×630 — or use `rsvg-convert -w 1200 -h 630 public/og-image.svg -o public/og-image.png` if you have the fonts installed system-wide.

## License

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). You are free to share and adapt the material non-commercially, with attribution. Commercial use requires permission. © 2026 Yki Lähteenmäki / YTD Holdings Oy.

## Status

Active — last updated 2026-05-19.
