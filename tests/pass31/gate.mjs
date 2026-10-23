// Pass 31 gate (docs/pass-31-brief.md sections 7, 10, 11, 15; docs/pass-31-calibration.md).
//   npm run fig:gate -- <fig-id> --intent="<intent sentence>" --job="function|real thing|two-part"
//        [--tree=<public dir>] [--part=part-N] [--rc2-tree=<public dir> | --rc2-rev=v1.0-rc2 | --no-pairwise]
//        [--order=random|cand-first|rc2-first] [--criteria=taught,judge,still,stripped,hedge,pairwise] [--out=<dir>]
//        [--model=claude-sonnet-5-5] [--label=<name>] [--author]
// Renders, with tests/pass30/bare.mjs at 375 px: a 12-frame strip sampled evenly across the cycle (frame 1 is the t=0
// still), the same strip with --no-text, and (pairwise) the rc2 version's strip. The judge packet is the book's
// prose up to the figure (every earlier part, and this part up to the card), never its caption, strip, <title> or
// <desc>. Testers are fresh Sonnet 5.5 sessions (claude -p, no tools, safe mode), each seeing only its message:
//   taught    mechanical: every label and object token taught before the figure (lib.mjs taughtYet)
//   judge     (a) the judge describes the 12 frames; (b) the scorer compares that with the intent for the job
//   hedge     (c) any hedge in the judge's description on what changes, why, or the result fails
//   still     (d) the t=0 still alone, judged and scored
//   stripped  (e) the text-stripped strip, judged and scored: does it still show what moves and what causes what
//   pairwise  (f) candidate against its rc2 version, both orders (the first one random unless --order): it fails
//             only when the rc2 version is judged better in both orders. Identical frames skip the call (SAME).
// The intent sentence is passed in by the caller (from the ledger) and only the scorer sees it.
// Output: <out>/verdict.json (every tester's reply, for the gate builder) and on stdout one JSON line
// {"id","pass","failed","failed_all"}; with --author only {"id","pass","failed"}.
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { args, tree, findFigure, readPart, packet as proseUpTo, knownTerms, taughtBefore, taughtYet, svgTexts, run, mkdirp, framesIn, REPO, OUT, PUBLIC, PARTS } from './lib.mjs';
import * as P from './prompts.mjs';

const { pos, o } = args(process.argv.slice(2));
const ID = pos[0];
const JOB = o.job || 'function';
let INTENT = o.intent || (o['intent-file'] ? fs.readFileSync(o['intent-file'], 'utf8').trim() : null);
if (!ID || !INTENT || !['function', 'real thing', 'two-part'].includes(JOB)) {
  console.log('usage: npm run fig:gate -- <fig-id> --intent="..." --job="function|real thing|two-part" [--tree=dir] [--rc2-tree=dir|--rc2-rev=v1.0-rc2|--no-pairwise] [--order=random|cand-first|rc2-first] [--author]');
  process.exit(2);
}
const MODEL = o.model || 'claude-sonnet-5-5';
const ROOT = tree(o.tree);
const ALL = ['taught', 'judge', 'hedge', 'still', 'stripped', 'pairwise'];
const CRIT = o.criteria ? String(o.criteria).split(',') : ALL.filter(c => !(c === 'pairwise' && o['no-pairwise']));
const STAMP = new Date().toISOString().replace(/[:.]/g, '-');
const OUTDIR = mkdirp(path.resolve(o.out || path.join(OUT, 'gate', `${ID}-${o.label || 'run'}-${STAMP}`)));
const SANDBOX = mkdirp(path.join(OUTDIR, 'sandbox'));     // the testers' empty working directory
const fig = findFigure(ROOT, ID);
if (!fig || (o.part && fig.part !== o.part)) { console.log(`gate: no figure ${ID}${o.part ? ' in ' + o.part : ''} in ${ROOT}`); process.exit(2); }
const log = (...a) => { if (!o.author) console.error(...a); };

