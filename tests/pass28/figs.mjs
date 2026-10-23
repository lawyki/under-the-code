// Pass 28 figure sweep (docs/pass-28-brief.md, law 3), extended for Pass 30 Gate 1 (docs/pass-29-30-brief.md). Per
// picture, per width and engine: smallest rendered label (CSS px), label count, overlapping text boxes, text outside
// the viewBox, text spilling out of its shape, caption words; and WCAG 2.2 contrast of text, named marks and icons
// (tests/pass30/contrast.mjs). Measured, not eyeballed.
//   node figs.mjs [--kind=figs|heroes|cover|icons|all] [--part=part-1[,index]] [--fig=fig-1-10[,fig-3-7]]
//                 [--widths=320,360,375,768,1024,1440] [--browser=chromium|webkit] [--times=0,1.5,3] [--motion]
//                 [--fullscreen] [--no-contrast] [--json=out.json] [--verbose]
// kinds: figs (the 222 cards, default), heroes (.chapter-hero-visual), cover (svg.cover-exhibit-svg on index), icons
// (insight-strip icons, the fullscreen open/close icons, the account mark, the place-bar close, the mark-menu glyphs).
// Heroes and the cover are measured only where they render; elsewhere they are "not rendered" (neither pass nor fail).
// --fig takes any row id: fig-1-2, hero-ch1, cover, insight-ch1-cpu-p11, fs-fig-1-2, account, pb-close, mark-glyph-3.
// Runs: default = the reduced-motion still (book.js pauses every SVG at t=0; the cover is judged at its end state).
//   --times       still frames at absolute SMIL times (as in Pass 28)
//   --motion      no reduced motion; each animated SVG paused at 0, 25, 50, 75 % of its cycle (largest SMIL begin + dur),
//                 CSS animations at the same fraction of their own duration; a play-once SVG also at its end state
//   --fullscreen  every card with a fullscreen control is also measured opened (rows marked fs); composes with --motion
//   contrast      on unless --no-contrast; at 1440 px only (colours do not depend on width), on the still or on each
//                 sampled frame; when 1440 is not in --widths a 1440 pass runs for contrast alone ("contrast only" rows)
// Gate 1 = the default run plus the --motion run, each with --fullscreen.
// The only skips are read from docs/pass-30-exceptions.json (never written here): label_floor.ids skip the 11 px floor,
// caption_length.ids skip the caption check, scroll_containers.ids are containers that scroll on purpose (an icon cut
// by one is not clipped). Each applied skip is printed on its row.
import { chromium, webkit } from '../pass25/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { contrastOf, iconContrast } from '../pass30/contrast.mjs';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = process.env.FIG_ROOT || new URL('../../public/', import.meta.url).pathname;   // FIG_ROOT: another public/ tree (Pass 31)
const KINDS = ARGS.kind === 'all' ? ['figs', 'heroes', 'cover', 'icons'] : [ARGS.kind || 'figs'];
if (KINDS.some(k => !['figs', 'heroes', 'cover', 'icons'].includes(k))) { console.log(`figs: bad --kind=${ARGS.kind} (figs|heroes|cover|icons|all)`); process.exit(2); }
const onPage = (k, p) => p === 'index' ? k === 'cover' || k === 'icons' : k !== 'cover';
const PARTS = ARGS.part ? String(ARGS.part).split(',') : ['part-1', 'part-2', 'part-3', 'part-4', 'part-5', 'index'].filter(p => KINDS.some(k => onPage(k, p)));
const WIDTHS = String(ARGS.widths || '320,360,375,768,1024,1440').split(',').map(Number);
const ENGINES = ARGS.browser ? [ARGS.browser] : ['chromium', 'webkit'];
const MIN_PX = 11;
const ONLY = ARGS.fig ? String(ARGS.fig).split(',') : null;
const MOTION = !!ARGS.motion, FULL = !!ARGS.fullscreen, CONTRAST = !ARGS['no-contrast'], CW = 1440;
const LOOP = CONTRAST && !WIDTHS.includes(CW) ? [...WIDTHS, CW] : WIDTHS;
const T0 = Date.now();

let EXC = {};
try { EXC = JSON.parse(fs.readFileSync(new URL('../../docs/pass-30-exceptions.json', import.meta.url), 'utf8')); }
catch (e) { console.log(`note: docs/pass-30-exceptions.json unreadable (${e.message}); nothing is skipped`); }
const FLOOR_X = new Set(EXC.label_floor?.ids || []), CAP_X = new Set(EXC.caption_length?.ids || []), SCROLL_X = EXC.scroll_containers?.ids || [];

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

// the pictures of one kind, as [container, id, svg, index]; fs = only the card open in fullscreen
function targets({ kind, fs }) {
  if (kind === 'figs') return [...document.querySelectorAll(fs ? '.is-fullscreen' : '.diagram-card, .light-diagram')].map((c, i) => [c, c.id || '', c.querySelector('svg'), i]);
  if (kind === 'heroes') return [...document.querySelectorAll('.chapter-hero-visual')].map((h, i) => [h, 'hero-' + ((h.closest('[id]') || {}).id || i), h.querySelector(':scope > svg'), i]);
  return [...document.querySelectorAll('svg.cover-exhibit-svg')].map((s, i) => [s.parentElement, 'cover', s, i]);
}

