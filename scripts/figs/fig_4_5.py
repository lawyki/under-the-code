# Fig 4.5 · Four schedulers, one workload (Pass 28, law 3). Simulated, not drawn by hand
# (sched_model.py): A arrives at 0 needing 8, B at 1 needing 4, C at 2 needing 9, D at 3 needing 5.
# A cursor fills each schedule in time; every row shows the two numbers the schedulers trade:
# average wait, and average time to first run.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, RED, MUTED
from sched_model import JOBS, fcfs, sjf, rr, mlfq, avg_wait
figlib.FONT = PLEX

W, H = 400, 376
X0, X1 = 64, 386
X = lambda t: X0 + t / 26 * (X1 - X0)
COL = {'A': GOLD, 'B': BLUE, 'C': PHOS, 'D': RED}
def merged(s):
    out = []
    for n, a0, a1, *_ in s:
        if out and out[-1][0] == n and out[-1][2] == a0: out[-1] = (n, out[-1][1], a1)
        else: out.append((n, a0, a1))
    return out
def first_run(s):
    first = {}
    for n, a0, *_ in s: first.setdefault(n, a0)
    return sum(first[n] - ar for n, ar, _ in JOBS) / len(JOBS)
ROWS = [('FCFS', fcfs()), ('SJF', sjf()), ('RR', rr()), ('MLFQ', mlfq())]
SW0, SW1 = 0.4, 6.4
tm = lambda t: SW0 + t / 26 * (SW1 - SW0)
T = Timeline(8, shift=7.2)
def show(t0):
    return T.anim('opacity', [(0.0, 0.12), (t0 - 0.001, 0.12), (t0, 1.0), (7.7, 1.0), (7.701, 0.12), (7.9995, 0.12)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-5 svgd-part2-5">')
a('<title id="svgt-part2-5">Fig 4.5 · Four schedulers, one workload</title>')
a('<desc id="svgd-part2-5">Four jobs: A arrives at time 0 needing 8 units, B at 1 needing 4, C at 2 needing 9, D at 3 needing 5. '
  'First come first served gives an average wait of 8.75 and an average of 8.75 before a job first runs. Shortest job first: 7.75 and 7.75. '
  'Round robin with a quantum of 2: average wait 12.75 but first run after 2 on average. MLFQ: 13 and 1.5. Short average waits and quick first responses pull against each other.</desc>')
# the workload
a(text(20, 22, 'JOBS', size=13, fill=MUTED))
for k, (n, ar, b) in enumerate(JOBS):
    x = 70 + k * 80
    a(f'<rect x="{x}" y="10" width="14" height="14" rx="2" fill="{COL[n]}" fill-opacity="0.6" stroke="{COL[n]}"/>')
    a(text(x + 20, 22, f'{n} {ar}+{b}', size=13, fill=PHOS_SOFT, ls='0'))
for r, (name, s) in enumerate(ROWS):
    y = 50 + r * 74
    a(text(20, y + 18, name, size=14, fill=PHOS, ls='0'))
    a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="26" rx="2" fill="{PLATE}" stroke="rgba(132,255,178,0.25)"/>')
    for n, a0, a1 in merged(s):
        w = X(a1) - X(a0)
        a(f'<g opacity="0.12">{show(tm(a0))}<rect x="{X(a0):.1f}" y="{y}" width="{w - 1:.1f}" height="26" fill="{COL[n]}" fill-opacity="0.45" stroke="{COL[n]}"/>'
          + (f'<text x="{X(a0) + w / 2:.1f}" y="{y + 18}" text-anchor="middle" {PLEX} font-size="13" fill="#fff">{n}</text>' if w >= 14 else '') + '</g>')
    a(text(X0, y + 46, f'avg wait {avg_wait(s):g}', size=13, fill=PHOS_SOFT, ls='0'))
    a(text(X1, y + 46, f'first run after {first_run(s):g}', anchor='end', size=13, fill=PHOS_SOFT, ls='0'))
# time axis and the cursor
for t in (0, 10, 20, 26):
    a(text(X(t), 352, str(t), anchor='middle' if t not in (26,) else 'end', size=13, fill=MUTED, ls='0'))
a(text(X0, 370, 'time units', size=13, fill='rgba(198,222,206,0.5)', ls='0'))
a(f'<line y1="44" y2="334" stroke="#fff" stroke-width="1.5" opacity="0">{T.anim("x1", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}{T.anim("x2", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (SW0 - 0.01, 0.0), (SW0, 0.8), (SW1, 0.8), (SW1 + 0.05, 0.0), (7.9995, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same four jobs under four schedulers. Shortest-job-first gives the lowest average wait; round robin and MLFQ give up average wait to start every job almost at once, which is what an interactive machine needs.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The jobs.</b> "A 0+8" means A arrives at time 0 and needs 8 units of CPU.</li>
          <li><b>FCFS.</b> First come, first served: A's eight units hold up everyone behind it, the convoy effect.</li>
          <li><b>SJF.</b> Shortest job first: the lowest average wait of the four here, and provably optimal when every job is ready at the start, but it needs to know job lengths in advance.</li>
          <li><b>Round robin.</b> Each job runs for a quantum of 2, then goes to the back of the queue: responsive, at the cost of many switches.</li>
          <li><b>MLFQ.</b> Multi-level feedback queue: a job that uses up its whole slice drops to a lower queue with a longer slice, so short jobs stay on top. Windows and classic UNIX schedulers descend from this idea.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-5">
      <div class="diagram-label">Fig 4.5 · Four schedulers, one workload</div>
      {svg}
      <p id="ch4-scheduling-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-5', 'ch4-scheduling-p7', card)
