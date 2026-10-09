// Host guard for every /api/* route. The same Functions are also reachable
// on the *.pages.dev aliases, which skip the zone's protections and — for
// preview branches — share the production database. When SITE_ORIGIN is
// configured, API requests for any other host (except local development)
// get a 404.
'use strict';

export async function onRequest(context) {
  const { request, env, next } = context;
  if (env.SITE_ORIGIN) {
    const host = new URL(request.url).hostname;
    const site = new URL(env.SITE_ORIGIN).hostname;
    if (host !== site && host !== 'localhost' && host !== '127.0.0.1') {
      return new Response('Not found', { status: 404 });
    }
  }
  return next();
}
