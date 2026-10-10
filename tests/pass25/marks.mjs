// Pass 25 section marks: dot + menu, painting (dot / chapter tab / rail),
// localStorage, sync through the fake /api/marks shared by two contexts,
// tombstones, server-t last-write-wins, the 250 limit, H11 (no resurrection),
// H12 (owner gating), menu keyboard, the place-bar path, account "Your marks".
//
//   node marks.mjs [--browser=webkit] [--only=<regex>]
import {
  reporter, withServer, launch, browsersFor, newContext, openPart, setSignedIn, watch, settle,
  progressRecord, marksLS, FakeApi, waitState, INSTRUMENT, BASE, C0, openPlaceBar, placeAction, snap, PLACE_LABELS,
} from './lib.mjs';

const R = reporter('marks');
const SEC = 'ch1-kernel', KEY = 'part-1|' + SEC;

async function open(ctx, opts = {}) {
  return openPart(ctx, 'part-1', { hash: C0.anchor, seedProgress: opts.noSeed ? undefined : progressRecord('part-1', C0.anchor, 0), seedMarks: opts.seedMarks, waitReading: true });
}
async function reopen(page) { await page.reload({ waitUntil: 'load' }); await settle(page, 1500); try { await waitState(page, ['READING', 'PINNED', 'EXCURSION'], 6000); } catch {} }
const dot = (sec = SEC) => `#${sec} .section-number > .mark-dot`;
async function openMenu(page, sec = SEC) {
  // Centre the heading first: the sticky navs would cover a dot scrolled to the top.
  await page.evaluate(sel => document.querySelector(sel).parentElement.scrollIntoView({ block: 'center', behavior: 'instant' }), dot(sec));
  await settle(page, 250);
  // force: the unmarked dot pulses (livePulse), which Playwright reads as "not stable".
  await page.locator(dot(sec)).click({ force: true });
  await page.locator('#utc-markmenu').waitFor({ state: 'visible', timeout: 3000 });
}
async function chooseSlot(page, i, sec = SEC) {
  await openMenu(page, sec);
  const items = page.locator('#utc-markmenu [role=menuitemradio]');
  await items.nth(i).click();
  await settle(page, 300);
}
async function painted(page, sec = SEC) {
  return page.evaluate(sec => {
    const d = document.querySelector(`#${sec} .section-number > .mark-dot`);
    const tab = document.querySelector(`.chapter-nav a.nav-item[href="#${sec}"]`);
    const tick = document.querySelector(`.rail-tick[data-target="${sec}"]`) || document.querySelector(`.rail-tick[href="#${sec}"]`);
    const c = el => (el && el.classList.contains('is-marked') ? el.dataset.c || '?' : null);
    return { dot: c(d), tab: c(tab), rail: c(tick), railExists: !!tick };
  }, sec);
}
async function waitPost(fake, from, pred = () => true, ms = 5000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    const hit = fake.calls.slice(from).find(c => c.method === 'POST' && c.path === '/api/marks' && pred(c));
    if (hit) return hit;
    await new Promise(r => setTimeout(r, 100));
  }
  return null;
}
const opsOf = c => (c && c.body && Array.isArray(c.body.ops) ? c.body.ops : []);

const TESTS = [];
const test = (name, fn) => TESTS.push({ name, fn });

test('signed out: dot + menu paints dot/tab/rail, writes localStorage, zero /api', async (t, b) => {
  const { ctx, net } = await newContext(b, { initScripts: [INSTRUMENT] });
  try {
    const page = await open(ctx);
    await openMenu(page);
    const items = await page.locator('#utc-markmenu [role=menuitemradio]').allTextContents();
    t.eq(items.length, 6, 'menu has None + 5 colours', items.join(' | '));
    t.check(/^\s*None\s*$/.test(items[0] || ''), 'first item is "None"', items[0]);
    t.check((await page.locator('#utc-markmenu', { hasText: 'Set my place here' }).count()) === 1, '"Set my place here" in the menu');
    await page.locator('#utc-markmenu [role=menuitemradio]').nth(1).click(); await settle(page, 400);
    const p = await painted(page);
    t.eq(p.dot, '1', 'dot painted data-c=1');
    t.eq(p.tab, '1', 'chapter tab painted data-c=1');
    t.check(p.railExists ? p.rail === '1' : false, 'rail tick painted data-c=1', JSON.stringify(p));
    const ls = await marksLS(page);
    t.check(ls && ls.v === 1 && ls.m && ls.m[KEY] && ls.m[KEY].c === 1, 'localStorage marks m["part-1|ch1-kernel"].c = 1', JSON.stringify(ls && ls.m && ls.m[KEY]));
    await reopen(page);
    t.eq((await painted(page)).dot, '1', 'mark survives reload');
    t.eq(net.api.length, 0, 'zero /api requests', net.api.map(a => a.method + ' ' + a.path).join(', '));
    t.check(page.__errors.length === 0, 'no console errors', page.__errors.join(' | '));
  } finally { await ctx.close(); }
});

