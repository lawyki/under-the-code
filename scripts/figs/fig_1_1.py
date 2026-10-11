# Fig 1.1 · A Turing machine (Pass 28, law 3; redrawn after the owner's read, 2026-10-12). One scene, one idea,
# read at a glance: a head walks a tape of three tally marks and does what the matching rule card says, so three
# marks become four. No binary (Chapter 2), no rule table, no states drawn (the prose names them), five labels.
# The owner rejected both a jargon version and an overloaded three-part one; Turing's model of a person computing
# by rules lives in the How it works strip. t=0 is the start; the result is stated beside it, so the still is complete.
from figlib import Timeline, text, splice, MONO, GOLD

W, H = 400, 300
INK = '#ece6da'
CX = lambda i: 52 + i * 50 + 23            # cell centres, cells 0..5
TY = 74                                    # tape top
T = Timeline(9, shift=0.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-2 svgd-part1-2">')
a('<title id="svgt-part1-2">Fig 1.1 · A Turing machine · three marks become four</title>')
a('<desc id="svgd-part1-2">A tape holds three tally marks. A head reads one cell at a time and follows two rules: on a mark, move '
  'one cell right; on an empty cell, write a mark and stop. It walks past the three marks, writes a fourth in the first empty '
  'cell and stops: 3 plus one is 4.</desc>')

def tally(cx, top, h, colour=INK, extra=''):
    return f'<line x1="{cx}" y1="{top + h * 0.22:g}" x2="{cx}" y2="{top + h * 0.78:g}" stroke="{colour}" stroke-width="3.5" stroke-linecap="round"{extra}/>'

# the tape
for i in range(6):
    a(f'<rect x="{52 + i * 50}" y="{TY}" width="46" height="52" rx="3" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    if i in (0, 1, 2): a(tally(CX(i), TY, 52))
a(tally(CX(3), TY, 52, GOLD, f' opacity="0">{T.anim("opacity", [(0.0, 0.0), (5.0, 0.0), (5.2, 1.0), (8.4, 1.0), (8.7, 0.0)])}</line'))

# the head: a gold frame round the cell it reads, with its name above, stepping right one cell per rule
moves = [(0.0, 0), (1.2, 0), (1.6, 1), (2.4, 1), (2.8, 2), (3.6, 2), (4.0, 3), (8.5, 3), (8.9, 0)]
a(f'<g>{T.translate([(t, n * 50) for t, n in moves], axis="x")}')
a(f'<rect x="{CX(0) - 27}" y="{TY - 4}" width="54" height="60" rx="5" fill="none" stroke="{GOLD}" stroke-width="2.5"/>')
a(text(CX(0), TY - 16, 'head', anchor='middle', size=15, fill=GOLD))
a('</g>')

# the two rules, as picture cards; the one in use lights up
def card(x, label, mark_in, fires):
    y = 166
    a(f'<rect x="{x}" y="{y}" width="190" height="66" rx="6" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    pts = [(0.0, 0.0)]
    for f in fires: pts += [(f - 0.1, 0.0), (f, 1.0), (f + 0.8 if mark_in else 8.3, 1.0), (f + 1.0 if mark_in else 8.5, 0.0)]
    a(f'<rect x="{x}" y="{y}" width="190" height="66" rx="6" fill="rgba(212,168,83,0.16)" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", pts)}</rect>')
    a(f'<rect x="{x + 16}" y="{y + 11}" width="34" height="44" rx="3" fill="none" stroke="rgba(255,255,255,0.42)"/>')
    if mark_in: a(tally(x + 33, y + 11, 44))
    a(f'<path d="M {x + 56} {y + 33} H {x + 72} M {x + 66} {y + 27} L {x + 72} {y + 33} L {x + 66} {y + 39}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    a(text(x + 78, y + 39, label, size=15, fill='#fff'))
card(8, 'move right', True, [0.8, 2.0, 3.2])
card(202, 'write, stop', False, [4.4])

# the result, stated from the first frame
a(text(200, 280, '3 + 1 = 4', anchor='middle', size=18, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('The head reads one cell at a time and does what the matching rule says: on a mark it moves right, on an empty cell '
           'it writes a mark and stops. Following just these two rules, it has added one.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Turing's model.</b> In 1936 Turing analysed what a person does when computing by rules with pencil and paper: looks at a few squares, keeps a state of mind, writes, moves on. His machine is that person reduced to parts: tape for the paper, head for the eye and pencil, rules for the rulebook.</li>
          <li><b>Tape.</b> An endless row of cells, one symbol in each; the head sees one cell at a time.</li>
          <li><b>Rule.</b> For the current state and the symbol under the head, a rule says what to write, where to move and which state comes next.</li>
          <li><b>This program.</b> The marks count like tallies, one mark for each unit: walking right to the first empty cell and writing a mark there adds one.</li>
          <li><b>Universal.</b> A machine whose rules read another machine's rules from its tape can run any of them: the universal machine of the text.</li>
        </ol>
      </details>'''
card_html = f'''<div class="diagram-card fig-v2" id="fig-1-1">
      <div class="diagram-label">Fig 1.1 · A Turing machine · three marks become four</div>
      {svg}
      <p id="ch1-context-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-1', 'ch1-context-p6', card_html)
