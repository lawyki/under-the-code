# Chapter 8 · decisions

Round 1: `docs/audit/round1/ch8.json` (64 confirmed) and part-3.json items 8, 15, 16, 17, 18, 19, 26 (1-based). Numbers below are the 0-based indexes in ch8.json.

## Applied (own wording where the judge's wording did not fit)
- 0, 60 · Fig 8.1 caption parses: "the same thing, twelve orders of magnitude (powers of ten) apart".
- 1, 28 · ch8-substrates-p2 names the twisted pair where the difference signal is introduced; "the trick behind the twist" gone.
- 2, 35, 4 · ch8-shannon-p8: bandwidth in hertz is "the width of the band of frequencies it passes, not its bit rate"; SNR is "a plain ratio: 30 dB is 1,000"; the Fig 8.4 caption says the same at its 30 dB.
- 3, 36 · ch8-shannon-p12: why powers become square roots (a voltage grows as the square root of the power it carries).
- 5, 37 · ch8-shannon-p10: what a coding scheme is here (redundant bits the receiver uses to repair damage), and "no matter how clever the coding".
- 6, 7, 32, 33, 34 · ch8-shannon-p6: why −log₂ p counts questions; one biased example, the figure's 90/10 (0.47 bits), with how grouping beats one bit per flip; the aphorism closer replaced. The Fig 8.3 caption names the picture.
- 62 · Fig 8.3's symmetry is "about the fair coin" (in the new caption).
- 8 · ch8-encoding-p2: one miscounted flat stretch puts every later bit one place out (not "the entire stream").
- 9, 46 · ch8-ethernet-p4: what a frame is, and that its header names sender and receiver by MAC address (below).
- 10, 47 · Fig 8.8 caption: "send a short jamming signal"; a slot is "the time a signal needs to cross the whole cable and back".
- 11, 12, 51 · ch8-ethernet-p11: the source MAC is whatever software writes; a full table can no longer keep the real entries; "flood the frame out of every port" (Fig 8.10's word).
- 13, 56 · ch8-layers-p6 without "that graph" (its antecedent was cut earlier) and without the hyphenated -ly adverb.
- 14, 26, 57 · Fig 8.2: the router-to-provider hop reads "phone line, a few km" again (§4g Fig 8.2 row: Ethernet's 100 m cannot reach the provider; Gate 2 had brought the old label back while removing "DSL"); desc "a telephone or cable-TV line, a few kilometres".
- 15, 27, part-3 26 · ch8-bridge-p3: "a signal" (fibre carries light), one question instead of three, "the rest of Part III".
- 16 · ch8-ethernet-p3: the 22 May 1973 memo with hand-drawn diagrams (CHM); no yellow paper or museum claim; it no longer says every LAN since shares one cable.
- 17 · Metcalfe "spent weeks there modelling the system" (historyofcomputercommunications.info 8.7), not "on the plane home".
- 18 · WPA3: "the flaws found in it in 2019 were patched" (Dragonblood).
- 19 · Raspberry Pi: older boards B8:27:EB, newer DC:A6:32 and others.
- 20 · Fig 8.10 strip: full duplex is "both ends able to send at the same time" (Gigabit uses all four pairs both ways).
- 21, 29, part-3 15 · bands: Wi-Fi 2.4, 5 and 6 GHz; cellular from below 1 GHz to tens of GHz (as Fig 8.2 and §4g).
- 22, 23, 31 · TEMPEST is "the US codename for standards"; Van Eck rebuilt "the picture on an unshielded monitor".
- 24 · ch8-shannon-p1: "close to a metaphor (Hartley had only counted equally likely messages, in 1928)" (Hartley, BSTJ 1928), which also explains the callout's Shannon–Hartley (38).
- 25 · Data link "moves frames between machines on the same local network, over cable, switch or radio link".
- 30 · fibre repeaters "tens of kilometres apart (50 to 100 km on an undersea cable)", one spacing for the chapter.
- 39 · NRZ "changes only when a bit differs from the one before it".
- 40 · Fig 8.5 caption names the picture; Fig 8.6 caption drops the repeated cost.
- 41 · "reads five zeros … reads all seven bits correctly".
- 42, 43 · Fig 8.7 caption names the picture and reconciles Wi-Fi 6's 10 bits with Fig 8.4's 6.7 (only on a far cleaner signal); "The carrier" cut.
- 44 · Fig 8.7 QAM bullet with parentheses.
- 45 · "In ever faster versions, Ethernet became…" (not the CSMA/CD rule).
- 48 · MAC spelled out ("Media Access Control; no relation to Apple's Mac").
- 49, part-3 18 · Fig 8.9 caption names the picture; "The halves" cut.
- 50 · ARP cache: "a while (seconds to minutes, depending on the system)", as the strip.
- 52 · ch8-layers-p1: encapsulation stated in the prose, not left to the figure.
- 53, 63, part-3 19 · Fig 8.11 caption without the TCP/IP collapse; Fig 8.12 caption reads across the picture; "HTTP as an example" cut.
- 54 · Fig 8.11 caption glosses TLS (Chapter 11) and the request.
- 55 · "OSI: Open Systems Interconnection"; "Data link" as in the figures.
- 58 · Fig 8.8: A's second frame now sweeps off the cable (tail from A to B) before B sends, as carrier sense requires.
- 59 · Fig 8.8: "line busy: B waits" appears only when A's signal reaches B.
- 61 · "3.43 kHz" in the Fig 8.4 caption and desc, so 33.6 ÷ 3.43 = 9.8 as drawn.
- part-3 8 · ch8-bridge-p1: "Parts I and II stayed inside one machine. Part III leaves it."
- part-3 16 · ch8-encoding-p3 points to Section 05 instead of introducing 10BASE5 early.
- part-3 17 · Fig 8.8 strip "Today" keeps only Wi-Fi's backoff (switches ending collisions is said in p4 and Fig 8.10).

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch8-newcomer.json`, `ch8-expert.json`

The expert found nothing. Applied from the newcomer (one revision):
- Fig 8.2 caption: "the programs above see none of it" (layers come only in Section 06).
- Fig 8.6: the two digit rows are labelled "read", as in Fig 8.5.
- Fig 8.11 caption: "most add their own wrapping" (Session adds nothing and the figure says so).

Fixed after Gate 1:
- Figs 8.1, 8.4 and 8.8: three captions had grown past 60 words with the glosses added above; trimmed back ("at scales a trillion times apart"; Fig 8.4 "Shannon's limit, the curve" with the signal-to-noise gloss kept; Fig 8.8's slot gloss shortened). The generators carry the page's captions.

## Checks
- `build:glossary`: two side effects of the new glosses fixed in the text, so no entry moved or appeared: "the encryption behind HTTPS" in the Fig 8.11 caption sent HTTPS's entry to Chapter 8 (now "the encryption of Chapter 11"), and "(OSI: Open Systems Interconnection)" in ch8-layers-p2 made a junk "OSI seven-layer model" entry (now "named for Open Systems Interconnection").
- `build:sections` (timestamp only, restored), `check:dashes` clean. Anchor ids outside SVGs unchanged.
- Gate 1 on Figs 8.1 to 8.12: still with fullscreen 36/144 (Chromium; all three captions over 60 words) before the trims, then 0/36 on Figs 8.1, 8.4, 8.8 (and 0/36 WebKit); 0/144 (WebKit). Motion with fullscreen 144/576 (Chromium; the same captions), then 0/144; motion 0/288 (WebKit).
- clip (part-3): 0 findings in 12 runs. pass25: see RESUME.md.
