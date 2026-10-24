// Pass 31 gate fingerprint (docs/pass-31-calibration.md, "Frozen"). The gate's behaviour lives in its prompts, in the
// code that renders, packs and scores, in the CLI that runs the testers and in the model id, so the freeze records all
// of them:
//   prompts   sha256 of each prompt as rendered with placeholder inputs (prompts.mjs frozenTexts(): system, judge,
//             scorer, hedge, still (t=0), stripped (text-stripped), pairwise)
//   files     sha256 of every file the gate runs: tests/pass31/{gate,prompts,lib,hash}.mjs, tests/pass31/common-words.txt,
//             tests/pass30/bare.mjs, scripts/known-terms.mjs, the sealed validation runner tests/pass31/validate.mjs
//             (its bars and its takeaway source; review fix 4), and the held-material strip, tests/pass31/held.mjs and
//             its list tests/pass31/held-strip.json (calibration section 16)
//   model     the tester model id
//   combined  sha256 of prompts, files and model (sorted JSON); gate.mjs writes it into every verdict; gate.mjs,
//             dev.mjs and validate.mjs refuse to run (exit 2) unless --expect-hash is given and equals it
//   cli       `claude --version`, recorded beside the hash but not in it: the CLI updates itself, so a version change
//             is reported (verdict.json, fig:validate) rather than blocking a run
//   npm run fig:hash [-- --model=claude-sonnet-5-5] [--json]
import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { run, REPO } from './lib.mjs';
import { frozenTexts } from './prompts.mjs';

export const CLAUDE = '/opt/homebrew/bin/claude';
export const GATE_FILES = ['tests/pass31/gate.mjs', 'tests/pass31/prompts.mjs', 'tests/pass31/lib.mjs', 'tests/pass31/hash.mjs', 'tests/pass31/common-words.txt', 'tests/pass30/bare.mjs', 'scripts/known-terms.mjs', 'tests/pass31/validate.mjs',
  'tests/pass31/held.mjs', 'tests/pass31/held-strip.json'];
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const sorted = o => JSON.stringify(o, Object.keys(o).sort());

export async function fingerprint(model = 'claude-sonnet-5-5') {
  const prompts = Object.fromEntries(Object.entries(frozenTexts()).map(([k, v]) => [k, sha(v)]));
  const files = Object.fromEntries(GATE_FILES.map(f => [f, sha(fs.readFileSync(path.join(REPO, f)))]));
  const r = await run(CLAUDE, ['--version'], { cwd: '/' });
  const cli = r.out.trim();
  const combined = sha(sorted({ prompts: sorted(prompts), files: sorted(files), model }));
  return { prompts, files, cli, model, combined };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const m = (process.argv.find(a => a.startsWith('--model=')) || '').slice(8) || 'claude-sonnet-5-5';
  const f = await fingerprint(m);
  if (process.argv.includes('--json')) console.log(JSON.stringify(f, null, 1));
  else {
    for (const [k, v] of Object.entries(f.prompts)) console.log(`prompt  ${k.padEnd(9)} ${v}`);
    for (const [k, v] of Object.entries(f.files)) console.log(`file    ${v}  ${k}`);
    console.log(`cli     ${f.cli}\nmodel   ${f.model}\ncombined ${f.combined}`);
  }
}
