# Fig 9.3 · Baran 1964: three architectural shapes (Pass 28, law 3). Chart Room paper card. The same
# strike hits all three: the star loses its centre, the decentralised net one hub, the mesh three
# nodes. Links to dead nodes vanish; survivors cut off turn grey; each shape reports how many survivors
# can still reach each other (computed by search, asserted). t=0 (shift): after the strike.
import math
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D, GREEN, RED = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f', '#2e7e4f', '#b3261e'
W, H = 400, 236
D = 8.0
STRIKE, AFTER, RESET = 1.6, 2.2, 7.4
T = Timeline(D, shift=5.0)
def gone(t):      # visible until t, back at the reset
    return T.anim('opacity', [(0.0, 1.0), (t - 0.008, 1.0), (t - 0.005, 0.0), (RESET - 0.002, 0.0), (RESET, 1.0), (D, 1.0)])
def comes(t):
    return T.anim('opacity', [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (RESET - 0.008, 1.0), (RESET - 0.005, 0.0), (D, 0.0)])
def comp(nodes, edges, alive):
    adj = {n: set() for n in nodes if n in alive}
    for u, v in edges:
        if u in alive and v in alive: adj[u].add(v); adj[v].add(u)
    reach = set()                     # survivors that can still reach at least one other survivor
    for s in adj:
        seen, st = {s}, [s]
        while st:
            x = st.pop()
            for y in adj[x] - seen: seen.add(y); st.append(y)
        if len(seen) > 1: reach |= seen
    return reach
def star(cx, cy):
    pos = {'c': (cx, cy)}
    for i in range(8):
        a_ = 2 * math.pi * i / 8
        pos[f'l{i}'] = (cx + 44 * math.cos(a_), cy + 44 * math.sin(a_))
    return pos, [('c', f'l{i}') for i in range(8)], {'c'}
def decent(cx, cy):
    pos, edges = {}, []
    hubs = [(cx, cy - 26), (cx - 30, cy + 22), (cx + 30, cy + 22)]
    for h, (hx, hy) in enumerate(hubs):
        pos[f'h{h}'] = (hx, hy)
        for j in range(3):
            a_ = -math.pi / 2 + (h * 2 * math.pi / 3) + (j - 1) * 0.7
            pos[f'h{h}l{j}'] = (hx + 22 * math.cos(a_), hy + 22 * math.sin(a_))
            edges.append((f'h{h}', f'h{h}l{j}'))
    edges += [('h0', 'h1'), ('h1', 'h2'), ('h0', 'h2')]
    return pos, edges, {'h0'}
def mesh(cx, cy):
    pos, edges = {}, []
    for r in range(3):
        for c in range(4):
            pos[f'm{r}{c}'] = (cx - 45 + c * 30, cy - 30 + r * 30)
            if c < 3: edges.append((f'm{r}{c}', f'm{r}{c + 1}'))
            if r < 2: edges.append((f'm{r}{c}', f'm{r + 1}{c}'))
    edges += [('m00', 'm11'), ('m12', 'm23'), ('m20', 'm11'), ('m13', 'm02')]
    return pos, edges, {'m11', 'm03', 'm22'}
PANELS = [('centralised', star(66, 96)), ('decentralised', decent(200, 96)), ('distributed', mesh(334, 96))]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-17 svgd-part3-17">')
a('<title id="svgt-part3-17">Fig 9.3 · Baran 1964: three architectural shapes</title>')
results = []
for name, (pos, edges, dead) in PANELS:
    alive = set(pos) - dead
    big = comp(pos, edges, alive)
    results.append((name, len(big), len(alive)))
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        line = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ACC}" stroke-opacity="0.55" stroke-width="1.5"/>'
        a(f'<g>{gone(AFTER)}{line}</g>' if (u in dead or v in dead) else line)
    for n, (x, y) in pos.items():
        if n in dead:
            a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{ACC}"><animate attributeName="fill" values="{ACC};{ACC}" dur="1s"/></circle>')
            a(f'<g>{comes(STRIKE)}<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{RED}"/>'
              f'<line x1="{x - 4:.1f}" y1="{y - 4:.1f}" x2="{x + 4:.1f}" y2="{y + 4:.1f}" stroke="#fff" stroke-width="2"/><line x1="{x + 4:.1f}" y1="{y - 4:.1f}" x2="{x - 4:.1f}" y2="{y + 4:.1f}" stroke="#fff" stroke-width="2"/></g>')
        else:
            a(f'<g>{gone(AFTER)}<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{ACC}"/></g>')
            col = GREEN if n in big else 'rgba(18,42,63,0.3)'
            a(f'<g>{comes(AFTER)}<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{col}"/></g>')
    cx = {'centralised': 66, 'decentralised': 200, 'distributed': 334}[name]
    a(text(cx, 168, name, anchor='middle', size=13, fill=INK, ls='0'))
    a(f'<g>{comes(AFTER + 0.4)}{text(cx, 190, f"{len(big)} of {len(alive)}", anchor="middle", size=14, fill=GREEN if len(big) == len(alive) else ROUTE_D, ls="0")}</g>')
assert [r[1] for r in results] == [0, 8, 9] and [r[2] for r in results] == [8, 11, 9], results
a(text(200, 22, 'the same strike on three networks', anchor='middle', size=13, fill=INK_SOFT, ls='0'))
a(f'<g>{comes(AFTER + 0.4)}{text(200, 222, "survivors that can reach another", anchor="middle", size=13, fill=INK_SOFT, ls="0")}</g>')
a('<desc id="svgd-part3-17">Paul Baran\'s three network shapes from 1964, each hit by the same kind of strike. The centralised star loses its centre, and none of its eight survivors can reach another. '
  'The decentralised network loses one of its three hubs: that hub\'s three nodes are cut off, and 8 of the 11 survivors stay connected. '
  'The distributed mesh loses three nodes, and all nine survivors can still reach each other by routing around the gaps.</desc>')
a('</svg>')
svg = '\n'.join(o)
svg = svg.replace('<animate attributeName="fill" values="#10719d;#10719d" dur="1s"/>', '')

caption = ('Paul Baran\'s 1964 RAND memoranda compared three shapes under attack: a star dies with its centre, a set of hubs loses whole regions, and a mesh with no hubs routes around its losses. '
           'His case for the third, packets finding their own way through redundant links, became the design argument of the ARPANET.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The question.</b> Baran, at RAND for the US Air Force, asked how a communications network could keep working after part of it was destroyed.</li>
          <li><b>Redundancy.</b> His studies found that each node needs only a few links, around three or four, for the mesh to survive heavy losses.</li>
          <li><b>Today.</b> The internet is no pure mesh, with large exchange points and backbones, but routing still sends traffic around a failed link or router.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-9-3">
      <div class="diagram-label">Fig 9.3 · Baran 1964: three architectural shapes</div>
      {svg}
      <p id="ch9-arpanet-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(results)
    splice('part-3', 'fig-9-3', 'ch9-arpanet-p5', card)
