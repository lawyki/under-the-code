# Fig 1.8 · Von Neumann architecture (Pass 28, law 3). One memory holds a three-line
# program and its data; one bus joins it to the CPU. The run: load A, add B, store C.
# Instructions (gold) and data (blue) take turns on the same bus. t=0: the run finished.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 492
T = Timeline(10, shift=9.0)
o = []; a = o.append

a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-9 svgd-part1-9">')
a('<title id="svgt-part1-9">Fig 1.8 · Von Neumann architecture · one memory, one bus</title>')
a('<desc id="svgd-part1-9">One memory holds a three-instruction program (load A, add B, store C) and its data (A = 5, B = 3, C = 0). '
  'The CPU fetches each instruction over the single bus, then the data it needs over the same bus; the ALU adds 5 and 3; the result 8 travels back up the bus into C.</desc>')

# memory: program and data side by side in one store
a(text(20, 28, 'MEMORY · ONE STORE FOR BOTH', fill=MUTED))
CELLS = [((20, 40), '0', 'load A', GOLD), ((20, 80), '1', 'add B', GOLD), ((20, 120), '2', 'store C', GOLD),
         ((210, 40), '3', 'A = 5', BLUE), ((210, 80), '4', 'B = 3', BLUE), ((210, 120), '5', 'C = 0', BLUE)]
