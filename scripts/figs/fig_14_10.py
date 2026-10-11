# Fig 14.10 · Equivalent security · ECC keys are dramatically smaller (Pass 28, law 3). Strongroom dossier plate. Key
# lengths for the same security strength (NIST SP 800-57 Part 1, Table 2): RSA/DH 1024, 2048, 3072, 7680, 15360
# against ECC 160, 224, 256, 384, 512 for 80, 112, 128, 192, 256 bits of strength. One linear scale, so the
# elliptic-curve bars stay slivers. Each row's bars grow in turn. t=0 (shift): all grown.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

ROWS = [(80, 1024, 160, 'retired'), (112, 2048, 224, ''), (128, 3072, 256, 'today'), (192, 7680, 384, ''), (256, 15360, 512, '')]
W = 400
BX, BMAX = 74, 258                                 # bar origin, width of 15360 bits
bw = lambda bits: max(2.0, bits / 15360 * BMAX)
R0, RS = 56, 48
D = 10.0
T = Timeline(D, shift=9.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
grow = lambda t0, w: T.anim('width', [(0.0, w), (0.3, w), (0.305, 0.0), (t0, 0.0), (t0 + 0.6, w), (D, w)])
o = []; a = o.append
a(f'<rect x="{BX}" y="12" width="14" height="10" fill="{OXBLOOD}"/>' + text(BX + 20, 22, 'RSA, DH', anchor='start', size=13, fill=PSOFT, ls='0'))
a(f'<rect x="{BX + 110}" y="12" width="14" height="10" fill="{SAGE}"/>' + text(BX + 130, 22, 'elliptic curve', anchor='start', size=13, fill=PSOFT, ls='0'))
a(text(10, 44, 'strength', anchor='start', size=13, fill=PMUTED, ls='0'))
for k, (lvl, rsa, ecc, note) in enumerate(ROWS):
    y = R0 + k * RS
    t0 = 0.8 + 1.1 * k
    a(text(10, y + 18, str(lvl), anchor='start', size=13, fill=SEAL, ls='0'))
    if note:
        a(text(10, y + 34, note, anchor='start', size=13, fill=PMUTED, ls='0'))
    for j, (bits, col) in enumerate(((rsa, OXBLOOD), (ecc, SAGE))):
        yy = y + 6 + j * 18
        w = bw(bits)
        a(f'<rect x="{BX}" y="{yy}" width="{w:.1f}" height="13" rx="1.5" fill="{col}">{grow(t0 + 0.2 * j, w)}</rect>')
        lab = text(BX + w + 6, yy + 12, f'{bits:,}', anchor='start', size=13, fill=col, ls='0') if BX + w + 6 + len(f'{bits:,}') * 7.8 < 396 else \
            text(BX + w - 6, yy + 12, f'{bits:,}', anchor='end', size=13, fill=DCARD, ls='0')
        a(f'<g opacity="0">{win(t0 + 0.6 + 0.2 * j)}{lab}</g>')
a(text(BX + BMAX, R0 + 5 * RS + 6, 'key length, bits', anchor='end', size=13, fill=PMUTED, ls='0'))
H = R0 + 5 * RS + 16
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-23 svgd-part4-23">')
o.insert(1, '<title id="svgt-part4-23">Fig 14.10 · Equivalent security · ECC keys are dramatically smaller</title>')
o.insert(2, '<desc id="svgd-part4-23">Key lengths for the same strength, on one scale. At 80 bits of strength, now retired, RSA needs 1024 bits and an elliptic curve 160. At 112, 2048 against 224. At 128, the level in use today, 3072 against 256. At 192, 7680 against 384. At 256, 15,360 against 512.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('For the same strength an elliptic-curve key is a sliver of an RSA key: 256 bits against 3,072 at the 128-bit level the web uses today, 512 against 15,360 at the top. '
           'Smaller keys mean shorter handshakes and far cheaper private-key operations, which is why TLS 1.3 defaults to elliptic curves.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Strength.</b> The bits of work an attacker must spend, matched to the work of breaking a symmetric key of that length; the sizes are NIST's (SP 800-57).</li>
          <li><b>Why RSA grows faster.</b> The best attack on RSA, the number field sieve, is sub-exponential, so each step up in strength needs a far larger modulus; the best known attack on a good curve is a generic square-root search, so twice the bits suffice.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-10">
      <div class="diagram-label">Fig 14.10 · Equivalent security · ECC keys are dramatically smaller</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-10"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-10', cap, card.replace('CAPID', cap))
