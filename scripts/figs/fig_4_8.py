# Fig 4.8 · x86-64 four-level page table walk (Pass 31 exemplar for Part II, from an empty script). Takeaway: an
# address splits into four indexes and an offset, and each index picks one entry per table level.
# Concept chosen of three (ledger): the four tables as Greenbar listing pages, one under the other, each showing the
# row its index picks; that row points to the next table, the last to the page, where the offset picks the byte.
# Motion steps (Part II's discrete motion): index by index, its row prints and its pointer drops to the next table.
# t=0 is the whole walk.
import figlib
from figlib import Timeline, text, obj, splice, PLEX, PHOS, PHOS_SOFT, PLATE, BLUE, MUTED
figlib.FONT = PLEX

IDX = [255, 488, 81, 300]
OFF = 1512
NAME = ['1st', '2nd', '3rd', '4th', 'offset']
INK = '#0c120e'
DIM = 'rgba(198,222,206,0.62)'

W, H = 400, 470
FY = 30                                  # address fields
PX0, PX1 = 96, 360                       # pages
PY0, PSTEP, PH = 112, 66, 58             # first page top, step, height
D = 11.0
T = Timeline(D, shift=10.4)
STEP = lambda k: T.beat(1.0 + 1.6 * k, f'index {k + 1}' if k < 4 else 'the offset')
RESET = 0.4
def held(t):  # off from the reset until t, then held to the end of the loop (on at t=0)
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.001, 0.0), (t - 0.001, 0.0), (t, 1.0), (D, 1.0)])
def unheld(t):
    return T.anim('opacity', [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, 1.0), (t - 0.001, 1.0), (t, 0.0), (D, 0.0)])

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-9 svgd-part2-9"{T.beats_attr()}>')
a('<title id="svgt-part2-9">Fig 4.8 · x86-64 four-level page table walk</title>')
a('<desc id="svgd-part2-9">A virtual address split into five parts: four indexes, 255, 488, 81 and 300, and an offset, 1512. '
  'Below it, four page tables drawn as listing pages, one under the other, and then the page of data. The CR3 register points '
  'to the first table. In it, the first index picks row 255, and that row points to the second table; there the second index '
  'picks row 488, which points to the third table; row 81 points to the fourth; row 300 points to the page of data, where the '
  'offset picks byte 1512. Four table reads and then the data: five reads for one load.</desc>')

# the address, split into its five fields
unit = 360 / 48
x = 20
for k, bits in enumerate([9, 9, 9, 9, 12]):
    w = bits * unit - 4
    col = BLUE if k == 4 else PHOS
    val = str(OFF if k == 4 else IDX[k])
    a(obj(f'<rect x="{x:.1f}" y="{FY}" width="{w:.1f}" height="46" rx="3" fill="none" stroke="{col}" stroke-width="1.5"/>',
          f'<rect x="{x - 2:.1f}" y="{FY - 2}" width="{w + 4:.1f}" height="50" rx="4" fill="none" stroke="{col}" stroke-width="3.5" opacity="0">'
          f'{T.anim("opacity", [(0.0, 0.0), (STEP(k) - 0.001, 0.0), (STEP(k), 1.0), (STEP(k) + 1.5, 1.0), (STEP(k) + 1.501, 0.0)])}</rect>',
          text(x + w / 2, FY + 18, NAME[k], anchor='middle', size=14, fill=DIM, ls='0'),
          text(x + w / 2, FY + 38, val, anchor='middle', size=16, fill=col, ls='0')))
    x += bits * unit
a(text(20, FY - 10, 'the address, split', size=14, fill=MUTED, ls='0', role='label'))