for (x, y), addr, val, col in CELLS:
    a(f'<rect x="{x}" y="{y}" width="170" height="32" rx="4" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(x + 12, y + 22, addr, size=13, fill='rgba(255,255,255,0.45)', ls='0'))
    if val == 'C = 0':
        a(f'<text x="{x + 36}" y="{y + 22}" {MONO} font-size="15" fill="#fff">C = 0{T.anim("opacity", [(0.0, 1.0), (7.599, 1.0), (7.6, 0.0), (9.799, 0.0), (9.8, 1.0), (10.0, 1.0)])}</text>')
        a(f'<text x="{x + 36}" y="{y + 22}" {MONO} font-size="15" fill="{GOLD}" opacity="0">C = 8{T.anim("opacity", [(0.0, 0.0), (7.599, 0.0), (7.6, 1.0), (9.799, 1.0), (9.8, 0.0), (10.0, 0.0)])}</text>')
    else:
        a(text(x + 36, y + 22, val, size=15, fill='#fff', ls='0'))
# the program counter's cell, highlighted in turn
for k, (on, off) in enumerate(((0.0, 2.6), (2.6, 5.4), (5.4, 9.8))):
    (x, y) = CELLS[k][0]
    pts = [(0.0, 0.0), (on - 0.001 if on else 0.0, 0.0), (on + 0.001, 1.0), (off - 0.001, 1.0), (off, 0.0), (10.0, 0.0)] if on else [(0.0, 1.0), (off - 0.001, 1.0), (off, 0.0), (9.8, 0.0), (9.801, 1.0), (10.0, 1.0)]
    a(f'<rect x="{x - 2}" y="{y - 2}" width="174" height="36" rx="5" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0">{T.anim("opacity", pts)}</rect>')

# the bus: one path between memory and CPU
a('<rect x="186" y="166" width="28" height="122" rx="4" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.25)"/>')
a(text(176, 232, 'bus', anchor='end', fill=MUTED))
a('<rect x="300" y="210" width="80" height="34" rx="4" fill="#161616" stroke="rgba(255,255,255,0.3)"/>')
a('<line x1="214" y1="227" x2="300" y2="227" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>')
a(text(340, 232, 'I/O', anchor='middle', fill=MUTED))

# the CPU
a('<rect x="14" y="288" width="372" height="200" rx="8" fill="#141414" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>')
a(text(28, 312, 'CPU', fill='rgba(255,255,255,0.8)'))
a(f'<rect x="28" y="324" width="166" height="62" rx="5" fill="{GOLD}" fill-opacity="0.1" stroke="{GOLD}" stroke-opacity="0.6"/>')
a(text(40, 344, 'control', size=13, fill='rgba(212,168,83,0.85)'))
for k, (ins, on, off) in enumerate((('load A', 1.2, 3.7), ('add B', 3.7, 6.5), ('store C', 6.5, 9.8))):
    pts = [(0.0, 0.0), (on - 0.001, 0.0), (on, 1.0), (off - 0.001, 1.0), (off, 0.0), (10.0, 0.0)]
    a(f'<text x="40" y="372" {MONO} font-size="17" fill="#fff" opacity="0">{ins}{T.anim("opacity", pts)}</text>')
a(f'<rect x="206" y="324" width="166" height="62" rx="5" fill="{BLUE}" fill-opacity="0.1" stroke="{BLUE}" stroke-opacity="0.6"/>')
a(text(218, 344, 'register', size=13, fill='rgba(134,168,255,0.9)'))
for v, on, off in (('5', 2.3, 5.0), ('8', 5.0, 9.8)):
    pts = [(0.0, 0.0), (on - 0.001, 0.0), (on, 1.0), (off - 0.001, 1.0), (off, 0.0), (10.0, 0.0)]
    a(f'<text x="218" y="372" {MONO} font-size="17" fill="#fff" opacity="0">{v}{T.anim("opacity", pts)}</text>')
a('<rect x="110" y="404" width="180" height="62" rx="5" fill="#1b1b1b" stroke="rgba(255,255,255,0.35)"/>')
a(text(122, 424, 'ALU', size=13, fill='rgba(255,255,255,0.6)'))
a(f'<text x="122" y="452" {MONO} font-size="17" fill="#fff" opacity="0">5 + 3 = 8{T.anim("opacity", [(0.0, 0.0), (4.8, 0.0), (4.801, 1.0), (9.8, 1.0), (9.801, 0.0), (10.0, 0.0)])}</text>')

# traffic on the bus: one packet at a time, leaving each cell into the gap between the columns
def packet(col, pts_xy, t0, t1):
    # the packet runs the whole length of the bus (its middle leg), then turns to its destination
    (x0, y0), (x1, y1), (x2, y2) = pts_xy
    down = y2 > y1
    leg = [(x0, y0), (x1, y1), (x1, 288 if down else 166), (x2, y2)] if down else [(x0, y0), (x1, 288), (x1, y1), (x2, y2)]
    ts = [t0, t0 + (t1 - t0) * 0.25, t0 + (t1 - t0) * 0.75, t1]
    cx = [(0.0, leg[0][0])] + [(t, p[0]) for t, p in zip(ts, leg)] + [(10.0, leg[-1][0])]
    cy = [(0.0, leg[0][1])] + [(t, p[1]) for t, p in zip(ts, leg)] + [(10.0, leg[-1][1])]
    op = [(0.0, 0.0), (t0 - 0.05, 0.0), (t0, 1.0), (t1, 1.0), (t1 + 0.05, 0.0), (10.0, 0.0)]
    a(f'<circle r="7" fill="{col}" stroke="#0e0e0e" stroke-width="1.5" opacity="0">{T.anim("cx", cx)}{T.anim("cy", cy)}{T.anim("opacity", op)}</circle>')
packet(GOLD, ((200, 56), (200, 176), (110, 330)), 0.3, 1.2)     # load A -> control
packet(BLUE, ((200, 56), (200, 176), (290, 330)), 1.4, 2.3)     # A = 5 -> register
packet(GOLD, ((200, 96), (200, 176), (110, 330)), 2.8, 3.7)     # add B -> control
packet(BLUE, ((200, 96), (200, 176), (200, 404)), 3.9, 4.8)     # B = 3 -> ALU
packet(GOLD, ((200, 136), (200, 176), (110, 330)), 5.6, 6.5)    # store C -> control
packet(BLUE, ((290, 330), (200, 166), (200, 136)), 6.7, 7.6)    # 8 -> C, back up the same bus
# legend: colour named, never the only cue
a(f'<circle cx="262" cy="306" r="6" fill="{GOLD}"/>'); a(text(272, 311, 'code', size=13, fill=MUTED))
a(f'<circle cx="316" cy="306" r="6" fill="{BLUE}"/>'); a(text(326, 311, 'data', size=13, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('One memory holds the program and the data it works on, and one bus carries both to the CPU, one at a time. '
           'Nearly every computer built since 1945 follows this design.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Fetch.</b> The program counter names the next cell; its instruction travels over the bus to the control unit.</li>
          <li><b>Execute.</b> The instruction asks for data, which travels over the same bus; the ALU does the arithmetic: 5 + 3.</li>
          <li><b>Store.</b> The result goes back up the bus into memory, and the counter moves on.</li>
          <li><b>One bus.</b> Code and data share it, so they take turns: the bottleneck the next sections return to.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-8">
      <div class="diagram-label">Fig 1.8 · Von Neumann architecture · one memory, one bus</div>
      {svg}
      <p id="ch1-vonneumann-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-8', 'ch1-vonneumann-p5', card)
