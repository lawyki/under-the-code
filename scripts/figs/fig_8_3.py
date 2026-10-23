# Fig 8.3 · Entropy of a binary source (Pass 28, law 3). Chart Room paper card. H(p) computed exactly;
# a marker sweeps p from 0 to 1 and back along the curve, a guide line dropping to the axis. The fair
# coin (1 bit) and the 90/10 source (0.47 bits) are marked. t=0 (shift): marker at the 90/10 point.
import math
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f'
def Hb(p):
    return 0.0 if p in (0, 1) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)
assert abs(Hb(0.9) - 0.469) < 0.001 and abs(Hb(0.75) - 0.811) < 0.001
W, H = 400, 270
PX0, PX1, PY0, PY1 = 60, 372, 222, 42          # p 0..1 -> x; H 0..1 -> y
xp = lambda p: PX0 + p * (PX1 - PX0)
yh = lambda h: PY0 - h * (PY0 - PY1)
D = 8.0
S0, S1 = 0.4, 7.6                               # sweep 0 -> 1 -> 0
def p_at(t):
    u = (t - S0) / (S1 - S0)
    return 2 * u if u <= 0.5 else 2 - 2 * u
T_09 = S0 + 0.45 * (S1 - S0)                     # p = 0.9 on the way up
T = Timeline(D, shift=T_09)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-4 svgd-part3-4">')
a('<title id="svgt-part3-4">Fig 8.3 · Entropy of a binary source as p varies</title>')
a('<desc id="svgd-part3-4">The entropy of a binary source, in bits per symbol, plotted against the probability p of a 1. It is 0 at p = 0 and p = 1, where every symbol is predictable, rises to 1 bit for a fair coin at p = 0.5, '
  'and is symmetric about it. A source that gives 1 nine times in ten carries about 0.47 bits per symbol, the least any lossless code can use for it.</desc>')
# axes
a(f'<line x1="{PX0}" y1="{PY0}" x2="{PX1}" y2="{PY0}" stroke="{INK_SOFT}"/>')
a(f'<line x1="{PX0}" y1="{PY0}" x2="{PX0}" y2="{PY1 - 6}" stroke="{INK_SOFT}"/>')
for p in (0, 0.5, 1):
    a(text(xp(p), PY0 + 20, f'{p:g}', anchor='middle', size=13, fill=INK_SOFT, ls='0'))
a(text(PX1, PY0 + 40, 'p, chance of a 1', anchor='end', size=13, fill=INK_SOFT, ls='0'))
for h in (0, 1):
    a(text(PX0 - 8, yh(h) + 5, str(h), anchor='end', size=13, fill=INK_SOFT, ls='0'))
a(text(PX0 - 8, PY1 - 14, 'bits', anchor='start', size=13, fill=INK_SOFT, ls='0'))
# the curve
pts = ' '.join(f'{xp(i / 200):.1f},{yh(Hb(i / 200)):.1f}' for i in range(201))
a(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="2.5"/>')
# marked points
for p, lab, dx, anchor in ((0.5, 'fair coin: 1 bit', 0, 'middle'), (0.9, '90/10: 0.47', -16, 'end')):
    x, y = xp(p), yh(Hb(p))
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{ROUTE_D}"/>')
    a(text(x + dx, y - 12, lab, anchor=anchor, size=13, fill=ROUTE_D, ls='0'))
a(f'<line x1="{xp(0.9):.1f}" y1="{yh(Hb(0.9)):.1f}" x2="{xp(0.9):.1f}" y2="{PY0}" stroke="{ROUTE_D}" stroke-dasharray="3 3"/>')
a(text(xp(0.9), PY0 + 20, '0.9', anchor='middle', size=13, fill=ROUTE_D, ls='0'))
# the moving marker, its x and y following the curve
N = 48
kx, ky = [], []
for i in range(N + 1):
    t = S0 + (S1 - S0) * i / N
    p = p_at(t)
    kx.append((t, xp(p) - xp(0)))
    ky.append((t, yh(Hb(p)) - yh(0)))
kx = [(0.0, 0.0)] + kx + [(D, 0.0)]; ky = [(0.0, 0.0)] + ky + [(D, 0.0)]
a(f'<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle class="fx" cx="{xp(0)}" cy="{yh(0)}" r="7" fill="none" stroke="{INK}" stroke-width="2"/></g>'
  f'<line class="fx" x1="{xp(0)}" y1="{PY0}" x2="{xp(0)}" y2="{PY0 - 8}" stroke="{INK}" stroke-width="2"/></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Entropy of a two-symbol source against p, the chance of a 1: 0 when every symbol is predictable, 1 bit for the fair coin, symmetric about it. A 90/10 source is marked at 0.47 bits, the least any lossless code can average for it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The formula.</b> H(p) = −p log₂ p − (1 − p) log₂(1 − p): the average surprise, in bits, of one symbol.</li>
          <li><b>Symmetry.</b> A 30/70 source is exactly as uncertain as a 70/30 one; the curve does not care which side is likelier.</li>
          <li><b>Reaching the floor.</b> Arithmetic coding comes within a few percent of H for long messages; coding bit by bit cannot go below 1 bit per symbol.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-8-3">
      <div class="diagram-label">Fig 8.3 · Entropy of a binary source as p varies</div>
      {svg}
      <p id="ch8-shannon-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-3', 'ch8-shannon-p7', card)
