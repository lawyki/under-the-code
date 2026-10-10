# Fig 4.13 · Journaling (Pass 28, law 3). Journal slots fill with the change, then a commit record;
# a power cut follows. Run 1: the commit is there, so boot replays it into the main filesystem
# (v1 → v2). Run 2: the cut comes before the commit, so boot discards the change (v2 stays).
# t=0 (shift): run 1 finished, journal holding the committed change, main at v2.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 262
D = 13.0
T = Timeline(D, shift=6.45)
def lit(t0, t1):  # off-before-on: keyTimes round to ~1.3 ms here, so swaps leave a 3 ms gap
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
SX = [20, 112, 204, 296]; SW = 84; SY, SH = 40, 32
MX = [20, 144, 268]; MW = 112; MY, MH = 128, 50
NAMES = ['inode', 'bitmap', 'dir']
HOMES = ['inode', 'bitmap', 'directory']
A_SLOTS = [0.8, 1.3, 1.8]; A_COMMIT = 2.6; A_CUT = 3.4; A_BOOT = 4.4; A_APPLY = [4.8, 5.2, 5.6]; A_END = 6.6
B_SLOTS = [7.2, 7.7]; B_CUT = 8.4; B_BOOT = 9.4; B_DROP = 9.8; B_END = 11.2
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-14 svgd-part2-14">')
a('<title id="svgt-part2-14">Fig 4.13 · Journaling: write your intent before doing it</title>')
a('<desc id="svgd-part2-14">A journal region and the main filesystem. A change to an inode, the free-block bitmap and a directory is first written to the journal, then sealed with a commit record. '
  'The power is cut. On boot the kernel finds the commit record and replays the change into the main filesystem, which moves from version 1 to version 2. '
  'A second change is logged, but the power is cut before its commit record is written; on boot the kernel discards it, and the main filesystem stays at version 2, consistent either way.</desc>')
a(text(20, 28, 'JOURNAL', size=13, fill=MUTED))
a(text(20, MY + MH + 20, 'MAIN FILESYSTEM', size=13, fill=MUTED))
for x in SX:
    a(f'<rect x="{x}" y="{SY}" width="{SW}" height="{SH}" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.2)" stroke-dasharray="3 3"/>')
# faint home lines
for k in range(3):
    a(f'<line x1="{SX[k] + SW / 2}" y1="{SY + SH}" x2="{MX[k] + MW / 2}" y2="{MY}" stroke="rgba(198,222,206,0.18)" stroke-width="1.2" stroke-dasharray="3 4"/>')
    a(f'<line class="fx" x1="{SX[k] + SW / 2}" y1="{SY + SH}" x2="{MX[k] + MW / 2}" y2="{MY}" stroke="{PHOS}" stroke-width="2.5" opacity="0">{lit(A_APPLY[k] - 0.2, A_APPLY[k] + 0.5)}</line>')
def slot(k, label, t0, t1, col=PHOS, fill_op=0.22):
    x = SX[k]
    a(f'<g opacity="0">{lit(t0, t1)}<rect x="{x}" y="{SY}" width="{SW}" height="{SH}" rx="3" fill="{col}" fill-opacity="{fill_op}" stroke="{col}"/>'
      f'{text(x + SW / 2, SY + 21, label, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
# run 1: logged, committed, replayed (the journal is freed at A_END)
for k in range(3):
    slot(k, f'{NAMES[k]} v2', A_SLOTS[k], A_END)
slot(3, 'COMMIT', A_COMMIT, A_END, col=PHOS, fill_op=0.5)
# run 2: logged, never committed, discarded
for k in range(2):
    slot(k, f'{NAMES[k]} v3', B_SLOTS[k], B_END)
    a(f'<g class="fx" opacity="0">{lit(B_DROP, B_END)}<rect x="{SX[k]}" y="{SY}" width="{SW}" height="{SH}" rx="3" fill="{PLATE}" fill-opacity="0.55" stroke="{RED}" stroke-dasharray="4 3"/>'
      f'<line x1="{SX[k] + 8}" y1="{SY + SH / 2}" x2="{SX[k] + SW - 8}" y2="{SY + SH / 2}" stroke="{RED}" stroke-width="2"/></g>')
# power cut
for t0, t1 in ((A_CUT, A_BOOT), (B_CUT, B_BOOT)):
    a(f'<g class="fx" opacity="0">{lit(t0, t1)}<line x1="20" y1="{(SY + SH + MY) / 2 - 6}" x2="380" y2="{(SY + SH + MY) / 2 - 6}" stroke="{RED}" stroke-width="2.5" stroke-dasharray="10 6"/></g>')
# main filesystem: v1 until replay, then v2 (run 2 never touches it)
for k in range(3):
    x = MX[k]
    a(f'<rect x="{x}" y="{MY}" width="{MW}" height="{MH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.4)"/>')
    a(f'<rect class="fx" x="{x}" y="{MY}" width="{MW}" height="{MH}" rx="3" fill="{PHOS}" fill-opacity="0.2" stroke="{PHOS}" stroke-width="2" opacity="0">{lit(A_APPLY[k], A_APPLY[k] + 0.7)}</rect>')
    a(text(x + MW / 2, MY + 21, HOMES[k], anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
    a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (0.003, 1.0), (A_APPLY[k] - 0.008, 1.0), (A_APPLY[k] - 0.005, 0.0), (D, 0.0)])}{text(x + MW / 2, MY + 41, "v1", anchor="middle", size=14, fill="rgba(198,222,206,0.6)", ls="0")}</g>')
    a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (A_APPLY[k] - 0.002, 0.0), (A_APPLY[k], 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])}{text(x + MW / 2, MY + 41, "v2", anchor="middle", size=14, fill=PHOS, ls="0")}</g>')
# status
SYS = 246
STAT = [(0.3, A_COMMIT, 'log the change', PHOS_SOFT), (A_COMMIT, A_CUT, 'commit: now it is durable', PHOS_SOFT),
        (A_CUT, A_BOOT, 'power cut', RED), (A_BOOT, A_END + 0.3, 'boot: commit found, replay', PHOS),
        (A_END + 0.3, B_CUT, 'log the next change', PHOS_SOFT), (B_CUT, B_BOOT, 'power cut before commit', RED),
        (B_BOOT, 12.7, 'boot: no commit, discard', RED)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{lit(t0, t1)}{text(W / 2, SYS, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The change goes to the journal first, sealed by a commit record, and only then to its home in the filesystem. '
           'After a crash, boot replays every committed change and discards any without a commit, so the disk is consistent in seconds.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The atomic step.</b> The commit record is one small block, written after the rest of the entry has reached the disk. Whether it exists decides the outcome.</li>
          <li><b>What is logged.</b> By default ext4 and NTFS journal metadata only (inodes, bitmaps, directories); ext4's <code>data=journal</code> mode also logs file contents, writing them twice.</li>
          <li><b>The lineage.</b> This is write-ahead logging, taken from databases (Chapter 13). Before journals, <code>fsck</code> had to scan the whole disk after a crash, which took hours.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-13">
      <div class="diagram-label">Fig 4.13 · Journaling: write your intent before doing it</div>
      {svg}
      <p id="ch4-fs-p10" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-13', 'ch4-fs-p10', card)
