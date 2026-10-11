# Fig 13.8 · A B+ tree · range scan walks the leaves left to right (Pass 28, law 3). Strongroom dossier plate. A
# small B+ tree: root [30], internal nodes [15] and [45], four linked leaves [5 10] [15 22] [30 38] [45 52]. The
# query age BETWEEN 20 AND 40 descends root, internal, leaf (three page reads) to the first key ≥ 20, then walks the
# leaf links rightwards emitting 22, 30, 38 and stops at 45. A page-read counter ticks. t=0 (shift): done.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

LEAVES = [(5, 10), (15, 22), (30, 38), (45, 52)]
LO, HI = 20, 40
HITS = [k for lf in LEAVES for k in lf if LO <= k <= HI]
assert HITS == [22, 30, 38]
W = 400
ROOT = (200, 46)
INT = [(100, 116), (300, 116)]
LX = [52, 150, 248, 346]
LY = 192
LW, NW, NH = 84, 56, 30
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
a(text(200, 16, f'WHERE age BETWEEN {LO} AND {HI}', anchor='middle', size=13, fill=SEAL, ls='0'))
def node(cx, cy, s, w, col):
    return (f'<rect x="{cx - w / 2}" y="{cy - NH / 2}" width="{w}" height="{NH}" rx="3" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(cx, cy + 5, s, anchor='middle', size=13, fill=col, ls='0'))
def edge(p, q):
    return f'<line x1="{p[0]}" y1="{p[1] + NH / 2}" x2="{q[0]}" y2="{q[1] - NH / 2}" stroke="{PMUTED}" stroke-opacity="0.7"/>'
for c in INT:
    a(edge(ROOT, c))
for i, lx in enumerate(LX):
    a(edge(INT[i // 2], (lx, LY)))
a(node(*ROOT, '30', NW, PARCH))
a(node(*INT[0], '15', NW, PARCH))
a(node(*INT[1], '45', NW, PARCH))
for i, (lx, (k1, k2)) in enumerate(zip(LX, LEAVES)):
    a(f'<rect x="{lx - LW / 2}" y="{LY - NH / 2}" width="{LW}" height="{NH}" rx="3" fill="{DCARD}" stroke="{BRASS}" stroke-width="1.5"/>')
    a(text(lx - 18, LY + 5, str(k1), anchor='middle', size=13, fill=PSOFT, ls='0'))
    a(text(lx + 18, LY + 5, str(k2), anchor='middle', size=13, fill=PSOFT, ls='0'))
    if i < 3:
        x1, x2 = lx + LW / 2, LX[i + 1] - LW / 2
        a(f'<path d="M{x1},{LY} H{x2 - 1} m-5,-4 l5,4 l-5,4" fill="none" stroke="{BRASS}" stroke-opacity="0.8"/>')
a(text(200, LY + 40, 'leaves linked left to right', anchor='middle', size=13, fill=BRASS, ls='0'))
# the descent: root, internal [15], leaf 2; then the walk along the leaves
VISIT = [(ROOT, NW, 0.8), (INT[0], NW, 1.8), ((LX[1], LY), LW, 2.8), ((LX[2], LY), LW, 4.8), ((LX[3], LY), LW, 6.4)]
for k, ((cx, cy), w, t0) in enumerate(VISIT):
    nxt = VISIT[k + 1][2] if k + 1 < len(VISIT) else 7.6
    a(f'<g class="fx" opacity="0">{lit(t0, nxt)}<rect x="{cx - w / 2 - 3}" y="{cy - NH / 2 - 3}" width="{w + 6}" height="{NH + 6}" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
# keys emitted or rejected
KEYS = [((LX[1] + 18, LY), 22, 3.4, True), ((LX[2] - 18, LY), 30, 5.3, True), ((LX[2] + 18, LY), 38, 5.8, True), ((LX[3] - 18, LY), 45, 6.9, False)]
for (x, y), k, t0, ok in KEYS:
    col = SAGE if ok else OXBLOOD
    a(f'<g opacity="0">{win(t0)}<rect x="{x - 15}" y="{y - 11}" width="30" height="21" rx="3" fill="{col}" fill-opacity="0.85"/>{text(x, y + 5, str(k), anchor="middle", size=13, fill=DCARD, ls="0")}</g>')
# page reads and results
SY = LY + 76
for n, (_, _, t0) in enumerate(VISIT, 1):
    t1 = VISIT[n][2] if n < len(VISIT) else None
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, SY, f"page reads: {n}", anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
a(f'<g opacity="0">{lit(0.31, 0.8)}{text(10, SY, "page reads: 0", anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
for k, (_, key, t0, ok) in enumerate(KEYS):
    s = f'found: {", ".join(str(x) for x in HITS[:k + 1])}' if ok else 'found: 22, 30, 38 · 45 &gt; 40: stop'
    t1 = KEYS[k + 1][2] if k + 1 < len(KEYS) else None
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, SY + 20, s, anchor="start", size=13, fill=SAGE if ok else PSOFT, ls="0")}</g>')
H = SY + 32
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-9 svgd-part4-9">')
o.insert(1, '<title id="svgt-part4-9">Fig 13.8 · A B+ tree · range scan walks the leaves left to right</title>')
o.insert(2, '<desc id="svgd-part4-9">A small B+ tree on age: a root holding 30, internal nodes holding 15 and 45, and four leaves, 5 and 10, 15 and 22, 30 and 38, 45 and 52, linked left to right. '
  'The query for ages 20 to 40 reads the root, the internal node 15 and the leaf holding 22, three page reads, then walks the leaf links: 22, 30 and 38 are found, and 45 ends the scan.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A lookup descends from the root, one page per level, to the leaf holding the first key in range; the scan then walks the linked leaves left to right, emitting keys until one passes the end. '
           'Here: three page reads down and two along (five in all), finding 22, 30 and 38; 45 stops it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Inserts.</b> A full leaf splits in two and pushes a key up to its parent; when the root splits, the tree grows a level at the top, so every leaf stays at the same depth.</li>
          <li><b>Why the links.</b> Only the leaves hold keys with row pointers; linking them turns a range into one descent plus a walk, the cost being the depth plus the matches divided by the leaf size.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-8">
      <div class="diagram-label">Fig 13.8 · A B+ tree · range scan walks the leaves left to right</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-8"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-8', cap, card.replace('CAPID', cap))
