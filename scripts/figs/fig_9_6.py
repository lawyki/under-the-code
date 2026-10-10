# Fig 9.6 · BGP path-vector announcements (Pass 28, law 3). Chart Room. Five ASes; the origin announces
# a prefix, each AS prepends its own number as it passes the route on, edges lighting as it crosses;
# 65030 hears two equal paths and picks one by policy; a copy that comes back to the origin is dropped
# as a loop. The steps list below. t=0 (shift): all steps shown.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 346
NW, NH = 62, 40
N = {'65001': (12, 104), '65010': (116, 26), '65020': (116, 182), '65030': (220, 104), '65099': (326, 104)}
def c(k):
    x, y = N[k]; return x + NW / 2, y + NH / 2
D = 11.0
STEPS = [(0.8, [('65001', '65010'), ('65001', '65020')], CYAN, '65001 announces 198.51.0.0/16'),
         (2.4, [('65010', '65030'), ('65020', '65030')], CYAN, 'path grows: 65010 65001, 65020 65001'),
         (4.0, [('65030', '65099')], CYAN, '65030 picks one by policy, adds itself'),
         (5.6, [('65010', '65001')], RED, 'back at 65001: its own number, dropped')]
T = Timeline(D, shift=9.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-20 svgd-part3-20">')
a('<title id="svgt-part3-20">Fig 9.6 · BGP path-vector announcements</title>')
a('<desc id="svgd-part3-20">Five autonomous systems. AS 65001 announces the prefix 198.51.0.0/16 with the path 65001. AS 65010 and AS 65020 each add their own number and pass it on, as 65010 65001 and 65020 65001. '
  'AS 65030 hears both equal-length paths, picks one by local policy, adds itself and announces 65030 65010 65001 to AS 65099. A copy announced back to AS 65001 carries its own number, so it is dropped as a loop.</desc>')
EDGES = [('65001', '65010'), ('65001', '65020'), ('65010', '65030'), ('65020', '65030'), ('65030', '65099')]
for u, v in EDGES:
    (x1, y1), (x2, y2) = c(u), c(v)
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity="0.3" stroke-width="2"/>')
for t0, edges, col, _ in STEPS:
    for u, v in edges:
        (x1, y1), (x2, y2) = c(u), c(v)
        dx = 0 if col != RED else 0
        a(f'<line class="fx" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="4" opacity="0">{win(t0, t0 + 1.4)}</line>')
for k, (x, y) in N.items():
    a(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="2" fill="{CDEEP}" stroke="{ROUTE if k == "65001" else CSOFT}" stroke-opacity="0.8"/>')
    a(text(x + NW / 2, y + 26, k, anchor='middle', size=13, fill='#fff', ls='0'))
a(text(12, 98, 'origin', size=13, fill=ROUTE, ls='0'))
a(text(326, 98, 'hears it', size=13, fill=CMUTED, ls='0'))
# what 65099 ends up with
a(f'<g>{held(4.0 + 0.8)}{text(388, 166, "65030 65010 65001", anchor="end", size=13, fill=CYAN, ls="0")}</g>')
# step list
LY = 252
a(text(12, LY - 12, 'AS NUMBERS · EACH ADDS ITSELF', size=13, fill=CMUTED))
for i, (t0, _, col, s) in enumerate(STEPS):
    y = LY + 8 + i * 22
    a(f'<g>{held(t0)}{text(12, y, f"{i + 1}", size=13, fill=CMUTED, ls="0")}{text(32, y, s, size=13, fill=RED if col == RED else CSOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('BGP routes by passing announcements: the origin announces its prefix, and each network adds its own AS number before passing the route on, so every route carries the list of networks it crossed. '
           'Seeing its own number in that list is how an AS spots a loop and drops it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Choosing.</b> Given several paths, an AS applies its own policy first, often business relationships; path length only breaks ties by default.</li>
          <li><b>AS numbers.</b> 65001 to 65099 here are from the private range; real networks use public numbers, such as 15169 for Google.</li>
          <li><b>Scale.</b> Every router at the internet's core holds a route to roughly a million IPv4 prefixes, learned this way.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-6">
      <div class="diagram-label">Fig 9.6 · BGP path-vector announcements</div>
      {svg}
      <p id="ch9-routing-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-6', 'ch9-routing-p3', card)
