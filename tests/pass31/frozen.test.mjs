// Pass 31 frozen-file checks (docs/pass-31-calibration.md section 18, item 4).
//   npm run fig:frozen-test
// Checks, without any tester call:
//   files    the fingerprint (hash.mjs) hashes the three inputs that change verdicts (/usr/share/dict/words,
//            docs/pass-30-exceptions.json, scripts/figs/build_into.py) and the teaching places (tests/pass31/places.mjs),
//            each at its file's current sha256; and every module a hashed file imports (statically or with
//            import(new URL(...))) is itself hashed, so no code of the gate sits outside the fingerprint (a third-party
//            package under node_modules, playwright, is a dependency like the CLI and is not hashed)
//   check    fig:check refuses (exit 2, nothing checked) with no --expect-hash and with a wrong one, as gate.mjs does,
//            and runs with the right one
//   dev      fig:dev refuses the same way (no --expect-hash, a wrong one)
//   partial  gate.mjs refuses --criteria with --author, --single included (exit 2), outside a decision's own runs; a
//            decision's own run (P31_GATE_DECISION_RUN=1, as the decision starts it) of part of the gate prints the
//            partial marker on the author's line
// Exit 0 when every check holds, 1 otherwise.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { run, REPO } from './lib.mjs';
import { fingerprint, GATE_FILES } from './hash.mjs';

let bad = 0, n = 0;
const check = (ok, line) => { n++; if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${line}`); };
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(path.resolve(REPO, f))).digest('hex');
const FP = await fingerprint();

// ---- files ---------------------------------------------------------------------------------------------------------
const NEW = ['/usr/share/dict/words', 'docs/pass-30-exceptions.json', 'scripts/figs/build_into.py', 'tests/pass31/places.mjs'];
for (const f of NEW) check(GATE_FILES.includes(f) && FP.files[f] === sha(f), `files: ${f} hashed (${(FP.files[f] || 'missing').slice(0, 12)}, file ${sha(f).slice(0, 12)})`);
{
  const missing = [];
  for (const f of GATE_FILES.filter(x => x.endsWith('.mjs'))) {
    const src = fs.readFileSync(path.resolve(REPO, f), 'utf8'), dir = path.dirname(path.resolve(REPO, f));
    const refs = [...src.matchAll(/\bfrom\s+'(\.{1,2}\/[^']+)'/g), ...src.matchAll(/import\(\s*new URL\(\s*'(\.{1,2}\/[^']+)'/g)].map(m => m[1]);
    // a third-party package (playwright under tests/pass25/node_modules) is a dependency, as the CLI is: not hashed
    for (const r of refs) { const rel = path.relative(REPO, path.resolve(dir, r)); if (!GATE_FILES.includes(rel) && !rel.split(path.sep).includes('node_modules')) missing.push(`${f} -> ${rel}`); }
  }
  check(!missing.length, `files: modules imported by the hashed files and not hashed: ${missing.length}${missing.length ? ` (${missing.join('; ')})` : ''}`);
}

// ---- check ---------------------------------------------------------------------------------------------------------
const node = (argv, env = {}) => run('node', argv, { env, timeout: 600000 });
{
  const a = await node([path.join(REPO, 'tests/pass31/check.mjs'), 'part-1', '--fig=fig-1-1', '--gate1=off']);
  const b = await node([path.join(REPO, 'tests/pass31/check.mjs'), 'part-1', '--fig=fig-1-1', '--gate1=off', `--expect-hash=${'0'.repeat(64)}`]);
  check(a.code === 2 && /refused: no --expect-hash/.test(a.out) && !/fig:check part-1/.test(a.out), `check: no --expect-hash -> exit ${a.code}, refused ${/refused/.test(a.out)}`);
  check(b.code === 2 && /refused: the gate's fingerprint/.test(b.out) && !/fig:check part-1/.test(b.out), `check: a wrong --expect-hash -> exit ${b.code}, refused ${/refused/.test(b.out)}`);
  const c = await node([path.join(REPO, 'tests/pass31/check.mjs'), 'part-1', '--fig=fig-1-1', '--gate1=off', `--expect-hash=${FP.combined}`, `--json=${path.join(REPO, 'tests/pass31/out/frozen-test-check.json')}`]);
  check([0, 1].includes(c.code) && !/refused/.test(c.out) && /fig:check part-1: /.test(c.out), `check: the frozen --expect-hash -> exit ${c.code}, ran ${/fig:check part-1: /.test(c.out)}`);
}

// ---- dev -----------------------------------------------------------------------------------------------------------
{
  const a = await node([path.join(REPO, 'tests/pass31/dev.mjs'), '--only=v4', '--runs=1']);
  const b = await node([path.join(REPO, 'tests/pass31/dev.mjs'), '--only=v4', '--runs=1', `--expect-hash=${'0'.repeat(64)}`]);
  check(a.code === 2 && /refused/.test(a.out) && b.code === 2 && /refused/.test(b.out), `dev: no --expect-hash -> exit ${a.code}; a wrong one -> exit ${b.code}`);
}

// ---- partial -------------------------------------------------------------------------------------------------------
{
  const G = path.join(REPO, 'tests/pass31/gate.mjs'), base = ['fig-1-1', '--intent=Function: a test takeaway.', '--job=function', '--no-pairwise', '--criteria=taught'];
  const a = await node([G, ...base, '--author', '--single', `--expect-hash=${FP.combined}`]);
  const b = await node([G, ...base, '--author', `--expect-hash=${FP.combined}`]);
  check(a.code === 2 && /--criteria with --author refused/.test(a.out), `partial: --single --author --criteria outside a decision -> exit ${a.code}, refused ${/refused/.test(a.out)}`);
  check(b.code === 2 && /--criteria with --author refused/.test(b.out), `partial: --author --criteria (a decision) -> exit ${b.code}, refused ${/refused/.test(b.out)}`);
  const out = path.join(REPO, 'tests/pass31/out/frozen-test-partial');
  const c = await node([G, ...base, '--author', '--single', `--out=${out}`, `--expect-hash=${FP.combined}`], { P31_GATE_DECISION_RUN: '1' });
  let line = null; try { line = JSON.parse(c.out.trim().split('\n').pop()); } catch {}
  check([0, 1].includes(c.code) && line && Array.isArray(line.partial) && line.partial.join() === 'taught', `partial: a decision's own run of part of the gate -> exit ${c.code}, the author's line ${JSON.stringify(line)}`);
}
console.log(`frozen-test: ${n - bad} of ${n} checks hold`);
process.exit(bad ? 1 : 0);
