# Fig 4.8 · x86-64 four-level page table walk (Pass 28, law 3). One real address split into its
# four 9-bit indices and 12-bit offset; CR3 leads to the top table, each chosen entry points to the
# next table, and the last one to the page. A counter fills to five reads for one load.
# t=0: the whole walk drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, BLUE, MUTED
figlib.FONT = PLEX

IDX = [255, 488, 81, 300]
OFF = 0x5E8
VA = IDX[0] << 39 | IDX[1] << 30 | IDX[2] << 21 | IDX[3] << 12 | OFF
h = f'{VA:012X}'
VA_TXT = f'0x{h[:4]}_{h[4:8]}_{h[8:]}'

W, H = 400, 432
FX0, FX1 = 20, 380                       # address fields
BITW = (FX1 - FX0) / 48
SX0, SX1 = 70, 372                       # table strips
ROW0, ROWH, STRIP = 150, 46, 22
D = 11.0
T = Timeline(D, shift=10.4)
STEP = lambda k: 1.0 + 1.6 * k           # story time step k starts (k = 0..4)
RESET = 0.4
def on_at(t):  # complete at t=0, cleared at RESET, back on at t, held to the loop end
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.001, 0.0), (t - 0.001, 0.0), (t, 1.0), (D, 1.0)])
def lit(t0, t1):  # only during one step
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.001, 1.0), (t1, 0.0), (D, 0.0)])

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-9 svgd-part2-9">')
a('<title id="svgt-part2-9">Fig 4.8 · x86-64 four-level page table walk</title>')
a(f'<desc id="svgd-part2-9">The 48-bit virtual address {VA_TXT} split into four 9-bit table indexes (255, 488, 81, 300) and a 12-bit page offset (1512). '
  'The CR3 register holds the address of the top table. Entry 255 of the level-4 table points to a level-3 table, its entry 488 to a level-2 table, entry 81 to a level-1 table, '
  'and entry 300 to the physical page, where the offset picks the byte. Four table reads and then the data: five memory reads for one load.</desc>')
a(text(FX0, 22, f'VIRTUAL ADDRESS {VA_TXT}', size=13, fill=MUTED))
fields = [('L4', 9, str(IDX[0])), ('L3', 9, str(IDX[1])), ('L2', 9, str(IDX[2])), ('L1', 9, str(IDX[3])), ('offset', 12, str(OFF))]
x = FX0
for k, (name, bits, val) in enumerate(fields):
    w = bits * BITW - 4
    col = BLUE if k == 4 else PHOS
    a(f'<rect x="{x:.1f}" y="34" width="{w:.1f}" height="46" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.45"/>')
    a(f'<rect class="fx" x="{x:.1f}" y="34" width="{w:.1f}" height="46" rx="3" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="2" opacity="0">{lit(STEP(k), STEP(k) + 1.6)}</rect>')
    a(text(x + w / 2, 52, name, anchor='middle', size=13, fill=MUTED, ls='0'))
    a(text(x + w / 2, 72, val, anchor='middle', size=15, fill=col, ls='0'))
    a(text(x + w / 2, 98, f'{bits} bits', anchor='middle', size=13, fill='rgba(198,222,206,0.6)', ls='0'))
    x += bits * BITW

