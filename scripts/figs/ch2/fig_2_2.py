"""Fig 2.2: Boole's AND and Shannon's AND are the same thing, by the reader's own hand.
Two switches in series, each closed or opened by a press (public/live-figures.js, data-live="switches"); the lamp
lights only with both closed, and Boole's circles above light with them: A, B, and the overlap for both.
Parts carry data-when="A&B" (shown while that holds), the switch levers data-turn, the press areas data-sw."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
SOFT = 'rgba(255,255,255,0.8)'
b = []
def when(cond, inner): return f'<g data-when="{cond}" opacity="0">{inner}</g>'
# --- Boole
b.append(text(20, 26, 'BOOLE · 1847', 14, SOFT, 'start', ' letter-spacing="0.06em"'))
for cx, name in ((160, 'A'), (240, 'B')):
    b.append(when(name, f'<circle cx="{cx}" cy="104" r="58" fill="rgba(134,168,255,0.56)"/>'))
    b.append(f'<circle cx="{cx}" cy="104" r="58" fill="none" stroke="#d4e0ff" stroke-width="1.5"/>')
b.append(when('A&B', f'<path d="M 200 62 A 58 58 0 0 1 200 146 A 58 58 0 0 1 200 62 Z" fill="{GOLD}" fill-opacity="0.8"/>'))
b.append(text(128, 110, 'A', 18, '#fff') + text(272, 110, 'B', 18, '#fff'))
# --- Shannon
b.append(text(20, 206, 'SHANNON · 1937', 14, SOFT, 'start', ' letter-spacing="0.06em"'))
Y = 246
wire = f'M 30 {Y} H 110 M 160 {Y} H 210 M 260 {Y} H 316 M 344 {Y} H 368 V {Y+54} H 30 V {Y+28} M 30 {Y+16} V {Y}'
b.append(f'<g data-when="!A|!B"><path d="{wire}" fill="none" stroke="{INK}" stroke-opacity="0.5" stroke-width="2"/></g>')
run = f'M 30 {Y+16} V {Y} H 368 V {Y+54} H 30 V {Y+28}'
b.append(when('A&B', f'<path d="{wire}" fill="none" stroke="{GOLD}" stroke-width="2.8" stroke-linejoin="round"/>'
              f'<path d="{run}" fill="none" stroke="#fff6d8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="0.1 23">'
              f'<animate attributeName="stroke-dashoffset" values="23.1;0" dur="0.6s" repeatCount="indefinite"/></path>'))
# battery
b.append(f'<path d="M 18 {Y+16} H 42 M 23 {Y+28} H 37" stroke="#fff" stroke-width="2.5"/>')
# the two switches: contacts, a lever that turns, a name, and a generous area to press
for x, name in ((110, 'A'), (210, 'B')):
    b.append(f'<circle cx="{x}" cy="{Y}" r="3.5" fill="#fff"/><circle cx="{x+50}" cy="{Y}" r="3.5" fill="#fff"/>')
    b.append(f'<line class="lv-lever" data-turn="{name}" x1="{x}" y1="{Y}" x2="{x+50}" y2="{Y}" stroke="#fff" stroke-width="3" stroke-linecap="round" style="transform-origin:{x}px {Y}px"/>')
    b.append(text(x + 25, Y + 28, name, 16, '#fff'))
# lamp
b.append(f'<circle cx="330" cy="{Y}" r="14" fill="none" stroke="{INK}" stroke-opacity="0.6" stroke-width="1.6"/>')
b.append(line(f'M 324 {Y+4} l 3 -8 l 3 8 l 3 -8', INK, 1.4, ' stroke-opacity="0.6"'))
b.append(when('A&B', f'<circle cx="330" cy="{Y}" r="26" fill="{GOLD}" fill-opacity="0.2"/><circle cx="330" cy="{Y}" r="14" fill="{GOLD}"/>' + line(f'M 324 {Y+4} l 3 -8 l 3 8 l 3 -8', '#0a0a0a', 1.4)))
# press areas last, on top; then the press-here marks (the first switch not yet pressed shows its mark)
for x, name in ((110, 'A'), (210, 'B')):
    b.append(f'<rect data-sw="{name}" x="{x-14}" y="{Y-40}" width="78" height="78" fill="#000" fill-opacity="0" style="cursor:pointer"/>')
    b.append(f'<g data-hint="{name}">{hint(x + 27, Y - 12)}</g>')
put('fig-2-2', '0 0 400 312', None, None,
    'Fig 2.2 · Boole\'s algebra · Shannon\'s switches',
    'Above, Boole (1847): two overlapping circles, A and B; A · B is their overlap, true only where both hold. Below, Shannon (1937): a battery, two switches in series and a lamp. The reader opens and closes each switch by pressing it. Closing switch A fills circle A, closing B fills circle B. Only with both closed does current run round the circuit and the lamp light, and at that moment the overlap of the two circles lights too.',
    b,
    caption='The same AND, in algebra and in wire.',
    attrs='data-live="switches" data-switches="A B"')
