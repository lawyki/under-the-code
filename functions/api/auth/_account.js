// Shared account logic for signup / recover / the legacy request route.
// Every branch sends (or silently skips) mail inside waitUntil and returns
// the same answer at the same speed, so no response reveals whether an
// address has an account.
'use strict';

import {
  issueToken, sendMail, mailBody, mailBudgetOk, siteOrigin,
} from '../_lib.js';

export async function findUser(env, email) {
  return env.DB.prepare(
    'SELECT id, email_verified_at AS verifiedAt, password_hash AS passwordHash FROM users WHERE email = ?'
  ).bind(email).first();
}

// Create-or-find without racing: two concurrent signups for one address
// both succeed and get the same row.
export async function ensureUser(env, email) {
  await env.DB.prepare(
    'INSERT INTO users (id, email, created_at) VALUES (?, ?, ?) ON CONFLICT(email) DO NOTHING'
  ).bind(crypto.randomUUID(), email, Date.now()).run();
  return findUser(env, email);
}

// Signup: new or unconfirmed address → confirm link (24 h; earlier confirm
// links are cancelled). Already-confirmed address → a notice with no token
// ("you already have an account"), so signup can't burn the owner's
// recovery budget or be used to take anything over.
export async function signupMail(env, request, email, nextPath) {
  const user = await ensureUser(env, email);
  if (!user) return null;
  if (!(await mailBudgetOk(env, email))) return null;
  if (!user.verifiedAt) {
    await env.DB.prepare("DELETE FROM login_tokens WHERE user_id = ? AND purpose = 'verify'").bind(user.id).run();
    const link = await issueToken(env, request, user.id, 'verify', nextPath);
    const { text, html } = mailBody({
      lead: 'Confirm your email to finish creating your Under the Code account.',
      linkText: 'Confirm my email →', link,
      note: 'The link works once, for 24 hours. If you didn’t ask for this, ignore it — an unconfirmed account is removed after 14 days.',
    });
    return { link, send: () => sendMail(env, { to: email, subject: 'Confirm your email — Under the Code', text, html }) };
  }
  const { text, html } = mailBody({
    lead: 'Someone (hopefully you) tried to create an Under the Code account with this address — you already have one.',
    linkText: 'Sign in →', link: `${siteOrigin(env, request)}/account`,
    note: 'Forgot how you sign in? On that page choose “Email me a sign-in link”. If this wasn’t you, nothing has changed.',
  });
  return { link: null, send: () => sendMail(env, { to: email, subject: 'You already have an account — Under the Code', text, html }) };
}

// Recovery: a sign-in link (30 min) for a known address; nothing for an
// unknown one. Confirms the address too (clicking proves inbox control).
export async function recoverMail(env, request, email, nextPath) {
  // Budget first for every address, so known and unknown cost the same work.
  const budget = await mailBudgetOk(env, email);
  const user = await findUser(env, email);
  if (!user || !budget) return null;
  const link = await issueToken(env, request, user.id, 'recover', nextPath);
  const { text, html } = mailBody({
    lead: 'Your sign-in link for Under the Code.',
    linkText: 'Sign in →', link,
    note: 'It works once and expires in 30 minutes. Once in, you can set a password or create a passkey. If you didn’t ask for this, ignore it — nothing happens without the link.',
  });
  return { link, send: () => sendMail(env, { to: email, subject: 'Your sign-in link — Under the Code', text, html }) };
}

// Notice after any change to how an account signs in.
export function changeNotice(env, request, email, what) {
  const { text, html } = mailBody({
    lead: `${what} on your Under the Code account.`,
    linkText: 'Review your account →', link: `${siteOrigin(env, request)}/account`,
    note: 'If this was you, there’s nothing to do. If it wasn’t, open the account page, choose “Email me a sign-in link”, and change how you sign in.',
  });
  return sendMail(env, { to: email, subject: 'Your sign-in settings changed — Under the Code', text, html });
}
