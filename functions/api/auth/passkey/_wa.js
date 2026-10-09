// Shared passkey (WebAuthn) plumbing. Passkeys are switched off until the
// domain move — a passkey is bound to the domain it is created on — and
// PASSKEYS_ENABLED="1" turns them on. RP_ID defaults to the site's hostname.
'use strict';

import { json, sha256Hex, siteOrigin, passkeysOn } from '../../_lib.js';

export const CHALLENGE_TTL_MS = 5 * 60 * 1000;

export function rp(env, request) {
  const origin = siteOrigin(env, request);
  return { origin, rpID: env.RP_ID || new URL(origin).hostname };
}

export function disabled(env) {
  return passkeysOn(env) ? null : json({ error: 'passkeys_disabled' }, 404);
}

export async function storeChallenge(env, challenge, purpose, userId) {
  const now = Date.now();
  await env.DB.prepare(
    'INSERT INTO webauthn_challenges (challenge_hash, user_id, purpose, created_at, expires_at) VALUES (?, ?, ?, ?, ?)'
  ).bind(await sha256Hex(challenge), userId || null, purpose, now, now + CHALLENGE_TTL_MS).run();
}

// A challenge checker for SimpleWebAuthn's expectedChallenge callback: the
// challenge row is looked up by the hash of the challenge itself and
// consumed atomically, so it works once and two tabs never collide.
export function consumeChallenge(env, purpose, userId) {
  return async challenge => {
    const row = await env.DB.prepare(
      `DELETE FROM webauthn_challenges
        WHERE challenge_hash = ? AND purpose = ? AND expires_at > ?
        RETURNING user_id`
    ).bind(await sha256Hex(challenge), purpose, Date.now()).first();
    if (!row) return false;
    return purpose === 'login' || row.user_id === userId;
  };
}

export async function readJson(request) {
  try {
    const v = JSON.parse((await request.text()).slice(0, 16384));
    return v && typeof v === 'object' && !Array.isArray(v) ? v : null;
  } catch { return null; }
}

// Reader-chosen passkey label: control characters stripped, 60 chars max.
export function cleanName(name, fallback) {
  const s = typeof name === 'string' ? name.replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, 60) : '';
  return s || fallback;
}
