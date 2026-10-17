# Fig 10.9 · TCP+TLS+HTTP vs QUIC: the same job, two stacks (Pass 28, law 3). Chart Room plate. Top: the two
# stacks, QUIC spanning the rows TLS and TCP hold on the left and sitting on UDP. Bottom: round trips until the
# page arrives. TCP + TLS 1.3: TCP handshake, TLS handshake, GET -> page = 3 RTT. QUIC (TLS 1.3 inside): one
# combined handshake, then GET -> page = 2. Resumed QUIC sends the GET in its first flight (0-RTT) = 1. The bars
# fill left to right on one clock; each row's "page after" readout lights as it lands. t=0 (shift): all filled.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, CSOFT, CMUTED
figlib.FONT = SPACE

GOLD, GREEN = '#d4a853', '#9bd89b'
W = 400
X0, X1 = 20, 380
# the stacks: 5 rows, two columns
SR, SH, SG = 30, 22, 4                          # first row y, row height, gap
ry = lambda r: SR + r * (SH + SG)
LC, RC, CW = 20, 210, 170
o = []; a = o.append
def box(x, r0, r1, col, l1, l2=None):
    y, h = ry(r0), ry(r1) - ry(r0) + SH
    a(f'<rect x="{x}" y="{y}" width="{CW}" height="{h}" rx="4" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-opacity="0.8"/>')
    if l2 is None:
        a(text(x + CW / 2, y + h / 2 + 5, l1, anchor='middle', size=13, fill=col, ls='0'))
    else:
        a(text(x + CW / 2, y + h / 2 - 3, l1, anchor='middle', size=13, fill=col, ls='0'))
        a(text(x + CW / 2, y + h / 2 + 13, l2, anchor='middle', size=13, fill=CSOFT, ls='0'))
# the timelines
RTT = (X1 - X0) / 3
xr = lambda r: X0 + r * RTT
ROWS = [('TCP + TLS 1.3', [('TCP handshake', CYAN), ('TLS 1.3', GOLD), ('GET → page', GREEN)]),
        ('QUIC (TLS 1.3 inside)', [('handshake', CYAN), ('GET → page', GREEN)]),
        ('QUIC, resumed (0-RTT)', [('GET → page', GREEN)])]
TY, TS, BH = ry(5) + 28, 60, 28                 # first row label baseline, row step, bar height
D, S0, S1 = 9.0, 0.5, 6.5
T = Timeline(D, shift=8.4)
tr = lambda r: S0 + r / 3 * (S1 - S0)
H = TY + 2 * TS + 8 + BH + 60
a0 = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-36 svgd-part3-36">'
a(text(LC, SR - 10, 'HTTP/2 stack', anchor='start', size=13, fill=CMUTED, ls='0'))
a(text(RC, SR - 10, 'HTTP/3 stack', anchor='start', size=13, fill=CMUTED, ls='0'))
box(LC, 0, 0, GREEN, 'HTTP/2')
box(LC, 1, 1, GOLD, 'TLS 1.3')
box(LC, 2, 3, CYAN, 'TCP', 'in the kernel')
box(LC, 4, 4, CMUTED, 'IP')
box(RC, 0, 0, GREEN, 'HTTP/3')
box(RC, 1, 2, CYAN, 'QUIC', 'TLS 1.3 inside')
box(RC, 3, 3, CMUTED, 'UDP')
box(RC, 4, 4, CMUTED, 'IP')
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
fills = []
for i, (name, segs) in enumerate(ROWS):
    y = TY + i * TS
    a(text(X0, y, name, anchor='start', size=13, fill=CSOFT, ls='0'))
    n = len(segs)
    a(f'<g class="fx" opacity="0">{win(tr(n))}{text(X1, y, f"page after {n}", anchor="end", size=13, fill=GREEN, ls="0")}</g>')
    for k, (lab, col) in enumerate(segs):
        x = xr(k) + 2
        a(f'<rect x="{x:.1f}" y="{y + 8}" width="{RTT - 4:.1f}" height="{BH}" rx="4" fill="none" stroke="{col}" stroke-opacity="0.45"/>')
        fills.append(f'<rect x="{x:.1f}" y="{y + 8}" width="{RTT - 4:.1f}" height="{BH}" rx="4" fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="1.5"/>')
# the fill: one clock for all three rows, revealed left to right
a(f'<defs><clipPath id="clip-fig-10-9"><rect class="fx" x="{X0}" y="0" width="{X1 - X0}" height="{H}">'
  f'{T.anim("width", [(0.0, X1 - X0), (0.3, X1 - X0), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0), (D, X1 - X0)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-10-9)">{"".join(fills)}</g>')
for i, (name, segs) in enumerate(ROWS):
    y = TY + i * TS
    for k, (lab, col) in enumerate(segs):
        a(text(xr(k) + RTT / 2, y + 8 + BH / 2 + 5, lab, anchor='middle', size=13, fill=CSOFT, ls='0'))
AY = TY + 2 * TS + 8 + BH
a(f'<line x1="{X0}" y1="{AY + 6}" x2="{X1}" y2="{AY + 6}" stroke="{CMUTED}"/>')
for r in range(4):
    a(f'<line x1="{xr(r):.1f}" y1="{AY + 2}" x2="{xr(r):.1f}" y2="{AY + 10}" stroke="{CMUTED}"/>')
    a(text(xr(r), AY + 26, str(r), anchor='middle' if 0 < r < 3 else ('start' if r == 0 else 'end'), size=13, fill=CMUTED, ls='0'))
a(text(X1, AY + 46, 'round trips', anchor='end', size=13, fill=CMUTED, ls='0'))
a('</svg>')
o.insert(0, a0)
o.insert(1, '<title id="svgt-part3-36">Fig 10.9 · TCP+TLS+HTTP vs QUIC: the same job, two stacks</title>')
o.insert(2, '<desc id="svgd-part3-36">Two protocol stacks side by side. On the left HTTP/2 sits on TLS 1.3, which sits on TCP in the kernel, on IP. '
  'On the right HTTP/3 sits on QUIC, which carries TLS 1.3 inside it, on UDP, on IP. Below, the round trips before a page arrives: '
  'over TCP and TLS 1.3, one for the TCP handshake, one for TLS and one for the request, three in all; over QUIC, one combined handshake and the request, two; '
  'a resumed QUIC connection sends the request in its first packet and has the page after one.</desc>')
svg = '\n'.join(o)

caption = ("Over TCP, one round trip goes to TCP's handshake and one to TLS's before the request can go; QUIC's single handshake does both jobs, so the page arrives after two round trips instead of three.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The stacks.</b> HTTP/3 runs on QUIC, which builds reliability, ordering, congestion control and TLS 1.3 into one protocol over UDP. Because it ships with the browser or server, not the operating system, it can change as fast as they do: its <strong>iterability</strong>.</li>
          <li><b>The round trips.</b> TCP with TLS 1.3 gets the page after three (four with TLS 1.2); QUIC after two. <span class="key-term">0-RTT resumption</span> sends the request with the first packet to a server the client has met before, so one.</li>
          <li><b>Beyond the handshake.</b> <strong>Per-stream multiplexing</strong>: a lost packet stalls only its own stream, not every request behind it as on TCP. <strong>Connection migration</strong>: a connection ID, not the address pair, names the connection, so a phone moving from Wi-Fi to mobile data keeps it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-9">
      <div class="diagram-label">Fig 10.9 · TCP+TLS+HTTP vs QUIC: the same job, two stacks</div>
      {svg}
      <p id="ch10-modern-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-9', 'ch10-modern-p7', card)
