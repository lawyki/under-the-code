# Fig 1.6 · Moore's Law (Pass 31, Part I, from an empty script). Job: function. Takeaway: transistor counts
# doubled about every two years, so on a tenfold-per-step scale they rise in a straight line.
# Concept: one chart, every gridline ten times the one below and said so on the plate (the ledger's Phase 2
# input: no "log scale" jargon). The chips land in time order (Part I's step verb) beside a dashed two-year
# doubling line; the last ones fall below it. t=0 is the finished chart.
from math import log10
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 330
INK = '#ece6da'
CHIPS = [('4004', 1971, 2300), ('8086', 1978, 29e3), ('386', 1985, 275e3), ('Pentium', 1993, 3.1e6),
         ('Pentium 4', 2000, 42e6), ('Core i7', 2008, 731e6), ('Epyc', 2017, 19.2e9), ('M4', 2024, 28e9)]
X0, X1, Y0, Y1 = 36, 366, 290, 34           # plot box: 1971..2024 across, 1 thousand..100 billion up
LO, HI = 3, 11
X = lambda yr: X0 + (yr - 1971) / (2024 - 1971) * (X1 - X0)
Y = lambda v: Y0 - (log10(v) - LO) / (HI - LO) * (Y0 - Y1)
T = Timeline(10, shift=8.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-7 svgd-part1-7"{T.steps([(1.3, "1971"), (3.6, "2000"), (7.0, "2024")])}>')
a("<title id=\"svgt-part1-7\">Fig 1.6 · Moore's Law · transistors per chip, 1971 to 2024</title>")
a('<desc id="svgd-part1-7">Transistors per chip from 1971 to 2024, on a chart where each gridline is ten times the one below, from a '
  'thousand at the bottom to a hundred billion at the top. A dashed line doubles every two years. The chips land on it one by one, '
  'from the Intel 4004 with 2,300 in 1971 to the Apple M4 with 28 billion in 2024, in a straight line for more than forty years; '
  'the last ones fall below it.</desc>')

# the gridlines: each ten times the one below
for d in range(LO, HI + 1):
    y = Y0 - (d - LO) / (HI - LO) * (Y0 - Y1)
    a(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="rgba(255,255,255,{0.55 if d in (3, 6, 9) else 0.5})" stroke-width="{1 if d in (3, 6, 9) else 0.6}"/>')
a(text(X1, Y(1e3) - 6, '1 thousand', anchor='end', size=14, fill=MUTED))
a(text(X1, Y(1e9) + 18, '1 billion', anchor='end', size=14, fill=MUTED))
# the tenfold step, shown once with a bracket
yb, yt = Y(1e5), Y(1e6)
a(f'<path d="M {X1 - 4} {yb:.1f} h 8 M {X1} {yb:.1f} V {yt:.1f} M {X1 - 4} {yt:.1f} h 8" stroke="{INK}" stroke-width="1.4" fill="none"/>')
a(text(X1 - 10, (yb + yt) / 2 + 5, 'each line ×10', anchor='end', size=14, fill=INK))

# the doubling line, every two years from the 4004, clipped at the top
yr_top = 1971 + (HI - log10(2300)) / (log10(2) / 2)
a(f'<line x1="{X(1971):.1f}" y1="{Y(2300):.1f}" x2="{X(yr_top):.1f}" y2="{Y1}" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="5 5" opacity="0.85"/>')
a(text(X(1997), (Y(1e4) + Y(1e5)) / 2 + 5, '×2 every 2 years', anchor='start', size=14, fill=GOLD))

# the chips, in time order
for k, (name, yr, n) in enumerate(CHIPS):
    t0 = 1.0 + k * 0.6
    late = yr > 2015
    fill = BLUE
    a(f'<circle cx="{X(yr):.1f}" cy="{Y(n):.1f}" r="5.5" fill="{fill}" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.01, 0.0), (t0, 1.0), (9.8, 1.0)])}</circle>')
# the years
a(text(X0, 316, '1971: 2,300', anchor='start', size=14, fill=INK))
a(text(X1, 316, '2024: 28 billion', anchor='end', size=14, fill=INK))
a('</svg>')
svg = '\n'.join(o)

caption = ('Each gridline is ten times the one below, so steady doubling draws a straight line. The chips follow the dashed '
           'two-year line for more than forty years, then fall below it: 2,300 transistors in 1971, 28 billion in 2024.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> Each gridline is ten times the one below (a logarithmic scale), so growth at a steady rate of doubling is a straight line.</li>
          <li><b>The chips.</b> 4004 (1971, 2,300) · 8086 (1978, 29 K) · 386 (1985, 275 K) · Pentium (1993, 3.1 M) · Pentium 4 (2000, 42 M) · Core i7 (2008, 731 M) · Epyc (2017, 19.2 B across four chips in one package) · M4 (2024, 28 B).</li>
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
