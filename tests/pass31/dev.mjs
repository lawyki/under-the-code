// Pass 31 gate development set (docs/pass-31-calibration.md). The gate builder's tuning runs, and nothing else:
//   npm run fig:dev -- [--runs=3] [--label=<attempt name>] [--only=v1,v2,v4,decoy1,decoy2,decoy3,enigma] [--criteria=...]
//                      [--jobs=3] [--ledger=<docs/pass-31-ledger.tsv>]
// Builds Fig 1.1 at three owner-judged commits into scratch public trees (each commit's own fig_1_1.py and
// figlib.py, run by scripts/figs/build_into.py against a copy of this worktree's public/), then runs
// tests/pass31/gate.mjs on each version --runs times. Each of those is one evaluation: one gate decision (at least
// two of three complete runs pass; docs/pass-31-calibration.md section 14), so --runs=3 makes 6 to 9 complete runs per
// item. Pairwise is against the v1.0-rc2 tag; the first order alternates per evaluation (candidate first, rc2 first,
// then random) and is passed to each of its runs, and every run asks both orders.
//   v1 4392ca0  rejected (binary, jargon)          expected FAIL
//   v2 c18836c  rejected (unexplained state labels) expected FAIL
//   v4 2a9ece9  approved                            expected PASS
// v3 is sealed (brief section 6): it is not in this list and this script never reads it.
// Decoys (built here from the v4 tree, each run without pairwise, as validation runs; each must fail on its own):
//   decoy1  the mechanism written out as text beside a decorative moving dot            expected FAIL
//   decoy2  tape, head and marks, the head walks and writes, but no rule is drawn       expected FAIL
//   decoy3  v4 with the head labelled "head · adding" (v2's unexplained state label)    expected FAIL
//   decoy4  Fig 1.2's takeaway drawn as a block schematic (boxes KEY, ROTORS, REFLECTOR, LAMP joined by arrows, a
//           stepping counter and a changing lamp letter), built from the Enigma tree: a schematic is never a real
//           thing (brief section 4, amended 2026-10-24), so under the job "real thing" it must fail  expected FAIL
// The must-pass (session e2): Fig 1.2 Enigma, praised by the owner, as it stands in this worktree's public/ (copied
// into a scratch tree), under its ledger job "real thing"                              expected PASS
// Every item's takeaway and job come from the ledger, read by header name (lib.mjs readLedger: columns "intent" and
// "job"); the ledger is copied into the attempt's folder and each gate run reads that copy, so a run is reproducible.
// Output: tests/pass31/out/dev/<label>/summary.json and one line per evaluation on stdout (each with its runs).
import fs from 'node:fs'; import path from 'node:path';
import { args, run, mkdirp, readLedger, ledgerTakeaway, LEDGER_DEFAULT, REPO, OUT, PUBLIC } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const SET = { v1: { id: 'fig-1-1', rev: '4392ca0', expect: false }, v2: { id: 'fig-1-1', rev: 'c18836c', expect: false }, v4: { id: 'fig-1-1', rev: '2a9ece9', expect: true },
  decoy1: { id: 'fig-1-1', from: 'v4', expect: false, decoy: true }, decoy2: { id: 'fig-1-1', from: 'v4', expect: false, decoy: true }, decoy3: { id: 'fig-1-1', from: 'v4', expect: false, decoy: true },
  enigma: { id: 'fig-1-2', copy: true, expect: true, must: true }, decoy4: { id: 'fig-1-2', from: 'enigma', expect: false, decoy: true } };
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
  decoy4: () => {   // three presses in a 6 s loop: the key box flashes, the counter steps 1, 2, 3, the lamp letter reads F, E, C
    const box = (x, y, w, label) => `<rect x="${x}" y="${y}" width="${w}" height="56" rx="6" fill="none" stroke="#e8e6e0" stroke-opacity="0.7"/><text x="${x + w / 2}" y="${y - 8}" text-anchor="middle" ${F} font-size="12">${label}</text>`;
    const step = (i, x, y, t) => `<text x="${x}" y="${y}" text-anchor="middle" ${F} font-size="20" fill="#d4a853" opacity="${i ? 0 : 1}"><animate attributeName="opacity" values="${[0, 1, 2].map(k => (k === i ? 1 : 0)).join(';')}" keyTimes="0;0.3333;0.6667" calcMode="discrete" dur="6s" repeatCount="indefinite"/>${t}</text>`;
    const arrow = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#e8e6e0" stroke-width="1.5"/><path d="M${x2} ${y2} l-7 -4 v8 z" fill="#e8e6e0" transform="rotate(${Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI} ${x2} ${y2})"/>`;
    return SVG(`<rect x="0" y="0" width="400" height="300" fill="#141414"/>
<text x="200" y="40" text-anchor="middle" ${F} font-size="13">PRESS A THREE TIMES</text>
${box(20, 110, 70, 'KEY')}<text x="55" y="146" text-anchor="middle" ${F} font-size="20">A</text>
<rect x="20" y="110" width="70" height="56" rx="6" fill="#d4a853" opacity="0"><animate attributeName="opacity" values="0;0.35;0;0;0.35;0;0;0.35;0;0" keyTimes="0;0.02;0.08;0.333;0.353;0.413;0.667;0.687;0.747;1" dur="6s" repeatCount="indefinite"/></rect>
${box(130, 110, 90, 'ROTORS')}${[0, 1, 2].map(i => step(i, 175, 146, String(i + 1))).join('')}
${box(260, 110, 110, 'REFLECTOR')}
${box(130, 210, 90, 'LAMP')}${[0, 1, 2].map(i => step(i, 175, 246, 'FEC'[i])).join('')}
${arrow(90, 138, 128, 138)}${arrow(220, 138, 258, 138)}${arrow(315, 166, 222, 228)}`);
  },
};
// the long Fig 1.1 intent the gate was tuned on up to try21 (docs/pass-31-calibration.md section 3), kept for the record
export const INTENT_1_1_TRY21 = "A Turing machine's head reads one tape cell at a time and follows two rules: on a mark, move right; on an empty cell, write a mark and stop. Starting from three tally marks it walks past them and writes a fourth, so these two rules alone compute 3 + 1 = 4.";
const RUNS = +(o.runs || 3), JOBS = +(o.jobs || 3);
const LABEL = o.label || new Date().toISOString().replace(/[:.]/g, '-');
const DIR = mkdirp(path.join(OUT, 'dev', LABEL));
const ONLY = o.only ? String(o.only).split(',') : Object.keys(SET);
// the ledger: read by header, copied into the attempt folder; every gate run reads the copy
const LEDGER_SRC = path.resolve(o.ledger || LEDGER_DEFAULT), LEDGER = path.join(DIR, 'ledger.tsv');
fs.copyFileSync(LEDGER_SRC, LEDGER);
const LG = readLedger(LEDGER), TAKE = Object.fromEntries([...new Set(ONLY.map(v => SET[v].id))].map(id => [id, ledgerTakeaway(LG, id)]));

