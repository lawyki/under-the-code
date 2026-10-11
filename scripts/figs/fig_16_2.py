# Fig 16.2 · The classic race · two threads, one counter, lost updates (Pass 28, law 3). Quorum glass plate. counter++
# is three steps: load, add, store. Two threads interleave them with counter = 100: T1 loads 100, T2 loads 100, T1
# adds and stores 101, T2 adds and stores 101. Two increments, the counter went up by one. Each step lights on its
# beat, the register values and the shared counter update in step. t=0 (shift): the race complete, 101 not 102.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
# the interleaving: (thread, step, register after, counter after)
STEPS = [(1, 'load', 100, 100), (2, 'load', 100, 100), (1, 'add', 101, 100), (1, 'store', 101, 101), (2, 'add', 101, 101), (2, 'store', 101, 101)]
reg = {1: None, 2: None}; cnt = 100
for th, op, r, c in STEPS:
    reg[th] = cnt if op == 'load' else (reg[th] + 1 if op == 'add' else reg[th])
    if op == 'store': cnt = reg[th]
    assert (reg[th], cnt) == (r, c)
assert cnt == 101
TS = [1.0 + 1.1 * k for k in range(len(STEPS))]
o = []; a = o.append
a(text(10, 18, 'counter++ is three steps:', anchor='start', size=13, fill=QSOFT, ls='0', extra=' style="font-variant-ligatures:none"'))
a(text(10, 38, 'load it, add 1, store it', anchor='start', size=13, fill=QMUTED, ls='0'))
# columns: thread 1, memory, thread 2
C1, CM, C2 = 70, 200, 330
for x, lab, col in ((C1, 'thread 1', VIOLET), (CM, 'counter', QAMBER), (C2, 'thread 2', TEAL)):
    a(text(x, 66, lab, anchor='middle', size=13, fill=col, ls='0'))
RY0, RS = 92, 30
for k, (th, op, r, c) in enumerate(STEPS):
    y = RY0 + k * RS
    x = C1 if th == 1 else C2
    col = VIOLET if th == 1 else TEAL
    s = f'{op}  {r}' if op != 'store' else f'store {r} →' if th == 1 else f'← store {r}'
    body = f'<rect x="{x - 56}" y="{y - 14}" width="112" height="22" rx="6" fill="{QCARD}" stroke="{col}" stroke-opacity="0.8"/>' + text(x, y + 2, s, anchor='middle', size=13, fill=col, ls='0')
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(TS[k])}{body}</g>')
    a(f'<g class="fx" opacity="0">{pulse(TS[k])}<rect x="{x - 58}" y="{y - 16}" width="116" height="26" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the counter's value over time, beside the steps
for k, (th, op, r, c) in enumerate(STEPS):
    y = RY0 + k * RS
    lost = op == 'store' and th == 2
    s = f'{c}' + ('  lost' if lost else '')
    col = QROSE if lost else (QAMBER if op == 'store' else QMUTED)
    a(f'<g opacity="0">{win(TS[k])}{text(CM, y + 2, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
# the verdict
VY = RY0 + 6 * RS + 12
a(f'<g opacity="0">{win(TS[-1] + 0.6)}{text(200, VY, "two increments, +1: expected 102, got 101", anchor="middle", size=13, fill=QROSE, ls="0")}</g>')
H = VY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-3 svgd-part5-3">')
o.insert(1, '<title id="svgt-part5-3">Fig 16.2 · The classic race · two threads, one counter, lost updates</title>')
o.insert(2, '<desc id="svgd-part5-3">counter++ is three steps: load, add one, store. With the counter at 100, thread 1 loads 100, then thread 2 loads 100 too. Thread 1 adds and stores 101. Thread 2 adds to its own stale copy and stores 101 as well. Two increments ran, and the counter rose by one: expected 102, got 101.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('<code>counter++</code> looks like one step but is three: load, add, store. When thread 2 loads before thread 1 has stored, both add one to the same 100 and both store 101, so one increment is lost.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>At scale.</b> Two threads doing a million increments each typically end well short of two million, and the total changes from run to run with the timing.</li>
          <li><b>Why it hides.</b> The bug depends on which instructions interleave, so it rarely shows in testing and appears under load.</li>
          <li><b>The fixes.</b> Make the read-modify-write one indivisible step (an atomic increment, Fig 16.4) or let only one thread in at a time (a mutex, Fig 16.3).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-2">
      <div class="diagram-label">Fig 16.2 · The classic race · two threads, one counter, lost updates</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-2"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-2', cap, card.replace('CAPID', cap))
