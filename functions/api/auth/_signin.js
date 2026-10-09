// Finishing a sign-in: mint the session, and when the sign-in is a
// "confirm it's you" step (reauth), refuse if it signed in as someone else.
'use strict';

import { json, getSession, createSession, safeNextPath } from '../_lib.js';

export async function finishSignin(request, env, userId, body) {
  if (body && body.reauth) {
    const current = await getSession(request, env);
    if (current && current.userId !== userId) return json({ error: 'different_account' }, 409);
  }
  const res = json({ ok: true, next: safeNextPath(body && body.next) || null });
  for (const c of await createSession(env, userId)) res.headers.append('Set-Cookie', c);
  return res;
}
