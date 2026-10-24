# Fig 17.6 · FLP impossibility (Pass 31 exemplar for Part V, from an empty script). Takeaway: a slow node and a crashed
# one look identical, so no protocol can both always decide and never disagree.
# Concept chosen of three (ledger): what A sees on top (no vote from C yet); below, the two worlds it cannot tell
# apart, C slow and C crashed; then a two-by-two grid, decide now or keep waiting in each world, with one failure in
# each row. Quorum's phase-synced motion: A waits in step in the view and in both worlds, while C's vote creeps toward
# A in the slow world only. t=0 is the whole argument, every cell shown.
import figlib
from figlib import Timeline, text, obj, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER
figlib.FONT = JETBRAINS

W, H = 400, 446
GX = [118, 264]                      # grid columns (left edges), width 128
CW = 128
D = 8.0
T = Timeline(D, shift=0.0)
T.beat(0.0, 'A waits; C is silent in both worlds')
T.beat(5.6, "in the slow world, C's vote arrives")

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-19 svgd-part5-19"{T.beats_attr()}>')
a('<title id="svgt-part5-19">Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure</title>')
a('<desc id="svgd-part5-19">Top: what node A sees, its link to node C with no vote from C yet. Below, the two worlds A cannot '
  'tell apart: in one C is slow and its vote is still on its way, in the other C has crashed and no vote will ever come. Then '
  'a grid of A\'s two choices in each world. Decide now: in the slow world C\'s vote arrives later and disagrees, a failure; in '
  'the crashed world it is fine. Keep waiting: in the slow world the vote arrives and all is fine; in the crashed world A waits '
  'for ever, a failure. Each choice fails in one world, so no deterministic protocol can be sure both to decide and never to disagree.</desc>')

def node(x, y, n, col, dead=False):
    dash = ' stroke-dasharray="3 3"' if dead else ''
    parts = [f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{col}" stroke-width="2"{dash}/>',
             text(x, y + 5, n, anchor='middle', size=15, fill=col, ls='0')]
    if dead:
        parts.append(f'<path d="M {x + 10} {y - 23} l 11 11 M {x + 21} {y - 23} l -11 11" stroke="{QROSE}" stroke-width="2.4"/>')
    return obj(*parts)

def waiting(x, y):
    """A's waiting ring, pulsing in phase everywhere it is drawn."""
    return (f'<circle cx="{x}" cy="{y}" r="21" fill="none" stroke="{VIOLET}" stroke-width="1.5" opacity="0">'
            f'{T.anim("opacity", [(0.0, 0.9), (1.0, 0.1), (2.0, 0.9), (3.0, 0.1), (4.0, 0.9), (5.0, 0.1), (6.0, 0.9), (7.0, 0.1), (8.0, 0.9)])}</circle>')

# what A sees
a('<g data-panel="view">')
a(text(20, 22, 'what A sees', size=14, fill=QMUTED, role='label'))
a(node(84, 58, 'A', VIOLET)); a(waiting(84, 58))
a(node(316, 58, 'C', QSOFT))
a(f'<line x1="100" y1="58" x2="300" y2="58" stroke="{QSOFT}" stroke-width="1.5" stroke-dasharray="4 5"/>')
a(text(200, 49, 'no vote yet', anchor='middle', size=14, fill=QSOFT, role='label'))
a('</g>')

# the two worlds
a('<g data-panel="worlds">')
for i, (name, dead) in enumerate((('C is slow', False), ('C crashed', True))):
    x0 = GX[i]
    a(obj(f'<rect x="{x0}" y="98" width="{CW}" height="76" rx="10" fill="none" stroke="{QSOFT}" stroke-width="1.3"/>'))
    a(text(x0 + CW / 2, 117, name, anchor='middle', size=14, fill=QMUTED, role='label'))
    a(node(x0 + 26, 150, 'A', VIOLET)); a(waiting(x0 + 26, 150))
    a(node(x0 + CW - 26, 150, 'C', QSOFT, dead))
    if not dead:  # the vote, on its way, slowly
        a(f'<circle cy="150" r="5" fill="{TEAL}">{T.anim("cx", [(0.0, x0 + CW - 44), (5.6, x0 + 44), (5.7, x0 + CW - 44), (8.0, x0 + CW - 44)])}'
          f'{T.anim("opacity", [(0.0, 1.0), (5.6, 1.0), (5.61, 0.0), (7.7, 0.0), (7.8, 1.0)])}</circle>')
a('</g>')

# A's two choices in each world
a('<g data-panel="choices">')
rows = [('decide', [('disagree', QROSE, False), ('fine', TEAL, True)]),
        ('wait', [('fine', TEAL, True), ('forever', QROSE, False)])]
for r, (choice, cells) in enumerate(rows):
    y = 196 + r * 94
    a(text(20, y + 46, choice, size=15, fill=QSOFT, role='label'))
    for i, (word, col, ok) in enumerate(cells):
        x0 = GX[i]
        mark = (f'<path d="M {x0 + CW / 2 - 9} {y + 30} l 6 7 l 13 -15" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' if ok else
                f'<path d="M {x0 + CW / 2 - 8} {y + 20} l 16 16 M {x0 + CW / 2 + 8} {y + 20} l -16 16" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')
        a(obj(f'<rect x="{x0}" y="{y}" width="{CW}" height="78" rx="10" fill="none" stroke="{col}" stroke-width="{2.2 if not ok else 1.4}"/>',
              mark, text(x0 + CW / 2, y + 62, word, anchor='middle', size=14, fill=col, ls='0',
                         role='label' if len(word) > 6 else None)))
a(text(200, H - 14, 'each choice fails in one world', anchor='middle', size=15, fill=QAMBER, role='label'))
a('</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('From A\'s side a slow C and a crashed C look the same (top). Deciding now fails if C was only slow and its vote '
           'disagrees, waiting fails for ever if C crashed, so no deterministic protocol keeps safety and liveness in both, and real systems '
           'use timeouts that start a new election, never a decision.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The silence.</b> A needs C's vote. With no bound on how long a message may take, A sees the same silence whether C is slow or has crashed.</li>
          <li><b>Decide now.</b> If C was only slow, its vote arrives afterwards and may disagree: safety lost.</li>
          <li><b>Keep waiting.</b> If C crashed, no vote ever comes: liveness lost.</li>
          <li><b>The theorem.</b> Fischer, Lynch and Paterson (1985) proved that no deterministic protocol escapes both in a fully asynchronous system with even one crash.</li>
          <li><b>In practice.</b> Raft assumes delays end and uses timeouts. It never decides wrongly, but during a long network storm it can stall, holding election after election until messages arrive in time again.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-6">
      <div class="diagram-label">Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure</div>
      {svg}
      <p id="ch17-consensus-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-5', 'fig-17-6', 'ch17-consensus-p9', card)
