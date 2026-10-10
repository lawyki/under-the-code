# Fig 7.5 · asyncio (Pass 28, law 3). One thread, three tasks. Each task runs until it awaits the
# network; the loop switches to another; the waits overlap; when nothing is ready the loop sleeps on
# epoll. A cursor draws time. t=0 (shift): the whole schedule.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 206
X0, X1, U = 92, 380, 24
xu = lambda u: X0 + u / U * (X1 - X0)
C0, C1 = 0.6, 7.6
tu = lambda u: C0 + u / U * (C1 - C0)
D = 10.0
T = Timeline(D, shift=9.0)
TASKS = {'A': ('#84ffb2', [(0, 3, 'run'), (3, 13, 'wait'), (13, 16, 'run')]),
         'B': ('#86a8ff', [(3, 6, 'run'), (6, 16, 'wait'), (16, 19, 'run')]),
         'C': ('#d4a853', [(6, 9, 'run'), (9, 19, 'wait'), (19, 22, 'run')])}
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-51 svgd-part2-51">')
a('<title id="svgt-part2-51">Fig 7.5 · asyncio: cooperative scheduling on one thread</title>')
a('<desc id="svgd-part2-51">One thread runs an event loop with three tasks. Task A runs until it awaits a network reply; the loop switches to task B, which runs until it awaits; then task C. '
  'While all three wait, their waits overlap and the loop sleeps until the operating system reports a reply. Then A resumes, then B, then C, each finishing. Only one task ever runs at a time, but the three waits happen together.</desc>')
def seg(x0, x1, y, h, fill, op, s, e, dash=False):
    w = x1 - x0 - 1
    da = ' stroke-dasharray="3 3" fill="none" stroke="' + fill + '"' if dash else f' fill="{fill}" fill-opacity="{op}"'
    a(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="2"{da}>'
      f'{T.anim("width", [(0.0, w), (0.4, w), (0.405, 0.0), (tu(s), 0.0), (tu(e), w), (D, w)])}</rect>')
# the one thread
a(text(20, 40, 'thread', size=13, fill='#fff', ls='0'))
a(f'<rect x="{X0}" y="24" width="{X1 - X0}" height="24" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.15)"/>')
for name, (col, ss) in TASKS.items():
    for s, e, k in ss:
        if k == 'run':
            seg(xu(s), xu(e), 24, 24, col, 0.6, s, e)
            a(f'<g opacity="0">{T.anim("opacity", [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (tu(e) - 0.002, 0.0), (tu(e), 1.0), (D, 1.0)])}'
              f'{text((xu(s) + xu(e)) / 2, 41, name, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (tu(13) - 0.002, 0.0), (tu(13), 1.0), (D, 1.0)])}'
  f'{text((xu(9) + xu(13)) / 2, 41, "idle", anchor="middle", size=13, fill=MUTED, ls="0")}</g>')
# the tasks
for i, (name, (col, ss)) in enumerate(TASKS.items()):
    y = 74 + i * 34
    a(text(20, y + 16, f'task {name}', size=13, fill=col, ls='0'))
    a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="22" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.1)"/>')
    for s, e, k in ss:
        if k == 'run':
            seg(xu(s), xu(e), y, 22, col, 0.6, s, e)
        else:
            seg(xu(s), xu(e), y + 2, 18, col, 0, s, e, dash=True)
    s, e, _ = ss[1]
    a(f'<g opacity="0">{T.anim("opacity", [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (tu(e) - 0.002, 0.0), (tu(e), 1.0), (D, 1.0)])}'
      f'{text(xu(s) + 8, y + 16, "await", size=13, fill=col, ls="0")}</g>')
# legend
LY = 196
a(f'<rect x="20" y="{LY - 11}" width="18" height="12" rx="2" fill="{PHOS}" fill-opacity="0.6"/>')
a(text(44, LY, 'runs on the thread', size=13, fill=PHOS_SOFT, ls='0'))
a(f'<rect x="210" y="{LY - 11}" width="18" height="12" rx="2" fill="none" stroke="{PHOS}" stroke-dasharray="3 3"/>')
a(text(234, LY, 'awaits a reply', size=13, fill=PHOS_SOFT, ls='0'))
# cursor
a(f'<line y1="20" y2="168" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}{T.anim("x2", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (C0 - 0.01, 0.0), (C0, 0.6), (C1, 0.6), (C1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One thread runs an event loop: each task runs until it awaits a network reply, and the loop switches to another that is ready, so the waits overlap although only one task runs at a time. '
           'A task can be interrupted only where it says <code>await</code>, so most shared state needs no locks.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The history.</b> <code>asyncio</code> arrived in Python 3.4 (2014); the <code>async def</code> and <code>await</code> keywords followed in 3.5.</li>
          <li><b>The idle gap.</b> When every task is waiting, the loop asks the operating system (<code>epoll</code>, <code>kqueue</code>) which sockets are ready, so one thread can watch thousands of connections.</li>
          <li><b>The catch.</b> A task that computes without awaiting holds up every other task, and <code>async</code> spreads to every function that calls an async one.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-5">
      <div class="diagram-label">Fig 7.5 · asyncio: cooperative scheduling on one thread</div>
      {svg}
      <p id="ch7-gil-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-5', 'ch7-gil-p4', card)