# CR3 into the top table
a(text(FX0, 130, 'CR3', size=13, fill=PHOS_SOFT, ls='0'))
a(f'<path d="M{FX0 + 32} 126 H{SX0 - 14} V{ROW0 + STRIP / 2} H{SX0 - 4}" fill="none" stroke="{PHOS_SOFT}" stroke-width="1.5"/>')
a(f'<polygon points="{SX0 - 4},{ROW0 + STRIP / 2 - 4} {SX0 + 2},{ROW0 + STRIP / 2} {SX0 - 4},{ROW0 + STRIP / 2 + 4}" fill="{PHOS_SOFT}"/>')
rows = [('L4', 512, IDX[0]), ('L3', 512, IDX[1]), ('L2', 512, IDX[2]), ('L1', 512, IDX[3]), ('page', 4096, OFF)]
for k, (name, n, i) in enumerate(rows):
    y = ROW0 + k * ROWH
    col = BLUE if k == 4 else PHOS
    a(text(FX0, y + 16, name, size=13, fill=MUTED, ls='0'))
    a(f'<rect x="{SX0}" y="{y}" width="{SX1 - SX0}" height="{STRIP}" rx="2" fill="{PLATE}" stroke="rgba(132,255,178,0.3)"/>')
    for q in range(1, 8):  # faint ruling: many entries
        xq = SX0 + q * (SX1 - SX0) / 8
        a(f'<line x1="{xq:.1f}" y1="{y + 3}" x2="{xq:.1f}" y2="{y + STRIP - 3}" stroke="rgba(132,255,178,0.12)"/>')
    mx = SX0 + i / n * (SX1 - SX0)
    t = STEP(k) + 0.3
    a(f'<g opacity="1">{on_at(t)}'
      f'<rect x="{mx - 4:.1f}" y="{y - 2}" width="8" height="{STRIP + 4}" rx="1" fill="{col}"/>'
      f'</g>')
    if k < 4:  # the entry points to the start of the next table
        ny = y + ROWH
        t2 = STEP(k) + 0.9
        a(f'<g opacity="1">{on_at(t2)}'
          f'<path d="M{mx:.1f} {y + STRIP + 2} L{SX0 + 6} {ny - 4}" fill="none" stroke="{PHOS_SOFT}" stroke-width="1.5"/>'
          f'<polygon points="{SX0 + 1},{ny - 2} {SX0 + 12},{ny - 7} {SX0 + 7},{ny - 12}" fill="{PHOS_SOFT}"/>'
          f'</g>')
a(text(SX1, ROW0 + 4 * ROWH + STRIP + 20, '4096 bytes', anchor='end', size=13, fill='rgba(198,222,206,0.6)', ls='0'))
a(text(SX1, ROW0 - 8, '512 entries each', anchor='end', size=13, fill='rgba(198,222,206,0.6)', ls='0'))

# five reads
yb = ROW0 + 4 * ROWH + STRIP + 40
a(text(FX0, yb + 17, 'reads', size=13, fill=MUTED, ls='0'))
for k in range(5):
    bx = SX0 + k * 62
    col = BLUE if k == 4 else PHOS
    a(f'<rect x="{bx}" y="{yb}" width="54" height="24" rx="2" fill="none" stroke="rgba(132,255,178,0.3)"/>')
    a(f'<g opacity="1">{on_at(STEP(k) + 0.3)}<rect x="{bx}" y="{yb}" width="54" height="24" rx="2" fill="{col}" fill-opacity="0.3" stroke="{col}"/>'
      f'{text(bx + 27, yb + 17, "data" if k == 4 else rows[k][0], anchor="middle", size=13, fill="#fff", ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The CPU splits a 48-bit address into four 9-bit indexes and a 12-bit offset, then follows CR3 down a tree of four tables, one index per level. Four table reads come before the data itself: five memory reads for one load, unless the TLB already holds the answer.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why 9 bits.</b> A table is one 4 KiB page of 8-byte entries, so it holds 512 of them, and 2<sup>9</sup> = 512. The last 12 bits address a byte inside a 4 KiB page.</li>
          <li><b>The pointers.</b> CR3 holds the physical address of the top table; each entry holds the physical address of the next table down, plus permission bits.</li>
          <li><b>Sparse by design.</b> Tables exist only for regions the process uses, so a few megabytes of tables map a whole program. Newer CPUs can add a fifth level for 57-bit addresses.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-8">
      <div class="diagram-label">Fig 4.8 · x86-64 four-level page table walk</div>
      {svg}
      <p id="ch4-vm-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(VA_TXT)
    splice('part-2', 'fig-4-8', 'ch4-vm-p6', card)
