# Fig 1.7 · ENIAC and the Apple M4 (Pass 31, Part I, from an empty script). Job: real thing. Takeaway: a room of
# tubes and a fingertip chip do the same switching; built together on chips, switches shrank.
# Concept: the two as they look, each at its own scale. Above, ENIAC's room in perspective: its U of cabinets lining
# three walls, each panel studded with glowing tubes, a person standing among them. Below, the M4 on a fingertip.
# The one figure between them is the ratio. Motion: now and then a tube burns out (a red flash), as they did.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 440
INK, HEAT = '#ece6da', '#f0a35a'
T = Timeline(8, shift=0.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-8 svgd-part1-8">')
a('<title id="svgt-part1-8">Fig 1.7 · ENIAC and the Apple M4 · the same job, 79 years apart</title>')
a('<desc id="svgd-part1-8">ENIAC, 1945, drawn as its room: a U of cabinets, thirty metres of them in all, lining three walls, every '
  'panel studded with glowing vacuum tubes, 17,468 of them, and a person standing among them for scale; now and then a tube burns '
  'out. Below, the Apple M4 of 2024: a chip resting on a fingertip, holding 28 billion transistors, about 1.6 million times as many '
  'switches.</desc>')

# ---------- ENIAC's room, one-point perspective ----------
BL, BR, BT, BB = 122, 278, 58, 118          # the back wall
FL, FR, FT, FB = 22, 378, 18, 176           # the front edges of the side walls
CAB, EDGE = '#24211c', 'rgba(236,230,218,0.42)'
def lerp(p, q, f): return p + (q - p) * f
def quad(pts, fill=CAB, stroke=EDGE):
    a(f'<path d="M {" L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"/>')
tubes = []
def tube_grid(corner, cols, rows):
    """corner: four points of one panel face (top-left, top-right, bottom-right, bottom-left)."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corner
    for r in range(rows):
        for c in range(cols):
            u, v = (c + 0.5) / cols, (r + 0.6) / (rows + 0.4)
            tx, ty = lerp(lerp(x0, x1, u), lerp(x3, x2, u), v), lerp(lerp(y0, y1, u), lerp(y3, y2, u), v)
            tubes.append((tx, ty, max(1.1, (x1 - x0) / cols * 0.22)))
# the floor
quad([(FL, FB), (BL, BB), (BR, BB), (FR, FB)], fill='#16140f', stroke='rgba(236,230,218,0.18)')
# back wall: 6 panels
for k in range(6):
    xa, xb = lerp(BL, BR, k / 6), lerp(BL, BR, (k + 1) / 6)
    quad([(xa, BT), (xb, BT), (xb, BB), (xa, BB)])
    tube_grid([(xa, BT), (xb, BT), (xb, BB), (xa, BB)], 3, 5)
# side walls: 5 panels each, receding to the back corners
for side in (0, 1):
    for k in range(5):
        f0, f1 = k / 5, (k + 1) / 5
        # perspective-ish spacing: panels shrink toward the back
        g0, g1 = f0 ** 0.7, f1 ** 0.7
        if side == 0:
            xa, xb = lerp(FL, BL, g0), lerp(FL, BL, g1)
            ta, tb, ba, bb = lerp(FT, BT, g0), lerp(FT, BT, g1), lerp(FB, BB, g0), lerp(FB, BB, g1)
        else:
            xa, xb = lerp(FR, BR, g0), lerp(FR, BR, g1)
            ta, tb, ba, bb = lerp(FT, BT, g0), lerp(FT, BT, g1), lerp(FB, BB, g0), lerp(FB, BB, g1)
        pts = [(xa, ta), (xb, tb), (xb, bb), (xa, ba)]
        quad(pts)
        tube_grid(pts, 2, 6)
for tx, ty, r in tubes:
    a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{r:.1f}" fill="{HEAT}" opacity="0.8"/>')
# a tube burns out now and then: it flashes red and goes dark
for (k, t0) in ((23, 1.5), (77, 5.2)):
    tx, ty, r = tubes[k]
    a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{r + 2.2:.1f}" fill="#ec4f4f" opacity="0">'
      f'{T.anim("opacity", [(t0 - 0.05, 0.0), (t0, 1.0), (t0 + 0.5, 0.0)])}</circle>')
# a person, for scale (cabinets about 2.4 m tall; a person about 1.75 m), standing on the floor near the back
px, pf = 200, 150
a(f'<g fill="#9fb4ff" opacity="0.95"><circle cx="{px}" cy="{pf - 33}" r="4.2"/>'
  f'<path d="M {px - 6} {pf - 27} h 12 l 1.5 14 h -3 l -0.5 13 h -3.6 l -0.4 -10 l -0.4 10 h -3.6 l -0.5 -13 h -3 z"/></g>')
a(text(20, 204, 'ENIAC · 1945', size=15, fill=INK))
a(text(380, 204, '17,468 vacuum tubes', anchor='end', size=14, fill=HEAT))
a(text(380, 222, '30 m of cabinets', anchor='end', size=14, fill=MUTED))

# ---------- the ratio ----------
a('<line x1="20" y1="244" x2="380" y2="244" stroke="rgba(255,255,255,0.12)"/>')
a(text(200, 276, '×1.6 million switches', anchor='middle', size=17, fill=GOLD))
a(text(200, 296, '79 years later', anchor='middle', size=14, fill=MUTED))
a('<line x1="20" y1="314" x2="380" y2="314" stroke="rgba(255,255,255,0.12)"/>')

# ---------- the M4 on a fingertip ----------
fx, ftip = 110, 344
a(f'<path d="M {fx - 42} {H} V {ftip + 44} C {fx - 42} {ftip + 8} {fx - 24} {ftip - 4} {fx} {ftip - 4} '
  f'C {fx + 24} {ftip - 4} {fx + 42} {ftip + 8} {fx + 42} {ftip + 44} V {H}" fill="none" stroke="rgba(236,230,218,0.7)" stroke-width="1.6"/>')
a(f'<path d="M {fx - 24} {ftip + 40} C {fx - 24} {ftip + 18} {fx + 24} {ftip + 18} {fx + 24} {ftip + 40}" fill="none" stroke="rgba(236,230,218,0.25)" stroke-width="1.2"/>')
# the chip package and its die, resting on the fingertip
a(f'<rect x="{fx - 22}" y="{ftip + 2}" width="44" height="44" rx="3" fill="#1d2230" stroke="#9aa3b4" stroke-width="1.4"/>')
a(f'<rect x="{fx - 12}" y="{ftip + 12}" width="24" height="24" rx="1.5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
a(f'<rect x="{fx - 12}" y="{ftip + 12}" width="24" height="24" rx="1.5" fill="{BLUE}" opacity="0.22"/>')
a(text(190, 362, 'Apple M4 · 2024', size=15, fill=INK))
a(text(190, 386, '28 billion', size=14, fill=BLUE))
a(text(190, 404, 'transistors', size=14, fill=BLUE))
a('</svg>')
svg = '\n'.join(o)

caption = ("ENIAC's thirty metres of cabinets held 17,468 vacuum tubes; the M4 fits under a fingertip and holds 28 billion "
           'transistors, about 1.6 million times as many switches. Each is drawn at its own scale: in life ENIAC\'s row of cabinets '
           'is some two thousand times longer than the chip.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The same job.</b> Both machines flip switches according to instructions; what changed is the size of the switch, from a glass tube to a speck of silicon.</li>
          <li><b>The red flashes.</b> As the figure plays, a tube burns out. ENIAC lost one about every two days; a chip's transistors run for years.</li>
          <li><b>The numbers.</b> 28,000,000,000 ÷ 17,468 ≈ 1.6 million. (From the 4004 of 1971 to the M4 the factor is twelve million: Fig 1.6.)</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-7">
      <div class="diagram-label">Fig 1.7 · ENIAC and the Apple M4 · the same job, 79 years apart</div>
      {svg}
      <p id="ch1-transistor-p17" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-7', 'ch1-transistor-p17', card)
