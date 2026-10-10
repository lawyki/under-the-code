# Fig 2.4 · Everything from NAND (Pass 28, law 3). Three live networks of NAND gates: inputs tied
# (NOT), NAND then NOT (AND), NOT both inputs then NAND (OR, De Morgan). Inputs step through every
# case; wires carrying a 1 turn gold; each output matches the gate it stands in for.
from figlib import Timeline, text, splice, MONO, GOLD, MUTED

W, H = 400, 424
STEP = 1.2
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
T = Timeline(STEP * 4, shift=STEP * 2 + 0.6)
OFF = 'rgba(255,255,255,0.35)'
def when(vals):
    pts = []
    for i, v in enumerate(vals):
        if i: pts.append((i * STEP - 0.001, 1.0 if vals[i - 1] else 0.0))
        pts.append((i * STEP, 1.0 if v else 0.0))
    pts.append((STEP * 4 - 0.001, 1.0 if vals[-1] else 0.0))
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
def nand(x, cy):              # input edge at x; output (after the bubble) at x + 60
    a(f'<path d="M {x} {cy - 20} h 22 a 20 20 0 0 1 0 40 h -22 Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
    a(f'<circle cx="{x + 48}" cy="{cy}" r="5" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
    return x + 53

a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-20 svgd-part1-20">')
a('<title id="svgt-part1-20">Fig 2.4 · Everything from NAND · NOT, AND and OR built from one gate</title>')
a('<desc id="svgd-part1-20">Three circuits built only of NAND gates. One NAND with its inputs tied together is NOT. A NAND followed by that NOT is AND. '
  'Inverting both inputs and then taking their NAND is OR, by De Morgan\'s law. The inputs step through every case and each output matches the ordinary gate.</desc>')
A = [c[0] for c in CASES]; B = [c[1] for c in CASES]
nA = [1 - v for v in A]; nB = [1 - v for v in B]
# NOT
a(text(20, 26, 'NOT', size=15, fill='#fff')); a(text(64, 26, 'one NAND, inputs tied', size=14, fill=MUTED))
value(34, 64, A)
wire('M 47 64 H 70 M 70 56 V 72 M 70 56 H 100 M 70 72 H 100', A)
out = nand(100, 64)
wire(f'M {out} 64 H 330', nA)
value(346, 64, nA)
# AND
a(text(20, 124, 'AND', size=15, fill='#fff')); a(text(64, 124, 'NAND, then NOT', size=14, fill=MUTED))
n1 = [1 - (x & y) for x, y in CASES]; AND = [x & y for x, y in CASES]
value(34, 150, A); value(34, 190, B)
wire('M 47 150 H 74 V 160 H 100', A); wire('M 47 190 H 74 V 180 H 100', B)
o1 = nand(100, 170)
wire(f'M {o1} 170 H 182 M 182 162 V 178 M 182 162 H 206 M 182 178 H 206', n1)
o2 = nand(206, 170)
wire(f'M {o2} 170 H 330', AND)
value(346, 170, AND)
# OR
a(text(20, 240, 'OR', size=15, fill='#fff')); a(text(64, 240, 'NOT both, then NAND', size=14, fill=MUTED))
OR = [x | y for x, y in CASES]
value(34, 278, A); value(34, 362, B)
wire('M 47 278 H 70 M 70 270 V 286 M 70 270 H 100 M 70 286 H 100', A)
wire('M 47 362 H 70 M 70 354 V 370 M 70 354 H 100 M 70 370 H 100', B)
oa = nand(100, 278); ob = nand(100, 362)
wire(f'M {oa} 278 H 184 V 310 H 206', nA); wire(f'M {ob} 362 H 184 V 330 H 206', nB)
o3 = nand(206, 320)
wire(f'M {o3} 320 H 330', OR)
value(346, 320, OR)
for jx, jy in ((70, 64), (182, 170), (70, 278), (70, 362)):   # junctions: one wire splitting to two inputs
    a(f'<circle cx="{jx}" cy="{jy}" r="3.5" fill="#e8e8e8"/>')
a(text(20, 412, 'every gate drawn here is a NAND', size=13, fill='rgba(255,255,255,0.45)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('NAND alone is enough: tie its inputs together and it is NOT, follow it with that NOT and it is AND, invert both inputs first and it is OR. '
           'From this one gate any circuit can be built, as Henry Sheffer showed in 1913.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>NAND.</b> AND with its output inverted: 0 only when both inputs are 1. The bubble on the symbol is the inversion.</li>
          <li><b>NOT.</b> With both inputs on A, NAND gives ¬(A · A), which is ¬A.</li>
          <li><b>AND.</b> Invert a NAND once more: ¬(¬(A · B)) = A · B.</li>
          <li><b>OR.</b> De Morgan's law: A + B = ¬(¬A · ¬B), a NAND of the two inverted inputs.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-4">
      <div class="diagram-label">Fig 2.4 · Everything from NAND · NOT, AND and OR built from one gate</div>
      {svg}
      <p id="ch2-gates-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-4', 'ch2-gates-p6', card)
