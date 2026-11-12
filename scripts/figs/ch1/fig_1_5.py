"""Fig 1.5: inside the switch, as a figure the reader drives (public/live-figures.js, data-live="mosfet").
The slider under the picture sets the gate voltage. Charge gathers on the gate, the holes beneath sink,
electrons creep in from both wells; at about 0.7 V they meet, current runs round the loop and the lamp lights.
This script writes the resting picture (0 V); the script file moves the marked parts.
Round six (owner: "too much things going on"): holes only where they matter, under the gate; six electrons a
well; no arrow; the outer wire turns gold as in Fig 1.4 and only the channel shows electrons moving."""
from plate import *
b = []
def plus(x, y, col=RED, w=1.8, r=4): return line(f'M {x-r} {y} H {x+r} M {x} {y-r} V {y+r}', col, w)
WY = 44                                  # the outer wire
# --- the loop outside: lamp and battery between drain and source
loop = f'M 88 124 V {WY} H 133 M 147 {WY} H 216 M 264 {WY} H 292 V 124'
b.append(line(loop))
b.append(f'<path class="lv-wire" d="{loop}" fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>')
# battery (minus end toward the source: the electrons leave it there)
b.append(f'<rect x="216" y="{WY-11}" width="44" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="2"/>')
b.append(f'<rect x="260" y="{WY-5}" width="5" height="10" rx="1" fill="{INK}"/>')
b.append(text(228, WY + 4.5, '−', 15, INK) + text(249, WY + 5, '+', 15, INK))
# lamp
lx, ly = 140, WY - 30
b.append(f'<rect x="{lx-7}" y="{WY-14}" width="14" height="15" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>')
b.append(f'<circle cx="{lx}" cy="{ly}" r="17" fill="none" stroke="{INK}" stroke-width="2"/>')
fil = f'M {lx-6} {WY-15} V {ly+4} l 3 -6 l 3 6 l 3 -6 l 3 6 V {WY-15}'
b.append(line(fil, INK, 1.5))
rays = ''.join(line(f'M {lx+dx*23:.1f} {ly+dy*23:.1f} L {lx+dx*30:.1f} {ly+dy*30:.1f}', GOLD, 2.2)
               for dx, dy in [(-0.97, -0.26), (-0.71, -0.71), (-0.26, -0.97), (0.26, -0.97), (0.71, -0.71), (0.97, -0.26)])
