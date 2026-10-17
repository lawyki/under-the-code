# Fig 8.8 · Two stations collide; both back off (Pass 28, law 3). Chart Room. A shared cable: A starts,
# B starts before A's signal reaches it; the signals overlap (collision) and each station hears it,
# both jam and stop, both pick a random number of slots (0 or 1 after a first collision): A picks 0
# and sends (its frame clears the cable before B sends; pre-read audit: the published SVG is the source of truth for that timing), B picks 1, finds the line busy and waits, then sends. Signals travel continuously.
# t=0 (shift): the collision on the wire.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 226
XA, XB, CY = 66, 334, 70                 # station edges on the cable
L = XB - XA
A0, B0, TP = 0.6, 1.2, 1.6               # A starts, B starts, end-to-end propagation time
v = L / TP
MEET = (TP + A0 + B0) / 2
A_AT_B, B_AT_A = A0 + TP, B0 + TP
JAM0, JAM1 = B_AT_A + 0.1, B_AT_A + 0.7
BACK = JAM1 + 0.2
A2, A2_END = BACK + 0.8, BACK + 0.8 + TP + 1.2       # A's retry: propagates, then the frame lasts
B2 = A2_END + 0.4
D = round(B2 + TP + 1.0, 2)
T = Timeline(D, shift=(MEET + A_AT_B) / 2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def grow_right(t0, col, t_end_show, y=CY - 6, h=12):
    return (f'<rect x="{XA}" y="{y}" width="0" height="{h}" fill="{col}" fill-opacity="0.7">'
            f'{T.anim("width", [(0.0, 0.0), (t0, 0.0), (t0 + TP, L), (t_end_show - 0.008, L), (t_end_show - 0.005, 0.0), (D, 0.0)])}</rect>')
def grow_left(t0, col, t_end_show, y=CY - 6, h=12):
    return (f'<rect x="{XB}" y="{y}" width="0" height="{h}" fill="{col}" fill-opacity="0.7">'
            f'{T.anim("x", [(0.0, XB), (t0, XB), (t0 + TP, XA), (t_end_show - 0.008, XA), (t_end_show - 0.005, XB), (D, XB)])}'
            f'{T.anim("width", [(0.0, 0.0), (t0, 0.0), (t0 + TP, L), (t_end_show - 0.008, L), (t_end_show - 0.005, 0.0), (D, 0.0)])}</rect>')
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-9 svgd-part3-9">')
a('<title id="svgt-part3-9">Fig 8.8 · Two stations collide; both back off</title>')
a('<desc id="svgd-part3-9">Two stations, A and B, at the ends of a shared cable. A starts sending; B, which has not yet heard A, starts too. The two signals meet and overlap on the wire: a collision. '
  'Each station hears it, sends a short jam signal and stops. After a first collision each picks 0 or 1 slot at random: A picks 0 and sends again, B picks 1, finds the line busy and waits, then sends once A has finished.</desc>')
for x, nm in ((14, 'A'), (XB, 'B')):
    a(f'<rect x="{x}" y="{CY - 22}" width="52" height="44" rx="3" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.6"/>')
    a(text(x + 26, CY + 6, nm, anchor='middle', size=15, fill='#fff', ls='0'))
a(f'<line x1="{XA}" y1="{CY}" x2="{XB}" y2="{CY}" stroke="{CMUTED}" stroke-width="2"/>')
# first attempt: both signals, the overlap red
a(grow_right(A0, ROUTE, JAM1))
a(grow_left(B0, CYAN, JAM1))
ov_x = [(0.0, XB), (MEET, XA + v * (MEET - A0)), (A_AT_B, XB - v * (A_AT_B - B0)), (B_AT_A, XA), (JAM1 - 0.008, XA), (JAM1 - 0.005, XB), (D, XB)]
ov_w = [(0.0, 0.0), (MEET, 0.0), (A_AT_B, XB - (XB - v * (A_AT_B - B0))), (B_AT_A, L), (JAM1 - 0.008, L), (JAM1 - 0.005, 0.0), (D, 0.0)]
a(f'<rect class="fx" x="{XB}" y="{CY - 9}" width="0" height="18" fill="{RED}">{T.anim("x", ov_x)}{T.anim("width", ov_w)}</rect>')
a(f'<g opacity="0">{win(MEET, JAM1)}{text(200, CY - 22, "collision", anchor="middle", size=14, fill=RED, ls="0")}</g>')
# backoff choices
a(f'<g opacity="0">{win(BACK, D - 0.3)}{text(20, 132, "A: wait 0 slots", size=13, fill=ROUTE, ls="0")}'
  f'{text(380, 132, "B: wait 1 slot", anchor="end", size=13, fill=CYAN, ls="0")}</g>')
# retries
a(grow_right(A2, ROUTE, A2_END + TP, y=CY - 6))
a(f'<g opacity="0">{win(A2 + 0.3, B2)}{text(380, 154, "line busy: B waits", anchor="end", size=13, fill=CYAN, ls="0")}</g>')
a(grow_left(B2, CYAN, D - 0.2, y=CY - 6))
# status
STAT = [(A0, MEET, 'A sends; B has not heard it yet', CSOFT), (MEET, JAM0, 'the signals overlap: collision', RED),
        (JAM0, BACK, 'both hear it, send a jam, stop', RED), (BACK, A2, 'each picks 0 or 1 slot at random', CSOFT),
        (A2, B2, 'A goes first; B defers', ROUTE), (B2, D - 0.2, 'then B sends', CYAN)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(200, 182, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
a(text(20, 214, 'after the k-th collision: 0 to 2ᵏ − 1 slots', size=13, fill=CMUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Two stations hear a quiet cable and start at almost the same moment; their signals collide, both notice, send a short jamming signal and stop. Each then waits a random number of slots (the time a signal takes to cross the cable and back), so one goes first and the other finds the line busy.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The backoff.</b> In <span class="key-term">truncated binary exponential backoff</span>, after the k-th collision in a row a station waits a random 0 to 2<sup>k</sup> − 1 slot times (k stops growing at 10), and gives up after 16 tries.</li>
          <li><b>Why random.</b> If both waited the same time they would collide again; each further collision doubles the range of waits, so the stations spread out as the line gets busier.</li>
          <li><b>Today.</b> In switched Ethernet each link joins just two devices, so collisions no longer happen; Wi-Fi uses the same random backoff but tries to avoid collisions rather than detect them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-8">
      <div class="diagram-label">Fig 8.8 · Two stations collide; both back off</div>
      {svg}
      <p id="ch8-ethernet-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print('D', D, 'meet', MEET)
    splice('part-3', 'fig-8-8', 'ch8-ethernet-p6', card)
