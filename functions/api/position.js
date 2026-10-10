// /api/position — the reader's single stored place in the book.
//
// GET  → { position: {…}, updated_at, owner } or { position: null, owner }.
// DELETE → forget the stored place (204).
// POST → save. The body is a whitelisted snapshot: part + anchor (a stable
//        element id baked into the HTML) + fractional offset within that
//        element, plus the human-readable labels the "continue from" offer
//        renders. sendBeacon delivers the final write on pagehide, so the
//        body may arrive with any Content-Type — parse it as JSON regardless.
//
// Pass 25, only while MARKS_SYNC = "1" (wrangler.toml; until then the POST
// below is exactly the pre-25 one): optional fields join the snapshot.
//   src  'auto' | 'set'   — tracked by the book, or set by the reader (a pin).
//   k    the paragraph at the reader's attention line (the labels name it);
//   end  1 when the place is in the part's last section ("reading on").
//   cid  /^[a-z0-9]{8,16}$/, seq a non-negative integer — the writing tab's
//        id and its write counter. A write from the same cid with a seq no
//        newer than the stored one is stale (it arrived out of order) and is
//        refused with 409 {error:'stale', updated_at}; the check and the
//        write are one conditional upsert, so two racing POSTs cannot both
//        win. A different cid always overwrites (last arrival wins, as before).
'use strict';

import { json, getSession, sameOrigin, sha256Hex } from './_lib.js';

const PART_RE = /^part-[1-5]$/;
const ANCHOR_RE = /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/;
const LABELS = ['section', 'chapterId', 'chapterNum', 'chapterTitle', 'sectionLabel', 'sectionTitle'];
const CID_RE = /^[a-z0-9]{8,16}$/;

export async function onRequestGet({ request, env }) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  const row = await env.DB.prepare(
    'SELECT data, updated_at FROM positions WHERE user_id = ?'
  ).bind(session.userId).first();
  // owner: the first 16 hex of SHA-256(user id), the same tag /api/marks uses —
  // lets the client tell a place left by another account on a shared device.
  const owner = (await sha256Hex(session.userId)).slice(0, 16);
  if (!row) return json({ position: null, owner });

  let position = null;
  try { position = JSON.parse(row.data); } catch { /* corrupt row: report empty */ }
  return json({ position, updated_at: row.updated_at, owner });
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
  if (env.MARKS_SYNC === '1') return saveVersioned(env, session, body, clean, now);
  await env.DB.prepare(
    `INSERT INTO positions (user_id, data, updated_at) VALUES (?, ?, ?)
     ON CONFLICT(user_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at`
  ).bind(session.userId, JSON.stringify(clean), now).run();

  return json({ ok: true, updated_at: now });
}

// Pass 25 save: src/cid/seq whitelisted, out-of-order writes refused.
async function saveVersioned(env, session, body, clean, now) {
  if (body.src === 'auto' || body.src === 'set') clean.src = body.src;
  if (typeof body.k === 'string' && ANCHOR_RE.test(body.k)) clean.k = body.k;   // the paragraph the labels name
  if (body.end === 1) clean.end = 1;                                         // in the part's last section
  const versioned = typeof body.cid === 'string' && CID_RE.test(body.cid)
    && Number.isSafeInteger(body.seq) && body.seq >= 0;
  if (versioned) { clean.cid = body.cid; clean.seq = body.seq; }

  // The update applies unless the stored row carries the same cid with a seq
  // at or above this one. Rows without cid (older clients) never block.
  const res = await env.DB.prepare(
    `INSERT INTO positions (user_id, data, updated_at) VALUES (?1, ?2, ?3)
     ON CONFLICT(user_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at
      WHERE CASE WHEN ?4 = 0 OR NOT json_valid(positions.data) THEN 1
                 ELSE json_extract(positions.data, '$.cid') IS NOT ?5
                   OR COALESCE(json_extract(positions.data, '$.seq'), -1) < ?6 END`
  ).bind(session.userId, JSON.stringify(clean), now,
         versioned ? 1 : 0, versioned ? clean.cid : null, versioned ? clean.seq : 0).run();

  if (!res.meta || res.meta.changes === 0) {
    const row = await env.DB.prepare('SELECT updated_at FROM positions WHERE user_id = ?')
      .bind(session.userId).first();
    return json({ error: 'stale', updated_at: row ? row.updated_at : null }, 409);
  }
  return json(versioned ? { ok: true, updated_at: now, seq: clean.seq } : { ok: true, updated_at: now });
}

// DELETE → forget the stored place (Undo of a reader's first-ever "Set my
// place"; Pass 25). Nothing else is removed.
export async function onRequestDelete({ request, env }) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  await env.DB.prepare('DELETE FROM positions WHERE user_id = ?').bind(session.userId).run();
  return new Response(null, { status: 204, headers: { 'Cache-Control': 'no-store' } });
}
