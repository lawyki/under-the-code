// GET /api/auth/me — who am I? { email } or 401. The client only calls
// this when the under_signedin hint cookie is present, so signed-out
// readers never generate the request.
'use strict';

import { json, getSession } from '../_lib.js';

export async function onRequestGet({ request, env }) {
  const session = await getSession(request, env);
  if (!session) return json({ error: 'signed_out' }, 401);
  return json({ email: session.email });
}
