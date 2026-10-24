# Fig 10.3 · TCP's state machine (Pass 31 exemplar for Part III, from an empty script). Takeaway: each segment, call
# or timer moves a connection one state along fixed rules from open to closed.
# Concept chosen of three (ledger): the client and the server as two lanes, time running down; each segment crosses
# between them, and each side's state changes where a segment leaves or lands, or where its program calls listen or
# close, or where TIME_WAIT's timer runs out. Chart Room's continuous flow: segments travel the chart like routes.
# t=0 is the whole connection, opened and closed.
import figlib
from figlib import Timeline, text, obj, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 482
CX, SX = 132, 268                    # the two lanes
CP, SP = 66, 334                     # state pills, centred
Y = lambda r: 54 + r * 31
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
a('<desc id="svgd-part3-30">Two lanes, the client on the left and the server on the right, with time running down. '
  'The server\'s program calls listen and the server waits in LISTEN; the client starts CLOSED. The client sends SYN and is in '
  'SYN_SENT; the server receives it, answers SYN+ACK and is in SYN_RCVD; the client receives that, sends ACK and is ESTABLISHED, '
  'and the server is ESTABLISHED when the ACK lands. Data flows both ways. Then the client\'s program calls close: it sends FIN '
  'and is in FIN_WAIT_1; the server receives it, acknowledges and is in CLOSE_WAIT; the ACK moves the client to FIN_WAIT_2. '
  'The server\'s program calls close: it sends FIN and is in LAST_ACK; the client receives it, sends the last ACK and enters '
  'TIME_WAIT, and the server is CLOSED when that ACK lands. The client waits out a timer, then is CLOSED. Each segment, call '
  'or timer moves one side one state.</desc>')

def pill(x, y, name, col, t=None, w=118):
    shape = f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="23" rx="11.5" fill="none" stroke="{col}" stroke-width="1.5"/>'
    word = text(x, y + 3, name, anchor='middle', size=14, fill=col, ls='0', role='label' if len(name) > 6 else None)
    g = obj(shape, word)
    return g if t is None else f'<g opacity="1">{held(t)}{g}</g>'

def segment(r_from, r_to, x1, x2, name, col):
    """A segment leaving one lane at row r_from and landing on the other at r_to; it travels from at(r_from)."""
    y1, y2 = Y(r_from) - 3, Y(r_to) - 3
    d = 1 if x2 > x1 else -1
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    t0, t1 = at(r_from), at(r_from) + 0.8
    draw = T.anim('stroke-dashoffset', [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, L), (t0, L), (t1, 0.0), (D, 0.0)])
    head = f'<polygon points="{x2},{y2} {x2 - 9 * d},{y2 - 6} {x2 - 9 * d},{y2 + 4}" fill="{col}"/>'
    word = text((x1 + x2) / 2, (y1 + y2) / 2 - 7, name, anchor='middle', size=14, fill=col, ls='0',
                role='label' if len(name) > 6 else None)
    a(f'<g opacity="1">{held(t0)}' +
      obj(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" stroke-dasharray="{L:.1f}" stroke-dashoffset="0">{draw}</line>',
          f'<g opacity="1">{held(t1)}{head}</g>', word) + '</g>')

