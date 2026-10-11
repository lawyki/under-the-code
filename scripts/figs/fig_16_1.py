# Fig 16.1 · Threads vs processes · the same parallelism, two isolation models (Pass 28, law 3). Quorum glass plate.
# Left: one process, three threads, one shared memory holding x = 0; thread 1 writes x = 5 and threads 2 and 3 read
# 5 at once. Right: three processes, each with its own memory; process A writes x = 5 and B and C still hold 0 until
# A sends a message through the kernel. Phase-synced: both sides act on the same beats. t=0 (shift): after the write
# and the message.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
TW, TR, TM, TA = 1.4, 2.4, 4.4, 5.6               # write, others read, message sent, message lands
o = []; a = o.append
def val(x, y, t_from, t_to, v, col):
    body = text(x, y, f'x = {v}', anchor='middle', size=13, fill=col, ls='0')
    a(f'<g opacity="0">{win(t_from) if t_to is None else lit(t_from, t_to)}{body}</g>')
# threads
a(text(10, 18, 'threads: one memory', anchor='start', size=13, fill=VIOLET, ls='0'))
a(f'<rect x="10" y="28" width="184" height="56" rx="10" fill="{QCARD}" stroke="{VIOLET}" stroke-width="1.5"/>')
a(text(102, 46, 'shared memory', anchor='middle', size=13, fill=QMUTED, ls='0'))
val(102, 70, 0.31, TW, 0, QSOFT); val(102, 70, TW, None, 5, VIOLET)
a(f'<g class="fx" opacity="0">{pulse(TW)}<rect x="10" y="28" width="184" height="56" rx="10" fill="none" stroke="#fff" stroke-width="2"/></g>')
TX = [30, 102, 174]
for k, x in enumerate(TX):
    a(f'<line x1="{x}" y1="84" x2="{x}" y2="112" stroke="{VIOLET}" stroke-opacity="0.6"/>')
    a(f'<rect x="{x - 28}" y="112" width="56" height="40" rx="8" fill="{QCARD}" stroke="{VIOLET}" stroke-opacity="0.7"/>')
    a(text(x, 128, f't{k + 1}', anchor='middle', size=13, fill=VIOLET, ls='0'))
    a(text(x, 145, 'stack', anchor='middle', size=13, fill=QMUTED, ls='0'))
    if k == 0:
        a(f'<g class="fx" opacity="0">{lit(TW - 0.6, TR)}{text(x, 172, "write 5", anchor="middle", size=13, fill=VIOLET, ls="0")}</g>')
    else:
        a(f'<g opacity="0">{win(TR)}{text(x, 172, "reads 5", anchor="middle", size=13, fill=VIOLET, ls="0")}</g>')
# processes
a(text(206, 18, 'processes: own memory', anchor='start', size=13, fill=TEAL, ls='0'))
PX = [234, 298, 362]
for k, x in enumerate(PX):
    a(f'<rect x="{x - 28}" y="28" width="56" height="124" rx="8" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="0.7"/>')
    a(text(x, 46, 'ABC'[k], anchor='middle', size=13, fill=TEAL, ls='0'))
    a(text(x, 145, 'stack', anchor='middle', size=13, fill=QMUTED, ls='0'))
    if k == 0:
        val(x, 72, 0.31, TW, 0, QSOFT); val(x, 72, TW, None, 5, TEAL)
    else:
        val(x, 72, 0.31, TA, 0, QSOFT); val(x, 72, TA, None, 5, TEAL)
        a(f'<g opacity="0">{lit(TR, TA)}{text(x, 172, "still 0", anchor="middle", size=13, fill=QROSE, ls="0")}</g>')
        a(f'<g opacity="0">{win(TA)}{text(x, 172, "got it", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
a(f'<g class="fx" opacity="0">{pulse(TW)}<rect x="{PX[0] - 28}" y="28" width="56" height="124" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the kernel and the message
KY = 200
a(f'<rect x="206" y="{KY}" width="184" height="26" rx="13" fill="none" stroke="{QMUTED}" stroke-dasharray="4 3"/>')
a(text(298, KY + 18, 'kernel: pipe, socket', anchor='middle', size=13, fill=QMUTED, ls='0'))
for x in PX[1:]:
    mv = T.translate([(0.0, 0.0), (TM, 0.0), (TA, x - PX[0]), (D, x - PX[0])], 'x')
    a(f'<g class="fx" opacity="0">{lit(TM, TA + 0.01)}<g>{mv}<circle cx="{PX[0]}" cy="{KY + 13}" r="6" fill="{TEAL}"/></g></g>')
a(f'<g class="fx" opacity="0">{lit(TM - 0.6, TA)}{text(PX[0] - 28, 172, "send", anchor="start", size=13, fill=TEAL, ls="0")}</g>')
# the trade, under each side
a(text(10, 252, 'fast: no copy', anchor='start', size=13, fill=VIOLET, ls='0'))
a(text(10, 270, 'one bug hits all', anchor='start', size=13, fill=QROSE, ls='0'))
a(text(206, 252, 'safe: walls', anchor='start', size=13, fill=TEAL, ls='0'))
a(text(206, 270, 'every share is a copy', anchor='start', size=13, fill=QROSE, ls='0'))
H = 282
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-2 svgd-part5-2">')
o.insert(1, '<title id="svgt-part5-2">Fig 16.1 · Threads vs processes · the same parallelism, two isolation models</title>')
o.insert(2, '<desc id="svgd-part5-2">Left: one process with three threads, each with its own stack, all sharing one memory that holds x = 0. Thread 1 writes x = 5 and threads 2 and 3 read 5 at once: fast, with no copy, but a bug in one thread can damage all of them. '
  'Right: three processes, each with its own memory. Process A writes x = 5 while B and C still hold 0 until A sends a message through the kernel, by pipe or socket: walls keep them safe, but every share is a copy.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Threads share one memory, so a value one writes the others can read at once, and a bug in one can damage all of them. '
           'Processes each have their own memory: nothing passes until one sends a message through the kernel, which is slower but walls each one off.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>What is shared.</b> Threads share the heap, globals and open files; each has its own stack and registers. Processes share nothing unless they set up shared memory or talk through the kernel.</li>
          <li><b>The costs.</b> Creating a thread or switching between threads of one process is cheaper than doing the same for processes, which need their own page tables (Chapter 4).</li>
          <li><b>The standard.</b> POSIX threads (1995) made the shared-memory model portable; C, C++, Java and Rust default to threads, and browsers put each site in its own process for safety.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-1">
      <div class="diagram-label">Fig 16.1 · Threads vs processes · the same parallelism, two isolation models</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-1"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-1', cap, card.replace('CAPID', cap))