# CR3 into the first table
a(text(PX0 - 10, PY0 - 12, 'CR3', anchor='end', size=14, fill=PHOS_SOFT, ls='0', role='label'))
a(f'<path d="M {PX0 - 6} {PY0 - 16} H {PX0 + 24} V {PY0 - 6}" fill="none" stroke="{PHOS_SOFT}" stroke-width="1.6"/>'
  f'<polygon points="{PX0 + 19},{PY0 - 8} {PX0 + 24},{PY0} {PX0 + 29},{PY0 - 8}" fill="{PHOS_SOFT}"/>')

# the four tables and the page: three rows each, the picked one in the middle
for k in range(5):
    y = PY0 + k * PSTEP
    col = BLUE if k == 4 else PHOS
    i = OFF if k == 4 else IDX[k]
    # the table: its frame and its two plain rows, one object; its name beside it is a label
    rows = [f'<rect x="{PX0}" y="{y}" width="{PX1 - PX0}" height="{PH}" rx="3" fill="none" stroke="{col}" stroke-opacity="0.85" stroke-width="1.4"/>']
    for r in range(3):
        ry = y + 2 + r * 18
        if r != 1:
            rows.append(text(PX0 + 12, ry + 14, str(i - 1 + r), size=14, fill=DIM, ls='0'))
    a(obj(*rows))
    a(text(PX0 - 10, y + 34, NAME[k] if k < 4 else 'page', anchor='end', size=14, fill=MUTED, ls='0', role='label'))
    # the picked row, its own object: plain before its step, printed in full from its step on (one number whose
    # ink changes, not a second number drawn over it)
    ry = y + 20
    on = STEP(k) + 0.3
    ink = T.discrete('fill', [(0.0, INK), (RESET + 0.001, DIM), (on, INK)])
    a(obj(f'<rect x="{PX0 + 2}" y="{ry}" width="{PX1 - PX0 - 4}" height="18" fill="{col}" opacity="1">{held(on)}</rect>',
          text(PX0 + 12, ry + 14, str(i), size=14, fill=INK, ls='0', role='object').replace('</text>', f'{ink}</text>'),
          text(PX1 - 10, ry + 14, ('next' if k < 4 else 'byte'), anchor='end', size=14, fill=INK, ls='0', role='object', extra=' opacity="1"').replace('</text>', f'{held(on)}</text>')))
    if k < 4:  # the picked row points to the next table
        ny = y + PSTEP
        a(f'<g opacity="1">{held(STEP(k) + 0.9)}'
          f'<path d="M {PX1} {ry + 9} H {PX1 + 18} V {ny - 6} H {PX1 - 26}" fill="none" stroke="{PHOS_SOFT}" stroke-width="1.6"/>'
          f'<polygon points="{PX1 - 22},{ny - 11} {PX1 - 30},{ny - 6} {PX1 - 22},{ny - 1}" fill="{PHOS_SOFT}"/></g>')

# the result
a(f'<g opacity="1">{held(STEP(4) + 0.6)}' + text(20, H - 14, 'five reads: four tables, then the data', size=14, fill=PHOS, ls='0', role='label') + '</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The address splits into four indexes and an offset. Each index picks one row of its table, that row points to the '
           'next table and the last to the page, so one load costs five memory reads unless the TLB already holds the answer.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The split.</b> The CPU cuts a 48-bit address into four 9-bit indexes and a 12-bit offset.</li>
          <li><b>The tables.</b> Each table is one 4 KiB page of 512 eight-byte entries, so 9 bits pick a row (2<sup>9</sup> = 512).</li>
          <li><b>The walk.</b> CR3 holds where the first table sits. Each picked row holds where the next table sits; the fourth points to the page of data, and the offset picks the byte inside it.</li>
          <li><b>The cost.</b> Four table reads, then the data: five reads for one load. The TLB keeps recent answers, so most loads skip the walk.</li>
          <li><b>Sparse.</b> Tables exist only for the parts of the address space a process uses, so a few megabytes of tables map a whole program.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-8">
      <div class="diagram-label">Fig 4.8 · x86-64 four-level page table walk</div>
      {svg}
      <p id="ch4-vm-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-8', 'ch4-vm-p6', card)
