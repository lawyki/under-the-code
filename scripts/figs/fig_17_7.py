# Fig 17.7 · CAP · when the network splits, consistency or availability (Pass 28, law 3). Quorum glass plate. Two replicas hold
# x = 1. The link between them breaks. A client writes x = 2 to replica 1; another client reads x from replica 2, which
# cannot reach replica 1. Run twice in step: a CP system makes replica 2 refuse ("can't confirm") and stay consistent;
# an AP system makes it answer with the stale x = 1 and stay available. t=0 (shift): both answers given.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
TCUT, TW, TR, TANS = 1.2, 2.4, 4.0, 5.2
o = []; a = o.append
def run(y0, head, hcol, answer, acol):
    a(text(10, y0, head, anchor='start', size=13, fill=hcol, ls='0'))
    R1, R2 = (110, y0 + 46), (290, y0 + 46)
    for (x, y), lab in ((R1, 'replica 1'), (R2, 'replica 2')):
        a(f'<rect x="{x - 56}" y="{y - 22}" width="112" height="44" rx="9" fill="{QCARD}" stroke="{VIOLET}" stroke-opacity="0.7"/>')
        a(text(x, y - 4, lab, anchor='middle', size=13, fill=QSOFT, ls='0'))
    # values
    a(f'<g opacity="0">{first(TW)}{text(R1[0], R1[1] + 14, "x = 1", anchor="middle", size=13, fill=QAMBER, ls="0")}</g>')
    a(f'<g opacity="0">{win(TW)}{text(R1[0], R1[1] + 14, "x = 2", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
    a(text(R2[0], R2[1] + 14, 'x = 1', anchor='middle', size=13, fill=QAMBER, ls='0'))
    # the link, then the cut
    a(f'<g opacity="0">{first(TCUT)}<line x1="{R1[0] + 56}" y1="{R1[1]}" x2="{R2[0] - 56}" y2="{R2[1]}" stroke="{QSOFT}" stroke-width="2"/></g>')
    a(f'<g opacity="0">{win(TCUT)}<line x1="{R1[0] + 56}" y1="{R1[1]}" x2="{R2[0] - 56}" y2="{R2[1]}" stroke="{QROSE}" stroke-width="2" stroke-dasharray="6 6"/>'
      f'<path d="M190,{R1[1] - 10} l20,20 M210,{R1[1] - 10} l-20,20" stroke="{QROSE}" stroke-width="3"/></g>')
    # the write and the read
    a(f'<g opacity="0">{win(TW - 0.4)}{text(R1[0], y0 + 92, "write x = 2", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
    a(f'<g opacity="0">{lit(TR, TANS)}{text(R2[0], y0 + 92, "read x?", anchor="middle", size=13, fill=QSOFT, ls="0")}</g>')
    a(f'<g opacity="0">{win(TANS)}{text(R2[0], y0 + 92, answer, anchor="middle", size=13, fill=acol, ls="0")}</g>')
run(18, 'CP: stay consistent', VIOLET, 'error: can’t confirm', QROSE)
run(140, 'AP: stay available', TEAL, 'x = 1 (stale)', QAMBER)
SY = 140 + 120
a(f'<g opacity="0">{win(TCUT)}{text(200, SY, "partition: the link is cut", anchor="middle", size=13, fill=QROSE, ls="0")}</g>')
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-20 svgd-part5-20">')
o.insert(1, '<title id="svgt-part5-20">Fig 17.7 · CAP · when the network splits, consistency or availability</title>')
o.insert(2, '<desc id="svgd-part5-20">Two replicas both hold x = 1. The link between them is cut. A client writes x = 2 to replica 1, and another client asks replica 2 for x. '
  'In a consistent system, replica 2 cannot confirm the latest value and returns an error. In an available system, replica 2 answers with what it has, the stale x = 1.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('When the link between replicas breaks, a write on one side cannot reach the other. '
           'Asked for x, the cut-off replica can refuse, staying consistent but unavailable, or answer with what it has, staying available but stale; with a partition, it cannot do both.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The theorem.</b> Eric Brewer's conjecture (2000), proved by Gilbert and Lynch (2002): under a network partition a replicated store must give up consistency or availability: <span class="key-term">CP systems</span> refuse, <span class="key-term">AP systems</span> answer.</li>
          <li><b>Why not CA.</b> Real networks do partition, so "consistent and available, without partition tolerance" is not an option a distributed system gets to choose.</li>
          <li><b>PACELC.</b> Daniel Abadi (2010): even with no partition, a system trades latency against consistency, waiting for replicas or answering from the nearest one.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-7">
      <div class="diagram-label">Fig 17.7 · CAP · when the network splits, consistency or availability</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-7"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-7', cap, card.replace('CAPID', cap))
