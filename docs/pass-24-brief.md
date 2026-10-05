# PASS 24 BRIEF (PROPOSED) — accounts v2: passkey or password (ledger §4x)

Authored by the bridge, 2026-10-05, from a 9-agent design workflow
(technical research with local tests, architect, adversarial security
review). **Status: ratified 2026-10-05 — owner decisions answered (bottom);
runs after the domain move.** Site work: `functions/`,
`schema.sql`, `public/account.html`, `wrangler.toml`, `package.json`. **Zero
book prose, zero anchors, zero figures, zero glossary.** Model: Fable.

**Context:** *Under the Code* is the owner's own published book
(under.atheric.eu). Read first: `CLAUDE.md`, `BRIDGE.md`, `UNDER.md` §4c
(the accounts build this replaces), §5, `STATE.md`.

## Owner's intent

A normal sign-in page that is always there. The reader chooses **passkey or
password** (or both). The email link is only for **confirming a new
account** (unconfirmed accounts are removed after 14 days) and for
**recovery**. Sessions stay 180 days. Existing magic-link readers keep their
reading position.

## The design (ratified shape — do not redesign)

**Email first, method second.** Sign-up asks only for an email. The
confirmation link signs the reader in and opens a setup panel: create a
passkey, set a password, or both. Consequences: no credential is ever
attached to an unconfirmed address (no pre-hijacking); passkey registration
always happens inside a real session; "confirmed but no method yet" is one
state, shared by new readers who skip setup and every migrated magic-link
reader, and both leave it the same way — the recovery link.

**Stack (researched and locally tested; re-verify on a preview deploy):**
- Passwords: **Argon2id** m=19456 KiB, t=2, p=1, 16-byte salt, 32-byte
  output, PHC string, rehash-on-login when parameters rise. Package
  `argon2id` (openpgpjs) via a **static `.wasm` import** with a custom
  loader that calls `WebAssembly.instantiate(importedModule, imports)` —
  Workers forbid compiling WASM from bytes. One instance per isolate;
  measure peak memory as well as CPU on the preview.
  **Fallback** only if Argon2 fails in production: PBKDF2-SHA256 at
  exactly **100,000** iterations (workerd's hard cap — local wrangler does
  NOT enforce it, production throws above it) plus an HMAC pepper from a
  Pages secret; version-prefixed so hashes migrate later.
- Passkeys: `@simplewebauthn/server` — pin a version that exists on npm and
  passes a full register + sign-in on the preview; `attestationType:
  'none'`, discoverable credentials (`residentKey: 'required'`),
  `userVerification: 'preferred'`. Client side: the browser's native
  WebAuthn API (`parseCreationOptionsFromJSON` / `toJSON` where present,
  ~30-line inline base64url fallback) — **no vendored library, no
  third-party request**; book pages load nothing new.
- Bundling: dependencies in `package.json` + committed lockfile; confirm
  Pages Git builds bundle `node_modules` and the `.wasm` import. If not,
  commit a pre-built bundle under `functions/_vendor/`.
- Rate limiting: D1 counters (`auth_attempts`, keys are SHA-256 of
  normalised email / `CF-Connecting-IP`, IPv6 by /64). The Workers
  Rate Limiting binding is not available on Pages.
- Cleanup without cron (Pages has none): lazy `maybeCleanup` inside
  signup/login/recover via `waitUntil`, at most every 6 h, slot claimed
  atomically in a `meta` row (INTEGER value).
- Migrations: D1 tracked migrations (`migrations/`, `wrangler d1
  migrations apply`), export + Time Travel restore point first.

**Schema (additive):** `users` + `email_verified_at`, `password_hash`,
`password_updated_at`; `login_tokens` + `purpose` (`verify` | `recover`,
legacy `login` treated as `recover`); new tables `credentials` (passkeys),
`webauthn_challenges`, `auth_attempts`, `meta`. `positions`, `sessions`,
cookies, `getSession`, `/api/position` and every line of `book.js`
unchanged. `users.id` never changes — that is what keeps reading positions.

**Endpoints** (`functions/api/auth/`): `signup`, `verify` (GET page / POST
consume — keep the scanner-safe pattern), `login`, `recover`, `me` (+
`hasPassword`, `passkeyCount`), `credentials`, `password`,
`password/remove`, `passkey/register-options`, `passkey/register-verify`,
`passkey/login-options`, `passkey/login-verify`, `passkey/rename`,
`passkey/remove`, `sessions/revoke-others`, `logout`, `delete`. Legacy
`request` kept 30 days for cached pages (unknown email → signup, known →
recover; never creates a verified user), then `410`.

**Flows:** new reader (password or passkey); returning reader (password
form, passkey button, passkey autofill via `autocomplete="username
webauthn"` + conditional mediation); add the other method later; forgot
password; lost passkey; existing magic-link reader — still signed in: a
card on `/account` invites them to choose a method, reading never
interrupted; signed out: "Email me a sign-in link" → setup panel, position
intact.

## Security requirements (from the adversarial review — all mandatory)

