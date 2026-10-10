// The dash law (CLAUDE.md, owner 2026-10-10): no em dash anywhere a reader can
// see. Scans what ships, with comments removed: public/ (HTML text and
// attributes, inline scripts, JS and JSON strings, CSS) and functions/ (mail
// and page strings). Fails on any U+2014 or its HTML entities.
//   npm run check:dashes
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { transformSync } from 'esbuild';

const ROOT = new URL('..', import.meta.url).pathname;
const DASH = /\u2014|&mdash;|&#8212;|&#x2014;/gi;

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === 'node_modules' || name === 'fonts' || name.startsWith('.')) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}
// Comments are for maintainers; strings and markup are for readers.
const stripJs = (src, loader = 'js') => transformSync(src, { loader, minifyWhitespace: true, legalComments: 'none' }).code;
const stripCss = src => src.replace(/\/\*[\s\S]*?\*\//g, '');
function stripHtml(src) {
  return src
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/(<script\b[^>]*>)([\s\S]*?)(<\/script>)/gi, (m, a, body, z) => a + (/type="application\/(ld\+)?json"/.test(a) ? body : stripJs(body)) + z)
    .replace(/(<style\b[^>]*>)([\s\S]*?)(<\/style>)/gi, (m, a, body, z) => a + stripCss(body) + z);
}

const files = [...walk(join(ROOT, 'public')), ...walk(join(ROOT, 'functions'))];
let bad = 0;
for (const f of files) {
  let text;
  const src = readFileSync(f, 'utf8');
  if (/\.(html|svg)$/.test(f)) text = stripHtml(src);
  else if (/\.m?js$/.test(f)) text = stripJs(src);
  else if (/\.css$/.test(f)) text = stripCss(src);
  else if (/\.(json|txt|xml)$/.test(f)) text = src;
  else continue;
  for (const m of text.matchAll(DASH)) {
    bad++;
    const ctx = text.slice(Math.max(0, m.index - 60), m.index + 60).replace(/\s+/g, ' ');
    console.log(`${relative(ROOT, f)}: …${ctx}…`);
  }
}
if (bad) { console.error(`\n${bad} em dash${bad === 1 ? '' : 'es'} a reader can see. Rewrite the sentence (CLAUDE.md, the dash law).`); process.exit(1); }
console.log('check:dashes: clean');
