# Fig 10.3 · TCP's state machine (Pass 31 exemplar for Part III, from an empty script). Takeaway: each segment, call
# or timer moves a connection one state along fixed rules from open to closed.
# Concept chosen of three (ledger), redesigned in round 6 as two states of the scene (session e2: the round-5 regroup
# split one scene into halves): on top the opening, below the closing, each with the client and the server as two
# lanes and time running down. Each segment is a packet, a small outlined box carrying its name, that the route reaches
# as it draws between the lanes; each side's state changes where a segment leaves or lands, where its program calls listen, connect or
# close, or where TIME_WAIT's timer runs out. Chart Room's continuous flow: packets travel the chart like routes.
# t=0 is the whole connection, opened and closed.
import figlib
from figlib import Timeline, text, obj, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 530
CX, SX = 146, 254                    # the two lanes
CP, SP = 75, 325                     # state pills, centred (20-unit side margins)
TOP0, BOT0 = 36, 252                 # where each panel's lanes start
def Y(r):                            # row r's height; rows 0 to 4 open, rows 6 to 12 close
    return 58 + r * 32 if r <= 5 else 78 + r * 33
D = 17.0
T = Timeline(D, shift=16.4)
RESET = 0.4
def at(r):                           # story time of event row r
    return 1.0 + 0.95 * r
