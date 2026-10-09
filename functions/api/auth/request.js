// POST /api/auth/request — the v1 magic-link route, kept only for browsers
// holding a cached copy of the old account page (retire after 2026-11-15:
// replace the body with a 410). A known address gets a recovery link, an
// unknown one the signup flow. It no longer creates a confirmed account.
'use strict';

import { mailRoute } from './_mailroute.js';
import { findUser, signupMail, recoverMail } from './_account.js';

export const onRequestPost = context => mailRoute(context, async (env, request, email, nextPath) =>
  (await findUser(env, email)) ? recoverMail(env, request, email, nextPath) : signupMail(env, request, email, nextPath));
