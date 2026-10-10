# Fig 3.2 · Rosetta 2 (Pass 28, law 3). Three x86-64 instructions, translated once into six ARM64
# ones that do the same work. x86 can do arithmetic on memory directly (add [rbp-4], 3); ARM is
# load/store, so the same step is ldur, add, stur. Colour ties each x86 line to its ARM group.
# A faithful translation of the same work, not Rosetta's literal output.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, MUTED

W, H = 400, 446
COL = [GOLD, BLUE, GREEN]
X86 = ['mov dword [rbp-4], 5', 'add dword [rbp-4], 3', 'mov eax, [rbp-4]']
ARM = [['mov  w8, #5', 'stur w8, [x29, #-4]'],
       ['ldur w8, [x29, #-4]', 'add  w8, w8, #3', 'stur w8, [x29, #-4]'],
       ['ldur w0, [x29, #-4]']]
T = Timeline(7.5, shift=6.8)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (7.4995, 0.0)])
def on_from(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (7.3, 1.0), (7.301, 0.0), (7.4995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-30 svgd-part1-30">')
a('<title id="svgt-part1-30">Fig 3.2 · Rosetta 2 · an Intel app, translated once for an ARM chip</title>')
a('<desc id="svgd-part1-30">Three x86-64 instructions from an Intel app: store 5 in memory, add 3 to it in place, load it into eax. '
  'Rosetta 2 translates them once, on first launch, into six ARM64 instructions that do the same work: ARM cannot add to memory directly, '
  'so the middle step becomes load, add, store. The translation is cached and runs natively.</desc>')
a(text(20, 22, 'x86-64 · AN INTEL APP', size=13, fill=MUTED))
for i, line in enumerate(X86):
    y = 34 + i * 30
    a(f'<rect x="20" y="{y}" width="360" height="26" rx="4" fill="#151515" stroke="rgba(255,255,255,0.18)"/>')
    a(f'<rect x="20" y="{y}" width="5" height="26" rx="1" fill="{COL[i]}"/>')
    a(f'<rect class="fx" x="18" y="{y - 2}" width="364" height="30" rx="5" fill="none" stroke="{COL[i]}" stroke-width="2" opacity="0">{win(0.4 + i * 1.8, 1.6 + i * 1.8)}</rect>')
    a(f'<text x="36" y="{y + 18}" {MONO} font-size="14" fill="#fff">{line.replace("[", "[").replace("]", "]")}</text>')
# Rosetta: translate once, cache
a('<path d="M 200 126 V 140" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>')
a(f'<rect x="60" y="140" width="280" height="44" rx="8" fill="#1d1810" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(f'<rect class="fx" x="60" y="140" width="280" height="44" rx="8" fill="{GOLD}" fill-opacity="0.18" opacity="0">'
  f'{T.anim("opacity", [(0.0, 0.0), (0.6, 0.0), (0.7, 1.0), (5.6, 1.0), (5.8, 0.0), (7.4995, 0.0)])}</rect>')
a(text(200, 160, 'Rosetta 2', anchor='middle', size=15, fill='#fff', ls='0'))
a(text(200, 177, 'translates once, on first launch', anchor='middle', size=13, fill=MUTED, ls='0'))
a('<path d="M 200 184 V 198" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/><polygon points="195,196 200,204 205,196" fill="rgba(255,255,255,0.5)"/>')
a(text(20, 222, 'ARM64 · CACHED, RUNS NATIVELY', size=13, fill=MUTED))
y = 232
for i, group in enumerate(ARM):
    y0 = y
    for line in group:
        a(f'<rect x="30" y="{y}" width="350" height="26" rx="4" fill="#151515" stroke="rgba(255,255,255,0.18)"/>')
        a(f'<g opacity="0">{on_from(1.0 + i * 1.8)}<text x="44" y="{y + 18}" {MONO} font-size="14" fill="#fff">{line}</text></g>')
        y += 30
    a(f'<rect x="20" y="{y0}" width="5" height="{y - y0 - 4}" rx="1" fill="{COL[i]}"/>')
    a(f'<rect class="fx" x="28" y="{y0 - 2}" width="354" height="{y - y0}" rx="5" fill="none" stroke="{COL[i]}" stroke-width="2" opacity="0">{win(1.0 + i * 1.8, 1.6 + i * 1.8 + 0.6)}</rect>')
a(text(20, 436, '3 instructions in, 6 out', size=13, fill='rgba(255,255,255,0.5)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Rosetta 2 let Intel apps run on Apple Silicon by translating their x86 code into ARM code once, on first launch, and caching it. '
           'Where x86 adds to memory in one instruction, ARM must load, add and store, so one line can become three.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Ahead of time.</b> Rosetta reads the whole executable on first launch, writes an ARM version, and caches it; later launches skip the translation. Translated code runs at roughly 80% of native speed.</li>
          <li><b>One for many.</b> Any x86 sequence has some ARM sequence with the same observable result; the translator's job is to find it. The ARM shown here is a faithful translation, not Rosetta's literal output.</li>
          <li><b>The hard part.</b> x86 promises a stricter order for memory operations than ARM. Apple's chips have a mode that enforces x86's order while translated code runs, so multithreaded programs behave as they did on Intel.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-2">
      <div class="diagram-label">Fig 3.2 · Rosetta 2 · an Intel app, translated once for an ARM chip</div>
      {svg}
      <p id="ch3-isa-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-2', 'ch3-isa-p5', card)
