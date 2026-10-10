// Pass 25 UI checks: hover strip (slow-hover gate, parked pointer, collapse),
// desktop drag (0 rect reads, Esc cancels, release sets), place bar at 375
// (44px targets, Esc, close on scroll), slider keys, forced colours, print,
// reduced-motion trace identity, readout clipping, sync shape (solid only
// after a 200; paused after 2 failures; 401 -> signed out, calls stop).
//
//   node ui.mjs [--browser=chromium] [--only=<regex>]
import {
  reporter, withServer, launch, browsersFor, newContext, openPart, startC0, snap, settle, wheel,
  waitState, progress, sameC, brief, geom, openPlaceBar, placeAction, FakeApi, INSTRUMENT, VIEWPORTS,
  progressRecord, traceWheel, traceFling, sourceHtml, C0,
} from './lib.mjs';

const R = reporter('ui');
const TESTS = [];
const test = (name, browsers, fn) => TESTS.push({ name, browsers, fn });
const BOTH = ['chromium', 'webkit'], CHR = ['chromium'];

async function cueHeight(page) {
  return page.evaluate(() => {
    const cue = document.querySelector('.book-nav .reading-cue');
    if (!cue) return null;
    // Painted height: elements that draw something (background), are not
    // the saved mark, and are not faded out (effective opacity).
    const eff = e => { let o = 1; for (let x = e; x && x !== cue.parentElement; x = x.parentElement) o *= +getComputedStyle(x).opacity; return o; };
    const paints = e => { const cs = getComputedStyle(e); return (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') || cs.backgroundImage !== 'none'; };
    const els = [cue, ...cue.querySelectorAll('*')].filter(e => !e.closest('.cue-mark, .cue-hit, .cue-ghost') && paints(e) && eff(e) > 0.05);
    return els.length ? Math.max(...els.map(e => e.getBoundingClientRect().height)) : 0;
  });
}
// Slow approach from below into the strip (< 0.5 px/ms), then small moves.
async function approach(page, x = 600) {
  let y = 300;
  await page.mouse.move(x, y);
  while (y > 44) { y = Math.max(44, y - 8); await page.mouse.move(x, y); await page.waitForTimeout(20); }
}
async function dwell(page, x = 600) { for (let i = 0; i < 6; i++) { await page.mouse.move(x + i, 44); await page.waitForTimeout(30); } }
async function slowHover(page, x = 600) { await approach(page, x); await dwell(page, x); }

test('hover strip: slow pointer widens to 8px after ~120 ms; collapses after leave', CHR, async (t, b) => {
  const { ctx, page } = await startC0(b, { clock: false });
  try {
    const h0 = await cueHeight(page);
    if (h0 === null) t.skipTest('no .reading-cue');
    t.check(h0 <= 2.5, 'at rest: 2px line', 'height ' + h0);
    await approach(page);
    const early = await cueHeight(page);           // within ~20 ms of entering the strip
    await dwell(page);
    await page.waitForTimeout(300);
    const h1 = await cueHeight(page);
    t.soft(early <= 3, 'not widened before the dwell', 'height ' + early + ' right after entering');
    t.check(h1 >= 7.5 && h1 <= 8.5, 'widened to 8px (scaleY 4)', 'height ' + h1);
    await page.mouse.move(600, 420);
    await page.waitForTimeout(120);
    t.soft((await cueHeight(page)) > 2.5, 'still open 120 ms after leaving');
    await page.waitForTimeout(600);
    t.check((await cueHeight(page)) <= 2.5, 'collapsed ~300 ms after leaving', 'height ' + (await cueHeight(page)));
  } finally { await ctx.close(); }
});

test('hover strip: fast or parked pointer does not open; scroll closes until the next move', CHR, async (t, b) => {
  const { ctx, page } = await startC0(b, { clock: false });
  try {
    if ((await cueHeight(page)) === null) t.skipTest('no .reading-cue');
    await page.mouse.move(100, 300);
    await page.mouse.move(1300, 44, { steps: 3 });     // fast sweep, ends parked in the strip
    await page.waitForTimeout(600);
    t.check((await cueHeight(page)) <= 2.5, 'fast sweep + parked: stays closed', 'height ' + (await cueHeight(page)));
    await slowHover(page);
    await page.waitForTimeout(400);
    t.check((await cueHeight(page)) >= 7.5, 'slow hover opens');
    await page.mouse.wheel(0, 200);
    await page.waitForTimeout(600);
    t.check((await cueHeight(page)) <= 2.5, 'wheel closes it', 'height ' + (await cueHeight(page)));
    await page.waitForTimeout(500);
    t.check((await cueHeight(page)) <= 2.5, 'stays closed while the pointer is parked');
  } finally { await ctx.close(); }
});

test('drag the mark (desktop): 0 rect reads during drag, Esc cancels, release sets the place', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { clock: false });
  try {
    const markBox = async () => page.evaluate(() => { const m = document.querySelector('.book-nav .cue-mark'); return m && m.getBoundingClientRect().toJSON(); });
    let mb = await markBox();
    if (!mb) t.skipTest('no .cue-mark');
    await slowHover(page, Math.round(mb.x + mb.width / 2));
    await page.waitForTimeout(400);
    mb = await markBox();
    const cx = mb.x + mb.width / 2, cy = mb.y + mb.height / 2;
    await page.mouse.move(cx, cy); await page.mouse.down();
    await page.evaluate(() => { window.__rectReads = 0; window.__countRects = true; });
    for (let i = 1; i <= 10; i++) { await page.mouse.move(cx + i * 20, cy); await page.waitForTimeout(20); }
    const reads = await page.evaluate(() => { window.__countRects = false; return window.__rectReads; });
    t.eq(reads, 0, '0 getBoundingClientRect calls during the drag');
    await page.keyboard.press('Escape'); await page.mouse.up(); await settle(page, 500);
    let s = await snap(page);
    t.check(sameC(s.C, s0.C) && s.writes === s0.writes, 'Esc cancels (C and writes unchanged)', brief(s.C) + ' writes ' + (s.writes - s0.writes));
    await slowHover(page, Math.round(cx)); await page.waitForTimeout(400);
    await page.mouse.move(cx, cy); await page.mouse.down();
    for (let i = 1; i <= 8; i++) { await page.mouse.move(cx + i * 20, cy); await page.waitForTimeout(20); }
    await page.mouse.up(); await settle(page, 700);
    s = await snap(page);
    t.check(!sameC(s.C, s0.C) && s.C.src === 'set', 'release sets the place (src set)', brief(s.C));
    t.eq(s.state, 'PINNED', 'state PINNED');
    t.eq(s.writes - s0.writes, 1, '1 write');
  } finally { await ctx.close(); }
});

