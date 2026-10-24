// Pass 31 taught-yet unit cases (docs/pass-31-calibration.md section 13): the rules of tests/pass31/lib.mjs taughtYet
// on fixed label strings, each placed at a real figure of a tree, so "before the figure" is the book's own prose.
//   npm run fig:taught-test [-- --tree=<public dir>]
// Exit 0 when every case holds, 1 otherwise. Each case: the figure that sets the position, the label text, and the
// tokens expected to fail (an empty list: every token passes).
import path from 'node:path';
import { args, tree, findFigure, readPart, packet, knownTerms, taughtBefore, taughtYet, svgTexts, run, mkdirp, REPO, OUT } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const ROOT = tree(o.tree);
const KT_FILE = path.join(mkdirp(path.join(OUT, 'taught-test')), 'known-terms.json');
const r = await run('node', [path.join(REPO, 'scripts/known-terms.mjs'), `--out=${path.relative(REPO, KT_FILE)}`, `--public=${ROOT}`]);
if (r.code) { console.log('taught-test: known-terms failed', r.err); process.exit(2); }
const kt = knownTerms(KT_FILE);

const CASES = [
  // item 1: all-capitals tokens. The nine dictionary words that are abbreviations fail before the prose teaches them.
  ['fig-1-1', 'AL AX ARM RAM MAC OS NAT LAN DOS', ['AL', 'AX', 'ARM', 'RAM', 'MAC', 'OS', 'nat', 'LAN', 'DOS']],
  // ... and pass where the prose has taught them (ARM at ch1-cpu-p4; RAM at ch1-memory-p2; OS at ch1-memory-p2)
  ['fig-3-2', 'ARM RAM OS CPU', []],
  // AX and AL are first written in Fig 3.3's own caption and strip, never in the prose before it; RAX is taught (ch3-registers-p2)
  ['fig-3-3', 'RAX AX AL', ['AX', 'AL']],
  // CR3 is taught at chBridge-mode-p4, before Fig BR.4 and Fig 4.8
  ['fig-br-4', 'CR3', []],
  ['fig-4-8', 'CR3 CPU', []],
  // TCP's state names are taught at ch10-handshake-p3: after Fig 10.2's card, before Fig 10.3's
  ['fig-10-2', 'SYN_SENT FIN_WAIT_1', ['SYN_SENT', 'FIN_WAIT_1']],
  ['fig-10-3', 'SYN_SENT SYN_RCVD FIN_WAIT_1 FIN_WAIT_2 CLOSE_WAIT LAST_ACK TIME_WAIT SYN-ACK ESTABLISHED LISTEN', []],
  ['fig-10-3', 'TCP IP HTTP DNS', []],
  // never taught in prose (CGNAT and IHL only in captions, labels and strips): they fail
  ['fig-9-8', 'CGNAT', ['cgnat']],
  ['fig-9-4', 'IHL', ['ihl']],
  // a common word or an everyday word set in capitals
  ['fig-1-1', 'THE MACHINE · TAPE · HEAD', []],
  ['fig-1-2', 'KEY · LAMP · ROTORS · REFLECTOR · PRESS A THREE TIMES', []],
  // an abbreviation the prose has not yet taught, before its paragraph
  ['fig-1-1', 'CPU', ['CPU']],
  // item 2: inflections pass when their stem does
  ['fig-1-1', 'lowest became rewritten databases written overwritten largest easiest shown held began', []],
  // ... and an inflection of a glossary term the figure has not taught fails like the term
  ['fig-1-1', 'kernels', ['kernels']],
  // item 3: a term first taught in the figure's own caption is not taught for that figure, even when every word of it
  // is an everyday word (Fig 1.14: Ring 3, Ring 0, system call)
  ['fig-1-14', 'Ring 3 · Ring 0 · system call', ['ring 3', 'ring 0', 'system call']],
  // a hyphenated term needs its hyphen: "a machine" is everyday English
  ['fig-1-1', 'a machine', []],
  // review fix 2 (docs/pass-31-calibration.md section 15): the same abbreviations in lower and title case fail before
  // they are taught (the dictionary does not make them everyday words), and so do s plurals of the book's capitals
  ['fig-1-1', 'ax al arm ram mac os lan dos', ['ax', 'al', 'arm', 'ram', 'mac', 'os', 'lan', 'dos']],
  ['fig-1-1', 'Ax Al Arm Ram Mac Os Lan Dos', ['ax', 'al', 'arm', 'ram', 'mac', 'os', 'lan', 'dos']],
  ['fig-1-1', 'rams macs arms', ['rams', 'macs', 'arms']],
  // ... while COMMON words the book also writes in capitals, their inflections and other everyday words pass
  ['fig-1-1', 'add adds added adding puts gets not non-volatile re-read Mar 10 ms', []],
  // ... and the taught forms pass once the prose has taught them, a short term's plural only written as the abbreviation
  ['fig-3-2', 'ram os arm rams arms CPUs RAMs OSes', []],
  ['fig-10-3', 'IPs', []],
  ['fig-10-3', 'ips', ['ips']],
  // RAX is taught at ch3-registers-p2, after Fig 3.1; CSS is never "CS" plus s; LO and AST before they are taught
  ['fig-3-1', 'add rax, 5', ['rax']],
  ['fig-11-14', 'css', ['css']],
  ['fig-8-5', 'lo', ['lo']],
  ['fig-4-1', 'ast', ['ast']],
];
let bad = 0;
for (const [id, label, expect] of CASES) {
  const fig = findFigure(ROOT, id);
  if (!fig) { console.log(`MISS ${id}: not in ${ROOT}`); bad++; continue; }
  const known = taughtBefore(kt, fig, readPart(ROOT, fig.part));
  const got = [...new Set(taughtYet(label, known, kt.glossary, packet(ROOT, fig)).map(b => b.token))];
  const ok = got.length === expect.length && expect.every(t => got.includes(t));
  if (!ok) bad++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${id.padEnd(9)} ${JSON.stringify(label)} -> fails ${JSON.stringify(got)}${ok ? '' : ` (expected ${JSON.stringify(expect)})`}`);
}
// the figures themselves: Fig 1.1 (v4) and Fig 1.2 (Enigma) as they stand in the tree
for (const id of ['fig-1-1', 'fig-1-2']) {
  const fig = findFigure(ROOT, id), known = taughtBefore(kt, fig, readPart(ROOT, fig.part));
  const got = svgTexts(fig.svg).flatMap(t => taughtYet(t.s, known, kt.glossary, packet(ROOT, fig)).map(b => b.token));
  if (got.length) bad++;
  console.log(`${got.length ? 'FAIL' : 'ok  '} ${id.padEnd(9)} (the figure's own text) -> fails ${JSON.stringify(got)}`);
}
console.log(`taught-test: ${CASES.length + 2 - bad} of ${CASES.length + 2} cases hold`);
process.exit(bad ? 1 : 0);
