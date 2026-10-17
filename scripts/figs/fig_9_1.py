# Fig 9.1 · One call, two architectures (Pass 28, law 3). Chart Room. A circuit: one path reserved
# end to end; the voice flows, stops for a silence, and the path stays reserved. A packet mesh: three
# packets take three paths, arrive 2, 1, 3, and are put back in order at B. t=0 (shift): all arrived.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 320
D = 8.0
T = Timeline(D, shift=7.2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
def node(x, y, lab="", big=False):
    if big:
        a(f'<rect x="{x - 18}" y="{y - 16}" width="36" height="32" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
        a(text(x, y + 6, lab, anchor='middle', size=15, fill='#fff', ls='0'))
    else:
        a(f'<circle cx="{x}" cy="{y}" r="8" fill="{CPLATE}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-15 svgd-part3-15">')
a('<title id="svgt-part3-15">Fig 9.1 · One call, two architectures</title>')
a('<desc id="svgd-part3-15">Two ways to carry a conversation from A to B. Circuit switching reserves one path through the switches for the whole call; the voice flows along it, and during a silence the path stays reserved and unused. '
  'Packet switching shares a mesh of routers: three packets from A take three different paths, arrive in the order 2, 1, 3, and B puts them back in order.</desc>')
# circuit
a(text(20, 22, 'CIRCUIT: one path, reserved', size=13, fill=ROUTE))
CY = 64
xs = [44, 130, 210, 290, 356]
a(f'<line x1="{xs[0]}" y1="{CY}" x2="{xs[-1]}" y2="{CY}" stroke="{ROUTE}" stroke-width="6" stroke-opacity="0.35"/>')
node(xs[0], CY, 'A', True); node(xs[-1], CY, 'B', True)
for x in xs[1:-1]: node(x, CY)
# voice samples flowing; a silence from 3.0 to 5.0
for k in range(6):
    t0 = 0.4 + k * 0.5
    if 3.0 <= t0 < 5.0: continue
    a(f'<g opacity="0">{win(t0, t0 + 1.6)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + 1.6, xs[-1] - xs[0] - 36), (D, xs[-1] - xs[0] - 36)], "x")}'
      f'<circle cx="{xs[0] + 18}" cy="{CY}" r="4" fill="{ROUTE}"/></g></g>')
for k in range(4):
    t0 = 5.0 + k * 0.5
    a(f'<g opacity="0">{win(t0, t0 + 1.6)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t0 + 1.6, xs[-1] - xs[0] - 36), (D, xs[-1] - xs[0] - 36)], "x")}'
      f'<circle cx="{xs[0] + 18}" cy="{CY}" r="4" fill="{ROUTE}"/></g></g>')
a(f'<g opacity="0">{win(3.4, 5.4)}{text(200, CY + 34, "silence: still reserved", anchor="middle", size=13, fill=ROUTE, ls="0")}</g>')
a(f'<g>{T.anim("opacity", [(0.0, 1.0), (3.4 - 0.008, 1.0), (3.4 - 0.005, 0.0), (5.4 - 0.002, 0.0), (5.4, 1.0), (D, 1.0)])}{text(200, CY + 34, "nobody else may use it", anchor="middle", size=13, fill=CMUTED, ls="0")}</g>')
# packets
a(text(20, 140, 'PACKETS: a shared mesh', size=13, fill=CYAN))
A, B = (44, 222), (356, 222)
R = {'r1': (150, 176), 'r2': (250, 176), 'r3': (150, 268), 'r4': (250, 268)}
EDGES = [(A, R['r1']), (A, R['r3']), (R['r1'], R['r2']), (R['r3'], R['r4']), (R['r1'], R['r4']), (R['r2'], B), (R['r4'], B), (R['r1'], R['r3']), (R['r2'], R['r4'])]
for (x1, y1), (x2, y2) in EDGES:
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="1.5"/>')
node(*A, 'A', True); node(*B, 'B', True)
for x, y in R.values(): node(x, y)
BE = (B[0] - 30, B[1])
PATHS = {1: [A, R['r1'], R['r2'], BE], 2: [A, R['r3'], R['r4'], BE], 3: [A, R['r1'], R['r4'], BE]}
START = {1: 0.6, 2: 1.0, 3: 1.4}
LEGS = {1: [0.7, 1.3, 0.7], 2: [0.6, 0.6, 0.6], 3: [0.7, 1.2, 0.9]}
ARR = {}
for n, pts in PATHS.items():
    t = START[n]
    kx, ky = [(0.0, 0.0), (t, 0.0)], [(0.0, 0.0), (t, 0.0)]
    for (x, y), dt in zip(pts[1:], LEGS[n]):
        t += dt
        kx.append((t, x - A[0])); ky.append((t, y - A[1]))
    ARR[n] = t
    kx.append((D, kx[-1][1])); ky.append((D, ky[-1][1]))
    a(f'<g class="fx" opacity="0">{win(START[n] + 0.25, t + 0.15)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}'
      f'<circle cx="{A[0]}" cy="{A[1]}" r="9" fill="{CYAN}"/>{text(A[0], A[1] + 5, str(n), anchor="middle", size=13, fill=CDEEP, ls="0")}</g></g></g>')
order = sorted(ARR, key=ARR.get)
assert order == [2, 1, 3], order
a(text(20, 312, 'arrived', size=13, fill=CMUTED, ls='0'))
for i, n in enumerate(order):
    a(f'<g>{held(ARR[n])}{text(104 + i * 22, 312, str(n), anchor="middle", size=14, fill=CYAN, ls="0")}</g>')
a(f'<g>{held(max(ARR.values()) + 0.4)}{text(380, 312, "in order: 1 2 3", anchor="end", size=13, fill="#fff", ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same call both ways: <span class="key-term">circuit switching</span> holds one path through every silence, while three packets cross a shared mesh by three paths, arrive 2, 1, 3 and are put back in order by B. Computers talk in bursts, which is why the ARPANET was built on packets.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Circuits.</b> They guarantee capacity and steady delay, which suits a voice that never stops; the price is capacity left idle whenever it does.</li>
          <li><b>Packets.</b> Each carries its destination, so a router can send it any way that works and route around a failure.</li>
          <li><b>Putting it back.</b> Sequence numbers let the receiver reorder packets and notice gaps; Chapter 10's TCP does exactly that.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-1">
      <div class="diagram-label">Fig 9.1 · One call, two architectures</div>
      {svg}
      <p id="ch9-circuits-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-1', 'ch9-circuits-p4', card)
