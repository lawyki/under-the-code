# Fig 4.9 · A page fault, decision tree (Pass 28, law 3). Two questions decide every fault: is the
# access legal, and is the data already in RAM? Three example accesses take the three exits in
# turn (stepped, the Greenbar idiom). t=0: the whole tree, nothing lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 352
L, C, R = 72, 200, 328
CW = 116
D = 12.0
T = Timeline(D, shift=0.0)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.001, 1.0), (t1, 0.0), (D, 0.0)])
o = []; a = o.append
LINE = 'rgba(132,255,178,0.35)'
def box(x, y, w, h, stroke=LINE, fill=PANEL):
    a(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}"/>')
def glow(x, y, w, h, col, t0, t1):
    a(f'<rect class="fx" x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2" opacity="0">{lit(t0, t1)}</rect>')
def wire(d, t_list=()):
    a(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    for col, t0, t1 in t_list:
        a(f'<path class="fx" d="{d}" fill="none" stroke="{col}" stroke-width="2.5" opacity="0">{lit(t0, t1)}</path>')
def head(x, y, col=LINE):
    a(f'<polygon points="{x - 5},{y - 7} {x + 5},{y - 7} {x},{y}" fill="{col}"/>')

a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-10 svgd-part2-10">')
a('<title id="svgt-part2-10">Fig 4.9 · A page fault, decision tree</title>')
a('<desc id="svgd-part2-10">Three memory accesses fault and reach the kernel handler, which asks two questions. Is the address mapped and the access allowed? '
  'If not, the fault is invalid: the process gets SIGSEGV, as a write through a NULL pointer does. If it is legal, is the data already in RAM? '
  'If yes, a minor fault: the kernel only fills in the page-table entry and resumes the process in microseconds, as for a shared-library page already cached. '
  'If no, a major fault: the kernel reads the page from disk, which takes milliseconds, as the first read of a memory-mapped file does.</desc>')

# the three accesses (episodes), each with its exit
EP = [  # chip x, label, exit column, colour, passes Q2
    (L, 'cached page', L, PHOS, True),
    (C, 'mmap read', C, GOLD, True),
    (R, '*NULL = 1', R, RED, False),
]
S = lambda e: 0.6 + 3.7 * e
for e, (cx, lab, ex, col, q2) in enumerate(EP):
    box(cx - CW / 2, 8, CW, 30)
    glow(cx - CW / 2, 8, CW, 30, col, S(e), S(e) + 3.4)
    a(text(cx, 28, lab, anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
    wire(f'M{cx} 38 L{cx} 48 L{C} 58 L{C} 64', [(col, S(e) + 0.25, S(e) + 3.4)])
head(C, 64)

# handler
box(C - 120, 64, 240, 32)
for e, (_, _, _, col, _) in enumerate(EP):
    glow(C - 120, 64, 240, 32, col, S(e) + 0.5, S(e) + 1.0)
a(text(C, 85, '#PF · kernel handler', anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
wire(f'M{C} 96 V122', [(col, S(e) + 0.75, S(e) + 3.4) for e, (_, _, _, col, _) in enumerate(EP)])
head(C, 122)

# Q1
box(C - 78, 122, 156, 46)
for e, (_, _, _, col, _) in enumerate(EP):
    glow(C - 78, 122, 156, 46, col, S(e) + 1.0, S(e) + 1.5)
a(text(C, 141, 'mapped address,', anchor='middle', size=13, fill='#fff', ls='0'))
a(text(C, 159, 'access allowed?', anchor='middle', size=13, fill='#fff', ls='0'))
# Q1 no -> invalid
wire(f'M{C + 78} 145 H{R} V270', [(RED, S(2) + 1.25, S(2) + 3.4)])
head(R, 270)
a(text(R - 18, 138, 'no', size=13, fill=MUTED, ls='0'))
# Q1 yes -> Q2
wire(f'M{C} 168 V198', [(EP[e][3], S(e) + 1.25, S(e) + 3.4) for e in (0, 1)])
head(C, 198)
a(text(C + 8, 188, 'yes', size=13, fill=MUTED, ls='0'))

# Q2
box(C - 66, 198, 132, 32)
for e in (0, 1):
    glow(C - 66, 198, 132, 32, EP[e][3], S(e) + 1.5, S(e) + 2.0)
a(text(C, 219, 'page in RAM?', anchor='middle', size=13, fill='#fff', ls='0'))
wire(f'M{C - 66} 214 H{L} V270', [(PHOS, S(0) + 1.75, S(0) + 3.4)])
head(L, 270)
a(text(C - 100, 207, 'yes', size=13, fill=MUTED, ls='0'))
wire(f'M{C} 230 V270', [(GOLD, S(1) + 1.75, S(1) + 3.4)])
head(C, 270)
a(text(C + 8, 256, 'no', size=13, fill=MUTED, ls='0'))

# exits
EXITS = [(L, 'minor', 'map it', '~µs', PHOS), (C, 'major', 'read disk', '~ms', GOLD), (R, 'invalid', 'SIGSEGV', 'dies', RED)]
for k, (x, name, act, cost, col) in enumerate(EXITS):
    box(x - CW / 2, 270, CW, 74, stroke=col, fill=PLATE)
    t_in = S(k) + (2.0 if k < 2 else 1.5)
    glow(x - CW / 2, 270, CW, 74, col, t_in, S(k) + 3.4)
    a(text(x, 292, name, anchor='middle', size=15, fill=col, ls='0'))
    a(text(x, 313, act, anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
    a(text(x, 333, cost, anchor='middle', size=13, fill='rgba(198,222,206,0.6)', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Most page faults are not errors. The kernel asks two questions, and three accesses take the three exits: '
           'a cached page is mapped in microseconds, a first read of a mapped file waits milliseconds for the disk, and a write through NULL ends in SIGSEGV.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Minor.</b> The data is already in RAM (a page another process has loaded, the page cache, or a fresh zero-filled page), so the kernel only writes the page-table entry.</li>
          <li><b>Major.</b> The kernel starts the disk read, runs other processes while it waits, then maps the page and resumes: about a thousand times slower than a minor fault.</li>
          <li><b>Invalid.</b> The address is unmapped or the access breaks the mapping's permissions; unless the process catches SIGSEGV, it dies with "segmentation fault".</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-9">
      <div class="diagram-label">Fig 4.9 · A page fault, decision tree</div>
      {svg}
      <p id="ch4-vm-p13" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-9', 'ch4-vm-p13', card)
