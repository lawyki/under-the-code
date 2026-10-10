# Fig 11.13 · Forward secrecy · stealing the long-term key tomorrow does not unlock yesterday (Pass 28, law 3).
# Chart Room plate. One timeline, 2024 to 2026, two ways to set up the session key. Row 1, RSA key transport
# (allowed in TLS 1.2): each session key crosses sealed with the server's long-term key, so when that key is stolen
# in 2026 every recorded session opens. Row 2, ephemeral Diffie–Hellman (TLS 1.3): the long-term key only signs and
# each session's secret is erased at its end, so the stolen key opens nothing. A cursor walks the years; sessions
# are recorded, the key is stolen, row 1 turns readable, row 2 stays locked. t=0 (shift): the end state.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
W = 400
XY = {2024: 60, 2025: 164, 2026: 290}
AY = 30                                            # the year axis
ROWS = [(78, 'RSA key transport (TLS 1.2)', ROUTE, True), (192, 'ephemeral Diffie–Hellman (TLS 1.3)', GREEN, False)]
SESS = [(2024, 'K1'), (2025, 'K2')]
BW, BH = 96, 44
D = 10.0
T = Timeline(D, shift=9.5)
xt = lambda t: 40 + (t - 0.5) / 5.5 * (360 - 40)  # cursor x over story time 0.5..6
tx = lambda x: 0.5 + (x - 40) / (360 - 40) * 5.5  # story time when the cursor reaches x
TS = {y: tx(XY[y]) for y in XY}
TFLIP = TS[2026] + 0.6
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
H = ROWS[1][0] + BH + 52
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-52 svgd-part3-52">')
a('<title id="svgt-part3-52">Fig 11.13 · Forward secrecy · stealing the long-term key tomorrow does not unlock yesterday</title>')
a('<desc id="svgd-part3-52">Two sessions, in 2024 and 2025, are recorded; in 2026 the server\'s long-term private key is stolen. '
  'With RSA key transport, allowed in TLS 1.2, each session key crossed the wire sealed with that long-term key, so the stolen key opens both recorded sessions. '
  'With ephemeral Diffie–Hellman, as in TLS 1.3, the long-term key only signed the handshake and each session\'s secret was erased when it ended, so both recordings stay locked.</desc>')
# the years
a(f'<line x1="40" y1="{AY}" x2="380" y2="{AY}" stroke="{CMUTED}"/>')
for y, x in XY.items():
    a(f'<line x1="{x}" y1="{AY - 4}" x2="{x}" y2="{AY + 4}" stroke="{CMUTED}"/>')
    a(text(x, AY - 10, str(y), anchor='middle', size=13, fill=LOSS if y == 2026 else CMUTED, ls='0'))
# the theft, across both rows
ks = XY[2026]
a(f'<line x1="{ks}" y1="{AY + 6}" x2="{ks}" y2="{ROWS[1][0] + BH + 8}" stroke="{LOSS}" stroke-dasharray="4 4" stroke-opacity="0.8"/>')
a(f'<g opacity="0.35">{text(ks + 8, AY + 24, "server key", anchor="start", size=13, fill=LOSS, ls="0")}{text(ks + 8, AY + 41, "stolen", anchor="start", size=13, fill=LOSS, ls="0")}</g>')
a(f'<g class="fx" opacity="0">{win(TS[2026])}{text(ks + 8, AY + 24, "server key", anchor="start", size=13, fill=LOSS, ls="0")}{text(ks + 8, AY + 41, "stolen", anchor="start", size=13, fill=LOSS, ls="0")}</g>')
for ry, head, col, opens in ROWS:
    a(text(10, ry - 10, head, anchor='start', size=13, fill=col, ls='0'))
    for yr, k in SESS:
        x = XY[yr] - 10
        a(f'<rect x="{x}" y="{ry}" width="{BW}" height="{BH}" rx="5" fill="#0a1c2d" stroke="{CSOFT}" stroke-opacity="0.5"/>')
        a(text(x + 10, ry + 18, f'session {k}', anchor='start', size=13, fill=CSOFT, ls='0'))
        t0 = TS[yr]
        a(f'<g class="fx" opacity="0">{lit(t0, TFLIP)}{text(x + 10, ry + 36, "recorded", anchor="start", size=13, fill=CMUTED, ls="0")}</g>')
        end = ('readable', LOSS) if opens else ('locked', GREEN)
        a(f'<g class="fx" opacity="0">{win(TFLIP)}{text(x + 10, ry + 36, end[0], anchor="start", size=13, fill=end[1], ls="0")}'
          f'<rect x="{x}" y="{ry}" width="{BW}" height="{BH}" rx="5" fill="none" stroke="{end[1]}" stroke-width="2"/></g>')
    # what the stolen key does to this row
    line = 'the stolen key unseals every K' if opens else 'key only signed; secrets gone'
    a(f'<g opacity="0.35">{text(10, ry + BH + 22, line, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{win(TFLIP + 0.4)}{text(10, ry + BH + 22, line, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
# the cursor
a(f'<g class="fx"><g>{T.translate([(0.0, 320), (0.3, 320), (0.305, 0.0), (0.5, 0.0), (6.0, 320), (D, 320)], "x")}'
  f'<circle cx="40" cy="{AY}" r="5" fill="#fff"/></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('If the session key crosses the wire sealed with the server\'s long-term key, whoever records the traffic and steals that key later can open every past session. '
           'With ephemeral Diffie–Hellman the long-term key only signs, and each session\'s secret is erased when it ends, so the stolen key opens nothing recorded.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rule.</b> TLS 1.2 allowed both rows; TLS 1.3 removed RSA key transport, so every full handshake has forward secrecy.</li>
          <li><b>What a stolen key still does.</b> It lets the thief pose as the server from then on, until the certificate is revoked or expires.</li>
          <li><b>What it does not cover.</b> Breaking the Diffie–Hellman exchange itself. A large quantum computer could do that from a recording, which is why recorded traffic is a reason to move key exchange to post-quantum methods now.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-13">
      <div class="diagram-label">Fig 11.13 · Forward secrecy · stealing the long-term key tomorrow does not unlock yesterday</div>
      {svg}
      <p id="ch11-tls-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(TS, TFLIP)
    splice('part-3', 'fig-11-13', 'ch11-tls-p7', card)
