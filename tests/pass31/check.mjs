// Pass 31 mechanical figure check (docs/pass-31-brief.md sections 7, 11, 15). Per part, per figure:
//   gate1    Gate 1 as in Pass 30: tests/pass28/figs.mjs (default run and --motion run, each --fullscreen), clip.mjs and
//            smooth.mjs on the part's page; findings are the tools' own (exit code and summary line)
//   cap      label cap: role-tagged label text at most 8 per panel. Object text is free only when tagged
//            data-role="object", inside a <g data-obj="1"> that also holds a shape, and at most 6 characters; any other
//            <text> (untagged included) counts as a label. A panel is a <g data-panel> group; without one the figure is one
//            panel; more than two panels count as one. Object text must be a direct child of its obj group, beside a
//            shape, with at most two texts in the group. Legend entries (data-role="legend") at most two per panel. At-bar and kept figures are exempt (docs/pass-31-exempt.json)
// Exemptions (docs/pass-31-exempt.json) exist only where the brief grants them (sections 10, 13, 15): the label cap for
// at-bar and kept figures, the floor and the caption check for kept figures, and the caption check for the owner's
// closing claim (fig-18-6). No other check takes an exemption, taught-yet least of all (a false flag is fixed in the
// checker, never by exempting a figure: calibration section 17); the file holding any other key, or a non-empty id list
// under any other check, is a refusal (exit 2).
//   gate1    (per figure) the figure's own figs.mjs rows, still and motion runs: overlap, outside, spill, caption words,
//            text and named-mark contrast; a failing row fails the figure (the part lines still carry each tool's summary)
//   floor    no label below 11 CSS px from 360 px up (figs.mjs measures it)
//   taught   every label and object token is a number or sign, a term taught before the figure, or an everyday word
//            (tests/pass31/lib.mjs taughtYet; the known terms come from scripts/known-terms.mjs run with --out,
//            --public on the tree checked and --strip, the held material out: calibration section 16)
//   band     at t=0, no empty band taller than a quarter of the plate (tests/pass31/band.py on a bare.mjs still, 375 px)
//   desc     <desc> present and not empty
//   caption  at most two sentences
//   strip    the How-it-works strip at most 150 words
//   dashes   check:dashes (the repo tree) or the same scan of the part (another tree)
//   anchors  the part's anchor ids (book.js candidates(): ch…, fig-N-M, outside svgs) unchanged against --base, or
//            every missing id aliased in ANCHOR_ALIASES; an added id is a finding too
//   npm run fig:check -- <part-1|1> [--fig=fig-1-1,fig-1-2] [--tree=<public dir>] [--base=main] [--gate1=full|quick|off]
//                        [--json=<file>] [--browser=chromium|webkit]
// Output: one line per figure (PASS, or FAIL with the failed checks), the part checks, and tests/pass31/out/check/<part>/check.json.
import fs from 'node:fs'; import path from 'node:path';
import { args, tree, readPart, figures, plain, capCount, LABELS, LEGEND, MAX_PANELS, sentences, runKnownTerms, taughtContext, taughtYet, svgTexts, run, mkdirp, framesIn, REPO, OUT, PUBLIC } from './lib.mjs';

const { pos, o } = args(process.argv.slice(2));
const part = pos[0] ? (/^\d$/.test(pos[0]) ? `part-${pos[0]}` : pos[0]) : null;
if (!part || !/^part-[1-5]$/.test(part)) { console.log('usage: npm run fig:check -- <part-1..5> [--fig=ids] [--tree=dir] [--base=main] [--gate1=full|quick|off] [--json=file]'); process.exit(2); }
const ROOT = tree(o.tree), IS_REPO = path.resolve(ROOT) === path.resolve(PUBLIC);
const BASE = o.base || 'main', G1 = o.gate1 || 'full', ENG = o.browser || 'chromium';
const OUTDIR = mkdirp(path.join(OUT, 'check', part));
const EX = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/pass-31-exempt.json'), 'utf8'));
const EXEMPTABLE = ['label_cap', 'floor', 'caption'];
{ const other = Object.keys(EX).filter(k => !['note', 'at_bar', 'kept', ...EXEMPTABLE].includes(k));
  if (other.length) { console.log(`check: docs/pass-31-exempt.json has ${other.join(', ')}: only ${EXEMPTABLE.join(', ')} take exemptions (calibration section 17)`); process.exit(2); } }
