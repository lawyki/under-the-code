# Fig 14.13 · Post-quantum migration · the algorithms that survive Shor (Pass 28, law 3). Strongroom dossier plate.
# A replacement table: Shor's algorithm strikes today's public-key schemes (X25519/RSA for key exchange, ECDSA/RSA
# for signatures) and NIST's 2024 standards stamp in (ML-KEM, FIPS 203; ML-DSA, FIPS 204; SLH-DSA, FIPS 205, the
# hash-only backup); AES and SHA-256 stay. Then the price, on one scale: a key-exchange share 32 bytes (X25519)
# against 1,184 (ML-KEM-768), a signature 64 bytes (Ed25519) against 3,309 (ML-DSA-65). t=0 (shift): all shown.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

assert 1184 // 32 == 37 and round(3309 / 64) == 52
W = 400
CX = (10, 128, 254)                                # columns: use, today, after Shor
ROWS = [('key exchange', 'X25519, RSA', 'ML-KEM', True), ('signatures', 'ECDSA, RSA', 'ML-DSA', True),
        ('backup sig', 'none', 'SLH-DSA', False), ('symmetric', 'AES, SHA-256', 'keep', False)]
R0, RS = 46, 30
D = 11.0
T = Timeline(D, shift=10.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
grow = lambda t0, w: T.anim('width', [(0.0, w), (0.3, w), (0.305, 0.0), (t0, 0.0), (t0 + 0.6, w), (D, w)])
TSHOR = 1.2
o = []; a = o.append
for x, h in zip(CX, ('use', 'today', 'after Shor')):
    a(text(x, 20, h, anchor='start', size=13, fill=PMUTED, ls='0'))
a(f'<line x1="10" y1="28" x2="390" y2="28" stroke="{PMUTED}" stroke-opacity="0.5"/>')
for k, (use, old, new, broken) in enumerate(ROWS):
    y = R0 + k * RS
    a(text(CX[0], y, use, anchor='start', size=13, fill=PSOFT, ls='0'))
    a(text(CX[1], y, old, anchor='start', size=13, fill=PSOFT if broken or old == 'none' else SAGE, ls='0'))
    if broken:
        w = len(old) * 7.8
        a(f'<g opacity="0">{win(TSHOR + 0.3 * k)}<line x1="{CX[1] - 2}" y1="{y - 4}" x2="{CX[1] + w + 2}" y2="{y - 4}" stroke="{STAMP}" stroke-width="2"/></g>')
    t1 = 2.8 + 0.5 * k
    a(f'<g opacity="0.2">{text(CX[2], y, new, anchor="start", size=13, fill=SAGE, ls="0")}</g><g opacity="0">{win(t1)}{text(CX[2], y, new, anchor="start", size=13, fill=SAGE, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t1)}<rect x="{CX[2] - 4}" y="{y - 15}" width="{len(new) * 7.8 + 8}" height="21" rx="3" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
a(f'<g opacity="0">{win(TSHOR)}{text(390, R0 + 4 * RS - 2, "struck: Shor", anchor="end", size=13, fill=STAMP, ls="0")}</g>')
# the price, on one scale
BY = R0 + 4 * RS + 34
a(text(10, BY, 'the price, in bytes', anchor='start', size=13, fill=SEAL, ls='0'))
BX, BMAX = 10, 300
bw = lambda n: max(2.0, n / 3309 * BMAX)
BARS = [('X25519 share', 32, PSOFT), ('ML-KEM-768 key', 1184, SAGE), ('Ed25519 signature', 64, PSOFT), ('ML-DSA-65 signature', 3309, SAGE)]
for k, (lab, n, col) in enumerate(BARS):
    y = BY + 22 + k * 34
    t0 = 5.4 + 0.5 * k
    a(text(BX, y, lab, anchor='start', size=13, fill=PMUTED, ls='0'))
    w = bw(n)
    a(f'<rect x="{BX}" y="{y + 5}" width="{w:.1f}" height="10" rx="1.5" fill="{col}">{grow(t0, w)}</rect>')
    a(f'<g opacity="0">{win(t0 + 0.6)}{text(BX + w + 6, y + 15, f"{n:,}", anchor="start", size=13, fill=col, ls="0")}</g>')
H = BY + 22 + 3 * 34 + 26
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-26 svgd-part4-26">')
o.insert(1, '<title id="svgt-part4-26">Fig 14.13 · Post-quantum migration · the algorithms that survive Shor</title>')
o.insert(2, '<desc id="svgd-part4-26">What changes after Shor. Key exchange: X25519 and RSA, struck out, are replaced by ML-KEM. Signatures: ECDSA and RSA, struck out, are replaced by ML-DSA, with SLH-DSA, built only on hash functions, as a backup. AES and SHA-256 are kept. '
  'The price in bytes: an X25519 key share is 32 bytes and an ML-KEM-768 key 1,184; an Ed25519 signature is 64 bytes and an ML-DSA-65 signature 3,309.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Shor\'s algorithm would break every public-key scheme in use today, so NIST\'s 2024 standards replace them: ML-KEM for key exchange, ML-DSA for signatures, and SLH-DSA, built only on hashes, as a backup. '
           'The price is size, a key share 37 times larger and signatures more than 50 times larger, and browsers already pair X25519 with ML-KEM.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Harvest now, decrypt later.</b> Traffic recorded today could be decrypted once a large quantum computer exists, which is why key exchange moved first.</li>
          <li><b>Hybrid.</b> Chrome added X25519 plus a draft of Kyber in 2023, turned it on by default in 2024 and switched to X25519MLKEM768 late that year; Apple's iMessage PQ3 shipped in 2024. A hybrid connection stays safe if either half holds.</li>
          <li><b>Symmetric is fine.</b> Grover's algorithm only square-roots a brute-force search, so AES-256 and SHA-256 keep about 128 bits.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-13">
      <div class="diagram-label">Fig 14.13 · Post-quantum migration · the algorithms that survive Shor</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-13"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-13', cap, card.replace('CAPID', cap))
