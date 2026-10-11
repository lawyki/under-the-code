# Fig 16.5 · Memory orderings · relaxed vs release and acquire (Pass 28, law 3). Quorum glass plate. The
# message-passing test, run twice in step, time left to right in five slots. A writer does x = 1, then flag = 1; a
# reader waits for flag = 1, then reads x. Relaxed, on a weakly ordered CPU (ARM, POWER): other cores may see flag
# before x, so the reader gets x = 0. Release on the flag store, acquire on the flag load: x is visible no later than
# the flag, so the reader gets 1. Phase-synced: slot k lights at the same beat in both runs. t=0 (shift): complete.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
SX = [100, 166, 232, 298, 364]                    # slot centres (time)
CW = 60
D = 10.0
T = Timeline(D, shift=9.4)
TS = [1.0 + 1.3 * k for k in range(5)]
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
def chip(slot, y, s, col, strong=False):
    x = SX[slot]
    body = (f'<rect x="{x - CW / 2}" y="{y - 13}" width="{CW}" height="22" rx="6" fill="{QCARD}" stroke="{col}" stroke-width="{2 if strong else 1.2}"/>'
            + text(x, y + 3, s, anchor='middle', size=13, fill=col, ls='0'))
    a(f'<g opacity="0">{win(TS[slot])}{body}</g>')
    a(f'<g class="fx" opacity="0">{pulse(TS[slot])}<rect x="{x - CW / 2 - 2}" y="{y - 15}" width="{CW + 4}" height="26" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
def panel(y0, head, hcol, events):
    a(text(10, y0, head, anchor='start', size=13, fill=hcol, ls='0'))
    for k, lab in enumerate(('write', 'seen', 'read')):
        y = y0 + 28 + k * 28
        a(text(10, y + 3, lab, anchor='start', size=13, fill=QMUTED, ls='0'))
        a(f'<line x1="66" y1="{y}" x2="396" y2="{y}" stroke="{QMUTED}" stroke-opacity="0.18"/>')
    for row, slot, s, col, strong in events:
        chip(slot, y0 + 28 + row * 28, s, col, strong)
P1, P2 = 18, 138
panel(P1, 'relaxed, on ARM or POWER', QROSE, [
    (0, 0, 'x=1', VIOLET, False), (0, 1, 'flag=1', VIOLET, False),
    (1, 1, 'flag=1', QSOFT, False), (1, 4, 'x=1', QSOFT, False),
    (2, 2, 'flag=1', TEAL, False), (2, 3, 'x=0', QROSE, True)])
panel(P2, 'release / acquire', TEAL, [
    (0, 0, 'x=1', VIOLET, False), (0, 1, 'flag=1', VIOLET, True),
    (1, 1, 'x=1', QSOFT, False), (1, 2, 'flag=1', QSOFT, False),
    (2, 3, 'flag=1', TEAL, True), (2, 4, 'x=1', TEAL, True)])
LY = P2 + 28 + 3 * 28 + 6
a(f'<rect x="10" y="{LY - 10}" width="22" height="12" rx="3" fill="none" stroke="{QSOFT}" stroke-width="2"/>' + text(40, LY + 1, 'release store / acquire load', anchor='start', size=13, fill=QMUTED, ls='0'))
H = LY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-6 svgd-part5-6">')
o.insert(1, '<title id="svgt-part5-6">Fig 16.5 · Memory orderings · relaxed vs release and acquire</title>')
o.insert(2, '<desc id="svgd-part5-6">A writer sets x to 1 and then a flag to 1; a reader waits for the flag and then reads x. Run with relaxed ordering on a weakly ordered processor such as ARM, other cores can see the flag before x, so the reader sees the flag but reads x as 0. '
  'Run with a release store on the flag and an acquire load on the reader\'s side, x becomes visible no later than the flag, so the reader reads 1.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A writer sets x, then a flag; a reader waits for the flag, then reads x. With relaxed ordering a weakly ordered CPU can show the flag first and the reader gets the old x; '
           'a release store on the flag paired with an acquire load guarantees x arrives with it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The four levels.</b> Relaxed: the operation is atomic, nothing more. Release: earlier writes go out first. Acquire: later reads wait for what the matching release published. Sequentially consistent: all threads agree on one order of every such operation, at the highest cost.</li>
          <li><b>Hardware differs.</b> x86 keeps stores in order, so this test passes there even with relaxed atomics, and the bug surfaces only on ARM or POWER; the compiler may reorder the two writes on any machine unless told not to.</li>
          <li><b>Defaults.</b> Java and Go atomics are sequentially consistent; C++ lets the programmer choose per operation and defaults to sequentially consistent; Rust makes every atomic operation name its ordering.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-5">
      <div class="diagram-label">Fig 16.5 · Memory orderings · relaxed vs release and acquire</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-5', cap, card.replace('CAPID', cap))