test('signed in: POST /api/marks carries the op; second device sees it after reload; remove propagates as tombstone', async (t, b) => {
  const fake = new FakeApi();
  const A = await newContext(b, { fake, initScripts: [INSTRUMENT] });
  const B = await newContext(b, { fake, initScripts: [INSTRUMENT] });
  try {
    const pa = await open(A.ctx);
    const pb = await open(B.ctx);
    for (let i = 0; i < 30 && fake.callsTo('GET', '/api/marks').length < 2; i++) await settle(pa, 100);
    t.check(fake.callsTo('GET', '/api/marks').length >= 2, 'both devices GET /api/marks on load', fake.calls.map(c => c.method + ' ' + c.path + c.query).join(', '));
    const n = fake.calls.length;
    await chooseSlot(pa, 3);
    const post = await waitPost(fake, n);
    t.check(post && opsOf(post).some(o => o.part === 'part-1' && o.a === SEC && o.c === 3) && post.body.v === 1, 'POST {v:1, ops:[{part,a,c:3}]}', JSON.stringify(post && post.body));
    t.check(fake.marks.get(KEY) && fake.marks.get(KEY).c === 3, 'server row c=3');
    await settle(pa, 500);
    const la = await marksLS(pa);
    t.check(la && la.m[KEY] && la.m[KEY].s === 1 && la.owner === fake.owner, 'A: local mark synced (s=1) and owner stored', JSON.stringify(la && { owner: la.owner, m: la.m[KEY] }));
    await reopen(pb);
    t.eq((await painted(pb)).dot, '3', 'B shows the mark after reload');
    // remove on A
    const n2 = fake.calls.length;
    await chooseSlot(pa, 0);
    const post2 = await waitPost(fake, n2);
    t.check(post2 && opsOf(post2).some(o => o.a === SEC && o.c === 0), 'remove sends c:0', JSON.stringify(post2 && post2.body));
    t.check(fake.marks.get(KEY) && fake.marks.get(KEY).x === 1, 'server tombstone x=1');
    t.eq((await painted(pa)).dot, null, 'A dot cleared');
    await reopen(pb);
    t.eq((await painted(pb)).dot, null, 'B: mark gone after reload (tombstone propagated)');
    const lb = await marksLS(pb);
    t.check(!lb || !lb.m[KEY] || lb.m[KEY].x === 1, 'B: local copy is a tombstone or gone', JSON.stringify(lb && lb.m[KEY]));
    t.check(pa.__errors.length + pb.__errors.length === 0, 'no console errors', pa.__errors.concat(pb.__errors).join(' | '));
  } finally { await A.ctx.close(); await B.ctx.close(); }
});

test('last write wins by server t (later device write wins on both)', async (t, b) => {
  const fake = new FakeApi();
  const A = await newContext(b, { fake });
  const B = await newContext(b, { fake });
  try {
    const pa = await open(A.ctx), pb = await open(B.ctx);
    let n = fake.calls.length;
    await chooseSlot(pa, 2); await waitPost(fake, n);
    const tA = fake.marks.get(KEY).t;
    n = fake.calls.length;
    await chooseSlot(pb, 5); await waitPost(fake, n);
    const rowB = fake.marks.get(KEY);
    t.check(rowB.c === 5 && rowB.t > tA, 'server t strictly increases (t = max(now, old.t+1))', tA + ' -> ' + rowB.t);
    await reopen(pa); await reopen(pb);
    t.eq((await painted(pa)).dot, '5', 'A converges on the later write');
    t.eq((await painted(pb)).dot, '5', 'B keeps the later write');
    const la = await marksLS(pa);
    t.check(la && la.m[KEY] && la.m[KEY].t === rowB.t, 'A adopted the server t', JSON.stringify(la && la.m[KEY]));
  } finally { await A.ctx.close(); await B.ctx.close(); }
});

