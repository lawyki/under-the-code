// Pass 25 tracking traces: spec §13 table + review additions (H1 H2 H3 H4
// H5, M5 M6). Every trace starts from C0 = part-1#ch1-kernel-p2 (seeded in
// localStorage, restored by hash) unless it says otherwise. Time is driven
// with page.clock (installed before navigation, runFor fires timers); scroll
// is driven with mouse.wheel / keyboard / window.scrollTo and real waits.
// Thresholds are the shipped ones unless a line says "T shrunk".
//
//   node traces.mjs [--browser=chromium|webkit] [--only=<regex>] [--headed]
import {
  reporter, withServer, launch, browsersFor, newContext, openPart, requireClient, waitState,
  snap, setT, progress, advance, settle, wheel, burst, key, scriptedJump, read, idle, blurAll,
  setHidden, anchorScrollY, anchorDrift, placeAction, placeBarHas, openPlaceBar, geom, sameC, cAdvanced, brief,
  startC0, C0, FakeApi, clickInBookLink, parkPointer, VIEWPORTS, INSTRUMENT, progressRecord, sourceHtml, url, watch, PARA_RE, BASE,
} from './lib.mjs';

const R = reporter('traces');
const TRACES = [];
// browsers: which engines run it. Everything runs on Chromium; WebKit runs
// the ones marked ['chromium','webkit'].
function trace(name, browsers, fn, timeout = 300000) { TRACES.push({ name, browsers, fn, timeout }); }
const BOTH = ['chromium', 'webkit'];
const CHR = ['chromium'];

// ---------------------------------------------------------------- §13 table
trace('wheel +120 every 8 s advances each step', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    t.check(sameC(s0.C, { ...C0, fraction: 0 }, 0.02), 'C0 restored', brief(s0.C));
    let prev = s0.C;
    for (let i = 1; i <= 6; i++) {
      await advance(page, 8000); await wheel(page, 120, 450); await advance(page, 600);
      const s = await snap(page);
      t.check(cAdvanced(prev, s.C) && s.state === 'READING', `step ${i} advances C`, brief(prev) + ' -> ' + brief(s.C) + ' ' + s.state);
      prev = s.C;
    }
  } finally { await ctx.close(); }
});

trace('PageDown every 45 s x4 -> 4 commits', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await blurAll(page);
    let prev = s0.C, commits = 0;
    for (let i = 1; i <= 4; i++) {
      await advance(page, 45000);
      const pre = await snap(page); const y0 = await page.evaluate(() => scrollY);
      await key(page, 'PageDown', 900); await advance(page, 600);
      const s = await snap(page); const y1 = await page.evaluate(() => [scrollY, innerHeight, __utcPlace.L()]);
      const ch = await page.evaluate(([a, b]) => [__utcPlace.chars(a + __utcPlace.navB(), b + __utcPlace.navB()), __utcPlace.chars(a + __utcPlace.navB(), a + innerHeight), __utcPlace.navB()], [y0, y1[0]]);
      t.info('pre', 'budget ' + pre.budget + '/' + pre.cap + ' state ' + pre.state + ' y0 ' + y0 + ' y1 ' + JSON.stringify(y1) + ' crossed/band/navB ' + JSON.stringify(ch));
      if (cAdvanced(prev, s.C)) commits++;
      t.check(s.state === 'READING', `PageDown ${i}: still READING`, s.state + ' C ' + brief(s.C));
      prev = s.C;
    }
    const s = await snap(page);
    t.eq(commits, 4, '4 commits (C advanced on every PageDown)');
    t.eq(s.writes - s0.writes, 4, '4 localStorage writes');
  } finally { await ctx.close(); }
});

trace('PageDown every 2 s x8 -> C moves at most one screen', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await blurAll(page);
    for (let i = 0; i < 8; i++) { await key(page, 'PageDown', 900); await advance(page, 1100); }
    await advance(page, 2000);
    const s = await snap(page); const g = await geom(page);
    const moved = (s.C && s0.C && typeof s.C.y === 'number') ? s.C.y - s0.C.y : NaN;
    t.check(moved <= g.innerHeight, 'C moved at most one screen', 'moved ' + moved + 'px, innerHeight ' + g.innerHeight + ', B ' + g.B + ', state ' + s.state + ', C ' + brief(s.C));
    t.check(s.state === 'EXCURSION', 'skimming ended as an EXCURSION', s.state);
  } finally { await ctx.close(); }
});

