// Pass 31 gate (docs/pass-31-brief.md sections 7, 10, 11, 15; docs/pass-31-calibration.md).
//   npm run fig:gate -- <fig-id> [--ledger=<docs/pass-31-ledger.tsv>] | [--intent="<takeaway>" --job="function|real thing|two-part"]
//        [--tree=<public dir>] [--part=part-N] [--rc2-tree=<public dir> | --rc2-rev=v1.0-rc2 | --no-pairwise]
//        [--order=random|cand-first|rc2-first] [--criteria=taught,judge,hedge,still,stripped,pairwise] [--out=<dir>]
//        [--model=claude-sonnet-5-5] [--label=<name>] --expect-hash=<combined sha256> [--author] [--single]
// --expect-hash is required: the gate computes its fingerprint (hash.mjs) first and refuses (exit 2) unless it equals
// the hash given, so only the frozen gate ever judges (docs/pass-31-calibration.md section 16).
// --criteria runs only the criteria named (a builder's diagnosis): the verdict carries "partial" and is never a verdict
// on the figure; with --author it is refused (calibration section 17), --single included, except inside a decision's
// own runs, and every output line of a partial run, the author's included, carries the partial marker (section 18).
// Renders, with tests/pass30/bare.mjs at 375 px: a 12-frame strip sampled evenly across the cycle (frame 1 is the t=0
// still), the same strip with --no-text, and (pairwise) the rc2 version's strip. A figure that does not animate renders
// one frame: its still is the whole figure, so `judge` is not applicable (n/a) and the still, the text-stripped still
// and the hedge check on both carry the test; except for the job "real thing", whose still is not scored on the
// mechanism (decision D1): there the still's description stands in for the judge's, scored and hedge-checked with the
// judge's real-thing rubric and hedge scope, so a real thing that does not animate must still give its mechanism
// (docs/pass-31-calibration.md section 15, review fix 1). The judge packet is the book's prose up to the figure (every earlier
// part, and this part up to the card), never its caption, strip, <title> or <desc>, and never held material
// (tests/pass31/held-strip.json, calibration section 16). Testers are fresh Sonnet 5.5
// sessions (claude -p, no tools, safe mode), each run in a new empty directory under the system temp dir (outside any
// repo), each seeing only its message:
//   taught    mechanical: every label and object token taught before the figure (lib.mjs taughtYet; known-terms run with
//             the held material stripped)
//   judge     (a) the judge describes the 12 frames; (b) the scorer compares that with the intent for the job
//   hedge     (c) any hedge on what changes, why, or the result fails: checked on the judge's, the still's and the
//             text-stripped descriptions, each in its own scope (prompts.mjs HEDGE)
//   still     (d) the t=0 still alone, judged and scored
//   stripped  (e) the text-stripped strip, judged and scored: does it still show what moves and what causes what
//   (the scorers and hedge checks are each asked three times; the majority decides)
//   pairwise  (f) candidate against its rc2 version, both orders (the first one random unless --order): it fails
//             only when the rc2 version is judged better in both orders. Identical frames skip the call (SAME).
// The takeaway is read from the ledger by header name (column "intent", the takeaway the scorer grades; column "job",
// the job it tests; never by column index; "content" is the fact checker's), default docs/pass-31-ledger.tsv, or
// given with --intent and --job for a figure outside the ledger. Only the scorer sees it. The verdict records the
// ledger file and its sha256.
// The decision (docs/pass-31-calibration.md section 14): the figure passes when at least two of three independent
// complete runs of everything above pass (runs 1 and 2 in parallel, run 3 only when they disagree). Each run's
// verdict is in <out>/run-k/verdict.json; --single makes one run (the decision's building block, never a verdict).
// A tool failure (render, CLI, an unreadable reply after three attempts) is not a figure failure: the verdict is
// failed "error" and the exit code 2 (a run that errs is made again once first). Exit 0 pass, 1 fail.
// Output: <out>/verdict.json (the decision and its runs; each run's own verdict.json holds every tester's reply, for
// the gate builder) and on stdout one JSON line {"id","pass","failed","failed_all"}; with --author only
// {"id","pass","failed"}. For a failed decision, failed_all lists the criteria its failing runs failed, most often first.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto'; import os from 'node:os';
import { args, tree, findFigure, packet as proseUpTo, runKnownTerms, taughtContext, taughtYet, svgTexts, run, mkdirp, framesIn, readLedger, ledgerTakeaway, LEDGER_DEFAULT, REPO, OUT, PUBLIC } from './lib.mjs';
import * as P from './prompts.mjs';
import { fingerprint, CLAUDE } from './hash.mjs';