function measure({ kind, only, fs, src }) {
  const targets = new Function('return ' + src)();
  const out = [];
  for (const [card, id, svg, i] of targets({ kind, fs })) {
    if (only && !only.includes(id)) continue;
    if (!svg) continue;
    if (kind !== 'figs') {   // heroes and the cover: measured only where they render (CSS hides them on small screens)
      const r = svg.getBoundingClientRect(); let why = '';
      for (let e = svg; e && !why; e = e.parentElement) if (getComputedStyle(e).display === 'none') why = 'display none';
      if (!why && (!r.width || !r.height)) why = 'zero size';
      if (why) { out.push({ id, i, rendered: false, why }); continue; }
    }
    const label = kind === 'figs' ? (card.querySelector('.diagram-label') || {}).textContent || card.id : (svg.querySelector('title') || {}).textContent || svg.getAttribute('aria-label') || id;
    const sr = svg.getBoundingClientRect();
    // the viewBox is fitted into the SVG box by preserveAspectRatio (default xMidYMid meet): in fullscreen the box is
    // letterboxed, so the scale is the fitted one and the viewBox area (v) is the rendered rect, not the box. In the
    // page, the hero and the cover the box has the viewBox's aspect and v is the box itself
    const vb = svg.viewBox.baseVal, par = svg.preserveAspectRatio.baseVal; let scale = 1, v = sr;
    if (vb && vb.width && vb.height) {
      const sx = sr.width / vb.width, sy = sr.height / vb.height, none = par.align === 1;
      scale = none ? Math.min(sx, sy) : par.meetOrSlice === 2 ? Math.max(sx, sy) : Math.min(sx, sy);
      const w = none ? sr.width : vb.width * scale, h = none ? sr.height : vb.height * scale;
      const ax = none ? 0 : [0, 0, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1][par.align], ay = none ? 0 : [0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1][par.align];
      const left = sr.left + (sr.width - w) * ax, top = sr.top + (sr.height - h) * ay;
      v = { left, top, right: left + w, bottom: top + h, width: w, height: h };
    }
    // what the reader sees now (the reduced-motion still): skip text faded out by an ancestor
    const shown = el => { let o = 1; for (let e = el; e && e !== svg.parentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; o *= parseFloat(cs.opacity); const a = e.getAttribute && e.getAttribute('opacity'); if (a !== null && e.tagName !== 'svg') o *= 1; } return o > 0.05; };
    const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && shown(t));
    const boxes = texts.map(t => { const b = t.getBoundingClientRect(); return { t: t.textContent.trim().slice(0, 40), x: b.left, y: b.top, w: b.width, h: b.height, fs: parseFloat(getComputedStyle(t).fontSize), fx: !!t.closest('.fx'), run: !!t.closest('.run') }; });
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
      // crowded: two labels on one line with almost no space between them read as one word
      // (.run marks pieces composed into one word or number on purpose: a line of code, a row of bits)
      else if (!a.fx && !b.fx && !(a.run && b.run) && iy > 0.5 * Math.min(ah, bh) && ix > -3 && ix <= 1) overlaps.push(a.t + ' ~ ' + b.t + ' (crowded)');
    }
    const outside = boxes.filter(b => b.x < v.left - 1 || b.y < v.top - 1 || b.x + b.w > v.right + 1 || b.y + b.h > v.bottom + 1).map(b => b.t);
    // spill: a label whose centre sits in a shape must fit inside that shape (the smallest one holding its centre)
    // .fx marks a moving overlay (a highlight, a spreading fill), not a container
    const shapes = [...svg.querySelectorAll('rect, circle, ellipse, polygon')].filter(r => shown(r) && !r.closest('.fx') && r.getAttribute('fill') !== 'none'
      && !/^(0|0\.0+)$/.test(r.getAttribute('fill-opacity') || '1')).map(r => r.getBoundingClientRect()).filter(b => b.width > 4 && b.height > 4 && b.width < v.width * 0.9);
    const spill = [];
    boxes.forEach(b => {
      if (b.fx) return;   // a moving token is not contained by what it flies over
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
      const hold = shapes.filter(r => cx > r.left && cx < r.right && cy > r.top && cy < r.bottom).sort((p, q) => p.width * p.height - q.width * q.height)[0];
      if (hold && (b.x < hold.left - 1 || b.x + b.w > hold.right + 1 || b.y < hold.top - 1.5 || b.y + b.h > hold.bottom + 1.5)) spill.push(b.t);
    });
    const cap = kind === 'figs' && card.querySelector('.diagram-caption');
    const capWords = cap ? cap.textContent.trim().split(/\s+/).length : 0;
    const svgWords = texts.reduce((n, t) => n + t.textContent.trim().split(/\s+/).length, 0);
    out.push({ id, i, label: label.trim().slice(0, 80), svgW: Math.round(sr.width), scale: +scale.toFixed(3), labels: texts.length, svgWords, minPx: minPx && +minPx.toFixed(1), small, overlaps, outside, spill, capWords });
  }
  return out;
}

