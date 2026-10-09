// POST /api/auth/recover — { email, next? }. "Email me a sign-in link":
// forgotten password, lost passkey, or an account that never set either.
// Same answer whether or not the address has an account.
'use strict';

import { mailRoute } from './_mailroute.js';
import { recoverMail } from './_account.js';

export const onRequestPost = context => mailRoute(context, recoverMail);
