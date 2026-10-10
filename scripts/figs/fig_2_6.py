# Fig 2.6 · Inside a full adder (Pass 28, law 3). Two half adders (XOR + AND each) and an OR,
# live: A, B and carry-in step through all eight cases; wires carrying a 1 turn gold.
# Below, the addition the gates just did. t=0: 1 + 1 + 1 = 11.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 352
STEP = 0.9
CASES = [(a_, b_, c_) for a_ in (0, 1) for b_ in (0, 1) for c_ in (0, 1)]
T = Timeline(STEP * 8, shift=STEP * 7 + 0.45)
OFF = 'rgba(255,255,255,0.35)'
def when(vals):
    pts = []
    for i, v in enumerate(vals):
        if i: pts.append((i * STEP - 0.001, 1.0 if vals[i - 1] else 0.0))
        pts.append((i * STEP, 1.0 if v else 0.0))
    pts.append((STEP * 8 - 0.001, 1.0 if vals[-1] else 0.0))
    return T.anim('opacity', pts)
o = []; a = o.append
def wire(d, vals):
    a(f'<path d="{d}" fill="none" stroke="{OFF}" stroke-width="2"/>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{when(vals)}</path>')
def value(cx, cy, vals, r=13):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#141414" stroke="{OFF}" stroke-width="1.5"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}" fill-opacity="0.3" stroke="{GOLD}" stroke-width="1.8" opacity="0">{when(vals)}</circle>')
    a(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" {MONO} font-size="14" fill="rgba(255,255,255,0.7)">0{when([not v for v in vals])}</text>')
    a(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" {MONO} font-size="14" fill="#fff" opacity="0">1{when(vals)}</text>')
def gate(kind, x, cy):        # input edge x, output at x + 54
    if kind == 'AND':
        a(f'<path d="M {x} {cy - 20} h 32 a 20 20 0 0 1 0 40 h -32 Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
    else:
        a(f'<path d="M {x} {cy - 20} Q {x + 14} {cy} {x} {cy + 20} Q {x + 36} {cy + 20} {x + 54} {cy} Q {x + 36} {cy - 20} {x} {cy - 20} Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
        if kind == 'XOR':
            a(f'<path d="M {x - 7} {cy - 20} Q {x + 7} {cy} {x - 7} {cy + 20}" fill="none" stroke="#e8e8e8" stroke-width="2"/>')
    a(f'<text x="{x + 24}" y="{cy + 5}" text-anchor="middle" {MONO} font-size="13" fill="rgba(255,255,255,0.75)">{kind}</text>')

A = [c[0] for c in CASES]; B = [c[1] for c in CASES]; C = [c[2] for c in CASES]
s1 = [x ^ y for x, y, _ in CASES]; c1 = [x & y for x, y, _ in CASES]
S = [p ^ z for p, z in zip(s1, C)]; c2 = [p & z for p, z in zip(s1, C)]; CO = [p | q for p, q in zip(c1, c2)]
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-22 svgd-part1-22">')
a('<title id="svgt-part1-22">Fig 2.6 · Inside a full adder · two half adders and an OR</title>')
a('<desc id="svgd-part1-22">A full adder built from gates. A and B meet in an XOR and an AND: the first half adder. The XOR\'s output meets the carry-in in a second XOR and AND: '
  'the second half adder; its XOR gives the sum bit. Either AND\'s carry, through an OR, gives the carry-out. The inputs step through all eight cases.</desc>')
# wires (drawn first, under the gates)
wire('M 57 50 H 80 V 260 H 110 M 80 60 H 110', A)
wire('M 57 92 H 70 M 70 80 V 280 H 110 M 70 80 H 110', B)
wire('M 164 70 H 186 V 180 H 222 M 186 100 H 222', s1)
wire('M 200 33 V 120 H 222 M 200 120 V 200 H 222', C)
wire('M 276 110 H 358', S)
wire('M 276 190 H 290 V 222 H 302', c2)
wire('M 164 270 H 290 V 238 H 302', c1)
wire('M 356 230 H 358', CO)
for jx, jy in ((80, 60), (70, 80), (186, 100), (200, 120)):
    a(f'<circle cx="{jx}" cy="{jy}" r="3.5" fill="#e8e8e8"/>')
# gates
gate('XOR', 110, 70); gate('AND', 110, 270)
gate('XOR', 222, 110); gate('AND', 222, 190)
gate('OR', 302, 230)
# values and their names
value(44, 50, A); a(text(14, 55, 'A', size=14, fill=MUTED))
value(44, 92, B); a(text(14, 97, 'B', size=14, fill=MUTED))
value(200, 20, C); a(text(220, 25, 'carry in', size=14, fill=MUTED))
value(372, 110, S); a(text(386, 88, 'sum', anchor='end', size=14, fill=MUTED))
value(372, 230, CO); a(text(386, 208, 'carry out', anchor='end', size=14, fill=MUTED))
# the addition just done, in digits
for i, (x, y, z) in enumerate(CASES):
    tot = x + y + z
    pts = [(0.0, 0.0), (i * STEP - 0.001 if i else 0.0, 0.0), (i * STEP + 0.0005, 1.0), ((i + 1) * STEP - 0.002, 1.0), ((i + 1) * STEP - 0.001, 0.0), (STEP * 8 - 0.0005, 0.0)]
    a(f'<text x="200" y="330" text-anchor="middle" {MONO} font-size="18" fill="#fff" opacity="0">{x} + {y} + {z} = <tspan fill="{GOLD}">{tot // 2}{tot % 2}</tspan>{T.anim("opacity", pts)}</text>')
a(text(200, 348, 'carry out, then sum', anchor='middle', size=13, fill='rgba(255,255,255,0.45)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('A full adder is two half adders and an OR. A and B meet in the first; its sum meets the carry-in in the second, which gives the sum bit; '
           'either half adder\'s carry becomes the carry-out.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Half adder.</b> XOR gives the sum of two bits, AND their carry: 1 + 1 is 0, carry 1.</li>
          <li><b>Adding the carry.</b> The second half adder adds the incoming carry to the first sum.</li>
          <li><b>One carry out.</b> The two half adders can never both carry, so an OR is enough. Chain four of these and you have Fig 2.5.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-6">
      <div class="diagram-label">Fig 2.6 · Inside a full adder · two half adders and an OR</div>
      {svg}
      <p id="ch2-arithmetic-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-6', 'ch2-arithmetic-p9', card)
