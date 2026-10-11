# Fig 14.4 · Password storage · plaintext to hash to salted hash to slow KDF (Pass 28, law 3, conceptual pass: the
# defence). Strongroom dossier plate. One table, two users with the same password p4ssw0rd, stored four ways in turn:
# as the password; as SHA-256 (the two rows identical, real digests computed below); salted per user (the rows differ);
# with argon2id at RFC 9106's second recommended setting (64 MiB, 3 passes, 4 lanes). Under the table, what a stolen copy
# gives away at each step. A tab marker steps through the four eras. t=0 (shift): argon2id.
import hashlib
from argon2.low_level import hash_secret, Type
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

PW = 'p4ssw0rd'
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
H0 = sha(PW)[:12]
HA, HB = sha('7f3a:' + PW)[:8], sha('c2e9:' + PW)[:8]
assert (H0, HA, HB) == ('48d2a5bbcf42', '24a8b7da', '57bea797')
# argon2id, RFC 9106's second recommended setting, real digests with per-user salts: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
A2 = [hash_secret(PW.encode(), salt, time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, type=Type.ID).decode().split('$') for salt in (b'7f3a-alice-salt!', b'c2e9-bob-salt!!!')]
A2A, A2B = ('argon2id · ' + x[4][:6] + ' · ' + x[5][:8] + '…' for x in A2)
assert A2A != A2B and A2[0][3] == 'm=65536,t=3,p=4'
ERAS = [('plain', (PW, PW), 'shows the passwords', SEAL),
        ('hash', (H0 + '…', H0 + '…'), 'shows who shares a password', SEAL),
        ('salt', ('7f3a · ' + HA + '…', 'c2e9 · ' + HB + '…'), 'must be guessed row by row', BRASS),
        ('slow', (A2A, A2B), 'row by row, 64 MiB per guess', SAGE)]
W = 400
D = 11.0
T = Timeline(D, shift=10.4)
TE = [0.6 + 2.5 * k for k in range(4)]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
def era(k, body):
    t1 = TE[k + 1] if k + 1 < 4 else None
    vis = win(TE[k]) if t1 is None else (first(t1) if k == 0 else lit(TE[k], t1))
    # era 0 also shows at the very start; the last era is the still
    if k == 0: vis = T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (TE[1] - 0.008, 1.0), (TE[1] - 0.005, 0.0), (D, 0.0)])
    a(f'<g opacity="0">{vis}{body}</g>')
o = []; a = o.append
# the tabs, and a marker that steps across them
TW = 84
tx = lambda k: 20 + k * (TW + 8)
for k, (name, _, _, col) in enumerate(ERAS):
    a(f'<rect x="{tx(k)}" y="12" width="{TW}" height="30" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
    a(text(tx(k) + TW / 2, 32, name, anchor='middle', size=13, fill=PSOFT, ls='0'))
pts = [(0.0, tx(3) - tx(0)), (0.3, tx(3) - tx(0)), (0.305, 0.0)]
for k in range(1, 4):
    pts += [(TE[k] - 0.25, tx(k - 1) - tx(0)), (TE[k], tx(k) - tx(0))]
pts += [(D, tx(3) - tx(0))]
a(f'<g>{T.translate(pts, "x")}<rect x="{tx(0) - 2}" y="10" width="{TW + 4}" height="34" rx="3" fill="none" stroke="{BRASS}" stroke-width="2.5"/></g>')
# the table
TY = 62
a(f'<rect x="20" y="{TY}" width="360" height="104" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.6"/>')
a(text(32, TY + 22, 'user', size=13, fill=PMUTED, ls='0'))
a(text(100, TY + 22, 'stored', size=13, fill=PMUTED, ls='0'))
a(f'<line x1="20" y1="{TY + 32}" x2="380" y2="{TY + 32}" stroke="{PMUTED}" stroke-opacity="0.4"/>')
for r, user in enumerate(('alice', 'bob')):
    a(text(32, TY + 56 + r * 30, user, size=13, fill=PARCH, ls='0'))
for k, (name, (va, vb), leak, col) in enumerate(ERAS):
    body = text(100, TY + 56, va, size=13, fill=col if k < 2 else PARCH, ls='0') + text(100, TY + 86, vb, size=13, fill=col if k < 2 else PARCH, ls='0')
    era(k, body)
for k in range(1, 4):
    a(f'<g class="fx" opacity="0">{pulse(TE[k])}<rect x="94" y="{TY + 38}" width="282" height="60" rx="2" fill="none" stroke="{ERAS[k][3]}" stroke-width="2"/></g>')
# what a stolen copy gives away
LY = TY + 134
a(text(20, LY, 'a stolen copy:', size=13, fill=PMUTED, ls='0'))
for k, (_, _, leak, col) in enumerate(ERAS):
    era(k, text(20, LY + 22, leak, size=13, fill=col, ls='0'))
H = LY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-17 svgd-part4-17">')
o.insert(1, '<title id="svgt-part4-17">Fig 14.4 · Password storage · plaintext to hash to salted hash to slow KDF</title>')
o.insert(2, f'<desc id="svgd-part4-17">A table with two users, alice and bob, who chose the same password, p4ssw0rd, stored four ways in turn. As plain text, a stolen copy gives away the passwords themselves. '
  f'As a SHA-256 hash, both rows read {H0}…, so equal rows give away equal passwords. Salted per user, with salts 7f3a and c2e9, the rows differ, {HA}… and {HB}…, so each must be guessed alone. '
  'With argon2id at 64 MiB of memory and 3 passes, the rows still differ by salt and every single guess also costs 64 MiB.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Stored well, a stolen password table gives away as little as possible: a hash hides the password, a per-user salt makes equal passwords look different, and a slow, memory-hard function makes every guess expensive. '
           'Each step closes the gap the one before it left open.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Lookup tables.</b> Without a salt, one precomputed table of common passwords' hashes serves every stolen database at once; LinkedIn's 2012 leak was unsalted SHA-1.</li>
          <li><b>Tuning.</b> argon2id's memory, passes and lanes are set so one login takes a fraction of a second on the server; OWASP's minimum is 19 MiB with 2 passes.</li>
          <li><b>Older choices.</b> bcrypt (1999) and scrypt (2009) remain acceptable; argon2 won the Password Hashing Competition in 2015.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-4">
      <div class="diagram-label">Fig 14.4 · Password storage · plaintext to hash to salted hash to slow KDF</div>
      {svg}
      <p id="ch14-hashing-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-14-4', 'ch14-hashing-p5', card)
