# Fig 14.6 · ECB's famous failure · structure leaks through (Pass 28, law 3, conceptual pass: why modes matter). Strongroom
# dossier plate. A 32 × 24 image of a padlock in which each square is one 16-byte block. It is encrypted for real with
# AES-128 (openssl, checked against the FIPS 197 example) in ECB and in CBC mode; each cipher block is drawn as a shade
# of its first byte. ECB turns each equal block into the same cipher block, so the padlock survives; CBC mixes in
# the block before, and it does not. The results are revealed block row by block row; the fourth cell zooms on two
# equal plaintext blocks and what each mode makes of them. t=0 (shift): both encryptions shown.
import base64, io, subprocess
from PIL import Image
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

KEY, IV = '2b7e151628aed2a6abf7158809cf4f3c', '000102030405060708090a0b0c0d0e0f'
def aes(mode, data, key=KEY):
    args = ['openssl', 'enc', f'-aes-128-{mode}', '-K', key, '-nopad'] + (['-iv', IV] if mode == 'cbc' else [])
    return subprocess.run(args, input=data, capture_output=True, check=True).stdout
assert aes('ecb', bytes.fromhex('00112233445566778899aabbccddeeff'), '000102030405060708090a0b0c0d0e0f').hex() == '69c4e0d86a7b0430d8cdb78070b4c55a'
# the padlock
WP, HP = 32, 24
BG, FG = 0x30, 0xE0
px = [[BG] * WP for _ in range(HP)]
for y in range(HP):
    for x in range(WP):
        if 3 <= y <= 10 and (8 <= x <= 10 or 21 <= x <= 23):
            px[y][x] = FG                                   # shackle posts
        if 1 <= y <= 3 and 9 <= x <= 22 and not (y == 1 and x in (9, 22)):
            px[y][x] = FG                                   # shackle arch
        if 10 <= y <= 21 and 4 <= x <= 27:
            px[y][x] = FG                                   # body
        if (14 <= y <= 16 and 14 <= x <= 17) or (17 <= y <= 19 and 15 <= x <= 16):
            px[y][x] = BG                                   # keyhole
plain = bytes(v for row in px for v in row for _ in range(16))   # each square is one 16-byte block
ECB, CBC = aes('ecb', plain), aes('cbc', plain)
blocks = lambda b: [b[i:i + 16] for i in range(0, len(b), 16)]
PB, EB, CB = blocks(plain), blocks(ECB), blocks(CBC)
assert len(PB) == WP * HP and PB[0] == PB[1] and EB[0] == EB[1] and CB[0] != CB[1]
assert len(set(EB)) == len(set(PB)) == 2 and len(set(CB)) == WP * HP
assert abs(EB[0][0] - EB[[i for i, b in enumerate(PB) if b[0] == FG][0]][0]) > 60   # the two ECB shades are far enough apart to see
def shade(v):
    lo, hi = (0x24, 0x1e, 0x1a), (0xe6, 0xd9, 0xbd)
    return tuple(round(lo[i] + (hi[i] - lo[i]) * v / 255) for i in range(3))
def png(data):
    im = Image.new('RGB', (WP, HP))
    im.putdata([shade(b[0]) for b in blocks(data)])          # one square per block, shaded by its first byte
    buf = io.BytesIO(); im.save(buf, format='PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
TE0, TE1, TC0, TC1 = 0.8, 3.6, 4.4, 7.2
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
o = []; a = o.append
IW, IH = 172, 129
CX = (20, 208)
RY = (30, 206)
cells = [(CX[0], RY[0], 'plaintext', PARCH), (CX[1], RY[0], 'AES-128, ECB', SEAL), (CX[1], RY[1], 'AES-128, CBC', SAGE)]
imgs = {'plaintext': png(plain), 'AES-128, ECB': png(ECB), 'AES-128, CBC': png(CBC)}
for x, y, lab, col in cells:
    a(text(x, y - 10, lab, size=13, fill=col, ls='0'))
    a(f'<rect x="{x - 1}" y="{y - 1}" width="{IW + 2}" height="{IH + 2}" fill="none" stroke="{PMUTED}" stroke-opacity="0.5"/>')
for (x, y, lab, col), (t0, t1), cid in ((cells[1], (TE0, TE1), 'e'), (cells[2], (TC0, TC1), 'c')):
    hh = T.anim('height', [(0.0, IH), (0.3, IH), (0.305, 0.0), (t0, 0.0), (t1, IH), (D, IH)])
    a(f'<defs><clipPath id="clip-fig-14-6-{cid}"><rect class="fx" x="{x}" y="{y}" width="{IW}" height="{IH}">{hh}</rect></clipPath></defs>')
    a(f'<g clip-path="url(#clip-fig-14-6-{cid})"><image x="{x}" y="{y}" width="{IW}" height="{IH}" href="{imgs[lab]}" style="image-rendering: pixelated" preserveAspectRatio="none"/></g>')
    # the block row being encrypted
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t1, IH), (D, IH)], 'y')
    a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1, 1.0), (t1 + 0.01, 0.0), (D, 0.0)])}<g>{mv}<rect x="{x}" y="{y - 1}" width="{IW}" height="2" fill="{BRASS}"/></g></g>')
