# Fig 5.4 · A pointer walks down memory (Pass 28, law 3). One ribbon of memory, three pointers that
# start at 0x100 and take the same step, ++, together: char moves 1 byte, int 4, double 8. A bracket
# under each marker spans what *p reads. t=0 (shift): each pointer one step in.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 240
RX, BW = 96, 8.75          # ribbon left, units per byte (32 bytes = 280)
RY, RH = 30, 34
VALS = ['17', '42', '99', '−7', '23', '8', '61', '12']
D = 8.0
T = Timeline(D, shift=1.7)
TICK = [0.4 + 0.9 * k for k in range(8)]   # TICK[k]: after k steps
LANES = [('char *c', '+1', 1, PHOS_SOFT, 108), ('int *p', '+4', 4, PHOS, 152), ('double *d', '+8', 8, BLUE, 196)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-28 svgd-part2-28">')
a('<title id="svgt-part2-28">Fig 5.4 · A pointer walks down memory</title>')
a('<desc id="svgd-part2-28">Thirty-two bytes of memory from address 0x100, holding eight 4-byte ints: 17, 42, 99, −7, 23, 8, 61, 12. '
  'Three pointers start at 0x100 and each is incremented together. The char pointer moves one byte per step, the int pointer four, the double pointer eight. '
  'A bracket under each shows how many bytes it reads: one, four or eight.</desc>')
# ribbon: int cells with byte ticks
for k, v in enumerate(VALS):
    x = RX + k * 4 * BW
    a(f'<rect x="{x:.1f}" y="{RY}" width="{4 * BW:.1f}" height="{RH}" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
    for b in (1, 2, 3):
        a(f'<line x1="{x + b * BW:.1f}" y1="{RY + RH - 7}" x2="{x + b * BW:.1f}" y2="{RY + RH}" stroke="rgba(132,255,178,0.3)"/>')
    a(text(x + 2 * BW, RY + 21, v, anchor='middle', size=13, fill='#fff', ls='0'))
    if k % 2 == 0:
        a(text(x, RY + RH + 18, f'0x{0x100 + 4 * k:X}', anchor='start', size=13, fill=MUTED, ls='0'))
for name, step, size, col, ly in LANES:
    a(text(20, ly + 14, name, size=13, fill=col, ls='0'))
    a(f'<rect x="{RX}" y="{ly}" width="{32 * BW:.1f}" height="20" rx="2" fill="{PLATE}" stroke="rgba(198,222,206,0.15)"/>')
    nmax = min(7, (32 - size) // size)
    xs = [RX + min(k, nmax) * size * BW for k in range(8)]
    pts = [(0.0, 0.0)]
    for k in range(1, 8):
        pts += [(TICK[k] - 0.15, xs[k - 1] - RX), (TICK[k], xs[k] - RX)]
    pts += [(D - 0.5, xs[-1] - RX), (D - 0.2, 0.0), (D, 0.0)]
    a(f'<g>{T.translate(pts, "x")}<rect class="fx" x="{RX}" y="{ly}" width="{size * BW:.1f}" height="20" rx="2" fill="{col}" fill-opacity="0.45" stroke="{col}" stroke-width="1.5"/></g>')
    for k in range(8):
        if k and xs[k] == xs[k - 1]:
            continue
        t0 = TICK[k] if k else 0.0
        nxt = next((TICK[j] for j in range(k + 1, 8) if xs[j] != xs[k]), D - 0.2)
        pts2 = ([(0.0, 1.0)] if k == 0 else [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0)]) + [(nxt - 0.008, 1.0), (nxt - 0.005, 0.0)]
        if k == 0: pts2 += [(D - 0.2 - 0.002, 0.0), (D - 0.2, 1.0), (D, 1.0)]
        else: pts2 += [(D, 0.0)]
        addr = 0x100 + int(round((xs[k] - RX) / BW))
        a(f'<g>{T.anim("opacity", pts2)}{text(20, ly + 34, f"= 0x{addr:X}", size=13, fill=MUTED, ls="0")}</g>')
a(text(RX + 32 * BW, RY - 10, 'each ++ moves one element', anchor='end', size=13, fill=MUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Three pointers start at 0x100 and take the same step, <code>++</code>: the <code>char</code> pointer moves 1 byte, the <code>int</code> pointer 4, the <code>double</code> pointer 8. '
           'The compiler scales pointer arithmetic by the size of the type, so <code>p + 1</code> always means the next element, never the next byte.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The sizes.</b> A <code>char</code> is 1 byte by definition; <code>int</code> is 4 and <code>double</code> 8 on today's common machines, though the standard only sets minimums.</li>
          <li><b>What <code>*p</code> reads.</b> The bracket under each pointer is the span a dereference loads: one, four or eight bytes from its address.</li>
          <li><b>Where it leads.</b> Strings are <code>char</code> pointers walking to a zero byte, and arrays are the same arithmetic in disguise, as the next figure shows.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-4">
      <div class="diagram-label">Fig 5.4 · A pointer walks down memory</div>
      {svg}
      <p id="ch5-pointers-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-4', 'ch5-pointers-p4', card)
