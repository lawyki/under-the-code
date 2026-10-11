# Fig 14.8 · RSA worked through · p=17, q=23 (Pass 28, law 3). Strongroom dossier plate. Key generation (n = 391,
# φ = 352, e = 3, d = 235, all computed and asserted), then the pipeline: 65 locked with the public pair to 143, 143
# unlocked with the private exponent back to 65. Eve holds (3, 391) and must factor 391 to find d. Lock-step: lines
# stamp in order. t=0 (shift): the round trip complete.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

P, Q, E, M = 17, 23, 3, 65
N, PHI = P * Q, (P - 1) * (Q - 1)
Dk = pow(E, -1, PHI)
C = pow(M, E, N)
assert (N, PHI, Dk, C, pow(C, Dk, N)) == (391, 352, 235, 143, 65) and E * Dk == 2 * PHI + 1
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
def staged(body, t0):
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(t0)}{body}</g>')
a(text(10, 18, 'make the keys', anchor='start', size=13, fill=SEAL, ls='0'))
KEYGEN = [(f'p = {P}, q = {Q}', 'two primes, kept secret'), (f'n = p × q = {N}', 'public'), (f'φ = 16 × 22 = {PHI}', 'secret'),
          (f'e = {E}, d = {Dk}', f'{E} × {Dk} = 2 × {PHI} + 1')]
for k, (l, r) in enumerate(KEYGEN):
    y = 42 + 20 * k
    staged(text(10, y, l, anchor='start', size=13, fill=PSOFT, ls='0') + text(390, y, r, anchor='end', size=13, fill=PMUTED, ls='0'), 0.6 + 0.8 * k)
def chip(x, y, s, col, w=None, anchor='middle'):
    w = w or len(s) * 7.8 + 16
    x0 = x - w / 2 if anchor == 'middle' else x
    return (f'<rect x="{x0}" y="{y - 13}" width="{w}" height="26" rx="4" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(x0 + w / 2, y + 5, s, anchor='middle', size=13, fill=col, ls='0'))
KY = 136
staged(chip(10, KY, f'public ({E}, {N})', SAGE, 176, 'start'), 3.8)
staged(chip(214, KY, f'private ({Dk}, {N})', OXBLOOD, 176, 'start'), 3.8)
# use them
a(text(10, 178, 'use them', anchor='start', size=13, fill=SEAL, ls='0'))
PY = 214
staged(chip(30, PY, str(M), PARCH), 4.8)
arrow = lambda x1, x2, col: f'<path d="M{x1},{PY} H{x2} m-6,-4 l6,4 l-6,4" fill="none" stroke="{col}" stroke-width="1.5"/>'
staged(arrow(52, 176, SAGE) + text(114, PY - 12, f'{M}³ mod {N}', anchor='middle', size=13, fill=SAGE, ls='0'), 5.4)
staged(chip(200, PY, str(C), PARCH), 5.8)
staged(arrow(226, 344, OXBLOOD) + text(285, PY - 12, f'{C}²³⁵ mod {N}', anchor='middle', size=13, fill=OXBLOOD, ls='0'), 6.6)
staged(chip(370, PY, str(M), SAGE), 7.0)
a(f'<g class="fx" opacity="0">{stamp(7.0)}<rect x="{370 - 20}" y="{PY - 16}" width="40" height="32" rx="5" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
staged(text(10, PY + 34, 'anyone can lock', anchor='start', size=13, fill=SAGE, ls='0') + text(390, PY + 34, 'only d unlocks', anchor='end', size=13, fill=OXBLOOD, ls='0'), 7.4)
staged(text(10, PY + 64, f'Eve has ({E}, {N}): finding d means factoring {N}', anchor='start', size=13, fill=PMUTED, ls='0'), 8.2)
H = PY + 76
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-21 svgd-part4-21">')
o.insert(1, '<title id="svgt-part4-21">Fig 14.8 · RSA worked through · p=17, q=23</title>')
o.insert(2, '<desc id="svgd-part4-21">RSA with tiny numbers. The primes 17 and 23 give n = 391 and φ = 352; the public exponent is 3 and the private exponent 235, because 3 times 235 is 705, one more than twice 352. '
  'The message 65 is locked with the public pair: 65 cubed mod 391 is 143. Only the private exponent unlocks it: 143 to the 235th mod 391 is 65 again. Eve, holding 3 and 391, would have to factor 391 to find 235.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Key generation multiplies two primes and derives a pair of exponents; anyone can lock 65 into 143 with the public pair (3, 391), and only the private exponent 235 turns 143 back into 65. '
           'Finding 235 from (3, 391) means factoring 391: trivial here, infeasible at 2048 bits.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it works.</b> e × d = 705 = 2 × 352 + 1, so raising to e and then to d is raising to 2φ + 1, which by Euler's theorem gives back m modulo 391.</li>
          <li><b>Real sizes.</b> Primes of about 1024 bits each, a 2048-bit n, and e = 65537. RSA is never used raw as drawn: messages are padded first (OAEP) and so are signatures (PSS).</li>
          <li><b>In TLS 1.3.</b> RSA no longer carries keys; where it appears it only signs, while elliptic-curve Diffie–Hellman agrees the key (Fig 14.11).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-8">
      <div class="diagram-label">Fig 14.8 · RSA worked through · p=17, q=23</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-8"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-8', cap, card.replace('CAPID', cap))
