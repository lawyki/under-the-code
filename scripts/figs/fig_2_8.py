# Fig 2.8 · The two's-complement wheel (Pass 28, law 3). 256 slots at their true angles:
# value v sits at v/256 of a turn clockwise from the top (negatives at 256 + v). The pointer
# steps +1: across the bottom seam +127 + 1 = −128 (overflow), across the top −1 + 1 = 0 (the
# dropped carry that makes subtraction work). t=0: just past the seam, at −128.
import math
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 440
C, R = (200, 196), 124
ang = lambda v: (v % 256) / 256 * 360            # degrees clockwise from the top
def pt(v, r):
    t = math.radians(ang(v) - 90)
    return C[0] + r * math.cos(t), C[1] + r * math.sin(t)
bits = lambda v: format(v % 256, '08b')
STEPS = [125, 126, 127, -128, -127, -2, -1, 0, 1]
ST = 0.85
tau_of = lambda i: 0.3 + i * ST
T = Timeline(tau_of(len(STEPS)) + 0.6, shift=tau_of(3) + 0.5)
D = T.dur
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-24 svgd-part1-24">')
a("<title id=\"svgt-part1-24\">Fig 2.8 · The two's-complement wheel · where addition wraps</title>")
a('<desc id="svgd-part1-24">The 256 values of a signed 8-bit number around a dial: 0 at the top, positives clockwise down the right to +127, '
  'negatives up the left from −128 to −1, so +127 and −128 meet at the bottom. Adding 1 turns the pointer one notch clockwise: '
  'from +127 it lands on −128, a silent overflow; from −1 it lands on 0, the dropped carry that makes subtraction by addition work.</desc>')
# the dial: positive half gold, negative half red
def arc(v0, v1, col):
    x0, y0 = pt(v0, R); x1, y1 = pt(v1, R)
    a(f'<path d="M {x0:.1f} {y0:.1f} A {R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="10" stroke-opacity="0.55"/>')
arc(0, 127.5, GOLD); arc(128, 255.5, RED)
for v in range(0, 256, 16):
    x0, y0 = pt(v, R - 9); x1, y1 = pt(v, R + 9)
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="rgba(255,255,255,0.35)" stroke-width="1.2"/>')
# the seam at the bottom, and the top where −1 meets 0
sx, sy = pt(127.5, R)
a(f'<line x1="{sx:.1f}" y1="{sy - 18:.1f}" x2="{sx:.1f}" y2="{sy + 18:.1f}" stroke="{RED}" stroke-width="3"/>')
# key labels outside the dial
for v, lab, dx, anchor, col in ((0, '0', 8, 'start', '#fff'), (-1, '−1', -8, 'end', RED), (64, '+64', 14, 'start', GOLD),
                                (-64, '−64', -14, 'end', RED), (127, '+127', 10, 'start', GOLD), (-128, '−128', -10, 'end', RED)):
    x, y = pt(v, R + 26)
    if v in (0, -1): y -= 4
    if v in (127, -128): y += 6
    a(text(x + dx, y + 5, lab, anchor=anchor, size=15, fill=col, ls='0'))
# the pointer: a hand from the centre, stepping one notch per +1
pts = []
for i, v in enumerate(STEPS):
    t0 = tau_of(i)
    th = ang(v)
    if i: th_prev = pts[-1][1]; th = th if th >= th_prev - 1e-9 else th + 360 * math.ceil((th_prev - th) / 360)
    pts.append((t0, th)); pts.append((t0 + ST * 0.7, th))
pts = [(0.0, pts[0][1])] + pts + [(D - 0.001, pts[-1][1])]
ev = sorted(((T.t(t), v) for t, v in pts if t < D - 1e-9), key=lambda p: p[0])
# unwrap across the loop seam so SMIL never spins backwards a whole turn
ts = sorted(set([0.0, D] + [p[0] for p in ev]))
def val(t):
    seq = [(ev[-1][0] - D, ev[-1][1])] + ev + [(ev[0][0] + D, ev[0][1])]
    for p, q in zip(seq, seq[1:]):
        if p[0] <= t <= q[0]:
            return p[1] if q[0] == p[0] else p[1] + (t - p[0]) / (q[0] - p[0]) * (q[1] - p[1])
    return ev[-1][1]
vs = [val(t) for t in ts]
a(f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{v:.2f} {C[0]} {C[1]}" for v in vs)}" '
  f'keyTimes="{";".join(f"{t / D:.4f}" for t in ts)}" dur="{D:g}s" repeatCount="indefinite"/>'
  f'<line x1="{C[0]}" y1="{C[1]}" x2="{C[0]}" y2="{C[1] - R + 16}" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
  f'<circle cx="{C[0]}" cy="{C[1] - R + 12}" r="6" fill="#fff"/></g>')
a(f'<circle cx="{C[0]}" cy="{C[1]}" r="52" fill="#121212" stroke="rgba(255,255,255,0.15)"/>')
# the readout in the middle: the value and its bits
for i, v in enumerate(STEPS):
    t0 = tau_of(i); t1 = tau_of(i + 1) if i + 1 < len(STEPS) else D - 0.0005
    op = T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D - 0.0005, 0.0)]) if i else \
         T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D - 0.0005, 0.0)])
    col = GOLD if v >= 0 else RED
    a(f'<g opacity="0">{op}<text x="{C[0]}" y="{C[1] + 6}" text-anchor="middle" {MONO} font-size="26" fill="{col}">{v:+d}</text>'
      f'<text x="{C[0]}" y="{C[1] + 28}" text-anchor="middle" {MONO} font-size="13" fill="rgba(255,255,255,0.6)">{bits(v)}</text></g>')
# what each crossing means
msgs = [(3, '+127 + 1 = −128', 'overflow: a silent wrap', RED), (7, '−1 + 1 = 0', 'the carry is dropped: correct', GOLD)]
for i, l1, l2, col in msgs:
    t0, t1 = tau_of(i), tau_of(i) + 2 * ST
    op = T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D - 0.0005, 0.0)])
    a(f'<g opacity="0">{op}<text x="200" y="398" text-anchor="middle" {MONO} font-size="18" fill="{col}">{l1}</text>'
      f'<text x="200" y="422" text-anchor="middle" {MONO} font-size="14" fill="rgba(255,255,255,0.7)">{l2}</text></g>')
a(text(20, 24, 'SIGNED 8-BIT · +1 TURNS ONE NOTCH', size=13, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('The 256 values of a signed byte sit on a wheel, not a line: adding 1 turns the pointer one notch. '
           'At the bottom +127 + 1 silently becomes −128; at the top −1 + 1 becomes 0, the same wrap that makes subtraction free in Fig 2.7.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The slots.</b> 0 at the top, positives clockwise to +127, negatives counter-clockwise from −1 to −128. There is one more negative than positive because 0 takes a "positive" slot.</li>
          <li><b>The seam.</b> 01111111 + 1 = 10000000: the top bit flips, and a top bit of 1 means negative. Nothing in the hardware complains.</li>
          <li><b>Every width.</b> 32- and 64-bit integers have the same wheel, with about 4 billion and 18 quintillion slots.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-8">
      <div class="diagram-label">Fig 2.8 · The two's-complement wheel · where addition wraps</div>
      {svg}
      <p id="ch2-twos-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-8', 'ch2-twos-p9', card)