for (const bn of BOTH) {
  test(`place bar at 375: opens, 44px targets, Esc returns focus, closes on scroll > 0.5B`, [bn], async (t, b) => {
    const { ctx, page } = await startC0(b, { viewport: VIEWPORTS.phone, hasTouch: true, isMobile: true, clock: false });
    try {
      const btn = page.locator('.book-nav .place-btn');
      if (!(await btn.count())) t.skipTest('no .place-btn');
      await btn.click(); await settle(page, 400);
      t.eq(await btn.getAttribute('aria-expanded'), 'true', 'aria-expanded=true');
      t.check(await page.locator('#utc-placebar').isVisible(), 'bar visible');
      const small = await page.evaluate(() => {
        const els = [document.querySelector('.book-nav .place-btn'),
          ...document.querySelectorAll('#utc-placebar button, #utc-placebar [role=slider], #utc-placebar a[href], #utc-placebar input')]
          .filter(e => e && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
        return els.map(e => { const r = e.getBoundingClientRect(); return { n: (e.textContent || e.className).trim().slice(0, 30), w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10 }; })
          .filter(x => x.w < 44 || x.h < 44);
      });
      t.check(small.length === 0, 'every control ≥ 44×44', JSON.stringify(small));
      await page.keyboard.press('Escape'); await settle(page, 300);
      t.check(!(await page.locator('#utc-placebar').isVisible()), 'Esc closes the bar');
      t.check(await page.evaluate(() => document.activeElement && document.activeElement.classList.contains('place-btn')), 'focus back on place-btn');
      await btn.click(); await settle(page, 400);
      const g = await geom(page);
      await page.evaluate(d => window.scrollBy({ top: d, behavior: 'instant' }), Math.round(0.5 * g.B + 40));
      await settle(page, 500);
      t.check(!(await page.locator('#utc-placebar').isVisible()), 'scroll > 0.5B closes the bar');
      // coarse-pointer hit area of a section dot (::after 44x44)
      const hit = await page.evaluate(() => {
        const d = document.querySelector('#ch1-kernel .section-number > .mark-dot');
        if (!d) return null;
        d.scrollIntoView({ block: 'center', behavior: 'instant' });
        const r = d.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        return [[0, 0], [-20, 0], [20, 0], [0, -20], [0, 20]].map(([dx, dy]) => {
          const e = document.elementFromPoint(cx + dx, cy + dy); return !!(e && e.closest('.mark-dot') === d);
        });
      });
      t.check(hit && hit.every(Boolean), 'section dot hit area ≥ 44×44 on touch', JSON.stringify(hit));
    } finally { await ctx.close(); }
  });
}

test('slider: ArrowRight/ArrowLeft move one paragraph without writing', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { viewport: VIEWPORTS.phone, hasTouch: true, clock: false });
  try {
    await openPlaceBar(page);
    const sl = page.locator('#utc-placebar [role=slider]').first();
    if (!(await sl.count())) t.skipTest('no [role=slider]');
    await sl.focus();
    const vt = () => sl.evaluate(e => e.getAttribute('aria-valuetext') || e.getAttribute('aria-valuenow'));
    const v0 = await vt();
    await page.keyboard.press('ArrowRight'); await settle(page, 300);
    const v1 = await vt();
    await page.keyboard.press('ArrowLeft'); await settle(page, 300);
    const v2 = await vt();
    t.check(v1 !== v0, 'ArrowRight changes the value', v0 + ' -> ' + v1);
    t.eq(v2, v0, 'ArrowLeft returns');
    const s = await snap(page);
    t.eq(s.writes - s0.writes, 0, 'no write while nudging');
  } finally { await ctx.close(); }
});

