# Fig 11.15 · HTTP/3 over QUIC · escaping TCP at the protocol layer (Pass 28, law 3). Chart Room plate. Head-of-line
# blocking, the reason QUIC exists. Three streams take turns, A1 B1 C1 A2 B2 C2 A3 B3 C3; A2 (the fourth packet) is
# lost and resent as the tenth. Over TCP (one ordered byte stream) everything after A2 waits for the resend; over
# QUIC (each stream ordered on its own) only A3 waits. Filled: handed to the application on arrival; hollow, with
# a dashed line: held until the resend lands. Both lanes reveal on one clock. t=0 (shift): complete.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
STREAMS = [('A', ROUTE), ('B', CYAN), ('C', GREEN)]
SEQ = [(s, k) for k in (1, 2, 3) for s in 'ABC']  # arrival order, slots 1..9
LOST, RESEND = 4, 10                               # A2 lost; resent in slot 10
assert SEQ[LOST - 1] == ('A', 2)
def held(slot, tcp):
    s, k = SEQ[slot - 1]
    return slot > LOST if tcp else (s == 'A' and k > 2)
W = 400
xs = lambda slot: 60 + (slot - 0.5) * 32
LANES = [(24, 'HTTP/2 over TCP: B and C wait for A', True), (140, 'HTTP/3 over QUIC: only A waits', False)]
ROW = 24
SQ = 14
D, S0, S1 = 10.0, 0.5, 7.5
T = Timeline(D, shift=9.4)
o = []; a = o.append
fills = []
for ly, head, tcp in LANES:
    a(text(10, ly, head, anchor='start', size=13, fill=CSOFT, ls='0'))
    for r, (s, col) in enumerate(STREAMS):
        y = ly + 22 + r * ROW
        a(text(30, y + 5, s, anchor='middle', size=13, fill=col, ls='0'))
        a(f'<line x1="48" y1="{y}" x2="382" y2="{y}" stroke="{CMUTED}" stroke-opacity="0.25"/>')
    for slot, (s, k) in enumerate(SEQ, 1):
        r = 'ABC'.index(s)
        col = STREAMS[r][1]
        y = ly + 22 + r * ROW
        x = xs(slot)
        if slot == LOST:
            fills.append(f'<path d="M{x - 6},{y - 6} l12,12 M{x + 6},{y - 6} l-12,12" stroke="{LOSS}" stroke-width="2.5"/>')
            continue
        if held(slot, tcp):
            fills.append(f'<line x1="{x + SQ / 2}" y1="{y}" x2="{xs(RESEND) - 4}" y2="{y}" stroke="{col}" stroke-dasharray="3 3" stroke-opacity="0.8"/>'
                         f'<rect x="{x - SQ / 2}" y="{y - SQ / 2}" width="{SQ}" height="{SQ}" rx="2" fill="#0a1c2d" stroke="{col}" stroke-width="2"/>'
                         f'<circle cx="{xs(RESEND)}" cy="{y}" r="3.5" fill="{col}"/>')
        else:
            fills.append(f'<rect x="{x - SQ / 2}" y="{y - SQ / 2}" width="{SQ}" height="{SQ}" rx="2" fill="{col}"/>')
    # the resend of A2
    y = ly + 22
    fills.append(f'<rect x="{xs(RESEND) - SQ / 2}" y="{y - SQ / 2}" width="{SQ}" height="{SQ}" rx="2" fill="{ROUTE}" stroke="#fff" stroke-width="1.5"/>')
a(f'<defs><clipPath id="clip-fig-11-15"><rect class="fx" x="44" y="0" width="{390 - 44}" height="400">'
  f'{T.anim("width", [(0.0, 346), (0.3, 346), (0.305, 0.0), (S0, 0.0), (S1, 346), (D, 346)])}</rect></clipPath></defs>')
a(f'<g clip-path="url(#clip-fig-11-15)">{"".join(fills)}</g>')
AY = LANES[1][0] + 22 + 2 * ROW + 24
a(f'<line x1="48" y1="{AY}" x2="382" y2="{AY}" stroke="{CMUTED}"/>')
for slot in range(1, RESEND + 1):
    a(f'<line x1="{xs(slot)}" y1="{AY - 3}" x2="{xs(slot)}" y2="{AY + 3}" stroke="{CMUTED}"/>')
a(text(xs(LOST), AY + 20, 'A2 lost', anchor='middle', size=13, fill=LOSS, ls='0'))
a(text(xs(RESEND) + 10, AY + 20, 'A2 resent', anchor='end', size=13, fill=ROUTE, ls='0'))
a(text(48, AY + 40, 'packets in arrival order', anchor='start', size=13, fill=CMUTED, ls='0'))
H = AY + 50
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-54 svgd-part3-54">')
o.insert(1, '<title id="svgt-part3-54">Fig 11.15 · HTTP/3 over QUIC · escaping TCP at the protocol layer</title>')
o.insert(2, '<desc id="svgd-part3-54">Nine packets from three streams, A, B and C, arrive in turn; the fourth, part of stream A, is lost and resent as the tenth. '
  'Over TCP every packet after the loss, from all three streams, is held until the resend arrives. Over QUIC the packets of B and C are delivered as they arrive, and only stream A waits.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('TCP hands the application one ordered byte stream, so when a packet of stream A is lost, the packets of B and C that arrive after it wait too. '
           'QUIC orders each stream on its own: B and C are delivered as they arrive, and only A waits for the resent packet.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The packets.</b> Three streams take turns; the fourth packet, part of A, is lost and resent at the end. A filled square is handed to the application on arrival; a hollow one waits along its dashed line.</li>
          <li><b>Why TCP cannot help.</b> It numbers bytes, not streams (Fig 10.4), so it cannot know that B's bytes do not depend on A's.</li>
          <li><b>The price of the fix.</b> QUIC runs over UDP and ships in the application, so every server, CDN and firewall had to learn it; the handshake folds in TLS 1.3 (Fig 10.9).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-15">
      <div class="diagram-label">Fig 11.15 · HTTP/3 over QUIC · escaping TCP at the protocol layer</div>
      {svg}
      <p id="ch11-modern-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-15', 'ch11-modern-p6', card)
