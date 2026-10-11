// Pass 28 book-wide no-clipping sweep (docs/pass-28-brief.md, "Last, after every figure is done"), extended for Pass 30
// Gate 1 (docs/pass-29-30-brief.md). Per page, width and engine, every visible text run outside the figures' SVGs
// (figs.mjs measures those) is checked for:
//   cut       extends past the padding box of an ancestor with overflow hidden/clip
//   offpage   extends past the viewport edge without a scrolling ancestor to hold it
//   overlap   intersects another text run (different node, not fixed against flow)
//   scroll    an overflow auto/scroll container whose content overflows it with visible text out of view (HTML text, or
//             SVG <text> of a picture inside it); allowed only when listed in docs/pass-30-exceptions.json scroll_containers
// plus page-level horizontal overflow (hscroll). Measured, not eyeballed. Zero findings is the bar.
// Runs: plain (default), --textsize=200 (root font-size 200 %, WCAG 1.4.4; 768 px and wider only), --spacing (WCAG 1.4.12
// text-spacing override on page text). Each given mode is its own run, and composes with --state.
// Scroll-driven reveals are cancelled before measuring: every element is measured at rest, as the reader meets it.
//   node clip.mjs [--pages=part-1,index] [--widths=320,360,375,768,1024,1440] [--browser=chromium|webkit] [--json=out.json]
//                 [--state=bar|menu|tip|fs|open] [--textsize=200] [--spacing] [--v]
import { chromium, webkit } from '../pass25/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../../public/', import.meta.url).pathname;
const PAGES = String(ARGS.pages || 'index,part-1,part-2,part-3,part-4,part-5,glossary,account,404').split(',');
const WIDTHS = String(ARGS.widths || '320,360,375,768,1024,1440').split(',').map(Number);
const ENGINES = ARGS.browser ? [ARGS.browser] : ['chromium', 'webkit'];
const T0 = Date.now();

// the only skip this tool knows: containers that scroll on purpose, by id or "<page>|<css selector>" (Gate 1 adds them)
let SCROLL_IDS = [];
try { SCROLL_IDS = JSON.parse(fs.readFileSync(new URL('../../docs/pass-30-exceptions.json', import.meta.url), 'utf8')).scroll_containers?.ids || []; }
catch (e) { console.log(`note: docs/pass-30-exceptions.json unreadable (${e.message}); no scroll container is listed`); }

// WCAG 1.4.12 text spacing on page text, never inside an SVG (figure text is drawn, not reflowed)
const SPACING_CSS = `body, body *:not(svg):not(svg *) { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; }
body p:not(svg *) { margin-bottom: 2em !important; }`;
const TEXT_PCT = ARGS.textsize === true ? 200 : Number(ARGS.textsize);
if (ARGS.textsize && !(TEXT_PCT > 0)) { console.log(`clip: bad --textsize=${ARGS.textsize} (a percentage, e.g. 200)`); process.exit(2); }
const settle = page => page.evaluate(async () => { void document.body.offsetHeight; await document.fonts.ready; await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); });
const MODES = [];
if (ARGS.textsize) MODES.push({ label: ` [text ${TEXT_PCT}%]`, min: 768, apply: async page => {
  await page.evaluate(v => { document.documentElement.style.fontSize = v; }, TEXT_PCT + '%'); await settle(page); await page.waitForTimeout(250); } });
// letter- and word-spacing inherit: each outermost <svg> is pinned to its own computed values first, so the override
// cannot leak into figure text through inheritance. Exact values, as the WCAG F104 test procedure sets them, even where the
// page is spaced wider at rest: layout is not monotonic (a flex row that wraps under wider spacing cuts text under these
// values; part-4 #ch14 .sr-redact at 360 px), and the rest values are the plain run's.
if (ARGS.spacing) MODES.push({ label: ' [spacing]', min: 0, apply: async page => {
  await page.evaluate(css => {
    const keep = [...document.querySelectorAll('svg:not(svg svg)')].map(s => { const c = getComputedStyle(s); return [s, c.letterSpacing, c.wordSpacing]; });
    const el = document.createElement('style'); el.textContent = css; document.head.appendChild(el);
    for (const [s, l, w] of keep) { s.style.setProperty('letter-spacing', l); s.style.setProperty('word-spacing', w); }
  }, SPACING_CSS);
  await settle(page); await page.waitForTimeout(250); } });
