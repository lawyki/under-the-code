# Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back (Pass 28, law 3, conceptual pass). Four
# milliseconds of one core with the timer set to 1 kHz. A cursor sweeps the timeline: process A runs, the timer counts
# down to zero and fires, a thin kernel slice runs the scheduler, then B, then C, which is stuck in while (1) and never
# yields, yet is cut off at the next tick exactly like the others, then A again. Below, the timer's countdown, refilled at
# each tick. t=0 (shift): the four milliseconds drawn.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W = 400
X0, X1 = 20, 380
MS = 4
xm = lambda t: X0 + t / MS * (X1 - X0)
K = 0.08                                            # kernel slice width, in ms (drawn wide enough to see)
SLICES = [('A', BLUE), ('B', GREEN), ('C · while (1)', RED), ('A', BLUE)]
D = 11.0
T = Timeline(D, shift=10.4)
S0, S1 = 0.8, 8.8
tm = lambda ms: S0 + ms / MS * (S1 - S0)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
a(text(X0, 22, 'one core, timer at 1,000 ticks a second', size=13, fill=MUTED, ls='0'))
LY, LH = 40, 46
fills = []
for k, (lab, col) in enumerate(SLICES):
    x0 = xm(k + (K if k else 0)); x1 = xm(k + 1)
    a(f'<rect x="{x0:.1f}" y="{LY}" width="{x1 - x0:.1f}" height="{LH}" rx="3" fill="none" stroke="{col}" stroke-opacity="0.5"/>')
    fills.append(f'<rect x="{x0:.1f}" y="{LY}" width="{x1 - x0:.1f}" height="{LH}" rx="3" fill="{col}" fill-opacity="0.28"/>')
    if k:
        fills.append(f'<rect x="{xm(k):.1f}" y="{LY}" width="{xm(k + K) - xm(k):.1f}" height="{LH}" fill="{GOLD}"/>')
a(f'<defs><clipPath id="clip-fig-br-6"><rect class="fx" x="{X0}" y="0" width="{X1 - X0}" height="400">'
  f'{T.anim("width", [(0.0, X1 - X0), (0.3, X1 - X0), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0), (D, X1 - X0)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-br-6)">{"".join(fills)}</g>')
for k, (lab, col) in enumerate(SLICES):
    cx = (xm(k + (K if k else 0)) + xm(k + 1)) / 2
    if 'while' in lab:
        a(text(cx, LY + 20, 'C', anchor='middle', size=13, fill='#fff', ls='0'))
        a(text(cx, LY + 37, 'while (1)', anchor='middle', size=13, fill=RED, ls='0'))
    else:
        a(text(cx, LY + 28, lab, anchor='middle', size=13, fill='#fff', ls='0'))
for k in range(1, MS):
    a(f'<g class="fx" opacity="0">{pulse(tm(k))}<rect x="{xm(k) - 3:.1f}" y="{LY - 4}" width="{xm(k + K) - xm(k) + 6:.1f}" height="{LH + 8}" rx="2" fill="none" stroke="#fff" stroke-width="2"/></g>')
# axis
AY = LY + LH + 18
a(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{MUTED}"/>')
for k in range(MS + 1):
    a(f'<line x1="{xm(k):.1f}" y1="{AY - 4}" x2="{xm(k):.1f}" y2="{AY + 4}" stroke="{MUTED}"/>')
    a(text(xm(k), AY + 20, f'{k} ms', anchor='start' if k == 0 else ('end' if k == MS else 'middle'), size=13, fill=MUTED, ls='0'))
a(f'<rect x="{X0}" y="{AY + 36}" width="12" height="12" fill="{GOLD}"/>' + text(X0 + 20, AY + 47, 'kernel: tick, scheduler picks next', size=13, fill=GOLD, ls='0'))
# the timer's countdown
CY = AY + 84
a(text(X0, CY, 'timer countdown', size=13, fill=MUTED, ls='0'))
BW = X1 - X0
a(f'<rect x="{X0}" y="{CY + 10}" width="{BW}" height="14" rx="3" fill="none" stroke="{GOLD}" stroke-opacity="0.6"/>')
pts = [(0.0, BW), (0.3, BW), (0.305, BW)]
for k in range(MS):
    pts += [(tm(k) + 0.01, BW), (tm(k + 1) - 0.01, 0.0)]
pts += [(tm(MS) + 0.01, BW), (D, BW)]
a(f'<rect x="{X0}" y="{CY + 10}" width="{BW}" height="14" rx="3" fill="{GOLD}" fill-opacity="0.7">{T.anim("width", pts)}</rect>')
a(f'<g opacity="0">{win(tm(MS))}{text(X0, CY + 46, "C never yielded; the tick took the CPU back", size=13, fill=RED, ls="0")}</g>')
H = CY + 58
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-48 svgd-part1-48">')
o.insert(1, '<title id="svgt-part1-48">Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back</title>')
o.insert(2, '<desc id="svgd-part1-48">Four milliseconds of one CPU core with the timer set to a thousand ticks a second. Process A runs until the timer\'s countdown reaches zero; the timer interrupts, the kernel runs for a moment and its scheduler picks process B; at the next tick, process C; at the next, A again. '
  'Process C is stuck in an endless loop and never gives up the CPU, but the tick takes it back exactly as it does from the others.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The kernel sets a hardware timer to interrupt it at a fixed rate; each tick hands the CPU to the kernel, whose scheduler decides what runs next. '
           'A program stuck in an endless loop never gives the CPU up, but the timer takes it back anyway.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rate.</b> Linux's tick is a build option, commonly 100, 250 or 1,000 per second; the kernel programs the local APIC timer (on ARM, the generic timer) at boot.</li>
          <li><b>Tickless.</b> An idle core can skip ticks entirely, and a core running one task can almost stop them (Linux's NO_HZ_IDLE and NO_HZ_FULL), saving power.</li>
          <li><b>Why it matters.</b> Privilege, traps and the MMU decide what user code may do; the timer is what guarantees the kernel gets to run at all.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-6">
      <div class="diagram-label">Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-6"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-6', cap, card.replace('CAPID', cap))
