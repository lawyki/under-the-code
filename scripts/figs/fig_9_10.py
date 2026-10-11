# Fig 9.10 · IP spoofing: a forged source field (Pass 28, law 3, conceptual pass: the gap and the defence). Chart Room.
# Top, the packet's header: the source field is whatever the sender wrote. A column, sender network 203.0.113.0/24 →
# ISP edge → internet (routes by destination only) → destination 192.0.2.10, with a bystander 198.51.100.5 beside it.
# Run 1, no filter at the edge: a packet with the forged source 198.51.100.5 gets through, and the reply goes to the
# bystander. Then the edge checks sources (BCP 38): run 2, the sender's own address passes; run 3, the forged source is
# dropped at the edge. Addresses from the documentation ranges. t=0 (shift): the filter on, the forged packet dropped.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W = 400
D = 12.5
T = Timeline(D, shift=12.0)
R1, RP, R2, R3 = 0.8, 3.0, 5.2, 8.4          # forged run, its reply, genuine run, forged run with the filter on
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
def box(x, y, w, h, col, op=0.8):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{CDEEP}" stroke="{col}" stroke-opacity="{op}"/>')
def phases(x, y, spans, anchor='start'):
    for t0, t1, s, col in spans:
        vis = win(t0) if t1 is None else (first(t1) if t0 < 0.5 else lit(t0, t1))
        a(f'<g opacity="0">{vis}{text(x, y, s, anchor=anchor, size=13, fill=col, ls="0")}</g>')
# the header
box(20, 12, 360, 54, CSOFT, 0.5)
a(text(32, 34, 'src', size=13, fill=CMUTED, ls='0'))
a(text(32, 56, 'dst', size=13, fill=CMUTED, ls='0'))
a(text(80, 56, '192.0.2.10', size=13, fill='#fff', ls='0'))
phases(80, 34, [(0.31, R2, '198.51.100.5', RED), (R2, R3, '203.0.113.7', CYAN), (R3, None, '198.51.100.5', RED)])
phases(368, 34, [(0.31, R2, 'forged', RED), (R2, R3, 'genuine', CYAN), (R3, None, 'forged', RED)], anchor='end')
# the path
NX, NW, NH = 20, 210, 36
YS, YE, YI, YD = 88, 150, 212, 280
box(NX, YS, NW, NH, CSOFT); a(text(NX + 12, YS + 23, 'sender 203.0.113.x', size=13, fill='#fff', ls='0'))
box(NX, YE, NW, NH, ROUTE); a(text(NX + 12, YE + 23, 'ISP edge router', size=13, fill='#fff', ls='0'))
phases(NX + NW + 12, YE + 23, [(0.31, R2 - 0.6, 'no filter', CMUTED), (R2 - 0.6, None, 'checks src', CYAN)])
box(NX, YI, NW, NH, CSOFT, 0.5); a(text(NX + 12, YI + 23, 'routes on dst only', size=13, fill=CMUTED, ls='0'))
box(NX, YD, NW, NH, CSOFT); a(text(NX + 12, YD + 23, '192.0.2.10', size=13, fill='#fff', ls='0'))
box(250, YD, 130, NH, CSOFT, 0.5); a(text(315, YD + 23, '198.51.100.5', anchor='middle', size=13, fill=CMUTED, ls='0'))
LX = NX + NW - 20                             # the packets run down the right edge of the column, clear of the labels
a(f'<line x1="{LX}" y1="{YS + NH}" x2="{LX}" y2="{YD}" stroke="{CSOFT}" stroke-opacity="0.35" stroke-width="2"/>')
a(f'<g class="fx" opacity="0">{pulse(R2 - 0.6)}<rect x="{NX - 3}" y="{YE - 3}" width="{NW + 6}" height="{NH + 6}" rx="4" fill="none" stroke="{CYAN}" stroke-width="2"/></g>')
def run(t0, col, stop=None):
    y1 = stop if stop else YD + 6
    t1 = t0 + 1.6 * (y1 - YS - NH / 2) / (YD + 6 - YS - NH / 2)
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t1, y1 - YS - NH / 2), (D, y1 - YS - NH / 2)], 'y')
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.5)}<g>{mv}<circle cx="{LX}" cy="{YS + NH / 2}" r="6" fill="{col}"/></g></g>')
    return t1
run(R1, RED)
run(R2, CYAN)
ts = run(R3, RED, stop=YE + NH / 2)
a(f'<g class="fx" opacity="0">{pulse(ts)}<rect x="{NX - 3}" y="{YE - 3}" width="{NW + 6}" height="{NH + 6}" rx="4" fill="{RED}" fill-opacity="0.2" stroke="{RED}" stroke-width="2"/></g>')
# the reply goes to the address in the src field
mv = T.translate([(0.0, 0.0), (RP, 0.0), (RP + 0.8, 52), (D, 52)], 'x')
a(f'<g class="fx" opacity="0">{lit(RP, RP + 1.2)}<g>{mv}<circle cx="{LX}" cy="{YD + NH / 2}" r="6" fill="{ROUTE}"/></g></g>')
a(f'<g class="fx" opacity="0">{pulse(RP + 0.8)}<rect x="247" y="{YD - 3}" width="136" height="{NH + 6}" rx="4" fill="none" stroke="{ROUTE}" stroke-width="2"/></g>')
SY = YD + NH + 26
phases(20, SY, [(0.31, RP, 'no filter: the forgery gets through', RED), (RP, R2 - 0.6, 'the reply goes to 198.51.100.5', ROUTE),
                (R2 - 0.6, R3, 'filter on: its own address passes', CYAN), (R3, None, 'forged source: dropped at the edge', RED)])
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-24 svgd-part3-24">')
o.insert(1, '<title id="svgt-part3-24">Fig 9.10 · IP spoofing: a forged source field</title>')
o.insert(2, '<desc id="svgd-part3-24">A packet\'s header has a source and a destination field, and the sender fills in both. A sender on the network 203.0.113.0/24 sends a packet to 192.0.2.10 with the source field set to 198.51.100.5, an address that is not its own. With no filter at the ISP\'s edge router it gets through, since routers forward on the destination only, and the reply goes to 198.51.100.5 instead of the sender. '
  'Then the edge router checks sources: a packet from the sender\'s own address 203.0.113.7 passes, and the packet with the forged source is dropped at the edge.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The sender writes the source address itself and routers forward on the destination alone, so a forged source gets through and any reply goes to the address it names. '
           'Source address validation (BCP 38, 2000) closes the gap at the edge: the ISP drops packets whose source is not one of the customer\'s own addresses.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>One way only.</b> A forger never sees the reply, so it cannot hold a TCP conversation; spoofing suits single packets, which is why Chapter 10's SYN flood relies on it.</li>
          <li><b>Automating the check.</b> Strict unicast reverse path forwarding (uRPF) accepts a packet only if the router's route back to its source leaves through the interface the packet arrived on.</li>
          <li><b>Uneven deployment.</b> The filter only works where each edge network applies it; measurement projects such as CAIDA's Spoofer still find networks that let forged packets out.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-10">
      <div class="diagram-label">Fig 9.10 · IP spoofing: a forged source field</div>
      {svg}
      <p id="ch9-security-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-10', 'ch9-security-p3', card)