const { pos, o } = args(process.argv.slice(2));
const ID = pos[0];
const USAGE = 'usage: npm run fig:gate -- <fig-id> [--ledger=file] | [--intent="..." --job="function|real thing|two-part"] [--tree=dir] [--rc2-tree=dir|--rc2-rev=v1.0-rc2|--no-pairwise] [--order=random|cand-first|rc2-first] --expect-hash=sha [--author]';
let INTENT = o.intent || (o['intent-file'] ? fs.readFileSync(o['intent-file'], 'utf8').trim() : null), JOB = o.job || null, SOURCE;
if (!ID) { console.log(USAGE); process.exit(2); }
if (INTENT && o.ledger) { console.log('gate: give the takeaway either from the ledger (--ledger) or with --intent, not both'); process.exit(2); }
if (INTENT) { JOB = JOB || 'function'; SOURCE = { from: 'command line' }; }
else {
  try {
    const L = readLedger(o.ledger ? path.resolve(o.ledger) : LEDGER_DEFAULT), t = ledgerTakeaway(L, ID);
    if (JOB && JOB !== t.job) throw new Error(`--job "${JOB}" is not the ledger's job "${t.job}" for ${ID}`);
    INTENT = t.intent; JOB = t.job; SOURCE = { from: 'ledger', file: L.file, sha256: L.sha256, columns: { takeaway: 'intent', job: 'job' } };
  } catch (e) { console.log(`gate: ${e.message}`); process.exit(2); }
}
if (!INTENT || !['function', 'real thing', 'two-part'].includes(JOB)) { console.log(USAGE); process.exit(2); }
const MODEL = o.model || 'claude-sonnet-5-5';
const VOTES = 3;   // votes per scorer and hedge check (fixed: part of the frozen gate)
const ROOT = tree(o.tree);
const ALL = ['taught', 'judge', 'hedge', 'still', 'stripped', 'pairwise'];
const FULL = ALL.filter(c => !(c === 'pairwise' && o['no-pairwise']));
const CRIT = o.criteria ? String(o.criteria).split(',') : FULL;
// --criteria runs part of the gate (a builder's diagnosis): its verdict says "partial" and is never the gate's verdict
// on a figure, so the author's form (--author) refuses it (calibration section 17), --single too (section 18): only a
// decision's own runs, which the decision below starts with P31_GATE_DECISION_RUN=1 and reads from verdict.json, run it
// in the author's form; and the author's output line of a partial run says "partial" all the same
const PARTIAL = !FULL.every(c => CRIT.includes(c));
const IN_DECISION = !!o.single && process.env.P31_GATE_DECISION_RUN === '1';
if (o.criteria && CRIT.some(c => !ALL.includes(c))) { console.log(`gate: unknown criterion in --criteria=${o.criteria} (${ALL.join(', ')})`); process.exit(2); }
if (PARTIAL && o.author && !IN_DECISION) { console.log('gate: --criteria with --author refused: the author gets only full verdicts (calibration sections 17 and 18)'); process.exit(2); }
const STAMP = new Date().toISOString().replace(/[:.]/g, '-');
const OUTDIR = mkdirp(path.resolve(o.out || path.join(OUT, 'gate', `${ID}-${o.label || 'run'}-${STAMP}`)));
const log = (...a) => { if (!o.author) console.error(...a); };
const V = { id: ID, tree: ROOT, job: JOB, intent: INTENT, intent_source: SOURCE, model: MODEL, label: o.label || null, criteria: {}, stamp: STAMP, ...(PARTIAL ? { partial: CRIT } : {}) };
let SANDBOX = null;

