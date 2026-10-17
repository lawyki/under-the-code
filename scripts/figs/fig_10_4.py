# Fig 10.4 · The sliding window (Pass 28, law 3). Chart Room. Bytes 100 to 114, a window of 6. Phases:
# 4 bytes in flight and 2 more allowed; the window full; ACK 103 slides it by 3; full again; ACK 109
# slides it on. Each cell is coloured by its state, the window bracket moves. t=0 (shift): after ACK 103.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

N, BASE, WIN = 15, 100, 6
W, H = 400, 236
X0, CWD, CY, CHT = 20, 24, 54, 34
D = 10.0
# phase: (t0, acked_upto (exclusive, offset), sent_upto (exclusive), window start, status)
PH = [(0.0, 0, 4, 0, '4 in flight, 2 more allowed'),
      (1.6, 0, 6, 0, 'window full: wait for an ACK'),
      (3.2, 3, 6, 3, 'ACK 103: the window slides by 3'),
      (4.8, 3, 9, 3, 'sent 106 to 108: full again'),
      (6.4, 9, 9, 9, 'ACK 109: it slides on')]
T = Timeline(D, shift=3.9)
def state(ph, i):
    _, acked, sent, w0, _ = ph
    if i < acked: return 'acked'
    if i < sent: return 'flight'
    if i < w0 + WIN: return 'may'
    return 'not'
COL = {'acked': ('#9bd89b', 0.25), 'flight': (ROUTE, 0.55), 'may': (CYAN, 0.0), 'not': (CSOFT, 0.0)}
def span_anim(t0, t1):
    if t0 == 0.0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)])
    if t1 >= D:
        return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-31 svgd-part3-31">')
a('<title id="svgt-part3-31">Fig 10.4 · The sliding window</title>')
a('<desc id="svgd-part3-31">A sender\'s view of bytes 100 to 114 with a window of six bytes. At first bytes 100 to 103 are in flight and 104 and 105 may still be sent. Then 104 and 105 go out and the window is full. '
  'An ACK numbered 103 arrives, meaning 100 to 102 are received: the window slides to cover 103 to 108, and 106 to 108 may be sent. They go, the window is full again, and ACK 109 slides it on to 109 to 114.</desc>')
a(text(X0, 22, 'BYTES 100 TO 114 · WINDOW 6', size=13, fill=CMUTED))
for i in range(N):
    x = X0 + i * CWD
    a(f'<rect x="{x}" y="{CY}" width="{CWD - 2}" height="{CHT}" rx="2" fill="{CDEEP}" stroke="rgba(223,234,242,0.15)"/>')
    # state colour per contiguous span of phases
    spans = []
    for k, ph in enumerate(PH):
        st = state(ph, i)
        t0 = ph[0]; t1 = PH[k + 1][0] if k + 1 < len(PH) else D
        if spans and spans[-1][0] == st: spans[-1][2] = t1
        else: spans.append([st, t0, t1])
    for st, t0, t1 in spans:
        if st == 'not': continue
        col, op = COL[st]
        extra = f' stroke="{col}" stroke-width="1.5"' if st == 'may' else f' stroke="{col}"'
        a(f'<rect x="{x}" y="{CY}" width="{CWD - 2}" height="{CHT}" rx="2" fill="{col}" fill-opacity="{op}"{extra} opacity="0">{span_anim(t0, t1)}</rect>')
    a(text(x + (CWD - 2) / 2, CY + 22, f'{(BASE + i) % 100:02d}', anchor='middle', size=13, fill='#fff', ls='0'))
# the window bracket
wpts = [(0.0, 0.0)]
for k, ph in enumerate(PH[1:], 1):
    t = ph[0]
    wpts += [(t - 0.3, wpts[-1][1]), (t, ph[3] * CWD)]
wpts += [(D - 0.3, wpts[-1][1]), (D, 0.0)]
a(f'<g>{T.translate(wpts, "x")}<rect x="{X0 - 3}" y="{CY - 7}" width="{WIN * CWD + 4}" height="{CHT + 14}" rx="3" fill="none" stroke="#fff" stroke-width="2"/>'
  f'{text(X0 - 2, CY - 13, "window", size=13, fill="#fff", ls="0")}</g>')
for k, ph in enumerate(PH):
    t0 = ph[0]; t1 = PH[k + 1][0] if k + 1 < len(PH) else D
    a(f'<g opacity="{1 if t0 == 0 else 0}">{span_anim(t0, t1)}{text(X0, 130, ph[4], size=13, fill=CSOFT, ls="0")}</g>')
# legend
for k, (st, lab) in enumerate((('acked', 'acked'), ('flight', 'in flight'), ('may', 'may send'), ('not', 'not yet'))):
    x = X0 + (k % 2) * 180; y = 170 + (k // 2) * 26
    col, op = COL[st]
    a(f'<rect x="{x}" y="{y - 12}" width="16" height="16" rx="2" fill="{col if st != "not" else CDEEP}" fill-opacity="{op if st != "not" else 1}" stroke="{col}" stroke-opacity="{1 if st != "not" else 0.3}"/>')
    a(text(x + 24, y + 1, lab, size=13, fill=CSOFT, ls='0'))
a(text(X0, 226, 'cells show the last two digits', size=13, fill=CMUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Bytes 100 to 114 with a six-byte window: ACK 103 says bytes 100 to 102 arrived, so the window moves up to 103 and three more bytes may go; ACK 109 moves it on by six.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>ACK numbers.</b> "ACK 103" means every byte before 103 arrived; TCP acknowledges the stream, not individual packets.</li>
          <li><b>Two limits.</b> The receiver's window protects the receiver; the congestion window, in the next figure, protects the network. The sender obeys the smaller.</li>
          <li><b>Real sizes.</b> Windows run to megabytes on fast long links; the window-scale option lets the 16-bit field describe them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-4">
      <div class="diagram-label">Fig 10.4 · The sliding window</div>
      {svg}
      <p id="ch10-aimd-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-4', 'ch10-aimd-p3', card)
