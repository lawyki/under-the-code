# Owner read map · where the book is weakest

For the owner's one full read (brief, THE CLOSE). It starts where the book is weakest: the open owner calls, then the pictures that needed the most help, then the largest prose changes. Every screenshot is the picture at the Pass 30 close (2026-10-15) at 375 px (heroes and the cover at 1440 px), the still a reader with reduced motion sees; Figs BR.7, 6.6, 6.9 and 10.3 changed since in the pre-read audit (`docs/audit/decisions/`).

## 1. Open owner calls

- Pre-read audit (2026-10-17), read these first: `docs/audit/owner-calls.md`, chapter by chapter, each with options and a recommendation. Most are kept-original figures or captions that disagree with the corrected prose (Figs 3.7 to 3.11, BR.3, 10.10, 10.11, 11.7, 12.9, 12.10, 13.10, 15.2, 15.4, 15.6, 15.8, 15.9); the rest are owner text (the Aleph One pull-quote, Chapter 18's closing passages, Fig 18.6's caption), two verdicts left to you (Chapter 4 Section 03, ch14-tls-pqc-p10) and the privacy wording. All 36 open ones are on https://claude.ai/artifact/NAF7n8U6uuQ3kwdb8gwA15. What changed in each chapter, and why: `docs/audit/decisions/<ch>.md`.
- Pass 30, seven calls still open (`docs/pass-30-owner-calls.md`, also on the decision page): Figs 6.6, 6.9, 12.3 and heroes Ch1, Ch3, Ch12 (§A, failing Gate 2 after two rounds), and the cover (§C). Figs BR.7 and 10.3 also failed Gate 2; their notation is now taught (hex in ch1-cpu-p2, TCP's close states in ch10-handshake-p3). Figs 14.3 and 14.6 (§C) were redrawn in the audit.
- Every per-picture Gate 2 verdict, with the blind reader's words: `docs/pass-30-gate2-record.md`.
- Pass 29, Part I: `docs/pass-29-owner-calls.md`, closed or moved (`docs/pass-29-part1-open.md`: 68 fixed and 6 obsolete 2026-10-12, the prose rest closed 2026-10-15); the kept-original figure errors are in `docs/audit/owner-calls.md`.
- Pass 29, Part V: ch18-intersect-p3 (owner text): `docs/audit/owner-calls.md`, Chapter 18.
- Kept-original figures, "kept original, small on a phone" (settled, reported only): `docs/pass-30-owner-calls.md` §B and `UNDER.md` §5.

## 2. Section prose against its ceiling

Section prose (`scripts/count-prose.mjs`), the Pass 27 close (02f486b) count and its 5% ceiling (brief). The owner lifted the restrictions on 2026-10-15 ("No restrictions for now until I say so", UNDER.md §4ac); the overruns are terms readers could not pass, defined where first used. "Now" = `main` at eb7fe95, after the pre-read audit.

| Part | 02f486b | Ceiling | Now | Headroom |
|---|---|---|---|---|
| I | 12,095 | 12,700 | 13,089 | −389 |
| II | 10,891 | 11,436 | 11,396 | 40 |
| III | 14,012 | 14,713 | 15,577 | −864 |
| IV | 9,761 | 10,249 | 11,562 | −1,313 |
| V | 6,181 | 6,490 | 6,820 | −330 |

## 3. The five largest Pass 29 edits per part

Largest by changed words between the Pass 28 close (7d56482) and the Pass 29 close (32d3188); each with the place a newcomer stopped that it closed. Read the paragraph on the site by its anchor (part page, `#id`).

### Part I
- `ch1-transistor-p7` (219 words changed): why a material must switch itself, what doping does (n-type, p-type, the hole) before the junction; the reader no longer meets "semiconductor" as a bare word.
- `ch2-twos-p6` (199): 7 − 5 done on the adder with real bits, the carry falling off the eighth place, and the negative case; replaces the 2ⁿ − x algebra a newcomer could not follow.
- `ch1-memory-p11` (190): why a buffer overflow gets past the MMU, with the stack, the buffer and the return address explained before the attack.
- `chBridge-io-p4` (181): DMA through one concrete SSD read (command queue, doorbell, the drive copying itself) with the MMIO arithmetic that shows why the CPU cannot copy.
- `ch1-context-p8` (179): what Enigma did and what the Bombe looked for (a guessed phrase, the no-letter-to-itself flaw) before how it searched.

### Part II
- `ch4-scheduling-p10` (128): Little's law with numbers (10 a second, 2 seconds each, 20 inside) and why waits explode as arrivals near capacity.
- `ch6-modern-p4` (122): move semantics from what a vector is (three pointers), so "steal the buffer" becomes three pointer copies.
- `ch4-scheduling-p5` (115): CFS without jargon first: sorted by time had, leftmost runs next; the red-black tree named after the idea.
- `ch6-zerocost-p4` (113): the compile-time trade said once, with the two concrete swaps (template for pointer, constexpr for runtime work).
- `ch5-malloc-p7` (105): what a garbage collector does and why its pause breaks audio, with the audio numbers explained.

### Part III
- `ch9-routing-p2` (78): transit and peering as business deals, and what a prefix is, before BGP's announcements.
- `ch9-arpanet-p3` (72): Kleinrock's result in plain words (bursty traffic on one shared link beats reserved lines).
- `ch12-eich-p2` (61): closures and prototype inheritance said as what they do, not as names.
- `ch8-encoding-p6` (59): carrier, amplitude, frequency and phase in plain words, and what a symbol is, before QAM.
- `ch8-substrates-p3` (57): total internal reflection explained rather than named.

### Part IV
- `ch13-algebra-p6` (91): selection and projection pushdown in words and why the join keys must stay; the formula kept only where it reads.
- `ch13-acid-p8` (87): why two-phase locking is called that, and MVCC's versions explained.
- `ch14-history-p1` (76): why Caesar's cipher falls: letter frequencies, said before "frequency analysis".
- `ch13-algebra-p4` (72): why SQL keeps duplicates, with the ten paid orders as one example.
- `ch13-sql-p6` (71): what Selinger's optimiser does (costs from statistics, joins built up from small groups), and "most cited" stated without overclaim.

### Part V
- `ch18-future-p1` (81): the end of Moore's law in atoms and leakage, quantum computing's reach stated exactly.
- `ch16-numa-p4` (72): Spectre's mechanism (the secret picks which line is touched; the cache keeps it).
- `ch17-microservices-p8` (71): what a feature flag is, so the Knight Capital failure can be followed.
- `ch16-lockfree-p3` (55): what a store buffer is and which CPUs reorder, before the x = 1, flag = true example.
- `ch17-consensus-p2` (51): quorum glossed as a majority where Paxos first needs it.

## 4. Sections that needed two repair rounds

Pass 29 Part I took every section (24) through the per-section method with two repair rounds (UNDER.md §4ac); ch2-gates closed every point, the rest left open points listed in `docs/pass-29-owner-calls.md`, most since closed by the Part I close (`7eb1d7a`). Parts II to V went through the law-4 pass in one round per chapter, read blind by a newcomer and an expert.

## 5. Every Gate 2 fail and near-miss

Fails (five; three still owner calls: 6.6, 6.9, 12.3; BR.7's hex and 10.3's state names are now taught in the prose): screenshots `docs/pass-30-shots/<id>.png` (Pass 30 close), the calls in `docs/pass-30-owner-calls.md` §A.

Near-misses (failed two readers twice, passed only after repair round 2): Figs 1.5, 2.3, 2.9, 3.2, 3.6, 4.3, 4.5, 4.9, 4.18, 4.22, 5.1, 5.2, 5.8, 8.2, 9.5, 9.7, 9.9, 11.5, 11.9, 12.5, 16.7, 17.8 and the trace (fig-18-trace). Screenshots: `docs/pass-30-shots/near/<id>.png`.

## 6. Every hero and the cover

Each at 1440 px in `docs/pass-30-shots/heroes/<id>.png` (the size a reader sees it). Gate 2 as for the figures: two blind readers, two repair rounds at most.

- Owner calls (failing after two rounds): Ch1, Ch3, Ch12; `docs/pass-30-owner-calls.md` §A.
- Passed after repair round 2: Ch2 (redrawn as the circuit of its own formula), the Bridge, Ch10, Ch14, the cover.
- Passed after repair round 1: Ch4, Ch5, Ch6, Ch7, Ch8, Ch11, Ch13, Ch15, Ch17, Ch18.
- Passed on the first read: Ch9, Ch16.

The redrawn heroes changed most: Ch2 (circuit), Ch10 (the three messages now run in turn), Ch14 (the curve drawn true to its equation), Ch15 (each attack stopped at a named ring), Ch17 (a failed follower added), the Bridge (the five pieces with their jobs).
