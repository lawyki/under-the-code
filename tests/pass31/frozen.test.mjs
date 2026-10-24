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
// Section 19 (the review of the section 18 freeze, D, G, H) adds:
//   single   gate.mjs refuses --single with --author outside a decision's own runs, with the full criteria too (exit 2);
//            a decision's own run prints "single" on the author's line, and a run without the pairwise test
//            "no_pairwise"
//   marks    fig:check with --gate1=off prints the partial mark on every figure line and part line, and its check.json
//            records the mode and the fingerprint it ran under
//   exempt   lib.mjs exemptProblems holds docs/pass-31-exempt.json to the brief's grants: the file as it stands passes;
//            a kept id that is no kept original, a label-cap id outside at_bar and kept, a floor id outside kept, a caption
//            id outside kept and fig-18-6, another key, and an id that is no figure id are each refused; and check.mjs
//            applies it before anything is checked
// Exit 0 when every check holds, 1 otherwise.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { run, exemptProblems, REPO } from './lib.mjs';
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
  const cj = path.join(REPO, 'tests/pass31/out/frozen-test-check.json');
  const c = await node([path.join(REPO, 'tests/pass31/check.mjs'), 'part-1', '--fig=fig-1-1', '--gate1=off', `--expect-hash=${FP.combined}`, `--json=${cj}`]);
  check([0, 1].includes(c.code) && !/refused/.test(c.out) && /fig:check part-1: /.test(c.out), `check: the frozen --expect-hash -> exit ${c.code}, ran ${/fig:check part-1: /.test(c.out)}`);
  // section 19 (G): every figure and part line of a --gate1=off run carries the partial mark; check.json the mode and
  // the fingerprint
  const lines = c.out.split('\n').filter(l => /^(PASS|FAIL) /.test(l)), marked = lines.filter(l => /\[partial: gate1 off\]$/.test(l));
  let J = null; try { J = JSON.parse(fs.readFileSync(cj, 'utf8')); } catch {}
  check(lines.length > 1 && marked.length === lines.length && J && J.fingerprint === FP.combined && J.partial === 'gate1 off',
    `marks: --gate1=off -> ${marked.length} of ${lines.length} lines marked partial; check.json fingerprint ${J && J.fingerprint === FP.combined ? 'the frozen one' : J && J.fingerprint}, partial ${J && J.partial}`);
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
  // section 19 (D, G): the same line says "single" and "no_pairwise"; --single --author with the full criteria is
  // refused outside a decision's own runs (before anything renders or calls a tester)
  check(line && line.single === true && line.no_pairwise === true, `single: a decision's own run prints single ${line && line.single}, no_pairwise ${line && line.no_pairwise} on the author's line`);
  const full = ['fig-1-1', '--intent=Function: a test takeaway.', '--job=function', '--no-pairwise'];
  const d = await node([G, ...full, '--author', '--single', `--expect-hash=${FP.combined}`]);
  check(d.code === 2 && /--single with --author refused/.test(d.out), `single: --single --author (full criteria) outside a decision -> exit ${d.code}, refused ${/refused/.test(d.out)}`);
}

// ---- exempt (section 19, H) ------------------------------------------------------------------------------------------
{
  const EX = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/pass-31-exempt.json'), 'utf8'));
  check(exemptProblems(EX).length === 0, `exempt: docs/pass-31-exempt.json as it stands -> ${exemptProblems(EX).length} breaches`);
  const variant = f => { const x = JSON.parse(JSON.stringify(EX)); f(x); return exemptProblems(x).length; };
  const cases = [
    ['a kept id that is no kept original', x => x.kept.push('fig-1-1'), 1],
    ['a label-cap id outside at_bar and kept', x => x.label_cap.ids.push('fig-1-1'), 1],
    ['a label-cap id that is at bar', x => { x.at_bar.push('fig-1-1'); x.label_cap.ids.push('fig-1-1'); }, 0],
    ['a floor id outside kept (fig-18-6)', x => x.floor.ids.push('fig-18-6'), 1],
    ['a floor id that is kept', x => x.floor.ids.push('fig-3-7'), 0],
    ['a caption id outside kept and fig-18-6', x => x.caption.ids.push('fig-1-1'), 1],
    ['another key (taught)', x => { x.taught = { ids: ['fig-1-1'] }; }, 1],
    ['an id that is no figure id', x => x.at_bar.push('everything'), 1],
  ];
  for (const [what, f, want] of cases) { const got = variant(f); check(want ? got >= 1 : got === 0, `exempt: ${what} -> ${got} breaches (expected ${want ? 'a refusal' : 'none'})`); }
  const src = fs.readFileSync(path.join(REPO, 'tests/pass31/check.mjs'), 'utf8');
  const at = src.indexOf('exemptProblems(EX)'), first = src.indexOf('runKnownTerms(ROOT');
  check(at > 0 && first > at && /process\.exit\(2\)/.test(src.slice(at, at + 300)), `exempt: check.mjs refuses on a breach (exit 2) before anything is checked: ${at > 0 && first > at}`);
}
console.log(`frozen-test: ${n - bad} of ${n} checks hold`);
process.exit(bad ? 1 : 0);
