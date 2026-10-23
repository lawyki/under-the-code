# Fig 11.11 · TLS 1.3 · one round trip from "hello" to encrypted data (Pass 28, law 3). Chart Room plate. A ladder,
# client left, server right, time down (RFC 8446). ClientHello + key share (the client's Diffie–Hellman half) in
# the clear; the server can now derive the keys, and its lane turns gold. ServerHello + key share in the clear,
# then {certificate, signature, Finished} encrypted; the client derives the keys, its lane turns gold. {Finished}
# {GET /}, then {200 OK and the page}. Braces mean encrypted. A bracket marks the one round trip from hello to
# keys. Tokens fly each message; labels light as they go. t=0 (shift): the whole exchange lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD = '#9bd89b', '#d4a853'
W = 400
CX, SX = 76, 372                                  # lanes
MID = (CX + SX) / 2
D = 10.0
T = Timeline(D, shift=9.5)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
MSGS = [  # (from client?, label lines [(text, colour)], arrow start y, arrow end y, flight)
    (True, [('ClientHello + key share', CSOFT), ('my half of a Diffie–Hellman', CMUTED)], 84, 118, (0.6, 1.8)),
    (False, [('ServerHello + key share', CSOFT), ('{certificate, signature, Finished}', GOLD)], 172, 206, (2.2, 3.4)),
    (True, [('{Finished} {GET /}', GOLD), ('the request, already encrypted', CMUTED)], 260, 294, (3.8, 5.0)),
    (False, [('{200 OK and the page}', GOLD)], 322, 356, (5.4, 6.6))]
TSK, TCK = MSGS[0][4][1], MSGS[1][4][1]           # server, client hold the keys
o = []; a = o.append
LB = 380
H = LB + 10
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-50 svgd-part3-50">')
a('<title id="svgt-part3-50">Fig 11.11 · TLS 1.3 · one round trip from &quot;hello&quot; to encrypted data</title>')
a('<desc id="svgd-part3-50">The TLS 1.3 handshake as a ladder, client on the left, server on the right, time running down. '
  'The client sends ClientHello with its key share, its half of a Diffie–Hellman exchange; from that moment the server can derive the keys. '
  'The server replies with ServerHello and its key share in the clear, then its certificate, signature and Finished, encrypted. '
  'One round trip after its hello the client holds the same keys; it sends Finished and its GET request, encrypted, and the server answers with the page, encrypted.</desc>')
a(text(CX, 22, 'client', anchor='middle', size=13, fill=GREEN, ls='0'))
a(text(SX, 22, 'server', anchor='end', size=13, fill=ROUTE, ls='0'))
# lanes: muted until that side holds the keys, gold after
for x, tk, yk in ((CX, TCK, MSGS[1][3]), (SX, TSK, MSGS[0][3])):
    a(f'<line x1="{x}" y1="32" x2="{x}" y2="{LB}" stroke="{CMUTED}" stroke-opacity="0.6"/>')
    a(f'<g opacity="0">{win(tk)}<line x1="{x}" y1="{yk}" x2="{x}" y2="{LB}" stroke="{GOLD}" stroke-width="3"/></g>')
# the round trip
yb0, yb1 = MSGS[0][2], MSGS[1][3]
a(f'<path d="M{CX - 14},{yb0} h-6 V{yb1} h6" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
a(text(CX - 26, (yb0 + yb1) / 2 - 4, '1', anchor='end', size=13, fill=CYAN, ls='0'))
a(text(CX - 26, (yb0 + yb1) / 2 + 13, 'RTT', anchor='end', size=13, fill=CYAN, ls='0'))
for fromc, lines, y0, y1, (t0, t1) in MSGS:
    xa, xb = (CX, SX) if fromc else (SX, CX)
    top = y0 - 10 - 17 * (len(lines) - 1)
    lab = ''.join(text(MID, top + 17 * i, s, anchor='middle', size=13, fill=c, ls='0') for i, (s, c) in enumerate(lines))
    a(f'<g opacity="0.4">{lab}</g>')
    a(f'<g class="fx" opacity="0">{win(t0)}{lab}</g>')
    enc = lines[0][0].startswith('{')
    col = GOLD if enc else CSOFT
    ah = -1 if fromc else 1
    a(f'<line x1="{xa}" y1="{y0}" x2="{xb}" y2="{y1}" stroke="{col}" stroke-width="1.5"/>'
      f'<path d="M{xb + ah * 10},{y1 - 6} L{xb},{y1} L{xb + ah * 10},{y1 + 5}" fill="none" stroke="{col}" stroke-width="1.5"/>')
    mvx = T.translate([(0.0, 0.0), (t0, 0.0), (t1, xb - xa), (D, xb - xa)], 'x')
    mvy = T.translate([(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)], 'y')
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{mvx}<g>{mvy}<circle cx="{xa}" cy="{y0}" r="5" fill="{col}"/></g></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Gold marks when each side holds the keys: the server as soon as the ClientHello lands, the client when the ServerHello arrives, one round trip after sending its own. Everything after that point is encrypted, the request included.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Plain and braced.</b> Only the two hellos cross in the clear; everything in braces is encrypted under keys derived (with HKDF) from the shared Diffie–Hellman secret. The gold lane marks when each side holds them.</li>
          <li><b>Proof of identity.</b> The <span class="key-term">X.509</span> certificate binds the server's public key to its name (Fig 11.12); the signature, over the handshake so far, proves the server holds the matching private key. Each Finished is a MAC over the whole transcript, so tampering shows.</li>
          <li><b>The cost.</b> One round trip before data, against two in TLS 1.2; the hellos also settle the <span class="key-term">cipher suite</span>, such as AES-GCM or ChaCha20-Poly1305. A client returning to a server it has met can even send early data with its hello (0-RTT).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-11">
      <div class="diagram-label">Fig 11.11 · TLS 1.3 · one round trip from "hello" to encrypted data</div>
      {svg}
      <p id="ch11-tls-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-11', 'ch11-tls-p3', card)
