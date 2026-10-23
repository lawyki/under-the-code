# Fig 10.5 · The TCP sawtooth (Pass 28, law 3). Chart Room paper card. Reno simulated, capacity 24
# segments: slow start doubles from 1; the first loss halves the window; then +1 per RTT, halving at
# every loss, a sawtooth between 12 and 25. The curve is drawn RTT by RTT. t=0 (shift): fully drawn.
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D, GREEN, RED = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f', '#2e7e4f', '#b3261e'
CAP, RTTS = 24, 40
cw, ssthresh, ss = 1, None, True
SER, LOSS = [], []
for r in range(RTTS + 1):
    SER.append(cw)
    if cw > CAP:
        LOSS.append(r); cw = cw // 2; ssthresh = cw; ss = False
    elif ss and (ssthresh is None or cw < ssthresh): cw *= 2
    else: cw += 1; ss = False
assert SER[:6] == [1, 2, 4, 8, 16, 32] and LOSS[0] == 5 and min(SER[6:]) == 12 and max(SER[7:]) == 25
W, H = 400, 270
X0, X1, Y0, Y1 = 46, 384, 210, 30
xr = lambda r: X0 + r / RTTS * (X1 - X0)
yc = lambda c: Y0 - c / 32 * (Y0 - Y1)
D = 9.0
S0, S1 = 0.4, 7.6
T = Timeline(D, shift=8.4)
tr = lambda r: S0 + r / RTTS * (S1 - S0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-32 svgd-part3-32">')
a('<title id="svgt-part3-32">Fig 10.5 · The TCP sawtooth</title>')
a('<desc id="svgd-part3-32">TCP\'s congestion window, in segments, over 40 round trips, on a path that can carry 24. Slow start doubles it each round trip, 1, 2, 4, 8, 16, 32, until the first loss halves it to 16. '
  'From then on it grows by one segment per round trip and halves at each loss, a sawtooth between about 12 and 25 around the capacity, which TCP never learns directly.</desc>')
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{INK_SOFT}"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 6}" stroke="{INK_SOFT}"/>')
for c in (0, 12, 24):
    a(text(X0 - 8, yc(c) + 5, str(c), anchor='end', size=13, fill=INK_SOFT, ls='0'))
a(f'<line x1="{X0}" y1="{yc(CAP)}" x2="{X1}" y2="{yc(CAP)}" stroke="{ACC}" stroke-dasharray="5 4"/>')
a(text(X1, yc(CAP) - 6, 'capacity', anchor='end', size=13, fill=ACC, ls='0'))
for r in (0, 20, 40):
    a(text(xr(r), Y0 + 20, str(r), anchor='middle', size=13, fill=INK_SOFT, ls='0'))
a(text(X1, Y0 + 40, 'round trips', anchor='end', size=13, fill=INK_SOFT, ls='0'))
a(text(X0 - 8, Y1 - 14, 'window', anchor='start', size=13, fill=INK_SOFT, ls='0'))
# the curve: a step per RTT, revealed with stroke-dashoffset
pts = []
for r, c in enumerate(SER):
    pts.append((xr(r), yc(c)))
a(f'<defs><clipPath id="clip-fig-10-5"><rect class="fx" x="{X0 - 4}" y="0" width="{X1 - X0 + 8}" height="{H}">'
  f'{T.anim("width", [(0.0, X1 - X0 + 8), (0.3, X1 - X0 + 8), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0 + 8), (D, X1 - X0 + 8)])}</rect></clipPath></defs>')
a(f'<polyline clip-path="url(#clip-fig-10-5)" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{ROUTE_D}" stroke-width="2.5"/>')
# loss marks appear when reached
for r in LOSS:
    a(f'<g opacity="0">{T.anim("opacity", [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (tr(r) - 0.002, 0.0), (tr(r), 1.0), (D, 1.0)])}'
      f'<circle cx="{xr(r):.1f}" cy="{yc(SER[r]):.1f}" r="4" fill="{RED}"/></g>')
a(text(xr(6.5), yc(30), 'slow start: ×2', size=13, fill=GREEN, ls='0'))
a(text(xr(10), yc(7), '+1 per RTT, halve on loss', size=13, fill=ROUTE_D, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('On a path that carries 24 segments, slow start overshoots to 32 before the first loss halves the window; from then on it saws between about 12 and 25. TCP never measures the capacity: it finds the limit by overshooting it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rule.</b> Additive increase, multiplicative decrease: AIMD. Classic Reno halves on a loss signalled by repeated ACKs and falls back to one segment on a timeout.</li>
          <li><b>The signal.</b> Here loss is the only signal; ECN lets routers mark packets instead of dropping them, and BBR (Fig 10.8) watches delay as well.</li>
          <li><b>This run.</b> Capacity 24 segments: the window settles into a cycle between 12 and 25.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-10-5">
      <div class="diagram-label">Fig 10.5 · The TCP sawtooth</div>
      {svg}
      <p id="ch10-aimd-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(SER, LOSS)
    splice('part-3', 'fig-10-5', 'ch10-aimd-p7', card)
