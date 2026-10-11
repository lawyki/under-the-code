# Fig 17.5 · Raft · leader election and log replication (Pass 28, law 3). Quorum glass plate. Five nodes, E down.
# Election: A's timeout runs out first; it becomes candidate for term 2 and asks the others for votes; B, C and D grant
# them (with its own, 4 of 5) and A leads. Replication: a client sends x; A appends it and sends it to the others; B
# and C acknowledge first, which with A's own copy makes 3 of 5, a majority, and x is committed; D's copy arrives
# later. Majority of 5 = 3, so 2 failures are tolerated. Phase-synced. t=0 (shift): A leads, x committed on 3 or more.
import math
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

N = 5
MAJ = N // 2 + 1
assert MAJ == 3 and (N - 1) // 2 == 2
W = 400
CX, CY, R = 200, 150, 96
NAMES = 'ABCDE'
POS = {n: (CX + R * math.cos(math.radians(-90 + 72 * i)), CY + R * math.sin(math.radians(-90 + 72 * i))) for i, n in enumerate(NAMES)}
D = 14.0
T = Timeline(D, shift=13.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
TT, TV0, TV1, TL = 1.6, 2.0, 2.8, 3.6               # timeout, votes out, votes back, leader
TX, TA0, TA1, TC, TD = 5.0, 5.8, 6.8, 7.6, 8.6       # client x, append out, acks back (B, C), committed, D's ack
o = []; a = o.append
def fly(p, q, t0, t1, col, r=5):
    (x0, y0), (x1, y1) = p, q
    kx = [(0.0, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)]; ky = [(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)]
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{x0:.1f}" cy="{y0:.1f}" r="{r}" fill="{col}"/></g></g></g>')
# links
for i, n in enumerate(NAMES):
    for m in NAMES[i + 1:]:
        (x0, y0), (x1, y1) = POS[n], POS[m]
        a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{QMUTED}" stroke-opacity="0.12"/>')
# nodes
for n in NAMES:
    x, y = POS[n]
    down = n == 'E'
    a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="{QCARD}" stroke="{QMUTED if down else TEAL}" stroke-opacity="{0.4 if down else 0.8}" stroke-dasharray="{"4 3" if down else "none"}"/>')
    a(text(x, y + 5, n, anchor='middle', size=13, fill=QMUTED if down else QSOFT, ls='0'))
    if down:
        a(text(x, y + 44, 'down', anchor='middle', size=13, fill=QROSE, ls='0'))
# A's role
ax, ay = POS['A']
a(f'<g opacity="0">{lit(TT, TL)}<circle cx="{ax:.1f}" cy="{ay:.1f}" r="24" fill="none" stroke="{QAMBER}" stroke-width="3"/></g>')
a(f'<g opacity="0">{win(TL)}<circle cx="{ax:.1f}" cy="{ay:.1f}" r="24" fill="{VIOLET}" fill-opacity="0.35" stroke="{VIOLET}" stroke-width="3"/></g>')
a(f'<g opacity="0">{lit(TT, TL)}{text(ax + 34, ay + 5, "candidate", anchor="start", size=13, fill=QAMBER, ls="0")}</g>')
a(f'<g opacity="0">{win(TL)}{text(ax + 34, ay + 5, "leader", anchor="start", size=13, fill=VIOLET, ls="0")}</g>')
# election messages
for n in 'BCD':
    fly(POS['A'], POS[n], TV0, TV1 - 0.2, QAMBER)
    fly(POS[n], POS['A'], TV1 - 0.1, TL - 0.1, TEAL)
fly(POS['A'], ((POS['A'][0] + POS['E'][0]) / 2, (POS['A'][1] + POS['E'][1]) / 2), TV0, TV1 - 0.2, QAMBER)
# replication: x appended at A, sent out, acks
for n in 'BCD':
    fly(POS['A'], POS[n], TA0, TA1 - 0.3 if n != 'D' else TC, VIOLET)
for n in 'BC':
    fly(POS[n], POS['A'], TA1 - 0.2, TC - 0.05, TEAL)
fly(POS['D'], POS['A'], TC + 0.1, TD, TEAL)
# x in each log
def logx(n, t0, col):
    x, y = POS[n]
    a(f'<g opacity="0">{win(t0)}<rect x="{x - 10:.1f}" y="{y - 46:.1f}" width="20" height="18" rx="3" fill="{col}" fill-opacity="0.85"/>{text(x, y - 32, "x", anchor="middle", size=13, fill=QCARD, ls="0")}</g>')
logx('A', TX, VIOLET)
for n, t0 in (('B', TA1 - 0.3), ('C', TA1 - 0.3), ('D', TC)):
    logx(n, t0, VIOLET)
# the status line
SY = CY + R + 52
for t0, t1, s, col in ((0.31, TT, 'all follow; no heartbeat arrives', QMUTED), (TT, TL, 'A times out first: votes for A?', QAMBER),
                       (TL, TX, 'B, C, D vote yes: A leads term 2', VIOLET), (TX, TC, 'A appends x, sends it out', QSOFT),
                       (TC, None, 'A, B, C hold x: 3 of 5, committed', TEAL)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(200, SY, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-18 svgd-part5-18">')
o.insert(1, '<title id="svgt-part5-18">Fig 17.5 · Raft · leader election and log replication</title>')
o.insert(2, '<desc id="svgd-part5-18">Five nodes, A to E; E is down. No leader\'s heartbeat arrives, and A\'s election timeout runs out first: it becomes a candidate for term 2 and asks for votes. B, C and D vote for it and A becomes leader. '
  'A client sends x; A appends it to its log and sends it to the others. B and C acknowledge first, so with A\'s own copy three of five nodes hold x, a majority, and x is committed. D\'s copy arrives later.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('When no leader is heard from, the node whose random timeout runs out first asks for votes and leads once a majority agrees. '
           'It appends each command to its log and copies it to the others; once a majority hold it, the entry is committed, so five nodes keep working with two down.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Majorities.</b> In <span class="key-term">log replication</span> an entry counts once a majority hold it. Any two majorities of the same cluster share a node, so a committed entry can never be lost by a later leader: N nodes tolerate ⌊(N − 1)/2⌋ failures, which is why clusters run 3, 5 or 7.</li>
          <li><b>Votes.</b> In <span class="key-term">leader election</span> a node votes once per term, and only for a candidate whose log is at least as up to date as its own; random timeouts make split votes rare.</li>
          <li><b>Where it runs.</b> Diego Ongaro and John Ousterhout published Raft in 2014 as an understandable alternative to Paxos; etcd, Consul and CockroachDB use it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-5">
      <div class="diagram-label">Fig 17.5 · Raft · leader election and log replication</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-5', cap, card.replace('CAPID', cap))
