# Pre-read audit · owner calls

Findings the author may not settle alone: owner text (epigraphs, pull-quotes, the thesis set, the colophon, Ch18's closing note, Fig 18.6's caption), the 18 kept-original figures, verdicts the judge marked "owner", and the account page's legal wording. One entry each: what, options, recommendation. Nothing here was changed in the text.

## Outside the chapters

- **Privacy notice: "a Cloudflare D1 database in the European Union"** (`public/account.html`, outside.json). `wrangler d1 info under-book` reports jurisdiction null and region EEUR, a location hint that Cloudflare says does not guarantee placement; only a database created with `--jurisdiction=eu` guarantees EU storage. Options: (a) recreate the database with `--jurisdiction=eu`, migrate the rows, keep the sentence; (b) reword to the setup as it is ("a Cloudflare D1 database placed in Cloudflare's Eastern Europe region"); (c) leave. Recommended: (a) if EU storage is a promise you want to make, otherwise (b) now; the sentence is a factual claim in a privacy notice, so (c) is the one option to avoid.
