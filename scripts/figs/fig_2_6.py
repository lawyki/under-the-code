# Fig 2.6 · Inside a full adder (Pass 31, Part I, from an empty script). Job: function. Takeaway: when the first half
# adder carries, its sum is 0, so the second cannot; one OR merges the carries.
# Concept: the full adder wired from gates in Fig 2.3's grammar (wires lit gold while they carry 1), the two half
# adders framed, the inputs stepping through all eight cases with the case strip below and the sum written out as the
# adder computes it. t=0 is 1 + 1 + 1, where the first half adder carries and the second cannot.
from figlib import Timeline, text, splice, GOLD, MUTED

W, H = 400, 352
INK, OFF = '#ece6da', 'rgba(255,255,255,0.55)'
STEP = 1.1
CASES = [(a_, b_, c_) for a_ in (0, 1) for b_ in (0, 1) for c_ in (0, 1)]
T = Timeline(STEP * 8, shift=STEP * 7 + 0.5)            # t=0: 1 + 1 + 1
def when(vals): return T.discrete('opacity', [(i * STEP, 1 if v else 0) for i, v in enumerate(vals)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-22 svgd-part1-22"{T.steps([(0.55, '000'), (1.6500000000000001, '001'), (2.75, '010'), (3.8500000000000005, '011'), (4.95, '100'), (6.05, '101'), (7.15, '110'), (8.250000000000002, '111')])}>')
a('<title id="svgt-part1-22">Fig 2.6 · Inside a full adder · two half adders and an OR</title>')
a('<desc id="svgd-part1-22">A full adder built from gates. A and B meet in an XOR and an AND: the first half adder. The XOR\'s output meets '
  'the carry-in in a second XOR and AND: the second half adder; its XOR gives the sum bit. Either AND\'s carry, through an OR, gives the '
  'carry-out; the two never carry at once, because when the first carries its sum is 0. The inputs step through all eight cases and '
  'the result is written out, from 0 + 0 + 0 = 00 to 1 + 1 + 1 = 11.</desc>')

def wire(d, vals):
    a(f'<path d="{d}" fill="none" stroke="{OFF}" stroke-width="2" opacity="0">{when([not v for v in vals])}</path>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{when(vals)}</path>')
def value(cx, cy, vals, r=14):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{OFF}" stroke-width="1.5" opacity="0">{when([not v for v in vals])}</circle>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{when(vals)}</circle>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="{MUTED}" opacity="0">{when([not v for v in vals])}0</text>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="#fff" opacity="0">{when(vals)}1</text>')
def dot(x, y): a(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{INK}"/>')
G = 'fill="none" stroke="#e8e8e8" stroke-width="2"'
def and_g(x, y): a(f'<path d="M {x} {y - 20} h 26 a 20 20 0 0 1 0 40 h -26 Z" {G}/>'); return x + 46
def or_g(x, y): a(f'<path d="M {x} {y - 20} Q {x + 14} {y} {x} {y + 20} Q {x + 34} {y + 20} {x + 50} {y} Q {x + 34} {y - 20} {x} {y - 20} Z" {G}/>'); return x + 50
def xor_g(x, y):
    a(f'<path d="M {x - 7} {y - 20} Q {x + 7} {y} {x - 7} {y + 20}" {G}/>')
    return or_g(x, y)

A_ = [c[0] for c in CASES]; B_ = [c[1] for c in CASES]; C_ = [c[2] for c in CASES]
X1 = [x ^ y for x, y, _ in CASES]; A1 = [x & y for x, y, _ in CASES]
S = [p ^ c for p, c in zip(X1, C_)]; A2 = [p & c for p, c in zip(X1, C_)]; CO = [p | q for p, q in zip(A1, A2)]

# the half adders, framed
a(f'<rect x="100" y="44" width="92" height="140" rx="8" fill="none" stroke="rgba(255,255,255,0.5)" stroke-dasharray="4 4"/>')
a(f'<rect x="204" y="34" width="92" height="124" rx="8" fill="none" stroke="rgba(255,255,255,0.5)" stroke-dasharray="4 4"/>')
a(text(146, 38, 'half adder', anchor='middle', size=14, fill=MUTED))
a(text(302, 128, 'half', size=14, fill=MUTED))
a(text(302, 144, 'adder', size=14, fill=MUTED))

# inputs
value(44, 64, A_); a(text(44, 42, 'A', anchor='middle', size=14, fill=INK))
value(44, 116, B_); a(text(44, 146, 'B', anchor='middle', size=14, fill=INK))
value(212, 20, C_, r=12); a(text(230, 25, 'carry in', size=14, fill=INK))
# first half adder: XOR1 and AND1 on A and B
o_x1 = xor_g(122, 74); o_a1 = and_g(118, 150)
wire('M 58 64 H 126', A_); wire('M 84 64 V 140 H 118', A_); dot(84, 64)
wire('M 58 116 H 100 V 84 H 126', B_); wire('M 100 116 V 160 H 118', B_); dot(100, 116)
# second half adder: XOR2 and AND2 on XOR1's sum and the carry-in
o_x2 = xor_g(230, 64); o_a2 = and_g(226, 122)
wire(f'M 212 32 V 112 H 226', C_); wire('M 212 54 H 234', C_); dot(212, 54)
wire(f'M {o_x1} 74 H 234', X1); wire('M 196 74 V 132 H 226', X1); dot(196, 74)
# outputs
wire(f'M {o_x2} 64 H 322', S); value(336, 64, S); a(text(356, 69, 'sum', size=14, fill=INK))
o_or = or_g(290, 214)
wire(f'M {o_a2} 122 H 280 V 204 H 296', A2)
wire(f'M {o_a1} 150 H 176 V 224 H 296', A1)
wire(f'M {o_or} 214 H 346', CO); value(360, 214, CO)
a(text(378, 248, 'carry out', anchor='end', size=14, fill=INK))

# the sum written out
for i, (x_, y_, c_) in enumerate(CASES):
    s = x_ + y_ + c_
    a(f'<text data-role="object" x="40" y="278" font-family="DM Mono" font-size="16" fill="{INK}" opacity="0">'
      f'{when([k == i for k in range(8)])}{x_} + {y_} + {c_} = {s >> 1}{s & 1}</text>')
a(text(40, 298, 'A + B + carry in = carry out, sum', size=14, fill=MUTED, ls='0'))
# every case
SY = 330
for i, (x_, y_, c_) in enumerate(CASES):
    cx = 42 + i * 45
    a(text(cx, SY + 5, f'{x_}{y_}{c_}', anchor='middle', size=14, fill=INK, ls='0'))
    a(f'<rect x="{cx - 20}" y="{SY - 14}" width="40" height="26" rx="6" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">'
      f'{when([k == i for k in range(8)])}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One full adder of Fig 2.5, opened: two half adders, each an XOR and an AND, joined by an OR, as the inputs step through '
           'all eight cases.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Half adder.</b> XOR gives the sum of two bits, AND their carry: 1 + 1 is 0, carry 1.</li>
          <li><b>Adding the carry.</b> The second half adder adds the incoming carry to the first sum.</li>
          <li><b>One carry out.</b> When the first half adder carries, its sum is 0, so the second cannot carry too: an OR is enough. Chain four of these and you have Fig 2.5.</li>
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
