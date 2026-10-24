// Pass 31 shared helpers (docs/pass-31-brief.md; docs/pass-31-calibration.md): the figure cards of a part, the
// judge's prose packet, the taught-yet token check, and small process helpers. Used by sheet.mjs, check.mjs and gate.mjs.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import { spawn } from 'node:child_process';

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

// ---- taught-yet (brief section 15; docs/pass-31-calibration.md section 13) ------------------------------------
// Every label and object token is one of:
//   - a number or a sign (arithmetic signs and arrows); a single letter (a key, a lamp);
//   - a term taught before the figure: known-terms.mjs lists it before the figure's section, or the section teaches
//     it in the prose before the card, or (an all-capitals abbreviation) the prose paragraph that first uses it comes
//     before the card. Prose never includes a figure card, so a term first written in the figure's own caption, label
//     or How-it-works strip is not taught for that figure;
//   - an everyday word: in /usr/share/dict/words or on the COMMON-word list (tests/pass31/common-words.txt), after
//     plain inflections are stripped (lowest, became, rewritten, databases), and not a glossary term (single or
//     multi-word, in any inflection) the figure has not yet taught;
//   - an all-capitals token only when the prose before the figure teaches it (above), when its lowercase form is on
//     the COMMON-word list (THE, KEY, PRESS), or when it is an everyday word set in capitals: four letters or more,
//     a lowercase dictionary entry, not a glossary term, and never written in capitals anywhere in the book's text
//     (so it is not an abbreviation the book uses: LAMP, ROTORS pass; ARM, RAM, OS, MAC, LAN, NAT, CPU do not until
//     taught). Three letters or fewer pass only through the COMMON-word list or teaching (AX, AL, DOS fail);
//   - a proper name the prose before the figure already uses (Shannon; LINUX for a name the prose spells Linux).
let DICT = null, LOWER = null, COMMON = null;
const dict = () => DICT || (DICT = new Set(fs.readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim().toLowerCase()).filter(Boolean)));
const lowerDict = () => LOWER || (LOWER = new Set(fs.readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim()).filter(w => w && w === w.toLowerCase())));
export const COMMON_FILE = new URL('./common-words.txt', import.meta.url).pathname;
export const common = () => COMMON || (COMMON = new Set(fs.readFileSync(COMMON_FILE, 'utf8').split('\n').map(w => w.trim()).filter(w => w && !w.startsWith('#'))));
// irregular forms of everyday words (past tenses, participles, plurals, comparatives): form -> stem
const IRREGULAR = Object.fromEntries(`became:become began:begin begun:begin bent:bend bound:bind bred:breed brought:bring built:build bought:buy
caught:catch chose:choose chosen:choose clung:cling crept:creep dealt:deal did:do done:do drew:draw drawn:draw dug:dig drove:drive driven:drive
ate:eat eaten:eat fed:feed fell:fall fallen:fall felt:feel fled:flee flung:fling flew:fly flown:fly fought:fight found:find forgot:forget
forgotten:forget froze:freeze frozen:freeze gave:give given:give went:go gone:go grew:grow grown:grow hung:hang had:have has:have heard:hear
held:hold hid:hide hidden:hide kept:keep knew:know known:know laid:lay led:lead left:leave lent:lend lit:light lost:lose made:make meant:mean
met:meet paid:pay ran:run rang:ring rose:rise risen:rise rode:ride ridden:ride said:say sang:sing sung:sing sank:sink sunk:sink sat:sit saw:see
seen:see sent:send shook:shake shaken:shake shone:shine shot:shoot showed:show shown:show slept:sleep slid:slide sold:sell sought:seek
spent:spend spoke:speak spoken:speak sped:speed spun:spin stole:steal stolen:steal stood:stand stuck:stick struck:strike swept:sweep
swung:swing swam:swim swum:swim swore:swear sworn:swear took:take taken:take taught:teach tore:tear torn:tear told:tell thought:think
threw:throw thrown:throw understood:understand woke:wake woken:wake wore:wear worn:wear won:win wound:wind wrote:write written:write
children:child men:man women:woman feet:foot teeth:tooth mice:mouse geese:goose indices:index matrices:matrix vertices:vertex axes:axis
analyses:analysis criteria:criterion phenomena:phenomenon better:good best:good worse:bad worst:bad less:little least:little more:much most:much`
  .split(/\s+/).filter(Boolean).map(x => x.split(':')));