const exempt = (check, id) => {
  if (!EXEMPTABLE.includes(check)) return false;
  const ids = new Set([...(EX[check]?.ids || []), ...EX.kept, ...(check === 'label_cap' ? EX.at_bar : [])]);
  return ids.has(id);
};
const html = readPart(ROOT, part);
let figs = figures(html, part);
const ONLY = o.fig ? String(o.fig).split(',') : null;
if (ONLY) { const miss = ONLY.filter(id => !figs.some(f => f.id === id)); if (miss.length) { console.log(`check: not in ${part}: ${miss.join(' ')}`); process.exit(2); } figs = figs.filter(f => ONLY.includes(f.id)); }
const R = new Map(figs.map(f => [f.id, { id: f.id, checks: {} }]));
const put = (id, check, pass, detail, skipped = false) => { R.get(id).checks[check] = { pass: skipped ? true : pass, ...(skipped ? { skipped: true, wouldPass: pass } : {}), detail }; };

// ---- per-figure static checks ---------------------------------------------------------------------------------
const KT_FILE = path.join(OUTDIR, 'known-terms.json');
let kt; try { kt = await runKnownTerms(ROOT, KT_FILE); } catch (e) { console.log('check:', e.message); process.exit(2); }
for (const f of figs) {
  const c = capCount(f.svg);
  put(f.id, 'cap', c.max <= LABELS && c.maxLegend <= LEGEND, `labels per panel ${JSON.stringify(c.panels)}${c.merged ? ` (${c.panelCount} panels, more than ${MAX_PANELS}: counted as one)` : ''}; legend entries ${JSON.stringify(c.legends)}; free object text ${c.rows.filter(r => r.free).length}`, exempt('label_cap', f.id));
  R.get(f.id).labels = c.rows;
  const tc = taughtContext(kt, ROOT, f);
  if (!tc) put(f.id, 'taught', false, `section ${f.section} not in known-terms`);
  else { const bad = svgTexts(f.svg).flatMap(t => taughtYet(t.s, tc.known, kt.glossary, tc.prior).map(b => `${b.token} (${b.why})`));
    put(f.id, 'taught', bad.length === 0, bad.length ? [...new Set(bad)].join('; ') : 'every token taught or everyday'); }
  put(f.id, 'desc', !!(f.desc && plain(f.desc)), f.desc ? `${plain(f.desc).split(/\s+/).length} words` : 'no <desc>');
  const n = sentences(f.caption).length;
  put(f.id, 'caption', n <= 2, `${n} sentence${n === 1 ? '' : 's'}`, exempt('caption', f.id));
  const w = f.how.join(' ').split(/\s+/).filter(Boolean).length;
  put(f.id, 'strip', w <= 150, `${w} words`);
}

// ---- t=0 empty band (stills at 375) ---------------------------------------------------------------------------
{
  const dir = path.join(OUTDIR, 'stills'); fs.rmSync(dir, { recursive: true, force: true }); mkdirp(dir);
  await run('node', [path.join(REPO, 'tests/pass30/bare.mjs'), `--page=${part}`, `--id=${figs.map(f => f.id).join(',')}`, `--out=${dir}`, '--times=0', '--width=375', `--browser=${ENG}`], { env: { FIG_ROOT: ROOT } });
  const files = figs.map(f => [f.id, framesIn(dir, f.id).find(x => x.t === 0)]);
  const r = await run('python3', [path.join(REPO, 'tests/pass31/band.py'), ...files.filter(x => x[1]).map(x => x[1].f)]);
  const by = new Map(r.out.trim().split('\n').filter(Boolean).map(l => JSON.parse(l)).map(j => [j.file, j]));
  for (const [id, fr] of files) {
    if (!fr) { put(id, 'band', false, 'no t=0 still rendered'); continue; }
    const j = by.get(fr.f); put(id, 'band', j.frac <= 0.25, `tallest empty band ${Math.round(j.frac * 100)}% of the plate (${j.band}/${j.h} px at y ${j.at})`);
  }
}

