// Pass 31 shared helpers (docs/pass-31-brief.md; docs/pass-31-calibration.md): the figure cards of a part, the
// judge's prose packet, the taught-yet token check, and small process helpers. Used by sheet.mjs, check.mjs and gate.mjs.
// Held material (tests/pass31/held-strip.json, applied by held.mjs) is blanked out of every part before it is read as
// prose: it never reaches a judge packet, and nothing taught-yet credits comes from it (calibration section 16).
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import { spawn } from 'node:child_process';
import { CARD, HELD_FILE, loadHeld, stripHeld } from './held.mjs';
import { teachingPieces } from './places.mjs';
export { CARD, HELD_FILE, loadHeld, stripHeld, teachingPieces };

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

// a card (held.mjs CARD): <div class="diagram-card|light-diagram ..." id="fig-..."> label, svg, caption, optional strip </div>
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
// Every earlier part whole, then this part up to the card. Taken out: the held material (held.mjs), every figure card
// (label, picture, caption, strip), every other <svg>, scripts, styles, navigation, comments. Never the figure's caption
// or strip.
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
// a part's HTML with the held material blanked (offsets kept), cached per file
// (H: the strip list; tests pass another only to show what the strip removes)
const HELD_CACHE = new Map();
export function heldStripped(root, part, H = loadHeld()) {
  const f = path.join(root, part + '.html'), st = fs.statSync(f), k = `${f}|${st.size}|${st.mtimeMs}|${H.sha256}`;
  if (!HELD_CACHE.has(k)) HELD_CACHE.set(k, { ...stripHeld(fs.readFileSync(f, 'utf8'), H), prose: null });
  return HELD_CACHE.get(k);
}
export function packet(root, fig, H = loadHeld()) {
  const parts = PARTS.slice(0, PARTS.indexOf(fig.part));
  const chunks = parts.map(p => { const c = heldStripped(root, p, H); return c.prose ?? (c.prose = prose(c.html)); });
  chunks.push(prose(heldStripped(root, fig.part, H).html.slice(0, fig.at)));
  return chunks.join('\n\n').trim();
}
// the prose before the card (taught-yet, calibration sections 16 to 18): the text of every teaching place
// (tests/pass31/places.mjs: a paragraph or list item outside the figure cards and the held material, never a caption
// or a part tagline, and the first cell of a defining table row), a <pre> block inside one left out, every earlier
// part whole and this part up to the card. Never a heading, section label, other table cell, chapter preview, part
// tagline or code block. Split into tokens as label text is split.
//   lower  every token, in lower case (the section 16 rule for a token that is neither a glossary term nor an
//          everyday word)
//   exact  the tokens as written, less the operands of a <code> span: inside <code> only the span's first token
//          counts (mov in "mov eax, 5", the instruction the sentence names; never eax, its operand, which the
//          sentence does not explain). Read only by the rule for a short abbreviation in lower case (section 17)
//   text   the paragraphs' plain text, one per line: where a proper name must already be written (section 17)
export const TOKEN_SPLIT = /[\s·•,;:!?"“”()[\]{}]+/u;
const trimTok = t => t.replace(/^['‘’.]+|['‘’.]+$/g, '');
const PRE = /<pre\b[\s\S]*?<\/pre>/gi;
const splitToks = h => dec(h.replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, ' ')).split(TOKEN_SPLIT).map(trimTok).filter(Boolean);
function paragraphProse(html, upto = html.length) {
  const cards = [...html.matchAll(CARD)].map(m => [m.index, m.index + m[0].length]);
  const all = [], exact = [], text = [];
  for (const pc of teachingPieces(html, cards)) {
    if (pc.start >= upto) break;
    const inner = pc.inner.replace(PRE, ' ');
    all.push(...splitToks(inner));
    // outside <code>: every token; inside: the first token of each span
    for (const sg of inner.split(/(<code\b[^>]*>[\s\S]*?<\/code>)/)) { if (/^<code\b/.test(sg)) exact.push(...splitToks(sg).slice(0, 1)); else exact.push(...splitToks(sg)); }
    text.push(plain(inner));
  }
  return { all, exact, text: text.join('\n') };
}
export function priorTokens(root, fig, H = loadHeld()) {
  const ps = [];
  for (const p of PARTS.slice(0, PARTS.indexOf(fig.part))) { const c = heldStripped(root, p, H); ps.push(c.para ?? (c.para = paragraphProse(c.html))); }
  ps.push(paragraphProse(heldStripped(root, fig.part, H).html, fig.at));
  const all = ps.flatMap(x => x.all);
  return { exact: new Set(ps.flatMap(x => x.exact)), lower: new Set(all.map(t => t.toLowerCase())), text: ps.map(x => x.text).join('\n') };
}

