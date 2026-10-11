// Pass 28 book-wide no-clipping sweep (docs/pass-28-brief.md, "Last, after every figure is done"). Per page, width
// and engine, every visible text run outside the figures' SVGs (figs.mjs measures those) is checked for:
//   cut       extends past the padding box of an ancestor with overflow hidden/clip
//   offpage   extends past the viewport edge without a scrolling ancestor to hold it
//   overlap   intersects another text run (different node, not fixed against flow)
// plus page-level horizontal overflow. Measured, not eyeballed. Zero findings is the bar.
//   node clip.mjs [--pages=part-1,index] [--widths=320,375,768,1024,1440] [--browser=chromium|webkit] [--json=out.json] [--state=menu]
import { chromium, webkit } from '/Users/yki/.npm/_npx/361ceb562f3b3235/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../../public/', import.meta.url).pathname;
const PAGES = String(ARGS.pages || 'index,part-1,part-2,part-3,part-4,part-5,glossary,account,404').split(',');
const WIDTHS = String(ARGS.widths || '320,375,768,1024,1440').split(',').map(Number);
const ENGINES = ARGS.browser ? [ARGS.browser] : ['chromium', 'webkit'];

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

function measure() {
  const W = innerWidth, out = { scrollWidth: document.documentElement.scrollWidth, innerWidth: W, cut: [], offpage: [], overlap: [] };
  const cs = new Map(); const st = e => { let s = cs.get(e); if (!s) { s = getComputedStyle(e); cs.set(e, s); } return s; };
  const hidden = e => { for (; e && e.nodeType === 1; e = e.parentElement) { const s = st(e); if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) return true; } return false; };
  const pathOf = e => { const p = []; for (; e && e.nodeType === 1 && p.length < 4; e = e.parentElement) p.unshift(e.tagName.toLowerCase() + (e.id ? '#' + e.id : e.classList[0] ? '.' + e.classList[0] : '')); return p.join(' > '); };
  const runs = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => {
    if (!n.textContent.trim()) return NodeFilter.FILTER_REJECT;
    const p = n.parentElement; if (!p || p.closest('svg, script, style, noscript, template')) return NodeFilter.FILTER_REJECT;
    return NodeFilter.FILTER_ACCEPT; } });
  const rng = document.createRange();
  let fixedOf = new Map();
  const fixedRoot = e => { if (fixedOf.has(e)) return fixedOf.get(e); let r = null; for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const p = st(x).position; if (p === 'fixed' || p === 'sticky' || x.matches('.glossary-tip, [popover], [role=tooltip], [role=menu], [role=dialog]')) { r = x; break; } } fixedOf.set(e, r); return r; };
  for (let n; (n = walker.nextNode());) {
    const p = n.parentElement; if (hidden(p)) continue;
    const det = p.closest('details:not([open])'); if (det && !p.closest('summary')) continue;   // closed details: not rendered
    rng.selectNodeContents(n);
    let rects = [...rng.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    if (!rects.length) continue;
    const own = rects;
    // clipping and scrolling ancestors
    let scroller = false, cutBy = null, cutBox = null;
    // containing-block escape: a fixed box ignores ancestors' overflow (unless one holds it via transform/filter/contain);
    // an absolute box ignores unpositioned ancestors' overflow up to its containing block
    let esc = null;
    for (let a = p; a && a !== document.documentElement; a = a.parentElement) {
      const s = st(a);
      if (esc) {
        const holds = s.transform !== 'none' || s.filter !== 'none' || /paint|layout|strict|content/.test(s.contain) || s.perspective !== 'none';
        if (esc === 'fixed' && !holds) continue;
        if (esc === 'abs' && s.position === 'static' && !holds) continue;
        esc = null;
      }
      const escNext = s.position === 'fixed' ? 'fixed' : s.position === 'absolute' ? 'abs' : null;
      const ox = s.overflowX, oy = s.overflowY;
      if (/auto|scroll/.test(ox + oy)) { scroller = true; rects = [a.getBoundingClientRect()]; if (escNext) esc = escNext; continue; }   // scrollable: the box must fit, not its content
      if (/hidden|clip/.test(ox) || /hidden|clip/.test(oy)) {
        const b = a.getBoundingClientRect();
        if (b.width <= 2 || b.height <= 2) { cutBy = 'sr'; break; }   // visually-hidden pattern: intentional
        const box = { l: b.left + a.clientLeft, t: b.top + a.clientTop, r: b.left + a.clientLeft + a.clientWidth, b: b.top + a.clientTop + a.clientHeight, hx: /hidden|clip/.test(ox), hy: /hidden|clip/.test(oy) };
        for (const r of rects) {
          if ((box.hx && (r.left < box.l - 1 || r.right > box.r + 1)) || (box.hy && (r.top < box.t - 1 || r.bottom > box.b + 1))) { cutBy = a; cutBox = box; break; }
        }
        if (cutBy) break;
      }
      if (escNext) esc = escNext;
    }
    const text = n.textContent.trim().replace(/\s+/g, ' ').slice(0, 50);
    if (cutBy && cutBy !== 'sr') {
      const r = rects.find(r => r.left < cutBox.l - 1 || r.right > cutBox.r + 1 || r.top < cutBox.t - 1 || r.bottom > cutBox.b + 1);
      out.cut.push({ text, at: pathOf(p), by: pathOf(cutBy), dx: Math.round(Math.max(cutBox.l - r.left, r.right - cutBox.r, 0)), dy: Math.round(Math.max(cutBox.t - r.top, r.bottom - cutBox.b, 0)) });
    }
    if (cutBy === 'sr') continue;
    rects = own;
    if (!scroller && rects.some(r => r.left < -1 || r.right > W + 1)) out.offpage.push({ text, at: pathOf(p), l: Math.round(Math.min(...rects.map(r => r.left))), r: Math.round(Math.max(...rects.map(r => r.right))) });
    const fr = fixedRoot(p);
    for (const r of rects) runs.push({ n, p, fr, text, l: r.left, r: r.right, t: r.top + scrollY, b: r.bottom + scrollY });
  }
  // overlaps: bucket by 40 px bands of page y
  const band = new Map();
  runs.forEach((r, i) => { for (let y = Math.floor(r.t / 40); y <= Math.floor(r.b / 40); y++) { (band.get(y) || band.set(y, []).get(y)).push(i); } });
  const seen = new Set();
  for (const ids of band.values()) for (let x = 0; x < ids.length; x++) for (let y = x + 1; y < ids.length; y++) {
    const A = runs[ids[x]], B = runs[ids[y]];
    if (A.n === B.n || A.fr !== B.fr) continue;
    const iw = Math.min(A.r, B.r) - Math.max(A.l, B.l), ih = Math.min(A.b, B.b) - Math.max(A.t, B.t);
    if (iw <= 2 || ih <= 0.4 * Math.min(A.b - A.t, B.b - B.t)) continue;
    const k = ids[x] < ids[y] ? ids[x] + ':' + ids[y] : ids[y] + ':' + ids[x]; if (seen.has(k)) continue; seen.add(k);
    out.overlap.push({ a: A.text, b: B.text, at: pathOf(A.p), with: pathOf(B.p), iw: Math.round(iw), ih: Math.round(ih) });
  }
  return out;
}

