"""Fig 2.6: inside a full adder. Redrawn 2026-11-20 (owner: "simplify most of them"; this was the densest figure of
the chapter: five gate symbols, two dashed groups, eight step buttons). Now three boxes, as its own caption always
said: two half adders and an OR. One sum runs through them, 1 + 1 + 1: the first half adder gives 0 carry 1, the
second adds the carry in and gives 1 carry 0, the OR joins the two carries. Sum 1, carry out 1: binary 11, three."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 8.0
CREAM = '#ece6da'
b = []
def box(x, y, w, h, name, t0, t1):
    b.append(show(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" stroke="{INK}" stroke-opacity="0.75" stroke-width="1.6"/>', [(0, t0), (t1, D)], D))
    b.append(show(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" stroke="{GOLD}" stroke-width="2.6"/>', [(t0, t1)], D))
    b.append(text(x + w / 2, y + h / 2 + 5, name, 14, CREAM))
def bit(x, y, v, t0):
    """A place for one bit on a wire: an empty ring until its value is known."""
    col = GOLD if v else INK
    val = f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{col}" stroke-width="1.8"/>' + text(x, y + 5, str(v), 14, col)
    if t0 is None: b.append(val)
    else:
        b.append(show(f'<circle cx="{x}" cy="{y}" r="10" fill="none" stroke="{INK}" stroke-opacity="0.6" stroke-width="1.5"/>', [(0, t0)], D))
        b.append(show(val, [(t0, D)], D))
wire = lambda d: b.append(line(d, INK, 1.4, ' stroke-opacity="0.55"'))
# wires first, so the boxes and the bits sit on them
wire('M 44 62 H 70 M 44 92 H 70')                 # A and B into the first half adder
wire('M 170 62 H 182 M 202 62 H 214')             # its sum on to the second
wire('M 264 32 V 48')                             # the carry in, from above
wire('M 314 77 H 330')                            # the sum out
wire('M 120 106 V 122 M 120 142 V 176 H 150 M 264 106 V 122 M 264 142 V 176 H 234')   # the two carries down to the OR
wire('M 192 196 V 212')                           # the carry out
box(70, 48, 100, 58, 'half adder', 1.2, 2.6)
box(214, 48, 100, 58, 'half adder', 2.6, 4.0)
box(150, 156, 84, 40, 'OR', 4.0, 5.4)
b.append(text(12, 67, 'A', 14, MUTE) + text(12, 97, 'B', 14, MUTE))
bit(34, 62, 1, None); bit(34, 92, 1, None)
b.append(text(282, 26, 'carry in', 13, MUTE, 'start')); bit(264, 22, 1, None)
bit(192, 62, 0, 1.9); bit(120, 132, 1, 1.9)        # first half adder: 1 + 1 = 0, carry 1
bit(340, 77, 1, 3.3); bit(264, 132, 0, 3.3)        # second: 0 + 1 = 1, carry 0
b.append(text(340, 104, 'sum', 13, MUTE))
bit(192, 222, 1, 4.7)
b.append(text(210, 227, 'carry out', 13, MUTE, 'start'))
put('fig-2-6', '0 6 362 236', None, None,
    'Fig 2.6 · Inside a full adder',
    'Three boxes: two labelled half adder, side by side, and one labelled OR below and between them. The bits A and B, both 1, enter the first half adder. It gives a sum of 0, which goes on to the second half adder, and a carry of 1, which goes down to the OR. The second half adder also takes the carry in, 1, from above; it gives the sum, 1, out to the right, and a carry of 0 down to the OR. The OR of the two carries, 1 and 0, is the carry out: 1. So 1 + 1 + 1 gives sum 1, carry 1, which is binary 11.',
    b,
    caption='1 + 1 + 1: sum 1, carry 1. Binary 11 is three.')