test('mark 251 is refused (server 409 mark_limit or local cap) and announced once', async (t, b) => {
  const fake = new FakeApi();
  for (let i = 0; i < 250; i++) fake.seedMark('part-5', 'ch99-fake-' + i, 1 + (i % 5));
  const { ctx } = await newContext(b, { fake, initScripts: [INSTRUMENT] });
  try {
    const page = await open(ctx);
    for (let i = 0; i < 50; i++) { const ls = await marksLS(page); if (ls && ls.m && Object.keys(ls.m).length >= 250) break; await settle(page, 100); }
    const n = fake.calls.length;
    await chooseSlot(page, 1);
    await waitPost(fake, n, () => true, 2500);
    await settle(page, 400);
    await chooseSlot(page, 2, 'ch1-memory');
    await waitPost(fake, n + 1, () => true, 2500);
    await settle(page, 800);
    const posts = fake.calls.slice(n).filter(c => c.method === 'POST' && c.path === '/api/marks');
    t.info('path', posts.length ? 'server: ' + posts.map(c => c.status).join(',') : 'refused locally (no POST)');
    t.check(fake.liveCount() <= 250, 'server never exceeds 250 live marks', String(fake.liveCount()));
    const live = await page.evaluate(() => window.__live || []);
    const limitMsgs = live.filter(s => /limit|250|full|too many|maximum|remove one/i.test(s));
    t.check(limitMsgs.length >= 1, 'the limit is announced', JSON.stringify(live));
    t.eq(limitMsgs.length, 1, 'announced exactly once across two attempts', JSON.stringify(limitMsgs));
    const errs = page.__errors.filter(e => !/Failed to load resource/.test(e));
    t.check(errs.length === 0, 'no script errors', errs.join(' | '));
  } finally { await ctx.close(); }
});

test('H11: removing a synced mark while signed out leaves a tombstone that wins on sign-in', async (t, b) => {
  const fake = new FakeApi();
  const { ctx, net } = await newContext(b, { fake });
  try {
    const page = await open(ctx);
    let n = fake.calls.length;
    await chooseSlot(page, 2); await waitPost(fake, n);
    await settle(page, 400);
    t.check(fake.marks.get(KEY) && fake.marks.get(KEY).c === 2 && !fake.marks.get(KEY).x, 'precondition: synced on the server');
    await setSignedIn(ctx, false);
    await reopen(page);
    const apiBefore = net.api.length;
    await chooseSlot(page, 0); await settle(page, 1500);
    t.eq(net.api.length - apiBefore, 0, 'signed out: zero /api while removing');
    const ls = await marksLS(page);
    t.check(ls && ls.m[KEY] && ls.m[KEY].x === 1, 'local tombstone kept (not deleted outright)', JSON.stringify(ls && ls.m[KEY]));
    await setSignedIn(ctx, true);
    n = fake.calls.length;
    await reopen(page);
    const post = await waitPost(fake, n, c => opsOf(c).some(o => o.a === SEC));
    t.check(post && opsOf(post).some(o => o.a === SEC && o.c === 0), 'sign-in uploads the removal (c:0)', JSON.stringify(post && post.body));
    t.check(fake.marks.get(KEY).x === 1, 'server row now a tombstone');
    await reopen(page);
    t.eq((await painted(page)).dot, null, 'mark does not resurrect');
  } finally { await ctx.close(); }
});

test('H12: marks owned by another account are not uploaded; anonymous ones are', async (t, b) => {
  const fake = new FakeApi({ owner: 'bbbbbbbbbbbbbbbb' });
  const A = 'aaaaaaaaaaaaaaaa';
  const seedMarks = { v: 1, owner: A, cursor: 0, m: {
    'part-1|ch1-context': { c: 2, t: 1000, s: 1, o: A },
    'part-1|ch1-transistor': { c: 4, t: 2000, s: 0, o: A },
    'part-1|ch1-cpu': { c: 5, t: 3000, s: 0, o: null },
  } };
  const { ctx } = await newContext(b, { fake });
  try {
    const page = await open(ctx, { seedMarks });
    await settle(page, 3000);
    const ops = fake.callsTo('POST', '/api/marks').flatMap(opsOf);
    t.check(ops.some(o => o.a === 'ch1-cpu' && o.c === 5), 'anonymous mark (o = null) uploaded', JSON.stringify(ops));
    t.check(!ops.some(o => o.a === 'ch1-context' || o.a === 'ch1-transistor'), "other account's marks not uploaded", JSON.stringify(ops));
  } finally { await ctx.close(); }
});

