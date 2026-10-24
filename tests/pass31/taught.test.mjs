// Pass 31 taught-yet unit cases (docs/pass-31-calibration.md sections 13, 15, 16, 17): the rules of tests/pass31/lib.mjs
// taughtYet on fixed label strings, each placed at a real figure of a tree, so "before the figure" is the book's own
// prose (held material stripped: known-terms runs with --strip, lib.mjs taughtContext). Section 16 adds the cases of
// its items 2a to 2e: same-section teaching before the card, the glossary placement (prose glosses), tokens taught by
// the prose before the card, everyday words that are glossary terms (still failing), and the regressions that must
// still fail. Section 17 (the review of the section 16 freeze) adds its defects 1 to 7: the name rules (no mention of
// a term taught only in held material or nowhere, of a term that is not a name, or in a heading or chapter preview
// credits it), EAX before ch3-registers, teaching only in paragraphs and list items (never a section label, heading,
// table cell or code block), inflections without a stripped prefix, HTTPS not a plural of HTTP, no taught exemption,
// and synthetic cases for the name rule.
//   npm run fig:taught-test [-- --tree=<public dir>]
// Exit 0 when every case holds, 1 otherwise. Each case: the figure that sets the position, the label text, and the
// tokens expected to fail (an empty list: every token passes).
import fs from 'node:fs'; import path from 'node:path';
import { args, tree, findFigure, runKnownTerms, taughtContext, taughtYet, svgTexts, mkdirp, OUT, REPO } from './lib.mjs';

const { o } = args(process.argv.slice(2));
const ROOT = tree(o.tree);
const KT_FILE = path.join(mkdirp(path.join(OUT, 'taught-test')), 'known-terms.json');
let kt; try { kt = await runKnownTerms(ROOT, KT_FILE); } catch (e) { console.log('taught-test:', e.message); process.exit(2); }

