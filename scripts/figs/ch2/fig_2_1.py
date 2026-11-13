"""Fig 2.1: why two levels and not three. Third form, 2026-11-13. The owner on the second (two boxes, dots,
"read as 0"): "way too much text and isn't visible what it even represents."
So: the lamp the reader already knows from Figs 1.3 to 1.5, and their own eye as the judge. Two lamps, off and
on, flicker: still plainly off and on. Three lamps, off, half and full, flicker by the same amount: the half-lit
one keeps looking like its neighbours. The only text is the digit each lamp stands for."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 4.8
NOISE = [0.30, -0.12, 0.22, -0.28, 0.05, 0.27, -0.20, 0.14, -0.30, 0.18, -0.06, 0.30]      # one flicker, the same for every lamp
KT = [i / (len(NOISE) - 1) for i in range(len(NOISE))]
b = []
def lamp(x, y, level, shift):
    """A lamp whose light is its level (0, 0.5 or 1) plus the noise; shift staggers the lamps so they do not blink as one."""
    r = 20
    seq = NOISE[shift:] + NOISE[1:shift + 1]
    vals = ['%.2f' % min(1, max(0, level + n)) for n in seq]
    base = (f'<rect x="{x-8}" y="{y+r-3}" width="16" height="17" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{INK}" stroke-width="2"/>')
    fil = f'M {x-7} {y+r-4} V {y+5} l 3.5 -7 l 3.5 7 l 3.5 -7 l 3.5 7 V {y+r-4}'
    rays = ''.join(line(f'M {x+dx*27:.1f} {y+dy*27:.1f} L {x+dx*33:.1f} {y+dy*33:.1f}', GOLD, 2.4)
                   for dx, dy in [(-0.97, -0.26), (-0.71, -0.71), (-0.26, -0.97), (0.26, -0.97), (0.71, -0.71), (0.97, -0.26)])
    light = (f'<g opacity="{vals[0]}">{anim("opacity", vals, KT, D)}<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" stroke="{GOLD}" stroke-width="2"/>{rays}</g>')
    b.append(light + base + line(fil, INK, 1.6))
Y = 70
for x, level, name, sh in ((62, 0, '0', 0), (132, 1, '1', 4)):
    lamp(x, Y, level, sh); b.append(text(x, Y + 62, name, 15, MUTE))
b.append(f'<line x1="186" y1="{Y-34}" x2="186" y2="{Y+66}" stroke="rgba(255,255,255,0.5)" stroke-width="1.2" stroke-dasharray="2 6"/>')
for x, level, name, sh in ((240, 0, '0', 0), (310, 0.5, '1', 7), (380, 1, '2', 4)):
    lamp(x, Y, level, sh); b.append(text(x, Y + 62, name, 15, MUTE))
put('fig-2-1', '14 10 414 136', None, None,
    'Fig 2.1 · Why binary survives noise · one threshold against two',
    'Five lamps in two groups, all flickering by the same amount. On the left, two lamps stand for the two levels of a binary wire: one dark, labelled 0, and one bright, labelled 1. Flicker and all, the dark one never looks bright and the bright one never looks dark. On the right, three lamps stand for the three levels of a ternary wire: dark (0), half lit (1) and bright (2). With the same flicker the half-lit lamp is at times as dim as the dark one and at times as bright as the bright one, so its level cannot be told reliably.',
    b,
    caption='With the same flicker, off and on stay easy to tell apart; half-lit does not.',
    strip=[('The lamps', 'Each lamp stands for one level a wire can be held at: its brightness is the voltage. Two lamps are binary\'s two levels; three are ternary\'s.'),
           ('The flicker', 'Noise. Ageing parts and temperature swings nudge every voltage a little, all the time.'),
           ('The margin', 'A level is read by which side of a dividing line it falls on. With two levels the line sits halfway, so a level must drift half the span to be misread. Three levels in the same span leave each only a quarter of the span, half of binary\'s margin.')])
