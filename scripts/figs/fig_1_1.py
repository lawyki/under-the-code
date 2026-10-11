# Fig 1.1 · A Turing machine (Pass 28, law 3; redrawn after the owner's read, 2026-10-12). The first figure
# in the book, so it assumes nothing: no binary (Chapter 2), no rule table. Three tally marks stand for 3;
# the head, in state "adding", follows two rules written as words (on a mark: move right; on a blank:
# write a mark and stop) and leaves four marks. Two parts, as the owner asked: the machine (animated) and its run, step by
# step (static rows that light in time with it), so the reduced-motion still is complete without showing the end first.
from figlib import Timeline, text, splice, MONO, GOLD, MUTED

W, H = 400, 580
CX = lambda i: 40 + i * 46 + 22               # cell centres
TY = 104                                       # tape top
MARKS = [1, 2, 3]                              # cells holding a mark at the start; the head starts on cell 1
NEW = 4                                        # the first blank, where the fourth mark goes
T = Timeline(10, shift=0.0)
INK = '#ece6da'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-2 svgd-part1-2">')
a('<title id="svgt-part1-2">Fig 1.1 · A Turing machine · adding one</title>')
a('<desc id="svgd-part1-2">A tape holds three tally marks, standing for 3. The head starts on the first mark in the state adding. '
  'Its two rules: on a mark, move one cell right; on a blank, write a mark and stop. It walks over the three marks, writes a '
  'fourth in the first blank and stops in the state done: 3 plus one is 4.</desc>')

def mark(cx, top, colour=INK, extra=''):
    return f'<line x1="{cx}" y1="{top + 11}" x2="{cx}" y2="{top + 37}" stroke="{colour}" stroke-width="3.5" stroke-linecap="round"{extra}/>'

# the tape
a(text(20, 34, 'THE MACHINE: TAPE, HEAD, RULES'))
a(f'<text x="18" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.45)">…</text>')
a(f'<text x="382" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.45)">…</text>')
for i in range(7):
    a(f'<rect x="{40 + i * 46}" y="{TY}" width="44" height="48" rx="3" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    if i in MARKS: a(mark(CX(i), TY))
# the fourth mark, written at tau 5.6 and kept until the loop resets
a(mark(CX(NEW), TY, GOLD, f' opacity="0">{T.anim("opacity", [(0.0, 0.0), (5.5, 0.0), (5.7, 1.0), (9.3, 1.0), (9.6, 0.0)])}</line'))

# the head: a box with its state over the cell it reads, stepping right one cell per rule
moves = [(0.0, 0), (1.4, 0), (1.9, 1), (2.8, 1), (3.3, 2), (4.2, 2), (4.7, 3), (9.4, 3), (9.8, 0)]
a(f'<g>{T.translate([(t, n * 46) for t, n in moves], axis="x")}')
a(f'<rect x="{CX(1) - 62}" y="48" width="124" height="36" rx="6" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
a(f'<text x="{CX(1)}" y="71" text-anchor="middle" {MONO} font-size="15" fill="{GOLD}">head · adding'
  f'{T.anim("opacity", [(0.0, 1.0), (5.9, 1.0), (6.0, 0.0), (9.5, 0.0), (9.7, 1.0)])}</text>')
a(f'<text x="{CX(1)}" y="71" text-anchor="middle" {MONO} font-size="15" fill="#fff">head · done'
  f'{T.anim("opacity", [(0.0, 0.0), (5.9, 0.0), (6.0, 1.0), (9.5, 1.0), (9.7, 0.0)])}</text>')
a(f'<polygon points="{CX(1) - 7},86 {CX(1) + 7},86 {CX(1)},96" fill="{GOLD}"/>')
a('</g>')

# the rules: all of them, as words; the one in use lights up
a(text(20, 184, 'ITS RULES, WHILE ADDING'))
RULES = [(True, 'if it reads a mark', 'move one cell right', [1.0, 2.4, 3.8]),
         (False, 'if it reads a blank', 'write a mark, then stop', [5.2])]
for r, (has_mark, cond, act, fires) in enumerate(RULES):
    y = 198 + r * 64
    a(f'<rect x="14" y="{y}" width="372" height="56" rx="6" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    pts = [(0.0, 0.0)]
    for f in fires: pts += [(f - 0.1, 0.0), (f, 1.0), (f + 0.9 if has_mark else 9.2, 1.0), (f + 1.1 if has_mark else 9.4, 0.0)]
    a(f'<rect x="14" y="{y}" width="372" height="56" rx="6" fill="rgba(212,168,83,0.16)" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", pts)}</rect>')
    a(f'<rect x="28" y="{y + 6}" width="34" height="44" rx="3" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    if has_mark: a(f'<line x1="45" y1="{y + 15}" x2="45" y2="{y + 41}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
    a(text(78, y + 23, cond, size=14, fill='rgba(255,255,255,0.68)'))
    a(text(78, y + 44, act, size=15, fill='#fff'))
# the run, step by step: the tape and head after each rule, lit in time with the machine above
a(text(20, 348, 'THE RUN, STEP BY STEP'))
ROWS = [([1, 2, 3], 1, 'mark: move right', 1.0, 1.9), ([1, 2, 3], 2, 'mark: move right', 2.4, 3.3),
        ([1, 2, 3], 3, 'mark: move right', 3.8, 4.7), ([1, 2, 3], 4, 'blank: write, stop', 5.2, 6.0),
        ([1, 2, 3, 4], 4, '4 marks: 3 + 1 = 4', 6.0, 9.4)]
for r, (marks, head, what, t0, t1) in enumerate(ROWS):
    y = 360 + r * 44
    a(f'<rect x="12" y="{y}" width="376" height="40" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", T.pulse(t0, t1, ramp=0.15))}</rect>')
    a(text(20, y + 26, str(r + 1), size=14, fill='rgba(255,255,255,0.6)'))
    for i in range(6):
        x = 40 + i * 30
        a(f'<rect x="{x}" y="{y + 8}" width="28" height="28" rx="2" fill="none" stroke="rgba(255,255,255,0.42)"/>')
        if i in marks:
            a(f'<line x1="{x + 14}" y1="{y + 13}" x2="{x + 14}" y2="{y + 31}" stroke="{GOLD if (i == NEW and r == 4) else INK}" stroke-width="3" stroke-linecap="round"/>')
    hx = 40 + head * 30 + 14
    a(f'<polygon points="{hx - 5},{y + 1} {hx + 5},{y + 1} {hx},{y + 7}" fill="{GOLD}"/>')
    a(text(232, y + 27, what, size=14, fill='#fff' if r == 4 else 'rgba(255,255,255,0.85)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Above, the machine: a tape of cells, a head that reads one cell at a time, and its two rules. Below, its run: on each mark '
           'the head moves right, and at the first blank it writes a mark and stops, so three marks become four.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tape.</b> An endless row of cells, one symbol in each; the head sees one cell at a time.</li>
          <li><b>Rule.</b> For the current state and the symbol under the head, a rule says what to write, where to move and which state comes next.</li>
          <li><b>This program.</b> The marks count like tallies, one mark for each unit: walking right to the first blank and writing a mark there adds one.</li>
          <li><b>Universal.</b> A machine whose rules read another machine's rules from its tape can run any of them: the universal machine of the text.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-1">
      <div class="diagram-label">Fig 1.1 · A Turing machine · adding one</div>
      {svg}
      <p id="ch1-context-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-1', 'ch1-context-p6', card)
