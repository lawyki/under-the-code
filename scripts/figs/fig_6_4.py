# Fig 6.4 · Inheritance: same vptr slot, different function (Pass 28, law 3). Greenbar paper card.
# One call site, print(Shape* s); s moves from a Circle to a Square to a Triangle, and the same slot 0
# of each class's vtable leads to a different body. t=0 (shift): s at the Circle, its path lit.
import math
import figlib
from figlib import Timeline, text, splice, PLEX
figlib.FONT = PLEX

INK, INK_SOFT, GB, AMBER = '#1d2b22', 'rgba(29,43,34,0.62)', '#2e6f52', '#8a5a00'
BOX = '#f5f8f3'
SHAPES = [('Circle', 'r = 2', 'π·r·r', math.pi * 4), ('Square', 'side = 3', 'side²', 9.0), ('Triangle', 'b = 4, h = 3', '½·b·h', 6.0)]
W, H = 400, 256
CX = [20, 142, 264]; CW = 116
D = 9.0
T = Timeline(D, shift=2.0)
ST = [0.6 + 2.8 * k for k in range(3)]
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-40 svgd-part2-40">')
a('<title id="svgt-part2-40">Fig 6.4 · Inheritance: same vptr slot, different function</title>')
a('<desc id="svgd-part2-40">A function print(Shape* s) calls s-&gt;area(). The pointer s is given a Circle with r = 2, then a Square with side 3, then a Triangle with base 4 and height 3. '
  'Each object\'s vptr leads to its own class\'s vtable, where slot 0 holds that class\'s area: Circle::area computes π·r·r and prints 12.57, Square::area side² and prints 9, Triangle::area ½·b·h and prints 6. '
  'The caller never changes.</desc>')
a(f'<rect x="20" y="12" width="360" height="40" rx="3" fill="{BOX}" stroke="{INK}" stroke-opacity="0.5"/>')
a(text(32, 37, 'print(Shape* s): s-&gt;area()', size=13, fill=INK, ls='0'))
for k, (nm, field, body, val) in enumerate(SHAPES):
    t0 = ST[k]; t1 = ST[k + 1] if k < 2 else D - 0.3
    a(f'<g opacity="0">{win(t0 + 1.2, t1)}{text(368, 37, f"prints {val:g}" if val != math.pi * 4 else "prints 12.57", anchor="end", size=13, fill=GB, ls="0")}</g>')
for k, (nm, field, body, val) in enumerate(SHAPES):
    x = CX[k]; cx = x + CW / 2
    t0 = ST[k]; t1 = ST[k + 1] if k < 2 else D - 0.3
    rows = [(86, 40, [(nm, 14, INK), (field, 13, INK_SOFT)]), (146, 40, [('vtable slot 0', 13, INK_SOFT), (f'{nm}::area', 13, INK)]), (206, 40, [(body, 14, GB)])]
    for i, (y, h, lines) in enumerate(rows):
        a(f'<rect x="{x}" y="{y}" width="{CW}" height="{h}" rx="3" fill="{BOX}" stroke="rgba(29,43,34,0.35)"/>')
        a(f'<rect class="fx" x="{x}" y="{y}" width="{CW}" height="{h}" rx="3" fill="{GB}" fill-opacity="0.15" stroke="{GB}" stroke-width="2.2" opacity="0">{win(t0 + 0.4 * i, t1)}</rect>')
        if len(lines) == 1:
            a(text(cx, y + 25, lines[0][0], anchor='middle', size=lines[0][1], fill=lines[0][2], ls='0'))
        else:
            a(text(cx, y + 17, lines[0][0], anchor='middle', size=lines[0][1], fill=lines[0][2], ls='0'))
            a(text(cx, y + 33, lines[1][0], anchor='middle', size=lines[1][1], fill=lines[1][2], ls='0'))
        if i < 2:
            a(f'<line x1="{cx}" y1="{y + h}" x2="{cx}" y2="{y + h + 14}" stroke="rgba(29,43,34,0.5)" stroke-width="1.4"/>')
            a(f'<polygon points="{cx - 4},{y + h + 12} {cx + 4},{y + h + 12} {cx},{y + h + 19}" fill="rgba(29,43,34,0.5)"/>')
# s: the one pointer, moving between objects
xs = [x + CW / 2 for x in CX]
pts = [(0.0, xs[0])]
for k in (1, 2):
    pts += [(ST[k] - 0.3, xs[k - 1]), (ST[k], xs[k])]
pts += [(D - 0.4, xs[2]), (D - 0.1, xs[0]), (D, xs[0])]
a(f'<g>{T.translate([(t, v - xs[0]) for t, v in pts], "x")}'
  f'<line x1="{xs[0]}" y1="52" x2="{xs[0]}" y2="78" stroke="{AMBER}" stroke-width="2"/>'
  f'<polygon points="{xs[0] - 5},76 {xs[0] + 5},76 {xs[0]},85" fill="{AMBER}"/>'
  f'{text(xs[0] + 8, 72, "s", size=13, fill=AMBER, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One call site, three classes: when <code>s</code> points at a Circle, a Square or a Triangle, the same slot 0 of each class\'s vtable leads to that class\'s own <code>area()</code>. The caller never changes; that is <span class="key-term">polymorphism</span>, code written for the general kind, Shape, not for any one shape\'s formula.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Same layout.</b> Every class derived from <code>Shape</code> puts <code>area()</code> in the same slot of its vtable, so the call compiles to the same two instructions.</li>
          <li><b>New shapes for free.</b> A <code>Hexagon</code> added next year works with <code>print()</code> unchanged and without recompiling.</li>
          <li><b>The rule.</b> <code>= 0</code> makes <code>Shape::area</code> pure virtual: <code>Shape</code> itself cannot be created, only its subclasses.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-6-4">
      <div class="diagram-label">Fig 6.4 · Inheritance: same vptr slot, different function</div>
      {svg}
      <p id="ch6-classes-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-4', 'ch6-classes-p5', card)
