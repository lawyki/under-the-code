// POST /api/auth/request — start a magic-link sign-in.
// Body: { email, next? }. Creates the user on first sign-in (no separate
// registration), stores a hashed one-time token (15 min), and emails the
// link via the Cloudflare Email Sending REST API (the [[send_email]] binding
// is Workers-only — Pages configuration rejects it, so the Function calls
// the API directly with an EMAIL_API_TOKEN secret). The response is the
// same whether or not the address already had an account.
'use strict';

import {
  json, newToken, sha256Hex, sameOrigin, isValidEmail, safeNextPath, TOKEN_TTL_MS,
} from '../_lib.js';

const FROM = 'Under the Code <under@atheric.eu>';

function emailBody(link) {
  const text =
`Your sign-in link for Under the Code:

${link}

It works once and expires in 15 minutes. If you didn't request it,
ignore this mail — nothing happens without the link.

— under.atheric.eu`;
  const html =
`<div style="font-family:Georgia,serif;max-width:34em;margin:0 auto;padding:24px;color:#1a1614">
  <p style="font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:#8a6a2a;font-family:monospace">Under the Code</p>
  <p>Your sign-in link:</p>
  <p><a href="${link}" style="color:#8a6a2a">Continue reading — sign in</a></p>
  <p style="color:#7a7570;font-size:14px">It works once and expires in 15 minutes.
  If you didn't request it, ignore this mail — nothing happens without the link.</p>
  <p style="color:#7a7570;font-size:14px">— under.atheric.eu</p>
</div>`;
  return { text, html };
}

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);

  let body;
  try { body = await request.json(); } catch { return json({ error: 'bad_request' }, 400); }
  const email = String(body.email || '').trim().toLowerCase();
  if (!isValidEmail(email)) return json({ error: 'bad_email' }, 400);
  const nextPath = safeNextPath(body.next);

  const now = Date.now();

  // Throttle: at most 3 outstanding links per address per 15 minutes.
  const recent = await env.DB.prepare(
    `SELECT COUNT(*) AS n FROM login_tokens t JOIN users u ON u.id = t.user_id
      WHERE u.email = ? AND t.created_at > ?`
  ).bind(email, now - TOKEN_TTL_MS).first();
  if (recent && recent.n >= 3) return json({ error: 'slow_down' }, 429);

  let user = await env.DB.prepare('SELECT id FROM users WHERE email = ?').bind(email).first();
  if (!user) {
    user = { id: crypto.randomUUID() };
    await env.DB.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)')
      .bind(user.id, email, now).run();
  }

  const token = newToken();
  await env.DB.prepare(
    'INSERT INTO login_tokens (token_hash, user_id, next_path, created_at, expires_at) VALUES (?, ?, ?, ?, ?)'
  ).bind(await sha256Hex(token), user.id, nextPath, now, now + TOKEN_TTL_MS).run();

  const url = new URL(request.url);
  const link = `${url.origin}/api/auth/verify?token=${token}`;
  const isLocal = url.hostname === 'localhost' || url.hostname === '127.0.0.1';

  let sent = false;
  let sendError = null;
  if (env.EMAIL_API_TOKEN && env.CF_ACCOUNT_ID) {
    try {
      const { text, html } = emailBody(link);
      const res = await fetch(
        `https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/email/sending/send`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.EMAIL_API_TOKEN}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            to: email,
            from: FROM,
            subject: 'Your sign-in link — Under the Code',
            text,
            html,
          }),
        }
      );
      const out = await res.json().catch(() => null);
      sent = !!(res.ok && out && out.success);
      if (!sent) sendError = 'api ' + res.status + ' ' + JSON.stringify((out && out.errors) || []);
    } catch (e) {
      sendError = (e && e.message) || 'send_failed';
    }
  }

  // Local dev only: surface the link so the flow is testable without mail.
  if (isLocal) return json({ ok: true, sent, devLink: link });

  if (!sent) {
    console.error('magic-link delivery failed:', sendError || 'EMAIL binding missing');
    return json({ error: 'delivery_unavailable' }, 503);
  }
  return json({ ok: true });
}
