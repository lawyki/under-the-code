"""Fig 2.1: why two levels and not three. Redrawn 2026-11-12 after the owner saw the Pass 28 figure for the first
time: "way too complex ... figures, not entire games ... places to learn, not things TO learn."
One idea, seen in one look: the same noise shakes a signal on a two-level wire and on a three-level wire. On two
levels it stays in its zone and is still read right; on three it strays into the zone above and is read wrong.
Two boxes, their dividing lines, one dot each, one line of reading under each. No steps, no rows of digits."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
CREAM = '#ece6da'; BAD = '#ec8d8d'
D = 6.0
TOP, BOT = 52, 226                       # the wire's span: its highest and lowest level
SPAN = BOT - TOP
LIFT = [60, 33, 42, 15, 24, 6, 18, 3, 21, 36, 27, 51, 42, 57, 60, 60]          # the noise, one shake (Pass 28's)
KT = [0, 1/15, 2/15, 3/15, 4/15, 5/15, 0.416667, 0.5, 0.583333, 10/15, 11/15, 12/15, 13/15, 14/15, 0.999917, 1]
lift = [v * 0.87 for v in LIFT]
wob = xform('translate', [f'0 {-v:.1f}' for v in lift], KT, D)
# when the three-level signal is past its dividing line (a quarter of the span above the middle level)
margin = SPAN / 4
over = []; t_in = 0.0 if lift[0] > margin else None
for i in range(len(KT) - 1):
    a, b_ = lift[i], lift[i + 1]
    if (a > margin) != (b_ > margin):
        t = (KT[i] + (KT[i + 1] - KT[i]) * (margin - a) / (b_ - a)) * D
        if t_in is None: t_in = t
        else: over.append((t_in, t)); t_in = None
if t_in is not None: over.append((t_in, D))
calm = [(e, s) for (_, e), (s, _) in zip(over, over[1:])]
b = []
def wire(x, title, lines, names):
    b.append(text(x + 45, 34, title, 15, CREAM))
    b.append(f'<rect x="{x}" y="{TOP-10}" width="90" height="{SPAN+20}" rx="6" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>')
    for y in lines: b.append(f'<line x1="{x}" y1="{y:.1f}" x2="{x+90}" y2="{y:.1f}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for n, y in names: b.append(text(x + 16, y + 5, n, 14, MUTE))
# two levels: the signal is sent low
wire(56, 'two levels', [TOP + SPAN / 2], [('1', TOP + SPAN / 4), ('0', TOP + 3 * SPAN / 4)])
b.append(f'<line x1="92" y1="{BOT}" x2="132" y2="{BOT}" stroke="{BLUE}" stroke-width="1.5" stroke-opacity="0.6"/>')
b.append(f'<g>{wob}<circle cx="105" cy="{BOT}" r="7.5" fill="{BLUE}"/></g>')
b.append(text(101, 262, 'read as 0', 15, CREAM))
# three levels in the same span: the signal is sent in the middle
mid = TOP + SPAN / 2
wire(214, 'three levels', [TOP + SPAN / 4, TOP + 3 * SPAN / 4], [('2', TOP + SPAN / 8 - 2), ('1', mid), ('0', BOT - SPAN / 8 + 2)])
b.append(f'<line x1="250" y1="{mid}" x2="290" y2="{mid}" stroke="{BLUE}" stroke-width="1.5" stroke-opacity="0.6"/>')
b.append(show(f'<rect x="215.5" y="{TOP-8.5}" width="87" height="{SPAN/4+8.5:.1f}" rx="5" fill="none" stroke="{BAD}" stroke-width="2.4"/>'
              + text(259, 262, 'read as 2', 15, BAD), over, D))
b.append(show(text(259, 262, 'read as 1', 15, CREAM), calm, D))
b.append(f'<g>{wob}<circle cx="263" cy="{mid}" r="7.5" fill="{BLUE}"/></g>')
put('fig-2-1', '20 10 320 268', None, None,
    'Fig 2.1 · Why binary survives noise · one threshold against two',
    'Two wires with the same voltage span, drawn as two boxes of the same height. The left wire has two levels, 0 and 1, with one dividing line across the middle. The right wire squeezes three levels, 0, 1 and 2, into the same height, with two dividing lines. A dot in each shows the signal: the left sends 0, the right sends 1, and the same noise shakes both upward by the same amount. The left dot never reaches its dividing line and is always read as 0. The right dot keeps crossing the line above it: while it is over, the top zone is outlined in red and the reading under the box changes from 1 to 2.',
    b,
    caption='The same noise leaves two levels readable; with three, the signal strays into the level above.')
