// Pass 31 sealed validation (docs/pass-31-brief.md section 10; docs/pass-31-calibration.md). Runs the frozen gate on
// the sealed set with its single-figure criteria only (taught, judge, hedge, still, stripped; no pairwise) and prints
// COUNTS ONLY: no figure id, verdict, criterion name or tester reply reaches stdout, so the gate builder can run it
// and see only whether validation held.
//   npm run fig:validate -- [--sealed=docs/pass-31-sealed] [--manifest=<sealed>/validation.json]
//                           [--expect-hash=<combined sha256 from the calibration record>] [--jobs=3]
// The manifest (written by whoever seals the set, never by the gate builder):
//   {"items": [{"name": "...", "id": "fig-1-1", "role": "v3|v4|worst|best", "job": "function|real thing|two-part",
//               "intent": "...", "tree": "<public dir>" | "rev": "<commit>", "script": "fig_1_1.py"}]}
//   tree: a prebuilt public dir; rev: that commit's scripts/figs/<script> and figlib.py built into a copy of public/
//   (as fig:dev builds); neither: this worktree's public/.
// Bars (section 10): every v3 item fails, every v4 item passes, every worst fails, at least half of the best pass.
// Everything else (built trees, every verdict, the counts) is written under <sealed>/, which is gitignored and never
// pushed, and each run appends one line to <sealed>/reads.log. Exit 0 validation holds, 1 it does not, 2 incomplete.
import fs from 'node:fs'; import path from 'node:path';
import { args, run, mkdirp, REPO, PUBLIC } from './lib.mjs';
import { fingerprint } from './hash.mjs';

const { o } = args(process.argv.slice(2));
const SEALED = path.resolve(REPO, o.sealed || 'docs/pass-31-sealed');
const MANIFEST = path.resolve(o.manifest || path.join(SEALED, 'validation.json'));
const JOBS = +(o.jobs || 3);
const say = s => console.log(`fig:validate ${s}`);
if (!fs.existsSync(MANIFEST)) { say(`no manifest at ${path.relative(REPO, MANIFEST)}`); process.exit(2); }
let items;
try { items = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')).items; } catch { say('the manifest is not readable JSON'); process.exit(2); }
const ROLES = ['v3', 'v4', 'worst', 'best'];
if (!Array.isArray(items) || !items.length || items.some(x => !x || !x.id || !x.intent || !ROLES.includes(x.role))) { say('the manifest has an item without id, intent or a role (v3, v4, worst, best)'); process.exit(2); }
const FP = await fingerprint(o.model || 'claude-sonnet-5-5');
if (o['expect-hash'] && o['expect-hash'] !== FP.combined) { say(`refused: the gate's fingerprint is not the frozen one (npm run fig:hash)`); process.exit(2); }
const STAMP = new Date().toISOString().replace(/[:.]/g, '-');
const DIR = mkdirp(path.join(SEALED, 'runs', STAMP));
fs.appendFileSync(path.join(SEALED, 'reads.log'), `${STAMP}\tfig:validate\t${items.length} items\tgate ${FP.combined}\tcli ${FP.cli}\n`);

// trees
for (const [k, it] of items.entries()) {
  it.key = `item-${String(k + 1).padStart(2, '0')}`;
  if (it.tree) { it.root = path.resolve(REPO, it.tree); continue; }
  if (!it.rev) { it.root = PUBLIC.slice(0, -1); continue; }
  const d = path.join(SEALED, 'trees', `${it.rev}-${it.script || 'fig'}`), src = mkdirp(path.join(d, 'src'));
  it.root = path.join(d, 'public');
  if (fs.existsSync(path.join(it.root, 'part-1.html'))) continue;
  fs.cpSync(PUBLIC, it.root, { recursive: true });
  for (const f of [it.script, 'figlib.py']) {
    const r = await run('git', ['show', `${it.rev}:scripts/figs/${f}`]);
    if (r.code) { say('a build failed (git show); incomplete'); process.exit(2); }
    fs.writeFileSync(path.join(src, f), r.out);
  }
  const b = await run('python3', [path.join(REPO, 'scripts/figs/build_into.py'), it.root, path.join(src, it.script)]);
  if (b.code) { say('a build failed (build_into.py); incomplete'); process.exit(2); }
}

// gate runs, quiet
const res = [];
const queue = [...items];
async function one(it) {
  const out = path.join(DIR, it.key);
  const argv = [path.join(REPO, 'tests/pass31/gate.mjs'), it.id, `--intent=${it.intent}`, `--job=${it.job || 'function'}`, `--tree=${it.root}`,
    '--no-pairwise', '--author', `--out=${out}`, `--label=validate-${it.key}`, ...(o['expect-hash'] ? [`--expect-hash=${o['expect-hash']}`] : [])];
  const r = await run('node', argv);
  let V = null; try { V = JSON.parse(fs.readFileSync(path.join(out, 'verdict.json'), 'utf8')); } catch {}
  res.push({ role: it.role, got: !V || V.failed === 'error' || r.code === 2 ? 'error' : V.pass ? 'pass' : 'fail' });
}
await Promise.all(Array.from({ length: JOBS }, async () => { while (queue.length) await one(queue.shift()); }));

const n = (role, got) => res.filter(r => r.role === role && (!got || r.got === got)).length;
const C = { v3: { fail: n('v3', 'fail'), of: n('v3') }, v4: { pass: n('v4', 'pass'), of: n('v4') }, worst: { fail: n('worst', 'fail'), of: n('worst') }, best: { pass: n('best', 'pass'), of: n('best') }, errors: res.filter(r => r.got === 'error').length };
const holds = C.errors === 0 && C.v3.of > 0 && C.v3.fail === C.v3.of && C.v4.of > 0 && C.v4.pass === C.v4.of && C.worst.fail === C.worst.of && C.best.pass * 2 >= C.best.of;
const verdict = C.errors ? 'INCOMPLETE' : holds ? 'HOLDS' : 'FAILS';
fs.writeFileSync(path.join(DIR, 'counts.json'), JSON.stringify({ stamp: STAMP, verdict, counts: C, fingerprint: FP }, null, 1));
say(`${verdict}: v3 failed ${C.v3.fail} of ${C.v3.of}; v4 passed ${C.v4.pass} of ${C.v4.of}; tapped worst failed ${C.worst.fail} of ${C.worst.of}; tapped best passed ${C.best.pass} of ${C.best.of}; tool errors ${C.errors}`);
process.exit(C.errors ? 2 : holds ? 0 : 1);
