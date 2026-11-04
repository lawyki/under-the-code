# Fig 1.8 · Von Neumann architecture (Pass 31, Part I, from an empty script). Job: function. Takeaway: the program
# sits in memory beside its data, so the CPU fetches each instruction like a number.
# Concept: memory as one row of numbered cells (Part I's recurring memory), the program in cells 0 to 2 and its
# data in 3 to 5, one bus down to the CPU. The program counter steps (the gold frame), and every word, instruction
# or number, makes the same trip down the same bus (flow). store C sends the 8 back up into cell 5.
# t=0 is the finished run: C holds 8.
from figlib import Timeline, text, obj, splice, GOLD, BLUE, MUTED

W, H = 400, 400
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D, SHIFT = 14.0, 12.5
T = Timeline(D, shift=SHIFT)
CX = lambda i: 48 + 60 * i                  # cell centres
CY0, CY1 = 62, 114                          # cell top and bottom
BUS, CPU_T = 124, 222
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-9 svgd-part1-9">')
a('<title id="svgt-part1-9">Fig 1.8 · Von Neumann architecture · one memory, one bus</title>')
a('<desc id="svgd-part1-9">One memory, a row of numbered cells, holds a three-instruction program in cells 0 to 2 (load A, add B, '
  'store C) and its data in cells 3 to 5 (A = 5, B = 3, C = 0). One bus joins it to the CPU. The program counter steps through '
  'cells 0, 1 and 2; each instruction travels down the bus like any number, then the data it names travels down the same bus: '
  'the register takes 5, then 5 + 3 = 8, and store C sends the 8 back up the bus into cell 5.</desc>')

def vis(*spans):
    """discrete opacity: on during each (t0, t1) span of story time, else off."""
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', pts)

def vtext(x, y, s, col, size, spans):
    return (f'<text data-role="object" x="{x:g}" y="{y:g}" text-anchor="middle" font-family="DM Mono" font-size="{size}" '
            f'letter-spacing="0.06em" fill="{col}" opacity="0">{vis(*spans)}{s}</text>')

# ---------- memory ----------
a(text(20, 30, 'memory', size=15, fill=INK))
CELLS = [('load', 'A'), ('add', 'B'), ('store', 'C'), ('A', '5'), ('B', '3'), ('C', None)]
for i, (top, bot) in enumerate(CELLS):
    x = CX(i) - 28
    col = GOLD if i < 3 else BLUE
    parts = [f'<rect x="{x}" y="{CY0}" width="56" height="{CY1 - CY0}" rx="4" fill="none" stroke="{col}" stroke-opacity="0.75" stroke-width="1.4"/>',
             text(CX(i), 52, str(i), anchor='middle', size=14, fill=MUTED, role='object'),
             text(CX(i), CY0 + 20, top, anchor='middle', size=14, fill=col if i < 3 else MUTED, role='object')]
    if bot: parts.append(text(CX(i), CY0 + 42, bot, anchor='middle', size=16, fill=INK if i < 3 else BLUE, role='object'))
    a(obj(*parts))
# cell 5 holds 0 until store C writes 8
a(vtext(CX(5), CY0 + 42, '0', BLUE, 16, [(0.0, 11.1)]))
a(vtext(CX(5), CY0 + 42, '8', GOLD, 16, [(11.1, D)]))
a(text(CX(1), 148, 'program', anchor='middle', size=14, fill=GOLD))
a(text(CX(4), 148, 'data', anchor='middle', size=14, fill=BLUE))
# the program counter's frame: the active cell
a(f'<g>{T.translate([(0.0, 0), (4.4, 0), (4.6, 60), (8.0, 60), (8.2, 120), (13.8, 120), (13.99, 0)], axis="x")}'
  f'<rect x="{CX(0) - 32}" y="{CY0 - 4}" width="64" height="{CY1 - CY0 + 8}" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.5"/></g>')

# ---------- the one bus ----------
a(f'<path d="M {CX(0)} {CY1} V {BUS} M {CX(5)} {CY1} V {BUS} M {CX(0)} {BUS} H {CX(5)} M 200 {BUS} V {CPU_T}" fill="none" stroke="{EDGE}" stroke-width="2"/>')
for i in (1, 2, 3, 4): a(f'<line x1="{CX(i)}" y1="{CY1}" x2="{CX(i)}" y2="{BUS}" stroke="{EDGE}" stroke-width="2"/>')
a(text(210, 186, 'bus', size=14, fill=INK))

