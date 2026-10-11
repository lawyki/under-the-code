# Fig 16.6 · CPU vs GPU · few clever cores vs thousands of simple ones (Pass 28, law 3). Quorum glass plate. The same
# job, shade 64 pixels, on both. A CPU with 4 fast cores does 4 pixels per quick step: 16 steps. A GPU with 64 slow,
# simple lanes does all 64 in one step four times as long. Both grids fill on one clock, so the GPU finishes at a
# quarter of the CPU's time even though each lane is four times slower. Phase-synced. t=0 (shift): both grids full.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

N, CPU_CORES, GPU_LANES = 64, 4, 64
STEP_CPU, STEP_GPU = 0.4, 1.6                      # a GPU lane is 4 times slower per operation
T_CPU = (N // CPU_CORES) * STEP_CPU
T_GPU = (N // GPU_LANES) * STEP_GPU
assert (T_CPU, T_GPU) == (6.4, 1.6)
W = 400
D = 10.0
T0 = 1.0
T = Timeline(D, shift=9.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
C = 20
def grid(x0, y0, done_at, col):
    for i in range(N):
        cx, cy = x0 + (i % 8) * C, y0 + (i // 8) * C
        a(f'<rect x="{cx}" y="{cy}" width="{C - 3}" height="{C - 3}" rx="2" fill="{QCARD}" stroke="{QMUTED}" stroke-opacity="0.3"/>')
        a(f'<g opacity="0">{win(done_at(i))}<rect x="{cx}" y="{cy}" width="{C - 3}" height="{C - 3}" rx="2" fill="{col}" fill-opacity="0.85"/></g>')
LX, RX, GY = 22, 218, 132
# CPU: 4 big cores
a(text(LX, 18, 'CPU: 4 fast cores', anchor='start', size=13, fill=VIOLET, ls='0'))
for k in range(CPU_CORES):
    a(f'<rect x="{LX + k * 40}" y="34" width="36" height="72" rx="6" fill="{QCARD}" stroke="{VIOLET}" stroke-width="1.5"/>')
a(text(LX, 124, '4 pixels per step', anchor='start', size=13, fill=QMUTED, ls='0'))
grid(LX, GY, lambda i: T0 + (i // CPU_CORES + 1) * STEP_CPU, VIOLET)
# GPU: 64 small lanes
a(text(RX, 18, 'GPU: 64 slow lanes', anchor='start', size=13, fill=TEAL, ls='0'))
for i in range(GPU_LANES):
    a(f'<rect x="{RX + (i % 16) * 10}" y="{34 + (i // 16) * 18}" width="7" height="15" rx="1.5" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="0.8"/>')
a(text(RX, 124, 'all 64 in one step', anchor='start', size=13, fill=QMUTED, ls='0'))
grid(RX, GY, lambda i: T0 + STEP_GPU, TEAL)
# finish times
FY = GY + 8 * C + 22
a(f'<g opacity="0">{win(T0 + T_GPU)}{text(RX, FY, "done: 1 long step", anchor="start", size=13, fill=TEAL, ls="0")}</g>')
a(f'<g opacity="0">{win(T0 + T_CPU)}{text(LX, FY, "done: 16 steps", anchor="start", size=13, fill=VIOLET, ls="0")}</g>')
a(text(200, FY + 22, 'one long step = four short ones', anchor='middle', size=13, fill=QMUTED, ls='0'))
H = FY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-7 svgd-part5-7">')
o.insert(1, '<title id="svgt-part5-7">Fig 16.6 · CPU vs GPU · few clever cores vs thousands of simple ones</title>')
o.insert(2, '<desc id="svgd-part5-7">The same job, shading 64 pixels, on two machines. A CPU with four fast cores shades four pixels per quick step and needs sixteen steps. A GPU with sixty-four simple lanes, each four times slower, shades all sixty-four in a single long step and finishes in a quarter of the time.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A CPU spends its transistors on a few cores that run one stream of instructions fast; a GPU spends them on many simple lanes that run the same instruction on different data. '
           'On 64 pixels the slower lanes finish first because they all work at once; on a long chain of dependent, branching steps the CPU wins.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Real sizes.</b> A desktop CPU has 8 to 24 cores; an NVIDIA H100 (SXM) has 132 streaming multiprocessors with about 17,000 lanes in all, run in groups of 32 that share one instruction (Fig 16.7).</li>
          <li><b>Where the transistors go.</b> A CPU core spends them on out-of-order execution, branch prediction and large caches; a GPU lane has almost none of that, and hides memory delays by switching between thousands of waiting threads.</li>
          <li><b>Why it took over.</b> Graphics, video and neural networks are the same arithmetic over huge arrays; training a network is mostly matrix multiplication, exactly the GPU's shape.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-6">
      <div class="diagram-label">Fig 16.6 · CPU vs GPU · few clever cores vs thousands of simple ones</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-6"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-6', cap, card.replace('CAPID', cap))
