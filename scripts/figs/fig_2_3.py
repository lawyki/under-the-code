# Fig 2.3 · The three gates (Pass 31, Part I, from an empty script). Job: function. Takeaway: as inputs step through
# every case, each gate's output follows its table: AND both, OR either, NOT the opposite.
# Concept: the three standard symbols at work, one row each, the inputs on the left stepping through every case
# together and each output following its rule, a wire carrying 1 lit gold. The truth tables are the prose's (they
# sit above the card), so the card keeps only a strip of the four cases with the current one framed. t=0: A = 1, B = 0.
from figlib import Timeline, text, splice, GOLD, MUTED

W, H = 400, 352
INK, OFF = '#ece6da', 'rgba(255,255,255,0.35)'
STEP = 1.4
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
T = Timeline(STEP * 4, shift=STEP * 2 + 0.6)          # t=0: A = 1, B = 0
def when(vals):
    pts = [(i * STEP, 1 if v else 0) for i, v in enumerate(vals)]
    return T.discrete('opacity', pts)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-19 svgd-part1-19">')
a('<title id="svgt-part1-19">Fig 2.3 · The three fundamental gates · AND, OR, NOT</title>')
a('<desc id="svgd-part1-19">AND outputs 1 only when both inputs are 1. OR outputs 1 when at least one input is 1. NOT outputs the opposite '
  'of its one input. Each gate is drawn with its standard symbol, inputs A and B on the left, its output on the right named in words '
  '(A and B, A or B, not A). The inputs step together through every case, 00, 01, 10 and 11, and each output follows its rule; a wire '
  'carrying 1 is lit.</desc>')

def wire(d, vals):
    a(f'<path d="{d}" fill="none" stroke="{OFF}" stroke-width="2" opacity="0">{when([not v for v in vals])}</path>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{when(vals)}</path>')
def value(cx, cy, vals, name=None, r=14):
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5" opacity="0">{when([not v for v in vals])}</circle>')
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{when(vals)}</circle>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="{MUTED}" opacity="0">{when([not v for v in vals])}0</text>')
    a(f'<text data-role="object" x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="DM Mono" font-size="15" fill="#fff" opacity="0">{when(vals)}1</text>')
    if name: a(text(cx - r - 8, cy + 5, name, anchor='end', size=14, fill=MUTED))

A_ = [c[0] for c in CASES]; B_ = [c[1] for c in CASES]
for name, out, f, Y in (('AND', 'A and B', lambda x, y: x & y, 20), ('OR', 'A or B', lambda x, y: x | y, 122)):
    Q = [f(*c) for c in CASES]
    a(text(20, Y + 45, name, size=16, fill=INK))
    value(110, Y + 18, A_, 'A'); value(110, Y + 62, B_, 'B')
    wire(f'M 124 {Y + 18} H 166', A_); wire(f'M 124 {Y + 62} H 166', B_)
    if name == 'AND':
        a(f'<path d="M 160 {Y} h 34 a 40 40 0 0 1 0 80 h -34 Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>'); tip = 234
    else:
        a(f'<path d="M 154 {Y} Q 176 {Y + 40} 154 {Y + 80} Q 210 {Y + 80} 238 {Y + 40} Q 210 {Y} 154 {Y} Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>'); tip = 238
    wire(f'M {tip} {Y + 40} H 290', Q)
    value(306, Y + 40, Q, r=16)
    a(text(330, Y + 45, out, size=14, fill=INK, ls='0'))
# NOT, on A alone
Y = 222
Q = [1 - v for v in A_]
a(text(20, Y + 45, 'NOT', size=16, fill=INK))
value(110, Y + 40, A_, 'A')
wire(f'M 124 {Y + 40} H 166', A_)
a(f'<path d="M 166 {Y + 12} L 166 {Y + 68} L 216 {Y + 40} Z" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
a(f'<circle cx="223" cy="{Y + 40}" r="6" fill="#1a1a1a" stroke="#e8e8e8" stroke-width="2"/>')
wire(f'M 229 {Y + 40} H 290', Q)
value(306, Y + 40, Q, r=16)
a(text(330, Y + 45, 'not A', size=14, fill=INK, ls='0'))

# every case, the current one framed
SY = 322
a(text(20, SY + 5, 'A B', size=14, fill=MUTED))
for i, (x_, y_) in enumerate(CASES):
    cx = 120 + i * 70
    a(text(cx, SY + 5, f'{x_} {y_}', anchor='middle', size=15, fill=INK, ls='0'))
    a(f'<rect x="{cx - 26}" y="{SY - 15}" width="52" height="28" rx="6" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">'
      f'{when([k == i for k in range(4)])}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('AND, OR and NOT, the three gates any circuit can be built from, in their standard symbols (unchanged since the 1960s), '
           'as the inputs step through every case.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reading a gate.</b> Inputs A and B enter on the left, the output leaves on the right named in words (A and B, A or B, not A); a wire carrying 1 is gold. The strip at the bottom marks the case being shown, the same rows as the tables above.</li>
          <li><b>The shapes.</b> AND has a flat back, OR a curved one, NOT is a triangle with a bubble, and the bubble alone means "invert".</li>
          <li><b>In silicon.</b> Each gate is a few transistors (Fig 1.5), switching in well under a nanosecond.</li>
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
