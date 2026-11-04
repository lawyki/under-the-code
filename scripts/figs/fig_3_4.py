# Fig 3.4 · System V calling convention (Pass 31, Part I, from an empty script). Job: function. Takeaway: a shared
# convention fixes where arguments and the result go, so compilers following it can call each other's code.
# Concept: one call's seven arguments flowing, one by one in order (Part I's flow verb), into the six argument registers
# and, for the seventh, the stack; then the result flowing back from RAX into r. The registers are numbered in the
# convention's order. t=0 is the call complete.
from figlib import Timeline, text, splice, GOLD, BLUE, GREEN, MUTED

W, H = 400, 340
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 11.0
T = Timeline(D, shift=9.6)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
ARGS = list('abcdefg')
REGS = ['RDI', 'RSI', 'RDX', 'RCX', 'R8', 'R9']
AX = lambda k: 52 + k * 50                     # argument chips
BOX = lambda k: (20 + (k % 3) * 124, 104 + (k // 3) * 56)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-32 svgd-part1-32"{T.steps([(3.4, 'a to c'), (6.2, 'd to f'), (7.2, 'g'), (9.0, 'result')])}>')
a('<title id="svgt-part1-32">Fig 3.4 · System V calling convention · which register holds which argument</title>')
a('<desc id="svgd-part1-32">A call work(a, b, c, d, e, f, g) with seven arguments. Under the System V AMD64 convention the first six go, in '
  'order, into the registers RDI, RSI, RDX, RCX, R8 and R9; the seventh is passed on the stack. The function\'s result comes back '
  'in RAX and lands in r.</desc>')

a(text(20, 28, 'int r = work(a, b, c, d, e, f, g);', size=15, fill=INK, ls='0'))
for k, c in enumerate(ARGS):
    a(f'<circle cx="{AX(k)}" cy="56" r="13" fill="none" stroke="{GREEN}" stroke-width="1.5"/>')
    a(text(AX(k), 61, c, anchor='middle', size=15, fill=GREEN, ls='0', role='object'))
for k, r in enumerate(REGS):
    x, y = BOX(k)
    a(f'<rect x="{x}" y="{y}" width="112" height="44" rx="6" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
    a(text(x + 10, y + 18, r, size=14, fill=BLUE, ls='0'))
    a(text(x + 102, y + 18, str(k + 1), anchor='end', size=14, fill=MUTED, ls='0'))
# the stack, for the seventh
a(text(20, 240, 'stack: the seventh and on', size=14, fill=MUTED))
a(f'<rect x="20" y="248" width="112" height="34" rx="5" fill="none" stroke="{EDGE}" stroke-width="1.5"/>')
a(f'<rect x="136" y="248" width="244" height="34" rx="5" fill="none" stroke="rgba(255,255,255,0.5)" stroke-dasharray="4 4"/>')
# each argument travels to its place, in order
for k, c in enumerate(ARGS):
    t0 = 0.6 + k * 0.9
    if k < 6:
        x, y = BOX(k); tx, ty = x + 56, y + 36
    else:
        tx, ty = 76, 270
    a(f'<g opacity="0">{vis([(t0, D - 0.3)])}<g>{T.translate([(0.0, 0), (t0, 0), (t0 + 0.7, tx - AX(k)), (D - 0.01, tx - AX(k))], axis="x")}'
      f'<g>{T.translate([(0.0, 0), (t0, 0), (t0 + 0.7, ty - 61), (D - 0.01, ty - 61)], axis="y")}'
      + text(AX(k), 61, c, anchor='middle', size=17, fill=GREEN, ls='0', role='object') + '</g></g></g>')
# the result comes back in RAX
a(f'<rect x="20" y="294" width="112" height="34" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
a(text(30, 316, 'RAX', size=14, fill=GOLD, ls='0'))
a(f'<g opacity="0">{vis([(7.4, D - 0.3)])}' + text(98, 316, 'result', anchor='middle', size=14, fill=INK, ls='0', role='object') + '</g>')
a(f'<g opacity="0">{vis([(8.0, D - 0.3)])}<path d="M 140 311 H 196 m -7 -5 l 7 5 l -7 5" fill="none" stroke="{GOLD}" stroke-width="2"/>'
  + text(206, 316, 'r', size=16, fill=GOLD, ls='0') + '</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Under the System V convention (Linux, macOS, BSD) the first six integer or pointer arguments travel in RDI, RSI, RDX, RCX, '
           'R8 and R9, the seventh and beyond on the stack, and the result comes back in RAX. That agreement lets code from any compiler '
           'call any other.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Registers first.</b> Registers are the fastest place to put a value, so the common case, six arguments or fewer, never touches memory.</li>
          <li><b>Other kinds.</b> Floating-point arguments use XMM0 to XMM7; structures larger than 16 bytes are copied onto the stack.</li>
          <li><b>Who saves what.</b> The caller saves any volatile registers it still needs; the callee must preserve RBX, RBP and R12 to R15.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-4">
      <div class="diagram-label">Fig 3.4 · System V calling convention · which register holds which argument</div>
      {svg}
      <p id="ch3-registers-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-4', 'ch3-registers-p5', card)
