# Fig 8.10 · Hub vs switch (Pass 28, law 3). Chart Room. One star of four hosts. As a hub it repeats
# A's frame to every port. As a switch it floods a frame for an unknown destination, learns each
# sender's port from the source address, and then forwards only to the right port; its table fills.
# t=0 (shift): the switch with a full table, A to B going only to B.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

W, H = 400, 330
D = 14.0
HUB0, HUB1 = 0.4, 4.2
F_HUB, F1, F2, F3 = 1.0, 5.0, 7.4, 9.8
T = Timeline(D, shift=11.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
HOSTS = {'A': (20, 40), 'B': (320, 40), 'C': (20, 186), 'D': (320, 186)}
PORT = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
CX, CY, CWD, CHT = 150, 112, 100, 48
def anchor(h):
    x, y = HOSTS[h]
    return (x + 60 if x < 200 else x, y + 18)
def corner(h):
    x, y = HOSTS[h]
    return (CX if x < 200 else CX + CWD, CY + (10 if y < 100 else CHT - 10))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-11 svgd-part3-11">')
a('<title id="svgt-part3-11">Fig 8.10 · Hub vs switch: broadcast vs learned</title>')
a('<desc id="svgd-part3-11">Four hosts, A, B, C and D, on one central box. As a hub, it repeats a frame from A to B out of every port, so B, C and D all receive it. '
  'As a switch it starts with an empty table: a frame from A to B, whose port it does not know yet, is sent to every port, and the switch notes that A is on port 1. '
  'B\'s reply goes only to port 1, and the switch notes that B is on port 2. The next frame from A to B goes only to port 2.</desc>')
for h, (x, y) in HOSTS.items():
    a(f'<rect x="{x}" y="{y}" width="60" height="36" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
    a(text(x + 30, y + 24, h, anchor='middle', size=15, fill='#fff', ls='0'))
    (x1, y1), (x2, y2) = anchor(h), corner(h)
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CMUTED}" stroke-width="1.5"/>')
    a(text(x + 30, y + 54 if y < 100 else y - 8, f'port {PORT[h]}', anchor='middle', size=13, fill=CMUTED, ls='0'))
a(f'<rect x="{CX}" y="{CY}" width="{CWD}" height="{CHT}" rx="3" fill="{CPLATE}" stroke="{CYAN}" stroke-width="1.5"/>')
a(f'<g opacity="0">{win(HUB0, HUB1)}{text(CX + CWD / 2, CY + 30, "hub", anchor="middle", size=15, fill=ROUTE, ls="0")}</g>')
a(f'<g>{T.anim("opacity", [(0.0, 1.0), (HUB0 - 0.008, 1.0), (HUB0 - 0.005, 0.0), (HUB1 - 0.002, 0.0), (HUB1, 1.0), (D, 1.0)])}{text(CX + CWD / 2, CY + 30, "switch", anchor="middle", size=15, fill=CYAN, ls="0")}</g>')
def frame(t, src, dsts, col):
    for h in [src] + dsts:
        (x1, y1), (x2, y2) = anchor(h), corner(h)
        a(f'<line class="fx" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="4" opacity="0">{win(t, t + 1.6)}</line>')
        if h != src:
            x, y = HOSTS[h]
            a(f'<rect class="fx" x="{x}" y="{y}" width="60" height="36" rx="2" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="2" opacity="0">{win(t + 0.3, t + 1.6)}</rect>')
frame(F_HUB, 'A', ['B', 'C', 'D'], ROUTE)
frame(F1, 'A', ['B', 'C', 'D'], ROUTE)
frame(F2, 'B', ['A'], CYAN)
frame(F3, 'A', ['B'], CYAN)
frame(F3 + 2.0, 'A', ['B'], CYAN)
# the switch's table
TY = 262
a(text(20, TY - 10, 'SWITCH TABLE', size=13, fill=CMUTED))
a(f'<rect x="20" y="{TY}" width="180" height="56" rx="2" fill="{CPLATE}" stroke="{CYAN}" stroke-opacity="0.4"/>')
for k, (h, t) in enumerate((('A', F1 + 0.4), ('B', F2 + 0.4))):
    a(f'<g>{T.anim("opacity", [(0.0, 1.0), (HUB0, 1.0), (HUB0 + 0.005, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])}{text(32, TY + 22 + k * 22, f"{h} → port {PORT[h]}", size=13, fill=CYAN, ls="0")}</g>')
STAT = [(HUB0, HUB1, 'hub: every port hears it', ROUTE), (F1, F2, 'B unknown: flood, learn A', ROUTE),
        (F2, F3, 'B replies: only to A; learn B', CYAN), (F3, D - 0.2, 'A to B: only B\'s port', CYAN)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(380, TY + 22, s.split(": ")[0] + ":", anchor="end", size=13, fill=col, ls="0")}'
      f'{text(380, TY + 44, s.split(": ")[1], anchor="end", size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A hub repeats every frame out of every port. A switch learns which address sits behind which port by reading the source of each frame, floods only while a destination is still unknown, and after that sends each frame down the one right cable.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Self-configuring.</b> Nobody fills the table in: it builds itself from traffic, and entries expire when a device stops talking.</li>
          <li><b>No more collisions.</b> With one device per switch port and both ends able to send at the same time (full duplex), collision detection never fires.</li>
          <li><b>Broadcasts.</b> Frames addressed to everyone, such as ARP requests, still go out of every port.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-10">
      <div class="diagram-label">Fig 8.10 · Hub vs switch: broadcast vs learned</div>
      {svg}
      <p id="ch8-ethernet-p10" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-10', 'ch8-ethernet-p10', card)
