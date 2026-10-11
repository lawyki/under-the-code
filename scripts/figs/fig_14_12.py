# Fig 14.12 · Digital signatures and Certificate Transparency · Merkle trees keep CAs honest (Pass 28, law 3).
# Strongroom dossier plate. Top: the CA signs a hash of the certificate with its private key; a browser verifies with
# the public key, the hash and the signature, and gets yes or no. Bottom: a CT log as a Merkle tree of eight
# certificates. Proving c5 is in the log takes its siblings at each level (c4, then the hash of c6 and c7, then the
# hash of c0 to c3): the path is recomputed up to the signed root, which matches. 3 hashes for 8 certificates,
# about 40 for a trillion (log2 1e12 ≈ 39.9). t=0 (shift): the proof complete.
import math
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

assert round(math.log2(1e12)) == 40
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
def staged(body, t0):
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(t0)}{body}</g>')
# signatures
a(text(10, 18, 'signature', anchor='start', size=13, fill=SEAL, ls='0'))
staged(text(10, 40, 'CA:', anchor='start', size=13, fill=PMUTED, ls='0') + text(70, 40, 'sign(private key, hash)', anchor='start', size=13, fill=PSOFT, ls='0'), 0.6)
staged(text(10, 60, 'browser:', anchor='start', size=13, fill=PMUTED, ls='0') + text(90, 60, 'verify(public key, hash, sig)', anchor='start', size=13, fill=PSOFT, ls='0'), 1.4)
staged(text(390, 80, '→ yes', anchor='end', size=13, fill=SAGE, ls='0'), 2.0)
# the CT log, a Merkle tree of eight certificates
a(text(10, 110, 'Certificate Transparency log', anchor='start', size=13, fill=SEAL, ls='0'))
LV = [292, 246, 200, 154]                          # leaves, level 1, level 2, root (y centres)
def xs(level, i):
    n = 8 >> level
    span = 376
    return 12 + span * (i + 0.5) / n
NODE = {}
for lv in range(4):
    for i in range(8 >> lv):
        NODE[(lv, i)] = (xs(lv, i), LV[lv])
for lv in range(1, 4):
    for i in range(8 >> lv):
        px, py = NODE[(lv, i)]
        for c in (2 * i, 2 * i + 1):
            cx, cy = NODE[(lv - 1, c)]
            a(f'<line x1="{px:.1f}" y1="{py + 10}" x2="{cx:.1f}" y2="{cy - 10}" stroke="{PMUTED}" stroke-opacity="0.6"/>')
def nodebox(lv, i, col, fill=None):
    x, y = NODE[(lv, i)]
    w = 40 if lv == 0 else (54 if lv < 3 else 60)
    f = f'fill="{fill}" fill-opacity="0.35"' if fill else f'fill="{DCARD}"'
    lab = f'c{i}' if lv == 0 else ('root' if lv == 3 else '')
    b = f'<rect x="{x - w / 2:.1f}" y="{y - 10}" width="{w}" height="20" rx="3" {f} stroke="{col}" stroke-width="1.5"/>'
    if lab:
        b += text(x, y + 5, lab, anchor='middle', size=13, fill=col if not fill else PARCH, ls='0')
    return b
for (lv, i) in NODE:
    a(nodebox(lv, i, PMUTED))
# the proof for c5: target, siblings, and the recomputed path
TGT, SIB, PATH = (0, 5), [(0, 4), (1, 3), (2, 0)], [(1, 2), (2, 1), (3, 0)]
TT = 3.0
a(f'<g opacity="0">{win(TT)}{nodebox(*TGT, SAGE, SAGE)}</g>')
for k, n in enumerate(SIB):
    a(f'<g opacity="0">{win(TT + 0.8 + 1.0 * k)}{nodebox(*n, BRASS, BRASS)}</g>')
    a(f'<g class="fx" opacity="0">{stamp(TT + 0.8 + 1.0 * k)}<circle cx="{NODE[n][0]:.1f}" cy="{NODE[n][1]}" r="20" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
for k, n in enumerate(PATH):
    a(f'<g opacity="0">{win(TT + 1.3 + 1.0 * k)}{nodebox(*n, SAGE, SAGE)}</g>')
TM = TT + 1.3 + 1.0 * 2 + 0.6
staged(text(390, 132, 'root signed by the log', anchor='end', size=13, fill=PMUTED, ls='0'), 0.6)
SY = LV[0] + 36
a(f'<g opacity="0.25">{text(10, SY, "c5 proved with 3 hashes", anchor="start", size=13, fill=SAGE, ls="0")}</g><g opacity="0">{win(TM)}{text(10, SY, "c5 proved with 3 hashes", anchor="start", size=13, fill=SAGE, ls="0")}</g>')
staged(text(10, SY + 20, 'a trillion certificates: about 40', anchor='start', size=13, fill=PSOFT, ls='0'), TM + 0.6)
legend = (f'<rect x="250" y="{SY - 10}" width="12" height="12" fill="{BRASS}" fill-opacity="0.6"/>' + text(268, SY, 'siblings sent', anchor='start', size=13, fill=PMUTED, ls='0'))
a(legend)
H = SY + 32
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-25 svgd-part4-25">')
o.insert(1, '<title id="svgt-part4-25">Fig 14.12 · Digital signatures and Certificate Transparency · Merkle trees keep CAs honest</title>')
o.insert(2, '<desc id="svgd-part4-25">Top: a certificate authority signs a hash of the certificate with its private key; a browser verifies it with the public key, the hash and the signature, and gets yes. '
  'Bottom: a Certificate Transparency log as a Merkle tree over eight certificates, c0 to c7, whose root the log signs. To prove c5 is in the log, the log sends three hashes, c4, the hash of c6 and c7, and the hash of c0 to c3; hashing upwards from c5 reproduces the root. A trillion certificates would need about 40.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A certificate authority signs each certificate with its private key, and any browser can check the signature with the public key. '
           'Certificate Transparency logs every certificate in a Merkle tree, so proving one is in the log takes only the sibling hashes along its path: three for eight certificates, about forty for a trillion.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Signing.</b> The CA signs a hash of the certificate; verifying takes the public key, the same hash and the signature, and answers yes or no. Only the private key could have made a signature that verifies.</li>
          <li><b>The log.</b> Each leaf is a certificate's hash, each node the hash of its two children, and the log signs the root. A proof for one certificate is its sibling at every level: log₂ N hashes.</li>
          <li><b>Why it exists.</b> In 2011 the breached Dutch CA DigiNotar issued a false certificate for <code>*.google.com</code> that went unnoticed for weeks. Since 2018 Chrome trusts a new certificate only if public logs hold it, so a domain owner can spot one issued in their name.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-12">
      <div class="diagram-label">Fig 14.12 · Digital signatures and Certificate Transparency · Merkle trees keep CAs honest</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-12"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-12', cap, card.replace('CAPID', cap))
