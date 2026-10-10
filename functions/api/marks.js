// /api/marks — the reader's coloured section marks (Pass 25, ledger §4y).
//
// Off until the owner approves the privacy copy: while MARKS_SYNC != "1"
// (wrangler.toml) every method answers 404 {error:'disabled'}, checked before
// anything else so a signed-out probe learns nothing new.
//
// GET  ?since=<v> → { owner, cursor, rows:[{part,a,c,x,t,v}], more? }
//        rows changed after version `since`, oldest first. `cursor` is the
//        version to send next time; `more: true` means call again from it.
//        `owner` is the first 16 hex of SHA-256(user id): lets the client
//        tell accounts apart on a shared device without holding the id.
// POST {v:1, ops:[{part,a,c}]} → { ok, rows:[the applied rows as stored] }
//        c 1..5 sets the colour slot, c 0 removes (writes a tombstone x = 1,
//        keeping the last colour, so other devices remove it too; removing a
//        section the server never held writes nothing and returns no row). 1..50 ops,
//        8 KB; the last op for a section wins. All or nothing (one batch).
//
// The server owns both clocks. t = max(now, old t + 1): when the mark last
// changed, server time, never the client's. v = per-user version, strictly
// increasing: max(now, the user's highest v + 1) inside the same statement,
// so two writes in one millisecond get distinct versions and the cursor can
// never skip a row. (Floored at server time rather than a plain +1 so a
// version is never handed out twice after the purge below removes a user's
// newest row.)
//
// Every POST, and a GET at most once an hour, first purges up to 100
// tombstones older than 180 days (Pages has no cron; the privacy notice
// promises the erasure). Marks may name only the book's own sections
// (_sections.js, generated with sections.json), so a reader holds at most
// 116 rows, live or removed.
'use strict';

import { json, getSession, sameOrigin, sha256Hex } from './_lib.js';
import { SECTIONS } from './_sections.js';

const PART_RE = /^part-[1-5]$/;
const SECTION_RE = /^ch[0-9B][A-Za-z0-9-]{0,95}$/;
const MAX_BYTES = 8192;
const MAX_OPS = 50;
const MARK_LIMIT = 250;                       // live marks per reader (the book has 116 sections)
const TOMBSTONE_TTL_MS = 180 * 24 * 60 * 60 * 1000;  // 180 days
const PURGE_BATCH = 100;
const PAGE = 500;                                    // rows per GET
const PURGE_EVERY_MS = 60 * 60 * 1000;               // GET-side purge cadence

function enabled(env) { return env.MARKS_SYNC === '1'; }

function purge(env, now) {
  return env.DB.prepare(
    `DELETE FROM marks WHERE rowid IN
       (SELECT rowid FROM marks WHERE x = 1 AND t < ? LIMIT ${PURGE_BATCH})`
  ).bind(now - TOMBSTONE_TTL_MS);
}

async function ownerTag(userId) { return (await sha256Hex(userId)).slice(0, 16); }

export async function onRequest({ request, env }) {
  if (!enabled(env)) return json({ error: 'disabled' }, 404);
  if (request.method === 'GET') return list(request, env);
  if (request.method === 'POST') return save(request, env);
  return json({ error: 'method_not_allowed' }, 405, { Allow: 'GET, POST' });
}

async function list(request, env) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  const p = new URL(request.url).searchParams.get('since');
  let since = /^\d{1,16}$/.test(p || '') ? Number(p) : 0;
  if (!Number.isSafeInteger(since)) since = 0;

  const uid = session.userId;
  // Reads stay reads: a GET purges at most once an hour (POSTs always purge).
  const now = Date.now();
  const last = await env.DB.prepare("SELECT value FROM meta WHERE key = 'marks_purge'").first();
  const due = !last || now - last.value > PURGE_EVERY_MS;
  const head = due
    ? [purge(env, now), env.DB.prepare(
        "INSERT INTO meta (key, value) VALUES ('marks_purge', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value"
      ).bind(now)]
    : [];
  const res = await env.DB.batch([
    ...head,
    env.DB.prepare(
      `SELECT part, a, c, x, t, v FROM marks WHERE user_id = ? AND v > ? ORDER BY v LIMIT ${PAGE + 1}`
    ).bind(uid, since),
    env.DB.prepare('SELECT MAX(v) AS v FROM marks WHERE user_id = ?').bind(uid),
  ]);
  const [page, top] = res.slice(head.length);

  let rows = page.results || [];
  const more = rows.length > PAGE;
  let cursor;
  if (more) {
    rows = rows.slice(0, PAGE);
    cursor = rows[rows.length - 1].v;
  } else {
    const max = top.results && top.results[0] ? top.results[0].v : null;
    cursor = max == null ? since : max;
  }
  const out = { owner: await ownerTag(uid), cursor, rows };
  if (more) out.more = true;
  return json(out);
}

