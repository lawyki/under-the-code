# Fig 13.2 · Three operators · selection, projection, join (Pass 28, law 3). Strongroom dossier plate. Three panels
# on small real tables. σ age > 18 (users): each row is checked in turn, the passing ones copied to the result.
# π name (users): the other columns fall away. users ⨝ orders on id = user_id: each order finds its user and a
# combined row is written. Lock-step motion, one row at a time. t=0 (shift): all three results written.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

USERS = [(1, 'Alice', 31), (2, 'Bob', 14), (3, 'Cara', 42), (4, 'Dan', 17)]
ORDERS = [(1, 'lamp'), (3, 'desk'), (1, 'pen')]
SEL = [u for u in USERS if u[2] > 18]
JOIN = [(next(u[1] for u in USERS if u[0] == uid), item) for uid, item in ORDERS]
assert [u[1] for u in SEL] == ['Alice', 'Cara'] and JOIN == [('Alice', 'lamp'), ('Cara', 'desk'), ('Alice', 'pen')]
W = 400
RH = 18
D = 14.0
T = Timeline(D, shift=13.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
dimto = lambda t0, lo: T.anim('opacity', [(0.0, lo), (0.3, lo), (0.305, 1.0), (t0 - 0.002, 1.0), (t0, lo), (D, lo)])
o = []; a = o.append
def table(x, y, cols, rows, colw, col, head_col=None):
    """draw a table; returns the y of each row's baseline."""
    wsum = sum(colw)
    a(f'<rect x="{x}" y="{y}" width="{wsum}" height="{RH * (len(rows) + 1) + 6}" rx="2" fill="{DCARD}" stroke="{col}" stroke-opacity="0.6"/>')
    cx = x
    for c, w in zip(cols, colw):
        a(text(cx + 6, y + 15, c, anchor='start', size=13, fill=head_col or col, ls='0'))
        cx += w
    a(f'<line x1="{x}" y1="{y + RH + 3}" x2="{x + wsum}" y2="{y + RH + 3}" stroke="{col}" stroke-opacity="0.4"/>')
    return [y + RH * (i + 2) + 2 for i in range(len(rows))]
def cells(x, ys, rows, colw, fill, wrap=None):
    out = []
    for yb, r in zip(ys, rows):
        cx, s = x, ''
        for v, w in zip(r, colw):
            s += text(cx + 6, yb, str(v), anchor='start', size=13, fill=fill, ls='0'); cx += w
        out.append(s)
    return out
# panel 1: selection
Y1 = 26
a(text(10, Y1 - 8, 'σ age > 18: keep rows', anchor='start', size=13, fill=SEAL, ls='0'))
UW = [28, 60, 40]
ys = table(10, Y1, ('id', 'name', 'age'), USERS, UW, SEAL)
rs = table(270, Y1, ('id', 'name', 'age'), SEL, UW, SEAL)
src = cells(10, ys, USERS, UW, PSOFT)
k = 0
for i, (u, s) in enumerate(zip(USERS, src)):
    t = 0.8 + 0.7 * i
    keep = u[2] > 18
    if keep:
        a(f'<g>{s}</g>')
        a(f'<g class="fx" opacity="0">{lit(t, t + 0.6)}<rect x="11" y="{ys[i] - 13}" width="{sum(UW) - 2}" height="{RH}" fill="{SAGE}" fill-opacity="0.25"/></g>')
        a(f'<g opacity="0">{win(t + 0.3)}{cells(270, [rs[k]], [u], UW, PSOFT)[0]}</g>')
        k += 1
    else:
        a(f'<g opacity="1">{dimto(t + 0.3, 0.3)}{s}</g>')
        a(f'<g opacity="0">{win(t + 0.3)}<line x1="14" y1="{ys[i] - 4}" x2="{10 + sum(UW) - 4}" y2="{ys[i] - 4}" stroke="{OXBLOOD}" stroke-width="1.5"/></g>')
a(f'<path d="M{10 + sum(UW) + 14},{Y1 + 50} H{262} m-6,-4 l6,4 l-6,4" fill="none" stroke="{PMUTED}"/>')
# panel 2: projection
Y2 = Y1 + RH * 5 + 46
a(text(10, Y2 - 8, 'π name: keep columns', anchor='start', size=13, fill=BRASS, ls='0'))
ys2 = table(10, Y2, ('id', 'name', 'age'), USERS, UW, BRASS)
rs2 = table(270, Y2, ('name',), USERS, [UW[1] + 20], BRASS)
TP = 4.2
for i, u in enumerate(USERS):
    a(f'<g opacity="1">{dimto(TP, 0.25)}{text(16, ys2[i], str(u[0]), anchor="start", size=13, fill=PSOFT, ls="0")}{text(10 + UW[0] + UW[1] + 6, ys2[i], str(u[2]), anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
    a(text(10 + UW[0] + 6, ys2[i], u[1], anchor='start', size=13, fill=PSOFT, ls='0'))
    a(f'<g opacity="0">{win(TP + 0.5 + 0.2 * i)}{text(276, rs2[i], u[1], anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
a(f'<g opacity="0">{win(TP)}<rect x="{10 + UW[0]}" y="{Y2}" width="{UW[1]}" height="{RH * 5 + 6}" fill="none" stroke="{BRASS}" stroke-width="2"/></g>')
a(f'<path d="M{10 + sum(UW) + 14},{Y2 + 50} H{262} m-6,-4 l6,4 l-6,4" fill="none" stroke="{PMUTED}"/>')
# panel 3: join
Y3 = Y2 + RH * 5 + 46
a(text(10, Y3 - 8, '⨝ id = user_id: pair rows', anchor='start', size=13, fill=OXBLOOD, ls='0'))
JW, OW, RW = [28, 60], [72, 50], [60, 50]
OX, RX = 110, 278
ysu = table(10, Y3, ('id', 'name'), USERS, JW, SEAL)
yso = table(OX, Y3, ('user_id', 'item'), ORDERS, OW, OXBLOOD)
ysr = table(RX, Y3, ('name', 'item'), JOIN, RW, OXBLOOD)
for i, u in enumerate(USERS):
    a(cells(10, [ysu[i]], [u[:2]], JW, PSOFT)[0])
for j, (o_, (uid, item)) in enumerate(zip(ORDERS, ORDERS)):
    a(cells(OX, [yso[j]], [(uid, item)], OW, PSOFT)[0])
    t = 6.4 + 1.1 * j
    ui = next(i for i, u in enumerate(USERS) if u[0] == uid)
    a(f'<g class="fx" opacity="0">{lit(t, t + 0.9)}<path d="M{OX},{yso[j] - 4} L{10 + sum(JW)},{ysu[ui] - 4}" stroke="{STAMP}" stroke-width="2"/>'
      f'<rect x="11" y="{ysu[ui] - 13}" width="{sum(JW) - 2}" height="{RH}" fill="{STAMP}" fill-opacity="0.2"/>'
      f'<rect x="{OX + 1}" y="{yso[j] - 13}" width="{sum(OW) - 2}" height="{RH}" fill="{STAMP}" fill-opacity="0.2"/></g>')
    a(f'<g opacity="0">{win(t + 0.5)}{cells(RX, [ysr[j]], [JOIN[j]], RW, PSOFT)[0]}</g>')
H = Y3 + RH * 5 + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-3 svgd-part4-3">')
o.insert(1, '<title id="svgt-part4-3">Fig 13.2 · Three operators · selection, projection, join</title>')
o.insert(2, '<desc id="svgd-part4-3">Three operations on small tables. Selection, age greater than 18, on a users table of Alice 31, Bob 14, Cara 42 and Dan 17: each row is checked and Alice and Cara are kept. '
  'Projection on name: the id and age columns fall away, leaving the four names. Join on id equals user_id between users and an orders table of lamp, desk and pen: each order finds its user, giving Alice lamp, Cara desk, Alice pen.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Selection keeps the rows that pass a test, projection keeps the columns you name, and a join pairs the rows of two tables that agree on a value. '
           'Each takes tables and returns a table, so the output of one can feed the next: that closure is what lets SQL queries nest.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>In SQL.</b> σ is the <code>WHERE</code> clause, π the column list after <code>SELECT</code>, ⨝ a <code>JOIN … ON</code>.</li>
          <li><b>Sets and bags.</b> In the algebra a relation is a set, so π drops duplicate rows; SQL keeps them unless you write <code>DISTINCT</code>.</li>
          <li><b>The rest of the algebra.</b> Its fundamental operators are selection, projection, union, difference, Cartesian product and rename; a join is a product followed by a selection, common enough to get its own symbol.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-2">
      <div class="diagram-label">Fig 13.2 · Three operators · selection, projection, join</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-2"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-2', cap, card.replace('CAPID', cap))
