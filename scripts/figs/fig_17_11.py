# Fig 17.11 · The architectural pendulum · same problems, different costumes (Pass 28, law 3). Quorum glass plate. A
# horizontal axis from "one deployable" to "many": eras sit on it as their typical granularity, and a pendulum bob swings
# out from the monolith (1990s) through SOA (~2005), microservices (~2014) and serverless functions (~2018), then back
# towards a modular monolith (2020s; Amazon Prime Video's 2023 write-up consolidating one monitoring service and
# cutting its cost by over 90%). Each era lights as the bob reaches it. t=0 (shift): the bob on its way back.
import math
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
PIV = (200, 26)
L = 150
ERAS = [(-50, '1990s', 'monolith', QSOFT), (-20, '~2005', 'SOA', VIOLET), (12, '~2014', 'microservices', TEAL),
        (42, '~2018', 'serverless', QAMBER), (-30, '2020s', 'modular monolith', QROSE)]
bob = lambda deg: (PIV[0] + L * math.sin(math.radians(deg)), PIV[1] + L * math.cos(math.radians(deg)))
D = 12.0
T = Timeline(D, shift=11.2)
TS = [0.8, 2.6, 4.4, 6.2, 9.0]
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# the arc and its two poles
arc = ' '.join(f'{bob(d)[0]:.1f},{bob(d)[1]:.1f}' for d in range(-56, 57, 2))
a(f'<polyline points="{arc}" fill="none" stroke="{QMUTED}" stroke-opacity="0.35" stroke-dasharray="3 4"/>')
lx, ly = bob(-56); rx, ry = bob(56)
a(text(10, PIV[1] + L + 28, '← one deployable', anchor='start', size=13, fill=QMUTED, ls='0'))
a(text(390, PIV[1] + L + 28, 'many →', anchor='end', size=13, fill=QMUTED, ls='0'))
a(f'<circle cx="{PIV[0]}" cy="{PIV[1]}" r="4" fill="{QMUTED}"/>')
# era markers on the arc, labels in a list below
for k, (deg, yr, name, col) in enumerate(ERAS):
    x, y = bob(deg)
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="none" stroke="{col}" stroke-width="2"/>')
    a(text(x, y - 13, str(k + 1), anchor='middle', size=13, fill=col, ls='0'))
LY0 = PIV[1] + L + 54
for k, (deg, yr, name, col) in enumerate(ERAS):
    y = LY0 + k * 20
    body = text(10, y, f'{k + 1}  {yr}', anchor='start', size=13, fill=col, ls='0') + text(110, y, name, anchor='start', size=13, fill=QSOFT, ls='0')
    a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(TS[k])}{body}</g>')
# the rod and bob: rotate about the pivot, stepping era to era
angs = [d for d, *_ in ERAS]
pts = [(0.0, angs[-1] + 8), (0.3, angs[-1] + 8), (0.305, angs[0])]
for k in range(len(ERAS)):
    if k:
        pts += [(TS[k] - 1.0, angs[k - 1]), (TS[k], angs[k])]
pts += [(D - 0.6, angs[-1]), (D, angs[-1] + 8)]
ts_ = sorted(set([0.0, D] + [T.t(t) for t, _ in pts]))
def at(tau):
    seq = sorted(((T.t(t), v) for t, v in pts))
    seq = [(seq[-1][0] - D, seq[-1][1])] + seq + [(seq[0][0] + D, seq[0][1])]
    for p, q in zip(seq, seq[1:]):
        if p[0] <= tau <= q[0]:
            return p[1] if q[0] == p[0] else p[1] + (tau - p[0]) / (q[0] - p[0]) * (q[1] - p[1])
vals = ';'.join(f'{-at(t):.2f} {PIV[0]} {PIV[1]}' for t in ts_)
kts = ';'.join(f'{t / D:.6f}' for t in ts_)
rot = f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{kts}" dur="{D:g}s" repeatCount="indefinite"/>'
bx, by = PIV[0], PIV[1] + L
a(f'<g class="fx">{rot}<line x1="{PIV[0]}" y1="{PIV[1]}" x2="{bx}" y2="{by}" stroke="{QSOFT}" stroke-opacity="0.6" stroke-width="1.5"/><circle cx="{bx}" cy="{by}" r="6" fill="#fff"/></g>')
H = LY0 + 4 * 20 + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-24 svgd-part5-24">')
o.insert(1, '<title id="svgt-part5-24">Fig 17.11 · The architectural pendulum · same problems, different costumes</title>')
o.insert(2, '<desc id="svgd-part5-24">A pendulum swinging between one deployable unit and many. It starts at the monolith of the 1990s, swings out through service-oriented architecture around 2005, microservices around 2014 and serverless functions around 2018, then back toward the modular monolith of the 2020s.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each generation split systems into smaller deployable pieces, from monoliths through SOA and microservices to single functions, until the cost of all that distribution pushed some teams back towards fewer, well-divided programs. '
           'The trade between independence and simplicity never went away; only its costume changed.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it swings out.</b> Smaller pieces let teams deploy and scale independently; the cost is everything Fig 17.9 shows, paid on every call.</li>
          <li><b>Why it swings back.</b> In 2023 Amazon Prime Video described folding one monitoring service from serverless functions into a single process and cutting its infrastructure cost by over 90%.</li>
          <li><b>The modular monolith.</b> One deployable, with module boundaries kept as strictly as service boundaries, so it can be split later if a team really needs to.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-11">
      <div class="diagram-label">Fig 17.11 · The architectural pendulum · same problems, different costumes</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-11"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-11', cap, card.replace('CAPID', cap))
