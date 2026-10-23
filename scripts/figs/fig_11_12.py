# Fig 11.12 · The certificate chain · why your browser trusts a stranger (Pass 28, law 3). Chart Room plate. Three
# certificates, root on top: ISRG Root X1 (self-signed, in the trust store), R11 (a Let's Encrypt intermediate
# since 2024), and a leaf for shop.example (a reserved, illustrative name). "signs" runs down; the browser's check
# runs up: the leaf's signature with R11's public key, R11's with the root's, then the root found in the store.
# Each check lights in turn. t=0 (shift): every link checked.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, BLUE = '#9bd89b', '#86a8ff'
W = 400
CX0, CX1 = 20, 300                                # certificate cards
CARDS = [(40, 'ISRG Root X1', 'self-signed, in the store', CYAN), (138, 'R11', 'intermediate', GREEN), (236, 'shop.example', 'leaf, 90 days', BLUE)]
CH = 58
CHK = [(CARDS[2][0], 'signature', 1.8), (CARDS[1][0], 'signature', 3.0), (CARDS[0][0], 'in the store', 4.2)]
D = 9.0
T = Timeline(D, shift=8.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.9, 0.0), (D, 0.0)])
o = []; a = o.append
H = CARDS[2][0] + CH + 16
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-51 svgd-part3-51">')
a('<title id="svgt-part3-51">Fig 11.12 · The certificate chain · why your browser trusts a stranger</title>')
a('<desc id="svgd-part3-51">Three certificates. At the top the root, ISRG Root X1, which signs itself and ships in the browser\'s trust store. It signs the intermediate R11, which signs the leaf for shop.example, valid 90 days. '
  'The browser checks upward: the leaf\'s signature with R11\'s public key, R11\'s signature with the root\'s public key, and finally that the root is in its trust store.</desc>')
for y, name, role, col in CARDS:
    a(f'<rect x="{CX0}" y="{y}" width="{CX1 - CX0}" height="{CH}" rx="6" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.8"/>')
    a(text(CX0 + 12, y + 23, name, anchor='start', size=13, fill=col, ls='0'))
    a(text(CX0 + 12, y + 43, role, anchor='start', size=13, fill=CMUTED, ls='0'))
# signs: down the left
for (y0, *_), (y1, *_) in zip(CARDS, CARDS[1:]):
    x = CX0 + 40
    a(f'<line x1="{x}" y1="{y0 + CH}" x2="{x}" y2="{y1 - 2}" stroke="{CMUTED}"/><path d="M{x - 5},{y1 - 8} L{x},{y1 - 2} L{x + 5},{y1 - 8}" fill="none" stroke="{CMUTED}"/>')
    a(text(x + 10, (y0 + CH + y1) / 2 + 5, 'signs', anchor='start', size=13, fill=CMUTED, ls='0'))
# checks: each card's badge lights when its check passes
for k, (yc, what, tc) in enumerate(CHK):
    # badge inside the card
    a(f'<g opacity="0.3">{text(CX1 - 12, yc + 23, "✓", anchor="end", size=16, fill=GREEN, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{win(tc)}{text(CX1 - 12, yc + 23, "✓", anchor="end", size=16, fill=GREEN, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{pulse(tc)}<rect x="{CX0}" y="{yc}" width="{CX1 - CX0}" height="{CH}" rx="6" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the check arrows: from the card above (its public key) to the card below (its signature)
for (yp, *_), (yc, *_), (_, _, tc) in ((CARDS[1], CARDS[2], CHK[0]), (CARDS[0], CARDS[1], CHK[1])):
    x = CX1 + 22
    path = f'<path d="M{CX1},{yp + CH / 2} h{x - CX1} V{yc + CH / 2} h-{x - CX1 - 6} m6,-5 l-6,5 l6,5" fill="none" stroke="{GREEN}" stroke-width="1.5"/>'
    a(f'<g opacity="0.3">{path}</g><g class="fx" opacity="0">{win(tc - 0.5)}{path}</g>')
    a(f'<g opacity="0.3">{text(x + 8, (yp + yc + CH) / 2 - 2, "check", anchor="start", size=13, fill=GREEN, ls="0")}{text(x + 8, (yp + yc + CH) / 2 + 15, "with key", anchor="start", size=13, fill=GREEN, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{win(tc - 0.5)}{text(x + 8, (yp + yc + CH) / 2 - 2, "check", anchor="start", size=13, fill=GREEN, ls="0")}{text(x + 8, (yp + yc + CH) / 2 + 15, "with key", anchor="start", size=13, fill=GREEN, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ("A server sends its own certificate and the intermediate's; the browser checks each signature with the public key of the certificate above it, until it reaches a root it already trusts. Here <code>shop.example</code> is vouched for by R11, and R11 by ISRG Root X1, which ships in the trust store.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>What is checked.</b> On the leaf: the name matches the site, today is within its dates, and it has not been revoked. On every link: the signature verifies with the parent's public key. Any failure ends in a browser warning.</li>
          <li><b>Why an intermediate.</b> The root's private key stays offline; the intermediate's signs every day and can be replaced without touching anyone's trust store. Let's Encrypt certificates last 90 days.</li>
          <li><b>Certificate Transparency.</b> Since 2018 Chrome has required every new certificate to be logged publicly, so one issued wrongly, as by the breached Dutch CA DigiNotar in 2011, cannot stay hidden.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-12">
      <div class="diagram-label">Fig 11.12 · The certificate chain · why your browser trusts a stranger</div>
      {svg}
      <p id="ch11-tls-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-12', 'ch11-tls-p5', card)
