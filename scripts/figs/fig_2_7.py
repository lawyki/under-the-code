# Fig 2.7 · 7 − 5 by addition (Pass 28, law 3). An 8-bit register holds 7 + (−5) as a column
# sum. Carries appear right to left; the last one is a ninth bit with no room in the register,
# and it drops away, leaving 00000010 = 2. t=0: the result, the dropped bit greyed outside.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 262
P, CW = 34, 31
X0 = 76                                    # bit 7 column left edge
cx = lambda bit: X0 + (7 - bit) * P + CW / 2
a_ = [int(c) for c in '00000111']; b_ = [int(c) for c in '11111011']
res, car = [], 0
cs = {}
for bit in range(8):
    s = a_[7 - bit] + b_[7 - bit] + car
    res.append(s % 2); car = s // 2; cs[bit + 1] = car
res = res[::-1]
assert ''.join(map(str, res)) == '00000010' and car == 1
T = Timeline(8, shift=7.0)
t_col = lambda bit: 0.5 + bit * 0.45
def show(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (7.7, 1.0), (7.701, 0.0), (7.999, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-23 svgd-part1-23">')
a("<title id=\"svgt-part1-23\">Fig 2.7 · Computing 7 − 5 = 2 with two's complement</title>")
a('<desc id="svgd-part1-23">Inside an 8-bit register, 00000111 (7) plus 11111011 (−5 in two\'s complement), added column by column from the right. '
  'Every column carries 1, and the final carry is a ninth bit the register cannot hold. It falls off and is dropped; what remains, 00000010, is 2.</desc>')
# the register: 8 cells per row
a(f'<rect x="{X0 - 6}" y="36" width="{8 * P + 8}" height="154" rx="6" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>')
a(text(X0 - 6, 28, "8-BIT REGISTER", size=13, fill=MUTED))
rows = [(78, a_, '7', '#fff'), (122, b_, '−5', '#fff')]
for y, bits, dec, col in rows:
    for bit in range(8):
        a(f'<text x="{cx(bit)}" y="{y}" text-anchor="middle" {MONO} font-size="20" fill="{col}">{bits[7 - bit]}</text>')
    a(text(388, y, dec, anchor='end', size=17, fill=BLUE, ls='0'))
a(text(X0 - 22, 122, '+', anchor='middle', size=20, fill='rgba(255,255,255,0.7)', ls='0'))
a(f'<line x1="{X0}" y1="138" x2="{X0 + 8 * P - 4}" y2="138" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>')
# carries, small, above the top row; then the result bits
for bit in range(1, 8):
    if cs[bit]:
        a(f'<text x="{cx(bit)}" y="56" text-anchor="middle" {MONO} font-size="14" fill="{GOLD}" opacity="0">1{show(t_col(bit - 1) + 0.2)}</text>')
for bit in range(8):
    a(f'<text x="{cx(bit)}" y="172" text-anchor="middle" {MONO} font-size="20" fill="{GOLD if res[7 - bit] else "#fff"}" opacity="0">{res[7 - bit]}{show(t_col(bit))}</text>')
    a(f'<rect x="{cx(bit) - CW / 2}" y="150" width="{CW}" height="30" rx="3" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t_col(bit) - 0.001, 0.0), (t_col(bit), 1.0), (t_col(bit) + 0.4, 1.0), (t_col(bit) + 0.401, 0.0), (7.999, 0.0)])}</rect>')
a(f'<text x="388" y="172" text-anchor="end" {MONO} font-size="17" fill="{GOLD}" opacity="0">2{show(t_col(7) + 0.3)}</text>')
# the ninth bit: born outside the register, then dropped
t9 = t_col(7) + 0.3
a(f'<text x="{X0 - 22}" y="172" text-anchor="middle" {MONO} font-size="20" fill="{RED}" opacity="0">1'
  f'{T.anim("opacity", [(0.0, 0.0), (t9 - 0.001, 0.0), (t9, 1.0), (t9 + 0.6, 1.0), (t9 + 1.4, 0.45), (7.7, 0.45), (7.701, 0.0), (7.999, 0.0)])}'
  f'{T.anim("y", [(0.0, 172), (t9 + 0.6, 172), (t9 + 1.4, 222), (7.7, 222), (7.701, 172), (7.999, 172)])}</text>')
a(f'<text x="{X0 - 6}" y="226" {MONO} font-size="14" fill="{RED}" opacity="0">ninth bit: no room, dropped{show(t9 + 1.4)}</text>')
a(text(X0 - 6, 254, 'the same adder as every addition', size=13, fill='rgba(255,255,255,0.45)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('To subtract 5 the CPU adds −5, written in two\'s complement, on its ordinary adder. '
           'The sum has a ninth bit the register cannot hold; it falls off, and what remains is exactly 7 − 5.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Making −5.</b> Flip every bit of 5 (00000101 → 11111010) and add 1: 11111011.</li>
          <li><b>Why it works.</b> 11111011 is 251, which is 256 − 5. Adding it adds 256 and takes away 5.</li>
          <li><b>The lost 256.</b> 256 is the ninth bit. An 8-bit register has no place for it, so it is dropped and the answer is 2. There is no separate subtractor in any modern CPU.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-7">
      <div class="diagram-label">Fig 2.7 · Computing 7 − 5 = 2 with two's complement</div>
      {svg}
      <p id="ch2-twos-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-7', 'ch2-twos-p7', card)
