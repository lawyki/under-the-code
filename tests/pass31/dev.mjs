// Pass 31 gate development set (docs/pass-31-calibration.md). The gate builder's tuning runs, and nothing else:
//   npm run fig:dev -- [--runs=3] [--label=<attempt name>] [--only=v1,v2,v4,decoy1,decoy2,decoy3] [--criteria=...] [--jobs=3]
// Builds Fig 1.1 at three owner-judged commits into scratch public trees (each commit's own fig_1_1.py and
// figlib.py, run by scripts/figs/build_into.py against a copy of this worktree's public/), then runs
// tests/pass31/gate.mjs on each version --runs times. Pairwise is against the v1.0-rc2 tag; the first order
// alternates per run (candidate first, rc2 first, then random), and every run asks both orders.
//   v1 4392ca0  rejected (binary, jargon)          expected FAIL
//   v2 c18836c  rejected (unexplained state labels) expected FAIL
//   v4 2a9ece9  approved                            expected PASS
// v3 is sealed (brief section 6): it is not in this list and this script never reads it.
// Decoys (built here from the v4 tree, each run without pairwise, as validation runs; each must fail on its own):
//   decoy1  the mechanism written out as text beside a decorative moving dot            expected FAIL
//   decoy2  tape, head and marks, the head walks and writes, but no rule is drawn       expected FAIL
//   decoy3  v4 with the head labelled "head · adding" (v2's unexplained state label)    expected FAIL
// Output: tests/pass31/out/dev/<label>/summary.json and one line per run on stdout.
import fs from 'node:fs'; import path from 'node:path';
import { args, run, mkdirp, REPO, OUT, PUBLIC } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const SET = { v1: { rev: '4392ca0', expect: false }, v2: { rev: 'c18836c', expect: false }, v4: { rev: '2a9ece9', expect: true },
  decoy1: { from: 'v4', expect: false, decoy: true }, decoy2: { from: 'v4', expect: false, decoy: true }, decoy3: { from: 'v4', expect: false, decoy: true } };
// the decoys' pictures (test fixtures, never book figures): the svg of fig-1-1 is replaced, or (decoy3) one label changed
const F = 'font-family="IBM Plex Mono" fill="#e8e6e0"';
const SVG = body => `<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" role="img">\n${body}\n</svg>`;
const DECOY = {
  decoy1: svg => SVG(`<rect x="0" y="0" width="400" height="300" fill="#141414"/>
<circle cx="40" cy="40" r="10" fill="#d4a853"><animate attributeName="cx" values="40;360;40" dur="6s" repeatCount="indefinite"/></circle>
<text x="20" y="90" ${F} font-size="14">THE MACHINE</text>
<text x="20" y="130" ${F} font-size="13">On a mark: move right</text>
<text x="20" y="165" ${F} font-size="13">On an empty cell: write a mark, stop</text>
<text x="20" y="205" ${F} font-size="13">Start: 3 marks</text>
<text x="20" y="235" ${F} font-size="13">End: 4 marks</text>
<text x="20" y="275" ${F} font-size="16" fill="#d4a853">3 + 1 = 4</text>`),
  decoy2: svg => SVG(`<rect x="0" y="0" width="400" height="300" fill="#141414"/>
${Array.from({ length: 6 }, (_, i) => `<rect x="${20 + 55 * i}" y="80" width="50" height="50" rx="3" fill="none" stroke="rgba(255,255,255,0.5)"/>`).join('')}${Array.from({ length: 3 }, (_, i) => `<line x1="${45 + 55 * i}" y1="92" x2="${45 + 55 * i}" y2="118" stroke="#e8e6e0" stroke-width="4"/>`).join('')}
<line x1="210" y1="92" x2="210" y2="118" stroke="#d4a853" stroke-width="4" opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.64;0.65;1" dur="6s" repeatCount="indefinite"/></line>
<rect x="17" y="77" width="56" height="56" rx="4" fill="none" stroke="#d4a853" stroke-width="2"><animate attributeName="x" values="17;17;72;127;182;182" keyTimes="0;0.1;0.25;0.4;0.55;1" dur="6s" repeatCount="indefinite"/></rect>
<text x="20" y="165" ${F} font-size="13">TAPE</text>
<text x="20" y="190" ${F} font-size="13" fill="#d4a853">HEAD</text>
<text x="20" y="270" ${F} font-size="16" fill="#d4a853">3 + 1 = 4</text>`),
  decoy3: svg => { const t = svg.replace(/(<text\b[^>]*>)head(<\/text>)/, '$1head · adding$2'); if (t === svg) throw new Error('decoy3: no "head" label in v4'); return t; },
};
export const INTENT_1_1 = "A Turing machine's head reads one tape cell at a time and follows two rules: on a mark, move right; on an empty cell, write a mark and stop. Starting from three tally marks it walks past them and writes a fourth, so these two rules alone compute 3 + 1 = 4.";
const RUNS = +(o.runs || 3), JOBS = +(o.jobs || 3);
const LABEL = o.label || new Date().toISOString().replace(/[:.]/g, '-');
const DIR = mkdirp(path.join(OUT, 'dev', LABEL));
const ONLY = o.only ? String(o.only).split(',') : Object.keys(SET);

