# Fig 11.10 · Symmetric vs asymmetric · the same secret · or two halves of one (Pass 28, law 3). Chart Room plate.
# Lane 1, symmetric: Alice and Bob both hold K; "hi" leaves Alice, crosses as ciphertext, opens at Bob. The catch:
# K had to reach Bob first. Lane 2, asymmetric: Bob's public key crosses openly to Alice; she locks "hi" with it;
# only Bob's private key, which never moves, opens it. Row 3: TLS uses both, key agreement, then a shared K,
# then AES on the data. t=0 (shift): both lanes settled (Alice holds Bob's public key), the TLS row lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS, GOLD = '#9bd89b', '#ec8d8d', '#d4a853'
W = 400
AX0, AX1, BX0, BX1 = 10, 92, 308, 390           # Alice and Bob boxes
D = 10.0
T = Timeline(D, shift=9.6)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
def chip(x, y, s, col, w=None):
    w = w or len(s) * 8 + 14
    return (f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="#0a1c2d" stroke="{col}" stroke-width="1.5"/>'
            + text(x, y + 5, s, anchor='middle', size=13, fill=col, ls='0'))
def people(y):
    for x0, x1, name, col in ((AX0, AX1, 'Alice', GREEN), (BX0, BX1, 'Bob', ROUTE)):
        a(f'<rect x="{x0}" y="{y - 16}" width="{x1 - x0}" height="32" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
        a(text((x0 + x1) / 2, y + 5, name, anchor='middle', size=13, fill=col, ls='0'))
    a(f'<line x1="{AX1 + 4}" y1="{y}" x2="{BX0 - 4}" y2="{y}" stroke="{CMUTED}" stroke-opacity="0.5" stroke-dasharray="3 4"/>')
def flight(y, t0, t1, xa, xb, plain, cipher=None, pcol=CSOFT):
    """a chip from xa to xb; shown as ciphertext in the middle half of the trip when cipher is given."""
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t1, xb - xa), (D, xb - xa)], 'x')
    if cipher is None:
        a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{mv}{chip(xa, y, plain, pcol)}</g></g>')
        return
    q1, q3 = t0 + (t1 - t0) * 0.25, t0 + (t1 - t0) * 0.75
    a(f'<g class="fx" opacity="0">{lit(t0, q1)}<g>{mv}{chip(xa, y, plain, pcol, 44)}</g></g>')
    a(f'<g class="fx" opacity="0">{lit(q1, q3)}<g>{mv}{chip(xa, y, cipher, LOSS, 44)}</g></g>')
    a(f'<g class="fx" opacity="0">{lit(q3, t1 + 0.01)}<g>{mv}{chip(xa, y, plain, pcol, 44)}</g></g>')
# lane 1: symmetric
Y1 = 62
a(text(10, 24, 'symmetric: one shared key', anchor='start', size=13, fill=CYAN, ls='0'))
people(Y1)
a(chip((AX0 + AX1) / 2, Y1 + 30, 'K', CYAN))
a(chip((BX0 + BX1) / 2, Y1 + 30, 'K', CYAN))
flight(Y1, 0.8, 2.6, AX1 + 26, BX0 - 26, 'hi', 'x7f')
a(text(200, Y1 + 34, 'fast, but how did', anchor='middle', size=13, fill=CMUTED, ls='0'))
a(text(200, Y1 + 51, 'K reach Bob?', anchor='middle', size=13, fill=LOSS, ls='0'))
# lane 2: asymmetric
Y2 = 184
a(text(10, Y2 - 38, 'asymmetric: a key pair', anchor='start', size=13, fill=GREEN, ls='0'))
people(Y2)
bx = (BX0 + BX1) / 2
a(chip(bx - 22, Y2 + 30, 'pub', GREEN))
a(chip(bx + 22, Y2 + 30, 'prv', ROUTE))
TP, TM = (3.2, 4.4), (4.8, 6.6)
flight(Y2, TP[0], TP[1], BX0 - 30, AX1 + 30, 'pub', pcol=GREEN)
a(f'<g opacity="0">{win(TP[1])}{chip((AX0 + AX1) / 2, Y2 + 30, "pub", GREEN)}</g>')
flight(Y2, TM[0], TM[1], AX1 + 26, BX0 - 26, 'hi', 'x9q')
a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (TM[1] - 0.002, 0.0), (TM[1], 1.0), (TM[1] + 0.6, 0.0), (D, 0.0)])}'
  f'<rect x="{bx + 22 - 22}" y="{Y2 + 19}" width="44" height="22" rx="4" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(text(200, Y2 + 34, 'pub locks, only', anchor='middle', size=13, fill=CMUTED, ls='0'))
a(text(200, Y2 + 51, 'prv unlocks', anchor='middle', size=13, fill=CMUTED, ls='0'))
# row 3: TLS uses both
Y3 = Y2 + 110
a(text(10, Y3 - 26, 'TLS uses both, once per connection:', anchor='start', size=13, fill=CSOFT, ls='0'))
STEPS = [(70, 'key pairs', GREEN), (200, 'shared K', CYAN), (330, 'AES data', GOLD)]
for k, (x, s, col) in enumerate(STEPS):
    a(f'<g opacity="0.35">{chip(x, Y3, s, col, 100)}</g>')
    a(f'<g class="fx" opacity="0">{win(7.2 + 0.5 * k)}{chip(x, Y3, s, col, 100)}</g>')
    if k:
        a(f'<path d="M{STEPS[k - 1][0] + 54},{Y3} L{x - 56},{Y3} m-6,-5 l6,5 l-6,5" fill="none" stroke="{CMUTED}"/>')
H = Y3 + 24
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-49 svgd-part3-49">')
o.insert(1, '<title id="svgt-part3-49">Fig 11.10 · Symmetric vs asymmetric · the same secret · or two halves of one</title>')
o.insert(2, '<desc id="svgd-part3-49">Symmetric: Alice and Bob both hold the same key K; a message leaves Alice, crosses as unreadable ciphertext and is opened by Bob with the same K. The question is how K reached Bob. '
  'Asymmetric: Bob holds a public key and a private key. The public key crosses openly to Alice; she locks the message with it; only Bob\'s private key, which never leaves him, opens it. '
  'TLS uses both: key pairs to agree on a shared key K, then AES with K for the data.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ("Top, one key K that must somehow reach Bob; below it, Bob's key pair, whose public half can cross openly. TLS uses the pair once per connection to agree on K, and AES with K carries the data.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Symmetric.</b> AES with a 128- or 256-bit key. CPUs have instructions for it, so it runs at gigabytes per second.</li>
          <li><b>Asymmetric.</b> In <span class="key-term">asymmetric encryption</span> the two keys are linked by mathematics (Fig 11.8): locking with the public key is easy, opening without the private key means solving the hard problem. Every operation is far slower than AES, so it never touches bulk data.</li>
          <li><b>In TLS.</b> TLS 1.3 uses Diffie–Hellman key agreement: each side sends a public half and combines the other's with its own private half, so both reach the same K without it ever crossing the wire.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-10">
      <div class="diagram-label">Fig 11.10 · Symmetric vs asymmetric · the same secret · or two halves of one</div>
      {svg}
      <p id="ch11-crypto-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-10', 'ch11-crypto-p8', card)
