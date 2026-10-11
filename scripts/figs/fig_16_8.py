# Fig 16.8 · Amdahl's law · the ceiling that won't move (Pass 28, law 3). Quorum glass plate. One job, 5% of it
# serial (p = 0.95). N steps 1, 2, 4, … 1024: the job's time bar keeps its serial 5% while the parallel 95% shrinks
# as 95/N, so the bar approaches the serial floor; below, S(N) = 1 / ((1 − p) + p/N) is drawn and a dot climbs it
# towards the ceiling of 20. Steps are discrete, phase-synced. t=0 (shift): N = 1024, S = 19.6.
import math
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

P = 0.95
S = lambda n: 1 / ((1 - P) + P / n)
NS = [2 ** k for k in range(11)]
assert abs(S(1024) - 19.64) < 0.01 and abs(S(8) - 5.93) < 0.01 and round(1 / (1 - P)) == 20
W = 400
D = 11.0
T = Timeline(D, shift=10.4)
TS = [0.8 + 0.8 * k for k in range(len(NS))]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# the time bar
BX, BW = 20, 360
a(text(BX, 18, 'time for one job, 5% serial', anchor='start', size=13, fill=QSOFT, ls='0'))
SW = (1 - P) * BW
a(f'<rect x="{BX}" y="28" width="{SW:.1f}" height="22" rx="3" fill="{QROSE}" fill-opacity="0.9"/>')
a(f'<rect x="{BX}" y="28" width="{BW}" height="22" rx="3" fill="none" stroke="{QMUTED}" stroke-opacity="0.35" stroke-dasharray="3 3"/>')
for k, n in enumerate(NS):
    t0, t1 = TS[k], (TS[k + 1] if k + 1 < len(NS) else None)
    pw = P / n * BW
    body = f'<rect x="{BX + SW:.1f}" y="28" width="{pw:.1f}" height="22" rx="3" fill="{TEAL}" fill-opacity="0.85"/>'
    lab = text(BX, 72, f'N = {n} cores · speedup {S(n):.1f}×', anchor='start', size=13, fill=TEAL, ls='0')
    vis = win(t0) if t1 is None else lit(t0, t1)
    if k == 0:
        vis = T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
    a(f'<g opacity="0">{vis}{body}{lab}</g>')
a(text(BX, 92, 'serial', anchor='start', size=13, fill=QROSE, ls='0'))
a(text(BX + BW, 92, 'parallel part shrinks as 95/N', anchor='end', size=13, fill=TEAL, ls='0'))
# the curve
PX0, PX1, PY0, PY1 = 46, 384, 280, 124
xn = lambda n: PX0 + math.log2(n) / 10 * (PX1 - PX0)
ys = lambda s: PY0 - s / 22 * (PY0 - PY1)
a(f'<line x1="{PX0}" y1="{PY0}" x2="{PX1}" y2="{PY0}" stroke="{QMUTED}"/><line x1="{PX0}" y1="{PY0}" x2="{PX0}" y2="{PY1}" stroke="{QMUTED}"/>')
a(f'<line x1="{PX0}" y1="{ys(20):.1f}" x2="{PX1}" y2="{ys(20):.1f}" stroke="{QROSE}" stroke-dasharray="5 4"/>')
a(text(PX1, ys(20) - 8, 'ceiling 1/(1 − p) = 20×', anchor='end', size=13, fill=QROSE, ls='0'))
pts = ' '.join(f'{xn(2 ** (i / 20)):.1f},{ys(S(2 ** (i / 20))):.1f}' for i in range(201))
a(f'<polyline points="{pts}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
for s in (0, 10, 20):
    a(text(PX0 - 8, ys(s) + 5, str(s), anchor='end', size=13, fill=QMUTED, ls='0'))
for n in (1, 32, 1024):
    a(text(xn(n), PY0 + 20, str(n), anchor='start' if n == 1 else ('end' if n == 1024 else 'middle'), size=13, fill=QMUTED, ls='0'))
a(text(PX1, PY0 + 40, 'cores, N', anchor='end', size=13, fill=QMUTED, ls='0'))
# the dot, stepping along the curve
ox, oy = xn(1), ys(S(1))
kx = [(0.0, xn(1024) - ox), (0.3, xn(1024) - ox), (0.305, 0.0)]
ky = [(0.0, ys(S(1024)) - oy), (0.3, ys(S(1024)) - oy), (0.305, 0.0)]
for k, n in enumerate(NS):
    if k:
        kx += [(TS[k] - 0.25, kx[-1][1]), (TS[k], xn(n) - ox)]
        ky += [(TS[k] - 0.25, ky[-1][1]), (TS[k], ys(S(n)) - oy)]
kx.append((D, kx[-1][1])); ky.append((D, ky[-1][1]))
a(f'<g class="fx"><g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{ox:.1f}" cy="{oy:.1f}" r="6" fill="#fff" stroke="{TEAL}" stroke-width="2"/></g></g></g>')
H = PY0 + 50
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-9 svgd-part5-9">')
o.insert(1, '<title id="svgt-part5-9">Fig 16.8 · Amdahl\'s law · the ceiling that won\'t move</title>')
o.insert(2, '<desc id="svgd-part5-9">One job whose work is 5% serial. As the number of cores doubles from 1 to 1,024, the parallel 95% of the time bar shrinks as 95 divided by N, but the serial 5% never does, so the bar approaches the serial floor. '
  'Below, the speedup curve S(N) = 1 / (0.05 + 0.95/N) rises fast at first and then flattens against its ceiling of 20: 5.9 at 8 cores, 15.4 at 64, 19.6 at 1,024.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Add cores and only the parallel part of a job shrinks; the serial part stays. '
           'With 5% serial work the speedup is 5.9× on 8 cores, 15.4× on 64 and 19.6× on 1,024, and no number of cores can take it past 20×.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The formula.</b> S(N) = 1 / ((1 − p) + p/N): the serial share 1 − p costs the same on any machine, the parallel share p is divided among N cores. As N grows, S approaches 1/(1 − p).</li>
          <li><b>Other values.</b> 50% parallel tops out at 2×, 90% at 10×, 99% at 100×: going from 95% to 99% parallel buys more than any number of extra cores.</li>
          <li><b>Who.</b> Gene Amdahl made the argument at the AFIPS conference in 1967; Fig 16.9 shows the answer to a different question.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-8">
      <div class="diagram-label">Fig 16.8 · Amdahl's law · the ceiling that won't move</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-8"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-8', cap, card.replace('CAPID', cap))
