# Fig 1.3 · The replacement (Pass 31, Part I, from an empty script). Job: real thing. Takeaway: a glowing tube
# and a small piece of crystal each let a small signal switch a large current. Drawn as they look: a glass tube
# on its pins, filament glowing, and the 1947 point-contact transistor (a plastic wedge pressing two gold
# contacts onto a germanium crystal on its metal base). One small signal feeds both; when it is on, both lamps
# light. t=0 is the on state, so the still is the whole story.
from figlib import Timeline, text, obj, splice, GOLD, BLUE, MUTED

W, H = 400, 340
INK, HEAT, WIRE = '#ece6da', '#f0a35a', 'rgba(255,255,255,0.55)'
T = Timeline(6, shift=0.0)
ON = [(0.0, 1.0), (3.6, 1.0), (3.8, 0.0), (5.6, 0.0), (5.8, 1.0)]          # the small signal: on, then off a while
OFF = [(t, 1.0 - v) for t, v in ON]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-4 svgd-part1-4">')
a('<title id="svgt-part1-4">Fig 1.3 · The replacement · the same switch, without the fire</title>')
a('<desc id="svgd-part1-4">Left, a vacuum tube of 1906: a glass bulb on metal pins with a filament glowing hot inside. Right, the '
  'first transistor, of 1947: a small plastic wedge pressing two gold contacts onto a sliver of crystal on a metal base. One small '
  'signal is wired to both. While it is on, electrons cross the tube and current crosses the crystal, and both lamps light; when it '
  'goes off, both lamps go dark, though the filament stays hot.</desc>')

