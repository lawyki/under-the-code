// Host guard for every /api/* route. The same Functions are also reachable
// on the *.pages.dev aliases, which skip the zone's protections and — for
// preview branches — share the production database. When SITE_ORIGIN is
// configured, API requests for any other host (except local development)
// get a 404.
'use strict';

export async function onRequest(context) {
  const { request, env, next } = context;
  const host = new URL(request.url).hostname;
  const local = host === 'localhost' || host === '127.0.0.1';
  // Fail closed: without SITE_ORIGIN only local development is served.
  const site = env.SITE_ORIGIN ? new URL(env.SITE_ORIGIN).hostname : null;
  if (!local && host !== site) return new Response('Not found', { status: 404 });
  return next();
}
