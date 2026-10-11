// Pass 28 smoothness check (docs/pass-28-brief.md, "Last, after every figure is done"). Chromium, 4x CPU throttle.
// Per page and width: scroll the whole page one frame at a time (as a reader's scroll reaches the main thread: scroll
// handlers, figure starts and stops, the place tracker) and record frame intervals, long tasks and layout shifts;
// then hold a screen of animated figures for two seconds. Static audit: CSS transitions/animations on layout
// properties. Reduced motion: every figure's SMIL paused, no CSS animation running.
//   node smooth.mjs [--pages=part-1] [--widths=375,1440] [--rate=4]
import { chromium } from '../pass25/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../../public/', import.meta.url).pathname;
const PAGES = String(ARGS.pages || 'index,part-1,part-2,part-3,part-4,part-5,glossary').split(',');
const WIDTHS = String(ARGS.widths || '375,1440').split(',').map(Number);
const RATE = Number(ARGS.rate || 4);
const FRAME = 1000 / 60;

const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.png': 'image/png' };
const server = http.createServer((q, r) => {
  let u = decodeURIComponent(new URL(q.url, 'http://x').pathname);
  if (u.startsWith('/api/')) { r.writeHead(404); return r.end('{}'); }
  let f = path.join(ROOT, u === '/' ? 'index.html' : u);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html';
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end('nf'); }
  r.writeHead(200, { 'Content-Type': T[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
await new Promise(r => server.listen(0, r));
const PORT = server.address().port;

const OBSERVE = () => {
  window.__lt = []; window.__ls = [];
  new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lt.push({ d: Math.round(e.duration), t: Math.round(e.startTime) }); }).observe({ type: 'longtask', buffered: false });
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__ls.push({ v: e.value, t: Math.round(e.startTime), src: (e.sources || []).map(s => s.node && (s.node.id || s.node.className || s.node.nodeName)).slice(0, 3) }); }).observe({ type: 'layout-shift', buffered: false });
};
// scroll the page top to bottom, one step per animation frame; returns the frame intervals
const SCROLL = async step => {
  const ivs = []; let last = performance.now();
  const max = document.documentElement.scrollHeight - innerHeight;
  window.scrollTo(0, 0);
  await new Promise(r => requestAnimationFrame(r)); last = performance.now();
  for (let y = 0; y < max; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => requestAnimationFrame(r));
    const now = performance.now(); ivs.push(now - last); last = now;
  }
  return ivs;
};
const HOLD = async ms => {   // frames while animated figures are on screen
  const ivs = []; let last = performance.now(); const end = last + ms;
  while (performance.now() < end) { await new Promise(r => requestAnimationFrame(r)); const now = performance.now(); ivs.push(now - last); last = now; }
  return ivs;
};
const stats = ivs => {
  const s = [...ivs].sort((a, b) => a - b);
  const pct = p => s[Math.min(s.length - 1, Math.floor(p * s.length))] || 0;
  const dropped = ivs.filter(v => v > FRAME * 1.5).length;
  return { frames: ivs.length, p50: +pct(0.5).toFixed(1), p95: +pct(0.95).toFixed(1), max: +Math.max(0, ...ivs).toFixed(1), dropped, droppedPct: +(100 * dropped / Math.max(1, ivs.length)).toFixed(1) };
};

