// POST /api/auth/signup — { email, next? }. Starts an account: the reader
// confirms the address by email first, and chooses a passkey or a password
// after. Same answer whether or not the address already has an account.
'use strict';

import { mailRoute } from './_mailroute.js';
import { signupMail } from './_account.js';

export const onRequestPost = context => mailRoute(context, signupMail);