// pause each picture's SVG at one frame. t: absolute SMIL time ('end' = after its last animation, the cover's still);
// f: fraction of the cycle, the largest begin + dur among its SMIL elements (every animation in the book repeats
// indefinitely, so that is one full period); CSS animations inside it go to the same fraction of their own duration.
// f = 1 is used only for play-once SVGs (their end state). The time is kept on the SVG so it can be re-imposed.
function setFrame({ kind, only, fs, t, f, src }) {
  const targets = new Function('return ' + src)();
  const clock = v => { let m; v = v.trim();
    if ((m = /^([-+]?[\d.]+)(ms|s|min|h)?$/.exec(v))) return parseFloat(m[1]) * { ms: 0.001, s: 1, min: 60, h: 3600 }[m[2] || 's'];
    if ((m = /^(-?)(?:(\d+):)?(\d+):([\d.]+)$/.exec(v))) return (m[1] ? -1 : 1) * ((+m[2] || 0) * 3600 + +m[3] * 60 + parseFloat(m[4]));
    return null; };
  const info = {};
  for (const [, id, svg] of targets({ kind, fs })) {
    if (!svg || (only && !only.includes(id))) continue;
    const smil = [...svg.querySelectorAll('animate, animateTransform, animateMotion, set')];
    const css = svg.getAnimations ? svg.getAnimations({ subtree: true }) : [];
    let cycle = 0, finite = smil.length > 0; const odd = [];
    for (const a of smil) {
      let b = null;
      for (const s of (a.getAttribute('begin') || '0').split(';').filter(s => s.trim())) { const v = clock(s); if (v === null) odd.push('begin=' + s.trim()); else b = b === null ? v : Math.max(b, v); }
      if (b === null) continue;   // event-only begin: not on the clock (reported)
      const d = clock(a.getAttribute('dur') || '');
      if (d === null) { if (a.tagName === 'set') cycle = Math.max(cycle, b); else odd.push('dur=' + a.getAttribute('dur')); continue; }
      cycle = Math.max(cycle, b + d);
      if (a.getAttribute('repeatCount') === 'indefinite' || a.getAttribute('repeatDur') === 'indefinite') finite = false;
    }
    let tt;
    if (f == null) {
      tt = t === 'end' ? cycle + 0.05 : +t;
      if (svg.setCurrentTime) { svg.pauseAnimations(); svg.setCurrentTime(tt); }
      if (t === 'end') css.forEach(a => { try { a.finish(); } catch (e) { /* infinite: left as it is */ } });
    } else {
      if (f >= 1 && !finite) continue;
      tt = f >= 1 ? cycle + 0.05 : f * cycle;
      if (svg.setCurrentTime) { svg.pauseAnimations(); svg.setCurrentTime(tt); }
      css.forEach(a => { a.pause(); const c = a.effect.getComputedTiming(); if (f >= 1 && isFinite(c.endTime)) a.finish(); else if (isFinite(c.duration)) a.currentTime = c.delay + f * c.duration; });
    }
    svg.dataset.f30t = tt;
    info[id] = { t: +tt.toFixed(3), cycle: +cycle.toFixed(3), static: !smil.length && !css.length, finite, odd: [...new Set(odd)], css: css.length };
  }
  return info;
}
// scrolling lets book.js's observer unpause figures it sees: put every sampled SVG back on its frame
const reapply = () => document.querySelectorAll('svg[data-f30t]').forEach(s => { if (s.setCurrentTime) { s.pauseAnimations(); s.setCurrentTime(+s.dataset.f30t); } });