test('forced-colors emulation renders without errors', CHR, async (t, b) => {
  const { ctx } = await newContext(b, { forcedColors: 'active' });
  try {
    const page = await openPart(ctx, 'part-1', { hash: C0.anchor, seedProgress: progressRecord('part-1', C0.anchor, 0) });
    await settle(page, 800);
    try { await openPlaceBar(page); await page.keyboard.press('Escape'); } catch (e) { t.info('place bar', e.message); }
    const ok = await page.evaluate(() => matchMedia('(forced-colors: active)').matches);
    t.check(ok, 'forced-colors active');
    const h = await cueHeight(page);
    t.check(h === null ? false : h > 0, 'cue rendered', String(h));
    t.check(page.__errors.length === 0, 'no console errors', page.__errors.join(' | '));
  } finally { await ctx.close(); }
});

test('print emulation hides the cue and the place bar', BOTH, async (t, b) => {
  const { ctx, page } = await startC0(b, { clock: false });
  try {
    await page.emulateMedia({ media: 'print' });
    const r = await page.evaluate(() => ['.book-nav .reading-cue', '#utc-placebar', '#utc-markmenu', '.book-nav .place-btn'].map(s => {
      const e = document.querySelector(s); return { s, exists: !!e, shown: !!(e && e.getClientRects().length && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden') };
    }));
    const cue = r[0];
    if (!cue.exists) t.skipTest('no .reading-cue');
    t.check(r.every(x => !x.shown), 'cue / place bar / menu / place-btn not printed', JSON.stringify(r));
  } finally { await ctx.close(); }
});

test('reduced motion: identical trace results', CHR, async (t, b) => {
  const out = {};
  for (const rm of ['no-preference', 'reduce']) {
    const { ctx, page } = await startC0(b, { reducedMotion: rm });
    try { out[rm] = { wheel: await traceWheel(page) }; } finally { await ctx.close(); }
    const x = await startC0(b, { reducedMotion: rm });
    try { out[rm].fling = await traceFling(x.page); } finally { await x.ctx.close(); }
  }
  t.eq(out.reduce.wheel, out['no-preference'].wheel, 'wheel trace identical');
  t.eq(out.reduce.fling, out['no-preference'].fling, 'fling trace identical');
});

test('readout not clipped at 621 / 960 / 1100 / 1440', BOTH, async (t, b) => {
  const bridge = (sourceHtml('part-1').match(/<p id="(chBridge-[A-Za-z0-9-]+-p\d+)"/) || [])[1];
  for (const anchor of [C0.anchor, bridge].filter(Boolean)) {
    for (const width of [621, 960, 1100, 1440]) {
      const { ctx, page } = await startC0(b, { viewport: { width, height: 900 }, anchor, clock: false });
      try {
        await page.waitForTimeout(1200); await wheel(page, 120, 900);
        const r = await page.evaluate(() => { const e = document.querySelector('.book-nav .book-progress'); return e && { sw: e.scrollWidth, cw: e.clientWidth, text: e.textContent.trim() }; });
        t.check(r && r.sw <= r.cw + 0.5, `${width}px ${anchor.split('-')[0]}: .book-progress not clipped`, r && (r.sw + ' > ' + r.cw + ' "' + r.text + '"'));
        const sw = await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth);
        t.check(sw, `${width}px: no horizontal scroll`);
      } finally { await ctx.close(); }
    }
  }
});

test('sync shape: solid only after a 200; paused after 2 failures; 401 stops calls', BOTH, async (t, b) => {
  const fake = new FakeApi();
  const hg = fake.hold('GET', '/api/position');     // no 200 of any kind until the POST is released
  const h = fake.hold('POST', '/api/position');      // the first POST (load or set) is held
  const { ctx, page, net } = await startC0(b, { fake, clock: false });
  try {
    const synced = () => page.evaluate(() => { const m = document.querySelector('.book-nav .cue-mark'); return m ? m.classList.contains('is-synced') : null; });
    if ((await synced()) === null) t.skipTest('no .cue-mark');
    t.check(!(await synced()), 'hollow at load');
    let seen = await Promise.race([h.seen, page.waitForTimeout(3000).then(() => null)]);
    if (!seen) {
      await page.evaluate(() => window.scrollBy({ top: 900, behavior: 'instant' })); await settle(page, 400);
      await placeAction(page, 'set'); await page.keyboard.press('Escape');
      seen = await Promise.race([h.seen, page.waitForTimeout(6000).then(() => null)]);
    }
    t.check(!!seen, 'POST sent');
    t.check(!(await synced()), 'still hollow while the POST is pending');
    h.release(); await settle(page, 800);
    t.check(await synced(), 'solid after the 200');
    hg.release(); await settle(page, 300);
    // two consecutive failures -> paused
    fake.failNext('POST', '/api/position', 503, { error: 'unavailable' }, 2);
    for (let i = 0; i < 2; i++) {
      await page.evaluate(() => window.scrollBy({ top: 900, behavior: 'instant' })); await settle(page, 300);
      await placeAction(page, 'set'); await page.keyboard.press('Escape'); await settle(page, 2500);
    }
    let s = await snap(page);
    t.eq(s.sync, 'paused', 'sync paused after 2 consecutive failures');
    t.check(!(await synced()), 'mark not solid while paused');
    // 401
    fake.signedIn = false;
    await page.evaluate(() => window.scrollBy({ top: 900, behavior: 'instant' })); await settle(page, 300);
    await placeAction(page, 'set'); await page.keyboard.press('Escape'); await settle(page, 2500);
    s = await snap(page);
    t.eq(s.sync, 'signedout', 'sync = signedout after a 401');
    t.check(!(await page.evaluate(() => /under_signedin=1/.test(document.cookie))), 'hint cookie cleared');
    t.soft(!(await page.evaluate(() => { const a = document.querySelector('.book-account'); return a && a.classList.contains('is-signed-in'); })), 'account mark follows the 401 (not gold)');
    const n = net.api.length;
    for (let i = 0; i < 2; i++) {
      await page.evaluate(() => window.scrollBy({ top: 900, behavior: 'instant' })); await settle(page, 300);
      await placeAction(page, 'set'); await page.keyboard.press('Escape'); await settle(page, 2500);
    }
    t.eq(net.api.length - n, 0, 'no further /api calls after the 401');
  } finally { await ctx.close(); }
});

async function run() {
  for (const bname of browsersFor(['chromium', 'webkit'])) {
    const browser = await launch(bname);
    try {
      for (const x of TESTS) {
        if (!x.browsers.includes(bname)) continue;
        await R.test(`${bname} ${x.name}`, t => x.fn(t, browser), { timeout: 180000 });
      }
    } finally { await browser.close(); }
  }
}
await withServer(run);
process.exit(R.summary());
