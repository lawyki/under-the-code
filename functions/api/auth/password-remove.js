// POST /api/auth/password-remove — remove the password. Needs a fresh
// sign-in and at least one passkey; the check and the delete are one
// statement, so racing removals can never leave an account with no way in.
'use strict';

import { json, getSession, isRecent, strictOrigin } from '../_lib.js';
import { changeNotice } from './_account.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  if (!isRecent(session)) return json({ error: 'reauth_required' }, 403);
  const res = await env.DB.prepare(
    `UPDATE users SET password_hash = NULL, password_updated_at = ?1
      WHERE id = ?2 AND password_hash IS NOT NULL
        AND (SELECT COUNT(*) FROM credentials WHERE user_id = ?2) > 0`
  ).bind(Date.now(), session.userId).run();
  if (!res.meta.changes) return json({ error: 'last_credential' }, 409);
  await env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash != ?')
    .bind(session.userId, session.tokenHash).run();
  context.waitUntil(changeNotice(env, request, session.email, 'Your password was removed'));
  return json({ ok: true });
}
