"""Fig 1.3: the replacement. A light bulb, a vacuum tube and a transistor, to scale on a centimetre rule.
The tube is built like the bulb (glass, vacuum, hot filament), so it glows, runs hot and burns out; the transistor has nothing to burn."""
from plate import *
D = 6.0
ON, OFF = [(0, 3.0)], [(3.0, D)]
HOT = '#ffb35c'; GLASS = '#ece6da'; METAL = '#8a857a'; PALE = '#b9b4a8'
BASE = 268
b = []
# the rule: 1 cm = 20 units
b.append(line(f'M 30 {BASE} H 390', MUTE, 1.4))
for i in range(19):
    b.append(line(f'M {30+i*20} {BASE} V {BASE + (9 if i % 5 == 0 else 5)}', MUTE, 1.2))
b.append(line('M 30 252 H 50', MUTE, 1.2) + line('M 30 248 V 256 M 50 248 V 256', MUTE, 1.2))
b.append(text(40, 242, '1 cm', 13, MUTE))
def waves(pts, col=HOT):
    out = ''
    for i, (x, y) in enumerate(pts):
        out += (f'<path d="M {x} {y} q 5 -7 0 -14 q -5 -7 0 -14" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" opacity="0">'
                f'<animateTransform attributeName="transform" type="translate" values="0 6;0 -10" dur="1.6s" begin="-{i*0.37:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;0.85;0" dur="1.6s" begin="-{i*0.37:.2f}s" repeatCount="indefinite"/></path>')
    return out
# --- light bulb (6 cm across, 10.5 cm tall), standing on its cap
bx = 100
glass = f'M {bx-18} 206 C {bx-18} 182, {bx-60} 162, {bx-60} 118 A 60 60 0 1 1 {bx+60} 118 C {bx+60} 162, {bx+18} 182, {bx+18} 206 Z'
b.append(show(f'<circle cx="{bx}" cy="122" r="46" fill="{HOT}" opacity="0.2"><animate attributeName="opacity" values="0.16;0.26;0.18;0.24;0.16" dur="1.9s" repeatCount="indefinite"/></circle>', ON, D))
b.append(line(f'M {bx-8} 206 L {bx-16} 132 M {bx+8} 206 L {bx+16} 132', METAL, 1.4))
coil = f'M {bx-16} 132 l 4 -7 l 4 7 l 4 -7 l 4 7 l 4 -7 l 4 7 l 4 -7 l 4 7'
b.append(show(line(coil, HOT, 2.6), ON, D))
b.append(show(line(f'M {bx-16} 132 l 4 -7 l 4 7 l 4 -7 M {bx+4} 132 l 4 -7 l 4 7 l 4 -7 l 4 7', METAL, 1.6) + line(f'M {bx-4} 125 l 3 12', METAL, 1.6), OFF, D))
b.append(f'<path d="{glass}" fill="rgba(236,230,218,0.05)" stroke="{GLASS}" stroke-opacity="0.75" stroke-width="1.6"/>')
b.append(f'<rect x="{bx-20}" y="206" width="40" height="44" rx="4" fill="#2a2621" stroke="{METAL}" stroke-width="1.3"/>')
b.append(line(' '.join(f'M {bx-20} {y} l 40 -5' for y in (220, 230, 240, 250)), METAL, 1.2))
b.append(f'<path d="M {bx-12} 250 h 24 l -5 18 h -14 Z" fill="{METAL}"/>')
b.append(show(waves([(bx-74, 150), (bx+74, 150), (bx-66, 100), (bx+66, 100)]), ON, D))
# --- vacuum tube (7 cm tall)
tx = 222
b.append(f'<rect x="{tx-15}" y="156" width="30" height="74" rx="2" fill="#2e2b26" stroke="{METAL}" stroke-width="1.4"/>')
b.append(line(f'M {tx-22} 152 H {tx+22} M {tx-22} 236 H {tx+22}', METAL, 2))
b.append(line(f'M {tx} 236 V 246 M {tx-8} 236 V 246 M {tx+8} 236 V 246', METAL, 1.2))
b.append(show(f'<ellipse cx="{tx}" cy="194" rx="20" ry="44" fill="{HOT}" opacity="0.22"><animate attributeName="opacity" values="0.18;0.3;0.2;0.28;0.18" dur="1.7s" repeatCount="indefinite"/></ellipse>'
              + line(f'M {tx} 160 V 228', HOT, 3) + line(f'M {tx-15} 236 H {tx+15}', HOT, 2), ON, D))
b.append(show(line(f'M {tx} 160 V 186 M {tx} 200 V 228', METAL, 1.8) + line(f'M {tx} 186 l 5 9', METAL, 1.8), OFF, D))
b.append(f'<path d="M {tx-26} 248 V 146 A 26 26 0 0 1 {tx+26} 146 V 248 Z" fill="rgba(236,230,218,0.05)" stroke="{GLASS}" stroke-opacity="0.75" stroke-width="1.6"/>')
b.append(f'<path d="M {tx-4} 120 l 2 -7 h 4 l 2 7 Z" fill="{METAL}"/>')
b.append(f'<rect x="{tx-30}" y="248" width="60" height="20" rx="3" fill="#2a2621" stroke="{METAL}" stroke-width="1.2"/>')
b.append(show(waves([(tx-38, 196), (tx+38, 196), (tx-40, 150), (tx+40, 150)]), ON, D))
# --- transistor (a 5 mm can on three legs)
qx = 340
b.append(line(f'M {qx-4} 244 V {BASE} M {qx} 244 V {BASE} M {qx+4} 244 V {BASE}', PALE, 1.2))
b.append(f'<rect x="{qx-6}" y="234" width="12" height="10" rx="2" fill="{PALE}"/>')
b.append(f'<rect x="{qx-7}" y="242" width="14" height="3" rx="1" fill="{METAL}"/>')
for x, s in ((bx, 'light bulb'), (tx, 'vacuum tube'), (qx, 'transistor')):
    b.append(text(x, 295, s, 14, GLASS))
put('fig-1-3', '18 44 384 262', [1.5, 4.5], ['glowing', 'burnt out'],
    'Fig 1.3 · The replacement · the same switch, without the fire',
    'Three objects drawn to scale, standing on a centimetre rule. On the left an ordinary light bulb, six centimetres across: a glass globe with a glowing filament, heat rising from it. In the middle a vacuum tube, seven centimetres tall, built the same way: a glass envelope with a heater glowing orange inside and heat rising. On the right a transistor: a metal can half a centimetre across on three thin legs, with nothing glowing. Later the bulb and the tube have both burnt out, dark, their filaments broken; the transistor is unchanged.',
    b,
    caption='Built like a light bulb, a tube runs hot and burns out; a transistor cannot.',
    strip=[('Tube', 'The first tubes were modified light bulbs. A filament, kept hot, boils electrons off; a metal plate draws them across the vacuum; a grid of fine wire between the two, set by a control signal, lets them through or holds them back. That makes it a switch.'),
           ('Transistor', 'The first one was built at Bell Labs in 1947; the one drawn is a 1950s metal can about 5 mm across. It does the tube\'s job in a solid crystal, with no filament, no vacuum and no glass (the next figures open it).'),
           ('The scale', 'All three are drawn to size against the centimetre rule.'),
           ('Why it won', 'A hot filament wears out, as a bulb\'s does: one of ENIAC\'s 17,468 tubes failed about every two days. A transistor has nothing to burn out, and it shrinks.')])
