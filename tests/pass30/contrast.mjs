// Pass 30 contrast (docs/pass-29-30-brief.md, Gate 1), imported by tests/pass28/figs.mjs. WCAG 2.2:
//   text   1.4.3, at least 4.5:1 at every size (the large-text 3:1 relaxation is not applied)
//   marks  1.4.11, at least 3:1 for a mark a label or the <desc> names (FAIL); an unnamed mark below 3:1 is LISTED
//   icons  3:1 (house rule), always a fail below
// Measured from pixels: the background is what the browser painted under a text or mark, read from a screenshot with
// that text or mark hidden; the foreground is its computed colour composited with its effective opacity (colour alpha
// x fill/stroke-opacity x every ancestor's opacity) over that background. The verdict is the ratio against the
// median-luminance background pixel; the worst pixel is reported beside it. Verdicts compare the unrounded ratio (r);
// the rounded one (ratio) is for display. A mark is judged on its worst paint: every stroke and fill must hold.
import zlib from 'node:zlib';

// ---- PNG: Playwright screenshots are 8-bit RGB or RGBA, not interlaced; alpha is ignored (screenshots are opaque)
const paeth = (a, b, c) => { const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c); return pa <= pb && pa <= pc ? a : pb <= pc ? b : c; };
export function decodePNG(buf) {
  let p = 8, w = 0, h = 0, bpp = 0; const idat = [];
  while (p < buf.length) {
    const len = buf.readUInt32BE(p), type = buf.toString('latin1', p + 4, p + 8), d = buf.subarray(p + 8, p + 8 + len);
    if (type === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); bpp = { 2: 3, 6: 4 }[d[9]]; if (d[8] !== 8 || d[12] || !bpp) throw new Error(`png: unsupported (depth ${d[8]}, colour ${d[9]}, interlace ${d[12]})`); }
    else if (type === 'IDAT') idat.push(d); else if (type === 'IEND') break;
    p += 12 + len;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat)), stride = w * bpp, px = new Uint8Array(w * h * 3);
  let prev = new Uint8Array(stride), cur = new Uint8Array(stride), q = 0;
  for (let y = 0; y < h; y++) {
    const ft = raw[q++];
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? cur[x - bpp] : 0, b = prev[x], c = x >= bpp ? prev[x - bpp] : 0, v = raw[q++];
      cur[x] = ft === 0 ? v : ft === 1 ? v + a : ft === 2 ? v + b : ft === 3 ? v + ((a + b) >> 1) : v + paeth(a, b, c);
    }
    for (let x = 0, o = y * w * 3; x < w; x++) { px[o++] = cur[x * bpp]; px[o++] = cur[x * bpp + 1]; px[o++] = cur[x * bpp + 2]; }
    [prev, cur] = [cur, prev];
  }
  return { w, h, px };
}

