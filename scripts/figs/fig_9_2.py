# Fig 9.2 · The first internet (Pass 28, law 3). Chart Room. The four-node ARPANET of December 1969 on
# an abstract map; the first message replayed: L and O travel UCLA -> SRI, then G, and SRI's system
# crashes. Below, the milestones, lit in turn. t=0 (shift): LO delivered, the crash marked.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 420
NODES = {'SRI': (92, 64), 'UCSB': (70, 150), 'UCLA': (150, 200), 'Utah': (316, 96)}
LINKS = [('UCLA', 'SRI'), ('UCLA', 'UCSB'), ('UCSB', 'SRI'), ('SRI', 'Utah')]
D = 12.0
LETTERS = [('L', 0.6), ('O', 1.9), ('G', 3.2)]
FLIGHT = 1.0
CRASH = 3.2 + FLIGHT
MS = [('1969', '4 nodes'), ('1971', '15 nodes'), ('1973', 'across the Atlantic'), ('1974', 'Cerf and Kahn: TCP'),
      ('1981', '213 hosts'), ('1983', 'switch to TCP/IP'), ('1990', 'ARPANET retired')]
MS0 = CRASH + 1.0
T = Timeline(D, shift=CRASH + 0.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0, t1=D):
    return T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-16 svgd-part3-16">')
a('<title id="svgt-part3-16">Fig 9.2 · The first internet</title>')
a('<desc id="svgd-part3-16">The ARPANET in December 1969: four computers, at UCLA, UCSB, SRI in Menlo Park and the University of Utah, joined by leased lines. '
  'The first message went from UCLA to SRI on 29 October 1969: the letters L and O arrived, and on G the receiving system crashed. '
  'Below, how it grew: 15 nodes in 1971, across the Atlantic in 1973, Cerf and Kahn\'s TCP paper in 1974, 213 hosts in 1981, the switch to TCP/IP in 1983, and the ARPANET retired in 1990.</desc>')
a(text(20, 24, 'DECEMBER 1969', size=13, fill=CMUTED))
for u, v in LINKS:
    (x1, y1), (x2, y2) = NODES[u], NODES[v]
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="2"/>')
for nm, (x, y) in NODES.items():
    a(f'<circle cx="{x}" cy="{y}" r="10" fill="{CDEEP}" stroke="{CYAN}" stroke-width="2"/>')
    dx, anchor = (16, 'start') if nm != 'UCSB' else (-16, 'end')
    if nm == 'UCSB': dx, anchor = (16, 'start')
    a(text(x + dx, y + 5, nm, anchor=anchor, size=13, fill='#fff', ls='0'))
# the first message
(ux, uy), (sx, sy) = NODES['UCLA'], NODES['SRI']
for ch, t0 in LETTERS:
    a(f'<g class="fx" opacity="0">{win(t0, t0 + FLIGHT)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + FLIGHT, sx - ux), (D, sx - ux)], "x")}'
      f'<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + FLIGHT, sy - uy), (D, sy - uy)], "y")}'
      f'<rect x="{ux - 11}" y="{uy - 11}" width="22" height="22" rx="3" fill="{ROUTE}"/>{text(ux, uy + 5, ch, anchor="middle", size=14, fill=CDEEP, ls="0")}</g></g></g>')
# what SRI received
a(text(150, 64, 'SRI got:', size=13, fill=CMUTED, ls='0'))
for i, (ch, t0) in enumerate(LETTERS[:2]):
    a(f'<g>{held(t0 + FLIGHT, MS0 + 7 * 0.7)}{text(228 + i * 16, 64, ch, size=15, fill=ROUTE, ls="0")}</g>')
a(f'<g>{held(CRASH, MS0 + 7 * 0.7)}{text(266, 64, "crash", size=13, fill=RED, ls="0")}'
  f'<line x1="{sx - 9}" y1="{sy - 9}" x2="{sx + 9}" y2="{sy + 9}" stroke="{RED}" stroke-width="2.5"/><line x1="{sx + 9}" y1="{sy - 9}" x2="{sx - 9}" y2="{sy + 9}" stroke="{RED}" stroke-width="2.5"/></g>')
a(text(150, 232, 'UCLA to SRI, 29 Oct 1969', size=13, fill=CMUTED, ls='0'))
# milestones
a(text(20, 262, 'HOW IT GREW', size=13, fill=CMUTED))
for k, (yr, ev) in enumerate(MS):
    y = 284 + k * 19
    a(text(20, y, yr, size=13, fill=CYAN, ls='0'))
    a(text(76, y, ev, size=13, fill=CSOFT, ls='0'))
    t0 = MS0 + k * 0.7
    a(f'<rect class="fx" x="14" y="{y - 14}" width="372" height="19" rx="2" fill="{CYAN}" fill-opacity="0.15" opacity="0">{win(t0, t0 + 0.7)}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('In December 1969 the ARPANET was four computers on leased 50 kbps lines, each joined to the network by an IMP, a refrigerator-sized packet switch built by BBN. '
           'Its first message, on 29 October, went from UCLA to SRI: L and O arrived, then the receiving system crashed.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The message.</b> UCLA was typing LOGIN; the second try, an hour later, went through.</li>
          <li><b>The IMPs.</b> Interface Message Processors were Honeywell DDP-516 minicomputers that did the packet switching, so the hosts did not have to.</li>
          <li><b>Flag day.</b> On 1 January 1983 the ARPANET switched from its original protocol, NCP, to TCP/IP, the protocols the internet still runs.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-2">
      <div class="diagram-label">Fig 9.2 · The first internet</div>
      {svg}
      <p id="ch9-arpanet-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-2', 'ch9-arpanet-p4', card)
