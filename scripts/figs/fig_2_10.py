# Fig 2.10 · IEEE 754 double (Pass 28, law 3). Real bits, decoded: 6.5 and −0.75 take turns.
# Sign, 11 exponent bits, the first 12 of 52 mantissa bits; each field lights as its meaning
# is worked out. Bits come from struct, not by hand. t=0: 6.5 fully decoded.
import struct
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 360
def fields(x):
    b = format(struct.unpack('>Q', struct.pack('>d', x))[0], '064b')
    return b[0], b[1:12], b[12:]
EX = [(6.5, '6.5', '1.101', '1.625', 4, '× 4'), (-0.75, '−0.75', '1.1', '1.5', 0.5, '× ½')]
for x, *_ in EX:
    s, e, m = fields(x)
for x, lab, mb, mdec, scale, sc in EX:
    s, e, m = fields(x)
    assert (-1) ** int(s) * float(mdec) * scale == x and 2.0 ** (int(e, 2) - 1023) == scale
HALF = 5.0
T = Timeline(2 * HALF, shift=4.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (2 * HALF - 0.0005, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-26 svgd-part1-26">')
a('<title id="svgt-part1-26">Fig 2.10 · IEEE 754 double precision · sign, exponent, mantissa</title>')
a('<desc id="svgd-part1-26">A 64-bit double is a sign bit, an 11-bit exponent and a 52-bit mantissa, read as (−1)^S × 1.M × 2^(E − 1023). '
  '6.5 has sign 0, exponent 10000000001 (1025, so 2 to the 2 = 4) and mantissa 101 then zeros (1.101 in binary = 1.625): 1.625 × 4 = 6.5. '
  '−0.75 has sign 1, exponent 01111111110 (1022, so one half) and mantissa 1 then zeros (1.5): −1.5 × ½ = −0.75.</desc>')
a(text(200, 66, '(−1)^S × 1.M × 2^(E − 1023)', anchor='middle', size=14, fill=MUTED, ls='0'))
a(text(20, 92, 'S', size=13, fill=RED)); a(text(52, 92, 'exponent · 11 bits', size=13, fill=BLUE))
a(text(20, 148, 'mantissa · 52 bits', size=13, fill=GOLD))
CELL = 26
for k, (x, lab, mb, mdec, scale, sc) in enumerate(EX):
    s, e, m = fields(x)
    t0 = k * HALF
    g = [f'<g opacity="0">{win(t0, t0 + HALF)}']
    g.append(f'<text x="200" y="38" text-anchor="middle" {MONO} font-size="28" fill="#fff">{lab}</text>')
    g.append(f'<rect x="20" y="100" width="{CELL - 2}" height="28" rx="3" fill="{RED}" fill-opacity="0.25" stroke="{RED}"/>'
             f'<text x="{20 + CELL / 2 - 1}" y="120" text-anchor="middle" {MONO} font-size="15" fill="#fff">{s}</text>')
    for i, bit in enumerate(e):
        xx = 52 + i * CELL
        g.append(f'<rect x="{xx}" y="100" width="{CELL - 2}" height="28" rx="3" fill="{BLUE}" fill-opacity="0.2" stroke="{BLUE}" stroke-opacity="0.8"/>'
                 f'<text x="{xx + CELL / 2 - 1}" y="120" text-anchor="middle" {MONO} font-size="15" fill="#fff">{bit}</text>')
    for i, bit in enumerate(m[:12]):
        xx = 20 + i * CELL
        g.append(f'<rect x="{xx}" y="156" width="{CELL - 2}" height="28" rx="3" fill="{GOLD}" fill-opacity="0.18" stroke="{GOLD}" stroke-opacity="0.8"/>'
                 f'<text x="{xx + CELL / 2 - 1}" y="176" text-anchor="middle" {MONO} font-size="15" fill="#fff">{bit}</text>')
    g.append(f'<text x="380" y="204" text-anchor="end" {MONO} font-size="13" fill="rgba(255,255,255,0.5)">… 40 more bits, all 0</text>')
    g.append('</g>'); a(''.join(g))
    # the decode, field by field
    E = int(e, 2)
    lines = [(0.6, RED, f'sign {s}', '+' if s == '0' else '−'),
             (1.6, BLUE, f'exponent {E} − 1023 = {E - 1023}'.replace('= -', '= −'), sc),
             (2.6, GOLD, f'mantissa 1.{mb[2:]} (binary)', f'= {mdec}')]
    for j, (td, col, l, r) in enumerate(lines):
        y = 236 + j * 28
        a(f'<g opacity="0">{win(t0 + td, t0 + HALF)}<text x="20" y="{y}" {MONO} font-size="15" fill="{col}">{l}</text>'
          f'<text x="380" y="{y}" text-anchor="end" {MONO} font-size="15" fill="#fff">{r}</text></g>')
    a(f'<g opacity="0">{win(t0 + 3.6, t0 + HALF)}<line x1="20" y1="{236 + 2 * 28 + 14}" x2="380" y2="{236 + 2 * 28 + 14}" stroke="rgba(255,255,255,0.3)"/>'
      f'<text x="380" y="{236 + 3 * 28 + 10}" text-anchor="end" {MONO} font-size="20" fill="{GOLD}">{"+" if s == "0" else "−"}{mdec} {sc} = {lab}</text></g>')
    # the field being read, outlined
    for td, x0, w, y0 in ((0.6, 18, CELL + 2, 98), (1.6, 50, 11 * CELL + 2, 98), (2.6, 18, 12 * CELL + 2, 154)):
        a(f'<rect x="{x0}" y="{y0}" width="{w}" height="32" rx="4" fill="none" stroke="#fff" stroke-width="2" opacity="0">{win(t0 + td, t0 + td + 1.0)}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A double is binary scientific notation: a sign, an 11-bit exponent stored 1023 too high so it can be negative, and 52 bits of mantissa after an implied leading 1. '
           'Here 6.5 and −0.75 are read straight off their bits.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Sign.</b> 0 is positive, 1 negative.</li>
          <li><b>Exponent.</b> Stored with a bias of 1023: 1025 means 2², 1022 means 2⁻¹. Eleven bits give a range of about 10⁻³⁰⁸ to 10³⁰⁸.</li>
          <li><b>Mantissa.</b> The digits after the binary point of 1.M; the leading 1 is implied, never stored. Fifty-two bits give 15 to 17 decimal digits.</li>
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
