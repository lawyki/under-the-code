# Fig 1.11 · Pipelined execution (Pass 31, Part I, from an empty script). Job: function. Takeaway: stages overlap
# like an assembly line, so once the line is full one instruction finishes every cycle.
# Concept: the line itself. Five stations in a row; five numbered instructions step along it one station per
# cycle (Part I's step verb), each entering as the one ahead moves on, and drop into the finished row. The still is
# cycle 5: every station busy, the first instruction about to finish. Below, the result: 9 cycles, not 25.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 360
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=5.4)
SX = lambda s: 54 + s * 73                    # station centres
SY, DY = 104, 196                             # station row, finished row
STAGES = ['fetch', 'decode', 'execute', 'memory', 'writeback']
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-12 svgd-part1-12">')
a('<title id="svgt-part1-12">Fig 1.11 · Pipelined execution · five instructions, five stages</title>')
a('<desc id="svgd-part1-12">Five stations in a row, like an assembly line: fetch, decode, execute, memory, writeback. Five numbered '
  'instructions step along it one station per cycle, each entering as the one ahead moves on, so by cycle 5 every station is busy. '
  'From then on one instruction finishes every cycle and drops into the finished row; all five are done after 9 cycles. Run one '
  'at a time, they would need 25.</desc>')

def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', pts)

# the stations
for s, name in enumerate(STAGES):
    a(f'<rect x="{SX(s) - 32}" y="{SY - 26}" width="64" height="52" rx="6" fill="none" stroke="{EDGE}" stroke-width="1.4" opacity="0">'
      f'{vis([(0.0, s + 1.0), (s + 6.0, D)])}</rect>')
    # a station lights while it holds an instruction (cycles s+1 .. s+5)
    a(f'<rect x="{SX(s) - 32}" y="{SY - 26}" width="64" height="52" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">'
      f'{vis([(s + 1.0, s + 6.0)])}</rect>')
    a(text(SX(s), SY + 48, name, anchor='middle', size=14, fill=MUTED, ls='0'))
    if s < 4: a(f'<path d="M {SX(s) + 34} {SY} h 5 m -3 -3 l 3 3 l -3 3" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
a(text(20, 34, 'cycle', size=14, fill=MUTED))
for c in range(1, 10):
    end = c + 1.0 if c < 9 else 11.8
    a(f'<text data-role="object" x="76" y="34" font-family="DM Mono" font-size="16" fill="{INK}" opacity="0">{vis([(float(c), end)])}{c}</text>')
a(text(20, DY + 4, 'done', size=14, fill=MUTED))

# the instructions
for k in range(1, 6):
    xs, ys = [(0.0, SX(0))], [(0.0, SY)]
    for c in range(k, k + 6):
        s = c - k
        x, y = (SX(s), SY) if s <= 4 else (92 + (k - 1) * 58, DY)
        px, py = xs[-1][1], ys[-1][1]
        xs += [(float(c), px), (c + 0.3, x)]; ys += [(float(c), py), (c + 0.3, y)]
    xs.append((D - 0.01, xs[-1][1])); ys.append((D - 0.01, ys[-1][1]))
    # relative offsets for the translate groups
    xo = [(t, v - SX(0)) for t, v in xs]; yo = [(t, v - SY) for t, v in ys]
    a(f'<g opacity="0">{vis([(float(k) - 0.05, 11.8)])}<g>{T.translate(xo, axis="x")}<g>{T.translate(yo, axis="y")}'
      f'<circle cx="{SX(0)}" cy="{SY}" r="15" fill="{GOLD}"/>'
      f'<text data-role="object" x="{SX(0)}" y="{SY + 6}" text-anchor="middle" font-family="DM Mono" font-size="16" fill="#1a1407">{k}</text>'
      '</g></g></g>')

# the result: the same five instructions one at a time, and pipelined
BY = 260
a(text(20, BY, 'one at a time', size=14, fill=MUTED)); a(text(380, BY, '25 cycles', anchor='end', size=14, fill=MUTED))
a(f'<rect x="20" y="{BY + 8}" width="360" height="12" rx="3" fill="rgba(255,255,255,0.5)"/>')
a(text(20, BY + 48, 'pipelined', size=14, fill=GOLD)); a(text(380, BY + 48, '9 cycles', anchor='end', size=15, fill=GOLD))
a(f'<rect x="20" y="{BY + 56}" width="{360 * 9 / 25:.1f}" height="12" rx="3" fill="{GOLD}"/>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Five instructions of five stages each, overlapped like an assembly line, finish in 9 cycles instead of 25. Each still '
           'takes five cycles; the gain is that once the pipeline is full, one instruction completes every cycle.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The stages.</b> Fetch, decode, execute, memory access (reading or writing data), writeback: in the usual short names IF, ID, EX, MEM and WB.</li>
          <li><b>The overlap.</b> Each instruction enters one cycle after the one before, so the stations always hold different instructions; in cycle 5 all five are busy at once.</li>
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
