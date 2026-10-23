# Fig 10.8 · BBR aims for the bandwidth-delay product (Pass 28, law 3). Chart Room plate. One bottleneck:
# 1 Gbit/s, 100 ms propagation round trip, so BDP = 12.5 MB; a buffer of 0.75 BDP behind it. Data in flight
# (x, 14 slots: 8 fill the pipe, 6 the queue) against delivery rate (rises to 1 Gbit/s at the BDP, then flat)
# and round-trip time (100 ms to the BDP, then +100 ms per BDP queued, 175 ms with the buffer full). A cursor
# sweeps in flight up to a full buffer, then back to the knee. BBR's operating point is the knee (Cardwell
# et al., ACM Queue 2016: max bandwidth × min RTT); loss-based TCP fills the buffer. t=0 (shift): at the knee.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

LOSS = '#ec8d8d'
N, PIPE = 14, 8                                # slots in flight: 8 = one BDP, the last 6 are the buffer
RATE = lambda n: min(n, PIPE) / PIPE          # share of 1 Gbit/s
RTT = lambda n: 100 + 100 * max(0.0, n - PIPE) / PIPE
assert RTT(N) == 175
W, H = 400, 304
X0, X1 = 56, 376
xs = lambda n: X0 + n / N * (X1 - X0)
SL = (X1 - X0) / N
CY0, CY1 = 36, 60                              # the strip of slots
RB, RT_ = 158, 104                             # rate plot: baseline, 1 Gbit/s
yr = lambda n: RB - RATE(n) * (RB - RT_)
TB = 258                                       # RTT plot baseline; 175 ms at 204
yt = lambda n: TB - RTT(n) / 175 * 54
D = 10.0
STEP, T0 = 0.4, 0.6
tau = lambda k: T0 + STEP * k                 # cell k fills at tau(k); full buffer at tau(14) = 6.2
DR0, DSTEP = 7.4, 0.2                          # drain back to the knee, one slot per 0.2 s
T = Timeline(D, shift=9.6)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-35 svgd-part3-35">')
a('<title id="svgt-part3-35">Fig 10.8 · BBR aims for the bandwidth-delay product</title>')
a('<desc id="svgd-part3-35">One bottleneck of 1 gigabit per second with a 100 millisecond round trip, so the pipe holds 12.5 megabytes, and a buffer behind it. '
  'As the data in flight grows to fill the pipe, the delivery rate rises to 1 gigabit per second while the round trip stays at 100 milliseconds. '
  'Past that point the rate stays flat and the extra data waits in the queue, raising the round trip to 175 milliseconds when the buffer is full and the next packet is lost. '
  'BBR aims for the knee, a full pipe and an empty queue; loss-based TCP keeps climbing to the full buffer.</desc>')
# the strip: pipe slots and queue slots, aligned with the x-axis below
a(text(xs(PIPE / 2), CY0 - 10, 'pipe', anchor='middle', size=13, fill=CYAN, ls='0'))
a(text(xs(PIPE + (N - PIPE) / 2), CY0 - 10, 'queue', anchor='middle', size=13, fill=ROUTE, ls='0'))
win = lambda on, off: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (on - 0.002, 0.0), (on, 1.0), (D, 1.0)]) if off is None else \
    T.anim('opacity', [(0.0, 0.0), (on - 0.002, 0.0), (on, 1.0), (off - 0.008, 1.0), (off - 0.005, 0.0), (D, 0.0)])
for i in range(1, N + 1):
    x = xs(i - 1) + 2
    col = CYAN if i <= PIPE else ROUTE
    a(f'<rect x="{x:.1f}" y="{CY0}" width="{SL - 4:.1f}" height="{CY1 - CY0}" rx="3" fill="none" stroke="{col}" stroke-opacity="0.55"/>')
    off = None if i <= PIPE else DR0 + DSTEP * (N + 1 - i)
    a(f'<g class="fx" opacity="0">{win(tau(i), off)}<rect x="{x + 3:.1f}" y="{CY0 + 3}" width="{SL - 10:.1f}" height="{CY1 - CY0 - 6}" rx="2" fill="{col}"/></g>')