b.append(f'<g class="lv-lamp" opacity="0"><circle cx="{lx}" cy="{ly}" r="17" fill="{GOLD}" fill-opacity="0.6" stroke="{GOLD}" stroke-width="2"/>' + line(fil, '#fff', 1.7) + rays + '</g>')
# --- silicon
b.append(f'<rect x="30" y="132" width="320" height="86" rx="4" fill="none" stroke="{RED}" stroke-opacity="0.9" stroke-width="1.4"/>')
for x in (46, 250):
    b.append(f'<rect x="{x}" y="132" width="84" height="48" rx="10" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    for dx in (18, 42, 66):
        for dy in (22, 37): b.append(f'<circle cx="{x+dx}" cy="{132+dy}" r="3.4" fill="{BLUE}"/>')
# the holes under the gate, with their name: they sink together
b.append('<g class="lv-holes">' + ''.join(plus(x, 154) for x in (150, 170, 190, 210, 230)) + text(190, 176, 'holes', 13, RED) + '</g>')
# the bridge electrons: each knows its well-side home and its place under the gate
for i, x in enumerate([140, 154, 168, 182, 238, 224, 210, 196]):
    home, rank = (124, i) if i < 4 else (256, i - 4)
    b.append(f'<circle class="lv-e" data-home="{home}" data-slot="{x}" data-rank="{rank}" cx="{home}" cy="139" r="3.4" fill="{BLUE}" opacity="0"/>')
# electrons on the move, shown by the script once the bridge is whole: out of the source, across, into the drain
b.append(f'<path class="lv-stream" d="M 98 139 H 282" fill="none" stroke="{BLUE}" stroke-width="6.8" stroke-linecap="round" stroke-dasharray="0.1 14" opacity="0"/>')
# oxide, gate, contacts
b.append(f'<rect x="122" y="124" width="136" height="8" fill="#8a857a"/>')
b.append(f'<rect x="130" y="102" width="120" height="22" rx="2" fill="#b9b4a8"/>')
b.append(f'<rect class="lv-gate" x="130" y="102" width="120" height="22" rx="2" fill="{GOLD}" opacity="0"/>')
for i, x in enumerate((148, 162, 176, 190, 204, 218, 232)):
    b.append(f'<g class="lv-q" data-n="{[5, 3, 1, 0, 2, 4, 6][i]}" opacity="0">' + line(f'M {x-4.5} 113 H {x+4.5} M {x} 108.5 V 117.5', '#3a2c08', 2.2) + '</g>')
for x in (88, 292):
    b.append(f'<rect x="{x-12}" y="124" width="24" height="8" fill="#b9b4a8"/>')
b.append(line('M 190 102 V 90'))
b.append(text(190, 80, 'gate', 14, MUTE, 'end', ' class="lv-gname"') + text(196, 80, '0.00 V', 14, MUTE, 'start', ' class="lv-v"'))
b.append(text(60, 118, 'source', 14, MUTE, 'end') + text(320, 118, 'drain', 14, MUTE, 'start'))
b.append(text(88, 198, 'electrons', 13, BLUE))
put('fig-1-5', '4 -24 372 248', None, None,
    'Fig 1.5 · Inside the switch · a field-effect transistor',
    'A cross-section of a transistor that the reader controls with a slider. A block of p-type silicon, with a row of plus signs under the gate for its holes, holds two n-type wells full of free electrons, drawn as blue dots: the source on the left and the drain on the right. Between them, on top, a metal gate sits on a thin insulating layer. A wire joins source and drain through a battery and a lamp. As the gate voltage is raised from 0, positive charge gathers on the gate, the holes beneath it are pushed down, and electrons creep in from both wells along the underside of the insulator. At about 0.7 volts the two rows meet: electrons then stream from the source across the bridge into the drain, the wire of the loop turns gold and the lamp lights, brighter as the voltage rises. Lower the voltage and the bridge breaks, the stream stops and the lamp goes dark.',
    b,
    caption='Raise the gate voltage until the electrons meet: the bridge closes and the lamp lights.',
    strip=[('The silicon', 'Source and drain are n-type, full of free electrons (the blue dots); the body between them is p-type, with holes (the plus signs). Where the two kinds meet, electrons fill the nearby holes and leave a thin barrier, so nothing joins source to drain.'),
           ('The pull', 'A positive voltage puts positive charge on the gate. Opposite charges attract: it draws electrons in from both wells and pushes the holes away beneath it.'),
           ('The threshold', 'Below about 0.7 V the two rows of electrons do not meet and nothing flows. Once they join, the bridge (the channel) carries electrons from source to drain: the switch is on. More voltage, more current. Back at 0 V the electrons return to their wells and the switch is off.'),
           ('The direction', 'The electrons cross from source to drain, pushed out of the battery\'s − end and drawn back to its +: the opposite way round to the conventional current drawn in Fig 1.4.'),
           ('The field', 'The gate never touches the electrons: it pulls through the insulator, as a rubbed balloon lifts hair, and that pull across a gap is an electric field.'),
           ('The name', 'MOSFET: metal-oxide-semiconductor field-effect transistor, the kind a modern chip holds billions of.')])
# mark the svg as live
import re
s = open(PAGE).read(); a = s.index('id="fig-1-5"'); m = re.compile(r'<svg\b[^>]*>').search(s, a)
if 'data-live' not in m.group(0):
    s = s[:m.end()-1] + ' data-live="mosfet">' + s[m.end():]; open(PAGE, 'w').write(s)