function finish(code) {
  if (SANDBOX) fs.rmSync(SANDBOX, { recursive: true, force: true });
  fs.writeFileSync(path.join(OUTDIR, 'verdict.json'), JSON.stringify(V, null, 1));
  console.log(JSON.stringify(o.author ? { id: ID, pass: V.pass, ...(PARTIAL ? { partial: CRIT } : {}), failed: V.failed } : { id: ID, label: V.label, pass: V.pass, ...(PARTIAL ? { partial: CRIT } : {}), failed: V.failed, failed_all: V.failed_all, ...(V.runs ? { runs: V.runs.map(x => (x.error ? 'ERROR' : x.pass ? 'PASS' : 'FAIL')) } : {}), ...(V.error ? { error: V.error } : {}), verdict: path.join(OUTDIR, 'verdict.json') }));
  process.exit(code);
}
function toolError(msg) { V.pass = false; V.failed = 'error'; V.failed_all = ['error']; V.error = String(msg).slice(0, 2000); finish(2); }
process.on('uncaughtException', e => toolError(e && e.stack || e));
process.on('unhandledRejection', e => toolError(e && e.stack || e));

// the frozen-file check (docs/pass-31-calibration.md section 16): nothing runs unless the fingerprint of the gate's
// files, prompts and model equals the --expect-hash given; a missing or different hash is a refusal (exit 2)
V.fingerprint = await fingerprint(MODEL);
if (!o['expect-hash'] || o['expect-hash'] === true) toolError(`no --expect-hash: the gate runs only against the frozen fingerprint (docs/pass-31-calibration.md; npm run fig:hash)`);
if (o['expect-hash'] !== V.fingerprint.combined) toolError(`gate fingerprint ${V.fingerprint.combined} is not the expected ${o['expect-hash']} (npm run fig:hash)`);