trace('+4000px in 300 ms then idle -> C0, 0 writes; then reading -> soft promote ~25 s; undo by a step at Rprev -> 1 write', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await burst(page, 4000, 300); await settle(page, 600);
    let s = await snap(page);
    t.eq(s.state, 'EXCURSION', 'burst -> EXCURSION');
    t.eq(s.excursion && s.excursion.kind, 'soft', 'direct seek is a soft excursion');
    await idle(page, 10000);
    s = await snap(page);
    t.check(sameC(s.C, s0.C), 'after 10 s idle: C = C0', brief(s.C));
    t.eq(s.writes - s0.writes, 0, '0 writes while idle in the excursion');
    let promotedAt = null; const t0 = 10600;
    for (let i = 1; i <= 12; i++) {
      await advance(page, 5000); await wheel(page, 120, 450); await advance(page, 450);
      s = await snap(page);
      if (!sameC(s.C, s0.C)) { promotedAt = t0 + i * 5900; break; }
    }
    t.check(promotedAt !== null, 'promoted while reading', brief(s.C) + ' ' + s.state);
    t.check(promotedAt !== null && promotedAt >= 25000 && promotedAt <= 50000, 'promoted ~25 s after the burst (soft rule)', 'at ~' + promotedAt + ' ms');
    t.check(s.Rprev && s.Rprev.anchor === s0.C.anchor, 'Rprev = C0 after promotion', brief(s.Rprev));
    // Undo: back to Rprev (a seek), then one reading step there.
    const w = s.writes;
    const y = await anchorScrollY(page, s0.C.anchor, s0.C.fraction);
    await page.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), y); await settle(page, 600);
    await advance(page, 4000); await wheel(page, 60, 450); await advance(page, 700);
    s = await snap(page);
    t.check(s.C && s.C.anchor === s0.C.anchor, 'a reading step at Rprev restores C0', brief(s.C));
    t.eq(s.writes - w, 1, 'undo costs exactly 1 write');
  } finally { await ctx.close(); }
});

trace('"Back to before the detour" in the place bar restores Rprev with 1 write', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await burst(page, 4000, 300); await settle(page, 600);
    let s;
    for (let i = 0; i < 12; i++) { await advance(page, 5000); await wheel(page, 120, 450); s = await snap(page); if (!sameC(s.C, s0.C)) break; }
    t.check(!sameC(s.C, s0.C), 'precondition: promoted', brief(s.C));
    await openPlaceBar(page);
    t.check(await placeBarHas(page, 'back'), '"Back to before the detour" offered');
    const w = s.writes;
    await placeAction(page, 'back'); await advance(page, 800);
    s = await snap(page);
    t.check(s.C && s.C.anchor === s0.C.anchor, 'C back to C0', brief(s.C));
    t.eq(s.writes - w, 1, '1 write');
  } finally { await ctx.close(); }
});

trace('fling 3B and back -> 0 writes', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    const g = await geom(page);
    await burst(page, 3 * g.B, 300); await settle(page, 250);
    await burst(page, -3 * g.B, 300); await settle(page, 900); await advance(page, 2000);
    const s = await snap(page);
    t.eq(s.writes - s0.writes, 0, '0 writes');
    t.check(sameC(s.C, s0.C), 'C = C0', brief(s.C));
    t.check(s.state === 'READING', 'returned (READING)', s.state);
  } finally { await ctx.close(); }
});

trace('scrollbar-like scripted scrollTo jump -> C0', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await scriptedJump(page, 3000); await advance(page, 10000);
    const s = await snap(page);
    t.eq(s.state, 'EXCURSION', 'unexplained jump -> EXCURSION');
    t.check(sameC(s.C, s0.C), 'C = C0', brief(s.C));
    t.eq(s.writes - s0.writes, 0, '0 writes');
    t.info('note', 'a real scrollbar drag cannot be driven headless; window.scrollTo with no input stands in for it');
  } finally { await ctx.close(); }
});

trace('fullscreen figure 60 s -> C0, paused', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    const opened = await page.evaluate(() => {
      const btns = [...document.querySelectorAll('.fs-button')];
      const vis = btns.find(x => { const r = x.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; });
      const near = vis || btns.sort((a, b) => Math.abs(a.getBoundingClientRect().top) - Math.abs(b.getBoundingClientRect().top))[0];
      if (!near) return false; near.click(); return true;
    });
    if (!opened) t.skipTest('no .fs-button on part-1');
    await settle(page, 900);
    let s = await snap(page);
    t.check(s.paused === true, 'tracking paused while fullscreen', JSON.stringify({ paused: s.paused, state: s.state }));
    await idle(page, 60000, { nudge: true });
    await page.keyboard.press('Escape'); await settle(page, 1200); await advance(page, 2000);
    s = await snap(page);
    t.check(sameC(s.C, s0.C), 'C = C0 after 60 s fullscreen', brief(s.C));
    t.eq(s.writes - s0.writes, 0, '0 writes');
  } finally { await ctx.close(); }
});

