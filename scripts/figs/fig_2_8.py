# Fig 2.8 · The two's-complement wheel (Pass 31, Part I, from an empty script). Job: function. Takeaway: a byte's values
# wrap round a wheel, so dropping the carry subtracts and +127 + 1 turns negative.
# Concept: the 256 values of a byte on a dial, the half whose top bit is 1 read as negatives (red), the rest positive
# (gold). Adding turns the pointer clockwise; the pointer steps round in jumps of 16 (Part I's step verb) with the value
# and its bits at the centre. Where +127 meets −128 at the bottom the wrap is a silent overflow; where −1 meets 0 at the
# top it is the dropped carry that makes subtraction work. t=0 is the pointer just past the bottom seam.
from math import sin, cos, radians
from figlib import Timeline, text, splice, GOLD, RED, MUTED

W, H = 400, 420
INK = '#ece6da'
CX, CY, R = 200, 196, 128
D = 10.0
T = Timeline(D, shift=4.2)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
ang = lambda u: radians(u * 360 / 256)          # clockwise from the top
P = lambda u, r: (CX + r * sin(ang(u)), CY - r * cos(ang(u)))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-24 svgd-part1-24">')
a("<title id=\"svgt-part1-24\">Fig 2.8 · The two's-complement wheel · where addition wraps</title>")
a('<desc id="svgd-part1-24">The 256 values of a signed 8-bit number around a dial: 0 at the top, positives clockwise down the right to +127, '
  'negatives up the left from −128 to −1, so +127 and −128 meet at the bottom. Adding turns the pointer clockwise; the value and its '
  'bits show at the centre. From +127, adding 1 lands on −128, a silent overflow; from −1, adding 1 lands on 0, the dropped carry '
  'that makes subtraction by addition work.</desc>')

# the two halves of the ring
def arc(u0, u1, col):
    (x0, y0), (x1, y1) = P(u0, R), P(u1, R)
    a(f'<path d="M {x0:.1f} {y0:.1f} A {R} {R} 0 0 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="butt"/>')
arc(0.4, 127.6, GOLD); arc(128.4, 255.6, RED)
for u in range(0, 256, 16):
    (x0, y0), (x1, y1) = P(u, R - 12), P(u, R + 12)
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="1.4"/>')
# the seam markers and their names
for u, lab, col, anc, dx, dy in ((0, '0', GOLD, 'start', 8, -22), (255, '−1', RED, 'end', -8, -22), (64, '+64', GOLD, 'start', 22, 5),
                                 (192, '−64', RED, 'end', -22, 5), (127, '+127', GOLD, 'start', 8, 32), (128, '−128', RED, 'end', -8, 32)):
    x, y = P(u, R)
    a(text(x + dx, y + dy, lab, anchor=anc, size=15, fill=col, ls='0'))

# the pointer, stepping clockwise 16 values at a time
seq = [(0.5 * k, (16 * k) % 256) for k in range(17)]
vals, kts = [], []
for tau, u in seq:
    t = T.t(tau); kts.append(t)
pairs = sorted((T.t(tau), u) for tau, u in seq)
first = pairs[-1][1] if pairs[0][0] > 0 else pairs[0][1]
steps = ([(0.0, first)] if pairs[0][0] > 0 else []) + pairs
kt = ';'.join(f'{t / D:.6f}' for t, _ in steps)
vs = ';'.join(f'{u * 360 / 256:.3f} {CX} {CY}' for _, u in steps)
a(f'<g><animateTransform attributeName="transform" type="rotate" values="{vs}" keyTimes="{kt}" calcMode="discrete" dur="{D:g}s" repeatCount="indefinite"/>'
  f'<line x1="{CX}" y1="{CY - 54}" x2="{CX}" y2="{CY - R + 22}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
  f'<circle cx="{CX}" cy="{CY - R + 22}" r="5" fill="{INK}"/></g>')
a(f'<circle cx="{CX}" cy="{CY}" r="50" fill="none" stroke="rgba(255,255,255,0.5)"/>')
# the value and its bits at the centre
for k, (tau, u) in enumerate(seq):
    end = D if k == len(seq) - 1 else tau + 0.5
    sv = u - 256 if u >= 128 else u
    col = RED if sv < 0 else GOLD
    a(f'<g opacity="0">{vis([(tau, end)])}'
      + text(CX, CY + 4, f'{sv:+d}'.replace('-', '−') if sv else '0', anchor='middle', size=24, fill=col, ls='0', role='object')
      + text(CX, CY + 26, format(u, '08b'), anchor='middle', size=14, fill=MUTED, ls='0', role='object') + '</g>')

# what each seam means
a(f'<g opacity="0">{vis([(4.0, 6.0)])}' + text(200, 380, '+127 + 1 = −128', anchor='middle', size=17, fill=RED, ls='0')
  + text(200, 402, 'overflow: a silent wrap', anchor='middle', size=14, fill=RED) + '</g>')
a(f'<g opacity="0">{vis([(0.0, 1.5), (8.0, D)])}' + text(200, 380, '−1 + 1 = 0', anchor='middle', size=17, fill=GOLD, ls='0')
  + text(200, 402, 'the carry dropped: correct', anchor='middle', size=14, fill=GOLD) + '</g>')
a(f'<g opacity="0">{vis([(1.5, 4.0), (6.0, 8.0)])}' + text(200, 380, 'adding turns the pointer clockwise', anchor='middle', size=14, fill=MUTED) + '</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The 256 values of a signed byte sit on a wheel, not a line: adding turns the pointer clockwise. At the bottom +127 + 1 '
           'silently becomes −128; at the top −1 + 1 becomes 0, the same wrap that makes subtraction free in Fig 2.7.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The slots.</b> 0 at the top, positives clockwise to +127, negatives counter-clockwise from −1 to −128. The pointer here jumps 16 values at a time; a +1 is one notch of 256.</li>
          <li><b>The seam.</b> 01111111 + 1 = 10000000: the top bit flips, and a top bit of 1 means negative. Nothing in the hardware complains.</li>
          <li><b>Every width.</b> 32- and 64-bit integers have the same wheel, with about 4 billion and 18 quintillion slots.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-8">
      <div class="diagram-label">Fig 2.8 · The two's-complement wheel · where addition wraps</div>
      {svg}
      <p id="ch2-twos-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-8', 'ch2-twos-p9', card)
