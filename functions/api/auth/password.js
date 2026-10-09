// POST /api/auth/password — { newPassword, currentPassword? }. Sets or
// changes the password. Always needs a fresh sign-in (session < 15 min) or
// the current password — including a FIRST password, so an old stolen
// cookie can never set one. Afterwards every other session is signed out,
// outstanding sign-in links are cancelled, and the owner gets a notice.
'use strict';

import {
  json, getSession, isRecent, strictOrigin, passwordProblem, hashPassword,
  verifyPassword, hit, pairKey, readBody,
} from '../_lib.js';
import { changeNotice } from './_account.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  const body = await readBody(request);
  if (!body) return json({ error: 'bad_request' }, 400);

  const problem = passwordProblem(body.newPassword);
  if (problem) return json({ error: problem }, 400);

  const user = await env.DB.prepare('SELECT password_hash AS passwordHash FROM users WHERE id = ?')
    .bind(session.userId).first();

  try {
    if (!isRecent(session)) {
      if (typeof body.currentPassword !== 'string' || !user.passwordHash) {
        return json({ error: 'reauth_required' }, 403);
      }
      // The same attempt counter as sign-in guards the current-password check.
      if (await hit(env, await pairKey(env, 'pw-pair', session.email, request), 15 * 60 * 1000) > 10) {
        return json({ error: 'slow_down' }, 429, { 'Retry-After': '900' });
      }
      if (!(await verifyPassword(env, body.currentPassword, user.passwordHash))) {
        return json({ error: 'wrong_password' }, 403);
      }
    }
    const hash = await hashPassword(env, body.newPassword);
    const now = Date.now();
    await env.DB.batch([
      env.DB.prepare('UPDATE users SET password_hash = ?, password_updated_at = ? WHERE id = ?').bind(hash, now, session.userId),
      env.DB.prepare('DELETE FROM sessions WHERE user_id = ? AND token_hash != ?').bind(session.userId, session.tokenHash),
      env.DB.prepare("DELETE FROM login_tokens WHERE user_id = ? AND purpose != 'verify'").bind(session.userId),
    ]);
  } catch (e) {
    console.error('password set failed', e && e.message);
    return json({ error: 'unavailable' }, 503);
  }
  context.waitUntil(changeNotice(env, request, session.email, user.passwordHash ? 'Your password was changed' : 'A password was set'));
  return json({ ok: true });
}
