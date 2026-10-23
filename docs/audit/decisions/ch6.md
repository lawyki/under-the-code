# Chapter 6 · decisions

Round 1: `docs/audit/round1/ch6.json` (55 confirmed) and part-2.json items 4, 8, 10, 12, 19, 21, 22 (1-based). Numbers below are the 0-based indexes in ch6.json.

## Applied (own wording where the judge's wording did not fit)
- 0, 31 · ch6-complexity-p3 opens "C programs of the 1980s reached the same size and hit the same wall. For C, the diagnosis was…" (OS/360 and Multics were not C).
- 1 · "thirty structs" (the reader knows types as char, int, double).
- 2, 18 · Fig 6.1 strip, "The wall": private members glossed; "every ordinary touch" (classes-p6 says a pointer can still reach a private field).
- 3, part-2 10 · a paragraph under "Inheritance is layout" (new id ch6-classes-p7, the next unused): a Circle begins with everything a Shape has, here the vptr, so code compiled for a Shape finds it in the same place.
- 4 · Fig 6.4 caption: polymorphism is "code written for the general kind, Shape, not for any one shape's formula".
- 5 · Fig 6.3 strip: the constructor glossed where it is used.
- 6, 24 · ch6-classes-p6: no "cast"; a caller can reach a private field "through a pointer to the object's bytes, as any C function could reach into a struct".
- 7, 32 · Fig 6.5 caption: buf's 1024 bytes sit on the heap and the vector on the stack owns them; the strip keeps only "Why reverse".
- 8, part-2 4 · use-after-move: valid but in a state the standard does not fix (Fig 6.8's vector happens to be empty); the harm is code that keeps using it.
- 9 · vtable corruption: the freed chunk is refilled with attacker bytes, read as the vtable pointer by the next virtual call.
- 10 · ch6-modern-p7: "memory reached directly through pointers" (not the Bridge's DMA).
- 11, 28, 42, part-2 12 · Fig 6.9 caption: "less bookkeeping", "one call over the whole vector, with no iterators to name" (C++98 had std::accumulate); the strip names C++11 and C++20 without repeating their lists; the desc says "in one call". Fig 6.2's caption names the picture only.
- 12, 46 · Fig 6.1 caption ends after Brooks's arithmetic; p3 says "nothing but the source file grouped functions" (C's static and opaque structs are coarse walls).
- 13 · Simula 67 widened the simulation language into a general-purpose one (Dahl and Nygaard, HOPL 1978).
- 14 · Fig 6.6 "same job, different cost" (glibc's qsort is a merge sort; libstdc++'s std::sort is introsort).
- 15, 35 · Fig 6.6's "A trap in C" bullet cut (the overflow line was also wrong: it overflows when the values are far apart, not merely large).
- 16, 49 · Effective Modern C++ "as a companion to his Effective C++, for the features C++11 and C++14 added" (aristeia.com).
- 17, part-2 21 · "By the late 1980s C was the language of most new systems software, with C++ spreading behind it".
- 19, 20, 43 · Fig 6.4 "same vtable slot, different function"; the desc no longer speaks of a vptr the picture does not draw.
- 21, 44 · Fig 6.4 strip: the "= 0" now has its declaration (`virtual double area() = 0;` in Shape) and says what it means without "pure virtual".
- 22 · Fig 6.3 caption names the picture.
- 23 · ch6-classes-p3: "two instructions: load the vtable pointer, then jump through slot 0" (agrees with the figure).
- 25 · Fig 6.3 strip: "barely slower than a direct call" (branch prediction is taught in Part V).
- 26, part-2 8 · ch6-stroustrup-p5 states the deal once and points to Section 03.
- 27 · Fig 6.2 caption names the picture; "Early compilers" cut, its point moved into p3 ("so that it ran wherever a C compiler did").
- 29, 30, part-2 19 · Fig 6.1's "The source" bullet cut (one Brooks, in p2).
- 33, part-2 22 · Fig 6.6 caption names the two traced paths; "Why C cannot inline" cut; "Templates" without the three-times figure (p2 has it).
- 34 · ch6-zerocost-p2: the comparator is "by default, <" (the figure's std::sort line passes none; the drawn comment had no room for more).
- 36, 53 · Fig 6.7 caption names the three lifetimes; "Moving, not copying" replaced by "Making one" (make_unique, make_shared).
- 37 · Fig 6.8 caption: "Before and after std::move".
- 38 · ch6-modern-p4: "by copying three pointers".
- 39, 40 · glossary homes: Thompson → ch5-bell-labs, move semantics → ch6-modern.
- 41 · "keep each other's count above zero".
- 45 · Fig 6.2: the 1998 row dims until the sweep reaches it.
- 47 · Fig 6.7: the shared row's box is the object, with the count as a tag above it.
- 48 · h3 "Seven standards" before Fig 6.9.
- 50 · Fig 6.8's title quotes the prose exactly: "I am done with this; take it".
- 51 · Fig 6.8: v1's limit row is ink like begin and end; v2's is the copied green.
- 52 · Fig 6.4: the Triangle's highlight rects are outline only, like the others.
- 54 · Ch6 hero: "Hexagon", not "Polygon" (a Square is a polygon).

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch6-newcomer.json`, `ch6-expert.json`

The expert found nothing. Applied from the newcomer (one revision):
- Fig 6.6 caption says what the drawn counters show: in the same time std::sort finishes five comparisons to qsort's two.
- ch6-modern-p4 names the vector's three pointers (where it begins, where its elements end, the limit of the space reserved), so Fig 6.8's begin, end and limit read.

## Checks
- Gate 1 on Figs 6.1 to 6.9 and the hero: still with fullscreen 6/108 and motion with fullscreen 24/432 (Chromium), all on Figs 6.5, 6.6 and 6.9 and all pre-existing (they fail the same on the committed page): a right-hand comment crowding a line of code at 360 px, where Chromium's whole-pixel glyph advances leave under 3 px between them. Figs 6.5 and 6.9 set their comments 6 units further right (still inside the code box); Fig 6.6's "2 steps, written into the loop" reads "2 steps, inside the loop". Re-gated: 0/36 still and 0/144 motion (Chromium), 0/36 still and 0/72 motion (WebKit). WebKit's first run 0/108 and 0/216; hero 0/4.
- `build:glossary`: Thompson's home is Chapter 5's Bell Labs section (where he begins UNIX) and move semantics' home is Section 04, where the prose now teaches it; both pinned in `glossary-defs.json`. No entry added or lost. `build:sections` timestamp only (restored). `check:dashes` clean. Anchor ids outside SVGs unchanged except the new paragraph `ch6-classes-p7`.
- clip (part-2): 0 findings in 12 runs. pass25: see RESUME.md.
