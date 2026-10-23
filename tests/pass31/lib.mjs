// Pass 31 shared helpers (docs/pass-31-brief.md; docs/pass-31-calibration.md): the figure cards of a part, the
// judge's prose packet, the taught-yet token check, and small process helpers. Used by sheet.mjs, check.mjs and gate.mjs.
import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process';

export const REPO = new URL('../../', import.meta.url).pathname;
export const PUBLIC = path.join(REPO, 'public') + '/';
export const OUT = path.join(REPO, 'tests/pass31/out') + '/';
export const PARTS = ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];

export const args = argv => {
  const pos = [], o = {};
  for (const a of argv) { const m = a.match(/^--([^=]+)(?:=([\s\S]*))?$/); if (m) o[m[1]] = m[2] ?? true; else pos.push(a); }
  return { pos, o };
};
export const tree = t => (t ? path.resolve(t) : PUBLIC.slice(0, -1)) + '/';
export const readPart = (root, part) => fs.readFileSync(path.join(root, part + '.html'), 'utf8');

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“', hellip: '…', times: '×', minus: '−', middot: '·', rarr: '→', larr: '←', euro: '€', pound: '£' };
export const dec = s => s.replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e) => e[0] === '#' ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1)) : (ENT[e] ?? m));
export const plain = h => dec(h.replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();

// a card: <div class="diagram-card|light-diagram ..." id="fig-..."> label, svg, caption, optional strip </div>
const CARD = /<div class="(?:diagram-card|light-diagram)[^"]*" id="([^"]+)">[\s\S]*?<\/svg>\s*<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>\s*(?:<details class="fig-how">[\s\S]*?<\/details>\s*)?<\/div>/g;
export function figures(html, part) {
  const secs = [...html.matchAll(/<section class="section" id="(ch[^"]+)"/g)].map(m => ({ id: m[1], at: m.index }));
  const out = [];
  for (const m of html.matchAll(CARD)) {
    const card = m[0], id = m[1];
    const sec = secs.filter(s => s.at < m.index).pop();
    const svg = (card.match(/<svg[\s\S]*<\/svg>/) || [''])[0];
    const cap = card.match(/<p\b([^>]*)class="diagram-caption"[^>]*>([\s\S]*?)<\/p>/);
    const how = (card.match(/<details class="fig-how">([\s\S]*?)<\/details>/) || [])[1] || '';
    out.push({
      id, part, at: m.index, end: m.index + card.length, card, svg,
      section: sec ? sec.id : null, chapter: sec ? sec.id.split('-')[0] : null,
      label: plain((card.match(/<div class="diagram-label">([\s\S]*?)<\/div>/) || [])[1] || ''),
      title: plain((svg.match(/<title[^>]*>([\s\S]*?)<\/title>/) || [])[1] || ''),
      desc: (svg.match(/<desc[^>]*>([\s\S]*?)<\/desc>/) || [])[1] ?? null,
      caption: cap ? plain(cap[2]) : '', captionId: cap ? (cap[1].match(/id="([^"]+)"/) || [])[1] : null,
      how: [...how.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/g)].map(x => plain(x[1])),
    });
  }
  return out;
}
export function allFigures(root) { return PARTS.flatMap(p => figures(readPart(root, p), p)); }
export function findFigure(root, id) { return allFigures(root).find(f => f.id === id) || null; }

// ---- the judge's prose packet: the book up to the figure, prose only ------------------------------------------
// Every earlier part whole, then this part up to the card. Taken out: every figure card (label, picture, caption,
// strip), every other <svg>, scripts, styles, navigation, comments. Never the figure's caption or strip.
function prose(html) {
  let h = html.replace(/<!--[\s\S]*?-->/g, '').replace(/<head[\s\S]*?<\/head>/i, '')
    .replace(/<(script|style|nav|button|noscript)\b[\s\S]*?<\/\1>/gi, '')
    .replace(CARD, '\n')
    .replace(/<svg[\s\S]*?<\/svg>/g, '')
    .replace(/<details class="fig-how">[\s\S]*?<\/details>/g, '')
    .replace(/<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>/g, '');
  h = h.replace(/<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi, (m, n, t) => `\n\n${'#'.repeat(Math.min(+n, 4))} ${plain(t)}\n\n`)
    .replace(/<li\b[^>]*>/gi, '\n- ').replace(/<\/(p|div|section|li|blockquote|tr|table|pre|ul|ol|aside|figure|header|main|article)>/gi, '\n')
    .replace(/<(br|hr)\b[^>]*>/gi, '\n').replace(/<\/t[dh]>/gi, ' | ');
  return dec(h.replace(/<[^>]+>/g, '')).split('\n').map(l => l.replace(/[ \t]+/g, ' ').trim()).filter((l, i, a) => l || (a[i - 1] && a[i - 1].trim()))
    .join('\n').replace(/\n{3,}/g, '\n\n').trim();
}
export function packet(root, fig) {
  const parts = PARTS.slice(0, PARTS.indexOf(fig.part));
  const chunks = parts.map(p => prose(readPart(root, p)));
  chunks.push(prose(readPart(root, fig.part).slice(0, fig.at)));
  return chunks.join('\n\n').trim();
}

// ---- taught-yet (brief section 15) ----------------------------------------------------------------------------
// Every label and object token is: a number or a sign (arithmetic signs and arrows), a term known-terms.mjs lists
// before the figure's section (or a term this section teaches in the prose before the figure), or an everyday word
// (in /usr/share/dict/words after plain inflections are stripped, not a glossary term anywhere in the book, and not
// an all-capitals abbreviation of two or more letters). A single letter is an everyday token (a key, a lamp).
let DICT = null;
const dict = () => DICT || (DICT = new Set(fs.readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim().toLowerCase()).filter(Boolean)));
const stems = w => {
  const s = [w];
  if (w.endsWith('ies')) s.push(w.slice(0, -3) + 'y');
  if (w.endsWith('es')) s.push(w.slice(0, -2));
  if (w.endsWith('s')) s.push(w.slice(0, -1));
  if (w.endsWith("'s") || w.endsWith('’s')) s.push(w.slice(0, -2));
  if (w.endsWith('ing')) { s.push(w.slice(0, -3)); s.push(w.slice(0, -3) + 'e'); if (/(.)\1ing$/.test(w)) s.push(w.slice(0, -4)); }
  if (w.endsWith('ed')) { s.push(w.slice(0, -2)); s.push(w.slice(0, -1)); if (/(.)\1ed$/.test(w)) s.push(w.slice(0, -3)); }
  if (w.endsWith('ied')) s.push(w.slice(0, -3) + 'y');
  if (w.endsWith('er')) { s.push(w.slice(0, -2)); s.push(w.slice(0, -1)); }
  if (w.endsWith('ly')) s.push(w.slice(0, -2));
  if (w.endsWith("n't")) s.push(w.slice(0, -3));
  // British spellings: centralised -> centralized, colour -> color
  for (const x of [...s]) { if (/is(e|ed|es|ing|ation)$/.test(x)) s.push(x.replace(/is(e|ed|es|ing|ation)$/, 'iz$1')); if (/our$/.test(x)) s.push(x.replace(/our$/, 'or')); }
  return s;
};
const normT = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();
export const SIGN = /^[+\-−×÷=<>≤≥≠≈*/%^()[\]{}|~→←↑↓↔⇒⇐·•…,.:;!?'"“”‘’&#@$€£¥°±√∑∞]+$/u;
// short words that are written in capitals in headings and are never abbreviations
const SHORT = new Set('a an the of to in on at by for and or nor but not no yes is are was be it its as if so do up out off all any one two six ten new old big end key run set put get add top low own per via who why how now then than this that each into from with what when'.split(' '));
const NUMBER = /^[€£$]?[+\-−]?\d[\d.,:]*(?:st|nd|rd|th)?(?:[%°]|[kKMGT]?B|[kmµn]?s|×)?$/u;

let KT = null;
export function knownTerms(file) {
  if (KT && KT.file === file) return KT;
  const j = JSON.parse(fs.readFileSync(file, 'utf8'));
  const glossary = new Set(Object.keys(j.taught).map(normT));
  return (KT = { file, j, glossary, by: new Map(j.by_section.map(s => [s.section, s])) });
}
// the terms taught before the figure: known before its section, plus those its section teaches in prose before the card
export function taughtBefore(kt, fig, partHtml) {
  const s = kt.by.get(fig.section); if (!s) return null;
  const secStart = partHtml.indexOf(`<section class="section" id="${fig.section}"`);
  const before = secStart >= 0 ? plain(partHtml.slice(secStart, fig.at).replace(CARD, ' ').replace(/<svg[\s\S]*?<\/svg>/g, ' ')).toLowerCase() : '';
  const inSec = s.defines.filter(t => before.includes(t.toLowerCase()));
  return [...s.known, ...inSec].map(normT);
}
export function svgTexts(svg) {
  return [...svg.replace(/<(title|desc)\b[\s\S]*?<\/\1>/g, '').matchAll(/<text\b([^>]*)>([\s\S]*?)<\/text>/g)].map(m => ({ attrs: m[1], s: plain(m[2]) })).filter(t => t.s);
}
export function taughtYet(text, known, glossary, before = '') {
  const bad = [];
  let s = ' ' + normT(text) + ' ';
  // known multi-word terms first (longest first), so "turing machine" is taken whole
  for (const t of [...known].sort((a, b) => b.length - a.length)) {
    const re = new RegExp(`(^|[^\\p{L}\\p{N}])${t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(s|es)?(?=$|[^\\p{L}\\p{N}])`, 'gu');
    s = s.replace(re, '$1 ');
  }
  const raw = text.split(/\s+/);
  for (const tok0 of s.split(/[\s·•,;:!?"“”()[\]{}]+/u)) {
    const tok = tok0.replace(/^['‘’.]+|['‘’.]+$/g, ''); if (!tok) continue;
    if (SIGN.test(tok) || NUMBER.test(tok)) continue;
    // arithmetic written solid: 3+1=4, 1011=11, /22
    if (/^[\d+\-−×÷=<>≤≥*/%^().]+$/u.test(tok) && /\d/.test(tok) && !/^\//.test(tok)) continue;
    if (/^\p{L}$/u.test(tok)) continue;                                      // one letter
    if (/^\/\d/.test(tok)) { bad.push({ token: tok, why: 'notation, not a plain number' }); continue; }   // /22
    const orig = (raw.find(r => r.toLowerCase().replace(/[^\p{L}\p{N}'’-]/gu, '') === tok.replace(/[^\p{L}\p{N}'’-]/gu, '')) || tok).replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
    const letters = orig.replace(/[^\p{L}]/gu, '');
    const caps = letters.length >= 2 && letters === letters.toUpperCase() && /\p{Lu}/u.test(letters);
    for (const part of tok.split(/[-–/]/)) {
      if (!part) continue;
      if (NUMBER.test(part) || SIGN.test(part) || /^\p{L}$/u.test(part)) continue;
      if (glossary.has(part)) { bad.push({ token: part, why: 'a glossary term not yet taught' }); continue; }
      const inDict = stems(part).some(w => dict().has(w));
      // all capitals: a heading word in capitals passes (THE, ITS, ROTORS); an abbreviation does not (EAX, CGNAT, IHL).
      // Three letters or fewer pass only as a common short word, since many abbreviations are also rare dictionary words.
      const title = part[0].toUpperCase() + part.slice(1);   // LINUX written for a name the prose spells Linux
      if (caps) { if (part.length <= 3 ? SHORT.has(part) : inDict) continue; if (before && part.length >= 4 && new RegExp(`(^|[^\\p{L}])${title}(?![\\p{L}])`, 'u').test(before)) continue;
        // an abbreviation the prose before the figure spells out: "main memory (RAM)", "ALU (arithmetic and logic unit)"
        const AB = part.toUpperCase();
        if (before && (before.includes(`(${AB})`) || new RegExp(`(^|[^\\p{L}])${AB} \\([\\p{Ll}]`, 'u').test(before))) continue;
        bad.push({ token: orig, why: 'an all-capitals abbreviation' }); continue; }
      if (inDict) continue;
      // a proper name (capital first letter, not all capitals) that the prose before the figure already uses
      if (/^\p{Lu}\p{Ll}/u.test(orig) && before && new RegExp(`(^|[^\\p{L}])${orig.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'u').test(before)) continue;
      bad.push({ token: part, why: /\d/.test(part) ? 'notation, not a plain number' : 'not an everyday word' });
    }
  }
  return bad;
}

// ---- label cap: a tag-stack walk over the svg -----------------------------------------------------------------
const SHAPE = /^(rect|circle|ellipse|line|polyline|polygon|path|use|image)$/;
export function capCount(svg) {
  const s = svg.replace(/<(title|desc)\b[\s\S]*?<\/\1>/g, '');
  const stack = [], texts = [], groups = [];
  for (const m of s.matchAll(/<(\/?)([a-zA-Z][\w:-]*)\b([^>]*?)(\/?)>|([^<]+)/g)) {
    if (m[5] !== undefined) { const t = stack.findLast(e => e.name === 'text'); if (t) t.s += m[5]; continue; }
    const [, close, name, attrs, self] = m;
    if (close) { const e = stack.pop(); if (e && e.name === 'text') texts.push(e); continue; }
    const e = { name, attrs, s: '', anc: stack.slice(), shape: false };
    if (SHAPE.test(name)) for (const a of stack) if (a.name === 'g') a.shape = true;
    if (name === 'g') groups.push(e);
    if (!self) stack.push(e);
  }
  const panels = new Map();
  const rows = texts.map(t => {
    const str = plain(t.s), role = (t.attrs.match(/\bdata-role="([^"]+)"/) || [])[1] || null;
    const og = t.anc.findLast(a => a.name === 'g' && /\bdata-obj="1"/.test(a.attrs));
    const free = role === 'object' && og && og.shape && [...str].length <= 6;
    const pg = t.anc.find(a => a.name === 'g' && /\bdata-panel\b/.test(a.attrs));
    const panel = pg ? (pg.attrs.match(/data-panel="([^"]*)"/) || [, 'panel'])[1] : 'figure';
    return { str, role, free, panel, why: free ? 'object' : role === 'object' ? (og ? (og.shape ? 'object over 6 characters: counted as label' : 'obj group without a shape: counted as label') : 'object outside obj(): counted as label') : role ? 'label' : 'untagged: counted as label' };
  }).filter(r => r.str);
  for (const r of rows) if (!r.free) panels.set(r.panel, (panels.get(r.panel) || 0) + 1);
  return { rows, panels: Object.fromEntries(panels), max: Math.max(0, ...panels.values()) };
}
// ---- caption sentences ----------------------------------------------------------------------------------------
const ABBR = /\b(e\.g|i\.e|etc|vs|Fig|Figs|No|Dr|Mr|Mrs|Ms|St|approx|cf|al|U\.S|U\.K|a\.m|p\.m)\./g;
export function sentences(t) {
  const s = t.replace(ABBR, m => m.replace(/\./g, '․')).replace(/(\d)\.(\d)/g, '$1․$2');
  return s.split(/(?<=[.!?])["”’)\]]*\s+(?=["“‘(\[]?[A-Z0-9])/).map(x => x.trim()).filter(x => /[\p{L}\p{N}]/u.test(x));
}

// ---- processes ------------------------------------------------------------------------------------------------
export function run(cmd, argv, { cwd = REPO, env = {}, input = null, quiet = true, timeout = 0 } = {}) {
  return new Promise((res) => {
    const p = spawn(cmd, argv, { cwd, env: { ...process.env, ...env }, stdio: ['pipe', 'pipe', 'pipe'] });
    let out = '', err = '', timer = null;
    if (timeout) timer = setTimeout(() => { p.kill('SIGTERM'); err += `\n[timeout after ${timeout} ms]`; }, timeout);
    p.stdout.on('data', d => { out += d; if (!quiet) process.stdout.write(d); });
    p.stderr.on('data', d => { err += d; if (!quiet) process.stderr.write(d); });
    p.on('close', code => { if (timer) clearTimeout(timer); res({ code, out, err }); });
    if (input !== null) p.stdin.end(input); else p.stdin.end();
  });
}
export const sh = (cmd, argv, o) => run(cmd, argv, o);
export const mkdirp = d => (fs.mkdirSync(d, { recursive: true }), d);
// bare.mjs files are named <id>-<width>-t<time>[-notext].png; sort them by time
export function framesIn(dir, id, width = 375, notext = false) {
  return fs.readdirSync(dir).filter(f => f.startsWith(`${id}-${width}-t`) && f.endsWith(notext ? '-notext.png' : '.png') && (notext || !f.endsWith('-notext.png')))
    .map(f => ({ f: path.join(dir, f), t: parseFloat(f.slice(`${id}-${width}-t`.length)) })).sort((a, b) => a.t - b.t);
}
