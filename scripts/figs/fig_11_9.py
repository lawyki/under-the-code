# Fig 11.9 · SHA-256 avalanche · one bit changed, all 256 bits scrambled (Pass 28, law 3). Chart Room plate.
# Two inputs one bit apart: "...lazy dog" and "...lazy doe" ('g' 01100111, 'e' 01100101). Their SHA-256 hashes,
# computed here, in hex; below, the 256 bits as a 16 x 16 grid that shows dog's hash, then doe's, then only the
# bits that differ (124 of 256). t=0 (shift): the difference grid and the count.
import hashlib
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

LOSS = '#ec8d8d'
A, B = 'The quick brown fox jumps over the lazy dog', 'The quick brown fox jumps over the lazy doe'
HA, HB = hashlib.sha256(A.encode()).hexdigest(), hashlib.sha256(B.encode()).hexdigest()
assert HA == 'd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592'
assert bin(ord('g') ^ ord('e')).count('1') == 1
bits = lambda h: [int(c) for c in bin(int(h, 16))[2:].zfill(256)]
BA, BB = bits(HA), bits(HB)
DIFF = [x ^ y for x, y in zip(BA, BB)]
ND = sum(DIFF)
assert ND == 124
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
PH = [(0.4, 3.4), (3.4, 6.4), (6.4, None)]       # dog's bits, doe's bits, the difference
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
def hexlines(y, h):
    a(text(20, y, ' '.join(h[i:i + 8] for i in range(0, 32, 8)), anchor='start', size=13, fill=CMUTED, ls='0'))
    a(text(20, y + 17, ' '.join(h[i:i + 8] for i in range(32, 64, 8)), anchor='start', size=13, fill=CMUTED, ls='0'))
a(text(20, 24, f'"{A[:-1]}<tspan fill="{CYAN}">g</tspan>"', anchor='start', size=13, fill=CSOFT, ls='0'))
hexlines(44, HA)
a(text(20, 92, f'"{B[:-1]}<tspan fill="{ROUTE}">e</tspan>"', anchor='start', size=13, fill=CSOFT, ls='0'))
hexlines(112, HB)
# the grid
GX, GY, C = 20, 152, 13
def grid(bitsv, col, timing):
    cells = ''.join(f'<rect x="{GX + (i % 16) * C}" y="{GY + (i // 16) * C}" width="{C - 2}" height="{C - 2}" rx="1.5" fill="{col}"/>' for i, b in enumerate(bitsv) if b)
    a(f'<g opacity="0">{timing}{cells}</g>')
a(f'<rect x="{GX - 3}" y="{GY - 3}" width="{16 * C + 4}" height="{16 * C + 4}" rx="3" fill="none" stroke="{CMUTED}" stroke-opacity="0.5"/>')
a(''.join(f'<rect x="{GX + (i % 16) * C}" y="{GY + (i // 16) * C}" width="{C - 2}" height="{C - 2}" rx="1.5" fill="#fff" fill-opacity="0.06"/>' for i in range(256)))
grid(BA, CYAN, lit(*PH[0]))
grid(BB, ROUTE, lit(*PH[1]))
grid(DIFF, LOSS, win(PH[2][0]))
# what the grid is showing
LX = GX + 16 * C + 16
for (t0, t1), l1, l2, col in ((PH[0], 'bits of', 'dog\'s hash', CYAN), (PH[1], 'bits of', 'doe\'s hash', ROUTE)):
    a(f'<g class="fx" opacity="0">{lit(t0, t1)}{text(LX, GY + 14, l1, anchor="start", size=13, fill=CSOFT, ls="0")}{text(LX, GY + 31, l2, anchor="start", size=13, fill=col, ls="0")}</g>')
a(f'<g class="fx" opacity="0">{win(PH[2][0])}{text(LX, GY + 14, "bits that", anchor="start", size=13, fill=CSOFT, ls="0")}'
  f'{text(LX, GY + 31, "differ:", anchor="start", size=13, fill=CSOFT, ls="0")}{text(LX, GY + 58, f"{ND} of 256", anchor="start", size=16, fill=LOSS, ls="0")}</g>')
H = GY + 16 * C + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-48 svgd-part3-48">')
o.insert(1, '<title id="svgt-part3-48">Fig 11.9 · SHA-256 avalanche · one bit changed, all 256 bits scrambled</title>')
o.insert(2, f'<desc id="svgd-part3-48">Two sentences one bit apart, ending lazy dog and lazy doe, and their SHA-256 hashes: {HA} and {HB}. '
  f'A 16 by 16 grid shows the 256 bits of the first hash, then of the second, then only the bits that differ: {ND} of 256, scattered with no pattern.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Change one bit of the input (<code>g</code> is 01100111, <code>e</code> is 01100101) and about half of SHA-256\'s 256 output bits flip, here 124, in no visible pattern. '
           'That is what makes a hash a fingerprint: any change at all, however small, gives a completely different one.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The grid.</b> The 256 bits of each hash, 16 to a row, a filled square for each 1: first dog's hash, then doe's, then only the squares where they differ.</li>
          <li><b>Why it matters.</b> Publish a file's hash and anyone can re-hash the download and compare; one changed bit anywhere gives a different hash. Git's commit IDs (still SHA-1 by default), Bitcoin's proof of work and Merkle trees rest on the same property.</li>
          <li><b>What it is not.</b> A hash is not encryption: there is no key and nothing to decrypt. The input cannot be worked back from the output, only checked against a guess.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-9">
      <div class="diagram-label">Fig 11.9 · SHA-256 avalanche · one bit changed, all 256 bits scrambled</div>
      {svg}
      <p id="ch11-crypto-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(HB, ND)
    splice('part-3', 'fig-11-9', 'ch11-crypto-p5', card)
