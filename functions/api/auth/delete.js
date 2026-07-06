// POST /api/auth/delete — delete the account and everything attached to it:
// position, sessions, outstanding login tokens, then the user row. This is
// the deletion route promised in the privacy notice; there is nothing else
// to delete anywhere.
'use strict';

import { json, getSession, sameOrigin, clearedCookies } from '../_lib.js';

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);

  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  await env.DB.batch([
    env.DB.prepare('DELETE FROM positions WHERE user_id = ?').bind(session.userId),
    env.DB.prepare('DELETE FROM sessions WHERE user_id = ?').bind(session.userId),
    env.DB.prepare('DELETE FROM login_tokens WHERE user_id = ?').bind(session.userId),
    env.DB.prepare('DELETE FROM users WHERE id = ?').bind(session.userId),
  ]);

  const headers = new Headers({
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  for (const c of clearedCookies()) headers.append('Set-Cookie', c);
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}
