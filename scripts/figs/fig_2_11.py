# Fig 2.11 · 0.1 + 0.2 (Pass 28, law 3). Above: 0.1 in binary repeats forever and is cut at
# 52 bits. Below: the representable doubles near 0.3, to scale. Exact 0.3 lies a fifth of a step
# above the double that "0.3" is stored as; 0.1 + 0.2 lands on the next double up.
# (Python: 0.3 is 0.29999999999999998889..., 0.1 + 0.2 is 0.30000000000000004440..., the next.)
import math
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, GREEN, MUTED

assert math.nextafter(0.3, 1) == 0.1 + 0.2
W, H = 400, 352
T = Timeline(8, shift=7.0)
def show(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (7.7, 1.0), (7.701, 0.0), (7.999, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-27 svgd-part1-27">')
a('<title id="svgt-part1-27">Fig 2.11 · 0.1 + 0.2 in binary · where the famous error lives</title>')
a('<desc id="svgd-part1-27">0.1 in binary is 0.0 0011 0011 0011 and so on forever, so a double keeps only the first 52 bits and rounds. '
  'Near 0.3 the doubles are spaced about 5.6 × 10⁻¹⁷ apart. The exact value 0.3 lies a fifth of a step above the double that 0.3 is stored as. '
  'Adding the rounded 0.1 and 0.2 lands on the next double up, which prints as 0.30000000000000004.</desc>')
# 0.1 in binary, repeating, cut
a(text(20, 26, '0.1 IN BINARY', size=13, fill=MUTED))
groups = ['0.0', '0011', '0011', '0011', '0011', '0011']
x = 20
for i, gname in enumerate(groups):
    col = '#fff' if i == 0 else (GOLD if i % 2 else 'rgba(212,168,83,0.75)')
    a(f'<text x="{x}" y="56" {MONO} font-size="17" fill="{col}">{gname}{show(0.3 + i * 0.25) if i else ""}</text>')
    x += 50 if i == 0 else 52
a(f'<text x="{x}" y="56" {MONO} font-size="17" fill="rgba(212,168,83,0.5)">…</text>')
a(text(20, 80, 'repeats forever; a double keeps 52 bits', size=14, fill=MUTED, ls='0'))
# the number line near 0.3, to scale: one tick per double
Y = 196
STEP = 92
X0 = 200 - STEP                      # the double "0.3" is stored as
xs = [X0 - STEP, X0, X0 + STEP, X0 + 2 * STEP]
a(text(20, 128, 'THE DOUBLES NEAR 0.3', size=13, fill=MUTED))
a(f'<line x1="14" y1="{Y}" x2="386" y2="{Y}" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>')
for xx in xs:
    a(f'<line x1="{xx}" y1="{Y - 12}" x2="{xx}" y2="{Y + 12}" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>')
a(f'<path d="M {X0} {Y + 20} v 6 h {STEP} v -6" fill="none" stroke="rgba(255,255,255,0.4)"/>')
a(text(X0 + STEP / 2, Y + 44, '5.6 × 10⁻¹⁷', anchor='middle', size=13, fill=MUTED, ls='0'))
# exact 0.3: a fifth of a step above
xe = X0 + 0.2 * STEP
a(f'<line x1="{xe:.1f}" y1="{Y - 46}" x2="{xe:.1f}" y2="{Y}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="4 3"/>')
a(text(xe + 6, Y - 50, 'exact 0.3', size=14, fill=GREEN, ls='0'))
# where "0.3" is stored, and where the sum lands
a(f'<circle cx="{X0}" cy="{Y}" r="8" fill="{BLUE}" stroke="#0e0e0e" stroke-width="2"/>')
a(text(X0, Y + 72, '0.3', anchor='middle', size=15, fill=BLUE, ls='0'))
a(text(X0, Y + 90, 'as stored', anchor='middle', size=13, fill=MUTED, ls='0'))
x1 = X0 + STEP
a(f'<g opacity="0">{show(2.4)}<circle cx="{x1}" cy="{Y}" r="8" fill="{RED}" stroke="#0e0e0e" stroke-width="2"/></g>')
a(f'<circle r="8" fill="{RED}" opacity="0" cy="{Y}">{T.anim("cx", [(0.0, 20.0), (1.4, 20.0), (2.4, x1), (8.0, x1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (1.39, 0.0), (1.4, 1.0), (2.4, 1.0), (2.401, 0.0), (7.999, 0.0)])}</circle>')
a(f'<g opacity="0">{show(2.4)}<text x="{x1 + 10}" y="{Y + 72}" {MONO} font-size="15" fill="{RED}">0.1 + 0.2</text>'
  f'<text x="{x1 + 10}" y="{Y + 90}" {MONO} font-size="13" fill="rgba(255,255,255,0.6)">one double up</text></g>')
a(f'<g opacity="0">{show(3.4)}<text x="20" y="{Y + 132}" {MONO} font-size="16" fill="#fff">0.1 + 0.2 prints <tspan fill="{RED}">0.30000000000000004</tspan></text></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('0.1 never fits in binary: its digits repeat forever, so the double keeps the nearest 52-bit fraction, and 0.2 likewise. '
           'Their sum lands one representable step above where 0.3 itself is stored; the error was in the inputs, not the addition.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it repeats.</b> 0.1 is 1/10, and 10 has a factor of 5 that no power of two can supply, just as 1/3 never ends in decimal.</li>
          <li><b>The grid.</b> Doubles are not continuous. Near 0.3 neighbours are 2⁻⁵⁴, about 5.6 × 10⁻¹⁷, apart; the true 0.3 falls between two of them.</li>
          <li><b>The result.</b> "0.3" is stored as the double just below it; the rounded 0.1 and 0.2 add up to the one just above. So in most languages 0.1 + 0.2 == 0.3 is false.</li>
          <li><b>Living with it.</b> Compare floats within a tolerance, and count money in whole cents.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-11">
      <div class="diagram-label">Fig 2.11 · 0.1 + 0.2 in binary · where the famous error lives</div>
      {svg}
      <p id="ch2-float-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-11', 'ch2-float-p8', card)
