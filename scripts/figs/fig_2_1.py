# Fig 2.1 · Why binary survives noise (Pass 28, law 3). The same voltage span, the same noise.
# Binary: one threshold, wide bands, every bit read right. Ternary: two thresholds, narrow bands,
# and one drift a binary wire would shrug off is read as the wrong digit. A cursor reads along.
import math, random
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 372
X0, SW = 64, 63                       # first symbol x, symbol width (5 symbols)
T = Timeline(7, shift=6.5)
rnd = random.Random(11)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-17 svgd-part1-17">')
a('<title id="svgt-part1-17">Fig 2.1 · Why binary survives noise · one threshold against two</title>')
a('<desc id="svgd-part1-17">Two wires with the same voltage span and the same noise. The binary wire has one threshold and wide bands; its five bits 0 1 1 0 1 are all read correctly. '
  'The ternary wire squeezes three levels into the same span with two thresholds; a small drift on its fourth digit crosses a threshold and the 0 is read as +1.</desc>')

def panel(y0, name, levels, thresholds, seq, drift_at=None):
    # levels: {digit: y}, thresholds: [y], seq: digits sent
    a(text(20, y0 - 10, name, size=14, fill='rgba(255,255,255,0.8)'))
    top, bot = min(levels.values()) - 14, max(levels.values()) + 14
    a(f'<rect x="{X0}" y="{top}" width="{5 * SW}" height="{bot - top}" rx="3" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.12)"/>')
    for d, y in levels.items():
        a(text(X0 - 10, y + 5, d, anchor='end', size=15, fill='rgba(255,255,255,0.7)', ls='0'))
    for y in thresholds:
        a(f'<line x1="{X0}" y1="{y}" x2="{X0 + 5 * SW}" y2="{y}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    # the signal: each digit's level plus the same small noise, and the same drift on the fourth digit
    pts = []
    for i, d in enumerate(seq):
        for k in range(9):
            x = X0 + i * SW + 4 + k * (SW - 8) / 8
            n = rnd.uniform(-9, 9)
            if drift_at == i: n -= 26 * math.sin(math.pi * k / 8)      # a drift upward, mid-symbol
            pts.append((x, levels[d] + n))
    a('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round"/>')
    return pts

def readout(y, seq, reads, t_of):
    for i, (sent, got) in enumerate(zip(seq, reads)):
        x = X0 + i * SW + SW / 2
        ok = sent == got
        col = '#fff' if ok else RED
        a(f'<text x="{x}" y="{y}" text-anchor="middle" {MONO} font-size="17" fill="{col}">{got}'
          f'{T.anim("opacity", [(0.0, 0.2), (t_of(i), 0.2), (t_of(i) + 0.05, 1.0), (6.9, 1.0), (6.95, 0.2)])}</text>')
        if not ok:
            a(f'<rect x="{x - 24}" y="{y - 19}" width="48" height="26" rx="5" fill="none" stroke="{RED}" stroke-width="1.8">'
              f'{T.anim("opacity", [(0.0, 0.0), (t_of(i), 0.0), (t_of(i) + 0.05, 1.0), (6.9, 1.0), (6.95, 0.0)])}</rect>')

t_of = lambda i: 0.5 + (i + 0.6) * 1.0
B = {'1': 52, '0': 128}
panel(36, 'BINARY · ONE THRESHOLD', B, [90], ['0', '1', '1', '0', '1'], drift_at=3)   # the same drift, absorbed
a(text(X0 + 6, 84, 'threshold', size=13, fill=GOLD))
readout(172, ['0', '1', '1', '0', '1'], ['0', '1', '1', '0', '1'], t_of)
TER = {'+1': 222, '0': 258, '−1': 294}
panel(206, 'TERNARY · TWO THRESHOLDS', TER, [240, 276], ['0', '+1', '−1', '0', '+1'], drift_at=3)
readout(338, ['0', '+1', '−1', '0', '+1'], ['0', '+1', '−1', '+1', '+1'], t_of)
a(text(X0 + 3.5 * SW, 364, 'sent 0, read +1', anchor='middle', size=13, fill=RED))
# the reading cursor, over both wires
a(f'<line y1="40" y2="345" stroke="#fff" stroke-width="1.5" opacity="0">{T.anim("x1", [(0.0, X0), (0.5, X0), (5.5, X0 + 5 * SW), (7.0, X0 + 5 * SW)])}'
  f'{T.anim("x2", [(0.0, X0), (0.5, X0), (5.5, X0 + 5 * SW), (7.0, X0 + 5 * SW)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (0.45, 0.0), (0.5, 0.8), (5.5, 0.8), (5.6, 0.0), (7.0, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same wire, the same noise. With one threshold binary leaves each level a wide margin; with two, ternary squeezes its bands until a drift binary would shrug off reads as the wrong digit.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A threshold.</b> The reader decides a digit by which side of a threshold the voltage is on.</li>
          <li><b>The margin.</b> Binary's single threshold sits halfway: a level must drift half the span to flip. Ternary's two thresholds leave each level only a sixth of the span on either side.</li>
          <li><b>The noise.</b> Ageing parts and temperature swings make small drifts constant, so the wider margin won. Engineering, not mathematics, decided it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-1">
      <div class="diagram-label">Fig 2.1 · Why binary survives noise · one threshold against two</div>
      {svg}
      <p id="ch2-binary-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-1', 'ch2-binary-p4', card)
