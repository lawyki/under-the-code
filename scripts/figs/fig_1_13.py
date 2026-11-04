# Fig 1.13 · Running a program in 1955 (Pass 31, Part I, from an empty script). Job: function. Takeaway: the
# machine ran one person's cards at a time and sat idle while the next person's cards went in.
# Concept: one illustrative hour on a clock line. Above, you: you hand in your cards at 9:00, wait, and collect the
# printout at 10:00. Below, the machine: four people's stacks of cards, one at a time, yours from 9:30 for ten
# minutes, and empty gaps while the next stack is loaded. A gold hand sweeps the hour (Part I's step verb on a
# track) and the machine's state under it reads running or idle. The words are p1's: cards, not jobs or decks.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 252
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
X = lambda m: 20 + 6 * m                      # minutes past 9:00 to x
RUNS = [(0, 10, False), (18, 24, False), (30, 40, True), (46, 55, False)]     # idle 25 of the 60 minutes
D, SWEEP = 11.0, 9.0                         # the hand takes 9 s for the hour, then holds
T = Timeline(D, shift=SWEEP + 0.5)
TAU = lambda m: 0.5 + m / 60 * SWEEP
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-14 svgd-part1-14"{T.steps([(1.25, '9:05'), (2.75, '9:15'), (5.75, '9:35'), (10.0, '10:00')])}>')
a('<title id="svgt-part1-14">Fig 1.13 · Running a program in 1955 · one job, one user, one machine</title>')
a('<desc id="svgd-part1-14">An illustrative hour, 9:00 to 10:00. You hand in your stack of punched cards at 9:00 and wait. The machine '
  'runs one person\'s cards at a time: four stacks, yours from 9:30 to 9:40, with empty gaps between them, 25 minutes in all, while '
  'the next stack is loaded and the machine stands idle. At 10:00 you collect your printout.</desc>')

def stack(x, y, col, n=3):
    """a stack of punched cards: the front card whole, the ones behind it as their top and right edges"""
    s = ''
    for k in range(n - 1, 0, -1):
        dx, dy = k * 3, -k * 3
        s += f'<path d="M {x + dx + 5} {y + dy} H {x + dx + 26} V {y + dy + 18}" fill="none" stroke="{col}" stroke-width="1.3"/>'
    s += f'<path d="M {x + 5} {y} H {x + 26} V {y + 18} H {x} V {y + 5} Z" fill="none" stroke="{col}" stroke-width="1.3"/>'
    return s

# the clock line
for m, lab in ((0, '9:00'), (30, '9:30'), (60, '10:00')):
    a(f'<line x1="{X(m)}" y1="38" x2="{X(m)}" y2="48" stroke="rgba(255,255,255,0.5)" stroke-width="0.8" stroke-dasharray="2 4"/>')
    a(text(X(m), 30, lab, anchor='start' if m == 0 else 'end' if m == 60 else 'middle', size=14, fill=MUTED))

# you
a(text(20, 84, 'you', size=14, fill=INK))
a(stack(X(0) + 34, 70, GOLD))
a(f'<path d="M {X(0) + 66} 82 H {X(60) - 34}" stroke="rgba(255,255,255,0.4)" stroke-dasharray="3 5" stroke-width="1.5"/>')
# the printout at 10:00
a(f'<path d="M {X(60) - 28} 68 h 22 v 28 h -22 z" fill="none" stroke="{INK}" stroke-width="1.3"/>')
for k in range(4): a(f'<line x1="{X(60) - 24}" y1="{74 + k * 6}" x2="{X(60) - 10}" y2="{74 + k * 6}" stroke="{INK}" stroke-opacity="0.6"/>')

# the machine
a(text(20, 136, 'the machine', size=14, fill=INK))
MY = 146
a(f'<rect x="{X(0)}" y="{MY}" width="{X(60) - X(0)}" height="40" rx="3" fill="none" stroke="rgba(255,255,255,0.5)" stroke-dasharray="4 4"/>')
for m0, m1, yours in RUNS:
    col = GOLD
    a(f'<rect x="{X(m0)}" y="{MY}" width="{X(m1) - X(m0)}" height="40" rx="3" fill="{"rgba(212,168,83,0.85)" if yours else "none"}" stroke="{col}" stroke-width="1.6"/>')
a(text(X(35), MY + 58, 'your cards', anchor='middle', size=14, fill=GOLD))
a(text(X(14), MY + 26, 'idle', anchor='middle', size=14, fill=MUTED))

# the sweeping hand, and what the machine is doing under it
a(f'<g>{T.translate([(0.0, 0), (0.5, 0), (0.5 + SWEEP, X(60) - X(0)), (D - 0.2, X(60) - X(0)), (D - 0.01, 0)], axis="x")}'
  f'<path d="M {X(0)} 50 l -6 10 h 12 z" fill="{GOLD}"/></g>')
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
run_spans, idle_spans, prev = [], [], 0
for m0, m1, _ in RUNS:
    if m0 > prev: idle_spans.append((TAU(prev), TAU(m0)))
    run_spans.append((TAU(m0), TAU(m1))); prev = m1
idle_spans.append((TAU(prev), D - 0.01))
idle_spans[-1] = (TAU(prev), TAU(60))
run_spans[0] = (0.0, run_spans[0][1])
held = (TAU(60), D - 0.01)
a('</svg>')
svg = '\n'.join(o)

caption = 'One illustrative hour: your cards run ten minutes, and in the gaps the machine stands idle.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A job.</b> A stack of punched cards, roughly one line of program per card, carried to the machine room.</li>
          <li><b>The queue.</b> An operator loaded the stacks one after another; each person's cards had the whole computer while they ran.</li>
          <li><b>The cost.</b> A bug meant new cards and another hour's wait, and the machine stood idle in the gaps.</li>
          <li><b>The hour.</b> Four stacks of cards run for 35 minutes in all; for the other 25 the machine waits while the next stack is loaded.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-13">
      <div class="diagram-label">Fig 1.13 · Running a program in 1955 · one job, one user, one machine</div>
      {svg}
      <p id="ch1-kernel-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-13', 'ch1-kernel-p2', card)
