# Fig 14.1 · Two thousand years of cryptography in one strip (Pass 28, law 3). Strongroom dossier plate. A thin
# axis to scale, 50 BCE to 2030, banded shared-key (to 1976) and public-key (after): the whole public-key era is the
# last sliver. Evenly spaced labels on the right, joined by non-crossing leaders: Caesar (~50 BCE, broken by letter
# frequencies, al-Kindi, 800s), Bellaso's "Vigenère" (1553; Babbage 1854, Kasiski 1863), Enigma (military, 1926; Rejewski 1932,
# Bombe 1940), Diffie–Hellman (1976), RSA (1977), AES (2001), NIST post-quantum (2024). A marker steps event by event.
# t=0 (shift): every event stamped.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
AX, Y0, Y1 = 58, 36, 330                          # axis x, y of 50 BCE, y of 2030
YR0, YR1 = -50, 2030
yy = lambda yr: Y0 + (yr - YR0) / (YR1 - YR0) * (Y1 - Y0)
EV = [(-50, '~50 BCE · Caesar shift', 'broken by letter frequencies', BRASS),
      (1553, '1553 · "Vigenère" (Bellaso)', 'broken: Babbage, Kasiski 1863', BRASS),
      (1926, '1926 · Enigma, German military', 'broken: Rejewski 1932, Bombe 1940', BRASS),
      (1976, '1976 · Diffie–Hellman', 'strangers agree a key in public', SAGE),
      (1977, '1977 · RSA', 'public-key encryption, signatures', SAGE),
      (2001, '2001 · AES', 'the shared-key standard', BRASS),
      (2024, '2024 · NIST post-quantum', 'ML-KEM, ML-DSA (Kyber, Dilithium)', SAGE)]
LX, L0, LS = 100, 50, 42
D = 12.0
T = Timeline(D, shift=11.4)
TE = [0.8 + 1.2 * i for i in range(len(EV))]      # one step per event
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
# legend
a(f'<rect x="{LX}" y="10" width="14" height="10" fill="{BRASS}" fill-opacity="0.8"/>' + text(LX + 20, 20, 'shared key', anchor='start', size=13, fill=PMUTED, ls='0'))
a(f'<rect x="{LX + 128}" y="10" width="14" height="10" fill="{SAGE}" fill-opacity="0.9"/>' + text(LX + 148, 20, 'public key', anchor='start', size=13, fill=PMUTED, ls='0'))
# the axis, banded by era
a(f'<rect x="{AX - 3}" y="{yy(YR0):.1f}" width="6" height="{yy(1976) - yy(YR0):.1f}" fill="{BRASS}" fill-opacity="0.55"/>')
a(f'<rect x="{AX - 3}" y="{yy(1976):.1f}" width="6" height="{yy(YR1) - yy(1976):.1f}" fill="{SAGE}" fill-opacity="0.9"/>')
for yr, lab in ((0, '0'), (1000, '1000'), (2000, '2000')):
    a(f'<line x1="{AX - 9}" y1="{yy(yr):.1f}" x2="{AX - 4}" y2="{yy(yr):.1f}" stroke="{PMUTED}"/>')
    a(text(AX - 22, yy(yr) + 5, lab, anchor='end', size=13, fill=PMUTED, ls='0'))
for i, (yr, l1, l2, col) in enumerate(EV):
    ly = L0 + i * LS
    dy = yy(yr)
    a(f'<path d="M{AX + 5},{dy:.1f} L{LX - 8},{ly - 5}" fill="none" stroke="{col}" stroke-opacity="0.5"/>')
    lab = text(LX, ly, l1, anchor='start', size=13, fill=col, ls='0') + text(LX, ly + 17, l2, anchor='start', size=13, fill=PSOFT, ls='0')
    a(f'<g opacity="0.35">{lab}</g><g opacity="0">{win(TE[i])}{lab}</g>')
    a(f'<g class="fx" opacity="0">{stamp(TE[i])}<rect x="{LX - 6}" y="{ly - 16}" width="{W - LX}" height="40" rx="3" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
# the marker steps from event to event
ky = [(0.0, yy(EV[-1][0]) - yy(YR0)), (0.3, yy(EV[-1][0]) - yy(YR0)), (0.305, 0.0)]
for t0, (yr, *_) in zip(TE, EV):
    ky += [(t0 - 0.3, ky[-1][1]), (t0, yy(yr) - yy(YR0))]
ky.append((D, ky[-1][1]))
a(f'<g class="fx"><g>{T.translate(ky, "y")}<path d="M{AX - 16},{yy(YR0) - 6} L{AX - 8},{yy(YR0)} L{AX - 16},{yy(YR0) + 6} Z" fill="{PARCH}"/></g></g>')
H = max(L0 + LS * (len(EV) - 1) + 30, int(Y1) + 14)
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-14 svgd-part4-14">')
o.insert(1, '<title id="svgt-part4-14">Fig 14.1 · Two thousand years of cryptography in one strip</title>')
o.insert(2, '<desc id="svgd-part4-14">A timeline drawn to scale from 50 BCE to 2030. Shared-key ciphers fill almost all of it: Caesar\'s shift, broken by letter frequencies; Bellaso\'s cipher of 1553, later called Vigenère\'s, broken by Babbage and by Kasiski in 1863; Enigma, in German military service from 1926, broken by Rejewski in 1932 and the Bombe in 1940. '
  'Public-key cryptography is the last sliver: Diffie–Hellman in 1976, RSA in 1977, then AES in 2001 for shared keys, and NIST\'s post-quantum standards in 2024.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('For two thousand years every cipher needed a key shared in advance, and each was broken by someone who noticed its structure. '
           'In 1976 Diffie and Hellman showed how strangers could agree on a key in public; drawn to scale, everything since fits in the last sliver.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> Each leader runs to the event's year on a line from 50 BCE to 2030; the public-key era is under its last 3%.</li>
          <li><b>The exception.</b> The <span class="key-term">one-time pad</span> is provably unbreakable, but it needs as much truly random shared key as there is message, so it never scaled.</li>
          <li><b>First, in secret.</b> At GCHQ, James Ellis, Clifford Cocks and Malcolm Williamson found public-key cryptography between 1969 and 1974; it stayed classified until 1997.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-1">
      <div class="diagram-label">Fig 14.1 · Two thousand years of cryptography in one strip</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-1"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-1', cap, card.replace('CAPID', cap))
