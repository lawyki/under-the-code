# Fig 1.11 · Pipelining (Pass 28, law 3). Five instructions, five stages, nine cycles.
# A cursor walks the cycles and the diagonal fills; below, the count as two bars:
# one at a time 25 cycles, pipelined 9. t=0: the grid complete.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 352
STAGES = [('IF', GOLD), ('ID', '#e9a66b'), ('EX', BLUE), ('MEM', GREEN), ('WB', RED)]
X0, PITCH, CW, Y0, RH = 58, 37, 34, 50, 38
STEP = 0.9
T = Timeline(9.9, shift=9.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-12 svgd-part1-12">')
a('<title id="svgt-part1-12">Fig 1.11 · Pipelined execution · five instructions, five stages</title>')
a('<desc id="svgd-part1-12">A grid of cycles 1 to 9 across and instructions 1 to 5 down. Each instruction passes through fetch, decode, execute, memory and writeback, '
  'starting one cycle after the one before, so the stages form a diagonal and all five finish by cycle 9. Run one at a time, they would need 25 cycles.</desc>')
for c in range(9):
    a(text(X0 + c * PITCH + CW / 2, 34, str(c + 1), anchor='middle', size=14, fill=MUTED, ls='0'))
a(text(20, 34, 'cycle', size=13, fill='rgba(255,255,255,0.45)', ls='0'))
# the cursor: one column at a time
cur = [(0.0, X0)] + sum(([(c * STEP, X0 + c * PITCH), ((c + 1) * STEP - 0.001, X0 + c * PITCH)] for c in range(9)), []) + [(9 * STEP, X0 + 8 * PITCH), (9.9 - 0.01, X0 + 8 * PITCH)]
a(f'<rect y="{Y0 - 6}" width="{CW}" height="{5 * RH + 6}" rx="4" fill="none" stroke="#fff" stroke-width="2" opacity="0">'
  f'{T.anim("x", cur)}{T.anim("opacity", [(0.0, 1.0), (9 * STEP, 1.0), (9 * STEP + 0.05, 0.0), (9.85, 0.0)])}</rect>')
for r in range(5):
    y = Y0 + r * RH
    a(text(20, y + 22, f'i{r + 1}', size=14, fill='rgba(255,255,255,0.75)', ls='0'))
    for s, (name, col) in enumerate(STAGES):
        c = r + s
        x = X0 + c * PITCH
        t_in = c * STEP
        a(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH - 6}" rx="3" fill="{col}" fill-opacity="0.3" stroke="{col}">'
          f'{T.anim("opacity", [(0.0, 0.15), (t_in, 0.15), (t_in + 0.12, 1.0), (9.75, 1.0), (9.85, 0.15)])}</rect>')
        a(f'<text x="{x + CW / 2}" y="{y + 21}" text-anchor="middle" {MONO} font-size="{13 if name == "MEM" else 14}" fill="#fff">{name}'
          f'{T.anim("opacity", [(0.0, 0.25), (t_in, 0.25), (t_in + 0.12, 1.0), (9.75, 1.0), (9.85, 0.25)])}</text>')
# the count, as lengths
PX = 13.2
by = Y0 + 5 * RH + 30
a(text(20, by, 'one at a time', size=14, fill=MUTED))
a(f'<rect x="20" y="{by + 8}" width="{25 * PX:.0f}" height="14" rx="3" fill="rgba(255,255,255,0.22)"/>')
a(text(380, by, '25 cycles', anchor='end', size=14, fill='rgba(255,255,255,0.75)'))
a(text(20, by + 50, 'pipelined', size=14, fill=GOLD))
a(f'<rect x="20" y="{by + 58}" width="{9 * PX:.0f}" height="14" rx="3" fill="{GOLD}" fill-opacity="0.8"/>')
a(text(380, by + 50, '9 cycles', anchor='end', size=14, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('Five instructions of five stages each, overlapped like an assembly line: they finish in 9 cycles instead of 25, '
           'and once the pipeline is full one instruction completes every cycle.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The stages.</b> IF fetch · ID decode · EX execute · MEM memory access · WB writeback.</li>
          <li><b>The diagonal.</b> Each instruction starts one cycle after the one before, so in any column every stage is busy with a different instruction.</li>
          <li><b>Beyond this.</b> Modern CPUs also duplicate stages and finish several instructions in one cycle.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-11">
      <div class="diagram-label">Fig 1.11 · Pipelined execution · five instructions, five stages</div>
      {svg}
      <p id="ch1-cpu-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-11', 'ch1-cpu-p8', card)
