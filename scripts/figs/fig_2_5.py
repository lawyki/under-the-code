# Fig 2.5 · A 4-bit adder (Pass 28, law 3). 5 + 3: four full adders, least significant on the
# right. Each waits for the carry from its right-hand neighbour, so the carry ripples leftward
# and the sum bits settle one at a time: 0101 + 0011 = 1000. t=0: settled.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 300
A, B = [0, 1, 0, 1], [0, 0, 1, 1]          # bit 3 .. bit 0
CX = [70, 160, 250, 340]                   # column centres, bit 3 .. bit 0
# the arithmetic, bit 0 first
carry, sums, couts = 0, [0] * 4, [0] * 4
for j in range(3, -1, -1):
    s = A[j] + B[j] + carry
    sums[j], carry = s % 2, s // 2
    couts[j] = carry
assert sums == [1, 0, 0, 0]
T = Timeline(6, shift=5.0)
t_bit = lambda j: 0.6 + (3 - j) * 0.8      # when column j settles
def on_from(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (5.8, 1.0), (5.801, 0.0), (5.999, 0.0)])
def off_from(t0):
    return T.anim('opacity', [(0.0, 1.0), (t0 - 0.001, 1.0), (t0, 0.0), (5.8, 0.0), (5.801, 1.0), (5.999, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-21 svgd-part1-21">')
a('<title id="svgt-part1-21">Fig 2.5 · Adding 5 + 3 in binary · a ripple-carry adder</title>')
a('<desc id="svgd-part1-21">Four full adders side by side, the least significant bit on the right. A is 0101 (5), B is 0011 (3). '
  'Bit 0: 1 + 1 gives 0, carry 1. Bit 1: 0 + 1 + carry gives 0, carry 1. Bit 2: 1 + 0 + carry gives 0, carry 1. Bit 3: 0 + 0 + carry gives 1. The sum is 1000, which is 8.</desc>')
a(text(20, 42, 'A', size=15, fill='rgba(255,255,255,0.8)')); a(text(380, 42, '5', anchor='end', size=16, fill=BLUE))
a(text(20, 74, 'B', size=15, fill='rgba(255,255,255,0.8)')); a(text(380, 74, '3', anchor='end', size=16, fill=BLUE))
for j in range(4):
    x = CX[j]
    a(f'<text x="{x - 12}" y="42" text-anchor="middle" {MONO} font-size="20" fill="#fff">{A[j]}</text>')
    a(f'<text x="{x + 12}" y="74" text-anchor="middle" {MONO} font-size="20" fill="#fff">{B[j]}</text>')
    a(f'<path d="M {x - 12} 50 V 116 M {x + 12} 82 V 116" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>')
    a(f'<rect x="{x - 32}" y="116" width="64" height="60" rx="6" fill="#1a1a1a" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    a(f'<text x="{x}" y="154" text-anchor="middle" {MONO} font-size="22" fill="rgba(255,255,255,0.75)">+</text>')
    a(f'<rect x="{x - 32}" y="116" width="64" height="60" rx="6" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t_bit(j) - 0.4, 0.0), (t_bit(j) - 0.3, 1.0), (t_bit(j) + 0.2, 1.0), (t_bit(j) + 0.3, 0.0), (5.999, 0.0)])}</rect>')
    a(f'<path d="M {x} 176 V 212" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>')
    a(f'<text x="{x}" y="238" text-anchor="middle" {MONO} font-size="22" fill="rgba(255,255,255,0.25)">?{off_from(t_bit(j))}</text>')
    a(f'<text x="{x}" y="238" text-anchor="middle" {MONO} font-size="22" fill="{GOLD if sums[j] else "#fff"}" opacity="0">{sums[j]}{on_from(t_bit(j))}</text>')
    # the carry out to the left-hand neighbour
    if j > 0:
        x0, x1 = x - 32, CX[j - 1] + 32
        col = GOLD if couts[j] else 'rgba(255,255,255,0.35)'
        a(f'<path d="M {x0} 146 H {x1 + 6}" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>'
          f'<polygon points="{x1 + 6},140 {x1},146 {x1 + 6},152" fill="rgba(255,255,255,0.3)"/>')
        a(f'<g opacity="0">{on_from(t_bit(j))}<path d="M {x0} 146 H {x1 + 6}" stroke="{col}" stroke-width="2.6"/>'
          f'<polygon points="{x1 + 6},140 {x1},146 {x1 + 6},152" fill="{col}"/>'
          f'<text x="{(x0 + x1) / 2}" y="134" text-anchor="middle" {MONO} font-size="14" fill="{col}">{couts[j]}</text></g>')
a(text(20, 238, 'SUM', size=14, fill=MUTED))
a(f'<text x="380" y="238" text-anchor="end" {MONO} font-size="16" fill="{GOLD}" opacity="0">8{on_from(t_bit(0))}</text>')
a(text(200, 278, 'carries ripple right to left', anchor='middle', size=14, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('Adding 5 + 3: four full adders, one per bit, the least significant on the right. Each must wait for the carry from its neighbour, so the carry ripples left and the answer, 1000, settles one bit at a time.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A full adder.</b> Adds two bits and a carry-in, and gives one sum bit and a carry-out (Fig 2.6 opens one).</li>
          <li><b>The ripple.</b> Bit 0: 1 + 1 = 0, carry 1. Bits 1 and 2: the carry makes 0 again, carry 1. Bit 3: the carry alone gives 1.</li>
          <li><b>Wider numbers.</b> A 64-bit add is 64 of these in a row. Real CPUs use carry-lookahead designs so they need not wait for the ripple.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-5">
      <div class="diagram-label">Fig 2.5 · Adding 5 + 3 in binary · a ripple-carry adder</div>
      {svg}
      <p id="ch2-arithmetic-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-5', 'ch2-arithmetic-p8', card)
