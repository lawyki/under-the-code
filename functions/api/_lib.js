// Shared helpers for the /api/* Pages Functions. Underscore-prefixed files
// are not routed by Pages; this module is only ever imported.
'use strict';

export const SESSION_COOKIE = '__Host-under_session';
export const HINT_COOKIE = 'under_signedin';
export const SESSION_MAX_AGE = 180 * 24 * 60 * 60;        // 180 days, seconds
export const TOKEN_TTL_MS = 15 * 60 * 1000;               // legacy magic link: 15 min
export const VERIFY_TTL_MS = 24 * 60 * 60 * 1000;         // confirm-your-email link: 24 h
export const RECOVER_TTL_MS = 30 * 60 * 1000;             // recovery link: 30 min
export const RECENT_MS = 15 * 60 * 1000;                  // "recent sign-in" for credential changes
export const UNVERIFIED_TTL_MS = 14 * 24 * 60 * 60 * 1000; // unconfirmed accounts removed after 14 days

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

// Resolve the session cookie to { userId, email, createdAt, tokenHash } or null.
export async function getSession(request, env) {
  const token = getCookie(request, SESSION_COOKIE);
  if (!token || token.length < 20 || token.length > 128) return null;
  const hash = await sha256Hex(token);
  const row = await env.DB.prepare(
    `SELECT s.user_id AS userId, u.email AS email, s.created_at AS createdAt
       FROM sessions s JOIN users u ON u.id = s.user_id
      WHERE s.token_hash = ? AND s.expires_at > ?`
  ).bind(hash, Date.now()).first();
  return row ? { ...row, tokenHash: hash } : null;
}

// A session minted within the last 15 minutes counts as a fresh sign-in,
// which every credential change requires (no exemption for accounts that
// have no password yet — an old stolen cookie must not be able to set one).
export function isRecent(session) {
  return !!session && Date.now() - session.createdAt < RECENT_MS;
}

// Mint a 180-day session for a user. Returns the Set-Cookie values.
export async function createSession(env, userId) {
  const token = newToken();
  const now = Date.now();
  await env.DB.prepare(
    'INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)'
  ).bind(await sha256Hex(token), userId, now, now + SESSION_MAX_AGE * 1000).run();
  return sessionCookies(token);
}

// --- Origins ---------------------------------------------------------------
// SITE_ORIGIN (wrangler.toml [vars]; .dev.vars overrides it locally) is the
// one origin mail links are built from and state-changing auth POSTs must
// come from. Never derived from the request when configured.
export function siteOrigin(env, request) {
  return env.SITE_ORIGIN || new URL(request.url).origin;
}

export function isLocal(request) {
  const h = new URL(request.url).hostname;
  return h === 'localhost' || h === '127.0.0.1';
}

// Strict check for auth POSTs: the Origin header must be present and equal
// the site origin. (Browsers always send Origin on POST.)
export function strictOrigin(request, env) {
  return request.headers.get('Origin') === siteOrigin(env, request);
}

// --- Passwords -------------------------------------------------------------
// PBKDF2-SHA256 at 100,000 iterations — the hard cap of the Workers runtime
// (local wrangler does not enforce it; production throws above it) — over an
// HMAC-SHA256 of the password keyed with a server-side pepper (Pages secret
// PASSWORD_PEPPER). Argon2id was evaluated and declined: its Wasm build needs
// a 65 MB memory per isolate against a 128 MB limit. The hash string is
// versioned ("p1$…") so it can be upgraded on the next sign-in later.
const PBKDF2_ITERATIONS = 100000;
const enc = new TextEncoder();