def lamp(cx, cy):
    """The Part I lamp: dark outline when off, gold with rays while the signal is on."""
    a(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#151515" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>')
    rays = ''.join(f'<line x1="{cx + 19 * c:.1f}" y1="{cy + 19 * s:.1f}" x2="{cx + 26 * c:.1f}" y2="{cy + 26 * s:.1f}"/>'
                   for c, s in ((-1, 0), (1, 0), (-0.71, -0.71), (0.71, -0.71), (0, -1)))
    a(f'<g opacity="0">{T.anim("opacity", ON)}<circle cx="{cx}" cy="{cy}" r="14" fill="{GOLD}"/>'
      f'<g stroke="{GOLD}" stroke-width="2" stroke-linecap="round">{rays}</g></g>')
    a(f'<path d="M {cx - 6} {cy + 3} l 3 -7 l 3 7 l 3 -7 l 3 7" fill="none" stroke="#3a2c10" stroke-width="1.6" stroke-linejoin="round"/>')

# ---------- the tube (centre x 100) ----------
TX = 100
lamp(TX, 44)
a(f'<line x1="{TX}" y1="58" x2="{TX}" y2="104" stroke="{WIRE}" stroke-width="2" opacity="0">{T.anim("opacity", OFF)}</line>')
a(f'<line x1="{TX}" y1="58" x2="{TX}" y2="104" stroke="{GOLD}" stroke-width="2" opacity="0">{T.anim("opacity", ON)}</line>')
# glass envelope with a soft highlight
a(f'<path d="M {TX - 38} 250 V 128 A 38 38 0 0 1 {TX + 38} 128 V 250 Z" fill="none" stroke="rgba(220,230,240,0.6)" stroke-width="1.6"/>')
a(f'<path d="M {TX - 28} 236 V 132 A 28 28 0 0 1 {TX - 12} 106" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="3" stroke-linecap="round"/>')
# the plate (catches electrons), the grid (a coil of fine wire), the filament (always hot)
a(f'<rect x="{TX - 20}" y="112" width="40" height="16" rx="2" fill="#8d8d8d" stroke="#bdbdbd"/>')
a(f'<line x1="{TX}" y1="104" x2="{TX}" y2="112" stroke="#bdbdbd" stroke-width="2"/>')
a(f'<path d="M {TX - 26} 176 ' + ' '.join(f'q 3.25 -6 6.5 0' for _ in range(8)) + '" fill="none" stroke="#bdbdbd" stroke-width="1.5"/>')
a(f'<ellipse cx="{TX}" cy="214" rx="26" ry="13" fill="{HEAT}" opacity="0.22"/>')
a(f'<path d="M {TX - 18} 220 l 6 -10 l 6 10 l 6 -10 l 6 10 l 6 -10 l 6 10" fill="none" stroke="{HEAT}" stroke-width="2.4" stroke-linejoin="round"/>')
# electrons boil off the filament and cross to the plate only while the signal is on
dots = []
for k in range(4):
    dots.append(f'<circle cx="{TX - 9 + k * 6}" cy="0" r="3" fill="{BLUE}"><animate attributeName="cy" values="204;132" '
                f'dur="1.2s" begin="{-k * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
a(f'<g>{T.anim("opacity", ON)}{"".join(dots)}</g>')
# while the signal is off the grid holds them back: they wait below it
a(f'<g opacity="0">{T.anim("opacity", OFF)}' + ''.join(f'<circle cx="{TX + dx}" cy="194" r="3" fill="{BLUE}"/>' for dx in (-12, -2, 9)) + '</g>')
# base and pins
a(f'<rect x="{TX - 34}" y="250" width="68" height="20" rx="3" fill="#2a2a2a" stroke="rgba(255,255,255,0.35)"/>')
for dx in (-20, -7, 7, 20):
    a(f'<line x1="{TX + dx}" y1="270" x2="{TX + dx}" y2="282" stroke="#9a9a9a" stroke-width="2.4" stroke-linecap="round"/>')
a(text(TX + 44, 222, 'filament,', size=14, fill=HEAT))
a(text(TX + 44, 239, 'always hot', size=14, fill=HEAT))
a(text(TX, 310, 'vacuum tube', anchor='middle', size=15, fill=INK))
a(text(TX, 328, '1906', anchor='middle', size=14, fill=MUTED))

# ---------- the transistor (centre x 300), the 1947 point-contact device ----------
PX = 300
lamp(PX, 44)
a(f'<line x1="{PX}" y1="58" x2="{PX}" y2="170" stroke="{WIRE}" stroke-width="2" opacity="0">{T.anim("opacity", OFF)}</line>')
a(f'<line x1="{PX}" y1="58" x2="{PX}" y2="170" stroke="{GOLD}" stroke-width="2" opacity="0">{T.anim("opacity", ON)}</line>')
# the plastic wedge, with gold foil down its two faces meeting the crystal
a(f'<path d="M {PX - 22} 170 H {PX + 22} L {PX + 3} 214 H {PX - 3} Z" fill="rgba(200,210,230,0.10)" stroke="rgba(220,230,240,0.6)" stroke-width="1.5" stroke-linejoin="round"/>')
a(f'<path d="M {PX - 22} 171 L {PX - 3} 213 M {PX + 22} 171 L {PX + 3} 213" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>')
# the crystal on its metal base
a(f'<rect x="{PX - 30}" y="214" width="60" height="14" rx="1.5" fill="#5f6674" stroke="#9aa3b4"/>')
a(f'<line x1="{PX - 26}" y1="217" x2="{PX - 8}" y2="217" stroke="rgba(255,255,255,0.35)" stroke-width="1.4"/>')
a(f'<rect x="{PX - 40}" y="228" width="80" height="12" rx="2" fill="#8d8d8d" stroke="#bdbdbd"/>')
# current crosses the crystal while the signal is on
a(f'<g opacity="0">{T.anim("opacity", ON)}<circle cx="{PX}" cy="221" r="9" fill="{GOLD}" opacity="0.3"/>'
  f'<circle cx="{PX}" cy="0" r="3" fill="{BLUE}"><animate attributeName="cy" values="166;212" dur="0.9s" repeatCount="indefinite"/></circle>'
  f'<circle cx="{PX}" cy="0" r="3" fill="{BLUE}"><animate attributeName="cy" values="166;212" dur="0.9s" begin="-0.45s" repeatCount="indefinite"/></circle></g>')
a(text(PX + 36, 260, 'crystal', anchor='middle', size=14, fill=INK))
a(text(PX, 310, 'transistor', anchor='middle', size=15, fill=INK))
a(text(PX, 328, '1947', anchor='middle', size=14, fill=MUTED))

# ---------- the one small signal, to the tube's grid and the transistor's base ----------
SIG = f'M 170 173 H {TX + 26} M 230 173 H 250 V 234 H {PX - 40}'
a(f'<path d="{SIG}" fill="none" stroke="{WIRE}" stroke-width="2" opacity="0">{T.anim("opacity", OFF)}</path>')
a(f'<path d="{SIG}" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{T.anim("opacity", ON)}</path>')
a(f'<rect x="170" y="160" width="60" height="26" rx="13" fill="none" stroke="rgba(255,255,255,0.55)"/>')
a(f'<g opacity="0">{T.anim("opacity", ON)}<rect x="170" y="160" width="60" height="26" rx="13" fill="{GOLD}"/></g>')
a(f'<text x="200" y="178" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#1a1407" opacity="0">on{T.anim("opacity", ON)}</text>')
a(f'<text x="200" y="178" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="{MUTED}" opacity="0">off{T.anim("opacity", OFF)}</text>')
a(text(200, 132, 'small', anchor='middle', size=14, fill=GOLD))
a(text(200, 149, 'signal', anchor='middle', size=14, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('A vacuum tube and a transistor do the same job: a small control signal decides whether a much larger current flows. '
           'The transistor does it in a sliver of crystal, with no glass, no glowing filament and nothing to burn out.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tube.</b> A filament, kept hot, boils electrons off; the plate at the top draws them across the vacuum; the grid between them, a coil of fine wire set by the control signal, lets them through or holds them back.</li>
          <li><b>Transistor.</b> The first one, built at Bell Labs in 1947: a plastic wedge presses two gold contacts onto a crystal of germanium. A small control signal between one contact and the metal base under the crystal lets a much larger current flow out through the other contact (the next figures open the switch).</li>
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
