// POST /api/auth/passkey/register-verify — { response, name? }. Finish adding
// a passkey: verify the browser's attestation against the stored challenge,
// store the public key, notify the owner.
'use strict';

import { json, getSession, isRecent, strictOrigin } from '../../_lib.js';
import { verifyRegistrationResponse } from '../../../_vendor/webauthn.mjs';
import { rp, disabled, consumeChallenge, readJson, cleanName } from './_wa.js';
import { changeNotice } from '../_account.js';

const TRANSPORTS = new Set(['ble', 'cable', 'hybrid', 'internal', 'nfc', 'smart-card', 'usb']);

export async function onRequestPost(context) {
  const { request, env } = context;
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  if (!isRecent(session)) return json({ error: 'reauth_required' }, 403);
  const body = await readJson(request);
  if (!body || !body.response) return json({ error: 'bad_request' }, 400);

  const { origin, rpID } = rp(env, request);
  let result;
  try {
    result = await verifyRegistrationResponse({
      response: body.response,
      expectedChallenge: consumeChallenge(env, 'register', session.userId),
      expectedOrigin: origin,
      expectedRPID: rpID,
      requireUserVerification: false,
    });
  } catch (e) {
    return json({ error: 'bad_response' }, 400);
  }
  if (!result.verified) return json({ error: 'bad_response' }, 400);

  const info = result.registrationInfo;
  const cred = info.credential;
  const transports = Array.isArray(cred.transports) ? cred.transports.filter(t => TRANSPORTS.has(t)) : [];
  const now = Date.now();
  const name = cleanName(body.name, info.credentialBackedUp ? 'Synced passkey' : 'Passkey on this device');
  try {
    await env.DB.prepare(
      `INSERT INTO credentials (id, user_id, public_key, counter, transports, backed_up, name, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(cred.id, session.userId, cred.publicKey, cred.counter || 0, JSON.stringify(transports),
      info.credentialBackedUp ? 1 : 0, name, now).run();
  } catch (e) {
    return json({ error: 'already_registered' }, 409);
  }
  context.waitUntil(changeNotice(env, request, session.email, 'A passkey was added'));
  return json({ ok: true, passkey: { id: cred.id, name, createdAt: now, lastUsedAt: null, backedUp: !!info.credentialBackedUp } });
}