// interactive states (--state=bar|menu|tip|fs); default: the page as loaded
const STATE = ARGS.state || '';
async function stateRuns(page, pg) {
  const part = /^part-/.test(pg);
  if (!STATE) return [['', await page.evaluate(measure)]];
  if (!part) return [];
  const mid = async () => { await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.3)); await page.waitForTimeout(400); };
  if (STATE === 'bar') {
    await mid();
    if (!(await page.$('.place-btn'))) return [[' [no place-btn]', await page.evaluate(measure)]];
    await page.click('.place-btn'); await page.waitForTimeout(500);
    return [[' [bar]', await page.evaluate(measure)]];
  }
  if (STATE === 'menu') {
    await mid();
    const ok = await page.evaluate(() => { const y = scrollY; const d = [...document.querySelectorAll('.mark-dot')].find(e => e.getBoundingClientRect().top > 60); if (!d) return false; d.scrollIntoView({ block: 'center' }); d.click(); return true; });
    await page.waitForTimeout(500);
    return [[ok ? ' [menu]' : ' [no mark-dot]', await page.evaluate(measure)]];
  }
  if (STATE === 'tip') {
    await mid();
    const sel = await page.evaluate(() => { const e = [...document.querySelectorAll('.glossary-ref')].find(e => e.getBoundingClientRect().top > 0) || document.querySelector('.glossary-ref'); if (!e) return null; e.scrollIntoView({ block: 'center' }); e.setAttribute('data-clip-tip', ''); return '[data-clip-tip]'; });
    if (!sel) return [[' [no glossary-ref]', await page.evaluate(measure)]];
    await page.hover(sel); await page.waitForTimeout(600);
    return [[' [tip]', await page.evaluate(measure)]];
  }
  if (STATE === 'fs') {
    const ids = await page.evaluate(() => [...document.querySelectorAll('.diagram-card .fs-button, .light-diagram .fs-button')].map(b => b.closest('[id]').id));
    const outs = [];
    for (const id of ids) {
      await page.evaluate(id => document.getElementById(id).scrollIntoView({ block: 'center' }), id);
      await page.evaluate(id => document.querySelector(`#${id} .fs-button`).click(), id); await page.waitForTimeout(450);
      const m = await page.evaluate(measure);
      outs.push([` [fs ${id}]`, m]);
      await page.keyboard.press('Escape'); await page.waitForTimeout(350);
    }
    return outs;
  }
  return [];
}

