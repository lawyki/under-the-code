"""Fig 1.4: a transistor is a switch flipped by electricity instead of a finger.
Two identical lamp loops. Left: a finger closes a lever. Right: a small signal makes the transistor conduct."""
from plate import *
D = 6.0
ON = [(3.0, 5.7)]
K = [0, 0.45, 0.5, 0.95, 1.0]           # off, off, on, on, off

def loop(x0, kind):
    x1, xm = x0 + 120, x0 + 60
    yt, yb = 78, 196
    b = []
    # wires (the switch gap is at x1, y 116..156)
    b.append(line(f'M {xm-29} {yb} H {x0} V {yt} H {xm-6} M {xm+6} {yt} H {x1} V 116'))
    b.append(line(f'M {x1} 156 V {yb} H {xm+22}'))
    # current, drawn under the parts: gold dashes running clockwise from the battery's +
    flow = (f'<path d="M {xm-30} {yb} H {x0} V {yt} H {x1} V {yb} H {xm+24}" fill="none" stroke="{GOLD}" stroke-width="4" '
            f'stroke-dasharray="8 10" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" values="18;0" dur="0.7s" repeatCount="indefinite"/></path>')
    b.append(show(flow, ON, D))
    # battery
    b.append(f'<rect x="{xm-24}" y="{yb-10}" width="46" height="20" rx="3" fill="none" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<rect x="{xm-29}" y="{yb-5}" width="5" height="10" rx="1" fill="{INK}"/>')
    b.append(text(xm - 12, yb + 5, '+', 14, INK))
    b.append(text(xm + 11, yb + 4, '−', 14, MUTE))
    # lamp: a bulb standing on the wire
    b.append(f'<rect x="{xm-6}" y="{yt-12}" width="12" height="13" rx="2" fill="none" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<circle cx="{xm}" cy="{yt-26}" r="16" fill="none" stroke="{INK}" stroke-width="2"/>')
    b.append(line(f'M {xm-5} {yt-13} V {yt-22} l 2.5 -5 l 2.5 5 l 2.5 -5 l 2.5 5 V {yt-13}', INK, 1.4))
    rays = ''.join(line(f'M {xm+dx*21:.1f} {yt-26+dy*21:.1f} L {xm+dx*28:.1f} {yt-26+dy*28:.1f}', GOLD, 2)
                   for dx, dy in [(-0.94, -0.34), (-0.6, -0.8), (0, -1), (0.6, -0.8), (0.94, -0.34)])
    glow = (f'<circle cx="{xm}" cy="{yt-26}" r="16" fill="{GOLD}" fill-opacity="0.55" stroke="{GOLD}" stroke-width="2"/>'
            + line(f'M {xm-5} {yt-13} V {yt-22} l 2.5 -5 l 2.5 5 l 2.5 -5 l 2.5 5 V {yt-13}', '#fff', 1.6) + rays)
    b.append(show(glow, ON, D))
    if kind == 'finger':
        b.append(f'<circle cx="{x1}" cy="116" r="3.2" fill="{INK}"/>')
        lever = line(f'M {x1} 156 V 116', INK, 3)
        b.append(f'<g>{xform("rotate", [f"30 {x1} 156", f"30 {x1} 156", f"0 {x1} 156", f"0 {x1} 156", f"30 {x1} 156"], K, D)}{lever}</g>')
        b.append(f'<circle cx="{x1}" cy="156" r="3.2" fill="{INK}"/>')
        fy = 136; tx = x1 + 14
        finger = (f'<path d="M {tx+46} {fy-10} H {tx+10} A 10 10 0 0 0 {tx+10} {fy+10} H {tx+46}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
                  f'<path d="M {tx+3} {fy-6} h 9 q 4 0 4 -4" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
                  f'<path d="M {tx+30} {fy-10} q 3 4 0 7 M {tx+36} {fy-10} q 3 4 0 7" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linecap="round" stroke-opacity="0.7"/>')
        b.append(f'<g>{xform("translate", ["0 0", "0 0", "-11 0", "-11 0", "0 0"], K, D)}{finger}</g>')
    else:
        cx = x1 + 12
        b.append(f'<circle cx="{x1+6}" cy="136" r="25" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        b.append(line(f'M {cx} 122 V 150', INK, 3.2))
        b.append(line(f'M {cx} 130 L {x1} 116'))
        b.append(line(f'M {cx} 142 L {x1} 156'))
        b.append(f'<path d="M {x1} 156 l 10.5 -3 l -5 -7.5 Z" fill="{INK}"/>')
        on = (line(f'M {cx} 130 L {x1} 116', GOLD, 3) + line(f'M {cx} 142 L {x1} 156', GOLD, 3)
              + f'<path d="M {x1} 156 l 10.5 -3 l -5 -7.5 Z" fill="{GOLD}"/>' + line(f'M {cx} 122 V 150', GOLD, 3.2))
        b.append(show(on, ON, D))
        b.append(line(f'M {cx} 136 H {x1+48}'))
        sig = (f'<path d="M {x1+84} 136 H {x1+50}" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-dasharray="4 4" stroke-linecap="round">'
               f'<animate attributeName="stroke-dashoffset" values="0;8" dur="0.7s" repeatCount="indefinite"/></path>'
               f'<path d="M {x1+48} 136 l 9 -5.5 v 11 Z" fill="{GOLD}"/>')
        b.append(show(sig, ON, D))
        b.append(text(x1 + 64, 122, 'signal', 14, MUTE))
        b.append(text(x1 + 60, 158, 'base', 14, MUTE))
        b.append(text(x1 - 14, 112, 'collector', 14, MUTE, 'end'))
        b.append(text(x1 - 14, 168, 'emitter', 14, MUTE, 'end'))
    return b

body = loop(26, 'finger') + loop(214, 'signal')
put('fig-1-4', '16 22 412 204', [1.5, 4.5], ['off', 'on'],
    'Fig 1.4 · Transistor as a switch',
    'Two identical circuits side by side, each a battery, a lamp and a switch in one loop. On the left the switch is a lever and a finger pushes it shut: current runs round the loop and the lamp lights. On the right the lever is replaced by a transistor and the finger by a small electrical signal arriving at the transistor\'s base: the transistor conducts from collector to emitter, the same current runs round the loop and the lamp lights. With no finger and no signal, both lamps are dark.',
    body,
    caption='The same lamp circuit twice: a finger closes one switch, a small signal closes the other.',
    strip=[('Three terminals', 'The large current runs from the collector to the emitter (the one with the arrow); the base controls it.'),
           ('The threshold', 'In this kind of transistor about 0.7 V on the base opens the path; below it, almost nothing flows.'),
           ('Small controls large', 'The signal into the base is tiny beside the current it lets through, so one transistor\'s output can be the signal for many others.'),
           ('The direction', 'The dashes run the conventional way, out of the battery\'s + and back to its other end; the electrons that carry the current drift the other way.'),
           ('The other kind', 'This is the older kind of transistor. Modern chips are built from the field-effect kind, whose control terminal is called the gate (Fig 1.5).')])
