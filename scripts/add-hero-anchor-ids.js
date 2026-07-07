#!/usr/bin/env node
// add-hero-anchor-ids.js — bake stable sub-anchor ids into the chapter heroes.
//
// The reading-position sync anchors the reader's place to the deepest baked id
// at the reading line, and stores a fraction *within* that element. Chapter
// heroes previously had no baked ids inside them, so a reader parked in a hero
// anchored to the whole `<section id="chN">` — a very tall, heterogeneous box.
// The same stored fraction then resolved to different content across viewports
// (a hero is ~90vh, but the chapter below it is not, so fraction-of-chapter is
// not fraction-of-text). This gives each hero's three text blocks their own id,
// so a mid-hero position anchors to a short, text-homogeneous element and the
// fraction maps to the same words on every device — exactly like a body
// paragraph (see scripts/add-anchor-ids.js).
//
// Per chapter hero, ids are added to (when present, when missing an id):
//   .chapter-label     -> chN-hero-label
//   the hero <h1>      -> chN-hero-title
//   .chapter-subtitle  -> chN-hero-lead
// where chN is the id of the enclosing chapter <section> (ch1..ch18, chBridge).
//
// Properties (same as add-anchor-ids.js): ids are literal text, never collide
// with an existing id, and re-running only touches elements that still lack one.
//
// Usage: node scripts/add-hero-anchor-ids.js [--check]
//   --check  report what would change, write nothing, exit 1 if changes.

'use strict';

const fs = require('fs');
const path = require('path');

const PUBLIC = path.join(__dirname, '..', 'public');
const FILES = ['part-1.html', 'part-2.html', 'part-3.html', 'part-4.html', 'part-5.html'];
const CHECK = process.argv.includes('--check');

// A chapter wrapper section: <section id="ch13"> / <section id="chBridge">.
const CHAPTER_ID = /^ch(?:\d+|Bridge)$/;
// Tokens we react to, in document order.
const TAG_RE = /<section\b[^>]*>|<div\b[^>]*class="[^"]*"[^>]*>|<h1\b[^>]*>|<p\b[^>]*class="[^"]*"[^>]*>/g;

function hasClass(tag, cls) {
  const m = /\bclass="([^"]*)"/.exec(tag);
  return !!m && new RegExp('\\b' + cls + '\\b').test(m[1]);
}
function idOf(tag) { const m = /\bid="([^"]*)"/.exec(tag); return m ? m[1] : null; }

let totalAdded = 0;

for (const file of FILES) {
  const full = path.join(PUBLIC, file);
  const src = fs.readFileSync(full, 'utf8');

  const taken = new Set();
  for (const m of src.matchAll(/\bid="([^"]+)"/g)) taken.add(m[1]);

  let chapter = null;                 // current chapter id, once inside its hero
  let want = null;                    // { label, title, lead } still to tag
  let out = '';
  let last = 0;
  let added = 0;

  const inject = (tag, index, id) => {
    if (taken.has(id)) return false;
    // insert id right after the tag name
    const patched = tag.replace(/^(<\w+)\b/, '$1 id="' + id + '"');
    out += src.slice(last, index) + patched;
    last = index + tag.length;
    taken.add(id);
    added++;
    return true;
  };

  for (const m of src.matchAll(TAG_RE)) {
    const tag = m[0];

    if (tag.startsWith('<section')) {
      const id = idOf(tag);
      if (id && CHAPTER_ID.test(id)) {
        // entering a chapter — its hero's blocks are the next label/h1/subtitle
        chapter = id;
        want = { label: true, title: true, lead: true };
      } else if (hasClass(tag, 'section') || hasClass(tag, 'part-opener')) {
        // content section or part opener — the hero (if any) is done
        chapter = null; want = null;
      }
      continue;
    }
    if (!chapter || !want) continue;

    if (want.label && tag.startsWith('<div') && hasClass(tag, 'chapter-label')) {
      if (!idOf(tag)) inject(tag, m.index, chapter + '-hero-label');
      want.label = false;
    } else if (want.title && tag.startsWith('<h1')) {
      if (!idOf(tag)) inject(tag, m.index, chapter + '-hero-title');
      want.title = false;
    } else if (want.lead && tag.startsWith('<p') && hasClass(tag, 'chapter-subtitle')) {
      if (!idOf(tag)) inject(tag, m.index, chapter + '-hero-lead');
      want.lead = false;
    }
  }
  out += src.slice(last);

  totalAdded += added;
  if (added && !CHECK) fs.writeFileSync(full, out);
  console.log(`${file}: ${added} hero id${added === 1 ? '' : 's'} ${CHECK ? 'missing' : 'added'}`);
}

if (CHECK && totalAdded > 0) process.exit(1);
console.log(CHECK ? 'check complete' : `done — ${totalAdded} hero ids baked`);
