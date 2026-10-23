# Fig 8.1 · One signal, two scales (Pass 28, law 3). Chart Room. Two panels in continuous flow: a pulse
# crosses a micrometre of chip wiring and arrives unchanged; a pulse crosses 5,600 km of ocean, fading
# with distance and restored at each repeater. t=0 (shift): both pulses in flight.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 300
D = 5.0
T = Timeline(D, shift=2.2)
F0, F1 = 0.4, 4.4                      # flight time of each pulse (story)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-2 svgd-part3-2">')
a('<title id="svgt-part3-2">Fig 8.1 · One signal, two scales</title>')
a('<desc id="svgd-part3-2">Two panels. Inside a chip, a pulse crosses about a micrometre of copper wiring from one gate to the next and arrives unchanged. '
  'Under the ocean, a pulse of light crosses about 5,600 km of glass fibre from New York to London, taking about 28 milliseconds; it fades as it travels and is restored at each repeater along the way, arriving weakened and noisy but still readable. '
  'The two distances are more than twelve orders of magnitude apart.</desc>')
def flight(x0, x1):
    return T.translate([(0.0, 0.0), (F0, 0.0), (F1, x1 - x0), (D, x1 - x0)], 'x')
def fade(pts):
    return T.anim('opacity', [(0.0, 0.0), (F0 - 0.01, 0.0), (F0, 1.0)] + pts + [(F1, 1.0), (F1 + 0.05, 0.0), (D, 0.0)])
# chip
a(text(20, 24, 'INSIDE A CHIP', size=13, fill=CMUTED))
for x, lab in ((24, 'gate'), (316, 'gate')):
    a(f'<rect x="{x}" y="44" width="60" height="40" rx="2" fill="{CDEEP}" stroke="{CYAN}" stroke-opacity="0.7"/>')
    a(text(x + 30, 69, lab, anchor='middle', size=13, fill=CSOFT, ls='0'))
a(f'<line x1="84" y1="64" x2="316" y2="64" stroke="{CYAN}" stroke-width="2" stroke-opacity="0.6"/>')
a(text(200, 54, '≈ 1 µm of copper', anchor='middle', size=13, fill=CSOFT, ls='0'))
a(f'<g opacity="0">{fade([])}<g>{flight(90, 310)}<circle cx="90" cy="64" r="7" fill="{CYAN}"/></g></g>')
a(text(200, 106, 'arrives unchanged', anchor='middle', size=13, fill=CYAN, ls='0'))
# ocean
a(text(20, 146, 'UNDER THE OCEAN', size=13, fill=CMUTED))
FX0, FX1, FY = 72, 328, 194
a(text(20, FY + 5, 'NYC', size=13, fill=CSOFT, ls='0'))
a(text(380, FY + 5, 'LON', anchor='end', size=13, fill=CSOFT, ls='0'))
a(f'<line x1="{FX0}" y1="{FY}" x2="{FX1}" y2="{FY}" stroke="{ROUTE}" stroke-width="2" stroke-opacity="0.7" stroke-dasharray="8 6">'
  f'<animate attributeName="stroke-dashoffset" values="0;-28" dur="1.4s" repeatCount="indefinite"/></line>')
REP = [FX0 + (FX1 - FX0) * k / 5 for k in range(1, 5)]
for x in REP:
    a(f'<rect x="{x - 5}" y="{FY - 5}" width="10" height="10" fill="{CPLATE}" stroke="{ROUTE}" stroke-width="1.5" transform="rotate(45 {x} {FY})"/>')
a(text(200, FY - 22, 'repeaters', anchor='middle', size=13, fill=ROUTE, ls='0'))
# the light pulse: shrinks between repeaters, restored at each
seg = (F1 - F0) / 5
rpts = [(0.0, 7.0)]
for k in range(5):
    t0 = F0 + k * seg
    rpts += [(t0, 7.0), (t0 + seg - 0.01, 2.6)]
rpts += [(F1, 2.6), (D, 7.0)]
a(f'<g opacity="0">{fade([])}<g>{flight(FX0, FX1)}<circle cx="{FX0}" cy="{FY}" r="7" fill="{CYAN}">{T.anim("r", rpts)}</circle></g></g>')
a(text(200, FY + 32, '≈ 5,600 km of glass · ≈ 28 ms', anchor='middle', size=13, fill=CSOFT, ls='0'))
a(text(200, FY + 54, 'fades, is restored, arrives noisy', anchor='middle', size=13, fill=ROUTE, ls='0'))
a(text(200, FY + 76, 'but readable', anchor='middle', size=13, fill=ROUTE, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('A bit crossing a micrometre of chip wiring and a bit crossing 5,600 km of ocean are the same thing at scales a trillion times apart: a signal guided along a line, in copper or in glass. On the chip it arrives unchanged; under the sea it fades with distance, and repeaters every 50 to 100 km restore it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The speed.</b> Light in fibre travels at about two-thirds of its speed in vacuum, so New York to London takes about 28 ms one way.</li>
          <li><b>The repeaters.</b> Modern undersea repeaters amplify the light directly, in erbium-doped fibre, without turning it back into electricity.</li>
          <li><b>The voltage.</b> Processor cores run at around 1 V; the older 3.3 V and 5 V levels survive only at the edges of boards and chips.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-1">
      <div class="diagram-label">Fig 8.1 · One signal, two scales</div>
      {svg}
      <p id="ch8-bridge-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-1', 'ch8-bridge-p4', card)
