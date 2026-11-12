"""Fig 1.4: a transistor is a switch flipped by electricity instead of a finger.
ONE lamp loop with one gap. First a hand pushes a lever across the gap; then the lever is swapped
for the transistor of Fig 1.3 (the can on three legs) and a small signal does the hand's job."""
from plate import *
D = 10.0
k = lambda t: t / D
# loop geometry
L, R, T, B = 56, 236, 74, 204          # left, right, top, bottom of the wire loop
G0, G1 = 106, 174                      # the gap in the right side
XM = (L + R) // 2
FING = [(2.4, 4.6)]                    # lamp lit by the finger
SIG = [(6.4, 9.4)]                     # lamp lit by the signal
LIT = FING + SIG
b = []
# --- wires (the top wire breaks under the bulb, the bottom under the battery)
b.append(line(f'M {XM-30} {B} H {L} V {T} H {XM-7} M {XM+7} {T} H {R} V {G0}'))
b.append(line(f'M {R} {G1} V {B} H {XM+26}'))
# --- current: the wire turns gold and bright dots run round it, clockwise from the battery's +
def current(d, spans):
    return show(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="#fff6d8" stroke-width="5.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="0.1 23">'
                f'<animate attributeName="stroke-dashoffset" values="23.1;0" dur="0.6s" repeatCount="indefinite"/></path>', spans, D)
b.append(current(f'M {XM-30} {B} H {L} V {T} H {R} V {B} H {XM+26}', FING))
b.append(current(f'M {XM-30} {B} H {L} V {T} H {R} V {G0} V 122 H 212 M 212 158 H {R} V {G1} V {B} H {XM+26}', SIG))
# --- battery
b.append(f'<rect x="{XM-25}" y="{B-11}" width="50" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="2"/>')
b.append(f'<rect x="{XM-30}" y="{B-5}" width="5" height="10" rx="1" fill="{INK}"/>')
b.append(text(XM - 12, B + 5, '+', 15, INK) + text(XM + 12, B + 4.5, '−', 15, MUTE))
# --- lamp
by = T - 32
b.append(f'<rect x="{XM-7}" y="{T-14}" width="14" height="15" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>')
b.append(f'<circle cx="{XM}" cy="{by}" r="19" fill="none" stroke="{INK}" stroke-width="2"/>')
fil = f'M {XM-6} {T-15} V {by+4} l 3 -6 l 3 6 l 3 -6 l 3 6 V {T-15}'
b.append(line(fil, INK, 1.5))
rays = ''.join(line(f'M {XM+dx*25:.1f} {by+dy*25:.1f} L {XM+dx*33:.1f} {by+dy*33:.1f}', GOLD, 2.2)
               for dx, dy in [(-0.97, -0.26), (-0.71, -0.71), (-0.26, -0.97), (0.26, -0.97), (0.71, -0.71), (0.97, -0.26)])
b.append(show(f'<circle cx="{XM}" cy="{by}" r="19" fill="{GOLD}" fill-opacity="0.6" stroke="{GOLD}" stroke-width="2"/>' + line(fil, '#fff', 1.7) + rays, LIT, D))
# --- act one: a lever across the gap, and a hand
HANDK = [0, k(2.0), k(2.4), k(4.6), k(5.0), 1]
lever = line(f'M {R} {G1} V {G0}', INK, 3.4)
act1 = (f'<circle cx="{R}" cy="{G0}" r="3.6" fill="{INK}"/><circle cx="{R}" cy="{G1}" r="3.6" fill="{INK}"/>'
        f'<g>{xform("rotate", [f"32 {R} {G1}", f"32 {R} {G1}", f"0 {R} {G1}", f"0 {R} {G1}", f"32 {R} {G1}", f"32 {R} {G1}"], HANDK, D)}{lever}</g>')
