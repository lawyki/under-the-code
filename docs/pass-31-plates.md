# Pass 31 · plate rules

One set of rules per part, written from its exemplar (brief §8). They are rules, not shared drawing code: every figure is still drawn by hand from an empty script. The colours and faces are those in `scripts/figs/figlib.py`.

## Rules for every part

- **Plate.** `viewBox` 400 wide, 20-unit side margins, height as the idea needs (the exemplars run 404 to 482). Labels 14 units, results 15 to 16, nothing under 14. At 375 px that renders 12.6 px.
- **Shapes are outlined.** A region a label names (a well, a page, a card, a cell) is drawn with a stroke and no tinted fill: Gate 1 judges a named shape by its dominant paint, and a faint fill on a dark plate fails 3:1. A solid fill is kept for the one thing that is on (Fig 1.5's gate, Fig 4.8's picked row), with dark lettering on it.
- **Text roles.** Glyphs inside a drawn object (a value, a node letter, a segment name), at most six characters, go in an `obj()` group as object text. Everything else is a label, at most 8 per panel. Split a figure into `data-panel` groups only where it really has parts.
- **Motion.** t=0 is the finished story, with the result on the plate. Motion is the mechanism, in the part's own verbs below. A layer that changes is a held group (off from the reset, on from its beat), so every still frame is complete.
- **Words.** Only terms the prose has taught before the figure; expert names stay out (Fig 4.8's L4 to L1 became 1st to 4th). One result line, stated plainly.

## Part I · the original grammar (exemplar: Fig 1.5; references: Fig 1.1 v4, Fig 1.2 Enigma)

- **Plate and type.** Card #111, DM Mono. Gold #d4a853 is the thing that acts or is on; blue #86a8ff is charge or data moving; red #ec8d8d is what blocks (p-type silicon, a refused path); green #9bd89b is what holds; ink #ece6da; muted white at 0.6.
- **Motion verbs.** *Step*: a discrete move along a track (the head, the program counter). *Light*: a lamp or a rule card lights when it fires. *Flow*: charge or data moving along a wire.
- **Recurring things.** The lamp of Figs 1.4 and 1.5 (gold with rays when lit). The voltage pill (0 V in grey outline, a positive voltage in gold). Electrons as filled blue dots, holes as red rings. Memory as a row of outlined cells with their numbers. The gold frame for whatever is active.

## Part II · Greenbar (exemplar: Fig 4.8)

- **Plate and type.** Plate #0c120e, IBM Plex Mono. Phosphor #84ffb2 for the program's own things, blue for data and offsets, soft phosphor for pointers.
- **Motion verbs.** *Print*: a row of a listing prints in solid phosphor. *Step*: the walk moves one level, one index at a time. *Wait*: the blocked side holds, its row unlit.
- **Recurring things.** The listing page: an outlined box of 18-unit rows, the picked row printed solid with dark text. Registers as outlined boxes with their name. A process as a panel with a `$` label. The kernel boundary as a dashed line.

## Part III · Chart Room (exemplar: Fig 10.3)

- **Plate and type.** Plate #0d2740, Space Mono. Signal cyan #4fc4e6 for opening and data, route orange #e07a3f for closing and routes, soft and muted parchment-white for structure.
- **Motion verbs.** *Flow*: a segment or packet travels its route like a line drawn on a chart. *Arrive*: a state lights where the segment lands. *Drift*: ambient dashes along a route, never carrying meaning.
- **Recurring things.** Each endpoint as a vertical lane; segments as diagonal arrows named in six characters or fewer; states as outlined pills beside their lane; packets as small outlined boxes.

## Part IV · Strongroom (exemplar: Fig 13.5, the merge reference)

- **Plate and type.** Dossier plate #171008, Courier Prime. Parchment #e6d9bd for records, seal #cf8d78 for warnings in text, stamp red #b8372f for strokes only (too dark for text on the plate), brass #c9a25a for reversal, sage #a9bf8e for what is kept.
- **Motion verbs.** *Stamp*: a record or verdict lands whole and stays. *Strike*: an old value is struck through and the new one written beside it. *Seal*: a commit closes a record.
- **Recurring things.** Account and data cards (name top left in muted, value bottom right). Log records as outlined lines. Verdicts as boxed stamped words.
- **Two-part cards.** The problem on top, the mechanism below, divided by a dotted rule. The lower panel continues the upper panel's own example, so the two read as one story. A merge keeps the lower figure's number and id, and the higher one's ids are aliased in `book.js` (brief §12).

## Part V · Quorum (exemplar: Fig 17.6)

- **Plate and type.** Void plate #14111f, JetBrains Mono. Violet #a08cff for nodes, teal #4fd8c2 for votes and what works, rose #f08aa8 for failure, amber #f2c46d for the result line.
- **Motion verbs.** *Pulse in step*: waiting or agreement shown in phase everywhere it appears. *Travel*: a message creeps along a link. *Converge*: several nodes settle on one value together.
- **Recurring things.** Nodes as lettered circles (radius 15); a crashed node as a dashed circle with a rose ×; a silent link dashed; outcomes as outlined cells with a tick or a cross.
