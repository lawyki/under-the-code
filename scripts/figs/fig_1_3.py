# Fig 1.3 · The replacement (Pass 31, 2026-11-04 refinement). Job: real thing. Takeaway: a glowing tube and a small piece
# of crystal each let a small signal switch a large current.
# Concept: each device drawn as it looks inside its own circuit: a thick loop (battery, lamp, device) for the large
# current and one thin wire for the small signal, the same signal to both. Signal off: both lamps dark (the tube's
# electrons wait under the grid). Signal on: current flows round both loops and both lamps light. The reader can hold
# either state with the steps (owner, 2026-11-04: the first version was hard to read; the loops make "switch" visible).
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 344
INK, HEAT, WIRE = '#ece6da', '#f0a35a', 'rgba(255,255,255,0.55)'
T = Timeline(6, shift=4.0)
ON = [(0.0, 0), (2.9, 0), (3.0, 1)]
OFF = [(0.0, 1), (2.9, 1), (3.0, 0)]
def disc(pts): return T.discrete('opacity', pts)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-4 svgd-part1-4"'
  f'{T.steps([(1.5, "signal off"), (4.5, "signal on")])}>')
a('<title id="svgt-part1-4">Fig 1.3 · The replacement · the same switch, without the fire</title>')
a('<desc id="svgd-part1-4">Two circuits side by side, each a battery, a lamp and a switching device in one thick loop, and one thin wire '
  'carrying the same small signal to both devices. Left, a vacuum tube of 1906: a glass bulb with a filament glowing hot inside. Right, '
  'the first transistor, of 1947: a small plastic wedge pressing two gold contacts onto a sliver of crystal. With the signal off, no '
  'current flows and both lamps are dark; the tube\'s electrons wait below its grid. With the signal on, current flows round both '
  'loops and both lamps light.</desc>')

