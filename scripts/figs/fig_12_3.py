# Fig 12.3 · The event loop · stack, microtasks, macrotasks, render (Pass 28, law 3). Chart Room plate. Four lines:
# log 1, setTimeout(log 4, 0), Promise.resolve().then(log 3), log 2. The script runs to the end on the stack
# (1, 2); the timer callback waits in the task queue, the promise callback in the microtask queue. The stack
# empties; every microtask runs (3); a render may happen; then the next task (4). The code line lights, chips fly
# to their queues and on to the stack, the console fills in order. t=0 (shift): done, console "1 2 3 4".
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD, LOSS = '#9bd89b', '#d4a853', '#ec8d8d'
W = 400
CODE = ['console.log(1);', 'setTimeout(() => console.log(4), 0);', 'Promise.resolve().then(() => console.log(3));', 'console.log(2);']
CY0, CL = 30, 20                                 # first code baseline, line step
cy = lambda i: CY0 + i * CL
SB = (10, 132, 120, 216)                         # stack box x0, x1, y0, y1
MQ = (142, 390, 120, 164)                        # microtask queue
TQ = (142, 390, 172, 216)                        # task queue
RY = 236                                         # render pill
OY = 276                                         # console line
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# code, with the running line lit
a(f'<rect x="10" y="{CY0 - 18}" width="380" height="{CL * 4 + 8}" rx="5" fill="#0a1c2d" stroke="{CMUTED}" stroke-opacity="0.5"/>')
TL = [(0.6, 1.4), (1.4, 2.4), (2.4, 3.4), (3.4, 4.4)]
for i, (t0, t1) in enumerate(TL):
    a(f'<g class="fx" opacity="0">{lit(t0, t1)}<rect x="12" y="{cy(i) - 14}" width="376" height="19" rx="2" fill="{CYAN}" fill-opacity="0.16"/></g>')
for i, s in enumerate(CODE):
    a(text(20, cy(i), s, anchor='start', size=13, fill=CSOFT, ls='0'))
# boxes
def box(b, label, sub, col):
    x0, x1, y0, y1 = b
    a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(x0 + 8, y0 + 15, label, anchor='start', size=13, fill=col, ls='0'))
    if sub:
        a(text(x1 - 8, y0 + 15, sub, anchor='end', size=13, fill=CMUTED, ls='0'))
box(SB, 'call stack', None, CYAN)
box(MQ, 'microtasks', 'promises', GREEN)
box(TQ, 'tasks', 'timers, clicks', GOLD)
def chip(x, y, s, col):
    w = len(s) * 8 + 14
    return (f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="#0a1c2d" stroke="{col}" stroke-width="1.5"/>'
            + text(x, y + 5, s, anchor='middle', size=13, fill=col, ls='0'))
stx, sty = (SB[0] + SB[1]) / 2, SB[3] - 18     # where a frame sits on the stack
# the script frame
a(f'<g class="fx" opacity="0">{lit(0.6, 4.4)}{chip(stx, sty, "script", CYAN)}</g>')
# chips: (label, colour, queue box, enqueue window, to-stack window, run until)
CHIPS = [('log 4', GOLD, TQ, (1.6, 2.3), (7.6, 8.2), 9.0), ('log 3', GREEN, MQ, (2.6, 3.3), (4.8, 5.4), 6.2)]
CODE_BOT = CY0 - 18 + CL * 4 + 8                   # bottom of the code box
for lab, col, q, (e0, e1), (s0, s1), r1 in CHIPS:
    # each queue's chip sits in the gap between that box's two labels; chips leave from just under the code box
    qx, qy = (225 if q is TQ else 274), q[2] + 31
    sx0, sy0 = 300, CODE_BOT + 12
    # fly from the code box to the queue
    a(f'<g class="fx" opacity="0">{lit(e0, e1 + 0.01)}<g>{T.translate([(0.0, 0.0), (e0, 0.0), (e1, qx - sx0), (D, qx - sx0)], "x")}'
      f'<g>{T.translate([(0.0, 0.0), (e0, 0.0), (e1, qy - sy0), (D, qy - sy0)], "y")}{chip(sx0, sy0, lab, col)}</g></g></g>')
    # wait in the queue
    a(f'<g class="fx" opacity="0">{lit(e1, s0)}{chip(qx, qy, lab, col)}</g>')
    # to the stack: across at the queue's own height, then down the stack's column
    sm = s0 + (s1 - s0) * 0.7
    kx = [(0.0, 0.0), (s0, 0.0), (sm, stx - qx), (s1, stx - qx), (D, stx - qx)]
    ky = [(0.0, 0.0), (s0, 0.0), (sm, 0.0), (s1, sty - qy), (D, sty - qy)]
    a(f'<g class="fx" opacity="0">{lit(s0, s1 + 0.01)}<g>{T.translate(kx, "x")}'
      f'<g>{T.translate(ky, "y")}{chip(qx, qy, lab, col)}</g></g></g>')
    a(f'<g class="fx" opacity="0">{lit(s1, r1)}{chip(stx, sty, lab, col)}</g>')
# render, between the microtasks and the next task
a(f'<rect x="142" y="{RY - 12}" width="248" height="24" rx="12" fill="none" stroke="{CMUTED}" stroke-opacity="0.6"/>')
a(text(266, RY + 5, 'render, if a frame is due', anchor='middle', size=13, fill=CMUTED, ls='0'))
a(f'<g class="fx" opacity="0">{lit(6.6, 7.3)}<rect x="142" y="{RY - 12}" width="248" height="24" rx="12" fill="{CYAN}" fill-opacity="0.2" stroke="{CYAN}" stroke-width="2"/></g>')
# the console
a(text(10, OY, 'console:', anchor='start', size=13, fill=CMUTED, ls='0'))
for k, (n, t0) in enumerate(((1, 1.0), (2, 3.8), (3, 5.8), (4, 8.6))):
    a(f'<g opacity="0">{win(t0)}{text(90 + k * 28, OY, str(n), anchor="start", size=16, fill=CSOFT, ls="0")}</g>')
H = OY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-58 svgd-part3-58">')
o.insert(1, '<title id="svgt-part3-58">Fig 12.3 · The event loop · stack, microtasks, macrotasks, render</title>')
o.insert(2, '<desc id="svgd-part3-58">Four lines of JavaScript: log 1; a zero-millisecond timer that logs 4; a resolved promise whose callback logs 3; log 2. '
  'The script runs to its end on the call stack and prints 1 and 2. The timer callback waits in the task queue and the promise callback in the microtask queue. '
  'When the stack is empty every microtask runs, printing 3; the browser may render; then the next task runs, printing 4. The console reads 1 2 3 4.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The script runs to its end first, printing 1 and 2; its timer callback waits in the task queue and its promise callback in the microtask queue. '
           'When the stack empties, every microtask runs (3), the browser may render, and only then does the next task run (4).')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>One turn of the loop.</b> Take one task, run it to the end, run every microtask, render if a frame is due (about every 16 ms on a 60 Hz screen), repeat.</li>
          <li><b>Why 0 ms still waits.</b> <code>setTimeout(…, 0)</code> only queues a task; it cannot run until the current script and every microtask have finished.</li>
          <li><b>The catch.</b> Anything long on the stack, a heavy <code>JSON.parse</code> or a tight loop, stops the loop: no clicks, no rendering. A frozen page and Node.js event-loop lag are the same bug.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-3">
      <div class="diagram-label">Fig 12.3 · The event loop · stack, microtasks, macrotasks, render</div>
      {svg}
      <p id="ch12-loop-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-3', 'ch12-loop-p3', card)
