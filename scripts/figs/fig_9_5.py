# Fig 9.5 · A 4 KB packet, fragmented onto a 1500-byte link (Pass 28, law 3). Chart Room. The packet
# splits into three fragments (1480 + 1480 + 1040 bytes of data, offsets 0, 185, 370 in 8-byte units).
# Run 1: all three cross and are reassembled. Run 2: fragment 2 is lost and the whole packet is
# discarded. t=0 (shift): run 1 reassembled.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
DATA, MTU, HDR = 4000, 1500, 20
SIZES = []
left = DATA
while left > 0:
    n = min(left, (MTU - HDR) // 8 * 8); SIZES.append(n); left -= n
OFFS = [sum(SIZES[:i]) // 8 for i in range(len(SIZES))]
assert SIZES == [1480, 1480, 1040] and OFFS == [0, 185, 370]
W, H = 400, 338
BX, BW, GAP = 20, 116, 6
FY, RY = 108, 228
D = 12.0
R1, R2 = 0.6, 6.4
FALL = 1.6
T = Timeline(D, shift=R1 + FALL + 2.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-19 svgd-part3-19">')
a('<title id="svgt-part3-19">Fig 9.5 · A 4 KB packet, fragmented onto a 1500-byte link</title>')
a('<desc id="svgd-part3-19">A packet carrying 4000 bytes of data, identification 42, meets a link whose largest packet is 1500 bytes. It is split into three fragments carrying 1480, 1480 and 1040 bytes, '
  'with fragment offsets 0, 185 and 370 (counted in 8-byte units) and the more-fragments flag set on all but the last. In a first run all three arrive and the receiver reassembles the packet. '
  'In a second run fragment 2 is lost, and since IP cannot ask for one fragment again, the receiver discards the whole packet.</desc>')
a(text(20, 22, 'ORIGINAL · ID 42', size=13, fill=CMUTED))
a(f'<rect x="20" y="32" width="360" height="36" rx="2" fill="{CPLATE}" stroke="{CYAN}" stroke-opacity="0.7"/>')
a(text(200, 55, f'{DATA} bytes of data', anchor='middle', size=13, fill='#fff', ls='0'))
a(text(20, 92, f'link MTU {MTU} bytes: split', size=13, fill=ROUTE, ls='0'))
a(text(20, RY + 72, 'RECEIVER', size=13, fill=CMUTED))
for k, (n, off) in enumerate(zip(SIZES, OFFS)):
    x = BX + k * (BW + GAP)
    mf = 1 if k < len(SIZES) - 1 else 0
    a(f'<rect x="{x}" y="{RY}" width="{BW}" height="52" rx="2" fill="{CDEEP}" stroke="rgba(223,234,242,0.2)" stroke-dasharray="3 3"/>')
    for run, t0 in enumerate((R1, R2)):
        lost = run == 1 and k == 1
        tk = t0 + 0.3 * k
        fy = [(0.0, 0.0), (tk, 0.0), (tk + FALL, (RY - FY) * (0.45 if lost else 1.0)), (D, (RY - FY) * (0.45 if lost else 1.0))]
        end = t0 + FALL + 3.6
        g = (f'<rect x="{x}" y="{FY}" width="{BW}" height="52" rx="2" fill="{CYAN}" fill-opacity="0.2" stroke="{CYAN}"/>'
             + text(x + BW / 2, FY + 21, f'{n} B', anchor='middle', size=13, fill='#fff', ls='0')
             + text(x + BW / 2, FY + 41, f'off {off} · MF {mf}', anchor='middle', size=13, fill=CSOFT, ls='0'))
        a(f'<g class="fx" opacity="0">{win(tk - 0.4, (tk + FALL) if lost else end)}<g>{T.translate(fy, "y")}{g}</g></g>')
        if lost:
            ly = FY + (RY - FY) * 0.45 + 26
            a(f'<g opacity="0">{win(tk + FALL, end)}<line x1="{x + 36}" y1="{ly - 20}" x2="{x + BW - 36}" y2="{ly + 20}" stroke="{RED}" stroke-width="4"/>'
              f'<line x1="{x + BW - 36}" y1="{ly - 20}" x2="{x + 36}" y2="{ly + 20}" stroke="{RED}" stroke-width="4"/>'
              f'{text(x + BW / 2, ly - 28, "lost", anchor="middle", size=13, fill=RED, ls="0")}</g>')
OK_T = R1 + 0.6 + FALL + 0.4
a(f'<g opacity="0">{win(OK_T, R2 - 0.2)}{text(20, 326, "all three in: packet rebuilt", size=13, fill=CYAN, ls="0")}</g>')
a(f'<g opacity="0">{win(R2 + 0.6 + FALL + 0.6, D - 0.3)}{text(20, 326, "one missing: whole packet discarded", size=13, fill=RED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A packet carrying 4000 bytes of data meets a link that carries at most 1500 bytes, so it is cut into three fragments. Lose any one and the receiver must throw the whole packet away, since IP cannot ask for a single fragment again.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The arithmetic.</b> Each fragment needs its own 20-byte header, leaving 1480 bytes of data; 1480 / 8 = 185, so the second fragment starts at offset 185.</li>
          <li><b>Avoiding it.</b> Path MTU discovery finds the smallest link on the route so the sender can send packets that fit.</li>
          <li><b>IPv6.</b> Routers never fragment; only the sender may, after learning the path's limit.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-5">
      <div class="diagram-label">Fig 9.5 · A 4 KB packet, fragmented onto a 1500-byte link</div>
      {svg}
      <p id="ch9-ip-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-5', 'ch9-ip-p4', card)