trace('chapter-nav click then reading -> C0, promoted only under the hard rule', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    const target = 'ch1-vonneumann';
    await page.locator(`.chapter-nav a.nav-item[href="#${target}"]`).first().click();
    await settle(page, 1800);
    let s = await snap(page);
    t.eq(s.state, 'EXCURSION', 'chapter-nav click -> EXCURSION');
    t.eq(s.excursion && s.excursion.kind, 'hard', 'in-book link (backward) is a hard excursion');
    const secEnd = await page.evaluate(id => { const e = document.getElementById(id); return e ? e.getBoundingClientRect().bottom + scrollY : null; }, target);
    const g = await geom(page);
    let elapsed = 0, promotedAt = null, endPassedAt = null;
    while (elapsed < 270000) {
      await advance(page, 8000); await wheel(page, 120, 450); elapsed += 8450;
      const y = await page.evaluate(() => scrollY);
      if (endPassedAt === null && secEnd !== null && y + g.L > secEnd) endPassedAt = elapsed;
      s = await snap(page);
      if (elapsed >= 40000 && elapsed < 48500) {
        t.check(sameC(s.C, s0.C) || (endPassedAt !== null), 'after ~40 s reading: still C0', brief(s.C));
      }
      if (!sameC(s.C, s0.C)) { promotedAt = elapsed; break; }
    }
    t.check(promotedAt !== null, 'eventually promoted', 'after ' + elapsed + ' ms');
    const legit = promotedAt !== null && (promotedAt >= 180000 || (endPassedAt !== null && promotedAt >= endPassedAt));
    t.check(legit, 'promoted only after >= 3 min (or past the end of the section)',
      'promotedAt ' + promotedAt + ' ms; section end passed at ' + endPassedAt + '; paragraphs: ' + JSON.stringify(s.excursion && s.excursion.paras));
  } finally { await ctx.close(); }
}, 420000);

async function findOtherPartTipLink(page) {
  return page.evaluate(async () => {
    const refs = [...document.querySelectorAll('.glossary-ref')];
    const here = scrollY;
    const found = [];
    for (const el of refs) {
      el.focus({ preventScroll: true });
      await new Promise(r => setTimeout(r, 20));
      const a = document.querySelector('.glossary-tip-link');
      const href = a && a.getAttribute('href');
      el.blur();
      if (href && /^part-[2-5]/.test(href)) found.push({ i: refs.indexOf(el), href, d: Math.abs(el.getBoundingClientRect().top) });
    }
    found.sort((x, y) => (/^part-3/.test(y.href) - /^part-3/.test(x.href)) || x.d - y.d);
    return found[0] || null;
  });
}

trace('tooltip link to another part, then goBack() -> C0', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    const f = await findOtherPartTipLink(page);
    if (!f) t.skipTest('no glossary tooltip on part-1 links to another part');
    t.info('tooltip link', f.href + ' (part-1 has no tooltip into part-3; nearest other-part link used)');
    await page.evaluate(i => {
      const el = document.querySelectorAll('.glossary-ref')[i];
      el.focus({ preventScroll: true });
    }, f.i);
    await settle(page, 300);
    await Promise.all([page.waitForURL(/\/part-[2-5]/, { timeout: 10000 }), clickInBookLink(page, '.glossary-tip-link')]);
    await requireClient(page); await parkPointer(page);
    let s = await waitState(page, ['EXCURSION', 'READING', 'PINNED'], 8000).catch(() => snap(page));
    t.check(s.state === 'EXCURSION' && s.C && s.C.part === 'part-1', 'on the other part (after SETTLING): EXCURSION, C still in part-1', s.state + ' ' + brief(s.C));
    await page.goBack(); await requireClient(page); await settle(page, 2000);
    s = await snap(page);
    t.check(sameC(s.C, s0.C), 'after goBack: C = C0', brief(s.C));
    const p = await progress(page);
    t.check(p && p.part === 'part-1' && p.anchor === s0.C.anchor, 'stored place = C0', p && (p.part + '#' + p.anchor));
  } finally { await ctx.close(); }
});

function firstPara(part) {
  const m = sourceHtml(part).match(/<p id="(ch[0-9B][A-Za-z0-9]*-[A-Za-z0-9-]+-p1)"/);
  return m && m[1];
}

trace('open part-3 directly (typed URL), read 40 s -> part-3', BOTH, async (t, b) => {
  const { ctx } = await newContext(b, { initScripts: [INSTRUMENT] });
  try {
    const target = firstPara('part-3');
    const page = await openPart(ctx, 'part-3', { hash: target, seedProgress: progressRecord('part-1', C0.anchor, 0), clock: true });
    let s = await waitState(page, ['EXCURSION', 'READING', 'PINNED'], 8000).catch(() => snap(page));
    t.check(s.C && s.C.part === 'part-1', 'arrival: C still part-1', brief(s.C) + ' ' + s.state);
    t.eq(s.excursion && s.excursion.kind, 'soft', 'direct arrival is a soft excursion');
    await read(page, 40000, { step: 120, every: 8000 }); await advance(page, 800);
    s = await snap(page);
    t.check(s.C && s.C.part === 'part-3', 'after 40 s reading: C in part-3', brief(s.C));
    const p = await progress(page);
    t.check(p && p.part === 'part-3', 'stored place in part-3', p && p.part + '#' + p.anchor);
    t.info('arrival hash', 'part-3#' + target + ' (the opener has no paragraphs to read)');
  } finally { await ctx.close(); }
});

