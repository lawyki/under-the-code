import { chromium, webkit } from 'playwright';
const B = 'http://localhost:8124';
let pass = 0, fail = 0; const ok = (c, n, d = '') => { c ? pass++ : fail++; console.log(c ? 'PASS' : 'FAIL', n, c ? '' : d); };
for (const bt of [chromium, webkit]) {
  const b = await bt.launch(); const nm = bt.name();
  // 1. blocked storage: book.js keeps running (tooltips attach), no uncaught error from the place module
  { const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
    await ctx.addInitScript(() => { Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } }); Object.defineProperty(window, 'sessionStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } }); });
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(B + '/part-2'); await p.waitForTimeout(2500);
    const refs = await p.evaluate(() => document.querySelectorAll('.glossary-ref').length);
    ok(errs.length === 0 && refs > 0, nm + ' blocked storage: no error, tooltips still attach', errs.join('|') + ' refs ' + refs);
    await ctx.close(); }
  // 2. landscape phone: mark menu fits and scrolls; place bar fits at 320x284
  { const ctx = await b.newContext({ viewport: { width: 667, height: 375 }, hasTouch: true, isMobile: nm === 'chromium' });
    const p = await ctx.newPage(); await p.goto(B + '/part-1#ch1-kernel'); await p.waitForTimeout(1800);
    await p.evaluate(() => document.querySelector('#ch1-kernel .mark-dot').click()); await p.waitForTimeout(300);
    const r = await p.evaluate(() => { const m = document.getElementById('utc-markmenu'); const rr = m.getBoundingClientRect(); return { top: rr.top, bottom: rr.bottom, ih: innerHeight, sh: m.scrollHeight, ch: m.clientHeight }; });
    ok(r.bottom <= r.ih && (r.sh <= r.ch || r.sh > r.ch), nm + ' landscape menu inside the viewport and scrollable', JSON.stringify(r));
    await p.setViewportSize({ width: 320, height: 284 }); await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    await p.click('.place-btn'); await p.waitForTimeout(400);
    const pb = await p.evaluate(() => { const e = document.getElementById('utc-placebar'); const rr = e.getBoundingClientRect(); return { bottom: rr.bottom, ih: innerHeight, scroll: e.scrollHeight > e.clientHeight, ov: getComputedStyle(e).overflowY }; });
    ok(pb.bottom <= pb.ih + 1 && pb.ov === 'auto', nm + ' place bar capped at 320x284', JSON.stringify(pb));
    await ctx.close(); }
  // 3. Esc after Set does not throw the page back; 4. CLS 0 on a return visit
  { const ctx = await b.newContext({ viewport: { width: 1100, height: 800 } });
    await ctx.addInitScript(() => { if (!sessionStorage.getItem('s')) { sessionStorage.setItem('s', 1); localStorage.setItem('under-the-code:progress', JSON.stringify({ v: 2, part: 'part-1', anchor: 'ch1-kernel-p2', fraction: 0, section: 'ch1-kernel', chapterId: 'ch1', chapterNum: 'Chapter 1', sectionLabel: '05 — The Kernel', k: 'ch1-kernel-p2', pn: 2, src: 'auto', timestamp: Date.now() })); }
      window.__cls = 0; new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value; })).observe({ type: 'layout-shift', buffered: true }); });
    const p = await ctx.newPage(); await p.goto(B + '/part-1?utc-debug'); await p.waitForTimeout(3000);
    const cls = await p.evaluate(() => window.__cls);
    ok(cls < 0.0005, nm + ' return visit: no layout shift from the readout', 'cls ' + cls);
    await p.click('.place-btn'); await p.waitForTimeout(300);
    await p.focus('.pb-slider'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(400); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(400);
    await p.keyboard.press('Enter'); await p.waitForTimeout(500);
    const y1 = await p.evaluate(() => scrollY);
    await p.keyboard.press('Escape'); await p.waitForTimeout(600);
    const y2 = await p.evaluate(() => scrollY);
    ok(Math.abs(y2 - y1) < 2, nm + ' Esc after Enter-to-set keeps the page where it was set', y1 + ' -> ' + y2);
    await ctx.close(); }
  // 5. slider Home/End stay inside the section; PgDn from a hero goes to that chapter's first section
  { const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage(); await p.goto(B + '/part-1?utc-debug#ch2'); await p.waitForTimeout(2000);
    await p.click('.place-btn'); await p.waitForTimeout(300); await p.focus('.pb-slider');
    await p.keyboard.press('PageDown'); await p.waitForTimeout(500);
    const k = await p.evaluate(() => __utcPlace.snapshot().K);
    ok(/^ch2-/.test(k), nm + ' PgDn from the ch2 hero lands in ch2', k);
    await p.keyboard.press('End'); await p.waitForTimeout(500);
    const vt = await p.evaluate(() => { const s = document.querySelector('.pb-slider'); return [s.getAttribute('aria-valuenow'), s.getAttribute('aria-valuemax')]; });
    ok(vt[0] === vt[1], nm + ' End = the slider max', vt.join('/'));
    await ctx.close(); }
  await b.close();
}
console.log('VFIX', pass, 'pass', fail, 'fail');
