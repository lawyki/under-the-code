# PASS 27 BRIEF: the cut (law 2: every paragraph does a job)

Authored by the bridge, 2026-10-10, from the owner's instruction: "it's
extremely easy for an AI to write long paragraphs of nothing… there are some
things not inherently serving a purpose, but I am not going to point out
precisely where they sit." Order ratified the same day: dashes (Pass 26), then
this, then figures (Pass 28). **One part per session, I → V**, each followed
by a Sonnet 5.5 verification (BRIDGE §5). Model: Opus 5.5.

## What the earlier language pass did and didn't do

Passes 14–18 re-carried passages that *listed* where they should *run*. They
rewrote; they rarely cut, and "already at bar" was the frequent verdict. This
pass asks a different question of every paragraph and sentence: **what job
does this do for a reader who has read everything before it?** If the answer
is "none", it goes.

## What gets cut (or merged)

- **Restatement:** the same point made twice, in the same paragraph or a
  neighbour; a paragraph that re-says the figure caption or the previous
  section.
- **Announcement and scaffolding:** "it is important to note", "let's look
  at", "in this section we will", "as we saw", "the key insight is that"
  before the insight.
- **Summary of what was just said**, unless it is a chapter's earned coda
  (the "What you now understand" instrument and the Ch7 pickle coda register
  are the bar and stay).
- **Example inflation:** three examples where one carries the idea.
- **Hedge and filler:** "essentially", "fundamentally", "in many ways",
  "it turns out that", stacked adjectives, throat-clearing first sentences.
- **Paragraphs that exist to bridge** two paragraphs that already connect.

## What does not get cut

- Mechanism. The cause-to-effect chain that teaches is the book's reason to
  exist (pedagogy first, BRIDGE §4). A shorter paragraph that no longer
  teaches has failed.
- §4g fact-ledger corrections, the thesis set, the authorship line, owner
  epigraphs.
- The arc devices §4w found working (the six-pattern unification, the four
  disciplines, the part-identity micro-arcs, the codas). Cut around them, not
  through them.
- Voice and per-volume register.

No quota. A typical honest edit of AI-drafted prose lands 15–30 % shorter;
the number is a symptom, not a target. "Already does its job" remains a valid
verdict, recorded per section.

## Method (per part)

1. **Section editors** (one per section): mark every paragraph *earns /
   restates / announces / pads / merge-with-N* with the reason, then propose
   the cut text. Sentence-level trims inside kept paragraphs are allowed.
2. **Adversarial defence**: an independent reader argues for each cut
   paragraph from the student's side ("what would I lose?"). Cuts that lose
   mechanism are restored.
3. **Fact and voice gate**: facts, numbers, terms, cross-references, figure
   references and glossary first-use sites survive; the voice still reads as
   one author.
4. **Anchors**: a removed or merged paragraph's id migrates through
   `ANCHOR_ALIASES` in `book.js` to the paragraph that now holds its content,
   verified live at zero pixel delta (anchor-ID law). Reading positions are
   user data.
5. Regenerate glossary and sections; `npm run check:dashes`; the
   `tests/pass25` suites; ledger with words before/after per section.

## Carry-overs to fix in this pass

- Glossary definitions that quote the wrong sentence after Pass 26: livelock,
  split brain (and any the regenerate shows).
- The §4w findings that are about redundancy rather than structure.