trace('detour by in-book link, read 40 s, close, reopen part-1 -> C0 (H2)', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    const href = await clickInBookLink(page, '#ch1-kernel a[href^="part-"]');
    if (!href) t.skipTest('no in-book cross-part link in #ch1-kernel');
    await page.waitForURL(/\/part-[2-5]/, { timeout: 10000 });
    await requireClient(page); await parkPointer(page);
    let s = await waitState(page, ['EXCURSION', 'READING', 'PINNED'], 8000).catch(() => snap(page));
    t.check(s.state === 'EXCURSION' && s.excursion && s.excursion.kind === 'hard', 'link detour = hard EXCURSION', s.state + ' ' + JSON.stringify(s.excursion));
    await read(page, 40000); await advance(page, 800);
    s = await snap(page);
    t.check(sameC(s.C, s0.C), 'after 40 s on the detour: C = C0', brief(s.C));
    await page.close({ runBeforeUnload: true });
    const p2 = watch(await ctx.newPage());
    await p2.goto(url('part-1'), { waitUntil: 'load' });
    await requireClient(p2); await settle(p2, 2500);
    s = await snap(p2);
    t.check(sameC(s.C, s0.C), 'reopened part-1: C = C0', brief(s.C));
    const drift = await anchorDrift(p2, s0.C.anchor, s0.C.fraction);
    t.check(drift !== null && Math.abs(drift) <= 1, 'reopened at C0 pixel-exact', 'drift ' + drift);
  } finally { await ctx.close(); }
});

trace('tab hidden during an excursion -> beacon/POST carries C, not the live position', BOTH, async (t, b) => {
  const { ctx, page, s0, fake } = await startC0(b, { signedIn: true });
  try {
    await setT(page, { POST_DEBOUNCE_MS: 600000 });
    t.info('T shrunk', 'POST_DEBOUNCE_MS=600000 so the committed C is still unsent (dirty) when the tab hides');
    await advance(page, 8000); await wheel(page, 120, 450); await advance(page, 700);
    const c1 = (await snap(page)).C;
    t.check(cAdvanced(s0.C, c1), 'precondition: one step committed C1', brief(c1));
    await scriptedJump(page, 3000);
    const live = await page.evaluate(() => window.__utcPlace.liveAnchor());
    const n = fake.calls.length;
    await setHidden(page, true); await settle(page, 800);
    const sent = fake.calls.slice(n).filter(c => c.method === 'POST' && c.path === '/api/position');
    t.check(sent.length >= 1, 'a beacon/POST was sent on hide', sent.length + ' sent (' + sent.map(c => c.type).join(',') + ')');
    const readable = sent.filter(c => c.body && typeof c.body === 'object');
    if (readable.length < sent.length) t.info('unreadable bodies', (sent.length - readable.length) + ' hide write(s) had no body visible to the route (beacon payload not exposed by this engine)');
    t.check(readable.length >= 1 && readable.every(c => c.body.anchor === c1.anchor && Math.abs(c.body.fraction - c1.fraction) < 0.011), 'every hide write carries C1 ' + brief(c1), readable.map(c => c.body && c.body.anchor + '@' + c.body.fraction).join(', '));
    t.check(!sent.some(c => c.body && live && c.body.anchor === live.anchor && live.anchor !== c1.anchor), 'no hide write carries the live position', live && live.anchor);
    await setHidden(page, false);
  } finally { await ctx.close(); }
});

trace('pin: held through scrolling elsewhere < 3 min, released by reading forward from within 1B', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b);
  try {
    await advance(page, 8000); await wheel(page, 240, 500); await advance(page, 700);
    await placeAction(page, 'set'); await advance(page, 500);
    let s = await snap(page);
    const pin = s.C;
    t.eq(s.state, 'PINNED', 'Set -> PINNED');
    t.eq(pin && pin.src, 'set', 'C.src = set');
    t.eq((await progress(page) || {}).src, 'set', 'stored src = set');
    t.check(await placeBarHas(page, 'track'), '"Let the book track" offered while pinned');
    await page.keyboard.press('Escape'); await settle(page, 300);
    await scriptedJump(page, 2500);
    await read(page, 60000); await advance(page, 800);
    s = await snap(page);
    t.check(sameC(s.C, pin), 'pin held after 60 s reading elsewhere', brief(s.C));
    const y = await anchorScrollY(page, pin.anchor, pin.fraction);
    await page.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), y); await settle(page, 700);
    await read(page, 24000); await advance(page, 800);
    s = await snap(page);
    t.check(s.C && s.C.src === 'auto' && cAdvanced(pin, s.C), 'reading forward from the pin releases it (src auto, C advanced)', brief(s.C) + ' ' + s.state);
    t.eq((await progress(page) || {}).src, 'auto', 'stored src = auto');
  } finally { await ctx.close(); }
});

