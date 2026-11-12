"""Fig 1.5: inside the switch. A cross-section where charge does the explaining:
gate off, electrons sit in two wells with a gap between; gate on, its + charge pulls electrons into a bridge; current then runs across."""
from plate import *
D = 9.0
P2, P3 = 3.0, 6.0                       # gate on at 3 s, current from 6 s
k = lambda t: t / D
body = []
# silicon body (p-type), wells (n-type)
body.append(f'<rect x="30" y="132" width="320" height="104" rx="4" fill="none" stroke="{RED}" stroke-opacity="0.9" stroke-width="1.4"/>')
for x in (46, 250):
    body.append(f'<rect x="{x}" y="132" width="84" height="48" rx="10" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
def plus(x, y, col=RED, w=1.8, r=4): return line(f'M {x-r} {y} H {x+r} M {x} {y-r} V {y+r}', col, w)
def dot(x, y, r=3.4, extra=''): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BLUE}">{extra}</circle>'
# holes that never move
for x in (52, 84, 116, 264, 296, 328):
    for y in (212, 228): body.append(plus(x, y))
# holes under the gate: at rest just under the oxide, pushed down while the gate is on
under = ''.join(plus(x, y) for x in (148, 169, 190, 211, 232) for y in (148, 166))
body.append(f'<g>{xform("translate", ["0 0", "0 0", "0 34", "0 34", "0 0"], [0, k(P2), k(P2 + 0.7), 0.97, 1], D)}{under}</g>')
# electrons at home in the wells
for x0 in (46, 250):
    for i, (dx, dy) in enumerate([(14, 21), (32, 21), (50, 21), (68, 21), (14, 37), (32, 37), (50, 37), (68, 37)]):
        body.append(dot(x0 + dx, 132 + dy))
# the bridge: electrons drawn in under the oxide from both wells
slots = [140, 154, 168, 182, 196, 210, 224, 238]
for i, x in enumerate(slots):
    home = 124 if i < 4 else 256
    body.append(f'<circle cy="139" r="3.4" fill="{BLUE}" cx="{home}" opacity="0">'
                + anim('cx', [home, home, x, x, home], [0, k(P2), k(P2 + 0.7), 0.97, 1], D)
                + anim('opacity', [0, 1, 0], [0, k(P2), k(P3)], D, discrete=True) + '</circle>')
# current: electrons streaming down the source lead, across the bridge, up the drain lead
stream = (f'<path d="M 88 66 V 139 H 292 V 66" fill="none" stroke="{BLUE}" stroke-width="6.8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="0.1 14">'
          f'<animate attributeName="stroke-dashoffset" values="14.1;0" dur="0.55s" repeatCount="indefinite"/></path>')
# oxide, gate, contacts, leads
body.append(f'<rect x="122" y="124" width="136" height="8" fill="#8a857a"/>')
body.append(f'<rect x="130" y="102" width="120" height="22" rx="2" fill="#b9b4a8"/>')
gate_on = (f'<rect x="130" y="102" width="120" height="22" rx="2" fill="{GOLD}"/>'
           + ''.join(plus(x, 113, '#3a2c08', 2.2, 4.5) for x in slots[::1][1:7]))
body.append(show(gate_on, [(P2, 0.97 * D)], D))
for x in (88, 292):
    body.append(f'<rect x="{x-12}" y="124" width="24" height="8" fill="#b9b4a8"/>')
    body.append(line(f'M {x} 124 V 66'))
body.append(line('M 190 102 V 84'))
body.append(show(stream, [(P3, 0.97 * D)], D))
body.append(show(line('M 160 160 H 214', BLUE, 2.4) + f'<path d="M 224 160 l -11 -6 v 12 Z" fill="{BLUE}"/>', [(P3, 0.97 * D)], D))
body.append(text(88, 196, 'electrons', 13, BLUE))
body.append(text(190, 230, 'holes', 13, RED))
body.append(text(88, 50, 'source', 14))
body.append(text(292, 50, 'drain', 14))
body.append(show(text(190, 76, 'gate 0 V', 14), [(0, P2), (0.97 * D, D)], D))
body.append(show(text(190, 76, 'gate +1 V', 14, GOLD), [(P2, 0.97 * D)], D))
put('fig-1-5', '14 30 352 214', [1.5, 4.8, 7.5], ['gate 0 V', 'gate +1 V', 'current'],
    'Fig 1.5 · Inside the switch · a field-effect transistor',
    'A cross-section of a transistor. A block of p-type silicon, marked with plus signs for its holes, holds two n-type wells full of free electrons, drawn as blue dots: the source on the left and the drain on the right. Between them, on top, a metal gate sits on a thin insulating layer. Gate at 0 volts: the holes fill the space under the gate, a gap separates the two wells and nothing flows. Gate at plus 1 volt: the gate turns gold and fills with positive charge; the holes beneath it are pushed down and electrons are pulled in from both wells to line up just under the insulator, bridging the gap. Then current flows: electrons stream down the source wire, across the bridge and up the drain wire.',
    body,
    caption='Positive charge on the gate pulls electrons into a bridge, and current crosses.',
    strip=[('The silicon', 'Source and drain are n-type, full of free electrons (the blue dots); the body between them is p-type, with holes (the plus signs). Where the two kinds meet, electrons fill the nearby holes and leave a thin barrier, so nothing joins source to drain.'),
           ('Gate on', 'A positive voltage puts positive charge on the gate. Opposite charges attract: it draws electrons in from both wells and pushes the holes away beneath it.'),
           ('The channel', 'The gathered electrons form a thin bridge under the oxide, and current can flow from source to drain: the switch is on.'),
           ('Gate off', 'At 0 V the pull stops, the electrons go back, the bridge is gone and the switch is off.'),
           ('The field', 'The gate never touches the electrons: it pulls through the insulator, as a rubbed balloon lifts hair, and that pull across a gap is an electric field.'),
           ('The name', 'MOSFET: metal-oxide-semiconductor field-effect transistor, the kind a modern chip holds billions of.')])
