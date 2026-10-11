# Fig 16.9 · Amdahl vs Gustafson · same hardware, different question (Pass 28, law 3). Quorum glass plate. One program,
# 5% serial, N stepping 1, 2, 4 … 64, two questions in step. Amdahl fixes the work: the time bar shrinks towards its
# serial floor, speedup 1 / (0.05 + 0.95/N) → 15.4 at 64. Gustafson fixes the time: the parallel part grows with N, so
# the work done in that time is 0.05 + 0.95·N → 60.9 at 64. t=0 (shift): N = 64.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

P = 0.95
AM = lambda n: 1 / ((1 - P) + P / n)
GU = lambda n: n - (1 - P) * (n - 1)
NS = [1, 2, 4, 8, 16, 32, 64]
assert abs(AM(64) - 15.42) < 0.01 and abs(GU(64) - 60.85) < 0.01 and abs(GU(64) - ((1 - P) + P * 64)) < 1e-9
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
TS = [0.8 + 1.0 * k for k in range(len(NS))]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
BX, BW = 20, 360
def stepped(draw):
    for k, n in enumerate(NS):
        t1 = TS[k + 1] if k + 1 < len(NS) else None
        vis = first(t1) if k == 0 else (win(TS[k]) if t1 is None else lit(TS[k], t1))
        a(f'<g opacity="0">{vis}{draw(n)}</g>')
a(f'<g>{text(BX, 18, "N = ", anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
stepped(lambda n: text(BX + 32, 18, f'{n} core{"s" if n > 1 else ""}', anchor='start', size=13, fill=QSOFT, ls='0'))
# Amdahl: fixed work, time shrinks
a(text(BX, 50, 'Amdahl: same job, how much faster?', anchor='start', size=13, fill=VIOLET, ls='0'))
SW = (1 - P) * BW
a(f'<rect x="{BX}" y="60" width="{BW}" height="20" rx="3" fill="none" stroke="{QMUTED}" stroke-opacity="0.35" stroke-dasharray="3 3"/>')
a(f'<rect x="{BX}" y="60" width="{SW:.1f}" height="20" rx="3" fill="{QROSE}" fill-opacity="0.9"/>')
stepped(lambda n: f'<rect x="{BX + SW:.1f}" y="60" width="{P / n * BW:.1f}" height="20" rx="3" fill="{VIOLET}" fill-opacity="0.85"/>'
        + text(BX, 102, f'time {(1 - P) + P / n:.2f} · speedup {AM(n):.1f}×', anchor='start', size=13, fill=VIOLET, ls='0'))
a(text(BX + BW, 102, 'ceiling 20×', anchor='end', size=13, fill=QROSE, ls='0'))
# Gustafson: fixed time, work grows
a(text(BX, 148, 'Gustafson: same time, how much more?', anchor='start', size=13, fill=TEAL, ls='0'))
a(f'<rect x="{BX}" y="158" width="{BW}" height="20" rx="3" fill="{TEAL}" fill-opacity="0.18" stroke="{TEAL}" stroke-opacity="0.5"/>')
a(f'<rect x="{BX}" y="158" width="{SW:.1f}" height="20" rx="3" fill="{QROSE}" fill-opacity="0.9"/>')
a(text(BX + BW, 196, 'time fixed', anchor='end', size=13, fill=QMUTED, ls='0'))
UW = BW / GU(64)                                   # px per unit of work
stepped(lambda n: f'<rect x="{BX}" y="210" width="{GU(n) * UW:.1f}" height="20" rx="3" fill="{TEAL}" fill-opacity="0.85"/>'
        + text(BX, 252, f'work done {GU(n) + 1e-9:.1f}× · grows with N', anchor='start', size=13, fill=TEAL, ls='0'))
a(text(BX, 196, 'work done in that time:', anchor='start', size=13, fill=QSOFT, ls='0'))
H = 264
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-10 svgd-part5-10">')
o.insert(1, '<title id="svgt-part5-10">Fig 16.9 · Amdahl vs Gustafson · same hardware, different question</title>')
o.insert(2, '<desc id="svgd-part5-10">One program whose work is 5% serial, on 1 to 64 cores, asked two questions. Amdahl keeps the job fixed and asks how much faster it runs: the time bar shrinks toward its serial floor, and the speedup reaches 15.4 at 64 cores, never more than 20. '
  'Gustafson keeps the time fixed and asks how much more work gets done: the parallel part grows with the cores, so the work done in the same time reaches 60.9 times as much at 64 cores.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Amdahl keeps the job fixed and asks how much faster more cores make it: with 5% of the time serial, 15.4× on 64 cores and never past 20×. '
           'Gustafson keeps the time fixed and asks how much more work fits: the parallel part grows with the machine, so 64 cores do about 61 times the work.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The two formulas.</b> Amdahl: S = 1 / ((1 − p) + p/N). Gustafson: S = (1 − p) + p·N, the same as N − (1 − p)(N − 1).</li>
          <li><b>Which applies.</b> A frame that must render in 16 ms, or one fixed compile, is Amdahl. A bigger simulation, a larger model or more samples in the same hour is Gustafson, which is why supercomputers and GPU clusters keep scaling.</li>
          <li><b>Who.</b> John Gustafson made the argument in 1988, after his team at Sandia ran problems scaled to 1,024 processors.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-9">
      <div class="diagram-label">Fig 16.9 · Amdahl vs Gustafson · same hardware, different question</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-9"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-9', cap, card.replace('CAPID', cap))
