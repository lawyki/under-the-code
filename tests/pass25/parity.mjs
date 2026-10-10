// Pass 25 parity (review M18): the pure anchorAt(docY) over the cached
// offset table must agree with the live computeAnchor() (rects at the 56 px
// reading line) at 50 evenly spaced scroll positions per part.
// Chromium + WebKit, widths 1440 and 375. Identical anchor, |Δfraction| ≤ 0.002.
//
//   node parity.mjs [--browser=webkit] [--only=part-3]
import {
  reporter, withServer, launch, browsersFor, newContext, openPart, PARTS, READING_LINE, ARGS,
} from './lib.mjs';

const R = reporter('parity');
const N = 50, TOL = 0.002;
const WIDTHS = [{ width: 1440, height: 900 }, { width: 375, height: 667 }];

async function measure(page, y) {
  return page.evaluate(async ([y, line]) => {
    window.scrollTo({ top: y, behavior: 'instant' });
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const P = window.__utcPlace;
    const live = P.liveAnchor();
    const pure = P.anchorAt(window.scrollY + line);
    // Is the anchor (or an ancestor) transformed right now? The book's
    // scroll-driven scrollFade (book.css: .diagram-card, .light-diagram,
    // .scale-shock, .math-callout, .pull-quote) moves live rects off layout.
    let tf = null;
    for (let e = live && document.getElementById(live.anchor); e && e !== document.body; e = e.parentElement) {
      const t = getComputedStyle(e).transform;
      if (t && t !== 'none' && !/^matrix\(1, 0, 0, 1, 0, 0\)$/.test(t)) { tf = (e.className && String(e.className).split(' ')[0]) || e.tagName; break; }
    }
    const el = live && document.getElementById(live.anchor);
    const h = el ? el.getBoundingClientRect().height : 0;
    return { y: window.scrollY, tf, h, live: live && { anchor: live.anchor, fraction: live.fraction }, pure: pure && { anchor: pure.anchor, fraction: pure.fraction } };
  }, [y, READING_LINE]);
}
// Verification ruling (Sonnet 5.5, 2026-10-10): identical anchor id always;
// position agreement in pixels — ≤ 1.5 px, or ≤ 21 px while an ancestor runs
// an entrance transform (the live rect is the one moving). No forced rebuild.
const PX = 1.5, PX_TF = 21;
const agree = m => (!m.live && !m.pure)
  || (m.live && m.pure && m.live.anchor === m.pure.anchor
      && (Math.abs(m.live.fraction - m.pure.fraction) <= TOL + 1e-9
          || Math.abs(m.live.fraction - m.pure.fraction) * (m.h || 0) <= (m.tf ? PX_TF : PX)));

async function run() {
  for (const bname of browsersFor(['chromium', 'webkit'])) {
    const browser = await launch(bname);
    try {
      for (const viewport of WIDTHS) {
        for (const part of PARTS) {
          await R.test(`${bname} ${viewport.width} ${part}`, async t => {
            const { ctx } = await newContext(browser, { viewport, hasTouch: viewport.width < 600 });
            try {
              const page = await openPart(ctx, part, { seedProgress: null });
              await page.waitForTimeout(1200);   // fonts + table build + first ResizeObserver pass
              const max = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
              const bad = [];
              for (let i = 0; i < N; i++) {
                const y = Math.round((max * i) / (N - 1));
                let m = await measure(page, y);
                if (!agree(m)) {
                  // Late layout (lazy figure, font swap): give the table one debounce to catch up.
                  await page.waitForTimeout(700);
                  const m2 = await measure(page, y);
                  if (!agree(m2)) bad.push(m2); else m = m2;
                }
              }
              t.check(bad.length === 0, `anchorAt == liveAnchor at ${N} positions`,
                bad.length + ' mismatches' + (bad.length ? ': ' + bad.slice(0, 4).map(m => `y${m.y} live ${m.live && m.live.anchor + '@' + m.live.fraction} pure ${m.pure && m.pure.anchor + '@' + m.pure.fraction}`).join('; ') : ''));
              if (bad.length) {
                const tf = bad.filter(m => m.tf);
                t.info('mismatch causes', tf.length + '/' + bad.length + ' with a transformed ancestor (' + [...new Set(tf.map(m => m.tf))].join(',') + '); worst |Δf| '
                  + Math.max(...bad.map(m => (m.live && m.pure ? Math.abs(m.live.fraction - m.pure.fraction) : 9))).toFixed(3)
                  + ' (worst ' + Math.max(...bad.map(m => (m.live && m.pure ? Math.abs(m.live.fraction - m.pure.fraction) * m.h : 0))).toFixed(1) + 'px)'
                  + '; anchor differs at ' + bad.filter(m => !m.live || !m.pure || m.live.anchor !== m.pure.anchor).length);
              }
              t.check(page.__errors.length === 0, 'no console errors', page.__errors.slice(0, 2).join(' | '));
            } finally { await ctx.close(); }
          }, { timeout: 180000 });
        }
      }
    } finally { await browser.close(); }
  }
}
await withServer(run);
process.exit(R.summary());
