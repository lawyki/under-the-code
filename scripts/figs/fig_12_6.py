# Fig 12.6 · Node.js · V8 + libuv + a JavaScript stdlib (Pass 28, law 3). Chart Room plate. The layers: your
# JavaScript, Node's APIs, V8 beside libuv (its event loop and a thread pool of four), the operating system. One
# fs.readFile is traced: down through the APIs into libuv, onto a pool thread and out to the disk; meanwhile V8's
# single thread is free and serves other requests; the read completes, libuv's loop queues the callback, V8 runs
# it. t=0 (shift): the read done, V8 running the callback.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD = '#9bd89b', '#d4a853'
W = 400
R1, R2, R3, R4 = (10, 54), (64, 108), (118, 200), (210, 254)   # row y ranges
V8X, LUX = (10, 192), (202, 390)
o = []; a = o.append
def box(x0, x1, y0, y1, col, l1, l2=None):
    a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(x0 + 10, y0 + 18, l1, anchor='start', size=13, fill=col, ls='0'))
    if l2:
        a(text(x0 + 10, y0 + 36, l2, anchor='start', size=13, fill=CMUTED, ls='0'))
box(10, 390, *R1, CSOFT, 'your JavaScript', 'app.js calls fs.readFile')
box(10, 390, *R2, GREEN, 'Node\'s APIs', 'fs, http, net, crypto…')
box(*V8X, *R3, CYAN, 'V8', 'one thread runs JS')
box(*LUX, *R3, GOLD, 'libuv', 'event loop')
box(10, 390, *R4, CMUTED, 'operating system', 'sockets, disks')
# libuv's thread pool: four cells
PX0, PY = LUX[0] + 10, R3[0] + 46
cells = [(PX0 + k * 30, PY) for k in range(4)]
for cx, cy in cells:
    a(f'<rect x="{cx}" y="{cy}" width="24" height="18" rx="3" fill="none" stroke="{GOLD}" stroke-opacity="0.6"/>')
a(text(PX0 + 4 * 30 + 4, PY + 14, 'pool', anchor='start', size=13, fill=CMUTED, ls='0'))
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
# the pool thread busy while the disk works
TW0, TW1 = 2.6, 5.6
a(f'<g class="fx" opacity="0">{lit(TW0, TW1)}<rect x="{cells[0][0]}" y="{PY}" width="24" height="18" rx="3" fill="{GOLD}" fill-opacity="0.8"/></g>')
# V8's thread: what it is doing
SY = R3[0] + 52
for t0, t1, s, col in ((0.31, 1.6, 'runs app.js', CSOFT), (1.6, 6.6, 'free: serves', GREEN), (6.6, None, 'runs callback', CYAN)):
    body = text(V8X[0] + 10, SY, s, anchor='start', size=13, fill=col, ls='0')
    if s.startswith('free'):
        body += text(V8X[0] + 10, SY + 18, 'other requests', anchor='start', size=13, fill=GREEN, ls='0')
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{body}</g>')
# the readFile token: down to the pool and the disk, back up through the loop to V8
DY = (R4[0] + R4[1]) / 2
P = [(0.8, (300, (R1[0] + R1[1]) / 2)), (1.4, (300, (R2[0] + R2[1]) / 2)), (2.0, (300, R3[0] + 26)), (2.6, (cells[0][0] + 12, PY + 9)), (3.2, (cells[0][0] + 12, DY)),
     (5.0, (cells[0][0] + 12, DY)), (5.6, (cells[0][0] + 12, PY + 9)), (6.0, (300, R3[0] + 26)), (6.6, (100, R3[1] - 20))]
x0, y0 = P[0][1]
kx = [(0.0, 0.0), (P[0][0], 0.0)] + [(t, x - x0) for t, (x, y) in P] + [(D, P[-1][1][0] - x0)]
ky = [(0.0, 0.0), (P[0][0], 0.0)] + [(t, y - y0) for t, (x, y) in P] + [(D, P[-1][1][1] - y0)]
a(f'<g class="fx" opacity="0">{lit(P[0][0], P[-1][0] + 0.4)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}'
  f'<circle cx="{x0}" cy="{y0}" r="7" fill="#fff" stroke="{CYAN}" stroke-width="2"/></g></g></g>')
H = R4[1] + 8
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-61 svgd-part3-61">')
o.insert(1, '<title id="svgt-part3-61">Fig 12.6 · Node.js · V8 + libuv + a JavaScript stdlib</title>')
o.insert(2, '<desc id="svgd-part3-61">Node\'s layers: your JavaScript on top, Node\'s APIs such as fs, http, net and crypto below it, then V8, which runs the JavaScript on one thread, beside libuv, which holds the event loop and a pool of four threads, and the operating system at the bottom. '
  'A file read travels down into libuv, takes a pool thread and goes to the disk. Meanwhile V8\'s thread is free and serves other requests. When the read completes, libuv\'s loop queues the callback and V8 runs it.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ("Node runs your JavaScript on one thread in V8 and hands everything slow to libuv. A file read takes a pool thread and goes to the disk while the JavaScript thread serves other requests; when the read is done, libuv's event loop queues the callback and V8 runs it.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The layers.</b> Your code calls Node's standard library, written partly in JavaScript and partly in C++ on top of V8 and libuv.</li>
          <li><b>Two kinds of waiting.</b> Sockets need no threads: libuv asks the OS which ones are ready (epoll on Linux, kqueue on macOS and BSD, IOCP on Windows). Files, DNS lookups and some crypto run on the pool, four threads by default.</li>
          <li><b>History.</b> Ryan Dahl showed Node at JSConf EU in November 2009; libuv was written for it in 2011, to bring it to Windows.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-6">
      <div class="diagram-label">Fig 12.6 · Node.js · V8 + libuv + a JavaScript stdlib</div>
      {svg}
      <p id="ch12-node-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-6', 'ch12-node-p5', card)
