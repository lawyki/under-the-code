# Fig 11.14 · HTTP/1.1 vs HTTP/2 · serial vs multiplexed on the same TCP connection (Pass 28, law 3). Chart Room
# plate. Six files on one connection; widths are wire time. slow.js needs 200 ms of server work before its 20 ms of
# bytes. HTTP/1.1: each response in turn, the wire idle while slow.js is prepared: done at 560 ms. HTTP/2: every
# response cut into 20 ms frames, interleaved round-robin among the streams that are ready; slow.js slots in when
# ready; done at 360 ms. Round trips ignored. Both lanes fill on one clock. t=0 (shift): both complete.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, BLUE, GOLD, LOSS = '#9bd89b', '#86a8ff', '#d4a853', '#ec8d8d'
FILES = [('html', 60, 0, CYAN), ('css', 60, 0, GREEN), ('slow.js', 20, 200, LOSS), ('app', 60, 0, GOLD), ('img1', 80, 0, BLUE), ('img2', 80, 0, BLUE)]
FR = 20
# HTTP/1.1: serial
H1, t = [], 0
for name, ms, ready, col in FILES:
    if ready:                                     # requested only now, so the server's work starts now
        H1.append(('wait', t, t + ready, None)); t += ready
    H1.append((name, t, t + ms, col)); t += ms
T1 = t
# HTTP/2: round-robin 20 ms frames among ready streams
left = {n: ms for n, ms, _, _ in FILES}
H2, t = [], 0
order = [n for n, *_ in FILES]
while any(left.values()):
    ready = [n for n, ms, r, _ in FILES if left[n] and r <= t]
    if not ready:
        t += FR; continue
    # round-robin: next stream in file order after the last served
    last = H2[-1][0] if H2 else None
    start = (order.index(last) + 1) if last in order else 0
    n = next(order[(start + k) % len(order)] for k in range(len(order)) if order[(start + k) % len(order)] in ready)
    H2.append((n, t, t + FR)); left[n] -= FR; t += FR
T2 = t
assert (T1, T2) == (560, 360)
COL = {n: c for n, _, _, c in FILES}
W = 400
X0, X1 = 20, 380
xm = lambda ms: X0 + ms / T1 * (X1 - X0)
D, S0, S1 = 10.0, 0.5, 7.5
T = Timeline(D, shift=9.4)
tm = lambda ms: S0 + ms / T1 * (S1 - S0)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
L1, L2, BH = 36, 132, 28
o = []; a = o.append
a(text(X0, L1 - 12, 'HTTP/1.1: one response at a time', anchor='start', size=13, fill=ROUTE, ls='0'))
a(text(X0, L2 - 12, 'HTTP/2: frames from every stream', anchor='start', size=13, fill=GREEN, ls='0'))
fills = []
for y in (L1, L2):
    a(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="{BH}" rx="3" fill="none" stroke="{CMUTED}" stroke-opacity="0.4"/>')
for name, t0, t1, col in H1:
    if col is None:
        fills.append(f'<rect x="{xm(t0):.1f}" y="{L1}" width="{xm(t1) - xm(t0):.1f}" height="{BH}" fill="none" stroke="{LOSS}" stroke-dasharray="3 3"/>')
        continue
    fills.append(f'<rect x="{xm(t0) + 0.5:.1f}" y="{L1}" width="{xm(t1) - xm(t0) - 1:.1f}" height="{BH}" rx="2" fill="{col}" fill-opacity="0.85"/>')
for name, t0, t1 in H2:
    fills.append(f'<rect x="{xm(t0) + 0.5:.1f}" y="{L2}" width="{xm(t1) - xm(t0) - 1:.1f}" height="{BH}" rx="2" fill="{COL[name]}" fill-opacity="0.85"/>')
# names on the HTTP/1.1 lane, where the blocks are wide enough
for name, t0, t1, col in H1:
    lab = 'slow.js wait' if col is None else name
    if name == 'slow.js':
        continue
    fills.append(text((xm(t0) + xm(t1)) / 2, L1 + BH / 2 + 5, lab, anchor='middle', size=13, fill=LOSS if col is None else '#0a1c2d', ls='0'))
a(f'<defs><clipPath id="clip-fig-11-14"><rect class="fx" x="{X0}" y="0" width="{X1 - X0}" height="400">'
  f'{T.anim("width", [(0.0, X1 - X0), (0.3, X1 - X0), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0), (D, X1 - X0)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-11-14)">{"".join(fills)}</g>')
# slow.js on the HTTP/2 lane, pointed out
s2 = next(f for f in H2 if f[0] == 'slow.js')
a(text(xm(s2[1]) + 1, L2 + BH + 18, '↑ slow.js, when ready', anchor='start', size=13, fill=LOSS, ls='0'))
# done
for y, tt in ((L1, T1), (L2, T2)):
    lx, ly = (X1, y - 12) if tt == T1 else (xm(tt) + 10, y + BH / 2 + 5)
    a(f'<g class="fx" opacity="0">{win(tm(tt))}{text(lx, ly, f"done {tt} ms", anchor="end" if tt == T1 else "start", size=13, fill=CSOFT, ls="0")}</g>')
AY = L2 + BH + 44
a(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{CMUTED}"/>')
for ms in (0, 200, 360, 560):
    a(f'<line x1="{xm(ms):.1f}" y1="{AY - 4}" x2="{xm(ms):.1f}" y2="{AY + 4}" stroke="{CMUTED}"/>')
    a(text(xm(ms), AY + 20, str(ms), anchor='start' if ms == 0 else ('end' if ms == T1 else 'middle'), size=13, fill=CMUTED, ls='0'))
a(text(X1, AY + 40, 'milliseconds', anchor='end', size=13, fill=CMUTED, ls='0'))
H = AY + 50
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-53 svgd-part3-53">')
o.insert(1, '<title id="svgt-part3-53">Fig 11.14 · HTTP/1.1 vs HTTP/2 · serial vs multiplexed on the same TCP connection</title>')
o.insert(2, '<desc id="svgd-part3-53">Six files over one connection. With HTTP/1.1 they go one after another: html, css, then a 200 millisecond wait while the server prepares slow.js, then slow.js, app, and two images, finishing at 560 milliseconds. '
  'With HTTP/2 every response is cut into small frames and the frames of all the files are interleaved; the other files use the wait, slow.js slips in when it is ready, and everything finishes at 360 milliseconds.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('On one HTTP/1.1 connection each response must finish before the next starts, so while the server prepares <code>slow.js</code> the wire sits idle. '
           'HTTP/2 cuts every response into frames tagged with a stream ID and interleaves them, so the other files use that time and the page is done at 360 ms, not 560.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The setting.</b> Six files on one connection, widths drawn as wire time; <code>slow.js</code> needs 200 ms of server work before its 20 ms of bytes. Round trips are left out.</li>
          <li><b>The workaround.</b> Browsers opened up to six HTTP/1.1 connections per host to get some parallelism; HTTP/2 needs only one.</li>
          <li><b>The limit.</b> HTTP/2 makes no byte faster, it only fills idle time. And all its frames ride one TCP byte stream, so a lost packet still stalls every stream behind it (Fig 11.15).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-14">
      <div class="diagram-label">Fig 11.14 · HTTP/1.1 vs HTTP/2 · serial vs multiplexed on the same TCP connection</div>
      {svg}
      <p id="ch11-modern-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(H2)
    splice('part-3', 'fig-11-14', 'ch11-modern-p3', card)
