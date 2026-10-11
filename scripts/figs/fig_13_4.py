# Fig 13.4 · Nested-loop · hash · merge: three ways to do the same join (Pass 28, law 3). Strongroom dossier plate.
# One small equality join, R keys 3 7 1 9 4 against S keys 4 1 8 3 6 (matches 1, 3, 4), run three ways. Nested loop:
# every pair, a 5 × 5 grid lit cell by cell, 25 comparisons. Hash join: R's keys dropped into buckets (key mod 4),
# then each S key probes one bucket: 5 inserts + 5 probes. Merge join: both lists sorted, two pointers walk them,
# 6 comparisons. Lock-step, one panel after another. t=0 (shift): all three done, matches marked.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

R, S = [3, 7, 1, 9, 4], [4, 1, 8, 3, 6]
MATCH = sorted(set(R) & set(S))
assert MATCH == [1, 3, 4]
# merge join steps over the sorted lists
RS, SS = sorted(R), sorted(S)
steps, i, j = [], 0, 0
while i < len(RS) and j < len(SS):
    steps.append((i, j, RS[i] == SS[j]))
    if RS[i] == SS[j]: i += 1; j += 1
    elif RS[i] < SS[j]: i += 1
    else: j += 1
assert len(steps) == 6
W = 400
D = 16.0
T = Timeline(D, shift=15.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
C = 20                                             # cell size
def cell(x, y, v, col, fill=None, w=C):
    f = f'fill="{fill}" fill-opacity="0.35"' if fill else f'fill="{DCARD}"'
    return f'<rect x="{x}" y="{y}" width="{w - 2}" height="{C - 2}" rx="2" {f} stroke="{col}" stroke-opacity="0.7"/>' + text(x + (w - 2) / 2, y + 14, str(v), anchor='middle', size=13, fill=col, ls='0')
def counter(x, y, t0, big, small):
    a(f'<g opacity="0">{win(t0)}{text(x, y, big, anchor="start", size=16, fill=PARCH, ls="0")}{text(x, y + 18, small, anchor="start", size=13, fill=PMUTED, ls="0")}</g>')
# panel 1: nested loop
Y1 = 20
a(text(10, Y1, 'nested loop: every pair', anchor='start', size=13, fill=SEAL, ls='0'))
GX, GY = 52, Y1 + 32
for k, s in enumerate(S):
    a(text(GX + k * C + 9, GY - 6, str(s), anchor='middle', size=13, fill=BRASS, ls='0'))
for r_, rv in enumerate(R):
    a(text(GX - 12, GY + r_ * C + 14, str(rv), anchor='middle', size=13, fill=SEAL, ls='0'))
    for k, sv in enumerate(S):
        x, y = GX + k * C, GY + r_ * C
        a(f'<rect x="{x}" y="{y}" width="{C - 2}" height="{C - 2}" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.4"/>')
        t0 = 0.6 + 0.12 * (r_ * len(S) + k)
        if rv == sv:
            a(f'<g opacity="0">{win(t0)}<rect x="{x}" y="{y}" width="{C - 2}" height="{C - 2}" rx="2" fill="{SAGE}" fill-opacity="0.8"/></g>')
        else:
            a(f'<g opacity="0">{win(t0)}<rect x="{x + 6}" y="{y + 6}" width="{C - 14}" height="{C - 14}" rx="1" fill="{PMUTED}" fill-opacity="0.45"/></g>')
T1 = 0.6 + 0.12 * 25
counter(200, GY + 40, T1, '25 comparisons', 'one for every pair')
# panel 2: hash join
Y2 = GY + 5 * C + 36
a(text(10, Y2, 'hash join: build, then probe', anchor='start', size=13, fill=SEAL, ls='0'))
BX, BY, BW = 10, Y2 + 12, 92
for b in range(4):
    a(f'<rect x="{BX + b * (BW + 4)}" y="{BY}" width="{BW}" height="{C + 22}" rx="3" fill="none" stroke="{PMUTED}" stroke-opacity="0.5"/>')
    a(text(BX + b * (BW + 4) + 6, BY + 15, f'mod 4 = {b}', anchor='start', size=13, fill=PMUTED, ls='0'))
fill_count = [0] * 4
TB = T1 + 0.6
for k, rv in enumerate(R):
    b = rv % 4
    x = BX + b * (BW + 4) + 6 + fill_count[b] * C; fill_count[b] += 1
    a(f'<g opacity="0">{win(TB + 0.3 * k)}{cell(x, BY + 20, rv, SEAL)}</g>')
PY = BY + C + 34
TPB = TB + 0.3 * len(R) + 0.4
for k, sv in enumerate(S):
    x = BX + 20 + k * 52
    a(cell(x, PY, sv, BRASS))
    b = sv % 4
    t0 = TPB + 0.45 * k
    hit = sv in R
    a(f'<g class="fx" opacity="0">{lit(t0, t0 + 0.4)}<rect x="{BX + b * (BW + 4)}" y="{BY}" width="{BW}" height="{C + 22}" rx="3" fill="none" stroke="{SAGE if hit else OXBLOOD}" stroke-width="2.5"/></g>')
    if hit:
        a(f'<g opacity="0">{win(t0)}<rect x="{x}" y="{PY}" width="{C - 2}" height="{C - 2}" rx="2" fill="{SAGE}" fill-opacity="0.8"/>{text(x + 9, PY + 14, str(sv), anchor="middle", size=13, fill=DCARD, ls="0")}</g>')
T2 = TPB + 0.45 * len(S)
counter(270, PY + 6, T2, '5 + 5', 'inserts, probes')
# panel 3: merge join
Y3 = PY + C + 40
a(text(10, Y3, 'merge join: walk two sorted lists', anchor='start', size=13, fill=SEAL, ls='0'))
MX, MR, MS = 60, Y3 + 12, Y3 + 12 + C + 14
a(text(MX - 14, MR + 14, 'R', anchor='middle', size=13, fill=SEAL, ls='0'))
a(text(MX - 14, MS + 14, 'S', anchor='middle', size=13, fill=BRASS, ls='0'))
for k in range(5):
    a(cell(MX + k * (C + 8), MR, RS[k], SEAL))
    a(cell(MX + k * (C + 8), MS, SS[k], BRASS))
TM = T2 + 0.6
for k, (i_, j_, eq) in enumerate(steps):
    t0 = TM + 0.6 * k
    xi, xj = MX + i_ * (C + 8), MX + j_ * (C + 8)
    a(f'<g class="fx" opacity="0">{lit(t0, t0 + 0.6)}<path d="M{xi + 9},{MR - 2} l-5,-7 h10 Z" fill="{PARCH}"/><path d="M{xj + 9},{MS + C} l-5,7 h10 Z" fill="{PARCH}"/>'
      f'<line x1="{xi + 9}" y1="{MR + C - 2}" x2="{xj + 9}" y2="{MS}" stroke="{SAGE if eq else PMUTED}" stroke-width="2"/></g>')
    if eq:
        a(f'<g opacity="0">{win(t0)}<line x1="{xi + 9}" y1="{MR + C - 2}" x2="{xj + 9}" y2="{MS}" stroke="{SAGE}" stroke-width="2"/></g>')
T3 = TM + 0.6 * len(steps)
counter(220, MR + 16, T3, '6 steps', 'once sorted')
assert T3 + 1.0 < D
H = MS + C + 16
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-5 svgd-part4-5">')
o.insert(1, '<title id="svgt-part4-5">Fig 13.4 · Nested-loop · hash · merge: three ways to do the same join</title>')
o.insert(2, '<desc id="svgd-part4-5">One join of keys 3, 7, 1, 9, 4 against 4, 1, 8, 3, 6, which match on 1, 3 and 4, done three ways. Nested loop compares every pair: 25 comparisons in a five by five grid. '
  'Hash join drops the first list into four buckets by key mod 4, then each key of the second list looks in one bucket: five inserts and five probes. '
  'Merge join sorts both lists and walks them with two pointers, advancing the smaller: six comparisons once sorted.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same equality join, three ways: a nested loop compares every pair, a hash join buckets one side and looks each key of the other up once, and a merge join walks two sorted lists together. '
           'Five rows a side: 25 comparisons against about ten; a million a side: a trillion against a few million.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Nested loop.</b> O(|R| × |S|), yet the right choice when one side is tiny or the inner side has an index on the join key, so each outer row costs one index lookup.</li>
          <li><b>Hash join.</b> O(|R| + |S|) for equality joins, if the smaller side's hash table fits in memory; otherwise it is split into partitions on disk.</li>
          <li><b>Merge join.</b> O(|R| + |S|) after sorting, so it wins when the inputs already arrive sorted, for example from an index. The optimiser picks among the three from table sizes, indexes and the join condition.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-4">
      <div class="diagram-label">Fig 13.4 · Nested-loop · hash · merge: three ways to do the same join</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-4"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-4', cap, card.replace('CAPID', cap))
