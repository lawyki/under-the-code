// Pass 28 figure sweep (docs/pass-28-brief.md, law 3). Per figure, per width and
// engine: smallest rendered label (CSS px), label count, overlapping text boxes,
// text outside the viewBox, caption words. Measured, not eyeballed.
//   node figs.mjs [--part=part-1] [--fig=fig-1-10] [--widths=320,375,1440] [--browser=chromium|webkit] [--json=out.json]
import { chromium, webkit } from '/Users/yki/.npm/_npx/361ceb562f3b3235/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../../public/', import.meta.url).pathname;
const PARTS = ARGS.part ? [ARGS.part] : ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];
const WIDTHS = String(ARGS.widths || '320,360,375,1440').split(',').map(Number);
const ENGINES = ARGS.browser ? [ARGS.browser] : ['chromium', 'webkit'];
const MIN_PX = 11;

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

function measureFigs(only) {
  const out = [];
  for (const card of document.querySelectorAll('.diagram-card, .light-diagram')) {
    if (only && card.id !== only) continue;
    const svg = card.querySelector('svg'); if (!svg) continue;
    const label = (card.querySelector('.diagram-label') || {}).textContent || card.id;
    const sr = svg.getBoundingClientRect();
    const vb = svg.viewBox.baseVal; const scale = vb && vb.width ? sr.width / vb.width : 1;
    // what the reader sees now (the reduced-motion still): skip text faded out by an ancestor
    const shown = el => { let o = 1; for (let e = el; e && e !== svg.parentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; o *= parseFloat(cs.opacity); const a = e.getAttribute && e.getAttribute('opacity'); if (a !== null && e.tagName !== 'svg') o *= 1; } return o > 0.05; };
    const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && shown(t));
    const boxes = texts.map(t => { const b = t.getBoundingClientRect(); return { t: t.textContent.trim().slice(0, 40), x: b.left, y: b.top, w: b.width, h: b.height, fs: parseFloat(getComputedStyle(t).fontSize) }; });
    // rendered font size: CSS font-size of an SVG <text> is in user units; scale to screen
    const sizes = boxes.map(b => b.fs * scale);
    const minPx = sizes.length ? Math.min(...sizes) : null;
    const small = boxes.filter((b, i) => sizes[i] < 11).length;
    const overlaps = [];
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      if (a.t === b.t && Math.abs(a.x - b.x) < 2 && Math.abs(a.y - b.y) < 2) continue;   // the same label lit over itself
      // ink boxes: a font box carries ascent/descent padding, so trim 10% top and bottom (stacked lines of one label may touch boxes, never ink)
      const ay = a.y + a.h * 0.1, ah = a.h * 0.8, by_ = b.y + b.h * 0.1, bh = b.h * 0.8;
      const ix = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), iy = Math.min(ay + ah, by_ + bh) - Math.max(ay, by_);
      if (ix > 1 && iy > 1 && ix * iy > 0.03 * Math.min(a.w * a.h, b.w * b.h)) overlaps.push(a.t + ' × ' + b.t);
    }
    const outside = boxes.filter(b => b.x < sr.left - 1 || b.y < sr.top - 1 || b.x + b.w > sr.right + 1 || b.y + b.h > sr.bottom + 1).map(b => b.t);
    // spill: a label whose centre sits in a shape must fit inside that shape (the smallest one holding its centre)
    // .fx marks a moving overlay (a highlight, a spreading fill), not a container
    const shapes = [...svg.querySelectorAll('rect, circle, ellipse, polygon')].filter(r => shown(r) && !r.closest('.fx') && r.getAttribute('fill') !== 'none'
      && !/^(0|0\.0+)$/.test(r.getAttribute('fill-opacity') || '1')).map(r => r.getBoundingClientRect()).filter(b => b.width > 4 && b.height > 4 && b.width < sr.width * 0.9);
    const spill = [];
    boxes.forEach(b => {
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
      const hold = shapes.filter(r => cx > r.left && cx < r.right && cy > r.top && cy < r.bottom).sort((p, q) => p.width * p.height - q.width * q.height)[0];
      if (hold && (b.x < hold.left - 1 || b.x + b.w > hold.right + 1 || b.y < hold.top - 1.5 || b.y + b.h > hold.bottom + 1.5)) spill.push(b.t);
    });
    const cap = card.querySelector('.diagram-caption');
    const capWords = cap ? cap.textContent.trim().split(/\s+/).length : 0;
    const svgWords = texts.reduce((n, t) => n + t.textContent.trim().split(/\s+/).length, 0);
    out.push({ id: card.id || '', label: label.trim().slice(0, 80), svgW: Math.round(sr.width), scale: +scale.toFixed(3), labels: texts.length, svgWords, minPx: minPx && +minPx.toFixed(1), small, overlaps, outside, spill, capWords });
  }
  return out;
}

const results = [];
for (const eng of ENGINES) {
  const browser = await (eng === 'webkit' ? webkit : chromium).launch();
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
    for (const part of PARTS) {
      const page = await ctx.newPage();
      await page.goto(`http://localhost:${PORT}/${part}`); await page.waitForTimeout(800);
      await page.evaluate(() => document.fonts && document.fonts.ready);
      // --times=0,1.5,3: also judge frames mid-animation (labels that only appear in motion)
      for (const t of String(ARGS.times || '0').split(',').map(Number)) {
        await page.evaluate(t => document.querySelectorAll('.diagram-card svg, .light-diagram svg').forEach(s => { if (s.setCurrentTime) { s.pauseAnimations(); s.setCurrentTime(t); } }), t);
        await page.waitForTimeout(60);
        const r = await page.evaluate(measureFigs, ARGS.fig || null);
        for (const f of r) results.push({ eng, w, part, t, ...f });
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
}
server.close();
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify(results, null, 1));
// legibility is judged from 360 px up (the smallest common phone); 320 must still not clip or overlap
const fail = f => (f.w >= 360 && f.minPx < MIN_PX) || f.overlaps.length || f.outside.length || f.spill.length || f.capWords > 60;
for (const f of results) if (ARGS.fig || ARGS.verbose || fail(f))
  console.log(`${fail(f) ? 'FAIL' : 'ok  '} ${f.eng} ${f.w} ${f.id}${f.t ? ' t' + f.t : ''} min ${f.minPx}px small ${f.small}/${f.labels} words ${f.svgWords} cap ${f.capWords}${f.overlaps.length ? ' overlaps ' + f.overlaps.length + ' [' + f.overlaps.slice(0, 2).join('; ') + ']' : ''}${f.outside.length ? ' outside ' + f.outside.length + ' [' + f.outside.slice(0, 2).join('; ') + ']' : ''}${f.spill.length ? ' spill ' + f.spill.length + ' [' + f.spill.slice(0, 3).join('; ') + ']' : ''}`);
const n = results.length, bad = results.filter(fail).length;
console.log(`figs: ${bad}/${n} fail (min label ${MIN_PX}px from 360, no overlap, inside viewBox, inside its shape, caption ≤ 60 words)`);
process.exit(bad ? 1 : 0);