// ---- the decision (docs/pass-31-calibration.md section 14): a figure passes when at least RUNS_NEEDED of RUNS_OF
// independent complete runs pass, each run the whole gate below (fresh renders, fresh testers, its own votes). Runs 1
// and 2 are made in parallel; run 3 only when they disagree, and it decides (the outcome is the one all three would
// give). A run that ends in a tool error is made again once; a second error makes the decision "error" (exit 2).
// This rule applies to every figure the gate judges (fig:dev, fig:validate, Phase 2): --single is one complete run,
// the decision's building block, never a verdict on a figure by itself.
const RUNS_NEEDED = 2, RUNS_OF = 3;
if (!o.single) {
  if (!findFigure(ROOT, ID) || (o.part && findFigure(ROOT, ID).part !== o.part)) { console.log(`gate: no figure ${ID}${o.part ? ' in ' + o.part : ''} in ${ROOT}`); process.exit(2); }
  const base = process.argv.slice(2).filter(a => !/^--(out|label|single)(=|$)/.test(a));
  V.rule = { pass_when: `at least ${RUNS_NEEDED} of ${RUNS_OF} complete runs pass`, runs_needed: RUNS_NEEDED, of: RUNS_OF, third_run: 'only when runs 1 and 2 disagree', error_retry: 1 };
  V.runs = [];
  const one = async (k, again = 0) => {
    const dir = path.join(OUTDIR, `run-${k}${again ? '-again' : ''}`);
    const r = await run('node', [path.join(REPO, 'tests/pass31/gate.mjs'), ...base, '--single', '--author', `--out=${dir}`, `--label=${o.label || 'run'}-run-${k}`], { env: { P31_GATE_DECISION_RUN: '1' } });
    let R = null; try { R = JSON.parse(fs.readFileSync(path.join(dir, 'verdict.json'), 'utf8')); } catch {}
    const err = !R || R.failed === 'error' || r.code === 2 || ![0, 1].includes(r.code);
    if (err && !again) { log(`gate ${ID}: run ${k} ended in a tool error; made again`); return one(k, 1); }
    const row = { k, dir, pass: err ? false : !!R.pass, error: err ? (R && R.error) || (r.out + r.err).slice(-1500) : null, failed: err ? 'error' : R.failed, failed_all: err ? ['error'] : R.failed_all,
      hedge_in: R && R.criteria && R.criteria.hedge ? R.criteria.hedge.failed_in : null,
      pairwise: R && R.criteria && R.criteria.pairwise ? (R.criteria.pairwise.replies ? R.criteria.pairwise.replies.map(x => `${x.order}: ${x.verdict}`) : R.criteria.pairwise.same_frames ? ['SAME (identical frames)'] : ['n/a']) : null,
      fingerprint: R && R.fingerprint ? R.fingerprint.combined : null };
    V.runs.push(row); log(`gate ${ID}: run ${k} ${row.error ? 'ERROR' : row.pass ? 'PASS' : 'FAIL'}${row.failed_all && row.failed_all.length ? ' (' + row.failed_all.join(', ') + ')' : ''}`);
    return row;
  };
  const first = await Promise.all([one(1), one(2)]);
  const rows = first.some(x => x.error) || first[0].pass === first[1].pass ? first : [...first, await one(3)];
  V.runs.sort((a, b) => a.k - b.k);
  const bad = rows.find(x => x.error);
  if (bad) toolError(`run ${bad.k}: ${bad.error}`);
  const passes = rows.filter(x => x.pass).length;
  V.pass = passes >= RUNS_NEEDED;
  if (V.pass) { V.failed = null; V.failed_all = []; }
  else {   // the criteria the failing runs failed, most often first (ties in the gate's order)
    const n = c => rows.filter(x => !x.pass && x.failed_all.includes(c)).length;
    V.failed_all = ALL.filter(c => n(c) > 0).sort((a, b) => n(b) - n(a) || ALL.indexOf(a) - ALL.indexOf(b));
    V.failed = V.failed_all[0] || null;
  }
  V.runs_passed = passes; V.runs_made = rows.length;
  if (rows.some(x => x.fingerprint && x.fingerprint !== V.fingerprint.combined)) toolError('a run reported a different gate fingerprint (the gate changed during the decision)');
  finish(V.pass ? 0 : 1);
}
SANDBOX =fs.mkdtempSync(path.join(os.tmpdir(), 'p31-tester-'));   // the testers' empty working directory, outside any repo
const fig = findFigure(ROOT, ID);
if (!fig || (o.part && fig.part !== o.part)) { console.log(`gate: no figure ${ID}${o.part ? ' in ' + o.part : ''} in ${ROOT}`); process.exit(2); }

