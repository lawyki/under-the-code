# Fig 1.9 · The instruction cycle (Pass 31, Part I, from an empty script). Job: function. Takeaway: the program
# counter advances by each instruction's length until an instruction sets it back, so the program loops.
# Concept: memory as a row of bytes (Part I's recurring memory) holding the real bytes of a three-instruction loop:
# five for mov, three for add, two for jmp. Above, the counter's steps (+5, +3); below, the jump back. The gold
# frame (the active thing) steps over each instruction while the four stages light in turn beneath it, once per
# instruction. The still already holds the loop: every step and the jump are drawn.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 360
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
T = Timeline(9, shift=0.0)
BYTES = ['B8', '05', '00', '00', '00', '83', 'C0', '03', 'EB', 'F6']
X = lambda i: 22 + i * 34 + 8 * (i >= 5) + 8 * (i >= 8)       # left edge of byte i
CT, CB = 52, 88                                                 # cell top, bottom
SPANS = [(0, 5, 'mov eax, 5', '0x00'), (5, 3, 'add eax, 3', '0x05'), (8, 2, 'jmp 0x00', '0x08')]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-10 svgd-part1-10"{T.steps([(1.5, 'mov'), (4.5, 'add'), (7.5, 'jmp')])}>')
a('<title id="svgt-part1-10">Fig 1.9 · The instruction cycle · fetch, decode, execute, writeback</title>')
a('<desc id="svgd-part1-10">Memory as a row of ten bytes holding a three-instruction loop: mov eax, 5 in five bytes at 0x00, add eax, 3 '
  'in three bytes at 0x05, jmp 0x00 in two bytes at 0x08. The program counter steps from 0x00 to 0x05 (+5) and to 0x08 (+3), '
  'the length of each instruction, and the jump sets it back to 0x00, so the program loops. For every instruction the four stages '
  'light in turn: fetch, decode, execute, writeback.</desc>')

def lit(spans):
    pts = [(0.0, 0.0)]
    for t0, t1 in spans: pts += [(t0, 0.0), (t0 + 0.12, 1.0), (t1 - 0.12, 1.0), (t1, 0.0)]
    pts = sorted(pts)
    return T.anim('opacity', pts)

# the bytes
for i, b in enumerate(BYTES):
    a(f'<rect x="{X(i)}" y="{CT}" width="32" height="{CB - CT}" rx="3" fill="none" stroke="{EDGE}" stroke-width="1.3"/>')
    a(text(X(i) + 16, CT + 23, b, anchor='middle', size=14, fill=INK, ls='0', role='object'))
# each instruction's start address and name
for i0, n, name, addr in SPANS:
    mid = X(i0) + (X(i0 + n - 1) + 32 - X(i0)) / 2
    a(text(X(i0) + 16, CB + 22, addr, anchor='middle', size=14, fill=BLUE, ls='0'))
    a(text(mid, CB + 44, name, anchor='middle', size=14, fill=GOLD, ls='0'))

# the counter's steps above (+5, +3) and the jump back below
c = [X(0) + 16, X(5) + 16, X(8) + 16]
def arc(d, head, spans, label=None, lx=0, ly=0):
    for stroke, op in ((EDGE, None), (GOLD, spans)):
        extra = f' opacity="0">{lit(op)}</path' if op else '/'
        a(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{2.2 if op else 1.5}"{extra}>')
        extra = f' opacity="0">{lit(op)}</path' if op else '/'
        a(f'<path d="{head}" fill="{stroke}" stroke="none"{extra}>')
    if label: a(text(lx, ly, label, anchor='middle', size=15, fill=INK))
arc(f'M {c[0]} {CT - 4} Q {(c[0] + c[1]) / 2} {CT - 46} {c[1] - 3} {CT - 8}', f'M {c[1]} {CT - 3} l -9 -3 l 4 -7 z', [(2.25, 3.4)], '+5', (c[0] + c[1]) / 2, CT - 34)
arc(f'M {c[1]} {CT - 4} Q {(c[1] + c[2]) / 2} {CT - 40} {c[2] - 3} {CT - 8}', f'M {c[2]} {CT - 3} l -9 -3 l 4 -7 z', [(5.25, 6.4)], '+3', (c[1] + c[2]) / 2, CT - 31)
RY = CB + 56
arc(f'M {c[2]} {RY} C {c[2]} {RY + 34} {c[0]} {RY + 34} {c[0]} {RY + 6}', f'M {c[0]} {RY} l -5 9 h 10 z', [(8.25, 9.0), (0.0, 0.4)])

# the gold frame: the instruction the counter points at
xs, ws = [], []
for k, (i0, n, _, _) in enumerate(SPANS):
    t0 = 3.0 * k
    x, w = X(i0) - 4, X(i0 + n - 1) + 32 - X(i0) + 8
    xs += [(t0, x), (t0 + 2.9, x)]; ws += [(t0, w), (t0 + 2.9, w)]
xs.append((9.0, xs[0][1])); ws.append((9.0, ws[0][1]))
a(f'<rect x="{xs[0][1]}" y="{CT - 4}" width="{ws[0][1]}" height="{CB - CT + 8}" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.5">'
  f'{T.anim("x", xs)}{T.anim("width", ws)}</rect>')

# the program counter
PY = 236
a(text(20, PY + 22, 'program counter', size=14, fill=MUTED))
a(f'<rect x="196" y="{PY}" width="90" height="34" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
for k, (_, _, _, addr) in enumerate(SPANS):
    a(f'<text data-role="object" x="241" y="{PY + 23}" text-anchor="middle" font-family="DM Mono" font-size="16" fill="{BLUE}" opacity="0">'
      f'{T.discrete("opacity", [(0.0, 1 if k == 0 else 0), (3.0, 1 if k == 1 else 0), (6.0, 1 if k == 2 else 0)])}{addr}</text>')

# the four stages, lit in turn for every instruction
SY = 290
for j, s in enumerate(['fetch', 'decode', 'execute', 'writeback']):
    x = 20 + j * 91
    a(f'<rect x="{x}" y="{SY}" width="85" height="30" rx="15" fill="none" stroke="{EDGE}"/>')
    spans = [(3.0 * k + 0.75 * j, 3.0 * k + 0.75 * (j + 1)) for k in range(3)]
    a(f'<rect x="{x}" y="{SY}" width="85" height="30" rx="15" fill="rgba(212,168,83,0.2)" stroke="{GOLD}" stroke-width="2.2" opacity="0">{lit(spans)}</rect>')
    a(text(x + 42.5, SY + 20, s, anchor='middle', size=14, fill=INK, ls='0'))
    if j < 3: a(f'<path d="M {x + 87} {SY + 15} l 4 0" stroke="{EDGE}"/>')
a('</svg>')
svg = '\n'.join(o)

caption = "The counter steps by each instruction's length, and the jump sends it back."
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Fetch.</b> Read the bytes at the address in the program counter.</li>
          <li><b>Decode.</b> Work out the operation and its operands from the bit pattern (Fig 1.10 takes one apart).</li>
          <li><b>Execute.</b> The ALU or another unit does the work: an addition, a comparison, an address.</li>
          <li><b>Writeback.</b> Store the result and move the counter on by the instruction's length; a jump sets the counter instead.</li>
          <li><b>The addresses.</b> Written in hexadecimal: 0x05 is 5 and 0x08 is 8. The first instruction takes five bytes and the second three.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-9">
      <div class="diagram-label">Fig 1.9 · The instruction cycle · fetch, decode, execute, writeback</div>
      {svg}
      <p id="ch1-cpu-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-9', 'ch1-cpu-p3', card)
