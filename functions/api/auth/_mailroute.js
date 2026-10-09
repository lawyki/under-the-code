// Common request handling for the three mail-sending routes.
'use strict';

import { json, strictOrigin, isValidEmail, safeNextPath, hit, ipKey, isLocal, maybeCleanup, readBody } from '../_lib.js';

export async function mailRoute(context, build) {
  const { request, env } = context;
  if (!strictOrigin(request, env)) return json({ error: 'bad_origin' }, 403);
  const body = await readBody(request);
  if (!body) return json({ error: 'bad_request' }, 400);
  const email = String(body.email || '').trim().toLowerCase();
  if (!isValidEmail(email)) return json({ error: 'bad_email' }, 400);
  const nextPath = safeNextPath(body.next);

  // Per-IP budget only (reveals nothing about any address).
  if (await hit(env, await ipKey(env, 'mail-ip', request), 60 * 60 * 1000) > 20) {
    return json({ error: 'slow_down' }, 429, { 'Retry-After': '900' });
  }

  const job = await build(env, request, email, nextPath);
  // Local development only: create the link now and echo it (no mail is sent).
  if (isLocal(request)) {
    const devLink = job ? (job.make ? await job.make() : job.link) : null;
    return json({ ok: true, devLink });
  }
  if (job) context.waitUntil(job.send());
  await maybeCleanup(env, p => context.waitUntil(p));
  return json({ ok: true });
}
