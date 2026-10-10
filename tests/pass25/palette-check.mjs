#!/usr/bin/env node
// Pass 25 "Place and Marks" — palette + glyph source of truth and measuring script.
// Re-runnable: `node pass25-palette-check.mjs` (exit code 1 if any hard constraint fails).
// Writes, next to itself: pass25-palette.json, pass25-palette-table.md, pass25-contact-sheet.html.
// Maths: WCAG 2.x relative luminance / contrast ratio; OKLCH (Ottosson); CIEDE2000 on CIELAB D65;
// CVD = Machado, Oliveira & Fernandes 2009, severity 1.0, applied to linear RGB (clamped 0..1).
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// ---------- colour maths ----------
const hex2rgb = h => { h = h.replace('#', ''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255); };
const rgb2hex = c => '#' + c.map(v => Math.round(Math.min(1, Math.max(0, v)) * 255).toString(16).padStart(2, '0')).join('');
const toLin = v => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
const lum = hex => { const [r, g, b] = hex2rgb(hex).map(toLin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const contrast = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
const over = (fg, a, bg) => { const f = hex2rgb(fg), b = hex2rgb(bg); return rgb2hex(f.map((v, i) => v * a + b[i] * (1 - a))); };
function oklch(hex) {
  const [r, g, b] = hex2rgb(hex).map(toLin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
  let h = Math.atan2(B, A) * 180 / Math.PI; if (h < 0) h += 360;
  return { L, C: Math.hypot(A, B), h };
}
function linToLab([r, g, b]) {
  const X = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047;
  const Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b;
  const Z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883;
  const f = t => (t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116);
  const fx = f(X), fy = f(Y), fz = f(Z);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
function ciede2000([L1, a1, b1], [L2, a2, b2]) {
  const rad = Math.PI / 180, deg = 180 / Math.PI;
  const C1 = Math.hypot(a1, b1), C2 = Math.hypot(a2, b2), Cb = (C1 + C2) / 2;
  const G = 0.5 * (1 - Math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)));
  const a1p = (1 + G) * a1, a2p = (1 + G) * a2;
  const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
  const hp = (b, a) => { if (b === 0 && a === 0) return 0; const h = Math.atan2(b, a) * deg; return h < 0 ? h + 360 : h; };
  const h1p = hp(b1, a1p), h2p = hp(b2, a2p);
  const dLp = L2 - L1, dCp = C2p - C1p;
  let dhp = 0;
  if (C1p * C2p !== 0) { dhp = h2p - h1p; if (dhp > 180) dhp -= 360; else if (dhp < -180) dhp += 360; }
  const dHp = 2 * Math.sqrt(C1p * C2p) * Math.sin(dhp / 2 * rad);
  const Lbp = (L1 + L2) / 2, Cbp = (C1p + C2p) / 2;
  let hbp = h1p + h2p;
  if (C1p * C2p !== 0) { if (Math.abs(h1p - h2p) > 180) hbp = h1p + h2p < 360 ? (h1p + h2p + 360) / 2 : (h1p + h2p - 360) / 2; else hbp = (h1p + h2p) / 2; }
  const T = 1 - 0.17 * Math.cos((hbp - 30) * rad) + 0.24 * Math.cos(2 * hbp * rad) + 0.32 * Math.cos((3 * hbp + 6) * rad) - 0.20 * Math.cos((4 * hbp - 63) * rad);
  const dTh = 30 * Math.exp(-(((hbp - 275) / 25) ** 2));
  const RC = 2 * Math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7));
  const SL = 1 + 0.015 * (Lbp - 50) ** 2 / Math.sqrt(20 + (Lbp - 50) ** 2);
  const SC = 1 + 0.045 * Cbp, SH = 1 + 0.015 * Cbp * T;
  const RT = -Math.sin(2 * dTh * rad) * RC;
  return Math.sqrt((dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2 + RT * (dCp / SC) * (dHp / SH));
}
const MACHADO = {
  protanopia: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
  deuteranopia: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
  tritanopia: [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
};
const MODES = ['normal', 'protanopia', 'deuteranopia', 'tritanopia'];
const labOf = (hex, mode) => { let lin = hex2rgb(hex).map(toLin); if (mode !== 'normal') { const M = MACHADO[mode]; lin = M.map(r => Math.min(1, Math.max(0, r[0] * lin[0] + r[1] * lin[1] + r[2] * lin[2]))); } return linToLab(lin); };
const dE = (a, b, mode) => ciede2000(labOf(a, mode), labOf(b, mode));

// ---------- grounds ----------
const BAR = '#0a0a0a', TRACK = '#1e1e1e';
const GROUNDS = {
  'part-1': { nav: '#111111', page: '#f5f0eb' },
  'part-2': { nav: '#0d130f', page: '#f6f7f1' },
  'part-3': { nav: '#081b2e', page: '#eef2f4' },
  'part-4': { nav: '#100b06', page: '#f1e9d6' },
  'part-5': { nav: '#0b0916', page: '#f3f2f8' },
};

// ---------- hue families (OKLCH hue, degrees) — the H10 rule ----------
const FAMILY = {
  1: { name: 'amber', test: o => o.C >= 0.05 && o.h >= 55 && o.h <= 90 },
  2: { name: 'red', test: o => o.C >= 0.05 && o.h >= 12 && o.h <= 40 },
  3: { name: 'blue', test: o => o.C >= 0.05 && o.h >= 250 && o.h <= 285 },
  4: { name: 'green', test: o => o.C >= 0.05 && o.h >= 140 && o.h <= 180 },
  5: { name: 'violet or neutral', test: o => o.C < 0.02 || (o.h >= 290 && o.h <= 325) },
};

// ---------- glyphs: inner markup for <svg viewBox="0 0 10 10">, drawn in currentColor ----------
const R = 'fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"';
const SQ = 'fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter"';
const SQX = SQ + ' shape-rendering="crispEdges"'; // orthogonal strokes only: crisp cell edges
const F = 'fill="currentColor"';
const GLYPHS = {
  'part-1': [ // the manuscript's reference marks; round, slightly calligraphic
    ['asterisk', `<path ${R} d="M5 1.4V8.6M1.9 3.2L8.1 6.8M1.9 6.8L8.1 3.2"/>`],
    ['dagger', `<path ${R} d="M5 1.2V8.8M2.3 3.6H7.7"/>`],
    ['double dagger', `<path ${R} d="M5 1.2V8.8M2.4 3H7.6M2.4 7H7.6"/>`],
    ['parallels', `<path ${R} d="M3.4 1.4V8.6M6.6 1.4V8.6"/>`],
    ['pilcrow', `<path ${F} d="M5.6 1.3V5.9H4.7A2.3 2.3 0 0 1 4.7 1.3Z"/><path ${R} d="M5.6 1.3V8.8M7.9 1.3V8.8M4.7 1.3H8.4"/>`],
  ],
  'part-2': [ // monospace-cell strokes, square caps, pixel feel
    ['>', `<path ${SQ} d="M2.6 1.9L7.2 5L2.6 8.1"/>`],
    ['#', `<path ${SQX} d="M3.6 1.6V8.4M6.4 1.6V8.4M1.6 3.6H8.4M1.6 6.4H8.4"/>`],
    ['=', `<path ${SQX} d="M1.9 3.3H8.1M1.9 6.7H8.1"/>`],
    ['/', `<path ${SQ} d="M2.4 8.4L7.6 1.6"/>`],
    ['*', `<path ${SQ} d="M5 1.8V8.2M2.2 3.4L7.8 6.6M2.2 6.6L7.8 3.4"/>`],
  ],
  'part-3': [ // chart symbols
    ['arrowhead', `<path ${F} d="M1.4 1.6L8.9 5L1.4 8.4L3.5 5Z"/>`],
    ['diamond', `<path ${F} d="M5 1L9 5L5 9L1 5Z"/>`],
    ['wave', `<path ${R} d="M0.9 5C2 2.4 3.6 2.4 4.9 5S7.9 7.6 9.1 5"/>`],
    ['triangle', `<path ${R} d="M5 1.5L8.7 8.1H1.3Z"/>`],
    ['ring', `<circle ${R} cx="5" cy="5" r="3.3"/>`],
  ],
  'part-4': [ // registry marks
    ['tick', `<path ${R} d="M1.6 5.3L4 7.8L8.5 2.3"/>`],
    ['redaction bar', `<rect ${F} x="0.9" y="3.2" width="8.2" height="3.6" rx="0.3"/>`],
    ['double rule', `<path ${R} stroke-linecap="butt" d="M1.2 2.9H8.8M1.2 7.1H8.8"/>`],
    ['lozenge', `<path ${R} d="M5 0.9L7.7 5L5 9.1L2.3 5Z"/>`],
    ['tab corner', `<path ${F} d="M1.2 1.2H8.8L1.2 8.8Z"/>`],
  ],
  'part-5': [ // consensus nodes
    ['half node', `<circle fill="none" stroke="currentColor" stroke-width="1.2" cx="5" cy="5" r="3.5"/><path ${F} d="M5 1.5A3.5 3.5 0 0 0 5 8.5Z"/>`],
    ['zigzag', `<path ${R} d="M0.9 6.6L3 3.4L5 6.6L7 3.4L9.1 6.6"/>`],
    ['double ring', `<circle fill="none" stroke="currentColor" stroke-width="1.1" cx="5" cy="5" r="3.9"/><circle fill="none" stroke="currentColor" stroke-width="1.1" cx="5" cy="5" r="1.5"/>`],
    ['hollow ring', `<circle ${R} cx="5" cy="5" r="3.3"/>`],
    ['square', `<rect ${F} x="2" y="2" width="6" height="6" rx="0.5"/>`],
  ],
};

// ---------- the palette (Pass 25, re-derived on the bridge's one-hue-family-per-slot rule) ----------
// was: the spec §7 hex where a slot changed; null where kept.
const PALETTE = {
  'part-1': [
    ['Sienna', '#b27749', null], ['Madder', '#9f4447', '#aa3853'], ['Smalt', '#787adf', null],
    ['Verdigris', '#459881', '#008374'], ['Murex', '#725491', null]],
  'part-2': [
    ['P3 amber', '#805c00', null], ['Ribbon red', '#d35f51', null], ['3270 blue', '#6680e2', null],
    ['P1 green', '#06a175', '#616462 (Carbon)'], ['Carbon', '#616462', '#ad459b (Magenta)']],
  'part-3': [
    ['Route', '#c36f16', null], ['Port', '#b9392b', '#a24389 (Chart magenta)'], ['Prussian', '#5569ca', null],
    ['Starboard', '#2e7e4f', null], ['Sounding', '#7c8589', null]],
  'part-4': [
    ['Ochre', '#ab7916', '#8b5a03'], ['Sealing wax', '#9a4536', '#7d5188 (Copying ink)'], ['Registry ink', '#7378b9', '#6d7bb9'],
    ['Baize', '#43946a', '#068d85 (Verdigris)'], ['Graphite', '#64615e', null]],
  'part-5': [
    ['Candidate', '#7b5e10', null], ['Heartbeat', '#d54e5a', '#b94065'], ['Replica', '#3f639a', null],
    ['Follower', '#1c9c7f', '#0a9394'], ['Commit', '#a078d8', '#6a8f3a']],
};
const CUE = { // saved mark + head fill, spec §7 (unchanged unless noted)
  'part-1': { mark: '#d4a853', fill: '#8a6a2a' },
  'part-2': { mark: '#84ffb2', fill: '#3fae7c' },
  'part-3': { mark: '#4fc4e6', fill: '#2f9dc4' },
  'part-4': { mark: '#cf8d78', fill: '#946657' },
  'part-5': { mark: '#a08cff', markSynced: '#4fd8c2', fill: '#7a68e0' },
};
const READOUT_ALPHA = 0.55;
const MIN_SLOT = 3.0, MIN_DE = 10;

// ---------- measure ----------
const r2 = x => Math.round(x * 100) / 100;
const out = { generated: new Date().toISOString(), method: 'WCAG 2.x contrast; CIEDE2000 on CIELAB D65; CVD Machado 2009 severity 1.0 on linear RGB; hue = OKLCH h', grounds: { bar: BAR, track: TRACK, ...GROUNDS }, parts: {}, readoutAlpha: null, minDeltaE: {} };
const fails = [];
for (const [part, slots] of Object.entries(PALETTE)) {
  const g = GROUNDS[part];
  const P = { slots: [], ...CUE[part], ratios: {} };
  slots.forEach(([name, hex, was], i) => {
    const o = oklch(hex), slot = i + 1;
    const ratios = { bar: r2(contrast(hex, BAR)), chapterNav: r2(contrast(hex, g.nav)), page: r2(contrast(hex, g.page)) };
    const fam = FAMILY[slot].test(o);
    if (Math.min(ratios.bar, ratios.chapterNav, ratios.page) < MIN_SLOT) fails.push(`${part} slot ${slot} ${hex} contrast`);
    if (!fam) fails.push(`${part} slot ${slot} ${hex} not ${FAMILY[slot].name} (h ${o.h.toFixed(0)})`);
    const [glyphName, svg] = GLYPHS[part][i];
    P.slots.push({ slot, hex, name, family: FAMILY[slot].name, wasInSpec: was, glyphName, svg, ratios, oklch: { L: +o.L.toFixed(3), C: +o.C.toFixed(3), h: +o.h.toFixed(1) } });
  });
  // min pairwise ΔE per mode
  const hexes = slots.map(s => s[1]);
  const md = {};
  for (const mode of MODES) {
    let best = { d: Infinity };
    for (let i = 0; i < 5; i++) for (let j = i + 1; j < 5; j++) { const d = dE(hexes[i], hexes[j], mode); if (d < best.d) best = { d, pair: [i + 1, j + 1] }; }
    md[mode] = { deltaE: +best.d.toFixed(1), pair: best.pair };
    if (best.d < MIN_DE) fails.push(`${part} ${mode} min ΔE ${best.d.toFixed(1)} < ${MIN_DE}`);
  }
  out.minDeltaE[part] = md;
  // cue colours
  const c = CUE[part];
  const markR = m => ({ bar: r2(contrast(m, BAR)), track: r2(contrast(m, TRACK)), fill: r2(contrast(m, c.fill)), gap: r2(contrast(m, BAR)) });
  P.ratios.mark = markR(c.mark);
  if (c.markSynced) P.ratios.markSynced = markR(c.markSynced);
  P.ratios.fill = { track: r2(contrast(c.fill, TRACK)), bar: r2(contrast(c.fill, BAR)), gapVsFill: r2(contrast(BAR, c.fill)) };
  for (const k of ['mark', 'markSynced']) if (P.ratios[k] && (P.ratios[k].bar < 3 || P.ratios[k].track < 3)) fails.push(`${part} ${k} vs bar/track < 3`);
  if (P.ratios.fill.bar < 3) fails.push(`${part} fill vs gap < 3`);
  out.parts[part] = P;
}
// readout
const readout = {};
for (const a of [0.4, 0.5, 0.55, 0.6]) { const c = over('#ffffff', a, BAR); readout[a] = { composite: c, ratio: r2(contrast(c, BAR)) }; }
out.readoutAlpha = { chosen: READOUT_ALPHA, css: `rgba(255,255,255,${READOUT_ALPHA})`, ratio: readout[READOUT_ALPHA].ratio, candidates: readout };
if (readout[READOUT_ALPHA].ratio < 5.3) fails.push('readout alpha < 5.3:1');
// cross-volume hue report
out.hueBySlot = {};
for (let s = 1; s <= 5; s++) out.hueBySlot[s] = Object.fromEntries(Object.entries(out.parts).map(([p, P]) => [p, P.slots[s - 1].oklch.C < 0.02 ? `neutral (C ${P.slots[s - 1].oklch.C})` : P.slots[s - 1].oklch.h]));
out.fails = fails;

const here = dirname(fileURLToPath(import.meta.url));
writeFileSync(join(here, 'pass25-palette.json'), JSON.stringify(out, null, 2));

// ---------- markdown table ----------
const roman = { 'part-1': 'I', 'part-2': 'II', 'part-3': 'III', 'part-4': 'IV', 'part-5': 'V' };
let md = '| Part | Slot | Name | Hex | Glyph | Bar / chapter nav / page | OKLCH h (C) | Spec §7 had |\n|---|---|---|---|---|---|---|---|\n';
for (const [p, P] of Object.entries(out.parts)) for (const s of P.slots)
  md += `| ${roman[p]} | ${s.slot} ${s.family} | ${s.name} | \`${s.hex}\` | ${s.glyphName} | ${s.ratios.bar.toFixed(2)} / ${s.ratios.chapterNav.toFixed(2)} / ${s.ratios.page.toFixed(2)} | ${s.oklch.C < 0.02 ? 'neutral' : s.oklch.h.toFixed(0) + '°'} (${s.oklch.C.toFixed(3)}) | ${s.wasInSpec ? s.wasInSpec.replace(/^(#[0-9a-f]{6})/, '`$1`') : 'kept'} |\n`;
md += '\nMinimum pairwise CIEDE2000 within each volume (pair in brackets):\n\n| Part | Normal | Protanopia | Deuteranopia | Tritanopia |\n|---|---|---|---|---|\n';
for (const [p, m] of Object.entries(out.minDeltaE)) md += `| ${roman[p]} | ${MODES.map(k => `${m[k].deltaE.toFixed(1)} (${m[k].pair.join('–')})`).join(' | ')} |\n`;
md += '\nSame slot across volumes, OKLCH hue (N = neutral, C < 0.02):\n\n| Slot | I | II | III | IV | V |\n|---|---|---|---|---|---|\n';
for (let k = 1; k <= 5; k++) md += `| ${k} ${FAMILY[k].name} | ${Object.values(out.hueBySlot[k]).map(v => (typeof v === 'number' ? v.toFixed(0) + '°' : 'N')).join(' | ')} |\n`;
md += '\nCue colours (saved mark, head fill). Mark vs fill is below 3:1 in every volume; the 1px `#0a0a0a` gap around the mark carries the separation (mark vs gap and gap vs fill both >= 3:1):\n\n| Part | Mark | Fill | Mark vs bar / track / fill / gap | Fill vs track | Gap vs fill |\n|---|---|---|---|---|---|\n';
for (const [p, P] of Object.entries(out.parts)) {
  const row = (lab, m, r) => `| ${roman[p]}${lab} | \`${m}\` | \`${P.fill}\` | ${r.bar.toFixed(2)} / ${r.track.toFixed(2)} / ${r.fill.toFixed(2)} / ${r.gap.toFixed(2)} | ${P.ratios.fill.track.toFixed(2)} | ${P.ratios.fill.gapVsFill.toFixed(2)} |\n`;
  md += row(p === 'part-5' ? ' local' : '', P.mark, P.ratios.mark);
  if (P.markSynced) md += row(' synced', P.markSynced, P.ratios.markSynced);
}
md += `\nReadout \`.book-progress\` (10px DM Mono) over \`#0a0a0a\`: ${Object.entries(readout).map(([a, v]) => `α ${a} → ${v.ratio.toFixed(2)}:1`).join(', ')}. Chosen: \`rgba(255,255,255,${READOUT_ALPHA})\`.\n`;
writeFileSync(join(here, 'pass25-palette-table.md'), md);

// ---------- contact sheet ----------
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
let html = `<!doctype html><meta charset="utf-8"><title>Pass 25 glyphs</title><style>
body{margin:0;background:#2a2a2a;font:11px/1.3 ui-monospace,Menlo,monospace;color:#ccc;padding:12px}
h2{font-size:13px;margin:14px 0 4px;color:#eee}.vol{display:flex;gap:8px;flex-wrap:wrap}
.g{padding:8px 10px;border-radius:4px;min-width:400px}.row{display:flex;align-items:center;gap:10px;margin:4px 0}
.lbl{width:96px;font-size:10px;opacity:.75}.cell{display:inline-flex;align-items:center;gap:6px;width:150px}
svg{display:block;flex:none}.cue{position:relative;height:8px;width:380px;background:${TRACK};margin:8px 0 2px}
.cue i{position:absolute;left:0;top:0;bottom:0}.cue b{position:absolute;top:-2px;bottom:-2px;outline:1px solid ${BAR}}
</style>`;
for (const [p, P] of Object.entries(out.parts)) {
  const g = GROUNDS[p];
  html += `<h2>Part ${roman[p]}</h2><div class="vol">`;
  for (const [gname, bg] of [['bar', BAR], ['chapter nav', g.nav], ['page', g.page]]) {
    const fg = gname === 'page' ? '#333' : '#bbb';
    html += `<div class="g" style="background:${bg};color:${fg}"><div style="font-size:10px">${gname} ${bg}</div>`;
    for (const sz of [10, 12, 40]) {
      html += `<div class="row"><span class="lbl">${sz}px</span>`;
      for (const s of P.slots) html += `<span style="color:${s.hex}"><svg width="${sz}" height="${sz}" viewBox="0 0 10 10" aria-hidden="true">${s.svg}</svg></span>`;
      html += `</div>`;
    }
    html += `<div class="row">${P.slots.map(s => `<span class="cell" style="width:auto"><span style="color:${s.hex}"><svg width="12" height="12" viewBox="0 0 10 10">${s.svg}</svg></span><span style="color:${s.hex}">${esc(s.name)}</span></span>`).join('')}</div>`;
    html += `</div>`;
  }
  html += `</div>`;
  // cue demo on the bar
  html += `<div style="background:${BAR};padding:8px 10px;width:400px;margin-top:6px"><div style="font-size:10px;color:rgba(255,255,255,${READOUT_ALPHA})">CH 4 · §03 · ¶7 — readout α ${READOUT_ALPHA}</div>
  <div class="cue"><i style="width:55%;background:${P.fill}"></i><b style="left:40%;width:3px;background:${P.mark}"></b>${P.markSynced ? `<b style="left:70%;width:3px;background:${P.markSynced}"></b>` : ''}</div>
  <div class="cue" style="height:2px"><i style="width:55%;background:${P.fill}"></i><b style="left:40%;width:3px;background:${P.mark}"></b></div></div>`;
}
writeFileSync(join(here, 'pass25-contact-sheet.html'), html);

// ---------- console summary ----------
for (const [p, P] of Object.entries(out.parts)) {
  console.log(`${p}: ` + P.slots.map(s => `${s.slot}:${s.name} ${s.hex} ${s.ratios.bar}/${s.ratios.chapterNav}/${s.ratios.page} h${s.oklch.C < 0.02 ? 'N' : s.oklch.h.toFixed(0)}`).join(' | '));
  console.log('   minΔE ' + MODES.map(m => `${m.slice(0, 4)} ${out.minDeltaE[p][m].deltaE}`).join(' ') + `  mark ${JSON.stringify(P.ratios.mark)} fill ${JSON.stringify(P.ratios.fill)}${P.markSynced ? ' synced ' + JSON.stringify(P.ratios.markSynced) : ''}`);
}
console.log('readout', JSON.stringify(out.readoutAlpha.candidates));
console.log(fails.length ? 'FAIL:\n  ' + fails.join('\n  ') : 'ALL HARD CONSTRAINTS PASS');
process.exitCode = fails.length ? 1 : 0;