// ---- colour (WCAG 2.2 relative luminance; browsers composite in gamma-encoded sRGB, so compositing happens before linearising)
const lin = c => (c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const LIN = Float64Array.from({ length: 256 }, (_, i) => lin(i));
export const lum = c => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
export const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const over = (c, a, bg) => [c[0] * a + bg[0] * (1 - a), c[1] * a + bg[1] * (1 - a), c[2] * a + bg[2] * (1 - a)];
// a computed colour -> [r, g, b, a]; null when the paint is not a plain colour (url(), none, context-fill)
export function parseColor(s) {
  if (!s) return null; s = String(s).trim(); let m;
  if ((m = /^rgba?\(([^)]+)\)$/.exec(s))) { const v = m[1].split(/[\s,/]+/).filter(Boolean).map(t => t.endsWith('%') ? parseFloat(t) / 100 : parseFloat(t)); return [v[0], v[1], v[2], v[3] ?? 1]; }
  if ((m = /^color\(srgb ([^)]+)\)$/.exec(s))) { const v = m[1].split(/[\s/]+/).filter(Boolean).map(parseFloat); return [v[0] * 255, v[1] * 255, v[2] * 255, v[3] ?? 1]; }
  if ((m = /^#([0-9a-f]{6})$/i.exec(s))) { const n = parseInt(m[1], 16); return [n >> 16, (n >> 8) & 255, n & 255, 1]; }
  return null;
}
const hex = c => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
const fmt = (c, a) => hex(c) + (a < 0.999 ? '@' + a.toFixed(2) : '');
// display only, truncated: a ratio is never shown at a threshold it is below (2.9999 shows 2.99, not 3)
const r2 = v => v == null ? null : Math.floor(v * 100) / 100;

// one paint over a set of background pixels: ratio against the median-luminance pixel (a 4096-bin luminance histogram
// finds it in one pass), and the worst pixel (cached per distinct colour: backgrounds are mostly flat fills)
function judge(img, idx, c, a) {
  const px = img.px, n = idx.length, H = new Uint32Array(4096), B = new Uint16Array(n);
  for (let k = 0; k < n; k++) { const o = idx[k] * 3; B[k] = Math.min(4095, ((0.2126 * LIN[px[o]] + 0.7152 * LIN[px[o + 1]] + 0.0722 * LIN[px[o + 2]]) * 4096) | 0); H[B[k]]++; }
  let acc = 0, mb = 0; for (; mb < 4096; mb++) { acc += H[mb]; if (acc * 2 >= n) break; }
  let bg = null, worst = Infinity; const seen = new Map();
  for (let k = 0; k < n; k++) {
    const o = idx[k] * 3, key = (px[o] << 16) | (px[o + 1] << 8) | px[o + 2];
    let r = seen.get(key); if (r === undefined) { const p = [px[o], px[o + 1], px[o + 2]]; r = ratio(over(c, a, p), p); seen.set(key, r); }
    if (r < worst) worst = r;
    if (!bg && B[k] === mb) bg = [px[o], px[o + 1], px[o + 2]];
  }
  return { ratio: ratio(over(c, a, bg), bg), worst, bg: hex(bg) };
}
// the colour a paint actually shows where it cannot be read from CSS (a gradient): the median-luminance pixel of its ink
// (base null: every pixel of idx counts)
function apparent(vis, base, idx) {
  const ink = base ? idx.filter(i => { const o = i * 3; return Math.max(Math.abs(vis.px[o] - base.px[o]), Math.abs(vis.px[o + 1] - base.px[o + 1]), Math.abs(vis.px[o + 2] - base.px[o + 2])) > 2; }) : idx;
  if (!ink.length) return null;
  const L = ink.map(i => [LIN[vis.px[i * 3]] * 0.2126 + LIN[vis.px[i * 3 + 1]] * 0.7152 + LIN[vis.px[i * 3 + 2]] * 0.0722, i]).sort((p, q) => p[0] - q[0]);
  const o = L[L.length >> 1][1] * 3; return [vis.px[o], vis.px[o + 1], vis.px[o + 2], 1];
}
// pixel indices of viewport rects [l, t, r, b] inside a screenshot taken at clip
function pixelsIn(img, clip, rects) {
  const out = [];
  for (const [l, t, r, b] of rects) {
    const x0 = Math.max(0, Math.floor(l - clip.x)), x1 = Math.min(img.w, Math.ceil(r - clip.x)), y0 = Math.max(0, Math.floor(t - clip.y)), y1 = Math.min(img.h, Math.ceil(b - clip.y));
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) out.push(y * img.w + x);
  }
  return out;
}
const differs = (A, B, i) => { const o = i * 3; return Math.abs(A.px[o] - B.px[o]) > 2 || Math.abs(A.px[o + 1] - B.px[o + 1]) > 2 || Math.abs(A.px[o + 2] - B.px[o + 2]) > 2; };