// icons: rendered at all, and not clipped (inside the viewport, not cut by an ancestor's overflow or paint containment)
function measureIcons({ groups, scrollIds }) {
  const G = { insight: 'svg.insight-svg', fs: '.fs-button svg', account: 'a.book-account svg', 'pb-close': '.pb-close svg', glyph: '.mark-menu .mm-glyph svg', 'fs-close': '.is-fullscreen .fs-close svg' };
  const ids = { insight: s => 'insight-' + (((s.closest('.insight-strip') || s).querySelector('[id]') || {}).id || ''), fs: s => 'fs-' + s.closest('.diagram-card, .light-diagram').id,
    account: s => s.closest('.cover') ? 'account-cover' : 'account', 'pb-close': () => 'pb-close', glyph: s => 'mark-glyph-' + s.closest('[data-c]').dataset.c, 'fs-close': s => 'fs-close-' + s.closest('.is-fullscreen').id };
  const vw = document.documentElement.clientWidth, vh = window.innerHeight, out = [];
  // a drawing's key is a hash of its markup, so one drawing has one key on every page (17 distinct in the book)
  const draw = s => { let h = 5381; for (const ch of s.innerHTML.replace(/\s+/g, ' ')) h = (h * 33 + ch.charCodeAt(0)) >>> 0; return 'd' + h.toString(16).padStart(8, '0').slice(-6); };
  for (const g of groups) document.querySelectorAll(G[g]).forEach((s, i) => {
    const id = ids[g](s), r = s.getBoundingClientRect();
    let why = !r.width || !r.height ? 'zero size' : getComputedStyle(s).visibility === 'hidden' ? 'hidden' : '';
    let fixed = false, o = 1;
    for (let e = s; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none') why = why || 'display none'; if (cs.position === 'fixed') fixed = true; o *= parseFloat(cs.opacity); }
    if (!why && !(o > 0)) why = 'opacity 0';
    if (why) { out.push({ id, sel: G[g], i, group: g, rendered: false, why }); return; }
    // ink box: the svg's box joined with every drawn shape (icons draw with overflow: visible), strokes included
    let [l, t, R, B] = [r.left, r.top, r.right, r.bottom];
    for (const m of s.querySelectorAll('rect, circle, ellipse, polygon, polyline, path, line')) {
      const c = getComputedStyle(m), q = m.getBoundingClientRect(), ctm = m.getScreenCTM(), h = c.stroke !== 'none' ? (parseFloat(c.strokeWidth) || 0) * (ctm ? Math.hypot(ctm.a, ctm.b) : 1) / 2 : 0;
      l = Math.min(l, q.left - h); t = Math.min(t, q.top - h); R = Math.max(R, q.right + h); B = Math.max(B, q.bottom + h);
    }
    const clipped = [], excs = [];
    if (l < -1 || R > vw + 1) clipped.push('viewport x');
    if (fixed && (t < -1 || B > vh + 1)) clipped.push('viewport y');   // in-flow icons scroll into view; fixed chrome cannot
    // an ancestor clips only inside the icon's containing-block chain: a fixed box escapes every ancestor but one that
    // makes a containing block for it (transform, filter, contain...); an absolute box escapes up to its positioned one
    let esc = /^(fixed|absolute)$/.test(getComputedStyle(s).position) ? getComputedStyle(s).position : null;
    for (let e = s.parentElement; e && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      const cbAll = cs.transform !== 'none' || cs.perspective !== 'none' || cs.filter !== 'none' || (cs.backdropFilter || 'none') !== 'none' || /paint|layout|strict|content/.test(cs.contain) || /transform|filter|perspective/.test(cs.willChange);
      const isCb = esc && (cbAll || (esc === 'absolute' && cs.position !== 'static'));
      const inChain = !esc || isCb;
      if (isCb) esc = null;
      if (cs.position === 'fixed') esc = 'fixed'; else if (cs.position === 'absolute' && esc !== 'fixed') esc = 'absolute';
      if (!inChain || cs.display === 'inline' || cs.display === 'contents') continue;
      const paint = /paint|strict|content/.test(cs.contain), cx = cs.overflowX !== 'visible' || paint, cy = cs.overflowY !== 'visible' || paint;
      if (!cx && !cy) continue;
      const b = e.getBoundingClientRect(), pl = b.left + e.clientLeft, pt = b.top + e.clientTop, pr = pl + e.clientWidth, pb = pt + e.clientHeight;
      if (!((cx && (l < pl - 1 || R > pr + 1)) || (cy && (t < pt - 1 || B > pb + 1)))) continue;
      const name = (e.id ? '#' + e.id : e.tagName.toLowerCase() + (e.classList[0] ? '.' + e.classList[0] : '')) + ' (' + (paint ? 'contain ' + cs.contain : 'overflow ' + (cx ? cs.overflowX : cs.overflowY)) + ')';
      if (e.id && scrollIds.includes(e.id) && /auto|scroll/.test(cs.overflowX + cs.overflowY)) excs.push(name); else clipped.push(name);
    }
    out.push({ id, sel: G[g], i, group: g, box: [Math.round(R - l), Math.round(B - t)], draw: g === 'insight' ? draw(s) : undefined, fixed, clipped, excs });
  });
  return out;
}

const SRC = targets.toString();
const KIND1 = { figs: 'fig', heroes: 'hero', cover: 'cover' };
// fullscreen naming: a label within 12 CSS px of a mark in the page is as near in fullscreen, so the distance grows with
// the fullscreen scale over the page scale (never below 12): fewer named marks would hide fullscreen failures
const spec = (kind, r, fs, ps) => fs ? { sel: '.is-fullscreen', i: 0, html: true, fixed: true, near: ps ? Math.max(12, 12 * r.scale / ps) : 12 } : kind === 'figs' ? { sel: '.diagram-card, .light-diagram', i: r.i, html: true }
  : kind === 'heroes' ? { sel: '.chapter-hero-visual > svg', i: r.i, ring: true } : { sel: 'svg.cover-exhibit-svg', i: r.i, ring: true };
const frames = kind => MOTION ? [0, 0.25, 0.5, 0.75, 1].map(f => ({ f })) : ARGS.times ? String(ARGS.times).split(',').map(t => ({ t: Number(t) })) : [{ t: kind === 'cover' ? 'end' : 0 }];
const vtDone = page => page.waitForFunction(() => !document.querySelector('.transitioning'), null, { timeout: 3000 }).catch(() => {});

const results = [], times = [];
// one frame of one kind: measure every picture, then (at 1440) its contrast on that same frame
async function pictures(page, kind, fr, fs, base, tm, first, ps) {
  const info = await page.evaluate(setFrame, { kind, only: ONLY, fs, src: SRC, ...fr });
  await page.waitForTimeout(60);
  const rows = await page.evaluate(measure, { kind, only: ONLY, fs, src: SRC });
  for (const r of rows) {
    const a = info[r.id];
    if (r.rendered === false ? !first : MOTION && (!a || (fr.f > 0 && a.static))) continue;   // a static SVG (and a hidden one) is reported once
    const row = { ...base, kind: KIND1[kind], fs: !!fs, t: a ? a.t : fr.t, f: MOTION ? fr.f : null, end: fr.t === 'end' || fr.f >= 1, cycle: a?.cycle, static: a?.static, odd: a?.odd?.length ? a.odd : undefined, ...r };
    if (base.cHere && r.rendered !== false) { const c = await contrastOf(page, spec(kind, r, fs, ps), reapply); row.contrast = c; tm.contrast += c.ms; tm.shots += c.shots || 0; tm.pics++; }
    results.push(row);
  }
}

for (const eng of ENGINES) {
  const browser = await (eng === 'webkit' ? webkit : chromium).launch();
  for (const w of LOOP) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, reducedMotion: MOTION ? 'no-preference' : 'reduce' });
    for (const part of PARTS) {
      const kinds = KINDS.filter(k => onPage(k, part)); if (!kinds.length) continue;
      const tm = { eng, w, part, load: 0, measure: 0, contrast: 0, shots: 0, pics: 0, fs: 0, icons: 0 }; let t1 = Date.now();
      const base = { eng, w, part, geomSkip: !WIDTHS.includes(w), cHere: CONTRAST && w === CW, motion: MOTION };
      const page = await ctx.newPage();
      await page.goto(`http://localhost:${PORT}/${part}`); await page.waitForTimeout(800);
      await page.evaluate(() => document.fonts && document.fonts.ready);
      // what a reader who has scrolled there sees: every scroll-reveal finished; page chrome on the document clock held
      // still (scroll-driven ones, such as the cards' scrollFade, keep following the scroll: a held one stays faded)
      if (MOTION) {
        await page.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('revealed')));
        await page.waitForTimeout(700);
        await page.evaluate(() => document.getAnimations().forEach(a => { if (!a.timeline || a.timeline === document.timeline) a.pause(); }));
      }
      tm.load = Date.now() - t1;
      for (const kind of kinds.filter(k => k !== 'icons')) for (const [n, fr] of frames(kind).entries()) { t1 = Date.now(); const c0 = tm.contrast; await pictures(page, kind, fr, false, base, tm, n === 0); tm.measure += Date.now() - t1 - (tm.contrast - c0); }
      // fullscreen: open each card from its own control, let the view transition land, measure, Escape
      if (FULL && kinds.includes('figs')) {
        t1 = Date.now(); const c0 = tm.contrast;
        const ids = await page.evaluate(only => [...document.querySelectorAll('.diagram-card, .light-diagram')].filter(c => c.querySelector('.fs-button') && (!only || only.includes(c.id))).map(c => c.id), ONLY);
        for (const id of ids) {
          // the card's in-page scale (fitted viewBox), for the fullscreen naming distance
          const ps = await page.evaluate(id => { const s = document.getElementById(id).querySelector('svg'), r = s.getBoundingClientRect(), v = s.viewBox.baseVal; return v && v.width && v.height ? Math.min(r.width / v.width, r.height / v.height) : 1; }, id);
          await page.evaluate(id => document.getElementById(id).querySelector('.fs-button').click(), id);
          await page.waitForTimeout(500); await vtDone(page);
          // WebKit under load can miss the first click (the view transition of the previous card still closing): try once
          // more, and if the view still is not open, stop with a clear error rather than measure the page as fullscreen
          if (!await page.evaluate(() => !!document.querySelector('.is-fullscreen'))) {
            await page.waitForTimeout(800); await page.evaluate(id => document.getElementById(id).querySelector('.fs-button').click(), id);
            await page.waitForTimeout(800); await vtDone(page);
            if (!await page.evaluate(() => !!document.querySelector('.is-fullscreen'))) throw new Error(`fullscreen did not open for ${id} (${eng} ${w})`);
          }
          if (MOTION) await page.evaluate(() => Promise.race([Promise.all(document.querySelector('.is-fullscreen').getAnimations().filter(a => isFinite(a.effect.getComputedTiming().endTime)).map(a => a.finished)), new Promise(r => setTimeout(r, 1500))]));
          for (const [n, fr] of frames('figs').entries()) await pictures(page, 'figs', fr, true, base, tm, n === 0, ps);
          await page.keyboard.press('Escape'); await page.waitForTimeout(350); await vtDone(page);
        }
        tm.fs = Date.now() - t1 - (tm.contrast - c0);
      }
      if (kinds.includes('icons')) { t1 = Date.now(); const c0 = tm.contrast; await icons(page, part, base, tm); tm.icons = Date.now() - t1 - (tm.contrast - c0); }
      times.push(tm);
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
}
server.close();

