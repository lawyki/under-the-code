# Fig 7.4 · Two Python threads, one GIL (Pass 28, law 3). One 30 ms axis, two panels. With the GIL the
# threads take turns at the 5 ms switch interval; when T1 waits on I/O it releases the lock and T2 runs.
# The 3.13 free-threaded build runs both at once. A cursor draws time; a GIL tag moves at each handoff.
# t=0 (shift): all drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 236
X0, X1, MS = 92, 380, 30
xm = lambda ms: X0 + ms / MS * (X1 - X0)
C0, C1 = 0.6, 7.6
tm = lambda ms: C0 + ms / MS * (C1 - C0)
D = 10.0
T = Timeline(D, shift=9.0)
RUN, WAIT, IO = PHOS, 'rgba(198,222,206,0.18)', GOLD
GIL_SEGS = {  # lane: [(start, end, kind)]
    'T1': [(0, 5, 'run'), (5, 10, 'wait'), (10, 15, 'run'), (15, 25, 'io'), (25, 30, 'run')],
    'T2': [(0, 5, 'wait'), (5, 10, 'run'), (10, 15, 'wait'), (15, 25, 'run'), (25, 30, 'wait')]}
FREE_SEGS = {'T1': [(0, 30, 'run')], 'T2': [(0, 30, 'run')]}
COL = {'run': RUN, 'wait': WAIT, 'io': IO}
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-50 svgd-part2-50">')
a('<title id="svgt-part2-50">Fig 7.4 · Two Python threads, one GIL</title>')
a('<desc id="svgd-part2-50">Thirty milliseconds of two Python threads. With the global interpreter lock, only the thread holding it runs: thread 1 runs for 5 ms, then thread 2, then thread 1, the lock passing at the 5 ms switch interval. '
  'From 15 ms thread 1 waits on I/O and releases the lock, so thread 2 runs for those 10 ms; at 25 ms thread 1 takes the lock back. In Python 3.13\'s optional free-threaded build there is no such lock, and both threads run for the whole 30 ms.</desc>')
def lanes(y0, title, segs, gil):
    a(text(20, y0, title, size=13, fill=MUTED, ls='0'))
    for i, (lane, ss) in enumerate(segs.items()):
        y = y0 + 10 + i * 28
        a(text(20, y + 16, lane, size=13, fill=PHOS_SOFT, ls='0'))
        a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="22" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.12)"/>')
        for s, e, kind in ss:
            x, w = xm(s), xm(e) - xm(s) - 1
            a(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="2" fill="{COL[kind]}" fill-opacity="{0.55 if kind != "wait" else 1}">'
              f'{T.anim("width", [(0.0, w), (0.4, w), (0.405, 0.0), (tm(s), 0.0), (tm(e), w), (D, w)])}</rect>')
    if gil:
        hand = [(0.0, 0.0)]
        owner = [(0, 0), (5, 28), (10, 0), (15, 28), (25, 0)]
        for (ms, dy), (ms0, dy0) in zip(owner[1:], owner):
            hand += [(tm(ms) - 0.1, dy0), (tm(ms), dy)]
        hand += [(D - 0.4, 0.0), (D, 0.0)]
        a(f'<g>{T.translate(hand, "y")}<rect x="44" y="{y0 + 10}" width="42" height="22" rx="3" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}"/>'
          f'{text(65, y0 + 26, "GIL", anchor="middle", size=13, fill=GOLD, ls="0")}</g>')
lanes(18, 'default build: one lock', GIL_SEGS, True)
lanes(132, '3.13 free-threaded build', FREE_SEGS, False)
for ms in (0, 10, 20):
    a(text(xm(ms), 104, str(ms), anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(X1, 104, '30 ms', anchor='end', size=13, fill=MUTED, ls='0'))
# legend
LY = 222
for x, col, lab in ((20, RUN, 'runs'), (110, IO, 'waits on I/O'), (250, 'rgba(198,222,206,0.35)', 'waits for GIL')):
    a(f'<rect x="{x}" y="{LY - 11}" width="12" height="12" rx="2" fill="{col}"/>')
    a(text(x + 18, LY, lab, size=13, fill=PHOS_SOFT, ls='0'))
# cursor
a(f'<line y1="24" y2="198" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}{T.anim("x2", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (C0 - 0.01, 0.0), (C0, 0.6), (C1, 0.6), (C1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('With the GIL, two CPU-bound threads take turns, the lock passing between them every 5 ms, so only one runs at a time; a thread waiting on I/O releases it, and then the other gets real work done. '
           'Python 3.13\'s optional free-threaded build removes the lock, and both threads run at once.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why one lock.</b> CPython's reference counts and internal structures were never safe to update from two threads at once; a single lock made them safe and kept the interpreter simple.</li>
          <li><b>The interval.</b> <code>sys.getswitchinterval()</code> is 0.005 seconds by default: after that, the running thread is asked to hand the lock over.</li>
          <li><b>Removing it.</b> PEP 703's free-threaded build uses per-object locks and biased reference counting; in 3.13 it is optional, and single-threaded code runs somewhat slower in it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-4">
      <div class="diagram-label">Fig 7.4 · Two Python threads, one GIL</div>
      {svg}
      <p id="ch7-gil-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-4', 'ch7-gil-p3', card)
