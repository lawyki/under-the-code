# Fig 14.11 · TLS 1.3 handshake at cryptographic depth (Pass 28, law 3). Strongroom dossier plate. Where Part III's
# Fig 11.11 drew the messages, this draws the key schedule (RFC 8446 §7.1, simplified): client secret x, server
# secret y; x·G and y·G cross; both compute the shared point xy·G (X25519); HKDF turns it into handshake keys, then,
# mixed with a hash of the transcript, into one AES-GCM traffic key per direction. The server signs the transcript
# inside the encrypted handshake, before the traffic keys exist. Lock-step: each stage stamps in order. t=0 (shift): the schedule complete.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
def staged(body, t0):
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(t0)}{body}</g>')
def box(x, y, w, h, l1, l2, col):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>' + text(x + w / 2, y + 18, l1, anchor='middle', size=13, fill=col, ls='0')
    if l2:
        b += text(x + w / 2, y + 36, l2, anchor='middle', size=13, fill=PSOFT, ls='0')
    return b
def down(y0, y1, x=200):
    return f'<path d="M{x},{y0} V{y1} m-4,-6 l4,6 l4,-6" fill="none" stroke="{PMUTED}"/>'
a(text(10, 18, 'client', anchor='start', size=13, fill=SEAL, ls='0'))
a(text(390, 18, 'server', anchor='end', size=13, fill=BRASS, ls='0'))
staged(text(10, 40, 'secret x', anchor='start', size=13, fill=SEAL, ls='0') + text(390, 40, 'secret y', anchor='end', size=13, fill=BRASS, ls='0'), 0.6)
staged(text(10, 62, 'sends x·G', anchor='start', size=13, fill=PSOFT, ls='0') + text(390, 62, 'sends y·G', anchor='end', size=13, fill=PSOFT, ls='0'), 1.2)
# the public shares cross
for (x0, x1, s, col) in ((60, 340, 'x·G', SEAL), (340, 60, 'y·G', BRASS)):
    y = 84 if s == 'x·G' else 102
    mv = T.translate([(0.0, x1 - x0), (0.3, x1 - x0), (0.305, 0.0), (1.8, 0.0), (2.8, x1 - x0), (D, x1 - x0)], 'x')
    a(f'<g class="fx" opacity="0">{win(1.8)}<g>{mv}<rect x="{x0 - 22}" y="{y - 10}" width="44" height="20" rx="4" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
      f'{text(x0, y + 5, s, anchor="middle", size=13, fill=col, ls="0")}</g></g>')
# the shared secret
staged(box(20, 118, 360, 44, 'shared = x·(y·G) = y·(x·G)', 'X25519: both get the same point', SAGE), 3.4)
a(f'<g class="fx" opacity="0">{stamp(3.4)}<rect x="17" y="115" width="366" height="50" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
a(down(164, 182))
staged(box(20, 184, 360, 44, 'HKDF → handshake keys', 'keyed by the shared point and the hellos', PARCH), 4.6)
a(down(230, 244))
staged(text(200, 262, 'server signs the transcript, encrypted', anchor='middle', size=13, fill=OXBLOOD, ls='0'), 5.4)
a(down(270, 284))
staged(box(20, 286, 360, 44, 'HKDF + transcript hash', 'everything said so far, mixed in', PARCH), 6.4)
a(f'<path d="M150,332 L100,350 m3,-7 l-3,7 l7,1" fill="none" stroke="{PMUTED}"/><path d="M250,332 L300,350 m-3,-7 l3,7 l-7,1" fill="none" stroke="{PMUTED}"/>')
staged(box(20, 352, 170, 44, 'client → server', 'AES-GCM key', SAGE) + box(210, 352, 170, 44, 'server → client', 'AES-GCM key', SAGE), 7.6)
H = 404
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-24 svgd-part4-24">')
o.insert(1, '<title id="svgt-part4-24">Fig 14.11 · TLS 1.3 handshake at cryptographic depth</title>')
o.insert(2, '<desc id="svgd-part4-24">The TLS 1.3 key schedule. The client keeps a secret x and sends x times the curve\'s base point G; the server keeps y and sends y·G. Each multiplies the other\'s point by its own secret, and both reach the same shared point. '
  'HKDF turns it, with the hellos, into handshake keys; under them the server signs the transcript. Then HKDF, mixed with a hash of the whole transcript, gives one AES-GCM key for each direction. The server signs the transcript hash with its certificate key.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each side multiplies the curve\'s base point by a fresh secret and sends the result; each then multiplies the other\'s point by its own secret, and both hold the same shared point. '
           'HKDF stretches it, mixed with a hash of the conversation, into separate AES-GCM keys, first for the handshake and then for the data each way.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The primitives.</b> X25519 (the curve arithmetic of Fig 14.9) for the shared secret; HKDF, built on HMAC (SHA-256 or SHA-384, by cipher suite), for every key; AES-GCM or ChaCha20-Poly1305 for the data; Ed25519, ECDSA or RSA-PSS for the server's signature.</li>
          <li><b>Why the transcript goes in.</b> A hash of every handshake message is mixed into the keys, so any tampering leaves the two sides with different keys and the Finished messages fail.</li>
          <li><b>Who is on the other end.</b> The server signs the transcript hash with its certificate's private key (CertificateVerify), and the certificate chains to a trusted root (Part III, Fig 11.12).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-11">
      <div class="diagram-label">Fig 14.11 · TLS 1.3 handshake at cryptographic depth</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-14-11"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-14-11', cap, card.replace('CAPID', cap))
