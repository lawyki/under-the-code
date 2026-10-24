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
//            decision's own run of part of the gate prints the partial marker on the author's line (section 20: a real
//            decision's runs, read from its verdict.json)
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
// Section 20 (the review of the section 19 freeze, D3, D5, D9, D10) adds:
//   own      gate.mjs refuses --rc2-tree, --rc2-rev, --intent, --intent-file and --job with --author (exit 2), before
//            anything renders; validate.mjs no longer runs the gate with --author
//   nonce    the old constant (P31_GATE_DECISION_RUN=1) and a forged nonce lift no refusal; a real decision's own runs
//            (its nonce) run in the author's form and print partial, single, no_pairwise and the takeaway's source on
//            their lines, which the decision's verdict.json keeps; the nonce file is gone when the decision ends; every
//            run records the svg and tree hashes
//   trees    the fingerprint hashes scripts/check-dashes.mjs and the gate's own public/ (a tree hash); fig:validate and
//            fig:dev rebuild their trees on every run (a file planted in a built tree is gone after the next run) and
//            record each tree's hash
//   atbar    lib.mjs atBarEvidence accepts an at_bar id only with a passing decision's verdict under the frozen
//            fingerprint for the figure's current svg (variants: a wrong fingerprint, svg, id, a single run, a partial
//            run, a failed decision, one run made, a run under another fingerprint are each refused); check.mjs applies
//            it to the label cap
//   npm run fig:frozen-test [-- --ledger=<docs/pass-31-ledger.tsv>]   (the ledger is read only for fig-1-1's row; a
//            synthetic one-row ledger is used when none is given)
// Exit 0 when every check holds, 1 otherwise.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { run, exemptProblems, atBarOK, atBarEvidence, svgSha, findFigure, mkdirp, args, REPO, PUBLIC, OUT } from './lib.mjs';
import { fingerprint, treeHash, GATE_FILES } from './hash.mjs';

let bad = 0, n = 0;
const check = (ok, line) => { n++; if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${line}`); };
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(path.resolve(REPO, f))).digest('hex');
const FP = await fingerprint();

// ---- files ---------------------------------------------------------------------------------------------------------
const NEW = ['/usr/share/dict/words', 'docs/pass-30-exceptions.json', 'scripts/figs/build_into.py', 'tests/pass31/places.mjs', 'scripts/check-dashes.mjs'];
for (const f of NEW) check(GATE_FILES.includes(f) && FP.files[f] === sha(f), `files: ${f} hashed (${(FP.files[f] || 'missing').slice(0, 12)}, file ${sha(f).slice(0, 12)})`);
// section 20 (D5): the gate's own public/, as a tree hash
check(GATE_FILES.includes('public/') && FP.files['public/'] === treeHash(PUBLIC), `trees: public/ hashed (${(FP.files['public/'] || 'missing').slice(0, 12)}, tree ${treeHash(PUBLIC).slice(0, 12)})`);
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
  // section 20 (D9): the old constant and a forged nonce lift no refusal
  const out = mkdirp(path.join(OUT, 'frozen-test-partial')), runDir = path.join(out, 'run-1');
  fs.rmSync(path.join(out, 'decision.nonce'), { force: true });
  const c0 = await node([G, ...base, '--author', '--single', `--out=${runDir}`, `--expect-hash=${FP.combined}`], { P31_GATE_DECISION_RUN: '1' });
  check(c0.code === 2 && /--criteria with --author refused/.test(c0.out), `nonce: the old constant P31_GATE_DECISION_RUN=1 -> exit ${c0.code}, refused ${/refused/.test(c0.out)}`);
  const forged = 'ab'.repeat(16);
  const c1 = await node([G, ...base, '--author', '--single', `--out=${runDir}`, `--expect-hash=${FP.combined}`], { P31_GATE_DECISION_NONCE: forged });
  fs.writeFileSync(path.join(out, 'decision.nonce'), `1 ${forged}\n`);   // a file naming a process that is not the run's parent
  const c2 = await node([G, ...base, '--author', '--single', `--out=${runDir}`, `--expect-hash=${FP.combined}`], { P31_GATE_DECISION_NONCE: forged });
  fs.rmSync(path.join(out, 'decision.nonce'), { force: true });
  check(c1.code === 2 && c2.code === 2 && /refused/.test(c1.out) && /refused/.test(c2.out), `nonce: a forged nonce with no file -> exit ${c1.code}; with a file naming another parent -> exit ${c2.code}`);
  // a real decision (the builder's form, part of the gate): its own runs run in the author's form; each run's line is
  // kept in the decision's verdict.json and says partial, single, no_pairwise and the takeaway's source
  const dd = path.join(OUT, 'frozen-test-decision'); fs.rmSync(dd, { recursive: true, force: true });
  const dc = await node([G, ...base, `--out=${dd}`, `--expect-hash=${FP.combined}`]);
  let DV = null; try { DV = JSON.parse(fs.readFileSync(path.join(dd, 'verdict.json'), 'utf8')); } catch {}
  const lines = DV && DV.runs ? DV.runs.map(r => r.line) : [];
  check([0, 1].includes(dc.code) && lines.length >= 2 && lines.every(l => l && Array.isArray(l.partial) && l.partial.join() === 'taught' && l.single === true && l.no_pairwise === true && l.takeaway === 'command line'),
    `partial: a decision's own runs of part of the gate -> exit ${dc.code}, the runs' author lines ${JSON.stringify(lines)}`);
  const f11 = findFigure(PUBLIC, 'fig-1-1');
  check(DV && !fs.existsSync(path.join(dd, 'decision.nonce')) && DV.svg_sha256 === svgSha(f11.svg) && DV.tree_sha256 === treeHash(PUBLIC) && DV.runs.every(r => r.svg_sha256 === DV.svg_sha256),
    `nonce: the decision's nonce file removed ${DV && !fs.existsSync(path.join(dd, 'decision.nonce'))}; svg and tree hashes recorded ${!!(DV && DV.svg_sha256 && DV.tree_sha256)}, the runs' svg hash the decision's ${!!(DV && DV.runs && DV.runs.every(r => r.svg_sha256 === DV.svg_sha256))}`);
  // section 19 (D, G): --single --author with the full criteria is refused outside a decision's own runs (before
  // anything renders or calls a tester)
  const full = ['fig-1-1', '--intent=Function: a test takeaway.', '--job=function', '--no-pairwise'];
  const d = await node([G, ...full, '--author', '--single', `--expect-hash=${FP.combined}`]);
  check(d.code === 2 && /--single with --author refused/.test(d.out), `single: --single --author (full criteria) outside a decision -> exit ${d.code}, refused ${/refused/.test(d.out)}`);
}