// ---- renders --------------------------------------------------------------------------------------------------
async function strip(root, dir, extra = []) {
  mkdirp(dir);
  const r = await run('node', [path.join(REPO, 'tests/pass30/bare.mjs'), `--page=${fig.part}`, `--id=${ID}`, `--out=${dir}`, '--frames=12', '--width=375', ...extra], { env: { FIG_ROOT: root } });
  if (r.code) throw new Error(`bare.mjs failed for ${root}: ${r.out.slice(-600)} ${r.err.slice(-600)}`);
  const fr = framesIn(dir, ID, 375, extra.includes('--no-text'));
  const cyc = (r.out.match(/cycle ([\d.]+)s/) || [])[1];
  return { frames: fr, cycle: cyc ? +cyc : null };
}
let rc2Root = null;
if (CRIT.includes('pairwise')) {
  if (o['rc2-tree']) rc2Root = tree(o['rc2-tree']);
  else {   // the rc2 version: this tree's assets with the part page as it is at --rc2-rev (default the v1.0-rc2 tag)
    const rev = o['rc2-rev'] || 'v1.0-rc2';
    const r = await run('git', ['show', `${rev}:public/${fig.part}.html`]);
    if (r.code) { console.log(`gate: cannot read ${rev}:public/${fig.part}.html`); process.exit(2); }
    rc2Root = path.join(OUTDIR, 'rc2-tree') + '/';
    fs.cpSync(PUBLIC, rc2Root, { recursive: true });
    fs.writeFileSync(path.join(rc2Root, `${fig.part}.html`), r.out);
  }
}
log(`gate ${ID}: rendering`);
const [cand, bare, rc2] = await Promise.all([
  strip(ROOT, path.join(OUTDIR, 'frames')),
  CRIT.includes('stripped') ? strip(ROOT, path.join(OUTDIR, 'frames-notext'), ['--no-text']) : null,
  rc2Root ? strip(rc2Root, path.join(OUTDIR, 'frames-rc2')) : null,
]);
if (cand.frames.length !== 12) throw new Error(`expected 12 frames, got ${cand.frames.length} (a static figure renders one: the strip is its still)`);

