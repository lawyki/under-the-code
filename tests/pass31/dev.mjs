// Pass 31 gate development set (docs/pass-31-calibration.md). The gate builder's tuning runs, and nothing else:
//   npm run fig:dev -- [--runs=3] [--label=<attempt name>] [--only=v1,v2,v4] [--criteria=...] [--jobs=3]
// Builds Fig 1.1 at three owner-judged commits into scratch public trees (each commit's own fig_1_1.py and
// figlib.py, run by scripts/figs/build_into.py against a copy of this worktree's public/), then runs
// tests/pass31/gate.mjs on each version --runs times. Pairwise is against the v1.0-rc2 tag; the first order
// alternates per run (candidate first, rc2 first, then random), and every run asks both orders.
//   v1 4392ca0  rejected (binary, jargon)          expected FAIL
//   v2 c18836c  rejected (unexplained state labels) expected FAIL
//   v4 2a9ece9  approved                            expected PASS
// v3 is sealed (brief section 6): it is not in this list and this script never reads it.
// Output: tests/pass31/out/dev/<label>/summary.json and one line per run on stdout.
import fs from 'node:fs'; import path from 'node:path';
import { args, run, mkdirp, REPO, OUT, PUBLIC } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const SET = { v1: { rev: '4392ca0', expect: false }, v2: { rev: 'c18836c', expect: false }, v4: { rev: '2a9ece9', expect: true } };
export const INTENT_1_1 = "A Turing machine's head reads one tape cell at a time and follows two rules: on a mark, move right; on an empty cell, write a mark and stop. Starting from three tally marks it walks past them and writes a fourth, so these two rules alone compute 3 + 1 = 4.";
const RUNS = +(o.runs || 3), JOBS = +(o.jobs || 3);
const LABEL = o.label || new Date().toISOString().replace(/[:.]/g, '-');
const DIR = mkdirp(path.join(OUT, 'dev', LABEL));
const ONLY = o.only ? String(o.only).split(',') : Object.keys(SET);

for (const v of ONLY) {
  const d = path.join(OUT, 'dev', 'trees', v), src = mkdirp(path.join(d, 'src'));
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
  if (o.criteria) argv.push(`--criteria=${o.criteria}`);
  const r = await run('node', argv);
  let V = null; try { V = JSON.parse(fs.readFileSync(path.join(out, 'verdict.json'), 'utf8')); } catch {}
  const row = { v: t.v, run: t.k, order: t.order, expect: SET[t.v].expect ? 'PASS' : 'FAIL', got: V ? (V.pass ? 'PASS' : 'FAIL') : 'ERROR',
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
const correct = results.filter(r => r.correct).length;
fs.writeFileSync(path.join(DIR, 'summary.json'), JSON.stringify({ label: LABEL, correct, of: results.length, results }, null, 1));
console.log(`fig:dev ${LABEL}: ${correct} of ${results.length} correct -> ${path.join(DIR, 'summary.json')}`);