// ---- own (section 20, D3) ------------------------------------------------------------------------------------------
{
  const G = path.join(REPO, 'tests/pass31/gate.mjs'), xf = path.join(mkdirp(path.join(OUT, 'frozen-test-own')), 'intent.txt');
  fs.writeFileSync(xf, 'Function: a test takeaway.');
  const variants = [['--rc2-tree', [`--rc2-tree=${PUBLIC}`]], ['--rc2-rev', ['--rc2-rev=v1.0-rc1']], ['--intent', ['--intent=Function: a test takeaway.', '--job=function']],
    ['--intent-file', [`--intent-file=${xf}`]], ['--job', [`--ledger=${xf}`, '--job=function']]];
  for (const [k, extra] of variants) {
    const r = await node([G, 'fig-1-1', ...extra, '--author', `--expect-hash=${FP.combined}`]);
    check(r.code === 2 && /with --author refused: the author's form judges against the ledger/.test(r.out) && r.out.includes(k), `own: ${k} with --author -> exit ${r.code}, refused ${/refused/.test(r.out)}`);
  }
  const vs = fs.readFileSync(path.join(REPO, 'tests/pass31/validate.mjs'), 'utf8'), argvAt = vs.indexOf("const argv = [path.join(REPO, 'tests/pass31/gate.mjs')");
  check(argvAt > 0 && !/'--author'/.test(vs.slice(argvAt, vs.indexOf(';', argvAt))), `own: validate.mjs runs the gate without --author: ${argvAt > 0 && !/'--author'/.test(vs.slice(argvAt, vs.indexOf(';', argvAt)))}`);
}

// ---- trees (section 20, D5) --------------------------------------------------------------------------------------------
{
  const { o } = args(process.argv.slice(2));
  const T = mkdirp(path.join(OUT, 'frozen-test-trees'));
  // a ledger with fig-1-1's row: the author's when given, else a synthetic one-row ledger
  const ledger = o.ledger && o.ledger !== true ? path.resolve(String(o.ledger)) : path.join(T, 'ledger.tsv');
  if (!(o.ledger && o.ledger !== true)) fs.writeFileSync(ledger, 'id\tjob\tintent\nfig-1-1\tfunction\tFunction: a test takeaway.\n');
  // fig:dev: v4's tree, a file planted in it, a run of one decoy made from v4 (decoy3), the taught criterion only (no
  // tester call): v4, the decoy's base, is rebuilt too (the file is gone), and both trees' hashes are in summary.json
  const v4 = path.join(OUT, 'dev', 'trees', 'v4', 'public'), d3 = path.join(OUT, 'dev', 'trees', 'decoy3', 'public');
  if (fs.existsSync(v4)) fs.writeFileSync(path.join(v4, 'planted.txt'), 'x');
  const dv = await node([path.join(REPO, 'tests/pass31/dev.mjs'), '--only=decoy3', '--runs=1', '--criteria=taught', '--label=frozen-test-dev', `--ledger=${ledger}`, `--expect-hash=${FP.combined}`]);
  let S = null; try { S = JSON.parse(fs.readFileSync(path.join(OUT, 'dev', 'frozen-test-dev', 'summary.json'), 'utf8')); } catch {}
  check(S && !fs.existsSync(path.join(v4, 'planted.txt')) && fs.existsSync(path.join(v4, 'part-1.html')) && S.trees && S.trees.v4 === treeHash(v4) && S.trees.decoy3 === treeHash(d3),
    `trees: fig:dev --only=decoy3 rebuilt its base v4 (planted file gone ${!fs.existsSync(path.join(v4, 'planted.txt'))}), both hashes in summary.json ${!!(S && S.trees && S.trees.v4 === treeHash(v4) && S.trees.decoy3 === treeHash(d3))} (exit ${dv.code})`);
  // fig:validate on a scratch sealed folder (never docs/pass-31-sealed): one rev item whose id is no figure, so the gate
  // refuses it and the run is incomplete (exit 2) after the tree is built; run twice with a file planted between
  const SD = path.join(T, 'sealed'); fs.rmSync(SD, { recursive: true, force: true }); mkdirp(SD);
  fs.writeFileSync(path.join(SD, 'validation.json'), JSON.stringify({ items: [{ name: 'test', id: 'fig-0-0', role: 'v4', job: 'function', intent: 'Function: a test takeaway.', rev: '2a9ece9', script: 'fig_1_1.py' }] }));
  const va = () => node([path.join(REPO, 'tests/pass31/validate.mjs'), `--sealed=${SD}`, `--ledger=${ledger}`, `--expect-hash=${FP.combined}`, '--jobs=1']);
  const a = await va(), built = path.join(SD, 'trees', '2a9ece9-fig_1_1.py', 'public');
  if (fs.existsSync(built)) fs.writeFileSync(path.join(built, 'planted.txt'), 'x');
  const b = await va();
  const runs = fs.existsSync(path.join(SD, 'runs')) ? fs.readdirSync(path.join(SD, 'runs')).sort() : [];
  let C = null; try { C = JSON.parse(fs.readFileSync(path.join(SD, 'runs', runs[runs.length - 1], 'counts.json'), 'utf8')); } catch {}
  check(a.code === 2 && b.code === 2 && fs.existsSync(path.join(built, 'part-1.html')) && !fs.existsSync(path.join(built, 'planted.txt')) && C && C.trees && C.trees['item-01'] === treeHash(built) && C.fingerprint.files['public/'] === treeHash(PUBLIC),
    `trees: fig:validate rebuilt its rev tree (planted file gone ${!fs.existsSync(path.join(built, 'planted.txt'))}), its hash in counts.json ${!!(C && C.trees && C.trees['item-01'] === treeHash(built))}, public/ in the fingerprint it records (exits ${a.code}, ${b.code}: incomplete, as the item is no figure)`);
}

// ---- atbar (section 20, D10) -------------------------------------------------------------------------------------------
{
  const f = findFigure(PUBLIC, 'fig-1-1'), h = svgSha(f.svg), fp = FP.combined;
  const good = { id: 'fig-1-1', pass: true, runs: [{ k: 1, fingerprint: fp }, { k: 2, fingerprint: fp }], runs_made: 2, runs_passed: 2, fingerprint: { combined: fp }, svg_sha256: h };
  check(atBarOK(good, 'fig-1-1', h, fp), 'atbar: a passing decision under the frozen fingerprint for the current svg is evidence');
  const bad = [['another fingerprint', x => { x.fingerprint.combined = '0'.repeat(64); }], ['another svg', x => { x.svg_sha256 = '0'.repeat(64); }], ['another figure', x => { x.id = 'fig-1-2'; }],
    ['a single run', x => { x.single = true; }], ['a partial run', x => { x.partial = ['taught']; }], ['a failed decision', x => { x.pass = false; }], ['one run made', x => { x.runs_made = 1; x.runs_passed = 1; x.runs = x.runs.slice(0, 1); }],
    ['a run under another fingerprint', x => { x.runs[1].fingerprint = '0'.repeat(64); }]];
  for (const [what, m] of bad) { const x = JSON.parse(JSON.stringify(good)); m(x); check(!atBarOK(x, 'fig-1-1', h, fp), `atbar: ${what} -> not evidence`); }
  const D = path.join(OUT, 'frozen-test-atbar'); fs.rmSync(D, { recursive: true, force: true });
  fs.mkdirSync(path.join(D, 'a'), { recursive: true }); fs.writeFileSync(path.join(D, 'a', 'verdict.json'), JSON.stringify({ ...good, single: true }));
  const none = atBarEvidence(D, 'fig-1-1', h, fp);
  fs.mkdirSync(path.join(D, 'b'), { recursive: true }); fs.writeFileSync(path.join(D, 'b', 'verdict.json'), JSON.stringify(good));
  const found = atBarEvidence(D, 'fig-1-1', h, fp);
  const src = fs.readFileSync(path.join(REPO, 'tests/pass31/check.mjs'), 'utf8');
  check(none === null && found === path.join(D, 'b', 'verdict.json') && /check === 'label_cap' && \(EX\.at_bar\.includes\(id\)[^\n]*atBarEvidence\(VERDICTS, id, svgSha\(f\.svg\), FP\.combined\)/.test(src),
    `atbar: a folder with only a single run's verdict gives ${none}; with a decision's, its file ${found === path.join(D, 'b', 'verdict.json')}; check.mjs takes at_bar's cap exemption only through atBarEvidence ${/atBarEvidence\(VERDICTS/.test(src)}`);
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
