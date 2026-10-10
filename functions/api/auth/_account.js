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
  if (!(await mailBudgetOk(env, email, request))) return null;
  if (!user.verifiedAt) {
    // Token work happens inside the job (after the response), so every
    // branch answers after the same work.
    const make = async () => {
      await env.DB.prepare("DELETE FROM login_tokens WHERE user_id = ? AND purpose = 'verify'").bind(user.id).run();
      return issueToken(env, request, user.id, 'verify', nextPath);
    };
    return mailJob(make, link => ({
      to: email, subject: 'Confirm your email · Under the Code',
      ...mailBody({
        lead: 'Confirm your email to finish creating your Under the Code account.',
        linkText: 'Confirm my email →', link,
        note: 'The link works once, for 24 hours. If you didn’t ask for this, ignore it: an unconfirmed account is removed after 14 days.',
      }),
    }), env);
  }
  const { text, html } = mailBody({
    lead: 'Someone (hopefully you) tried to create an Under the Code account with this address. You already have one.',
    linkText: 'Sign in →', link: `${siteOrigin(env, request)}/account`,
    note: 'Forgot how you sign in? On that page choose “Email me a sign-in link”. If this wasn’t you, nothing has changed.',
  });
  return { link: null, make: null, send: () => sendMail(env, { to: email, subject: 'You already have an account · Under the Code', text, html }) };
}

// A mail job whose token is created inside send(). For local development the
// route awaits make() to echo the link; in production it all runs after the response.
function mailJob(make, compose, env) {
  let made = null;
  const ensure = () => (made = made || make());
  return {
    make: ensure,
    send: async () => sendMail(env, compose(await ensure())),
  };
}

// Recovery: a sign-in link (30 min) for a known address; nothing for an
// unknown one. Confirms the address too (clicking proves inbox control).
export async function recoverMail(env, request, email, nextPath) {
  // Budget first for every address, so known and unknown cost the same work;
  // the token itself is written inside the job, after the response.
  const budget = await mailBudgetOk(env, email, request);
  const user = await findUser(env, email);
  if (!user || !budget) return null;
  return mailJob(() => issueToken(env, request, user.id, 'recover', nextPath), link => ({
    to: email, subject: 'Your sign-in link · Under the Code',
    ...mailBody({
      lead: 'Your sign-in link for Under the Code.',
      linkText: 'Sign in →', link,
      note: 'It works once and expires in 30 minutes. Once in, you can set a password. If you didn’t ask for this, ignore it. Nothing happens without the link.',
    }),
  }), env);
}

// Notice after any change to how an account signs in.
export function changeNotice(env, request, email, what) {
  const { text, html } = mailBody({
    lead: `${what} on your Under the Code account.`,
    linkText: 'Review your account →', link: `${siteOrigin(env, request)}/account`,
    note: 'If this was you, there’s nothing to do. If it wasn’t, open the account page, choose “Email me a sign-in link”, and change how you sign in.',
  });
  return sendMail(env, { to: email, subject: 'Your sign-in settings changed · Under the Code', text, html });
}