const all = []; let fails = 0;
for (const eng of ENGINES) {
  const browser = await (eng === 'webkit' ? webkit : chromium).launch();
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    for (const pg of PAGES) {
      await page.goto(`http://localhost:${PORT}/${pg === 'index' ? '' : pg}`, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(150);
      const ms = await stateRuns(page, pg);
      for (const [label, m] of ms) {
      const hs = m.scrollWidth > m.innerWidth;
      const n = m.cut.length + m.offpage.length + m.overlap.length + (hs ? 1 : 0);
      fails += n;
      console.log(`${eng} ${w} ${pg}${label}: ${n ? 'FAIL' : 'ok'}  cut ${m.cut.length} · offpage ${m.offpage.length} · overlap ${m.overlap.length}${hs ? ` · hscroll ${m.scrollWidth}>${m.innerWidth}` : ''}`);
      if (n && ARGS.v) for (const k of ['cut', 'offpage', 'overlap']) for (const f of m[k].slice(0, 8)) console.log('   ', k, JSON.stringify(f));
      all.push({ eng, w, page: pg + label, ...m });
      }
      continue;
      const m = await page.evaluate(measure);
      const hs = m.scrollWidth > m.innerWidth;
      const n = m.cut.length + m.offpage.length + m.overlap.length + (hs ? 1 : 0);
      fails += n;
      console.log(`${eng} ${w} ${pg}: ${n ? 'FAIL' : 'ok'}  cut ${m.cut.length} · offpage ${m.offpage.length} · overlap ${m.overlap.length}${hs ? ` · hscroll ${m.scrollWidth}>${m.innerWidth}` : ''}`);
      if (n && ARGS.v) for (const k of ['cut', 'offpage', 'overlap']) for (const f of m[k].slice(0, 8)) console.log('   ', k, JSON.stringify(f));
      all.push({ eng, w, page: pg, ...m });
    }
    await ctx.close();
  }
  await browser.close();
}
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify(all, null, 1));
console.log(`clip: ${fails} finding${fails === 1 ? '' : 's'}`);
server.close();
process.exit(fails ? 1 : 0);