trace('set then Undo -> previous place restored in both stores', BOTH, async (t, b) => {
  const { ctx, page, s0, fake } = await startC0(b, { signedIn: true });
  try {
    await scriptedJump(page, 1500);
    await placeAction(page, 'set'); await advance(page, 600);
    let s = await snap(page);
    t.check(!sameC(s.C, s0.C) && s.C.src === 'set', 'set moved C', brief(s.C));
    t.check(await placeBarHas(page, 'undo'), 'Undo offered after a set');
    await placeAction(page, 'undo'); await advance(page, 3000); await settle(page, 500);
    s = await snap(page);
    t.check(sameC(s.C, s0.C), 'Undo restores C0', brief(s.C));
    const p = await progress(page);
    t.check(p && p.anchor === s0.C.anchor, 'localStorage restored', p && p.anchor);
    t.check(fake.position && fake.position.anchor === s0.C.anchor, 'server restored', fake.position && fake.position.anchor);
  } finally { await ctx.close(); }
});

trace('read to the end of the page -> last paragraph', CHR, async (t, b) => {
  const html = sourceHtml('part-1');
  const ids = [...html.matchAll(/<p id="(ch[0-9B][A-Za-z0-9]*-[A-Za-z0-9-]+-p\d+)"/g)].map(m => m[1]);
  const start = ids[Math.max(0, ids.length - 8)];
  const { ctx, page, s0 } = await startC0(b, { anchor: start });
  try {
    await blurAll(page);
    for (let i = 0; i < 40; i++) {
      const g = await geom(page);
      if (g.scrollY >= g.max - 4) break;
      await advance(page, 45000); await key(page, 'PageDown', 900);
    }
    await advance(page, 1500);
    const s = await snap(page);
    const last = await page.evaluate(src => {
      const re = new RegExp(src);
      const ps = [...document.querySelectorAll('p[id]')].filter(p => re.test(p.id));
      const vis = ps.filter(p => { const r = p.getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight && r.height > 0; });
      return vis.length ? vis[vis.length - 1].id : null;
    }, PARA_RE.source);
    t.eq(s.K, last, 'K = last paragraph whose top is visible');
    const p = await progress(page);
    t.eq(p && p.k, last, 'stored k = last paragraph');
  } finally { await ctx.close(); }
});

trace('open with no hash (navigate) -> pixel-exact restore', BOTH, async (t, b) => {
  const { ctx } = await newContext(b, { initScripts: [INSTRUMENT] });
  try {
    const anchor = 'ch1-kernel-p4', fraction = 0.37;
    const page = await openPart(ctx, 'part-1', { seedProgress: progressRecord('part-1', anchor, fraction) });
    await settle(page, 2500);
    const navType = await page.evaluate(() => performance.getEntriesByType('navigation')[0].type);
    t.eq(navType, 'navigate', 'navigation type');
    const drift = await anchorDrift(page, anchor, fraction);
    t.check(drift !== null && Math.abs(drift) <= 1, 'anchor + fraction at 56px ±1', 'drift ' + drift);
  } finally { await ctx.close(); }
});

trace('reload mid-excursion -> no forced jump', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { clock: false });
  try {
    await scriptedJump(page, 3000); await settle(page, 800);
    const y1 = await page.evaluate(() => scrollY);
    await page.reload({ waitUntil: 'load' }); await requireClient(page); await settle(page, 2500);
    const y2 = await page.evaluate(() => scrollY);
    const navType = await page.evaluate(() => performance.getEntriesByType('navigation')[0].type);
    const s = await snap(page);
    t.eq(navType, 'reload', 'navigation type');
    t.check(Math.abs(y2 - y1) < 200, 'browser scroll restoration kept (no jump to C)', 'before ' + y1 + ' after ' + y2);
    t.check(sameC(s.C, s0.C), 'C still C0', brief(s.C));
  } finally { await ctx.close(); }
});

trace('rotation 375x667 -> 667x375 and back: no commit, view re-pinned', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { viewport: VIEWPORTS.phone, hasTouch: true, isMobile: true, clock: false });
  try {
    for (const vp of [{ width: 667, height: 375 }, { width: 375, height: 667 }]) {
      await page.setViewportSize(vp); await settle(page, 2500);
      const s = await snap(page);
      t.eq(s.writes - s0.writes, 0, `${vp.width}x${vp.height}: no commit`);
      const drift = await anchorDrift(page, s.C.anchor, s.C.fraction);
      t.check(drift !== null && Math.abs(drift) <= 2, `${vp.width}x${vp.height}: view re-pinned to C`, 'drift ' + drift + ' C ' + brief(s.C));
    }
  } finally { await ctx.close(); }
});

trace('zoom-like width change 1440 -> 1180 -> 1440: no commit, view re-pinned', BOTH, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { clock: false });
  try {
    for (const vp of [{ width: 1180, height: 900 }, { width: 1440, height: 900 }, { width: 1440, height: 760 }]) {
      await page.setViewportSize(vp); await settle(page, 2500);
      const s = await snap(page);
      t.eq(s.writes - s0.writes, 0, `${vp.width}x${vp.height}: no commit`);
      const drift = await anchorDrift(page, s.C.anchor, s.C.fraction);
      const tol = vp.height !== 900 ? 400 : 2;   // height-only change: B/L recomputed, no re-pin required
      t.check(drift !== null && Math.abs(drift) <= tol, `${vp.width}x${vp.height}: ` + (tol === 2 ? 'view re-pinned to C' : 'no step taken'), 'drift ' + drift);
    }
  } finally { await ctx.close(); }
});

