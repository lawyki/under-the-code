#!/usr/bin/env node
// Build script for the auto-glossary.
//
// Walks all 5 part-N.html files in priority order and extracts terms from
// three increasingly-noisy signals:
//
//   1. <span class="key-term">  — canonical term marker. Always trusted.
//   2. <em>...</em>             — italicised, BUT only if followed by a clear
//                                 definitional cue ("— def", ": def", ", the X that").
//   3. <strong>...</strong>     — bold, BUT also only with a clear definitional
//                                 cue, AND with a strict word/length limit. The
//                                 book uses <strong> heavily for prose emphasis,
//                                 so this signal needs harsh filtering.
//
// Earlier passes win dedup races. After the three passes, a curated allow-list
// of canonical terms (TCP, MMU, AIMD, etc.) is checked — for any term not yet
// in the glossary, we search for its first plain-text occurrence in any part
// and pull a definition from the surrounding sentence.
//
// Run from anywhere — paths are resolved relative to the book directory:
//   node scripts/build-glossary.js
//
// Re-run any time content changes meaningfully.

'use strict';

const fs = require('fs');
const path = require('path');

const BOOK_DIR = path.resolve(__dirname, '..', 'public');
const PARTS = ['part-1.html', 'part-2.html', 'part-3.html', 'part-4.html', 'part-5.html'];

// Generic words that occasionally end up in <strong> but are not glossary
// candidates under any circumstances.
const SKIP_WORDS = new Set([
  'a','an','and','or','but','if','then','else','not','never','always','every','all','any','some',
  'the','very','exactly','just','only','really','actually','simply','clearly','strictly','fully',
  'is','was','are','were','be','been','being','do','does','did','done',
  'can','will','would','should','could','must','may',
  'one','two','three','four','five','six','seven','eight','nine','ten',
  'first','second','third','fourth','fifth','last','final',
  'now','today','here','there','this','that','these','those',
  'yes','no','true','false','none',
  'most','more','less','few','many','much',
  'why this matters','famous','note','important','crucial','key',
  'gab', // <em>g<sup>ab</sup></em> math markup in ch14, not a term
  'a a a', // <em>A · A = A</em> / <em>A + A = A</em> Boolean-law markup in ch2, not a term
  // ch1 instruction-cycle stage names are set in <em> for reading emphasis, but they are
  // common verbs used all over the book (fetch a page, execute a query, decode a header);
  // marking them as terms would fire CPU-cycle tooltips on every unrelated use. Skip them —
  // "instruction cycle" itself remains the glossary term.
  'fetch','decode','execute','writeback',
  // Part IV language-pass (pass-17 verification) re-carries bolded these mid-sentence
  // for prose emphasis, which mints entries whose auto-extracted definitions are not
  // self-contained (they open with a parenthetical date or back-reference). The book
  // deliberately left them un-glossaried in their original flat-list form; keep it that way.
  'intrusion detection system','endpoint detection and response',
  'zero-trust architecture','relationally complete',
]);

