// POST /api/auth/passkey/login-options — start a passkey sign-in. No
// account is named: discoverable passkeys let the device offer its own.
'use strict';

import { json, strictOrigin, hit, ipKey } from '../../_lib.js';
import { generateAuthenticationOptions } from '../../../_vendor/webauthn.mjs';
import { rp, disabled, storeChallenge } from './_wa.js';

export async function onRequestPost({ request, env }) {
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  if (await hit(env, await ipKey(env, 'wa-ip', request), 5 * 60 * 1000) > 30) {
    return json({ error: 'slow_down' }, 429, { 'Retry-After': '300' });
  }
  const { rpID } = rp(env, request);
  const options = await generateAuthenticationOptions({ rpID, allowCredentials: [], userVerification: 'preferred' });
  await storeChallenge(env, options.challenge, 'login', null);
  return json(options);
}
