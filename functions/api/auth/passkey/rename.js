// POST /api/auth/passkey/rename — { id, name }.
'use strict';

import { json, getSession, strictOrigin } from '../../_lib.js';
import { disabled, readJson, cleanName } from './_wa.js';

export async function onRequestPost({ request, env }) {
  const off = disabled(env); if (off) return off;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  const body = await readJson(request);
  if (!body || typeof body.id !== 'string') return json({ error: 'bad_request' }, 400);
  const name = cleanName(body.name, '');
  if (!name) return json({ error: 'bad_name' }, 400);
  const res = await env.DB.prepare('UPDATE credentials SET name = ? WHERE id = ? AND user_id = ?')
    .bind(name, body.id, session.userId).run();
  return res.meta.changes ? json({ ok: true, name }) : json({ error: 'not_found' }, 404);
}