// Curated canonical terms that should always appear in the glossary even if
// they are not wrapped in any of the structured tags. The script will search
// the text of every part for the first plain-text occurrence and extract a
// definition from the surrounding sentence.
//
// Order is rough chapter-of-introduction order, but the script doesn't care
// about that — it just searches every part top-to-bottom and uses whichever
// match comes first.
const CURATED_TERMS = [
  // Hardware (Part I)
  'transistor', 'MOSFET', 'logic gate', 'NAND', 'NOR', 'XOR', 'half-adder', 'full-adder',
  'two\'s complement', 'IEEE 754', 'mantissa', 'buffer overflow',
  // CPU & memory model
  'register', 'opcode', 'pipeline', 'speculative execution',
  'cache line', 'memory hierarchy',
  // ISA & assembly (Part I Ch 3)
  'ISA', 'x86-64', 'ARM64', 'RISC-V', 'calling convention', 'system call',
  // Bridge & kernel (Part I Bridge / Part II Ch 4)
  'kernel', 'privilege ring', 'trap', 'IDT', 'MMU', 'TLB', 'DMA', 'MMIO',
  'page table', 'virtual memory', 'page fault', 'COW', 'copy-on-write',
  'fork', 'exec', 'mmap', 'inode', 'hard link', 'journaling', 'CFS',
  'pipe', 'signal', 'shared memory', 'semaphore',
  'monolithic kernel', 'microkernel', 'eBPF', 'Dirty COW',
  // Languages (Part II Ch 5–7)
  'undefined behavior', 'pointer arithmetic', 'stack frame', 'heap',
  'malloc', 'free', 'use-after-free', 'memory leak',
  'compiler', 'bytecode', 'GIL',
  'inheritance', 'vtable', 'RAII', 'move semantics',
  // Memory-safety attacks (Part I Ch 3 + woven elsewhere)
  'buffer overflow', 'stack canary', 'ASLR', 'DEP', 'NX', 'ROP', 'JOP', 'CFI',
  'PAC', 'CET', 'race condition', 'TOCTOU',
  // Network — link & physical (Part III Ch 8)
  'CSMA/CD', 'NRZ', 'Manchester encoding', 'modulation',
  'channel capacity', 'Shannon entropy', 'OUI', 'ARP',
  'OSI model', 'TCP/IP model',
  // Network — packets (Ch 9)
  'TCP', 'UDP', 'IP', 'IPv4', 'IPv6', 'ICMP',
  'autonomous system', 'BGP', 'BGP hijacking', 'route leak',
  'NAT', 'CGNAT', 'IP spoofing', 'BCP 38', 'RPKI',
  // TCP (Ch 10)
  'three-way handshake', 'sliding window', 'AIMD', 'slow start',
  'congestion control', 'BDP', 'BBR', 'CUBIC', 'Reno',
  'MTU', 'MSS', 'ISN', 'RTT', 'TCB',
  'SYN flood', 'SYN cookies', 'RST injection',
  'QUIC', 'TCP hijacking',
  // Web & TLS (Ch 11)
  'HTTP', 'HTTPS', 'HTTP/2', 'HTTP/3', 'DNS', 'TLS', 'SSL',
  'certificate authority', 'X.509', 'forward secrecy', 'cipher suite',
  'TLS handshake', 'OCSP', 'CRL',
  'recursive resolver', 'authoritative server', 'DNS poisoning',
  // JavaScript & web (Ch 12)
  'event loop', 'callback', 'promise', 'async/await',
  'V8', 'Node.js', 'DOM', 'same-origin policy',
  'XSS', 'CSRF', 'CSP', 'CORS',
  // Databases (Part IV Ch 13)
  'relational algebra', 'ACID', 'B-tree',
  'write-ahead logging', 'transaction',
  'SQL injection', 'parameterized query',
  // Cryptography (Ch 14)
  'one-way function', 'hash function', 'SHA-256', 'collision resistance',
  'symmetric encryption', 'AES',
  'asymmetric encryption',
  'Diffie–Hellman', 'RSA',
  'elliptic curve', 'ECC', 'ECDSA', 'ECDH', 'HMAC',
  // Attack/defense (Ch 15)
  'threat model', 'attack surface', 'least privilege',
  'firewall', 'IDS', 'IPS', 'SIEM', 'EDR', 'zero trust', 'CTF',
  'MITM', 'ARP spoofing', 'DNS poisoning',
  // Concurrency & GPU (Ch 16)
  'thread', 'process', 'mutex', 'lock-free', 'atomic',
  'memory ordering', 'cache coherence', 'NUMA',
  'SIMD', 'CUDA', 'Amdahl\'s law', 'Gustafson\'s law',
  // Cloud & distributed (Ch 17)
  'hypervisor', 'KVM', 'container', 'namespace', 'cgroup',
  'Kubernetes', 'control loop',
  'consensus', 'Paxos', 'Raft', 'CAP theorem',
  'serverless', 'microservice',
  // Math threads
  'Boolean algebra', 'set theory', 'information theory', 'control theory',
  'number theory', 'graph theory', 'queueing theory', 'Little\'s Law',
  // People — short forms preferred since the book often uses last names alone
  'Shannon', 'Boole', 'Turing', 'von Neumann',
  'Ritchie', 'Thompson', 'Stroustrup', 'Codd',
  'Berners-Lee', 'van Rossum', 'Eich',
  'Diffie', 'Hellman', 'Rivest', 'Shamir', 'Adleman',
  'Cerf', 'Kahn', 'Baran', 'Kleinrock', 'Metcalfe',
  'Bernstein', 'Jacobson', 'Mitnick', 'Shimomura',
  // Places / institutions
  'Bell Labs', 'Xerox PARC', 'PARC', 'CERN', 'ARPANET', 'RAND',
  'IETF', 'IEEE', 'IANA', 'ICANN',
];