def lamp(cx, cy):
    a(f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5">{disc(OFF)}</circle>')
    a(f'<g opacity="0">{disc(ON)}<circle cx="{cx}" cy="{cy}" r="14" fill="{GOLD}"/><g stroke="{GOLD}" stroke-width="2" stroke-linecap="round">'
      + ''.join(f'<line x1="{cx + 19 * c:.1f}" y1="{cy + 19 * s:.1f}" x2="{cx + 26 * c:.1f}" y2="{cy + 26 * s:.1f}"/>'
                for c, s in ((-0.71, -0.71), (0, -1), (0.71, -0.71))) + '</g></g>')
    a(f'<path d="M {cx - 6} {cy + 3} l 3 -7 l 3 7 l 3 -7 l 3 7" fill="none" stroke="#8a7a5a" stroke-width="1.6" stroke-linejoin="round"/>')
def battery(x, y):
    a(f'<line x1="{x - 13}" y1="{y}" x2="{x + 13}" y2="{y}" stroke="{INK}" stroke-width="2.4"/>')
    a(f'<line x1="{x - 7}" y1="{y + 10}" x2="{x + 7}" y2="{y + 10}" stroke="{INK}" stroke-width="4"/>')
def loop(d):
    a(f'<path d="{d}" fill="none" stroke="{WIRE}" stroke-width="3.4" stroke-linejoin="round">{disc(OFF)}</path>')
    a(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="3.4" stroke-linejoin="round" opacity="0">{disc(ON)}</path>')
def flow(d, n, dur):
    a(f'<g opacity="0">{disc(ON)}' + ''.join(f'<circle r="3" fill="#fff3d6"><animateMotion dur="{dur}s" begin="{-k * dur / n:.2f}s" repeatCount="indefinite" path="{d}"/></circle>' for k in range(n)) + '</g>')

# ---------- the tube's circuit (left) ----------
TX = 112
lamp(TX, 40)
dT = f'M {TX} 54 V 96 M {TX} 226 V 266 H 28 V 186 M 28 166 V 20 H {TX} V 26'
loop(dT); battery(28, 168)
a(f'<path d="M {TX - 36} 214 V 112 A 36 36 0 0 1 {TX + 36} 112 V 214 Z" fill="none" stroke="rgba(220,230,240,0.7)" stroke-width="1.6"/>')
a(f'<rect x="{TX - 18}" y="96" width="36" height="12" rx="2" fill="#8d8d8d"/>')
a(f'<path d="M {TX - 24} 150 ' + ' '.join('q 3 -6 6 0' for _ in range(8)) + '" fill="none" stroke="#bdbdbd" stroke-width="1.5"/>')
a(f'<ellipse cx="{TX}" cy="190" rx="24" ry="11" fill="{HEAT}" opacity="0.25"/>')
a(f'<path d="M {TX - 15} 195 l 5 -9 l 5 9 l 5 -9 l 5 9 l 5 -9 l 5 9" fill="none" stroke="{HEAT}" stroke-width="2.4" stroke-linejoin="round"/>')
a(f'<rect x="{TX - 30}" y="214" width="60" height="12" rx="2" fill="#3a3a3a"/>')
a(f'<g opacity="0">{disc(OFF)}' + ''.join(f'<circle cx="{TX + dx}" cy="170" r="3" fill="{BLUE}"/>' for dx in (-12, 0, 12)) + '</g>')
a(f'<g opacity="0">{disc(ON)}' + ''.join(f'<circle cx="{TX - 8 + 8 * k}" cy="0" r="3" fill="{BLUE}"><animate attributeName="cy" values="180;112" dur="1s" begin="{-k * 0.33:.2f}s" repeatCount="indefinite"/></circle>' for k in range(3)) + '</g>')
a(text(TX, 300, 'vacuum tube', anchor='middle', size=15, fill=INK))
a(text(TX, 318, '1906', anchor='middle', size=14, fill=MUTED))

# ---------- the transistor's circuit (right) ----------
PX = 300
lamp(PX, 40)
dP = f'M {PX} 54 V 118 H {PX - 12} V 150 M {PX + 12} 150 V 118 H {PX + 50} V 266 H 372 V 186 M 372 166 V 20 H {PX} V 26'
loop(dP); battery(372, 168)
a(f'<path d="M {PX - 24} 140 H {PX + 24} L {PX + 4} 182 H {PX - 4} Z" fill="none" stroke="rgba(220,230,240,0.7)" stroke-width="1.5" stroke-linejoin="round"/>')
a(f'<path d="M {PX - 12} 150 L {PX - 3} 181 M {PX + 12} 150 L {PX + 3} 181" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"/>')
a(f'<rect x="{PX - 30}" y="182" width="60" height="14" rx="1.5" fill="#5f6674"/>')
a(f'<rect x="{PX - 38}" y="196" width="76" height="12" rx="2" fill="#8d8d8d"/>')
a(text(PX, 300, 'transistor', anchor='middle', size=15, fill=INK))
a(text(PX, 318, '1947', anchor='middle', size=14, fill=MUTED))

# ---------- the one small signal ----------
SIG = f'M 200 150 H {TX + 36} M 200 150 V 202 H {PX - 38}'
a(f'<path d="{SIG}" fill="none" stroke="{WIRE}" stroke-width="1.4">{disc(OFF)}</path>')
a(f'<path d="{SIG}" fill="none" stroke="{GOLD}" stroke-width="1.6" opacity="0">{disc(ON)}</path>')
a(f'<circle cx="200" cy="150" r="5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
a(text(207, 176, 'small', size=14, fill=GOLD))
a(text(207, 193, 'signal', size=14, fill=GOLD))
a(text(200, 240, 'large current', anchor='middle', size=14, fill=INK, extra=' opacity="0"'))
flow(dT, 8, 4); flow(dP, 8, 4)
a('</svg>')
svg = '\n'.join(l for l in o if "large current" not in l)

caption = ('A vacuum tube and a transistor do the same job: a small control signal (the thin wire) decides whether a much larger current '
           '(the thick loop) flows. The transistor does it in a sliver of crystal, with no glass, no glowing filament and nothing to burn out.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tube.</b> A filament, kept hot, boils electrons off; the plate at the top draws them across the vacuum; the grid between them, a coil of fine wire set by the control signal, lets them through or holds them back.</li>
          <li><b>Transistor.</b> The first one, built at Bell Labs in 1947: a plastic wedge presses two gold contacts onto a crystal of germanium. A small control signal between one contact and the metal base under the crystal lets a much larger current flow through the other (the next figures open the switch).</li>
          <li><b>Why it won.</b> A tube is hot, fragile and wears out: one of ENIAC's 17,468 tubes failed about every two days. A transistor has nothing to burn out, and it shrinks.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-3">
      <div class="diagram-label">Fig 1.3 · The replacement · the same switch, without the fire</div>
      {svg}
      <p id="ch1-transistor-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-3', 'ch1-transistor-p3', card)
