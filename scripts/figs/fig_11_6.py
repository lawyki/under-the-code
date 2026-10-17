# Fig 11.6 · Recursive resolution · four servers, four questions, one answer (Pass 28, law 3). Chart Room plate.
# A cold lookup of example.com. The laptop asks its resolver; the resolver asks the root (referral: ask com), the
# com servers (referral: ask example.com's servers), then example.com's own servers (the address); it caches the
# answer and hands it to the laptop. Tokens run the walk; each server's reply lights as the question lands; the
# resolver's cache fills. t=0 (shift): the walk done, every reply lit, the answer cached and delivered.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, BLUE = '#9bd89b', '#86a8ff'
W = 400
SX0, SX1 = 214, 390                              # server column
SRV = [(58, 'root (.)', '→ ask com', CYAN), (138, 'com servers', '→ ask example.com', GREEN), (218, 'example.com', '→ the address', BLUE)]
SBH = 50
RX0, RX1, RY = 10, 158, 138                      # resolver
LY = 268                                         # laptop
D = 9.5
T = Timeline(D, shift=8.9)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
H = LY + 40
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-45 svgd-part3-45">')
a('<title id="svgt-part3-45">Fig 11.6 · Recursive resolution · four servers, four questions, one answer</title>')
a('<desc id="svgd-part3-45">A cold DNS lookup of example.com. The laptop asks its resolver once. The resolver asks a root server, which refers it to the com servers; '
  'asks a com server, which refers it to example.com\'s own servers; and asks one of those, which returns the address. The resolver caches the answer and passes it to the laptop.</desc>')
# links
rr = (RX1, RY)
for y, *_ in SRV:
    a(f'<line x1="{RX1}" y1="{RY}" x2="{SX0}" y2="{y}" stroke="{CMUTED}" stroke-opacity="0.6" stroke-dasharray="3 4"/>')
lx = (RX0 + RX1) / 2
a(f'<line x1="{lx}" y1="{RY + 34}" x2="{lx}" y2="{LY - 22}" stroke="{CMUTED}" stroke-opacity="0.6" stroke-dasharray="3 4"/>')
# servers: the reply lights when the question lands
legs = []                                        # (t0, t1, from, to, colour)
t = 1.4
for y, name, reply, col in SRV:
    a(f'<rect x="{SX0}" y="{y - SBH / 2}" width="{SX1 - SX0}" height="{SBH}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(SX0 + 10, y - 4, name, anchor='start', size=13, fill=col, ls='0'))
    a(f'<g opacity="0.3">{text(SX0 + 10, y + 15, reply, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{win(t + 0.6)}{text(SX0 + 10, y + 15, reply, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
    legs += [(t, t + 0.6, rr, (SX0 - 6, y), CSOFT), (t + 0.7, t + 1.3, (SX0 - 6, y), rr, col)]
    t += 1.5
TC = t - 0.2                                     # answer cached
TA = (TC + 0.2, TC + 0.8)                        # resolver to laptop
# resolver
a(f'<rect x="{RX0}" y="{RY - 34}" width="{RX1 - RX0}" height="68" rx="5" fill="#0a1c2d" stroke="{CSOFT}" stroke-opacity="0.7"/>')
a(text(RX0 + 10, RY - 12, 'resolver', anchor='start', size=13, fill=CSOFT, ls='0'))
a(text(RX0 + 10, RY + 6, 'ISP or 1.1.1.1', anchor='start', size=13, fill=CMUTED, ls='0'))
a(f'<g opacity="0">{lit(0.31, TC)}{text(RX0 + 10, RY + 24, "cache: empty", anchor="start", size=13, fill=CMUTED, ls="0")}</g>')
a(f'<g opacity="0">{win(TC)}{text(RX0 + 10, RY + 24, "cache: 1 hour", anchor="start", size=13, fill=BLUE, ls="0")}</g>')
# laptop
a(f'<rect x="{RX0}" y="{LY - 22}" width="{RX1 - RX0}" height="44" rx="5" fill="#0a1c2d" stroke="{ROUTE}" stroke-opacity="0.7"/>')
a(text(RX0 + 10, LY - 3, 'laptop', anchor='start', size=13, fill=ROUTE, ls='0'))
a(f'<g opacity="0">{lit(0.31, TA[1])}{text(RX0 + 10, LY + 14, "example.com?", anchor="start", size=13, fill=CMUTED, ls="0")}</g>')
a(f'<g opacity="0">{win(TA[1])}{text(RX0 + 10, LY + 14, "has the address", anchor="start", size=13, fill=BLUE, ls="0")}</g>')
a(text(lx + 10, (RY + 34 + LY - 22) / 2 + 5, 'asks once', anchor='start', size=13, fill=CMUTED, ls='0'))
legs = [(0.6, 1.2, (lx, LY - 22), (lx, RY + 34), ROUTE)] + legs + [(TA[0], TA[1], (lx, RY + 34), (lx, LY - 22), BLUE)]
for t0, t1, (xa, ya), (xb, yb), col in legs:
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, xb - xa), (D, xb - xa)], "x")}'
      f'<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, yb - ya), (D, yb - ya)], "y")}<circle cx="{xa}" cy="{ya}" r="5" fill="{col}"/></g></g></g>')
assert TA[1] < D - 1.0
a('</svg>')
svg = '\n'.join(o)

caption = ("Only the resolver walks the tree; the laptop asks once and gets one answer. Held in the resolver's cache for an hour, that answer spares the next asker the whole walk.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Referrals.</b> The root and <code>com</code> servers do not know the address; they reply with the names and addresses of the servers one level down.</li>
          <li><b>On the wire.</b> Queries go over UDP port 53. If an answer is too big for the UDP size the asker offered (512 bytes without EDNS), the server marks it truncated and the asker repeats the query over TCP. DNS over HTTPS and over TLS carry the same messages encrypted.</li>
          <li><b>The cache.</b> A busy resolver already holds the root and <code>com</code> referrals, so most lookups skip to the last step or need no walk at all.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-6">
      <div class="diagram-label">Fig 11.6 · Recursive resolution · four servers, four questions, one answer</div>
      {svg}
      <p id="ch11-dns-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-6', 'ch11-dns-p6', card)
