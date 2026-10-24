// Pass 31 taught-yet unit cases (docs/pass-31-calibration.md sections 13, 15, 16, 17): the rules of tests/pass31/lib.mjs
// taughtYet on fixed label strings, each placed at a real figure of a tree, so "before the figure" is the book's own
// prose (held material stripped: known-terms runs with --strip, lib.mjs taughtContext). Section 16 adds the cases of
// its items 2a to 2e: same-section teaching before the card, the glossary placement (prose glosses), tokens taught by
// the prose before the card, everyday words that are glossary terms (still failing), and the regressions that must
// still fail. Section 17 (the review of the section 16 freeze) adds its defects 1 to 7: the name rules (no mention of
// a term taught only in held material or nowhere, of a term that is not a name, or in a heading or chapter preview
// credits it), EAX before ch3-registers, teaching only in paragraphs and list items (never a section label, heading,
// table cell or code block), inflections without a stripped prefix, HTTPS not a plural of HTTP, no taught exemption,
// and synthetic cases for the name rule. Section 18 (the review of the section 17 freeze) adds its holes H1 to H5, the
// eleven false flags and the same placement class (each passing at the first figure after its teaching paragraph and
// failing at the figure just before), the teaching places (defining table rows teach, value rows, part taglines and
// pointer sentences do not), and a synthetic tree that plants plain uses of everyday glossary words (they must still
// fail) beside one control sentence per new cue (each must teach). Section 19 (the review of the section 18 freeze)
// adds A (no abbreviation placed by a mention in a sentence that points elsewhere, nor a noMention term or one first
// written in held material by a mention: DNS, ASLR, CFI, HTTPS, SBOM, CVE, CA must fail where the review named them;
// DNS after its teaching, DEP, GCHQ and the glosses in pointer sentences must pass; the abbreviations' placements),
// B (a line break in the HTML source is no sentence start: planted mid-sentence uses fail, a control passes), E (a
// possessive apposition glosses: C++), F (a hexadecimal run is notation taught with hexadecimal; a word in capitals
// passes as the word the prose writes), each with its regressions.
//   npm run fig:taught-test [-- --tree=<public dir>]
// Exit 0 when every case holds, 1 otherwise. Each case: the figure that sets the position, the label text, and the
// tokens expected to fail (an empty list: every token passes).
import fs from 'node:fs'; import path from 'node:path';
import { args, tree, findFigure, runKnownTerms, taughtContext, taughtYet, svgTexts, mkdirp, readPart, plain, CARD, PARTS, OUT, REPO } from './lib.mjs';

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
  // material only; Reno nowhere), not even at the book's last figure. (SHA-256 left this case in section 18: a
  // definitional sentence at ch11-crypto-p4 teaches it, see below)
  ['fig-18-6', 'SQL injection · SYN flood · Reno', ['sql injection', 'syn flood', 'reno']],
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
  // pair) fails before ch11-crypto-p7 teaches it (section 18 corrects this case, which sat at Fig 11.11, after that
  // teaching), Amdahl's law (a possessive law), Promises (the book writes promise in lower case)
  ['fig-11-9', 'Diffie–Hellman', ['diffie hellman']],
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
  // a table row whose other cells are values does not teach (section 18): OS, written before Fig 3.2 only in Chapter
  // 1's memory table ("OS kernel" under "Managed by"). (The scheduling policies, which section 17 had here, are taught
  // by Chapter 4's table, whose rows define them: see section 18 below)
  ['fig-3-2', 'OS', ['OS']],
  // ---- defect 4: an inflection of a taught term is by plain endings only, never by a stripped prefix
  ['fig-17-6', 'subprocess · subthreads · substack · unpipelined', ['subprocess', 'subthreads', 'substack', 'unpipelined']],
  // ... and a prefixed word is a word of its own, not the glossary term inside it: SubBytes (the prose names it before
  // Fig 14.5) passes as any token the prose writes; everyday prefixed words pass; the prose writing kernel does not
  // teach unkernel
  ['fig-14-5', 'SubBytes', []],
  ['fig-1-1', 'upload · subsystem · unpaid · rewrite', []],
  ['fig-1-14', 'unkernel', ['unkernel']],
  // ---- defect 5: HTTPS is not a plural of HTTP. (Section 19: HTTPS, a glossary term written in its section only inside
  // held material and first written there, is never placed by a mention, so it fails at Fig 11.2 too; HTTP, written
  // before Fig 4.19 only in the Part III teaser at ch4-ipc-p15, fails there and passes from ch7-types-p3, where HTTPS
  // still fails)
  ['fig-4-19', 'HTTPS', ['https']],
  ['fig-4-19', 'HTTP', ['http']],
  ['fig-7-3', 'HTTP', []],
  ['fig-7-3', 'HTTPS', ['https']],
  ['fig-11-2', 'HTTPS', ['https']],

  // ==== section 18 (the review of the section 17 freeze) ===============================================================
  // ---- H1: a prefix comes off only when what remains is an everyday word as written, of four letters or more: redis
  // is not re plus dis (no paragraph before Fig 4.20 writes it), subnet and unmap fail; everyday prefixed words and
  // their inflections still pass
  ['fig-4-20', 'redis', ['redis']],
  ['fig-1-1', 'subnet · unmap', ['subnet', 'unmap']],
  ['fig-1-1', 'upload · uploads · subsystem · unpaid · rewrite · rewrote · rewritten · overwritten', []],
  // ---- H2: a plural or possessive of an abbreviation is judged as the abbreviation (brief section 15), and so is
  // each piece of a compound (DRAM in DRAM-only); lower-case possessives as the short abbreviation
  ['fig-1-1', "RAM's · OS's · ARM's · DRAMs · DRAM's · FIFOs · FIFO's · BIOSs · NULLs · ENIACs", ["RAM's", "OS's", "ARM's", 'DRAMs', "DRAM's", 'FIFOs', "FIFO's", 'BIOSs', 'NULLs', 'ENIACs']],
  ['fig-1-1', "ram's · os's · Mac's", ["ram's", "os's", "mac's"]],
  ['fig-1-1', 'DRAM-only · SYN-ACK', ['DRAM', 'SYN', 'ACK']],
  ['fig-3-5', "RAM's · OS's · ram's · os's", []],
  ['fig-16-10', 'DRAM-only · DRAMs', []],
  // ---- H3: a term the book marks with a key-term span is a concept it teaches, never a name a mention credits:
  // Ethernet (key-term at ch8-ethernet-p1) fails at Figs 8.2 and 8.7, passes from Fig 8.8; JavaScript (taught at
  // ch11-modern-p1) fails at Fig 5.11, passes from Fig 11.14
  ['fig-8-2', 'Ethernet', ['ethernet']],
  ['fig-8-7', 'Ethernet', ['ethernet']],
  ['fig-8-8', 'Ethernet', []],
  ['fig-5-11', 'JavaScript', ['javascript']],
  ['fig-11-14', 'JavaScript', []],
  // ---- H4: the prose's loss does not teach "los" (the plural of lo, untaught before Chapter 9)
  ['fig-4-13', 'los', ['los']],
  // ---- H5: a part tagline never teaches: Part II's end-of-part teaser names Part III's people; each passes only
  // after a paragraph writes it
  ['fig-8-1', 'Baran · Cerf · Kahn · Berners-Lee · Eich', ['baran', 'cerf', 'kahn', 'berners lee', 'eich']],
  ['fig-9-2', 'Baran', []],
  ['fig-10-2', 'Cerf · Kahn', []],
  ['fig-11-1', 'Berners-Lee', []],
  ['fig-12-2', 'Eich', []],
  // ---- the eleven false flags, fixed in the checker (each: the figure just before its teaching fails, the first
  // figure after passes, and the figures the review named pass)
  // Diffie–Hellman: "Diffie–Hellman (1976), which is key agreement" at ch11-crypto-p7 (the year is skipped)
  ['fig-11-10', 'Diffie–Hellman', []],
  ['fig-11-11', 'Diffie–Hellman', []],
  ['fig-11-13', 'Diffie–Hellman', []],
  ['fig-14-1', 'Diffie–Hellman', []],
  // SHA-256: "SHA-256 is the workhorse" at ch11-crypto-p4 (a definitional sentence), though its glossary section is held
  ['fig-11-8', 'SHA-256', ['sha 256']],
  ['fig-11-9', 'SHA-256', []],
  ['fig-14-2', 'SHA-256', []],
  ['fig-14-13', 'SHA-256', []],
  ['fig-18-6', 'SHA-256', []],
  // month and chapter abbreviations are everyday shorthand (COMMON); dec stays out (the book writes DEC, the company)
  // and mar stays out of the list (MAR in capitals must be taught; mar in lower case is a dictionary word)
  ['fig-9-2', 'Oct', []],
  ['fig-11-1', 'Aug · Apr · Ch 3', []],
  ['fig-1-1', 'Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov · Ch', []],
  ['fig-1-1', 'DEC', ['DEC']],
  ['fig-1-1', 'Dec', ['dec']],
  ['fig-1-1', 'MAR', ['MAR']],
  // ERROR with its caret (grep ^ERROR) is judged by its letters; a caret makes no abbreviation everyday
  ['fig-4-16', '^ERROR · ERROR', []],
  ['fig-1-10', '^EAX', ['EAX']],
  // etcd: 'Kubernetes' "source of truth", etcd, runs' at ch17-consensus-p1 (a reverse apposition)
  ['fig-17-4', 'etcd', ['etcd']],
  ['fig-17-5', 'etcd', []],
  ['fig-17-8', 'etcd', []],
  // virtual machine and VM: "A virtual machine imitates an entire computer" and "lightweight VMs" at ch4-security-p6
  // (a generic definition; a plural abbreviation placed as its singular)
  ['fig-4-18', 'virtual machine · VM', ['virtual machine', 'VM']],
  ['fig-4-18', 'VMs', ['VMs']],
  ['fig-4-19', 'virtual machine · VM · VMs', []],
  // ---- the same placement class
  // page table and page fault, emphasised where Chapter 1 introduces them (ch1-memory-p9 and p10)
  ['fig-1-15', 'page table · page fault', ['page table', 'page fault']],
  ['fig-2-1', 'page table · page fault', []],
  ['fig-br-3', 'page fault', []],
  ['fig-br-4', 'page table · page fault', []],
  ['fig-br-5', 'page table', []],
  // mutex: "a semaphore admits one process at a time, a mutex;" at ch4-ipc-p12 (a naming apposition)
  ['fig-4-17', 'mutex', ['mutex']],
  ['fig-4-18', 'mutex', []],
  ['fig-6-5', 'mutex', []],
  // control plane: "control-plane components (the parts that decide what should run where)" at ch17-k8s-p1
  ['fig-17-2', 'control plane', ['control plane']],
  ['fig-17-3', 'control plane', []],
  ['fig-17-10', 'control plane', []],
  // JSON, written only in Chapter 12's lead (a chapter lead teaches): fails before it, in capitals and lower case
  ['fig-11-15', 'JSON · json', ['JSON', 'json']],
  ['fig-12-1', 'JSON · json', []],
  // ---- teaching places: a table row that expands or defines its term teaches it; one whose cells are values does not
  // HDD (spinning disk) in Chapter 1's memory table (between Figs 1.14 and 1.15)
  ['fig-1-14', 'HDD', ['HDD']],
  ['fig-1-15', 'HDD', []],
  // the same table's value rows and value cells teach nothing: SATA ("SATA bus"), NVMe ("SSD (NVMe)"), L2 ("L2 Cache")
  ['fig-1-15', 'SATA · NVMe · L2', ['SATA', 'nvme', 'l2']],
  // Chapter 3's register table defines each register in its second cell ("Counter: used for loop counts ...")
  ['fig-3-3', 'RDX · RCX · rbx', ['RDX', 'RCX', 'rbx']],
  ['fig-3-4', 'RDX · RCX', []],
  ['fig-br-1', 'rbx', []],
  ['fig-br-2', 'RCX', []],
  // Chapter 4's scheduling table expands and defines each policy ("First-come, first-served. Run processes ...")
  ['fig-4-3', 'FCFS · SJF · MLFQ', ['FCFS', 'SJF', 'MLFQ']],
  ['fig-4-4', 'FCFS · SJF · MLFQ', []],
  ['fig-4-5', 'FCFS · SJF · MLFQ', []],
  // Chapter 4's IPC table: the Named pipe (FIFO) row defines its head, so FIFO is taught from Fig 4.15; so do the
  // Semaphore and Shared memory rows, each a one-sentence definition; the signals the Signal row lists in a description
  // cell are not taught by it
  ['fig-4-14', 'FIFO', ['FIFO']],
  ['fig-4-15', 'FIFO', []],
  ['fig-4-14', 'semaphore · shared memory', ['semaphore', 'shared memory']],
  ['fig-4-15', 'semaphore · shared memory', []],
  ['fig-4-15', 'SIGKILL', ['SIGKILL']],

  // ==== section 19 (the review of the section 18 freeze) ===============================================================
  // ---- A: a writing in a sentence that points elsewhere places no abbreviation, nor does a mention of one that is never
  // credited by a mention (a noMention glossary term, or one the book first writes inside held material); only a gloss
  // of it does. DNS, written before Chapter 10 only in the Part III teaser (ch4-ipc-p15), fails at Fig 8.12 and passes
  // from Chapter 10 (its lead writes it) and after its teaching paragraph ch11-dns-p1
  ['fig-8-12', 'HTTP, DNS, SSH', ['dns']],
  ['fig-10-1', 'DNS', []],
  ['fig-11-5', 'DNS', []],
  // ASLR (taught nowhere outside held material; ch1-memory-p11's sentence points to Chapter 3) fails from Fig 2.1 on;
  // DEP, glossed there ("the defence called DEP"), passes from Fig 2.1 and fails before
  ['fig-2-1', 'ASLR · DEP', ['aslr']],
  ['fig-1-15', 'DEP', ['dep']],
  // CFI (Chapter 3's closing list) and HTTPS (Chapter 11's lead), never glossed outside held material, fail where the
  // review placed them and at the book's last figure; SBOM, first written in held Chapter 15 and then only in a sentence
  // pointing to it (ch17-microservices-p7), fails at Fig 18-trace
  ['fig-br-1', 'CFI', ['cfi']],
  ['fig-11-1', 'HTTPS', ['https']],
  ['fig-18-6', 'HTTPS · ASLR · CFI', ['https', 'aslr', 'cfi']],
  ['fig-18-trace', 'SBOM', ['SBOM']],
  // the older cases of the class, first written in held material: CVE (a bare identifier, ch4-vm-p17) and CA (ch14-tls-
  // pqc-p3) fail after those writings; GCHQ, glossed by a possessive apposition at ch14-history-p6 ("GCHQ, Britain's
  // signals-intelligence agency"), passes from Fig 14.2 and fails at Fig 14.1
  ['fig-4-12', 'CVE', ['CVE']],
  ['fig-14-12', 'CA', ['CA']],
  ['fig-14-1', 'GCHQ', ['GCHQ']],
  ['fig-14-2', 'GCHQ', []],
  // ... while a gloss in a pointer sentence still places it (RAM, SSD at ch1-memory-p2, a sentence naming Section 03;
  // IRQ at chBridge-io-p2, naming Section 02), and neither an aside in parentheses that cites another section or chapter
  // (SIGSEGV at ch4-vm-p12, DH at ch14-publickey-p6) nor a figure of the writing's own chapter (MEM at ch1-cpu-p7, "Fig
  // 1.11 adds a fifth stage, MEM, ..."; ES2015 at ch12-loop-p4) makes the sentence point elsewhere; a part's number is
  // the book's numbering (II, III, IV); SQL opens a sentence of Chapter 13's lead with a verb in -s (the generic form)
  ['fig-1-14', 'RAM · SSD', ['RAM', 'SSD']],
  ['fig-1-15', 'RAM · SSD', []],
  ['fig-br-7', 'IRQ', []],
  ['fig-4-8', 'SIGSEGV', ['SIGSEGV']],
  ['fig-4-9', 'SIGSEGV', []],
  ['fig-14-8', 'DH', ['DH']],
  ['fig-14-9', 'DH', []],
  ['fig-1-10', 'MEM', ['MEM']],
  ['fig-1-11', 'MEM', []],
  ['fig-12-4', 'ES2015', []],
  ['fig-18-5', 'Part II · Part III · Part IV', []],
  ['fig-12-7', 'SQL', ['SQL']],
  ['fig-13-1', 'SQL', []],
  // ---- E: a possessive apposition glosses like an article one: C++ at ch5-survives-p1 ("in C++, C's best-known
  // descendant."), between Figs 5.9 and 5.10
  ['fig-5-9', 'C++', ['c++']],
  ['fig-5-10', 'C++', []],
  ['fig-5-11', 'C++', []],
  // ---- F: a run of hexadecimal groups (a MAC address) is notation, taught once the prose writes "hexadecimal"
  // (ch1-cpu-p2, between Figs 1.8 and 1.9); a word in capitals that the prose writes in lower case passes like the word
  // (HEXADECIMAL, FILESYSTEM, DESCRIPTOR), unless the book writes it in capitals (COMMIT); a lone group is judged as before
  ['fig-8-9', 'B8:27:EB:9C:DA:C7 · 9C:DA:C7 · 8C:85:90:1F:33:42 · MAC ADDRESS · 48 BITS IN HEXADECIMAL', []],
  ['fig-1-8', '9C:DA:C7 · HEXADECIMAL', ['9C:DA:C7', 'HEXADECIMAL']],
  ['fig-1-9', '9C:DA:C7 · 8c-85-90', []],
  ['fig-8-9', 'DA', ['DA']],
  ['fig-1-1', '10:25:11 · 12:30', []],
  ['fig-4-13', 'MAIN FILESYSTEM', []],
  ['fig-br-3', 'INTERRUPT DESCRIPTOR TABLE', []],
  ['fig-4-13', 'COMMIT', ['COMMIT']],
  ['fig-1-1', 'FILESYSTEM', ['FILESYSTEM']],
];
// item 2b: the paragraph known-terms places each term at (the first prose gloss)
const PLACED = { register: 'ch1-vonneumann-p4', byte: 'ch1-cpu-p2', compiler: 'ch1-vonneumann-p3', thread: 'ch7-gil-p1' };
// section 18: where known-terms places each fixed term, and by which route (the paragraph, and the source)
const PLACED18 = { 'Diffie–Hellman': ['ch11-crypto-p7', 'prose gloss (which)'], 'SHA-256': ['ch11-crypto-p4', 'prose gloss (definition)'],
  'virtual machine': ['ch4-security-p6', 'prose gloss (generic)'], mutex: ['ch4-ipc-p12', 'prose gloss (naming)'], etcd: ['ch17-consensus-p1', 'prose gloss (reverse)'],
  'control plane': ['ch17-k8s-p1', 'prose gloss (modifier)'], 'page table': ['ch1-memory-p9', 'emphasis'], 'page fault': ['ch1-memory-p10', 'emphasis'] };