// ---- renders --------------------------------------------------------------------------------------------------
async function strip(root, dir, extra = []) {
  mkdirp(dir);
  const r = await run('node', [path.join(REPO, 'tests/pass30/bare.mjs'), `--page=${fig.part}`, `--id=${ID}`, `--out=${dir}`, '--frames=12', '--width=375', ...extra], { env: { FIG_ROOT: root } });
  if (r.code) throw new Error(`bare.mjs failed for ${root}: ${r.out.slice(-600)} ${r.err.slice(-600)}`);
  const fr = framesIn(dir, ID, 375, extra.includes('--no-text'));
  if (fr.length !== 12 && fr.length !== 1) throw new Error(`bare.mjs gave ${fr.length} frames for ${ID} in ${root} (expected 12, or 1 for a figure that does not animate)`);
  const cyc = (r.out.match(/cycle ([\d.]+)s/) || [])[1];
  return { frames: fr, cycle: cyc ? +cyc : null };
}
let rc2Root = null;
if (CRIT.includes('pairwise')) {
  if (o['rc2-tree']) rc2Root = tree(o['rc2-tree']);
  else {   // the rc2 version: this tree's assets with the part page as it is at --rc2-rev (default the v1.0-rc2 tag)
    const rev = o['rc2-rev'] || 'v1.0-rc2';
    const r = await run('git', ['show', `${rev}:public/${fig.part}.html`]);
    if (r.code) toolError(`cannot read ${rev}:public/${fig.part}.html`);
    rc2Root = path.join(OUTDIR, 'rc2-tree') + '/';
    fs.cpSync(PUBLIC, rc2Root, { recursive: true });
    fs.writeFileSync(path.join(rc2Root, `${fig.part}.html`), r.out);
  }
}
log(`gate ${ID}: rendering`);
const [cand, bare, rc2] = await Promise.all([
  strip(ROOT, path.join(OUTDIR, 'frames')),
  CRIT.includes('stripped') || CRIT.includes('hedge') ? strip(ROOT, path.join(OUTDIR, 'frames-notext'), ['--no-text']) : null,
  rc2Root ? strip(rc2Root, path.join(OUTDIR, 'frames-rc2')).catch(e => (findFigure(rc2Root, ID) ? Promise.reject(e) : null)) : null,
]);
const STATIC = cand.frames.length === 1;
V.frames = cand.frames.map(f => path.basename(f.f)); V.cycle = cand.cycle; V.static = STATIC;
if (bare && bare.frames.length !== cand.frames.length) toolError(`text-stripped render has ${bare.frames.length} frames, the figure ${cand.frames.length}`);

// ---- testers --------------------------------------------------------------------------------------------------
const img = f => ({ type: 'image', source: { type: 'base64', media_type: 'image/png', data: fs.readFileSync(f).toString('base64') } });
const frameBlocks = (fr, cycle, who = '') => fr.length === 1 ? [{ type: 'text', text: `${who}the still picture:` }, img(fr[0].f)]
  : fr.flatMap((x, i) => [{ type: 'text', text: `${who}Frame ${i + 1} of ${fr.length}${cycle ? ` (t = ${x.t} s of a ${cycle} s loop)` : ''}:` }, img(x.f)]);
let calls = 0;
async function ask(name, content) {
  const file = path.join(OUTDIR, `${name}.in.jsonl`);
  fs.writeFileSync(file, JSON.stringify({ type: 'user', message: { role: 'user', content } }) + '\n');
  for (let attempt = 1; attempt <= 3; attempt++) {
    calls++;
    const r = await run(CLAUDE, ['-p', '--model', MODEL, '--safe-mode', '--restricted', '--tools', '', '--strict-mcp-config', '--no-session-persistence',
      '--system-prompt', P.SYSTEM, '--input-format', 'stream-json', '--output-format', 'stream-json', '--verbose'], { cwd: SANDBOX, input: fs.readFileSync(file, 'utf8'), timeout: 900000 });
    const res = r.out.split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean).find(m => m.type === 'result');
    const text = res && typeof res.result === 'string' ? res.result : '';
    const used = res ? Object.keys(res.modelUsage || res.model_usage_since_last_result || {}) : [];
    fs.writeFileSync(path.join(OUTDIR, `${name}.out${attempt > 1 ? '.' + attempt : ''}.txt`), text || r.out.slice(-4000) + r.err.slice(-2000));
    const a = text.indexOf('{'), b = text.lastIndexOf('}');
    if (res && !res.is_error && a >= 0 && b > a) {
      try { return { ...JSON.parse(text.slice(a, b + 1)), _model: used }; } catch {}
    }
    log(`  ${name}: unreadable reply (attempt ${attempt})`);
    if (attempt < 3) await new Promise(r => setTimeout(r, 15000 * attempt));   // a rate limit or a CLI self-update passes
  }
  return { _error: `${name}: no readable reply after 3 attempts` };
}
const PACKET = proseUpTo(ROOT, fig);
fs.writeFileSync(path.join(OUTDIR, 'packet.txt'), PACKET);
const text = s => ({ type: 'text', text: s });
const need = c => CRIT.includes(c);

