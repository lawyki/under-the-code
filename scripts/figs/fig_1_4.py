# Fig 1.4 · Transistor as a switch (Pass 31, 2026-11-04 refinement). Job: function. Takeaway: a small voltage on a
# transistor's base lets a large current light the lamp, doing a glowing tube's job.
# Concept: one lamp circuit, the base switched between 0 V and 0.7 V (the reader can hold either with the steps). The
# moving dots are the current, flowing the way the emitter's arrow points: out of the battery's + side, through the
# lamp, collector to emitter, back to the - side (owner, 2026-11-04: electrons drawn against the arrow read backwards).
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 300
INK, WIRE = '#ece6da', 'rgba(255,255,255,0.55)'
T = Timeline(6, shift=4.0)
ON = [(0.0, 0.0), (2.9, 0.0), (3.0, 1.0), (5.9, 1.0), (6.0, 0.0)]
OFF = [(t, 1 - v) for t, v in ON]
def disc(pts): return T.discrete('opacity', [(t, v) for t, v in pts])
XC, XB = 226, 320                         # collector/emitter line, battery line
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-5 svgd-part1-5"'
  f'{T.steps([(1.5, "0 V"), (4.5, "0.7 V")])}>')
a('<title id="svgt-part1-5">Fig 1.4 · Transistor as a switch · base off, base on</title>')
a('<desc id="svgd-part1-5">A battery, a lamp and a transistor in one loop, with a wire to the transistor\'s base. With 0 volts on the base '
  'no current flows between collector and emitter and the lamp is dark. With 0.7 volts on the base current flows round the loop, out of '
  'the battery\'s plus side, through the lamp and the transistor from collector to emitter, the way the emitter\'s arrow points, and the '
  'lamp lights.</desc>')

loop = f'M {XB} 140 V 26 H {XC} V 134 M {XC} 196 V 258 H {XB} V 160'
a(f'<path d="{loop}" fill="none" stroke="{WIRE}" stroke-width="2.4"/>')
a(f'<path d="{loop}" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{disc(ON)}</path>')
# the battery, long plate (+) on top
a(f'<line x1="{XB - 18}" y1="142" x2="{XB + 18}" y2="142" stroke="{INK}" stroke-width="2.6"/>')
a(f'<line x1="{XB - 10}" y1="156" x2="{XB + 10}" y2="156" stroke="{INK}" stroke-width="4.5"/>')
a(text(XB + 26, 140, '+', size=16, fill=INK)); a(text(XB + 26, 166, '−', size=16, fill=INK))
# the lamp
LY = 64
a(f'<circle cx="{XC}" cy="{LY}" r="17" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.6">{disc(OFF)}</circle>')
a(f'<g opacity="0">{disc(ON)}<circle cx="{XC}" cy="{LY}" r="17" fill="{GOLD}"/>'
  f'<g stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round">' + ''.join(
      f'<line x1="{XC + 23 * c:.1f}" y1="{LY + 23 * s:.1f}" x2="{XC + 31 * c:.1f}" y2="{LY + 31 * s:.1f}"/>'
      for c, s in ((-1, 0), (-0.71, -0.71), (0.71, -0.71), (1, 0))) + '</g></g>')
a(f'<path d="M {XC - 7} {LY + 4} l 3.5 -8 l 3.5 8 l 3.5 -8 l 3.5 8" fill="none" stroke="#8a7a5a" stroke-width="1.8" stroke-linejoin="round"/>')
# the transistor
a(f'<circle cx="{XC - 12}" cy="165" r="38" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"/>')
a(f'<line x1="{XC - 26}" y1="144" x2="{XC - 26}" y2="186" stroke="{INK}" stroke-width="3.4"/>')
a(f'<path d="M {XC - 26} 155 L {XC} 136 V 134 M {XC - 26} 175 L {XC} 194 V 196" fill="none" stroke="{INK}" stroke-width="2.2"/>')
a(f'<path d="M {XC - 1} 193 l -11 -1 l 5 -8 z" fill="{INK}"/>')
# the base wire and its voltage
a(f'<line x1="104" y1="165" x2="{XC - 26}" y2="165" stroke="{WIRE}" stroke-width="2.2">{disc(OFF)}</line>')
a(f'<line x1="104" y1="165" x2="{XC - 26}" y2="165" stroke="{GOLD}" stroke-width="2.4" opacity="0">{disc(ON)}</line>')
a(f'<rect x="30" y="150" width="74" height="30" rx="15" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5">{disc(OFF)}</rect>')
a(f'<rect x="30" y="150" width="74" height="30" rx="15" fill="{GOLD}" opacity="0">{disc(ON)}</rect>')
a(f'<text data-role="object" x="67" y="170" text-anchor="middle" font-family="DM Mono" font-size="15" fill="{MUTED}">{disc(OFF)}0 V</text>')
a(f'<text data-role="object" x="67" y="170" text-anchor="middle" font-family="DM Mono" font-size="15" fill="#1a1407" opacity="0">{disc(ON)}0.7 V</text>')
a(text(67, 140, 'base', anchor='middle', size=14, fill=INK))
a(text(XC - 8, 110, 'collector', anchor='end', size=14, fill=MUTED))
a(text(XC + 10, 222, 'emitter', size=14, fill=MUTED))
# the current, moving the way the arrow points
path = f'M {XB} 140 V 26 H {XC} V 134 L {XC - 26} 155 L {XC - 26} 175 L {XC} 194 V 258 H {XB} V 160'
dots = ''.join(f'<circle r="3.4" fill="{GOLD}"><animateMotion dur="3s" begin="{-k * 0.375:.3f}s" repeatCount="indefinite" path="{path}"/></circle>' for k in range(8))
a(f'<g opacity="0">{disc(ON)}{dots}</g>')
a('</svg>')
svg = '\n'.join(l for l in o if 'opacity="0">no current' not in l)

caption = 'Switch the base between 0 V and 0.7 V and watch the lamp.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Three terminals.</b> Collector and emitter carry the current; the base controls it.</li>
          <li><b>The loop.</b> The battery pushes current round the loop, through the lamp and the transistor. The transistor is the one gap in it: shut, the whole loop is dead.</li>
          <li><b>The threshold.</b> In this kind of transistor about 0.7 V on the base opens the path; below it, almost nothing flows. In the field-effect transistors of modern chips the control terminal is called the gate (Fig 1.5).</li>
          <li><b>The dots.</b> The current, drawn the way the emitter's arrow points, from + round to −. The electrons that carry it drift the other way.</li>
          <li><b>The other kind.</b> This is the older kind of transistor; modern chips are built from the field-effect kind (Fig 1.5).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-4">
      <div class="diagram-label">Fig 1.4 · Transistor as a switch · base off, base on</div>
      {svg}
      <p id="ch1-transistor-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-4', 'ch1-transistor-p6', card)