// a mark: its ink is where the screenshot changes when it alone (in its batch) is hidden; what touches it is the hidden
// screenshot under that ink plus a 2 px ring around it (the mask dilated twice by one pixel, minus the ink).
// A paint's colour is its CSS colour composited. Seen through later see-through paints (m.veils, plain colours) it is
// what the reader sees there: S0 = a.(V2 o V1 o P) + (1 - a).SK for veils V1, V2 over the opaque paint P at its alpha
// a, since compositing is affine. Where no colour can be computed (a gradient paint or veil, a filter, a blend) it is
// read from the ink, the median pixel of S0 there; SN (the batch with the strokes of m.split marks removed) parts the
// ink of a two-paint mark into its stroke (S0 vs SN) and its fill (SN vs SK).
// probe: the probe shot of a mark that showed no ink. Its footprint there is where it is on screen: the pixels where the
// magenta makes at least half of the colour (pa: its ancestors' opacity). A mark under an opaque later one of the same
// shape shows magenta only in the anti-aliased edge, (1 - c).c <= 1/4 of a pixel: that is covered, not on screen.
// What is under the footprint equals the mark (no ink), so it is judged against the 2 px ring around it.
function judgeMark(m, S0, SK, clip, SN, probe) {
  const x0 = Math.max(0, Math.floor(m.bb[0] - 3 - clip.x)), y0 = Math.max(0, Math.floor(m.bb[1] - 3 - clip.y));
  const x1 = Math.min(S0.w, Math.ceil(m.bb[2] + 3 - clip.x)), y1 = Math.min(S0.h, Math.ceil(m.bb[3] + 3 - clip.y)), W = x1 - x0, H = y1 - y0;
  const res = { sig: m.sig, named: m.named || null, by: m.by || null };
  if (W <= 0 || H <= 0) return { ...res, skip: 'off screen' };
  const ink = new Uint8Array(W * H); let n = 0;
  const share = i => { const o = i * 3; let e = 0, g = 0; for (let ch = 0; ch < 3; ch++) { const sk = SK.px[o + ch], E = [255, 0, 255][ch] * m.pa + sk * (1 - m.pa); e = Math.max(e, Math.abs(E - sk)); g = Math.max(g, Math.abs(probe.px[o + ch] - sk)); } return e < 3 ? 0 : g / e; };
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = (y0 + y) * S0.w + x0 + x; if (probe ? share(i) >= 0.5 : differs(S0, SK, i)) { ink[y * W + x] = 1; n++; } }
  // nothing changes without it: covered by a later mark, or painted within 2 levels of what is under it. contrastOf
  // tells the two apart with a probe shot (the mark repainted magenta): a footprint there means it is on screen
  if (!n) return { ...res, skip: 'no ink' };
  let d = ink;
  for (let pass = 0; pass < 2; pass++) {
    const h = new Uint8Array(W * H), v = new Uint8Array(W * H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = y * W + x; h[i] = d[i] || (x > 0 && d[i - 1]) || (x < W - 1 && d[i + 1]) ? 1 : 0; }
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = y * W + x; v[i] = h[i] || (y > 0 && h[i - W]) || (y < H - 1 && h[i + W]) ? 1 : 0; }
    d = v;
  }
  const idx = [], inkIdx = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (d[y * W + x]) { const i = (y0 + y) * S0.w + x0 + x; if (ink[y * W + x]) inkIdx.push(i); if (!probe || !ink[y * W + x]) idx.push(i); }
  if (!idx.length) idx.push(...inkIdx);   // a probed mark that fills the whole shot has no ring: what is under it
  const paints = {};
  for (const [k, css, a] of [['fill', m.fill, m.fa], ['stroke', m.stroke, m.sa]]) {
    if (!(k === 'fill' ? m.hasF : m.hasS)) continue;
    const V = m.veils && m.veils[k];
    let c = parseColor(css), from = probe ? 'footprint' : 'css', al = c ? c[3] * a : 1;
    if (!c || (V && V.some(v => !v.plain))) {
      // on screen without ink (probe): what shows on its footprint; else its own ink
      c = probe ? apparent(S0, null, inkIdx) : m.split && SN ? (k === 'stroke' ? apparent(S0, SN, idx) : apparent(SN, SK, idx)) : apparent(S0, SK, inkIdx);
      if (!probe) from = 'ink'; al = 1;
    } else if (V) {
      let rgb = c.slice(0, 3); for (const v of V) { const vc = parseColor(v.c); rgb = over(vc, vc[3] * v.a, rgb); }
      c = [...rgb, 1]; if (!probe) from = 'veil';
    }
    if (!c || al <= 0) continue;
    const j = judge(SK, idx, c, al);
    paints[k] = { fg: fmt(c, al), ratio: r2(j.ratio), r: j.ratio, worst: r2(j.worst), bg: j.bg, from, veils: V ? V.map(v => v.sig + ' ' + v.paint) : undefined };
  }
  const ps = Object.values(paints);
  if (!ps.length) return { ...res, skip: 'no paint' };
  // every stroke and fill of a named mark must hold (brief, Gate 1): the verdict is the worst paint; best is kept for
  // the report (an outline that carries a faint fill is an owner call, never a default here)
  const r = Math.min(...ps.map(p => p.r));
  return { ...res, ...paints, r, ratio: r2(r), best: r2(Math.max(...ps.map(p => p.r))), veil: m.veils ? [...new Set(Object.values(m.veils).flat().map(v => v.sig))].join(', ') : undefined, ink: n, box: [Math.round(m.bb[2] - m.bb[0]), Math.round(m.bb[3] - m.bb[1])] };
}

