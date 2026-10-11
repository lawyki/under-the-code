# Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure (Pass 28, law 3). Quorum glass plate. Node A
# waits for C's vote. Two worlds that A cannot tell apart: in one C is slow and its message is still on the way; in
# the other C has crashed. A's clock runs the same in both. If A decides now, the slow world's late vote can make it
# wrong (safety lost); if A waits, the crashed world never answers (liveness lost). The escape real systems take: assume
# delays are bounded eventually and use timeouts. Phase-synced. t=0 (shift): both dilemmas shown.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
def world(x0, head, crashed):
    a(text(x0, 18, head, anchor='start', size=13, fill=QSOFT, ls='0'))
    a(f'<circle cx="{x0 + 30}" cy="66" r="22" fill="{QCARD}" stroke="{TEAL}" stroke-width="1.5"/>' + text(x0 + 30, 71, 'A', anchor='middle', size=13, fill=TEAL, ls='0'))
    a(f'<circle cx="{x0 + 154}" cy="66" r="22" fill="{QCARD}" stroke="{QMUTED if crashed else VIOLET}" stroke-width="1.5" stroke-dasharray="{"4 3" if crashed else "none"}"/>')
    a(text(x0 + 154, 71, 'C', anchor='middle', size=13, fill=QMUTED if crashed else VIOLET, ls='0'))
    a(f'<line x1="{x0 + 54}" y1="66" x2="{x0 + 130}" y2="66" stroke="{QMUTED}" stroke-opacity="0.4" stroke-dasharray="3 4"/>')
    if crashed:
        a(f'<path d="M{x0 + 144},56 l20,20 M{x0 + 164},56 l-20,20" stroke="{QROSE}" stroke-width="3"/>')
    else:
        # the vote crawls towards A, never quite arriving within the loop
        mv = T.translate([(0.0, -60.0), (0.3, -60.0), (0.305, 0.0), (0.8, 0.0), (D - 0.5, -60.0)], 'x')
        a(f'<g class="fx"><g>{mv}<circle cx="{x0 + 128}" cy="66" r="6" fill="{VIOLET}"/></g></g>')
    # A's clock, the same in both
    w = 150
    a(f'<rect x="{x0 + 10}" y="100" width="{w}" height="10" rx="3" fill="none" stroke="{QMUTED}" stroke-opacity="0.5"/>')
    a(f'<rect x="{x0 + 10}" y="100" width="{w}" height="10" rx="3" fill="{TEAL}" fill-opacity="0.6">'
      f'{T.anim("width", [(0.0, w), (0.3, w), (0.305, 0.0), (0.8, 0.0), (D - 0.5, w), (D, w)])}</rect>')
    a(text(x0 + 10, 130, 'A has waited…', anchor='start', size=13, fill=QMUTED, ls='0'))
world(10, 'world 1: C is slow', False)
world(206, 'world 2: C crashed', True)
a(text(200, 162, 'from A, the two look the same', anchor='middle', size=13, fill=QAMBER, ls='0'))
# the dilemma
for k, (t0, l1, l2, col) in enumerate(((3.0, 'decide now:', "C's late vote may disagree, safety lost", QROSE),
                                         (5.0, 'keep waiting:', 'in world 2, for ever; liveness lost', QROSE),
                                         (7.0, 'real systems:', 'time out, assume delays end (Raft)', TEAL))):
    y = 194 + k * 42
    a(f'<g opacity="0.2">{text(10, y, l1, anchor="start", size=13, fill=col, ls="0")}{text(10, y + 18, l2, anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
    a(f'<g opacity="0">{win(t0)}{text(10, y, l1, anchor="start", size=13, fill=col, ls="0")}{text(10, y + 18, l2, anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
H = 194 + 2 * 42 + 30
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-19 svgd-part5-19">')
o.insert(1, '<title id="svgt-part5-19">Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure</title>')
o.insert(2, '<desc id="svgd-part5-19">Node A waits for node C\'s vote. In one world C is slow and its vote is still on the way; in the other C has crashed. A\'s waiting clock runs the same in both, so A cannot tell them apart. '
  'If A decides now, the slow world\'s late vote may disagree with its decision, and safety is lost. If A keeps waiting, in the crashed world it waits for ever, and liveness is lost. Real systems time out, assuming delays eventually end, as Raft does.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('If messages can be delayed without limit, a node cannot tell a slow peer from a crashed one. '
           'Deciding without it risks disagreeing later, and waiting for it risks waiting for ever: no deterministic protocol can rule out both, so real systems assume delays end and use timeouts.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The theorem.</b> Fischer, Lynch and Paterson (1985): in a fully asynchronous system with even one crash, no deterministic protocol is guaranteed both to agree and to finish.</li>
          <li><b>The escapes.</b> Partial synchrony (Paxos, Raft: safe always, live once delays settle); randomness (Ben-Or's coin flips); or weaker agreement (eventually consistent stores such as Dynamo).</li>
          <li><b>In practice.</b> Raft never decides wrongly, but during a long network storm it can stall, electing leader after leader until messages arrive in time again.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-6">
      <div class="diagram-label">Fig 17.6 · FLP impossibility · safety vs liveness vs asynchronous failure</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-6"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-6', cap, card.replace('CAPID', cap))
