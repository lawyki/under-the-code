# Fig 1.15 · The hierarchy of forgetting (Pass 31, Part I, from an empty script). Job: function. Takeaway: each
# level down is bigger but slower, so a cache keeps recent reads close and repeats are fast.
# Concept: the levels as a ladder, each rung a bar as long as the level is big (tenfold steps), its time beside it
# on a human scale where a register answers in one second. One read drops down the ladder (Part I's step verb),
# misses the three caches and waits three minutes on RAM; on its way back each cache keeps a copy (blue). The same
# read again stops at L1 in four seconds. t=0 is after both reads: the copies are in place and both times stated.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 372
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
LEVELS = [('registers', 96, '1 s'), ('L1 cache', 100, '4 s'), ('L2 cache', 120, '12 s'), ('L3 cache', 146, '40 s'),
          ('RAM', 190, '3 min'), ('SSD', 226, '2 days'), ('hard disk', 250, '6 months')]
RY = lambda i: 44 + i * 38                    # row top
BX = 22                                       # bars start
D = 12.0
T = Timeline(D, shift=8.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-16 svgd-part1-16"{T.steps([(3.9, '1st read'), (5.6, 'copies'), (6.9, 'read again')])}>')
a('<title id="svgt-part1-16">Fig 1.15 · The hierarchy of forgetting · bigger and slower at every step</title>')
a('<desc id="svgd-part1-16">Seven levels from registers to hard disk, each bar longer (more capacity, in tenfold steps) and slower. If a '
  'register access took one second, L1 would take 4 seconds, L2 12, L3 40, RAM 3 minutes, an SSD 2 days and a hard disk 6 months. '
  'A first read misses every cache and fetches from RAM, leaving copies in L3, L2 and L1 on the way back; a second read of the same '
  'data stops at L1.</desc>')

a(text(20, 26, 'bigger', size=14, fill=MUTED))
a(f'<path d="M 82 21 h 34 m -6 -5 l 6 5 l -6 5" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
a(text(380, 26, 'if a register took 1 s', anchor='end', size=14, fill=MUTED))
for i, (name, w, t) in enumerate(LEVELS):
    y = RY(i)
    col = GOLD if i == 0 else BLUE if i <= 3 else INK if i == 4 else 'rgba(236,230,218,0.75)'
    a(f'<rect x="{BX}" y="{y}" width="{w * 1.06:.0f}" height="28" rx="4" fill="none" stroke="{col}" stroke-opacity="0.8" stroke-width="1.4"/>')
    a(text(BX + 10, y + 19, name, size=14, fill=col))
    a(text(380, y + 19, t, anchor='end', size=15 if i in (1, 4) else 14, fill=INK if i in (1, 4) else MUTED))

# the read: a gold dot dropping down the ladder at the bars' right ends
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
DX = 300
cyc = lambda i: RY(i) + 14
first = [(0.0, cyc(0)), (0.6, cyc(0)), (1.0, cyc(1)), (1.4, cyc(1)), (1.8, cyc(2)), (2.2, cyc(2)), (2.6, cyc(3)), (3.0, cyc(3)),
         (3.5, cyc(4)), (4.3, cyc(4)), (5.3, cyc(0)), (D - 0.01, cyc(0))]
a(f'<g opacity="0">{vis([(0.6, 5.3)])}<g>{T.translate([(t, v - cyc(0)) for t, v in first], axis="y")}'
  f'<circle cx="{DX}" cy="{cyc(0)}" r="6" fill="{GOLD}"/></g></g>')
second = [(0.0, cyc(0)), (6.0, cyc(0)), (6.4, cyc(1)), (D - 0.01, cyc(1))]
a(f'<g opacity="0">{vis([(6.0, 7.4)])}<g>{T.translate([(t, v - cyc(0)) for t, v in second], axis="y")}'
  f'<circle cx="{DX}" cy="{cyc(0)}" r="6" fill="{GOLD}"/></g></g>')
# misses on the first read
for i, t0 in ((1, 1.0), (2, 1.8), (3, 2.6)):
    a(f'<g opacity="0">{vis([(t0, t0 + 0.6)])}<path d="M {DX + 14} {cyc(i) - 5} l 10 10 m 0 -10 l -10 10" stroke="{RED}" stroke-width="2.4" stroke-linecap="round"/></g>')
# found in RAM, then again in L1
for i, t0, t1 in ((4, 3.5, 4.4), (1, 6.4, 7.4)):
    a(f'<g opacity="0">{vis([(t0, t1)])}<path d="M {DX + 12} {cyc(i)} l 4 5 l 9 -10" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>')
# the copies each cache keeps on the way back up
for i, t0 in ((3, 4.6), (2, 4.85), (1, 5.1)):
    x = BX + LEVELS[i][1] * 1.06 + 10
    a(f'<g opacity="0">{vis([(t0, D - 0.3)])}<rect x="{x:.0f}" y="{RY(i) + 7}" width="14" height="14" rx="2" fill="{BLUE}"/></g>')
a(f'<g opacity="0">{vis([(0.0, 0.6)])}' + ''.join(
    f'<rect x="{BX + LEVELS[i][1] * 1.06 + 10:.0f}" y="{RY(i) + 7}" width="14" height="14" rx="2" fill="{BLUE}"/>' for i in (1, 2, 3)) + '</g>')
a(f'<g opacity="0">{vis([(D - 0.3, D - 0.01)])}' + ''.join(
    f'<rect x="{BX + LEVELS[i][1] * 1.06 + 10:.0f}" y="{RY(i) + 7}" width="14" height="14" rx="2" fill="{BLUE}"/>' for i in (1, 2, 3)) + '</g>')

# the result
YR = RY(7) + 22
a(text(20, YR, 'first read', size=14, fill=MUTED)); a(text(20, YR + 20, 'RAM, 3 min', size=15, fill=INK))
a(text(380, YR, 'read again', anchor='end', size=14, fill=MUTED)); a(text(380, YR + 20, 'L1 copy, 4 s', anchor='end', size=15, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('Each level down is bigger and far slower: at a scale where a register answers in one second, a hard disk takes six months. '
           'A cache keeps a copy of what was just read, so reading it again costs seconds, not minutes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> One register access, about 0.3 ns, becomes one second; every other time keeps its ratio to it. Bar length is size, each step about ten times the last.</li>
          <li><b>A miss.</b> The first read looks in L1, L2 and L3, finds nothing, and waits for RAM: about 60 ns.</li>
          <li><b>A copy.</b> On the way back each cache keeps a copy of the data and its neighbours (the blue squares).</li>
          <li><b>A hit.</b> The next read of the same data, or of data next to it, stops at L1: about 1.2 ns.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-15">
      <div class="diagram-label">Fig 1.15 · The hierarchy of forgetting · bigger and slower at every step</div>
      {svg}
      <p id="ch1-memory-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-15', 'ch1-memory-p3', card)
