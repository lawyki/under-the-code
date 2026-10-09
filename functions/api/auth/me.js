// GET /api/auth/me — who am I? { email, hasPassword, passkeyCount, recent }
// or 401. The client only calls this when the under_signedin hint cookie is
// present, so signed-out readers never generate the request.
'use strict';

import { json, getSession, isRecent } from '../_lib.js';

export async function onRequestGet({ request, env }) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  const row = await env.DB.prepare(
    `SELECT password_hash IS NOT NULL AS hasPassword,
            (SELECT COUNT(*) FROM credentials WHERE user_id = ?1) AS passkeyCount
       FROM users WHERE id = ?1`
  ).bind(session.userId).first();
  return json({
    email: session.email,
    hasPassword: !!(row && row.hasPassword),
    passkeyCount: (row && row.passkeyCount) || 0,
    recent: isRecent(session),
  });
}
