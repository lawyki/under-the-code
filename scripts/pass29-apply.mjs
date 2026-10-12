#!/usr/bin/env node
// Apply Pass 29 section edits to a part, with the brief's guards (docs/pass-29-30-brief.md).
//
//   node scripts/pass29-apply.mjs --part=part-1 --edits=a.json[,b.json…] [--base=<part file>] [--out=<file>] [--write]
//
// An edits file: { "section": "<id>", "edits": [ … ] }, each edit one of
//   { "op": "replace", "id": "<p or li id>", "html": "<new inner HTML>" }
//   { "op": "insert_after", "after": "<id>", "html": "<inner HTML>" }        a new <p>, id assigned here
//   { "op": "delete", "id": "<id>", "alias_to": "<surviving id>" }          the id migrates via ANCHOR_ALIASES
// Files apply in order, each edit by id inside its own section only. Refused (nothing written): an id
// missing or outside the section, a locked unit (pull-quotes; captions of the kept-original figures and
// fig 18.6; text inside a figure other than its caption), a changed tag, an em dash, unbalanced markup,
// an alias whose target does not survive, and a section where more than a quarter of its paragraphs
// change: an owner call, not a rewrite (paragraphs = every <p> with a -pN id, captions included, as
// the book numbers them). New ids take <section>-p<N>, N one more than the highest the section ever
// used (current ids, ANCHOR_ALIASES keys, git history), so none is reused.
// --no-quarter lifts the quarter-paragraph limit: only for the law-4 language pass (owner ruling, 2026-10-12, "redo the entire book").
// Without --write the patched part goes to --out (default: stdout report only). With --write it goes to
// public/<part>.html and new aliases are added to ANCHOR_ALIASES in public/book.js.
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { countPart } from './count-prose.mjs';

