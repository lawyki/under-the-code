#!/usr/bin/env node
// Known terms per section, in reading order (Pass 29/30, docs/pass-29-30-brief.md).
//
// For every <section class="section" id="ch…"> of parts 1 to 5, in reading order:
//   known    the terms the book has taught before the section starts
//   defines  the terms first taught inside it
// Sources: public/glossary.json (each entry's first-use part and section, the
// extractor's own assignment) and every <span class="key-term"> in the parts
// (taught where it stands; one outside a section, such as a hero lead, counts
// as taught before the next section). Terms merge case-insensitively.
//
// Also (Pass 31, brief section 15), two lists the figure checks read; known and
// defines are unchanged by them:
//   abbreviations  every all-capitals token (two or more capital letters, digits
//                  and underscores allowed: CPU, CR3, SYN_SENT) at the prose
//                  paragraph that first uses it: part, section, the nearest id
//                  before it, and its offset in the part's HTML. Prose is the
//                  text of the sections with every figure card (label, picture,
//                  caption, How-it-works strip), every other <svg>, scripts and
//                  styles taken out, so a token first written in a figure's own
//                  caption, label or strip is not taught for that figure.
//   capitals       every all-capitals token the book's text writes anywhere
//                  outside the figure cards (sections, heroes, leads).
//
//   node scripts/known-terms.mjs [--out=docs/pass-29-known-terms.json] [--public=<public dir>]
import fs from 'node:fs'; import path from 'node:path';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../', import.meta.url).pathname;
const OUT = ARGS.out || 'docs/pass-29-known-terms.json';
const PUB = ARGS.public && ARGS.public !== true ? path.resolve(ARGS.public) + '/' : `${ROOT}public/`;   // the tree to read
const PARTS = ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“' };
const plain = s => s.replace(/<[^>]+>/g, '').replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e) => e[0] === '#' ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1)) : (ENT[e] ?? m)).replace(/\s+/g, ' ').trim();
const norm = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();

// reading order
const sections = [];
const keyTerms = [];   // { term, at: index of the section it is taught in (or before) }
for (const part of PARTS) {
  const src = fs.readFileSync(`${PUB}${part}.html`, 'utf8');
  const starts = [...src.matchAll(/<section class="section" id="(ch[^"]+)"/g)].map(m => ({ id: m[1], start: m.index }));
  const base = sections.length;
  starts.forEach((s, i) => {
    const close = src.indexOf('</section>', s.start);
    const body = src.slice(s.start, close);
    const title = (body.match(/<h2[^>]*>([\s\S]*?)<\/h2>/) || [])[1];
    const label = (body.match(/<div class="section-number">([^<]+)<\/div>/) || [])[1];
    sections.push({ part, section: s.id, label: label ? plain(label) : '', title: title ? plain(title) : '', start: s.start, end: close });
  });
  for (const m of src.matchAll(/<span class="key-term">([\s\S]*?)<\/span>/g)) {
    const term = plain(m[1]); if (!term) continue;
    // inside a section: that section; between sections (a hero lead): before the next one
    let at = -1;
    for (let i = base; i < sections.length; i++) {
      if (m.index >= sections[i].start && m.index < sections[i].end) { at = i; break; }
      if (m.index < sections[i].start) { at = i - 0.5; break; }
    }
    if (at === -1) at = sections.length - 0.5;   // after the last section of the part
    keyTerms.push({ term, at, part });
  }
}
const idx = new Map(sections.map((s, i) => [s.part + '|' + s.section, i]));

// every term with the point it is first taught: an integer i (inside section i) or i - 0.5 (before section i)
const terms = new Map();
const add = (term, at, source) => {
  const k = norm(term); const cur = terms.get(k);
  if (!cur || at < cur.at) terms.set(k, { term, at, source: cur && cur.at === at ? cur.source : source });
};
const g = JSON.parse(fs.readFileSync(`${PUB}glossary.json`, 'utf8'));
let unplaced = [];
for (const e of Object.values(g.entries)) {
  const i = idx.get(e.part + '|' + e.section);
  if (i === undefined) { unplaced.push(e.term); continue; }
  add(e.term, i, 'glossary');
}
for (const k of keyTerms) add(k.term, k.at, 'key-term');