// Definitional cues that signal "this italic/bold/span is introducing a term".
// All look at the head of the text immediately following the closing tag.
function isDefContext(after) {
  const head = after.substring(0, 80);
  // " — definition", " – definition"
  if (/^\s*[—–-]\s+[A-Za-z]/.test(head)) return true;
  // ": definition"
  if (/^:\s+[A-Za-z]/.test(head)) return true;
  // ", or ACRONYM" (italicised expansion followed by acronym)
  if (/^,\s+or\s+[A-Z][A-Za-z0-9-]+/.test(head)) return true;
  // ", the X that ..." (appositive definition)
  if (/^,\s+(the|a|an)\s+[a-z]/.test(head)) return true;
  // "(definition)" — parenthetical definition immediately after
  if (/^\s*\(\s*[A-Za-z]/.test(head)) return true;
  return false;
}

function normalizeKey(term) {
  return term
    .toLowerCase()
    .replace(/<[^>]+>/g, ' ')
    .replace(/[^a-z0-9 -]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// Strict acceptance criteria for a candidate term.
//   strictWord — max words allowed (3 for <strong>, 5 for <em>, 7 for key-term)
//   strictLen  — max characters allowed
function isLikelyTerm(rawTerm, strictWords, strictLen) {
  const cleaned = rawTerm.replace(/<[^>]+>/g, '').trim();
  if (!cleaned) return false;
  if (cleaned.length < 2) return false;
  if (cleaned.length > strictLen) return false;

  const words = cleaned.split(/\s+/);
  if (words.length > strictWords) return false;

  // Reject if the term contains internal sentence-fragment punctuation.
  // A real glossary term doesn't contain ":", ";", trailing periods, etc.
  if (/[:;]/.test(cleaned)) return false;
  if (/[—–]/.test(cleaned)) return false;
  if (cleaned.endsWith('.') && words.length > 1) return false;
  if (cleaned.endsWith(',')) return false;

  // Reject pronoun-led "terms" — almost certainly a sentence fragment.
  if (/^(it|he|she|they|we|you|i|its|this|that|these|those|there|here)\b/i.test(cleaned)) return false;

  const norm = normalizeKey(cleaned);
  if (!norm) return false;
  if (SKIP_WORDS.has(norm)) return false;

  // Reject "Why X" / "How X" / "When X" — these are nearly always
  // section-heading-style emphasis, not glossary terms.
  if (/^(why|how|when|where|what|who)\b/i.test(cleaned) && words.length > 1) return false;

  return true;
}

function stripHtmlPlain(s) {
  return s
    .replace(/<[^>]+>/g, ' ')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–')
    .replace(/&middot;/g, '·')
    .replace(/&hellip;/g, '…')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&[a-z]+;/gi, ' ')
    .replace(/\s+/g, ' ');
}

function extractDefinition(after) {
  // Truncate `after` at the start of a figure / svg / pre block so the
  // forward extraction never crosses into figure-label or diagram text.
  let truncEnd = after.length;
  for (const marker of ['<div class="diagram-card"', '<div class="diagram-label"', '<svg', '<pre']) {
    const idx = after.indexOf(marker);
    if (idx !== -1 && idx < truncEnd) truncEnd = idx;
  }
  if (truncEnd < after.length) after = after.substring(0, truncEnd);

  let stripped = stripHtmlPlain(after).trim();

  if (!stripped) return '';

  // Strip leading connector punctuation so the definition reads cleanly when
  // shown beneath the term as a label. The leading period strip handles the
  // case where the match is at the end of a sentence and the forward window
  // begins with `.</p>` — after HTML strip, a stray "." becomes the lead.
  stripped = stripped.replace(/^[\s.—–\-,;:·)]+/, '').trim();

  let snippet = stripped.substring(0, 280);

  // Prefer a clean sentence ending.
  const sentenceEnd = snippet.search(/[.!?](\s|$)/);
  if (sentenceEnd > 30 && sentenceEnd < 260) {
    snippet = snippet.substring(0, sentenceEnd + 1);
  } else if (snippet.length === 280 && stripped.length > 280) {
    snippet = snippet.substring(0, 240).replace(/\s+\S*$/, '') + '…';
  }

  return snippet.trim();
}

// Compose a definition from html surrounding a term match. First tries the
// forward window (matches the "TERM — definition" pattern); if that yields a
// fragment (lowercase opener, "that"/"which" continuation, list continuation),
// looks backward for the start of the sentence containing the term and
// composes the full sentence as the definition.
function composeDefinition(html, termStart, termEnd) {
  const afterRaw = html.substring(termEnd, termEnd + 1200);
  const forward = extractDefinition(afterRaw);

  // Decide whether `forward` reads as a self-contained definition or a
  // mid-sentence continuation. Continuation indicators: starts with a
  // lowercase letter (after leading punct already stripped), or starts with
  // a connector word ("that"/"which"/"and"/"or"/"but"/"too"/"also"/"so"/
  // "is"/"are"/"was"/"were"/"means").
  const looksLikeContinuation = forward.length === 0 ||
    /^[a-z]/.test(forward) ||
    /^(that|which|and|or|but|too|also|so|is|are|was|were|means|gives|gave|takes|took|provides|provided|becomes|became|made|makes)\b/i.test(forward);

  if (!looksLikeContinuation) return forward;

  // Look backward for the start of the sentence that contains the term.
  // Cap the window at the start of the current paragraph (or other block
  // element) so we don't cross figure boundaries and pull in <svg> labels or
  // diagram captions belonging to a different chunk of content.
  let beforeRaw = html.substring(Math.max(0, termStart - 1200), termStart);
  let blockBoundary = -1;
  for (const re of [/<p\b[^>]*>/g, /<h[1-6]\b[^>]*>/g, /<\/svg>/g, /<\/div>/g]) {
    let mm;
    while ((mm = re.exec(beforeRaw)) !== null) {
      const after = mm.index + mm[0].length;
      if (after > blockBoundary) blockBoundary = after;
    }
  }
  if (blockBoundary > 0) beforeRaw = beforeRaw.substring(blockBoundary);
  let beforePlain = stripHtmlPlain(beforeRaw);

  // Find the rightmost sentence boundary in `beforePlain`: a [.!?] followed
  // by whitespace and an uppercase / opening-quote / paren that begins the
  // current sentence.
  const re = /[.!?]\s+(?=["'(]?[A-Z])/g;
  let lastBoundary = -1;
  let m;
  while ((m = re.exec(beforePlain)) !== null) {
    lastBoundary = m.index + m[0].length;
  }

  let sentenceBefore = lastBoundary >= 0
    ? beforePlain.substring(lastBoundary)
    : beforePlain;
  sentenceBefore = sentenceBefore.replace(/\s+/g, ' ').trim();

  // If there's no usable preceding context, fall back to the forward fragment.
  if (!sentenceBefore) return forward;

  // If the preceding sentence is itself absurdly long, trim the head.
  if (sentenceBefore.length > 220) {
    sentenceBefore = '…' + sentenceBefore.substring(sentenceBefore.length - 200);
  }

  const termText = stripHtmlPlain(html.substring(termStart, termEnd)).trim();

  let composed = (sentenceBefore + ' ' + termText + ' ' + forward)
    .replace(/\s+/g, ' ')
    .trim();

  // Cap at the first sentence-ending punctuation after the term, or at 280
  // chars with an ellipsis fallback.
  const minPos = sentenceBefore.length + 1 + termText.length;
  let cutAt = -1;
  for (let i = minPos; i < composed.length && i < 320; i++) {
    if (/[.!?]/.test(composed[i]) && (i + 1 === composed.length || /\s/.test(composed[i + 1]))) {
      cutAt = i + 1;
      break;
    }
  }
  if (cutAt > 0) {
    composed = composed.substring(0, cutAt);
  } else if (composed.length > 280) {
    composed = composed.substring(0, 240).replace(/\s+\S*$/, '') + '…';
  }

  return composed.trim();
}

function findContainingSection(html, position) {
  const before = html.substring(0, position);
  const re = /<section class="section" id="([^"]+)">/g;
  let last = null;
  let m;
  while ((m = re.exec(before)) !== null) last = m;
  return last ? last[1] : null;
}

function getSectionMeta(html, sectionId) {
  const idMarker = `id="${sectionId}"`;
  const start = html.indexOf(idMarker);
  if (start < 0) return { label: '', title: '' };
  const end = html.indexOf('</section>', start);
  const slice = html.substring(start, end > 0 ? end : start + 8000);

  const labelM = slice.match(/<div class="section-number">([^<]+)<\/div>/);
  const titleM = slice.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);

  return {
    label: labelM ? labelM[1].trim() : '',
    title: titleM ? titleM[1].replace(/<[^>]+>/g, '').trim() : ''
  };
}