# the client's lane
a('<g data-panel="client">')
a(text(CP, 22, 'client', anchor='middle', size=14, fill=CMUTED, role='label'))
a(f'<line x1="{CX}" y1="34" x2="{CX}" y2="{Y(13) + 4}" stroke="{CSOFT}" stroke-opacity="0.55"/>')
a(pill(CP, Y(0), 'CLOSED', CSOFT))
a(pill(CP, Y(1), 'SYN_SENT', CSOFT, at(1)))
a(pill(CP, Y(3), 'ESTABLISHED', CYAN, at(2) + 0.8, w=128))
a(f'<g opacity="1">{held(at(6) - 0.4)}' + text(CX - 8, Y(6) - 18, 'close', anchor='end', size=14, fill=ROUTE, ls='0', role='label') + '</g>')
a(pill(CP, Y(6), 'FIN_WAIT_1', ROUTE, at(6)))
a(pill(CP, Y(8), 'FIN_WAIT_2', ROUTE, at(7) + 0.8))
a(pill(CP, Y(10), 'TIME_WAIT', ROUTE, at(9) + 0.8))
# TIME_WAIT's timer: a bar that runs out, then CLOSED
tw0, tw1 = at(10) + 0.8, at(10) + 3.4
a(f'<g opacity="1">{held(tw0)}' + obj(
    f'<rect x="{CP - 44}" y="{Y(11) - 6}" width="88" height="8" rx="4" fill="none" stroke="{ROUTE}" stroke-width="1.3"/>',
    f'<rect x="{CP - 44}" y="{Y(11) - 6}" width="88" height="8" rx="4" fill="{ROUTE}">'
    f'{T.anim("width", [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, 88.0), (tw0, 88.0), (tw1, 0.0), (D, 0.0)])}</rect>',
    text(CP, Y(11) + 18, 'timer', anchor='middle', size=14, fill=CMUTED, ls='0')) + '</g>')
a(f'<g opacity="1">{held(tw1)}<path d="M {CP} {Y(11) + 26} V {Y(13) - 22}" stroke="{CSOFT}" stroke-width="1.5"/>'
  f'<polygon points="{CP - 5},{Y(13) - 24} {CP + 5},{Y(13) - 24} {CP},{Y(13) - 17}" fill="{CSOFT}"/></g>')
a(pill(CP, Y(13), 'CLOSED', CSOFT, tw1))
a('</g>')

# the server's lane
a('<g data-panel="server">')
a(text(SP, 22, 'server', anchor='middle', size=14, fill=CMUTED, role='label'))
a(f'<line x1="{SX}" y1="34" x2="{SX}" y2="{Y(13) + 4}" stroke="{CSOFT}" stroke-opacity="0.55"/>')
a(text(SX - 8, Y(0) + 3, 'listen', anchor='end', size=14, fill=CYAN, ls='0', role='label'))
a(pill(SP, Y(0), 'LISTEN', CSOFT))
a(pill(SP, Y(2), 'SYN_RCVD', CSOFT, at(1) + 0.8))
a(pill(SP, Y(4), 'ESTABLISHED', CYAN, at(3) + 0.8, w=128))
a(pill(SP, Y(7), 'CLOSE_WAIT', ROUTE, at(6) + 0.8))
a(f'<g opacity="1">{held(at(9) - 0.4)}' + text(SX + 8, Y(9) - 18, 'close', size=14, fill=ROUTE, ls='0', role='label') + '</g>')
a(pill(SP, Y(9), 'LAST_ACK', ROUTE, at(9)))
a(pill(SP, Y(11), 'CLOSED', CSOFT, at(10) + 0.8))
a('</g>')

# the segments between them
a('<g data-panel="segments">')
segment(1, 2, CX, SX, 'SYN', CYAN)
segment(2, 3, SX, CX, 'SYN+ACK', CYAN)
segment(3, 4, CX, SX, 'ACK', CYAN)
a(f'<g opacity="1">{held(at(4) + 0.6)}' + obj(f'<rect x="{CX + 8}" y="{Y(4) + 12}" width="{SX - CX - 16}" height="40" rx="4" fill="none" stroke="{CYAN}" stroke-opacity="0.6" stroke-dasharray="3 4"/>',
                                           text(200, Y(5) + 6, 'data', anchor='middle', size=14, fill=CYAN, ls='0')) + '</g>')
segment(6, 7, CX, SX, 'FIN', ROUTE)
segment(7, 8, SX, CX, 'ACK', ROUTE)
segment(9, 10, SX, CX, 'FIN', ROUTE)
segment(10, 11, CX, SX, 'ACK', ROUTE)
a('</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Time runs down: each segment drawn between the two lanes, and each listen or close from the program, moves one side to '
           'its next state. The side that closes first waits in TIME_WAIT so that stray packets from this connection die before '
           'its addresses and ports are reused.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Opening.</b> SYN, SYN+ACK, ACK: three segments carry each side from CLOSED or LISTEN to ESTABLISHED.</li>
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
