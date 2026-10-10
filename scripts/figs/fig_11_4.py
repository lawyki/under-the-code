# Fig 11.4 · HTTP methods · what they promise, what caches and clients assume (Pass 28, law 3). Chart Room plate.
# Top: the method table (RFC 9110; PATCH per RFC 5789): safe, idempotent, cacheable. Bottom: the property at work.
# A request reaches the server, the reply is lost, the client sends it again. PUT quantity = 3: the state is
# qty 3 either way. POST a new order: two orders. Tokens fly out, back (lost), out again, back. t=0 (shift): the
# end state, qty 3 and orders 2, with the lost reply marked.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
W = 400
CX = (150, 250, 350)                            # column centres: safe, idempotent, cacheable
METHODS = [('GET', GREEN, 'yes', 'yes', 'yes'), ('HEAD', GREEN, 'yes', 'yes', 'yes'),
           ('POST', ROUTE, 'no', 'no', 'rarely'), ('PUT', CYAN, 'no', 'yes', 'no'),
           ('DELETE', CYAN, 'no', 'yes', 'no'), ('PATCH', ROUTE, 'no', 'no*', 'no'),
           ('OPTIONS', GREEN, 'yes', 'yes', 'no')]
HY, R0, RS = 24, 50, 24
o = []; a = o.append
D = 10.0
T = Timeline(D, shift=9.5)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
a(text(14, HY, 'method', anchor='start', size=13, fill=CMUTED, ls='0'))
for x, h in zip(CX, ('safe', 'idempotent', 'cacheable')):
    a(text(x, HY, h, anchor='middle', size=13, fill=CMUTED, ls='0'))
a(f'<line x1="10" y1="{HY + 9}" x2="390" y2="{HY + 9}" stroke="{CMUTED}" stroke-opacity="0.6"/>')
for i, (m, col, *cells) in enumerate(METHODS):
    y = R0 + i * RS
    if i % 2 == 0:
        a(f'<rect x="10" y="{y - 16}" width="380" height="{RS}" fill="#fff" fill-opacity="0.04"/>')
    a(text(14, y, m, anchor='start', size=13, fill=col, ls='0'))
    for x, c in zip(CX, cells):
        a(text(x, y, c, anchor='middle', size=13, fill=GREEN if c == 'yes' else CSOFT if c == 'rarely' else LOSS, ls='0'))
# the property at work: a lost reply and a retry
DY = R0 + 6 * RS + 38
a(text(10, DY, 'The reply is lost; the client sends again:', anchor='start', size=13, fill=CSOFT, ls='0'))
XC, XS0, XS1 = 66, 270, 390                     # path start, server box left, right
XL = 168                                        # where the reply is lost
OUT1, IN1, OUT2, IN2 = (0.8, 1.8), (2.0, 2.8), (3.6, 4.6), (4.8, 5.8)
def lane(y, head, states):
    a(text(10, y - 22, head, anchor='start', size=13, fill=CSOFT, ls='0'))
    a(text(10, y + 5, 'client', anchor='start', size=13, fill=CMUTED, ls='0'))
    a(f'<line x1="{XC}" y1="{y}" x2="{XS0 - 6}" y2="{y}" stroke="{CMUTED}" stroke-dasharray="3 4"/>')
    a(f'<rect x="{XS0}" y="{y - 13}" width="{XS1 - XS0}" height="26" rx="4" fill="#0a1c2d" stroke="{CSOFT}" stroke-opacity="0.6"/>')
    # the lost reply, marked
    a(f'<path d="M{XL - 5},{y - 5} l10,10 M{XL + 5},{y - 5} l-10,10" stroke="{LOSS}" stroke-width="2"/>')
    a(text(XL, y + 22, 'lost', anchor='middle', size=13, fill=LOSS, ls='0'))
    (s0, s1, s2) = states
    mx = (XS0 + XS1) / 2
    a(f'<g opacity="0">{lit(0.31, OUT1[1])}{text(mx, y + 5, s0, anchor="middle", size=13, fill=CSOFT, ls="0")}</g>')
    if s1 == s2:
        a(f'<g opacity="0">{win(OUT1[1])}{text(mx, y + 5, s1, anchor="middle", size=13, fill=GREEN, ls="0")}</g>')
    else:
        a(f'<g opacity="0">{lit(OUT1[1], OUT2[1])}{text(mx, y + 5, s1, anchor="middle", size=13, fill=CSOFT, ls="0")}</g>')
        a(f'<g opacity="0">{win(OUT2[1])}{text(mx, y + 5, s2, anchor="middle", size=13, fill=LOSS, ls="0")}</g>')
    # each arrival flashes the box
    for t in (OUT1[1], OUT2[1]):
        a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (t + 0.5, 0.0), (D, 0.0)])}'
          f'<rect x="{XS0}" y="{y - 13}" width="{XS1 - XS0}" height="26" rx="4" fill="none" stroke="#fff" stroke-width="2"/></g>')
    # tokens: out, back (lost at XL), out again, back
    for (t0, t1), xa, xb, col in ((OUT1, XC, XS0 - 8, CSOFT), (IN1, XS0 - 8, XL, CSOFT), (OUT2, XC, XS0 - 8, CSOFT), (IN2, XS0 - 8, XC, GREEN)):
        a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, xb - xa), (D, xb - xa)], "x")}'
          f'<circle cx="{xa}" cy="{y}" r="5" fill="{col}"/></g></g>')
lane(DY + 44, 'PUT quantity = 3', ('qty 1', 'qty 3', 'qty 3'))
lane(DY + 104, 'POST a new order', ('orders 0', 'orders 1', 'orders 2'))
H = DY + 104 + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-43 svgd-part3-43">')
o.insert(1, '<title id="svgt-part3-43">Fig 11.4 · HTTP methods · what they promise, what caches and clients assume</title>')
o.insert(2, '<desc id="svgd-part3-43">A table of HTTP methods. GET and HEAD are safe, idempotent and cacheable. POST is neither safe nor idempotent and rarely cacheable. '
  'PUT and DELETE are idempotent but not safe or cacheable. PATCH is neither safe nor, in general, idempotent. OPTIONS is safe and idempotent, not cacheable. '
  'Below, a request reaches the server, the reply is lost and the client sends it again. PUT quantity 3 leaves the quantity at 3; POST a new order leaves two orders.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A method is a promise to every cache, proxy and retry loop on the path: a safe one changes nothing, an idempotent one has the same effect sent once or twice. '
           'When a reply is lost and the client sends again, a PUT leaves the quantity at 3, but a POST places a second order.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rest of the table.</b> HEAD is GET without the body; PATCH changes part of a resource; OPTIONS asks what the server allows, and browsers send it as the CORS preflight.</li>
          <li><b>The asterisk.</b> PATCH is idempotent only when its format is: a JSON Merge Patch applied twice gives the same result; a JSON Patch that appends to a list does not.</li>
          <li><b>Caches and retries.</b> A shared cache stores GET responses its headers allow and in practice never a POST's; a retry library resends GETs and PUTs freely but a POST only with an <code>Idempotency-Key</code> the server checks.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-4">
      <div class="diagram-label">Fig 11.4 · HTTP methods · what they promise, what caches and clients assume</div>
      {svg}
      <p id="ch11-http-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-4', 'ch11-http-p9', card)