trace('multi-tab: a stale hidden tab must not overwrite (H3)', BOTH, async (t, b) => {
  const fake = new FakeApi();
  const { ctx, page: A, s0 } = await startC0(b, { fake, clock: false });
  try {
    const B = await openPart(ctx, 'part-1', { hash: C0.anchor });
    await waitState(B, ['READING', 'PINNED'], 8000);
    await setT(A, { POST_DEBOUNCE_MS: 300 });
    await A.bringToFront();
    await A.mouse.move(A.viewportSize().width - 8, 500);
    for (let i = 0; i < 3; i++) { await A.waitForTimeout(1200); await wheel(A, 120, 450); }
    await A.waitForTimeout(1500);
    const c1 = (await snap(A)).C;
    t.check(cAdvanced(s0.C, c1), 'tab A committed C1', brief(c1));
    t.check(fake.position && fake.position.anchor === c1.anchor, 'server has C1', fake.position && fake.position.anchor);
    await B.waitForTimeout(500);
    const sb = await snap(B);
    t.check(sb.C && sb.C.anchor === c1.anchor, 'tab B adopted C1 from the storage event', brief(sb.C));
    const n = fake.calls.length;
    await setHidden(B, true); await B.waitForTimeout(800);
    const fromB = fake.calls.slice(n).filter(c => c.method === 'POST' && c.path === '/api/position');
    t.check(!fromB.some(c => c.body && c.body.anchor === s0.C.anchor), 'B hidden: no write of the stale C0', fromB.map(c => c.body && c.body.anchor).join(','));
    t.check(fake.position && fake.position.anchor === c1.anchor, 'server still C1', fake.position && fake.position.anchor);
    const p = await progress(A);
    t.check(p && p.anchor === c1.anchor, 'localStorage still C1', p && p.anchor);
  } finally { await ctx.close(); }
});

trace('out-of-order POSTs: one in flight, solid only for the latest seq; 409 stale handled quietly (H4)', BOTH, async (t, b) => {
  const fake = new FakeApi();
  // Hold the load GET for the whole trace: no 200 reaches the page except the
  // POST acks this trace releases, so the mark's state reflects only those
  // (H9 lets any healthy 200 keep it solid; H4 needs the seq rule isolated).
  const hg = fake.hold('GET', '/api/position');
  const h1 = fake.hold('POST', '/api/position');     // whatever POST comes first (load or set) is held
  const { ctx, page } = await startC0(b, { fake, clock: false });
  try {
    const synced = () => page.evaluate(() => { const m = document.querySelector('.book-nav .cue-mark'); return !!(m && m.classList.contains('is-synced')); });
    t.check(!(await synced()), 'page load starts hollow (nothing acked yet)');
    let c1 = await Promise.race([h1.seen, page.waitForTimeout(3000).then(() => null)]);
    if (!c1) { await scriptedJump(page, 700); await placeAction(page, 'set'); await page.keyboard.press('Escape'); c1 = await Promise.race([h1.seen, page.waitForTimeout(6000).then(() => null)]); }
    t.check(!!c1, 'first POST sent (held by the fake)', c1 && c1.body && c1.body.anchor + '/' + c1.body.seq);
    if (!c1) return;
    const h2 = fake.hold('POST', '/api/position');
    await scriptedJump(page, 900);          // a different K, so the set is a real change
    await placeAction(page, 'set'); await page.keyboard.press('Escape');
    await page.waitForTimeout(2500);
    t.eq(fake.maxInflight['POST /api/position'], 1, 'one POST in flight at a time');
    t.check(!(await synced()), 'not solid while the first POST is unanswered');
    h1.release(); await page.waitForTimeout(600);
    t.check(!(await synced()), 'ack of the older seq does not turn the mark solid');
    const c2 = await Promise.race([h2.seen, page.waitForTimeout(6000).then(() => null)]);
    t.check(c2 && c2.body && c1.body && c2.body.seq > c1.body.seq, 'second POST carries a newer seq',
      c2 ? (c1.body.seq + ' -> ' + c2.body.seq) : 'no second POST; calls: ' + fake.calls.filter(c => c.method === 'POST').map(c => c.path + ' ' + c.status + ' ' + (c.body && c.body.anchor + '/' + c.body.seq)).join(', '));
    h2.release(); await page.waitForTimeout(800);
    t.check(await synced(), 'solid after the latest seq is acked');
    t.check(fake.position && c2 && fake.position.anchor === c2.body.anchor, 'server holds the latest place');
    // 409 stale
    fake.failNext('POST', '/api/position', 409, { error: 'stale', updated_at: Date.now() });
    const n = fake.calls.length, errs = page.__errors.length;
    await scriptedJump(page, 900); await placeAction(page, 'set'); await page.keyboard.press('Escape'); await page.waitForTimeout(3500);
    const posts = fake.calls.slice(n).filter(c => c.method === 'POST' && c.path === '/api/position');
    t.check(posts.length >= 1 && posts.length <= 3, '409 stale: no retry storm', posts.length + ' POSTs');
    const newErrs = page.__errors.slice(errs).filter(e => !/Failed to load resource/.test(e));
    t.check(newErrs.length === 0, '409 stale: no script errors', newErrs.join(' | '));
    const s = await snap(page);
    t.soft(s.sync !== 'paused' && s.sync !== 'signedout', '409 stale: sync not paused by one stale answer', s.sync);
  } finally { hg.release(); await ctx.close(); }
});

