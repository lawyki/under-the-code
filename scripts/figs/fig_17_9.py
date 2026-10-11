# Fig 17.9 · Monolith vs microservices · same business logic, different deployment (Pass 28, law 3). Quorum glass plate.
# One checkout traced both ways on the same beats: orders → auth → payment. In the monolith each step is a function call
# inside one process, sharing one database. In microservices each step is a network call between separately deployed
# services, each with its own database; the payment call times out once and is retried. t=0 (shift): both done.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
MODS = ['orders', 'auth', 'payment']
MX = [70, 200, 330]
def fly(x0, x1, y, t0, t1, col):
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)], "x")}<circle cx="{x0}" cy="{y}" r="5" fill="{col}"/></g></g>')
# monolith
a(text(10, 18, 'monolith: one process, one database', anchor='start', size=13, fill=VIOLET, ls='0'))
a(f'<rect x="10" y="28" width="380" height="66" rx="12" fill="none" stroke="{VIOLET}" stroke-opacity="0.6"/>')
for x, m in zip(MX, MODS):
    a(f'<rect x="{x - 52}" y="38" width="104" height="30" rx="6" fill="{QCARD}" stroke="{VIOLET}" stroke-opacity="0.7"/>' + text(x, 58, m, anchor='middle', size=13, fill=QSOFT, ls='0'))
a(text(200, 86, 'one database', anchor='middle', size=13, fill=QMUTED, ls='0'))
T1 = [(1.0, 1.4), (1.6, 2.0)]
for k, (t0, t1) in enumerate(T1):
    fly(MX[k] + 52, MX[k + 1] - 52, 53, t0, t1, VIOLET)
a(f'<g opacity="0">{win(2.0)}{text(10, 116, "2 function calls: done", anchor="start", size=13, fill=VIOLET, ls="0")}</g>')
# microservices
Y0 = 150
a(text(10, Y0, 'microservices: three services, three databases', anchor='start', size=13, fill=TEAL, ls='0'))
for x, m in zip(MX, MODS):
    a(f'<rect x="{x - 52}" y="{Y0 + 12}" width="104" height="56" rx="10" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="0.7"/>' + text(x, Y0 + 34, m, anchor='middle', size=13, fill=QSOFT, ls='0'))
    a(text(x, Y0 + 56, 'own DB', anchor='middle', size=13, fill=QMUTED, ls='0'))
NY = Y0 + 27
fly(MX[0] + 52, MX[1] - 52, NY, 1.0, 2.2, TEAL)
fly(MX[1] + 52, MX[2] - 52, NY, 2.6, 3.8, TEAL)                       # first try: lost
a(f'<g opacity="0">{lit(3.8, 6.0)}<path d="M{MX[2] - 64},{NY - 8} l12,12 M{MX[2] - 52},{NY - 8} l-12,12" stroke="{QROSE}" stroke-width="2.5"/></g>')
a(f'<g opacity="0">{lit(4.0, 5.2)}{text(10, Y0 + 92, "payment call timed out: retry", anchor="start", size=13, fill=QROSE, ls="0")}</g>')
fly(MX[1] + 52, MX[2] - 52, NY, 5.2, 6.4, TEAL)                       # retry
a(f'<g opacity="0">{win(6.4)}{text(10, Y0 + 92, "2 network calls, 1 retry: done", anchor="start", size=13, fill=TEAL, ls="0")}</g>')
H = Y0 + 104
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-22 svgd-part5-22">')
o.insert(1, '<title id="svgt-part5-22">Fig 17.9 · Monolith vs microservices · same business logic, different deployment</title>')
o.insert(2, '<desc id="svgd-part5-22">One checkout, orders then auth then payment, traced two ways. In a monolith the three are modules in one process sharing one database, and each step is a function call. '
  'As microservices they are three separately deployed services, each with its own database, and each step is a network call; here the call to payment times out and has to be retried.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same checkout, built two ways: inside a monolith each step is a function call that cannot get lost; between microservices each is a network call that can time out and has to be retried. '
           'In return each service deploys, scales and fails on its own.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>What it buys.</b> Teams ship their service on their own schedule, in their own language, and a crash in one service need not take down the rest.</li>
          <li><b>What it costs.</b> Every former function call can be slow or fail; one order spans several databases, so it needs a saga of steps and compensations instead of one transaction; following a request takes distributed tracing.</li>
          <li><b>The usual advice.</b> Split only where a team needs that independence; a well-structured monolith is the cheaper default.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-9">
      <div class="diagram-label">Fig 17.9 · Monolith vs microservices · same business logic, different deployment</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-9"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-9', cap, card.replace('CAPID', cap))