const PREFIX = /^(re|un|over|under|pre|mis|out|up|sub|non)(?=[a-z]{3,})/;
export const stems = (w, deep = true) => {
  const s = [w];
  if (IRREGULAR[w]) s.push(IRREGULAR[w]);
  if (w.endsWith('ies')) s.push(w.slice(0, -3) + 'y');
  if (w.endsWith('es')) s.push(w.slice(0, -2));
  if (w.endsWith('s')) s.push(w.slice(0, -1));
  if (w.endsWith("'s") || w.endsWith('’s')) s.push(w.slice(0, -2));
  if (w.endsWith('ing')) { s.push(w.slice(0, -3)); s.push(w.slice(0, -3) + 'e'); if (/(.)\1ing$/.test(w)) s.push(w.slice(0, -4)); }
  if (w.endsWith('ed')) { s.push(w.slice(0, -2)); s.push(w.slice(0, -1)); if (/(.)\1ed$/.test(w)) s.push(w.slice(0, -3)); }
  if (w.endsWith('ied')) s.push(w.slice(0, -3) + 'y');
  if (w.endsWith('er')) { s.push(w.slice(0, -2)); s.push(w.slice(0, -1)); if (/(.)\1er$/.test(w)) s.push(w.slice(0, -3)); }
  if (w.endsWith('ier')) s.push(w.slice(0, -3) + 'y');
  if (w.endsWith('est')) { s.push(w.slice(0, -3)); s.push(w.slice(0, -2)); if (/(.)\1est$/.test(w)) s.push(w.slice(0, -4)); }   // lowest, largest, biggest
  if (w.endsWith('iest')) s.push(w.slice(0, -4) + 'y');                                                                       // easiest
  if (/(.)\1en$/.test(w)) { s.push(w.slice(0, -3) + 'e'); s.push(w.slice(0, -3)); }                                          // written, bitten, rewritten
  else if (w.endsWith('en')) { s.push(w.slice(0, -2)); s.push(w.slice(0, -1)); }                                             // fallen, taken
  if (/(?:[aeo]w|ee)n$/.test(w)) s.push(w.slice(0, -1));                                                                      // shown, seen
  if (w.endsWith('ly')) s.push(w.slice(0, -2));
  if (w.endsWith("n't")) s.push(w.slice(0, -3));
  // British spellings: centralised -> centralized, colour -> color
  for (const x of [...s]) { if (/is(e|ed|es|ing|ation)$/.test(x)) s.push(x.replace(/is(e|ed|es|ing|ation)$/, 'iz$1')); if (/our$/.test(x)) s.push(x.replace(/our$/, 'or')); }
  // a plain prefix on an everyday word: rewrote, overwritten, unpaid
  if (deep && PREFIX.test(w)) for (const x of stems(w.replace(PREFIX, ''), false)) s.push(x);
  return s;
};
const normT = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();
const esc = t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export const SIGN = /^[+\-−×÷=<>≤≥≠≈*/%^()[\]{}|~→←↑↓↔⇒⇐·•…,.:;!?'"“”‘’&#@$€£¥°±√∑∞]+$/u;
const NUMBER = /^[€£$]?[+\-−]?\d[\d.,:]*(?:st|nd|rd|th)?(?:[%°]|[kKMGT]?B|[kmµn]?s|×)?$/u;

let KT = null;
export function knownTerms(file) {
  if (KT && KT.file === file) return KT;
  const j = JSON.parse(fs.readFileSync(file, 'utf8'));
  const glossary = new Set(Object.keys(j.taught).map(normT));
  // glossary entries that are proper names (a capital, then lower case: "Shannon", not "ALU"): a figure may use the
  // name once the prose before it has (the reader has met the person or place; the entry teaches more about them later)
  glossary.names = new Set(Object.keys(j.taught).filter(k => /^\p{Lu}\p{Ll}/u.test(k)).map(normT));
  // multi-word entries (normalised, longest first), each with its written form: "system call", "Ring 0", "log scale"
  glossary.multi = Object.keys(j.taught).filter(k => normT(k).includes(' ')).map(k => ({ t: normT(k), form: k })).sort((a, b) => b.t.length - a.t.length);
  // every all-capitals token the book's text writes outside the figure cards (known-terms.mjs "capitals")
  glossary.capitals = new Set(j.capitals || []);
  if (!j.abbreviations || !j.capitals) throw new Error(`${file}: no abbreviations or capitals (scripts/known-terms.mjs is older than the Pass 31 follow-up)`);
  return (KT = { file, j, glossary, abbrev: j.abbreviations, by: new Map(j.by_section.map(s => [s.section, s])) });
}
// the terms taught before the figure: known before its section, those its section teaches in prose before the card,
// and every all-capitals abbreviation whose first prose paragraph comes before the card (known-terms.mjs must have
// read the same tree as partHtml: run it with --public=<tree>)
export function taughtBefore(kt, fig, partHtml) {
  const s = kt.by.get(fig.section); if (!s) return null;
  const secStart = partHtml.indexOf(`<section class="section" id="${fig.section}"`);
  const before = secStart >= 0 ? plain(partHtml.slice(secStart, fig.at).replace(CARD, ' ').replace(/<svg[\s\S]*?<\/svg>/g, ' ')).toLowerCase() : '';
  const inSec = s.defines.filter(t => before.includes(t.toLowerCase()));
  const pi = PARTS.indexOf(fig.part);
  const ab = Object.entries(kt.abbrev).filter(([, a]) => PARTS.indexOf(a.part) < pi || (a.part === fig.part && a.at < fig.at)).map(([t]) => t);
  return [...s.known, ...inSec, ...ab].map(normT);
}
export function svgTexts(svg) {
  return [...svg.replace(/<(title|desc)\b[\s\S]*?<\/\1>/g, '').matchAll(/<text\b([^>]*)>([\s\S]*?)<\/text>/g)].map(m => ({ attrs: m[1], s: plain(m[2]) })).filter(t => t.s);
}
const B = '[^\\p{L}\\p{N}_]';   // a word boundary that keeps SYN_SENT and CR3 whole
export function taughtYet(text, known, glossary, before = '') {
  const bad = [];
  let s = ' ' + normT(text) + ' ';
  // known terms first (longest first), so "turing machine" is taken whole
  for (const t of [...known].sort((a, b) => b.length - a.length)) s = s.replace(new RegExp(`(^|${B})${esc(t)}(s|es)?(?=$|${B})`, 'gu'), '$1 ');
  // then multi-word glossary terms not yet taught ("system call", "ring 0"): each fails whole, even when every word in
  // it is an everyday word; a named one ("Bell Labs", "von Neumann") passes once the prose before the figure uses it.
  // Matched on the text as written (a hyphen in the term needs a hyphen: "a-machine" is not "a machine").
  const knownSet = new Set(known), rawL = ' ' + text.toLowerCase().replace(/\s+/g, ' ') + ' ';
  for (const { t, form } of glossary.multi || []) {
    if (knownSet.has(t)) continue;
    const pat = form.toLowerCase().split(/(\s+|[-–])/).map(x => /^\s+$/.test(x) ? '[\\s\\-–]+' : /^[-–]$/.test(x) ? '[-–]' : esc(x)).join('');
    if (!new RegExp(`(^|${B})${pat}(s|es)?(?=$|${B})`, 'u').test(rawL)) continue;
    if (!(/\p{Lu}/u.test(form) && before && new RegExp(`(^|[^\\p{L}])${esc(form)}(?![\\p{L}])`, 'u').test(before))) bad.push({ token: t, why: 'a glossary term not yet taught' });
    s = s.replace(new RegExp(`(^|${B})${esc(t)}(s|es)?(?=$|${B})`, 'gu'), '$1 ');
  }
  const raw = text.split(/\s+/);
  for (const tok0 of s.split(/[\s·•,;:!?"“”()[\]{}]+/u)) {
    const tok = tok0.replace(/^['‘’.]+|['‘’.]+$/g, ''); if (!tok) continue;
    if (SIGN.test(tok) || NUMBER.test(tok)) continue;
    // arithmetic written solid: 3+1=4, 1011=11, /22
    if (/^[\d+\-−×÷=<>≤≥*/%^().]+$/u.test(tok) && /\d/.test(tok) && !/^\//.test(tok)) continue;
    if (/^\p{L}$/u.test(tok)) continue;                                      // one letter
    if (/^\/\d/.test(tok)) { bad.push({ token: tok, why: 'notation, not a plain number' }); continue; }   // /22
    const orig = (raw.find(r => r.toLowerCase().replace(/[^\p{L}\p{N}'’_-]/gu, '') === tok.replace(/[^\p{L}\p{N}'’_-]/gu, '')) || tok).replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
    const letters = orig.replace(/[^\p{L}]/gu, '');
    const caps = letters.length >= 2 && letters === letters.toUpperCase() && /\p{Lu}/u.test(letters);
    for (const part of tok.split(/[-–/]/)) {
      if (!part) continue;
      if (NUMBER.test(part) || SIGN.test(part) || /^\p{L}$/u.test(part)) continue;
      const st = stems(part), g = st.find(w => glossary.has(w));
      if (g !== undefined) {   // a glossary term (in any inflection) the figure has not yet taught
        const name = g[0].toUpperCase() + g.slice(1);
        if (glossary.names && glossary.names.has(g) && before && new RegExp(`(^|[^\\p{L}])${esc(name)}(?![\\p{L}])`, 'u').test(before)) continue;
        bad.push({ token: part, why: 'a glossary term not yet taught' }); continue; }
      const everyday = st.some(w => dict().has(w) || common().has(w));
      const title = part[0].toUpperCase() + part.slice(1);   // LINUX written for a name the prose spells Linux
      if (caps) {
        const AB = part.toUpperCase();
        if ((part.length >= 4 ? st : [part]).some(w => common().has(w))) continue;                    // THE, KEY, PRESS (inflected only from four letters: DOS is not "do")
        if (part.replace(/[^\p{L}]/gu, '').length >= 4 && !st.some(w => glossary.capitals?.has(w.toUpperCase())) && st.some(w => lowerDict().has(w) || common().has(w))) continue;   // LAMP, ROTORS
        if (before && part.length >= 4 && /^\p{L}+$/u.test(part) && new RegExp(`(^|[^\\p{L}])${esc(title)}(?![\\p{L}])`, 'u').test(before)) continue;   // LINUX
        bad.push({ token: orig.includes('-') || orig.includes('/') ? AB : orig, why: 'an all-capitals abbreviation not taught before the figure' }); continue; }
      if (everyday) continue;
      // a proper name (capital first letter, not all capitals) that the prose before the figure already uses
      if (/^\p{Lu}\p{Ll}/u.test(orig) && before && new RegExp(`(^|[^\\p{L}])${esc(orig)}`, 'u').test(before)) continue;
      bad.push({ token: part, why: /\d/.test(part) ? 'notation, not a plain number' : 'not an everyday word' });
    }
  }
  return bad;
}

// ---- the ledger (docs/pass-31-ledger.tsv, kept on the author's branch) -----------------------------------------
// Read by header name, never by column index: "intent" holds the takeaway the scorer grades (brief section 7),
// "content" the names and numbers for the fact checker, "job" the job the gate tests. Throws when a needed column is
// missing or an id repeats. Returns { file, sha256, header, rows: Map(id -> {column: value}) }.
export const LEDGER_DEFAULT = path.join(REPO, 'docs/pass-31-ledger.tsv');
export function readLedger(file = LEDGER_DEFAULT, need = ['id', 'job', 'intent']) {
  const buf = fs.readFileSync(file), lines = buf.toString('utf8').split('\n').filter(l => l.trim());
  const header = lines[0].replace(/\r$/, '').split('\t').map(h => h.trim());
  const miss = need.filter(h => !header.includes(h));
  if (miss.length) throw new Error(`${file}: no column ${miss.join(', ')} in the header (${header.join(', ')})`);
  const rows = new Map();
  for (const l of lines.slice(1)) {
    const cells = l.replace(/\r$/, '').split('\t'), row = Object.fromEntries(header.map((h, i) => [h, (cells[i] ?? '').trim()]));
    if (!row.id) continue;
    if (rows.has(row.id)) throw new Error(`${file}: id ${row.id} appears twice`);
    rows.set(row.id, row);
  }
  return { file, sha256: crypto.createHash('sha256').update(buf).digest('hex'), header, rows };
}
// the takeaway and job of one figure; throws when the row is missing, held (no job or takeaway) or the job unknown
export function ledgerTakeaway(L, id) {
  const r = L.rows.get(id);
  if (!r) throw new Error(`${L.file}: no row for ${id}`);
  if (!r.intent || !r.job) throw new Error(`${L.file}: ${id} has no takeaway (column intent) or no job (a held figure?)`);
  if (!['function', 'real thing', 'two-part'].includes(r.job)) throw new Error(`${L.file}: ${id} has job "${r.job}" (function, real thing or two-part)`);
  return { intent: r.intent, job: r.job };
}

// ---- label cap: a tag-stack walk over the svg -----------------------------------------------------------------
// Object text is free only when: tagged data-role="object", at most 6 characters, its direct parent is a
// <g data-obj="1"> that has a shape (or a group holding a shape) as a direct child beside it, and that obj group holds
// at most OBJ_TEXTS object texts (a group with more is a text block on a background: all its texts count as labels).
// Panels are <g data-panel> groups; a figure with more than MAX_PANELS of them is counted as one panel.
// Legend entries (data-role="legend") count as labels and are capped at LEGEND per panel.
const SHAPE = /^(rect|circle|ellipse|line|polyline|polygon|path|use|image)$/;
export const OBJ_TEXTS = 2, MAX_PANELS = 2, LEGEND = 2, LABELS = 8;
export function capCount(svg) {
  const s = svg.replace(/<(title|desc)\b[\s\S]*?<\/\1>/g, '');
  const stack = [], texts = [];
  const shaped = (e) => { const p = stack[stack.length - 1]; if (p) p.direct = true; };
  for (const m of s.matchAll(/<(\/?)([a-zA-Z][\w:-]*)\b([^>]*?)(\/?)>|([^<]+)/g)) {
    if (m[5] !== undefined) { const t = stack.findLast(e => e.name === 'text'); if (t) t.s += m[5]; continue; }
    const [, close, name, attrs, self] = m;
    if (close) {
      const e = stack.pop();
      if (e && e.name === 'text') texts.push(e);
      if (e && e.name === 'g' && e.shape) shaped(e);
      continue;
    }
    const e = { name, attrs, s: '', anc: stack.slice(), shape: false, direct: false, parent: stack[stack.length - 1] || null };
    if (SHAPE.test(name)) { for (const a of stack) if (a.name === 'g') a.shape = true; shaped(e); }
    if (!self) stack.push(e);
  }
  const isObj = g => g && g.name === 'g' && /\bdata-obj="1"/.test(g.attrs);
  const objTexts = new Map();
  for (const t of texts) if (isObj(t.parent) && /\bdata-role="object"/.test(t.attrs) && plain(t.s)) objTexts.set(t.parent, (objTexts.get(t.parent) || 0) + 1);
  const panelOf = t => { const pg = t.anc.find(a => a.name === 'g' && /\bdata-panel\b/.test(a.attrs)); return pg ? (pg.attrs.match(/data-panel="([^"]*)"/) || [, 'panel'])[1] || 'panel' : 'figure'; };
  const names = new Set(texts.filter(t => plain(t.s)).map(panelOf));
  const merged = [...names].filter(n => n !== 'figure').length > MAX_PANELS;
  const rows = texts.map(t => {
    const str = plain(t.s), role = (t.attrs.match(/\bdata-role="([^"]+)"/) || [])[1] || null;
    const og = t.anc.findLast(a => isObj(a));
    const direct = isObj(t.parent), n = direct ? objTexts.get(t.parent) || 0 : 0;
    const free = role === 'object' && direct && t.parent.direct && n <= OBJ_TEXTS && [...str].length <= 6;
    const panel = merged ? 'figure' : panelOf(t);
    const why = free ? 'object' : role === 'object'
      ? (!og ? 'object outside obj(): counted as label'
        : !direct ? 'object not a direct child of its obj group: counted as label'
        : !t.parent.direct ? 'obj group without a shape beside the text: counted as label'
        : n > OBJ_TEXTS ? `obj group with ${n} texts (more than ${OBJ_TEXTS}): counted as label`
        : 'object over 6 characters: counted as label')
      : role === 'legend' ? 'legend entry (counted as label)' : role ? 'label' : 'untagged: counted as label';
    return { str, role, free, panel, why };
  }).filter(r => r.str);
  const panels = new Map(), legends = new Map();
  for (const r of rows) if (!r.free) panels.set(r.panel, (panels.get(r.panel) || 0) + 1);
  for (const r of rows) if (r.role === 'legend') legends.set(r.panel, (legends.get(r.panel) || 0) + 1);
  return { rows, panels: Object.fromEntries(panels), max: Math.max(0, ...panels.values()),
    legends: Object.fromEntries(legends), maxLegend: Math.max(0, ...legends.values()),
    panelCount: [...names].filter(n => n !== 'figure').length, merged };
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
    let done = false;
    p.on('error', e => { if (done) return; done = true; if (timer) clearTimeout(timer); res({ code: -1, out, err: err + `\n[spawn error: ${e.message}]` }); });   // e.g. the CLI mid-update
    p.on('close', code => { if (done) return; done = true; if (timer) clearTimeout(timer); res({ code, out, err }); });
    p.stdin.on('error', () => {});
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
