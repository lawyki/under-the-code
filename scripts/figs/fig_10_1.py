# Fig 10.1 · UDP (Pass 28, law 3). Chart Room. The eight-byte header of one real datagram (a DNS query,
# port 51234 to 53); then three datagrams sent, the second lost: nothing in UDP notices, the receiver
# simply has 1 and 3, and any retry is the application's job. t=0 (shift): after the loss.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 300
GX, BW = 24, 11
D = 8.0
SENDS = [0.6, 1.4, 2.2]
FLY = 1.6
T = Timeline(D, shift=5.2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-28 svgd-part3-28">')
a('<title id="svgt-part3-28">Fig 10.1 · UDP: eight bytes, no state, no apologies</title>')
a('<desc id="svgd-part3-28">A UDP header is eight bytes: source port 51234, destination port 53 (DNS), length 37 bytes including the header, and a checksum. Then a sender sends three datagrams; the second is lost on the way. '
  'Nothing in UDP notices or resends it: the receiver simply has datagrams 1 and 3, and if anything is to be retried, the application must do it.</desc>')
a(text(GX, 22, 'UDP HEADER · 8 BYTES', size=13, fill=CMUTED))
for r, row in enumerate([[('source port', '51234'), ('destination port', '53 · DNS')], [('length', '37'), ('checksum', 'optional in IPv4')]]):
    for c, (nm, val) in enumerate(row):
        x, y = GX + c * 16 * BW, 32 + r * 46
        a(f'<rect x="{x}" y="{y}" width="{16 * BW}" height="46" fill="{CPLATE}" stroke="rgba(79,196,230,0.45)"/>')
        a(text(x + 8, y + 18, nm, size=13, fill=CMUTED, ls='0'))
        a(text(x + 8, y + 37, val, size=13, fill='#fff', ls='0'))
a(f'<rect x="{GX}" y="128" width="{32 * BW}" height="28" fill="{CDEEP}" stroke="rgba(79,196,230,0.25)" stroke-dasharray="4 3"/>')
a(text(GX + 8, 147, 'payload: the DNS query', size=13, fill=CMUTED, ls='0'))
# three datagrams
LY = 214
SX, RX = 24, 288
a(f'<rect x="{SX}" y="{LY - 18}" width="72" height="36" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
a(text(SX + 36, LY + 5, 'sender', anchor='middle', size=13, fill='#fff', ls='0'))
a(f'<rect x="{RX}" y="{LY - 18}" width="88" height="36" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
a(text(RX + 44, LY + 5, 'receiver', anchor='middle', size=13, fill='#fff', ls='0'))
a(f'<line x1="{SX + 72}" y1="{LY}" x2="{RX}" y2="{LY}" stroke="{CSOFT}" stroke-opacity="0.25"/>')
for k, t0 in enumerate(SENDS):
    lost = k == 1
    dist = (RX - SX - 72 - 20) * (0.5 if lost else 1.0)
    end = t0 + FLY * (0.5 if lost else 1.0)
    a(f'<g class="fx" opacity="0">{win(t0, end)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (end, dist), (D, dist)], "x")}'
      f'<rect x="{SX + 76}" y="{LY - 10}" width="20" height="20" rx="2" fill="{CYAN}"/>{text(SX + 86, LY + 5, str(k + 1), anchor="middle", size=13, fill=CDEEP, ls="0")}</g></g>')
    if lost:
        x = SX + 76 + dist + 10
        a(f'<g>{held(end)}<line x1="{x - 8}" y1="{LY - 8}" x2="{x + 8}" y2="{LY + 8}" stroke="{RED}" stroke-width="3"/><line x1="{x + 8}" y1="{LY - 8}" x2="{x - 8}" y2="{LY + 8}" stroke="{RED}" stroke-width="3"/></g>')
GOT = [(0, SENDS[0] + FLY), (2, SENDS[2] + FLY)]
a(text(RX, LY + 40, 'has:', size=13, fill=CMUTED, ls='0'))
for i, (k, t) in enumerate(GOT):
    a(f'<g>{held(t)}{text(RX + 44 + i * 18, LY + 40, str(k + 1), size=14, fill=CYAN, ls="0")}</g>')
a(f'<g>{held(SENDS[1] + FLY)}{text(SX, LY + 40, "sender: no idea", size=13, fill=CMUTED, ls="0")}</g>')
a(f'<g>{held(SENDS[2] + FLY + 0.4)}{text(SX, LY + 64, "no resend: retrying is the application\'s job", size=13, fill=ROUTE, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('UDP is an envelope around your bytes: eight bytes of header with two ports, a length and a checksum, and nothing else. '
           'No connection, no order, no retransmission: a lost datagram is simply missing, and the application decides whether to try again.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The standard.</b> RFC 768, from August 1980, is three pages long. The checksum is optional over IPv4 and required over IPv6.</li>
          <li><b>Where it wins.</b> DNS fits a question and an answer into one datagram each; voice, video and games would rather lose a packet than wait for it.</li>
          <li><b>Building on it.</b> QUIC, the transport under HTTP/3, runs on UDP and adds its own reliability and encryption on top.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-1">
      <div class="diagram-label">Fig 10.1 · UDP: eight bytes, no state, no apologies</div>
      {svg}
      <p id="ch10-udp-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-1', 'ch10-udp-p3', card)
