#!/usr/bin/env node
// add-anchor-ids.js — bake stable paragraph anchor ids into the part files.
//
// The reading-position sync (book.js + /api/position) anchors the reader's
// place to the deepest element with a stable id at the top of the viewport.
// Sections and figures already carry ids; prose paragraphs did not. This
// script gives every <p> inside a `section.section[id]` a baked id of the
// form `<sectionId>-pN` (e.g. ch4-anatomy-p7), numbered in document order.
//
// Properties that make these ids *stable*:
//   - They are literal text in the HTML — hand edits never renumber them.
//   - Re-running the script only touches <p> tags that still lack an id,
//     and never assigns an id that already exists in the file, so a
//     paragraph inserted later gets the next free number, not a neighbour's.
//
// Paragraphs outside a section.section (part openers, chapter heroes) are
// left alone — the chapter/section id is a good enough anchor there.
//
// Usage: node scripts/add-anchor-ids.js [--check]
//   --check  report what would change, write nothing, exit 1 if changes.

'use strict';

const fs = require('fs');
const path = require('path');

const PUBLIC = path.join(__dirname, '..', 'public');
const FILES = ['part-1.html', 'part-2.html', 'part-3.html', 'part-4.html', 'part-5.html'];
const CHECK = process.argv.includes('--check');

const TAG_RE = /<section\b[^>]*>|<\/section>|<p\b[^>]*>/g;

let totalAdded = 0;

for (const file of FILES) {
  const full = path.join(PUBLIC, file);
  const src = fs.readFileSync(full, 'utf8');

  // Every id already present in the file (any element) — never collide.
  const taken = new Set();
  for (const m of src.matchAll(/\bid="([^"]+)"/g)) taken.add(m[1]);

  // Stack of open <section> scopes; an entry is the section id when the
  // section is a content section (class contains "section" and it has an
  // id), else null.
  const stack = [];
  const counters = new Map(); // sectionId -> next candidate number

  let out = '';
  let last = 0;
  let added = 0;

  for (const m of src.matchAll(TAG_RE)) {
    const tag = m[0];
    if (tag === '</section>') {
      stack.pop();
      continue;
    }
    if (tag.startsWith('<section')) {
      const cls = /\bclass="([^"]*)"/.exec(tag);
      const id = /\bid="([^"]*)"/.exec(tag);
      const isContent = cls && /\bsection\b/.test(cls[1]) && id;
      stack.push(isContent ? id[1] : null);
      continue;
    }
    // <p ...> — only inside an id'd content section, only if it has no id.
    const scope = stack.length ? stack[stack.length - 1] : null;
    if (!scope) continue;
    if (/\bid="/.test(tag)) continue;

    let n = counters.get(scope) || 1;
    let candidate;
    do { candidate = scope + '-p' + n++; } while (taken.has(candidate));
    counters.set(scope, n);
    taken.add(candidate);

    const patched = tag.replace(/^<p\b/, '<p id="' + candidate + '"');
    out += src.slice(last, m.index) + patched;
    last = m.index + tag.length;
    added++;
  }
  out += src.slice(last);

  totalAdded += added;
  if (added && !CHECK) fs.writeFileSync(full, out);
  console.log(`${file}: ${added} paragraph id${added === 1 ? '' : 's'} ${CHECK ? 'missing' : 'added'}`);
}

if (CHECK && totalAdded > 0) process.exit(1);
console.log(CHECK ? 'check complete' : `done — ${totalAdded} ids baked`);
