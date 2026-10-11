# Fig 14.9 · Point addition on an elliptic curve · geometric picture (Pass 28, law 3). Strongroom dossier plate. The
# real curve y² = x³ − 3x + 5 (one branch), P = (−2, √3), Q = (0, √5). The line through them meets the curve a third
# time at R′ = (λ² + 2, …), computed here; reflected across the x-axis it is P + Q. Lock-step: P, Q, the line drawn,
# R′, the reflection, P + Q. t=0 (shift): the construction complete.
import math
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

A, B = -3, 5
f = lambda x: x ** 3 + A * x + B
P = (-2.0, math.sqrt(f(-2.0)))
Q = (0.0, math.sqrt(f(0.0)))
lam = (Q[1] - P[1]) / (Q[0] - P[0])
x3 = lam ** 2 - P[0] - Q[0]
yR = P[1] + lam * (x3 - P[0])
R1 = (x3, yR)                                     # the third intersection
S = (x3, -yR)                                     # P + Q
assert abs(yR ** 2 - f(x3)) < 1e-9 and abs(x3 - 2.0635) < 1e-3
# the curve's real root (left end of the branch)
lo, hi = -3.0, -2.0
for _ in range(60):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if f(m) < 0 else (lo, m)
X0R = hi
W = 400
XMIN, XMAX, YMAX = -2.6, 3.0, 4.2
PX0, PX1, PY0, PY1 = 24, 384, 40, 296
sx = lambda x: PX0 + (x - XMIN) / (XMAX - XMIN) * (PX1 - PX0)
sy = lambda y: (PY0 + PY1) / 2 - y / YMAX * (PY1 - PY0) / 2
D = 11.0
T = Timeline(D, shift=10.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
TP, TQ, TL0, TL1, TR, TF, TS = 0.8, 1.6, 2.4, 3.6, 3.8, 4.8, 5.8
o = []; a = o.append
a(text(PX0, 20, 'y² = x³ − 3x + 5', anchor='start', size=13, fill=PSOFT, ls='0'))
# axes
a(f'<line x1="{PX0}" y1="{sy(0):.1f}" x2="{PX1}" y2="{sy(0):.1f}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
a(f'<line x1="{sx(0):.1f}" y1="{PY0}" x2="{sx(0):.1f}" y2="{PY1}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
# the curve: upper half, then lower half back, one closed branch
xs = [X0R + (XMAX - X0R) * (i / 200) ** 2 for i in range(201)]
up = [(sx(x), sy(math.sqrt(max(f(x), 0)))) for x in xs if math.sqrt(max(f(x), 0)) <= YMAX]
dn = [(sx(x), sy(-math.sqrt(max(f(x), 0)))) for x in reversed(xs) if math.sqrt(max(f(x), 0)) <= YMAX]
a(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in dn + up)}" fill="none" stroke="{BRASS}" stroke-width="2"/>')
# the line through P and Q, extended past R′, drawn in
lx0, lx1 = P[0] - 0.4, x3 + 0.35
L = f'<line x1="{sx(lx0):.1f}" y1="{sy(P[1] + lam * (lx0 - P[0])):.1f}" x2="{sx(lx1):.1f}" y2="{sy(P[1] + lam * (lx1 - P[0])):.1f}" stroke="{SEAL}" stroke-width="1.5"/>'
a(f'<defs><clipPath id="clip-fig-14-9"><rect class="fx" x="{PX0}" y="0" width="{PX1 - PX0}" height="400">'
  f'{T.anim("width", [(0.0, PX1 - PX0), (0.3, PX1 - PX0), (0.305, 0.0), (TL0, 0.0), (TL1, PX1 - PX0), (D, PX1 - PX0)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-14-9)">{L}</g>')
# the reflection
a(f'<g opacity="0">{win(TF)}<line x1="{sx(x3):.1f}" y1="{sy(yR) + 6:.1f}" x2="{sx(x3):.1f}" y2="{sy(-yR) - 6:.1f}" stroke="{PMUTED}" stroke-dasharray="4 3"/></g>')
def point(pt, lab, col, t0, dx, dy, anchor='start'):
    x, y = sx(pt[0]), sy(pt[1])
    body = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{col}"/>' + text(x + dx, y + dy, lab, anchor=anchor, size=13, fill=col, ls='0')
    a(f'<g opacity="0">{win(t0)}{body}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t0)}<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
point(P, 'P', PARCH, TP, -12, -10, 'end')
point(Q, 'Q', PARCH, TQ, -12, -10, 'end')
point(R1, 'R′', SEAL, TR, -14, -12, 'end')
point(S, 'P + Q', SAGE, TS, -14, 22, 'end')
H = PY1 + 10
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-22 svgd-part4-22">')
o.insert(1, '<title id="svgt-part4-22">Fig 14.9 · Point addition on an elliptic curve · geometric picture</title>')
o.insert(2, '<desc id="svgd-part4-22">The curve y squared equals x cubed minus 3x plus 5, one smooth branch. P is at x = −2 and Q at x = 0, both above the axis. '
  'The straight line through them meets the curve a third time at R prime, near x = 2.06, y = 2.76. Reflecting R prime across the x-axis gives the point P + Q, at x = 2.06, y = −2.76.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('To add two points on the curve, draw the line through them, find where it meets the curve a third time, and reflect that point across the x-axis. '
           'Adding a point to itself k times is fast, but recovering k from the result is the elliptic-curve discrete log, the trapdoor ECC rests on.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The numbers.</b> On y² = x³ − 3x + 5, P = (−2, 1.73) and Q = (0, 2.24); the line through them meets the curve again at (2.06, 2.76), so P + Q = (2.06, −2.76).</li>
          <li><b>A real group.</b> The addition is commutative and associative, with a "point at infinity" as zero. Cryptography uses the same rules over a finite field instead of the real numbers, where the curve is a scatter of points, not a line.</li>
          <li><b>In use.</b> Curve25519 (X25519, Ed25519) and secp256k1 (Bitcoin) work over prime fields of about 256 bits; a 256-bit key gives about 128 bits of security.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-9">
      <div class="diagram-label">Fig 14.9 · Point addition on an elliptic curve · geometric picture</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    print(P, Q, R1, S)
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-9"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-9', cap, card.replace('CAPID', cap))