if (!MODES.length) MODES.push({ label: '', min: 0, apply: null });

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

function measure({ pg, scrollIds }) {
  const W = innerWidth, out = { scrollWidth: document.documentElement.scrollWidth, innerWidth: W, cut: [], offpage: [], overlap: [], scroll: [], scrollListed: 0, warn: [], idsFound: [] };
  const cs = new Map(); const st = e => { let s = cs.get(e); if (!s) { s = getComputedStyle(e); cs.set(e, s); } return s; };
  const hidden = e => { for (; e && e.nodeType === 1; e = e.parentElement) { const s = st(e); if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) return true; } return false; };
  const pathOf = e => { const p = []; for (; e && e.nodeType === 1 && p.length < 4; e = e.parentElement) p.unshift(e.tagName.toLowerCase() + (e.id ? '#' + e.id : e.classList[0] ? '.' + e.classList[0] : '')); return p.join(' > '); };
  // a selector that names one element, for a "<page>|<selector>" exceptions entry: the nearest id plus tag.class when that
  // is unique (it survives a sibling inserted by a prose edit), else the positional chain
  const selOf = e => { if (e.id) return '#' + CSS.escape(e.id);
    let a = e.parentElement; while (a && a !== document.body && !a.id) a = a.parentElement;
    const anc = `${a && a.id ? '#' + CSS.escape(a.id) : 'body'} ${e.tagName.toLowerCase()}${e.classList[0] ? '.' + CSS.escape(e.classList[0]) : ''}`;
    if (document.querySelectorAll(anc).length === 1) return anc;
    const p = []; for (; e && e !== document.body; e = e.parentElement) {
    if (e.id) { p.unshift('#' + CSS.escape(e.id)); return p.join(' > '); }
    let k = 1; for (let s = e.previousElementSibling; s; s = s.previousElementSibling) if (s.tagName === e.tagName) k++;
    p.unshift(e.tagName.toLowerCase() + (e.classList[0] ? '.' + CSS.escape(e.classList[0]) : '') + `:nth-of-type(${k})`); } return ['body', ...p].join(' > '); };
  // body's overflow-x:hidden propagates to the viewport and leaves body's computed overflow-y 'auto'; read as a scrolling
  // ancestor it held every in-flow run and silenced offpage. The viewport is the document scroller (hscroll and offpage
  // measure it), so the climb stops below <body> whenever body's overflow is the one that propagates.
  const hst = st(document.documentElement);
  const docTop = hst.overflowX === 'visible' && hst.overflowY === 'visible' ? document.body : document.documentElement;
  // scrollport of a scrolling box and the axes on which its content overflows it
  const ports = new Map();
  const portOf = a => { let P = ports.get(a); if (P) return P; const b = a.getBoundingClientRect(), s = st(a), l = b.left + a.clientLeft, t = b.top + a.clientTop;
    P = { l, t, r: l + a.clientWidth, b: t + a.clientHeight, x: /auto|scroll/.test(s.overflowX) && a.scrollWidth > a.clientWidth + 1, y: /auto|scroll/.test(s.overflowY) && a.scrollHeight > a.clientHeight + 1 };
    ports.set(a, P); return P; };
  const outside = (q, P) => (P.x && (q.left < P.l - 1 || q.right > P.r + 1)) || (P.y && (q.top < P.t - 1 || q.bottom > P.b + 1));
  // clipping and scrolling ancestors of a run with client rects `rects`, from element p up
  const climb = (p, rects) => {
    let scroller = false, cutBy = null, cutBox = null; const hits = [];
    // containing-block escape: a fixed box ignores ancestors' overflow (unless one holds it via transform/filter/contain);
    // an absolute box ignores unpositioned ancestors' overflow up to its containing block
    let esc = null;
    for (let a = p; a && a !== docTop && a !== document.documentElement; a = a.parentElement) {
      const s = st(a);
      if (esc) {
        const holds = s.transform !== 'none' || s.filter !== 'none' || /paint|layout|strict|content/.test(s.contain) || s.perspective !== 'none';
        if (esc === 'fixed' && !holds) continue;
        if (esc === 'abs' && s.position === 'static' && !holds) continue;
        esc = null;
      }
      const escNext = s.position === 'fixed' ? 'fixed' : s.position === 'absolute' ? 'abs' : null;
      const ox = s.overflowX, oy = s.overflowY;
      if (/auto|scroll/.test(ox + oy)) {   // scrollable: the box must fit, not its content
        scroller = true;
        const P = portOf(a); if ((P.x || P.y) && rects.some(q => outside(q, P))) hits.push(a);   // the run is out of view until scrolled
        // overflow-x:hidden computes overflow-y:auto (and the reverse): the hidden axis still cuts (no sr skip here; that
        // rule stays where it was, on boxes with no scrolling axis)
        const hx = /hidden|clip/.test(ox), hy = /hidden|clip/.test(oy);
        if ((hx || hy) && rects.some(r => (hx && (r.left < P.l - 1 || r.right > P.r + 1)) || (hy && (r.top < P.t - 1 || r.bottom > P.b + 1)))) {
          cutBy = a; cutBox = { l: P.l, t: P.t, r: P.r, b: P.b, hx, hy }; break; }
        rects = [a.getBoundingClientRect()]; if (escNext) esc = escNext; continue;
      }
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
    return { scroller, cutBy, cutBox, rects, hits };
  };
  const scr = new Map();   // scroll container -> first out-of-view text, out-of-view run count
  const hit = (a, text) => { const v = scr.get(a); if (v) v.n++; else scr.set(a, { text, n: 1 }); };
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
    const own = [...rng.getClientRects()].filter(r => r.width > 0.5 && r.height > 0.5);
    if (!own.length) continue;
    const { scroller, cutBy, cutBox, rects, hits } = climb(p, own);
    const text = n.textContent.trim().replace(/\s+/g, ' ').slice(0, 50);
    if (cutBy && cutBy !== 'sr') {
      // the rect past a clipping axis (a mixed box's scrolling axis is the scroll check's, not a cut)
      const r = rects.find(r => (cutBox.hx && (r.left < cutBox.l - 1 || r.right > cutBox.r + 1)) || (cutBox.hy && (r.top < cutBox.t - 1 || r.bottom > cutBox.b + 1)));
      out.cut.push({ text, at: pathOf(p), by: pathOf(cutBy), dx: cutBox.hx ? Math.round(Math.max(cutBox.l - r.left, r.right - cutBox.r, 0)) : 0, dy: cutBox.hy ? Math.round(Math.max(cutBox.t - r.top, r.bottom - cutBox.b, 0)) : 0 });
    }
    if (cutBy === 'sr') continue;
    for (const a of hits) hit(a, text);
    if (!scroller && own.some(r => r.left < -1 || r.right > W + 1)) out.offpage.push({ text, at: pathOf(p), l: Math.round(Math.min(...own.map(r => r.left))), r: Math.round(Math.max(...own.map(r => r.right))) });
    const fr = fixedRoot(p);
    for (const r of own) runs.push({ n, p, fr, text, l: r.left, r: r.right, t: r.top + scrollY, b: r.bottom + scrollY });
  }
  // pictures inside a scroll container: their <text> counts as visible text for the scroll check only (cut, offpage and
  // overlap of SVG text are figs.mjs's). The climb starts above the <svg>, whose own overflow is the viewBox clip.
  const inScroller = e => { for (let a = e.parentElement; a && a !== docTop && a !== document.documentElement; a = a.parentElement) if (/auto|scroll/.test(st(a).overflowX + st(a).overflowY)) return true; return false; };
  for (const svg of document.body.querySelectorAll('svg:not(svg svg)')) {
    if (!inScroller(svg) || hidden(svg)) continue;
    const det = svg.closest('details:not([open])'); if (det && !svg.closest('summary')) continue;
    const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && !hidden(t)).map(t => [t, t.getBoundingClientRect()]).filter(([, r]) => r.width > 0.5 && r.height > 0.5);
    if (!texts.length) continue;
    const { cutBy, hits } = climb(svg.parentElement, texts.map(([, r]) => r));
    if (cutBy === 'sr') continue;
    for (const a of hits) { const P = portOf(a), t = (texts.find(([, r]) => outside(r, P)) || texts[0])[0]; hit(a, 'svg: ' + t.textContent.trim().replace(/\s+/g, ' ').slice(0, 45)); }
  }
  // a "<page>|<selector>" entry must name exactly one element on its page, or a skip can land on an unlisted container
  for (const k of scrollIds) { const i = k.indexOf('|');
    if (i < 0) { if (document.getElementById(k)) out.idsFound.push(k); continue; }
    if (k.slice(0, i) !== pg) continue;
    let c; try { c = document.querySelectorAll(k.slice(i + 1)).length; } catch (e) { throw new Error(`bad scroll_containers selector in docs/pass-30-exceptions.json: ${k}`); }
    if (c !== 1) out.warn.push(`scroll_containers entry ${k} matches ${c} elements (wants exactly 1)`); }
  const listed = a => scrollIds.some(k => { const i = k.indexOf('|'); if (i < 0) return a.id && k === a.id; if (k.slice(0, i) !== pg) return false;
    try { return a.matches(k.slice(i + 1)); } catch (e) { throw new Error(`bad scroll_containers selector in docs/pass-30-exceptions.json: ${k}`); } });
  for (const [a, v] of scr) {
    if (listed(a)) { out.scrollListed++; continue; }
    out.scroll.push({ page: pg, at: pathOf(a), sel: selOf(a), sw: a.scrollWidth, cw: a.clientWidth, sh: a.scrollHeight, ch: a.clientHeight, text: v.text, runs: v.n });
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
  const meas = () => page.evaluate(measure, { pg, scrollIds: SCROLL_IDS });
  const part = /^part-/.test(pg);
  if (!STATE) return [['', await meas()]];
  if (!part) return [];
  const mid = async () => { await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.3)); await page.waitForTimeout(400); };
  if (STATE === 'bar') {
    await mid();
    if (!(await page.$('.place-btn'))) return [[' [no place-btn]', await meas()]];
    await page.click('.place-btn'); await page.waitForTimeout(500);
    return [[' [bar]', await meas()]];
  }
  if (STATE === 'menu') {
    await mid();
    const ok = await page.evaluate(() => { const y = scrollY; const d = [...document.querySelectorAll('.mark-dot')].find(e => e.getBoundingClientRect().top > 60); if (!d) return false; d.scrollIntoView({ block: 'center' }); d.click(); return true; });
    await page.waitForTimeout(500);
    return [[ok ? ' [menu]' : ' [no mark-dot]', await meas()]];
  }
  if (STATE === 'tip') {
    await mid();
    const sel = await page.evaluate(() => { const e = [...document.querySelectorAll('.glossary-ref')].find(e => e.getBoundingClientRect().top > 0) || document.querySelector('.glossary-ref'); if (!e) return null; e.scrollIntoView({ block: 'center' }); e.setAttribute('data-clip-tip', ''); return '[data-clip-tip]'; });
    if (!sel) return [[' [no glossary-ref]', await meas()]];
    await page.hover(sel); await page.waitForTimeout(600);
    return [[' [tip]', await meas()]];
  }
  if (STATE === 'open') {   // every closed <details> opened (the figures' "How it works" strips): measured as read
    const n = await page.evaluate(() => { const d = [...document.querySelectorAll('details:not([open])')]; for (const x of d) x.open = true; return d.length; });
    await page.waitForTimeout(300);
    return [[n ? ' [open]' : ' [no details]', await meas()]];
  }
  if (STATE === 'fs') {
    const ids = await page.evaluate(() => [...document.querySelectorAll('.diagram-card .fs-button, .light-diagram .fs-button')].map(b => b.closest('[id]').id));
    const outs = [];
    for (const id of ids) {
      await page.evaluate(id => document.getElementById(id).scrollIntoView({ block: 'center' }), id);
      await page.evaluate(id => document.querySelector(`#${id} .fs-button`).click(), id); await page.waitForTimeout(450);
      const m = await meas();
      outs.push([` [fs ${id}]`, m]);
      await page.keyboard.press('Escape'); await page.waitForTimeout(350);
    }
    return outs;
  }
  return [];
}