// ---- testers --------------------------------------------------------------------------------------------------
const img = f => ({ type: 'image', source: { type: 'base64', media_type: 'image/png', data: fs.readFileSync(f).toString('base64') } });
const frameBlocks = (fr, cycle, who = '') => fr.flatMap((x, i) => [{ type: 'text', text: `${who}Frame ${i + 1} of ${fr.length}${cycle ? ` (t = ${x.t} s of a ${cycle} s loop)` : ''}:` }, img(x.f)]);
let calls = 0;
async function ask(name, content) {
  const file = path.join(OUTDIR, `${name}.in.jsonl`);
  fs.writeFileSync(file, JSON.stringify({ type: 'user', message: { role: 'user', content } }) + '\n');
  for (let attempt = 1; attempt <= 3; attempt++) {
    calls++;
    const r = await run('/opt/homebrew/bin/claude', ['-p', '--model', MODEL, '--safe-mode', '--restricted', '--tools', '', '--strict-mcp-config', '--no-session-persistence',
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
  }
  return { _error: 'no readable reply after 3 attempts' };
}
const PACKET = proseUpTo(ROOT, fig);
fs.writeFileSync(path.join(OUTDIR, 'packet.txt'), PACKET);
const text = s => ({ type: 'text', text: s });
const V = { id: ID, tree: ROOT, job: JOB, intent: INTENT, model: MODEL, label: o.label || null, criteria: {}, frames: cand.frames.map(f => path.basename(f.f)), cycle: cand.cycle, stamp: STAMP };

// taught (mechanical)
if (CRIT.includes('taught')) {
  const ktFile = path.join(OUTDIR, 'known-terms.json');
  await run('node', [path.join(REPO, 'scripts/known-terms.mjs'), `--out=${path.relative(REPO, ktFile)}`]);
  const kt = knownTerms(ktFile), known = taughtBefore(kt, fig, readPart(ROOT, fig.part));
  const bad = known ? svgTexts(fig.svg).flatMap(t => taughtYet(t.s, known, kt.glossary, PACKET).map(b => `${b.token} (${b.why})`)) : ['section not in known-terms'];
  V.criteria.taught = { pass: bad.length === 0, untaught: [...new Set(bad)] };
}

// first round in parallel: the judge, the still, the stripped judge, the pairwise pair
const order1 = o.order === 'cand-first' ? 'cand' : o.order === 'rc2-first' ? 'rc2' : (crypto.randomInt(2) ? 'cand' : 'rc2');
const same = rc2 && rc2.frames.length === cand.frames.length && rc2.frames.every((x, i) => fs.readFileSync(x.f).equals(fs.readFileSync(cand.frames[i].f)));
const pair = first => {
  const [A, B] = first === 'cand' ? [cand, rc2] : [rc2, cand];
  return [text(P.PAIRWISE(PACKET)), ...frameBlocks(A.frames, A.cycle, 'Version A, '), ...frameBlocks(B.frames, B.cycle, 'Version B, ')];
};
log(`gate ${ID}: testers (round 1)`);
const need = c => CRIT.includes(c);
const [judge, still, stripped, pw1, pw2] = await Promise.all([
  need('judge') || need('hedge') ? ask('judge', [text(P.JUDGE(PACKET)), ...frameBlocks(cand.frames, cand.cycle)]) : null,
  need('still') ? ask('still', [text(P.STILL(PACKET)), { type: 'text', text: 'The still:' }, img(cand.frames[0].f)]) : null,
  need('stripped') ? ask('stripped', [text(P.STRIPPED(PACKET)), ...frameBlocks(bare.frames, bare.cycle)]) : null,
  need('pairwise') && !same ? ask('pairwise-1', pair(order1)) : null,
  need('pairwise') && !same ? ask('pairwise-2', pair(order1 === 'cand' ? 'rc2' : 'cand')) : null,
]);

// second round: the scorers and the hedge check, each on one description
log(`gate ${ID}: testers (round 2)`);
const score = (kind, d) => d && !d._error ? ask(`score-${kind}`, [text(P.SCORER({ kind, job: JOB, intent: INTENT, description: strip_(d) }))]) : Promise.resolve(d ? { _error: d._error } : null);
function strip_(d) { const { _model, ...rest } = d; return rest; }
const [sJ, sS, sT, hd] = await Promise.all([
  need('judge') ? score('judge', judge) : null,
  need('still') ? score('still', still) : null,
  need('stripped') ? score('stripped', stripped) : null,
  need('hedge') && judge && !judge._error ? ask('hedge', [text(P.HEDGE(strip_(judge)))]) : null,
]);
const passOf = s => !!(s && !s._error && String(s.verdict).toUpperCase() === 'PASS');
if (need('judge')) V.criteria.judge = { pass: passOf(sJ), description: judge, score: sJ };
if (need('hedge')) {
  const unsure = judge && Array.isArray(judge.unsure) ? judge.unsure.filter(Boolean) : [];
  V.criteria.hedge = { pass: !!(hd && !hd._error && hd.hedged === false && (!hd.hedges || hd.hedges.length === 0)), check: hd, unsure };
}
if (need('still')) V.criteria.still = { pass: passOf(sS), description: still, score: sS };
if (need('stripped')) V.criteria.stripped = { pass: passOf(sT), description: stripped, score: sT };
if (need('pairwise')) {
  if (same) V.criteria.pairwise = { pass: true, same_frames: true, note: 'candidate frames byte-identical to the rc2 frames: SAME, no call' };
  else {
    // in reply 1 the candidate is A when order1 is cand; in reply 2 it is the other letter
    const rc2Letter = (k) => (k === 1 ? (order1 === 'cand' ? 'B' : 'A') : (order1 === 'cand' ? 'A' : 'B'));
    const v = (r, k) => !r || r._error ? 'ERROR' : String(r.better).toUpperCase().trim() === 'SAME' ? 'SAME' : String(r.better).toUpperCase().trim() === rc2Letter(k) ? 'RC2' : 'CANDIDATE';
    const a = v(pw1, 1), b = v(pw2, 2);
    V.criteria.pairwise = { pass: !(a === 'RC2' && b === 'RC2') && a !== 'ERROR' && b !== 'ERROR', first_order: order1 === 'cand' ? 'candidate is A' : 'rc2 is A', replies: [{ order: order1 === 'cand' ? 'candidate A' : 'rc2 A', verdict: a, raw: pw1 }, { order: order1 === 'cand' ? 'rc2 A' : 'candidate A', verdict: b, raw: pw2 }] };
  }
}
const failedAll = ALL.filter(c => V.criteria[c] && !V.criteria[c].pass);
V.pass = failedAll.length === 0 && CRIT.every(c => V.criteria[c]);
V.failed = failedAll[0] || null; V.failed_all = failedAll; V.calls = calls;
fs.writeFileSync(path.join(OUTDIR, 'verdict.json'), JSON.stringify(V, null, 1));
console.log(JSON.stringify(o.author ? { id: ID, pass: V.pass, failed: V.failed } : { id: ID, label: V.label, pass: V.pass, failed: V.failed, failed_all: failedAll, verdict: path.join(OUTDIR, 'verdict.json') }));
process.exit(V.pass ? 0 : 1);