for (const v of [...ONLY].sort((a, b) => !!SET[a].from - !!SET[b].from)) {
  const d = path.join(OUT, 'dev', 'trees', v), src = mkdirp(path.join(d, 'src'));
  if (SET[v].from) {   // a decoy: the v4 tree with fig-1-1's svg replaced (rebuilt every run: cheap, and never stale)
    const base = path.join(OUT, 'dev', 'trees', SET[v].from, 'public');
    if (!fs.existsSync(path.join(base, 'part-1.html'))) throw new Error(`${v}: build ${SET[v].from} first (--only=${SET[v].from},${v})`);
    fs.rmSync(path.join(d, 'public'), { recursive: true, force: true }); fs.cpSync(base, path.join(d, 'public'), { recursive: true });
    const p = path.join(d, 'public', 'part-1.html'), h = fs.readFileSync(p, 'utf8');
    const i = h.indexOf('id="fig-1-1"'), a = h.indexOf('<svg', i), b = h.indexOf('</svg>', a) + 6;
    fs.writeFileSync(p, h.slice(0, a) + DECOY[v](h.slice(a, b)) + h.slice(b));
    continue;
  }
  if (!fs.existsSync(path.join(d, 'public', 'part-1.html'))) {
    fs.cpSync(PUBLIC, path.join(d, 'public'), { recursive: true });
    for (const f of ['fig_1_1.py', 'figlib.py']) {
      const r = await run('git', ['show', `${SET[v].rev}:scripts/figs/${f}`]);
      if (r.code) throw new Error(`git show ${SET[v].rev}:${f}: ${r.err}`);
      fs.writeFileSync(path.join(src, f), r.out);
    }
    const b = await run('python3', [path.join(REPO, 'scripts/figs/build_into.py'), path.join(d, 'public'), path.join(src, 'fig_1_1.py')]);
    if (b.code) throw new Error(`build ${v}: ${b.err}`);
  }
}
const tasks = [];
for (let k = 1; k <= RUNS; k++) for (const v of ONLY) tasks.push({ v, k, order: k === 1 ? 'cand-first' : k === 2 ? 'rc2-first' : 'random' });
const results = [];
async function one(t) {
  const out = path.join(DIR, `${t.v}-run${t.k}`);
  const argv = [path.join(REPO, 'tests/pass31/gate.mjs'), 'fig-1-1', `--intent=${INTENT_1_1}`, '--job=function',
    `--tree=${path.join(OUT, 'dev', 'trees', t.v, 'public')}`, `--order=${t.order}`, `--label=${LABEL}-${t.v}-run${t.k}`, `--out=${out}`];
  if (SET[t.v].decoy) argv.push('--no-pairwise');
  if (o.criteria) argv.push(`--criteria=${o.criteria}`);
  const r = await run('node', argv);
  let V = null; try { V = JSON.parse(fs.readFileSync(path.join(out, 'verdict.json'), 'utf8')); } catch {}
  const row = { v: t.v, run: t.k, order: SET[t.v].decoy ? 'no pairwise' : t.order, expect: SET[t.v].expect ? 'PASS' : 'FAIL', got: !V || V.failed === 'error' ? 'ERROR' : V.pass ? 'PASS' : 'FAIL',
    hedge_in: V && V.criteria.hedge ? V.criteria.hedge.failed_in : null,
    failed: V ? V.failed : null, failed_all: V ? V.failed_all : null,
    single_failed: V ? V.failed_all.filter(c => c !== 'pairwise') : null,
    pairwise: V && V.criteria.pairwise ? (V.criteria.pairwise.replies || []).map(x => `${x.order}: ${x.verdict}`) : null, dir: out };
  row.correct = row.got === row.expect;
  results.push(row);
  console.log(JSON.stringify(row));
  if (!V) console.error(r.out.slice(-800), r.err.slice(-800));
}
const queue = [...tasks];
await Promise.all(Array.from({ length: JOBS }, async () => { while (queue.length) await one(queue.shift()); }));
results.sort((a, b) => a.v.localeCompare(b.v) || a.run - b.run);
const core = results.filter(r => !SET[r.v].decoy), dec = results.filter(r => SET[r.v].decoy);
const correct = core.filter(r => r.correct).length, dcorrect = dec.filter(r => r.correct).length;
// without pairwise (as the sealed validation runs): would v1 and v2 still fail on their single-figure criteria alone?
const single = core.filter(r => r.single_failed).map(r => ({ v: r.v, run: r.run, got: r.single_failed.length ? 'FAIL' : 'PASS' }));
let hash = null; try { hash = JSON.parse(fs.readFileSync(path.join(core[0]?.dir || dec[0].dir, 'verdict.json'), 'utf8')).fingerprint; } catch {}
fs.writeFileSync(path.join(DIR, 'summary.json'), JSON.stringify({ label: LABEL, correct, of: core.length, decoys_correct: dcorrect, decoys_of: dec.length, single_criteria: single, fingerprint: hash, results }, null, 1));
console.log(`fig:dev ${LABEL}: ${correct} of ${core.length} correct (v1, v2, v4); decoys ${dcorrect} of ${dec.length} correct -> ${path.join(DIR, 'summary.json')}`);