async function save(request, env) {
  if (!sameOrigin(request)) return json({ error: 'bad_origin' }, 403);

  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);

  const raw = await request.text();
  if (new TextEncoder().encode(raw).length > MAX_BYTES) return json({ error: 'too_large' }, 413);
  let body;
  try { body = JSON.parse(raw); } catch { return json({ error: 'bad_request' }, 400); }
  if (!body || typeof body !== 'object' || Array.isArray(body)) return json({ error: 'bad_request' }, 400);
  if (body.v !== 1) return json({ error: 'bad_version' }, 400);
  if (!Array.isArray(body.ops) || body.ops.length < 1 || body.ops.length > MAX_OPS) {
    return json({ error: 'bad_ops' }, 400);
  }

  // Validate, then dedupe by section keeping the last op (re-inserted so the
  // batch order follows the last occurrence).
  const ops = new Map();
  for (const op of body.ops) {
    if (!op || typeof op !== 'object'
        || typeof op.part !== 'string' || !PART_RE.test(op.part)
        || typeof op.a !== 'string' || !SECTION_RE.test(op.a)
        || !Number.isInteger(op.c) || op.c < 0 || op.c > 5
        || !SECTIONS.has(op.part + '|' + op.a)) {      // only the book's own sections: at most 116 rows a reader
      return json({ error: 'bad_op' }, 400);
    }
    const key = op.part + '|' + op.a;
    ops.delete(key);
    ops.set(key, { part: op.part, a: op.a, c: op.c });
  }

  const uid = session.userId;
  const now = Date.now();

  // Limit (spec §6): refuse a batch that would leave more than MARK_LIMIT
  // live marks and adds to the count. Checked here for the answer, and again
  // inside the batch (the guard below) so parallel requests cannot slip past.
  const live = await env.DB.prepare('SELECT part, a FROM marks WHERE user_id = ? AND x = 0')
    .bind(uid).all();
  const set = new Set((live.results || []).map(r => r.part + '|' + r.a));
  const before = set.size;
  for (const [key, op] of ops) { if (op.c > 0) set.add(key); else set.delete(key); }
  if (set.size > MARK_LIMIT && set.size > before) {
    return json({ error: 'mark_limit', limit: MARK_LIMIT }, 409);
  }

  const nextV = '(SELECT MAX(?5, COALESCE(MAX(v), 0) + 1) FROM marks WHERE user_id = ?1)';
  const stmts = [purge(env, now)];
  for (const op of ops.values()) {
    stmts.push(op.c > 0
      ? env.DB.prepare(
          `INSERT INTO marks (user_id, part, a, c, x, t, v) VALUES (?1, ?2, ?3, ?4, 0, ?5, ${nextV})
           ON CONFLICT(user_id, part, a) DO UPDATE SET
             c = excluded.c, x = 0, t = MAX(excluded.t, marks.t + 1), v = excluded.v
           RETURNING part, a, c, x, t, v`
        ).bind(uid, op.part, op.a, op.c, now)
      : env.DB.prepare(
          // A removal only ever turns an existing row into a tombstone: an id
          // the server never held writes nothing (no unbounded tombstones).
          `UPDATE marks SET x = 1, t = MAX(?5, t + 1), v = ${nextV}
            WHERE user_id = ?1 AND part = ?2 AND a = ?3 AND x = 0
           RETURNING part, a, c, x, t, v`
        ).bind(uid, op.part, op.a, 0, now));
  }
  // Atomic limit guard: if the batch left the reader over the limit (and
  // above where they started), this insert violates NOT NULL and the whole
  // batch rolls back.
  stmts.push(env.DB.prepare(
    `INSERT INTO marks (user_id, part, a, c, x, t, v)
     SELECT NULL, NULL, NULL, NULL, 0, 0, 0
      WHERE (SELECT COUNT(*) FROM marks WHERE user_id = ?1 AND x = 0) > MAX(?2, ?3)`
  ).bind(uid, MARK_LIMIT, before));

  let results;
  try {
    results = await env.DB.batch(stmts);
  } catch (e) {
    if (/NOT NULL/i.test(String(e && e.message))) return json({ error: 'mark_limit', limit: MARK_LIMIT }, 409);
    throw e;
  }
  const rows = results.slice(1, -1).map(r => r.results && r.results[0]).filter(Boolean);
  return json({ ok: true, rows });
}
