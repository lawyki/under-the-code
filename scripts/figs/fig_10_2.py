# Fig 10.2 · The three-way handshake, in time (Pass 28, law 3). Chart Room. Time runs down; three segments
# cross with real numbers (client ISN 4170, server ISN 9012); each side's state changes as they arrive;
# a bracket marks the round trip spent before the first data. t=0 (shift): established, data leaving.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

CX, SX = 70, 330
X_ISN, S_ISN = 4170, 9012
MSGS = [('c', 'SYN · seq 4170', 90, 106), ('s', f'SYN-ACK · seq {S_ISN} · ack {X_ISN + 1}', 150, 166), ('c', f'ACK · ack {S_ISN + 1}', 210, 226)]
W, H = 400, 300
D = 9.0
T0 = [0.8, 2.4, 4.0]
FLY = 1.2
DATA = T0[2] + 0.1
T = Timeline(D, shift=DATA + FLY + 1.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.39, 1.0), (0.395, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
def until(t1):
    return T.anim('opacity', [(0.0, 0.0), (0.398, 0.0), (0.402, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-29 svgd-part3-29">')
a('<title id="svgt-part3-29">Fig 10.2 · The three-way handshake, in time</title>')
a(f'<desc id="svgd-part3-29">Time runs downward between a client and a server. The client sends SYN with its initial sequence number, {X_ISN}, and moves from CLOSED to SYN_SENT. The server, listening, replies SYN-ACK with its own number, {S_ISN}, '
  f'acknowledging {X_ISN + 1}, and moves to SYN_RCVD. The client replies ACK, acknowledging {S_ISN + 1}; both sides are ESTABLISHED. One full round trip passes before the client\'s first byte of data can leave.</desc>')
for x, nm in ((CX, 'client'), (SX, 'server')):
    a(text(x, 22, nm, anchor='middle', size=14, fill='#fff', ls='0'))
    a(f'<line x1="{x}" y1="{68}" x2="{x}" y2="{276}" stroke="{CSOFT}" stroke-opacity="0.5" stroke-width="2"/>')
# states
CST = [(None, T0[0], 'CLOSED'), (T0[0], T0[1] + FLY, 'SYN_SENT'), (T0[1] + FLY, None, 'ESTABLISHED')]
SST = [(None, T0[0] + FLY, 'LISTEN'), (T0[0] + FLY, T0[2] + FLY, 'SYN_RCVD'), (T0[2] + FLY, None, 'ESTABLISHED')]
for x, states in ((CX, CST), (SX, SST)):
    for t0, t1, s in states:
        g = until(t1) if t0 is None else (held(t0) if t1 is None else win(t0, t1))
        col = CYAN if s == 'ESTABLISHED' else ROUTE
        a(f'<g opacity="{1 if t0 is None else 0}">{g}{text(x, 46, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
# the segments
for k, (who, lab, y0, y1) in enumerate(MSGS):
    x0, x1 = (CX, SX) if who == 'c' else (SX, CX)
    t0 = T0[k]
    a(f'<g>{held(t0 + FLY)}<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{CYAN}" stroke-width="2"/>'
      f'<polygon points="{x1 + (-8 if x1 > x0 else 8)},{y1 - 7} {x1 + (-8 if x1 > x0 else 8)},{y1 + 3} {x1},{y1}" fill="{CYAN}"/></g>')
    a(f'<g class="fx" opacity="0">{win(t0, t0 + FLY)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + FLY, x1 - x0), (D, x1 - x0)], "x")}'
      f'<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + FLY, y1 - y0), (D, y1 - y0)], "y")}<circle cx="{x0}" cy="{y0}" r="6" fill="{CYAN}"/></g></g></g>')
    a(f'<g>{held(t0)}{text(200, (y0 + y1) / 2 - 10, lab, anchor="middle", size=13, fill=CSOFT, ls="0")}</g>')
# first data and the round-trip bracket
a(f'<g>{held(DATA + FLY)}<line x1="{CX}" y1="250" x2="{SX}" y2="266" stroke="{ROUTE}" stroke-width="2" stroke-dasharray="6 4"/>'
  f'{text(200, 248, "first data", anchor="middle", size=13, fill=ROUTE, ls="0")}</g>')
a(f'<g>{held(T0[1] + FLY)}<path d="M{CX - 14} 90 H{CX - 22} V166 H{CX - 14}" fill="none" stroke="{ROUTE}" stroke-width="1.5"/>'
  f'{text(CX - 28, 133, "1 RTT", anchor="end", size=13, fill=ROUTE, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ("The client sends SYN with its starting sequence number; the server answers with its own and acknowledges the client's plus one; the client acknowledges the server's plus one, and both now know both counters. That costs one full round trip before the first byte of data, the tax QUIC (Section 05) sets out to cut.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Random starts.</b> Each side picks its initial sequence number unpredictably, so an outsider cannot guess the numbers needed to inject into the connection.</li>
          <li><b>Plus one.</b> SYN counts as one byte of sequence space, which is why the acknowledgements are 4171 and 9013.</li>
          <li><b>Data early.</b> The third segment may already carry data, but nothing can leave before it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-2">
      <div class="diagram-label">Fig 10.2 · The three-way handshake, in time</div>
      {svg}
      <p id="ch10-handshake-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-2', 'ch10-handshake-p2', card)
