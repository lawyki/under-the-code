import fs from 'node:fs';
const LIB = process.argv[2]; const { PUBLIC, readPart, figures, knownTerms, taughtContext, taughtYet, PARTS } = await import(LIB);
const [, ktFile, takeFile] = process.argv.slice(2);
const kt = knownTerms(ktFile);
const take = new Map(fs.readFileSync(takeFile, 'utf8').trim().split('\n').map(l => l.split('\t')));
let bad = 0;
for (const part of PARTS) {
  const html = readPart(PUBLIC, part);
  for (const f of figures(html, part)) {
    if (!take.has(f.id)) continue;
    const t = take.get(f.id).replace(/^(Function|Real thing):\s*/, '');
    const tc = taughtContext(kt, PUBLIC, f);
    if (!tc) { console.log(f.id, 'NO SECTION'); bad++; continue; }
    const fails = taughtYet(t, tc.known, kt.glossary, tc.prior);
    if (fails.length) { bad++; console.log('FAIL ' + f.id + '  ' + fails.map(b => `${b.token} (${b.why})`).join('; ')); }
  }
}
console.log('fails', bad);
