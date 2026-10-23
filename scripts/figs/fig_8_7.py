# Fig 8.7 · Three ways to ride bits on a carrier (Pass 28, law 3). Chart Room. 1 0 1 0 on a sine carrier
# three ways: amplitude, frequency, phase; exact sines. A cursor sweeps, reading each bit from the one
# property that changes. t=0 (shift): all read.
import math
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

BITS = [1, 0, 1, 0]
W, H = 400, 290
X0, CW = 104, 68                   # four bits, 272 wide
D = 7.0
S0, S1 = 0.4, 6.0
T = Timeline(D, shift=6.4)
xt = lambda x: S0 + (x - X0) / (CW * len(BITS)) * (S1 - S0)
def from_t(t):
    return T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])
def wave(y, f):
    pts = []
    for i in range(len(BITS) * CW + 1):
        x = X0 + i
        b = BITS[min(i // CW, len(BITS) - 1)]
        pts.append((x, y - f(b, i)))
    return '<polyline points="' + ' '.join(f'{x},{v:.1f}' for x, v in pts) + f'" fill="none" stroke="{CYAN}" stroke-width="2"/>'
LANES = [('AM', 'amplitude', lambda b, i: (18 if b else 6) * math.sin(2 * math.pi * 3 * i / CW), ('big', 'small')),
         ('FM', 'frequency', lambda b, i: 16 * math.sin(2 * math.pi * (4 if b else 2) * i / CW), ('fast', 'slow')),
         ('PSK', 'phase', lambda b, i: 16 * math.sin(2 * math.pi * 3 * (i % CW) / CW + (0 if b else math.pi)), ('rises', 'falls'))]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-8 svgd-part3-8">')
a('<title id="svgt-part3-8">Fig 8.7 · Three ways to ride bits on a carrier</title>')
a('<desc id="svgd-part3-8">The bits 1 0 1 0 carried on a sine wave three ways. Amplitude modulation makes the wave big for 1 and small for 0. Frequency modulation makes it faster for 1 and slower for 0. '
  'Phase shift keying keeps size and speed but flips the wave, starting each 1 rising and each 0 falling. A receiver reads each bit from whichever property the scheme changes.</desc>')
a(text(20, 24, 'bits', size=13, fill=CMUTED, ls='0'))
for i, b in enumerate(BITS):
    a(text(X0 + i * CW + CW / 2, 24, str(b), anchor='middle', size=15, fill='#fff', ls='0'))
for i in range(1, len(BITS)):
    a(f'<line x1="{X0 + i * CW}" y1="34" x2="{X0 + i * CW}" y2="{36 + 3 * 80}" stroke="rgba(223,234,242,0.12)" stroke-dasharray="2 3"/>')
for k, (nm, prop, f, (one, zero)) in enumerate(LANES):
    y = 70 + k * 80
    a(text(20, y - 4, nm, size=14, fill='#fff', ls='0'))
    a(text(20, y + 14, prop, size=13, fill=CMUTED, ls='0'))
    a(wave(y, f))
    for i, b in enumerate(BITS):
        m = X0 + i * CW + CW / 2
        a(f'<g>{from_t(xt(X0 + (i + 1) * CW) - 0.05)}{text(m, y + 38, one if b else zero, anchor="middle", size=13, fill=ROUTE, ls="0")}</g>')
x1 = X0 + CW * len(BITS)
a(f'<line y1="34" y2="{36 + 3 * 80}" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}{T.anim("x2", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (S0 - 0.01, 0.0), (S0, 0.6), (S1, 0.6), (S1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ("The bits 1 0 1 0 carried three ways: with each bit the wave's size, its speed or its starting direction changes. Wi-Fi and cable modems change size and phase together (QAM), packing many bits into each symbol: up to 10 in Wi-Fi 6, but only on a far cleaner signal than the 20 dB point in Fig 8.4.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Noise.</b> Interference mostly disturbs amplitude, so FM and PSK resist it better; Edwin Armstrong patented FM in 1933 for exactly that reason.</li>
          <li><b>QAM.</b> 16 combinations of size and phase carry 4 bits per symbol; Wi-Fi 6 uses 1024, 10 bits, and Wi-Fi 7 4096, 12 bits, when the signal is clean, dropping to fewer as it degrades.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-7">
      <div class="diagram-label">Fig 8.7 · Three ways to ride bits on a carrier</div>
      {svg}
      <p id="ch8-encoding-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-7', 'ch8-encoding-p7', card)
