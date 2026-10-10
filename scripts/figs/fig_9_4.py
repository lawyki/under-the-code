# Fig 9.4 · The IPv4 header, byte by byte (Pass 28, law 3). Chart Room. One real header (RFC 791 layout,
# 32 bits per row) for a TCP packet from 192.0.2.10 to 198.51.100.7, checksum computed. One router hop
# runs on it: look up the destination, decrement TTL 64 -> 63, recompute the checksum, forward.
# t=0: the header as it arrives.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

def csum(ttl):
    words = [0x4500, 60, 0x1C46, 0x4000, (ttl << 8) | 6, 0, 0xC000, 0x020A, 0xC633, 0x6407]
    s = sum(words)
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF
C64, C63 = csum(64), csum(63)
def ok(ttl, c):
    words = [0x4500, 60, 0x1C46, 0x4000, (ttl << 8) | 6, c, 0xC000, 0x020A, 0xC633, 0x6407]
    s = sum(words)
    while s >> 16: s = (s & 0xFFFF) + (s >> 16)
    return s == 0xFFFF
assert ok(64, C64) and ok(63, C63) and C63 == C64 + 0x100
W, H = 400, 314
GX, BW = 24, 11                    # 32 bits x 11 = 352
RY, RH = 34, 42
D = 9.0
LOOK, TTL, SUM, FWD, RESET = 1.0, 2.6, 4.0, 5.4, 8.6
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def before(t):
    return T.anim('opacity', [(0.0, 1.0), (t - 0.008, 1.0), (t - 0.005, 0.0), (RESET - 0.002, 0.0), (RESET, 1.0), (D, 1.0)])
def after(t):
    return win(t, RESET)
ROWS = [[('Ver', 4, '4'), ('IHL', 4, '5'), ('ToS', 8, '0'), ('Total length', 16, '60')],
        [('Identification', 16, '0x1C46'), ('Flg', 3, 'DF'), ('Fragment offset', 13, '0')],
        [('TTL', 8, None), ('Protocol', 8, '6 TCP'), ('Header checksum', 16, None)],
        [('Source address', 32, '192.0.2.10')],
        [('Destination address', 32, '198.51.100.7')]]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-18 svgd-part3-18">')
a('<title id="svgt-part3-18">Fig 9.4 · The IPv4 header, byte by byte</title>')
a(f'<desc id="svgd-part3-18">A real 20-byte IPv4 header, laid out 32 bits to a row as in RFC 791: version 4, header length 5 words, type of service 0, total length 60 bytes; identification 0x1C46, the don\'t-fragment flag, offset 0; '
  f'time to live 64, protocol 6 for TCP, header checksum 0x{C64:04X}; source 192.0.2.10; destination 198.51.100.7. A router reads the destination to choose the next hop, '
  f'lowers the time to live to 63, recomputes the checksum to 0x{C63:04X} and forwards the packet.</desc>')
a(text(GX, 22, '0', size=13, fill=CMUTED, ls='0'))
a(text(GX + 32 * BW, 22, '31', anchor='end', size=13, fill=CMUTED, ls='0'))
a(text(GX + 16 * BW, 22, 'bits', anchor='middle', size=13, fill=CMUTED, ls='0'))
cells = {}
for r, row in enumerate(ROWS):
    x, y = GX, RY + r * RH
    for nm, bits, val in row:
        w = bits * BW
        cells[nm] = (x, y, w)
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="{CPLATE}" stroke="rgba(79,196,230,0.45)"/>')
        a(text(x + 6, y + 16, nm, size=13, fill=CMUTED, ls='0'))
        if val: a(text(x + 6, y + 34, val, size=13, fill='#fff', ls='0'))
        x += w
def cellval(nm, s0, s1, t):
    x, y, w = cells[nm]
    a(f'<g>{before(t)}{text(x + 6, y + 34, s0, size=13, fill="#fff", ls="0")}</g>')
    a(f'<g opacity="0">{after(t)}{text(x + 6, y + 34, s1, size=13, fill=ROUTE, ls="0")}</g>')
cellval('TTL', '64', '63', TTL)
cellval('Header checksum', f'0x{C64:04X}', f'0x{C63:04X}', SUM)
def glow(nm, t0, t1):
    x, y, w = cells[nm]
    a(f'<rect class="fx" x="{x}" y="{y}" width="{w}" height="{RH}" fill="{ROUTE}" fill-opacity="0.18" stroke="{ROUTE}" stroke-width="2.5" opacity="0">{win(t0, t1)}</rect>')
glow('Destination address', LOOK, TTL)
glow('TTL', TTL, SUM)
glow('Header checksum', SUM, FWD)
PY = RY + 5 * RH + 8
a(f'<rect x="{GX}" y="{PY}" width="{32 * BW}" height="30" fill="{CDEEP}" stroke="rgba(79,196,230,0.25)" stroke-dasharray="4 3"/>')
a(text(GX + 6, PY + 20, 'payload: a TCP segment', size=13, fill=CMUTED, ls='0'))
STAT = [(LOOK, TTL, 'router: look up the destination'), (TTL, SUM, 'decrement the time to live'), (SUM, FWD, 'recompute the checksum'), (FWD, RESET, 'forward to the next hop')]
for t0, t1, s in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(GX, PY + 54, s, size=13, fill=ROUTE, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Twenty bytes in front of every IPv4 packet, laid out as RFC 791 set them in 1981. '
           'At each hop a router reads the destination to pick the next link, lowers the time to live by one and recomputes the checksum; the rest travels untouched.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The small fields.</b> <span class="key-term">IHL</span> is the header length in 32-bit words, almost always 5; <span class="key-term">ToS</span> once meant priority and now carries DSCP and ECN; <span class="key-term">Total length</span> counts header and payload, at most 65,535 bytes.</li>
          <li><b>Time to live.</b> The <span class="key-term">TTL</span> drops by one at every hop; if it reaches 0 the router drops the packet and reports back, which is how <code>traceroute</code> maps a path: probes with TTL 1, 2, 3 make each hop answer in turn. The checksum covers only the header, so each hop recomputes it.</li>
          <li><b>The source.</b> The sender writes it and no router checks it, which is why a source address alone proves nothing.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-4">
      <div class="diagram-label">Fig 9.4 · The IPv4 header, byte by byte</div>
      {svg}
      <p id="ch9-ip-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(hex(C64), hex(C63))
    splice('part-3', 'fig-9-4', 'ch9-ip-p2', card)
