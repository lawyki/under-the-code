# Fig 2.1 · Why binary survives noise (Pass 31, Part I, from an empty script). Job: function. Takeaway: binary
# splits a wire's voltage into two wide bands, so noise that tips ternary's narrow bands leaves binary right.
# Concept: the two wires as two gauges of the same height (the same span), binary cut once, ternary twice. The
# fourth digit is on both: binary's 0 and ternary's 0, and the same noise lifts both by the same amount (the dot
# jitters in step on both gauges). Binary's dot stays in its band; ternary's crosses into +1, which lights red.
# Under each gauge, the five digits sent and read. t=0 is the worst moment of the noise: the misread on the plate.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 372
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
TOP, BOT = 64, 264                      # the span: 1 at TOP, 0 at BOT
V = lambda f: BOT - f * (BOT - TOP)
DRIFT = 0.3
T = Timeline(6, shift=0.0)
# the shared noise: fraction of DRIFT over time (1 = the full lift), jittery, the peak at t=0
NOISE = [(0.0, 1.0), (0.4, 0.55), (0.8, 0.7), (1.2, 0.25), (1.6, 0.4), (2.0, 0.1), (2.5, 0.3), (3.0, 0.05), (3.5, 0.35),
         (4.0, 0.6), (4.4, 0.45), (4.8, 0.85), (5.2, 0.7), (5.6, 0.95), (6.0, 1.0)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-17 svgd-part1-17"{T.steps([(2.0, 'a little noise'), (5.9, 'a lot')])}>')
a('<title id="svgt-part1-17">Fig 2.1 · Why binary survives noise · one threshold against two</title>')
a('<desc id="svgd-part1-17">Two wires with the same voltage span and the same noise, drawn as two gauges of the same height. The binary '
  'wire has one threshold and two wide bands; the ternary wire squeezes three levels into the same span with two thresholds. Both '
  'send 0 as their fourth digit and the same noise lifts both by the same amount: binary\'s level stays in its band, ternary\'s '
  'crosses a threshold and the 0 is read as +1. Binary reads all five bits 0 1 1 0 1 right.</desc>')

def gauge(x0, bands, level, label, sent, read, wrong):
    w = 84
    a(text(x0 + w / 2, 40, label, anchor='middle', size=15, fill=INK))
    a(f'<rect x="{x0}" y="{TOP - 10}" width="{w}" height="{BOT - TOP + 20}" rx="5" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
    # thresholds and band names
    for (f0, f1, name) in bands:
        a(text(x0 - 10, (V(f0) + V(f1)) / 2 + 5, name, anchor='end', size=14, fill=MUTED, ls='0'))
    for (f0, f1, name) in bands[1:]:
        a(f'<line x1="{x0}" y1="{V(f0):.1f}" x2="{x0 + w}" y2="{V(f0):.1f}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    # the band the fourth digit is misread into lights red while the noise holds it there
    if wrong:
        f0, f1, _ = wrong
        cross = (bands[-1][0] - level) / DRIFT          # noise fraction at which the dot crosses
        pts = [(0.0, 1.0)]
        for (t0, v0), (t1, v1) in zip(NOISE, NOISE[1:]):
            pts.append((t1, 1.0 if v1 >= cross else 0.0))
        a(f'<rect x="{x0 + 1}" y="{V(f1) - 9:.1f}" width="{w - 2}" height="{V(f0) - V(f1) + 9:.1f}" fill="none" stroke="{RED}" stroke-width="2.4">'
          f'{T.discrete("opacity", pts)}</rect>')
    # the sent level, and the dot the noise jostles
    a(f'<line x1="{x0 + 8}" y1="{V(level):.1f}" x2="{x0 + w - 8}" y2="{V(level):.1f}" stroke="{BLUE}" stroke-width="1.5" opacity="0.6"/>')
    ys = [(t, -(BOT - TOP) * DRIFT * v) for t, v in NOISE]
    a(f'<g>{T.translate(ys, axis="y")}<circle cx="{x0 + w / 2}" cy="{V(level):.1f}" r="7" fill="{BLUE}" stroke="#111" stroke-width="1.5"/></g>')
    # the five digits, sent and read
    for k, (s, r) in enumerate(zip(sent, read)):
        cx = x0 + w / 2 + (k - 2) * 30
        a(text(cx, 312, s, anchor='middle', size=14, fill=MUTED, ls='0'))
        a(text(cx, 340, r, anchor='middle', size=15, fill=RED if s != r else INK, ls='0'))
    cx = x0 + w / 2 + 30
    bad = sent[3] != read[3]
    a(f'<rect x="{cx - 17}" y="294" width="34" height="56" rx="5" fill="none" stroke="{RED if bad else GOLD}" stroke-width="1.6"/>')

gauge(66, [(0.0, 0.5, '0'), (0.5, 1.0, '1')], 0.0, 'binary', ['0', '1', '1', '0', '1'], ['0', '1', '1', '0', '1'], None)
gauge(276, [(0.0, 0.25, '−1'), (0.25, 0.75, '0'), (0.75, 1.0, '+1')], 0.5, 'ternary',
      ['0', '+1', '−1', '0', '+1'], ['0', '+1', '−1', '+1', '+1'], (0.75, 1.0, '+1'))
# the same lift, marked once between the gauges
a(f'<path d="M 200 {V(0.5):.1f} V {V(0.5 + DRIFT) + 6:.1f} m -5 0 l 5 -6 l 5 6" fill="none" stroke="{INK}" stroke-width="1.6"/>')
a(text(200, V(0.5) + 22, 'same', anchor='middle', size=14, fill=INK))
a(text(200, V(0.5) + 39, 'noise', anchor='middle', size=14, fill=INK))
a(text(213, 312, 'sent', anchor='middle', size=14, fill=MUTED))
a(text(213, 340, 'read', anchor='middle', size=14, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = "The same noise lifts both fourth digits; only ternary's crosses a threshold."
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A threshold.</b> The reader decides a digit by which side of a threshold the voltage is on (the dashed lines).</li>
          <li><b>The margin.</b> Binary's single threshold sits halfway: a level must drift half the span to flip. Ternary's two thresholds put a level a quarter of the span from the nearest threshold, half binary's margin.</li>
          <li><b>The noise.</b> Ageing parts and temperature swings make small drifts constant, so the wider margin won.</li>
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
