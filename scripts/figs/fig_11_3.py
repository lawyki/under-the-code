# Fig 11.3 · One curl, fully traced (Pass 28, law 3). Chart Room plate. curl https://example.com/ as a waterfall:
# a resolver 10 ms away with the name cached, a server 20 ms away. DNS 0-10 ms; TCP handshake 10-30 (SYN out,
# SYN-ACK back); TLS 1.3 30-50 (the ClientHello rides with the final ACK; ServerHello, certificate, Finished
# back); HTTP 50-70 (Finished + GET out, 200 OK back). Each bar starts only when the one before has ended. The
# bars fill on one clock, each row's time lighting as it lands. t=0 (shift): all filled.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, CSOFT, CMUTED
figlib.FONT = SPACE

GOLD, GREEN, BLUE = '#d4a853', '#9bd89b', '#86a8ff'
W = 400
X0, X1, TMAX = 20, 380, 70
xm = lambda ms: X0 + ms / TMAX * (X1 - X0)
ROWS = [('DNS: ', 'name to address', 0, 10, BLUE),
        ('TCP: ', 'SYN, SYN-ACK, ACK', 10, 30, CYAN),
        ('TLS 1.3: ', 'keys, certificate', 30, 50, GOLD),
        ('HTTP: ', 'GET, then 200 OK', 50, 70, GREEN)]
TY, TS, BH = 26, 56, 22                         # first label baseline, row step, bar height
AY = TY + 3 * TS + 8 + BH + 10
H = AY + 50
D, S0, S1 = 9.0, 0.5, 6.5
T = Timeline(D, shift=8.4)
tm = lambda ms: S0 + ms / TMAX * (S1 - S0)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-42 svgd-part3-42">')
a('<title id="svgt-part3-42">Fig 11.3 · One curl, fully traced</title>')
a('<desc id="svgd-part3-42">A waterfall of the four exchanges behind curl https://example.com/, with a 10 millisecond round trip to the resolver and 20 milliseconds to the server. '
  'DNS turns the name into an address from 0 to 10 milliseconds. The TCP handshake runs from 10 to 30, the TLS 1.3 handshake from 30 to 50, and the HTTP request and response from 50 to 70. '
  'Each starts only when the one before it has finished.</desc>')
# faint guides at each hand-off
for ms in (10, 30, 50):
    a(f'<line x1="{xm(ms):.1f}" y1="{TY + 8}" x2="{xm(ms):.1f}" y2="{AY}" stroke="{CMUTED}" stroke-opacity="0.35" stroke-dasharray="2 4"/>')
fills = []
for i, (k, what, t0, t1, col) in enumerate(ROWS):
    y = TY + i * TS
    a(text(X0, y, f'<tspan fill="{col}">{k}</tspan>{what}', anchor='start', size=13, fill=CSOFT, ls='0'))
    a(f'<g class="fx" opacity="0">{win(tm(t1))}{text(X1, y, f"{t0}–{t1} ms", anchor="end", size=13, fill=col, ls="0")}</g>')
    a(f'<rect x="{xm(t0):.1f}" y="{y + 8}" width="{xm(t1) - xm(t0):.1f}" height="{BH}" rx="3" fill="none" stroke="{col}" stroke-opacity="0.45"/>')
    fills.append(f'<rect x="{xm(t0):.1f}" y="{y + 8}" width="{xm(t1) - xm(t0):.1f}" height="{BH}" rx="3" fill="{col}" fill-opacity="0.35" stroke="{col}" stroke-width="1.5"/>')
    # out and back: the round trip each bar is
    mid = (xm(t0) + xm(t1)) / 2
    fills.append(f'<path d="M{xm(t0) + 5:.1f},{y + 8 + BH / 2 + 4} L{mid:.1f},{y + 8 + BH / 2 - 4} L{xm(t1) - 5:.1f},{y + 8 + BH / 2 + 4}" fill="none" stroke="#fff" stroke-opacity="0.75" stroke-width="1.5"/>')
a(f'<defs><clipPath id="clip-fig-11-3"><rect class="fx" x="{X0}" y="0" width="{X1 - X0}" height="{H}">'
  f'{T.anim("width", [(0.0, X1 - X0), (0.3, X1 - X0), (0.305, 0.0), (S0, 0.0), (S1, X1 - X0), (D, X1 - X0)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-11-3)">{"".join(fills)}</g>')
a(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{CMUTED}"/>')
for ms in (0, 10, 30, 50, 70):
    a(f'<line x1="{xm(ms):.1f}" y1="{AY - 4}" x2="{xm(ms):.1f}" y2="{AY + 4}" stroke="{CMUTED}"/>')
    a(text(xm(ms), AY + 20, str(ms), anchor='start' if ms == 0 else ('end' if ms == TMAX else 'middle'), size=13, fill=CMUTED, ls='0'))
a(text(X1, AY + 40, 'milliseconds', anchor='end', size=13, fill=CMUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Fetching one page over HTTPS is four exchanges in a row, each waiting for the one before: DNS finds the address, TCP opens a connection, TLS agrees on keys, and only then does HTTP ask for the page. '
           'With a 20 ms round trip to the server, the page arrives at 70 ms; only the last 20 carry the request.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The setting.</b> A resolver a 10 ms round trip away that already has the name cached, and a server a 20 ms round trip away. A cold lookup that has to walk the DNS tree (Fig 11.6) takes longer.</li>
          <li><b>The overlaps.</b> The TLS ClientHello rides in the same flight as TCP's final ACK, and the GET rides with TLS's Finished, so each handshake costs one round trip, not more.</li>
          <li><b>Inside TLS.</b> Once the keys are agreed, the GET and the page cross the wire as encrypted bytes. curl prints the body as it arrives, then closes the connection or keeps it for the next request.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-3">
      <div class="diagram-label">Fig 11.3 · One curl, fully traced</div>
      {svg}
      <p id="ch11-http-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-3', 'ch11-http-p7', card)
