# Fig 14.2 · The four one-way functions cryptography is built on (Pass 28, law 3). Strongroom dossier plate. Four
# rows, each a tiny real instance, quick forwards and infeasible backwards at real sizes: SHA-256("abc"); 5^6 mod 23
# = 8 (discrete log); 61 × 53 = 3233 (factoring); k·G = Q on an elliptic curve. The forward line stamps "easy", the
# backward line waits on "hard"; then the quantum verdict lands: Shor breaks the last three, Grover only halves the
# hash's bits. t=0 (shift): every verdict shown.
import hashlib
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

H_ABC = hashlib.sha256(b'abc').hexdigest()
assert H_ABC.startswith('ba7816bf') and pow(5, 6, 23) == 8 and [x for x in range(1, 23) if pow(5, x, 23) == 8] == [6] and 61 * 53 == 3233
ROWS = [('hash', f'SHA-256("abc") = {H_ABC[:8]}…', f'{H_ABC[:8]}… = SHA-256( ? )', 'Grover: half the bits', SAGE),
        ('discrete log', '5⁶ mod 23 = 8', '5ˣ mod 23 = 8 → x = ?', 'Shor breaks it', STAMP),
        ('factoring', '61 × 53 = 3233', '3233 = ? × ?', 'Shor breaks it', STAMP),
        ('elliptic curve', 'k · G = Q', 'Q, G → k = ?', 'Shor breaks it', STAMP)]
W = 400
R0, RS = 22, 84
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
TQ = 7.6                                           # the quantum verdicts
o = []; a = o.append
for r, (name, fwd, back, q, qcol) in enumerate(ROWS):
    y = R0 + r * RS
    t0 = 0.8 + 1.5 * r
    a(text(10, y, f'{r + 1} · {name}', anchor='start', size=13, fill=SEAL, ls='0'))
    # forward: easy
    a(text(26, y + 22, fwd, anchor='start', size=13, fill=PSOFT, ls='0'))
    tag = text(390, y + 22, 'easy', anchor='end', size=13, fill=SAGE, ls='0')
    a(f'<g opacity="0">{win(t0)}{tag}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="{390 - 44}" y="{y + 8}" width="46" height="20" rx="3" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
    # backward: hard, and the quantum verdict
    a(text(26, y + 42, back, anchor='start', size=13, fill=PMUTED, ls='0'))
    hard = text(390, y + 42, 'hard', anchor='end', size=13, fill=OXBLOOD, ls='0')
    a(f'<g opacity="0">{win(t0 + 0.6)}{hard}</g>')
    qt = text(390, y + 60, q, anchor='end', size=13, fill=qcol, ls='0')
    a(f'<g opacity="0">{win(TQ + 0.4 * r)}{qt}</g>')
    a(f'<g class="fx" opacity="0">{stamp(TQ + 0.4 * r)}<rect x="{390 - len(q) * 7.8 - 8}" y="{y + 46}" width="{len(q) * 7.8 + 10}" height="20" rx="3" fill="none" stroke="{qcol}" stroke-width="2"/></g>')
    if r < 3:
        a(f'<line x1="10" y1="{y + RS - 12}" x2="390" y2="{y + RS - 12}" stroke="{PMUTED}" stroke-opacity="0.2"/>')
H = R0 + 3 * RS + 72
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-15 svgd-part4-15">')
o.insert(1, '<title id="svgt-part4-15">Fig 14.2 · The four one-way functions cryptography is built on</title>')
o.insert(2, f'<desc id="svgd-part4-15">Four one-way functions, each easy forwards and hard backwards. A hash: SHA-256 of abc is {H_ABC[:8]} and so on, but nothing finds an input for a given hash short of trying. A discrete log: 5 to the 6th mod 23 is 8, but finding the exponent from 8 is the hard direction. '
  'Factoring: 61 times 53 is 3233, but splitting 3233 back is the hard direction. An elliptic curve: k times a point G gives Q, but recovering k from Q is hard. A large quantum computer running Shor\'s algorithm breaks the last three; Grover\'s algorithm only halves the hash\'s bits of strength.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every primitive in this chapter rests on a function that is quick one way and infeasible the other: hashing (<span class="key-term">SHA-256</span>), modular powers (<span class="key-term">Diffie–Hellman</span>), multiplying primes, multiplying a point on an elliptic curve. '
           'A large quantum computer running Shor\'s algorithm would undo the last three; hashing would only lose half its bits of strength.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The sizes.</b> Inverting SHA-256 means trying about 2²⁵⁶ inputs; 2048-bit RSA and 3072-bit discrete logs resist every known classical method (the public factoring record is 270 digits, RSA-896, September 2026); a 256-bit elliptic-curve key matches 3072-bit RSA.</li>
          <li><b>Not proven.</b> These are assumptions: nobody has proven that any one-way function exists; these are believed hard because decades of attack have found nothing fast.</li>
          <li><b>After Shor.</b> NIST's 2024 standards replace the last three with lattice problems (ML-KEM, ML-DSA) and hash-based signatures (SLH-DSA).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-2">
      <div class="diagram-label">Fig 14.2 · The four one-way functions cryptography is built on</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-2"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-2', cap, card.replace('CAPID', cap))
