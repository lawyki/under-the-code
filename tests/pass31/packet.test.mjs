// Pass 31 held material out of the judge packets (docs/pass-31-calibration.md section 16, item 1).
//   npm run fig:packet-test [-- --tree=<public dir>] [--ledger=<the author's docs/pass-31-ledger.tsv>]
// Checks, on a tree, with the strip list tests/pass31/held-strip.json (ids only; this test never prints content):
//   list     every listed figure, chapter, section and paragraph id exists in the tree; every section whose only
//            figures are held (found by structure) is in sections.held_only; a listed paragraph that sits inside a
//            figure card sits inside a held card; no strip zone cuts into a figure that is not held
//   ledger   (calibration section 18) the ledger's held ids (rows with status "held", read by header name) are exactly
//            held_figures, and sections.held_only is exactly the set of sections whose figures in the tree are all
//            held by the ledger (a section with no figure is not one): nothing missing, nothing extra. The gate
//            branch keeps no ledger, so --ledger names the author's; without one the check fails
//   packets  every non-held figure's packet (lib.mjs packet) and its prose tokens (priorTokens) are built; no run of
//            eight words that only held material holds (a held card's label, picture text, caption or strip; a listed
//            chapter, section or paragraph; a toc card to them) appears in any of them
//   markers  a scratch copy of the tree gets a unique marker inside every strip zone (a word, an all-capitals token
//            and a key-term span); no marker reaches any non-held packet or prose-token set, and known-terms.mjs
//            --strip teaches none of them (no known or defines entry, no abbreviation); as a control, known-terms
//            without --strip does list the zones' abbreviation markers, so the check is not empty
//   names    (calibration section 17) the same zones also get two name-shaped markers (one word, two words), each made
//            a glossary entry of the zone's section in the scratch glossary: known-terms --strip lists none of them as a
//            name, and taught-yet fails every one of them at every non-held figure (the mention rules credit nothing
//            from held material); controls: without --strip they are names, and a name planted in a paragraph before
//            Fig 1.1 (taught at ch18-final) passes at Fig 1.1 while a term with a word in capitals planted beside it fails
// Exit 0 when every check holds, 1 otherwise, 2 when the tree cannot be read.
import fs from 'node:fs'; import path from 'node:path';
import { args, tree, allFigures, figures, readPart, packet, priorTokens, plain, loadHeld, run, mkdirp, runKnownTerms, taughtContext, taughtYet, readLedger, LEDGER_DEFAULT, PARTS, REPO, OUT, HELD_FILE } from './lib.mjs';
import { heldZones, CARD } from './held.mjs';

