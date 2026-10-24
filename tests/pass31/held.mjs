// Pass 31 held material (docs/pass-31-calibration.md section 16): the strip list in tests/pass31/held-strip.json,
// applied to a part's HTML before anything reads it as prose. Used by lib.mjs (the judge packet, the prose tokens
// taught-yet credits, the section text before a card) and by scripts/known-terms.mjs --strip (known, defines,
// abbreviations), so a term whose only teaching sits in held material is never credited.
// stripHeld() blanks (spaces, newlines kept), never deletes, so every offset into the part stays valid:
//   - each held figure's card, whole (label, picture, caption, How-it-works strip);
//   - each listed chapter, section and paragraph element, from its start tag to its matching end tag (nesting of the
//     same tag counted);
//   - a part opener's toc card (<a class="toc-card">) that links to a stripped chapter or section.
import fs from 'node:fs'; import crypto from 'node:crypto';

export const HELD_FILE = new URL('./held-strip.json', import.meta.url).pathname;
// a figure card: <div class="diagram-card|light-diagram ..." id="fig-..."> label, svg, caption, optional strip </div>
export const CARD = /<div class="(?:diagram-card|light-diagram)[^"]*" id="([^"]+)">[\s\S]*?<\/svg>\s*<p\b[^>]*class="diagram-caption"[^>]*>[\s\S]*?<\/p>\s*(?:<details class="fig-how">[\s\S]*?<\/details>\s*)?<\/div>/g;

const cache = new Map();
export function loadHeld(file = HELD_FILE) {
  if (cache.has(file)) return cache.get(file);
  const buf = fs.readFileSync(file), j = JSON.parse(buf.toString('utf8'));
  const need = ['held_figures', 'chapters', 'sections', 'paragraphs'];
  const miss = need.filter(k => !j[k]); if (miss.length) throw new Error(`${file}: no ${miss.join(', ')}`);
  const sections = [...new Set([...(j.sections.named || []), ...(j.sections.held_only || [])])];
  const H = { file, sha256: crypto.createHash('sha256').update(buf).digest('hex'), figures: new Set(j.held_figures), chapters: j.chapters, sections, paragraphs: j.paragraphs,
    targets: new Set([...j.chapters, ...sections]), elements: [...j.chapters, ...sections, ...j.paragraphs] };
  cache.set(file, H);
  return H;
}
const esc = t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export const blank = s => s.replace(/[^\n]/g, ' ');
// the end (exclusive) of the element whose start tag begins at `at`: its matching end tag, nesting of the same tag counted
export function elementEnd(html, at, tag) {
  const re = new RegExp(`<(/?)${esc(tag)}\\b[^>]*?(/?)>`, 'gi'); re.lastIndex = at;
  let depth = 0;
  for (let m; (m = re.exec(html));) {
    if (m[1]) { depth--; if (depth === 0) return m.index + m[0].length; }
    else if (!m[2]) depth++;
    else if (depth === 0) return m.index + m[0].length;   // self-closing at the start
  }
  return html.length;
}
// the zones of held material in one part's HTML: [start, end, kind, id]
export function heldZones(html, H = loadHeld()) {
  const zones = [];
  for (const id of H.elements) {
    const re = new RegExp(`<([a-zA-Z][\\w-]*)\\b[^>]*\\bid="${esc(id)}"[^>]*>`, 'g');
    for (const m of html.matchAll(re)) zones.push([m.index, elementEnd(html, m.index, m[1]), H.paragraphs.includes(id) ? 'paragraph' : H.chapters.includes(id) ? 'chapter' : 'section', id]);
  }
  for (const m of html.matchAll(CARD)) if (H.figures.has(m[1])) zones.push([m.index, m.index + m[0].length, 'figure', m[1]]);
  for (const m of html.matchAll(/<a\b[^>]*\bclass="toc-card"[^>]*>/g)) {
    const t = (m[0].match(/\bhref="[^"#]*#([^"]+)"/) || [])[1];
    if (t && H.targets.has(t)) zones.push([m.index, elementEnd(html, m.index, 'a'), 'toc-card', t]);
  }
  return zones.sort((a, b) => a[0] - b[0]);
}
export function stripHeld(html, H = loadHeld()) {
  const zones = heldZones(html, H);
  if (!zones.length) return { html, zones };
  let out = '', at = 0;
  for (const [s, e] of zones) { if (e <= at) continue; const s1 = Math.max(s, at); out += html.slice(at, s1) + blank(html.slice(s1, e)); at = e; }
  return { html: out + html.slice(at), zones };
}
export const inZone = (zones, i) => zones.some(([s, e]) => i >= s && i < e);