# the buffer overflows: the next packet is lost
a(f'<g class="fx" opacity="0">{win(tau(N) + 0.3, DR0)}{text(X1, CY0 - 10, "loss", anchor="end", size=13, fill=LOSS, ls="0")}</g>')
# rate plot
a(text(X0 - 8, RT_ - 16, 'delivery rate', anchor='start', size=13, fill=CSOFT, ls='0'))
a(f'<line x1="{X0}" y1="{RB}" x2="{X1}" y2="{RB}" stroke="{CMUTED}"/><line x1="{X0}" y1="{RB}" x2="{X0}" y2="{RT_ - 6}" stroke="{CMUTED}"/>')
a(f'<polyline points="{xs(0):.1f},{yr(0):.1f} {xs(PIPE):.1f},{yr(PIPE):.1f} {xs(N):.1f},{yr(N):.1f}" fill="none" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round"/>')
a(text(X1 - 8, RT_ - 12, '1 Gbit/s', anchor='end', size=13, fill=CYAN, ls='0'))
# RTT plot
a(text(X0 - 8, yt(N) - 16, 'round-trip time', anchor='start', size=13, fill=CSOFT, ls='0'))
a(f'<line x1="{X0}" y1="{TB}" x2="{X1}" y2="{TB}" stroke="{CMUTED}"/><line x1="{X0}" y1="{TB}" x2="{X0}" y2="{yt(N) - 6}" stroke="{CMUTED}"/>')
a(f'<polyline points="{xs(0):.1f},{yt(0):.1f} {xs(PIPE):.1f},{yt(PIPE):.1f} {xs(N):.1f},{yt(N):.1f}" fill="none" stroke="{ROUTE}" stroke-width="2.5" stroke-linejoin="round"/>')
a(text(xs(1), yt(0) - 12, '100 ms', anchor='start', size=13, fill=ROUTE, ls='0'))
a(text(X1 - 12, yt(N) - 12, '175 ms', anchor='end', size=13, fill=ROUTE, ls='0'))
# the two operating points
for n in (PIPE, N):
    a(f'<line x1="{xs(n):.1f}" y1="{CY1 + 6}" x2="{xs(n):.1f}" y2="{TB}" stroke="{CSOFT}" stroke-opacity="0.5" stroke-dasharray="3 4"/>')
a(f'<circle cx="{xs(PIPE):.1f}" cy="{yt(PIPE):.1f}" r="7" fill="none" stroke="{CYAN}" stroke-width="2"/>')
a(f'<circle cx="{xs(N):.1f}" cy="{yt(N):.1f}" r="7" fill="none" stroke="{LOSS}" stroke-width="2"/>')
a(text(xs(PIPE) - 12, yt(PIPE) + 22, 'BBR aims here', anchor='end', size=13, fill=CYAN, ls='0'))
a(text(xs(N) - 12, yt(PIPE) + 22, 'loss-based', anchor='end', size=13, fill=LOSS, ls='0'))
a(text(X0 - 8, TB + 5, '0', anchor='end', size=13, fill=CMUTED, ls='0'))
a(text(xs(PIPE), TB + 20, 'BDP', anchor='middle', size=13, fill=CSOFT, ls='0'))
a(text(X1, TB + 20, 'buffer full', anchor='end', size=13, fill=CSOFT, ls='0'))
a(text(X1, TB + 40, 'data in flight', anchor='end', size=13, fill=CMUTED, ls='0'))
# the cursor (a dot on each curve): rises to a full buffer, holds, drains back to the knee
kn = [(0.0, PIPE), (0.3, PIPE), (0.305, 0.0), (T0, 0.0), (tau(PIPE), PIPE), (tau(N), N), (DR0, N), (DR0 + DSTEP * (N - PIPE), PIPE), (D, PIPE)]
off = lambda f: [(t, f(n) - f(PIPE)) for t, n in kn]
a(f'<g class="fx"><g>{T.translate(off(xs), "x")}'
  f'<g>{T.translate(off(yr), "y")}<circle cx="{xs(PIPE):.1f}" cy="{yr(PIPE):.1f}" r="5" fill="#fff"/></g>'
  f'<g>{T.translate(off(yt), "y")}<circle cx="{xs(PIPE):.1f}" cy="{yt(PIPE):.1f}" r="5" fill="#fff"/></g></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ("Until the pipe is full, more data in flight means more throughput; after that the extra only waits in the bottleneck's queue, adding delay until the buffer overflows. BBR measures the bottleneck rate and the shortest round trip to sit at the knee, while loss-based TCP climbs until a packet is dropped.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The pipe.</b> 1 Gbit/s × 100 ms = 12.5 MB: the <em>bandwidth-delay product</em> (BDP), the data in flight that keeps the link busy with nothing queued.</li>
          <li><b>BBR.</b> Bottleneck Bandwidth and Round-trip propagation time: it takes the highest delivery rate and the lowest round trip it has recently seen, paces at that rate, and keeps about one BDP in flight, probing a little above and below to keep both estimates fresh.</li>
          <li><b>Loss-based TCP.</b> Reno and CUBIC grow until the buffer overflows, so with a deep buffer every packet waits in the queue (bufferbloat). The first BBR largely ignored loss; later versions react to it too, partly because the first crowded out CUBIC flows.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-8">
      <div class="diagram-label">Fig 10.8 · BBR aims for the bandwidth-delay product</div>
      {svg}
      <p id="ch10-modern-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-8', 'ch10-modern-p5', card)