// ---- in-page halves (serialised into the page: no closures) --------------------------------------------------------
// bring a target into view (centred when it fits); fixed targets (the fullscreen card) stay where they are
export function c30Scroll(spec) {
  const el = document.querySelectorAll(spec.sel)[spec.i]; const r = el.getBoundingClientRect();
  if (!spec.fixed) window.scrollTo({ top: window.scrollY + r.top - Math.max(4, (window.innerHeight - r.height) / 2), behavior: 'instant' });
  return { h: r.height };
}
// hide fixed or sticky chrome (the top bar, the rail) painted over the clip: it is not what is under the picture
export function c30Overlays({ sel, i, clip }) {
  const target = document.querySelectorAll(sel)[i];
  if (!document.getElementById('c30-style')) {
    const s = document.createElement('style'); s.id = 'c30-style';
    s.textContent = '[data-c30-ov], [data-c30-ov] * { visibility: hidden !important; } text[data-c30-hide], text[data-c30-hide] * { visibility: hidden !important; }'
      + ' [data-c30-hide]:not(text), [data-c30-hide]:not(text) * { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; text-decoration-color: transparent !important; transition: none !important; }'
      + ' [data-c30-off] { visibility: hidden !important; } [data-c30-nostroke] { stroke: none !important; }'
      // the probe: a mark that showed no ink repainted opaque magenta (only the paints it has), to see whether it is on screen
      + ' [data-c30-probe] { opacity: 1 !important; } [data-c30-probe*=f] { fill: #ff00ff !important; fill-opacity: 1 !important; } [data-c30-probe*=s] { stroke: #ff00ff !important; stroke-opacity: 1 !important; }';
    document.head.appendChild(s);
  }
  const fixed = window.__c30fixed || (window.__c30fixed = [...document.querySelectorAll('body *')].filter(e => /^(fixed|sticky)$/.test(getComputedStyle(e).position)));
  for (const e of fixed) {
    if (e.contains(target) || target.contains(e)) continue;
    const b = e.getBoundingClientRect();
    if (b.right > clip.x && b.left < clip.x + clip.width && b.bottom > clip.y && b.top < clip.y + clip.height) e.setAttribute('data-c30-ov', '');
  }
}
// list a picture's texts (SVG <text>, and for a figure card its label, caption and strip summary) and marks, with their
// boxes in viewport px, computed paints and effective opacity; group marks into batches whose padded boxes never meet,
// so one screenshot per batch shows each mark's own ground
export function c30Collect(spec) {
  const target = document.querySelectorAll(spec.sel)[spec.i];
  const svg = target.matches('svg') ? target : target.querySelector('svg');
  const st = el => getComputedStyle(el), vw = document.documentElement.clientWidth, vh = window.innerHeight;
  const tr = target.getBoundingClientRect(), g = spec.ring ? 2 : 0;
  const x0 = Math.max(0, Math.floor(tr.left - g)), y0 = Math.max(0, Math.floor(tr.top - g));
  const clip = { x: x0, y: y0, width: Math.min(vw, Math.ceil(tr.right + g)) - x0, height: Math.min(vh, Math.ceil(tr.bottom + g)) - y0 };
  const alpha = el => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = st(e); if (cs.display === 'none') return 0; o *= parseFloat(cs.opacity); } return st(el).visibility === 'hidden' ? 0 : o; };
  // figs.mjs's own notion of a shown text (what the reader sees now)
  const shown = el => { let o = 1; for (let e = el; e && e !== svg.parentElement; e = e.parentElement) { const cs = st(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; o *= parseFloat(cs.opacity); } return o > 0.05; };
  const ink = b => [b.left, b.top + b.height * 0.1, b.right, b.bottom - b.height * 0.1];   // the file's ink box: font box less 10% top and bottom
  const texts = [], hide = [], labels = [];
  for (const t of svg.querySelectorAll('text')) {
    hide.push(t);
    if (!t.textContent.trim() || !shown(t)) continue;
    labels.push({ t: t.textContent.trim(), box: (b => [b.left, b.top, b.right, b.bottom])(t.getBoundingClientRect()) });
    // a <tspan> painted differently from its <text> is its own text
    const cs = st(t), tsp = [...t.querySelectorAll('tspan')].filter(s => s.textContent.trim());
    const own = tsp.filter(s => { const c = st(s); return c.fill !== cs.fill || c.fillOpacity !== cs.fillOpacity || c.opacity !== '1'; });
    const direct = [...t.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || tsp.length > own.length;
    for (const e of direct ? [t, ...own] : own) { const c = st(e); texts.push({ src: 'svg', t: e.textContent.trim().slice(0, 40), fill: c.fill, a: alpha(e) * parseFloat(c.fillOpacity), rects: [ink(e.getBoundingClientRect())] }); }
  }
  if (spec.html) for (const [src, q] of [['label', '.diagram-label'], ['caption', '.diagram-caption'], ['how', '.fig-how > summary']]) {
    const host = target.querySelector(q); if (!host) continue;
    hide.push(host);
    const w = document.createTreeWalker(host, NodeFilter.SHOW_TEXT); let n;
    while ((n = w.nextNode())) {
      if (!n.textContent.trim()) continue;
      const p = n.parentElement, a = alpha(p); if (!(a > 0)) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      const rects = [...rg.getClientRects()].filter(b => b.width > 0 && b.height > 0).map(ink);
      if (rects.length) texts.push({ src, t: n.textContent.trim().slice(0, 40), fill: st(p).color, a, rects });
    }
  }
  // marks: every drawn shape outside <defs> and friends with a paint that is there (fill/stroke not none, opacity not 0)
  const cAlpha = s => { const m = /rgba?\(([^)]*)\)/.exec(s); if (!m) return 1; const v = m[1].split(/[\s,/]+/).filter(Boolean); return v.length > 3 ? parseFloat(v[3]) : 1; };
  const marks = [], els = [], skipped = { none: 0, hidden: 0, tiny: 0, image: 0 };
  // a fill paints only where the shape encloses an area: some point of a 6 x 6 (then 16 x 16) grid over its box is in it.
  // The grid is off-centre (0.37, 0.61 of a cell) so no point sits on a diagonal stroke: WebKit counts a point on a
  // zero-area path as inside its fill
  const filled = el => { if (!el.isPointInFill) return true; const g = el.getBBox(), p = svg.createSVGPoint();
    for (const N of [6, 16]) for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { p.x = g.x + (x + 0.37) * g.width / N; p.y = g.y + (y + 0.61) * g.height / N; if (el.isPointInFill(p)) return true; }
    return false; };
  // raster <image> marks have no paint to read: counted as not judged
  for (const im of svg.querySelectorAll('image')) if (!im.closest('defs, clipPath, mask, marker, pattern, symbol')) skipped.image++;
  // a paint whose colour the CSS gives as a plain colour (else a gradient or pattern: read from the ink)
  const plain = v => /^(rgba?\(|color\(srgb |#[0-9a-f]{6}$)/i.test(v);
  const sig = m => { const A = n => m.getAttribute(n); const tag = m.tagName.toLowerCase(); const k = { rect: ['x', 'y', 'width', 'height'], circle: ['cx', 'cy', 'r'], ellipse: ['cx', 'cy', 'rx', 'ry'], line: ['x1', 'y1', 'x2', 'y2'] }[tag];
    return tag + '[' + (k ? k.map(n => n + '=' + (A(n) ?? '')).join(' ') : ((A('d') || A('points') || '').replace(/\s+/g, ' ').slice(0, 28))) + ']'; };
  let n = -1;
  for (const m of svg.querySelectorAll('rect, circle, ellipse, polygon, polyline, path, line')) {
    if (m.closest('defs, clipPath, mask, marker, pattern, symbol')) continue;
    n++;   // #n: the mark's index among the SVG's drawn shapes, in document order
    const a = alpha(m); if (!(a > 0)) { skipped.hidden++; continue; }
    const c = st(m), sw = parseFloat(c.strokeWidth) || 0, fill = m.tagName === 'line' ? 'none' : c.fill, fo = parseFloat(c.fillOpacity), so = parseFloat(c.strokeOpacity);
    const b = m.getBoundingClientRect();   // a fill needs an area: open ticks like "M0 0 v5" or an X of two strokes paint none
    const hasF = fill !== 'none' && fo > 0 && cAlpha(fill) > 0 && b.width > 0 && b.height > 0 && filled(m), hasS = c.stroke !== 'none' && so > 0 && sw > 0 && cAlpha(c.stroke) > 0;
    if (!hasF && !hasS) { skipped.none++; continue; }
    const ctm = m.getScreenCTM(), k = ctm ? Math.hypot(ctm.a, ctm.b) : 1, half = hasS ? sw * k / 2 : 0;
    const bb = [b.left - half, b.top - half, b.right + half, b.bottom + half];
    if (Math.max(bb[2] - bb[0], bb[3] - bb[1]) < 2) { skipped.tiny++; continue; }
    // see-through paints (alpha < 1, a gradient, or the mark filtered, blended or masked): what is under them shows
    // through. odd: its reach or colour is not what its geometry and CSS say (also when clipped); a clip alone leaves an
    // opaque paint opaque where it paints
    const fx = c.filter !== 'none' || c.mixBlendMode !== 'normal' || !!m.closest('[mask]');
    const odd = fx || !!m.closest('[clip-path]') || (c.clipPath || 'none') !== 'none';
    const thru = { fill: hasF && (fx || a * fo * cAlpha(fill) < 1 || !plain(fill)), stroke: hasS && (fx || a * so * cAlpha(c.stroke) < 1 || !plain(c.stroke)) };
    marks.push({ sig: '#' + n + ' ' + sig(m), pa: alpha(m.parentElement), fill, fa: a * fo, stroke: c.stroke, sa: a * so, hasF, hasS, bb, thru, odd, gradient: (hasF && !plain(fill)) || (hasS && !plain(c.stroke)) }); els.push(m);
  }
  // No mark is skipped for being under another: the pixels decide (one wholly under an opaque later mark shows no ink).
  // A paint seen through later see-through paints shows their colour over its own. Veils of a paint: the later
  // see-through paints that cover at least half of its sample points (its fill on a 6 x 6 grid, its stroke at 12 points
  // along it), so they are what its median ink pixel shows. Plain-colour veils are composited exactly (contrastOf);
  // a gradient, filtered, blended, clipped or masked veil leaves the paint to be read from its ink
  const meet0 = (p, q) => p[0] < q[2] && q[0] < p[2] && p[1] < q[3] && q[1] < p[3];
  const pts = (el, k) => {
    const out = [];
    try {
      if (k === 'fill') { const g = el.getBBox(); for (let y = 0; y < 6; y++) for (let x = 0; x < 6; x++) { const p = svg.createSVGPoint(); p.x = g.x + (x + 0.5) * g.width / 6; p.y = g.y + (y + 0.5) * g.height / 6; if (el.isPointInFill(p)) out.push(p); } }
      else { const L = el.getTotalLength(); for (let j = 0; j < 12; j++) out.push(el.getPointAtLength(L * (j + 0.5) / 12)); }
    } catch (e) { /* no geometry: no samples, no veil */ }
    return out;
  };
  marks.forEach((m, i) => {
    const later = marks.map((q, k) => k).filter(k => k > i && (marks[k].thru.fill || marks[k].thru.stroke) && meet0(marks[k].bb, m.bb));
    if (!later.length) return;
    const ctm = els[i].getScreenCTM();
    for (const kind of ['fill', 'stroke']) {
      if (!(kind === 'fill' ? m.hasF : m.hasS)) continue;
      const P = pts(els[i], kind); if (!P.length || !ctm) continue;
      const V = [];
      for (const k of later) {
        const q = marks[k], qe = els[k], qc = qe.getScreenCTM(); if (!qc) continue;
        const M = qc.inverse().multiply(ctm), Q = P.map(p => p.matrixTransform(M));
        for (const qk of ['fill', 'stroke']) {
          if (!q.thru[qk]) continue;
          const hit = Q.filter(p => qk === 'fill' ? qe.isPointInFill(p) : qe.isPointInStroke(p)).length;
          if (hit * 2 >= P.length) V.push({ sig: q.sig, paint: qk, c: qk === 'fill' ? q.fill : q.stroke, a: qk === 'fill' ? q.fa : q.sa, plain: !q.odd && plain(qk === 'fill' ? q.fill : q.stroke) });
        }
      }
      if (V.length) (m.veils || (m.veils = {}))[kind] = V;
    }
    const inkRead = k => m.veils?.[k]?.some(v => !v.plain);
    m.split = m.hasF && m.hasS && (m.gradient || inkRead('fill') || inkRead('stroke'));
  });
  // named: a shown label's box meets the mark or lies within 12 CSS px of its bbox; or the <desc> contains a label's
  // text, which then names the mark nearest to that label (short labels match case-sensitively: "A" is not "a")
  const gap = (p, q) => Math.hypot(Math.max(0, p[0] - q[2], q[0] - p[2]), Math.max(0, p[1] - q[3], q[1] - p[3]));
  const desc = ((svg.querySelector('desc') || {}).textContent || '').replace(/\s+/g, ' ');
  const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const inDesc = t => desc && new RegExp('(^|[^\\p{L}\\p{N}])' + esc(t) + '($|[^\\p{L}\\p{N}])', t.length <= 2 ? 'u' : 'iu').test(desc);
  // spec.near: the naming distance in CSS px (12; a fullscreen row passes the in-page 12 px at its own scale)
  const near = spec.near || 12;
  for (const m of marks) { const l = labels.find(x => gap(x.box, m.bb) <= near); if (l) { m.named = 'label'; m.by = l.t.slice(0, 30); } }
  for (const l of labels) {
    if (!inDesc(l.t)) continue;
    let best = null, bd = Infinity;
    for (const m of marks) { const d = gap(l.box, m.bb), ar = (m.bb[2] - m.bb[0]) * (m.bb[3] - m.bb[1]); if (d < bd || (d === bd && best && ar < (best.bb[2] - best.bb[0]) * (best.bb[3] - best.bb[1]))) { bd = d; best = m; } }
    if (best && !best.named) { best.named = 'desc'; best.by = l.t.slice(0, 30); }
  }
  const pad = b => [b[0] - 3, b[1] - 3, b[2] + 3, b[3] + 3], meet = (p, q) => p[0] < q[2] && q[0] < p[2] && p[1] < q[3] && q[1] < p[3];
  const batches = [];
  for (const i of marks.map((m, i) => i).sort((p, q) => (marks[q].bb[2] - marks[q].bb[0]) * (marks[q].bb[3] - marks[q].bb[1]) - (marks[p].bb[2] - marks[p].bb[0]) * (marks[p].bb[3] - marks[p].bb[1]))) {
    const pb = pad(marks[i].bb); let k = batches.findIndex(B => B.every(j => !meet(pad(marks[j].bb), pb)));
    if (k < 0) { k = batches.length; batches.push([]); } batches[k].push(i);
  }
  window.__c30 = { hide, marks: els, batches };
  return { clip, texts, marks, batches, skipped };
}
// one state of the picture: texts hidden; a batch of marks hidden; or (nostroke) only the strokes of those marks
// removed; or (probe: {mark index: 'f'|'s'|'fs'}) the batch hidden but those marks repainted magenta
export function c30Hide({ texts, batch, nostroke, probe }) {
  const S = window.__c30;
  for (const a of ['data-c30-off', 'data-c30-nostroke', 'data-c30-probe']) document.querySelectorAll('[' + a + ']').forEach(e => e.removeAttribute(a));
  if (texts) S.hide.forEach(e => e.setAttribute('data-c30-hide', ''));
  if (batch != null) S.batches[batch].forEach(i => probe && probe[i] ? S.marks[i].setAttribute('data-c30-probe', probe[i]) : S.marks[i].setAttribute('data-c30-off', ''));
  if (nostroke) nostroke.forEach(i => S.marks[i].setAttribute('data-c30-nostroke', ''));
  if (S.icon) S.icon.setAttribute('data-c30-off', '');
  // two frames: WebKit's snapshot shows a visibility change only after a full rendering update (one rAF is not enough)
  return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
}
export function c30Restore() {
  for (const a of ['data-c30-hide', 'data-c30-off', 'data-c30-ov', 'data-c30-nostroke', 'data-c30-probe']) document.querySelectorAll('[' + a + ']').forEach(e => e.removeAttribute(a));
  delete window.__c30;
}
// an icon: in view (fixed chrome stays put, anything else is scrolled to the middle), its shapes' paints, its ink box
export function c30IconScroll(spec) {
  const s = document.querySelectorAll(spec.sel)[spec.i];
  for (let e = s; e; e = e.parentElement) if (getComputedStyle(e).position === 'fixed') return;
  const r = s.getBoundingClientRect(); window.scrollTo({ top: window.scrollY + r.top - window.innerHeight / 2, behavior: 'instant' });
}
export function c30IconCollect(spec) {
  const svg = document.querySelectorAll(spec.sel)[spec.i], st = el => getComputedStyle(el);
  const alpha = el => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = st(e); if (cs.display === 'none') return 0; o *= parseFloat(cs.opacity); } return st(el).visibility === 'hidden' ? 0 : o; };
  const shapes = []; let l = Infinity, t = Infinity, r = -Infinity, b = -Infinity;
  // as in c30Collect: a fill paints only where the shape encloses an area (an X of two strokes has none)
  const filled = el => { if (!el.isPointInFill) return true; const g = el.getBBox(), p = svg.createSVGPoint(); if (!(g.width > 0 && g.height > 0)) return false;
    for (const N of [6, 16]) for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { p.x = g.x + (x + 0.37) * g.width / N; p.y = g.y + (y + 0.61) * g.height / N; if (el.isPointInFill(p)) return true; }
    return false; };
  const join = q => { l = Math.min(l, q[0]); t = Math.min(t, q[1]); r = Math.max(r, q[2]); b = Math.max(b, q[3]); };
  const sb = svg.getBoundingClientRect(); join([sb.left, sb.top, sb.right, sb.bottom]);
  for (const m of svg.querySelectorAll('rect, circle, ellipse, polygon, polyline, path, line')) {
    const a = alpha(m); if (!(a > 0)) continue;
    const c = st(m), sw = parseFloat(c.strokeWidth) || 0, fill = m.tagName === 'line' ? 'none' : c.fill;
    const hasF = fill !== 'none' && parseFloat(c.fillOpacity) > 0 && filled(m), hasS = c.stroke !== 'none' && parseFloat(c.strokeOpacity) > 0 && sw > 0;
    if (!hasF && !hasS) continue;
    const ctm = m.getScreenCTM(), k = ctm ? Math.hypot(ctm.a, ctm.b) : 1, half = hasS ? sw * k / 2 : 0, q = m.getBoundingClientRect();
    join([q.left - half, q.top - half, q.right + half, q.bottom + half]);
    shapes.push({ tag: m.tagName.toLowerCase(), fill, fa: a * parseFloat(c.fillOpacity), stroke: c.stroke, sa: a * parseFloat(c.strokeOpacity), hasF, hasS });
  }
  const vw = document.documentElement.clientWidth, vh = window.innerHeight;
  const x0 = Math.max(0, Math.floor(l - 2)), y0 = Math.max(0, Math.floor(t - 2));
  const clip = { x: x0, y: y0, width: Math.min(vw, Math.ceil(r + 2)) - x0, height: Math.min(vh, Math.ceil(b + 2)) - y0 };
  window.__c30 = { hide: [], marks: [], batches: [], icon: svg };
  return { clip, shapes };
}

const frames2 = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));

