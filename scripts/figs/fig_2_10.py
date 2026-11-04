# Fig 2.10 · IEEE 754 double precision (Pass 31, Part I, from an empty script). Job: function. Takeaway: a sign, an
# exponent that moves the point and the digits rebuild 6.5 straight from a double's bits.
# Concept: the three fields as three boxes holding the real bits, then the rebuild: the sign gives +, the exponent
# (stored 1023 too high, said on the plate, since ch2-float-p6 teaches the bias only after the card) gives 2, and the
# binary point of 1.101 slides two places right (the "floating"), giving 110.1 = 6.5. The figure then does the same
# for −0.75, whose point slides one place left. t=0 is 6.5 rebuilt.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, MUTED

W, H = 400, 372
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
D = 10.0
T = Timeline(D, shift=3.2)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
A, B = [(0.0, 5.0)], [(5.0, D)]               # the two values' turns
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-26 svgd-part1-26"{T.steps([(3.5, '6.5'), (8.5, '−0.75')])}>')
a('<title id="svgt-part1-26">Fig 2.10 · IEEE 754 double precision · sign, exponent, mantissa</title>')
a('<desc id="svgd-part1-26">A 64-bit double is a sign bit, an 11-bit exponent and a 52-bit mantissa, read as ±1.mantissa with the binary '
  'point moved by the exponent, which is stored 1023 too high. 6.5 has sign 0, exponent 10000000001 (1025, so 2) and mantissa 101 then '
  'zeros: 1.101 with the point moved two places right is 110.1, which is 4 + 2 + one half = 6.5. −0.75 has sign 1, exponent '
  '01111111110 (1022, so −1) and mantissa 1 then zeros: 1.1 with the point moved one place left is 0.11, three quarters, negative.</desc>')

def fields(sign, exp, mant, spans):
    g = []
    g.append(f'<rect x="20" y="52" width="30" height="34" rx="4" fill="none" stroke="{RED}" stroke-width="1.5"/>')
    g.append(text(35, 75, sign, anchor='middle', size=15, fill=RED, ls='0', role='object'))
    g.append(f'<rect x="56" y="52" width="124" height="34" rx="4" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
    g.append(text(118, 75, exp, anchor='middle', size=14, fill=BLUE, ls='0', role='object'))
    g.append(f'<rect x="186" y="52" width="194" height="34" rx="4" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
    g.append(text(283, 75, mant, anchor='middle', size=14, fill=GOLD, ls='0', role='object'))
    a(f'<g opacity="0">{vis(spans)}{"".join(g)}</g>')
a(text(20, 42, 'sign', size=14, fill=RED))
a(text(118, 42, 'exponent', anchor='middle', size=14, fill=BLUE))
a(text(283, 42, 'mantissa', anchor='middle', size=14, fill=GOLD))
fields('0', '10000000001', '1010000000000…', A)
fields('1', '01111111110', '1000000000000…', B)

# the rebuild, three lines
def rows(sign_s, exp_n, shift_s, spans):
    g = [text(20, 122, 'sign', size=14, fill=MUTED), text(380, 122, sign_s, anchor='end', size=15, fill=RED, ls='0'),
         text(20, 148, f'exponent {exp_n} − 1023', size=14, fill=MUTED, ls='0'), '']
    a(f'<g opacity="0">{vis(spans)}{"".join(g)}</g>')
rows('+', 1025, 'point 2 right', A)
rows('−', 1022, 'point 1 left', B)

# the digits and the sliding binary point
CW, CX0, CY = 46, 112, 206
def digits(ds, x0, p0, p1, t0, spans, col_new=None):
    """ds: digit strings in cells from x0; the point sits after cell p0, slides to after cell p1 at story time t0."""
    g = []
    for i, d in enumerate(ds):
        x = x0 + i * CW
        g.append(f'<rect x="{x}" y="{CY}" width="{CW - 12}" height="44" rx="5" fill="none" stroke="{EDGE}"/>')
        g.append(text(x + (CW - 12) / 2, CY + 30, d, anchor='middle', size=20, fill=INK, ls='0', role='object'))
    px0, px1 = x0 + (p0 + 1) * CW - 6, x0 + (p1 + 1) * CW - 6
    s0, s1 = spans[0]
    mv = T.translate([(0.0, 0), (s0, 0), (s0 + t0, 0), (s0 + t0 + 0.8, px1 - px0), (s1 - 0.01, px1 - px0), (s1, 0), (D - 0.01, 0)], axis='x')
    g.append(f'<g>{mv}<circle cx="{px0}" cy="{CY + 38}" r="5" fill="{GOLD}"/></g>')
    a(f'<g opacity="0">{vis(spans)}{"".join(g)}</g>')
digits(['1', '1', '0', '1'], CX0, 0, 2, 1.4, A[0:1])
digits(['0', '1', '1'], CX0 - CW, 1, 0, 1.4, B[0:1])
# the results
res_a = [text(200, 286, '110.1 = 4 + 2 + 0.5', anchor='middle', size=15, fill=INK, ls='0'), text(200, 322, '+6.5', anchor='middle', size=20, fill=GOLD, ls='0')]
res_b = [text(200, 286, '0.11 = 0.5 + 0.25', anchor='middle', size=15, fill=INK, ls='0'), text(200, 322, '−0.75', anchor='middle', size=20, fill=GOLD, ls='0')]
a(f'<g opacity="0">{vis([(0.0, 5.0)])}{"".join(res_a)}</g>')
a(f'<g opacity="0">{vis([(5.0, D)])}{"".join(res_b)}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = 'The exponent slides the binary point: two places right for 6.5, one left for −0.75.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Sign.</b> 0 is positive, 1 negative.</li>
          <li><b>Exponent.</b> Stored with 1023 added, so 1025 means move the point 2 right and 1022 means 1 left. Eleven bits give a range of about 10⁻³⁰⁸ to 10³⁰⁸.</li>
          <li><b>Mantissa.</b> The digits after the hidden leading 1; fifty-two bits give 15 to 17 decimal digits.</li>
          <li><b>Single precision.</b> The 32-bit float is the same with 1, 8 and 23 bits.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-10">
      <div class="diagram-label">Fig 2.10 · IEEE 754 double precision · sign, exponent, mantissa</div>
      {svg}
      <p id="ch2-float-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-10', 'ch2-float-p5', card)
