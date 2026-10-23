# Fig 9.12 · A route leak (Pass 28, law 3). Chart Room. Customer C buys transit from P1 and P2. Run 1:
# traffic goes SRC -> P1 -> P2 -> DST over the providers' direct link. C then leaks P2's routes to P1;
# P1 prefers routes learned from a customer, and run 2's traffic squeezes through C's thin links.
# t=0 (shift): the detour.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 300
BW, BH = 100, 40
P1, P2, C = (24, 52), (276, 52), (150, 150)
SRC, DST = (24, 224), (276, 224)
def mid(b, side):
    x, y = b
    return {'top': (x + BW / 2, y), 'bot': (x + BW / 2, y + BH), 'l': (x, y + BH / 2), 'r': (x + BW, y + BH / 2)}[side]
D = 12.0
RUN1, LEAK, RUN2 = 0.6, 4.2, 6.0
T = Timeline(D, shift=RUN2 + 2.2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-26 svgd-part3-26">')
a('<title id="svgt-part3-26">Fig 9.12 · A route leak: traffic takes the wrong door</title>')
a('<desc id="svgd-part3-26">Two large providers, P1 and P2, connected directly; a small customer network C buys transit from both. Traffic from a source behind P1 to a destination behind P2 normally crosses the direct P1 to P2 link. '
  'Then C mistakenly passes the routes it learned from P2 on to P1. P1 prefers routes learned from a paying customer, so the traffic now detours through C\'s two thin links, which cannot carry it.</desc>')
# links
(x1, y1), (x2, y2) = mid(P1, 'r'), mid(P2, 'l')
a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="6"/>')
a(text(200, y1 - 12, 'direct, wide', anchor='middle', size=13, fill=CMUTED, ls='0'))
for b, side in ((P1, 'bot'), (P2, 'bot')):
    (x1, y1), (x2, y2) = mid(b, side), mid(C, 'l' if b == P1 else 'r')
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CSOFT}" stroke-opacity="0.4" stroke-width="1.5"/>')
for b, s in ((P1, SRC), (P2, DST)):
    (x1, y1), (x2, y2) = mid(b, 'bot'), mid(s, 'top')
    a(f'<line x1="{x1}" y1="{y1 + 0}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="3"/>')
for (x, y), lab, col in ((P1, 'P1', CSOFT), (P2, 'P2', CSOFT), (C, 'C · small', ROUTE), (SRC, 'source', CSOFT), (DST, 'destination', CSOFT)):
    a(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="2" fill="{CDEEP}" stroke="{col}" stroke-opacity="0.8"/>')
    a(text(x + BW / 2, y + (17 if lab.startswith('C') else 25), lab, anchor='middle', size=13, fill='#fff', ls='0'))
# the leak: C tells P1 about P2's routes
(lx1, ly1), (lx2, ly2) = mid(C, 'top'), mid(P1, 'r')
a(f'<g opacity="0">{win(LEAK, D - 0.3)}<path d="M{lx1} {ly1} Q{lx1 - 10} {ly2 + 30} {lx2 + 6} {ly2 + 12}" fill="none" stroke="{ROUTE}" stroke-width="2.5" stroke-dasharray="6 4">'
  f'<animate attributeName="stroke-dashoffset" values="0;-20" dur="1s" repeatCount="indefinite"/></path>'
  f'{text(200, 212, "leaked route", anchor="middle", size=13, fill=ROUTE, ls="0")}</g>')
# packets
def flow(pts, t0, t1, col, n=4):
    for k in range(n):
        s = t0 + k * 0.35
        kx = [(0.0, 0.0), (s, 0.0)]; ky = [(0.0, 0.0), (s, 0.0)]
        seg = 1.4 / (len(pts) - 1)
        for i, (x, y) in enumerate(pts[1:], 1):
            kx.append((s + i * seg, x - pts[0][0])); ky.append((s + i * seg, y - pts[0][1]))
        kx.append((D, kx[-1][1])); ky.append((D, ky[-1][1]))
        a(f'<g class="fx" opacity="0">{win(s, s + 1.4)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="5" fill="{col}"/></g></g></g>')
normal = [mid(SRC, 'top'), mid(P1, 'bot'), mid(P1, 'r'), mid(P2, 'l'), mid(P2, 'bot'), mid(DST, 'top')]
detour = [mid(SRC, 'top'), mid(P1, 'bot'), (C[0], C[1] + 31), (C[0] + BW, C[1] + 31), mid(P2, 'bot'), mid(DST, 'top')]   # under C's label
flow(normal, RUN1, LEAK - 0.4, CYAN)
flow(detour, RUN2, D - 0.4, RED, n=8)
a(f'<rect class="fx" x="{C[0] - 3}" y="{C[1] - 3}" width="{BW + 6}" height="{BH + 6}" rx="3" fill="none" stroke="{RED}" stroke-width="2.5" opacity="0">{win(RUN2 + 0.8, D - 0.3)}</rect>')
STAT = [(RUN1, LEAK, 'normal: across the direct link', CYAN), (LEAK, RUN2, 'C leaks P2\'s routes to P1', ROUTE),
        (RUN2, D - 0.3, 'P1 prefers them: traffic through C', RED)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(200, 290, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Customer C buys transit from P1 and P2; when it mistakenly passes P2\'s routes on to P1, P1 prefers them, since a paying customer\'s routes usually win, and traffic that crossed directly now squeezes through C\'s small links. That is a <span class="key-term">route leak</span>: genuine routes reaching a neighbour that should never have heard them, with no attacker at all.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rule broken.</b> A customer should pass its providers' routes only to its own customers, never to another provider; RFC 7908 (2016) catalogues the ways this goes wrong.</li>
          <li><b>Why it spreads.</b> BGP trusts what neighbours announce, so P1 passes the leaked route on to everyone it talks to.</li>
          <li><b>Defences.</b> Route filters, the routing registries, RPKI and the newer ASPA records all exist, and are only partly deployed.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-12">
      <div class="diagram-label">Fig 9.12 · A route leak: traffic takes the wrong door</div>
      {svg}
      <p id="ch9-security-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-12', 'ch9-security-p6', card)
