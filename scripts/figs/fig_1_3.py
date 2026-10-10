# Fig 1.3 · The replacement (Pass 28, law 3). Two switches on one control signal:
# when it turns on, electrons flow and both lamps light. The tube needs a filament
# kept glowing hot; the transistor is a sliver of silicon. t=0: signal on.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 392
HEAT = '#f0a35a'
T = Timeline(6, shift=3.0)
ON = [(0.0, 0.0), (1.4, 0.0), (1.6, 1.0), (4.9, 1.0), (5.1, 0.0), (6.0, 0.0)]   # control signal
ON_TXT = [(0.0, 0.0), (1.499, 0.0), (1.5, 1.0), (4.999, 1.0), (5.0, 0.0), (6.0, 0.0)]   # the words snap
OFF_TXT = [(0.0, 1.0), (1.498, 1.0), (1.499, 0.0), (5.0, 0.0), (5.001, 1.0), (6.0, 1.0)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-4 svgd-part1-4">')
a('<title id="svgt-part1-4">Fig 1.3 · Vacuum tube and transistor · the same switch</title>')
a('<desc id="svgd-part1-4">One small control signal drives both devices. When it turns on, electrons flow and both lamps light. '
  'In the vacuum tube a filament, kept glowing hot, boils off electrons that reach the plate only when the grid lets them through. '
  'In the transistor the control goes to the base of a small piece of silicon and current flows through it.</desc>')

def lamp(cx, cy):
    a(f'<circle cx="{cx}" cy="{cy}" r="15" fill="#151515" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{GOLD}" opacity="0">{T.anim("opacity", ON)}</circle>')
    a(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{GOLD}" opacity="0">{T.anim("opacity", [(t, v * 0.18) for t, v in ON])}</circle>')
    a(f'<path d="M {cx - 6} {cy + 4} l 3 -8 l 3 8 l 3 -8 l 3 8" fill="none" stroke="#0a0a0a" stroke-width="1.4" opacity="0.8"/>')

def electrons(x, y0, y1, n=4, period=1.0, wobble=0):
    g = [f'<g opacity="0">{T.anim("opacity", ON)}']
    for k in range(n):
        g.append(f'<circle cx="{x + (k % 2) * wobble - wobble / 2:g}" cy="{y0}" r="3" fill="{BLUE}">'
                 f'<animate attributeName="cy" values="{y0};{y1}" dur="{period}s" begin="-{k * period / n:.2f}s" repeatCount="indefinite"/></circle>')
    g.append('</g>'); a(''.join(g))

# headings
a(text(90, 26, 'VACUUM TUBE', anchor='middle', fill='rgba(255,255,255,0.75)'))
a(text(90, 44, '1906', anchor='middle', fill=MUTED))
a(text(315, 26, 'TRANSISTOR', anchor='middle', fill='rgba(255,255,255,0.75)'))
a(text(315, 44, '1947', anchor='middle', fill=MUTED))

# --- the tube (left) ---
lamp(90, 80)
a('<line x1="90" y1="95" x2="90" y2="128" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
a('<rect x="58" y="112" width="64" height="176" rx="32" fill="rgba(160,190,220,0.06)" stroke="rgba(200,220,240,0.45)" stroke-width="1.5"/>')
a('<rect x="70" y="128" width="40" height="8" rx="2" fill="#9a9a9a"/>')                       # plate
a('<line x1="66" y1="206" x2="114" y2="206" stroke="#bdbdbd" stroke-width="2" stroke-dasharray="5 4"/>')   # grid
a(f'<path d="M 72 262 l 6 -8 l 6 8 l 6 -8 l 6 8 l 6 -8 l 6 8" fill="none" stroke="{HEAT}" stroke-width="2.4"/>')  # filament
a(f'<ellipse cx="90" cy="258" rx="30" ry="14" fill="{HEAT}" opacity="0.22"><animate attributeName="opacity" values="0.16;0.3;0.16" dur="1.6s" repeatCount="indefinite"/></ellipse>')
electrons(90, 252, 140, n=5, period=0.9, wobble=14)
a(text(132, 136, 'plate', fill=MUTED))
a(text(132, 211, 'grid', fill=MUTED))
a(text(132, 254, 'filament,', fill=HEAT))
a(text(132, 272, 'always hot', fill=HEAT))
# control into the grid
a('<path d="M 66 206 H 20 V 326" fill="none" stroke="rgba(212,168,83,0.35)" stroke-width="2"/>')

# --- the transistor (right) ---
lamp(315, 80)
a('<line x1="315" y1="95" x2="315" y2="186" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
a('<line x1="315" y1="214" x2="315" y2="288" stroke="rgba(255,255,255,0.45)" stroke-width="1.5"/>')
a('<rect x="299" y="186" width="32" height="28" rx="3" fill="#2a2620" stroke="rgba(212,168,83,0.7)" stroke-width="1.5"/>')   # silicon
electrons(315, 284, 98, n=6, period=1.2)
a(text(324, 236, 'silicon', fill=MUTED))
a(text(254, 192, 'base', anchor='middle', fill=MUTED))
a('<path d="M 299 200 H 236 V 326" fill="none" stroke="rgba(212,168,83,0.35)" stroke-width="2"/>')

# --- the one control signal ---
a('<path d="M 20 326 H 236" fill="none" stroke="rgba(212,168,83,0.35)" stroke-width="2"/>')
a(f'<path d="M 66 206 H 20 V 326 H 236 V 200 H 299" fill="none" stroke="{GOLD}" stroke-width="2.5" opacity="0">{T.anim("opacity", ON)}</path>')
a(text(20, 356, 'SMALL CONTROL SIGNAL', fill=MUTED))
a(f'<rect x="268" y="338" width="64" height="26" rx="13" fill="#1a1a1a" stroke="rgba(255,255,255,0.25)"/>')
a(f'<text x="300" y="356" text-anchor="middle" {MONO} font-size="14" fill="rgba(255,255,255,0.55)">off{T.anim("opacity", OFF_TXT)}</text>')
a(f'<rect x="268" y="338" width="64" height="26" rx="13" fill="rgba(212,168,83,0.25)" stroke="{GOLD}" opacity="0">{T.anim("opacity", ON)}</rect>')
a(f'<text x="300" y="356" text-anchor="middle" {MONO} font-size="14" fill="{GOLD}" opacity="0">on{T.anim("opacity", ON_TXT)}</text>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A vacuum tube and a transistor do the same job: a small control signal decides whether a much larger current flows. '
           'The transistor does it in a sliver of silicon, with no glass, no glowing filament and nothing to burn out.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tube.</b> A filament, kept hot, boils electrons off; the plate draws them across the vacuum; the grid between them, set by the control signal, lets them through or holds them back.</li>
          <li><b>Transistor.</b> The control signal goes to the base, and current flows through the silicon between the other two terminals (the next figures open it).</li>
          <li><b>Why it won.</b> A tube is hot, fragile and wears out: ENIAC's 17,468 tubes failed about every two days. A transistor has nothing to burn out, and it shrinks.</li>
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
