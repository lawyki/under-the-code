# Chapter 7 · decisions

Round 1: `docs/audit/round1/ch7.json` (55, all confirmed) and part-2.json items 3 and 18 (1-based). Numbers below are the 0-based indexes in ch7.json. No kept originals or owner text in this chapter; the Zen-of-Python line cut under 39 is the book's quotation, not an owner epigraph.

## Applied (own wording where the judge's wording did not fit)
### 01 · Interpreters
- 16, 24, 44 · Russell's 1959 program was "a working interpreter", not the first ever; "read each Lisp expression at runtime and executed it directly".
- 17 · "an IBM 704 at MIT around the turn of 1959".
- 0 · imported modules glossed (code files a program loads with `import`).
- 15, 25 · "dozens to hundreds of CPU instructions".
- 9 · the specialised instruction explained at first use ("swaps a faster, specialised instruction in for one that keeps meeting the same types").
- 49 · Fig 7.1: the Python row shows "first run, then cached" in order; the cache line no longer lights before the first run has compiled.

### 02 · Van Rossum
- 38 · the opening says who van Rossum was and where he worked before the hobby project.
- 26, 46 · "four years on ABC, a language CWI built for teaching" (van Rossum, "Personal History, part 1", 2009).
- 22, 27 · "many of the world's introductory programming courses".
- 28, 45, 52, part-2 18 · "Usenet" in the prose, the glossary definition and Chapter 4.
- 39 · ch7-vanrossum-p2 ends on `self`; the Zen-of-Python clause cut (the paragraph's job is done).
- 2, 3 · Fig 7.2 strip "What 3.0 fixed": Unicode glossed (characters from any alphabet, where Python 2 text was plain bytes), `1/2` was 0, `print "x"` became `print("x")`.
- 37, 51 · Fig 7.2 caption opens on the split; the restating first sentence cut.
- 1 · Fig 7.2's "no GIL" points to Section 04.
- 48 · "Van Rossum (1996)" capitalised at the start of a sentence.

### 03 · Types
- 13, 30 · "(Python, Ruby, Lisp)": JavaScript coerces rather than failing with a type error.
- 40 · the "static is safer; dynamic is faster" closer cut; p3 opens on duck typing.
- 12, 29 · "(a file, an HTTP response, a stand-in for testing)".
- 4 · Fig 7.3 strip: type hints glossed (optional labels Python ignores at run time and a checker such as mypy reads).

### 04 · The GIL
- 43 · h2: "One Python thread runs at a time, for reasons that are running out."
- 5 · "a thread waiting on the network, or calling a C library that works on its own data, can let go of the lock".
- 20, 32 · "how many references point to it (names, list slots, attributes)".
- part-2 3 · why earlier attempts failed (every reference-count update made atomic or locked, slowing single-threaded code).
- 6, 35 · asyncio said once, in a new paragraph `ch7-gil-p5` after Fig 7.4 (the next unused number): a waiting thread needs no core, and asyncio shares one thread among many tasks where a thread apiece would cost too much.
- 7, 42 · Fig 7.4 strip: "Why one lock" cut; "Removing it" names biased reference counting and per-object locks plainly.
- 19, 31 · "about 40% slower in it, in 3.14 about 5–10%".
- 18 · Fig 7.4: thread 1's I/O ends at 25 ms and it waits for the lock; thread 2 hands it over at 30 ms, when its interval runs out.

### 05 · CPython
- 23 · `ceval.c` described by what it does (a case for every bytecode instruction), not by a line count.
- 10 · Fig 7.6 "The loop": jumps straight from each instruction to its C handler.
- 33, 50 · "prints this bytecode, between a RESUME and a RETURN_VALUE".
- 47 · "at runtime" throughout the chapter.
- 8 · Fig 7.7 step 5: "read the values out of both".
- 36 · Fig 7.7 "Since 3.11": the specialised instruction of Fig 7.6 skips the lookup, though not the boxes.

### 06 · Data science
- 11 · the billion multiply-adds explained (each of the million cells is 1000 products added up); matrices glossed.
- 14, 41 · Stroustrup and van Rossum's trade stated as costs: no more at runtime than hand-written code, against "let the machine do a hundred times the work to save a programmer five minutes".
- 21, 34 · "Several web frameworks that accepted pickled session cookies have been bitten by this".

### Hero
- 53 · both code lines left-aligned at x = 189, the loop body indented.
- 54 · "10 to 100 times slower than C" in place of "slow but predictable", as the lead says.

## Rejected
- None.

## Blind retest (Sonnet 5.5): `docs/audit/retest/ch7-newcomer.json`, `ch7-expert.json`

The expert found nothing. Applied from the newcomer (one revision), both in the pickle strip (ch7-datasci-p7):
- what `pickle.loads` does (rebuilds a Python object from the bytes `pickle` saved it as) and what `os.system()` does (runs a command on the computer);
- PyPI glossed (the public index Python libraries are installed from), and why a look-alike name is an attack (installing runs the package's own setup code).

## Checks
- Gate 1 on Figs 7.1 to 7.4, 7.6, 7.7 and the hero: still with fullscreen 0/72 (Chromium) and 0/72 (WebKit); motion with fullscreen 0/288 (Chromium); motion 0/144 (WebKit); hero 0/4.
- `build:glossary`: no entry added or lost; the GIL entry carries the new Section 04 title and van Rossum's definition reads "Usenet". `build:sections` carries the new h2. `check:dashes` clean. Anchor ids outside SVGs unchanged except the new paragraph `ch7-gil-p5`.
- clip (part-2): 0 findings in 12 runs. pass25: see RESUME.md.
