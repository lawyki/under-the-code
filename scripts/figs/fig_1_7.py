# Fig 1.7 · ENIAC and the M4 (Pass 28, law 3). Each at its own scale, marked: the hall
# with a person, the chip under a fingertip. 28 billion / 17,468 = 1.6 million times as many
# switches (the old caption said twelve million: that is 4004 -> M4). A tube now and then burns out.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 452
T = Timeline(8, shift=0.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-8 svgd-part1-8">')
a('<title id="svgt-part1-8">Fig 1.7 · ENIAC and the Apple M4 · the same job, 79 years apart</title>')
a('<desc id="svgd-part1-8">ENIAC, 1945: a U of cabinets around a thirty-metre hall, a person drawn for scale, 17,468 vacuum tubes, 30 tons, 150 kilowatts; '
  'now and then a tube burns out. The Apple M4, 2024: a chip under a fingertip with 28 billion transistors, about 1.6 million times as many switches.</desc>')

# --- ENIAC ---
a(text(20, 28, 'ENIAC · 1945', fill='rgba(255,255,255,0.85)'))
# a U of cabinets: the long back wall and two short arms, seen from above
cab = []
for i in range(18): cab.append((20 + i * 20, 46))                 # back wall
for j in range(1, 5): cab.append((20, 46 + j * 20)); cab.append((360, 46 + j * 20))
for (x, y) in cab:
    a(f'<rect x="{x}" y="{y}" width="18" height="18" rx="2" fill="#2a241a" stroke="rgba(212,168,83,0.45)"/>')
    a(f'<circle cx="{x + 9}" cy="{y + 9}" r="2.6" fill="{GOLD}" opacity="0.8"/>')
# a tube burns out now and then (ENIAC failed about every two days)
for k, (x, y) in enumerate([cab[5], cab[13], cab[20]]):
    t0 = 1.0 + k * 2.4
    a(f'<circle cx="{x + 9}" cy="{y + 9}" r="3.4" fill="{RED}" opacity="0">{T.anim("opacity", [(0.0, 0.0), (t0, 0.0), (t0 + 0.1, 1.0), (t0 + 1.6, 1.0), (t0 + 1.8, 0.0), (8.0, 0.0)])}</circle>')
# a person for scale (1.7 m in a 30 m hall: 360 px = 30 m)
px_per_m = 360 / 30
ph = 1.7 * px_per_m
a(f'<g transform="translate(200,{150 - ph:.1f})" fill="rgba(255,255,255,0.8)"><circle cx="0" cy="2.6" r="2.6"/><rect x="-2.6" y="5.6" width="5.2" height="{ph - 6:.1f}" rx="2"/></g>')
a(text(212, 148, 'a person', size=13, fill='rgba(255,255,255,0.55)'))
# scale bar: 10 m
a(f'<path d="M 20 170 v 6 h {10 * px_per_m:g} v -6" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>')
a(text(20 + 5 * px_per_m, 196, '10 m', anchor='middle', size=13, fill='rgba(255,255,255,0.6)'))
a(text(380, 176, '17,468 vacuum tubes', anchor='end', fill='rgba(255,255,255,0.8)'))
a(text(380, 196, '30 tons · 150 kW', anchor='end', fill=MUTED))

# --- the punchline ---
a('<line x1="20" y1="222" x2="380" y2="222" stroke="rgba(255,255,255,0.1)"/>')
a(f'<text x="200" y="258" text-anchor="middle" {MONO} font-size="22" fill="{GOLD}">×1.6 million switches</text>')
a(text(200, 280, '79 years later', anchor='middle', fill=MUTED))
a('<line x1="20" y1="298" x2="380" y2="298" stroke="rgba(255,255,255,0.1)"/>')

# --- M4 ---
a(text(20, 326, 'APPLE M4 · 2024', fill='rgba(255,255,255,0.85)'))
# a fingertip (outline) with the chip under it
a('<path d="M 60 452 V 382 Q 60 340 104 340 Q 148 340 148 382 V 452" fill="rgba(240,205,180,0.12)" stroke="rgba(240,205,180,0.55)" stroke-width="1.5"/>')
a('<path d="M 82 372 Q 104 360 126 372" fill="none" stroke="rgba(240,205,180,0.35)"/>')
a(f'<rect x="86" y="388" width="36" height="36" rx="3" fill="#1d1d1d" stroke="{BLUE}" stroke-width="1.5"/>')
a(f'<rect x="92" y="394" width="24" height="24" rx="1" fill="{BLUE}" fill-opacity="0.35"/>')
a(text(162, 380, 'a fingertip', size=13, fill='rgba(255,255,255,0.55)'))
a(text(380, 410, '28 billion', anchor='end', size=18, fill='#fff'))
a(text(380, 432, 'transistors', anchor='end', fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('ENIAC filled a thirty-metre hall with 17,468 vacuum tubes; the M4 fits under a fingertip and holds 28 billion transistors, '
           'about 1.6 million times as many switches. Each is drawn at its own scale: in life the hall is some two thousand times longer than the chip.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The same job.</b> Both machines flip switches according to instructions; the distance between them is the history of the integrated circuit.</li>
          <li><b>The red flashes.</b> A tube burning out. ENIAC lost one about every two days; a chip's transistors run for years.</li>
          <li><b>The numbers.</b> 28,000,000,000 ÷ 17,468 ≈ 1.6 million. (From the 4004 of 1971 to the M4 the factor is twelve million: Fig 1.6.)</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-7">
      <div class="diagram-label">Fig 1.7 · ENIAC and the Apple M4 · the same job, 79 years apart</div>
      {svg}
      <p id="ch1-transistor-p17" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-7', 'ch1-transistor-p17', card)
