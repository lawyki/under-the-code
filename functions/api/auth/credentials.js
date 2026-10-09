// GET /api/auth/credentials — the account page's "Sign-in methods" panel.
'use strict';

import { json, getSession } from '../_lib.js';

export async function onRequestGet({ request, env }) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  const user = await env.DB.prepare(
    'SELECT password_hash IS NOT NULL AS hasPassword, password_updated_at AS passwordUpdatedAt FROM users WHERE id = ?'
  ).bind(session.userId).first();
  const { results } = await env.DB.prepare(
    `SELECT id, name, created_at AS createdAt, last_used_at AS lastUsedAt, backed_up AS backedUp
       FROM credentials WHERE user_id = ? ORDER BY created_at`
  ).bind(session.userId).all();
  return json({
    hasPassword: !!user.hasPassword,
    passwordUpdatedAt: user.passwordUpdatedAt || null,
    passkeys: results.map(r => ({ ...r, backedUp: !!r.backedUp })),
  });
}