const { o } = args(process.argv.slice(2));
const ROOT = tree(o.tree);
const H = loadHeld();
let bad = 0, n = 0;
const check = (ok, line) => { n++; if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${line}`); };
let html;
try { html = Object.fromEntries(PARTS.map(p => [p, readPart(ROOT, p)])); } catch (e) { console.log(`packet-test: ${e.message}`); process.exit(2); }

// ---- list --------------------------------------------------------------------------------------------------------
const figs = allFigures(ROOT), ids = new Set(figs.map(f => f.id));
check([...H.figures].every(id => ids.has(id)), `list: held figures found in the tree ${[...H.figures].filter(id => ids.has(id)).length} of ${H.figures.size}${[...H.figures].some(id => !ids.has(id)) ? ` (missing ${[...H.figures].filter(id => !ids.has(id)).join(' ')})` : ''}`);
const all = Object.values(html).join('\n');
const missing = H.elements.filter(id => !all.includes(`id="${id}"`));
check(!missing.length, `list: chapter, section and paragraph ids found ${H.elements.length - missing.length} of ${H.elements.length}${missing.length ? ` (missing ${missing.join(' ')})` : ''}`);
const bySec = new Map();
for (const f of figs) { if (!bySec.has(f.section)) bySec.set(f.section, []); bySec.get(f.section).push(f.id); }
const heldOnly = [...bySec].filter(([, xs]) => xs.every(x => H.figures.has(x))).map(([s]) => s);
const unlisted = heldOnly.filter(s => !H.sections.includes(s));
check(!unlisted.length, `list: sections whose only figures are held ${heldOnly.length}, listed ${heldOnly.length - unlisted.length}${unlisted.length ? ` (not listed: ${unlisted.join(' ')})` : ''}`);
let inCardBad = [], cutBad = [];
for (const p of PARTS) {
  const cards = [...html[p].matchAll(CARD)].map(m => ({ id: m[1], a: m.index, b: m.index + m[0].length }));
  for (const [a, b, kind, id] of heldZones(html[p], H)) {
    const c = cards.find(c => a >= c.a && a < c.b);
    if (kind === 'paragraph' && c && !H.figures.has(c.id)) inCardBad.push(id);
    for (const k of cards) if (!H.figures.has(k.id) && ((a > k.a && a < k.b) || (b > k.a && b < k.b))) cutBad.push(`${id}/${k.id}`);
  }
}
check(!inCardBad.length, `list: listed paragraphs inside a figure card that is not held: ${inCardBad.length}${inCardBad.length ? ` (${inCardBad.join(' ')})` : ''}`);
check(!cutBad.length, `list: strip zones that cut into a figure that is not held: ${cutBad.length}${cutBad.length ? ` (${cutBad.join(' ')})` : ''}`);

// ---- ledger (calibration section 18) ---------------------------------------------------------------------------------
{
  const LF = path.resolve(o.ledger || LEDGER_DEFAULT);
  let L = null; try { L = readLedger(LF, ['id', 'status']); } catch (e) { check(false, `ledger: not readable by header at ${LF} (${e.message.slice(0, 120)}); give --ledger=<the author's docs/pass-31-ledger.tsv>`); }
  if (L) {
    const held = new Set([...L.rows.values()].filter(r => r.status === 'held').map(r => r.id));
    const extra = [...H.figures].filter(id => !held.has(id)), miss = [...held].filter(id => !H.figures.has(id));
    check(!extra.length && !miss.length && held.size > 0, `ledger: held rows ${held.size} (sha256 ${L.sha256.slice(0, 8)}), held_figures ${H.figures.size}: not in the ledger as held ${extra.length}${extra.length ? ` (${extra.join(' ')})` : ''}, held in the ledger but not listed ${miss.length}${miss.length ? ` (${miss.join(' ')})` : ''}`);
    const cmp = (heldIds, listedIds) => {
      const byStruct = [...bySec].filter(([, xs]) => xs.length && xs.every(x => heldIds.has(x))).map(([sec]) => sec).sort();
      return { byStruct, notListed: byStruct.filter(x => !listedIds.includes(x)), notStruct: listedIds.filter(x => !byStruct.includes(x)) };
    };
    const J = JSON.parse(fs.readFileSync(HELD_FILE, 'utf8')), listed = [...new Set(J.sections.held_only)].sort();
    const r = cmp(held, listed);
    check(!r.notListed.length && !r.notStruct.length, `ledger: sections whose figures are all held by the ledger ${r.byStruct.length}, held_only ${listed.length}: missing from held_only ${r.notListed.length}${r.notListed.length ? ` (${r.notListed.join(' ')})` : ''}, in held_only without that structure ${r.notStruct.length}${r.notStruct.length ? ` (${r.notStruct.join(' ')})` : ''}`);
    // controls: one held figure of a held-only section made not held, and one section with a figure that is not held
    // added to the list: the same comparison finds each
    const sec0 = listed.find(x => bySec.has(x)), one = new Set(held); one.delete(bySec.get(sec0)[0]);
    const other = [...bySec.keys()].find(x => !r.byStruct.includes(x));
    const c1 = cmp(one, listed), c2 = cmp(held, [...listed, other].sort());
    check(c1.notStruct.includes(sec0) && c2.notStruct.includes(other), `ledger (controls): a held figure made not held -> ${sec0} flagged ${c1.notStruct.includes(sec0)}; a section that is not held-only listed -> ${other} flagged ${c2.notStruct.includes(other)}`);
  }
}

