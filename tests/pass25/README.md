# Pass 25 verification suites (ledger `UNDER.md` §4y)

Playwright 1.61.1 (`npm i` here; Chromium + WebKit). Local only — nothing here
touches production.

| Command | What |
|---|---|
| `./run-all.sh` | invariants, traces, parity, marks, ui (static server on :8123, in-memory fake API; logs in `out/`) |
| `node vfix.mjs` | the Sonnet 5.5 verification fixes (needs `node serve.mjs 8124`) |
| `bash server-test.sh` | `/api/marks` + `/api/position` against `wrangler pages dev` with a fresh local D1 (`WRANGLER=…` to pick a binary) |
| `node e2e.mjs`, `node e2e2.mjs <0\|1>` | two devices against the real API on :8798 (start `wrangler pages dev public --port 8798 --binding MARKS_SYNC=<flag>` and seed sessions as `server-test.sh` does) |
| `node palette-check.mjs` | contrast + colour-blind check of the 25 marker colours (hexes inline; keep in step with `public/book.css` `[data-vol]`) |

Flags: `--browser=chromium|webkit`, `--only=<regex>`. Thresholds live in
`public/book.js` `T`; load any part with `?utc-debug` to watch the tracker.
