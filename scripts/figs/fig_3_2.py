# Fig 3.2 · Rosetta 2 (Pass 31, Part I, from an empty script). Job: function. Takeaway: ARM cannot add in memory, so
# Rosetta 2 rewrites each Intel add in memory as load, add and store.
# Concept: the mechanism the ledger names, not the listing: one memory cell holding 5. Above, Intel adds 3 to it in
# place, one instruction. Below, after Rosetta 2's one-time translation, ARM must make three trips: load the value
# into a register, add 3 there, store it back. The value travels (Part I's flow verb) and each ARM instruction
# lights as it runs (light). t=0 is the end: both cells hold 8.
from figlib import Timeline, text, splice, GOLD, BLUE, GREEN, MUTED

W, H = 400, 404
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=11.0)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
def lit(t0, t1): return T.anim('opacity', [(0.0, 0.0), (t0, 0.0), (t0 + 0.2, 1.0), (t1 - 0.2, 1.0), (t1, 0.0)])
def val(x, y, s, col, spans, size=18):
    return (f'<text data-role="object" x="{x}" y="{y}" text-anchor="middle" font-family="DM Mono" font-size="{size}" '
            f'fill="{col}" opacity="0">{vis(spans)}{s}</text>')
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-30 svgd-part1-30"{T.steps([(2.4, 'Intel'), (5.2, 'load'), (7.2, 'add'), (10.6, 'store')])}>')
a('<title id="svgt-part1-30">Fig 3.2 · Rosetta 2 · an Intel app, translated once for an ARM chip</title>')
a('<desc id="svgd-part1-30">One value, 5, in memory. Above, the Intel app adds 3 to it where it sits, in one instruction, and memory holds 8. '
  'Rosetta 2 translates the app once, on first launch. Below, the ARM translation cannot add in memory, so the one line becomes three: '
  'ldur loads the 5 into register w8, add makes it 8 there, and stur stores the 8 back into memory. The whole three-line app becomes '
  'six ARM lines.</desc>')

def pill(x, y, w, label, col, spans=None):
    off = f' opacity="0">{vis([(0.0, spans[0]), (spans[1], D)])}</rect>' if spans else '/>'
    a(f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="6" fill="none" stroke="{EDGE}" stroke-width="1.4"{off}')
    if spans: a(f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="6" fill="none" stroke="{col}" stroke-width="2.4" opacity="0">{vis([spans])}</rect>')
    a(text(x + 12, y + 22, label, size=15, fill=col, ls='0'))
def cell(x, y, name, before, after, t_change, col=BLUE, t_from=0.0, label_at=None):
    a(f'<rect x="{x}" y="{y}" width="96" height="42" rx="5" fill="none" stroke="{col}" stroke-width="1.6"/>')
    if label_at: a(text(label_at[0], label_at[1], name, anchor='end', size=14, fill=MUTED))
    else: a(text(x + 48, y - 8, name, anchor='middle', size=14, fill=MUTED))
    a(val(x + 48, y + 28, before, col, [(t_from, t_change)]))
    a(val(x + 48, y + 28, after, GOLD, [(t_change, D)]))

# ---------- Intel: add in place ----------
a(text(20, 28, 'Intel', size=14, fill=INK))
pill(20, 48, 150, 'add [x], 3', GOLD, (0.6, 2.2))
a(f'<path d="M 178 65 H 262 m -7 -6 l 7 6 l -7 6" fill="none" stroke="{GOLD}" stroke-width="2"/>')
cell(276, 44, 'memory', '5', '8', 1.6)

# ---------- Rosetta 2, once ----------
a(f'<rect x="40" y="118" width="320" height="52" rx="8" fill="none" stroke="{INK}" stroke-width="1.4"/>')
a(text(200, 140, 'Rosetta 2', anchor='middle', size=15, fill=INK))
a(f'<path d="M 200 102 V 116 M 200 172 V 186 m -5 -6 l 5 6 l 5 -6" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')

# ---------- ARM: load, add, store ----------
a(text(20, 204, 'ARM', size=14, fill=INK))
pill(20, 224, 150, 'ldur', GOLD, (3.6, 5.6))
pill(20, 270, 150, 'add 3', GOLD, (5.8, 7.6))
pill(20, 316, 150, 'stur', GOLD, (7.8, 9.8))
cell(276, 232, 'memory', '5', '8', 9.6)
cell(276, 336, 'register w8', '5', '8', 7.0, t_from=4.9, label_at=(266, 362))
# the register is empty until the load arrives
# the trips: down to the register, back up to memory
a(f'<path d="M 304 276 V 330 m -5 -7 l 5 7 l 5 -7" fill="none" stroke="{EDGE}" stroke-width="1.6"/>')
a(f'<path d="M 344 330 V 278 m -5 7 l 5 -7 l 5 7" fill="none" stroke="{EDGE}" stroke-width="1.6"/>')
def trip(x, y0, y1, s, t0, t1):
    a(f'<g opacity="0">{vis([(t0, t1)])}<g>{T.translate([(0.0, 0), (t0, 0), (t1, y1 - y0), (D - 0.01, y1 - y0)], axis="y")}'
      f'<circle cx="{x}" cy="{y0}" r="12" fill="#141414" stroke="{GOLD}" stroke-width="1.6"/>'
      f'<text data-role="object" x="{x}" y="{y0 + 5}" text-anchor="middle" font-family="DM Mono" font-size="14" fill="{GOLD}">{s}</text></g></g>')
trip(304, 262, 356, '5', 4.0, 4.9)
trip(344, 356, 262, '8', 8.4, 9.5)
a('</svg>')
svg = '\n'.join(o)

caption = 'Intel adds in memory; ARM must load, add and store back.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The app.</b> Three Intel lines: store 5 in memory, add 3 to it in place, load it into eax. In ARM, storing 5 takes two lines (<code>mov</code>, <code>stur</code>), the add takes the three drawn here, and the last load one (<code>ldur</code>): six.</li>
          <li><b>Ahead of time.</b> Rosetta reads the whole executable on first launch, writes an ARM version, and caches it; later launches skip the translation. Translated code runs at roughly 80% of native speed.</li>
          <li><b>One for many.</b> Any x86 sequence has some ARM sequence with the same observable result; the translator's job is to find it. The ARM shown here is a faithful translation, not Rosetta's literal output.</li>
          <li><b>The hard part.</b> x86 and ARM differ in the order in which one core's memory writes become visible to the others (Chapter 16). Apple's chips can enforce x86's order while translated code runs, so programs running on several cores at once behave as they did on Intel.</li>
          <li><b>Once.</b> Rosetta 2 translates the app once, at its first launch.</li>
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