hx, hy = R + 26, 138                    # fingertip (at rest), finger pointing left
hand = (f'<path d="M {hx+40} {hy-7} H {hx+7} a 7 7 0 0 0 0 14 H {hx+34}" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M {hx+40} {hy-7} q 2 -9 14 -9 h 16 q 10 0 10 10 v 34 q 0 10 -10 10 h -20 q -9 0 -11 -8" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M {hx+34} {hy+7} q -7 1 -7 7 q 0 6 8 6 h 10 M {hx+29} {hy+20} q -5 1 -5 6 q 0 6 8 6 h 10 M {hx+33} {hy+32} q -3 2 -2 6" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M {hx+46} {hy-16} q 6 -10 16 -8" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
        f'<rect x="{hx+80}" y="{hy-15}" width="13" height="52" rx="3" fill="none" stroke="{INK}" stroke-width="2"/>')      # a closed cuff: the arm ends inside the picture
act1 += f'<g>{xform("translate", ["0 0", "0 0", "-23 0", "-23 0", "0 0", "0 0"], HANDK, D)}{hand}</g>'
b.append(show(act1, [(0, 5.2)], D))
# --- act two: the transistor of Fig 1.3 in the same gap, its third leg taking the signal
can = (line(f'M {R} {G0} V 122 H 212') + line(f'M 212 158 H {R} V {G1}') + line(f'M 212 140 H {R+44}')
       + f'<rect x="166" y="116" width="38" height="48" rx="6" fill="none" stroke="{INK}" stroke-width="2"/>'
       + f'<rect x="204" y="112" width="8" height="56" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>')
names = text(156, 145, 'transistor', 14, MUTE, 'end') + text(R + 8, 128, 'base', 13, MUTE, 'start') + text(R + 66, 164, 'signal', 14, MUTE)
sig = (f'<path d="M {R+86} 140 H {R+52}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-dasharray="5 5" stroke-linecap="round">'
       f'<animate attributeName="stroke-dashoffset" values="0;10" dur="0.6s" repeatCount="indefinite"/></path>'
       f'<path d="M {R+44} 140 l 10 -6 v 12 Z" fill="{GOLD}"/>'
       + line(f'M 212 140 H {R+44}', GOLD, 2.4)
       + f'<rect x="166" y="116" width="38" height="48" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.6"/>'
       + f'<rect x="204" y="112" width="8" height="56" rx="2" fill="none" stroke="{GOLD}" stroke-width="2.2"/>')
b.append(show(can, [(5.2, SIG[0][0]), (SIG[0][1], D)], D))     # white while idle; the gold copy below takes over on the signal
b.append(show(names, [(5.2, D)], D))
b.append(show(sig, SIG, D))
put('fig-1-4', '30 4 342 228', [1.0, 3.6, 8.0], ['off', 'finger', 'signal'],
    'Fig 1.4 · Transistor as a switch',
    'One circuit: a battery, a lamp and a gap in the wire. First a lever sits across the gap, open, and the lamp is dark. A hand pushes the lever shut: current runs round the loop and the lamp lights. Then the lever is replaced by a transistor, the small metal can on three legs from Fig 1.3: two legs join the two sides of the gap, the third, the base, leads away to the right. With nothing on the base the lamp is dark. A small signal arrives on the base: the transistor conducts, the same current runs round the loop and the lamp lights, with nothing moving.',
    b,
    caption='First a finger closes the gap; then a transistor does, on a small signal.',
    strip=[('Three legs', 'Two of the transistor\'s legs, the collector and the emitter, sit in the gap and carry the large current; the third, the base, controls it.'),
           ('The threshold', 'In this kind of transistor about 0.7 V on the base opens the path; below it, almost nothing flows.'),
           ('Small controls large', 'The signal into the base is tiny beside the current it lets through, so one transistor\'s output can be the signal for many others.'),
           ('The direction', 'The dots run the conventional way, out of the battery\'s + and back to its other end; the electrons that carry the current drift the other way.'),
           ('The other kind', 'This is the older kind of transistor. Modern chips are built from the field-effect kind, whose control terminal is called the gate (Fig 1.5).')])
