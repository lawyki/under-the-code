# Fig 10.7 · CUBIC vs Reno: same loss, different recovery (Pass 28, law 3). Chart Room plate. A 1 Gbit/s
# path with a 100 ms round trip and 1,460-byte segments: W_max = 12.5 MB / 1,460 B ≈ 8,600 segments. At t = 0
# both lose. Reno halves to 4,300 and adds one segment per RTT (10 per second): back at W_max after 430 s.
# CUBIC (RFC 9438: beta 0.7, C 0.4) cuts to 6,020 and follows W(t) = C (t - K)^3 + W_max in real time,
# K = cbrt(W_max (1 - beta) / C) ≈ 18.6 s. Both curves draw left to right; t=0 (shift): fully drawn.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

LOSS = '#ec8d8d'
WMAX, BETA, C, RTT = 8600, 0.7, 0.4, 0.1
K = ((WMAX * (1 - BETA)) / C) ** (1 / 3)
assert 18.5 < K < 18.7 and round(WMAX * 0.5 / (1 / RTT)) == 430
cubic = lambda t: C * (t - K) ** 3 + WMAX
reno = lambda t: WMAX / 2 + t / RTT
TMIN, TMAX, VMAX = -2.0, 30.0, 10000
W, H = 400, 262
X0, X1, Y0, Y1 = 56, 384, 214, 34
xt = lambda t: X0 + (t - TMIN) / (TMAX - TMIN) * (X1 - X0)
yv = lambda v: Y0 - v / VMAX * (Y0 - Y1)
D = 9.0
S0, S1 = 0.5, 7.5
T = Timeline(D, shift=8.4)
ts = lambda t: S0 + (t - TMIN) / (TMAX - TMIN) * (S1 - S0)       # story time at which the reveal reaches t
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-34 svgd-part3-34">')
a('<title id="svgt-part3-34">Fig 10.7 · CUBIC vs Reno: same loss, different recovery</title>')
a('<desc id="svgd-part3-34">Congestion window over the 30 seconds after one loss, on a 1 gigabit per second path with a 100 millisecond round trip, where the window that last filled the link, W max, is about 8,600 segments. '
  'Reno halves to 4,300 and adds one segment per round trip, a nearly flat line that would take about 430 seconds to get back. '
  'CUBIC cuts to 0.7 of W max and follows a cubic curve: it rises fast, flattens as it nears W max, reaches it after about 19 seconds, then climbs past it to probe for more.</desc>')
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{CMUTED}"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 4}" stroke="{CMUTED}"/>')
for t in (0, 10, 20, 30):
    a(text(xt(t), Y0 + 20, str(t), anchor='middle', size=13, fill=CMUTED, ls='0'))
a(text(X1, Y0 + 40, 'seconds after the loss', anchor='end', size=13, fill=CMUTED, ls='0'))
a(text(X0 - 8, Y1 - 14, 'window', anchor='start', size=13, fill=CMUTED, ls='0'))
a(text(X0 - 8, yv(0) + 5, '0', anchor='end', size=13, fill=CMUTED, ls='0'))
# W_max: the window that last filled the link
a(f'<line x1="{X0}" y1="{yv(WMAX):.1f}" x2="{X1}" y2="{yv(WMAX):.1f}" stroke="{CSOFT}" stroke-dasharray="5 4"/>')
a(text(X1, yv(WMAX) + 20, 'the last peak', anchor='end', size=13, fill=CSOFT, ls='0'))
# the curves: the shared pre-loss window, then each cut and recovery, revealed left to right
def pts(f):
    p = [(xt(TMIN), yv(WMAX)), (xt(0), yv(WMAX))]
    n = 160
    for i in range(n + 1):
        t = TMAX * i / n
        p.append((xt(t), yv(f(t))))
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in p)
a(f'<defs><clipPath id="clip-fig-10-7"><rect class="fx" x="{X0 - 4}" y="0" width="{X1 - X0 + 8}" height="{H}">'
  f'{T.anim("width", [(0.0, X1 - X0 + 8), (0.3, X1 - X0 + 8), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0 + 8), (D, X1 - X0 + 8)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-10-7)">'
  f'<polyline points="{pts(reno)}" fill="none" stroke="{ROUTE}" stroke-width="2.5" stroke-linejoin="round"/>'
  f'<polyline points="{pts(cubic)}" fill="none" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round"/></g>')
# the loss
a(f'<circle cx="{xt(0):.1f}" cy="{yv(WMAX):.1f}" r="4.5" fill="{LOSS}"/>')
a(text(xt(0), yv(WMAX) - 10, 'loss', anchor='middle', size=13, fill=LOSS, ls='0'))
a(text(xt(0) + 8, yv(BETA * WMAX) + 20, '×0.7', anchor='start', size=13, fill=CYAN, ls='0'))
a(text(xt(0) + 8, yv(WMAX / 2) + 20, '×0.5', anchor='start', size=13, fill=ROUTE, ls='0'))
# curve names
a(text(xt(9), yv(cubic(9)) + 24, 'CUBIC', anchor='start', size=13, fill=CYAN, ls='0'))
a(text(xt(12), yv(reno(12)) - 10, 'Reno: +1 per round trip', anchor='start', size=13, fill=ROUTE, ls='0'))
# back at W_max: CUBIC after K seconds
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
a(f'<g opacity="0">{win(ts(K))}<circle cx="{xt(K):.1f}" cy="{yv(WMAX):.1f}" r="4.5" fill="{CYAN}"/>'
  f'{text(xt(K), yv(WMAX) - 10, "19 s", anchor="middle", size=13, fill=CYAN, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('After one loss, Reno halves its window and adds a segment per round trip; CUBIC cuts to 0.7 and follows a cubic curve in real time, racing back, slowing near the old peak, then probing past it. With a 1 Gbit/s path and a 100 ms round trip, CUBIC recovers in 19 seconds, Reno in seven minutes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The path.</b> 1 Gbit/s × 100 ms = 12.5 MB in flight, about 8,600 segments of 1,460 bytes: the <em>W_max</em> both flows had reached when the loss came.</li>
          <li><b>Reno.</b> Halves to 4,300 and gains one segment per 100 ms round trip: 4,300 round trips, about 430 seconds, to get back.</li>
          <li><b>CUBIC.</b> W(t) = C(t − K)³ + W_max with C = 0.4 and a cut to 0.7 (RFC 9438). K = ∛(W_max × 0.3 / C) ≈ 18.6 s is when it reaches W_max again; growth is set by the clock, not by round trips. Linux's default since kernel 2.6.19 (2006).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-7">
      <div class="diagram-label">Fig 10.7 · CUBIC vs Reno: same loss, different recovery</div>
      {svg}
      <p id="ch10-modern-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(round(K, 2), round(cubic(30)), reno(30))
    splice('part-3', 'fig-10-7', 'ch10-modern-p3', card)
