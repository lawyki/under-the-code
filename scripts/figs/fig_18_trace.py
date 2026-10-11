# Fig 18.1.5 · The trace · what happens when you press Enter on google.com (Pass 28, law 3). Quorum glass plate. The
# eighteen stations of one search as a vertical path through three zones (your machine, the network, Google), each
# with its chapter. A pulse steps down the stations in order; red dotted lines mark the four trust boundaries Chapter 15
# defends (user → kernel, client → resolver, client → server TLS, query → SQL). Then the response climbs back up the
# return line. t=0 (shift): every station lit, the response home.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

ZONES = [('your machine', TEAL, [('KEY', 'contact closes', '1'), ('GATE', 'keycode decoded', '2'), ('CPU', 'interrupt taken', '3'),
                                  ('TRAP', 'into the kernel', 'Bridge'), ('KERN', 'event queued', '4'), ('libc', 'to user space', '5'),
                                  ('V8', 'event loop', '12'), ('JS', 'builds the request', '12')]),
         ('the network', VIOLET, [('DNS', 'name → address', '11'), ('TCP', 'handshake', '10'), ('TLS', 'keys agreed', '14'),
                                  ('HTTP', 'GET /search', '11'), ('IP', 'routed (BGP)', '9'), ('WIRE', 'fibre, Ethernet', '8')]),
         ('Google', QAMBER, [('CLOUD', 'pods, orchestrated', '17'), ('SVC', 'a microservice', '17'), ('INDEX', 'index lookup', '13'),
                             ('RANK', 'many cores, GPUs', '16')])]
BOUND = {'TRAP', 'DNS', 'TLS', 'INDEX'}             # a trust boundary is crossed on the way into these
STATIONS = [(z, col, st) for z, col, sts in ZONES for st in sts]
assert len(STATIONS) == 18
W = 400
RH, HH = 21, 26                                      # row height, zone heading height
PX = 22                                              # the path's x
D = 13.0
T = Timeline(D, shift=12.4)
STEP, T0 = 0.42, 0.8
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
y = 14
rows = []                                            # (y of the station's baseline)
k = 0
for zname, zcol, sts in ZONES:
    y += HH
    a(text(PX + 18, y - 6, zname, anchor='start', size=13, fill=zcol, ls='0'))
    for name, what, ch in sts:
        y += RH
        if name in BOUND:
            a(f'<line x1="{PX + 12}" y1="{y - 15}" x2="390" y2="{y - 15}" stroke="{QROSE}" stroke-opacity="0.8" stroke-dasharray="2 3"/>')
        rows.append(y)
        t0 = T0 + STEP * k
        body = (text(PX + 18, y, name, anchor='start', size=13, fill=zcol, ls='0') + text(PX + 76, y, what, anchor='start', size=13, fill=QSOFT, ls='0')
                + text(390, y, ('Ch ' + ch) if ch != 'Bridge' else 'Bridge', anchor='end', size=13, fill=QMUTED, ls='0'))
        a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(t0)}{body}</g>')
        a(f'<g opacity="0">{win(t0)}<circle cx="{PX}" cy="{y - 4}" r="4" fill="{zcol}"/></g>')
        k += 1
YTOP, YBOT = rows[0] - 4, rows[-1] - 4
a(f'<line x1="{PX}" y1="{YTOP}" x2="{PX}" y2="{YBOT}" stroke="{QMUTED}" stroke-opacity="0.35"/>')
# the return line, on the far left
RX = 8
TRET0 = T0 + STEP * 18 + 0.4
TRET1 = TRET0 + 2.0
a(f'<g opacity="0">{win(TRET0)}<line x1="{RX}" y1="{YBOT}" x2="{RX}" y2="{YTOP}" stroke="{TEAL}" stroke-opacity="0.7" stroke-width="2"/></g>')
# the outgoing pulse, stepping station to station
ky = [(0.0, YBOT - YTOP), (0.3, YBOT - YTOP), (0.305, 0.0)]
for i, ry in enumerate(rows):
    t0 = T0 + STEP * i
    if i:
        ky += [(t0 - 0.12, ky[-1][1]), (t0, ry - 4 - YTOP)]
ky.append((D, ky[-1][1]))
a(f'<g class="fx" opacity="0">{lit(T0, TRET0)}<g>{T.translate(ky, "y")}<circle cx="{PX}" cy="{YTOP}" r="7" fill="none" stroke="#fff" stroke-width="2"/></g></g>')
# the response, climbing home
a(f'<g class="fx" opacity="0">{lit(TRET0, TRET1 + 0.01)}<g>{T.translate([(0.0, 0.0), (TRET0, 0.0), (TRET1, YTOP - YBOT), (D, YTOP - YBOT)], "y")}<circle cx="{RX}" cy="{YBOT}" r="5" fill="{TEAL}"/></g></g>')
SY = y + 30
a(f'<line x1="{PX + 18}" y1="{SY - 4}" x2="{PX + 40}" y2="{SY - 4}" stroke="{QROSE}" stroke-dasharray="2 3"/>' + text(PX + 48, SY, 'trust boundary (Ch 15)', anchor='start', size=13, fill=QMUTED, ls='0'))
a(f'<g opacity="0.3">{text(PX + 18, SY + 22, "the response returns the same way up", anchor="start", size=13, fill=TEAL, ls="0")}</g><g opacity="0">{win(TRET0)}{text(PX + 18, SY + 22, "the response returns the same way up", anchor="start", size=13, fill=TEAL, ls="0")}</g>')
H = SY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-27 svgd-part5-27">')
o.insert(1, '<title id="svgt-part5-27">Fig 18.1.5 · The trace · what happens when you press Enter on google.com</title>')
o.insert(2, '<desc id="svgd-part5-27">Eighteen stations of one search, top to bottom. On your machine: the key\'s contact closes (Chapter 1), the keycode is decoded (2), the CPU takes the interrupt (3), the trap into the kernel (the Bridge), the event is queued (4), libc carries it to user space (5), V8\'s event loop picks it up (12), and JavaScript builds the request (12). '
  'In the network: DNS turns the name into an address (11), TCP shakes hands (10), TLS agrees keys (14), HTTP sends GET /search (11), IP routes it by BGP (9), and the wire carries it as light and voltage (8). '
  'At Google: orchestrated pods (17), a microservice (17), an index lookup (13), and ranking on many cores and GPUs (16). Four trust boundaries are marked, into the kernel, to the resolver, to the server\'s TLS and into the database. The response then returns the same way up.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One search, followed from a key\'s contact to Google\'s ranking and back, passes through sixteen chapters and the Bridge, and crosses four trust boundaries that Chapter 15 defends. '
           'Each station keeps the promise the next relies on, and the whole round trip takes well under a second.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reading it.</b> Top to bottom is the order of the request; the chapter on the right is where each step was taught. The response climbs back up: TLS decrypts, TCP reassembles, the browser parses, the GPU draws.</li>
          <li><b>The red lines.</b> Each is a place where data moves from less trusted to more trusted hands, and where Chapter 15's defences apply.</li>
          <li><b>A first visit.</b> Later searches reuse the open connection and skip DNS, TCP and TLS; and once a browser has learned Google speaks QUIC, the request rides UDP where TCP is drawn here (Fig 10.9).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-trace">
      <div class="diagram-label">Fig 18.1.5 · The trace · what happens when you press Enter on google.com</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-trace"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-trace', cap, card.replace('CAPID', cap))