for (const v of [...ONLY].sort((a, b) => !!SET[a].from - !!SET[b].from)) {
  const d = path.join(OUT, 'dev', 'trees', v), src = mkdirp(path.join(d, 'src'));
  if (SET[v].copy) {   // a figure as it stands: this worktree's public/ copied whole (rebuilt every run, never stale)
    fs.rmSync(path.join(d, 'public'), { recursive: true, force: true }); fs.cpSync(PUBLIC, path.join(d, 'public'), { recursive: true });
    continue;
  }
  if (SET[v].from) {   // a decoy: the v4 tree with fig-1-1's svg replaced (rebuilt every run: cheap, and never stale)
    const base = path.join(OUT, 'dev', 'trees', SET[v].from, 'public');
    if (!fs.existsSync(path.join(base, 'part-1.html'))) throw new Error(`${v}: build ${SET[v].from} first (--only=${SET[v].from},${v})`);
    fs.rmSync(path.join(d, 'public'), { recursive: true, force: true }); fs.cpSync(base, path.join(d, 'public'), { recursive: true });
    const p = path.join(d, 'public', 'part-1.html'), h = fs.readFileSync(p, 'utf8');
    const i = h.indexOf(`id="${SET[v].id}"`), a = h.indexOf('<svg', i), b = h.indexOf('</svg>', a) + 6;
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
  const out = path.join(DIR, `${t.v}-eval${t.k}`);
  const argv = [path.join(REPO, 'tests/pass31/gate.mjs'), SET[t.v].id, `--ledger=${LEDGER}`,
    `--tree=${path.join(OUT, 'dev', 'trees', t.v, 'public')}`, `--order=${t.order}`, `--label=${LABEL}-${t.v}-eval${t.k}`, `--out=${out}`];
  if (SET[t.v].decoy) argv.push('--no-pairwise');
  if (o.criteria) argv.push(`--criteria=${o.criteria}`);
  const r = await run('node', argv);
  let V = null; try { V = JSON.parse(fs.readFileSync(path.join(out, 'verdict.json'), 'utf8')); } catch {}
  const runs = V && V.runs ? V.runs.map(x => ({ k: x.k, got: x.error ? 'ERROR' : x.pass ? 'PASS' : 'FAIL', failed_all: x.failed_all, hedge_in: x.hedge_in, pairwise: x.pairwise,
    single_failed: x.failed_all ? x.failed_all.filter(c => c !== 'pairwise') : null })) : [];
  const row = { v: t.v, id: SET[t.v].id, run: t.k, order: SET[t.v].decoy ? 'no pairwise' : t.order, expect: SET[t.v].expect ? 'PASS' : 'FAIL', got: !V || V.failed === 'error' ? 'ERROR' : V.pass ? 'PASS' : 'FAIL',
    failed: V ? V.failed : null, failed_all: V ? V.failed_all : null, runs_passed: V ? V.runs_passed : null, runs_made: V ? V.runs_made : null, runs,
    // without pairwise (as validation runs): the decision on each run's single-figure criteria (at least two of the runs made, or two of two)
    single_got: runs.length ? (runs.filter(x => x.single_failed && !x.single_failed.length).length >= 2 ? 'PASS' : 'FAIL') : null, dir: out };
  row.correct = row.got === row.expect;
  results.push(row);
  console.log(JSON.stringify(row));
  if (!V) console.error(r.out.slice(-800), r.err.slice(-800));
}
const queue = [...tasks];
await Promise.all(Array.from({ length: JOBS }, async () => { while (queue.length) await one(queue.shift()); }));
results.sort((a, b) => a.v.localeCompare(b.v) || a.run - b.run);
const core = results.filter(r => !SET[r.v].decoy && !SET[r.v].must), dec = results.filter(r => SET[r.v].decoy), must = results.filter(r => SET[r.v].must);
const correct = core.filter(r => r.correct).length, dcorrect = dec.filter(r => r.correct).length, mcorrect = must.filter(r => r.correct).length;
// without pairwise (as the sealed validation runs): would v1 and v2 still fail on their single-figure criteria alone?
// (a lower bound for a split decision: run 3 was made only when runs 1 and 2 disagreed with pairwise counted)
const single = core.filter(r => r.single_got).map(r => ({ v: r.v, eval: r.run, got: r.single_got }));
const perRun = Object.fromEntries(ONLY.map(v => { const rs = results.filter(r => r.v === v).flatMap(r => r.runs); return [v, { passed: rs.filter(x => x.got === 'PASS').length, of: rs.length }]; }));
let hash = null; try { hash = JSON.parse(fs.readFileSync(path.join((core[0] || dec[0] || must[0]).dir, 'verdict.json'), 'utf8')).fingerprint; } catch {}
fs.writeFileSync(path.join(DIR, 'summary.json'), JSON.stringify({ label: LABEL, correct, of: core.length, decoys_correct: dcorrect, decoys_of: dec.length, must_pass_correct: mcorrect, must_pass_of: must.length,
  ledger: { source: LEDGER_SRC, copy: LEDGER, sha256: LG.sha256, takeaways: TAKE }, rule: 'a decision passes when at least 2 of 3 complete runs pass', single_criteria: single, runs_per_item: perRun, fingerprint: hash, results }, null, 1));
console.log(`fig:dev ${LABEL}: decisions: ${correct} of ${core.length} correct (v1, v2, v4); decoys ${dcorrect} of ${dec.length} correct; must-pass (Enigma) ${mcorrect} of ${must.length}; complete runs passed per item: ${Object.entries(perRun).map(([v, x]) => `${v} ${x.passed}/${x.of}`).join(', ')} -> ${path.join(DIR, 'summary.json')}`);
