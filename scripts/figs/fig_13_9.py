# Fig 13.9 · B-tree vs hash index · which one wins which workload (Pass 28, law 3). Strongroom dossier plate. The same
# eight keys indexed two ways: a B-tree keeps them in order (its leaves, drawn as one sorted row), a hash index puts
# each in bucket 37 × key mod 8, a toy hash. Query 1, id = 43: one descent in the B-tree, one bucket in the hash. Query 2, id BETWEEN
# 40 AND 45: the B-tree finds 40 and reads its neighbours; the hash has scattered 40, 41, 43, 45 across buckets 0,
# 5, 7, 1, so every bucket must be checked. t=0 (shift): query 2 answered.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

KEYS = [12, 27, 40, 41, 43, 45, 58, 71]
NB = 8
h = lambda k: (37 * k) % NB                       # a toy multiplicative hash
BUCKETS = [[k for k in KEYS if h(k) == b] for b in range(NB)]
RANGE = [k for k in KEYS if 40 <= k <= 45]
assert RANGE == [40, 41, 43, 45] and [h(k) for k in RANGE] == [0, 5, 7, 1] and BUCKETS[7] == [27, 43]
W = 400
CX0, CW = 24, 44
cx = lambda i: CX0 + i * CW
D = 11.0
T = Timeline(D, shift=10.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
Q1, Q2 = (0.6, 4.4), (4.4, None)
o = []; a = o.append
a(f'<g opacity="0">{lit(0.31, Q2[0])}{text(200, 16, "WHERE id = 43", anchor="middle", size=13, fill=SEAL, ls="0")}</g>')
a(f'<g opacity="0">{win(Q2[0])}{text(200, 16, "WHERE id BETWEEN 40 AND 45", anchor="middle", size=13, fill=SEAL, ls="0")}</g>')
# the B-tree's sorted row
BY = 52
a(text(CX0, BY - 10, 'B-tree: keys kept in order', anchor='start', size=13, fill=BRASS, ls='0'))
for i, k in enumerate(KEYS):
    a(f'<rect x="{cx(i)}" y="{BY}" width="{CW - 4}" height="26" rx="2" fill="{DCARD}" stroke="{BRASS}" stroke-opacity="0.7"/>')
    a(text(cx(i) + (CW - 4) / 2, BY + 18, str(k), anchor='middle', size=13, fill=PSOFT, ls='0'))
def hit(x, y, w, h, t0, t1, col):
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="2"/>'
    a(f'<g class="fx" opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{body}</g>')
# the hash buckets
HY = 124
a(text(CX0, HY - 24, 'hash: bucket = 37 × id mod 8', anchor='start', size=13, fill=OXBLOOD, ls='0'))
for b in range(NB):
    a(text(cx(b) + (CW - 4) / 2, HY - 6, str(b), anchor='middle', size=13, fill=PMUTED, ls='0'))
    a(f'<rect x="{cx(b)}" y="{HY}" width="{CW - 4}" height="44" rx="2" fill="{DCARD}" stroke="{OXBLOOD}" stroke-opacity="0.7"/>')
    for j, k in enumerate(BUCKETS[b]):
        a(text(cx(b) + (CW - 4) / 2, HY + 18 + j * 18, str(k), anchor='middle', size=13, fill=PSOFT, ls='0'))
# query 1: id = 43
i43 = KEYS.index(43)
hit(cx(i43), BY, CW - 4, 26, 1.4, Q1[1], SAGE)
hit(cx(h(43)), HY, CW - 4, 44, 1.8, Q1[1], SAGE)
# query 2: the range
for n, k in enumerate(RANGE):
    hit(cx(KEYS.index(k)), BY, CW - 4, 26, 5.0 + 0.3 * n, None, SAGE)
for b in range(NB):
    t0 = 5.0 + 0.45 * b
    col = SAGE if any(40 <= k <= 45 for k in BUCKETS[b]) else PMUTED
    hit(cx(b), HY, CW - 4, 44, t0, None, col)
T2B, T2H = 5.0 + 0.3 * 4, 5.0 + 0.45 * NB
# results
RY = HY + 76
for t0, t1, s, col in ((1.4, Q2[0], 'B-tree: one descent', SAGE), (5.0, T2B, 'B-tree: descend to 40…', PSOFT), (T2B, None, 'B-tree: descend, then 3 neighbours', SAGE)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(CX0, RY, s, anchor="start", size=13, fill=col, ls="0")}</g>')
for t0, t1, s, col in ((1.8, Q2[0], 'hash: one bucket', SAGE), (5.0, T2H, 'hash: checking every bucket…', PSOFT), (T2H, None, 'hash: all 8 buckets, no order', OXBLOOD)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(CX0, RY + 20, s, anchor="start", size=13, fill=col, ls="0")}</g>')
assert T2H + 0.8 < D
H = RY + 32
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-10 svgd-part4-10">')
o.insert(1, '<title id="svgt-part4-10">Fig 13.9 · B-tree vs hash index · which one wins which workload</title>')
o.insert(2, '<desc id="svgd-part4-10">The keys 12, 27, 40, 41, 43, 45, 58 and 71 indexed two ways. A B-tree keeps them in order; a hash index puts each in bucket 37 times key mod 8, so 27 and 43 share bucket 7. '
  'Looking up 43 takes one descent in the B-tree and one bucket in the hash. The range 40 to 45 is one descent and three neighbours in the B-tree, but the hash has scattered those keys across buckets 0, 5, 7 and 1, so every bucket must be checked.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Both indexes find a single key in a step or two; a range is where they part. '
           'The B-tree keeps keys in order, so 40 to 45 sit side by side, while hashing scatters them across the buckets and the only way to find them is to look in every one.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>B-tree.</b> O(log N) to find a key, plus k to read k neighbours; it also serves <code>ORDER BY</code> and prefix matches such as <code>LIKE 'Al%'</code>.</li>
          <li><b>Hash.</b> O(1) on average for equality, nothing for ranges or order (the toy hash here is 37 × id mod 8; real ones scramble harder). PostgreSQL's hash indexes are crash-safe (WAL-logged) since version 10, yet almost every index people create is a B-tree.</li>
          <li><b>The cost of any index.</b> Every insert and update must keep each index in step, so too many indexes slow every write.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-9">
      <div class="diagram-label">Fig 13.9 · B-tree vs hash index · which one wins which workload</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-9"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-9', cap, card.replace('CAPID', cap))