const CASES = [
  // item 1: all-capitals tokens. The nine dictionary words that are abbreviations fail before the prose teaches them.
  ['fig-1-1', 'AL AX ARM RAM MAC OS NAT LAN DOS', ['AL', 'AX', 'ARM', 'RAM', 'MAC', 'OS', 'nat', 'LAN', 'DOS']],
  // ... and pass where the prose has taught them (ARM at ch1-cpu-p4; RAM at ch1-memory-p2; OS, which the book writes
  // first in a summary table and in a paragraph only at ch3-stack-p1, from Fig 3.5: section 17)
  ['fig-3-2', 'ARM RAM CPU', []],
  ['fig-3-5', 'ARM RAM OS CPU', []],
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
  ['fig-3-2', 'ram arm rams arms CPUs RAMs', []],
  ['fig-3-5', 'ram os arm rams arms CPUs RAMs OSes', []],
  ['fig-10-3', 'IPs', []],
  ['fig-10-3', 'ips', ['ips']],
  // RAX is taught at ch3-registers-p2, after Fig 3.1; CSS is never "CS" plus s; LO and AST before they are taught
  ['fig-3-1', 'add rax, 5', ['rax']],
  ['fig-11-14', 'css', ['css']],
  ['fig-8-5', 'lo', ['lo']],
  ['fig-4-1', 'ast', ['ast']],

  // ---- section 16, item 2a: a term known-terms lists as first taught in the figure's own section passes when the
  // prose teaches it before the card (doping and semiconductor at ch1-transistor-p6 and p7, before Fig 1.5;
  // pipelining at ch1-cpu-p6, before Fig 1.11; instruction set architecture at ch1-cpu-p4, before Fig 1.10), and an
  // inflection of a taught term passes like the term (pipelined; registered once register is taught)
  ['fig-1-5', 'doping · semiconductor', []],
  ['fig-1-11', 'pipelining · pipelined', []],
  ['fig-1-10', 'instruction set architecture', []],
  ['fig-br-1', 'registered', []],
  // ... and fails when its section teaches it only after the card (2e)
  ['fig-1-4', 'doping · semiconductor', ['doping', 'semiconductor']],
  ['fig-1-10', 'pipelining', ['pipelining']],
  ['fig-1-9', 'instruction set architecture', ['instruction set architecture']],
  ['fig-4-8', 'mmap', ['mmap']],
  // ---- item 2b: the glossary placement. known-terms teaches a term at its first prose gloss when that comes before
  // the glossary's section: register (ch1-vonneumann-p4) and byte (ch1-cpu-p2) before Fig 1.10, compiler
  // (ch1-vonneumann-p3) before Fig 3.4, thread (ch7-gil-p1) before Figs 7.4 and 7.5 (the PLACED list below checks
  // the paragraph each is placed at)
  ['fig-1-10', 'register · registers · byte · bytes', []],
  ['fig-3-4', 'compiler', []],
  ['fig-7-4', 'thread · threads · threaded', []],
  ['fig-7-5', 'thread', []],
  // ---- item 2c: a token that is not a glossary term and not an everyday word passes when a paragraph or list item
  // of the prose before the card holds it (as written, or an inflection); mov needs "mov" itself (ch1-cpu-p5)
  ['fig-8-4', 'bandwidth', []],
  ['fig-12-1', 'applet', []],
  ['fig-12-3', 'microtask · microtasks', []],
  ['fig-16-8', 'speedup', []],
  ['fig-16-9', 'speedup', []],
  ['fig-5-1', 'int', []],
  ['fig-1-10', 'mov', []],
  ['fig-3-2', 'mov', []],
  ['fig-3-3', 'mov', []],
  // ... and fails before that prose (mov and int are first written after Figs 1.9 and 3.4; bandwidth after Fig 8.3;
  // applet after Fig 11.14; speedup, as "speedups", after Fig 13.2)
  ['fig-1-9', 'mov', ['mov']],
  ['fig-3-4', 'int', ['int']],
  ['fig-8-3', 'bandwidth', ['bandwidth']],
  ['fig-11-14', 'applet', ['applet']],
  ['fig-13-2', 'speedup', ['speedup']],
  // ---- item 2d: an everyday word that is also a glossary term keeps failing until known-terms places its teaching
  // before the figure: plain uses in the prose before (safety at ch4-anatomy-p4, releases at ch6-raii-p1, groups at
  // ch4-fs-p1) teach nothing (the synthetic case below covers key, bucket, port, node, edge, toss)
  ['fig-4-1', 'safety', ['safety']],
  ['fig-4-2', 'safety', ['safety']],
  ['fig-5-11', 'safety', ['safety']],
  ['fig-6-5', 'release · released', ['release', 'released']],
  ['fig-9-9', 'group · groups', ['group', 'groups']],
  // ---- item 2e: regressions that must still fail
  // EAX before the prose teaches it (first written at ch1-cpu-p5, after Fig 1.9)
  ['fig-1-8', 'EAX', ['EAX']],
  ['fig-1-9', 'EAX', ['EAX']],
  ['fig-1-9', 'mov eax, 5', ['mov', 'eax']],
  // CGNAT and IHL: written only in figure cards (captions, labels, strips), never in the prose, so they fail at every
  // figure, the book's last included (a glossary entry whose section writes the term only in a card teaches nothing)
  ['fig-9-9', 'CGNAT · IHL', ['cgnat', 'ihl']],
  ['fig-18-6', 'CGNAT · IHL', ['cgnat', 'ihl']],
  // a token written only in the figure's own caption or strip (ARM's STUR and LDUR at Fig 3.2; execve at Fig 4.10;
  // vptr at Fig 6.3), as Ring 0 and system call at Fig 1.14 above
  ['fig-3-2', 'stur · ldur', ['stur', 'ldur']],
  ['fig-4-10', 'execve', ['execve']],
  ['fig-6-3', 'vptr', ['vptr']],
  // lower-case abbreviations where untaught, beside the cases above: js before JS is taught (the prose's "Node.js" is
  // one token, not js), css (the prose's "/style.css" is one token)
  ['fig-12-1', 'js', ['js']],
  ['fig-11-14', 'css · js', ['css', 'js']],
  ['fig-3-3', 'ax · al', ['ax', 'al']],

  // ---- section 17 (the review of the section 16 freeze), defect 1: the name rules. A glossary term is credited by
  // being mentioned only when known-terms lists it as a name (a person, place, organisation, paper or product), and
  // only when a paragraph or list item before the card writes it (never a heading, section label, table or chapter
  // preview). Taught only in held material or nowhere: never credited (SQL injection, SYN flood, SHA-256 in held
  // material only; Reno nowhere), not even at the book's last figure
  ['fig-18-6', 'SQL injection · SYN flood · SHA-256 · Reno', ['sql injection', 'syn flood', 'sha 256', 'reno']],
  // not name-shaped (a word in capitals, a digit): fails until taught, however often it is mentioned (IEEE 754 in the
  // Part I chapter preview; TLS handshake, CAP theorem, IP header in paragraphs before their teaching)
  ['fig-1-1', 'IEEE 754', ['ieee 754']],
  ['fig-3-1', 'TLS handshake', ['tls handshake']],
  ['fig-16-1', 'CAP theorem', ['cap theorem']],
  ['fig-8-1', 'IP header', ['ip header']],
  // ... and passes once taught (IEEE 754 at ch2-float-p7, before Fig 2.11; TLS handshake at ch11-crypto-p1, before
  // Fig 11.8; CAP theorem at ch17-cap-p1, before Fig 17.7; IP header at ch9-ip-p1, before Fig 9.4)
  ['fig-2-11', 'IEEE 754', []],
  ['fig-11-8', 'TLS handshake', []],
  ['fig-17-7', 'CAP theorem', []],
  ['fig-9-4', 'IP header', []],
  // named methods and laws, and a common noun opening a sentence, are not names: Diffie–Hellman (an en dash joins the
  // pair), Amdahl's law (a possessive law), Promises (the book writes promise in lower case)
  ['fig-11-11', 'Diffie–Hellman', ['diffie hellman']],
  ['fig-16-2', "Amdahl's law", ["amdahl's law"]],
  ['fig-12-2', 'Promises', ['promises']],
  // names pass once a paragraph before the card writes them (Bell Labs, Shannon, Diffie, von Neumann), and not when
  // only a heading or chapter preview does (von Neumann before Fig 1.1)
  ['fig-1-3', 'Bell Labs', []],
  ['fig-2-2', 'Shannon', []],
  ['fig-11-10', 'Diffie', []],
  ['fig-1-8', 'von Neumann', []],
  ['fig-1-1', 'von Neumann', ['von neumann']],
  // ---- defect 2: EAX is never taught before ch3-registers: the book writes it first in a code comment (a <pre> block,
  // which teaches nothing) after ch1-cpu-p5, in Fig 3.3's own caption, then in a paragraph at ch3-call-p3; and eax in
  // ch1-cpu-p5's "mov eax, 5" is the operand of a <code> span, which teaches nothing (mov, the span's first word, does)
  ...['fig-1-10', 'fig-2-5', 'fig-3-1', 'fig-3-2'].flatMap(id => [[id, 'EAX', ['EAX']], [id, 'eax', ['eax']]]),
  ['fig-1-10', 'mov eax, 5', ['eax']],
  ['fig-3-6', 'EAX', []],
  ['fig-3-6', 'eax', []],
  // ---- defect 3: a term is taught in its section's paragraphs and list items, never by its section label, heading or a
  // table cell: each of these is credited only from such a place before the card, so it fails
  ['fig-1-13', 'kernel', ['kernel']],
  ['fig-10-4', 'congestion control', ['congestion control']],
  ['fig-10-7', 'BBR', ['bbr']],
  ['fig-17-9', 'serverless', ['serverless']],
  ['fig-17-10', 'serverless', ['serverless']],
  ['fig-5-9', 'undefined behaviour', ['undefined behaviour']],
  ['fig-6-3', 'OO', ['OO']],
  ['fig-6-4', 'OO', ['OO']],
  // ... and each passes from the first figure after a paragraph teaches it (kernel at ch1-kernel-p3; congestion
  // control's key-term at ch10-aimd-p4; BBR at ch10-modern-p4; serverless, undefined behaviour in their sections later)
  ['fig-1-14', 'kernel', []],
  ['fig-10-5', 'congestion control', []],
  ['fig-10-8', 'BBR', []],
  ['fig-17-11', 'serverless', []],
  ['fig-5-10', 'undefined behaviour', []],
  // tables do not teach: OS and the scheduling policies are written before Figs 3.2 and 4.5 only in table cells
  ['fig-3-2', 'OS', ['OS']],
  ['fig-4-5', 'FCFS · SJF · MLFQ', ['FCFS', 'SJF', 'MLFQ']],
  // ---- defect 4: an inflection of a taught term is by plain endings only, never by a stripped prefix
  ['fig-17-6', 'subprocess · subthreads · substack · unpipelined', ['subprocess', 'subthreads', 'substack', 'unpipelined']],
  // ... and a prefixed word is a word of its own, not the glossary term inside it: SubBytes (the prose names it before
  // Fig 14.5) passes as any token the prose writes; everyday prefixed words pass; the prose writing kernel does not
  // teach unkernel
  ['fig-14-5', 'SubBytes', []],
  ['fig-1-1', 'upload · subsystem · unpaid · rewrite', []],
  ['fig-1-14', 'unkernel', ['unkernel']],
  // ---- defect 5: HTTPS is not a plural of HTTP (the book writes HTTPS as its own abbreviation, first at ch11-http-p1)
  ['fig-4-19', 'HTTPS', ['https']],
  ['fig-4-19', 'HTTP', []],
  ['fig-11-2', 'HTTPS', []],
];
// item 2b: the paragraph known-terms places each term at (the first prose gloss)
const PLACED = { register: 'ch1-vonneumann-p4', byte: 'ch1-cpu-p2', compiler: 'ch1-vonneumann-p3', thread: 'ch7-gil-p1' };
// item 2d, synthetic: everyday words made glossary terms (key, bucket, port, node, edge, toss, release, group,
// safety), not yet taught, each also in the prose before and in its tokens: every one fails as a glossary term
const EVERYDAY_GLOSSARY = ['key', 'bucket', 'port', 'node', 'edge', 'toss', 'release', 'group', 'safety'];
let bad = 0, n = 0;
const check = (ok, line) => { n++; if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${line}`); };
for (const [id, label, expect] of CASES) {
  const fig = findFigure(ROOT, id);
  if (!fig) { check(false, `${id}: not in ${ROOT}`); continue; }
  const c = taughtContext(kt, ROOT, fig);
  const got = [...new Set(taughtYet(label, c.known, kt.glossary, c.prior).map(b => b.token))];
  const ok = got.length === expect.length && expect.every(t => got.includes(t));
  check(ok, `${id.padEnd(9)} ${JSON.stringify(label)} -> fails ${JSON.stringify(got)}${ok ? '' : ` (expected ${JSON.stringify(expect)})`}`);
}
for (const [t, p] of Object.entries(PLACED)) {
  const e = kt.j.taught[t];
  check(e && e.paragraph === p && /^prose gloss/.test(e.source), `placed  ${t} at ${e && e.paragraph} (${e && e.source}; expected ${p}, a prose gloss)`);
}
{
  const g = new Set(EVERYDAY_GLOSSARY); g.names = new Set(); g.multi = []; g.capitals = new Set(); g.forms = new Map(EVERYDAY_GLOSSARY.map(t => [t, t])); g.noMention = new Set();
  const text = EVERYDAY_GLOSSARY.join(' '), prior = { exact: new Set(EVERYDAY_GLOSSARY), lower: new Set(EVERYDAY_GLOSSARY), text };
  const got = [...new Set(taughtYet(text, [], g, prior).filter(b => b.why === 'a glossary term not yet taught').map(b => b.token))];
  check(got.length === EVERYDAY_GLOSSARY.length, `synthetic ${JSON.stringify(text)} as untaught glossary terms, in the prose before -> fail as glossary terms ${JSON.stringify(got)}`);
}
// section 17, synthetic: the name rule on its own. A name passes only when it is in glossary.names (known-terms
// "names", less noMention) and the prose before the card (prior.text: paragraphs and list items) writes it as the
// entry writes it; a name-shaped term known-terms does not list as a name fails even when written there
{
  const mk = (names) => { const t = ['qzname labs', 'qzsolo', 'qzother labs']; const g = new Set(t); g.names = new Set(names); g.capitals = new Set(); g.noMention = new Set();
    g.forms = new Map([['qzname labs', 'Qzname Labs'], ['qzsolo', 'Qzsolo'], ['qzother labs', 'Qzother Labs']]); g.multi = [{ t: 'qzname labs', form: 'Qzname Labs' }, { t: 'qzother labs', form: 'Qzother Labs' }]; return g; };
  const label = 'Qzname Labs · Qzsolo · Qzother Labs', text = 'We met Qzname Labs and Qzsolo, and Qzother Labs.';
  const prior = t => ({ exact: new Set(), lower: new Set(), text: t });
  const run = (g, t) => [...new Set(taughtYet(label, [], g, prior(t)).map(b => b.token))].sort();
  const a = run(mk(['qzname labs', 'qzsolo']), text), b = run(mk(['qzname labs', 'qzsolo']), 'We met qzname labs.'), c = run(mk([]), text);
  check(JSON.stringify(a) === JSON.stringify(['qzother labs']), `synthetic names written in a paragraph before: listed names pass, the unlisted one fails -> fails ${JSON.stringify(a)}`);
  check(JSON.stringify(b) === JSON.stringify(['qzname labs', 'qzother labs', 'qzsolo']), `synthetic names not written (or only in lower case) before -> fail ${JSON.stringify(b)}`);
  check(JSON.stringify(c) === JSON.stringify(['qzname labs', 'qzother labs', 'qzsolo']), `synthetic names written before but not listed as names (taught nowhere, held only, or not name-shaped) -> fail ${JSON.stringify(c)}`);
  let threw = false; try { taughtYet('x', [], mk([]), 'a packet string'); } catch { threw = true; }
  check(threw, 'taughtYet refuses the packet as its fourth argument (the mention rules read paragraphs only)');
}
// known-terms "names" on this tree: never a term with a word in capitals, a digit or an en dash, never one taught
// nowhere or only in held material
{
  const bad = kt.j.names.filter(n => /\p{N}|–/u.test(n) || n.split(/[\s-]+/).some(w => w.length >= 2 && w === w.toUpperCase() && /\p{Lu}/u.test(w))
    || kt.j.taught_nowhere.includes(n) || (kt.j.strip.glossary_terms_only_in_held || []).includes(n));
  check(!bad.length && kt.j.names.length > 0, `names: ${kt.j.names.length} listed, ${bad.length} breaking the name rule`);
}
// section 17, defect 6: no per-figure taught exemption. docs/pass-31-exempt.json holds only the brief's exemptions
// (label_cap, floor, caption), and tests/pass31/check.mjs takes no other
{
  const EX = JSON.parse(fs.readFileSync(path.join(REPO, 'docs/pass-31-exempt.json'), 'utf8'));
  const other = Object.keys(EX).filter(k => !['note', 'at_bar', 'kept', 'label_cap', 'floor', 'caption'].includes(k));
  const src = fs.readFileSync(path.join(REPO, 'tests/pass31/check.mjs'), 'utf8');
  check(!other.length && !/exempt\('(taught|desc|strip|band)'/.test(src) && /const EXEMPTABLE = \['label_cap', 'floor', 'caption'\];/.test(src),
    `exemptions: keys beyond the brief's ${other.length}; check.mjs exempts only label_cap, floor, caption`);
}
// the figures themselves: Fig 1.1 (v4) and Fig 1.2 (Enigma) as they stand in the tree
for (const id of ['fig-1-1', 'fig-1-2']) {
  const fig = findFigure(ROOT, id), c = taughtContext(kt, ROOT, fig);
  const got = svgTexts(fig.svg).flatMap(t => taughtYet(t.s, c.known, kt.glossary, c.prior).map(b => b.token));
  check(!got.length, `${id.padEnd(9)} (the figure's own text) -> fails ${JSON.stringify(got)}`);
}
console.log(`taught-test: ${n - bad} of ${n} cases hold`);
process.exit(bad ? 1 : 0);
