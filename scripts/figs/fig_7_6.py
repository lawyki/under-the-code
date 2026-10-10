# Fig 7.6 · CPython's pipeline, in detail (Pass 28, law 3). The front end in one strip, then the stack
# machine itself: a + b * c with a=2, b=3, c=4, stepping through its bytecode while the value stack
# grows and shrinks to 14. Opcode names as CPython 3.11+ prints them (dis). t=0 (shift): three loads done.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

CODE = ['LOAD_NAME a', 'LOAD_NAME b', 'LOAD_NAME c', 'BINARY_OP *', 'BINARY_OP +']
STACKS = [['2'], ['2', '3'], ['2', '3', '4'], ['2', '12'], ['14']]
assert 2 + 3 * 4 == 14
W, H = 400, 262
D = 9.0
ST = [0.8 + 1.3 * k for k in range(5)]
END = ST[-1] + 1.6
T = Timeline(D, shift=ST[2] + 0.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-52 svgd-part2-52">')
a('<title id="svgt-part2-52">Fig 7.6 · CPython\'s pipeline, in detail</title>')
a('<desc id="svgd-part2-52">The line a + b * c, with a = 2, b = 3 and c = 4, goes through CPython\'s front end: tokens, a syntax tree, bytecode, then the eval loop. '
  'The bytecode is LOAD_NAME a, LOAD_NAME b, LOAD_NAME c, BINARY_OP *, BINARY_OP +. Running it, the loads push 2, 3 and 4 onto the value stack; '
  'BINARY_OP * pops 3 and 4 and pushes 12; BINARY_OP + pops 2 and 12 and pushes 14.</desc>')
a(text(20, 22, 'a + b * c', size=14, fill='#fff', ls='0'))
a(text(380, 22, 'a=2, b=3, c=4', anchor='end', size=13, fill=MUTED, ls='0'))
for k, lab in enumerate(['tokens', 'AST', 'bytecode', 'eval loop']):
    x = 20 + k * 92
    a(f'<rect x="{x}" y="34" width="84" height="28" rx="3" fill="{PANEL}" stroke="{PHOS if k == 3 else "rgba(132,255,178,0.35)"}"/>')
    a(text(x + 42, 53, lab, anchor='middle', size=13, fill='#fff' if k == 3 else PHOS_SOFT, ls='0'))
    if k < 3:
        a(f'<polygon points="{x + 86},44 {x + 90},48 {x + 86},52" fill="rgba(132,255,178,0.5)"/>')
# bytecode
a(text(20, 92, 'bytecode', size=13, fill=MUTED, ls='0'))
for i, ins in enumerate(CODE):
    y = 100 + i * 28
    a(f'<rect x="20" y="{y}" width="200" height="24" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.15)"/>')
    a(f'<rect class="fx" x="20" y="{y}" width="200" height="24" rx="2" fill="{BLUE}" fill-opacity="0.25" stroke="{BLUE}" stroke-width="2" opacity="0">{win(ST[i], ST[i + 1] if i < 4 else END)}</rect>')
    a(text(30, y + 17, ins, size=13, fill='#fff', ls='0'))
# value stack, bottom up
a(text(252, 92, 'value stack', size=13, fill=MUTED, ls='0'))
BASE = 232
a(f'<line x1="252" y1="{BASE + 2}" x2="380" y2="{BASE + 2}" stroke="rgba(198,222,206,0.5)" stroke-width="1.5"/>')
for i, st in enumerate(STACKS):
    t0, t1 = ST[i] + 0.3, (ST[i + 1] + 0.3 if i < 4 else END)
    g = []
    for j, v in enumerate(st):
        y = BASE - (j + 1) * 30
        top = j == len(st) - 1
        g.append(f'<rect x="262" y="{y}" width="108" height="26" rx="3" fill="{GOLD if top else PANEL}" fill-opacity="{0.3 if top else 1}" stroke="{GOLD if top else "rgba(198,222,206,0.4)"}"/>'
                 + text(316, y + 18, v, anchor='middle', size=14, fill='#fff', ls='0'))
    a(f'<g opacity="0">{win(t0, t1)}{"".join(g)}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('CPython turns <code>a + b * c</code> into bytecode for a stack machine: three loads push 2, 3 and 4; <code>BINARY_OP&nbsp;*</code> pops 3 and 4 and pushes 12; <code>BINARY_OP&nbsp;+</code> pops 2 and 12 and pushes 14. '
           'The eval loop does exactly this, one instruction at a time, for every line of Python.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>See it yourself.</b> <code>import dis; dis.dis("a + b * c")</code> prints this bytecode.</li>
          <li><b>Since 3.11.</b> One <code>BINARY_OP</code> with an argument replaced <code>BINARY_ADD</code>, <code>BINARY_MULTIPLY</code> and the rest, and the interpreter specialises hot instructions once it has seen their types, such as <code>BINARY_OP_ADD_INT</code>.</li>
          <li><b>The loop.</b> <code>ceval.c</code> jumps from each instruction to its C handler, using computed gotos where the compiler supports them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-6">
      <div class="diagram-label">Fig 7.6 · CPython's pipeline, in detail</div>
      {svg}
      <p id="ch7-cpython-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-6', 'ch7-cpython-p3', card)
