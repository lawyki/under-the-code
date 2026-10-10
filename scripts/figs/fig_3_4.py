# Fig 3.4 · The System V calling convention (Pass 28, law 3). work(a, b, c, d, e, f, g): the
# arguments leave the call in order and land in RDI, RSI, RDX, RCX, R8, R9; the seventh goes on the
# stack; the result comes back in RAX. t=0: every argument in place, the result returned.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, MUTED

W, H = 400, 352
CH = 9.0                                         # DM Mono advance at 15 units, approx
T = Timeline(9, shift=8.0)
REGS = ['RDI', 'RSI', 'RDX', 'RCX', 'R8', 'R9']
ARGS = 'abcdefg'
pieces = ['int r = work(', 'a', ', ', 'b', ', ', 'c', ', ', 'd', ', ', 'e', ', ', 'f', ', ', 'g', ');']
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-32 svgd-part1-32">')
a('<title id="svgt-part1-32">Fig 3.4 · System V calling convention · which register holds which argument</title>')
a('<desc id="svgd-part1-32">A call work(a, b, c, d, e, f, g) with seven arguments. Under the System V AMD64 convention the first six go into the registers RDI, RSI, RDX, RCX, R8 and R9 in that order; '
  'the seventh is passed on the stack. The function\'s result comes back in RAX and lands in r.</desc>')
a(text(20, 22, 'THE CALL', size=13, fill=MUTED))
x = 20; argx = {}
for p in pieces:
    if p in ARGS:
        argx[p] = x
        a(f'<text x="{x}" y="48" {MONO} font-size="15" fill="{GOLD if p != "g" else GREEN}">{p}</text>')
    else:
        a(f'<text x="{x}" y="48" {MONO} font-size="15" fill="rgba(255,255,255,0.85)">{p}</text>')
    x += len(p) * CH
slots = {}
for i, r in enumerate(REGS):
    row, col = divmod(i, 3)
    bx, by = 20 + col * 124, 94 + row * 64
    a(f'<rect x="{bx}" y="{by}" width="114" height="54" rx="6" fill="#151a24" stroke="{BLUE}" stroke-opacity="0.6"/>')
    a(text(bx + 12, by + 21, r, size=14, fill=BLUE, ls='0'))
    a(text(bx + 102, by + 21, str(i + 1), anchor='end', size=13, fill=MUTED, ls='0'))
    slots[ARGS[i]] = (bx + 57, by + 44)
a(text(20, 248, 'STACK · ARGUMENTS 7 ONWARD', size=13, fill=MUTED))
a('<rect x="20" y="258" width="360" height="34" rx="5" fill="#161616" stroke="rgba(255,255,255,0.3)"/>')
for k in range(1, 6):
    a(f'<line x1="{20 + k * 60}" y1="258" x2="{20 + k * 60}" y2="292" stroke="rgba(255,255,255,0.12)"/>')
slots['g'] = (50, 281)
# the arguments travel, one after another, along clear routes: into the gap under the call line,
# across, then down a gap between the boxes (row 2) or the right-hand margin (the stack)
GAP = {0: 139, 1: 263, 2: 263}
for i, arg in enumerate(ARGS):
    t0, t1 = 0.4 + i * 0.6, 0.4 + i * 0.6 + 0.55
    sx = argx[arg]
    dx, dy = slots[arg]
    dxt = dx - 4.5
    if i < 3:                                           # row 1: straight down its own column
        way = [(sx, 70), (sx, 76), (dxt, 76), (dxt, dy)]
    elif i < 6:                                         # row 2: down the gap, then in
        gx = GAP[i - 3] - 4.5
        way = [(sx, 70), (sx, 76), (gx, 76), (gx, dy), (dxt, dy)]
    else:                                               # the stack: round the right-hand margin
        way = [(sx, 70), (sx, 76), (386, 76), (386, dy), (dxt, dy)]
    n = len(way) - 1
    ts = [t0 + (t1 - t0) * k / n for k in range(n + 1)]
    xs = [(0.0, way[0][0])] + [(t, p[0]) for t, p in zip(ts, way)] + [(9.0, way[-1][0])]
    ys = [(0.0, way[0][1])] + [(t, p[1]) for t, p in zip(ts, way)] + [(9.0, way[-1][1])]
    col = GOLD if arg != 'g' else GREEN
    a(f'<text {MONO} font-size="18" fill="{col}" opacity="0">{arg}'
      f'{T.anim("x", xs)}{T.anim("y", ys)}'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (8.6, 1.0), (8.601, 0.0), (9.0, 0.0)])}</text>')
# the result comes back in RAX
a(f'<rect x="20" y="306" width="180" height="40" rx="6" fill="{GOLD}" fill-opacity="0.12" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(text(34, 331, 'RAX', size=15, fill=GOLD, ls='0'))
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (5.6, 0.0), (5.601, 1.0), (8.6, 1.0), (8.601, 0.0), (9.0, 0.0)])}'
  f'<text x="84" y="331" {MONO} font-size="15" fill="#fff">result</text>'
  f'<path d="M 206 326 H 262" stroke="{GOLD}" stroke-width="2"/><polygon points="262,320 272,326 262,332" fill="{GOLD}"/>'
  f'<text x="282" y="331" {MONO} font-size="15" fill="#fff">r</text></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Under the System V convention (Linux, macOS, BSD) the first six integer or pointer arguments travel in RDI, RSI, RDX, RCX, R8 and R9, the seventh and beyond on the stack, and the result comes back in RAX. '
           'That agreement lets code from any compiler call any other.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Registers first.</b> Registers are the fastest place to put a value, so the common case, six arguments or fewer, never touches memory.</li>
          <li><b>Other kinds.</b> Floating-point arguments use XMM0 to XMM7; structures larger than 16 bytes are passed by a hidden pointer.</li>
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
