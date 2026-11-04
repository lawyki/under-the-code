# Fig 3.6 · The stack during a function call (Pass 31, Part I, from an empty script). Job: function. Takeaway: call
# pushes the return address onto the stack and jumps; ret pops it into RIP, so the caller resumes.
# Concept: the code on the left (main and add, line by line) with RIP as the gold frame on the line about to run, and
# the stack on the right growing down, RSP marking its top. call pushes "return to main" and RIP jumps into add; add
# saves main's rbp, works, restores it; ret pops the return address into RIP and main carries on at its next line. A
# dashed line ties the saved return address to the line it names. t=0 is inside add, both pushes on the stack.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 318
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=5.0)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
def steps(pairs):
    """[(tau, value)] held values -> keyframes for T.translate (a quick 0.25 s move at each step)"""
    pts = [(0.0, pairs[0][1])]
    prev = pairs[0][1]
    for tau, v in pairs[1:]:
        pts += [(tau, prev), (tau + 0.25, v)]; prev = v
    pts.append((D - 0.3, prev)); pts.append((D - 0.01, pairs[0][1]))
    return pts
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-34 svgd-part1-34">')
a('<title id="svgt-part1-34">Fig 3.6 · The stack during a function call</title>')
a('<desc id="svgd-part1-34">Left, the code: main, whose call add is followed by pop rbp, and add, which saves rbp, adds, restores rbp and '
  'returns. RIP, the register that holds the next instruction to run, is drawn as a frame on that line. Right, the stack, growing '
  'down, with RSP, the stack pointer, at its top. main\'s frame (the saved rbp of main\'s caller, then main\'s local variables) sits on the '
  'stack. call add pushes the return address, the next line of main, and jumps into add. add pushes main\'s rbp; on the way out pop '
  'rbp removes it, and ret pops the return address into RIP, so execution continues in main at the next line.</desc>')

# ---------- the code ----------
LINES = [('main', None), ('call add', 0), ('pop rbp', 1), ('add', None), ('push rbp', 2), ('add eax, esi', 3), ('pop rbp', 4), ('ret', 5)]
LY = {}
y = 30
for s, k in LINES:
    if k is None:
        y += 18 if s == 'add' else 0
        a(text(40, y, s, size=14, fill=MUTED))
        y += 14
    else:
        LY[k] = y + 12
        a(text(48, y + 17, s, size=15, fill=INK, ls='0'))
        y += 30
# RIP: the gold frame on the line about to run
rip = steps([(0.0, LY[0]), (2.0, LY[2]), (4.0, LY[3]), (6.0, LY[4]), (7.6, LY[5]), (9.0, LY[1])])
a(f'<g>{T.translate([(t, v - LY[0]) for t, v in rip], axis="y")}'
  f'<rect x="38" y="{LY[0] - 14}" width="134" height="28" rx="5" fill="none" stroke="{GOLD}" stroke-width="2.4"/>'
  + text(30, LY[0] + 5, 'RIP', anchor='end', size=14, fill=GOLD) + '</g>')

# ---------- the stack ----------
SX, SW = 236, 146
SY = lambda i: 44 + i * 40
a(text(SX, 30, 'stack', size=14, fill=MUTED))
a(f'<path d="M 390 {SY(0)} V {SY(3) + 26} m -4 -6 l 4 6 l 4 -6" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
SLOTS = [("caller's rbp", MUTED, None), ("main's locals", INK, None), ('return: main', GOLD, (2.0, 9.0)), ("main's rbp", BLUE, (4.0, 6.6))]
for i, (lab, col, span) in enumerate(SLOTS):
    body = (f'<rect x="{SX}" y="{SY(i)}" width="{SW}" height="32" rx="5" fill="none" stroke="{col if col != MUTED else EDGE}" stroke-width="1.6"/>'
            + text(SX + 12, SY(i) + 21, lab, size=14, fill=col, ls='0'))
    a(f'<g opacity="0">{vis([span])}{body}</g>' if span else body)
# RSP: the top of the stack
rsp = steps([(0.0, SY(1)), (2.0, SY(2)), (4.0, SY(3)), (6.6, SY(2)), (9.0, SY(1))])
a(f'<g>{T.translate([(t, v - SY(1)) for t, v in rsp], axis="y")}'
  f'<path d="M {SX - 6} {SY(1) + 16} l -10 -7 v 14 z" fill="{INK}"/>' + text(SX - 22, SY(1) + 21, 'RSP', anchor='end', size=14, fill=INK) + '</g>')
# the return address names main's next line
a(f'<g opacity="0">{vis([(2.0, 9.0)])}<path d="M {SX} {SY(2) + 16} C 196 {SY(2) + 16} 200 {LY[1]} 176 {LY[1]}" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="4 4"/>'
  f'<path d="M 174 {LY[1]} l 8 -5 v 10 z" fill="{GOLD}"/></g>')
a(text(200, 306, 'call saves where to come back; ret goes there', anchor='middle', size=14, fill=MUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = 'The stack and RIP through one call of <code>add</code>, from <code>call</code> to <code>ret</code>.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>RSP.</b> The stack pointer always marks the top of the stack; on x86-64 that is the lowest address in use.</li>
          <li><b>call.</b> Pushes the address of the next instruction in main (its <code>pop rbp</code>), then jumps to <code>add</code>.</li>
          <li><b>The chain.</b> Each saved rbp points at the frame before it, so the frames form a list back through every call: what a debugger walks to print a stack trace.</li>
          <li><b>ret.</b> Pops whatever is at the top of the stack into RIP.</li>
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
