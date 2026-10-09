// POST /api/auth/signout-others — "Sign out everywhere else": ends every
// session of this account except the one making the request.
'use strict';

import { json, getSession, strictOrigin } from '../_lib.js';

export async function onRequestPost({ request, env }) {
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  const res = await env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash != ?')
    .bind(session.userId, session.tokenHash).run();
  return json({ ok: true, ended: res.meta.changes || 0 });
}
