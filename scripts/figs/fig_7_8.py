# Fig 7.8 · How NumPy actually does work (Pass 28, law 3). One np.dot call descends four layers, the
# work fills at the bottom, and an array comes back up. The time column shows where the time goes.
# t=0 (shift): the work under way at the bottom, every layer drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

LAYERS = [('Python', 'C = np.dot(A, B)', 'µs', BLUE),
          ('NumPy, in C', 'check types and shapes, pick a routine', 'µs', BLUE),
          ('BLAS: dgemm', 'blocked for the cache, vector instructions', 'ms', GOLD),
          ('CPU vector units', 'several doubles per instruction', '', GOLD)]
W, H = 400, 290
LH, GAP, Y0 = 52, 14, 12
D = 9.0
DOWN = [0.6 + 0.5 * k for k in range(4)]
WORK0, WORK1 = DOWN[-1] + 0.2, DOWN[-1] + 3.4
UP = [WORK1 + 0.2 + 0.4 * k for k in range(3)]
T = Timeline(D, shift=(WORK0 + WORK1) / 2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-54 svgd-part2-54">')
a('<title id="svgt-part2-54">Fig 7.8 · How NumPy actually does work</title>')
a('<desc id="svgd-part2-54">One line of Python, C = np.dot(A, B), descends four layers. NumPy\'s C code checks the types and shapes and picks a routine. A BLAS routine, dgemm, does the multiplication, blocked to fit the cache and using vector instructions, '
  'which the CPU\'s vector units execute several doubles at a time (four or eight on typical x86 chips). The Python and NumPy layers take microseconds; for a 1000 by 1000 matrix the BLAS work takes milliseconds. The result comes back up as one NumPy array.</desc>')
for k, (name, what, tm, col) in enumerate(LAYERS):
    y = Y0 + k * (LH + GAP)
    a(f'<rect x="20" y="{y}" width="360" height="{LH}" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.6"/>')
    if k == 3:  # the work, filling
        a(f'<rect class="fx" x="20" y="{y}" width="360" height="{LH}" rx="3" fill="{GOLD}" fill-opacity="0.22">'
          f'{T.anim("width", [(0.0, 0.0), (WORK0, 0.0), (WORK1, 360.0), (UP[-1] + 0.4, 360.0), (UP[-1] + 0.6, 0.0), (D, 0.0)])}</rect>')
    a(text(32, y + 21, name, size=14, fill=col, ls='0'))
    a(text(32, y + 41, what, size=13, fill=PHOS_SOFT, ls='0'))
    if tm: a(text(368, y + 21, tm, anchor='end', size=13, fill=MUTED, ls='0'))
    a(f'<rect class="fx" x="20" y="{y}" width="360" height="{LH}" rx="3" fill="none" stroke="#fff" stroke-width="2" opacity="0">{win(DOWN[k], DOWN[k] + 0.6)}</rect>')
    if k < 3:
        a(f'<rect class="fx" x="20" y="{y}" width="360" height="{LH}" rx="3" fill="none" stroke="{PHOS}" stroke-width="2" opacity="0">{win(UP[2 - k], UP[2 - k] + 0.5)}</rect>')
        ay = y + LH
        a(f'<line x1="60" y1="{ay}" x2="60" y2="{ay + GAP}" stroke="rgba(198,222,206,0.4)"/><polygon points="56,{ay + GAP - 5} 64,{ay + GAP - 5} 60,{ay + GAP}" fill="rgba(198,222,206,0.4)"/>')
        a(f'<line x1="340" y1="{ay + GAP}" x2="340" y2="{ay}" stroke="rgba(132,255,178,0.4)"/><polygon points="336,{ay + 5} 344,{ay + 5} 340,{ay}" fill="rgba(132,255,178,0.4)"/>')
a(f'<g opacity="0">{win(UP[-1], D - 0.3)}{text(20, H - 8, "back in Python: one array", size=13, fill=PHOS, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One line of Python descends through NumPy\'s C code into a BLAS routine that the CPU\'s vector units execute, and comes back as a single array. '
           'The Python layers cost microseconds; for a 1000 × 1000 multiplication the BLAS work takes milliseconds, so the interpreter all but disappears from the bill.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>BLAS.</b> The Basic Linear Algebra Subprograms began in 1979, and matrix routines such as dgemm joined in 1990. NumPy's Linux and Windows builds ship OpenBLAS; on Apple Silicon Macs it can use Apple's Accelerate.</li>
          <li><b>Blocking.</b> dgemm multiplies the matrices in tiles small enough to stay in cache, so each number fetched from memory is used many times.</li>
          <li><b>Vectors.</b> On x86, AVX2 works on 4 doubles at once and AVX-512 on 8; Arm's NEON on 2. The work is also split across every core.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-8">
      <div class="diagram-label">Fig 7.8 · How NumPy actually does work</div>
      {svg}
      <p id="ch7-datasci-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-8', 'ch7-datasci-p2', card)
