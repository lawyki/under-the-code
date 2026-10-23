# Fig 7.9 · The same matmul, two ways (Pass 28, law 3). A race on a logarithmic time axis, 1 ms to
# 1000 s: a cursor moves at constant speed through the decades; np.dot finishes near 12 ms, pure Python
# near 2 minutes. t=0 (shift): both finished.
import math
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 196
X0, X1 = 92, 380
LO, HI = -3, 3                       # log10 seconds
xs = lambda sec: X0 + (math.log10(sec) - LO) / (HI - LO) * (X1 - X0)
C0, C1 = 0.6, 7.6
ts = lambda sec: C0 + (math.log10(sec) - LO) / (HI - LO) * (C1 - C0)
NP_S, PY_S = 0.012, 120.0
assert 9000 < PY_S / NP_S < 11000
D = 10.0
T = Timeline(D, shift=9.0)
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-55 svgd-part2-55">')
a('<title id="svgt-part2-55">Fig 7.9 · The same matmul, two ways</title>')
a('<desc id="svgd-part2-55">Multiplying two 1000 by 1000 matrices, timed on a logarithmic axis from one millisecond to a thousand seconds. np.dot finishes in about 0.012 seconds. '
  'Pure Python, with three nested loops, finishes in about two minutes, roughly ten thousand times later.</desc>')
a(text(20, 22, '1000 × 1000 matrix multiply, time to finish', size=13, fill=MUTED, ls='0'))
for i, (name, sec, col, lab) in enumerate((('np.dot', NP_S, PHOS, '≈ 0.012 s'), ('pure Python', PY_S, GOLD, '≈ 2 min'))):
    y = 40 + i * 50
    a(text(20, y + 18, name.split(' ')[0], size=13, fill=col, ls='0'))
    if ' ' in name: a(text(20, y + 34, name.split(' ')[1], size=13, fill=col, ls='0'))
    a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="26" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.12)"/>')
    w = xs(sec) - X0
    a(f'<rect x="{X0}" y="{y}" width="{w:.1f}" height="26" rx="2" fill="{col}" fill-opacity="0.5">'
      f'{T.anim("width", [(0.0, w), (0.4, w), (0.405, 0.0), (C0, 0.0), (ts(sec), w), (D, w)])}</rect>')
    lx = xs(sec) + 6 if xs(sec) + 70 < X1 else xs(sec) - 6
    anchor = 'start' if xs(sec) + 70 < X1 else 'end'
    a(f'<g>{held(ts(sec))}{text(lx, y + 18, lab, anchor=anchor, size=13, fill="#fff", ls="0")}</g>')
# log axis
AY = 152
a(f'<line x1="{X0}" y1="{AY - 12}" x2="{X1}" y2="{AY - 12}" stroke="rgba(198,222,206,0.3)"/>')
for e, lab in zip(range(LO, HI + 1), ['1 ms', '10', '0.1 s', '1', '10 s', '100', '1000 s']):
    x = xs(10 ** e)
    a(f'<line x1="{x:.1f}" y1="{AY - 16}" x2="{x:.1f}" y2="{AY - 8}" stroke="rgba(198,222,206,0.4)"/>')
    if e in (-3, -1, 1, 3):
        a(text(x, AY + 6, lab, anchor='middle' if e not in (-3, 3) else ('start' if e == -3 else 'end'), size=13, fill=MUTED, ls='0'))
a(text(20, AY + 34, 'log scale: each tick is ×10', size=13, fill=MUTED, ls='0'))
# cursor, constant speed in log time
a(f'<line y1="34" y2="{AY - 12}" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}{T.anim("x2", [(0.0, X0), (C0, X0), (C1, X1), (D, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (C0 - 0.01, 0.0), (C0, 0.6), (C1, 0.6), (C1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ("Multiplying two 1000 × 1000 matrices takes about two minutes in pure Python, a billion multiply-adds each paying the interpreter's toll, and about a hundredth of a second with <code>np.dot</code>. On this logarithmic axis that is four steps of ten.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The count.</b> Three nested loops over 1000 make 10<sup>9</sup> multiply-adds, and in pure Python each one runs the steps of Fig 7.7.</li>
          <li><b>The other side.</b> <code>np.dot</code> hands the whole job to BLAS (Fig 7.8). Exact times vary with the machine; the ratio stays in the thousands.</li>
          <li><b>The rule.</b> Keep Python out of the inner loop: let it call code that loops in C.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-9">
      <div class="diagram-label">Fig 7.9 · The same matmul, two ways</div>
      {svg}
      <p id="ch7-datasci-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-9', 'ch7-datasci-p3', card)
