# Fig 6.1 · The 1980s software crisis, in one chart (Pass 28, law 3). Brooks's arithmetic: n parts that
# can all affect each other have n(n − 1)/2 possible interactions. The graph steps through 2, 4, 8 and
# 16 parts with every pair drawn; a bar row per stage charts the count. t=0 (shift): 16 parts, all rows.
import math
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

NS = [2, 4, 8, 16]
pairs = lambda n: n * (n - 1) // 2
assert [pairs(n) for n in NS] == [1, 6, 28, 120]
W, H = 400, 330
GX, GY, GR = 200, 102, 80
D = 9.0
T = Timeline(D, shift=8.4)
ST = [0.8 + 1.6 * k for k in range(len(NS))]
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-37 svgd-part2-37">')
a('<title id="svgt-part2-37">Fig 6.1 · The 1980s software crisis, in one chart</title>')
a('<desc id="svgd-part2-37">Parts of a program drawn as points on a circle, with a line for every pair that could interact. Two parts have 1 possible interaction, four have 6, eight have 28 and sixteen have 120: '
  'n parts have n(n − 1)/2 pairs, so doubling the parts roughly quadruples the interactions.</desc>')
for k, n in enumerate(NS):
    pts = [(GX + GR * math.cos(2 * math.pi * i / n - math.pi / 2), GY + GR * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    vis = win(ST[k], ST[k + 1]) if k + 1 < len(NS) else held(ST[k])
    op = 0.75 if n <= 4 else (0.45 if n == 8 else 0.28)
    a(f'<g opacity="{0 if k + 1 < len(NS) else 1}">{vis}')
    for i in range(n):
        for j in range(i + 1, n):
            a(f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1"/>')
    for x, y in pts:
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{PANEL}" stroke="{PHOS}" stroke-width="2"/>')
    a('</g>')
# the chart: one row per stage
RX, RW = 112, 210
for k, n in enumerate(NS):
    y = 222 + k * 26
    w = max(3, pairs(n) / 120 * RW)
    a(f'<g>{held(ST[k])}{text(20, y + 13, f"{n} parts", size=13, fill=PHOS_SOFT, ls="0")}'
      f'<rect x="{RX}" y="{y}" width="{w:.1f}" height="16" rx="2" fill="{GOLD}" fill-opacity="0.6"/>'
      f'{text(RX + w + 8, y + 13, str(pairs(n)), size=13, fill=GOLD, ls="0")}</g>')
a(text(380, 214, 'possible interactions', anchor='end', size=13, fill=MUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ("Brooks's arithmetic: <em>n</em> parts that can each affect the others have <em>n</em>(<em>n</em>&#8239;−&#8239;1)/2 possible interactions, so doubling the parts roughly quadruples what can go wrong between them.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The source.</b> Fred Brooks, <em>The Mythical Man-Month</em> (1975), applied the count to people: each pair on a team needs a channel, so adding people to a late project makes it later.</li>
          <li><b>The same for code.</b> When any function may touch any data, every new part can collide with every old one, and the pairs outgrow the parts.</li>
          <li><b>The wall.</b> A class with private members lets the compiler refuse every touch that bypasses the interface, cutting the lines that may exist.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-1">
      <div class="diagram-label">Fig 6.1 · The 1980s software crisis, in one chart</div>
      {svg}
      <p id="ch6-complexity-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-1', 'ch6-complexity-p4', card)