// taught (mechanical)
if (need('taught')) {
  let kt = null;
  try { kt = await runKnownTerms(ROOT, path.join(OUTDIR, 'known-terms.json')); } catch (e) { toolError(e.message); }
  const c = taughtContext(kt, ROOT, fig);
  const bad = c ? svgTexts(fig.svg).flatMap(t => taughtYet(t.s, c.known, kt.glossary, c.prior).map(b => `${b.token} (${b.why})`)) : ['section not in known-terms'];
  V.criteria.taught = { pass: bad.length === 0, untaught: [...new Set(bad)] };
}

// first round in parallel: the describers and the pairwise pair
const order1 = o.order === 'cand-first' ? 'cand' : o.order === 'rc2-first' ? 'rc2' : (crypto.randomInt(2) ? 'cand' : 'rc2');
const same = rc2 && rc2.frames.length === cand.frames.length && rc2.frames.every((x, i) => fs.readFileSync(x.f).equals(fs.readFileSync(cand.frames[i].f)));
const pair = first => {
  const [A, B] = first === 'cand' ? [cand, rc2] : [rc2, cand];
  return [text(P.PAIRWISE(PACKET, A.frames.length, B.frames.length)), ...frameBlocks(A.frames, A.cycle, 'Version A, '), ...frameBlocks(B.frames, B.cycle, 'Version B, ')];
};
// a real thing that does not animate: its still's description stands in for the judge's (review fix 1)
const STAND_IN = STATIC && JOB === 'real thing';
const wantJudge = !STATIC && (need('judge') || need('hedge'));
const wantStill = need('still') || (need('hedge') && STATIC) || (STAND_IN && need('judge'));
const wantStripped = need('stripped') || need('hedge');
log(`gate ${ID}: testers (round 1)${STATIC ? (STAND_IN ? ' (does not animate, real thing: the still stands in for the judge)' : ' (does not animate: judge n/a)') : ''}`);
const [judge, still, stripped, pw1, pw2] = await Promise.all([
  wantJudge ? ask('judge', [text(P.JUDGE(PACKET)), ...frameBlocks(cand.frames, cand.cycle)]) : null,
  wantStill || need('hedge') ? ask('still', [text(P.STILL(PACKET)), { type: 'text', text: 'The still:' }, img(cand.frames[0].f)]) : null,
  wantStripped ? ask('stripped', [text(P.STRIPPED(PACKET, bare.frames.length)), ...frameBlocks(bare.frames, bare.cycle)]) : null,
  need('pairwise') && rc2 && !same ? ask('pairwise-1', pair(order1)) : null,
  need('pairwise') && rc2 && !same ? ask('pairwise-2', pair(order1 === 'cand' ? 'rc2' : 'cand')) : null,
]);

