# Fig 1.4 · Transistor as a switch (Pass 28, law 3). Two of the same transistor:
# base at 0 V (no current) and at 0.7 V (current flows, the lamp lights). The still
# is the comparison itself; the motion is the electrons flowing in the one that is on.
from figlib import text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 330
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-5 svgd-part1-5">')
a('<title id="svgt-part1-5">Fig 1.4 · Transistor as a switch · base off, base on</title>')
a('<desc id="svgd-part1-5">Two identical transistors. On the left the base is at 0 volts: no current flows between collector and emitter and the lamp is dark. '
  'On the right the base is at 0.7 volts: electrons flow through and the lamp lights.</desc>')

def transistor(cx, on, labels):
    lx = cx + 14                                    # collector/emitter rail
    # supply and lamp
    a(f'<text x="{lx}" y="44" text-anchor="middle" {MONO} font-size="15" fill="rgba(255,255,255,0.6)">+</text>')
    a(f'<line x1="{lx}" y1="50" x2="{lx}" y2="62" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    a(f'<circle cx="{lx}" cy="78" r="15" fill="{GOLD if on else "#151515"}" stroke="{GOLD if on else "rgba(255,255,255,0.35)"}" stroke-width="1.5"/>')
    if on: a(f'<circle cx="{lx}" cy="78" r="27" fill="{GOLD}" opacity="0.18"/>')
    a(f'<path d="M {lx - 6} 82 l 3 -8 l 3 8 l 3 -8 l 3 8" fill="none" stroke="{"#0a0a0a" if on else "rgba(255,255,255,0.35)"}" stroke-width="1.4"/>')
    a(f'<line x1="{lx}" y1="93" x2="{lx}" y2="160" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    # the symbol
    a(f'<circle cx="{cx}" cy="190" r="36" fill="#161616" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>')
    a(f'<line x1="{cx - 12}" y1="170" x2="{cx - 12}" y2="210" stroke="#e8e8e8" stroke-width="3"/>')
    a(f'<line x1="{cx - 12}" y1="180" x2="{lx}" y2="160" stroke="#e8e8e8" stroke-width="2"/>')
    a(f'<line x1="{cx - 12}" y1="200" x2="{lx}" y2="220" stroke="#e8e8e8" stroke-width="2"/>')
    a(f'<polygon points="{lx},220 {lx - 11},218 {lx - 5},211" fill="#e8e8e8"/>')
    a(f'<line x1="{lx}" y1="220" x2="{lx}" y2="262" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    a(f'<path d="M {lx - 12} 262 H {lx + 12} M {lx - 7} 268 H {lx + 7} M {lx - 3} 274 H {lx + 3}" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
    # the base and its voltage
    col = GOLD if on else 'rgba(255,255,255,0.45)'
    a(f'<line x1="{cx - 72}" y1="190" x2="{cx - 12}" y2="190" stroke="{col}" stroke-width="{2.5 if on else 1.5}"/>')
    a(f'<circle cx="{cx - 72}" cy="190" r="4" fill="{col}"/>')
    a(f'<text x="{cx - 72}" y="176" {MONO} font-size="15" fill="{col}">{"0.7 V" if on else "0 V"}</text>')
    if labels:
        a(text(lx - 10, 140, 'collector', anchor='end', fill=MUTED))
        a(text(cx - 72, 216, 'base', fill=MUTED))
        a(text(lx - 10, 250, 'emitter', anchor='end', fill=MUTED))
    if on:   # electrons drift from emitter up to collector while the base is on
        g = ['<g>']
        for k in range(6):
            g.append(f'<circle cx="{lx}" r="3" fill="{BLUE}"><animate attributeName="cy" values="258;96" dur="1.4s" begin="-{k * 1.4 / 6:.2f}s" repeatCount="indefinite"/></circle>')
        g.append('</g>'); a(''.join(g))
    a(f'<text x="{cx}" y="312" text-anchor="middle" {MONO} font-size="15" fill="{GOLD if on else MUTED}">{"current flows" if on else "no current"}</text>')

transistor(96, False, True)
a('<line x1="200" y1="36" x2="200" y2="300" stroke="rgba(255,255,255,0.08)"/>')
transistor(296, True, False)
a('</svg>')
svg = '\n'.join(o)

caption = ('With no voltage on the base, no current flows between collector and emitter; with a small one, it does. '
           'Every computer is built from this one switch: a modern CPU holds roughly fifty billion of them.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Three terminals.</b> Collector and emitter carry the current; the base controls it.</li>
          <li><b>The threshold.</b> In this kind of transistor about 0.7 V on the base opens the path; below it, almost nothing flows. In the field-effect transistors of modern chips the base is called the gate.</li>
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
