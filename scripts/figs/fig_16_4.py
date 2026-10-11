# Fig 16.4 · Compare-and-swap · the atomic primitive everything else is built on (Pass 28, law 3). Quorum glass plate.
# Fig 16.2's race replayed with CAS(addr, expected, new): store only if the value is still the one read. Counter 100;
# T1 reads 100, T2 reads 100; T1's CAS(100 → 101) succeeds; T2's CAS(100 → 101) fails because the counter is now 101,
# so T2 reads again and CAS(101 → 102) succeeds. Two increments, +2. Each step lights on its beat, in step with the
# counter column. t=0 (shift): 102.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
# (thread, label, counter after, ok?)  ok: None for reads, True/False for CAS
STEPS = [(1, 'read 100', 100, None), (2, 'read 100', 100, None), (1, 'CAS 100→101', 101, True),
         (2, 'CAS 100→101', 101, False), (2, 'read 101', 101, None), (2, 'CAS 101→102', 102, True)]
# check the story: a CAS succeeds exactly when the counter equals what that thread last read
cnt, seen = 100, {}
for th, lab, after, ok in STEPS:
    if lab.startswith('read'):
        seen[th] = cnt
    else:
        exp, new = (int(v) for v in lab.split()[1].split('→'))
        assert exp == seen[th] and (cnt == exp) == ok
        if ok: cnt = new
    assert cnt == after
assert cnt == 102
TS = [1.0 + 1.2 * k for k in range(len(STEPS))]
o = []; a = o.append
a(text(10, 18, 'CAS(addr, expected, new): store new', anchor='start', size=13, fill=QSOFT, ls='0'))
a(text(10, 38, 'only if addr still holds expected', anchor='start', size=13, fill=QMUTED, ls='0'))
C1, CM, C2 = 70, 200, 330
for x, lab, col in ((C1, 'thread 1', VIOLET), (CM, 'counter', QAMBER), (C2, 'thread 2', TEAL)):
    a(text(x, 66, lab, anchor='middle', size=13, fill=col, ls='0'))
RY0, RS = 92, 30
for k, (th, lab, after, ok) in enumerate(STEPS):
    y = RY0 + k * RS
    x = C1 if th == 1 else C2
    col = VIOLET if th == 1 else TEAL
    edge = QROSE if ok is False else col
    s = lab + ('  ✗' if ok is False else '  ✓' if ok else '')
    body = f'<rect x="{x - 62}" y="{y - 14}" width="124" height="22" rx="6" fill="{QCARD}" stroke="{edge}" stroke-opacity="0.85"/>' + text(x, y + 2, s, anchor='middle', size=13, fill=edge, ls='0')
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(TS[k])}{body}</g>')
    a(f'<g class="fx" opacity="0">{pulse(TS[k])}<rect x="{x - 64}" y="{y - 16}" width="128" height="26" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
    note = {False: ('101 ≠ 100', QROSE)}.get(ok, (str(after), QAMBER if ok else QMUTED))
    a(f'<g opacity="0">{win(TS[k])}{text(CM, y + 2, note[0], anchor="middle", size=13, fill=note[1], ls="0")}</g>')
VY = RY0 + 6 * RS + 12
a(f'<g opacity="0">{win(TS[-1] + 0.6)}{text(200, VY, "two increments, +2: 102, no lock taken", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
H = VY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-5 svgd-part5-5">')
o.insert(1, '<title id="svgt-part5-5">Fig 16.4 · Compare-and-swap · the atomic primitive everything else is built on</title>')
o.insert(2, '<desc id="svgd-part5-5">The race of Fig 16.2 replayed with compare-and-swap, which stores a new value only if the old one is still there. With the counter at 100, both threads read 100. Thread 1 swaps 100 for 101 and succeeds. '
  'Thread 2 tries to swap 100 for 101 and fails, because the counter now holds 101; it reads again and swaps 101 for 102. Two increments, and the counter rose by two, with no lock taken.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Compare-and-swap stores a new value only if the old one is still there, in one indivisible step. '
           'Thread 2\'s swap fails because thread 1 got there first, so it reads again and retries: both increments land, and no thread ever waits on a lock.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>In hardware.</b> <code>lock cmpxchg</code> on x86; on ARM a load-exclusive/store-exclusive pair, or a single CAS instruction since ARMv8.1. Languages expose it as <code>compare_exchange</code> (C++, Rust) or <code>compareAndSet</code> (Java).</li>
          <li><b>The price.</b> Under heavy contention threads keep losing and retrying; and a value that changes from A to B and back to A fools the check (the ABA problem).</li>
          <li><b>What it builds.</b> Locks themselves, lock-free queues and stacks (Michael and Scott's queue, 1996), and reference counts.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-4">
      <div class="diagram-label">Fig 16.4 · Compare-and-swap · the atomic primitive everything else is built on</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-4"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-4', cap, card.replace('CAPID', cap))
