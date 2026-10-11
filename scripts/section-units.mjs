#!/usr/bin/env node
// The editable units of one section, as JSON, for Pass 29's teacher (docs/pass-29-30-brief.md).
//
// Every <p> or <li> with an id inside <section class="section" id="…">: its id,
// tag, class, where it sits (prose, caption, insight, pull-quote, list), its
// inner HTML exactly as the file has it (edits replace this), its plain text and
// word count, and whether Pass 29 may touch it (pull-quotes are owner-chosen;
// the captions of the kept-original figures and fig 18.6 stay as they are).
//   node scripts/section-units.mjs <section-id> [--html=<part file>]
import fs from 'node:fs';

const ARGS = Object.fromEntries(process.argv.slice(3).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const SID = process.argv[2];
const ROOT = new URL('../', import.meta.url).pathname;
const EXC = JSON.parse(fs.readFileSync(`${ROOT}docs/pass-30-exceptions.json`, 'utf8'));
const FROZEN_CAPTIONS = new Set(EXC.caption_length.ids);   // the 18 kept originals and fig 18.6

let part = null, src = null;
for (const p of ['part-1', 'part-2', 'part-3', 'part-4', 'part-5']) {
  const s = ARGS.html && fs.readFileSync(ARGS.html, 'utf8').includes(`<section class="section" id="${SID}"`) ? fs.readFileSync(ARGS.html, 'utf8') : fs.readFileSync(`${ROOT}public/${p}.html`, 'utf8');
  if (s.includes(`<section class="section" id="${SID}"`)) { part = p; src = s; break; }
}
if (!part) { console.error(`no section ${SID}`); process.exit(1); }
const st = src.indexOf(`<section class="section" id="${SID}"`), en = src.indexOf('</section>', st);
const body = src.slice(st, en);
const text = h => h.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();

// figure spans, to tell a caption from prose
const figs = [...body.matchAll(/<div class="(?:diagram-card|light-diagram)[^"]*"[^>]*\bid="(fig-[^"]+)"/g)].map(m => {
  const s = m.index; let depth = 0, i = s, e = s;
  for (const t of body.slice(s).matchAll(/<(\/?)div\b[^>]*>/g)) { depth += t[1] ? -1 : 1; if (!depth) { e = s + t.index + t[0].length; break; } }
  return { id: m[1], s, e };
});
const units = [];
for (const m of body.matchAll(/<(p|li)\b([^>]*\bid="([^"]+)"[^>]*)>([\s\S]*?)<\/\1>/g)) {
  const [, tag, attrs, id, inner] = m;
  const cls = (attrs.match(/class="([^"]+)"/) || [])[1] || '';
  const fig = figs.find(f => m.index > f.s && m.index < f.e);
  const before = body.slice(Math.max(0, m.index - 200), m.index);
  const where = fig ? (cls.includes('diagram-caption') ? 'caption' : 'figure') : /class="pull-quote">\s*$/.test(before) ? 'pull-quote' : cls.includes('insight-text') ? 'insight' : tag === 'li' ? 'list' : 'prose';
  const locked = where === 'pull-quote' ? 'pull-quote: owner-chosen, verbatim'
    : where === 'figure' ? 'inside a figure: Pass 29 changes no SVG or figure text but captions'
    : where === 'caption' && FROZEN_CAPTIONS.has(fig.id) ? `caption of ${fig.id}: kept original or owner-authored, stays as it is` : null;
  units.push({ id, tag, class: cls, where, figure: fig ? fig.id : null, words: text(inner) ? text(inner).split(' ').length : 0, locked, text: text(inner), html: inner });
}
console.log(JSON.stringify({ part, section: SID, units }, null, 1));
