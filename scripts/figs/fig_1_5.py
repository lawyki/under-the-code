# Fig 1.5 · Inside the switch (Pass 28, law 3). A MOSFET in cross-section. Gate on:
# the field reaches through the oxide, electrons gather under it into a channel,
# current flows source to drain. t=0: on, channel formed, current flowing.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 362
T = Timeline(8, shift=5.0)
ON = [(0.0, 0.0), (1.4, 0.0), (1.5, 1.0), (6.4, 1.0), (6.5, 0.0), (8.0, 0.0)]
CH = [(0.0, 0.0), (2.7, 0.0), (3.1, 1.0), (6.5, 1.0), (7.0, 0.0), (8.0, 0.0)]          # the channel
ONT = [(0.0, 0.0), (1.449, 0.0), (1.45, 1.0), (6.449, 1.0), (6.45, 0.0), (8.0, 0.0)]  # words snap
OFFT = [(0.0, 1.0), (1.448, 1.0), (1.449, 0.0), (6.45, 0.0), (6.451, 1.0), (8.0, 1.0)]
CHT = [(0.0, 0.0), (3.099, 0.0), (3.1, 1.0), (6.799, 1.0), (6.8, 0.0), (8.0, 0.0)]
NCT = [(0.0, 1.0), (3.098, 1.0), (3.099, 0.0), (6.8, 0.0), (6.801, 1.0), (8.0, 1.0)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-6 svgd-part1-6">')
a('<title id="svgt-part1-6">Fig 1.5 · Inside the switch · a field-effect transistor in cross-section</title>')
a('<desc id="svgd-part1-6">A slab of p-type silicon with two n-type regions, the source and the drain, and between them a gate resting on a thin insulating oxide. '
  'With the gate at 0 V there is no path. A positive gate voltage acts through the oxide as a field, pulls electrons up into a thin channel under it, and current flows from source to drain.</desc>')

# terminals
for x, name in ((72, 'source'), (328, 'drain')):
    a(text(x, 30, name, anchor='middle', fill='rgba(255,255,255,0.7)'))
    a(f'<line x1="{x}" y1="38" x2="{x}" y2="134" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    a(f'<rect x="{x - 20}" y="134" width="40" height="20" rx="2" fill="#8d8d8d"/>')
a(f'<rect x="168" y="14" width="64" height="26" rx="13" fill="#1a1a1a" stroke="rgba(255,255,255,0.25)"/>')
a(f'<text x="200" y="32" text-anchor="middle" {MONO} font-size="14" fill="rgba(255,255,255,0.6)">0 V{T.anim("opacity", OFFT)}</text>')
a(f'<rect x="168" y="14" width="64" height="26" rx="13" fill="rgba(212,168,83,0.25)" stroke="{GOLD}" opacity="0">{T.anim("opacity", ONT)}</rect>')
a(f'<text x="200" y="32" text-anchor="middle" {MONO} font-size="14" fill="{GOLD}" opacity="0">+V{T.anim("opacity", ONT)}</text>')
a('<line x1="200" y1="40" x2="200" y2="92" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
a(f'<line x1="200" y1="40" x2="200" y2="92" stroke="{GOLD}" stroke-width="2.5" opacity="0">{T.anim("opacity", ON)}</line>')

# the slab
a(f'<rect x="20" y="154" width="360" height="168" rx="4" fill="{RED}" fill-opacity="0.13" stroke="{RED}" stroke-opacity="0.4"/>')
a(text(200, 308, 'p-type silicon', anchor='middle', fill='rgba(236,141,141,0.9)'))
for x0 in (30, 276):
    a(f'<path d="M {x0} 154 V 190 Q {x0} 210 {x0 + 20} 210 H {x0 + 74} Q {x0 + 94} 210 {x0 + 94} 190 V 154 Z" fill="{BLUE}" fill-opacity="0.24" stroke="{BLUE}" stroke-opacity="0.6"/>')
    a(text(x0 + 47, 192, 'n+', anchor='middle', fill=BLUE))
# gate on oxide
a('<rect x="124" y="92" width="152" height="42" rx="3" fill="#5c4d33" stroke="rgba(212,168,83,0.7)"/>')
a(text(200, 119, 'gate', anchor='middle', fill='#f3e7cc'))
a('<rect x="124" y="134" width="152" height="20" fill="#cfdde6" fill-opacity="0.55"/>')
a(f'<text x="200" y="149" text-anchor="middle" {MONO} font-size="13" fill="#10151a">oxide</text>')
# the field: through the insulator, not a current
g = [f'<g opacity="0">{T.anim("opacity", ON)}']
for x in (146, 254):
    g.append(f'<path d="M {x} 124 V 152" stroke="{GOLD}" stroke-width="2" stroke-dasharray="3 3"/><polygon points="{x - 4},148 {x + 4},148 {x},155" fill="{GOLD}"/>')
g.append('</g>'); a(''.join(g))

# electrons: scattered in the body, gathered up under the oxide when the gate is on
import random
rnd = random.Random(7)
for k in range(9):
    x = 136 + k * 16
    y0 = rnd.randint(224, 286)
    a(f'<circle cx="{x}" r="3.2" fill="{BLUE}">{T.anim("cy", [(0.0, y0), (1.6, y0), (2.9 + k * 0.03, 160), (6.5, 160), (7.6, y0), (8.0, y0)])}</circle>')
# the channel, and current along it
a(f'<rect x="124" y="155" width="152" height="11" fill="{BLUE}" opacity="0">{T.anim("opacity", [(t, v * 0.55) for t, v in CH])}</rect>')
g = [f'<g opacity="0">{T.anim("opacity", CH)}']
for k in range(7):
    g.append(f'<circle cy="160" r="3" fill="#fff"><animate attributeName="cx" values="76;324" dur="1.6s" begin="-{k * 1.6 / 7:.2f}s" repeatCount="indefinite"/></circle>')
g.append('</g>'); a(''.join(g))

# what is happening, in words that snap with the state
a(f'<text x="200" y="350" text-anchor="middle" {MONO} font-size="15" fill="rgba(255,255,255,0.6)">no path · no current{T.anim("opacity", NCT)}</text>')
a(f'<text x="200" y="350" text-anchor="middle" {MONO} font-size="15" fill="{GOLD}" opacity="0">channel · current flows{T.anim("opacity", CHT)}</text>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A positive voltage on the gate pulls electrons up under the oxide until they form a thin channel between source and drain, and current flows. '
           'The gate never touches the channel: its field reaches through the insulator, which is why these are called field-effect transistors.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The silicon.</b> The body is p-type silicon, doped with electron-accepting atoms; the source and drain are n-type, rich in free electrons. With the gate off, nothing joins them.</li>
          <li><b>The field.</b> The gate's voltage acts across the oxide as an electric field. No charge crosses the insulator.</li>
          <li><b>The channel.</b> The field gathers electrons under the oxide until that thin layer inverts, from p-type to n-type, and conducts.</li>
          <li><b>The name.</b> MOSFET: metal-oxide-semiconductor field-effect transistor. Every modern CPU is a stack of these about 3 nanometres wide.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-5">
      <div class="diagram-label">Fig 1.5 · Inside the switch · a field-effect transistor in cross-section</div>
      {svg}
      <p id="ch1-transistor-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-5', 'ch1-transistor-p8', card)
