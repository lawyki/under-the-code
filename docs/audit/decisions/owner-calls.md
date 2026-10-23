# Owner calls · decided under the owner's delegation (2026-10-23)

Owner, 2026-10-23: "you just take the best option / pedagogic etc. knowing the book's goal", and "reword for honesty on the legal / privacy". Criteria: the four laws (`CLAUDE.md`), the fact ledger (`UNDER.md` §4g), the §4w arc devices kept whole, the lightest change that does the job. Each card's options are in `docs/audit/owner-calls.md` and on the decision page. Branch `owner-calls`; deployed only on the owner's word.

## Applied

| Card | Decision | Why |
|---|---|---|
| ch18-intersect | (a), all five reader fixes; the paragraph now ends "has both the words and the discipline that produced them" | Law 4: five terms or phrases readers could not pass. The four moves stay listed once, in ch18-final-p3 (card ch18-moves). |
| ch18-moves | (a) | Law 2: the same list twice in one chapter. |
| ch18-bet | (a), cut | Law 2: restates the closing note's first sentences. |
| ch18-finalp3 | (a), p3 begins "The reasoning skills the book asked for" | Law 2: its first two sentences restated ch18-future-p1 and ch18-future-p3. "The vocabulary is durable." kept. |
| ch18-fragments | final-p1's two fragments joined into the sentence they continue (no word changed); the closers of p3 and p4 kept | The fragments are the clipped pattern the editorial brief lists; p4 is the book's last paragraph, restored verbatim in Pass 27 as yours. |
| ch18-fig186 | (a), two sentences | Law 3. The closing claim kept almost word for word; the Kubernetes and AWS chain, which the picture does not draw, dropped. |
| ch14-coda | keep | §4w asked for consolidation codas; the ratchet is now glossed where it appears. |
| ch4-mmu | keep (the recommendation) | p4 holds the book's only derivation of the 512 GiB sum. |
| ch15-fig152 | (a), plus ASLR drawn before DEP (the Fig 3.11 card's fix, same figure family) and "1988 · buffer overflow" | §4g: the order implied ROP broke ASLR; dates as sourced in owner-calls.md. |
| ch15-fig154, ch15-fig156 | (a) | §4g (ARP: persistence, not speed); IMDSv2 is a default, not a mandate. |
| ch15-fig158 | (a), shortened to fit its 640-unit box; "AV" and "BSODs" spelled out | Sourced estimate; untaught abbreviations. |
| ch15-fig159 | (a), "almost every" in label, title and caption; caption otherwise whole | The six-pattern unification is a §4w arc device. |
| ch13-psn | (b), "the 2011 Sony Pictures breach by LulzSec (tens of thousands of customer accounts)" | PSN was never confirmed as SQL injection; LulzSec's "a million" was a claim, Sony counted about 37,500. |
| ch13-hash | (a) | The column as drawn holds stored passwords. |
| ch12-fig129row, ch12-fig129owasp, ch12-fig1210lax, ch12-fig1210form | (a) each | Facts as in owner-calls.md. |
| p30-fig123 | (b): `setTimeout(f, 0)` named in ch12-loop-p2, `console.log` in the Fig 12.3 caption | Readers met both in the figure before the text named them. |
| ch11-fig117cap, ch11-fig117short | the short caption | It removes the wrong timing claim with the retelling. |
| ch11-fig117label | (a) | The real reply is dropped for arriving second, not for its source. |
| ch10-captions, ch10-fig1010cap | both captions cut to two sentences; Fig 10.10's claim narrowed | Law 3; Windows ships no SYN cookies. |
| ch10-fig1011 | (a) | The prose puts the MSS beside the hash. Glossary: "cookie" kept by name (`scripts/build-glossary.js`), its cue having gone with the long caption. |
| br-fig3, br-fig3cap | (a); the optional "e.g." before handler names not added | §4g: SYSCALL does not go through the IDT. |
| p30-hero1 | (a): the dashed line labelled "software that runs on the CPU" | Readers took it for a wire. |
| p30-hero3 | (a): one-line key for addresses, a pointer from "stack top" to the newest call | Readers could not tie "high/low address" or "stack top" to anything. |
| p30-fig66, p30-fig69, p30-hero12, p30-cover | accept (the recommendations) | |
| keep-bundle | keep all | |
| (punch list) | the Ch4 hero's title id `svgt-part2-1` renamed `svgt-part2-ch4-hero` | It duplicated Fig 4.1's; no duplicate id is left in any part. |

## Blind retest (workflow `owner-calls-retest`, Sonnet 5.5) and one revision

Gate 2 on the two changed heroes: hero-ch1 and hero-ch3 each passed with both fresh readers (4 of 4). Newcomer and expert per changed chapter: Chapters 13 and 18's expert, all clear. Revised from their flags: ch18-intersect-p3's example is now Bitcoin's ledger (named in Chapter 14; "a blockchain" is never taught); Fig BR.3's two hardware vectors read "32+" (the "…" looked like the gap rows) and its caption's last sentence now names exceptions and interrupts, since "every involuntary entry" clashed with the int instruction; Fig 10.10's caption says Linux and FreeBSD, and Fig 10.11's says spoofed SYNs never get state (both were overclaims in the new wording); Fig 15.9's footer says the defence is "usually" already known, to match "almost every". Left: flags on terms the kept-original figures never taught (Chapters 12 and 15) and on wording the edits did not touch; they belong to the punch list.

## Not applied

- **Chapter 3** (ch3-aleph, ch3-fig37, ch3-fig38cap, ch3-fig38head, ch3-fig39, ch3-fig310, ch3-fig311, ch3-captions): Claude's safety filter stopped work on these figures twice on 2026-10-23 (and a Fig 3.7 redesign on 2026-10-11). Left for the owner; the recommended text is in `docs/audit/owner-calls.md`, Chapter 3.
- **marks-wording**: a privacy switch, not a teaching choice; the owner's.
- **out-privacy** and the rest of the privacy notice: below.

## Privacy and legal text (owner: "reword for honesty")

Every claim on the account page, in the emails and in the video viewer was checked against `functions/`, `schema.sql`, `wrangler.toml`, `public/*.js` and the live response headers (workflow `privacy-claims-verify`: 58 claims, a Sonnet 5.5 skeptic on each), and the load-bearing ones again by hand. Rewritten in `public/account.html` (#privacy, the page intro, the delete button's second-press label and its success message) and in the confirmation mail (`functions/api/auth/_account.js`):

- "collects nothing", "no analytics, no trackers": now no analytics or tracking scripts, no cookie before sign-in, and Cloudflare named as the host that sees IP address and browser details and keeps its own logs.
- "never leaves your device": the first sign-in on a device can upload that browser's place; signed-out marks and settings are named.
- Added: the random account ID, session start and end, chapter and section numbers; the two cookies (`__Host-under_session`, `under_signedin`, 180 days); that the abuse counters are keyed on IP address as well as email, exist for anyone who uses the forms, and are pseudonymous, not anonymous.
- Mail: the once-a-day sign-in link after a password attempt on an account with no password or passkey, and what a stranger's sign-up attempt sends (at most 20 a day).
- out-privacy: "a Cloudflare D1 database in the European Union" replaced by the setup as it is (an Eastern Europe location hint, best effort; requests handled at the nearest data centre; Cloudflare a US company). The owner chose rewording over recreating the database with `--jurisdiction=eu`.
- Retention and deletion now say when things really go (at the next clean-up, which needs sign-in traffic; D1's restore history up to 30 days; this browser's own copy), instead of "immediately and completely".
- Rights added: access, correction, erasure, objection by email, and a complaint to the Finnish Data Protection Ombudsman.
- Passkeys described as not switched on yet; the private key "never received by this site" (a synced passkey's key does leave the device).
- "run by Google Ireland Limited" → "run by Google" (the entity depends on the reader's region); what Google receives now includes the video and the referring site.

Left for the owner (facts only he has, or legal choices): the controller's Business ID and postal address; the legal bases (contract, legitimate interest) and the basis for transfers to Cloudflare as a US company; whether hello@atheric.eu is read; the colophon's "© … YDT Holdings Oy" against LICENSE's "Yki Lähteenmäki / YDT Holdings Oy", and that no page states the CC BY-NC 4.0 licence (the colophon is owner text). Marks sync stays off; `docs/pass-25-copy.md` must be redrafted against the new notice before it is approved.
