// POST /api/auth/passkey/register-options — start adding a passkey to the
// signed-in account. Needs a fresh sign-in.
'use strict';

import { json, getSession, isRecent, strictOrigin } from '../../_lib.js';
import { generateRegistrationOptions } from '../../../_vendor/webauthn.mjs';
import { rp, disabled, storeChallenge } from './_wa.js';

export async function onRequestPost({ request, env }) {
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  if (!isRecent(session)) return json({ error: 'reauth_required' }, 403);

  const { results } = await env.DB.prepare('SELECT id, transports FROM credentials WHERE user_id = ?')
    .bind(session.userId).all();
  const { rpID } = rp(env, request);
  const options = await generateRegistrationOptions({
    rpName: 'Under the Code',
    rpID,
    userName: session.email,
    userID: new TextEncoder().encode(session.userId),   // the account's UUID — no personal data
    attestationType: 'none',
    excludeCredentials: results.map(r => ({ id: r.id, transports: r.transports ? JSON.parse(r.transports) : undefined })),
    authenticatorSelection: { residentKey: 'required', userVerification: 'preferred' },
  });
  await storeChallenge(env, options.challenge, 'register', session.userId);
  return json(options);
}
