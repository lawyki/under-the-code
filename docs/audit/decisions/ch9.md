# Chapter 9 · decisions

Round 1: `docs/audit/round1/ch9.json` (52 confirmed) and part-3.json items 1 and 5 (1-based). Numbers below are the 0-based indexes in ch9.json.

## Applied (own wording where the judge's wording did not fit)
- 0, 38 · Fig 9.3 caption: Baran's third shape "became the ARPANET's design, though survival was" not ARPA's purpose; the strip's "The question" (a repeat) cut.
- 1, 2, 37 · Fig 9.4 strip "Time to live": why the TTL exists (a packet caught in a routing loop dies), how traceroute uses it, and what the header checksum is and why each hop recomputes it.
- 3 · Fig 9.5 strip "Avoiding it": path MTU discovery in place of the bare "IPv6 forbids router-side fragmentation" in ch9-ip-p3 (cut there); the IPv6 rule stays in the strip.
- 4 · "your internet provider (ISP)".
- 5, 24 · the CGNAT caption glosses the port ("a label that tells conversations apart", pointing to Chapter 10, where ch10-udp-p1 now teaches it).
- 6 · Fig 9.8 strip "The shared range": why 100.64.0.0/10 exists and never leaves an ISP.
- 7, 9, 42, part-3 5 · Fig 9.10 strip "One way only": a forger never sees the reply, so spoofing suits single packets that need no answer (hiding the sender, aiming replies at a victim, as the SYN flood often does); a blind TCP conversation means guessing the replies, as Mitnick did.
- 8, 22 · ch9-security-p4: "BGP can also be misled, by malice or by mistake"; BGP hijacking is "announcing addresses you do not hold, whether on purpose or by error".
- 10, 23 · Fig 9.11 strip "No malice": two mistakes, Pakistan Telecom's announcement to PCCW and PCCW's passing it on unfiltered; the route-leak sentence says the routes were genuine but reached a neighbour that should never have heard them.
- 11, 35 · "about six thousand machines (by the usual rough estimate, a tenth of the internet of the time)"; the CFAA line, a fact the paragraph did not need, cut with it.
- 12, part-3 1 · rsh: "the trusted-host logins of rsh (remote login), which skipped the password for listed machines, helped along by guessable passwords". Morris is now "the Cornell graduate student of Chapter 3".
- 13 · "a student programmer in Leonard Kleinrock's lab".
- 14, 27 · ch9-arpanet-p3 split into sentences; the LO message is "the ARPANET's packet switching going live"; BBN's IMPs named as the first routers.
- 15, 47 · "hundreds of homes share one public address".
- 16 · "for nearly a hundred years".
- 17 · "nothing in IP itself verifies it"; the strip's "The source" bullet cut (the prose carries it).
- 18, 19, 20 · ch9-ip-p1: "every IP packet (inside the Ethernet frame of Chapter 8)", the fields "every router on the path reads", and the protocol field told apart as the receiver's.
- 21, 30, 46 · "a packet carrying 4000 bytes of data" in prose, caption, label and title; the caption names the three fragments and why losing one loses the packet.
- 25 · ch9-routing-p1 opens on what the internet is, without the "not one network" reveal.
- 26 · h2 "The first message, and the ideas behind it."
- 28 · Fig 9.1 caption names the picture (the call both ways, packets arriving 2, 1, 3).
- 29 · Fig 9.2 caption: four computers on 50 kbps lines, each joined by an IMP; the strip's "The message" cut, "The IMPs" says what they did.
- 31 · Fig 9.6 caption names the steps (1 to 3, the loop at step 4); strip "AS numbers" points out the private range.
- 32 · Fig 9.8 strip "The dates" cut (p1 gives them).
- 33 · Fig 9.9 strip "The price".
- 34 · Fig 9.10 caption: the same forged packet twice, with and without the BCP 38 check; the strip adds uRPF, how routers apply it.
- 36 · Fig 9.4 strip: "ToS once meant priority; today it marks a traffic class and congestion".
- 39 · "In October 1962, midway through that work, the Cuban Missile Crisis".
- 40 · "4,294,967,296 possible addresses, which sounded like a lot in 1981, though fewer are usable".
- 41 · "Nothing has to be reserved or set up before traffic flows."
- 43 · Fig 9.7 caption: a packet's climb, the peering crossing, and money flowing up both sides.
- 44 · Fig 9.9: the two 64-bit halves are drawn equal.
- 45 · Fig 9.6: each lit link is clipped like its thin link, so the highlight no longer runs through the boxes; the thin link hides while its highlight is lit (Gate 1 measured it against the highlight).
- 48 · Fig 9.9 label: 10<sup>38</sup> as a tspan in the figure font.
- 49 · Fig 9.4 strip: Flags are three bits; 010 sets don't fragment.
- 50 · Fig 9.1: the "silence: still reserved" label waits until the last voice dot has arrived, and the two late dots no longer wrap.
- 51 · Fig 9.7: the dashed arrows and their labels moved outward, clear of the boxes.

- Figs 9.8 and 9.12 (found by Gate 1): two captions had grown past 60 words; trimmed ("Many ISPs now put customers behind"; the route-leak caption ends "genuine routes reaching a neighbour that should never have heard them, with no attacker at all").

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch9-newcomer.json`, `ch9-expert.json`

The expert found nothing. Applied from the newcomer (one revision):
- Fig 9.10: at rest the grey line ran from the sender past the edge router to 192.0.2.10 under "dropped at the edge". The line below the router now shows only while a packet is let through (the no-filter run and the genuine one), so the resting frame stops at the router.
- Fig 9.8 strip: the 192.168 addresses are "the 192.168 addresses that each home router gives its own devices".
- Fig 9.5 strip: path MTU discovery works because the sender marks its packets "don't fragment" (the flag of Fig 9.4); the router's drop no longer contradicts the prose's split.
- ch9-v6-p1: IANA is "the body that hands out address blocks to the regional registries".
- Fig 9.8 caption: "not a socket on a switch" cut.

## Checks
- Gate 1 on Figs 9.1 to 9.12, first run: still with fullscreen 24/144 (Chromium; captions of Figs 9.8 and 9.12 over 60 words), motion with fullscreen 30/576 (Chromium; the same captions, and Fig 9.6's lit links measured at low contrast), WebKit 0/144 still and 0/288 motion. Fixed: the two captions trimmed; Fig 9.6 hides each thin link while its highlight is lit. Re-gated Figs 9.6, 9.8, 9.12: 0/36 and 0/144 (Chromium), 0/36 and 0/72 (WebKit); Fig 9.8 again after the NAT wording below, 0/12.
- `build:glossary`: "Flags" (newly marked in the Fig 9.3 strip) took the whole bullet as its definition; it now has a curated one in `glossary-defs.json`. The Fig 9.8 caption had lost the word NAT and with it the NAT entry; it reads "carrier-grade NAT (CGNAT), network address translation at ISP scale" again. "BGP hijacking" now has its home in Section 06 of this chapter, where the Pakistan Telecom story is told, ahead of Chapter 15. The Section 01 entries carry the new section title. `build:sections` carries the new h2. `check:dashes` clean. Anchor ids outside SVGs unchanged.
- clip (part-3): 0 findings in 12 runs. pass25: see RESUME.md.
