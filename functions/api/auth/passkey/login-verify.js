// POST /api/auth/passkey/login-verify — { response, next?, reauth? }.
// Every failure is the same 401.
'use strict';

import { json, strictOrigin } from '../../_lib.js';
import { verifyAuthenticationResponse } from '../../../_vendor/webauthn.mjs';
import { rp, disabled, consumeChallenge, readJson } from './_wa.js';
import { finishSignin } from '../_signin.js';

const fail = () => json({ error: 'invalid_credentials' }, 401);

export async function onRequestPost({ request, env }) {
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const body = await readJson(request);
  const response = body && body.response;
  if (!response || typeof response.id !== 'string') return fail();

  const row = await env.DB.prepare(
    `SELECT c.id, c.user_id AS userId, c.public_key AS publicKey, c.counter, c.transports,
            u.email_verified_at AS verifiedAt
       FROM credentials c JOIN users u ON u.id = c.user_id WHERE c.id = ?`
  ).bind(response.id).first();
  if (!row || !row.verifiedAt) return fail();

  // The passkey's user handle must name the same account.
  const handle = response.response && response.response.userHandle;
  if (handle) {
    let decoded = '';
    try { decoded = atob(handle.replace(/-/g, '+').replace(/_/g, '/')); } catch { return fail(); }
    if (decoded !== row.userId) return fail();
  }

  const { origin, rpID } = rp(env, request);
  let result;
  try {
    result = await verifyAuthenticationResponse({
      response,
      expectedChallenge: consumeChallenge(env, 'login', null),
      expectedOrigin: origin,
      expectedRPID: rpID,
      credential: {
        id: row.id,
        publicKey: new Uint8Array(row.publicKey),   // D1 returns BLOBs as number[]
        counter: row.counter,
        transports: row.transports ? JSON.parse(row.transports) : undefined,
      },
      requireUserVerification: false,
    });
  } catch (e) {
    return fail();
  }
  if (!result.verified) return fail();

  await env.DB.prepare('UPDATE credentials SET counter = ?, last_used_at = ? WHERE id = ?')
    .bind(result.authenticationInfo.newCounter, Date.now(), row.id).run();
  return finishSignin(request, env, row.userId, body);
}
