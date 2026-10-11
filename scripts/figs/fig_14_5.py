# Fig 14.5 · One AES round · four steps on a 4×4 byte grid (Pass 28, law 3). Strongroom dossier plate. Round 1 of the
# worked example in FIPS 197 (Appendix B), computed here: S-box, key schedule, ShiftRows, MixColumns, all asserted
# against the standard's printed values. One 4 × 4 grid (column-major, as AES lays out its state) steps through
# SubBytes, ShiftRows, MixColumns and AddRoundKey; the step's chip lights and the bytes it changes stamp in.
# t=0 (shift): the round done.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

# ---- AES, round 1 of FIPS 197 Appendix B ----
def xt(a): return ((a<<1)^0x1b)&0xff if a&0x80 else a<<1
def mul(a,b):
    r=0
    while b:
        if b&1: r^=a
        a=xt(a); b>>=1
    return r
inv=[0]*256
for a in range(1,256):
    for b in range(1,256):
        if mul(a,b)==1: inv[a]=b; break
def aff(x):
    r=0
    for i in range(8):
        bit=((x>>i)^(x>>((i+4)%8))^(x>>((i+5)%8))^(x>>((i+6)%8))^(x>>((i+7)%8))^(0x63>>i))&1
        r|=bit<<i
    return r
SB=[aff(inv[x]) for x in range(256)]
assert SB[0]==0x63 and SB[0x53]==0xed
inp=bytes.fromhex('3243f6a8885a308d313198a2e0370734'); key=bytes.fromhex('2b7e151628aed2a6abf7158809cf4f3c')
# key expansion
w=[list(key[4*i:4*i+4]) for i in range(4)]
rcon=1
for i in range(4,44):
    t=w[i-1][:]
    if i%4==0:
        t=t[1:]+t[:1]; t=[SB[b] for b in t]; t[0]^=rcon; rcon=xt(rcon)
    w.append([w[i-4][j]^t[j] for j in range(4)])
rk=lambda r: bytes(sum(w[4*r:4*r+4],[]))
st=bytes(a^b for a,b in zip(inp,rk(0)))
sb=bytes(SB[b] for b in st)
# state s[r][c]=b[r+4c]
def shift(b): return bytes(b[((c+r)%4)*4+r] for c in range(4) for r in range(4))
sr=shift(sb)
def mixcol(col):
    a=col; return [mul(a[0],2)^mul(a[1],3)^a[2]^a[3], a[0]^mul(a[1],2)^mul(a[2],3)^a[3], a[0]^a[1]^mul(a[2],2)^mul(a[3],3), mul(a[0],3)^a[1]^a[2]^mul(a[3],2)]
mc=bytes(sum((mixcol(list(sr[4*c:4*c+4])) for c in range(4)),[]))
ark=bytes(a^b for a,b in zip(mc,rk(1)))
assert (st.hex(), sb.hex(), sr.hex(), mc.hex(), rk(1).hex(), ark.hex()) == (
    '193de3bea0f4e22b9ac68d2ae9f84808', 'd42711aee0bf98f1b8b45de51e415230', 'd4bf5d30e0b452aeb84111f11e2798e5',
    '046681e5e0cb199a48f8d37a2806264c', 'a0fafe1788542cb123a339392a6c7605', 'a49c7ff2689f352b6b5bea43026a5049')

# ---- the figure ----
STATES = [st, sb, sr, mc, ark]
STEPS = [('SubBytes', SEAL), ('ShiftRows', BRASS), ('MixColumns', SAGE), ('AddRoundKey', OXBLOOD)]
W = 400
GX, GY, C = 22, 66, 44                              # grid origin, cell size
D = 14.0
T = Timeline(D, shift=13.4)
TS = [0.31, 2.0, 4.8, 7.6, 10.4]                    # each state appears
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
# the step chips
x = 12
for k, (name, col) in enumerate(STEPS):
    w = len(name) * 7.8 + 12
    body = f'<rect x="{x}" y="10" width="{w}" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.5"/>' + text(x + w / 2, 27, name, anchor='middle', size=13, fill=col, ls='0')
    a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(TS[k + 1])}{body}</g>')
    x += w + 6
