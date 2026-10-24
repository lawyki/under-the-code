// Pass 31 teaching places (docs/pass-31-brief.md section 15, as amended in round 5; docs/pass-31-calibration.md
// section 18): where the book's prose teaches. scripts/known-terms.mjs (every teaching point) and tests/pass31/lib.mjs
// (the prose before a card) both read these places and no others, so the two never disagree.
//   - every <p> and <li> outside the figure cards: section paragraphs, section leads (p.lead), chapter leads (the
//     chapter hero's p.chapter-subtitle), insight and timeline paragraphs, chapter closings, list items. Never a
//     caption (p.diagram-caption) and never a part tagline (p.part-tagline: a part opener's line or an end-of-part
//     teaser such as Part II's, which names Part III's people before Part III);
//   - the first cell of a table row that expands or defines its term: the cell glosses itself with a parenthesis that
//     opens with a lower-case word (HDD (spinning disk)), or the row's second cell is a definition: a phrase closed by
//     a colon or a full stop and followed by more words ("Counter: used for loop counts and shift amounts", "Shortest
//     Job First. When the CPU is free, ...", "Base Pointer (the frame pointer): points to ..."), or a sentence of four
//     words or more closed by a full stop ("A counter that processes change in one indivisible step, used to
//     coordinate access to a shared resource."). Only that first cell teaches: the row's other cells do not (SIGTERM,
//     listed in the Signal row's description, is not taught there), a header row does not, and a row whose other
//     cells are values does not (Chapter 1's memory table: SATA in "SATA bus", OS in "OS kernel", NVMe in "SSD
//     (NVMe)", L2 in "L2 Cache").
// Never a place that teaches: a heading, a section label (div.section-number), a math label (div.math-label), a part
// opener's chapter preview (a toc card), a code block (<pre>, blanked inside a piece by the readers), anything inside a
// figure card (label, picture, caption, How-it-works strip).
//   teachingPieces(html, cards) -> [{ kind: 'p'|'li'|'row', start, end, a, inner }] in reading order: start and end
//   bound the element (for a row, its first cell), a is where its content starts, inner its content (HTML).
// The html is a part as the reader sees it (held material already blanked by held.mjs); cards are [start, end] ranges
// of the figure cards in it.
const plainText = h => h.replace(/<br\s*\/?>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&(#x?[0-9a-f]+|\w+);/gi, ' ').replace(/\s+/g, ' ').trim();
const SKIP_P = /class="[^"]*\b(?:diagram-caption|part-tagline)\b/;
// a row's second cell that defines: a phrase of words closed by a colon or a full stop (a closing bracket or quote
// may come between), then more words; or a sentence of four words or more closed by a full stop (a value such as
// "~200 cycles (~60 ns)", "1–20 TB" or "On the CPU die, shared by cores" is neither)
const PHRASE = /\p{L}{2,}[)"”’]*[:.]\s+\p{L}/u, SENTENCE = /\p{L}{2,}[)"”’]*\.$/u;
export const defines = t => { const x = t.trim(); return PHRASE.test(x) || (SENTENCE.test(x) && x.split(/\s+/).length >= 4); };
// a first cell that expands itself: a parenthesis opening with a lower-case word (never a lone abbreviation, "(DRAM)",
// "(NVMe)")
export const EXPANDS = /\(\s*\p{Ll}/u;
export function definingRows(html, inCard) {
  const out = [];
  for (const t of html.matchAll(/<table\b[^>]*>[\s\S]*?<\/table>/g)) {
    if (inCard(t.index)) continue;
    for (const r of t[0].matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/g)) {
      const innerAt = t.index + r.index + r[0].indexOf('>') + 1;
      const cells = [...r[1].matchAll(/<(t[dh])\b([^>]*)>([\s\S]*?)<\/\1>/g)];
      if (cells.length < 2 || cells.every(c => c[1] === 'th')) continue;   // a header row
      const head = cells[0], start = innerAt + head.index, a = start + head[0].indexOf('>') + 1;
      const ex = EXPANDS.test(plainText(head[3])), df = defines(plainText(cells[1][3]));
      if (ex || df) out.push({ kind: 'row', start, end: start + head[0].length, a, inner: head[3], why: ex ? 'expands' : 'defines' });
    }
  }
  return out;
}
export function teachingPieces(html, cards) {
  const inCard = off => cards.some(([x, y]) => off >= x && off < y);
  const out = [];
  for (const m of html.matchAll(/<(p|li)\b([^>]*)>([\s\S]*?)<\/\1>/g)) {
    if ((m[1] === 'p' && SKIP_P.test(m[2])) || inCard(m.index)) continue;
    out.push({ kind: m[1], start: m.index, end: m.index + m[0].length, a: m.index + m[0].indexOf('>') + 1, inner: m[3] });
  }
  out.push(...definingRows(html, inCard));
  return out.sort((x, y) => x.start - y.start);
}
