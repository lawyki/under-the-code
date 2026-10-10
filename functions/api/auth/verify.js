// /api/auth/verify — the landing page for every emailed link.
//
// GET renders a tiny confirm page and does NOT consume the token: mail
// scanners and link-preview bots prefetch GET links, and a token consumed by
// a scanner would strand the reader. The human presses the one button,
// which POSTs back here; POST requires the site's own Origin (no login CSRF),
// atomically consumes the token, confirms the address, mints a session and
// lands on the account page — in setup mode after a confirm link, in
// recovery mode after a sign-in link.
'use strict';

import { json, sha256Hex, safeNextPath, strictOrigin, createSession } from '../_lib.js';

function page(inner) {
  return new Response(
`<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<meta name="referrer" content="same-origin">
<title>Sign in · Under the Code</title>
<style>
  body { background:#0a0a0a; color:rgba(245,240,230,0.9); font-family:Georgia,serif;
         display:flex; min-height:100vh; align-items:center; justify-content:center; margin:0; }
  main { max-width:26em; padding:32px; text-align:center; }
  .eyebrow { font-family:monospace; font-size:11px; letter-spacing:0.3em;
             text-transform:uppercase; color:rgba(212,168,83,0.7); margin-bottom:18px; }
  h1 { font-weight:500; font-size:1.5rem; font-style:italic; color:#d4a853; margin:0 0 14px; }
  p { line-height:1.7; color:rgba(245,240,230,0.72); font-size:0.95rem; }
  button { margin-top:22px; font-family:monospace; font-size:13px; letter-spacing:0.12em;
           padding:12px 28px; background:rgba(212,168,83,0.08); color:#d4a853;
           border:1px solid rgba(212,168,83,0.4); border-radius:4px; cursor:pointer; }
  button:hover { background:rgba(212,168,83,0.16); }
  a { color:#d4a853; }
</style>
</head>
<body>
<main>
  <div class="eyebrow">Under the Code</div>
  ${inner}
</main>
</body>
</html>`,
    { status: 200, headers: {
      'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store',
      // The confirm button must never be clickable inside someone else's frame.
      'X-Frame-Options': 'DENY', 'Content-Security-Policy': "frame-ancestors 'none'",
    } });
}

const TOKEN_RE = /^[A-Za-z0-9_-]{20,128}$/;

const EXPIRED = `<h1>This link has expired.</h1>
  <p>Emailed links work once and expire: confirm links after 24 hours,
  sign-in links after 30 minutes. Get a fresh one from
  <a href="/account">your account page</a>.</p>`;

export async function onRequestGet({ request, env }) {
  const token = new URL(request.url).searchParams.get('token') || '';
  if (!TOKEN_RE.test(token)) {
    return page(`<h1>That link isn&rsquo;t right.</h1>
      <p>The link is malformed. Get a fresh one from
      <a href="/account">your account page</a>.</p>`);
  }
  // Read-only lookup to word the page; the token is not consumed here.
  const row = await env.DB.prepare(
    'SELECT purpose FROM login_tokens WHERE token_hash = ? AND expires_at > ?'
  ).bind(await sha256Hex(token), Date.now()).first();
  if (!row) return page(EXPIRED);
  const confirm = row.purpose === 'verify';
  return page(`<h1>${confirm ? 'Confirm your email.' : 'Continue where you left off.'}</h1>
    <p>${confirm
      ? 'Press the button to confirm this address. Next you choose how you&rsquo;ll sign in: a passkey or a password.'
      : 'Press the button to finish signing in. The link works once.'}</p>
    <form method="POST" action="/api/auth/verify">
      <input type="hidden" name="token" value="${token}">
      <button type="submit">${confirm ? 'Confirm &rarr;' : 'Sign in &rarr;'}</button>
    </form>`);
}

export async function onRequestPost({ request, env }) {
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  let token = '';
  const type = request.headers.get('Content-Type') || '';
  if (type.includes('form')) {
    token = (await request.formData()).get('token') || '';
  } else {
    try { token = (await request.json()).token || ''; } catch { /* fall through */ }
  }
  if (!TOKEN_RE.test(token)) return json({ error: 'bad_token' }, 400);

  const now = Date.now();
  // Atomic consume: the row is gone the instant it is read.
  const tokenHash = await sha256Hex(token);
  const row = await env.DB.prepare(
    'DELETE FROM login_tokens WHERE token_hash = ? AND expires_at > ? RETURNING user_id, next_path, purpose, created_at, expires_at'
  ).bind(tokenHash, now).first();
  if (!row) return page(EXPIRED);

  let cookies;
  try {
    // Clicking any emailed link proves the reader controls the inbox.
    await env.DB.prepare('UPDATE users SET email_verified_at = COALESCE(email_verified_at, ?) WHERE id = ?')
      .bind(now, row.user_id).run();
    cookies = await createSession(env, row.user_id);
  } catch (e) {
    // A transient failure after the consume must not burn the reader's link.
    await env.DB.prepare(
      'INSERT OR IGNORE INTO login_tokens (token_hash, user_id, next_path, created_at, expires_at, purpose) VALUES (?, ?, ?, ?, ?, ?)'
    ).bind(tokenHash, row.user_id, row.next_path, row.created_at, row.expires_at, row.purpose).run().catch(() => {});
    return json({ error: 'unavailable' }, 503);
  }

  const mode = row.purpose === 'verify' ? 'setup' : 'recover';
  const next = safeNextPath(row.next_path);
  const location = `/account?${mode}=1` + (next && next !== '/account' ? '&next=' + encodeURIComponent(next) : '');
  const headers = new Headers({ Location: location, 'Cache-Control': 'no-store' });
  for (const c of cookies) headers.append('Set-Cookie', c);
  return new Response(null, { status: 303, headers });
}