function getChapterFromSection(sectionId) {
  return sectionId ? sectionId.split('-')[0] : null;
}

function formatChapterNum(chapterId) {
  if (!chapterId) return '';
  if (chapterId === 'chBridge') return 'Bridge';
  const n = chapterId.replace(/^ch/, '');
  return /^\d+$/.test(n) ? 'Chapter ' + n : chapterId;
}

function extractFollowingAcronym(after) {
  const m = after.match(/^,\s+or\s+([A-Z][A-Za-z0-9-]{1,12})\b/);
  return m ? m[1] : null;
}

const glossary = {};
let scanned = 0;
let kept = 0;

function recordTerm(term, html, termStart, termEnd, part) {
  const key = normalizeKey(term);
  if (!key || key in glossary) return null;

  // Store the page reference extensionless so links match the site's
  // extensionless URL scheme (Cloudflare Pages serves /part-1, not /part-1.html).
  part = part.replace(/\.html$/, '');

  const sectionId = findContainingSection(html, termEnd);
  if (!sectionId) return null;

  const sectionMeta = getSectionMeta(html, sectionId);
  const chapterId = getChapterFromSection(sectionId);
  const chapterNum = formatChapterNum(chapterId);

  const after = html.substring(termEnd, termEnd + 1200);
  const definition = composeDefinition(html, termStart, termEnd);
  if (!definition || definition.length < 10) return null;

  glossary[key] = {
    term,
    definition,
    part,
    section: sectionId,
    chapter: chapterId,
    chapter_num: chapterNum,
    section_label: sectionMeta.label,
    section_title: sectionMeta.title
  };
  kept++;

  // If followed by ", or ACRONYM", index the acronym separately.
  const acronym = extractFollowingAcronym(after);
  if (acronym) {
    const ackey = normalizeKey(acronym);
    if (ackey && !(ackey in glossary)) {
      glossary[ackey] = {
        term: acronym,
        definition: term + ' — ' + definition.replace(/^,\s+or\s+[A-Z][A-Za-z0-9-]+\.?\s*/, ''),
        part,
        section: sectionId,
        chapter: chapterId,
        chapter_num: chapterNum,
        section_label: sectionMeta.label,
        section_title: sectionMeta.title
      };
      kept++;
    }
  }

  return { sectionId, chapterId };
}

