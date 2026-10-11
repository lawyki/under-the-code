#!/usr/bin/env node
// One section as a reading packet for Pass 29's agents (docs/pass-29-30-brief.md).
//
// Prints the section in reading order as plain text: every paragraph and list
// item with its id, headings, callouts, pull-quotes and insight strips marked,
// and each figure as its label, the picture's <desc> and visible labels, the
// caption and the "How it works" strip, followed by that figure's caption at
// commit 664e794 (before Passes 27 and 28) and the section's entry in
// docs/pass-29-known-terms.json.
//   node scripts/section-packet.mjs <section-id> [--rev=<commit>] [--no-old] [--no-terms] [--html=<file>]
// --html reads the part from a file instead of public/ (a planted-gap copy, a draft).
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const ARGS = Object.fromEntries(process.argv.slice(3).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const SID = process.argv[2];
if (!SID) { console.error('usage: section-packet.mjs <section-id> [--rev=…] [--no-old] [--no-terms] [--html=file]'); process.exit(2); }
const ROOT = new URL('../', import.meta.url).pathname;
const OLD = '664e794';
const git = (rev, file) => execFileSync('git', ['show', `${rev}:${file}`], { cwd: ROOT, encoding: 'utf8', maxBuffer: 64 << 20 });

const ENT = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“', hellip: '…', times: '×', minus: '−', middot: '·' };
const dec = s => s.replace(/&(#x?[0-9a-f]+|\w+);/gi, (m, e) => e[0] === '#' ? String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1)) : (ENT[e] ?? m));
// inline markup kept as light marks: key-term **x**, strong *x*, em _x_, code `x`, sup ^x
const inline = h => dec(h
  .replace(/<span class="key-term">([\s\S]*?)<\/span>/g, '**$1**')
  .replace(/<(strong|b)\b[^>]*>([\s\S]*?)<\/\1>/g, '*$2*')
  .replace(/<(em|i|cite)\b[^>]*>([\s\S]*?)<\/\1>/g, '_$2_')
  .replace(/<code\b[^>]*>([\s\S]*?)<\/code>/g, '`$1`')
  .replace(/<sup\b[^>]*>([\s\S]*?)<\/sup>/g, '^$1')
  .replace(/<sub\b[^>]*>([\s\S]*?)<\/sub>/g, '_$1')
  .replace(/<br\s*\/?>/g, ' ')
  .replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();

const partOf = sid => {
  for (const p of ['part-1', 'part-2', 'part-3', 'part-4', 'part-5']) {
    const src = ARGS.html && fs.readFileSync(ARGS.html, 'utf8').includes(`id="${sid}"`) ? fs.readFileSync(ARGS.html, 'utf8')
      : ARGS.rev ? git(ARGS.rev, `public/${p}.html`) : fs.readFileSync(`${ROOT}public/${p}.html`, 'utf8');
    if (src.includes(`<section class="section" id="${sid}"`)) return [p, src];
  }
  return [null, null];
};
const [part, src] = partOf(SID);
if (!part) { console.error(`no section ${SID}`); process.exit(1); }
const st = src.indexOf(`<section class="section" id="${SID}"`);
const body = src.slice(st, src.indexOf('</section>', st));

// the figure block: everything from a card's opening div to the end of its strip
function figure(h) {
  const id = (h.match(/\bid="(fig-[^"]+)"/) || [])[1] || '?';
  const label = inline((h.match(/<div class="diagram-label">([\s\S]*?)<\/div>/) || [])[1] || '');
  const svg = (h.match(/<svg[\s\S]*?<\/svg>/) || [''])[0];
  const title = inline((svg.match(/<title[^>]*>([\s\S]*?)<\/title>/) || [])[1] || '');
  const desc = inline((svg.match(/<desc[^>]*>([\s\S]*?)<\/desc>/) || [])[1] || '');
  const labels = [...new Set([...svg.matchAll(/<text\b[^>]*>([\s\S]*?)<\/text>/g)].map(m => inline(m[1])).filter(Boolean))];
  const cap = h.match(/<p([^>]*)class="diagram-caption"[^>]*>([\s\S]*?)<\/p>/);
  const capId = cap ? (cap[1].match(/id="([^"]+)"/) || [])[1] : null;
  const how = (h.match(/<details class="fig-how">([\s\S]*?)<\/details>/) || [])[1] || '';
  const items = [...how.matchAll(/<li\b[^>]*>([\s\S]*?)<\/li>/g)].map(m => inline(m[1]));
  const out = [`[FIGURE ${id}] ${label}`];
  if (title) out.push(`  picture title: ${title}`);
  if (desc) out.push(`  picture (its <desc>, what the drawing shows): ${desc}`);
  if (labels.length) out.push(`  words drawn in the picture: ${labels.join(' | ')}`);
  if (cap) out.push(`  caption${capId ? ` (${capId})` : ''}: ${inline(cap[2])}`);
  if (items.length) out.push('  How it works (closed strip, opened by the reader):', ...items.map(i => `    - ${i}`));
  return { id, text: out.join('\n') };
}

// top-level child elements of an HTML fragment, balanced by tag (void and self-closing tags skipped)
const VOID = new Set(['br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'wbr', 'col', 'area', 'base', 'embed', 'param', 'track']);
function children(h) {
  const out = []; const stack = []; let start = -1;
  for (const m of h.matchAll(/<(\/?)([a-zA-Z][\w:-]*)\b[^>]*?(\/?)>/g)) {
    const [tok, close, name, self] = m; const n = name.toLowerCase();
    if (!close && (self || VOID.has(n))) continue;
    if (!close) { if (!stack.length) start = m.index; stack.push(n); continue; }
    while (stack.length && stack[stack.length - 1] !== n) stack.pop();   // tolerate stray tags
    stack.pop();
    if (!stack.length && start >= 0) { out.push(h.slice(start, m.index + tok.length)); start = -1; }
  }
  return out;
}
const idOf = h => (h.match(/^<\w+[^>]*\bid="([^"]+)"/) || [])[1];
const clsOf = h => (h.match(/^<\w+[^>]*\bclass="([^"]+)"/) || [])[1] || '';
const inner = h => h.replace(/^<[^>]+>/, '').replace(/<\/\w+>\s*$/, '');
// any block: one or more lines of text
function render(h, depth = 0) {
  const tag = (h.match(/^<(\w+)/) || [])[1].toLowerCase(), cls = clsOf(h), id = idOf(h), pad = '  '.repeat(depth);
  if (/\b(diagram-card|light-diagram)\b/.test(cls)) { const f = figure(h); figs.push(f.id); return ['', f.text, '']; }
  if (cls === 'section-number') return [`SECTION ${SID} · ${inline(h)}`];
  if (tag === 'h2') return [`TITLE: ${inline(h)}`, ''];
  if (/^h[3-6]$/.test(tag)) return ['', `${'#'.repeat(+tag[1] - 1)} ${inline(h)}`];
  if (tag === 'p') return [`${pad}${id ? id + ': ' : ''}${inline(h)}`];
  if (tag === 'ul' || tag === 'ol') return children(inner(h)).map((li, i) => `${pad}  ${tag === 'ol' ? i + 1 + '.' : '-'} ${idOf(li) ? idOf(li) + ': ' : ''}${inline(li)}`);
  if (tag === 'pre') return [`${pad}[CODE]`, dec(h.replace(/<[^>]+>/g, '')).replace(/^\n+|\n+$/g, ''), `${pad}[/CODE]`];
  if (tag === 'table') return [`${pad}[TABLE]`, ...[...h.matchAll(/<tr\b[\s\S]*?<\/tr>/g)].map(r => `${pad}  ` + [...r[0].matchAll(/<t[hd]\b[^>]*>([\s\S]*?)<\/t[hd]>/g)].map(c => inline(c[1])).join(' | ')), `${pad}[/TABLE]`];
  if (cls === 'pull-quote') return [`[PULL-QUOTE${(h.match(/id="([^"]+)"/) || [])[1] ? ' ' + h.match(/id="([^"]+)"/)[1] : ''}, owner-chosen, verbatim] ${inline(h.replace(/<span class="attr">([\s\S]*?)<\/span>/, ' (attribution: $1)'))}`];
  if (cls === 'insight-strip') { const pid = (h.match(/<p id="([^"]+)"/) || [])[1]; return [`[INSIGHT STRIP${pid ? ' ' + pid : ''}] ${inline(h)}`]; }
  if (tag === 'div' || tag === 'blockquote' || tag === 'aside' || tag === 'figure') {
    const kids = children(inner(h));
    const label = cls ? cls.split(/\s+/)[0].toUpperCase() : tag.toUpperCase();
    if (!kids.length) return [`${pad}${id ? id + ': ' : ''}${inline(h)}`];   // a leaf div: its text
    return [`${pad}[${label}${id ? ' ' + id : ''}]`, ...kids.flatMap(k => render(k, depth + 1)), `${pad}[/${label}]`];
  }
  if (tag === 'details') { const kids = children(inner(h)); const sum = kids.find(k => /^<summary/i.test(k)); return [`${pad}[DETAILS${sum ? ': ' + inline(sum) : ''}, closed by default]`, ...kids.filter(k => k !== sum).flatMap(k => render(k, depth + 1)), `${pad}[/DETAILS]`]; }
  return [`${pad}${inline(h)}`];
}
const lines = [];
const figs = [];
for (const c of children(body.replace(/^<section[^>]*>/, ''))) lines.push(...render(c));

console.log(`PART ${part}`);
console.log(lines.join('\n').replace(/\n{3,}/g, '\n\n'));

if (!ARGS['no-old'] && figs.length) {
  const [, oldSrc] = (() => { try { return [null, git(OLD, `public/${part}.html`)]; } catch { return [null, '']; } })();
  console.log(`\nOLD CAPTIONS at ${OLD} (before Passes 27 and 28; a step taught only here and carried by neither the new figure, its strip nor the prose is a search point):`);
  for (const id of figs) {
    const i = oldSrc.indexOf(`id="${id}"`);
    const cap = i < 0 ? null : (oldSrc.slice(i, i + 200000).match(/class="diagram-caption"[^>]*>([\s\S]*?)<\/p>/) || [])[1];
    console.log(`  ${id}: ${cap ? inline(cap) : '(no caption found)'}`);
  }
}
if (!ARGS['no-terms']) {
  const kt = JSON.parse(fs.readFileSync(`${ROOT}docs/pass-29-known-terms.json`, 'utf8'));
  const e = kt.by_section.find(s => s.section === SID);
  if (e) {
    console.log(`\nKNOWN TERMS before this section (${e.known.length}): ${e.known.join('; ')}`);
    console.log(`\nTERMS THIS SECTION TEACHES (${e.defines.length}): ${e.defines.join('; ')}`);
  }
}
