// POST /api/auth/login — { email, password, next?, reauth? }.
// Attempt counters are reserved BEFORE hashing (parallel guesses cannot slip
// past), unknown addresses are counted too, and every failure — unknown,
// unconfirmed, no password, wrong password — is the same 401 after the same
// amount of work. An account that has never set a password or passkey gets
// one sign-in link by email (at most once a day) instead of a dead end.
'use strict';

import {
  json, strictOrigin, isValidEmail, hit, clearHits, emailKey, ipKey,
  verifyPassword, maybeCleanup,
} from '../_lib.js';
import { findUser, recoverMail } from './_account.js';
import { finishSignin } from './_signin.js';

const WINDOW = 15 * 60 * 1000;

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  let body;
  try { body = JSON.parse((await request.text()).slice(0, 2048)); } catch { return json({ error: 'bad_request' }, 400); }
  const email = String(body.email || '').trim().toLowerCase();
  const password = typeof body.password === 'string' ? body.password : '';
  if (!isValidEmail(email) || !password || password.length > 512) return json({ error: 'invalid_credentials' }, 401);

  const ipK = await ipKey('pw-ip', request);
  const emK = await emailKey('pw-email', email);
  const ipCount = await hit(env, ipK, WINDOW);
  const emCount = await hit(env, emK, WINDOW);
  if (ipCount > 50 || emCount > 10) {
    return json({ error: 'slow_down' }, 429, { 'Retry-After': '900' });
  }

  const user = await findUser(env, email);
  const usable = user && user.verifiedAt && user.passwordHash;
  let ok = false;
  try {
    ok = await verifyPassword(env, password, usable ? user.passwordHash : null);
  } catch (e) {
    console.error('password check unavailable', e && e.message);
    return json({ error: 'unavailable' }, 503);
  }
  context.waitUntil(maybeCleanup(env, p => context.waitUntil(p)));

  if (ok && usable) {
    await clearHits(env, emK);
    return finishSignin(request, env, user.id, body);
  }

  // Nudge: confirmed account with no sign-in method at all (a reader from
  // the email-link era) → one sign-in link, at most once per day.
  if (user && user.verifiedAt && !user.passwordHash) {
    const passkeys = await env.DB.prepare('SELECT COUNT(*) AS n FROM credentials WHERE user_id = ?').bind(user.id).first();
    if (!passkeys.n && await hit(env, 'nudge:' + user.id, 24 * 60 * 60 * 1000) === 1) {
      const job = await recoverMail(env, request, email, body.next);
      if (job) context.waitUntil(job.send());
    }
  }
  return json({ error: 'invalid_credentials' }, 401);
}
