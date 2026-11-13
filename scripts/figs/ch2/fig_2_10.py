"""Fig 2.10: a floating-point number. Redrawn 2026-11-13 (was three bit strings, two derivation lines, a row of boxes,
an equation, a result and two steps). One example, one move: the exponent slides the point through the digits.
Sign +, exponent 2, mantissa 1.101: the point moves two places and the digits read 110.1, which is 6.5."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 7.0
k = lambda t: t / D
CREAM = '#ece6da'
b = []
# the three stored parts, in plain values
for x, w, col, name, val in ((40, 56, RED, 'sign', '+'), (112, 88, BLUE, 'exponent', '2'), (216, 104, GOLD, 'mantissa', '1.101')):
    b.append(text(x + w / 2, 38, name, 13, col))
    b.append(f'<rect x="{x}" y="46" width="{w}" height="32" rx="5" fill="none" stroke="{col}" stroke-width="1.6"/>')
    b.append(text(x + w / 2, 68, val, 16, col))
# the digits, and the point that the exponent moves
X0, W, GAP, Y = 82, 38, 14, 118
for i, d in enumerate('1101'):
    x = X0 + i * (W + GAP)
    b.append(f'<rect x="{x}" y="{Y}" width="{W}" height="46" rx="6" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
    b.append(text(x + W / 2, Y + 31, d, 22, CREAM))
    b.append(show(text(x + W / 2, Y - 8, ['4', '2', '1', '0.5'][i], 13, MUTE), [(3.6, D)], D))
px = X0 + W + GAP / 2
step = W + GAP
b.append(f'<g>{xform("translate", ["0 0", "0 0", f"{step} 0", f"{step} 0", f"{2*step} 0", f"{2*step} 0"], [0, k(1.4), k(2.0), k(2.4), k(3.0), 1], D)}'
         f'<circle cx="{px}" cy="{Y+42}" r="5.5" fill="{BLUE}"/></g>')
b.append(show(text(180, 204, '+6.5', 22, GOLD), [(4.2, D)], D))
put('fig-2-10', '20 16 320 200', None, None,
    'Fig 2.10 · A floating-point number',
    'Above, the three parts a floating-point number is stored as, each in its own box: the sign, here plus; the exponent, here 2; and the mantissa, here 1.101 in binary. Below, the four digits 1 1 0 1 in a row of boxes with a point after the first. The point slides two boxes to the right, as the exponent says, so the digits read 110.1. Their place values appear above them, 4, 2, 1 and 0.5: 4 plus 2 plus 0.5, with the sign, is +6.5.',
    b,
    caption='A double keeps 1 bit of sign, 11 of exponent and 52 of mantissa.')
