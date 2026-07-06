// /api/auth/verify — the magic-link landing.
//
// GET renders a tiny self-contained confirm page and does NOT consume the
// token: corporate mail scanners and link-preview bots prefetch GET links,
// and a consumed-by-scanner token would strand the actual reader. The
// human presses the one button, which POSTs back here; POST atomically
// consumes the token (DELETE … RETURNING), mints a session, sets cookies,
// and redirects into the book.
'use strict';

import {
  json, newToken, sha256Hex, sessionCookies, SESSION_MAX_AGE,
} from '../_lib.js';

function page(inner) {
  return new Response(
`<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<meta name="referrer" content="no-referrer">
<title>Sign in — Under the Code</title>
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
    { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } });
}

const TOKEN_RE = /^[A-Za-z0-9_-]{20,128}$/;

export async function onRequestGet({ request }) {
  const token = new URL(request.url).searchParams.get('token') || '';
  if (!TOKEN_RE.test(token)) {
    return page(`<h1>That link isn&rsquo;t right.</h1>
      <p>The sign-in link is malformed. Request a fresh one from
      <a href="/account">your account page</a>.</p>`);
  }
  return page(`<h1>Continue where you left off.</h1>
    <p>Press the button to finish signing in. The link works once
    and expires fifteen minutes after it was sent.</p>
    <form method="POST" action="/api/auth/verify">
      <input type="hidden" name="token" value="${token}">
      <button type="submit">Sign in &rarr;</button>
    </form>`);
}

export async function onRequestPost({ request, env }) {
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
  const row = await env.DB.prepare(
    'DELETE FROM login_tokens WHERE token_hash = ? AND expires_at > ? RETURNING user_id, next_path'
  ).bind(await sha256Hex(token), now).first();

  if (!row) {
    return page(`<h1>This link has expired.</h1>
      <p>Sign-in links work once and expire after fifteen minutes.
      Request a fresh one from <a href="/account">your account page</a>.</p>`);
  }

  const session = newToken();
  await env.DB.prepare(
    'INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)'
  ).bind(await sha256Hex(session), row.user_id, now, now + SESSION_MAX_AGE * 1000).run();

  const headers = new Headers({
    Location: row.next_path || '/account',
    'Cache-Control': 'no-store',
  });
  for (const c of sessionCookies(session)) headers.append('Set-Cookie', c);
  return new Response(null, { status: 303, headers });
}