// ---- Gate 1 and the floor -------------------------------------------------------------------------------------
const gate1 = [];
const figArg = ONLY ? [`--fig=${ONLY.join(',')}`] : [];
const quick = G1 === 'quick' ? ['--widths=360,375', `--browser=${ENG}`] : [];
async function tool(name, file, argv) {
  const json = path.join(OUTDIR, `${name}.json`);
  const r = await run('node', [path.join(REPO, 'tests/pass28', file), ...argv, `--json=${json}`], { env: { FIG_ROOT: ROOT } });
  const sum = r.out.split('\n').filter(l => /^(figs|clip|smooth):/.test(l)).join(' ');
  gate1.push({ name, pass: r.code === 0, summary: sum || r.err.slice(-300) });
  try { return JSON.parse(fs.readFileSync(json, 'utf8')); } catch { return null; }
}
let floorRows = null, motionRows = null;
if (G1 !== 'off') {
  floorRows = await tool('figs', 'figs.mjs', [`--part=${part}`, ...figArg, '--fullscreen', ...quick]);
  motionRows = await tool('figs-motion', 'figs.mjs', [`--part=${part}`, ...figArg, '--motion', '--fullscreen', ...quick]);
  await tool('clip', 'clip.mjs', [`--pages=${part}`, ...(G1 === 'quick' ? ['--widths=375', `--browser=${ENG}`] : [])]);
  await tool('smooth', 'smooth.mjs', [`--pages=${part}`, ...(G1 === 'quick' ? ['--widths=375'] : [])]);
} else {
  const json = path.join(OUTDIR, 'floor.json');
  await run('node', [path.join(REPO, 'tests/pass28/figs.mjs'), `--part=${part}`, ...figArg, '--widths=360,375', `--browser=${ENG}`, '--no-contrast', `--json=${json}`], { env: { FIG_ROOT: ROOT } });
  try { floorRows = JSON.parse(fs.readFileSync(json, 'utf8')); } catch {}
}
for (const f of figs) {
  const rows = (floorRows || []).filter(r => r.id === f.id && r.w >= 360 && r.minPx != null);
  if (!rows.length) { put(f.id, 'floor', false, 'not measured'); continue; }
  const min = Math.min(...rows.map(r => r.minPx));
  put(f.id, 'floor', min >= 11, `smallest label ${min} CSS px from 360 px up`, exempt('floor', f.id));
}

