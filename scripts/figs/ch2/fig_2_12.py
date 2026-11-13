"""Fig 2.12: the Patriot's clock. Redrawn 2026-11-13 (was a graph, a radar track, a bracket and three steps).
One scene: the Scud, and the place the radar looks for it. As the hours run up, the place slides away from the Scud."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 8.0
k = lambda t: t / D
CREAM = '#ece6da'
Y = 110
b = []
b.append(line(f'M 26 {Y} H 334', INK, 1.2, ' stroke-opacity="0.5" stroke-dasharray="3 6"'))
b.append(f'<circle cx="270" cy="{Y}" r="9" fill="{RED}"/>' + text(270, Y + 48, 'Scud', 14, RED))
# where the radar looks: on the Scud at first, 570 m behind it after 100 hours
SH = -150
slide = xform('translate', ['0 0', '0 0', f'{SH} 0', f'{SH} 0'], [0, k(1.0), k(5.6), 1], D)
b.append(f'<g>{slide}<rect x="236" y="{Y-26}" width="68" height="52" rx="7" fill="none" stroke="{BLUE}" stroke-width="2"/>' + text(270, Y - 36, 'radar', 14, BLUE) + '</g>')
# the hours
hrs = [(0, 0.0, 2.15), (25, 2.15, 3.3), (50, 3.3, 4.45), (75, 4.45, 5.6), (100, 5.6, D)]
for h, t0, t1 in hrs:
    b.append(show(text(30, 48, f'{h} h', 20, CREAM, 'start'), [(t0, t1)], D))
b.append(show(line(f'M 120 {Y+26} v 8 H 270 v -8', CREAM, 1.4) + text(195, Y + 54, '570 m', 14, CREAM), [(5.9, D)], D))
put('fig-2-12', '14 20 332 152', None, None,
    'Fig 2.12 · The Patriot\'s clock',
    'A dashed line, the path through the sky, with a red dot on it: the Scud. A blue box labelled radar marks where the Patriot system looks for it. At 0 hours the box sits on the Scud. A counter at the top left runs up through 25, 50 and 75 to 100 hours, and as it does the box slides steadily away from the Scud. At 100 hours a bracket between them reads 570 metres: the radar is looking at empty sky.',
    b,
    caption='In 100 hours the clock fell 0.34 s behind: some 570 m of sky.')
