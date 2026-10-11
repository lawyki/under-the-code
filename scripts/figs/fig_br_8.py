# Fig BR.8 · Direct memory access · the device writes RAM by itself (Pass 28, law 3, conceptual pass). One disk read.
# 1: the kernel writes a small command into the SSD's registers: read these blocks into the buffer at 0x4a20_0000.
# 2: the SSD streams the data straight into RAM, filling the buffer block by block, while the CPU runs another process.
# 3: the SSD raises an interrupt; the kernel finishes the request and wakes the process that asked. The CPU never touches
# the data. t=0 (shift): the buffer full, the waiting process woken.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
TC, TS0, TS1, TI = 0.8, 2.2, 7.0, 7.6
NB = 8
o = []; a = o.append
def box(x, y, w, h, col):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="0.6"/>')
box(20, 14, 170, 70, BLUE)
a(text(32, 36, 'CPU', size=13, fill=BLUE, ls='0'))
for t0, t1, s, col in ((0.31, TC, 'process A asks', MUTED), (TC, TS0, 'kernel: command', GOLD), (TS0, TI, 'runs process B', BLUE),
                       (TI, TI + 1.2, 'IRQ: kernel done', GOLD), (TI + 1.2, None, 'A woken', GREEN)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(32, 62, s, size=13, fill=col, ls="0")}</g>')
box(210, 14, 170, 70, GOLD)
a(text(222, 36, 'NVMe SSD', size=13, fill=GOLD, ls='0'))
a(f'<g opacity="0">{lit(TC + 0.6, TI)}{text(222, 62, "reading blocks", size=13, fill="#fff", ls="0")}</g>')
a(f'<g opacity="0">{win(TI)}{text(222, 62, "done", size=13, fill="#fff", ls="0")}</g>')
# RAM buffer
RY = 120
box(20, RY, 360, 74, GREEN)
a(text(32, RY + 22, 'RAM: buffer at 0x4a20_0000', size=13, fill=GREEN, ls='0'))
BW = (336 - (NB - 1) * 4) / NB
for b in range(NB):
    x = 32 + b * (BW + 4)
    a(f'<rect x="{x:.1f}" y="{RY + 34}" width="{BW:.1f}" height="28" rx="3" fill="none" stroke="{GREEN}" stroke-opacity="0.5"/>')
    tb = TS0 + (TS1 - TS0) * (b + 1) / NB
    a(f'<g opacity="0">{win(tb)}<rect x="{x:.1f}" y="{RY + 34}" width="{BW:.1f}" height="28" rx="3" fill="{GREEN}" fill-opacity="0.75"/></g>')
# the three movements
def fly(x0, y0, x1, y1, t0, t1, col):
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)], "x")}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)], "y")}<circle cx="{x0}" cy="{y0}" r="6" fill="{col}"/></g></g></g>')
fly(190, 49, 210, 49, TC, TC + 0.6, GOLD)                      # 1: command
for b in range(NB):                                             # 2: data, block by block
    t0 = TS0 + (TS1 - TS0) * b / NB
    x = 32 + b * (BW + 4) + BW / 2
    fly(295, 84, x, RY + 48, t0, t0 + (TS1 - TS0) / NB, GREEN)
fly(210, 70, 190, 70, TI, TI + 0.6, RED)                        # 3: interrupt
LY = RY + 100
STEPS = [('1', 'kernel writes a small command', GOLD, TC), ('2', 'the SSD fills RAM on its own', GREEN, TS0), ('3', 'an interrupt says done', RED, TI)]
for k, (n, s, col, t0) in enumerate(STEPS):
    body = text(20, LY + k * 22, f'{n}  {s}', size=13, fill=col, ls='0')
    a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(t0)}{body}</g>')
a(text(20, LY + 3 * 22 + 6, 'the CPU never touches the data', size=13, fill=MUTED, ls='0'))
H = LY + 3 * 22 + 18
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-50 svgd-part1-50">')
o.insert(1, '<title id="svgt-part1-50">Fig BR.8 · Direct memory access · the device writes RAM by itself</title>')
o.insert(2, '<desc id="svgd-part1-50">A disk read by direct memory access. Process A asks for data and the kernel writes a small command into the SSD\'s registers: read these blocks into the buffer at 0x4a20_0000. '
  'The SSD then streams the data straight into RAM, filling the buffer block by block, while the CPU runs process B. When the transfer is finished the SSD raises an interrupt, the kernel completes the request and wakes process A. The CPU never touches the data itself.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('With direct memory access the kernel only writes a small command telling the device where to put the data; the device then copies it into RAM on its own while the CPU runs something else. '
           'An interrupt says when it is done, so the CPU handles the command and the completion but never the data.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Queues.</b> An NVMe drive takes its commands from queues in RAM that the kernel fills; one register write (a doorbell) tells it new work is waiting.</li>
          <li><b>The IOMMU.</b> A second address-translation unit, for devices: the kernel decides which parts of RAM each device may reach, so a faulty or untrusted device cannot write anywhere it likes.</li>
          <li><b>Why it pays.</b> Copying gigabytes a second through the CPU would take a core's whole attention; with DMA it takes almost none.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-8">
      <div class="diagram-label">Fig BR.8 · Direct memory access · the device writes RAM by itself</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-8"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-8', cap, card.replace('CAPID', cap))
