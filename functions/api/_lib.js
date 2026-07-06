// Shared helpers for the /api/* Pages Functions. Underscore-prefixed files
// are not routed by Pages; this module is only ever imported.
'use strict';

export const SESSION_COOKIE = '__Host-under_session';
export const HINT_COOKIE = 'under_signedin';
export const SESSION_MAX_AGE = 180 * 24 * 60 * 60;        // 180 days, seconds
export const TOKEN_TTL_MS = 15 * 60 * 1000;               // magic link: 15 min

export function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...extraHeaders,
    },
  });
}

// 256-bit random token, base64url (no padding).
export function newToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  let s = '';
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export async function sha256Hex(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
}

export function getCookie(request, name) {
  const header = request.headers.get('Cookie') || '';
  for (const part of header.split(/;\s*/)) {
    const eq = part.indexOf('=');
    if (eq > 0 && part.slice(0, eq) === name) return part.slice(eq + 1);
  }
  return null;
}

export function sessionCookies(token, maxAge = SESSION_MAX_AGE) {
  return [
    `${SESSION_COOKIE}=${token}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=${maxAge}`,
    // JS-readable hint so the client never fires an API call for a
    // signed-out reader. Carries no secret — just "a session may exist".
    `${HINT_COOKIE}=1; Path=/; Secure; SameSite=Lax; Max-Age=${maxAge}`,
  ];
}

export function clearedCookies() {
  return sessionCookies('', 0).map(c => c.replace('=1;', '=;'));
}

// Same-origin guard for state-changing requests. SameSite=Lax already keeps
// cross-site POSTs cookie-less; this adds an explicit check when the
// browser sends an Origin header at all.
export function sameOrigin(request) {
  const origin = request.headers.get('Origin');
  if (!origin) return true;
  try { return new URL(origin).host === new URL(request.url).host; }
  catch { return false; }
}

// Resolve the session cookie to { userId, email } or null.
export async function getSession(request, env) {
  const token = getCookie(request, SESSION_COOKIE);
  if (!token || token.length < 20 || token.length > 128) return null;
  const hash = await sha256Hex(token);
  const row = await env.DB.prepare(
    `SELECT s.user_id AS userId, u.email AS email
       FROM sessions s JOIN users u ON u.id = s.user_id
      WHERE s.token_hash = ? AND s.expires_at > ?`
  ).bind(hash, Date.now()).first();
  return row || null;
}

export function isValidEmail(email) {
  return typeof email === 'string'
    && email.length <= 254
    && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}

// A next-path must be a same-origin absolute path like "/part-2#ch5".
export function safeNextPath(p) {
  return (typeof p === 'string' && p.length <= 200 && /^\/(?!\/)/.test(p)) ? p : null;
}
