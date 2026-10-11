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
//   node scripts/known-terms.mjs [--out=docs/pass-29-known-terms.json]
import fs from 'node:fs';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../', import.meta.url).pathname;
const OUT = ARGS.out || 'docs/pass-29-known-terms.json';
const PARTS = ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“' };
const plain = s => s.replace(/<[^>]+>/g, '').replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e) => e[0] === '#' ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1)) : (ENT[e] ?? m)).replace(/\s+/g, ' ').trim();
const norm = s => s.toLowerCase().replace(/[–-]/g, ' ').replace(/\s+/g, ' ').trim();

// reading order
const sections = [];
const keyTerms = [];   // { term, at: index of the section it is taught in (or before) }
for (const part of PARTS) {
  const src = fs.readFileSync(`${ROOT}public/${part}.html`, 'utf8');
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
const g = JSON.parse(fs.readFileSync(`${ROOT}public/glossary.json`, 'utf8'));
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

fs.writeFileSync(`${ROOT}${OUT}`, JSON.stringify({
  note: 'Pass 29/30 known terms (scripts/known-terms.mjs). Per section in reading order: known = taught before it, defines = first taught in it. Sources: public/glossary.json first-use sections and <span class="key-term"> positions.',
  glossary_generated: g.generated, glossary_count: g.count, terms: terms.size, sections: out.length,
  taught, by_section: out
}, null, 1).replace(/\[\n\s+("[^\]]*?)\n\s+\]/g, (m, inner) => '[' + inner.replace(/,\n\s+/g, ', ') + ']'));
console.log(`known-terms: ${out.length} sections, ${terms.size} terms (${g.count} glossary + key-term spans) -> ${OUT}`);
if (unplaced.length) console.log(`  glossary entries with no section in reading order: ${unplaced.join(', ')}`);
