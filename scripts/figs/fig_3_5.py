# Fig 3.5 · A process's address space (Pass 28, law 3). One column, high addresses at the top.
# The stack pushes frames downward as main calls f calls g, then pops them; the heap grows upward
# as blocks are allocated. t=0: main, f, g on the stack, two heap blocks.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 440
X0, X1 = 70, 290
T = Timeline(9, shift=4.0)
def life(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-33 svgd-part1-33">')
a('<title id="svgt-part1-33">Fig 3.5 · A process\'s virtual address space</title>')
a('<desc id="svgd-part1-33">A column of addresses, highest at the top. The kernel\'s half is off limits. Below it the stack, which grows downward: frames for main, f and g are pushed as the calls happen and popped as they return. '
  'Far below, the heap grows upward as memory is allocated. Below the heap, the global data, and at the bottom the program\'s machine code, read-only.</desc>')
a(text(X0, 22, 'high addresses', size=13, fill=MUTED))
def region(y0, y1, col, name, sub, fill_op=0.14):
    a(f'<rect x="{X0}" y="{y0}" width="{X1 - X0}" height="{y1 - y0}" fill="{col}" fill-opacity="{fill_op}" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(X0 + 12, y0 + 22, name, size=15, fill='#fff', ls='0'))
    if sub: a(text(X0 + 12, y0 + 40, sub, size=13, fill=MUTED, ls='0'))
region(32, 84, '#8a8a8a', 'kernel', 'off limits to the program', 0.18)
# stack: a fixed band whose frames come and go
a(f'<rect x="{X0}" y="84" width="{X1 - X0}" height="124" fill="{GOLD}" fill-opacity="0.05" stroke="{GOLD}" stroke-opacity="0.5"/>')
a(text(X1 + 10, 102, 'stack', size=15, fill=GOLD, ls='0'))
a(text(X1 + 10, 122, 'grows', size=13, fill=MUTED, ls='0'))
a(f'<path d="M {X1 + 30} 132 v 30" stroke="{GOLD}" stroke-width="2"/><polygon points="{X1 + 24},158 {X1 + 30},168 {X1 + 36},158" fill="{GOLD}"/>')
FR = [('main', 0.0, 9.0), ('f()', 0.8, 7.6), ('g()', 1.8, 6.4)]
for k, (name, t0, t1) in enumerate(FR):
    y = 88 + k * 38
    rect = (f'<rect x="{X0 + 6}" y="{y}" width="{X1 - X0 - 12}" height="34" rx="3" fill="{GOLD}" fill-opacity="0.3" stroke="{GOLD}"/>'
            f'<text x="{X0 + 18}" y="{y + 22}" {MONO} font-size="15" fill="#fff">{name} frame</text>')
    a(rect if k == 0 else f'<g opacity="0">{life(t0, t1)}{rect}</g>')
# the gap
a(text((X0 + X1) / 2, 246, 'unused', anchor='middle', size=13, fill='rgba(255,255,255,0.35)', ls='0'))
# heap: blocks from the bottom up
a(f'<rect x="{X0}" y="270" width="{X1 - X0}" height="84" fill="{BLUE}" fill-opacity="0.05" stroke="{BLUE}" stroke-opacity="0.5"/>')
a(text(X1 + 10, 346, 'heap', size=15, fill=BLUE, ls='0'))
a(text(X1 + 10, 326, 'grows', size=13, fill=MUTED, ls='0'))
a(f'<path d="M {X1 + 30} 312 v -30" stroke="{BLUE}" stroke-width="2"/><polygon points="{X1 + 24},286 {X1 + 30},276 {X1 + 36},286" fill="{BLUE}"/>')
for k, (t0, t1) in enumerate(((1.2, 8.2), (2.6, 8.2))):
    y = 316 - k * 38
    a(f'<g opacity="0">{life(t0, t1)}<rect x="{X0 + 6}" y="{y}" width="{X1 - X0 - 12}" height="34" rx="3" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}"/>'
      f'<text x="{X0 + 18}" y="{y + 22}" {MONO} font-size="15" fill="#fff">malloc block</text></g>')
region(354, 384, GREEN, 'data · globals', '', 0.14)
region(384, 418, RED, 'text · machine code', '', 0.14)
a(text(X0, 436, 'low addresses', size=13, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('Every process sees the same layout: its code and globals at the bottom, the heap growing up from them, the stack growing down from just under the kernel. '
           'A call pushes a frame onto the stack and a return pops it; a malloc takes a block from the heap.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Virtual.</b> These are virtual addresses: each process gets the whole picture to itself (the MMU of the Bridge maps it to real RAM).</li>
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
