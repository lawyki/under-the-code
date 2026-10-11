# Fig 9.11 · Pakistan/YouTube, 24 February 2008 (Pass 28, law 3, conceptual pass: most-specific-wins, and the defence).
# Chart Room. YouTube's block 208.65.152.0/22 as four /24 cells. Traffic to 208.65.153.x follows the most specific
# route: YouTube's /22 (18:46 UTC); Pakistan Telecom's /24, leaked worldwide by PCCW, wins (18:47) and the traffic dies
# in Pakistan's null route; YouTube's two /25s win it back (20:18); PCCW withdraws the /24 (20:51). Times from the RIPE
# NCC RIS case study. t=0 (shift): the /24 withdrawn, the /25s carrying the traffic.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W = 400
D = 13.0
T = Timeline(D, shift=12.4)
P0, P1, P2, P3 = 0.8, 3.6, 6.8, 9.8
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
a(text(20, 22, "208.65.152.0/22, YouTube's block", size=13, fill=CMUTED, ls='0'))
CX0, CW = 20, 90
cx = lambda k: CX0 + k * CW
for k in range(4):
    a(f'<rect x="{cx(k)}" y="32" width="{CW}" height="30" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.5"/>')
    a(text(cx(k) + CW / 2, 52, f'.{152 + k}', anchor='middle', size=13, fill='#fff' if k == 1 else CMUTED, ls='0'))
# the routes
RA, RB, RC, RHt = 74, 112, 150, 28
a(f'<rect x="20" y="{RA}" width="360" height="{RHt}" rx="3" fill="{CYAN}" fill-opacity="0.18" stroke="{CYAN}" stroke-opacity="0.7"/>')
a(text(32, RA + 19, '/22 YouTube', size=13, fill=CYAN, ls='0'))
X1 = cx(1)
a(f'<g opacity="0">{lit(P1, P3)}<rect x="{X1}" y="{RB}" width="{CW}" height="{RHt}" rx="3" fill="{RED}" fill-opacity="0.35" stroke="{RED}"/></g>')
a(f'<g opacity="0">{win(P3)}<rect x="{X1}" y="{RB}" width="{CW}" height="{RHt}" rx="3" fill="none" stroke="{RED}" stroke-opacity="0.6" stroke-dasharray="5 4"/></g>')
a(f'<g opacity="0">{win(P1)}{text(X1 + CW + 12, RB + 19, "/24 Pakistan Telecom", size=13, fill=RED, ls="0")}</g>')
a(f'<g opacity="0">{win(P2)}<rect x="{X1}" y="{RC}" width="{CW / 2 - 2}" height="{RHt}" rx="3" fill="{CYAN}" fill-opacity="0.35" stroke="{CYAN}"/>'
  f'<rect x="{X1 + CW / 2 + 2}" y="{RC}" width="{CW / 2 - 2}" height="{RHt}" rx="3" fill="{CYAN}" fill-opacity="0.35" stroke="{CYAN}"/>'
  f'{text(X1 + CW + 12, RC + 19, "two /25s, YouTube", size=13, fill=CYAN, ls="0")}</g>')
# the winner, outlined at each change
for t0, y, h, x, w in ((P0, RA, RHt, 20, 360), (P1, RB, RHt, X1, CW), (P2, RC, RHt, X1, CW)):
    a(f'<g class="fx" opacity="0">{pulse(t0)}<rect x="{x - 3}" y="{y - 3}" width="{w + 6}" height="{h + 6}" rx="4" fill="none" stroke="#fff" stroke-width="2"/></g>')
# where the traffic ends up
BY = 220
a(f'<rect x="20" y="{BY}" width="170" height="40" rx="3" fill="{CDEEP}" stroke="{CYAN}" stroke-opacity="0.8"/>')
a(text(105, BY + 25, 'YouTube', anchor='middle', size=13, fill='#fff', ls='0'))
a(f'<rect x="210" y="{BY}" width="170" height="40" rx="3" fill="{CDEEP}" stroke="{RED}" stroke-opacity="0.8"/>')
a(text(295, BY + 25, 'Pakistan: dropped', anchor='middle', size=13, fill='#fff', ls='0'))
TX = X1 + CW / 2
def traffic(t0, t1, to_x, col, n=3):
    for k in range(n):
        s = t0 + 0.2 + k * 0.8
        if s + 0.9 > t1: break
        ky = [(0.0, 0.0), (s, 0.0), (s + 0.55, 190 - 47), (s + 0.9, BY + 20 - 47), (D, BY + 20 - 47)]
        kx = [(0.0, 0.0), (s + 0.55, 0.0), (s + 0.9, to_x - TX), (D, to_x - TX)]
        a(f'<g class="fx" opacity="0">{lit(s, s + 0.95)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{TX}" cy="47" r="5" fill="{col}"/></g></g></g>')
traffic(P0, P1, 105, CYAN)
traffic(P1, P2, 295, RED)
traffic(P2, P3, 105, CYAN)
traffic(P3, D - 0.4, 105, CYAN)
SY = BY + 66
for t0, t1, s, col in ((0.31, P1, '18:46 UTC: the /22 is the best match', CYAN), (P1, P2, '18:47: the leaked /24 is more specific', RED),
                       (P2, P3, '20:18: two /25s win the traffic back', CYAN), (P3, None, '20:51: the /24 is withdrawn', CSOFT)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(20, SY, s, size=13, fill=col, ls="0")}</g>')
a(text(20, SY + 22, 'traffic to 208.65.153.x', size=13, fill=CMUTED, ls='0'))
H = SY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-25 svgd-part3-25">')
o.insert(1, '<title id="svgt-part3-25">Fig 9.11 · Pakistan/YouTube, 24 February 2008</title>')
o.insert(2, '<desc id="svgd-part3-25">YouTube\'s address block 208.65.152.0/22, drawn as four /24s, and traffic to 208.65.153.x. At 18:46 UTC the only route is YouTube\'s /22 and the traffic reaches YouTube. '
  'At 18:47 Pakistan Telecom\'s announcement of 208.65.153.0/24, meant to block YouTube inside Pakistan and leaked worldwide by its upstream, is more specific, so routers everywhere send the traffic to Pakistan, where it is dropped. '
  'At 20:18 YouTube announces two /25s, more specific again, and wins the traffic back; at 20:51 the /24 is withdrawn.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Routers follow the most specific route they know, so Pakistan Telecom\'s /24, meant to block YouTube at home but leaked worldwide by its upstream PCCW, beat YouTube\'s own /22 everywhere. '
           'YouTube answered with two still more specific /25s; withdrawing the /24 ended the outage after about two hours.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>No malice.</b> The block was a domestic order; the outage came from a configuration mistake upstream, where PCCW passed its customer's announcement on without filtering it.</li>
          <li><b>Origin validation.</b> With RPKI, a prefix holder signs a route origin authorisation (ROA) naming who may announce its prefixes and how specific they may be; a router that checks it drops a /24 like this one as invalid.</li>
          <li><b>Why it must be automatic.</b> A new route spreads across the world's routers within minutes, faster than any operator can notice and react.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-11">
      <div class="diagram-label">Fig 9.11 · Pakistan/YouTube, 24 February 2008</div>
      {svg}
      <p id="ch9-security-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-11', 'ch9-security-p5', card)