for (const vp of ['desktop', 'phone']) {
  trace(`labels at a section start come from K (H1) ${vp}`, BOTH, async (t, b) => {
    const { ctx, page } = await startC0(b, { viewport: VIEWPORTS[vp], hasTouch: vp === 'phone', isMobile: vp === 'phone', clock: false });
    try {
      const target = 'ch1-cpu-p1';
      const pos = await page.evaluate(id => {
        const P = window.__utcPlace; const row = P.table().find(r => r.id === id);
        return row ? { top: row.top, L: P.L() } : null;
      }, target);
      if (!pos) t.skipTest('table() has no ' + target);
      await page.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), Math.round(pos.top - pos.L + 2));
      await settle(page, 900);
      const s = await snap(page);
      t.eq(s.K, target, 'K at the attention line = first paragraph of §04');
      await placeAction(page, 'set'); await settle(page, 600);
      const want = await page.evaluate(() => {
        const sec = document.getElementById('ch1-cpu');
        const h = sec.querySelector('h2').cloneNode(true); h.querySelectorAll('br').forEach(x => x.replaceWith(' '));
        return { label: sec.querySelector('.section-number').textContent.trim(), title: h.textContent.replace(/\s+/g, ' ').trim() };
      });
      const p = await progress(page);
      t.eq(p && p.section, 'ch1-cpu', 'stored section = ch1-cpu');
      t.eq(p && p.sectionLabel, want.label, 'stored sectionLabel from K');
      t.eq(p && p.sectionTitle, want.title, 'stored sectionTitle from K');
      t.eq(p && p.k, target, 'stored k');
      const y = await page.evaluate(() => scrollY);
      const back = await anchorScrollY(page, p.anchor, p.fraction);
      t.check(Math.abs(back - y) <= 4, 'anchor/fraction still encode line 56 (restore lands here)', 'restore y ' + back + ' vs ' + y);
      const idx = watch(await ctx.newPage());
      await idx.goto(BASE + '/', { waitUntil: 'load' }); await settle(idx, 1200);
      const meta = await idx.evaluate(() => { const m = document.querySelector('.resume-card'); return m ? m.textContent.replace(/\s+/g, ' ') : null; });
      t.check(meta && /§04/.test(meta), 'index resume card says §04', meta);
    } finally { await ctx.close(); }
  });
}

trace('keyboard reader: focused glossary term, ArrowDown keeps tracking (H5)', BOTH, async (t, b) => {
  // Find a paragraph with a glossary term, then start there.
  let anchor;
  {
    const { ctx } = await newContext(b);
    const p = await ctx.newPage();
    await p.goto(url('part-1', '', { debug: false })); await p.waitForTimeout(1500);
    anchor = await p.evaluate(() => { const el = [...document.querySelectorAll('.glossary-ref')].find(e => e.closest('p[id]')); return el && el.closest('p[id]').id; });
    await ctx.close();
  }
  if (!anchor) t.skipTest('no glossary term inside a paragraph on part-1');
  const { ctx, page, s0 } = await startC0(b, { anchor });
  try {
    await page.evaluate(id => document.getElementById(id).querySelector('.glossary-ref').focus({ preventScroll: true }), anchor);
    await settle(page, 400);
    const tipOpen = () => page.evaluate(() => !!document.querySelector('.glossary-tip.visible'));
    t.check(await tipOpen(), 'tooltip open on focus');
    let prev = s0.C;
    const y0 = await page.evaluate(() => scrollY);
    for (let i = 0; i < 5; i++) {
      await advance(page, 8000);
      for (let k = 0; k < 3; k++) await page.keyboard.press('ArrowDown');
      await settle(page, 600); await advance(page, 600);
    }
    const s = await snap(page);
    const y1 = await page.evaluate(() => scrollY);
    if (y1 - y0 < 100 && b.browserType().name() === 'webkit') t.skipTest('headless WebKit barely scrolls on ArrowDown from a focused term ('+(y1-y0)+'px); run the manual Safari check');
    t.check(y1 - y0 > 100, 'ArrowDown scrolled the page', (y1 - y0) + 'px');
    t.check(!(await tipOpen()), 'tooltip hidden by scrolling');
    t.check(s.paused === false, 'tracking not paused', String(s.paused));
    t.check(cAdvanced(prev, s.C) && s.writes > s0.writes, 'C advanced while arrowing', brief(prev) + ' -> ' + brief(s.C));
  } finally { await ctx.close(); }
});

