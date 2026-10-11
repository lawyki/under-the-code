#!/usr/bin/env node
// Section-prose words per section and per part (Pass 29 budget, docs/pass-29-30-brief.md).
//
// "Section prose" is what Pass 27 counted (§4aa): every <p> and <li> inside a
// <section class="section" id="ch…">, with figure cards (drawing, caption and
// "How it works" strip) masked out, section-number labels skipped, tags
// stripped, words split on whitespace. A port of Pass 27's p27/extract.py.
//
//   node scripts/count-prose.mjs [--rev=02f486b] [--part=part-1] [--sections] [--json=out.json]
//
// --rev reads public/part-N.html from that commit (git show); default: the working tree.
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../', import.meta.url).pathname;
const PARTS = ARGS.part ? [ARGS.part] : ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];

const read = part => ARGS.rev
  ? execFileSync('git', ['show', `${ARGS.rev}:public/${part}.html`], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 << 20 })
  : fs.readFileSync(`${ROOT}public/${part}.html`, 'utf8');

const words = s => { const t = s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim(); return t ? t.split(' ').length : 0; };

export function countPart(src) {
  const secs = [...src.matchAll(/<section class="section" id="(ch[^"]+)"/g)].map(m => [m.index, m[1]]);
  const out = [];
  secs.forEach(([st, id], i) => {
    let end = i + 1 < secs.length ? secs[i + 1][0] : src.indexOf('</main>', st);
    if (end < 0) end = src.length;
    const body = src.slice(st, end);
    // mask figures and their captions so prose inside them is never counted
    const masked = body.replace(/<div class="(?:diagram-card|light-diagram)[^"]*"[\s\S]*?<\/svg>[\s\S]*?<\/div>/g, m => ' '.repeat(m.length));
    let n = 0, units = 0;
    for (const m of masked.matchAll(/<(p|li)\b[^>]*>[\s\S]*?<\/\1>/g)) {
      const h = body.slice(m.index, m.index + m[0].length);
      if (h.slice(0, 120).includes('diagram-caption') || h.includes('class="section-number"')) continue;
      n += words(h); units++;
    }
    out.push({ id, words: n, units });
  });
  return out;
}

const result = {};
for (const part of PARTS) {
  const secs = countPart(read(part));
  result[part] = { words: secs.reduce((s, x) => s + x.words, 0), sections: secs };
}
if (ARGS.json) fs.writeFileSync(ARGS.json, JSON.stringify({ rev: ARGS.rev || 'worktree', ...result }, null, 1));
let total = 0;
for (const part of PARTS) {
  const r = result[part]; total += r.words;
  console.log(`${part}: ${r.words.toLocaleString('en')} words, ${r.sections.length} sections`);
  if (ARGS.sections) for (const s of r.sections) console.log(`  ${s.id} ${s.words}`);
}
if (PARTS.length > 1) console.log(`total: ${total.toLocaleString('en')}`);