a(f'<image x="{CX[0]}" y="{RY[0]}" width="{IW}" height="{IH}" href="{imgs["plaintext"]}" style="image-rendering: pixelated" preserveAspectRatio="none"/>')
# the zoom: two equal plaintext blocks (the top row's two background blocks)
ZX, ZY = CX[0], RY[1]
a(text(ZX, ZY - 10, 'two blocks, close up', size=13, fill=BRASS, ls='0'))
SW = 3.6
for r, (lab, bl, col, t0) in enumerate((('plain: equal', PB, PARCH, 0.31), ('ECB: still equal', EB, SEAL, TE0), ('CBC: different', CB, SAGE, TC0))):
    y = ZY + r * 46
    body = text(ZX, y + 12, lab, size=13, fill=col, ls='0')
    for j in range(2):
        x0 = ZX + j * (16 * SW + 6)
        body += ''.join(f'<rect x="{x0 + i * SW:.1f}" y="{y + 18}" width="{SW:.1f}" height="18" fill="#{"".join(f"{c:02x}" for c in shade(v))}"/>' for i, v in enumerate(bl[j]))
        body += f'<rect x="{x0}" y="{y + 18}" width="{16 * SW:.1f}" height="18" fill="none" stroke="{col}" stroke-opacity="0.8"/>'
    a(body if r == 0 else f'<g opacity="0">{win(t0)}{body}</g>')
H = RY[1] + IH + 8
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-19 svgd-part4-19">')
o.insert(1, '<title id="svgt-part4-19">Fig 14.6 · ECB\'s famous failure · structure leaks through</title>')
o.insert(2, '<desc id="svgd-part4-19">A small picture of a padlock, in which each square is one sixteen-byte AES block, is encrypted with AES-128 twice and each ciphertext block drawn as a shade. '
  'In ECB mode every block is encrypted on its own, so equal blocks of background and of the lock\'s body give equal ciphertext and the padlock is still plain to see. In CBC mode each block is first mixed with the ciphertext before it, and the result is uniform noise. '
  'A close-up of two equal plaintext blocks shows ECB turning them into two identical blocks and CBC into two different ones.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('In ECB mode every 16-byte block is encrypted on its own, so equal plaintext blocks come out as equal ciphertext and the padlock is still there to see. <span class="key-term">CBC</span> mixes each block with the ciphertext before it, and the same picture becomes noise: AES is sound, but the mode decides what leaks.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Real encryption.</b> Each square is one 16-byte block, and both images are the actual AES-128 output, each block shaded by its first byte: ECB gives exactly two shades, CBC 768 different blocks.</li>
          <li><b>What to use.</b> <span class="key-term">GCM</span>: counter mode (<span class="key-term">CTR</span>, AES encrypting a running counter) for secrecy, plus an authentication tag that detects tampering, which CBC alone does not.</li>
          <li><b>The famous one.</b> The same experiment on Tux, the Linux penguin, has illustrated this since 2004.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-6">
      <div class="diagram-label">Fig 14.6 · ECB's famous failure · structure leaks through</div>
      {svg}
      <p id="ch14-symmetric-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-14-6', 'ch14-symmetric-p5', card)