const browser = await chromium.launch();
const report = []; let fails = 0;
for (const w of WIDTHS) for (const pg of PAGES) {
  const ctx = await browser.newContext({ viewport: { width: w, height: w < 600 ? 780 : 900 } });
  const page = await ctx.newPage();
  await page.route(/^https?:\/\/(?!localhost)/, r => r.abort());
  const cdp = await ctx.newCDPSession(page);
  await page.goto(`http://localhost:${PORT}/${pg === 'index' ? '' : pg}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  if (!ARGS.noobs) await page.evaluate(OBSERVE); else await page.evaluate(() => { window.__lt = []; window.__ls = []; });
  // measured once the page has settled (1.2 s): the first second after load is initial raster, which headless
  // Chromium does in software and which says nothing about the page's own work
  await page.waitForTimeout(Number(ARGS.wait ?? 1200));
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: RATE });
  const scroll = stats(await page.evaluate(SCROLL, w < 600 ? 60 : 90));
  // a screen with an animated figure in it
  await page.evaluate(() => { const f = [...document.querySelectorAll('.fig-v2 svg')].find(s => s.querySelector('animate, animateTransform')); if (f) f.scrollIntoView({ block: 'center' }); });
  await page.waitForTimeout(300);
  const hold = stats(await page.evaluate(HOLD, 2000));
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
  const { lt, ls } = await page.evaluate(() => ({ lt: window.__lt, ls: window.__ls }));
  const cls = +ls.reduce((a, e) => a + e.v, 0).toFixed(4);
  const bad = (scroll.p95 > FRAME * 1.5 ? 1 : 0) + (hold.p95 > FRAME * 1.5 ? 1 : 0) + lt.length + (cls > 0.001 ? 1 : 0);
  fails += bad;
  console.log(`${w} ${pg}: ${bad ? 'FAIL' : 'ok'}  scroll p50 ${scroll.p50} p95 ${scroll.p95} max ${scroll.max} dropped ${scroll.droppedPct}% · figures p95 ${hold.p95} dropped ${hold.droppedPct}% · long tasks ${lt.length}${lt.length ? ' (' + lt.slice(0, 5).map(e => e.d + 'ms').join(' ') + ')' : ''} · CLS ${cls}`);
  if (ARGS.v && ls.length) console.log('   shifts', JSON.stringify(ls.slice(0, 5)));
  report.push({ w, page: pg, scroll, hold, lt, cls, ls: ls.slice(0, 10) });
  await ctx.close();
}

// reduced motion: figures paused, no CSS animation running
{
  const ctx = await browser.newContext({ viewport: { width: 375, height: 780 }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  for (const pg of PAGES.filter(p => /^part-/.test(p))) {
    await page.goto(`http://localhost:${PORT}/${pg}`, { waitUntil: 'load' });
    await page.waitForTimeout(400);
    const r = await page.evaluate(async () => {
      const figs = [...document.querySelectorAll('.diagram-card svg, .light-diagram svg')].filter(s => s.querySelector('animate, animateTransform, animateMotion, set'));
      const running = [];
      for (const s of figs) { s.closest('[id]').scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 30)); if (!s.animationsPaused()) running.push(s.closest('[id]').id); }
      const anims = document.getAnimations().filter(a => a.playState === 'running').map(a => (a.animationName || a.transitionProperty || 'anim') + '@' + ((a.effect && a.effect.target && (a.effect.target.id || a.effect.target.className)) || ''));
      return { figs: figs.length, running, anims: anims.slice(0, 10), nAnims: anims.length, smooth: getComputedStyle(document.documentElement).scrollBehavior };
    });
    const bad = r.running.length + r.nAnims + (r.smooth === 'smooth' ? 1 : 0);
    fails += bad;
    console.log(`reduced-motion ${pg}: ${bad ? 'FAIL' : 'ok'}  ${r.figs} animated figures, still running ${r.running.length}${r.running.length ? ' (' + r.running.slice(0, 6).join(' ') + ')' : ''} · CSS animations running ${r.nAnims}${r.nAnims ? ' (' + r.anims.join(' ') + ')' : ''} · scroll-behavior ${r.smooth}`);
  }
  await ctx.close();
}
await browser.close();

// static audit: transitions and keyframe animations on layout properties
const LAYOUT = /^(all|width|height|min-width|max-width|min-height|max-height|top|left|right|bottom|inset|margin(-[a-z]+)?|padding(-[a-z]+)?|border(-[a-z]+)?-width|font-size|line-height|letter-spacing|grid-template[a-z-]*|flex|flex-basis|flex-grow|flex-shrink|gap|background-size|background-position)$/;
let audit = 0;
for (const f of fs.readdirSync(ROOT).filter(f => f.endsWith('.css'))) {
  const css = fs.readFileSync(path.join(ROOT, f), 'utf8');
  for (const m of css.matchAll(/transition(?:-property)?\s*:\s*([^;}]+)/g)) {
    const props = m[1].split(',').map(p => p.trim().split(/\s+/)[0]);
    const bad = props.filter(p => LAYOUT.test(p));
    if (bad.length) { audit++; const line = css.slice(0, m.index).split('\n').length; console.log(`transition ${f}:${line}: ${bad.join(', ')}`); }
  }
  for (const m of css.matchAll(/@keyframes\s+([\w-]+)\s*\{([\s\S]*?\})\s*\}/g)) {
    const props = [...m[2].matchAll(/([a-z-]+)\s*:/g)].map(x => x[1]).filter(p => LAYOUT.test(p));
    if (props.length) { audit++; const line = css.slice(0, m.index).split('\n').length; console.log(`keyframes ${f}:${line} ${m[1]}: ${[...new Set(props)].join(', ')}`); }
  }
}
fails += audit;
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify(report, null, 1));
console.log(`smooth: ${fails} finding${fails === 1 ? '' : 's'}`);
server.close();
process.exit(fails ? 1 : 0);
