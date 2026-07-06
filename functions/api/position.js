// /api/position — the reader's single stored place in the book.
//
// GET  → { position: {…}, updated_at } or { position: null }.
// POST → save. The body is a whitelisted snapshot: part + anchor (a stable
//        element id baked into the HTML) + fractional offset within that
//        element, plus the human-readable labels the "continue from" offer
//        renders. sendBeacon delivers the final write on pagehide, so the
//        body may arrive with any Content-Type — parse it as JSON regardless.
'use strict';

import { json, getSession, sameOrigin } from './_lib.js';

const PART_RE = /^part-[1-5]$/;
const ANCHOR_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
const LABELS = ['section', 'chapterId', 'chapterNum', 'chapterTitle', 'sectionLabel', 'sectionTitle'];

export async function onRequestGet({ request, env }) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  const row = await env.DB.prepare(
    'SELECT data, updated_at FROM positions WHERE user_id = ?'
  ).bind(session.userId).first();
  if (!row) return json({ position: null });

  let position = null;
  try { position = JSON.parse(row.data); } catch { /* corrupt row: report empty */ }
  return json({ position, updated_at: row.updated_at });
}

export async function onRequestPost({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);

  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  const raw = await request.text();
  if (raw.length > 2048) return json({ error: 'too_large' }, 413);
  let body;
  try { body = JSON.parse(raw); } catch { return json({ error: 'bad_request' }, 400); }

  if (!PART_RE.test(body.part || '')) return json({ error: 'bad_part' }, 400);
  if (!ANCHOR_RE.test(body.anchor || '')) return json({ error: 'bad_anchor' }, 400);
  const fraction = Number(body.fraction);
  if (!Number.isFinite(fraction) || fraction < 0 || fraction > 3) {
    return json({ error: 'bad_fraction' }, 400);
  }

  const clean = { part: body.part, anchor: body.anchor, fraction: Math.round(fraction * 1000) / 1000 };
  for (const key of LABELS) {
    if (typeof body[key] === 'string' && body[key].length <= 200) clean[key] = body[key];
  }

  const now = Date.now();
  await env.DB.prepare(
    `INSERT INTO positions (user_id, data, updated_at) VALUES (?, ?, ?)
     ON CONFLICT(user_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at`
  ).bind(session.userId, JSON.stringify(clean), now).run();

  return json({ ok: true, updated_at: now });
}