const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../', import.meta.url).pathname;
const PART = ARGS.part;
if (!PART || !ARGS.edits) { console.error('usage: pass29-apply.mjs --part=part-N --edits=a.json[,b.json] [--base=file] [--out=file] [--write]'); process.exit(2); }
let src = fs.readFileSync(ARGS.base || `${ROOT}public/${PART}.html`, 'utf8');
const orig = src;
const EXC = JSON.parse(fs.readFileSync(`${ROOT}docs/pass-30-exceptions.json`, 'utf8'));
const FROZEN = new Set(EXC.caption_length.ids);
const BOOKJS = fs.readFileSync(`${ROOT}public/book.js`, 'utf8');
const aliasBlock = BOOKJS.slice(BOOKJS.indexOf('const ANCHOR_ALIASES = {'), BOOKJS.indexOf('};', BOOKJS.indexOf('const ANCHOR_ALIASES = {')));
const oldAliases = new Set([...aliasBlock.matchAll(/'([^']+)':/g)].map(m => m[1]));
const hist = new Set(execFileSync('git', ['log', '-p', '--format=', '--', `public/${PART}.html`], { cwd: ROOT, encoding: 'utf8', maxBuffer: 256 << 20 }).match(/id="ch[0-9A-Za-z]+-[A-Za-z0-9-]+-p\d+"/g)?.map(s => s.slice(4, -1)) || []);

const problems = [], log = [], aliases = {};
const text = h => h.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
const words = h => { const t = text(h); return t ? t.split(' ').length : 0; };
const balanced = h => { const st = []; for (const m of h.matchAll(/<(\/?)([a-zA-Z][\w-]*)\b[^>]*?(\/?)>/g)) { const n = m[2].toLowerCase(); if (m[3] || ['br', 'img', 'wbr'].includes(n)) continue; if (!m[1]) st.push(n); else if (st.pop() !== n) return false; } return !st.length; };
function sectionSpan(sid) { const s = src.indexOf(`<section class="section" id="${sid}"`); if (s < 0) return null; return [s, src.indexOf('</section>', s)]; }
function figSpans(s, e) {
  const out = [];
  for (const m of src.slice(s, e).matchAll(/<div class="(?:diagram-card|light-diagram)[^"]*"[^>]*\bid="(fig-[^"]+)"/g)) {
    const a = s + m.index; let d = 0, b = a;
    for (const t of src.slice(a, e).matchAll(/<(\/?)div\b[^>]*>/g)) { d += t[1] ? -1 : 1; if (!d) { b = a + t.index + t[0].length; break; } }
    out.push({ id: m[1], a, b });
  }
  return out;
}
function findUnit(sid, id) {
  const sp = sectionSpan(sid); if (!sp) return { err: `section ${sid} not found` };
  const re = new RegExp(`<(p|li)\\b([^>]*\\bid="${id.replace(/[-.]/g, '\\$&')}"[^>]*)>([\\s\\S]*?)<\\/\\1>`, 'g');
  const all = [...src.matchAll(re)];
  if (all.length !== 1) return { err: `${id} occurs ${all.length} times` };
  const m = all[0];
  if (m.index < sp[0] || m.index > sp[1]) return { err: `${id} is outside ${sid}` };
  const fig = figSpans(sp[0], sp[1]).find(f => m.index > f.a && m.index < f.b);
  const cls = (m[2].match(/class="([^"]+)"/) || [])[1] || '';
  const pq = /class="pull-quote">\s*$/.test(src.slice(Math.max(0, m.index - 200), m.index));
  let locked = null;
  if (pq) locked = 'pull-quote (owner-chosen)';
  else if (fig && !cls.includes('diagram-caption')) locked = `figure text in ${fig.id}`;
  else if (fig && FROZEN.has(fig.id)) locked = `caption of ${fig.id} (kept original or owner-authored)`;
  return { m, tag: m[1], attrs: m[2], inner: m[3], start: m.index, end: m.index + m[0].length, open: `<${m[1]}${m[2]}>`, locked, isProse: !fig && !pq };
}
function proseCount(sid) { const sp = sectionSpan(sid); return [...src.slice(sp[0], sp[1]).matchAll(/<p\b[^>]*\bid="[^"]+-p\d+"/g)].length; }   // every numbered paragraph, captions included
function nextId(sid) {
  let max = 0;
  const re = new RegExp(`^${sid.replace(/[-.]/g, '\\$&')}-p(\\d+)$`);
  for (const pool of [[...src.matchAll(/id="([^"]+)"/g)].map(m => m[1]), [...oldAliases], [...hist], Object.keys(aliases), [...usedNew]]) for (const id of pool) { const m = id.match(re); if (m) max = Math.max(max, +m[1]); }
  return `${sid}-p${max + 1}`;
}
const usedNew = new Set();
const touched = {};   // section -> Set of prose ids changed
const baseProse = {};

for (const f of String(ARGS.edits).split(',').filter(Boolean)) {
  const job = JSON.parse(fs.readFileSync(f, 'utf8'));
  const sid = job.section;
  if (!sectionSpan(sid)) { problems.push(`${f}: section ${sid} not in ${PART}`); continue; }
  if (!(sid in baseProse)) { const save = src; src = orig; baseProse[sid] = sectionSpan(sid) ? proseCount(sid) : 0; src = save; }
  touched[sid] ||= new Set();
  for (const e of job.edits || []) {
    if (e.html && /—/.test(e.html)) { problems.push(`${sid} ${e.id || e.after}: em dash`); continue; }
    if (e.html && !balanced(e.html)) { problems.push(`${sid} ${e.id || e.after}: unbalanced markup`); continue; }
    if (e.op === 'replace') {
      const u = findUnit(sid, e.id); if (u.err) { problems.push(`${sid}: ${u.err}`); continue; }
      if (u.locked) { problems.push(`${sid} ${e.id}: locked, ${u.locked}`); continue; }
      const indent = (u.inner.match(/^\n(\s*)/) || [])[1];
      const html = indent !== undefined ? `\n${indent}${e.html.trim()}\n${(u.inner.match(/\n(\s*)$/) || [, ''])[1]}` : e.html;
      log.push(`${sid} replace ${e.id}: ${words(u.inner)} -> ${words(html)} words`);
      src = src.slice(0, u.start) + u.open + html + `</${u.tag}>` + src.slice(u.end);
      if (u.isProse) touched[sid].add(e.id);
    } else if (e.op === 'insert_after') {
      const u = findUnit(sid, e.after); if (u.err) { problems.push(`${sid}: ${u.err}`); continue; }
      if (!u.isProse) { problems.push(`${sid} insert after ${e.after}: only after a prose paragraph`); continue; }
      const id = nextId(sid); usedNew.add(id);
      const ls = src.lastIndexOf('\n', u.start); const ind = src.slice(ls + 1, u.start).match(/^\s*/)[0];
      const blk = `\n\n${ind}<p id="${id}">\n${ind}  ${e.html.trim()}\n${ind}</p>`;
      // after the paragraph, or after the whole list item's list if it is an li
      let at = u.end; if (u.tag === 'li') { const close = src.indexOf('</ul>', u.end), close2 = src.indexOf('</ol>', u.end); at = Math.min(...[close, close2].filter(x => x > 0)) + 5; }
      src = src.slice(0, at) + blk + src.slice(at);
      log.push(`${sid} insert ${id} after ${e.after}: ${words(e.html)} words`);
      touched[sid].add(id);
    } else if (e.op === 'delete') {
      const u = findUnit(sid, e.id); if (u.err) { problems.push(`${sid}: ${u.err}`); continue; }
      if (u.locked) { problems.push(`${sid} ${e.id}: locked, ${u.locked}`); continue; }
      if (!e.alias_to) { problems.push(`${sid} delete ${e.id}: no alias_to`); continue; }
      const ls = src.lastIndexOf('\n', u.start);
      src = src.slice(ls + 1, u.start).trim() === '' ? src.slice(0, ls) + src.slice(u.end) : src.slice(0, u.start) + src.slice(u.end);
      aliases[e.id] = e.alias_to; touched[sid].add(e.id);
      log.push(`${sid} delete ${e.id} (alias -> ${e.alias_to}): -${words(u.inner)} words`);
    } else problems.push(`${sid}: unknown op ${e.op}`);
  }
}
for (const [a, t] of Object.entries(aliases)) { let x = t; const seen = new Set(); while (aliases[x] && !seen.has(x)) { seen.add(x); x = aliases[x]; } aliases[a] = x; if (!src.includes(`id="${x}"`)) problems.push(`alias ${a} -> ${x}: target does not survive`); }
for (const [sid, set] of Object.entries(touched)) {
  const n = baseProse[sid]; if (!ARGS['no-quarter'] && set.size * 4 > n) problems.push(`${sid}: ${set.size} of ${n} paragraphs touched, more than a quarter (owner call)`);
}
// section word deltas, counted exactly as scripts/count-prose.mjs counts them
const count = s => Object.fromEntries(countPart(s).map(x => [x.id, x.words]));
const before = count(orig), after = count(src);
let tb = 0, ta = 0; for (const k in before) { tb += before[k]; ta += after[k] ?? 0; }
for (const l of log) console.log(l);
for (const sid of Object.keys(touched)) console.log(`${sid}: ${before[sid]} -> ${after[sid]} words (${after[sid] - before[sid] >= 0 ? '+' : ''}${after[sid] - before[sid]}), ${touched[sid].size} of ${baseProse[sid]} paragraphs touched`);
console.log(`${PART}: ${tb} -> ${ta} section-prose words (${ta - tb >= 0 ? '+' : ''}${ta - tb}); aliases ${JSON.stringify(aliases)}`);
if (problems.length) { for (const p of problems) console.log('PROBLEM', p); console.log(`refused: ${problems.length} problem(s), nothing written`); process.exit(1); }
if (ARGS.out) { fs.writeFileSync(ARGS.out, src); console.log('patched copy ->', ARGS.out); }
if (ARGS.write) {
  fs.writeFileSync(`${ROOT}public/${PART}.html`, src);
  if (Object.keys(aliases).length) {
    const end = BOOKJS.indexOf('};', BOOKJS.indexOf('const ANCHOR_ALIASES = {'));
    const head = BOOKJS.slice(0, end).replace(/\s*$/, '');
    const add = `,\n    // Pass 29 (the book teaches), ${PART}\n` + Object.entries(aliases).map(([a, t]) => `    '${a}': '${t}'`).join(',\n') + '\n  ';
    fs.writeFileSync(`${ROOT}public/book.js`, head + add + BOOKJS.slice(end));
  }
  console.log('written', `public/${PART}.html`, Object.keys(aliases).length ? '+ book.js aliases' : '');
}
