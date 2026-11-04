# Fig BR.6 · The timer interrupt loop (Pass 31, Part I, from an empty script). Job: function. Takeaway: at each tick the
# hardware timer hands the CPU to the kernel, so even an endless loop loses it.
# Concept: four milliseconds of one core on a time line, the timer above it. A hand sweeps the time (Part I's step verb
# on a track); at every millisecond the timer fires (light), a tick drops onto the core, the kernel takes a sliver of
# time and its scheduler starts the next process. C is stuck in an endless loop and never gives the CPU up, and the
# third tick takes it back all the same. The still is the whole four milliseconds.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 300
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
X0, MS = 36, 84                                  # x of 0 ms, units per ms
X = lambda ms: X0 + ms * MS
D, SWEEP = 10.0, 8.0
T = Timeline(D, shift=SWEEP + 1.0)
TAU = lambda ms: 0.5 + ms / 4 * SWEEP
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-48 svgd-part1-48">')
a('<title id="svgt-part1-48">Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back</title>')
a('<desc id="svgd-part1-48">Four milliseconds of one CPU core with the timer set to a thousand ticks a second. Process A runs until the '
  'timer fires; the tick interrupts, the kernel runs for a moment and its scheduler picks process B; at the next tick, process C; at '
  'the next, A again. Process C is stuck in an endless loop and never gives up the CPU, but the tick takes it back exactly as it does '
  'from the others.</desc>')

# the timer
a(f'<circle cx="{X0 + 12}" cy="38" r="16" fill="none" stroke="{GOLD}" stroke-width="1.8"/>')
a(f'<path d="M {X0 + 12} 38 V 28 M {X0 + 12} 38 L {X0 + 19} 42" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round"/>')
a(text(X0 + 38, 43, 'timer · 1,000 ticks a second', size=14, fill=GOLD))
# the core's time line
LY = 112
a(text(20, LY - 24, 'one core', size=14, fill=MUTED))
RUNS = [(0, 1, 'A', BLUE), (1, 2, 'B', GREEN), (2, 3, 'C', RED), (3, 4, 'A', BLUE)]
for m0, m1, name, col in RUNS:
    x0, x1 = X(m0) + (6 if m0 else 0), X(m1) - 6 if m1 < 4 else X(m1)
    a(f'<rect x="{x0}" y="{LY}" width="{x1 - x0}" height="44" rx="4" fill="none" stroke="{col}" stroke-width="1.8"/>')
    a(text((x0 + x1) / 2, LY + 27, name, anchor='middle', size=16, fill=col, role='object'))
# C's endless loop, drawn inside its slot
cx = (X(2) + X(3)) / 2 + 22
a(f'<path d="M {cx + 9} {LY + 16} A 9 9 0 1 1 {cx - 1} {LY + 13}" fill="none" stroke="{RED}" stroke-width="1.6"/>')
a(f'<path d="M {cx - 4} {LY + 9} l 4 4 l -5 2" fill="none" stroke="{RED}" stroke-width="1.6"/>')
# each tick: the timer fires, the kernel takes a sliver, the next process starts
for m in (1, 2, 3):
    x = X(m)
    a(f'<rect x="{x - 5}" y="{LY - 4}" width="10" height="52" rx="2" fill="{GOLD}"/>')
    a(f'<path d="M {x} 62 V {LY - 8} m -5 -7 l 5 7 l 5 -7" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    t = TAU(m)
    a(f'<circle cx="{X0 + 12}" cy="38" r="20" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{vis([(t - 0.05, t + 0.45)])}</circle>')
    a(f'<path d="M {x} 62 V {LY - 8}" stroke="{GOLD}" stroke-width="3" opacity="0">{vis([(t - 0.05, t + 0.45)])}</path>')
a(f'<rect x="{X0}" y="{LY + 68}" width="12" height="12" rx="2" fill="{GOLD}"/>')
a(text(X0 + 20, LY + 79, 'kernel: the scheduler picks the next', size=14, fill=INK, ls='0'))
# the time axis
for m in range(5):
    a(f'<line x1="{X(m)}" y1="{LY + 50}" x2="{X(m)}" y2="{LY + 58}" stroke="{EDGE}"/>')
    a(text(X(m), LY + 112, f'{m} ms', anchor='middle', size=14, fill=MUTED))
# the hand sweeping the four milliseconds
a(f'<g>{T.translate([(0.0, 0), (0.5, 0), (0.5 + SWEEP, X(4) - X0), (D - 0.2, X(4) - X0), (D - 0.01, 0)], axis="x")}'
  f'<path d="M {X0} {LY + 62} l -6 10 h 12 z" fill="{INK}"/></g>')
a(text(20, 280, 'C never gave the CPU up; the tick took it', size=14, fill=RED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Four milliseconds of one core at 1,000 ticks a second: at each tick the kernel\'s scheduler picks the next process, and C, '
           'stuck in an endless loop, loses the CPU like the others.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rate.</b> Linux's tick is a build option, commonly 100, 250, 300 or 1,000 per second; the kernel programs the timer in each core's interrupt controller (the local APIC on x86; on ARM, the generic timer) at boot.</li>
          <li><b>Not to scale.</b> The kernel slices are drawn wide enough to see; a real tick takes microseconds, and the scheduler often lets one process run for several ticks.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-6">
      <div class="diagram-label">Fig BR.6 · The timer interrupt loop · how the kernel takes the CPU back</div>
      {svg}
      <p id="chBridge-timer-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-6', 'chBridge-timer-p3', card)