// ---- Gate 1 rows, attributed to their figure: the findings figs.mjs counts (its why(), restated here because figs.mjs
// is a script, not a module; keep the two in step). The floor has its own check above, so it is left out here.
if (G1 !== 'off') {
  let EXC = {}; try { EXC = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/pass-30-exceptions.json'), 'utf8')); } catch {}
  const CAP_X = new Set(EXC.caption_length?.ids || []);
  const why = r => {
    if (r.rendered === false || r.kind !== 'fig') return [];
    const w = [];
    if (!r.geomSkip) {
      if (r.overlaps?.length) w.push('overlap'); if (r.outside?.length) w.push('outside'); if (r.spill?.length) w.push('spill');
      if (!CAP_X.has(r.id) && r.capWords > 60) w.push('caption-words');
    }
    const c = r.contrast;
    if (c) { if (c.error || c.texts.some(x => x.r == null || x.r < 4.5)) w.push('text-contrast'); if (!c.error && c.marks.some(m => m.named && m.r < 3)) w.push('mark-contrast'); }
    return w;
  };
  for (const f of figs) {
    const rows = [...(floorRows || []).filter(r => r.id === f.id).map(r => ['still', r]), ...(motionRows || []).filter(r => r.id === f.id).map(r => ['motion', r])];
    if (!rows.length) { put(f.id, 'gate1', false, 'no Gate 1 rows for this figure (figs.mjs did not measure it)'); continue; }
    const tally = {}; let bad = 0;
    for (const [k, r] of rows) { const w = why(r); if (w.length) bad++; for (const x of w) tally[`${k} ${x}`] = (tally[`${k} ${x}`] || 0) + 1; }
    put(f.id, 'gate1', bad === 0, bad ? `${bad} of ${rows.length} rows fail: ${Object.entries(tally).map(([k, n]) => `${k} ${n}`).join(', ')}` : `${rows.length} rows clean`);
  }
}

// ---- part checks: dashes, anchors -----------------------------------------------------------------------------
const partChecks = {};
{
  if (IS_REPO) { const r = await run('node', [path.join(REPO, 'scripts/check-dashes.mjs')]); partChecks.dashes = { pass: r.code === 0, detail: (r.out + r.err).trim().split('\n').slice(-3).join(' ') }; }
  else { const t = html.replace(/<!--[\s\S]*?-->/g, ''); const n = (t.match(/—|&mdash;|&#8212;|&#x2014;/gi) || []).length; partChecks.dashes = { pass: n === 0, detail: `${n} em dash${n === 1 ? '' : 'es'} in ${part}.html (tree scan)` }; }
}
{
  const ids = h => [...h.replace(/<svg[\s\S]*?<\/svg>/g, '').matchAll(/\bid="([^"]+)"/g)].map(m => m[1]).filter(id => /^(ch[0-9B][^ ]*|fig-[0-9]+-[0-9]+[a-z]?)$/.test(id));
  const r = await run('git', ['show', `${BASE}:public/${part}.html`]);
  if (r.code) partChecks.anchors = { pass: false, detail: `cannot read ${BASE}:public/${part}.html` };
  else {
    const was = ids(r.out), now = ids(html), nowS = new Set(now), wasS = new Set(was);
    const bookJs = fs.readFileSync(path.join(ROOT, 'book.js'), 'utf8');
    const al = new Set([...(bookJs.match(/const ANCHOR_ALIASES = \{([\s\S]*?)\};/) || [, ''])[1].matchAll(/'([^']+)'\s*:/g)].map(m => m[1]));
    const missing = was.filter(id => !nowS.has(id)), unaliased = missing.filter(id => !al.has(id)), added = now.filter(id => !wasS.has(id));
    const order = missing.length === 0 && added.length === 0 && was.join() !== now.join();
    partChecks.anchors = { pass: unaliased.length === 0 && added.length === 0 && !order, detail: `${now.length} anchors against ${BASE} (${was.length}); missing ${missing.length} (unaliased ${unaliased.join(' ') || 'none'}); added ${added.join(' ') || 'none'}${order ? '; order changed' : ''}` };
  }
}
for (const g of gate1) partChecks['gate1:' + g.name] = { pass: g.pass, detail: g.summary };

// ---- report ---------------------------------------------------------------------------------------------------
const rows = [...R.values()];
for (const r of rows) {
  const failed = Object.entries(r.checks).filter(([, c]) => !c.pass).map(([k]) => k);
  const skips = Object.entries(r.checks).filter(([, c]) => c.skipped).map(([k, c]) => `${k}${c.wouldPass ? '' : '!'}`);
  r.pass = failed.length === 0;
  console.log(`${r.pass ? 'PASS' : 'FAIL'} ${r.id}${failed.length ? '  ' + failed.map(k => `${k}: ${r.checks[k].detail}`).join(' | ') : ''}${skips.length ? `  (exempt: ${skips.join(' ')})` : ''}`);
}
for (const [k, c] of Object.entries(partChecks)) console.log(`${c.pass ? 'PASS' : 'FAIL'} ${part} ${k}: ${c.detail}`);
const nFail = rows.filter(r => !r.pass).length, pFail = Object.values(partChecks).filter(c => !c.pass).length;
const report = { part, tree: ROOT, base: BASE, gate1: G1, figures: rows, part_checks: partChecks, failed_figures: nFail, failed_part_checks: pFail };
fs.writeFileSync(o.json ? path.resolve(o.json) : path.join(OUTDIR, 'check.json'), JSON.stringify(report, null, 1));
console.log(`fig:check ${part}: ${rows.length - nFail}/${rows.length} figures clean, ${Object.keys(partChecks).length - pFail}/${Object.keys(partChecks).length} part checks clean (gate1 ${G1})`);
process.exit(nFail || pFail ? 1 : 0);
