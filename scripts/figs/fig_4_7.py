# Fig 4.7 · A periodic task and its deadline (Pass 28, law 3). A 100 Hz brake controller: every
# 10 ms a job must finish before the next period starts. Three jobs take 5 ms; the fourth takes
# 12 ms and runs past its 40 ms deadline. A cursor runs time forward. t=0: all four drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 206
X0, X1 = 30, 380
X = lambda ms: X0 + ms / 44 * (X1 - X0)
JOBS = [(0, 5), (10, 5), (20, 5), (30, 12)]
SW0, SW1 = 0.4, 6.0
tm = lambda ms: SW0 + ms / 44 * (SW1 - SW0)
T = Timeline(8, shift=7.2)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-7 svgd-part2-7">')
a('<title id="svgt-part2-7">Fig 4.7 · A periodic task and the deadline it must meet</title>')
a('<desc id="svgd-part2-7">A brake controller that runs at 100 Hz: every 10 milliseconds a new job starts and must finish before the next one. '
  'The first three jobs take 5 milliseconds and finish with time to spare. The fourth takes 12 milliseconds and is still running at its 40 millisecond deadline: a missed deadline, which in a brake controller is a failure, not a slowdown.</desc>')
a(text(X0, 24, '100 Hz BRAKE CONTROLLER · 10 ms PERIOD', size=13, fill=MUTED))
a(f'<rect x="{X0}" y="80" width="{X1 - X0}" height="44" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.25)"/>')
# deadlines: the end of each period
for k in range(1, 5):
    x = X(k * 10)
    a(f'<line x1="{x:.1f}" y1="54" x2="{x:.1f}" y2="136" stroke="{PHOS_SOFT}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    a(f'<polygon points="{x - 6:.1f},48 {x + 6:.1f},48 {x:.1f},56" fill="{PHOS_SOFT}"/>')
a(text(X(10) - 10, 52, 'deadline', anchor='end', size=13, fill=PHOS_SOFT, ls='0'))
HOLD = [(7.7, 1.0), (7.701, 0.0), (7.9995, 0.0)]
def show(t):  # off until story time t, on until the loop resets
    return T.anim('opacity', [(0.0, 0.0), (t - 0.001, 0.0), (t, 1.0)] + HOLD)
for i, (s0, d) in enumerate(JOBS):
    dl = (i + 1) * 10
    miss = s0 + d > dl
    end_ok = min(s0 + d, dl)
    w = X(end_ok) - X(s0) - 1
    a(f'<rect x="{X(s0):.1f}" y="86" width="{w:.1f}" height="32" rx="2" fill="{PHOS}" fill-opacity="0.35" stroke="{PHOS}">'
      f'{T.anim("width", [(0.0, w), (SW0, w), (SW0 + 0.001, 0.0), (tm(s0), 0.0), (tm(end_ok), w), (8.0, w)])}</rect>')
    if miss:
        wr = X(s0 + d) - X(dl)
        a(f'<rect x="{X(dl):.1f}" y="86" width="{wr:.1f}" height="32" rx="2" fill="{RED}" fill-opacity="0.5" stroke="{RED}" stroke-width="2">'
          f'{T.anim("width", [(0.0, wr), (SW0, wr), (SW0 + 0.001, 0.0), (tm(dl), 0.0), (tm(s0 + d), wr), (8.0, wr)])}</rect>')
        a(f'<g>{T.anim("opacity", [(0.0, 1.0), (SW0, 1.0), (SW0 + 0.001, 0.0), (tm(dl) - 0.001, 0.0), (tm(dl), 1.0), (8.0, 1.0)])}'
          f'{text(X1, 160, "missed by 2 ms", anchor="end", size=15, fill=RED, ls="0")}</g>')
    lab = f'{d} ms'
    lx = (X(s0) + X(end_ok)) / 2
    t_lab = tm(s0 + d)
    a(f'<g>{T.anim("opacity", [(0.0, 1.0), (SW0, 1.0), (SW0 + 0.001, 0.0), (t_lab - 0.001, 0.0), (t_lab, 1.0), (8.0, 1.0)])}'
      + (text(lx, 107, lab, anchor='middle', size=13, fill='#fff', ls='0') if not miss else text(X(s0) + 6, 107, lab, size=13, fill='#fff', ls='0'))
      + '</g>')
for ms in (0, 10, 20, 30, 40):
    a(text(X(ms), 190, str(ms), anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(X1, 190, 'ms', anchor='end', size=13, fill=MUTED, ls='0'))
a(f'<line y1="64" y2="136" stroke="#fff" stroke-width="1.5" opacity="0">{T.anim("x1", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}{T.anim("x2", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (SW0 - 0.01, 0.0), (SW0, 0.8), (SW1, 0.8), (SW1 + 0.05, 0.0), (7.9995, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A real-time task must finish each job inside its period: here every 10 ms. Three jobs fit with room to spare; the fourth runs 12 ms and is still going at its deadline, which in a brake controller is a failure, not a stutter.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          
          <li><b>The guarantee.</b> Rate-monotonic scheduling meets every deadline if total utilisation stays under about 69%; earliest-deadline-first, up to 100% (Liu and Layland, 1973).</li>
          <li><b>The overrun.</b> A job that takes longer than its budget breaks the arithmetic, which is why real-time code is written to bounded, measured worst cases.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-7">
      <div class="diagram-label">Fig 4.7 · A periodic task and the deadline it must meet</div>
      {svg}
      <p id="ch4-scheduling-p13" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-7', 'ch4-scheduling-p13', card)
