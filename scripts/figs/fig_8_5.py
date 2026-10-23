# Fig 8.5 · Manchester: every bit is a transition (Pass 28, law 3). Chart Room. The waveform for
# 1 0 1 1 0 0 1 in the IEEE 802.3 convention (a rising mid-bit edge is 1, a falling one 0). A cursor
# sweeps; at each mid-bit edge a tick lights and the decoded bit appears. t=0 (shift): all decoded.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

BITS = [1, 0, 1, 1, 0, 0, 1]
W, H = 400, 200
X0, CW = 50, 46
HI, LO = 58, 98
D = 7.0
S0, S1 = 0.4, 6.0
T = Timeline(D, shift=6.4)
xt = lambda x: S0 + (x - X0) / (CW * len(BITS)) * (S1 - S0)
def from_t(t):
    return T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-6 svgd-part3-6">')
a('<title id="svgt-part3-6">Fig 8.5 · Manchester: every bit is a transition</title>')
a('<desc id="svgd-part3-6">The bits 1 0 1 1 0 0 1 in Manchester code, as Ethernet\'s IEEE 802.3 standard defines it: each bit period has a transition in its middle, rising for a 1 and falling for a 0. '
  'Between two equal bits the line also changes at the boundary to get ready. A receiver reads the direction of each mid-bit edge and recovers 1 0 1 1 0 0 1, and because there is an edge in every bit, it also recovers the clock.</desc>')
a(text(20, 30, 'bits', size=13, fill=CMUTED, ls='0'))
for i, b in enumerate(BITS):
    a(text(X0 + i * CW + CW / 2, 30, str(b), anchor='middle', size=15, fill='#fff', ls='0'))
    if i: a(f'<line x1="{X0 + i * CW}" y1="42" x2="{X0 + i * CW}" y2="112" stroke="rgba(223,234,242,0.15)" stroke-dasharray="2 3"/>')
# waveform
pts = []
for i, b in enumerate(BITS):
    x, m = X0 + i * CW, X0 + i * CW + CW / 2
    first, second = (LO, HI) if b else (HI, LO)
    if pts and pts[-1][1] != first: pts.append((x, first))
    if not pts: pts.append((x, first))
    pts += [(m, first), (m, second), (x + CW, second)]
a('<polyline points="' + ' '.join(f'{x:.1f},{y}' for x, y in pts) + f'" fill="none" stroke="{CYAN}" stroke-width="2.5"/>')
a(text(20, HI + 5, 'hi', size=13, fill=CMUTED, ls='0'))
a(text(20, LO + 5, 'lo', size=13, fill=CMUTED, ls='0'))
# mid-bit edges: tick and decoded bit as the cursor passes
for i, b in enumerate(BITS):
    m = X0 + i * CW + CW / 2
    t = xt(m)
    head = f'<polygon points="{m - 6},{HI + 10} {m + 6},{HI + 10} {m},{HI}" fill="{ROUTE}"/>' if b else f'<polygon points="{m - 6},{LO - 10} {m + 6},{LO - 10} {m},{LO}" fill="{ROUTE}"/>'
    a(f'<g>{from_t(t)}{head}{text(m, 140, str(b), anchor="middle", size=15, fill=ROUTE, ls="0")}</g>')
a(text(20, 140, 'read', size=13, fill=CMUTED, ls='0'))
a(text(20, 184, 'rising mid-bit edge = 1, falling = 0', size=13, fill=CSOFT, ls='0'))
# cursor
x1 = X0 + CW * len(BITS)
a(f'<line y1="42" y2="150" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}{T.anim("x2", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (S0 - 0.01, 0.0), (S0, 0.6), (S1, 0.6), (S1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ("The bits 1 0 1 1 0 0 1 in Manchester code: each mid-bit edge gives the bit and keeps the receiver's clock in step.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Two conventions.</b> Ethernet (IEEE 802.3) uses rising for 1; the older G. E. Thomas convention is the reverse. Either works if both ends agree.</li>
          <li><b>The bandwidth.</b> 10 Mbps Ethernet carries up to 20 million signal changes per second, which is why the next speed, 100 Mbps, moved to more efficient line codes.</li>
          <li><b>Boundary edges.</b> Between two equal bits the line must also change at the boundary, to be on the right side for the next mid-bit edge.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-5">
      <div class="diagram-label">Fig 8.5 · Manchester: every bit is a transition</div>
      {svg}
      <p id="ch8-encoding-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-5', 'ch8-encoding-p4', card)
