# Fig 8.6 · Same bits, two waveforms (Pass 28, law 3). Chart Room. 1 0 0 0 0 1 1 sent as NRZ and as
# Manchester to a receiver whose clock runs 20% fast (exaggerated). The NRZ receiver can resync only
# on the rare edges and samples the four-zero run five times: an extra 0. The Manchester receiver
# resyncs on every mid-bit edge and reads all seven bits. A cursor sweeps; samples and reads appear.
# t=0 (shift): both read out.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

BITS = [1, 0, 0, 0, 0, 1, 1]
N = len(BITS)
W, H = 400, 222
X0, CW = 50, 46
RATE = 0.8                       # receiver bit period, in sent bit periods (clock 20% fast)
D = 8.0
S0, S1 = 0.4, 6.8
T = Timeline(D, shift=7.4)
xb = lambda u: X0 + u * CW       # u in sent bit periods
tb = lambda u: S0 + u / N * (S1 - S0)
def from_t(t):
    return T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])
# NRZ receiver: resync at each edge, sample half a (fast) period later, then every period
edges = [i for i in range(1, N) if BITS[i] != BITS[i - 1]]
samples, start = [], 0.0
for seg_end in edges + [N]:
    u = start + RATE / 2
    while u < seg_end:
        samples.append(u); u += RATE
    start = seg_end
nrz_read = [BITS[int(u)] for u in samples]
assert nrz_read == [1, 0, 0, 0, 0, 0, 1, 1], nrz_read     # one zero too many
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-7 svgd-part3-7">')
a('<title id="svgt-part3-7">Fig 8.6 · Same bits, two waveforms</title>')
a('<desc id="svgd-part3-7">The bits 1 0 0 0 0 1 1 sent two ways to a receiver whose clock runs fast. In NRZ the four zeros are one flat stretch with no edges, so the receiver cannot correct its clock and samples that stretch five times, reading 1 0 0 0 0 0 1 1: one zero too many. '
  'In Manchester every bit has an edge in its middle, so the receiver corrects its clock on every bit and reads 1 0 0 0 0 1 1 correctly.</desc>')
a(text(20, 24, 'sent', size=13, fill=CMUTED, ls='0'))
for i, b in enumerate(BITS):
    a(text(xb(i + 0.5), 24, str(b), anchor='middle', size=15, fill='#fff', ls='0'))
    if i: a(f'<line x1="{xb(i)}" y1="34" x2="{xb(i)}" y2="190" stroke="rgba(223,234,242,0.12)" stroke-dasharray="2 3"/>')
def lane(y, title, pts, reads, col, wrong=None):
    a(text(20, y + 22, title, size=13, fill=CMUTED, ls='0'))
    hi, lo = y + 6, y + 34
    a('<polyline points="' + ' '.join(f'{xb(u):.1f},{hi if v else lo}' for u, v in pts) + f'" fill="none" stroke="{col}" stroke-width="2.5"/>')
    for k, (u, v) in enumerate(reads):
        x = xb(u); t = tb(u)
        c = ROUTE if k == wrong else col
        a(f'<g>{from_t(t)}<line x1="{x:.1f}" y1="{hi - 4}" x2="{x:.1f}" y2="{lo + 4}" stroke="{c}" stroke-width="1.5"/>'
          f'{text(x, lo + 24, str(v), anchor="middle", size=15, fill=c, ls="0")}</g>')
# NRZ: level = bit
nrz = []
for i, b in enumerate(BITS):
    nrz += [(i, b), (i + 1, b)]
lane(40, 'NRZ', nrz, list(zip(samples, nrz_read)), CYAN, wrong=5)
# Manchester (IEEE 802.3: 1 = rising mid-bit)
man = []
for i, b in enumerate(BITS):
    f, s = (0, 1) if b else (1, 0)
    man += [(i, f), (i + 0.5, f), (i + 0.5, s), (i + 1, s)]
lane(118, 'Manch.', man, [(i + 0.5, b) for i, b in enumerate(BITS)], CYAN)
a(text(20, 214, 'receiver clock 20% fast, exaggerated', size=13, fill=CMUTED, ls='0'))
x1 = xb(N)
a(f'<line y1="34" y2="190" stroke="#fff" stroke-width="1.2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}{T.anim("x2", [(0.0, X0), (S0, X0), (S1, x1), (D, x1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (S0 - 0.01, 0.0), (S0, 0.6), (S1, 0.6), (S1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Sent to a receiver whose clock runs fast, NRZ\'s four zeros are one flat stretch with nothing to correct against, so the receiver reads five. '
           'Manchester gives it an edge in every bit, so it corrects its clock each time and reads all seven, at the cost of up to twice the signal changes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Real drift.</b> Real clocks differ by parts per million, not 20%, but over a long enough run of identical bits the error adds up the same way.</li>
          <li><b>The compromise.</b> Modern links use codes such as 8b/10b and 64b/66b, which stay close to NRZ's efficiency while guaranteeing an edge every few bits.</li>
          <li><b>NRZ.</b> Non-return-to-zero simply holds the level for each bit: high for 1, low for 0.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-6">
      <div class="diagram-label">Fig 8.6 · Same bits, two waveforms</div>
      {svg}
      <p id="ch8-encoding-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-6', 'ch8-encoding-p5', card)