// icons in three states: the page with its place bar open; the mark menu opened from a section dot; one card per card
// style open in fullscreen (its close icon). Contrast (1440) right after each state's measurement.
async function icons(page, part, base, tm) {
  const isPart = /^part-/.test(part);
  const run = async (groups, note) => {
    const rows = (await page.evaluate(measureIcons, { groups, scrollIds: SCROLL_X })).filter(r => !ONLY || ONLY.includes(r.id));
    rows.sort((a, b) => (b.fixed ? 1 : 0) - (a.fixed ? 1 : 0));   // fixed chrome first: scrolling to the others may close the bar
    for (const r of rows) {
      const row = { ...base, kind: 'icon', note, ...r };
      if (base.cHere && r.rendered !== false) { const c = await iconContrast(page, { sel: r.sel, i: r.i }); row.contrast = c; tm.contrast += c.ms; tm.shots++; tm.pics++; }
      results.push(row);
    }
  };
  if (isPart) {
    await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight * 0.3, behavior: 'instant' })); await page.waitForTimeout(400);
    await page.evaluate(() => document.querySelector('.place-btn')?.click()); await page.waitForTimeout(500);
  }
  await run(['insight', 'fs', 'account', 'pb-close']);
  if (!isPart) return;
  await page.evaluate(() => document.querySelector('.pb-close')?.click()); await page.waitForTimeout(300);
  // the mark menu from a section dot (as a pointer opens it); a dot that is not shown falls back to the bar's button
  const via = await page.evaluate(() => {
    const d = [...document.querySelectorAll('.mark-dot')].find(e => e.getBoundingClientRect().width > 0 && e.getBoundingClientRect().top > 60);
    if (d) { d.scrollIntoView({ block: 'center', behavior: 'instant' }); d.setAttribute('data-f30-dot', ''); return 'mark-dot'; }
    document.querySelector('.place-btn')?.click(); return 'pb-mark';
  });
  await page.waitForTimeout(400);   // let the scroll settle first: a scroll closes an open menu
  await page.evaluate(via => via === 'pb-mark' ? document.querySelector('.pb-mark')?.click() : document.querySelector('[data-f30-dot]').click(), via);
  await page.waitForTimeout(500);
  await run(['glyph'], via === 'pb-mark' ? 'menu via pb-mark (no mark-dot shown)' : undefined);
  await page.keyboard.press('Escape'); await page.waitForTimeout(300);
  const ids = await page.evaluate(() => ['.diagram-card:not(.light-diagram)', '.light-diagram'].map(s => document.querySelector(s + ' .fs-button')?.closest('[id]').id).filter(Boolean));
  for (const id of ids) {
    await page.evaluate(id => document.getElementById(id).querySelector('.fs-button').click(), id);
    await page.waitForTimeout(500); await vtDone(page);
    await run(['fs-close']);
    await page.keyboard.press('Escape'); await page.waitForTimeout(350); await vtDone(page);
  }
}