# the grid: s[r][c] = byte r + 4c
cell = lambda r, c: (GX + c * C, GY + r * C)
for r in range(4):
    for c in range(4):
        cx, cy = cell(r, c)
        a(f'<rect x="{cx}" y="{cy}" width="{C - 4}" height="{C - 4}" rx="3" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
for k, S in enumerate(STATES):
    t0 = TS[k]; t1 = TS[k + 1] if k + 1 < len(STATES) else None
    col = PSOFT if k == 0 else STEPS[k - 1][1]
    cells = ''.join(text(cell(r, c)[0] + (C - 4) / 2, cell(r, c)[1] + 26, f'{S[r + 4 * c]:02x}', anchor='middle', size=13, fill=col, ls='0') for r in range(4) for c in range(4))
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{cells}</g>')
    if k:
        changed = [(r, c) for r in range(4) for c in range(4) if S[r + 4 * c] != STATES[k - 1][r + 4 * c]]
        a(f'<g class="fx" opacity="0">{stamp(t0)}' + ''.join(f'<rect x="{cell(r, c)[0] - 1}" y="{cell(r, c)[1] - 1}" width="{C - 2}" height="{C - 2}" rx="3" fill="none" stroke="{STAMP}" stroke-width="2"/>' for r, c in changed) + '</g>')
# what each step does, beside the grid
NX = GX + 4 * C + 12
NOTES = [('the block, after', 'the first key XOR'), ('each byte swapped', 'through the S-box'), ('row r rotates', 'left by r'), ('each column times', 'a fixed matrix'), ('XOR with the', 'round-1 key')]
for k, (l1, l2) in enumerate(NOTES):
    t0 = TS[k]; t1 = TS[k + 1] if k + 1 < len(STATES) else None
    col = PSOFT if k == 0 else STEPS[k - 1][1]
    body = text(NX, GY + 70, l1, anchor='start', size=13, fill=col, ls='0') + text(NX, GY + 88, l2, anchor='start', size=13, fill=PSOFT, ls='0')
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{body}</g>')
H = GY + 4 * C + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-18 svgd-part4-18">')
o.insert(1, '<title id="svgt-part4-18">Fig 14.5 · One AES round · four steps on a 4×4 byte grid</title>')
o.insert(2, '<desc id="svgd-part4-18">Round 1 of the worked example in the AES standard, as a 4 by 4 grid of bytes. The state 19 3d e3 be, a0 f4 e2 2b, 9a c6 8d 2a, e9 f8 48 08 (by column) goes through SubBytes, each byte swapped through the S-box, giving d4 27 11 ae and so on; '
  'ShiftRows, row r rotated left by r; MixColumns, each column multiplied by a fixed matrix, giving 04 66 81 e5 for the first column; and AddRoundKey, an XOR with the round key, giving a4 9c 7f f2 for the first column.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each AES round runs four steps on a 4 × 4 grid of bytes: each byte is swapped through a fixed table, row r rotates left by r, each column is mixed by a fixed matrix, and the round key is XORed in. '
           'Ten rounds, for a 128-bit key, make every output bit depend on every input and key bit.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The values.</b> Round 1 of the worked example in the AES standard (FIPS 197, Appendix B), computed and checked: the first column goes 19 3d e3 be, then d4 27 11 ae, d4 bf 5d 30, 04 66 81 e5, and a4 9c 7f f2.</li>
          <li><b>What each step adds.</b> SubBytes is the only non-linear step, the source of confusion; ShiftRows and MixColumns spread each byte across the block, diffusion; AddRoundKey brings in the key.</li>
          <li><b>Rounds.</b> 10, 12 or 14 for 128-, 192- and 256-bit keys, the last skipping MixColumns. Rijndael, by Joan Daemen and Vincent Rijmen, won NIST's competition in 2000 and became the standard in 2001.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-5">
      <div class="diagram-label">Fig 14.5 · One AES round · four steps on a 4×4 byte grid</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-5', cap, card.replace('CAPID', cap))