function b64u(bytes) {
  let s = '';
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function unb64u(str) {
  const bin = atob(str.replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(bin, c => c.charCodeAt(0));
}

export function passwordProblem(pw) {
  if (typeof pw !== 'string') return 'weak_password';
  const n = [...pw.normalize('NFKC')].length;
  if (n < 8 || n > 128) return 'weak_password';
  return null;
}

async function derive(env, password, salt) {
  if (!env.PASSWORD_PEPPER) throw new Error('pepper_missing');
  const pepperKey = await crypto.subtle.importKey(
    'raw', enc.encode(env.PASSWORD_PEPPER), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const peppered = await crypto.subtle.sign('HMAC', pepperKey, enc.encode(password.normalize('NFKC')));
  const base = await crypto.subtle.importKey('raw', peppered, 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', hash: 'SHA-256', salt, iterations: PBKDF2_ITERATIONS }, base, 256);
  return new Uint8Array(bits);
}

export async function hashPassword(env, password) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const hash = await derive(env, password, salt);
  return `p1$${PBKDF2_ITERATIONS}$${b64u(salt)}$${b64u(hash)}`;
}

function equalBytes(a, b) {
  if (a.byteLength !== b.byteLength) return false;
  if (crypto.subtle.timingSafeEqual) return crypto.subtle.timingSafeEqual(a, b);
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a[i] ^ b[i];
  return d === 0;
}

// Always does the full derivation, even with no stored hash, so a missing
// account or password costs the same time as a wrong one.
export async function verifyPassword(env, password, stored) {
  const parts = typeof stored === 'string' ? stored.split('$') : [];
  const valid = parts.length === 4 && parts[0] === 'p1';
  const salt = valid ? unb64u(parts[2]) : crypto.getRandomValues(new Uint8Array(16));
  const got = await derive(env, typeof password === 'string' ? password : '', salt);
  if (!valid) return false;
  return equalBytes(got, unb64u(parts[3]));
}

// --- Rate limits -----------------------------------------------------------
// Fixed-window counter, incremented atomically and checked BEFORE any
// expensive work (reserve first, so parallel requests cannot all slip past
// the check). Keys are hashed. Returns the count including this hit.
export async function hit(env, key, windowMs) {
  const now = Date.now();
  const row = await env.DB.prepare(
    `INSERT INTO auth_attempts (key, window_start, count) VALUES (?1, ?2, 1)
     ON CONFLICT(key) DO UPDATE SET
       count        = CASE WHEN window_start < ?3 THEN 1  ELSE count + 1 END,
       window_start = CASE WHEN window_start < ?3 THEN ?2 ELSE window_start END
     RETURNING count`
  ).bind(key, now, now - windowMs).first();
  return row ? row.count : 1;
}

export async function clearHits(env, key) {
  await env.DB.prepare('DELETE FROM auth_attempts WHERE key = ?').bind(key).run();
}

// Counter keys are HMAC'd with the server pepper (a plain SHA-256 of an IPv4
// address is trivially reversible), so the stored key reveals neither the
// address nor the network.
async function keyHash(env, value) {
  if (!env.PASSWORD_PEPPER) return sha256Hex(value);
  const k = await crypto.subtle.importKey('raw', enc.encode(env.PASSWORD_PEPPER), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = new Uint8Array(await crypto.subtle.sign('HMAC', k, enc.encode('counter:' + value)));
  return Array.from(sig, b => b.toString(16).padStart(2, '0')).join('');
}

export function clientIp(request, v4Prefix24 = false) {
  let ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (ip.includes(':')) return ip.split(':').slice(0, 4).join(':') + '::/64';
  return v4Prefix24 ? ip.split('.').slice(0, 3).join('.') + '.0/24' : ip;
}

export async function emailKey(env, prefix, email) { return prefix + ':' + await keyHash(env, email); }
export async function ipKey(env, prefix, request, v4Prefix24 = false) { return prefix + ':' + await keyHash(env, clientIp(request, v4Prefix24)); }
export async function pairKey(env, prefix, email, request) {
  return prefix + ':' + await keyHash(env, email + '|' + clientIp(request, true));
}

// --- Mail ------------------------------------------------------------------
// Cloudflare Email Sending REST API (the [[send_email]] binding is
// Workers-only — Pages configuration rejects it).
const FROM = 'Under the Code <under@atheric.eu>';

export async function sendMail(env, { to, subject, text, html }) {
  if (!env.EMAIL_API_TOKEN || !env.CF_ACCOUNT_ID) {
    console.error('mail not configured');
    return false;
  }
  try {
    const res = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/email/sending/send`,
      {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${env.EMAIL_API_TOKEN}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ to, from: FROM, subject, text, html }),
      });
    const out = await res.json().catch(() => null);
    const ok = !!(res.ok && out && out.success);
    if (!ok) console.error('mail failed', res.status, JSON.stringify((out && out.errors) || []));
    return ok;
  } catch (e) {
    console.error('mail failed', (e && e.message) || e);
    return false;
  }
}

// One mail template in the book's register: a line of copy, an optional
// button-link, a footnote.
export function mailBody({ lead, linkText, link, note }) {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const text = [lead, link ? '\n' + link + '\n' : '', note, '\nunder.atheric.eu'].filter(Boolean).join('\n');
  const html =
`<div style="font-family:Georgia,serif;max-width:34em;margin:0 auto;padding:24px;color:#1a1614">
  <p style="font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:#8a6a2a;font-family:monospace">Under the Code</p>
  <p>${esc(lead)}</p>
  ${link ? `<p><a href="${esc(link)}" style="color:#8a6a2a">${esc(linkText)}</a></p>` : ''}
  <p style="color:#7a7570;font-size:14px">${esc(note)}</p>
  <p style="color:#7a7570;font-size:14px">under.atheric.eu</p>
</div>`;
  return { text, html };
}

// Issue a one-time emailed token of the given purpose. Returns the link.
export async function issueToken(env, request, userId, purpose, nextPath) {
  const token = newToken();
  const now = Date.now();
  const ttl = purpose === 'verify' ? VERIFY_TTL_MS : RECOVER_TTL_MS;
  await env.DB.prepare(
    'INSERT INTO login_tokens (token_hash, user_id, next_path, created_at, expires_at, purpose) VALUES (?, ?, ?, ?, ?, ?)'
  ).bind(await sha256Hex(token), userId, nextPath, now, now + ttl, purpose).run();
  return `${siteOrigin(env, request)}/api/auth/verify?token=${token}`;
}

// Mail budget: 3 per 15 min per (address, requesting network /24) — so a
// stranger cannot use up the owner's budget from elsewhere — plus a loose
// 20-a-day cap per address against mail-bombing. Over budget, callers skip
// sending silently (the response never changes).
export async function mailBudgetOk(env, email, request) {
  const short = await hit(env, await pairKey(env, 'mail-15m', email, request), 15 * 60 * 1000);
  const day = await hit(env, await emailKey(env, 'mail-day', email), 24 * 60 * 60 * 1000);
  return short <= 3 && day <= 20;
}

// --- Cleanup without cron --------------------------------------------------
// Pages has no cron triggers. At most every 6 hours, one request claims the
// slot atomically and, after responding, removes: unconfirmed accounts older
// than 14 days (unless a live confirm link is out), expired tokens, sessions
// and challenges, and day-old rate-limit counters.
export async function maybeCleanup(env, waitUntil) {
  const now = Date.now();
  await env.DB.prepare('INSERT OR IGNORE INTO meta (key, value) VALUES (\'last_cleanup\', 0)').run();
  const claimed = await env.DB.prepare(
    "UPDATE meta SET value = ?1 WHERE key = 'last_cleanup' AND value < ?2 RETURNING value"
  ).bind(now, now - 6 * 60 * 60 * 1000).first();
  if (!claimed) return;
  const stale = `SELECT id FROM users WHERE email_verified_at IS NULL AND created_at < ?1
                   AND NOT EXISTS (SELECT 1 FROM login_tokens t WHERE t.user_id = users.id
                                     AND t.purpose = 'verify' AND t.expires_at > ?2)`;
  const cutoff = now - UNVERIFIED_TTL_MS;
  const work = env.DB.batch([
    env.DB.prepare(`DELETE FROM positions WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM marks WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM sessions WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM credentials WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM webauthn_challenges WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM login_tokens WHERE user_id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare(`DELETE FROM users WHERE id IN (${stale})`).bind(cutoff, now),
    env.DB.prepare('DELETE FROM login_tokens WHERE expires_at < ?').bind(now),
    env.DB.prepare('DELETE FROM sessions WHERE expires_at < ?').bind(now),
    env.DB.prepare('DELETE FROM webauthn_challenges WHERE expires_at < ?').bind(now),
    env.DB.prepare('DELETE FROM auth_attempts WHERE window_start < ?').bind(now - 24 * 60 * 60 * 1000),
  ]).catch(e => console.error('cleanup failed', e && e.message));
  if (waitUntil) waitUntil(work); else await work;
}

// Passkeys stay switched off until the domain move (a passkey is bound to
// the domain it was created on). PASSKEYS_ENABLED="1" turns them on.
export function passkeysOn(env) { return env.PASSKEYS_ENABLED === '1'; }

// Parse a small JSON object body; anything else (null, arrays, numbers,
// oversized, malformed) is null.
export async function readBody(request, max = 2048) {
  try {
    const v = JSON.parse((await request.text()).slice(0, max));
    return v && typeof v === 'object' && !Array.isArray(v) ? v : null;
  } catch { return null; }
}

export function isValidEmail(email) {
  return typeof email === 'string'
    && email.length <= 254
    && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}

// A next-path must be a same-origin absolute path like "/part-2#ch5".
// Parsed with the WHATWG URL parser (the one the browser will apply to the
// Location header), so "/\evil.com" and tab/newline tricks — which a regex
// passes but the parser resolves off-site — are rejected. Returns the
// normalised path or null.
const NEXT_BASE = 'https://next.invalid';
export function safeNextPath(p) {
  if (typeof p !== 'string' || p.length > 200 || p[0] !== '/') return null;
  if (/[\u0000-\u001f\u007f\\]/.test(p)) return null;
  let u;
  try { u = new URL(p, NEXT_BASE); } catch { return null; }
  if (u.origin !== NEXT_BASE) return null;
  const out = u.pathname + u.search + u.hash;
  // Normalising can itself produce "//host" (e.g. "/..//evil.com").
  return out.startsWith('//') ? null : out;
}
