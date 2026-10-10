# Fig 4.10 · Fork, then write (Pass 28, law 3). Parent page table | physical frames | child page
# table. After fork both tables point at the same frames, read-only. The child writes page B: a
# fault, the kernel copies B into a new frame and re-points only the child's entry, now writable.
# t=0 (shift): the finished state, B copied.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 300
PX, FX, CX, CW = 20, 150, 280, 100
ROWS = [('A', 52), ('B', 94), ('C', 136)]
RH = 32
NEWY = 190
D = 10.0
T = Timeline(D, shift=9.0)
WRITE, COPY, REPOINT = 2.6, 3.8, 4.8
def on_from(t):
    return T.anim('opacity', [(0.0, 0.0), (t - 0.001, 0.0), (t, 1.0), (D, 1.0)])
def on_until(t):
    return T.anim('opacity', [(0.0, 1.0), (t - 0.001, 1.0), (t, 0.0), (D, 0.0)])
def on_between(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.001, 1.0), (t1, 0.0), (D, 0.0)])
LINE = 'rgba(198,222,206,0.6)'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-11 svgd-part2-11">')
a('<title id="svgt-part2-11">Fig 4.10 · Fork, then write: when shared pages diverge</title>')
a('<desc id="svgd-part2-11">The parent\'s and the child\'s page tables after fork both point at the same three physical pages, A, B and C, all marked read-only, so nothing has been copied. '
  'The child writes to page B. The write faults; the kernel copies B into a new physical page and points the child\'s entry at the copy, now read-write. '
  'Pages A and C stay shared, and the parent never notices.</desc>')
for x, lab in ((PX, 'parent'), (FX, 'RAM'), (CX, 'child')):
    a(text(x + CW / 2, 30, lab, anchor='middle', size=13, fill=MUTED, ls='0'))
for name, y in ROWS:
    # frames
    a(f'<rect x="{FX}" y="{y}" width="{CW}" height="{RH}" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.5)"/>')
    a(text(FX + CW / 2, y + 21, f'page {name}', anchor='middle', size=13, fill=PHOS, ls='0'))
    for x in (PX, CX):
        a(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.3)"/>')
        a(text(x + 12, y + 21, name, size=14, fill='#fff', ls='0'))
    ym = y + RH / 2
    a(f'<line x1="{PX + CW}" y1="{ym}" x2="{FX}" y2="{ym}" stroke="{LINE}" stroke-width="1.5"/>')
    tag_x = PX + CW - 12
    a(text(tag_x, y + 21, 'RO', anchor='end', size=13, fill=GOLD, ls='0'))
    if name != 'B':
        a(f'<line x1="{CX}" y1="{ym}" x2="{FX + CW}" y2="{ym}" stroke="{LINE}" stroke-width="1.5"/>')
        a(text(CX + CW - 12, y + 21, 'RO', anchor='end', size=13, fill=GOLD, ls='0'))
    else:
        yb = y
        a(f'<g>{on_until(REPOINT)}<line x1="{CX}" y1="{ym}" x2="{FX + CW}" y2="{ym}" stroke="{LINE}" stroke-width="1.5"/>'
          f'{text(CX + CW - 12, y + 21, "RO", anchor="end", size=13, fill=GOLD, ls="0")}</g>')
        a(f'<g>{on_from(REPOINT)}<path d="M{CX} {ym} H{CX - 14} V{NEWY + RH / 2} H{FX + CW}" fill="none" stroke="{PHOS}" stroke-width="2"/>'
          f'{text(CX + CW - 12, y + 21, "RW", anchor="end", size=13, fill=PHOS, ls="0")}</g>')
        # the write faults
        a(f'<rect class="fx" x="{CX}" y="{y}" width="{CW}" height="{RH}" rx="3" fill="{RED}" fill-opacity="0.25" stroke="{RED}" stroke-width="2" opacity="0">{on_between(WRITE, COPY)}</rect>')
# the copy
a(f'<g>{on_from(COPY)}<rect x="{FX}" y="{NEWY}" width="{CW}" height="{RH}" rx="3" fill="{PLATE}" stroke="{PHOS}" stroke-width="2"/>'
  f'{text(FX + CW / 2, NEWY + 21, "copy of B", anchor="middle", size=13, fill=PHOS, ls="0")}</g>')
a(f'<g class="fx" opacity="0">{on_between(COPY, REPOINT)}<path d="M{FX + CW / 2} {ROWS[1][1] + RH + 4} V{NEWY - 4}" stroke="{PHOS}" stroke-width="2" stroke-dasharray="4 4"/>'
  f'<polygon points="{FX + CW / 2 - 5},{NEWY - 10} {FX + CW / 2 + 5},{NEWY - 10} {FX + CW / 2},{NEWY - 2}" fill="{PHOS}"/></g>')
# step line
SY = 262
steps = [(0.0, WRITE, 'fork(): shared, nothing copied'), (WRITE, COPY, 'child writes B: page fault'), (COPY, REPOINT, 'kernel copies B'), (REPOINT, D, 'child gets its own B; 1 page copied')]
for t0, t1, s in steps:
    an = on_between(t0, t1) if t1 < D else on_from(t0)
    if t0 == 0.0: an = on_until(t1)
    a(f'<g>{an}{text(W / 2, SY, s, anchor="middle", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('After <code>fork()</code> the two page tables point at the same pages, all read-only, and nothing is copied. '
           'When the child writes page B, the fault makes the kernel copy that one page and give the child its own; A and C stay shared.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The trap.</b> Marking shared pages read-only turns the first write into a page fault, so the kernel learns exactly which page needs copying, when.</li>
          <li><b>The parent's side.</b> If the parent writes B later, the kernel sees that nobody else maps it any more and simply makes it writable again, without a copy.</li>
          <li><b>Fork, then exec.</b> A child that calls <code>execve()</code> straight away replaces its address space before writing anything, so launching a program copies almost no pages.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-10">
      <div class="diagram-label">Fig 4.10 · Fork, then write: when shared pages diverge</div>
      {svg}
      <p id="ch4-vm-p16" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-10', 'ch4-vm-p16', card)