const out = sections.map((s, i) => {
  const known = [], defines = [];
  for (const t of terms.values()) {
    if (t.at < i) known.push(t.term);
    else if (t.at === i) defines.push(t.term);
  }
  const cmp = (a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' });
  return { part: s.part, section: s.section, label: s.label, title: s.title, known: known.sort(cmp), defines: defines.sort(cmp) };
});
const taught = Object.fromEntries([...terms.values()].sort((a, b) => a.at - b.at).map(t => {
  const i = Math.ceil(t.at); const s = sections[Math.min(i, sections.length - 1)];
  return [t.term, { part: s.part, section: s.section, where: Number.isInteger(t.at) ? 'in' : 'before', source: t.source }];
}));

// all-capitals tokens in the prose (offsets kept: everything that is not prose is blanked, not removed)
const CARD = /<div class="(?:diagram-card|light-diagram)[^"]*" id="([^"]+)">[\s\S]*?<\/svg>\s*<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>\s*(?:<details class="fig-how">[\s\S]*?<\/details>\s*)?<\/div>/g;
const blank = m => m.replace(/[^\n]/g, ' ');
const prose = src => src.replace(/<!--[\s\S]*?-->/g, blank).replace(/<head[\s\S]*?<\/head>/i, blank)
  .replace(/<(script|style|nav|button|noscript)\b[\s\S]*?<\/\1>/gi, blank).replace(CARD, blank).replace(/<svg[\s\S]*?<\/svg>/g, blank)
  .replace(/<details class="fig-how">[\s\S]*?<\/details>/g, blank).replace(/<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>/g, blank)
  .replace(/<[^>]+>/g, blank);
const CAPS = /(?<![\p{L}\p{N}_])[\p{Lu}\d_]*\p{Lu}[\p{Lu}\d_]*(?![\p{L}\p{N}_])/gu;
const abbreviations = {}, capitals = new Set();
for (const part of PARTS) {
  const src = fs.readFileSync(`${PUB}${part}.html`, 'utf8'), txt = prose(src);
  const secs = sections.filter(s => s.part === part);
  for (const m of txt.matchAll(CAPS)) {
    const t = m[0]; if ((t.match(/\p{Lu}/gu) || []).length < 2) continue;
    capitals.add(t);
    if (abbreviations[t]) continue;
    const sec = secs.find(s => m.index >= s.start && m.index < s.end); if (!sec) continue;   // taught only inside a section
    const idAt = src.lastIndexOf(' id="', m.index), paragraph = idAt >= sec.start ? src.slice(idAt + 5, src.indexOf('"', idAt + 5)) : sec.section;
    abbreviations[t] = { part, section: sec.section, paragraph, at: m.index };
  }
}

fs.writeFileSync(`${ROOT}${OUT}`, JSON.stringify({
  note: 'Pass 29/30 known terms (scripts/known-terms.mjs). Per section in reading order: known = taught before it, defines = first taught in it. Sources: public/glossary.json first-use sections and <span class="key-term"> positions.',
  glossary_generated: g.generated, glossary_count: g.count, terms: terms.size, sections: out.length,
  taught, by_section: out,
  abbreviations, capitals: [...capitals].sort()
}, null, 1).replace(/\[\n\s+("[^\]]*?)\n\s+\]/g, (m, inner) => '[' + inner.replace(/,\n\s+/g, ', ') + ']'));
console.log(`known-terms: ${out.length} sections, ${terms.size} terms (${g.count} glossary + key-term spans), ${Object.keys(abbreviations).length} abbreviations at their first prose paragraph -> ${OUT}`);
if (unplaced.length) console.log(`  glossary entries with no section in reading order: ${unplaced.join(', ')}`);