// ... and the abbreviations: a plural placed as its singular (VM), a chapter lead (JSON), defining table rows (the
// nearest id before each table: HDD after ch1-memory-p2, the registers after ch3-registers-p3, the policies after
// ch4-scheduling-p4, FIFO after ch4-ipc-p2); never a value row or a description cell (SATA, SIGKILL), never a part tagline
const ABBR18 = { VM: 'ch4-security-p6', JSON: 'ch12-hero-lead', HDD: 'ch1-memory-p2', RCX: 'ch3-registers-p3', RDX: 'ch3-registers-p3', RBX: 'ch3-registers-p3',
  FCFS: 'ch4-scheduling-p4', SJF: 'ch4-scheduling-p4', MLFQ: 'ch4-scheduling-p4', FIFO: 'ch4-ipc-p2' };
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
for (const [t, [p, src]] of Object.entries(PLACED18)) {
  const e = kt.j.taught[t];
  check(e && e.paragraph === p && e.source === src, `placed  ${t} at ${e && e.paragraph} (${e && e.source}; expected ${p}, ${src})`);
}
for (const [t, p] of Object.entries(ABBR18)) {
  const a = kt.abbrev[t];
  check(a && a.paragraph === p, `abbreviation ${t} placed after ${a && a.paragraph} (expected ${p})`);
}
// section 19: where each abbreviation the review named is placed now, and by which writing (a plain writing, a gloss,
// a part number), and which are never placed (no gloss outside held material, no writing outside a pointer)
const ABBR19 = { DNS: ['ch10-hero-lead', 'writing'], HTTP: ['ch7-types-p3', 'writing'], ARPANET: ['ch9-hero-lead', 'writing'], SQL: ['ch13-hero-lead', 'gloss (generic)'],
  GCHQ: ['ch14-history-p6', 'gloss (apposition)'], DEP: ['ch1-memory-p11', 'gloss (called)'], TTL: ['ch11-dns-p5', 'gloss (expansion)'], RAM: ['ch1-memory-p2', 'gloss (expansion)'],
  MEM: ['ch1-cpu-p7', 'writing'], SIGSEGV: ['ch4-vm-p12', 'writing'], DH: ['ch14-publickey-p6', 'writing'], II: ['ch1-kernel-p10', 'part number'] };
