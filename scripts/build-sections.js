#!/usr/bin/env node
// Build script for the sections map (Pass 25).
//
// Reads public/part-1..5.html and writes public/sections.json: one entry per
// <section class="section" id="ch…">, keyed "part-N|<section id>", carrying
// the labels the client shows for a mark or a place that lives in another
// part (the account page's "Your marks" list, the docked cue) without
// loading that part's HTML:
//
//   { part, a, chapterId, chapterNum, label, title }
//
//   chapterNum — "Chapter 4" / "Bridge", the same rule as book.js formatChapterNum
//   label      — the .section-number text ("03 — The Architecture")
//   title      — the section's h2 text
//
// Both texts: <br> becomes a space, tags dropped, entities decoded,
// whitespace collapsed (book.js headingText).
//
// No dependencies; simple regex parsing over the baked HTML, like
// build-glossary.js. Re-run after any prose edit that touches a section
// heading or id:
//   npm run build:sections

'use strict';

const fs = require('fs');
const path = require('path');

const BOOK_DIR = path.resolve(__dirname, '..', 'public');
const OUT = path.join(BOOK_DIR, 'sections.json');
// Section counts per part (UNDER.md / pass-25 review H7). A mismatch means the
// parse broke or the book changed; fail loudly rather than ship a short map.
const EXPECTED = { 'part-1': 24, 'part-2': 24, 'part-3': 30, 'part-4': 19, 'part-5': 19 };

const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
  mdash: '—', ndash: '–', middot: '·', hellip: '…', rsquo: '’', lsquo: '‘',
  rdquo: '”', ldquo: '“', times: '×', rarr: '→', larr: '←', shy: '' };

function decode(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === '#') {
      const n = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(n) ? String.fromCodePoint(n) : m;
    }
    const v = NAMED[e.toLowerCase()];
    return v === undefined ? m : v;
  });
}

function text(html) {
  return decode(html.replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]*>/g, ''))
    .replace(/\s+/g, ' ').trim();
}

function formatChapterNum(chapterId) {
  if (chapterId === 'chBridge') return 'Bridge';
  const n = chapterId.replace(/^ch/, '');
  return /^\d+$/.test(n) ? 'Chapter ' + n : chapterId;
}

const sections = {};
const counts = {};
let failed = false;

for (let i = 1; i <= 5; i++) {
  const part = 'part-' + i;
  const html = fs.readFileSync(path.join(BOOK_DIR, part + '.html'), 'utf8');
  const openRe = /<section class="section" id="(ch[^"]+)"[^>]*>/g;
  const opens = [];
  let m;
  while ((m = openRe.exec(html))) opens.push({ id: m[1], start: m.index + m[0].length });
  counts[part] = opens.length;

  opens.forEach((o, k) => {
    // The section's own markup: up to its closing tag (sections do not nest),
    // bounded by the next section's opening as a safety net.
    const limit = k + 1 < opens.length ? opens[k + 1].start : html.length;
    const close = html.indexOf('</section>', o.start);
    const body = html.slice(o.start, close >= 0 && close < limit ? close : limit);
    const lab = /<div class="section-number"[^>]*>([\s\S]*?)<\/div>/.exec(body);
    const h2 = /<h2\b[^>]*>([\s\S]*?)<\/h2>/.exec(body);
    if (!lab || !h2) {
      console.error(`${part} ${o.id}: missing ${!lab ? '.section-number' : 'h2'}`);
      failed = true;
    }
    const chapterId = o.id.split('-')[0];
    const key = part + '|' + o.id;
    if (sections[key]) { console.error('duplicate ' + key); failed = true; }
    sections[key] = {
      part,
      a: o.id,
      chapterId,
      chapterNum: formatChapterNum(chapterId),
      label: lab ? text(lab[1]) : '',
      title: h2 ? text(h2[1]) : '',
    };
  });
}

for (const [part, n] of Object.entries(EXPECTED)) {
  if (counts[part] !== n) { console.error(`${part}: ${counts[part]} sections, expected ${n}`); failed = true; }
}
if (failed) process.exit(1);

fs.writeFileSync(OUT, JSON.stringify({ generated: new Date().toISOString(), sections }, null, 1) + '\n');
const total = Object.keys(sections).length;
console.log(`sections.json: ${total} sections (${Object.values(counts).join('/')})`);