// ---- taught-yet (brief section 15; docs/pass-31-calibration.md sections 13, 15, 16, 17, 18) --------------------
// "The prose before the card" is priorTokens() above: the teaching places only (tests/pass31/places.mjs: paragraphs
// and list items, never a caption or a part tagline, and the first cell of a defining table row), held material out.
// Section 18: a plural or possessive of an abbreviation, and each piece of a compound, is judged as the abbreviation
// (DRAMs, DRAM's, OSes, RAM's, ram's, DRAM in DRAM-only); an all-capitals piece by its letters (^ERROR as ERROR); a
// prefix comes off only when what remains is an everyday word as written, of four letters or more (stems()); and the
// prose's plural teaches a short abbreviation's singular only when that singular does not itself end in s (inPrior).
// Every label and object token is one of:
//   - a number or a sign (arithmetic signs and arrows); a single letter (a key, a lamp);
//   - a term taught before the figure: known-terms.mjs (run with --strip, held material out) lists it before the
//     figure's section, or lists it as first taught in the figure's own section at a place in its paragraphs before
//     the card (defines_at), or (an all-capitals abbreviation) the paragraph or list item that first writes it comes
//     before the card. known-terms reads paragraphs and list items only, so a term first written in the figure's own
//     caption, label or How-it-works strip, or in a heading, section label, table cell or code block, is not taught
//     for that figure. An inflection of a taught term passes (pipelined, registered once pipelining, register are
//     taught), but only by plain endings, never by a stripped prefix (subprocess is not an inflection of process),
//     and never when the inflected form is an abbreviation of its own, one the book writes in capitals or a glossary
//     entry written in capitals (HTTPS is not a plural of HTTP: section 17);
//   - an everyday word: in /usr/share/dict/words or on the COMMON-word list (tests/pass31/common-words.txt), after
//     plain inflections are stripped (lowest, became, rewritten, databases), and not a glossary term (single or
//     multi-word, in any inflection) the figure has not yet taught. A glossary term not yet taught fails whatever
//     else is true of it: no rule passes it for being an everyday word or for appearing in the prose (key, safety,
//     release, group fail until known-terms places their teaching before the figure);
//   - an all-capitals token only when the prose before the figure teaches it (above), when its lowercase form is on
//     the COMMON-word list (THE, KEY, PRESS), or when it is an everyday word set in capitals: four letters or more,
//     a lowercase dictionary entry, not a glossary term, and never written in capitals anywhere in the book's text
//     (so it is not an abbreviation the book uses: LAMP, ROTORS pass; ARM, RAM, OS, MAC, LAN, NAT, CPU do not until
//     taught). Three letters or fewer pass only through the COMMON-word list or teaching (AX, AL, DOS fail);
//   - a proper name the prose before the card already writes (Shannon; LINUX for a name the prose spells Linux). For
//     a glossary entry, only one known-terms lists as a name (section 17; the rule is in that script: no digit, no
//     word in capitals, no en dash, no possessive law, a capital on every word, the initials not an abbreviation the
//     book writes, a one-word name never written in lower case: "Bell Labs", "von Neumann", "Shannon"; never "TLS
//     handshake", "IEEE 754", "SHA-256", "Diffie–Hellman", "Amdahl's law", "Turing machine", "Promises"), and never
//     one taught nowhere or written in its section only inside held material (Reno, SQL injection): such a term is
//     never credited by being mentioned;
//   - (section 16) a token that is not a glossary term and not an everyday word (bandwidth, applet, microtasks,
//     speedup, int, mov, 0x05): taught when the same token, as written or in an inflection, stands in the prose before
//     the card. Tokens are cut as label text is cut, so "css" is not in "/style.css" and "js" not in "Node.js". A
//     short abbreviation in lower case (below) needs the token in exactly that case and never as the operand of a
//     <code> span (mov after "mov eax, 5" passes; eax there does not), never the capitals of a different word.
// Short abbreviations in lower or mixed case (docs/pass-31-calibration.md section 15, review fix 2): a token of three
// letters or fewer that is not all capitals (ram, Mac, os, rax, lo, js) needs teaching like the abbreviation when its
// capitalised form is one the book writes in capitals (known-terms "capitals") or it is one of brief section 15's
// dictionary abbreviations (SHORT_ABBR), unless the token itself is on the COMMON list (add, get, not); a plain s
// plural of a word the book writes in capitals (rams, macs, arms) needs teaching too, unless that word is on the
// COMMON list (adds, puts pass). The dictionary never makes these everyday words. A taught term of two letters or
// fewer takes an s or es ending only written as the abbreviation (IPs, PCs, OSes), never in lower case (css is not
// "CS" plus s).
let DICT = null, LOWER = null, COMMON = null;
const dict = () => DICT || (DICT = new Set(fs.readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim().toLowerCase()).filter(Boolean)));
const lowerDict = () => LOWER || (LOWER = new Set(fs.readFileSync('/usr/share/dict/words', 'utf8').split('\n').map(w => w.trim()).filter(w => w && w === w.toLowerCase())));
export const COMMON_FILE = new URL('./common-words.txt', import.meta.url).pathname;
export const common = () => COMMON || (COMMON = new Set(fs.readFileSync(COMMON_FILE, 'utf8').split('\n').map(w => w.trim()).filter(w => w && !w.startsWith('#'))));
// dictionary words that are abbreviations (brief section 15: ax, al, arm, ram, nat, lan, dos; the review: mac, os),
// flagged in lower and mixed case even where the book's prose never writes them in capitals
export const SHORT_ABBR = new Set(['ax', 'al', 'arm', 'ram', 'nat', 'lan', 'dos', 'mac', 'os']);
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
// a plain prefix (section 18, brief section 15): it comes off only when what remains, as written, is an everyday word of
// four letters or more (a lower-case dictionary entry or on the COMMON list): upload (load), rewrote (wrote),
// subsystem; never through the remainder's own stems, and never to make a name or an abbreviation everyday words
// (redis is not re plus dis; subnet, unmap)
const PREFIX = /^(re|un|over|under|pre|mis|out|up|sub|non)(?=[a-z]{4,}$)/;
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
  // a plain prefix on an everyday word, after plain endings: uploads (load), rewrote (wrote), overwritten (written)
  if (deep) for (const x of [...s]) { const m = x.match(PREFIX); if (!m) continue; const r = x.slice(m[1].length); if (lowerDict().has(r) || common().has(r)) s.push(r); }
  return s;
};
const normT = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();
const esc = t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export const SIGN = /^[+\-−×÷=<>≤≥≠≈*/%^()[\]{}|~→←↑↓↔⇒⇐·•…,.:;!?'"“”‘’&#@$€£¥°±√∑∞]+$/u;
const NUMBER = /^[€£$]?[+\-−]?\d[\d.,:]*(?:st|nd|rd|th)?(?:[%°]|[kKMGT]?B|[kmµn]?s|×)?$/u;

let KT = null;
export function knownTerms(file) {
  const mt = fs.statSync(file).mtimeMs;
  if (KT && KT.file === file && KT.mtime === mt) return KT;
  const j = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!j.abbreviations || !j.capitals) throw new Error(`${file}: no abbreviations or capitals (scripts/known-terms.mjs is older than the Pass 31 follow-up)`);
  if (!j.by_section.every(s => s.defines_at)) throw new Error(`${file}: no defines_at (scripts/known-terms.mjs is older than calibration section 16)`);
  if (!Array.isArray(j.names)) throw new Error(`${file}: no names (scripts/known-terms.mjs is older than calibration section 17)`);
  const H = loadHeld();
  if (!j.strip || j.strip.sha256 !== H.sha256) throw new Error(`${file}: not made with --strip=${path.relative(REPO, H.file)} (held material would be credited)`);
  const glossary = new Set(Object.keys(j.taught).map(normT));
  // each entry's written form (normalised -> as written)
  glossary.forms = new Map(Object.keys(j.taught).map(k => [normT(k), k]));
  // entries never credited by being mentioned (section 17): taught nowhere, or written in their section only inside
  // held material (known-terms taught_nowhere and strip.glossary_terms_only_in_held)
  glossary.noMention = new Set([...(j.taught_nowhere || []), ...((j.strip && j.strip.glossary_terms_only_in_held) || [])].map(normT));
  // entries that are proper names (known-terms "names", its rule in the script: "Shannon", "Bell Labs", "von Neumann";
  // never "TLS handshake", "IEEE 754", "Diffie–Hellman", "Amdahl's law", "Turing machine", "Translation Lookaside
  // Buffer", "Promises") and not in noMention. A figure may use such a name once the prose before the card writes it as
  // the entry writes it (the reader has met the person, place or product; the entry teaches more about them later)
  glossary.names = new Set(j.names.map(normT).filter(k => !glossary.noMention.has(k)));
  // multi-word entries (normalised, longest first), each with its written form: "system call", "Ring 0", "log scale"
  glossary.multi = Object.keys(j.taught).filter(k => normT(k).includes(' ')).map(k => ({ t: normT(k), form: k })).sort((a, b) => b.t.length - a.t.length);
  // every all-capitals token the book's text writes outside the figure cards (known-terms.mjs "capitals")
  glossary.capitals = new Set(j.capitals || []);
  return (KT = { file, mtime: mt, j, glossary, abbrev: j.abbreviations, by: new Map(j.by_section.map(s => [s.section, s])) });
}
// known-terms.mjs on a tree, held material stripped (the only way the gate's tools run it)
export async function runKnownTerms(root, outFile) {
  const r = await run('node', [path.join(REPO, 'scripts/known-terms.mjs'), `--out=${outFile}`, `--public=${root}`, `--strip=${HELD_FILE}`]);
  if (r.code) throw new Error(`known-terms failed: ${(r.err || r.out).slice(-600)}`);
  return knownTerms(outFile);
}
// the terms taught before the figure: known before its section, those its section first teaches at a place in its
// prose before the card (known-terms defines_at), and every all-capitals abbreviation whose first prose paragraph
// comes before the card (known-terms.mjs must have read the same tree: run it with --public=<tree> --strip)
export function taughtBefore(kt, fig) {
  const s = kt.by.get(fig.section); if (!s) return null;
  const inSec = s.defines.filter(t => s.defines_at[t] !== null && s.defines_at[t] !== undefined && s.defines_at[t] < fig.at);
  const pi = PARTS.indexOf(fig.part);
  const ab = Object.entries(kt.abbrev).filter(([, a]) => PARTS.indexOf(a.part) < pi || (a.part === fig.part && a.at < fig.at)).map(([t]) => t);
  return [...s.known, ...inSec, ...ab].map(normT);
}
// everything taught-yet reads for one figure: the known terms and the prose before the card (priorTokens: its tokens
// and its text). The judge packet is not read: it also holds headings, section labels, tables and chapter previews,
// none of which teaches (section 17)
export function taughtContext(kt, root, fig) {
  const known = taughtBefore(kt, fig);
  return known ? { known, prior: priorTokens(root, fig) } : null;
}
// does the prose before the card write this form (case as written, whole words)?
const writes = (prior, form) => !!(prior && prior.text && new RegExp(`(^|[^\\p{L}\\p{N}])${esc(form)}(?![\\p{L}\\p{N}])`, 'u').test(prior.text));
export function svgTexts(svg) {
  return [...svg.replace(/<(title|desc)\b[\s\S]*?<\/\1>/g, '').matchAll(/<text\b([^>]*)>([\s\S]*?)<\/text>/g)].map(m => ({ attrs: m[1], s: plain(m[2]) })).filter(t => t.s);
}
const B = '[^\\p{L}\\p{N}_]';   // a word boundary that keeps SYN_SENT and CR3 whole
// the section 16 rule: does the prose before the card hold this token (as written, or a plain inflection of it; never
// a stripped prefix: "process" in the prose does not teach subprocess, section 17)?
const inPrior = (prior, part, orig, exact) => {
  if (!prior) return false;
  // (section 18) the prose's plural teaches the singular (movs: mov), never a word that already ends in s (loss is
  // not "los" plus s)
  if (exact) return prior.exact.has(orig) || (!/s$/u.test(orig) && prior.exact.has(orig + 's'));
  return stems(part, false).some(w => prior.lower.has(w)) || prior.lower.has(part + 's') || prior.lower.has(part + 'es');
};
export function taughtYet(text, known, glossary, prior = null) {
  if (typeof prior === 'string') throw new Error('taughtYet(text, known, glossary, prior): the packet is no longer an argument (calibration section 17)');
  const bad = [];
  // a taught term of two letters or fewer takes an s or es ending only written as the abbreviation: IPs, PCs, OSes
  // (the ending dropped here, before case is folded); css, js and Ips keep theirs and are checked as tokens
  const isShort = t => t.replace(/[^\p{L}\p{N}]/gu, '').length <= 2;
  let t0 = text;
  for (const t of known) if (isShort(t) && /^[\p{L}\p{N}]+$/u.test(t)) t0 = t0.replace(new RegExp(`(^|${B})(${esc(t.toUpperCase())})(s|es)(?=$|${B})`, 'gu'), '$1$2');
  let s = ' ' + normT(t0) + ' ';
  // a form that is an abbreviation of its own (section 17): the book writes it in capitals, or its glossary entry is
  // written in capitals (HTTPS). It is never a plural or other inflection of a taught term (HTTPS is not HTTP plus s)
  const ownAbbr = w => !!(glossary.capitals?.has(w.toUpperCase()) || /^[^\p{Ll}]*\p{Lu}[^\p{Ll}]*$/u.test(glossary.forms?.get(w) || ''));
  const endings = t => { if (isShort(t)) return ''; const xs = ['s', 'es'].filter(x => !ownAbbr(t + x)); return xs.length ? `(?:${xs.join('|')})?` : ''; };
  // known terms first (longest first), so "turing machine" is taken whole
  for (const t of [...known].sort((a, b) => b.length - a.length)) s = s.replace(new RegExp(`(^|${B})${esc(t)}${endings(t)}(?=$|${B})`, 'gu'), '$1 ');
  // then multi-word glossary terms not yet taught ("system call", "ring 0"): each fails whole, even when every word in
  // it is an everyday word; a name ("Bell Labs", "von Neumann": glossary.names) passes once the prose before the card
  // writes it. Matched on the text as written (a hyphen in the term needs a hyphen: "a-machine" is not "a machine").
  const knownSet = new Set(known), rawL = ' ' + text.toLowerCase().replace(/\s+/g, ' ') + ' ';
  // a taught single word of three letters or more, and its own stems of five letters or more (pipelining: pipeline),
  // so an inflection of a taught term passes (pipelined, registered); a taught term of two letters never lends its
  // stem (ips is not IP plus s)
  const knownStems = new Set();
  for (const k of known) if (!k.includes(' ') && k.replace(/[^\p{L}\p{N}]/gu, '').length > 2) for (const w of stems(k, false)) if (w === k || w.length >= 5) knownStems.add(w);
  for (const { t, form } of glossary.multi || []) {
    if (knownSet.has(t)) continue;
    const pat = form.toLowerCase().split(/(\s+|[-–])/).map(x => /^\s+$/.test(x) ? '[\\s\\-–]+' : /^[-–]$/.test(x) ? '[-–]' : esc(x)).join('');
    if (!new RegExp(`(^|${B})${pat}(s|es)?(?=$|${B})`, 'u').test(rawL)) continue;
    if (!(glossary.names?.has(t) && writes(prior, form))) bad.push({ token: t, why: 'a glossary term not yet taught' });
    s = s.replace(new RegExp(`(^|${B})${esc(t)}(s|es)?(?=$|${B})`, 'gu'), '$1 ');
  }
  // the label's tokens in their original case, cut as the folded text is cut (dashes and hyphens made spaces), so
  // each piece of a compound keeps its capitals: DRAM in DRAM-based is the abbreviation, not the everyday word dram
  // (section 18); the whole-word lookup below is the fallback
  const rawToks = (' ' + t0.replace(/[–-]/g, ' ') + ' ').split(TOKEN_SPLIT).map(trimTok).filter(Boolean);
  const raw = text.split(/\s+/);
  const bareOf = x => x.replace(/^[^\p{L}\p{N}_]+|[^\p{L}\p{N}_]+$/gu, '');   // ^ERROR: ERROR
  let rp = 0;   // tokens are matched to their original in order, so "JSON · json" keeps each one's case
  const origOf = tok => { const k = rawToks.findIndex((r, i) => i >= rp && r.toLowerCase() === tok); if (k < 0) return rawToks.find(r => r.toLowerCase() === tok); rp = k + 1; return rawToks[k]; };
  for (const tok0 of s.split(TOKEN_SPLIT)) {
    const tok = trimTok(tok0); if (!tok) continue;
    if (SIGN.test(tok) || NUMBER.test(tok)) continue;
    // arithmetic written solid: 3+1=4, 1011=11, /22
    if (/^[\d+\-−×÷=<>≤≥*/%^().]+$/u.test(tok) && /\d/.test(tok) && !/^\//.test(tok)) continue;
    if (/^\p{L}$/u.test(tok)) continue;                                      // one letter
    if (/^\/\d/.test(tok)) { if (!inPrior(prior, tok, tok, false)) bad.push({ token: tok, why: 'notation, not a plain number' }); continue; }   // /22
    const orig = (origOf(tok) || raw.find(r => r.toLowerCase().replace(/[^\p{L}\p{N}'’_-]/gu, '') === tok.replace(/[^\p{L}\p{N}'’_-]/gu, '')) || tok).replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '');
    const origParts = orig.split(/[-–/]/);
    for (const part of tok.split(/[-–/]/)) {
      if (!part) continue;
      if (NUMBER.test(part) || SIGN.test(part) || /^\p{L}$/u.test(part)) continue;
      // this piece as the label writes it
      const op = origParts.find(x => bareOf(x).toLowerCase() === bareOf(part)) || part, ob = bareOf(op);
      // a glossary term in a plain inflection (kernels, pipelined). A stripped prefix makes a different word
      // (subprocess is not process, SubBytes is not bytes): it is checked as a token of its own below, and the
      // prefix never makes it an everyday word when what remains is a glossary term (section 17)
      const guarded = w => { const a = stems(w, false), d = stems(w); return d.some(x => !a.includes(x) && glossary.has(x)) ? a : d; };
      const st0 = stems(part, false), g = st0.find(w => glossary.has(w)), st = guarded(part);
      if (g !== undefined) {
        // an inflection of a taught term, by plain endings only (pipelined, registered), and never a form that is an
        // abbreviation of its own (HTTPS)
        if (st0.some(w => knownStems.has(w) && (w === part || !ownAbbr(part)))) continue;
        // a name the prose before the card writes, as the entry writes it (Shannon)
        const form = glossary.forms?.get(g);
        if (glossary.names?.has(g) && form && writes(prior, form)) continue;
        bad.push({ token: part, why: 'a glossary term not yet taught' }); continue; }
      const everyday = st.some(w => dict().has(w) || common().has(w));
      // an all-capitals piece, or the plural or possessive of one (DRAMs, DRAM's, OSes, RAM's: section 18, brief
      // section 15), judged as the abbreviation itself, its letters only (^ERROR as ERROR)
      const abm = ob.match(/^([\p{Lu}\d_]*\p{Lu}[\p{Lu}\d_]*)(?:['’]s|es|s)$/u);
      const abStem = abm && (abm[1].match(/\p{Lu}/gu) || []).length >= 2 ? abm[1] : null;
      const lt = ob.replace(/[^\p{L}]/gu, '');
      if (abStem || (lt.length >= 2 && lt === lt.toUpperCase() && /\p{Lu}/u.test(lt))) {
        const j = (abStem || ob).toLowerCase(), sj = guarded(j);
        if ((j.length >= 4 ? sj : [j]).some(w => common().has(w))) continue;                    // THE, KEY, PRESS (inflected only from four letters: DOS is not "do")
        if (j.replace(/[^\p{L}]/gu, '').length >= 4 && !sj.some(w => glossary.capitals?.has(w.toUpperCase())) && sj.some(w => lowerDict().has(w) || common().has(w))) continue;   // LAMP, ROTORS
        if (j.length >= 4 && /^\p{L}+$/u.test(j) && writes(prior, j[0].toUpperCase() + j.slice(1))) continue;   // LINUX
        bad.push({ token: ob || op, why: 'an all-capitals abbreviation not taught before the figure' }); continue; }
      // a short abbreviation in lower or mixed case (ram, Mac, os, rax, lo), its possessive (ram's: section 18), or a
      // plain plural of one the book writes in capitals (rams, arms): taught like the abbreviation, unless the token
      // itself is on the COMMON list (add, not), or (section 16) the prose before the card writes this very token in
      // this very case (mov)
      const bp = part.replace(/['’]s$/u, ''), obp = op.replace(/['’]s$/u, '');
      if (/^\p{L}+$/u.test(bp) && !common().has(bp) && !common().has(part)) {
        const short = w => [...w].length >= 2 && [...w].length <= 3;
        const abbr = short(bp) && (glossary.capitals?.has(bp.toUpperCase()) || SHORT_ABBR.has(bp));
        const w = bp.replace(/s$/, ''), plural = w !== bp && short(w) && glossary.capitals?.has(w.toUpperCase()) && !common().has(w);   // adds, puts: add, put are COMMON
        if (abbr || plural) {
          if (inPrior(prior, bp, obp, true)) continue;
          bad.push({ token: part, why: 'an abbreviation not taught before the figure (not written in capitals)' }); continue; }
      }
      if (everyday) continue;
      // a proper name (capital first letter, not all capitals) that the prose before the card already writes
      if (/^\p{Lu}\p{Ll}/u.test(orig) && writes(prior, orig)) continue;
      // section 16: neither a glossary term nor an everyday word, and the prose before the card holds it
      if (inPrior(prior, part, part, false)) continue;
      bad.push({ token: part, why: /\d/.test(part) ? 'notation, not a plain number' : 'not an everyday word' });
    }
  }
  return bad;
}

// ---- the ledger (docs/pass-31-ledger.tsv, kept on the author's branch) -----------------------------------------
// Read by header name, never by column index: "intent" holds the takeaway the scorer grades (brief section 7),
// "content" the names and numbers for the fact checker, "job" the job the gate tests. Throws when a needed column is
// missing, a column name repeats in the header, or an id repeats. Returns { file, sha256, header, rows: Map(id -> {column: value}) }.
export const LEDGER_DEFAULT = path.join(REPO, 'docs/pass-31-ledger.tsv');
export function readLedger(file = LEDGER_DEFAULT, need = ['id', 'job', 'intent']) {
  const buf = fs.readFileSync(file), lines = buf.toString('utf8').split('\n').filter(l => l.trim());
  const header = lines[0].replace(/\r$/, '').split('\t').map(h => h.trim());
  const dup = [...new Set(header.filter((h, i) => h && header.indexOf(h) !== i))];
  if (dup.length) throw new Error(`${file}: column ${dup.join(', ')} appears more than once in the header`);
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