def held(t):                         # off from the reset until t, then held (on at t=0)
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.001, 0.0), (t - 0.001, 0.0), (t, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-30 svgd-part3-30"{T.beats_attr()}>')
a("<title id=\"svgt-part3-30\">Fig 10.3 · TCP's state machine</title>")
a('<desc id="svgd-part3-30">Two parts, the opening above the closing, each with two lanes, the client on the left and the server on the right, '
  'and time running down. Each segment is drawn as a small packet carrying its name across the lanes. Opening: the server\'s program calls listen '
  'and the server waits in LISTEN; the client starts CLOSED. The client\'s program calls connect: it sends SYN and is in SYN_SENT; the server '
  'receives it, answers SYN-ACK and is in SYN_RCVD; the client receives that, sends ACK and is ESTABLISHED, and the server is ESTABLISHED when '
  'the ACK lands. Data flows both ways. Closing: the client\'s program calls close: it sends FIN and is in FIN_WAIT_1; the server receives it, '
  'acknowledges and is in CLOSE_WAIT; the ACK moves the client to FIN_WAIT_2. The server\'s program calls close: it sends FIN and is in '
  'LAST_ACK; the client receives it, sends the last ACK and enters TIME_WAIT, and the server is CLOSED when that ACK lands. The client waits '
  'out a timer, then is CLOSED. Each segment, call or timer moves one side one state; data moves none.</desc>')

def pill(x, y, name, col, t=None, w=102):
    shape = f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="23" rx="11.5" fill="none" stroke="{col}" stroke-width="1.5"/>'
    word = text(x, y + 3, name, anchor='middle', size=14, fill=col, ls='0', role='label' if len(name) > 6 else None)
    g = obj(shape, word)
    return g if t is None else f'<g opacity="1">{held(t)}{g}</g>'

def segment(r_from, r_to, x1, x2, names, col):
    """A segment leaving one lane at row r_from and landing on the other at r_to: the route draws, and a packet (an
    outlined box carrying the segment's name) travels it, from at(r_from), to sit at the route's middle."""
    y1, y2 = Y(r_from) - 3, Y(r_to) - 3
    d = 1 if x2 > x1 else -1
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    t0, t1 = at(r_from), at(r_from) + 0.8
    draw = T.anim('stroke-dashoffset', [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, L), (t0, L), (t1, 0.0), (D, 0.0)])
    head = f'<polygon points="{x2},{y2} {x2 - 9 * d},{y2 - 6} {x2 - 9 * d},{y2 + 4}" fill="{col}"/>'
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    bw, bh = (46, 26) if len(names) == 1 else (84, 26)
    box = f'<rect x="{mx - bw / 2}" y="{my - bh / 2}" width="{bw}" height="{bh}" rx="3" fill="none" stroke="{col}" stroke-width="1.5"/>'
    mid = f'f103-m{r_from}'
    mask = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'
            f'<rect x="{mx - bw / 2 - 2}" y="{my - bh / 2 - 2}" width="{bw + 4}" height="{bh + 4}" fill="#000"/></mask>')
    tb = t0 + 0.8 * max(0.0, 0.5 - (bw / 2 + 2) / L)
    words = [text(mx, my + 5, names[0], anchor='middle', size=14, fill=col, ls='0')] if len(names) == 1 else \
            [text(mx - 19, my + 5, names[0], anchor='middle', size=14, fill=col, ls='0'), text(mx + 19, my + 5, names[1], anchor='middle', size=14, fill=col, ls='0')]
    a(f'<g opacity="1">{held(t0)}{mask}'
      f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" stroke-dasharray="{L:.1f}" stroke-dashoffset="0" mask="url(#{mid})">{draw}</line>'
      f'<g opacity="1">{held(t1)}{head}</g>'
      f'<g opacity="1">{held(tb)}' + obj(box, *words) + '</g></g>')

def lanes(y0, y1):
    for x in (CX, SX):
        a(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{CSOFT}" stroke-opacity="0.55"/>')

# ---- the opening: from CLOSED and LISTEN to ESTABLISHED
a('<g data-panel="opening">')
a(text(CP, 22, 'client', anchor='middle', size=14, fill=CMUTED, role='label'))
a(text(SP, 22, 'server', anchor='middle', size=14, fill=CMUTED, role='label'))
lanes(TOP0, Y(4) + 44)
DIV = (Y(4) + 44 + BOT0) / 2
a(pill(CP, Y(0), 'CLOSED', CSOFT))
a(text(SX - 8, Y(0) + 3, 'listen', anchor='end', size=14, fill=CYAN, ls='0', role='label'))
a(pill(SP, Y(0), 'LISTEN', CSOFT))
a(f'<g opacity="1">{held(at(1) - 0.4)}' + text(CX + 8, Y(1) - 8, 'connect', anchor='start', size=14, fill=CYAN, ls='0', role='label') + '</g>')
a(pill(CP, Y(1), 'SYN_SENT', CSOFT, at(1)))
a(pill(SP, Y(2), 'SYN_RCVD', CSOFT, at(1) + 0.8))
a(pill(CP, Y(3), 'ESTABLISHED', CYAN, at(2) + 0.8, w=110))
a(pill(SP, Y(4), 'ESTABLISHED', CYAN, at(3) + 0.8, w=110))
segment(1, 2, CX, SX, ['SYN'], CYAN)
segment(2, 3, SX, CX, ['SYN', 'ACK'], CYAN)
segment(3, 4, CX, SX, ['ACK'], CYAN)
a(f'<g opacity="1">{held(at(4) + 0.6)}' + obj(f'<rect x="{CX + 8}" y="{Y(4) + 16}" width="{SX - CX - 16}" height="24" rx="4" fill="none" stroke="{CYAN}" stroke-opacity="0.6" stroke-dasharray="3 4"/>',
                                           text(200, Y(4) + 33, 'data', anchor='middle', size=14, fill=CYAN, ls='0')) + '</g>')
a('</g>')

a(f'<line x1="20" y1="{DIV}" x2="380" y2="{DIV}" stroke="{CSOFT}" stroke-opacity="0.7" stroke-dasharray="2 5"/>')

# ---- the closing: each side's FIN, its ACK, and TIME_WAIT's timer
a('<g data-panel="closing">')
YC = Y(11) + 60                       # the client's last CLOSED, below its timer
lanes(BOT0, YC + 4)
a(f'<g opacity="1">{held(at(6) - 0.4)}' + text(CX - 8, Y(6) - 20, 'close', anchor='end', size=14, fill=ROUTE, ls='0', role='label') + '</g>')
a(pill(CP, Y(6), 'FIN_WAIT_1', ROUTE, at(6)))
a(pill(SP, Y(7), 'CLOSE_WAIT', ROUTE, at(6) + 0.8))
a(pill(CP, Y(8), 'FIN_WAIT_2', ROUTE, at(7) + 0.8))
a(f'<g opacity="1">{held(at(9) - 0.4)}' + text(SX + 8, Y(9) - 20, 'close', size=14, fill=ROUTE, ls='0', role='label') + '</g>')
a(pill(SP, Y(9), 'LAST_ACK', ROUTE, at(9)))
a(pill(CP, Y(10), 'TIME_WAIT', ROUTE, at(9) + 0.8))
a(pill(SP, Y(11), 'CLOSED', CSOFT, at(10) + 0.8))
segment(6, 7, CX, SX, ['FIN'], ROUTE)
segment(7, 8, SX, CX, ['ACK'], ROUTE)
segment(9, 10, SX, CX, ['FIN'], ROUTE)
segment(10, 11, CX, SX, ['ACK'], ROUTE)
# TIME_WAIT's timer: a bar that runs out, then CLOSED
tw0, tw1 = at(10) + 0.8, at(10) + 3.4
a(f'<g opacity="1">{held(tw0)}' + obj(
    f'<rect x="{CP - 44}" y="{Y(11) - 6}" width="88" height="8" rx="4" fill="none" stroke="{ROUTE}" stroke-width="1.3"/>',
    f'<rect x="{CP - 44}" y="{Y(11) - 6}" width="88" height="8" rx="4" fill="{ROUTE}">'
    f'{T.anim("width", [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, 88.0), (tw0, 88.0), (tw1, 0.0), (D, 0.0)])}</rect>') + '</g>')
a(f'<g opacity="1">{held(tw0)}' + text(CP, Y(11) + 18, 'timer', anchor='middle', size=14, fill=CMUTED, ls='0', role='label') + '</g>')
a(f'<g opacity="1">{held(tw1)}<path d="M {CP} {Y(11) + 25} V {YC - 20}" stroke="{CSOFT}" stroke-width="1.5"/>'
  f'<polygon points="{CP - 5},{YC - 22} {CP + 5},{YC - 22} {CP},{YC - 15}" fill="{CSOFT}"/></g>')
a(pill(CP, YC, 'CLOSED', CSOFT, tw1))
a('</g>')

a('</svg>')
svg = '\n'.join(o)

caption = ('Above, the opening: SYN, SYN-ACK and ACK carry each side from CLOSED or LISTEN to ESTABLISHED. Below, the closing: each '
           'FIN, its ACK, each close call and TIME_WAIT\'s timer move one side one state, and the side that closes first waits so '
           'stray packets die before its addresses and ports are reused.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Opening.</b> SYN, SYN-ACK, ACK: three segments carry each side from CLOSED or LISTEN to ESTABLISHED.</li>
          <li><b>Data.</b> In ESTABLISHED both sides send and acknowledge bytes.</li>
          <li><b>Closing.</b> Each side's program calls close, and each side sends its own FIN, which the other acknowledges. The first to close passes FIN_WAIT_1 and FIN_WAIT_2; the second, CLOSE_WAIT and LAST_ACK.</li>
          <li><b>TIME_WAIT.</b> It lasts twice the maximum segment lifetime (Linux uses 60 seconds), so a late copy of a segment cannot land in a new connection.</li>
          <li><b>The eleventh state.</b> CLOSING, reached only when both sides send FIN at once, is not drawn; RFC 793 (1981) defined all eleven. <code>ss -tan</code> on Linux lists every connection's state.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-10-3">
      <div class="diagram-label">Fig 10.3 · TCP's state machine</div>
      {svg}
      <p id="ch10-handshake-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-10-3', 'ch10-handshake-p4', card)