const KINDS = ['cut', 'offpage', 'overlap', 'scroll'];
const all = []; let fails = 0, nruns = 0; const tot = { cut: 0, offpage: 0, overlap: 0, scroll: 0, hscroll: 0 };
const scrollSeen = new Map();   // page|sel -> finding + where it was seen
const warns = new Set(), idsFound = new Set();
for (const eng of ENGINES) {
  const browser = await (eng === 'webkit' ? webkit : chromium).launch();
  for (const w of WIDTHS) {
    const modes = MODES.filter(m => w >= m.min);
    for (const m of MODES) if (w < m.min) console.log(`${eng} ${w}${m.label}: skipped (runs at ${m.min} px and wider)`);
    if (!modes.length) continue;
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.route(/^https?:\/\/(?!localhost)/, r => r.abort());
    for (const pg of PAGES) for (const mode of modes) {
      await page.goto(`http://localhost:${PORT}/${pg === 'index' ? '' : pg}`, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(150);
      if (mode.apply) await mode.apply(page);
      // scroll-driven reveals (h2 glassReveal, part-4 srStamp) hold every heading below the fold at their first keyframe
      // (opacity 0, shifted, scaled up), so hidden() skipped them and the scale inflated hscroll. The reader meets each one
      // at rest, and their end keyframes equal the base style, so cancel() leaves exactly the resting geometry.
      await page.evaluate(() => { if (typeof DocumentTimeline === 'function') for (const x of document.getAnimations()) if (x.timeline && !(x.timeline instanceof DocumentTimeline)) x.cancel(); });
      await page.waitForTimeout(50);
      const ms = await stateRuns(page, pg);
      for (const [label, m] of ms) {
        const hs = m.scrollWidth > m.innerWidth;
        const n = m.cut.length + m.offpage.length + m.overlap.length + m.scroll.length + (hs ? 1 : 0);
        fails += n; nruns++;
        for (const k of KINDS) tot[k] += m[k].length; tot.hscroll += hs ? 1 : 0;
        console.log(`${eng} ${w} ${pg}${mode.label}${label}: ${n ? 'FAIL' : 'ok'}  cut ${m.cut.length} · offpage ${m.offpage.length} · overlap ${m.overlap.length} · scroll ${m.scroll.length}${m.scrollListed ? ` (+${m.scrollListed} listed)` : ''} · hscroll ${hs ? `${m.scrollWidth}>${m.innerWidth}` : 0}`);
        if (n && ARGS.v) for (const k of KINDS) for (const f of m[k].slice(0, 8)) console.log('   ', k, JSON.stringify(f));
        for (const x of m.warn) warns.add(x); for (const x of m.idsFound) idsFound.add(x);
        for (const f of m.scroll) { const key = f.page + '|' + f.sel; const s = scrollSeen.get(key) || scrollSeen.set(key, { ...f, where: new Set() }).get(key); s.where.add(`${eng} ${w}${mode.label}`); }
        all.push({ eng, w, page: pg + mode.label + label, ...m });
      }
    }
    await ctx.close();
  }
  await browser.close();
}
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify(all, null, 1));
console.log(`clip: ${fails} finding${fails === 1 ? '' : 's'} in ${nruns} run${nruns === 1 ? '' : 's'} (cut ${tot.cut} · offpage ${tot.offpage} · overlap ${tot.overlap} · scroll ${tot.scroll} · hscroll ${tot.hscroll}), ${((Date.now() - T0) / 1000).toFixed(1)} s`);
// scroll containers to fix or to list (by "<page>|<sel>") in docs/pass-30-exceptions.json, each one once
for (const s of scrollSeen.values()) console.log(`  scroll ${s.page}|${s.sel}  ${s.sw}/${s.cw} x ${s.sh}/${s.ch}  "${s.text}"  [${[...s.where].join(', ')}]`);
for (const x of warns) console.log(`warn: ${x}`);
for (const k of SCROLL_IDS) if (!k.includes('|') && !idsFound.has(k)) console.log(`warn: scroll_containers id ${k} not found on the measured pages`);
server.close();
process.exit(fails ? 1 : 0);