// ---- Node halves ------------------------------------------------------------------------------------------------------
// one picture (figure card, hero or cover): texts against what is under their ink, marks against what touches them.
// reapply re-imposes the sampled frame after scrolling (book.js's observer unpauses figures that come into view)
export async function contrastOf(page, spec, reapply) {
  const t0 = Date.now(), vp = page.viewportSize(); let shots = 0, grown = false, split2 = 0, probes = 0;
  let s = await page.evaluate(c30Scroll, spec);
  // a card taller than the viewport is shot whole: the viewport grows for it (width, and so layout, unchanged)
  if (!spec.fixed && s.h + 8 > vp.height) { await page.setViewportSize({ width: vp.width, height: Math.ceil(s.h + 16) }); grown = true; s = await page.evaluate(c30Scroll, spec); }
  await page.evaluate(frames2);
  if (reapply) await page.evaluate(reapply);
  const info = await page.evaluate(c30Collect, spec);
  await page.evaluate(c30Overlays, { ...spec, clip: info.clip });
  const shot = async () => { shots++; return decodePNG(await page.screenshot({ clip: info.clip, scale: 'css' })); };
  const texts = [], marks = [];
  try {
    if (info.clip.width <= 0 || info.clip.height <= 0) return { error: 'not in view', shots, ms: Date.now() - t0 };
    const vis = info.texts.some(x => !parseColor(x.fill)) ? (await page.evaluate(c30Hide, {}), await shot()) : null;
    await page.evaluate(c30Hide, { texts: true });
    const S0 = await shot();
    for (const x of info.texts) {
      const idx = pixelsIn(S0, info.clip, x.rects);
      let c = parseColor(x.fill), from = 'css', a = c ? c[3] * x.a : 1;
      if (!c && vis) { c = apparent(vis, S0, idx); from = 'ink'; a = 1; }
      if (!idx.length || !c) { texts.push({ src: x.src, t: x.t, ratio: null, skip: !c ? 'no colour' : 'off screen' }); continue; }
      const j = judge(S0, idx, c, a);
      texts.push({ src: x.src, t: x.t, fg: fmt(c, a), bg: j.bg, ratio: r2(j.ratio), r: j.ratio, worst: r2(j.worst), from });
    }
    for (let k = 0; k < info.batches.length; k++) {
      const B = info.batches[k], split = B.filter(i => info.marks[i].split);
      await page.evaluate(c30Hide, { texts: true, batch: k });
      const SK = await shot();
      let SN = null;
      if (split.length) { await page.evaluate(c30Hide, { texts: true, nostroke: split }); SN = await shot(); split2 += split.length; }
      const res = B.map(i => judgeMark(info.marks[i], S0, SK, info.clip, SN));
      // a mark that showed no ink: repaint it magenta (its batch hidden). No footprint = covered or clipped, rightly
      // unseen; a footprint = on screen, painted within 2 levels of what is under it: judged, not skipped
      const probe = {};
      B.forEach((i, x) => { if (res[x].skip === 'no ink') { const m = info.marks[i]; probe[i] = (m.hasF ? 'f' : '') + (m.hasS ? 's' : ''); } });
      if (Object.keys(probe).length) {
        await page.evaluate(c30Hide, { texts: true, batch: k, probe });
        const P = await shot(); probes += Object.keys(probe).length;
        B.forEach((i, x) => { if (probe[i]) { const j = judgeMark(info.marks[i], S0, SK, info.clip, null, P); if (!j.skip) res[x] = { ...j, probed: true }; } });
      }
      marks.push(...res);
    }
  } finally {
    await page.evaluate(c30Restore);
    if (grown) { await page.setViewportSize(vp); await page.evaluate(frames2); if (reapply) await page.evaluate(reapply); }
  }
  const sk = { ...info.skipped }; for (const m of marks) if (m.skip) sk[m.skip] = (sk[m.skip] || 0) + 1;
  return { texts, marks: marks.filter(m => !m.skip), skipped: sk, unjudged: marks.filter(m => m.skip).map(m => m.sig + ' ' + m.skip), batches: info.batches.length, split: split2, probed: probes, shots, ms: Date.now() - t0 };
}
// one icon: each shape's paints against the background behind the icon (icon hidden); a shape is its lower paint, the
// icon its worst shape (every stroke and fill holds 3:1, the house rule)
export async function iconContrast(page, spec) {
  const t0 = Date.now();
  await page.evaluate(c30IconScroll, spec); await page.evaluate(frames2);
  const info = await page.evaluate(c30IconCollect, spec);
  await page.evaluate(c30Overlays, { ...spec, clip: info.clip });
  let img;
  try {
    if (info.clip.width <= 0 || info.clip.height <= 0) return { error: 'not in view', ms: Date.now() - t0 };
    await page.evaluate(c30Hide, {});
    img = decodePNG(await page.screenshot({ clip: info.clip, scale: 'css' }));
  } finally { await page.evaluate(c30Restore); }
  const idx = Array.from({ length: img.w * img.h }, (_, i) => i);
  let worst = null;
  for (const s of info.shapes) {
    let low = null;
    for (const [k, css, a] of [['fill', s.fill, s.fa], ['stroke', s.stroke, s.sa]]) {
      if (!(k === 'fill' ? s.hasF : s.hasS)) continue;
      const c = parseColor(css); if (!c || c[3] * a <= 0) continue;
      const j = judge(img, idx, c, c[3] * a);
      if (!low || j.ratio < low.r) low = { paint: k, fg: fmt(c, c[3] * a), bg: j.bg, ratio: r2(j.ratio), r: j.ratio, worst: r2(j.worst) };
    }
    if (low && (!worst || low.r < worst.r)) worst = { tag: s.tag, ...low };
  }
  return worst ? { ...worst, ms: Date.now() - t0 } : { error: 'no paint', ms: Date.now() - t0 };
}
