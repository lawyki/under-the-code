# Fig 2.4 · Everything from NAND (Pass 31, Part I, from an empty script). Job: function. Takeaway: NAND is AND
# inverted, so tied inputs give NOT and inverting again gives AND: one gate builds all.
# Concept: Fig 2.3's grammar (the same values, wires lit gold while they carry 1, the case strip), now with one shape
# only: every gate drawn is a NAND. NOT is one NAND with its inputs tied; AND is a NAND followed by that NOT; OR is a
# NAND of the two inverted inputs. The inputs step through every case together and each output matches its gate.
from figlib import Timeline, text, splice, GOLD, MUTED

W, H = 400, 392
INK, OFF = '#ece6da', 'rgba(255,255,255,0.55)'
STEP = 1.4
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
T = Timeline(STEP * 4, shift=STEP * 2 + 0.6)          # t=0: A = 1, B = 0
def when(vals): return T.discrete('opacity', [(i * STEP, 1 if v else 0) for i, v in enumerate(vals)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-20 svgd-part1-20">')
a('<title id="svgt-part1-20">Fig 2.4 · Everything from NAND · NOT, AND and OR built from one gate</title>')
a('<desc id="svgd-part1-20">Three circuits built only of NAND gates, the AND shape with a bubble. One NAND with its inputs tied together '
  'is NOT. A NAND followed by that NOT is AND. Inverting both inputs and then taking their NAND is OR, by De Morgan\'s law. The '
  'inputs step together through every case, 00, 01, 10 and 11, and each output matches the ordinary gate.</desc>')

def wire(d, vals):
    a(f'<path d="{d}" fill="none" stroke="{OFF}" stroke-width="2" opacity="0">{when([not v for v in vals])}</path>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{when(vals)}</path>')
def value(cx, cy, vals, name=None, r=14):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{OFF}" stroke-width="1.5" opacity="0">{when([not v for v in vals])}</circle>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{when(vals)}</circle>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="{MUTED}" opacity="0">{when([not v for v in vals])}0</text>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="#fff" opacity="0">{when(vals)}1</text>')
    if name: a(text(cx - r - 8, cy + 5, name, anchor='end', size=14, fill=MUTED))
def nand(x, y):
    """a NAND at x (left edge), centre y; inputs at y-11 and y+11, output at x + 58"""
    a(f'<path d="M {x} {y - 22} h 22 a 22 22 0 0 1 0 44 h -22 Z" fill="none" stroke="#e8e8e8" stroke-width="2"/>')
    a(f'<circle cx="{x + 49}" cy="{y}" r="5" fill="none" stroke="#e8e8e8" stroke-width="2"/>')
    return x + 54
def tied(x, y, vals, x_from):
    """a wire from x_from into both inputs of a NAND at x"""
    wire(f'M {x_from} {y} H {x - 8} M {x - 8} {y - 11} V {y + 11} M {x - 8} {y - 11} H {x} M {x - 8} {y + 11} H {x}', vals)
    a(f'<circle cx="{x - 8}" cy="{y}" r="2.6" fill="{INK}"/>')

A_ = [c[0] for c in CASES]; B_ = [c[1] for c in CASES]
nA = [1 - v for v in A_]; nB = [1 - v for v in B_]
AND = [x & y for x, y in CASES]; NAND = [1 - v for v in AND]; OR = [x | y for x, y in CASES]
OUT_X = 300
def output(y, vals, words):
    value(OUT_X, y, vals, r=15)
    a(text(OUT_X + 22, y + 5, words, size=14, fill=INK, ls='0'))

# NOT: one NAND, inputs tied
Y = 46
a(text(20, Y - 24, 'NOT', size=15, fill=INK))
value(72, Y, A_, 'A')
tied(150, Y, A_, 86)
o_ = nand(150, Y); wire(f'M {o_} {Y} H {OUT_X - 15}', nA)
output(Y, nA, 'not A')

# AND: a NAND, then that NOT
Y = 150
a(text(20, Y - 40, 'AND', size=15, fill=INK))
value(72, Y - 18, A_, 'A'); value(72, Y + 18, B_, 'B')
wire(f'M 86 {Y - 18} H 100 V {Y - 11} H 120', A_); wire(f'M 86 {Y + 18} H 100 V {Y + 11} H 120', B_)
o1 = nand(120, Y)
tied(216, Y, NAND, o1)
o2 = nand(216, Y); wire(f'M {o2} {Y} H {OUT_X - 15}', AND)
output(Y, AND, 'A and B')

# OR: NAND of the two inverted inputs
Y = 272
a(text(20, Y - 58, 'OR', size=15, fill=INK))
value(72, Y - 30, A_, 'A'); value(72, Y + 30, B_, 'B')
tied(126, Y - 30, A_, 86); oa = nand(126, Y - 30)
tied(126, Y + 30, B_, 86); ob = nand(126, Y + 30)
wire(f'M {oa} {Y - 30} H {oa + 16} V {Y - 11} H 222', nA)
wire(f'M {ob} {Y + 30} H {ob + 16} V {Y + 11} H 222', nB)
o3 = nand(222, Y); wire(f'M {o3} {Y} H {OUT_X - 15}', OR)
output(Y, OR, 'A or B')

# every case, the current one framed
SY = 344
a(text(20, SY + 5, 'A B', size=14, fill=MUTED))
for i, (x_, y_) in enumerate(CASES):
    cx = 120 + i * 70
    a(text(cx, SY + 5, f'{x_} {y_}', anchor='middle', size=15, fill=INK, ls='0'))
    a(f'<rect x="{cx - 26}" y="{SY - 15}" width="52" height="28" rx="6" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">'
      f'{when([k == i for k in range(4)])}</rect>')
a(text(200, 382, 'every gate drawn here is a NAND', anchor='middle', size=14, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = 'NOT, AND and OR, each wired from NAND gates alone; the inputs step through every case.'
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
