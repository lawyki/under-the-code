# Fig 2.11 · 0.1 + 0.2 in binary (Pass 31, Part I, from an empty script). Job: function. Takeaway: stored 0.1 and 0.2
# run slightly high, so their sum lands halfway between doubles and the tie rounds up.
# Concept: three number lines, each drawn to the scale of the doubles near it (the ticks are neighbouring doubles).
# On the first two the stored value sits a little right of the exact one: both run high. On the third, the exact sum
# of the two stored values lands exactly halfway between two doubles, and the tie rounds up to the one that prints
# 0.30000000000000004; the stored 0.3 is the double below. The first panel of the old card (0.1's repeating bits)
# repeated ch2-float-p2 and is gone, as the ledger asks. t=0 is the rounded result.
from figlib import Timeline, text, splice, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 330
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
T = Timeline(8, shift=6.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-27 svgd-part1-27"{T.steps([(1.3, 'sum lands'), (5.0, 'rounds up')])}>')
a('<title id="svgt-part1-27">Fig 2.11 · 0.1 + 0.2 in binary · where the famous error lives</title>')
a('<desc id="svgd-part1-27">Three number lines, each showing the neighbouring doubles near one value, to that value\'s own scale. 0.1 and '
  '0.2 cannot be stored exactly; each is stored as the nearest double, which lies slightly above the exact value. Near 0.3 the doubles '
  'are about 5.6 × 10⁻¹⁷ apart, and the exact 0.3 lies a fifth of a step above the double that 0.3 is stored as. The exact sum of the '
  'stored 0.1 and 0.2 falls exactly halfway between two doubles, and the tie rounds up to the next double, which prints as '
  '0.30000000000000004.</desc>')

X0, STEP = 60, 100                          # tick k at X0 + k * STEP
def line(y, name, ticks=4):
    a(f'<line x1="30" y1="{y}" x2="380" y2="{y}" stroke="{EDGE}" stroke-width="1.4"/>')
    for k in range(ticks):
        a(f'<line x1="{X0 + k * STEP}" y1="{y - 8}" x2="{X0 + k * STEP}" y2="{y + 8}" stroke="{INK}" stroke-width="1.6"/>')
    a(text(20, y - 16, name, size=15, fill=INK, ls='0'))
def exact(x, y): a(f'<line x1="{x}" y1="{y - 18}" x2="{x}" y2="{y + 4}" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="3 2"/>')
def stored(x, y): a(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{BLUE}"/>')

# the legend
a(f'<line x1="214" y1="16" x2="214" y2="32" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="3 2"/>')
a(text(224, 29, 'exact', size=14, fill=GREEN))
a(f'<circle cx="302" cy="24" r="6" fill="{BLUE}"/>')
a(text(314, 29, 'stored', size=14, fill=BLUE))

# 0.1 and 0.2: each stored as the double just above it (0.4 of a step)
for y, name in ((76, '0.1'), (142, '0.2')):
    line(y, name)
    exact(X0 + 1.6 * STEP, y); stored(X0 + 2 * STEP, y)

# 0.3: d0 at tick 1 (where 0.3 is stored), d1 at tick 2
Y = 230
line(Y, '0.1 + 0.2')
d0, d1 = X0 + STEP, X0 + 2 * STEP
exact(d0 + 0.2 * STEP, Y)
stored(d0, Y)
a(text(d0, Y + 30, '0.3 stored', anchor='middle', size=14, fill=BLUE))
mid = (d0 + d1) / 2
# the exact sum lands halfway, then rounds up to the next double
a(f'<path d="M {mid} {Y - 28} V {Y - 10}" stroke="{GOLD}" stroke-width="2"/>')
a(f'<circle cx="{mid}" cy="{Y}" r="5" fill="none" stroke="{GOLD}" stroke-width="2"/>')
a(text(mid, Y - 34, 'sum', anchor='middle', size=14, fill=GOLD))
a(f'<path d="M {mid + 8} {Y + 14} Q {(mid + d1) / 2} {Y + 30} {d1 - 6} {Y + 14}" fill="none" stroke="{GOLD}" stroke-width="1.8"/>')
a(f'<path d="M {d1 - 3} {Y + 10} l -8 1 l 4 7 z" fill="{GOLD}"/>')
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (2.0, 0.0), (2.6, 1.0), (7.8, 1.0), (7.99, 0.0)])}'
  f'<circle cx="{d1}" cy="{Y}" r="7" fill="{GOLD}"/></g>')
# the moving sum: drops onto the halfway point, then rolls up to d1
a(f'<g opacity="0">{T.anim("opacity", [(0.3, 0.0), (0.5, 1.0), (2.6, 1.0), (2.8, 0.0)])}'
  f'<g>{T.translate([(0.0, 0), (1.4, 0), (2.4, d1 - mid), (7.99, d1 - mid)], axis="x")}'
  f'<g>{T.translate([(0.0, -40), (0.5, -40), (1.2, 0), (7.99, 0)], axis="y")}<circle cx="{mid}" cy="{Y}" r="6" fill="{GOLD}"/></g></g></g>')
a(f'<path d="M {d0 + 10} {Y + 46} H {d1 - 10}" stroke="{MUTED}"/>')
a(text(mid, Y + 64, '5.6 × 10⁻¹⁷', anchor='middle', size=14, fill=MUTED, ls='0'))
a(text(200, 318, '0.1 + 0.2 prints 0.30000000000000004', anchor='middle', size=14, fill=INK, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = 'Both stored values run high, so their sum lands halfway and rounds up.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it repeats.</b> 0.1 is 1/10, and 10 has a factor of 5 that no power of two can supply, just as 1/3 never ends in decimal.</li>
          <li><b>The grid.</b> Doubles are not continuous: the ticks are neighbouring doubles, and each line has its own scale. Near 0.3 neighbours are 2⁻⁵⁴, about 5.6 × 10⁻¹⁷, apart; the true 0.3 falls between two of them.</li>
          <li><b>The result.</b> "0.3" is stored as the double just below it; the rounded 0.1 and 0.2 add up to a value exactly halfway between that double and the next, and the tie rounds up to the next. So in most languages 0.1 + 0.2 == 0.3 is false.</li>
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