// ---- packets -----------------------------------------------------------------------------------------------------
const words = t => t.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim().split(' ').filter(Boolean);
const SH = 8;
const shingles = (t, into = new Set()) => { const w = words(t); for (let i = 0; i + SH <= w.length; i++) into.add(w.slice(i, i + SH).join(' ')); return into; };
// the runs of eight words held material holds, less any run the rest of the book also holds
const heldSh = new Set(), restSh = new Set();
let zonesN = 0, zonesShort = 0;
for (const p of PARTS) {
  const zs = heldZones(html[p], H); let at = 0, rest = '';
  for (const [a, b] of zs) {
    zonesN++;
    const t = plain(html[p].slice(a, b)); if (words(t).length < SH) zonesShort++; shingles(t, heldSh);
    if (a > at) rest += ' ' + html[p].slice(at, a); at = Math.max(at, b);
  }
  rest += ' ' + html[p].slice(at);
  shingles(plain(rest.replace(CARD, m => { const id = (m.match(/id="([^"]+)"/) || [])[1]; return H.figures.has(id) ? ' ' : m; })), restSh);
}
for (const s of restSh) heldSh.delete(s);
console.log(`     packets: ${zonesN} strip zones, ${heldSh.size} runs of ${SH} words only held material holds (${zonesShort} zones under ${SH} words: label-sized, covered by the markers)`);
const nonHeld = figs.filter(f => !H.figures.has(f.id));
let leaks = 0, leakFigs = [], built = 0;
for (const f of nonHeld) {
  const pk = packet(ROOT, f); built++;
  const sh = shingles(pk);
  let hit = 0; for (const s of sh) if (heldSh.has(s)) hit++;
  if (hit) { leaks += hit; leakFigs.push(f.id); }
}
check(leaks === 0, `packets: ${built} non-held figure packets built; runs of held material found in them: ${leaks}${leakFigs.length ? ` (in ${leakFigs.length} packets: ${leakFigs.slice(0, 12).join(' ')})` : ''}`);
// control: the same check finds held runs when nothing is stripped (the last non-held figure's packet)
const NONE = { file: 'none', sha256: 'none', figures: new Set(), chapters: [], sections: [], paragraphs: [], targets: new Set(), elements: [] };
{ const last = nonHeld[nonHeld.length - 1], sh = shingles(packet(ROOT, last, NONE)); let hit = 0; for (const s of sh) if (heldSh.has(s)) hit++;
  check(heldSh.size > 0 && hit > 0, `packets (control): with nothing stripped, the last non-held figure's packet holds ${hit} of the ${heldSh.size} held runs`); }

// ---- markers -----------------------------------------------------------------------------------------------------
const MT = path.join(mkdirp(path.join(OUT, 'packet-test')), 'tree');
fs.rmSync(MT, { recursive: true, force: true }); mkdirp(MT);
const GL = JSON.parse(fs.readFileSync(path.join(ROOT, 'glossary.json'), 'utf8'));
const markers = [];
const alpha = k => { let s = ''; do { s = String.fromCharCode(97 + (k % 26)) + s; k = Math.floor(k / 26) - 1; } while (k >= 0); return s; };   // names hold no digit
const CTL = { p1: 'ch1-context-p1', p5: 'ch18-final-p1', section: 'ch18-final', text: ' Qzctlname and Qzctl Lab and QZCTL handshake ' };
for (const p of PARTS) {
  const h = html[p], zs = heldZones(h, H);
  const ins = [];   // [offset, text]
  const secs = [...h.matchAll(/<section class="section" id="(ch[^"]+)"/g)].map(m => ({ id: m[1], at: m.index }));
  for (const [a, b, kind] of zs) {
    const k = markers.length, word = `qzheldword${k}`, caps = `QZHELD${k}X`, term = `qzheldterm${k}`, name1 = `Qzheldname${alpha(k)}`, name2 = `Qzheld Lab${alpha(k)}`;
    const m = `<span class="key-term">${term}</span> ${word} ${caps} ${name1} ${name2} (a marker)`;
    markers.push({ k, kind, word, caps, term, name1, name2 });
    // the zone's section: its own (a section zone), the first inside it (a chapter), or the one it sits in
    const sec = kind === 'toc-card' ? null : (secs.find(x => x.at >= a && x.at < b) || secs.filter(x => x.at <= a).pop() || null);
    if (sec) for (const t of [name1, name2]) GL.entries[t.toLowerCase()] = { term: t, part: p, section: sec.id };
    const startEnd = h.indexOf('>', a) + 1;
    if (kind === 'figure') { const cap = h.slice(a, b).search(/<p\b[^>]*class="diagram-caption"[^>]*>/); const ce = h.indexOf('>', a + cap) + 1; ins.push([ce, ` ${m} `]); }
    else if (kind === 'paragraph' || kind === 'toc-card') ins.push([startEnd, ` ${m} `]);
    else ins.push([startEnd, `<p>${m}</p><ul><li>${word}li ${caps}</li></ul>`]);
  }
  // the controls: the same kind of name, and a term with a word in capitals, in two paragraphs outside held material
  for (const id of [CTL.p1, CTL.p5]) { const at = h.indexOf(`id="${id}"`); if (at >= 0) ins.push([h.indexOf('>', at) + 1, CTL.text]); }
  let out = h; for (const [at, t] of ins.sort((x, y) => y[0] - x[0])) out = out.slice(0, at) + t + out.slice(at);
  fs.writeFileSync(path.join(MT, p + '.html'), out);
}
for (const t of ['Qzctlname', 'Qzctl Lab', 'QZCTL handshake']) GL.entries[t.toLowerCase()] = { term: t, part: 'part-5', section: CTL.section };
fs.writeFileSync(path.join(MT, 'glossary.json'), JSON.stringify(GL));
const mfigs = PARTS.flatMap(p => figures(fs.readFileSync(path.join(MT, p + '.html'), 'utf8'), p)).filter(f => !H.figures.has(f.id));
let mleak = 0, mleakFigs = new Set();
for (const f of mfigs) {
  const pk = packet(MT + '/', f).toLowerCase(), pt = priorTokens(MT + '/', f);
  const found = pk.includes('qzheld') || [...pt.lower].some(t => t.includes('qzheld'));
  if (found) { mleak++; mleakFigs.add(f.id); }
}
{ const last = mfigs[mfigs.length - 1], pk = packet(MT + '/', last, NONE).toLowerCase(), pt = priorTokens(MT + '/', last, NONE);
  const nm = markers.filter(m => pk.includes(m.word) || pt.lower.has(m.word)).length;
  check(nm > 0, `markers (control): with nothing stripped, the last non-held figure's packet or prose tokens hold ${nm} of the ${markers.length} markers`); }
check(mfigs.length === nonHeld.length && mleak === 0, `markers: ${markers.length} markers in ${markers.length} strip zones; non-held packets and prose-token sets built ${mfigs.length}; with a marker: ${mleak}${mleak ? ` (${[...mleakFigs].slice(0, 12).join(' ')})` : ''}`);
const kt = async strip => {
  const f = path.join(OUT, 'packet-test', `known-terms${strip ? '' : '-nostrip'}.json`);
  const r = await run('node', [path.join(REPO, 'scripts/known-terms.mjs'), `--out=${f}`, `--public=${MT}`, ...(strip ? [`--strip=${HELD_FILE}`] : [])]);
  if (r.code) { console.log(`packet-test: known-terms failed ${r.err.slice(-300)}`); process.exit(2); }
  return JSON.parse(fs.readFileSync(f, 'utf8'));
};
const K = await kt(true), K0 = await kt(false);
const isM = t => /qzheld/i.test(t);
const taughtM = K.by_section.flatMap(s => [...s.known, ...s.defines]).filter(isM);
const abbrM = Object.keys(K.abbreviations).filter(isM);
check(!taughtM.length && !abbrM.length, `markers: known-terms --strip teaches ${new Set(taughtM).size} marker terms and lists ${abbrM.length} marker abbreviations`);
const ctlAbbr = Object.keys(K0.abbreviations).filter(isM).length, ctlTerm = new Set(K0.by_section.flatMap(s => [...s.known, ...s.defines]).filter(isM)).size;
check(ctlAbbr > 0 && ctlTerm > 0, `markers (control): known-terms without --strip lists ${ctlAbbr} marker abbreviations and teaches ${ctlTerm} marker terms`);

// ---- names (calibration section 17) --------------------------------------------------------------------------------
const NAMES = markers.flatMap(m => [m.name1, m.name2]);
const isN = t => /^qzheld(name| lab)/i.test(t);
check(!K.names.filter(isN).length && K0.names.filter(isN).length > 0, `names: known-terms --strip lists ${K.names.filter(isN).length} of ${NAMES.length} held name markers as names (control: without --strip, ${K0.names.filter(isN).length})`);
{
  const KT = await runKnownTerms(MT + '/', path.join(OUT, 'packet-test', 'known-terms-lib.json'));
  const label = NAMES.join(' · ');
  let credited = 0, figsWith = new Set();
  for (const f of mfigs) {
    const c = taughtContext(KT, MT + '/', f);
    const failed = new Set(taughtYet(label, c.known, KT.glossary, c.prior).map(b => b.token));
    // credited: neither the marker nor any word of it failed (a toc card's markers are no glossary entry: their words fail one by one)
    const n = NAMES.filter(x => !failed.has(x.toLowerCase()) && !x.toLowerCase().split(' ').some(w => failed.has(w))).length;
    if (n) { credited += n; figsWith.add(f.id); }
  }
  check(credited === 0, `names: ${NAMES.length} held name markers at ${mfigs.length} non-held figures: credited ${credited} times${figsWith.size ? ` (${[...figsWith].slice(0, 12).join(' ')})` : ''}`);
  const f1 = mfigs.find(f => f.id === 'fig-1-1'), c1 = f1 && taughtContext(KT, MT + '/', f1);
  const ok = c1 ? taughtYet('Qzctlname · Qzctl Lab', c1.known, KT.glossary, c1.prior).map(b => b.token) : ['no fig-1-1'];
  const caps = c1 ? taughtYet('QZCTL handshake', c1.known, KT.glossary, c1.prior).map(b => b.token) : [];
  check(KT.j.names.includes('Qzctlname') && KT.j.names.includes('Qzctl Lab') && !ok.length && caps.includes('qzctl handshake'),
    `names (control): planted before Fig 1.1, taught at ${CTL.section}: the two names pass at Fig 1.1 (failing ${JSON.stringify(ok)}), "QZCTL handshake" fails (${JSON.stringify(caps)})`);
}
console.log(`packet-test: ${n - bad} of ${n} checks hold (${ROOT})`);
process.exit(bad ? 1 : 0);
