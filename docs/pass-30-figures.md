# Pass 30 · the figure ledger

Brief: `docs/pass-29-30-brief.md`. Lists below written 2026-10-11 from `docs/pass-28-figures.md` at the Pass 28 close (7d56482).

## Security figures (concept level)

Every figure the git history of `docs/pass-28-figures.md` (`git log -p`) ever marked *deferred: conceptual pass* or *held: owner decision* that now reads *done*. Their intended message is the defence or the idea; no repair moves them toward attack mechanics.

| Part | Figure |
|---|---|
| 1 | `fig-br-4` Fig BR.4 · The MMU · silicon between the CPU and the RAM |
| 1 | `fig-br-5` Fig BR.5 · The TLB · why the walk usually doesn't happen |
| 1 | `fig-br-6` Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back |
| 1 | `fig-br-7` Fig BR.7 · The physical address space · devices among the RAM |
| 1 | `fig-br-8` Fig BR.8 · Direct memory access · the device writes RAM by itself |
| 1 | `fig-br-9` Fig BR.9 · Hardware features → kernel → abstractions |
| 2 | `fig-4-11` Fig 4.11 · Dirty COW: the race that broke Linux |
| 2 | `fig-5-7` Fig 5.7 · Leak vs use-after-free |
| 3 | `fig-9-10` Fig 9.10 · IP spoofing: a forged source field |
| 3 | `fig-9-11` Fig 9.11 · Pakistan/YouTube, 24 February 2008 |
| 3 | `fig-12-11` Fig 12.11 · CSP · the server tells the browser which scripts to trust, the browser refuses the rest |
| 4 | `fig-13-11` Fig 13.11 · Parameterised queries · code and data on separate wires |
| 4 | `fig-14-3` Fig 14.3 · Three hash properties · three different attacks |
| 4 | `fig-14-4` Fig 14.4 · Password storage · plaintext to hash to salted hash to slow KDF |
| 4 | `fig-14-6` Fig 14.6 · ECB's famous failure · structure leaks through |
| 4 | `fig-15-1` Fig 15.1 · STRIDE · the six classes of threat to enumerate |
| 4 | `fig-15-5` Fig 15.5 · SQL injection defence in depth · five layers, each independent |
| 4 | `fig-15-7` Fig 15.7 · Five generations of defence · firewall → IDS → SIEM → EDR → zero trust |
| 5 | `fig-18-6` Fig 18.6 · The closing zoom-out · the inverse of where Chapter 1 began |

19 figures.

## Kept original

The owner settled these on 2026-10-11. Not redrawn or edited. Gate 1 checks clipping, overlap and text outside the viewBox (must be zero); the 11 px label floor, the caption length and Gate 2 do not apply. A finding is reported to the owner with a screenshot and does not block v1.0.

| Part | Figure |
|---|---|
| 1 | `fig-3-7` Fig 3.7 · Stack frame of greet(): normal vs overflow |
| 1 | `fig-3-8` Fig 3.8 · The stack canary · a tripwire between buffer and return address |
| 1 | `fig-3-9` Fig 3.9 · ASLR · the same binary, three random load layouts |
| 1 | `fig-3-10` Fig 3.10 · Return-Oriented Programming · arbitrary computation from existing code |
| 1 | `fig-3-11` Fig 3.11 · The arms race, in one diagram |
| 1 | `fig-br-3` Fig BR.3 · The interrupt descriptor table · 256 doors into the kernel |
| 3 | `fig-10-10` Fig 10.10 · SYN flood: half-open connections fill the table |
| 3 | `fig-10-11` Fig 10.11 · SYN cookies: the state goes into the wire |
| 3 | `fig-11-7` Fig 11.7 · Cache poisoning · the attacker races the real answer |
| 3 | `fig-12-9` Fig 12.9 · XSS · three ways for attacker code to run with your origin's privileges |
| 3 | `fig-12-10` Fig 12.10 · CSRF · the cookie attaches to the cross-site request unless we add a token |
| 4 | `fig-13-10` Fig 13.10 · SQL injection · a single quote turns a SELECT into a tautology |
| 4 | `fig-15-2` Fig 15.2 · The arms race continued · Fig 3.11 extended through 2026 |
| 4 | `fig-15-3` Fig 15.3 · Man-in-the-middle · with and without TLS |
| 4 | `fig-15-4` Fig 15.4 · ARP spoofing · poisoning the address-resolution cache |
| 4 | `fig-15-6` Fig 15.6 · SSRF · the server makes the request the attacker can't |
| 4 | `fig-15-8` Fig 15.8 · Stuxnet · four zero-days, a USB jump, sabotage of physical machines |
| 4 | `fig-15-9` Fig 15.9 · The attack-pattern map · every specific exploit reduces to a few patterns |

18 figures.

## Handed over by Pass 29 (figure text Pass 29 may not change)

Found by Pass 29 Part I and its Sonnet 5.5 verification (2026-10-11; UNDER.md §4ac). Fix in the figure's turn; log each fact in §4g.

| Figure | Finding | Fix |
|---|---|---|
| `fig-1-6` | The 2017 Epyc point (a four-die package) sits on the two-year line the caption says the chips fall below after about 2015 | Re-check the data point; the caption is an open owner call (docs/pass-29-owner-calls.md) |
| `fig-2-1` | Strip: "half the span" (binary) against "a sixth of the span" (ternary) uses two different baselines | One baseline: rails give a half for binary and a quarter for ternary |
| `fig-2-2` | Strip: "closed is 1, open is 0" credits Shannon with a convention he did not use (his 1938 paper gave 0 to the closed circuit's hindrance) | "label closed 1, open 0" |
| `fig-2-9` | Title "How a signed overflow becomes a buffer overflow": the bug is a signed-to-unsigned conversion (CWE-195) | "How a signed length becomes a buffer overflow" |
| `fig-2-10` | Caption repeats "after an implied leading 1", which ch2-float-p6 now says | Drop the phrase (say it once) |
| `fig-2-12` | Strip: "570 m" is 0.34 s × 1,676 m/s (Mach 5); GAO gives the 0.3433 s drift and a range-gate shift, not 570 m | "about 570 m at Mach 5" |
| `fig-3-3` | Strip: RFLAGS "set by every arithmetic operation" (INC leaves CF; MULX sets none) | "set by most arithmetic operations" |
| `fig-3-4` | Strip: "structures larger than 16 bytes are passed by a hidden pointer" (System V ABI 3.2.3: class MEMORY, copied onto the stack) | "structures larger than 16 bytes are copied onto the stack" |
| `fig-3-6` | Label, desc and strip give the return address as "main+5"; the section's own listing puts it at main+19 | "main+19" in all three |

Not queued: Fig 1.5's "3 nm" is owner-ruled (UNDER.md §5); a change would be a re-ruling request to the owner, not a repair.

## Owner's direction for Gate 2 (2026-10-12)

After reading the book again from the start, the owner found Fig 1.1 not understandable for a newcomer ("someone lower IQ would never figure out what that means") while Fig 1.2 Enigma works because it draws the real machine. His rule for every repair: **a figure may come in parts, one showing the real thing and one depicting its function, and anything that actually makes it understandable is allowed.** Fig 1.1 is redrawn this way (the machine with its two rules, then the run step by step, tally marks instead of binary): see UNDER.md §4ac. Also found: the book-wide `.diagram-label` text (rgba 255,255,255,0.3) fails 4.5:1 on every figure; fix it once in CSS during Gate 1.
