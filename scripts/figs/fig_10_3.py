# Fig 10.3 · TCP's state machine (Pass 28, law 3). Chart Room. All eleven states, unrolled top to bottom
# (CLOSED drawn at both ends). Two lives play in turn: the client's (active open, active close), then
# the server's (passive open, passive close); a token walks each path and a status line names each
# event. t=0 (shift): the client in TIME_WAIT.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 470
NW, NH = 118, 32
NODES = {'CLOSED': (141, 14), 'SYN_SENT': (12, 70), 'LISTEN': (270, 70), 'SYN_RCVD': (270, 126),
         'ESTABLISHED': (141, 182), 'FIN_WAIT_1': (12, 238), 'CLOSE_WAIT': (270, 238), 'FIN_WAIT_2': (12, 294),
         'CLOSING': (141, 294), 'LAST_ACK': (270, 294), 'TIME_WAIT': (12, 350), 'CLOSED ': (141, 404)}
def c(n):
    x, y = NODES[n]; return x + NW / 2, y + NH / 2
CLIENT = [('CLOSED', 'connect(): send SYN'), ('SYN_SENT', 'SYN-ACK in: send ACK'), ('ESTABLISHED', 'close(): send FIN'),
          ('FIN_WAIT_1', 'ACK in'), ('FIN_WAIT_2', 'FIN in: send ACK'), ('TIME_WAIT', 'wait 2 × MSL'), ('CLOSED ', '')]
SERVER = [('CLOSED', 'listen()'), ('LISTEN', 'SYN in: send SYN-ACK'), ('SYN_RCVD', 'ACK in'), ('ESTABLISHED', 'FIN in: send ACK'),
          ('CLOSE_WAIT', 'close(): send FIN'), ('LAST_ACK', 'ACK in'), ('CLOSED ', '')]
EXTRA = [('FIN_WAIT_1', 'CLOSING'), ('CLOSING', 'TIME_WAIT')]
D = 16.0
STEP = 1.05
C0, S0 = 0.6, 8.4
T = Timeline(D, shift=C0 + 5 * STEP + 0.4)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-30 svgd-part3-30">')
a('<title id="svgt-part3-30">Fig 10.3 · TCP\'s state machine</title>')
a('<desc id="svgd-part3-30">TCP\'s eleven connection states. A client goes from CLOSED to SYN_SENT when it connects, to ESTABLISHED when the SYN-ACK arrives, to FIN_WAIT_1 when it closes, FIN_WAIT_2 when its FIN is acknowledged, '
  'TIME_WAIT when the other side\'s FIN arrives, and back to CLOSED after waiting twice the maximum segment lifetime. A server goes from CLOSED to LISTEN, to SYN_RCVD when a SYN arrives, to ESTABLISHED on the ACK, '
  'to CLOSE_WAIT when the client\'s FIN arrives, to LAST_ACK when it closes too, and to CLOSED when its FIN is acknowledged. CLOSING is reached only when both sides close at once.</desc>')
def edge(u, v, dashed=False):
    (x1, y1), (x2, y2) = c(u), c(v)
    y1 += NH / 2 if y2 > y1 else 0; y2 -= NH / 2 if y2 > y1 else 0
    if y1 == y2: x1, x2 = (x1 + NW / 2, x2 - NW / 2) if x2 > x1 else (x1 - NW / 2, x2 + NW / 2)
    return x1, y1, x2, y2
for path in (CLIENT, SERVER):
    for (u, _), (v, _) in zip(path, path[1:]):
        x1, y1, x2, y2 = edge(u, v)
        a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CSOFT}" stroke-opacity="0.3" stroke-width="1.5"/>')
for u, v in EXTRA:
    x1, y1, x2, y2 = edge(u, v)
    a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{CSOFT}" stroke-opacity="0.25" stroke-width="1.5" stroke-dasharray="3 3"/>')
for n, (x, y) in NODES.items():
    dim = n == 'CLOSING'
    a(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="{0.3 if dim else 0.6}"/>')
    a(text(x + NW / 2, y + 21, n.strip(), anchor='middle', size=13, fill=CMUTED if dim else '#fff', ls='0'))
def life(path, t0, col, who):
    (sx, sy) = c(path[0][0])
    kx, ky = [(0.0, 0.0), (t0, 0.0)], [(0.0, 0.0), (t0, 0.0)]
    for i, (n, _) in enumerate(path[1:], 1):
        x, y = c(n); t = t0 + i * STEP
        kx += [(t - 0.35, kx[-1][1]), (t, x - sx)]; ky += [(t - 0.35, ky[-1][1]), (t, y - sy)]
        x1, y1, x2, y2 = edge(path[i - 1][0], n)
        a(f'<line class="fx" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="3" opacity="0">{win(t - 0.35, t + 0.5)}</line>')
    kx.append((D, kx[-1][1])); ky.append((D, ky[-1][1]))
    end = t0 + (len(path) - 1) * STEP + 0.6
    a(f'<g class="fx" opacity="0">{win(t0 - 0.2, end)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}'
      f'<rect x="{sx - NW / 2 - 3}" y="{sy - NH / 2 - 3}" width="{NW + 6}" height="{NH + 6}" rx="3" fill="none" stroke="{col}" stroke-width="2.5"/></g></g></g>')
    for i, (n, ev) in enumerate(path[:-1]):
        t = t0 + i * STEP
        a(f'<g opacity="0">{win(t, t + STEP)}{text(200, H - 10, f"{who}: {ev}", anchor="middle", size=13, fill=col, ls="0")}</g>')
life(CLIENT, C0, ROUTE, 'client')
life(SERVER, S0, CYAN, 'server')
a('</svg>')
svg = '\n'.join(o)

caption = ('TCP\'s eleven states, as RFC 793 defined them in 1981: the client connects and later closes first, the server listens and closes second, each move triggered by a segment arriving or a call from the program. '
           'The side that closes first waits in TIME_WAIT so that stray packets from this connection die before its addresses and ports are reused.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>TIME_WAIT.</b> It lasts twice the maximum segment lifetime; Linux uses 60 seconds.</li>
          <li><b>CLOSING.</b> Reached only when both sides send FIN at the same moment; most connections never see it.</li>
          <li><b>Seeing it live.</b> <code>ss -tan</code> on Linux lists every connection with its current state.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-3">
      <div class="diagram-label">Fig 10.3 · TCP's state machine</div>
      {svg}
      <p id="ch10-handshake-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-3', 'ch10-handshake-p4', card)
