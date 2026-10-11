# Fig 14.7 · Diffie–Hellman with actual numbers · g=5, p=23 (Pass 28, law 3). Strongroom dossier plate. Alice keeps
# a = 6, Bob b = 15; each publishes 5^secret mod 23 (8 and 19), the numbers cross the public channel where Eve sees
# them, and each raises the other's number to their own secret: 19^6 = 8^15 = 2 (mod 23). Eve is left with
# 5^x mod 23 = 8. Lock-step: each line stamps in turn. t=0 (shift): the exchange complete.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

P, G, A_, B_ = 23, 5, 6, 15
PA, PB = pow(G, A_, P), pow(G, B_, P)
K = pow(PB, A_, P)
assert (PA, PB, K) == (8, 19, 2) and pow(PA, B_, P) == K and pow(G, A_ * B_, P) == K
assert [x for x in range(1, P) if pow(G, x, P) == PA] == [6]
W = 400
AX, BX = 10, 210                                   # column left edges
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
a(text(200, 18, f'public: p = {P}, g = {G}', anchor='middle', size=13, fill=PSOFT, ls='0'))
a(text(AX, 46, 'Alice', anchor='start', size=13, fill=SEAL, ls='0'))
a(text(BX, 46, 'Bob', anchor='start', size=13, fill=BRASS, ls='0'))
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
sup = lambda n: str(n).translate(SUP)
def line(x, y, s, col, t0):
    a(f'<g opacity="0.25">{text(x, y, s, anchor="start", size=13, fill=col, ls="0")}</g><g opacity="0">{win(t0)}{text(x, y, s, anchor="start", size=13, fill=col, ls="0")}</g>')
# secrets, kept at home
line(AX, 70, f'secret a = {A_}', SEAL, 0.8)
line(BX, 70, f'secret b = {B_}', BRASS, 0.8)
# public numbers
line(AX, 94, f'A = 5{sup(A_)} mod 23 = {PA}', PSOFT, 1.8)
line(BX, 94, f'B = 5{sup(B_)} mod 23 = {PB}', PSOFT, 1.8)
# the public channel, and Eve
CY0, CY1 = 108, 186
a(f'<rect x="4" y="{CY0}" width="392" height="{CY1 - CY0}" rx="3" fill="{OXBLOOD}" fill-opacity="0.12" stroke="{OXBLOOD}" stroke-opacity="0.5" stroke-dasharray="4 3"/>')
a(text(392, CY1 - 8, 'public channel', anchor='end', size=13, fill=OXBLOOD, ls='0'))
eve = text(10, CY0 + 16, f'Eve sees {PA} and {PB}', anchor='start', size=13, fill=OXBLOOD, ls='0')
a(f'<g opacity="0.25">{eve}</g><g opacity="0">{win(3.4)}{eve}</g>')
def token(x0, x1, y, s, col, t0, t1):
    w = len(s) * 7.8 + 14
    mv = T.translate([(0.0, x1 - x0), (0.3, x1 - x0), (0.305, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)], 'x')
    a(f'<g class="fx" opacity="0">{win(t0)}<g>{mv}<rect x="{x0 - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
      f'{text(x0, y + 5, s, anchor="middle", size=13, fill=col, ls="0")}</g></g>')
token(60, 300, CY0 + 32, f'A = {PA}', SEAL, 2.6, 3.8)
token(300, 60, CY0 + 56, f'B = {PB}', BRASS, 2.6, 3.8)
# each combines the other's number with their own secret
line(AX, 210, f'K = {PB}{sup(A_)} mod 23 = {K}', PSOFT, 5.0)
line(BX, 210, f'K = {PA}{sup(B_)} mod 23 = {K}', PSOFT, 5.4)
same = f'<rect x="130" y="222" width="140" height="26" rx="13" fill="none" stroke="{SAGE}" stroke-width="2"/>' + text(200, 240, f'same K = {K}', anchor='middle', size=13, fill=SAGE, ls='0')
a(f'<g opacity="0.2">{same}</g><g opacity="0">{win(6.2)}{same}</g>')
a(f'<g class="fx" opacity="0">{stamp(6.2)}<rect x="126" y="218" width="148" height="34" rx="17" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
line(10, 274, 'Eve needs x: 5ˣ mod 23 = 8', OXBLOOD, 7.0)
H = 286
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-20 svgd-part4-20">')
o.insert(1, '<title id="svgt-part4-20">Fig 14.7 · Diffie–Hellman with actual numbers · g=5, p=23</title>')
o.insert(2, '<desc id="svgd-part4-20">Public numbers p = 23 and g = 5. Alice keeps a secret 6 and sends 5 to the 6th mod 23, which is 8; Bob keeps a secret 15 and sends 5 to the 15th mod 23, which is 19. '
  'Eve sees 8 and 19 on the public channel. Alice computes 19 to the 6th mod 23 and Bob computes 8 to the 15th mod 23; both get 2. To find it Eve would need the exponent x with 5 to the x mod 23 equal to 8.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Alice and Bob each keep a secret exponent and publish only 5 raised to it, mod 23; each raises the other\'s public number to their own secret, and both arrive at 2. '
           'Eve sees 8 and 19, but to reach 2 she must recover an exponent, the discrete log, which at real sizes no one can.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why both get 2.</b> (5⁶)¹⁵ and (5¹⁵)⁶ are both 5⁹⁰, and 5⁹⁰ mod 23 = 2.</li>
          <li><b>Real sizes.</b> p has 2048 bits or more, or the group is an elliptic curve (X25519 in TLS 1.3). With p = 23, Eve would simply try all 22 exponents.</li>
          <li><b>In TLS.</b> Fresh secrets are picked for every connection and thrown away after, which is forward secrecy (Part III, Fig 11.13); a signature, not Diffie–Hellman, proves who is on the other end.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-7">
      <div class="diagram-label">Fig 14.7 · Diffie–Hellman with actual numbers · g=5, p=23</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-7"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-7', cap, card.replace('CAPID', cap))