// ----------------------------------------------------------------------------
// Walk every part once per signal type. Pass order matters: earlier passes win
// dedup races, so put the highest-precision signal first.

const partHtml = {};
for (const part of PARTS) {
  const filePath = path.join(BOOK_DIR, part);
  if (!fs.existsSync(filePath)) {
    console.warn(`Skipping ${part} (not found at ${filePath})`);
    continue;
  }
  partHtml[part] = fs.readFileSync(filePath, 'utf-8');
}

// ---- Pass 1: <span class="key-term"> — canonical, always trusted ----------
for (const part of PARTS) {
  const html = partHtml[part];
  if (!html) continue;

  const re = /<span class="key-term">([\s\S]*?)<\/span>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    scanned++;
    if (isInsideExcludedZone(html, m.index)) continue;
    const term = m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    // key-term is the canonical signal — accept generously (up to 7 words).
    if (!isLikelyTerm(term, 7, 80)) continue;
    recordTerm(term, html, m.index, m.index + m[0].length, part);
  }
}

// ---- Pass 2: <em> with definitional context -------------------------------
for (const part of PARTS) {
  const html = partHtml[part];
  if (!html) continue;

  const re = /<em>([\s\S]*?)<\/em>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    scanned++;
    if (isInsideExcludedZone(html, m.index)) continue;
    const term = m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    if (!isLikelyTerm(term, 5, 60)) continue;

    const after = html.substring(m.index + m[0].length, m.index + m[0].length + 200);
    if (!isDefContext(after)) continue;

    recordTerm(term, html, m.index, m.index + m[0].length, part);
  }
}