// second round: the scorers and the hedge checks, each on one description. Each check is asked VOTES times (fresh
// sessions, in parallel) and the majority decides: the description is fixed, so the votes only damp the checker's own
// noise in applying its rules.
log(`gate ${ID}: testers (round 2, ${VOTES} votes per check)`);
function strip_(d) { const { _model, ...rest } = d; return rest; }
async function vote(name, content, ok) {
  const r = await Promise.all(Array.from({ length: VOTES }, (_, i) => ask(`${name}-${i + 1}`, content)));
  const err = r.find(x => x._error); if (err) return err;
  const yes = r.filter(ok).length;
  return { votes: r, pass_votes: yes, of: VOTES, pass: yes * 2 > VOTES };
}
const scoreOK = s => String(s.verdict).toUpperCase() === 'PASS';
const hedgeOK1 = h => h.hedged === false && (!h.hedges || h.hedges.length === 0);
const score = (kind, d) => d && !d._error ? vote(`score-${kind}`, [text(P.SCORER({ kind, job: JOB, intent: INTENT, description: strip_(d) }))], scoreOK) : Promise.resolve(d);
const hedge = (kind, d) => d && !d._error ? vote(`hedge-${kind}`, [text(P.HEDGE(kind, strip_(d), JOB))], hedgeOK1) : Promise.resolve(d);
const [sJ, sS, sT, hJ, hS, hT] = await Promise.all([
  need('judge') && !STATIC ? score('judge', judge) : need('judge') && STAND_IN ? score('judge', still) : null,
  need('still') ? score('still', still) : null,
  need('stripped') ? score('stripped', stripped) : null,
  need('hedge') && !STATIC ? hedge('judge', judge) : need('hedge') && STAND_IN ? hedge('judge', still) : null,
  need('hedge') ? hedge('still', still) : null,
  need('hedge') ? hedge('stripped', stripped) : null,
]);
const errors = [judge, still, stripped, pw1, pw2, sJ, sS, sT, hJ, hS, hT].filter(x => x && x._error).map(x => x._error);
if (errors.length) toolError(errors.join('; '));

const passOf = s => !!(s && s.pass);
const hedgeOK = h => !!(h && h.pass);
if (need('judge')) V.criteria.judge = STAND_IN ? { pass: passOf(sJ), stand_in: 'still', note: 'a real thing that does not animate: the still\'s description scored with the judge\'s real-thing rubric', description: still, score: sJ }
  : STATIC ? { pass: true, na: true, note: 'the figure does not animate: its still is the whole figure (criterion still)' } : { pass: passOf(sJ), description: judge, score: sJ };
if (need('hedge')) {
  const per = { ...(STATIC && !STAND_IN ? {} : { judge: { pass: hedgeOK(hJ), check: hJ, ...(STAND_IN ? { stand_in: 'still' } : {}) } }), still: { pass: hedgeOK(hS), check: hS }, stripped: { pass: hedgeOK(hT), check: hT } };
  V.criteria.hedge = { pass: Object.values(per).every(x => x.pass), failed_in: Object.keys(per).filter(k => !per[k].pass), per };
}
if (need('still')) V.criteria.still = { pass: passOf(sS), description: still, score: sS };
if (need('stripped')) V.criteria.stripped = { pass: passOf(sT), description: stripped, score: sT };
if (need('pairwise')) {
  if (!rc2) V.criteria.pairwise = { pass: true, na: true, note: `no ${ID} in the rc2 version: nothing to compare` };
  else if (same) V.criteria.pairwise = { pass: true, same_frames: true, note: 'candidate frames byte-identical to the rc2 frames: SAME, no call' };
  else {
    // in reply 1 the candidate is A when order1 is cand; in reply 2 it is the other letter
    const rc2Letter = (k) => (k === 1 ? (order1 === 'cand' ? 'B' : 'A') : (order1 === 'cand' ? 'A' : 'B'));
    const v = (r, k) => { const b = String(r.better).toUpperCase().trim(); return b === 'SAME' ? 'SAME' : b === rc2Letter(k) ? 'RC2' : 'CANDIDATE'; };
    const a = v(pw1, 1), b = v(pw2, 2);
    V.criteria.pairwise = { pass: !(a === 'RC2' && b === 'RC2'), first_order: order1 === 'cand' ? 'candidate is A' : 'rc2 is A', replies: [{ order: order1 === 'cand' ? 'candidate A' : 'rc2 A', verdict: a, raw: pw1 }, { order: order1 === 'cand' ? 'rc2 A' : 'candidate A', verdict: b, raw: pw2 }] };
  }
}
const failedAll = ALL.filter(c => V.criteria[c] && !V.criteria[c].pass);
V.pass = failedAll.length === 0 && CRIT.every(c => V.criteria[c]);
V.failed = failedAll[0] || null; V.failed_all = failedAll; V.calls = calls;
finish(V.pass ? 0 : 1);
