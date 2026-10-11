# Fig 16.7 · The CUDA hierarchy · thread → warp → block → grid (Pass 28, law 3). Quorum glass plate. A zoom: a grid of
# 8 blocks; one block of 4 warps; one warp of 32 threads. Then the warp's lockstep shown by a branch: if (i < 16) a();
# else b(); lanes 0 to 15 run a() while 16 to 31 wait, then the reverse, so a split warp pays for both paths.
# Phase-synced. t=0 (shift): the zoom drawn, both halves of the branch done.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# grid of 8 blocks
a(text(10, 18, 'grid of blocks', anchor='start', size=13, fill=QSOFT, ls='0'))
for i in range(8):
    x, y = 10 + (i % 4) * 30, 28 + (i // 4) * 30
    a(f'<rect x="{x}" y="{y}" width="26" height="26" rx="4" fill="{QCARD}" stroke="{VIOLET}" stroke-opacity="{1 if i == 0 else 0.5}" stroke-width="{2 if i == 0 else 1}"/>')
# zoom lines to the block
a(f'<path d="M36,28 L160,28 M36,54 L160,88" fill="none" stroke="{QMUTED}" stroke-opacity="0.4" stroke-dasharray="3 3"/>')
a(text(160, 18, 'block: up to 1,024 threads', anchor='start', size=13, fill=VIOLET, ls='0'))
for k in range(3):
    a(f'<rect x="{160 + k * 78}" y="28" width="72" height="60" rx="6" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="{1 if k == 0 else 0.5}" stroke-width="{2 if k == 0 else 1}"/>')
    a(text(160 + k * 78 + 36, 62, f'warp {k}', anchor='middle', size=13, fill=TEAL if k == 0 else QMUTED, ls='0'))
# the 32 lanes
LW, LX0, LY = 11, 23, 146
lane_x = lambda i: LX0 + i * LW
a(f'<path d="M160,88 L{LX0},{LY} M232,88 L{lane_x(31) + LW - 2},{LY}" fill="none" stroke="{QMUTED}" stroke-opacity="0.4" stroke-dasharray="3 3"/>')
for i in range(32):
    a(f'<rect x="{lane_x(i)}" y="{LY}" width="{LW - 2}" height="26" rx="2" fill="{QCARD}" stroke="{QMUTED}" stroke-opacity="0.5"/>')
a(text(lane_x(0), LY + 44, '0', anchor='start', size=13, fill=QMUTED, ls='0'))
a(text(lane_x(31) + LW - 2, LY + 44, '31', anchor='end', size=13, fill=QMUTED, ls='0'))
TA, TB, TE = 2.0, 4.2, 6.4
def half(lo, hi, col, t0, t1):
    cells = ''.join(f'<rect x="{lane_x(i)}" y="{LY}" width="{LW - 2}" height="26" rx="2" fill="{col}" fill-opacity="0.85"/>' for i in range(lo, hi))
    a(f'<g opacity="0">{lit(t0, t1)}{cells}</g>')
half(0, 16, VIOLET, TA, TB)
half(16, 32, QAMBER, TB, TE)
# the done state: both halves ran, shown dimmed
a(f'<g opacity="0">{win(TE)}' + ''.join(f'<rect x="{lane_x(i)}" y="{LY}" width="{LW - 2}" height="26" rx="2" fill="{VIOLET if i < 16 else QAMBER}" fill-opacity="0.45"/>' for i in range(32)) + '</g>')
a(text(10, LY + 66, 'warp: 32 threads, one instruction', anchor='start', size=13, fill=TEAL, ls='0'))
CY = LY + 98
a(text(10, CY, 'if (i &lt; 16) a(); else b();', anchor='start', size=13, fill=QSOFT, ls='0'))
for t0, t1, s, col in ((TA, TB, 'step 1: lanes 0–15 run a(), 16–31 wait', VIOLET), (TB, TE, 'step 2: lanes 16–31 run b(), 0–15 wait', QAMBER),
                       (TE, None, 'a split warp pays for both paths', QROSE)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, CY + 22, s, anchor="start", size=13, fill=col, ls="0")}</g>')
H = CY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-8 svgd-part5-8">')
o.insert(1, '<title id="svgt-part5-8">Fig 16.7 · The CUDA hierarchy · thread → warp → block → grid</title>')
o.insert(2, '<desc id="svgd-part5-8">A zoom through CUDA\'s hierarchy: a grid of blocks is one kernel launch; a block holds up to 1,024 threads in warps; a warp is 32 threads that execute one instruction together. '
  'When the code branches on the thread number, if i is less than 16 run a, else run b, lanes 0 to 15 run a while lanes 16 to 31 wait, then the other way round: a warp split by a branch pays for both paths.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A kernel launch is a grid of blocks, each block a set of warps, each warp 32 threads that execute one instruction together. '
           'When a branch splits a warp, the two halves take turns while the other waits, so divergent code runs at a fraction of the speed.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Blocks.</b> Threads in one block share fast on-chip memory (up to 227 KB per block on an H100) and can wait for each other; in the classic model separate blocks cannot, and share data through slow global memory.</li>
          <li><b>Memory.</b> Registers are per thread and nearly free; global memory (HBM, 80 GB on an H100) is huge and slow per access. Fast kernels keep data in shared memory and have each warp read neighbouring addresses together (coalesced access).</li>
          <li><b>The model.</b> The programmer writes one thread's code; the launch runs it for every thread of the grid, each finding its own index.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-7">
      <div class="diagram-label">Fig 16.7 · The CUDA hierarchy · thread → warp → block → grid</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-7"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-7', cap, card.replace('CAPID', cap))
