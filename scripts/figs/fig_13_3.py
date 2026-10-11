# Fig 13.3 · Same query, three forms · SQL → relational algebra → execution plan (Pass 28, law 3). Strongroom
# dossier plate. The SQL on top; below it the algebra tree as parsed (π over σ age > 18 over the join of users and
# orders); the optimiser pushes σ below the join, onto users, since the test uses only users' columns; then the plan
# stamps its choices onto the nodes: an index scan on age, a full scan of orders, a hash join. t=0 (shift): the
# rewritten tree with the plan.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
SQL = [('SELECT', ' u.name, o.product'), ('FROM', ' users u JOIN orders o'), ('', '  ON u.id = o.user_id'), ('WHERE', ' u.age &gt; 18;')]
NB = {'pi': (200, 132), 'join': (200, 232), 'users': (110, 330), 'orders': (290, 330)}
SIG0, SIG1 = (200, 182), (110, 282)              # σ before and after the rewrite
NW, NH = 140, 30
D = 11.0
T = Timeline(D, shift=10.4)
TM0, TM1 = 2.0, 3.6                               # σ moves
TP = [4.6, 5.2, 5.8]                             # plan stamps
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<rect x="10" y="8" width="380" height="{18 * len(SQL) + 12}" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.6"/>')
for i, (kw, rest) in enumerate(SQL):
    a(text(20, 26 + 18 * i, f'<tspan fill="{SEAL}">{kw}</tspan>{rest}', anchor='start', size=13, fill=PSOFT, ls='0'))
def node(cx, cy, s, col):
    return (f'<rect x="{cx - NW / 2}" y="{cy - NH / 2}" width="{NW}" height="{NH}" rx="3" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(cx, cy + 5, s, anchor='middle', size=13, fill=col, ls='0'))
def edge(p, q):
    return f'<line x1="{p[0]}" y1="{p[1] + NH / 2}" x2="{q[0]}" y2="{q[1] - NH / 2}" stroke="{PMUTED}" stroke-width="1.5"/>'
# edges before the rewrite, then after
before = edge(NB['pi'], SIG0) + edge(SIG0, NB['join']) + edge(NB['join'], NB['users'])
after = edge(NB['pi'], NB['join']) + edge(NB['join'], SIG1) + edge(SIG1, NB['users'])
a(f'<g opacity="0">{lit(0.31, TM1)}{before}</g><g opacity="0">{win(TM1)}{after}</g>')
a(edge(NB['join'], NB['orders']))
a(node(*NB['pi'], 'π name, product', PARCH))
a(node(*NB['join'], '⨝ id = user_id', OXBLOOD))
a(node(*NB['users'], 'users', BRASS))
a(node(*NB['orders'], 'orders', BRASS))
dx, dy = SIG1[0] - SIG0[0], SIG1[1] - SIG0[1]
mvx = T.translate([(0.0, dx), (0.3, dx), (0.305, 0.0), (TM0, 0.0), (TM1, dx), (D, dx)], 'x')
mvy = T.translate([(0.0, dy), (0.3, dy), (0.305, 0.0), (TM0, 0.0), (TM1, dy), (D, dy)], 'y')
a(f'<g class="fx"><g>{mvx}<g>{mvy}{node(*SIG0, "σ age &gt; 18", SEAL)}</g></g></g>')
# the plan, stamped on
PLAN = [(NB['users'], 'full scan + filter', TP[0], 'below'), (NB['orders'], 'full scan', TP[1], 'below'), (NB['join'], 'hash join', TP[2], 'right')]
for (cx, cy), s, t0, where in PLAN:
    x, y, anc = (cx, cy + NH / 2 + 18, 'middle') if where == 'below' else (cx + NW / 2 + 10, cy + 5, 'start')
    lab = text(x, y, s, anchor=anc, size=13, fill=STAMP if False else SEAL, ls='0')
    a(f'<g opacity="0">{win(t0)}{lab}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="{cx - NW / 2 - 3}" y="{cy - NH / 2 - 3}" width="{NW + 6}" height="{NH + 6}" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
# what stage we are in
SY = NB['users'][1] + NH / 2 + 46
for t0, t1, s in ((0.31, TM0, 'parsed: the algebra tree'), (TM0, TP[0], 'optimiser: push σ down'), (TP[0], None, 'plan: what actually runs')):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, SY, s, anchor="start", size=13, fill=PSOFT, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-4 svgd-part4-4">')
o.insert(1, '<title id="svgt-part4-4">Fig 13.3 · Same query, three forms · SQL → relational algebra → execution plan</title>')
o.insert(2, '<desc id="svgd-part4-4">The query SELECT u.name, o.product FROM users u JOIN orders o ON u.id = o.user_id WHERE u.age > 18. '
  'Parsed, it becomes a tree: a projection of name and product over a selection of age greater than 18 over the join of users and orders. '
  'The optimiser moves the selection below the join, onto users, because the test uses only users\' columns. Then the plan is chosen: a full scan of users with the age test applied as rows stream by, a full scan of orders, and a hash join.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The SQL is parsed into an algebra tree, and the optimiser rewrites the tree before anything runs: here it moves the age filter below the join, so only adults are joined, then picks how to run each node. '
           'The plan, not the SQL, decides how fast the query is.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rewrite.</b> Filtering first gives the same answer with fewer rows to join: σ(R ⨝ S) = σ(R) ⨝ S whenever the test uses only R's columns.</li>
          <li><b>The choices.</b> Statistics on table sizes and value spread decide each step: an index on age only if few rows pass (here nearly everyone is an adult, so scanning wins), a hash join when both inputs are large (Fig 13.4).</li>
          <li><b>Seeing it.</b> <code>EXPLAIN</code> in PostgreSQL or MySQL prints the plan the engine chose.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-3">
      <div class="diagram-label">Fig 13.3 · Same query, three forms · SQL → relational algebra → execution plan</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-3"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-3', cap, card.replace('CAPID', cap))
