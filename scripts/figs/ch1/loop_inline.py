"""The instruction cycle as a small running loop set in the text of section 04 (owner, 2026-11-12: "at least
somewhere having the loop running ... embedded to the paper"). Not a figure card and not interactive: four stations
on a track, a dot going round, the station it has reached lit. Drawn in the page's ink, on the paper."""
import re
from plate import PAGE, kt
D = 3.6
INK = '#1a1614'; DIM = '#5f5a55'; GOLD = '#8a6a2a'
track = 'M 85 30 H 200 A 20 20 0 0 1 200 70 H 60 A 20 20 0 0 1 60 30 Z'
stations = [('fetch', 85, 30, 17, 0.0), ('decode', 175, 30, 17, 90 / 405.66), ('execute', 175, 70, 93, 202.83 / 405.66), ('writeback', 85, 70, 93, 292.83 / 405.66)]
o = [f'<path d="{track}" fill="none" stroke="{INK}" stroke-opacity="0.4" stroke-width="1.6"/>']
# direction: one chevron on each straight
o.append(f'<path d="M 127 25.5 l 6 4.5 l -6 4.5 M 133 65.5 l -6 4.5 l 6 4.5" fill="none" stroke="{INK}" stroke-opacity="0.55" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
for i, (name, x, y, ty, t) in enumerate(stations):
    # the word is lit while the dot is nearer to its station than to any other
    prev = stations[i - 1][4] if i else stations[3][4] - 1
    nxt = stations[i + 1][4] if i < 3 else 1.0
    lo, hi = (prev + t) / 2, (t + nxt) / 2
    def a(attr, on, off):
        if lo < 0: vs, ks = [on, off, on], [0, hi, 1 + lo]
        else: vs, ks = [off, on, off], [0, lo, hi]
        return f'<animate attributeName="{attr}" values="{";".join(vs)}" keyTimes="{kt(ks)}" calcMode="discrete" dur="{D}s" repeatCount="indefinite"/>'
    first = t == 0
    o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#f5f0eb" stroke="{INK}" stroke-opacity="0.7" stroke-width="1.6"/>')
    o.append(f'<text x="{x}" y="{ty}" text-anchor="middle" font-family="DM Mono" font-size="13" fill="{INK if first else DIM}">{name}{a("fill", INK, DIM)}</text>')
    o.append(f'<path d="M {x-len(name)*3.9:.1f} {ty+4} h {len(name)*7.8:.1f}" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" opacity="{1 if first else 0}">{a("opacity", "1", "0")}</path>')
o.append(f'<circle r="5.5" fill="{GOLD}"><animateMotion path="{track}" dur="{D}s" repeatCount="indefinite" calcMode="linear"/></circle>')
svg = ('<div class="text-loop">\n      <svg viewBox="26 2 208 98" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The loop: fetch, decode, execute, writeback, then fetch again.">\n'
       + '\n'.join(o) + '\n</svg>\n    </div>')
s = open(PAGE).read()
old = re.search(r'\n\n    <div class="text-loop">[\s\S]*?</div>', s)
if old: s = s[:old.start()] + s[old.end():]
m = re.compile(r'<p id="ch1-cpu-p1"[\s\S]*?</p>').search(s)
s = s[:m.end()] + '\n\n    ' + svg + s[m.end():]
open(PAGE, 'w').write(s); print('loop in', len(svg))