// ---- Pass 3: <strong> with strict filter + definitional context -----------
// <strong> is heavily used for prose emphasis; only accept very short bolds
// that are immediately followed by a definitional cue. This eliminates the
// "thinking itself could be mechanized:" style noise.
for (const part of PARTS) {
  const html = partHtml[part];
  if (!html) continue;

  const re = /<strong>([\s\S]*?)<\/strong>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    scanned++;
    if (isInsideExcludedZone(html, m.index)) continue;
    const term = m[1].replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    // Strict: ≤4 words, ≤40 chars, no internal punctuation.
    if (!isLikelyTerm(term, 4, 40)) continue;

    const after = html.substring(m.index + m[0].length, m.index + m[0].length + 200);
    if (!isDefContext(after)) continue;

    recordTerm(term, html, m.index, m.index + m[0].length, part);
  }
}

// ---- Pass 4: curated canonical-term backfill ------------------------------
// For every term in CURATED_TERMS that isn't yet in the glossary, find its
// first plain-text occurrence anywhere in the parts and use the surrounding
// sentence as a (best-effort) definition.
//
// We escape regex special chars in the term and require word-boundary matching
// where applicable. Some "terms" (e.g. ".NX", "x86-64") have characters that
// trip word boundaries — handle them with a flexible boundary check.
function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Returns true if `pos` is inside one of the structural zones we don't want
// definitions extracted from: the chapter-hero block (which has metadata like
// "Topics: AIMD · BBR · CUBIC" that's a list, not a definition), the contents
// of any <svg> element, or a <code> block that runs longer than a sentence.
function isInsideExcludedZone(html, pos) {
  const before = html.substring(0, pos);

  // chapter-hero: from `class="chapter-hero"` until its </div> closes,
  // recognised by the appearance of `<nav class="chapter-nav">` which always
  // follows.
  const heroStart = before.lastIndexOf('class="chapter-hero"');
  if (heroStart !== -1) {
    const navAfterHero = before.indexOf('class="chapter-nav"', heroStart);
    if (navAfterHero === -1) return true;
  }

  // chapter-nav block — list of nav-item links with subsection titles.
  // Definitions extracted here become "04 — Flow & congestion control 05 —
  // CUBIC, BBR..." gibberish.
  const navStart = before.lastIndexOf('<nav class="chapter-nav">');
  if (navStart !== -1) {
    const navClose = before.indexOf('</nav>', navStart);
    if (navClose === -1) return true;
  }

  // <svg> element
  const svgStart = before.lastIndexOf('<svg');
  if (svgStart !== -1) {
    const svgClose = before.indexOf('</svg>', svgStart);
    if (svgClose === -1) return true;
  }

  // <pre> code block
  const preStart = before.lastIndexOf('<pre');
  if (preStart !== -1) {
    const preClose = before.indexOf('</pre>', preStart);
    if (preClose === -1) return true;
  }

  // part-toc block (chapter cards on the part-opener)
  const tocStart = before.lastIndexOf('class="part-toc"');
  if (tocStart !== -1) {
    const tocClose = before.indexOf('</section>', tocStart);
    if (tocClose === -1) return true;
  }

  // Heading elements — section/chapter titles and the section-number prefix.
  // Definitions extracted from these are heading text, not prose.
  for (const tag of ['h1', 'h2', 'h3', 'h4']) {
    const open = before.lastIndexOf('<' + tag + '>');
    const openAttr = before.lastIndexOf('<' + tag + ' ');
    const start = Math.max(open, openAttr);
    if (start !== -1) {
      const close = before.indexOf('</' + tag + '>', start);
      if (close === -1) return true;
    }
  }

  // <div class="section-number"> — the "04 — Flow control" prefix at the top
  // of every section.
  const sectionNumStart = before.lastIndexOf('class="section-number"');
  if (sectionNumStart !== -1) {
    const sectionNumClose = before.indexOf('</div>', sectionNumStart);
    if (sectionNumClose === -1) return true;
  }

  // Pull-quote callouts (with their <span class="attr">— Author</span>
  // attribution lines). Matches here produce attribution-as-definition.
  const pullStart = before.lastIndexOf('class="pull-quote"');
  if (pullStart !== -1) {
    const pullClose = before.indexOf('</div>', pullStart);
    if (pullClose === -1) return true;
  }

  // Figure/diagram cards — labels and captions belong to the figure, not the
  // term definition.
  const diagStart = before.lastIndexOf('class="diagram-label"');
  if (diagStart !== -1) {
    const diagClose = before.indexOf('</div>', diagStart);
    if (diagClose === -1) return true;
  }

  return false;
}

