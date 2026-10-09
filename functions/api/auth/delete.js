// POST /api/auth/delete — delete the account and everything attached to it:
// position, passkeys, challenges, sessions, outstanding emailed links,
// rate-limit nudge, then the user row. Needs a fresh sign-in. This is the
// deletion route promised in the privacy notice; there is nothing else to
// delete anywhere.
'use strict';

import { json, getSession, isRecent, strictOrigin, clearedCookies } from '../_lib.js';

export async function onRequestPost({ request, env }) {
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);

  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  if (!isRecent(session)) return json({ error: 'reauth_required' }, 403);

  const id = session.userId;
  await env.DB.batch([
    env.DB.prepare('DELETE FROM positions WHERE user_id = ?').bind(id),
    env.DB.prepare('DELETE FROM credentials WHERE user_id = ?').bind(id),
    env.DB.prepare('DELETE FROM webauthn_challenges WHERE user_id = ?').bind(id),
    env.DB.prepare('DELETE FROM sessions WHERE user_id = ?').bind(id),
    env.DB.prepare('DELETE FROM login_tokens WHERE user_id = ?').bind(id),
    env.DB.prepare('DELETE FROM auth_attempts WHERE key = ?').bind('nudge:' + id),
    env.DB.prepare('DELETE FROM users WHERE id = ?').bind(id),
  ]);

  const headers = new Headers({
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
  });
  for (const c of clearedCookies()) headers.append('Set-Cookie', c);
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}
