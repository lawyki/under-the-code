// POST /api/auth/logout — delete the session row and clear both cookies.
'use strict';

import {
  json, getCookie, sha256Hex, clearedCookies, sameOrigin, SESSION_COOKIE,
} from '../_lib.js';

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);

  const token = getCookie(request, SESSION_COOKIE);
  if (token) {
    await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?')
      .bind(await sha256Hex(token)).run();
  }

  const headers = new Headers({ 'Cache-Control': 'no-store' });
  for (const c of clearedCookies()) headers.append('Set-Cookie', c);

  // Plain form POSTs (no-JS fallback) bounce back to the account page.
  const type = request.headers.get('Content-Type') || '';
  if (type.includes('form')) {
    headers.set('Location', '/account');
    return new Response(null, { status: 303, headers });
  }
  headers.set('Content-Type', 'application/json; charset=utf-8');
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}