// True if `pos` is inside the angle-bracket region of an HTML tag (between an
// unmatched '<' and the next '>'). This catches matches like AIMD inside
// id="ch10-aimd-something", whose extracted "definition" reads forward past
// the closing > into a section number / heading.
function isInsideHtmlTag(html, pos) {
  // Look back ~500 chars for the most recent '<' and '>'.
  const before = html.substring(Math.max(0, pos - 500), pos);
  const lastLt = before.lastIndexOf('<');
  const lastGt = before.lastIndexOf('>');
  return lastLt > lastGt;
}

// Build a regex source from a curated term that:
//   - matches across whitespace and HTML tags between words (so "Kevin\n      Mitnick" works)
//   - allows an optional trailing 's' for plurals (so "MOSFETs", "ciphers" match a "MOSFET" / "cipher" entry)
//   - requires a non-alphanumeric boundary on either side
function buildTermPattern(term) {
  // Split on whitespace, escape each word, rejoin with a flexible whitespace
  // pattern that also allows HTML tags (e.g. </strong> followed by ' '). The
  // pattern \s|<\/?[a-z][^>]*> matches one of: whitespace, opening tag,
  // closing tag — so "Kevin</strong>\n     <strong>Mitnick" still matches
  // "Kevin Mitnick".
  const words = term.split(/\s+/).map(escapeRegex);
  const sep = '(?:\\s|<\\/?[a-z][^>]*>)+';
  const body = words.join(sep);
  // Boundary chars that mark a real word-end. Crucially excludes "/" so that
  // "TCP" doesn't match inside "TCP/IP". Hyphen is intentionally NOT
  // excluded — compounds like "fork-and-exec" should still let "exec" match,
  // and "Mitnick-Shimomura" should still let "Mitnick" match. Trailing "s"
  // allowed for plurals (MOSFETs → MOSFET).
  return '(?:^|[^A-Za-z0-9/])(' + body + ')(?:s)?(?![A-Za-z0-9/])';
}

let curatedAdded = 0;
let curatedMissing = [];

