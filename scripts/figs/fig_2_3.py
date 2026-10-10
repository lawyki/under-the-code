# Fig 2.3 · The three gates (Pass 28, law 3). AND, OR, NOT, live: inputs step through every
# case, wires carrying a 1 turn gold, and each gate's truth table beside it marks the current row,
# so the still holds the whole behaviour.
from figlib import Timeline, text, splice, MONO, GOLD, MUTED

W, H = 400, 324
STEP = 1.2
CASES2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
T = Timeline(STEP * 4, shift=STEP * 2 + 0.6)     # t=0: A=1, B=0
def when(vals):               # vals: the 4 per-step booleans -> snapping opacity
    pts = []
    for i, v in enumerate(vals):
        if i: pts.append((i * STEP - 0.001, 1.0 if vals[i - 1] else 0.0))
        pts.append((i * STEP, 1.0 if v else 0.0))
    pts.append((STEP * 4 - 0.001, 1.0 if vals[-1] else 0.0))
    return T.anim('opacity', pts)
OFF = 'rgba(255,255,255,0.35)'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-19 svgd-part1-19">')
a('<title id="svgt-part1-19">Fig 2.3 · The three fundamental gates · AND, OR, NOT</title>')
a('<desc id="svgd-part1-19">AND outputs 1 only when both inputs are 1. OR outputs 1 when at least one input is 1. NOT outputs the opposite of its one input. '
  'Each gate is drawn with its standard symbol and its truth table; the inputs step through every case.</desc>')

def wire(d, vals):
    a(f'<path d="{d}" fill="none" stroke="{OFF}" stroke-width="2"/>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{when(vals)}</path>')
def value(cx, cy, vals, r=14):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#141414" stroke="{OFF}" stroke-width="1.5"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}" fill-opacity="0.3" stroke="{GOLD}" stroke-width="1.8" opacity="0">{when(vals)}</circle>')
    a(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" {MONO} font-size="15" fill="rgba(255,255,255,0.7)">0{when([not v for v in vals])}</text>')
    a(f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" {MONO} font-size="15" fill="#fff" opacity="0">1{when(vals)}</text>')
def table(x, y0, rows, cur):
    for i, (ins, out) in enumerate(rows):
        yy = y0 + i * 16
        a(f'<text x="{x}" y="{yy}" {MONO} font-size="13" fill="{GOLD if out else "rgba(255,255,255,0.6)"}">{ins} {out}</text>')
    for i in range(len(rows)):
        vals = [cur(k) == i for k in range(4)]
        a(f'<rect x="{x - 5}" y="{y0 + i * 16 - 12}" width="{(len(rows[0][0]) + 2) * 8 + 10}" height="16" rx="3" fill="none" stroke="#fff" stroke-width="1.2" opacity="0">{when(vals)}</rect>')

rows = [('AND', 'A · B', lambda A, B: A & B, 18), ('OR', 'A + B', lambda A, B: A | B, 122)]
for name, formula, f, Y in rows:
    a(text(20, Y + 30, name, size=16, fill='#fff'))
    a(text(20, Y + 50, formula, size=14, fill=MUTED, ls='0'))
    A_ = [c[0] for c in CASES2]; B_ = [c[1] for c in CASES2]; Q = [f(*c) for c in CASES2]
    value(96, Y + 18, A_); value(96, Y + 62, B_)
    wire(f'M 110 {Y + 18} H 156', A_); wire(f'M 110 {Y + 62} H 156', B_)
    if name == 'AND':
        a(f'<path d="M 150 {Y} h 34 a 40 40 0 0 1 0 80 h -34 Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
        tip = 224
    else:
        a(f'<path d="M 144 {Y} Q 166 {Y + 40} 144 {Y + 80} Q 200 {Y + 80} 228 {Y + 40} Q 200 {Y} 144 {Y} Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
        tip = 228
    wire(f'M {tip} {Y + 40} H 268', Q)
    value(284, Y + 40, Q, r=16)
    table(334, Y + 18, [(f'{a_}{b_}', f(a_, b_)) for a_, b_ in CASES2], lambda k: k)
# NOT
Y = 226
a(text(20, Y + 30, 'NOT', size=16, fill='#fff'))
a(text(20, Y + 50, '¬A', size=14, fill=MUTED, ls='0'))
A_ = [0, 1, 0, 1]; Q = [1, 0, 1, 0]
value(96, Y + 40, A_)
wire(f'M 110 {Y + 40} H 156', A_)
a(f'<path d="M 156 {Y + 12} L 156 {Y + 68} L 206 {Y + 40} Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
a(f'<circle cx="213" cy="{Y + 40}" r="6" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
wire(f'M 219 {Y + 40} H 268', Q)
value(284, Y + 40, Q, r=16)
table(334, Y + 34, [('0', 1), ('1', 0)], lambda k: k % 2)
a('</svg>')
svg = '\n'.join(o)

caption = ('The three gates every circuit is built from: AND gives 1 only when both inputs are 1, OR when at least one is, and NOT turns its input over. '
           'The shapes are the standard symbols, unchanged since the 1960s.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reading a gate.</b> Inputs enter on the left, the output leaves on the right; the table beside it lists every case.</li>
          <li><b>The shapes.</b> AND has a flat back, OR a curved one, NOT is a triangle with a bubble, and the bubble alone means "invert".</li>
          <li><b>In silicon.</b> Each gate is a few transistors (Fig 1.4), switching in well under a nanosecond.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-3">
      <div class="diagram-label">Fig 2.3 · The three fundamental gates · AND, OR, NOT</div>
      {svg}
      <p id="ch2-gates-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-3', 'ch2-gates-p3', card)