def trip(label, col, i, t0, up=False):
    """One word travels between cell i and the CPU over the bus: down, across, down (or the reverse)."""
    w = 14 + 9 * len(label)
    cx = CX(i); dx = 200 - cx
    if not up:
        xs = [(0.0, 0), (t0 + 0.35, 0), (t0 + 0.85, dx), (D - 0.01, dx)]
        ys = [(0.0, 0), (t0, 0), (t0 + 0.35, BUS - 88), (t0 + 0.85, BUS - 88), (t0 + 1.3, CPU_T - 88), (D - 0.01, CPU_T - 88)]
    else:
        xs = [(0.0, dx), (t0 + 0.45, dx), (t0 + 0.95, 0), (D - 0.01, 0)]
        ys = [(0.0, CPU_T - 88), (t0, CPU_T - 88), (t0 + 0.45, BUS - 88), (t0 + 0.95, BUS - 88), (t0 + 1.3, 0), (D - 0.01, 0)]
    a(f'<g opacity="0">{vis((t0, t0 + 1.3))}<g>{T.translate(xs, axis="x")}<g>{T.translate(ys, axis="y")}'
      f'<rect x="{cx - w / 2}" y="76" width="{w}" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.6"/>'
      + text(cx, 93, label, anchor='middle', size=14, fill=col, role='object') + '</g></g></g>')

# ---------- the CPU ----------
a(f'<rect x="20" y="{CPU_T}" width="360" height="126" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
a(text(34, CPU_T + 24, 'CPU', size=15, fill=INK))
SLOTS = {'pc': (36, 80), 'ins': (138, 124), 'reg': (284, 80)}
for k, (x, w) in SLOTS.items():
    a(f'<rect x="{x}" y="{CPU_T + 38}" width="{w}" height="38" rx="5" fill="none" stroke="{GOLD if k != "reg" else BLUE}" stroke-opacity="0.75" stroke-width="1.4"/>')
VY = CPU_T + 63
def slot_value(k, s, col, spans):
    x, w = SLOTS[k]
    a(vtext(x + w / 2, VY, s, col, 16, spans))
slot_value('pc', '0', GOLD, [(0.0, 4.4)]); slot_value('pc', '1', GOLD, [(4.4, 8.0)]); slot_value('pc', '2', GOLD, [(8.0, D)])
slot_value('ins', 'load A', GOLD, [(2.3, 5.9)]); slot_value('ins', 'add B', GOLD, [(5.9, 9.5)]); slot_value('ins', 'store C', GOLD, [(9.5, D)])
slot_value('reg', '5', BLUE, [(3.9, 7.5)]); slot_value('reg', '8', BLUE, [(7.5, D)])
a(text(76, CPU_T + 98, 'program', anchor='middle', size=14, fill=MUTED))
a(text(76, CPU_T + 115, 'counter', anchor='middle', size=14, fill=MUTED))
a(text(200, CPU_T + 98, 'instruction', anchor='middle', size=14, fill=MUTED))
a(text(324, CPU_T + 98, 'register', anchor='middle', size=14, fill=MUTED))

# the trips, in order: each instruction, then the data it names
trip('load A', GOLD, 0, 1.0); trip('5', BLUE, 3, 2.6)
trip('add B', GOLD, 1, 4.6); trip('3', BLUE, 4, 6.2)
trip('store C', GOLD, 2, 8.2); trip('8', BLUE, 5, 9.8, up=True)
a(text(200, 384, 'code and data: one memory, one bus', anchor='middle', size=15, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('One memory holds the program and its data; one bus, shared wires that the input and output devices (I/O) also use, '
           'carries both to the CPU one transfer at a time. There the control unit reads each instruction and the ALU (arithmetic '
           'and logic unit) computes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Fetch.</b> The program counter names the next cell; its instruction travels over the bus to the control unit.</li>
          <li><b>Execute.</b> The instruction asks for data, which travels over the same bus; the ALU does the arithmetic: 5 + 3.</li>
          <li><b>Store.</b> The result goes back up the bus into memory, and the counter moves on.</li>
          <li><b>One bus.</b> Code and data share it, so they take turns: the bottleneck the next sections return to.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-8">
      <div class="diagram-label">Fig 1.8 · Von Neumann architecture · one memory, one bus</div>
      {svg}
      <p id="ch1-vonneumann-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-8', 'ch1-vonneumann-p5', card)