for (const term of CURATED_TERMS) {
  const key = normalizeKey(term);
  if (!key || key in glossary) continue;

  // Use the global flag so we can iterate all matches, not just the first.
  // Skip matches that fall inside chapter-heroes, SVGs, or part-tocs — those
  // produce garbage definitions like "CUBIC · BBR · QUIC · SYN flood" pulled
  // from chapter-hero metadata.
  const re = new RegExp(buildTermPattern(term), 'gi');

  // Iterate ALL matches across ALL parts, score each one, and take the best.
  // Score signals (highest first):
  //   - Section ID contains the term's normalized words: this is where the
  //     term is being introduced as a topic, not name-dropped in passing.
  //   - Section label or title contains the term: same idea, weaker signal.
  //   - The match's surrounding prose looks like a definition: forward window
  //     starts with uppercase or `(` (not a mid-sentence continuation).
  // We tie-break by part order (earlier parts first) so deterministic.
  const termWords = normalizeKey(term).split(/\s+/).filter(Boolean);
  const candidates = [];
  for (const part of PARTS) {
    const html = partHtml[part];
    if (!html) continue;
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(html)) !== null) {
      const matchStart = m.index;
      const lead = m[0].length - m[1].length;
      const termStart = matchStart + lead;
      const termEnd = termStart + m[1].length;
      if (isInsideExcludedZone(html, termStart)) continue;
      if (isInsideHtmlTag(html, termStart)) continue;
      const sectionId = findContainingSection(html, termStart);
      if (!sectionId) continue;

      // Score this match. Two signals carry weight: prose quality (does the
      // forward window read like a definition, or like a fragment?) and
      // section-naming (is this the section that introduces the term?).
      // Prose quality is weighted higher — a good prose match in any section
      // beats a heading-text match in the section named after the term.
      let score = 0;
      const sectionMeta = getSectionMeta(html, sectionId);
      const sectionIdLower = sectionId.toLowerCase();
      const sectionLabelLower = (sectionMeta.label || '').toLowerCase();
      const sectionTitleLower = (sectionMeta.title || '').toLowerCase();
      const allWordsInId = termWords.every(w => sectionIdLower.includes(w));
      if (allWordsInId) score += 30;
      const allWordsInLabel = termWords.every(w => sectionLabelLower.includes(w));
      if (allWordsInLabel) score += 15;
      const allWordsInTitle = termWords.every(w => sectionTitleLower.includes(w));
      if (allWordsInTitle) score += 5;

      // Wrapped-in-emphasis signal. If the term is at the immediate start of
      // a <strong>, <em>, or <span class="key-term"> element, that's the
      // strongest possible "this is the introduction" cue regardless of how
      // the forward window reads.
      const beforeChar = html.substring(Math.max(0, termStart - 80), termStart);
      const lastClose = beforeChar.lastIndexOf('>');
      if (lastClose !== -1 && /^\s*$/.test(beforeChar.substring(lastClose + 1))) {
        const tagOpen = beforeChar.lastIndexOf('<', lastClose);
        if (tagOpen !== -1) {
          const tag = beforeChar.substring(tagOpen, lastClose + 1);
          if (/^<(strong|em)>$/.test(tag) || /^<span class="key-term">$/.test(tag)) {
            score += 60;
          }
        }
      }

      // Forward-window quality.
      const peekRaw = stripHtmlPlain(html.substring(termEnd, termEnd + 200));
      const peek = peekRaw.replace(/^[\s.—–\-,;:·)]+/, '').trim();
      // Strong defcontext signal: the term is followed by a clean dash or
      // colon and then a capitalised continuation — the definitional pattern.
      if (/^\s*[—–-]\s+[A-Z]/.test(peekRaw) || /^\s*:\s+[A-Z]/.test(peekRaw)) {
        score += 50;
      } else if (/^[A-Z(]/.test(peek)) {
        // Peek begins with capital or open-paren after leading punct stripped.
        score += 25;
      } else if (/^[a-z]/.test(peek) || peek === '') {
        // Lowercase / empty forward — a fragment continuation.
        score -= 10;
      }

      candidates.push({ score, part, termStart, termEnd, html, partIdx: PARTS.indexOf(part) });
    }
  }

  if (candidates.length === 0) {
    curatedMissing.push(term);
    continue;
  }

  // Pick highest score; break ties by earliest part.
  candidates.sort((a, b) => b.score - a.score || a.partIdx - b.partIdx);
  const best = candidates[0];

  const result = recordTerm(term, best.html, best.termStart, best.termEnd, best.part);
  if (result) curatedAdded++;
}

// ---- Output ---------------------------------------------------------------

// Sort entries alphabetically by term for stable, readable output.
const sortedKeys = Object.keys(glossary).sort();
const sortedGlossary = {};
for (const k of sortedKeys) sortedGlossary[k] = glossary[k];

const out = {
  generated: new Date().toISOString(),
  count: kept,
  scanned,
  curated_added: curatedAdded,
  curated_missing: curatedMissing,
  entries: sortedGlossary
};

const outPath = path.join(BOOK_DIR, 'glossary.json');
fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
console.log(`Scanned ${scanned} candidates across <span class="key-term">, <em>, <strong>.`);
console.log(`Kept ${kept} glossary entries (${curatedAdded} added by curated backfill).`);
if (curatedMissing.length > 0) {
  console.log(`Curated terms that could not be located in any part (${curatedMissing.length}):`);
  curatedMissing.forEach(t => console.log(`  · ${t}`));
}
console.log(`Wrote ${outPath}`);
