# Fig 11.8 · One-way function · easy forward, infeasible backward (Pass 28, law 3). Chart Room plate. The
# textbook RSA toy: 61 × 53 = 3233 in one step. Backward, trial division tries each prime in turn and finds 53
# on the 16th try (every prime up to 53; sqrt(3233) ≈ 56.9). Then the real sizes, bars by digits: 4 (the toy),
# 250 (RSA-250, the largest RSA challenge number factored, February 2020, about 2,700 core-years with the
# General Number Field Sieve) and 617 (a 2048-bit RSA modulus). t=0 (shift): product shown, factor found.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
P, Q, N = 61, 53, 3233
assert P * Q == N
PRIMES = [k for k in range(2, Q + 1) if all(k % d for d in range(2, int(k ** 0.5) + 1))]
assert len(PRIMES) == 16 and PRIMES[-1] == Q and all(N % k for k in PRIMES[:-1])
assert len(str(2 ** 2047)) == 617
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# row A: multiply
a(text(20, 26, 'easy: multiply', anchor='start', size=13, fill=GREEN, ls='0'))
a(text(20, 60, f'{P} × {Q}', anchor='start', size=20, fill=CSOFT, ls='0'))
TF = 0.8
a(f'<g opacity="0">{win(TF)}{text(116, 60, f"= {N}", anchor="start", size=20, fill=GREEN, ls="0")}</g>')
a(f'<g opacity="0">{win(TF)}{text(380, 60, "1 step", anchor="end", size=13, fill=GREEN, ls="0")}</g>')
# row B: factor by trial division
a(text(20, 104, 'hard: factor', anchor='start', size=13, fill=LOSS, ls='0'))
a(text(20, 138, f'{N} ÷', anchor='start', size=20, fill=CSOFT, ls='0'))
T0, STEP = 1.6, 0.26
for i, k in enumerate(PRIMES):
    t0 = T0 + i * STEP
    last = i == len(PRIMES) - 1
    body = text(106, 138, str(k), anchor='start', size=20, fill=GREEN if last else CSOFT, ls='0') + \
        (text(146, 138, f"= {P}", anchor='start', size=20, fill=GREEN, ls='0') if last else text(146, 138, "no", anchor='start', size=20, fill=CMUTED, ls='0')) + \
        text(380, 138, f'{i + 1} {"try" if i == 0 else "tries"}', anchor='end', size=13, fill=GREEN if last else LOSS, ls='0')
    a(f'<g class="fx" opacity="0">{win(t0) if last else lit(t0, t0 + STEP)}{body}</g>')
TD = T0 + 15 * STEP
assert TD + 1.0 < D
# row C: the real sizes, bars by digits
a(text(20, 186, 'at real sizes, digits of the product:', anchor='start', size=13, fill=CSOFT, ls='0'))
BX, BW = 20, 360
ROWS = [(4, 'the toy: 16 tries', CSOFT), (250, 'record, 2020: ~2,700 core-years', ROUTE), (617, 'RSA-2048: out of reach', LOSS)]
for j, (dg, lab, col) in enumerate(ROWS):
    y = 214 + j * 40
    a(text(BX, y, f'{dg}', anchor='start', size=13, fill=col, ls='0'))
    a(text(BX + 40, y, lab, anchor='start', size=13, fill=CSOFT, ls='0'))
    a(f'<rect x="{BX}" y="{y + 7}" width="{max(3.0, dg / 617 * BW):.1f}" height="10" rx="2" fill="{col}" fill-opacity="0.75"/>')
H = 214 + 2 * 40 + 30
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-47 svgd-part3-47">')
o.insert(1, '<title id="svgt-part3-47">Fig 11.8 · One-way function · easy forward, infeasible backward</title>')
o.insert(2, '<desc id="svgd-part3-47">Forward: 61 times 53 equals 3233, in one step. Backward: to factor 3233 by trial division, divide by 2, 3, 5, 7 and each prime in turn; 53 divides it, on the 16th try, giving 61. '
  'Below, the sizes that matter, in digits of the product: 4 for the toy; 250 for the largest RSA challenge number ever factored, in 2020, at about 2,700 core-years; 617 for a 2048-bit RSA key.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Multiplying two primes is one step; getting them back from the product is a search. '
           'For 3233 it takes 16 tries; the largest such number ever factored had 250 digits and took about 2,700 core-years, and a 2048-bit RSA key has 617.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The toy.</b> 61 × 53 = 3233 is the textbook RSA example. Trial division tries each prime up to √3233 ≈ 57 and finds 53 on the 16th.</li>
          <li><b>The record.</b> RSA-250 (829 bits) was factored in February 2020 with the General Number Field Sieve, about 2,700 core-years of computing. Each extra digit makes the job harder; 617 digits is far beyond any known classical method.</li>
          <li><b>Why it matters.</b> The product goes into the <em>public key</em>; the <em>private key</em> is computed from the primes. Shor's algorithm (1994) would factor quickly on a large enough quantum computer, which is why post-quantum cryptography is being deployed.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-8">
      <div class="diagram-label">Fig 11.8 · One-way function · easy forward, infeasible backward</div>
      {svg}
      <p id="ch11-crypto-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-8', 'ch11-crypto-p3', card)
