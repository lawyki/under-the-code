# Fig 1.1 · A Turing machine (Pass 28, law 3; redrawn after the owner's read, 2026-10-12). The first figure in the
# book, so it assumes nothing. Anchor, map, run: (1) what Turing modelled, a person computing by rules with pencil
# and paper (SEP "Turing Machines": he formalised human computation, a "computor" who sees a bounded number of
# squares and has finitely many states of mind); (2) the same job as a machine, each part named by its counterpart;
# (3) the run, step by step. Tally marks, not binary (Chapter 2): 3 marks become 4. t=0 is the start; every part is
# readable in the still.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 784
INK = '#ece6da'
T = Timeline(10, shift=0.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-2 svgd-part1-2">')
a('<title id="svgt-part1-2">Fig 1.1 · A Turing machine · a person\'s pencil work, as a machine</title>')
a('<desc id="svgd-part1-2">Top: a person looks at one square of a paper strip holding three tally marks, keeps "adding" in mind and '
  'follows a rulebook: on a mark, move right; on an empty cell, write a mark and stop. Middle: Turing\'s machine does the same job, '
  'with a tape for the paper, a head for the eye and pencil, showing its state, and the same two rules. Bottom: the run, step by '
  'step: the head passes the three marks, writes a fourth in the first empty cell and stops. 3 plus one is 4.</desc>')

def cell(x, y, w, h, marked=False, colour=INK):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="none" stroke="rgba(255,255,255,0.42)"/>'
    if marked: s += f'<line x1="{x + w / 2:g}" y1="{y + h * 0.22:g}" x2="{x + w / 2:g}" y2="{y + h * 0.78:g}" stroke="{colour}" stroke-width="3" stroke-linecap="round"/>'
    return s

# ---- 1 · what Turing modelled: a person computing by rules
a(text(20, 30, '1 · WHAT TURING MODELLED: A PERSON'))
a(f'<circle cx="46" cy="86" r="15" fill="none" stroke="{INK}" stroke-width="2"/>')                       # head
a(f'<path d="M 20 132 Q 46 100 72 132" fill="none" stroke="{INK}" stroke-width="2"/>')                   # shoulders
a(text(20, 60, 'in mind: adding', size=14, fill=GOLD))
for i in range(4): a(cell(86 + i * 30, 104, 28, 30, marked=i < 3))                                        # the paper
a(f'<line x1="60" y1="92" x2="98" y2="108" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="4 3"/>')  # eye on one square
a(f'<line x1="14" y1="140" x2="386" y2="140" stroke="rgba(255,255,255,0.35)"/>')                         # the desk
a(f'<rect x="214" y="46" width="174" height="80" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
a(text(226, 68, 'RULEBOOK', size=14, fill=BLUE))
a(text(226, 92, 'mark: move right', size=14, fill='rgba(255,255,255,0.88)'))
a(text(226, 114, 'empty: mark, stop', size=14, fill='rgba(255,255,255,0.88)'))
a(text(20, 166, 'paper · eye and pencil · rulebook', size=14, fill='rgba(255,255,255,0.68)'))

# ---- 2 · the same job as a machine
a(text(20, 214, '2 · THE SAME JOB AS A MACHINE'))
CX = lambda i: 40 + i * 46 + 22
TY = 284
for i in range(7): a(cell(40 + i * 46, TY, 44, 48, marked=i in (1, 2, 3)))
a(f'<text x="18" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.45)">…</text>')
a(f'<text x="382" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.45)">…</text>')
a(f'<line x1="{CX(4)}" y1="{TY + 11}" x2="{CX(4)}" y2="{TY + 37}" stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round" opacity="0">'
  f'{T.anim("opacity", [(0.0, 0.0), (5.5, 0.0), (5.7, 1.0), (9.3, 1.0), (9.6, 0.0)])}</line>')
moves = [(0.0, 0), (1.4, 0), (1.9, 1), (2.8, 1), (3.3, 2), (4.2, 2), (4.7, 3), (9.4, 3), (9.8, 0)]
a(f'<g>{T.translate([(t, n * 46) for t, n in moves], axis="x")}')
a(f'<rect x="{CX(1) - 90}" y="228" width="180" height="36" rx="6" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
a(f'<text x="{CX(1)}" y="251" text-anchor="middle" {MONO} font-size="15" fill="{GOLD}">head, state: adding'
  f'{T.anim("opacity", [(0.0, 1.0), (5.9, 1.0), (6.0, 0.0), (9.5, 0.0), (9.7, 1.0)])}</text>')
a(f'<text x="{CX(1)}" y="251" text-anchor="middle" {MONO} font-size="15" fill="#fff">head, state: done'
  f'{T.anim("opacity", [(0.0, 0.0), (5.9, 0.0), (6.0, 1.0), (9.5, 1.0), (9.7, 0.0)])}</text>')
a(f'<polygon points="{CX(1) - 7},266 {CX(1) + 7},266 {CX(1)},276" fill="{GOLD}"/>')
a('</g>')
a(text(20, 358, 'tape = the paper', size=14, fill='rgba(255,255,255,0.68)'))
a(text(206, 358, 'head = eye + pencil', size=14, fill='rgba(255,255,255,0.68)'))
a(text(20, 394, 'RULES = THE RULEBOOK', fill=BLUE))
RULES = [(True, 'if it reads a mark', 'move one cell right', [1.0, 2.4, 3.8]),
         (False, 'if it reads an empty cell', 'write a mark, then stop', [5.2])]
for r, (has_mark, cond, act, fires) in enumerate(RULES):
    y = 406 + r * 62
    a(f'<rect x="14" y="{y}" width="372" height="54" rx="6" fill="none" stroke="rgba(134,168,255,0.6)"/>')
    pts = [(0.0, 0.0)]
    for f in fires: pts += [(f - 0.1, 0.0), (f, 1.0), (f + 0.9 if has_mark else 9.2, 1.0), (f + 1.1 if has_mark else 9.4, 0.0)]
    a(f'<rect x="14" y="{y}" width="372" height="54" rx="6" fill="rgba(212,168,83,0.16)" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", pts)}</rect>')
    a(cell(28, y + 6, 32, 42, marked=has_mark))
    a(text(76, y + 22, cond, size=14, fill='rgba(255,255,255,0.68)'))
    a(text(76, y + 43, act, size=15, fill='#fff'))

# ---- 3 · the run, step by step (lit in time with the machine)
a(text(20, 570, '3 · THE RUN, STEP BY STEP'))
a(f'<polygon points="304,560 316,560 310,568" fill="{GOLD}"/>')
a(text(322, 570, '= head', size=14, fill='rgba(255,255,255,0.68)'))
ROWS = [([1, 2, 3], 1, 'mark: move right', 1.0, 1.9), ([1, 2, 3], 2, 'mark: move right', 2.4, 3.3),
        ([1, 2, 3], 3, 'mark: move right', 3.8, 4.7), ([1, 2, 3], 4, 'empty: write, stop', 5.2, 6.0),
        ([1, 2, 3, 4], 4, '4 marks: 3 + 1 = 4', 6.0, 9.4)]
for r, (marks, head, what, t0, t1) in enumerate(ROWS):
    y = 582 + r * 40
    a(f'<rect x="12" y="{y}" width="376" height="36" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", T.pulse(t0, t1, ramp=0.15))}</rect>')
    a(text(20, y + 24, str(r + 1), size=14, fill='rgba(255,255,255,0.6)'))
    for i in range(6): a(cell(40 + i * 30, y + 7, 28, 26, marked=i in marks, colour=GOLD if (i == 4 and r == 4) else INK))
    hx = 40 + head * 30 + 14
    a(f'<polygon points="{hx - 5},{y + 1} {hx + 5},{y + 1} {hx},{y + 6}" fill="{GOLD}"/>')
    a(text(232, y + 25, what, size=14, fill='#fff' if r == 4 else 'rgba(255,255,255,0.85)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Turing modelled a person working out a sum with pencil and paper by fixed rules, one square at a time, and kept only '
           'those parts: tape, head, rules. Run on three tally marks, the machine moves right past each and writes a fourth in the first blank, so 3 becomes 4.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Turing's model.</b> In 1936 Turing analysed what a person does when computing by rules: looks at a few squares, keeps a state of mind, writes, moves on. His machine is that person reduced to parts.</li>
          <li><b>Tape.</b> An endless row of cells, one symbol in each; the head sees one cell at a time.</li>
          <li><b>Rule.</b> For the current state and the symbol under the head, a rule says what to write, where to move and which state comes next.</li>
          <li><b>This program.</b> The marks count like tallies, one mark for each unit: walking right to the first blank and writing a mark there adds one.</li>
          <li><b>Universal.</b> A machine whose rules read another machine's rules from its tape can run any of them: the universal machine of the text.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-1">
      <div class="diagram-label">Fig 1.1 · A Turing machine · a person's pencil work, as a machine</div>
      {svg}
      <p id="ch1-context-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-1', 'ch1-context-p6', card)