trace('reading past a tall figure stays READING', CHR, async (t, b) => {
  const { ctx: c0 } = await newContext(b);
  const p0 = await c0.newPage();
  await p0.goto(url('part-1', '', { debug: false })); await p0.waitForTimeout(1200);
  const start = await p0.evaluate(() => {
    const figs = [...document.querySelectorAll('[id^="fig-"]')].filter(f => !f.closest('svg'));
    figs.sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height);
    const f = figs[0]; if (!f) return null;
    const ps = [...document.querySelectorAll('p[id]')].filter(p => p.compareDocumentPosition(f) & Node.DOCUMENT_POSITION_FOLLOWING);
    return { para: ps.length ? ps[ps.length - 1].id : null, fig: f.id, h: Math.round(f.getBoundingClientRect().height) };
  });
  await c0.close();
  if (!start || !start.para) t.skipTest('no figure with a paragraph before it');
  t.info('figure', start.fig + ' ' + start.h + 'px, starting at ' + start.para);
  const { ctx, page } = await startC0(b, { anchor: start.para });
  try {
    await blurAll(page);
    let ok = true;
    for (let i = 0; i < 3; i++) {
      await advance(page, 45000);
      const pre = await snap(page); const y0 = await page.evaluate(() => scrollY);
      await key(page, 'PageDown', 900); await advance(page, 600);
      const s = await snap(page); const y1 = await page.evaluate(() => [scrollY, innerHeight, __utcPlace.L()]);
      const ch = await page.evaluate(([a, b]) => [__utcPlace.chars(a + __utcPlace.navB(), b + __utcPlace.navB()), __utcPlace.chars(a + __utcPlace.navB(), a + innerHeight), __utcPlace.navB()], [y0, y1[0]]);
      t.info('pre', 'budget ' + pre.budget + '/' + pre.cap + ' state ' + pre.state + ' y0 ' + y0 + ' y1 ' + JSON.stringify(y1) + ' crossed/band/navB ' + JSON.stringify(ch)); if (s.state !== 'READING') { ok = false; t.info('state', 'PageDown ' + (i + 1) + ': ' + s.state + ' ' + JSON.stringify(s.excursion) + ' budget ' + s.budget + '/' + s.cap); }
    }
    t.check(ok, 'stays READING across the figure');
  } finally { await ctx.close(); }
});

trace('CDP flick: 0.4B reads, 4B seeks', CHR, async (t, b) => {
  const { ctx, page, s0 } = await startC0(b, { clock: false });
  try {
    const cdp = await ctx.newCDPSession(page);
    const g = await geom(page);
    const flick = async d => {
      await cdp.send('Input.synthesizeScrollGesture', { x: 700, y: 500, yDistance: -d, speed: 2000, gestureSourceType: 'touch' });
      await settle(page, 1200);
    };
    await page.waitForTimeout(3000);
    await flick(Math.round(0.4 * g.B));
    let s = await snap(page);
    t.check(s.state === 'READING', 'flick 0.4B -> READING (a step)', s.state);
    await page.waitForTimeout(3000);
    await flick(Math.round(4 * g.B));
    s = await snap(page);
    t.check(s.state === 'EXCURSION', 'flick 4B -> EXCURSION', s.state);
  } finally { await ctx.close(); }
});

trace('4x CPU throttle fling: no long task > 50 ms; rect reads recorded', CHR, async (t, b) => {
  const { ctx, page } = await startC0(b, { clock: false });
  try {
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await settle(page, 1500);
    await page.evaluate(() => { window.__longtasks.length = 0; window.__rectReads = 0; window.__countRects = true; });
    const g = await geom(page);
    await burst(page, 3 * g.B, 300, 12); await settle(page, 200);
    const during = await page.evaluate(() => window.__rectReads);
    await settle(page, 1500);
    const r = await page.evaluate(() => ({ lt: window.__longtasks.map(x => Math.round(x.d)), reads: window.__rectReads, unsupported: !!window.__longtaskUnsupported }));
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
    if (r.unsupported) t.skip('long tasks', 'PerformanceObserver longtask unsupported');
    else t.check(r.lt.every(d => d <= 50), 'no long task > 50 ms during the fling', 'long tasks: [' + r.lt.join(', ') + ']');
    t.soft(during === 0, '0 getBoundingClientRect calls during the fling burst', during + ' during, ' + r.reads + ' incl. burst end');
  } finally { await ctx.close(); }
});

// ---------------------------------------------------------------- runner
async function run() {
  for (const bname of browsersFor(['chromium', 'webkit'])) {
    const browser = await launch(bname);
    try {
      for (const tr of TRACES) {
        if (!tr.browsers.includes(bname)) continue;
        await R.test(`${bname} ${tr.name}`, t => tr.fn(t, browser), { timeout: tr.timeout });
      }
    } finally { await browser.close(); }
  }
}
await withServer(run);
process.exit(R.summary());
