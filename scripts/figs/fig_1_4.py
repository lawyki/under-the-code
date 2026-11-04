# Fig 1.4 · Transistor as a switch (Pass 31, Part I, from an empty script). Job: function. Takeaway: a small
# voltage on a transistor's base lets a large current light the lamp, doing a glowing tube's job.
# Concept: the same lamp circuit twice, a battery driving a loop through the lamp and the transistor. Left, 0 V on
# the base: the loop is dead and the lamp dark. Right, 0.7 V: electrons flow round the loop (Part I's flow verb)
# and the lamp is lit. The still is the comparison; the motion is only the current that the base lets through.
from figlib import text, splice, GOLD, BLUE, MUTED

W, H = 400, 330
INK, WIRE, DEAD = '#ece6da', 'rgba(255,255,255,0.55)', 'rgba(255,255,255,0.5)'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-5 svgd-part1-5">')
a('<title id="svgt-part1-5">Fig 1.4 · Transistor as a switch · base off, base on</title>')
a('<desc id="svgd-part1-5">The same circuit twice: a battery, a lamp and a transistor in one loop, with a wire to the transistor\'s '
  'base. Left, the base is at 0 volts: no current flows between collector and emitter and the lamp is dark. Right, the base is '
  'at 0.7 volts: electrons flow round the loop, through the transistor from emitter to collector, and the lamp lights.</desc>')

def panel(cx, on):
    xc = cx + 22                                   # the collector/emitter line
    wire = WIRE if on else DEAD
    loop = f'M {xc} 290 V 200 M {xc} 150 V 70 M {xc} 42 V 26 H {cx + 78} V 140 M {cx + 78} 156 V 290 H {xc}'
    a(f'<path d="{loop}" fill="none" stroke="{wire}" stroke-width="2"/>')
    if on: a(f'<path d="{loop}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.55"/>')
    # battery, long plate (+) on top
    a(f'<line x1="{cx + 64}" y1="142" x2="{cx + 92}" y2="142" stroke="{INK}" stroke-width="2.4"/>')
    a(f'<line x1="{cx + 70}" y1="154" x2="{cx + 86}" y2="154" stroke="{INK}" stroke-width="4"/>')
    a(text(cx + 98, 140, '+', size=14, fill=MUTED))
    # the lamp
    ly = 56
    if on:
        a(f'<circle cx="{xc}" cy="{ly}" r="14" fill="{GOLD}"/>')
        a(f'<g stroke="{GOLD}" stroke-width="2" stroke-linecap="round">' + ''.join(
            f'<line x1="{xc + 19 * c:.1f}" y1="{ly + 19 * s:.1f}" x2="{xc + 26 * c:.1f}" y2="{ly + 26 * s:.1f}"/>'
            for c, s in ((-1, 0), (-0.71, -0.71), (-0.71, 0.71))) + '</g>')
        zig = '#3a2c10'
    else:
        a(f'<circle cx="{xc}" cy="{ly}" r="14" fill="#151515" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>')
        zig = 'rgba(255,255,255,0.45)'
    a(f'<path d="M {xc - 6} {ly + 3} l 3 -7 l 3 7 l 3 -7 l 3 7" fill="none" stroke="{zig}" stroke-width="1.6" stroke-linejoin="round"/>')
    # the transistor: a circle with the base bar, collector above, emitter (arrow) below
    a(f'<circle cx="{cx + 10}" cy="175" r="30" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>')
    a(f'<line x1="{cx}" y1="158" x2="{cx}" y2="192" stroke="{INK}" stroke-width="3"/>')
    a(f'<path d="M {cx} 167 L {xc} 152 V 150 M {cx} 183 L {xc} 198 V 200" fill="none" stroke="{INK}" stroke-width="2"/>')
    a(f'<path d="M {xc - 2} 197 l -9 -1 l 4 -7 z" fill="{INK}"/>')
    # the base wire and its voltage pill
    a(f'<line x1="{cx - 22}" y1="175" x2="{cx}" y2="175" stroke="{GOLD if on else wire}" stroke-width="2"/>')
    pw = 60 if on else 50
    px = cx - 22 - pw
    if on:
        a(f'<rect x="{px}" y="162" width="{pw}" height="26" rx="13" fill="{GOLD}"/>')
        a(text(px + pw / 2, 180, '0.7 V', anchor='middle', size=14, fill='#1a1407', ls='0.02em'))
    else:
        a(f'<rect x="{px}" y="162" width="{pw}" height="26" rx="13" fill="none" stroke="rgba(255,255,255,0.45)"/>')
        a(text(px + pw / 2, 180, '0 V', anchor='middle', size=14, fill=MUTED, ls='0.02em'))
    if on:
        # electrons leave the battery's minus side, cross the transistor from emitter to collector, light the lamp
        path = f'M {cx + 78} 290 H {xc} V 198 L {cx} 183 L {cx} 167 L {xc} 152 V 26 H {cx + 78} V 290'
        for k in range(7):
            a(f'<circle r="3.2" fill="{BLUE}"><animateMotion dur="3.5s" begin="{-k * 0.5:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')
    a(text(cx + 22, 318, 'current flows' if on else 'no current', anchor='middle', size=15, fill=GOLD if on else MUTED))

panel(80, False)
panel(280, True)
# terminal names, once, on the left circuit
a(text(96, 118, 'collector', anchor='end', size=14, fill=INK))
a(text(40, 214, 'base', anchor='middle', size=14, fill=INK))
a(text(96, 246, 'emitter', anchor='end', size=14, fill=INK))
a('</svg>')
svg = '\n'.join(o)

caption = ('Left, 0 V on the base and the lamp stays dark; right, 0.7 V and it lights. This is the older kind of transistor; '
           'modern chips are built from the field-effect kind, opened in Fig 1.5.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Three terminals.</b> Collector and emitter carry the current; the base controls it.</li>
          <li><b>The loop.</b> The battery pushes current round the loop, through the lamp and the transistor. The transistor is the one gap in it: shut, the whole loop is dead.</li>
          <li><b>The threshold.</b> In this kind of transistor about 0.7 V on the base opens the path; below it, almost nothing flows. In the field-effect transistors of modern chips the control terminal is called the gate (Fig 1.5).</li>
          <li><b>The dots.</b> Electrons, drifting from emitter to collector for as long as the base signal is there.</li>
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
