# Fig 3.5 · A process's virtual address space (Pass 31, Part I, from an empty script). Job: function. Takeaway: the
# stack starts high and grows down: each call extends it and each return shrinks it.
# Concept: the address space as one column, high addresses at the top: the kernel's part (off limits), the stack just
# under it, the unused gap, the heap, data and the machine code at the bottom. The stack is alive: main calls f, f calls
# g, each call pushing a frame downward and each return popping it (Part I's step verb), RSP following the bottom
# edge; a block of heap appears as the program allocates. t=0 is the deepest moment: main, f and g on the stack.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 428
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 10.0
T = Timeline(D, shift=4.2)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
CX0, CW = 60, 210                               # the column
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-33 svgd-part1-33"{T.steps([(1.5, 'main'), (2.8, 'f'), (4.4, 'g'), (7.0, 'return')])}>')
a("<title id=\"svgt-part1-33\">Fig 3.5 · A process's virtual address space</title>")
a('<desc id="svgd-part1-33">A column of addresses, highest at the top. The kernel\'s part is off limits. Below it the stack, which grows '
  'downward: frames for main, f and g are pushed as the calls happen (main calls f, f calls g) and popped as they return, RSP marking '
  'the bottom edge. Far below, the heap grows upward as memory is allocated. Below the heap, the data region of global variables, and '
  'at the bottom the program\'s machine code, read-only.</desc>')

a(text(CX0, 22, 'high addresses', size=14, fill=MUTED))
a(text(CX0, 420, 'low addresses', size=14, fill=MUTED))
def region(y, h, label, col, dash=False, sub=None):
    d = ' stroke-dasharray="4 4"' if dash else ''
    a(f'<rect x="{CX0}" y="{y}" width="{CW}" height="{h}" rx="5" fill="none" stroke="{col}" stroke-width="1.5"{d}/>')
    a(text(CX0 + 12, y + 21, label, size=14, fill=col, ls='0'))
    if sub: a(text(CX0 + 12, y + 39, sub, size=14, fill=MUTED, ls='0'))
region(32, 50, 'kernel', RED, sub='off limits')
# the stack: frames pushed downward, one per call
FR = [('main', 0.6, 9.4), ('f', 2.0, 7.8), ('g', 3.4, 6.2)]
FY = lambda k: 92 + k * 38
a(f'<rect x="{CX0}" y="88" width="{CW}" height="122" rx="5" fill="none" stroke="rgba(212,168,83,0.6)" stroke-width="1.4"/>')
a(text(CX0 + CW + 14, 104, 'stack', size=14, fill=GOLD))
a(f'<path d="M {CX0 + CW + 30} 114 V 160 m -5 -7 l 5 7 l 5 -7" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
a(text(CX0 + CW + 14, 182, 'grows down', size=14, fill=MUTED))
for k, (name, t0, t1) in enumerate(FR):
    y = FY(k)
    a(f'<g opacity="0">{vis([(t0, t1)])}<rect x="{CX0 + 6}" y="{y}" width="{CW - 12}" height="32" rx="4" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
      + text(CX0 + 18, y + 21, f"{name}'s frame", size=14, fill=INK, ls='0') + '</g>')
# RSP follows the bottom of the newest frame
rsp = [(0.0, FY(0)), (0.6, FY(0)), (2.0, FY(0)), (2.2, FY(1)), (3.4, FY(1)), (3.6, FY(2)), (6.2, FY(2)), (6.4, FY(1)), (7.8, FY(1)),
       (8.0, FY(0)), (9.4, FY(0)), (D - 0.01, FY(0))]
a(f'<g opacity="0">{vis([(0.6, 9.4)])}<g>{T.translate([(t, v - FY(0)) for t, v in rsp], axis="y")}'
  f'<path d="M {CX0 - 4} {FY(0) + 32} l -10 -6 v 12 z" fill="{INK}"/>' + text(CX0 - 18, FY(0) + 37, 'RSP', anchor='end', size=14, fill=INK) + '</g></g>')
# the gap, the heap growing up, data, text
a(text(CX0 + CW / 2, 246, 'unused', anchor='middle', size=14, fill=MUTED))
a(f'<rect x="{CX0}" y="266" width="{CW}" height="66" rx="5" fill="none" stroke="rgba(134,168,255,0.6)" stroke-width="1.4"/>')
a(text(CX0 + CW + 14, 282, 'heap', size=14, fill=BLUE))
a(text(CX0 + CW + 14, 350, 'grows up', size=14, fill=MUTED))
a(f'<path d="M {CX0 + CW + 30} 334 V 292 m -5 7 l 5 -7 l 5 7" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
a(f'<rect x="{CX0 + 6}" y="300" width="{CW - 12}" height="26" rx="4" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
a(text(CX0 + 18, 318, 'malloc block', size=14, fill=INK, ls='0'))
a(f'<g opacity="0">{vis([(4.6, 9.8)])}<rect x="{CX0 + 6}" y="272" width="{CW - 12}" height="24" rx="4" fill="none" stroke="{BLUE}" stroke-width="1.6"/>'
  + text(CX0 + 18, 289, 'malloc block', size=14, fill=INK, ls='0') + '</g>')
region(338, 30, 'data · global variables', GREEN)
region(370, 30, 'text · machine code', INK)
a('</svg>')
svg = '\n'.join(o)

caption = ('Every process sees the same layout: machine code (text) and global variables (data) at the bottom; the heap, memory taken '
           'with <code>malloc</code> while the program runs and kept until freed, growing up from them; the stack growing down from just '
           'under the kernel, one frame of local values per call, gone when the call returns.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Virtual.</b> These are virtual addresses: each process gets the whole picture to itself (the MMU from Chapter 1, opened up in the Bridge, maps it to real RAM).</li>
          <li><b>Kernel.</b> On x86-64 Linux the top half of the address space belongs to the kernel and is off limits in Ring 3.</li>
          <li><b>Text.</b> The machine code is read-only and executable; data and the heap are writable but not executable.</li>
          <li><b>Toward each other.</b> Stack and heap grow into the unused gap between them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-5">
      <div class="diagram-label">Fig 3.5 · A process's virtual address space</div>
      {svg}
      <p id="ch3-stack-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-5', 'ch3-stack-p2', card)
