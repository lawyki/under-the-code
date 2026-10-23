// Pass 31 contact sheets (docs/pass-31-brief.md section 7): one PNG per chapter, every figure at 375 px at t=0 (the
// reduced-motion still), with Fig 1.1 (v4) and Fig 1.2 (Enigma) pinned first on every sheet as the two references.
//   npm run fig:sheet [-- --chapter=ch1[,ch4]] [--tree=<public dir>] [--pin-tree=<public dir>] [--out=<dir>] [--cols=4]
//                      [--browser=chromium|webkit]
// --tree      where the chapter figures come from (default public/); a scratch tree shows candidates.
// --pin-tree  where the pinned references come from (default public/, the approved v4 and Enigma).
// Output: tests/pass31/out/sheets/<chapter>.png (gitignored). Stills are rendered by tests/pass30/bare.mjs (the svg
// alone; label, caption and strip are never painted); each cell is labelled with its figure id under the picture.
import fs from 'node:fs'; import path from 'node:path';
import { args, tree, allFigures, PUBLIC, OUT, REPO, run, mkdirp, framesIn } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const ROOT = tree(o.tree), PIN_ROOT = tree(o['pin-tree']);
const OUTDIR = mkdirp(path.resolve(o.out || path.join(OUT, 'sheets')));
const SHOTS = mkdirp(path.join(OUTDIR, '.stills'));
const ENG = o.browser || 'chromium', COLS = String(o.cols || 4);
const PINS = ['fig-1-1', 'fig-1-2'];
const figs = allFigures(ROOT);
const chapters = [...new Set(figs.map(f => f.chapter))];
const want = o.chapter ? String(o.chapter).split(',') : chapters;
const bad = want.filter(c => !chapters.includes(c));
if (bad.length) { console.log(`sheet: no such chapter ${bad.join(', ')} (have ${chapters.join(' ')})`); process.exit(2); }

async function stills(root, dir, byPart) {
  for (const [part, ids] of byPart) {
    const r = await run('node', [path.join(REPO, 'tests/pass30/bare.mjs'), `--page=${part}`, `--id=${ids.join(',')}`, `--out=${dir}`, '--times=0', '--width=375', `--browser=${ENG}`],
      { env: { FIG_ROOT: root } });
    if (r.code) { console.log(r.out.split('\n').filter(l => /MISS|DRIFT|COLLIDE/.test(l)).join('\n') || r.err.slice(-800)); }
  }
}
// the pinned references, from their own tree, in their own folder (bare.mjs refuses to mix owners in one folder)
const pinDir = mkdirp(path.join(SHOTS, 'pins'));
await stills(PIN_ROOT, pinDir, [['part-1', PINS]]);
const chDir = mkdirp(path.join(SHOTS, 'tree'));
const sel = figs.filter(f => want.includes(f.chapter));
const byPart = new Map(); for (const f of sel) byPart.set(f.part, [...(byPart.get(f.part) || []), f.id]);
await stills(ROOT, chDir, byPart);

let made = 0;
for (const ch of want) {
  const list = sel.filter(f => f.chapter === ch);
  const cells = [], labels = [];
  for (const id of PINS) { const fr = framesIn(pinDir, id)[0]; if (fr) { cells.push(fr.f); labels.push(`${id} (pinned)`); } }
  for (const f of list) { const fr = framesIn(chDir, f.id).find(x => x.t === 0); if (fr) { cells.push(fr.f); labels.push(f.id); } else labels.push(null), console.log(`sheet: no still for ${f.id}`); }
  const out = path.join(OUTDIR, `${ch}.png`);
  const r = await run('python3', [path.join(REPO, 'tests/pass31/strip.py'), out, `--cols=${COLS}`, '--width=375', `--labels=${labels.filter(Boolean).join('|')}`,
    `--title=${ch} · ${list.length} figures · 375 px · t=0 · first two pinned (Fig 1.1 v4, Fig 1.2 Enigma)`, ...cells]);
  if (r.code) { console.log(`sheet: ${ch} failed: ${r.err.slice(-600)}`); continue; }
  made++; console.log(`sheet ${ch}: ${list.length} figures + 2 pinned -> ${out}`);
}
console.log(`fig:sheet: ${made}/${want.length} sheets in ${OUTDIR}`);
process.exit(made === want.length ? 0 : 1);
