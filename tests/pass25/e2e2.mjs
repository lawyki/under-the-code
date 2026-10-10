import { chromium } from 'playwright';
const B = 'http://localhost:8798', FLAG = process.argv[2];
const TA = 'tokenEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', TB = 'tokenFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', TC = 'tokenGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG';
let pass = 0, fail = 0; const ok = (c, n, d = '') => { c ? pass++ : fail++; console.log(c ? 'PASS' : 'FAIL', '[flag ' + FLAG + ']', n, c ? '' : d); };
const b = await chromium.launch();
const login = async (ctx, t) => ctx.addCookies([{ name: '__Host-under_session', value: t, domain: 'localhost', path: '/', secure: true, httpOnly: true, sameSite: 'Lax' }, { name: 'under_signedin', value: '1', domain: 'localhost', path: '/', secure: true, sameSite: 'Lax' }]);
const api = (t, path, opt = {}) => fetch(B + path, Object.assign({ headers: { Cookie: '__Host-under_session=' + t, Origin: B, 'Content-Type': 'application/json' } }, opt)).then(r => r.status === 204 ? {} : r.json());
// A. sign-out keeps marks that never reached the server
{ const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); await login(ctx, TA);
  const p = await ctx.newPage(); await p.goto(B + '/part-1#ch1-kernel'); await p.waitForTimeout(2500);
  await p.evaluate(() => document.querySelector('#ch1-kernel .mark-dot').click()); await p.waitForTimeout(300);
  await p.click('#utc-markmenu .mm-item[data-c="2"]'); await p.waitForTimeout(1800);
  const acc = await ctx.newPage(); await acc.goto(B + '/account'); await acc.waitForTimeout(1500);
  await acc.click('#acct-signout'); await acc.waitForTimeout(1500);
  const m = await acc.evaluate(() => JSON.parse(localStorage.getItem('under-the-code:marks') || '{}'));
  const e = m.m && m.m['part-1|ch1-kernel'];
  if (FLAG === '0') ok(e && !e.x && e.c === 2 && !e.o, 'sign-out keeps a mark the server never held', JSON.stringify(m));
  else ok(!e, 'sign-out forgets a mark the server holds (H12)', JSON.stringify(m));
  await ctx.close(); }
// B. Undo of a first-ever Set removes it from the server too
{ await api(TB, '/api/position', { method: 'DELETE' });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); await login(ctx, TB);
  const p = await ctx.newPage(); await p.goto(B + '/part-2'); await p.waitForTimeout(2500);
  await p.evaluate(() => document.querySelector('#ch4-anatomy').scrollIntoView()); await p.waitForTimeout(800);
  await p.click('.place-btn'); await p.waitForTimeout(300); await p.click('.pb-set'); await p.waitForTimeout(1200);
  const before = await api(TB, '/api/position');
  await p.click('.pb-undo'); await p.waitForTimeout(1200);
  const after = await api(TB, '/api/position');
  ok(before.position && after.position === null, 'Undo of a first Set clears the server place', JSON.stringify([before.position && before.position.anchor, after.position]));
  await ctx.close(); }
// C. a pin is not replaced by another device's tracked place
{ await api(TC, '/api/position', { method: 'DELETE' });
  const A = await b.newContext({ viewport: { width: 1440, height: 900 } }); await login(A, TC);
  const pa = await A.newPage(); await pa.goto(B + '/part-1?utc-debug#ch1-kernel-p3'); await pa.waitForTimeout(2500);
  await pa.click('.place-btn'); await pa.waitForTimeout(300); await pa.click('.pb-set'); await pa.waitForTimeout(1500);
  const pin = await pa.evaluate(() => __utcPlace.snapshot().C);
  await api(TC, '/api/position', { method: 'POST', body: JSON.stringify({ part: 'part-3', anchor: 'ch9-ip-p3', fraction: 0.2, src: 'auto' }) });
  await pa.reload(); await pa.waitForTimeout(3000);
  const s = await pa.evaluate(() => __utcPlace.snapshot());
  ok(s.C && s.C.anchor === pin.anchor && s.C.src === 'set', 'pin survives a newer tracked place from another device', JSON.stringify(s.C));
  ok(await pa.evaluate(() => !!document.querySelector('.sync-chip:not(.place-toast)')), 'the other device is offered as a chip');
  await A.close(); }
// D. a place left by another account is dropped, never uploaded into this one
{ await api(TB, '/api/position', { method: 'DELETE' }); await api(TC, '/api/position', { method: 'DELETE' });
  const A = await b.newContext({ viewport: { width: 1440, height: 900 } }); await login(A, TC);
  const pa = await A.newPage(); await pa.goto(B + '/part-1?utc-debug#ch1-cpu-p3'); await pa.waitForTimeout(2500);
  await pa.click('.place-btn'); await pa.waitForTimeout(300); await pa.click('.pb-set'); await pa.waitForTimeout(1500); await pa.keyboard.press('Escape');
  const owned = await pa.evaluate(() => JSON.parse(localStorage.getItem('under-the-code:progress')));
  await A.clearCookies(); await login(A, TB);   // session ends elsewhere; B signs in on this device
  await pa.reload(); await pa.waitForTimeout(3500);
  const posB = await api(TB, '/api/position');
  ok(owned && owned.own && !(posB.position && posB.position.anchor === owned.anchor), "another account's place is not uploaded", JSON.stringify([owned && owned.own, posB.position]));
  await A.close(); }
console.log('E2E2', pass, 'pass', fail, 'fail');
await b.close();
