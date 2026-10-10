# Fig 4.12 · Filename → inode → data blocks (Pass 28, law 3). A directory is a list of
# (name, inode) pairs; two names hold inode 4827, so they are one file. The inode lists the
# blocks, scattered on disk. Opening notes.txt, then backup.txt, lights the same inode and the
# same blocks (stepped). t=0: the whole map, nothing lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

W, H = 400, 384
X0, X1 = 20, 372
RY, RH, RG = 34, 28, 4
ENTRIES = [('notes.txt', 4827), ('draft.md', 4828), ('photo.jpg', 4829), ('backup.txt', 4827)]
BLOCKS = [102, 103, 104, 500, 501]
SIZE = '18,400'          # five 4 KB blocks hold it: 4 × 4096 < 18,400 ≤ 5 × 4096
assert 4 * 4096 < int(SIZE.replace(',', '')) <= 5 * 4096
IY, IH = 172, 76
CELLS = [101, 102, 103, 104, 105, None, 499, 500, 501, 502]
CY, CWD, CH = 290, 34, 30
D = 11.0
T = Timeline(D, shift=0.0)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.001, 1.0), (t1, 0.0), (D, 0.0)])
EP = [(0, 0.8), (3, 5.8)]          # (directory row, start)
LEN = 4.4
LINE = 'rgba(198,222,206,0.5)'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-13 svgd-part2-13">')
a('<title id="svgt-part2-13">Fig 4.12 · Filename → inode → data blocks</title>')
a('<desc id="svgd-part2-13">The directory /home/yki is a list of names and inode numbers: notes.txt 4827, draft.md 4828, photo.jpg 4829, backup.txt 4827. '
  f'notes.txt and backup.txt hold the same inode number, so they are one file with two names, a hard link. Inode 4827 records the size ({SIZE} bytes), the permissions, a link count of 2, '
  'and the data blocks 102, 103, 104, 500 and 501, which sit in two separate places on the disk. Opening either name reaches the same inode and the same blocks.</desc>')
a(text(X0, 20, 'DIRECTORY /home/yki', size=13, fill=MUTED))
rows_mid = []
for k, (name, ino) in enumerate(ENTRIES):
    y = RY + k * (RH + RG)
    rows_mid.append(y + RH / 2)
    a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="{RH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.3)"/>')
    for r, t0 in EP:
        if r == k:
            a(f'<rect class="fx" x="{X0}" y="{y}" width="{X1 - X0}" height="{RH}" rx="3" fill="{PHOS}" fill-opacity="0.16" stroke="{PHOS}" stroke-width="2" opacity="0">{lit(t0, t0 + LEN)}</rect>')
    hot = ino == 4827
    a(text(X0 + 12, y + 19, name, size=14, fill='#fff' if hot else PHOS_SOFT, ls='0'))
    a(text(X1 - 12, y + 19, f'→ {ino}', anchor='end', size=14, fill=PHOS if hot else 'rgba(198,222,206,0.6)', ls='0'))
