#!/usr/bin/env node
// Known terms per section, in reading order (Pass 29/30, docs/pass-29-30-brief.md; Pass 31,
// docs/pass-31-calibration.md sections 13, 15, 16 and 17).
//
// For every <section class="section" id="ch…"> of parts 1 to 5, in reading order:
//   known       the terms the book has taught before the section starts
//   defines     the terms first taught inside it
//   defines_at  for each of those, the offset (in the part's HTML) of the first place in the section's paragraphs
//               that teaches it (null: no such place, which the rules below never produce): a figure in the same
//               section is credited the term only when this offset comes before its card
// Teaching happens only in the places tests/pass31/places.mjs lists (sections 17 and 18; brief section 15): the text
// of a <p> or <li> outside every figure card (chapter and section leads, chapter closings included), never a caption
// or a part tagline, with any <pre> block inside it blanked; and the first cell of a table row that expands or defines
// its term (HDD (spinning disk); RCX | Counter: ...; FCFS | First-come, first-served. ...). Not teaching: a figure card
// (label, picture, caption, How-it-works strip), which no judge sees; a heading, a section label (div.section-number),
// a math label, any other table cell (a row whose cells are values lists its term, it does not explain it), a <pre>
// code block, a part opener's chapter preview, a part tagline. A term is first taught at the earliest of these, in
// reading order:
//   - glossary: its entry in public/glossary.json (the section the extractor assigns), located at the first use in
//     that section's paragraphs and list items. An entry whose section writes the term only elsewhere teaches
//     nothing, and is listed by where it does write it: only in held material (glossary_terms_only_in_held), only in
//     a figure card (glossary_terms_only_in_cards: CGNAT, IHL), only in headings, labels, tables or code blocks
//     (glossary_terms_only_outside_paragraphs), or not at all (glossary_terms_not_located). The extractor does not
//     record the first teaching: it keeps the first *marked* use (<span class="key-term">, or <em>/<strong> before a
//     definitional cue) and, for a curated term, the best-*scored* use (a section named after the term, emphasis, a
//     definitional window), so a term the prose already glosses in place earlier (a register (a slot in the CPU
//     ...), a compiler, which turns code ...) sat in a later section. That is why the next source exists;
//   - prose gloss: the first paragraph or list item where the term, or its plural, is glossed in place: followed by
//     a parenthesis that opens with a word ("register (a slot"), by ", which" or ", who", by ", or ACRONYM", by an
//     apposition (", the|a|an …", or, section 19, ", <a possessive noun> …": "C++, C's best-known descendant."; or up
//     to four words then "that|which|who": "threads, streams of instructions that"), or preceded by "called" or
//     "known as"; a parenthesised number between the term and its cue is skipped
//     ("Diffie–Hellman (1976), which is key agreement"). Section 18 adds five cues, each a definition by its form:
//       definition   the sentence opens with the term (after "A" or "An" at most) and goes on "is|are a|an|the"
//                    ("SHA-256 is the workhorse", "A pipe is a kernel-allocated ring buffer");
//       generic      a term of two words or more opens the sentence after "A" or "An" and a verb in -s follows
//                    ("A virtual machine imitates an entire computer"); never a one-word term, whose everyday sense
//                    reads the same (a key opens a lock);
//       naming       a clause of four words or more, then ", a|an TERM" closed by ";" or "." ("a semaphore admits one
//                    process at a time, a mutex;"); a list's last item ("a lock, a counter, a mutex.") is not one;
//       reverse      a noun phrase opening its clause with an article or a possessive, then ", TERM," and a verb
//                    ("Kubernetes' "source of truth", etcd, runs"); a list ("canaries, DEP, ASLR, CFI, pointer
//                    authentication") is not one;
//       modifier     a term of two words or more, written as the modifier of one noun that a parenthesis glosses
//                    ("control-plane components (the parts that decide what should run where)");
//     A plain use is not a gloss, so an everyday word that is also a glossary term (safety, release, group, key,
//     bucket, port, node, edge) is not taught by being used;
//   - emphasis (section 18): the term written whole inside <em> or <strong> in a paragraph or list item, the book's
//     mark for a term it introduces ("the kernel keeps <em>page tables</em> that say ...", "the MMU stops it with a
//     <em>page fault</em>"), unless its sentence points elsewhere (a chapter, section, part or figure number: "the
//     stack canary, <em>ASLR</em> and DEP" in a sentence naming Chapter 3 teaches nothing);
//   - table row (section 18): a term written in the first cell of a defining table row (above);
//   - key-term: every <span class="key-term"> in a paragraph or list item (one outside a section, such as a chapter
//     lead, counts as taught before the next section).
// A marked term (glossary entry or key-term span) with none of these is listed in "taught" as taught nowhere: it
// stays a term, so a label that uses it fails.
// Terms merge case-insensitively.
//
// With --strip=<tests/pass31/held-strip.json> (Pass 31, always given by the gate's tools) the held material is
// blanked first (tests/pass31/held.mjs): held figure cards, the listed chapter, sections and paragraphs. Nothing
// inside it teaches: no key-term, no prose gloss, no abbreviation; a glossary entry whose section is stripped, or
// whose term the section uses outside its paragraphs only inside held material, gives no teaching point. Such a term
// is taught only where the rest of the book teaches it, or not at all.
//
// Also (Pass 31, brief section 15), two lists the figure checks read:
//   abbreviations  every all-capitals token (two or more capital letters, digits
//                  and underscores allowed: CPU, CR3, SYN_SENT), its plural
//                  (VMs, OSes) recorded as the singular (section 18), at the
//                  first teaching place that writes it (as above: a paragraph,
//                  list item or defining row's first cell; never a caption,
//                  heading, label, other table cell, part tagline or <pre>
//                  block; <code> inside a paragraph counts, it is part of the
//                  sentence), a chapter lead or closing outside the sections
//                  included (JSON in Chapter 12's lead: section 18): part,
//                  section (the one holding it, else the next in the part),
//                  the nearest id before it, and its offset in the part's
//                  HTML. So a token first written in a figure's own caption,
//                  label or strip, or in a code comment, is not taught for
//                  that figure (EAX: section 17). Section 19: a writing
//                  places it only when it glosses it (a prose-gloss cue on
//                  it, or its expansion before it: "main memory (RAM)"), or
//                  when it is a plain writing in a sentence that does not
//                  point elsewhere (a chapter, section, part or another
//                  chapter's figure, outside the parentheses that do not hold
//                  it: "Part III opens up ...: ... DNS") of an abbreviation that
//                  a mention may credit (never a glossary term taught nowhere
//                  or only in held material, ASLR, CFI, HTTPS, nor one the book
//                  first writes inside held material, CVE, CA, SBOM); a part's
//                  roman number (Part II) is placed where it is written. Each
//                  record says by which (by: writing, gloss (cue), part number).
//   capitals       every all-capitals token the book's text writes anywhere
//                  outside the figure cards (sections, heroes, leads, tables,
//                  code), held material included (the list only ever makes a
//                  check stricter).
//
//   node scripts/known-terms.mjs [--out=docs/pass-29-known-terms.json] [--public=<public dir>] [--strip=<held-strip.json>]
import fs from 'node:fs'; import path from 'node:path';
import { teachingPieces } from '../tests/pass31/places.mjs';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, ...v] = a.replace(/^--/, '').split('='); return [k, v.length ? v.join('=') : true]; }));
const ROOT = new URL('../', import.meta.url).pathname;
const OUT = ARGS.out || 'docs/pass-29-known-terms.json';
const PUB = ARGS.public && ARGS.public !== true ? path.resolve(ARGS.public) + '/' : `${ROOT}public/`;   // the tree to read
const PARTS = ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];
const STRIP = ARGS.strip && ARGS.strip !== true ? path.resolve(ARGS.strip) : null;
const HM = STRIP ? await import(new URL('../tests/pass31/held.mjs', import.meta.url).href) : null;
const H = HM ? HM.loadHeld(STRIP) : null;

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“', hellip: '…', times: '×', minus: '−', middot: '·', rarr: '→', larr: '←', euro: '€', pound: '£' };
const decode = e => e[0] === '#' ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1)) : (ENT[e] ?? `&${e};`);
const plain = s => s.replace(/<[^>]+>/g, '').replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e) => decode(e)).replace(/\s+/g, ' ').trim();
const norm = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();
const blank = m => m.replace(/[^\n]/g, ' ');
const CARD = /<div class="(?:diagram-card|light-diagram)[^"]*" id="([^"]+)">[\s\S]*?<\/svg>\s*<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>\s*(?:<details class="fig-how">[\s\S]*?<\/details>\s*)?<\/div>/g;
const esc = t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const PRE = /<pre\b[\s\S]*?<\/pre>/gi;
// the text of an HTML string with the offset of each character: a tag is one space, entities decoded
function textMap(html, base = 0) {
  const chars = [], map = [];
  for (const m of html.matchAll(/<[^>]*>|&(#x?[0-9a-f]+|\w+);|[^<&]+|[<&]/gi)) {
    const s = m[0];
    if (s[0] === '<' && s.length > 1) { chars.push(' '); map.push(base + m.index); continue; }
    if (m[1] !== undefined) { for (const ch of decode(m[1]).split('')) { chars.push(ch); map.push(base + m.index); } continue; }
    for (let k = 0; k < s.length; k++) { chars.push(s[k]); map.push(base + m.index + k); }
  }
  return { text: chars.join(''), map };
}
// section 19 (the review of the section 18 freeze, B): a piece's text with every run of whitespace made one space (the
// run keeps its first character's offset) and trimmed, so a line break in the HTML source is a space like any other;
// pieces are joined with SEP, a character that is not whitespace, so no cue, term or sentence start reads across two
// pieces, and a piece's start (and only that, or a sentence end) is a sentence's start
const SEP = '\u001E';
function collapse({ text, map }) {
  const t = [], m = [];
  for (let i = 0; i < text.length; i++) {
    if (/\s/u.test(text[i])) { if (t.length && t[t.length - 1] !== ' ') { t.push(' '); m.push(map[i]); } continue; }
    t.push(text[i]); m.push(map[i]);
  }
  if (t[t.length - 1] === ' ') { t.pop(); m.pop(); }
  return { text: t.join(''), map: m };
}
// a term as a pattern: words joined by any run of spaces or hyphens, either apostrophe, an optional plural ending.
// Case: exact for an abbreviation (no lower-case letter) and for a one-word name (Scheme is not the everyday word
// scheme); a lower-case term may open with a capital (a sentence start); any other term (Translation Lookaside
// Buffer, Ring 0) in any case
function termRe(term) {
  const t = term.trim(), words = t.split(/[\s\-–]+/).map(w => esc(w).replace(/['’]/g, "['’]"));
  let flags = 'gu';
  if (!/\p{Lu}/u.test(t)) { if (/^\p{Ll}/u.test(words[0])) words[0] = `[${words[0][0].toUpperCase()}${words[0][0]}]${words[0].slice(1)}`; }
  else if (/\p{Ll}/u.test(t) && !(words.length === 1 && /^\p{Lu}/u.test(t))) flags = 'giu';
  return new RegExp(`(?<![\\p{L}\\p{N}_])(${words.join('[\\s\\-–]+')})(?:s|es)?(?![\\p{L}\\p{N}_])`, flags);
}
// a prose gloss right after (or before) a use of the term. Not a gloss: a parenthesis that opens with a pointer, an
// aside word or a lone abbreviation ("(Fig 1.2)", "(over TCP, ...)", "(ECDSA)"); an apposition that is one item of a
// list ("a privilege bit, a trap, a memory-management unit, a timer"; "the page tables, the trap table, the timer"), or
// a pointer elsewhere ("a trap, the subject of the next section")
const ASIDE = 'Figs?|see|See|Chapter|chapter|Part|part|Section|section|§|e\\.g|i\\.e|in|on|at|for|from|with|by|over|under|into|as|and|or|but|so|which|who|that|also|usually|typically|often|now|then|still|even|only|just|not|below|above|here|there|this|these|those|its|their|his|her|our|your|my|when|where|while|if|because|since|after|before|unlike|like|about|around|via|per|plus|minus|versus|vs';
const STOP = 'and|or|but|so|then|thus|while|because|since|if|when|where|as|yet|not|nor|which|who|whose|that|the|a|an|it|its|they|their|we|our|you|your|he|his|she|her|this|these|those|there|here|each|every|all|some|in|on|at|of|for|to|from|with|by|into|onto|over|under|after|before|until|unless|though|although|also|still|even|only|just|both|either|neither';
// an apposition's determiner: an article, or (section 19, the review of the section 18 freeze, E) a possessive noun, as
// the reverse cue's OPENS_NP accepts ("in C++, C's best-known descendant."; "at GCHQ, Britain's signals-intelligence
// agency:"); the list and pointer guards apply to both
const DET = `(?:the|a|an|[\\p{L}\\p{N}.+#-]*\\p{L}(?:['’]s|s['’]|['’]))`;
const LIST = new RegExp(`^,\\s+${DET}\\s+[^,.;:()]*,\\s+(?:${DET}|and|or)\\s`, 'u');
const POINTER = new RegExp(`^,\\s+${DET}\\s+[^,.;:()]*\\b(?:[Ss]ections?|[Cc]hapters?|[Pp]arts?|[Ff]igs?|[Ff]igures?|§)\\b`, 'u');   // "a trap, the subject of the next section
const APPOS = new RegExp(`^,\\s+${DET}\\s+\\p{Ll}`, 'u');
const GLOSS_AFTER = [
  ['parenthesis', new RegExp(`^\\s*\\(\\s*(?!(?:${ASIDE})\\b)(?![\\p{Lu}\\d][\\p{Lu}\\d_\\-./]*\\s*[),;])\\p{L}`, 'u')],
  ['which', /^,\s+(?:which|who)\b/u],
  ['or-acronym', /^,\s+or\s+\p{Lu}[\p{L}\p{N}-]+/u],
  ['apposition', { test: a => APPOS.test(a) && !LIST.test(a) && !POINTER.test(a) }],
  ['apposition', new RegExp(`^,\\s+(?!(?:${STOP})\\b)(?:[\\p{L}'’-]+\\s+){1,4}(?:that|which|who)\\b`, 'u')],
  // section 20 (the review of the section 19 freeze, D1): a quoted definition right after the term, three words or more
  // closed by a colon, semicolon or full stop ('Take XOR, "exactly one of A and B is 1": it gives 1 when ...'); with D1
  // an entry's plain writing places nothing, so this form, which glosses it, is read as the gloss it is
  ['quoted', /^,\s+["“](?:[^"”,.;:()]+\s+){2,}[^"”,.;:()]*["”]\s*[:;.]/u],
];
const GLOSS_BEFORE = /(?:^|[^\p{L}])(?:called|known as)\s+(?:an?\s+|the\s+)?$/iu;
// section 18: a parenthesised number between the term and its cue is skipped ("Diffie–Hellman (1976), which")
const NUMBER_PAREN = /^\s*\(\s*(?:c\.\s*)?\d[\d\s,.–-]*\)/u;
// section 18: the definitional forms (header). Pieces are joined with SEP (section 19: never a newline, which the HTML
// source puts mid-sentence), so a piece's start is a sentence's start
const SENT = `(?:^\\s*|${SEP}\\s*|[.!?:]["”’)\\]]*\\s+)`;
const DEF_BEFORE = new RegExp(`${SENT}(?:(?:A|An)\\s+)?$`, 'u'), GEN_BEFORE = new RegExp(`${SENT}(?:A|An)\\s+$`, 'u');
const DEF_AFTER = /^\s+(?:is|are)\s+(?:a|an|the)\b/u;
const AUX = 'is|are|was|were|has|have|had|can|could|will|would|may|might|must|should|shall|does|did|do';
const VERB_S = `(?!\\p{Ll}*ss\\b)\\p{Ll}{2,}s\\b`;
const GEN_AFTER = new RegExp(`^\\s+(?!(?:${AUX})\\b)${VERB_S}`, 'u');
const REV_AFTER = new RegExp(`^,\\s+(?:is|are|was|were|${VERB_S})`, 'u');
const OPENS_NP = /^(?:(?:the|a|an|The|A|An)\s|[\p{L}\p{N}.-]+(?:['’]s|s['’]|['’])(?=\s))/u;
const MOD_AFTER = new RegExp(`^\\s+\\p{Ll}[\\p{L}-]*\\s*\\(\\s*(?!(?:${ASIDE})\\b)(?![\\p{Lu}\\d][\\p{Lu}\\d_\\-./]*\\s*[),;])\\p{L}`, 'u');
// the clause before a comma that ends `before` (back to the last , ; : . ! ? ( ) or piece start; quotes kept), and the
// character that opens it ('' at a piece or text start)
const clauseBefore = b => { const t = b.replace(/,\s*$/u, ''); const i = Math.max(...[',', ';', ':', '.', '!', '?', '(', ')', SEP].map(c => t.lastIndexOf(c))); return { seg: t.slice(i + 1).trim(), opener: i >= 0 ? t[i] : '', rest: i >= 0 ? t.slice(0, i) : '' }; };
const words = x => x.split(/\s+/).filter(w => /[\p{L}\p{N}]/u.test(w)).length;
// section 20 (the review of the section 19 freeze, D4): the naming cue's list guard. ", a TERM" closing a list of items
// that each open with an article ("a hosting company, a corporate IT department, a CDN.") is the list's last item, not
// a naming, however long the items: the clause before opens after ", a|an|the", and the clause before that one opens
// with an article too (two items before the term), as LIST reads a list forward. "Initialised to 1, a semaphore admits one process
// at a time, a mutex;" stays a naming: the clause before its clause does not open with an article
const ART = /^(?:a|an|the)\s/iu;
const listTail = before => {
  const c1 = clauseBefore(before); if (c1.opener !== ',' || !ART.test(c1.seg)) return false;
  return ART.test(clauseBefore(c1.rest).seg);
};
// the section 18 cues on one use of a term: rawBefore holds up to 200 characters before it (newlines kept), after the
// text after it (number parenthesis removed)
function formCue(term, rawBefore, after) {
  const multi = /[\s\-–]/u.test(term.trim());
  if (DEF_BEFORE.test(rawBefore) && DEF_AFTER.test(after)) return 'definition';
  if (multi && GEN_BEFORE.test(rawBefore) && GEN_AFTER.test(after)) return 'generic';
  if (/,\s+(?:a|an)\s+$/u.test(rawBefore) && /^\s*[;.]/u.test(after)) { const pre = rawBefore.replace(/\s+(?:a|an)\s+$/u, ''), { seg } = clauseBefore(pre); if (words(seg) >= 4 && !listTail(pre)) return 'naming'; }
  if (/,\s+$/u.test(rawBefore) && REV_AFTER.test(after)) { const { seg, opener } = clauseBefore(rawBefore); if (opener !== ',' && OPENS_NP.test(seg) && words(seg) >= 2 && words(seg) <= 8) return 'reverse'; }
  if (multi && MOD_AFTER.test(after)) return 'modifier';
  return null;
}

// reading order
const sections = [];
const P = {};          // per part: raw HTML, the text read (held material blanked), cards, zones
const keyTerms = [];   // { term, at: index of the section it is taught in (or before), off, prose }
const posAt = (part, off) => {   // the section index of an offset: i inside section i, i - 0.5 before it
  const secs = sections.map((s, i) => ({ ...s, i })).filter(s => s.part === part);
  for (const s of secs) { if (off >= s.start && off < s.end) return s.i; if (off < s.start) return s.i - 0.5; }
  return secs.length ? secs[secs.length - 1].i + 0.5 : -1;
};
for (const part of PARTS) {
  const raw = fs.readFileSync(`${PUB}${part}.html`, 'utf8');
  const S = H ? HM.stripHeld(raw, H) : { html: raw, zones: [] };
  const src = S.html;
  const starts = [...raw.matchAll(/<section class="section" id="(ch[^"]+)"/g)].map(m => ({ id: m[1], start: m.index }));
  starts.forEach(s => {
    const close = raw.indexOf('</section>', s.start);
    const body = raw.slice(s.start, close);
    const title = (body.match(/<h2[^>]*>([\s\S]*?)<\/h2>/) || [])[1];
    const label = (body.match(/<div class="section-number">([^<]+)<\/div>/) || [])[1];
    const stripped = S.zones.some(([a, b]) => s.start >= a && s.start < b);
    sections.push({ part, section: s.id, label: label ? plain(label) : '', title: title ? plain(title) : '', start: s.start, end: close, stripped });
  });
  const cards = [...src.matchAll(CARD)].map(m => [m.index, m.index + m[0].length]);
  const inCard = off => cards.some(([a, b]) => off >= a && off < b);
  // the teaching places (tests/pass31/places.mjs; sections 17 and 18): every <p> and <li> outside the figure cards,
  // never a caption or a part tagline, and the first cell of a defining table row; a <pre> block inside one blanked;
  // joined in reading order with each character's offset in the part (-1 between pieces)
  const pres = [...src.matchAll(PRE)].map(m => [m.index, m.index + m[0].length]);
  const pieces = teachingPieces(src, cards).map(x => ({ ...collapse(textMap(x.inner.replace(PRE, blank), x.a)), start: x.start, end: x.end, kind: x.kind, inner: x.inner, a: x.a }));
  const joined = { text: pieces.map(p => p.text).join(SEP), map: pieces.flatMap(p => [...p.map, -1]) };
  const inPiece = off => pieces.some(p => off >= p.start && off < p.end) && !pres.some(([a, b]) => off >= a && off < b);
  // the whole book's paragraph and list-item text, held material included, code and <pre> left out: where a word is
  // written in lower case (the names rule below; it only ever makes the check stricter)
  const rawCards = [...raw.matchAll(CARD)].map(m => [m.index, m.index + m[0].length]);
  const plainText = [...raw.matchAll(/<(p|li)\b([^>]*)>([\s\S]*?)<\/\1>/g)].filter(m => !/class="[^"]*diagram-caption/.test(m[2]) && !rawCards.some(([a, b]) => m.index >= a && m.index < b))
    .map(m => plain(m[3].replace(PRE, ' ').replace(/<code\b[^>]*>[\s\S]*?<\/code>/g, ' '))).join('\n');
  // the same teaching places read with held material in (section 19: only to tell which abbreviations the book first
  // writes inside held material; nothing here teaches)
  const rawPieces = teachingPieces(raw, rawCards).map(x => collapse(textMap(x.inner.replace(PRE, blank), x.a)));
  const rawJoined = { text: rawPieces.map(p => p.text).join(SEP), map: rawPieces.flatMap(p => [...p.map, -1]) };
  P[part] = { raw, src, cards, zones: S.zones, inCard, pieces, joined, inPiece, plainText, rawJoined };
}
const idx = new Map(sections.map((s, i) => [s.part + '|' + s.section, i]));
for (const part of PARTS) {
  for (const m of P[part].src.matchAll(/<span class="key-term">([\s\S]*?)<\/span>/g)) {
    const term = plain(m[1]); if (!term) continue;
    keyTerms.push({ term, at: posAt(part, m.index), part, off: m.index, prose: P[part].inPiece(m.index) });   // in a paragraph or list item only
  }
}

// every teaching point of every term: { term, at (section index, or i - 0.5), off (offset in the part, or null), prose, source }
const cand = new Map();
const add = (term, c) => { const k = norm(term); if (!cand.has(k)) cand.set(k, { term, list: [] }); cand.get(k).list.push(c); };
const g = JSON.parse(fs.readFileSync(`${PUB}glossary.json`, 'utf8'));
const unplaced = [], strippedOnly = [], cardOnly = [], outsideParagraphs = [], notLocated = [];
const secText = new Map();
const sectionText = (i, which) => {   // the section's text (held material blanked, or raw) with offsets
  const k = i + '|' + which; if (secText.has(k)) return secText.get(k);
  const s = sections[i], h = P[s.part][which];
  const t = textMap(h.slice(s.start, s.end), s.start); secText.set(k, t); return t;
};
const sectionPieces = i => {   // the section's paragraph and list-item text with offsets
  const k = i + '|pieces'; if (secText.has(k)) return secText.get(k);
  const s = sections[i], ps = P[s.part].pieces.filter(p => p.start >= s.start && p.start < s.end);
  const t = { text: ps.map(p => p.text).join(SEP), map: ps.flatMap(p => [...p.map, -1]) }; secText.set(k, t); return t;
};
for (const e of Object.values(g.entries)) {
  const i = idx.get(e.part + '|' + e.section);
  if (i === undefined) { unplaced.push(e.term); continue; }
  const s = sections[i];
  if (s.stripped) { strippedOnly.push(e.term); continue; }
  const pt = sectionPieces(i), first = pt.text.matchAll(termRe(e.term)).next().value;
  if (first) { add(e.term, { at: i, off: pt.map[first.index], prose: true, source: 'glossary' }); continue; }
  // not in the section's paragraphs: say where the section does write it (held material first, then a card, then a
  // heading, label, table cell or code block), for the record; none of these teaches
  let card = false, other = false, held = false;
  for (const m of sectionText(i, 'src').text.matchAll(termRe(e.term))) { const off = sectionText(i, 'src').map[m.index]; if (P[s.part].inCard(off)) card = true; else other = true; }
  if (H) for (const m of sectionText(i, 'raw').text.matchAll(termRe(e.term))) if (HM.inZone(P[s.part].zones, sectionText(i, 'raw').map[m.index])) { held = true; break; }
  if (held) strippedOnly.push(e.term);            // used there (outside its paragraphs) only inside held material
  else if (card) cardOnly.push(e.term);           // the section writes it only in a figure card
  else if (other) outsideParagraphs.push(e.term); // only in a heading, section label, table cell or code block
  else notLocated.push(e.term);
}
for (const k of keyTerms) if (k.prose) add(k.term, { at: k.at, off: k.off, prose: true, source: 'key-term' });
// every term the book marks (glossary entries, key-term spans in the full text, held material and cards included): a
// term with no teaching point in the prose outside held material stays a term, taught nowhere
const universe = new Map();
for (const e of Object.values(g.entries)) if (!universe.has(norm(e.term))) universe.set(norm(e.term), e.term);
for (const part of PARTS) for (const m of P[part].raw.matchAll(/<span class="key-term">([\s\S]*?)<\/span>/g)) { const t = plain(m[1]); if (t && !universe.has(norm(t))) universe.set(norm(t), t); }
// prose glosses: paragraphs (not captions) and list items outside every figure card
let glossed = 0;
for (const part of PARTS) {
  const t = P[part].joined;
  for (const term of universe.values()) {
    for (const m of t.text.matchAll(termRe(term))) {
      const after = t.text.slice(m.index + m[0].length, m.index + m[0].length + 160).replace(/\s+/g, ' ').replace(NUMBER_PAREN, '');
      const before = t.text.slice(Math.max(0, m.index - 30), m.index).replace(/\s+/g, ' ');
      const rawBefore = t.text.slice(Math.max(0, m.index - 200), m.index);
      const cue = (GLOSS_AFTER.find(([, re]) => re.test(after)) || [])[0] || (GLOSS_BEFORE.test(before) ? 'called' : null) || formCue(term, rawBefore, after);
      if (!cue) continue;
      const off = t.map[m.index];
      add(term, { at: posAt(part, off), off, prose: true, source: `prose gloss (${cue})`, part }); glossed++;
      break;   // the first gloss in this part is the earliest here
    }
  }
}
// emphasis (section 18): a term written whole inside <em> or <strong> in a teaching place (its plural too), unless the
// sentence holding it points elsewhere (a chapter, section, part or figure number); case as termRe() matches it
const POINTS = /\b(?:Chapters?|Sections?|Parts?|Figs?\.?|Figures?)\s+(?:\d|[IVX]+\b)|§/u;
const byNorm = new Map(); for (const term of universe.values()) { const k = norm(term); if (!byNorm.has(k)) byNorm.set(k, []); byNorm.get(k).push(term); }
let emphasised = 0;
for (const part of PARTS) {
  const { src, pieces } = P[part];
  for (const m of src.matchAll(/<(em|strong)\b[^>]*>([\s\S]*?)<\/\1>/g)) {
    const inner = m.index + m[0].indexOf('>') + 1, pc = pieces.find(x => inner >= x.start && inner < x.end);
    if (!pc) continue;
    // the first character of the emphasis in the piece's text (section 19: a tag right inside <em> is a space that the
    // whitespace collapse merges into the one before, so the first character at or after the content's start)
    const i = pc.map.findIndex(x => x >= inner); if (i < 0) continue;
    const said = plain(m[2]), k = norm(said); if (!k) continue;
    const terms = [k, k.replace(/s$/, ''), k.replace(/es$/, '')].flatMap(x => byNorm.get(x) || []).filter(term => new RegExp(`^${termRe(term).source}$`, termRe(term).flags.replace('g', '')).test(said));
    if (!terms.length) continue;
    const a = Math.max(pc.text.lastIndexOf('.', i), pc.text.lastIndexOf('!', i), pc.text.lastIndexOf('?', i)) + 1;
    const ends = ['.', '!', '?'].map(c => pc.text.indexOf(c, i)).filter(x => x >= 0), b = ends.length ? Math.min(...ends) : pc.text.length;
    if (POINTS.test(pc.text.slice(a, b))) continue;
    for (const term of [...new Set(terms)]) { add(term, { at: posAt(part, inner), off: inner, prose: true, source: 'emphasis', part }); emphasised++; }
  }
}
// table row (section 18): a term written in the first cell of a defining table row (tests/pass31/places.mjs)
let rowTaught = 0;
for (const part of PARTS) for (const pc of P[part].pieces.filter(x => x.kind === 'row')) for (const term of universe.values()) {
  const m = pc.text.matchAll(termRe(term)).next().value; if (!m) continue;
  add(term, { at: posAt(part, pc.map[m.index]), off: pc.map[m.index], prose: true, source: 'table row', part }); rowTaught++;
}

// the first teaching point of each term (the earliest section, then the earliest offset; an unlocated one last)
const order = (a, b) => a.at - b.at || (a.off ?? Infinity) - (b.off ?? Infinity);
const terms = new Map();
for (const [k, { term, list }] of cand) terms.set(k, { term: universe.get(k) || term, first: [...list].sort(order)[0], list });
const out = sections.map((s, i) => {
  const known = [], defines = [], at = {};
  for (const t of terms.values()) {
    if (t.first.at < i) known.push(t.term);
    else if (t.first.at === i) {
      defines.push(t.term);
      const p = t.list.filter(c => c.at === i && c.prose && c.off !== null).sort(order)[0];
      at[t.term] = p ? p.off : null;
    }
  }
  const cmp = (a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' });
  return { part: s.part, section: s.section, label: s.label, title: s.title, ...(H ? { stripped: s.stripped } : {}), known: known.sort(cmp), defines: defines.sort(cmp),
    defines_at: Object.fromEntries(Object.keys(at).sort(cmp).map(k => [k, at[k]])) };
});
// the nearest id before an offset, in the part with held material blanked (so a record never names a held element)
const paragraphAt = (part, off, s) => { const src = P[part].src, idAt = src.lastIndexOf(' id="', off); return idAt >= 0 && (idAt >= s.start || off < s.start) ? src.slice(idAt + 5, src.indexOf('"', idAt + 5)) : s.section; };
const taught = Object.fromEntries([...terms.values()].sort((a, b) => order(a.first, b.first)).map(t => {
  const i = Math.ceil(t.first.at); const s = sections[Math.min(i, sections.length - 1)];
  return [t.term, { part: s.part, section: s.section, where: Number.isInteger(t.first.at) ? 'in' : 'before', source: t.first.source,
    ...(t.first.off !== null && Number.isInteger(t.first.at) ? { paragraph: paragraphAt(s.part, t.first.off, s), at: t.first.off } : {}) }];
}));
const untaught = [...universe].filter(([k]) => !terms.has(k)).map(([, t]) => t).sort();
for (const t of untaught) taught[t] = { part: null, section: null, where: 'nowhere', source: 'no teaching in the prose (or only in held material)' };

// all-capitals tokens. capitals: the whole text outside the figure cards (offsets kept: everything else is blanked, not
// removed), held material included; abbreviations: the paragraph and list-item text only, held material out
const prose = src => src.replace(/<!--[\s\S]*?-->/g, blank).replace(/<head[\s\S]*?<\/head>/i, blank)
  .replace(/<(script|style|nav|button|noscript)\b[\s\S]*?<\/\1>/gi, blank).replace(CARD, blank).replace(/<svg[\s\S]*?<\/svg>/g, blank)
  .replace(/<details class="fig-how">[\s\S]*?<\/details>/g, blank).replace(/<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>/g, blank)
  .replace(/<[^>]+>/g, blank);
// an all-capitals token, with an optional plural ending in lower case (VMs, OSes: section 18); group 1 is the singular
const CAPS = /(?<![\p{L}\p{N}_])([\p{Lu}\d_]*\p{Lu}[\p{Lu}\d_]*)(?:s|es)?(?![\p{L}\p{N}_])/gu;
// section 19 (the review of the section 18 freeze, A): which writings place an abbreviation. A writing places it when
// it glosses it (abbrCue below), or when it is a plain writing and neither of these holds:
//   - its sentence points elsewhere (POINTS, as for emphasis: a chapter, section, part or figure number), as a teaser
//     or a pointer does ("Part III opens up ...: ARPANET, packet switching, TCP, DNS, TLS, HTTP"; "Chapter 15's answers
//     (SBOMs, ...)"; "Chapter 3 shows the defences, among them ... ASLR");
//   - the abbreviation is never credited by a mention: a glossary term taught nowhere or written in its section only
//     inside held material (lib.mjs glossary.noMention: ASLR, CFI, HTTPS), or one the book first writes inside held
//     material (its first writing in a teaching place, read with held material in, lies in held material: CVE, US,
//     GCHQ, CA, SBOM).
// A gloss of an abbreviation: a cue of the prose-gloss list above on that writing (a parenthesis that opens with a word,
// ", which", an apposition, "called", a definitional form), or its expansion before it, the abbreviation alone in a
// parenthesis after a word ("main memory (RAM)", "interrupt request (IRQ)", "time to live (TTL)") or after ", or "
const heldOnlyT = new Set(strippedOnly.map(norm)), nowhereT = new Set(untaught.map(norm));
const firstInHeld = new Set();
if (H) { const seen = new Set();
  for (const part of PARTS) { const rj = P[part].rawJoined;
    for (const m of rj.text.matchAll(CAPS)) { const t = m[1], off = rj.map[m.index];
      if (seen.has(t) || off < 0 || (t.match(/\p{Lu}/gu) || []).length < 2) continue;
      seen.add(t); if (HM.inZone(P[part].zones, off)) firstInHeld.add(t); } } }
const restricted = t => nowhereT.has(norm(t)) || heldOnlyT.has(norm(t)) || firstInHeld.has(t);
const EXPAND_PAREN = /\p{L}[\p{L}\p{N}'’-]*\s*\(\s*$/u, EXPAND_OR = /\p{L}[\p{L}\p{N}'’-]*,\s+or\s+$/u;
function abbrCue(text, i, len, term) {
  const after = text.slice(i + len, i + len + 160).replace(/\s+/g, ' ').replace(NUMBER_PAREN, '');
  const before = text.slice(Math.max(0, i - 30), i).replace(/\s+/g, ' ');
  const rawBefore = text.slice(Math.max(0, i - 200), i);
  return (GLOSS_AFTER.find(([, re]) => re.test(after)) || [])[0] || (GLOSS_BEFORE.test(before) ? 'called' : null) || formCue(term, rawBefore, after)
    || ((EXPAND_PAREN.test(before) && /^\s*\)/u.test(after)) || (EXPAND_OR.test(before) && /^\s*[,.;:)]/u.test(after)) ? 'expansion' : null)
    // the generic form (section 18) for an abbreviation too: it opens the sentence and a verb in -s follows ("SQL tells
    // it what you want"); the one-word limit there guards an everyday sense, which an abbreviation in capitals lacks
    || (DEF_BEFORE.test(rawBefore) && GEN_AFTER.test(after) ? 'generic' : null);
}
// the sentence holding character i of a joined text: from the piece start or the last sentence end (. ! ? and any
// closing marks, then a space) before it, to the next one or the piece end; a decimal point (Fig 1.11) ends nothing.
// Returns the sentence and where the writing sits in it
const SENT_END = new RegExp(`${SEP}|[.!?]["”’)\\]]*\\s`, 'gu');
const sentenceAt = (text, i) => {
  const back = text.slice(Math.max(0, i - 2000), i), fwd = text.slice(i, i + 2000);
  let a = 0; for (const m of back.matchAll(SENT_END)) a = m.index + m[0].length;
  const e = fwd.search(new RegExp(SENT_END.source, 'u'));
  return { s: back.slice(a) + (e < 0 ? fwd : fwd.slice(0, e + 1)), at: back.length - a };
};
// does the sentence of a writing point elsewhere? POINTS, read on the sentence less every parenthesis that does not
// hold the writing (an aside citing where something else is covered, "a SIGSEGV signal (Section 05 covers signals),
// which ...", "forward secrecy (Chapter 11, Section 05): each session uses ephemeral DH values", is not the sentence
// pointing elsewhere), and less every figure number of the writing's own chapter (a sentence that brings in the
// figure beside it, "Fig 1.11 adds a fifth stage, MEM, for reading or writing data in memory", "drawn in Fig 3.4", is
// the teaching the figure goes with); a figure of another chapter ("the IP header's TTL, Fig 9.4" in Chapter 11) points
// elsewhere
const asidesOut = ({ s, at }) => {
  let out = '', depth = 0, open = -1;
  for (let k = 0; k < s.length; k++) {
    const c = s[k];
    if (c === '(') { if (depth++ === 0) open = k; continue; }
    if (c === ')' && depth > 0) { if (--depth === 0) { if (at > open && at < k) out += s.slice(open, k + 1); else out += ' '; } continue; }
    if (depth === 0) out += c;
  }
  return depth > 0 ? out + s.slice(open) : out;
};
// the chapter of an element id (ch12-hero-lead, ch3-call-p6, chBridge-io-p2, fig-3-6): its number, BR for the bridge
const chapterOf = id => { const m = String(id).match(/^(?:ch(\d+|Bridge)|fig-(\d+|br))-/); return m ? ((m[1] || m[2]) === 'Bridge' || m[2] === 'br' ? 'BR' : (m[1] || m[2])) : null; };
const FIGNUM = /\b(?:Figs?\.?|Figures?)\s+(BR|\d+)\.\d+[a-z]?(?:(?:,\s*|\s+(?:and|to|or)\s+)(?:BR|\d+)\.\d+[a-z]?)*/gu;
const pointsElsewhere = (sen, ch) => {
  const t = asidesOut(sen).replace(FIGNUM, m => [...m.matchAll(/(BR|\d+)\.\d+/gu)].every(x => x[1] === ch) ? ' ' : m);
  return POINTS.test(t);
};
// a roman numeral written as a part's number ("Part II's kernel chapter", "Parts II and III") is the book's own
// numbering, notation it uses from Part I on: placed at that writing, as a plain writing of it is
const PART_NUMERAL = /^(?:I{2,3}|IV|VI{0,3}|IX|X)$/u, PART_BEFORE = /\bParts?\s+(?:[IVX]+(?:,\s*|\s+(?:and|to|or)\s+))*$/u;
const abbreviations = {}, capitals = new Set();
for (const part of PARTS) {
  const { raw, joined } = P[part];
  for (const m of prose(raw).matchAll(CAPS)) if ((m[1].match(/\p{Lu}/gu) || []).length >= 2) capitals.add(m[1]);
  const secs = sections.filter(s => s.part === part);
  for (const m of joined.text.matchAll(CAPS)) {
    const t = m[1]; if ((t.match(/\p{Lu}/gu) || []).length < 2) continue;
    if (abbreviations[t]) continue;
    const off = joined.map[m.index]; if (off < 0) continue;
    // the section holding it; a chapter lead or closing outside the sections counts too (section 18), recorded with
    // the next section of the part (or its last); the check reads only part and offset
    const sec = secs.find(s => off >= s.start && off < s.end) || secs.find(s => s.start > off) || secs[secs.length - 1]; if (!sec) continue;
    const para = paragraphAt(part, off, sec), cue = abbrCue(joined.text, m.index, m[0].length, t);
    const numeral = !cue && PART_NUMERAL.test(t) && PART_BEFORE.test(joined.text.slice(Math.max(0, m.index - 40), m.index));
    // a chapter lead or closing sits outside its sections: its chapter is the nearest id's (the lead's own, or the last
    // section's paragraph before a closing), never the next section's
    const ch = chapterOf(para) || chapterOf(sec.section);
    // section 20 (the review of the section 19 freeze, D1): a glossary or key-term entry (TLS, TCP, UDP, HTTP, IP, DNS,
    // RSA) is placed by a gloss of it or at its own teaching point (the terms above), never by a plain writing that
    // comes first ("a TLS handshake", "using TCP or UDP"): brief section 15, the abbreviations the prose teaches are
    // listed at the paragraph that teaches them
    if (!cue && !numeral && (restricted(t) || universe.has(norm(t)) || pointsElsewhere(sentenceAt(joined.text, m.index), ch))) continue;   // a mention that places nothing
    abbreviations[t] = { part, section: sec.section, paragraph: para, at: off, by: cue ? `gloss (${cue})` : numeral ? 'part number' : 'writing' };
  }
}

// proper names (section 17): the entries a figure may use once the prose before its card writes them (tests/pass31/
// lib.mjs taughtYet), because they name a person, place, organisation, paper or product, not a mechanism. A name:
//   - has a capital letter, no digit and no word written in capitals (TLS handshake, IEEE 754, SHA-256, CAP theorem);
//   - has no en dash: the book joins two names with one for a named method (Diffie–Hellman);
//   - has no possessive followed by a word (Amdahl's law, Moore's Law: a named law);
//   - opens every word with a capital, but for the particles von, van, de, der, du, da, di, la, le (Turing machine,
//     Boolean algebra, Shannon entropy name mechanisms);
//   - of several words: their initials are not an abbreviation the book writes (Translation Lookaside Buffer: TLB;
//     Domain Name System: DNS);
//   - of one word: opens with a capital and a lower-case letter, and the book's paragraphs and list items (code left
//     out, held material included) never write it, its singular or its plural in lower case (Signals, Promises,
//     Consistency: common nouns that open a sentence or a list item);
//   - is taught somewhere outside held material: never one taught nowhere or written in its section only inside held
//     material (Reno, SQL injection), which no mention credits;
//   - is never marked with a key-term span anywhere outside the figure cards (section 18; held material included, so
//     the list only ever makes the check stricter): the book marks a concept it teaches that way (Ethernet at
//     ch8-ethernet-p1, JavaScript, Kubernetes, Raft), and such a term is credited only where it is taught, never by an
//     earlier mention.
const PARTICLES = new Set(['von', 'van', 'de', 'der', 'du', 'da', 'di', 'la', 'le']);
const bookLower = PARTS.map(p => P[p].plainText).join('\n');
const heldOnly = new Set(strippedOnly.map(norm)), nowhere = new Set(untaught.map(norm));
const keyMarked = new Set();
for (const part of PARTS) { const { raw } = P[part], rc = [...raw.matchAll(CARD)].map(m => [m.index, m.index + m[0].length]);
  for (const m of raw.matchAll(/<span class="key-term">([\s\S]*?)<\/span>/g)) if (!rc.some(([a, b]) => m.index >= a && m.index < b)) keyMarked.add(norm(plain(m[1]))); }
// section 20 (the review of the section 19 freeze, D8): an entry whose glossary definition names a mechanism is no name,
// though it is name-shaped and no key-term marks it: its head noun (the last word of the definition's first noun
// phrase, read after an expansion and its colon, up to the first , : ; ( . or relative word or preposition) is a step,
// protocol, algorithm, value, method ... ("The AES round step that ...": AddRoundKey; "Leslie Lamport's classic
// consensus protocol (1989): ...": Paxos; "Not a Number: the IEEE 754 special value ...": NaN). A person, place,
// organisation, paper or product ("Leonard Adleman, who ...", "The research laboratory where ...", "The container
// tool, released ...") keeps the name rule
const MECH = new Set(['step', 'round', 'protocol', 'algorithm', 'value', 'method', 'scheme', 'technique', 'cipher', 'procedure', 'operation', 'instruction', 'function', 'attack',
  'rule', 'law', 'theorem', 'principle', 'pattern', 'format', 'encoding', 'mechanism', 'transform', 'transformation', 'primitive', 'mode', 'construction', 'policy', 'strategy',
  'model', 'metric', 'notation', 'representation', 'structure', 'problem', 'effect', 'property', 'loop', 'test', 'check', 'routine', 'command', 'opcode', 'exchange', 'handshake']);
const defOf = new Map(Object.values(g.entries).map(e => [norm(e.term), e.definition || '']));
const headNoun = def => {
  let d = String(def || '').trim(); if (!d) return null;
  const x = d.match(/^[^:;,(.]{1,60}:\s+(?=(?:the|a|an)\s)/iu); if (x) d = d.slice(x[0].length);   // an expansion first: "Not a Number: the ..."
  const seg = d.split(/[,:;(.]|\s(?:that|which|who|whose|where|when|for|of|with|in|on|at|by|from|to|whereby|used|built|designed|written|made|released|meant|published|between|after|before)\s/u)[0];
  const w = seg.trim().split(/\s+/).pop(); return w ? w.toLowerCase().replace(/[^\p{L}-]/gu, '') : null;
};
const mechanism = form => MECH.has(headNoun(defOf.get(norm(form))));
const isName = form => {
  if (!/\p{Lu}/u.test(form) || /\p{N}/u.test(form) || /–/.test(form) || /['’]s\s/u.test(form)) return false;
  if (nowhere.has(norm(form)) || heldOnly.has(norm(form)) || keyMarked.has(norm(form))) return false;
  if (mechanism(form)) return false;
  const words = form.split(/[\s\-]+/).filter(Boolean);
  if (words.some(w => { const l = w.replace(/[^\p{L}]/gu, ''); return l.length >= 2 && l === l.toUpperCase(); })) return false;
  if (words.some(w => !/^\p{Lu}/u.test(w) && !PARTICLES.has(w))) return false;
  if (words.length > 1) return !capitals.has(words.filter(w => !PARTICLES.has(w)).map(w => w[0]).join(''));
  if (!/^\p{Lu}\p{Ll}/u.test(form)) return false;
  const lw = form.toLowerCase().replace(/['’]s$/, ''), forms = [...new Set([lw, lw.replace(/s$/, ''), lw.replace(/es$/, '')])].filter(x => x.length > 1);
  return !forms.some(x => new RegExp(`(?<![\\p{L}\\p{N}_])${esc(x)}(?:s|es)?(?![\\p{L}\\p{N}_])`, 'u').test(bookLower));
};
const names = [...universe.values()].filter(isName).sort();

fs.writeFileSync(path.resolve(ROOT, OUT), JSON.stringify({
  note: 'Known terms (scripts/known-terms.mjs). Per section in reading order: known = taught before it, defines = first taught in it, defines_at = where in the section\'s paragraphs and list items it is first taught (null: not there). A term is taught at the earliest of its glossary section (its first use in that section\'s paragraphs and list items), a prose gloss in a paragraph or list item, and a key-term span in a paragraph or list item; never in a figure card, heading, section label, table cell or code block (see the script header).',
  glossary_generated: g.generated, glossary_count: g.count, terms: terms.size, sections: out.length,
  ...(H ? { strip: { file: path.relative(ROOT, H.file), sha256: H.sha256, stripped_sections: sections.filter(s => s.stripped).map(s => s.section), glossary_terms_only_in_held: strippedOnly.sort() } } : {}),
  glossary_terms_only_in_cards: cardOnly.sort(), glossary_terms_only_outside_paragraphs: outsideParagraphs.sort(), glossary_terms_not_located: notLocated.sort(), taught_nowhere: untaught,
  taught, by_section: out,
  abbreviations, capitals: [...capitals].sort(), names
}, null, 1).replace(/\[\n\s+("[^\]]*?)\n\s+\]/g, (m, inner) => '[' + inner.replace(/,\n\s+/g, ', ') + ']'));
console.log(`known-terms: ${out.length} sections, ${universe.size} terms (${untaught.length} taught nowhere) (${g.count} glossary + key-term spans), ${glossed} prose glosses, ${emphasised} emphasised uses, ${rowTaught} table-row uses, ${Object.keys(abbreviations).length} abbreviations at their first prose paragraph${H ? `, held material stripped (${sections.filter(s => s.stripped).length} sections; ${strippedOnly.length} glossary terms used in their section only inside it)` : ''} -> ${OUT}`);
if (unplaced.length) console.log(`  glossary entries with no section in reading order: ${unplaced.join(', ')}`);
