# Fig 16.3 · Mutex protects · deadlock is the new failure mode (Pass 28, law 3). Quorum glass plate. Two threads and
# two locks, run twice in step. Opposite order: A takes L1, B takes L2, A waits for L2, B waits for L1, and the
# wait-for arrows close a cycle: both stop for ever. Same order (both take L1 first): B waits for L1 while A takes L2,
# finishes and releases; then B goes through. Phase-synced: both lanes run on the same beats. t=0 (shift): the left
# frozen in its cycle, the right finished.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
B1, B2, B3, B4 = 1.0, 2.6, 4.2, 5.8                # beats
o = []; a = o.append
def panel(x0, head, hcol):
    a(text(x0, 18, head, anchor='start', size=13, fill=hcol, ls='0'))
    for k, (lab, col) in enumerate((('A', VIOLET), ('B', TEAL))):
        cx = x0 + 34 + k * 118
        a(f'<circle cx="{cx}" cy="70" r="22" fill="{QCARD}" stroke="{col}" stroke-width="1.5"/>')
        a(text(cx, 75, lab, anchor='middle', size=13, fill=col, ls='0'))
    for k, lab in enumerate(('L1', 'L2')):
        cx = x0 + 34 + k * 118
        a(f'<rect x="{cx - 24}" y="150" width="48" height="30" rx="6" fill="{QCARD}" stroke="{QAMBER}" stroke-width="1.5"/>')
        a(text(cx, 170, lab, anchor='middle', size=13, fill=QAMBER, ls='0'))
def holds(x0, th, lk, t0, t1):
    tx, lx = x0 + 34 + th * 118, x0 + 34 + lk * 118
    col = VIOLET if th == 0 else TEAL
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}<line x1="{tx}" y1="92" x2="{lx}" y2="150" stroke="{col}" stroke-width="3"/></g>')
def wants(x0, th, lk, t0, t1):
    tx, lx = x0 + 34 + th * 118, x0 + 34 + lk * 118
    col = VIOLET if th == 0 else TEAL
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}<line x1="{tx}" y1="92" x2="{lx}" y2="150" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 3"/></g>')
# opposite order: deadlock
L = 10
panel(L, 'opposite order', QROSE)
holds(L, 0, 0, B1, None); holds(L, 1, 1, B1, None)
wants(L, 0, 1, B2, None); wants(L, 1, 0, B2, None)
a(f'<g opacity="0">{win(B3)}{text(L + 93, 214, "cycle: both wait", anchor="middle", size=13, fill=QROSE, ls="0")}{text(L + 93, 232, "for ever", anchor="middle", size=13, fill=QROSE, ls="0")}</g>')
# same order: B waits, A finishes
R = 206
panel(R, 'same order: L1 first', TEAL)
holds(R, 0, 0, B1, B4); holds(R, 0, 1, B2, B4)
wants(R, 1, 0, B1, B4)
holds(R, 1, 0, B4, None); holds(R, 1, 1, B4 + 0.8, None)
a(f'<g opacity="0">{lit(B3, B4)}{text(R + 93, 214, "A finishes,", anchor="middle", size=13, fill=VIOLET, ls="0")}{text(R + 93, 232, "lets go", anchor="middle", size=13, fill=VIOLET, ls="0")}</g>')
a(f'<g opacity="0">{win(B4)}{text(R + 93, 214, "then B runs", anchor="middle", size=13, fill=TEAL, ls="0")}{text(R + 93, 232, "no cycle", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
# legend
a(f'<line x1="10" y1="262" x2="34" y2="262" stroke="{QSOFT}" stroke-width="3"/>' + text(40, 267, 'holds', anchor='start', size=13, fill=QMUTED, ls='0'))
a(f'<line x1="110" y1="262" x2="134" y2="262" stroke="{QSOFT}" stroke-width="1.5" stroke-dasharray="4 3"/>' + text(140, 267, 'waits for', anchor='start', size=13, fill=QMUTED, ls='0'))
H = 278
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-4 svgd-part5-4">')
o.insert(1, '<title id="svgt-part5-4">Fig 16.3 · Mutex protects · deadlock is the new failure mode</title>')
o.insert(2, '<desc id="svgd-part5-4">Two threads, A and B, and two locks, L1 and L2, run two ways. Taking them in opposite orders: A holds L1, B holds L2, then A waits for L2 and B waits for L1. The waits form a cycle and both wait for ever. '
  'Taking them in the same order, L1 first: B waits for L1 while A takes L2, finishes and releases both; then B takes them in turn. With no cycle there is no deadlock.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A mutex lets one thread in at a time, which fixes the race but creates a new failure: if A holds L1 and waits for L2 while B holds L2 and waits for L1, both wait for ever. '
           'If every thread takes locks in the same order, the waits can never form a cycle, and the deadlock cannot happen.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The wait-for graph.</b> An arrow from each waiting thread to the holder of the lock it wants; deadlock is exactly a cycle in that graph.</li>
          <li><b>Lock ordering.</b> Large codebases such as Linux and PostgreSQL document a hierarchy of locks; taking them out of order is a review red flag, and Linux's lockdep checks for it at run time.</li>
          <li><b>Livelock.</b> The same shape with threads that keep backing off and retrying in step instead of blocking: busy, yet no progress.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-3">
      <div class="diagram-label">Fig 16.3 · Mutex protects · deadlock is the new failure mode</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-3"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-3', cap, card.replace('CAPID', cap))