for (const [t, [p, by]] of Object.entries(ABBR19)) {
  const a = kt.abbrev[t];
  check(a && a.paragraph === p && a.by === by, `abbreviation ${t} placed after ${a && a.paragraph} by ${a && a.by} (expected ${p}, ${by})`);
}
{ const never = ['ASLR', 'CFI', 'HTTPS', 'CVE', 'CA', 'SBOM'], placed = never.filter(t => kt.abbrev[t]);
  check(!placed.length, `abbreviations never placed (no gloss outside held material, every other writing a mention): ${never.length - placed.length} of ${never.length}${placed.length ? ` (placed: ${placed.join(', ')})` : ''}`); }
{ const e = kt.j.taught['C++']; check(e && e.paragraph === 'ch5-survives-p1' && e.source === 'prose gloss (apposition)', `placed  C++ at ${e && e.paragraph} (${e && e.source}; expected ch5-survives-p1, prose gloss (apposition))`); }
check(!kt.abbrev.SATA && (!kt.abbrev.SIGKILL || kt.abbrev.SIGKILL.paragraph !== 'ch4-ipc-p2'),`abbreviations: SATA (a value cell) ${kt.abbrev.SATA ? 'placed' : 'not placed'}; SIGKILL (a description cell in the table after ch4-ipc-p2) ${kt.abbrev.SIGKILL ? 'placed at ' + kt.abbrev.SIGKILL.paragraph : 'not placed'}`);
// H3: no name is a term the book marks with a key-term span (outside the figure cards)
{
  const marked = new Set();
  for (const p of PARTS) { const h = readPart(ROOT, p), cards = [...h.matchAll(CARD)].map(m => [m.index, m.index + m[0].length]);
    for (const m of h.matchAll(/<span class="key-term">([\s\S]*?)<\/span>/g)) if (!cards.some(([a, b]) => m.index >= a && m.index < b)) marked.add(plain(m[1]).toLowerCase()); }
  const bad = kt.j.names.filter(n => marked.has(n.toLowerCase()));
  check(!bad.length && ['Ethernet', 'Kubernetes', 'Raft', 'JavaScript'].every(n => !kt.j.names.includes(n)), `names: ${bad.length} of ${kt.j.names.length} are marked with a key-term span (Ethernet, Kubernetes, Raft, JavaScript listed: ${['Ethernet', 'Kubernetes', 'Raft', 'JavaScript'].filter(n => kt.j.names.includes(n)).length})`);
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
// section 18, synthetic tree: a scratch copy of the tree with, before Fig 1.1 (in ch1-context-p1 and a table after
// it), plain uses of eight everyday words made glossary terms of ch18-final (they must still fail at Fig 1.1, as
// glossary terms not yet taught: none of the new cues credits a plain use), one control sentence per new cue for a
// planted term (each must pass), a pointer sentence's emphasis and a part tagline's gloss and abbreviation (they must
// fail), and a table with an expanding row, three defining rows (a phrase, a sentence), a row whose second cell is two
// words, a value row, a header row and a description cell
{
  const T = path.join(OUT, 'taught-test', 'tree18'); fs.rmSync(T, { recursive: true, force: true }); mkdirp(T);
  for (const p of PARTS) fs.copyFileSync(path.join(ROOT, p + '.html'), path.join(T, p + '.html'));
  const GL = JSON.parse(fs.readFileSync(path.join(ROOT, 'glossary.json'), 'utf8'));
  const PLAIN = ['safety', 'release', 'group', 'key', 'bucket', 'port', 'node', 'edge'];
  const CUE = ['qzdefword', 'qzgen machine', 'qznamed', 'qzrev', 'qzmod plane', 'Qzyear–Pair', 'qzemph table', 'qzrowterm', 'qznlterm', 'qzposs'];
  const NEG = ['qzpointed', 'qztagterm', 'qzvalterm'];
  // section 19 (A): two abbreviations made glossary entries of ch18-final that its paragraphs never write, so they are
  // taught nowhere (noMention): one only mentioned before Fig 1.1, one glossed there by its expansion
  const NOMEN = ['QZNOMEN', 'QZNOMGL'];
  for (const t of [...PLAIN, ...CUE, ...NEG, ...NOMEN]) GL.entries[t.toLowerCase()] = { term: t, part: 'part-5', section: 'ch18-final' };
  fs.writeFileSync(path.join(T, 'glossary.json'), JSON.stringify(GL));
  const plainUses = ' Safety is important here, and the release of the report is late. A key opens the lock; each node has a bucket. The key is in the drawer. The release is the last step. We packed a lock, a counter, a bucket. Node 3 sends a packet over the edge router (a box) on port number 80 (16 bits). Chapter 9 shows the <em>port</em> and the <em>node</em>. A bucket is full. Ports, nodes, edges, groups and keys. '
    // section 19 (B): a line break in the HTML source mid-sentence is no sentence start (the definitional cue must not
    // read "and\nsafety is a" or "as a\ngroup is a" as one); (E) a possessive apposition in a list or a pointer is no gloss
    + ' We tried it, and\nsafety is a concern; we treat them as a\ngroup is a mistake. We met the port, Kim\'s lamp, a cup. Then the bucket, Kim\'s subject of the next chapter, broke. ';
  const cues = ' Qzdefword is a planted term. A qzgen machine imitates a planted thing. Initialised to one, a planted counter admits one at a time, a qznamed; that is all. The planted store\'s "source", qzrev, runs a protocol. It has qzmod-plane parts (the pieces that decide what runs). In Qzyear–Pair (1976), which is a planted method, two sides agree. The kernel keeps <em>qzemph tables</em> that map pages. Chapter 9 shows the <em>qzpointed</em> at work. '
    // section 19: a real sentence start after a line break in the source (B), and a possessive apposition (E), each teach
    + ' That is all.\nQznlterm is a planted term. We use the qzposs, Kim\'s planted device. '
    // section 19 (A): a pointer sentence's mention and a noMention term's mention place no abbreviation; a gloss does
    + ' We saw QZNOMEN today. A planted noun (QZNOMGL) sits here. Chapter 9 covers QZPTRA and more. Section 04 explains the planted store (QZPTRB). ';
  const table = '<table class="summary-table"><tr><th>Name</th><th>What it is</th><th>Size</th></tr><tr><td>QZEXP (a planted expansion)</td><td>On the die</td><td>5 ms</td></tr>'
    + '<tr><td>QZDEF</td><td>Planted: a definition of the term, with QZDESC named in it.</td><td>10 GB</td></tr><tr><td>qzrowterm</td><td>Planted row. It defines the term here.</td><td>1</td></tr>'
    + '<tr><td>QZSENT</td><td>A planted sentence that defines it.</td><td>2</td></tr><tr><td>QZSHORT</td><td>Fast disk.</td><td>3</td></tr>'
    + '<tr><td>QZVAL qzvalterm</td><td>On the board</td><td>8 GB</td></tr><tr><th>QZHEAD</th><th>Header</th><th>Row</th></tr></table>';
  let h = fs.readFileSync(path.join(T, 'part-1.html'), 'utf8');
  const at = h.indexOf('id="ch1-context-p1"'), open = h.indexOf('>', at) + 1, close = h.indexOf('</p>', open) + 4;
  h = h.slice(0, open) + plainUses + cues + h.slice(open, close) + table + h.slice(close);
  const tg = h.search(/<p class="part-tagline"[^>]*>/), tge = h.indexOf('>', tg) + 1;
  h = h.slice(0, tge) + ' QZTAGX and qztagterm (a planted gloss), ' + h.slice(tge);
  fs.writeFileSync(path.join(T, 'part-1.html'), h);
  const K = await runKnownTerms(T + '/', path.join(OUT, 'taught-test', 'known-terms-tree18.json'));
  const f = findFigure(T + '/', 'fig-1-1'), c = taughtContext(K, T + '/', f);
  const run1 = label => taughtYet(label, c.known, K.glossary, c.prior);
  const a = run1(PLAIN.join(' · ')), aG = [...new Set(a.filter(b => b.why === 'a glossary term not yet taught').map(b => b.token))];
  check(f.at > close && aG.length === PLAIN.length, `synthetic tree: plain uses of ${PLAIN.join(', ')} before Fig 1.1 -> fail as glossary terms not yet taught: ${aG.length} of ${PLAIN.length} ${JSON.stringify(aG)}`);
  { const nl = ['safety', 'group'].filter(t => K.j.taught[t] && K.j.taught[t].part === 'part-1' && /definition/.test(K.j.taught[t].source));
    check(!nl.length && ['safety', 'group'].every(t => aG.includes(t)), `synthetic tree (section 19, B): "and\\nsafety is a", "as a\\ngroup is a" -> placed by the definitional cue: ${nl.length ? nl.join(', ') : 'none'}; both fail at Fig 1.1`); }
  const b = [...new Set(run1(CUE.join(' · ')).map(x => x.token))];
  check(!b.length, `synthetic tree: one control per new cue (definition, generic, naming, reverse, modifier, a year skipped, emphasis, table row) -> fails ${JSON.stringify(b)}`);
  const n = [...new Set(run1(NEG.join(' · ')).map(x => x.token))];
  check(n.length === NEG.length, `synthetic tree: emphasis in a pointer sentence, a part tagline's gloss, a value row's term -> fail ${JSON.stringify(n)}`);
  { const pass = [...new Set(run1('QZPTRB · QZNOMGL').map(x => x.token))], fail = [...new Set(run1('QZPTRA · QZNOMEN').map(x => x.token))];
    check(!pass.length && fail.length === 2, `synthetic tree (section 19, A): an expansion in a pointer sentence and a noMention term's expansion place them (fails ${JSON.stringify(pass)}); a pointer sentence's mention and a noMention term's mention do not (fail ${JSON.stringify(fail)})`); }
  const ab = run1('QZEXP · QZDEF · QZSENT'), abN = [...new Set(run1('QZSHORT · QZVAL · QZHEAD · QZDESC · QZTAGX').map(x => x.token))];
  check(!ab.length && abN.length === 5, `synthetic tree: abbreviations of an expanding row and of rows defined by a phrase and by a sentence pass (${JSON.stringify(ab.map(x => x.token))}); of a row whose second cell is two words, a value row, a header row, a description cell and a part tagline fail ${JSON.stringify(abN)}`);
}
// the figures themselves: Fig 1.1 (v4) and Fig 1.2 (Enigma) as they stand in the tree
for (const id of ['fig-1-1', 'fig-1-2']) {
  const fig = findFigure(ROOT, id), c = taughtContext(kt, ROOT, fig);
  const got = svgTexts(fig.svg).flatMap(t => taughtYet(t.s, c.known, kt.glossary, c.prior).map(b => b.token));
  check(!got.length, `${id.padEnd(9)} (the figure's own text) -> fails ${JSON.stringify(got)}`);
}
console.log(`taught-test: ${n - bad} of ${n} cases hold`);
process.exit(bad ? 1 : 0);
