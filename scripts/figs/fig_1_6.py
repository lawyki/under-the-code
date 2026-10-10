# Fig 1.6 · Moore's Law (Pass 28, law 3). Log chart, phone-first. Chips appear in time
# order; the dashed line doubles every two years from the 4004. After ~2015 the chips
# fall below it. t=0: everything drawn.
import math
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 328
CHIPS = [('4004', 1971, 2300), ('8086', 1978, 29e3), ('386', 1985, 275e3), ('Pentium', 1993, 3.1e6),
         ('Pentium 4', 2000, 42e6), ('Core i7', 2008, 731e6), ('Epyc', 2017, 19.2e9), ('M4', 2024, 28e9)]
X0, X1, Y0, Y1 = 64, 372, 272, 24                 # plot box: 1971..2024, 100..100 B
X = lambda yr: X0 + (yr - 1971) / 53 * (X1 - X0)
Y = lambda n: Y0 - (math.log10(n) - 2) / 9 * (Y0 - Y1)
T = Timeline(8, shift=6.5)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-7 svgd-part1-7">')
a("<title id=\"svgt-part1-7\">Fig 1.6 · Moore's Law · transistors per chip, 1971 to 2024</title>")
a('<desc id="svgd-part1-7">Transistors per chip on a logarithmic scale, from the Intel 4004 in 1971 with 2,300 to the Apple M4 in 2024 with 28 billion, '
  'twelve million times more. A dashed line doubles every two years from the 4004; the chips follow it closely until about 2015, then fall below it.</desc>')
# grid: a line every 10x, a label every 100x
for d in range(2, 12):
    y = Y(10 ** d)
    a(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="rgba(255,255,255,{0.12 if d % 2 else 0.06})"/>')
for d, lab in ((2, '100'), (4, '10 K'), (6, '1 M'), (8, '100 M'), (10, '10 B')):
    a(text(X0 - 8, Y(10 ** d) + 5, lab, anchor='end', size=14, fill=MUTED, ls='0'))
for yr in (1971, 2000, 2024):
    a(text(X(yr), Y0 + 24, str(yr), anchor='middle', size=14, fill=MUTED, ls='0'))
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="rgba(255,255,255,0.3)"/>')
# the two-year doubling line from the 4004, to where it leaves the chart
yr_end = 1971 + (11 - math.log10(2300)) / (math.log10(2) / 2)
x2, y2 = X(yr_end), Y(1e11)
ln = math.dist((X(1971), Y(2300)), (x2, y2))
a(f'<line x1="{X(1971):.1f}" y1="{Y(2300):.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="5 5" opacity="0.7"/>')
a(f'<rect x="216" y="150" width="160" height="94" rx="4" fill="#111111" fill-opacity="0.92"/>')   # keep the gridlines out from under the words
a(text(X1, 170, '×2 every 2 years', anchor='end', fill=GOLD))
# chips appear in time order
for i, (name, yr, n) in enumerate(CHIPS):
    t0 = 0.5 + i * 0.45
    a(f'<circle cx="{X(yr):.1f}" cy="{Y(n):.1f}" r="5.5" fill="{BLUE}" stroke="#0e0e0e" stroke-width="1.5">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0, 0.0), (t0 + 0.15, 1.0), (7.6, 1.0), (7.9, 0.0)])}<title>{name} · {yr}</title></circle>')
a(text(X(1971) + 10, Y(2300) + 24, '4004 · 2,300', size=14, fill='rgba(255,255,255,0.85)', ls='0'))
a(text(X(2024) - 4, Y(28e9) + 26, 'M4 · 28 B', anchor='end', size=14, fill='rgba(255,255,255,0.85)', ls='0'))
a(f'<text x="{X1}" y="218" text-anchor="end" {MONO} font-size="20" fill="#fff">×12 million</text>')
a(text(X1, 238, 'in 53 years', anchor='end', fill=MUTED))
a(text(X0, H - 8, 'transistors per chip, log scale', size=13, fill='rgba(255,255,255,0.45)', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('On a log scale steady doubling draws a straight line: from 2,300 transistors in 1971 to 28 billion in 2024. '
           'Since about 2015 the chips have fallen below the two-year line as transistors approach the size of atoms.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> Each gridline is ten times the one below, so growth at a steady rate of doubling is a straight line.</li>
          <li><b>The chips.</b> 4004 (1971, 2,300) · 8086 (1978, 29 K) · 386 (1985, 275 K) · Pentium (1993, 3.1 M) · Pentium 4 (2000, 42 M) · Core i7 (2008, 731 M) · Epyc (2017, 19.2 B) · M4 (2024, 28 B).</li>
          <li><b>The line.</b> Doubling every two years from the 4004. Across the whole span the chips doubled about every two and a quarter years.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-6">
      <div class="diagram-label">Fig 1.6 · Moore's Law · transistors per chip, 1971 to 2024</div>
      {svg}
      <p id="ch1-transistor-p11" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-6', 'ch1-transistor-p11', card)