// --json stays an array of rows, as in Pass 28 (contrast details ride on each row; per-page timings are on stdout)
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify(results.map(({ cHere, ...r }) => r), null, 1));
// legibility is judged from 360 px up (the smallest common phone); 320 must still not clip or overlap
// verdicts on the unrounded ratio (r): WCAG thresholds are not rounded (2.996:1 is below 3)
const tFail = x => x.r == null || x.r < 4.5, mFail = m => m.named && m.r < 3, low3 = m => m.r < 3;
const failing = m => ['fill', 'stroke'].filter(k => m[k] && m[k].r < 3);   // the paint(s) below 3:1
function why(f) {
  if (f.rendered === false) return [];
  const w = [];
  if (f.kind === 'icon') {
    if (!f.geomSkip && f.clipped.length) w.push('icon-clip');
    if (f.contrast && (f.contrast.error || f.contrast.r < 3)) w.push('icon-contrast');
    return w;
  }
  if (!f.geomSkip) {
    if (!FLOOR_X.has(f.id) && f.w >= 360 && f.minPx < MIN_PX) w.push('floor');
    if (f.overlaps.length) w.push('overlap');
    if (f.outside.length) w.push('outside');
    if (f.spill.length) w.push('spill');
    if (f.kind === 'fig' && !CAP_X.has(f.id) && f.capWords > 60) w.push('caption');
  }
  const c = f.contrast;
  if (c) { if (c.error || c.texts.some(tFail)) w.push('text-contrast'); if (!c.error && c.marks.some(mFail)) w.push('mark-contrast'); }
  return w;
}
const fail = f => why(f).length > 0;
const pct = v => Math.round(v * 100) + '%';
const tag = f => (f.fs ? ' fs' : '') + (f.motion ? (f.static ? ' static' : ` t${f.t} ${f.f >= 1 ? 'end' : pct(f.f)}`) : f.end ? ` end t${f.t}` : (f.t ? ' t' + f.t : '')) + (f.geomSkip ? ' [contrast only]' : '');
const excTag = f => { const s = [];
  if (FLOOR_X.has(f.id)) s.push('exc label_floor' + (f.w >= 360 && f.minPx < MIN_PX ? ` (min ${f.minPx}px not judged)` : ''));
  if (f.kind === 'fig' && CAP_X.has(f.id)) s.push('exc caption_length' + (f.capWords > 60 ? ` (${f.capWords} words not judged)` : ''));
  return s.length && !f.geomSkip ? ' [' + s.join('; ') + ']' : ''; };
