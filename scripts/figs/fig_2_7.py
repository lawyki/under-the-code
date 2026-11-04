# Fig 2.7 · Computing 7 − 5 (Pass 31, Part I, from an empty script). Job: function. Takeaway: minus x is stored as
# 256 − x, so adding it and dropping the ninth bit subtracts x.
# Concept: the column addition itself inside an 8-bit register frame. The carries ripple in from the right, one column
# at a time (Part I's step verb), and the last one has nowhere to go: it lands outside the frame and falls away. What
# is left is 2. t=0 is the finished sum, the ninth bit already fallen.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, MUTED

W, H = 400, 300
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
A, B = 7, 256 - 5
S = A + B
ab, bb = format(A, '08b'), format(B, '08b')
carries, c = [], 0
for i in range(7, -1, -1):
    s_ = int(ab[i]) + int(bb[i]) + c
    c = s_ >> 1
    carries.append(c)                      # carry out of column i (right to left)
res = format(S & 255, '08b')
CW, X0 = 30, 98                            # column width, first column x
CX = lambda i: X0 + i * CW + CW / 2
D = 9.0
T = Timeline(D, shift=7.5)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-23 svgd-part1-23"{T.steps([(0.3, 'start'), (2.8, 'carrying'), (8.0, 'result')])}>')
a("<title id=\"svgt-part1-23\">Fig 2.7 · Computing 7 − 5 = 2 with two's complement</title>")
a('<desc id="svgd-part1-23">Inside an 8-bit register, 00000111 (7) plus 11111011 (−5 in two\'s complement, which is 256 − 5), added column '
  'by column from the right. Every column carries 1 into the next, and the final carry is a ninth bit the register cannot hold. It '
  'falls off and is dropped; what remains, 00000010, is 2.</desc>')

# the register frame
a(f'<rect x="{X0 - 8}" y="34" width="{8 * CW + 16}" height="166" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
a(text(X0 - 8, 24, '8-bit register', size=14, fill=MUTED))
# the two numbers
for i in range(8):
    a(text(CX(i), 92, ab[i], anchor='middle', size=18, fill=INK, ls='0', role='object'))
    a(text(CX(i), 128, bb[i], anchor='middle', size=18, fill=INK, ls='0', role='object'))
a(text(X0 - 22, 128, '+', anchor='middle', size=18, fill=INK))
a(text(380, 92, '7', anchor='end', size=16, fill=BLUE)); a(text(380, 128, '−5', anchor='end', size=16, fill=BLUE))
a(f'<line x1="{X0}" y1="144" x2="{X0 + 8 * CW}" y2="144" stroke="{INK}" stroke-width="1.6"/>')
# the carries and the sum, column by column from the right
for k in range(8):
    i = 7 - k
    t0 = 0.6 + k * 0.55
    a(f'<g opacity="0">{vis([(t0, D)])}' + text(CX(i), 180, res[i], anchor='middle', size=18, fill=GOLD, ls='0', role='object') + '</g>')
    if carries[k] and i > 0:
        a(f'<g opacity="0">{vis([(t0 + 0.2, D)])}' + text(CX(i - 1), 60, '1', anchor='middle', size=14, fill=GOLD, ls='0', role='object') + '</g>')
a(text(380, 180, '2', anchor='end', size=16, fill=GOLD))
# the ninth bit: carried out of the last column, no room, falls away
t9 = 0.6 + 8 * 0.55
nx = X0 - 48
a(f'<g opacity="0">{vis([(t9, D)])}<g>{T.translate([(0.0, 0), (t9 + 0.4, 0), (t9 + 1.4, 50), (D - 0.01, 50)], axis="y")}'
  + text(nx, 180, '1', anchor='middle', size=18, fill=RED, ls='0', role='object') + '</g></g>')
a(f'<g opacity="0">{vis([(t9, D)])}<path d="M {X0 + 4} 62 Q {nx} 70 {nx} 162" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="3 3"/></g>')
a(text(nx - 14, 262, 'ninth bit: no room, dropped', size=14, fill=RED))
a('</svg>')
svg = '\n'.join(o)

caption = '7 − 5 on the ordinary adder: 7 plus 11111011, with the ninth bit dropped.'
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