test('menu keyboard: arrows move focus only, Enter commits, Esc closes and returns focus', async (t, b) => {
  const { ctx } = await newContext(b);
  try {
    const page = await open(ctx);
    await openMenu(page);
    const inMenu = () => page.evaluate(() => { const a = document.activeElement; return a && a.closest('#utc-markmenu') ? (a.textContent || '').trim() : null; });
    const f0 = await inMenu();
    t.check(f0 !== null, 'focus moves into the menu on open', String(f0));
    const before = JSON.stringify(await marksLS(page));
    await page.keyboard.press('ArrowDown'); await settle(page, 200);
    const f1 = await inMenu();
    t.check(f1 !== null && f1 !== f0, 'ArrowDown moves focus', f0 + ' -> ' + f1);
    await page.keyboard.press('ArrowDown'); await settle(page, 200);
    t.eq(JSON.stringify(await marksLS(page)), before, 'arrows write nothing');
    t.eq((await painted(page)).dot, null, 'dot still unmarked');
    const focusedC = await page.evaluate(() => document.activeElement.dataset.c);
    await page.keyboard.press('Enter'); await settle(page, 400);
    t.eq((await painted(page)).dot, focusedC, 'Enter commits the focused colour');
    t.check(!(await page.locator('#utc-markmenu').isVisible()), 'menu closes after commit');
    await openMenu(page);
    await page.keyboard.press('Escape'); await settle(page, 300);
    t.check(!(await page.locator('#utc-markmenu').isVisible()), 'Esc closes the menu');
    const back = await page.evaluate(() => { const a = document.activeElement; return a ? (a.className || a.tagName) : null; });
    // Pointer-opened from a section dot (aria-hidden, not a tab stop): focus is
    // released, never parked on a hidden element (integrator ruling, ledger §4y).
    t.check(!/mark-menu|mm-item|mark-dot/.test(String(back)), 'pointer-opened menu: focus released, not left on a hidden dot', String(back));
    // Keyboard path: place button -> place bar -> Mark this section -> Esc returns there.
    await page.focus('.place-btn'); await page.keyboard.press('Enter'); await settle(page, 300);
    await page.focus('#utc-placebar .pb-mark'); await page.keyboard.press('Enter'); await settle(page, 300);
    t.check(await page.locator('#utc-markmenu').isVisible(), 'Mark this section opens the menu');
    await page.keyboard.press('Escape'); await settle(page, 300);
    const back2 = await page.evaluate(() => document.activeElement && document.activeElement.className);
    t.check(/pb-mark/.test(String(back2)), 'keyboard-opened menu: Esc returns focus to Mark this section', String(back2));
  } finally { await ctx.close(); }
});

test('keyboard path: place-btn -> place bar -> "Mark this section" marks the section holding K', async (t, b) => {
  const { ctx } = await newContext(b);
  try {
    const page = await open(ctx);
    await page.locator('.book-nav .place-btn').focus();
    await page.keyboard.press('Enter'); await settle(page, 300);
    t.check(await page.locator('#utc-placebar').isVisible(), 'Enter on place-btn opens the bar');
    const markBtn = page.locator('#utc-placebar button:visible', { hasText: PLACE_LABELS.mark }).first();
    await markBtn.focus(); await page.keyboard.press('Enter'); await settle(page, 300);
    t.check(await page.locator('#utc-markmenu').isVisible(), '"Mark this section" opens the mark menu');
    await page.keyboard.press('ArrowDown'); await page.keyboard.press('ArrowDown');
    const c = await page.evaluate(() => document.activeElement && document.activeElement.dataset.c);
    await page.keyboard.press('Enter'); await settle(page, 400);
    const s = await snap(page);
    const sec = await page.evaluate(k => { const e = document.getElementById(k); const s = e && e.closest('section.section'); return s && s.id; }, s.K);
    t.eq((await painted(page, sec)).dot, c, `section of K (${sec}) marked with the chosen colour`);
  } finally { await ctx.close(); }
});

test('account page lists "Your marks"', async (t, b) => {
  const fake = new FakeApi();
  fake.seedMark('part-1', SEC, 3);
  fake.seedMark('part-2', 'ch4-vm', 1);
  const { ctx } = await newContext(b, { fake });
  try {
    const page = watch(await ctx.newPage());
    await page.goto(BASE + '/account', { waitUntil: 'load' });
    await settle(page, 2000);
    const has = await page.getByText('Your marks').count();
    t.check(has > 0, '"Your marks" heading present');
    const hrefs = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')));
    t.check(hrefs.some(h => /part-1#ch1-kernel/.test(h)) && hrefs.some(h => /part-2#ch4-vm/.test(h)), 'each mark links to its section', hrefs.filter(h => /#ch/.test(h)).join(', '));
    t.check(page.__errors.length === 0, 'no console errors', page.__errors.join(' | '));
  } finally { await ctx.close(); }
});

async function run() {
  for (const bname of browsersFor(['chromium', 'webkit'])) {
    const browser = await launch(bname);
    try {
      for (const x of TESTS) await R.test(`${bname} ${x.name}`, t => x.fn(t, browser), { timeout: 120000 });
    } finally { await browser.close(); }
  }
}
await withServer(run);
process.exit(R.summary());