const ctag = f => { const c = f.contrast; if (!c) return ''; if (c.error) return ` | contrast ERROR ${c.error}`;
  const tr = c.texts.filter(x => x.ratio != null).map(x => x.ratio), named = c.marks.filter(m => m.named), low = c.marks.filter(low3);
  return ` | contrast text ${c.texts.length} min ${tr.length ? Math.min(...tr) : '-'}${c.texts.filter(tFail).length ? ' FAIL ' + c.texts.filter(tFail).length : ''} · marks ${c.marks.length} named ${named.length}${named.filter(mFail).length ? ' FAIL ' + named.filter(mFail).length : ''} listed ${low.filter(m => !m.named).length}`; };
const paint = p => p ? `${p.fg} ${p.ratio}:1 (worst ${p.worst}) on ${p.bg}${{ ink: ' [from ink]', veil: ' [seen through a later mark]', footprint: ' [no ink: on screen, judged against its ring]' }[p.from] || ''}` : '';
function details(f) {
  const c = f.contrast; if (!c || c.error) return;
  const L = [];
  for (const x of c.texts.filter(tFail)) L.push(`      text FAIL ${x.ratio == null ? 'not judged (' + x.skip + ')' : x.ratio + ':1 (worst ' + x.worst + ') ' + x.fg + ' on ' + x.bg} ${x.src} "${x.t}"`);
  for (const m of c.marks.filter(mFail)) L.push(`      mark FAIL ${m.ratio}:1 on ${failing(m).join('+')} ${m.sig} named by ${m.named} "${m.by}"${m.fill ? ' fill ' + paint(m.fill) : ''}${m.stroke ? ' stroke ' + paint(m.stroke) : ''}${m.veil ? ' under ' + m.veil : ''} (ink ${m.ink} px in a ${m.box.join('x')} box)`);
  if (ARGS.verbose) {
    for (const m of c.marks.filter(m => !m.named && low3(m))) L.push(`      mark list ${m.ratio}:1 on ${failing(m).join('+')} ${m.sig}${m.fill ? ' fill ' + paint(m.fill) : ''}${m.stroke ? ' stroke ' + paint(m.stroke) : ''}`);
    // a named mark failing on one paint while its other paint holds: the failure stands; an outline relaxation is an owner call
    for (const m of c.marks.filter(m => mFail(m) && m.best >= 3)) L.push(`      mark note ${m.sig} fails on ${failing(m).join('+')} only (best paint ${m.best}:1) named by ${m.named} "${m.by}"`);
    if (f.odd) L.push(`      smil not on the clock: ${f.odd.join(', ')}`);
  }
  if (L.length > 14 && !ARGS.verbose) L.splice(12, L.length - 12, `      … ${L.length - 12} more (--verbose, --json)`);
  L.forEach(l => console.log(l));
}
const shownRows = results.filter(f => f.rendered !== false);
for (const f of shownRows) if (ARGS.fig || ARGS.verbose || fail(f)) {
  const st = fail(f) ? 'FAIL' : 'ok  ';
  if (f.kind === 'icon') {
    const c = f.contrast;
    console.log(`${st} ${f.eng} ${f.w} ${f.id}${f.geomSkip ? ' [contrast only]' : ''} icon ${f.box.join('x')}${f.draw ? ' drawing ' + f.draw : ''}${!f.geomSkip && f.clipped.length ? ' clipped [' + f.clipped.join('; ') + ']' : ''}${f.excs?.length ? ' [exc scroll_containers: ' + f.excs.join('; ') + ']' : ''}${f.note ? ' (' + f.note + ')' : ''}${c ? c.error ? ' | contrast ERROR ' + c.error : ` | contrast ${c.ratio}:1 (worst ${c.worst}) ${c.tag} ${c.paint} ${c.fg} on ${c.bg}` : ''}`);
    continue;
  }
  console.log(`${st} ${f.eng} ${f.w} ${f.id}${tag(f)} min ${f.minPx}px small ${f.small}/${f.labels} words ${f.svgWords}${f.kind === 'fig' ? ' cap ' + f.capWords : ''}${f.overlaps.length ? ' overlaps ' + f.overlaps.length + ' [' + f.overlaps.slice(0, 2).join('; ') + ']' : ''}${f.outside.length ? ' outside ' + f.outside.length + ' [' + f.outside.slice(0, 2).join('; ') + ']' : ''}${f.spill.length ? ' spill ' + f.spill.length + ' [' + f.spill.slice(0, 3).join('; ') + ']' : ''}${excTag(f)}${ctag(f)}`);
  details(f);
}
// not rendered: one line per width and page (heroes and the cover where CSS hides them; an icon whose state did not open)
const nr = new Map();
for (const f of results.filter(f => f.rendered === false)) { const k = `${f.eng} ${f.w} ${f.part}`; nr.set(k, [...(nr.get(k) || []), f.id + (f.why === 'display none' ? '' : ' (' + f.why + ')')]); }
for (const [k, ids] of nr) console.log(`--   ${k} not rendered: ${ids.join(' ')}`);
// SMIL begins that are not clock values (events, syncbases) cannot be sampled on the clock: reported, never guessed
const odd = new Map(); for (const f of results) if (f.odd) odd.set(f.part + ' ' + f.id, f.odd.join(', '));
for (const [k, v] of odd) console.log(`note: ${k} smil not on the clock (ignored for its cycle): ${v}`);
for (const t of times) console.log(`# time ${t.eng} ${t.w} ${t.part}: load ${(t.load / 1000).toFixed(1)}s, measure ${(t.measure / 1000).toFixed(1)}s${t.fs ? `, fullscreen ${(t.fs / 1000).toFixed(1)}s` : ''}${t.icons ? `, icons ${(t.icons / 1000).toFixed(1)}s` : ''}${t.pics ? `, contrast ${(t.contrast / 1000).toFixed(1)}s (${t.pics} pictures, ${t.shots} shots)` : ''}`);
const n = shownRows.length, bad = shownRows.filter(fail).length, by = {};
for (const f of shownRows) for (const k of why(f)) by[k] = (by[k] || 0) + 1;
const exF = shownRows.filter(f => FLOOR_X.has(f.id) && !f.geomSkip), exC = shownRows.filter(f => f.kind === 'fig' && CAP_X.has(f.id) && !f.geomSkip);
const allMarks = shownRows.flatMap(f => f.contrast?.marks || []);
console.log(`figs: ${bad}/${n} fail (min label ${MIN_PX}px from 360, no overlap, inside viewBox, inside its shape, caption ≤ 60 words${CONTRAST ? '; contrast at 1440: text ≥ 4.5, named marks ≥ 3, icons ≥ 3' : ''})`);
console.log(`by check: ${['floor', 'overlap', 'outside', 'spill', 'caption', 'text-contrast', 'mark-contrast', 'icon-clip', 'icon-contrast'].map(k => `${k} ${by[k] || 0}`).join(' · ')} · not rendered ${results.length - n}`
  + ` · exceptions applied: label_floor ${exF.length} rows (${exF.filter(f => f.w >= 360 && f.minPx < MIN_PX).length} below the floor), caption_length ${exC.length} rows (${exC.filter(f => f.capWords > 60).length} over 60 words)`
  + (KINDS.includes('icons') ? ` · insight drawings ${new Set(shownRows.filter(f => f.draw).map(f => f.draw)).size} distinct` : '')
  + (CONTRAST ? ` · marks listed (unnamed < 3:1) ${allMarks.filter(m => !m.named && low3(m)).length} · named marks failing on one paint with the other ≥ 3:1 ${allMarks.filter(m => mFail(m) && m.best >= 3).length}`
    + ` · marks seen through a later see-through mark ${allMarks.filter(m => m.veil).length}, on screen without ink (probe) ${allMarks.filter(m => m.probed).length}`
    + ` · marks not judged: ${Object.entries(shownRows.reduce((o, f) => { for (const [k, v] of Object.entries(f.contrast?.skipped || {})) o[k] = (o[k] || 0) + v; return o; }, {})).map(([k, v]) => k + ' ' + v).join(', ') || 'none'}` : ''));
console.log(`# time total ${((Date.now() - T0) / 1000).toFixed(1)}s`);
const miss = ONLY ? ONLY.filter(id => !results.some(f => f.id === id)) : [];
if (miss.length) console.log(`note: --fig ids not found: ${miss.join(' ')}`);
if (!n) { console.log(`figs: nothing measured (${results.length} not rendered): not a pass`); process.exit(2); }
process.exit(bad ? 1 : 0);
