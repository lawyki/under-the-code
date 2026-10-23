# Fig 8.4 · Channel capacity as a function of SNR (Pass 28, law 3). Chart Room. log2(1 + SNR) computed
# exactly against SNR in dB; the region above the curve shaded as unreachable; a marker sweeps the curve.
# Marked: a phone line at 30 dB (ceiling 10 b/Hz) with V.34's 33.6 kbps over its 3.43 kHz band (9.8 b/Hz) just under it, and
# Wi-Fi 6 at 20 dB. t=0 (shift): marker near the phone-line point.
import math
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

C = lambda db: math.log2(1 + 10 ** (db / 10))
assert abs(C(30) - 9.97) < 0.01 and abs(C(20) - 6.66) < 0.01 and abs(33.6 / 3.429 - 9.8) < 0.01 and abs(C(30) * 3.429 - 34.2) < 0.1
W, H = 400, 290
X0, X1, Y0, Y1 = 60, 372, 244, 44
DBMAX, CMAX = 40, 14
xd = lambda db: X0 + db / DBMAX * (X1 - X0)
yc = lambda c: Y0 - c / CMAX * (Y0 - Y1)
D = 8.0
S0, S1 = 0.4, 7.4
T = Timeline(D, shift=S0 + 0.75 * (S1 - S0))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-5 svgd-part3-5">')
a('<title id="svgt-part3-5">Fig 8.4 · Channel capacity as a function of SNR</title>')
a('<desc id="svgd-part3-5">Shannon\'s limit, in bits per second per hertz of bandwidth, against signal-to-noise ratio in decibels: log₂(1 + SNR). Above the curve no code can transmit without errors. '
  'Wi-Fi 6 at about 20 dB is allowed about 6.7 bits per hertz. A phone line at about 30 dB is allowed about 10, which over the 3.4 kHz band V.34 modems used is about 34 kbps; they reached 33.6 kbps, 9.8 bits per hertz, just under the curve.</desc>')
pts = [(db / 4) for db in range(0, DBMAX * 4 + 1)]
curve = ' '.join(f'{xd(d):.1f},{yc(C(d)):.1f}' for d in pts)
a(f'<polygon points="{X0},{Y1} {curve} {X1},{Y1}" fill="{ROUTE}" fill-opacity="0.1"/>')
a(text(X0 + 14, Y1 + 22, 'no code can go here', size=13, fill=ROUTE, ls='0'))
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{CMUTED}"/>')
a(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{CMUTED}"/>')
for db in (0, 10, 20, 30, 40):
    a(text(xd(db), Y0 + 20, str(db), anchor='middle', size=13, fill=CMUTED, ls='0'))
a(text(X1, Y0 + 42, 'SNR, dB', anchor='end', size=13, fill=CMUTED, ls='0'))
for c in (0, 5, 10):
    a(text(X0 - 8, yc(c) + 5, str(c), anchor='end', size=13, fill=CMUTED, ls='0'))
a(text(X0 - 8, Y1 - 12, 'bits per Hz', size=13, fill=CMUTED, ls='0'))
a(f'<polyline points="{curve}" fill="none" stroke="{CYAN}" stroke-width="2.5"/>')
# marked points
def dot(db, c, col, r=4.5):
    a(f'<circle cx="{xd(db):.1f}" cy="{yc(c):.1f}" r="{r}" fill="{col}"/>')
dot(20, C(20), CYAN)
a(text(xd(20) + 10, yc(C(20)) + 20, 'Wi-Fi 6 · 6.7', size=13, fill=CYAN, ls='0'))
dot(30, C(30), CYAN)
dot(30, 9.8, ROUTE)
a(text(xd(30) + 10, yc(9.8) + 18, 'V.34', size=13, fill=ROUTE, ls='0'))
a(text(xd(30) + 10, yc(9.8) + 35, '9.8', size=13, fill=ROUTE, ls='0'))
a(text(xd(30) - 10, yc(C(30)) - 10, 'phone line · 10', anchor='end', size=13, fill=CYAN, ls='0'))
# the marker, sweeping SNR
N = 40
kx, ky = [(0.0, 0.0)], [(0.0, 0.0)]
for i in range(N + 1):
    t = S0 + (S1 - S0) * i / N
    db = DBMAX * i / N
    kx.append((t, xd(db) - xd(0))); ky.append((t, yc(C(db)) - yc(C(0))))
kx.append((D, 0.0)); ky.append((D, 0.0))
a(f'<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle class="fx" cx="{xd(0)}" cy="{yc(C(0)):.1f}" r="7" fill="none" stroke="#fff" stroke-width="2"/></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Shannon\'s limit, the curve: a channel of bandwidth B carries at most <span style="white-space:nowrap">B · log₂(1 + SNR)</span> bits per second, and above it errors cannot be avoided. A phone line at 30&nbsp;dB (signal 1,000 times the noise) allows about 10 bits per hertz, about 34&nbsp;kbps over the 3.43&nbsp;kHz band V.34 modems use; they reached 33.6&nbsp;kbps.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reading it.</b> At high SNR each doubling of signal power (+3 dB) buys about one more bit per hertz; doubling the bandwidth doubles the capacity outright.</li>
          <li><b>Wi-Fi 6.</b> At about 20 dB the limit is 6.7 bits per hertz; over an 80 MHz channel that is a few hundred Mbps per stream.</li>
          <li><b>56k modems.</b> They beat 33.6k only because the downstream path stayed digital until the last stretch of phone line, dodging most of the noise.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-4">
      <div class="diagram-label">Fig 8.4 · Channel capacity as a function of SNR</div>
      {svg}
      <p id="ch8-shannon-p11" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-4', 'ch8-shannon-p11', card)
