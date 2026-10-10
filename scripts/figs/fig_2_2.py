# Fig 2.2 · Boole and Shannon (Pass 28, law 3). One algebra, two drawings. A and B step through
# 00, 10, 01, 11: the Venn circles light where true, the overlap only when both; two switches in
# series close to match and the lamp lights only when both are closed. t=0: A = B = 1.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 410
STEP = 1.6
CASES = [(0, 0), (1, 0), (0, 1), (1, 1)]
T = Timeline(STEP * 4, shift=STEP * 3 + 0.8)
def when(pred):               # opacity: 1 during the steps where pred(A, B) holds (snapping), else 0
    pts = [(0.0, 1.0 if pred(*CASES[0]) else 0.0)]
    for i, (A, B) in enumerate(CASES):
        v = 1.0 if pred(A, B) else 0.0
        t0 = i * STEP
        if i: pts.append((t0 - 0.001, pts[-1][1]))
        pts.append((t0, v))
    pts.append((STEP * 4 - 0.001, pts[-1][1]))
    return T.anim('opacity', pts)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-18 svgd-part1-18">')
a("<title id=\"svgt-part1-18\">Fig 2.2 · Boole's algebra · Shannon's switches · the same AND</title>")
a('<desc id="svgd-part1-18">Above, Boole (1847): two overlapping circles, A and B; A · B is their overlap, true only where both hold. '
  'Below, Shannon (1937): a battery, two switches in series and a lamp; current reaches the lamp only when both switches are closed. '
  'A and B step through all four cases; the overlap and the lamp light together, only for A = 1 and B = 1.</desc>')
# Boole
a(text(20, 26, 'BOOLE · 1847', size=14, fill='rgba(255,255,255,0.8)'))
for cx, name, pred in ((160, 'A', lambda A, B: A), (240, 'B', lambda A, B: B)):
    a(f'<circle cx="{cx}" cy="104" r="58" fill="{BLUE}" fill-opacity="0.04" stroke="{BLUE}" stroke-opacity="0.7" stroke-width="1.5"/>')
    a(f'<circle cx="{cx}" cy="104" r="58" fill="{BLUE}" fill-opacity="0.18" opacity="0">{when(pred)}</circle>')
a(f'<path d="M 200 62 A 58 58 0 0 1 200 146 A 58 58 0 0 1 200 62 Z" fill="{GOLD}" fill-opacity="0.75" opacity="0">{when(lambda A, B: A and B)}</path>')
a(text(128, 110, 'A', anchor='middle', size=18, fill='#fff', ls='0'))
a(text(272, 110, 'B', anchor='middle', size=18, fill='#fff', ls='0'))
a(text(200, 182, 'A · B is the overlap', anchor='middle', size=14, fill=GOLD))
# Shannon
a(text(20, 222, 'SHANNON · 1937', size=14, fill='rgba(255,255,255,0.8)'))
WIRE = 'M 30 262 H 110 M 160 262 H 210 M 260 262 H 316 M 344 262 H 368 V 316 H 30 V 300 M 30 278 V 262'
a(f'<path d="{WIRE}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>')
a(f'<path d="{WIRE}" fill="none" stroke="{GOLD}" stroke-width="2.5" opacity="0">{when(lambda A, B: A and B)}</path>')
a('<path d="M 18 278 H 42 M 23 290 H 37" stroke="#fff" stroke-width="2.5"/>')       # the battery
a('<line x1="30" y1="290" x2="30" y2="300" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>')
for x0, name, idx in ((110, 'A', 0), (210, 'B', 1)):
    a(f'<circle cx="{x0}" cy="262" r="3.5" fill="#fff"/><circle cx="{x0 + 50}" cy="262" r="3.5" fill="#fff"/>')
    a(f'<line x1="{x0}" y1="262" x2="{x0 + 46}" y2="240" stroke="#fff" stroke-width="2.5" stroke-linecap="round">{when(lambda A, B, k=idx: not (A, B)[k])}</line>')
    a(f'<line x1="{x0}" y1="262" x2="{x0 + 50}" y2="262" stroke="{GOLD}" stroke-width="2.8" stroke-linecap="round" opacity="0">{when(lambda A, B, k=idx: (A, B)[k])}</line>')
    a(text(x0 + 25, 290, name, anchor='middle', size=16, fill='#fff', ls='0'))
a('<circle cx="330" cy="262" r="14" fill="#151515" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>')
a(f'<circle cx="330" cy="262" r="14" fill="{GOLD}" opacity="0">{when(lambda A, B: A and B)}</circle>')
a(f'<circle cx="330" cy="262" r="26" fill="{GOLD}" opacity="0">{T.anim("opacity", [(0.0, 0.0), (STEP * 3 - 0.001, 0.0), (STEP * 3, 0.2), (STEP * 4 - 0.002, 0.2)])}</circle>')
a('<path d="M 324 266 l 3 -8 l 3 8 l 3 -8" fill="none" stroke="#0a0a0a" stroke-width="1.4"/>')
a(text(200, 342, 'two switches in series', anchor='middle', size=14, fill=GOLD))
# the truth table, the current row outlined
for i, (A, B) in enumerate(CASES):
    x = 20 + i * 92
    a(f'<rect x="{x}" y="358" width="84" height="44" rx="5" fill="#141414" stroke="rgba(255,255,255,0.18)"/>')
    pts = [(0.0, 0.0), (i * STEP - 0.001 if i else 0.0, 0.0), (i * STEP + 0.001, 1.0), ((i + 1) * STEP - 0.002, 1.0), ((i + 1) * STEP - 0.001, 0.0), (STEP * 4 - 0.0005, 0.0)]
    a(f'<rect x="{x}" y="358" width="84" height="44" rx="5" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">{T.anim("opacity", pts)}</rect>')
    a(text(x + 42, 377, f'{A} {B}', anchor='middle', size=14, fill=MUTED, ls='0'))
    a(text(x + 42, 395, f'→ {A & B}', anchor='middle', size=15, fill=GOLD if A & B else '#fff', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ("Boole's A · B, true only where both propositions hold, is the overlap of two circles; Shannon saw that two switches in series pass current only when both are closed. "
           'The same algebra, ninety years apart, is the AND gate in every CPU.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Boole, 1847.</b> Propositions as sets of cases: A · B, "A and B", is the set where both hold, the overlap.</li>
          <li><b>Shannon, 1937.</b> His master's thesis showed relay circuits obey Boole's algebra exactly: closed is 1, open is 0.</li>
          <li><b>Series and parallel.</b> Switches in series are AND; side by side they would be OR (Fig 2.3).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-2">
      <div class="diagram-label">Fig 2.2 · Boole's algebra · Shannon's switches · the same AND</div>
      {svg}
      <p id="ch2-boole-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-2', 'ch2-boole-p9', card)
