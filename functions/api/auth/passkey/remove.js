// POST /api/auth/passkey/remove — { id }. Needs a fresh sign-in. Refused for
// the last way in (last passkey and no password) — checked and deleted in
// one statement, so racing removals can't strand the account. Signs out
// every other session (a lost device's session ends with its passkey).
'use strict';

import { json, getSession, isRecent, strictOrigin } from '../../_lib.js';
import { disabled, readJson } from './_wa.js';
import { changeNotice } from '../_account.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  if (!isRecent(session)) return json({ error: 'reauth_required' }, 403);
  const body = await readJson(request);
  if (!body || typeof body.id !== 'string') return json({ error: 'bad_request' }, 400);
  const res = await env.DB.prepare(
    `DELETE FROM credentials WHERE id = ?1 AND user_id = ?2
       AND ((SELECT password_hash FROM users WHERE id = ?2) IS NOT NULL
            OR (SELECT COUNT(*) FROM credentials WHERE user_id = ?2) > 1)`
  ).bind(body.id, session.userId).run();
  if (!res.meta.changes) return json({ error: 'last_credential' }, 409);
  await env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash != ?')
    .bind(session.userId, session.tokenHash).run();
  context.waitUntil(changeNotice(env, request, session.email, 'A passkey was removed'));
  return json({ ok: true });
}