1. **Every credential change needs a fresh sign-in** (session < 15 min) or
   `currentPassword` — including setting a *first* password. No exemption
   for accounts without one (otherwise a stolen old cookie takes over).
2. **Fix the open redirect in `next`** (exists today: `/\evil.com` passes
   `safeNextPath`). Parse with `new URL(p, SITE_ORIGIN)` and require the
   same origin; re-check on the client before navigating.
3. **No timing leaks:** signup and recover send mail inside `waitUntil` in
   every branch and do equal database work; login always runs Argon2
   (dummy hash for unknown / unconfirmed / no-password).
4. **Reserve-then-hash rate limits:** atomic increment *before* hashing on
   `pw-email`, `pw-ip`, and `currentPassword` checks; reset on success;
   unknown emails counted too.
5. **Recovery can't be blocked or used to mail-bomb:** sign-up for an
   already-confirmed address sends a notice with no token; per-email daily
   mail cap (~10); recover budget keyed per (email, IP /24); per-email 429
   on signup returns a silent 200.
6. **Login CSRF on `POST /verify`:** require `Origin === SITE_ORIGIN`, and
   change the confirm page's referrer meta from `no-referrer` to
   `same-origin` first (no-referrer makes the browser send `Origin: null`
   and would break every real click).
7. **Migration marks only proven readers confirmed:** `email_verified_at =
   created_at` only for users with a session or a position row; the rest
   stay unconfirmed and age out.
8. **Sessions and notices:** delete other sessions on password change,
   password removal, passkey removal and recovery-link use; notice mail on
   every credential change ("Not you? Recover here"); recent sign-in for
   `/delete`; "Sign out everywhere else" button.
9. **Passkey challenges** looked up by hash of the challenge itself (not
   one shared cookie — two tabs must not clobber each other).
10. Remaining review items L1–L14 (last-method removal race as one
    conditional statement, `ON CONFLICT` signup, reauth must stay the same
    user, auto-nudge stored as `nudge:<user_id>`, cleanup skips rows with a
    live verify token, passkey names via `textContent`, D1 BLOB →
    `Uint8Array`, `timingSafeEqual` length check, top-10k common-password
    list kept locally). Full text in this pass's design dossier
    (reproduce it in the ledger).
11. **Preview isolation:** a separate D1 database under `[env.preview]`;
    `SITE_ORIGIN`/`RP_ID` overrides via `[env.preview.vars]`; reject
    `/api/*` on hosts other than the site host (the pages.dev alias skips
    the zone WAF).

## account.html

Same visual language (`.acct-block`, `.acct-btn`, mono labels,
`role="status"`), inline JS. Views: sign in (default), create account,
recover, setup panel, signed-in with a **Sign-in methods** block (password
set/change/remove; passkey list with rename/remove; remove disabled on the
last method). Correct `autocomplete` on every field, show/hide toggle, no
confirm-password field, errors with a recovery path. **Copy changes need
owner approval:** the "one email, one signed link, no password" intro and
the privacy notice (what is stored: password hash, passkey public keys,
short-lived hashed rate-limit counters; retention: confirm links 24 h,
recovery links 30 min, unconfirmed accounts 14 days).

## Verification & close-out

Preview deploy first, against the preview database: full passkey register
+ sign-in on Safari, Chrome and Firefox (macOS + iOS + Android); password
sign-up, sign-in, change, forgot; migrated-user path both ways; every
security requirement above exercised with a failing case; Argon2 CPU and
memory measured. Then production: migration applied, a real migrated
account verified to keep its position, §7 harness on account/index/one part
page in Chromium + WebKit — 0 console errors, 0 external requests. Ledger
**`UNDER.md` §4x**. Update `STATE.md`.

## Owner decisions (answered 2026-10-05)

1. **Domain: the site moves to a new domain in about a month.** Passkeys
   are permanently bound to the domain they are created on (`RP_ID`), so
   passkeys made before the move would stop working after it. **This pass
   therefore runs after the domain move**, with `RP_ID` and `SITE_ORIGIN`
   set to the new domain. Keep both as config vars, never hard-coded. If
   the pass must run earlier, ship passwords only and turn passkeys on
   after the move.
2. **Workers Paid: confirmed by the owner.** Argon2id it is. The PBKDF2
   fallback is used only if Argon2 fails the preview measurement.
3. **No breached-password check, and no common-password list.** Owner's
   ruling on proportion: *this is a book, not a bank — do the thing well,
   don't over-engineer.* Requirements 1–9 and 11 above are the real core
   (they are ordinary correctness, not bank-grade ceremony). Treat item 10
   as judgment, not a checklist: do what is cheap and obviously right,
   skip what adds friction for readers.
4. **Account-page and privacy copy:** the pass drafts it; the owner
   approves before deploy.

## Note for the domain move (not this pass)

Moving domains signs every reader out (cookies are host-bound) and
**loses signed-out readers' saved positions** (localStorage is
per-origin). The move should redirect old URLs with their `#anchor`
intact, and could hand local positions across with a one-time
`?resume=` parameter on the redirect. Brief that with the move.
