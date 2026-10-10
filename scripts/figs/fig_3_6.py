# Fig 3.6 · The stack during a call (Pass 28, law 3). One stack, the round trip: call add pushes
# the return address and jumps; push rbp begins add's frame; pop rbp and ret unwind it, and the
# return address flies back into RIP. RSP marks the top of the stack throughout. t=0: inside add.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, MUTED

W, H = 400, 318
SX, SW, SH, SY = 120, 190, 40, 46
slot_y = lambda i: SY + i * SH
T = Timeline(10, shift=4.6)
D = 10
# (tau, rsp slot index = number of slots in use, rip text)
STATES = [(0.0, 2, 'main: call add'), (1.6, 3, 'add: push rbp'), (3.6, 4, 'add: …'), (5.6, 3, 'add: ret'), (8.2, 2, 'main+5: pop rbp')]
RSP_AT = {4: 7.4}   # ret pops at 7.4; RIP changes when the address lands, at 8.2
def span(i):
    t0 = STATES[i][0]; t1 = STATES[i + 1][0] if i + 1 < len(STATES) else 9.6
    return t0, t1
def win(t0, t1):
    if t0 <= 0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (9.6, 0.0), (9.601, 1.0), (D, 1.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-34 svgd-part1-34">')
a('<title id="svgt-part1-34">Fig 3.6 · The stack during a function call</title>')
a('<desc id="svgd-part1-34">main\'s frame sits on the stack. call add pushes the return address, main+5, and jumps into add. add pushes main\'s frame pointer and begins its own frame. '
  'On the way out, pop rbp removes it, and ret pops the return address into RIP, so execution continues in main at the next instruction. RSP, the stack pointer, follows the top of the stack.</desc>')
a(text(SX, 26, 'THE STACK · GROWS DOWN', size=13, fill=MUTED))
SLOTS = [("main's locals", 'rgba(255,255,255,0.75)', None), ("main's rbp", 'rgba(255,255,255,0.75)', None),
         ('return → main+5', GOLD, (1.6, 7.4)), ("main's rbp, saved", BLUE, (3.6, 5.6))]
for i in range(5):
    a(f'<rect x="{SX}" y="{slot_y(i)}" width="{SW}" height="{SH - 4}" rx="4" fill="#141414" stroke="rgba(255,255,255,0.15)"/>')
for i, (lab, col, life) in enumerate(SLOTS):
    body = (f'<rect x="{SX}" y="{slot_y(i)}" width="{SW}" height="{SH - 4}" rx="4" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-opacity="0.7"/>'
            f'<text x="{SX + 12}" y="{slot_y(i) + 24}" {MONO} font-size="14" fill="#fff">{lab}</text>')
    a(body if life is None else f'<g opacity="0">{win(*life)}{body}</g>')
# frames, bracketed on the right
a(f'<path d="M {SX + SW + 8} {slot_y(0)} h 6 V {slot_y(2) - 4} h -6" fill="none" stroke="rgba(255,255,255,0.5)"/>')
a(text(SX + SW + 20, slot_y(1) + 4, 'main', size=13, fill=MUTED, ls='0'))
a(f'<g opacity="0">{win(3.6, 5.6)}<path d="M {SX + SW + 8} {slot_y(3)} h 6 V {slot_y(4) - 4} h -6" fill="none" stroke="{BLUE}"/>'
  f'<text x="{SX + SW + 20}" y="{slot_y(3) + 24}" {MONO} font-size="13" fill="{BLUE}">add</text></g>')
# RSP: the top of the stack (the bottom edge of the lowest slot in use)
pts = []
for k, (t0, n, _) in enumerate(STATES):
    t0 = RSP_AT.get(k, t0)
    y = slot_y(n) - 2
    if k: pts.append((t0 - 0.0015, pts[-1][1]))
    pts.append((t0 + 0.25, y) if k else (t0, y))
pts.append((9.6, pts[-1][1])); pts.append((9.8, slot_y(2) - 2))
a(f'<g>{T.translate(pts)}<polygon points="{SX - 6},0 {SX - 18},-7 {SX - 18},7" fill="{GOLD}"/>'
  f'<text x="{SX - 24}" y="5" text-anchor="end" {MONO} font-size="15" fill="{GOLD}">RSP</text></g>')
# RIP: where execution is
a(f'<rect x="20" y="262" width="360" height="44" rx="6" fill="#141414" stroke="rgba(255,255,255,0.25)"/>')
a(text(34, 290, 'RIP', size=15, fill=GREEN, ls='0'))
for i, (t0, n, rip) in enumerate(STATES):
    a(f'<text x="86" y="290" {MONO} font-size="15" fill="#fff" opacity="0">{rip}{win(*span(i))}</text>')
# ret: the return address flies from the stack into RIP
a(f'<text class="fx" {MONO} font-size="14" fill="{GOLD}" opacity="0">main+5'
  f'{T.anim("x", [(0.0, SX + 12), (7.4, SX + 12), (8.2, 86), (D, 86)])}{T.anim("y", [(0.0, slot_y(2) + 24), (7.4, slot_y(2) + 24), (8.2, 290), (D, 290)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (7.399, 0.0), (7.4, 1.0), (8.2, 1.0), (8.201, 0.0), (D, 0.0)])}</text>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One call, start to finish: call pushes the return address and jumps; add saves main\'s frame pointer and builds its own frame; '
           'on the way out the frame is unwound and ret pops the return address into RIP, so main resumes at the next instruction.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>RSP.</b> The stack pointer always marks the top of the stack; on x86-64 that is the lowest address in use.</li>
          <li><b>call.</b> Pushes the address of the next instruction (main+5), then jumps. Neither function sees the handoff.</li>
          <li><b>The chain.</b> Each saved rbp points at the frame before it, so the frames form a list back through every call: what a debugger walks to print a stack trace.</li>
          <li><b>ret.</b> Pops whatever is at the top of the stack into RIP. If something has overwritten that slot, ret jumps there instead: the next section's attack.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-6">
      <div class="diagram-label">Fig 3.6 · The stack during a function call</div>
      {svg}
      <p id="ch3-call-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-6', 'ch3-call-p5', card)
