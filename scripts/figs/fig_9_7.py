# Fig 9.7 · The internet's tier hierarchy (Pass 28, law 3). Chart Room. Three tiers, two sides; a packet
# climbs from a home ISP through a regional network to a Tier 1, crosses to another Tier 1 by
# settlement-free peering, and comes down to the server's host. "Pays" arrows show the money going up.
# t=0 (shift): packet crossing the peering link.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 300
NW, NH = 116, 40
ROWS = {1: 40, 2: 136, 3: 232}
L, R = (20, 264)
NODES = {('L', 1): 'NTT', ('R', 1): 'Lumen', ('L', 2): 'regional ISP', ('R', 2): 'regional ISP',
         ('L', 3): 'your ISP', ('R', 3): 'server host'}
def box(side, tier):
    return (L if side == 'L' else R, ROWS[tier])
def ctr(side, tier):
    x, y = box(side, tier); return x + NW / 2, y + NH / 2
D = 8.0
T = Timeline(D, shift=3.6)
PATH = [('L', 3), ('L', 2), ('L', 1), ('R', 1), ('R', 2), ('R', 3)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-21 svgd-part3-21">')
a('<title id="svgt-part3-21">Fig 9.7 · The internet\'s tier hierarchy</title>')
a('<desc id="svgd-part3-21">Three tiers of networks on each side. A packet leaves your ISP, a Tier 3 network, climbs to a regional ISP and then to a Tier 1 network such as NTT, crosses to another Tier 1 such as Lumen over a peering link for which neither pays, '
  'and comes down through a regional ISP to the server\'s host. Money flows the other way up each side: your ISP pays the regional network for transit, and the regional network pays the Tier 1.</desc>')
for (side, tier), lab in NODES.items():
    x, y = box(side, tier)
    a(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="2" fill="{CDEEP}" stroke="{ROUTE if tier == 1 else CSOFT}" stroke-opacity="0.8"/>')
    a(text(x + NW / 2, y + 25, lab, anchor='middle', size=13, fill='#fff', ls='0'))
for tier, y in ROWS.items():
    a(text(200, y + 25, f'Tier {tier}' if tier > 1 else '', anchor='middle', size=13, fill=CMUTED, ls='0'))
# links along the packet's path
for p, q in zip(PATH, PATH[1:]):
    (x1, y1), (x2, y2) = ctr(*p), ctr(*q)
    if p[1] == q[1]:
        x1, x2 = x1 + NW / 2, x2 - NW / 2
    else:
        y1, y2 = (y1 - NH / 2, y2 + NH / 2) if q[1] < p[1] else (y1 + NH / 2, y2 - NH / 2)
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.5" stroke-width="2"/>')
a(text(200, ROWS[1] - 6, 'Tier 1s peer, no payment', anchor='middle', size=13, fill=ROUTE, ls='0'))
# money: pays upward
for side in ('L', 'R'):
    for tier in (3, 2):
        x, _ = ctr(side, tier)
        x += -38 if side == 'L' else 38
        y0, y1 = ROWS[tier] - 4, ROWS[tier - 1] + NH + 4
        a(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1 + 6}" stroke="#d4a853" stroke-width="1.5" stroke-dasharray="3 3"/>')
        a(f'<polygon points="{x - 5},{y1 + 7} {x + 5},{y1 + 7} {x},{y1}" fill="#d4a853"/>')
        a(text(x + (6 if side == 'L' else -6), (y0 + y1) / 2 + 5, 'pays', anchor='start' if side == 'L' else 'end', size=13, fill='#d4a853', ls='0'))
# the packet
pts = [ctr(*p) for p in PATH]
seg = (D - 1.0) / (len(pts) - 1)
kx, ky = [(0.0, 0.0), (0.4, 0.0)], [(0.0, 0.0), (0.4, 0.0)]
for i, (x, y) in enumerate(pts[1:], 1):
    t = 0.4 + i * seg
    kx.append((t, x - pts[0][0])); ky.append((t, y - pts[0][1]))
kx.append((D, kx[-1][1])); ky.append((D, ky[-1][1]))
a(f'<g class="fx">{T.anim("opacity", [(0.0, 0.0), (0.39, 0.0), (0.4, 1.0), (D - 0.6, 1.0), (D - 0.59, 0.0), (D, 0.0)])}'
  f'<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="7" fill="{CYAN}" stroke="#fff" stroke-width="1.5"/></g></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A packet climbs from your ISP through a regional network to a Tier 1, crosses to another Tier 1 by peering, and comes back down to the server. Money flows up on both sides: each network pays the one above it for transit, while the dozen or so Tier 1s exchange traffic with each other for free.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tier 1.</b> A network that reaches the whole internet without paying anyone: Lumen, NTT, Arelion (formerly Telia Carrier), Tata, Cogent and a few more.</li>
          <li><b>Shortcuts.</b> Large networks also peer directly at internet exchange points, and big content providers connect straight into ISPs, so many packets never reach Tier 1.</li>
          <li><b>No centre.</b> The graph is held together by BGP announcements and commercial contracts; no authority runs it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-7">
      <div class="diagram-label">Fig 9.7 · The internet's tier hierarchy</div>
      {svg}
      <p id="ch9-routing-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-7', 'ch9-routing-p4', card)