# both 4827 entries feed one bracket into the inode
BX = X1 + 14
br = f'M{X1} {rows_mid[0]} H{BX} V{rows_mid[3]} H{X1} M{BX} {rows_mid[3]} V{IY + 26} H{X1 + 4}'
a(f'<path d="{br}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
for r, t0 in EP:
    seg = f'M{X1} {rows_mid[r]} H{BX} ' + (f'V{IY + 26} H{X1 + 4}' if r == 3 else f'V{IY + 26} H{X1 + 4}')
    a(f'<path class="fx" d="{seg}" fill="none" stroke="{PHOS}" stroke-width="2.5" opacity="0">{lit(t0 + 0.6, t0 + LEN)}</path>')
a(f'<polygon points="{X1 + 10},{IY + 21} {X1 + 10},{IY + 31} {X1 + 2},{IY + 26}" fill="{PHOS_SOFT}"/>')

# inode
a(f'<rect x="{X0}" y="{IY}" width="{X1 - X0}" height="{IH}" rx="3" fill="{PLATE}" stroke="{PHOS}" stroke-opacity="0.6"/>')
for r, t0 in EP:
    a(f'<rect class="fx" x="{X0}" y="{IY}" width="{X1 - X0}" height="{IH}" rx="3" fill="{PHOS}" fill-opacity="0.14" stroke="{PHOS}" stroke-width="2" opacity="0">{lit(t0 + 1.2, t0 + LEN)}</rect>')
a(text(X0 + 12, IY + 22, 'inode 4827', size=15, fill=PHOS, ls='0'))
a(text(X0 + 12, IY + 44, f'{SIZE} bytes · rw-r--r--', size=13, fill=PHOS_SOFT, ls='0'))
a(text(X0 + 12, IY + 64, 'links 2 · blocks 102–104, 500–501', size=13, fill=PHOS_SOFT, ls='0'))

# disk
cx = {}
x = X0
for c in CELLS:
    if c is None:
        a(text(x + 12, CY + 20, '…', anchor='middle', size=14, fill='rgba(198,222,206,0.6)', ls='0'))
        x += 24
        continue
    on = c in BLOCKS
    a(f'<rect x="{x}" y="{CY}" width="{CWD - 2}" height="{CH}" rx="2" fill="{PHOS if on else PANEL}" fill-opacity="{0.3 if on else 1}" stroke="{PHOS if on else "rgba(132,255,178,0.25)"}"/>')
    a(text(x + (CWD - 2) / 2, CY + 20, str(c), anchor='middle', size=13, fill='#fff' if on else 'rgba(198,222,206,0.55)', ls='0'))
    cx[c] = x + (CWD - 2) / 2
    x += CWD
for k, b in enumerate(BLOCKS):
    sx = X0 + 40 + k * 24
    a(f'<line x1="{sx}" y1="{IY + IH}" x2="{cx[b]:.1f}" y2="{CY - 2}" stroke="{LINE}" stroke-width="1.2"/>')
    for r, t0 in EP:
        tb = t0 + 1.8 + 0.3 * k
        a(f'<line class="fx" x1="{sx}" y1="{IY + IH}" x2="{cx[b]:.1f}" y2="{CY - 2}" stroke="{PHOS}" stroke-width="2.5" opacity="0">{lit(tb, t0 + LEN)}</line>')
        a(f'<rect class="fx" x="{cx[b] - (CWD - 2) / 2:.1f}" y="{CY}" width="{CWD - 2}" height="{CH}" rx="2" fill="none" stroke="#fff" stroke-width="2" opacity="0">{lit(tb, t0 + LEN)}</rect>')
a(text(X0, CY + CH + 22, 'DISK BLOCKS', size=13, fill=MUTED))
# status line
SY = CY + CH + 52
st = [(EP[0][1], EP[0][1] + LEN, 'open notes.txt → inode 4827'), (EP[1][1], EP[1][1] + LEN, 'open backup.txt → same inode')]
for t0, t1, s in st:
    a(f'<g opacity="0">{lit(t0, t1)}{text(W / 2, SY, s, anchor="middle", size=13, fill=PHOS_SOFT, ls="0")}</g>')
rest = [(0.0, 1.0), (EP[0][1] - 0.001, 1.0), (EP[0][1], 0.0), (EP[0][1] + LEN - 0.001, 0.0), (EP[0][1] + LEN, 1.0),
        (EP[1][1] - 0.001, 1.0), (EP[1][1], 0.0), (EP[1][1] + LEN - 0.001, 0.0), (EP[1][1] + LEN, 1.0), (D, 1.0)]
a(f'<g>{T.anim("opacity", rest)}{text(W / 2, SY, "two names, one file: a hard link", anchor="middle", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The name lives in the directory and the file lives in the inode: notes.txt and backup.txt hold the same inode number, so they are one file with two names. '
           'The inode lists the file\'s blocks, which can sit far apart on the disk.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Lookup.</b> Opening <code>/home/yki/notes.txt</code> reads one directory per path component, from <code>/</code> down, until the last name gives the inode number.</li>
          <li><b>Hard links.</b> The link count says how many names point at the inode. Deleting a name lowers it; the data is freed only when it reaches zero.</li>
          <li><b>Runs of blocks.</b> Modern filesystems (ext4, XFS, APFS) record runs such as 102–104 instead of every block number, and try to keep a file's blocks together.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-12">
      <div class="diagram-label">Fig 4.12 · Filename → inode → data blocks</div>
      {svg}
      <p id="ch4-fs-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-12', 'ch4-fs-p5', card)
