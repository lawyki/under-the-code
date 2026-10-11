# Fig 17.8 · CAP in production · which database picked which corner (Pass 28, law 3). Quorum glass plate. Two columns,
# the systems that refuse during a partition (CP) and those that keep answering (AP), each with the job it suits. A
# partition strikes; on the same beat each system shows its reaction: CP systems turn away writes on the minority side,
# AP systems accept them and reconcile when the link returns. t=0 (shift): both reactions shown.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

CP = [('etcd, ZooKeeper', 'who leads, cluster config'), ('Spanner, CockroachDB', 'ledgers, orders'), ('MongoDB (default)', 'primary steps down')]
AP = [('Cassandra', 'telemetry, feeds'), ('Dynamo-style stores', 'shopping carts'), ('DNS', 'names: stale beats none')]
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.8, 0.0), (D, 0.0)])
TP, TR = 2.0, 3.2
o = []; a = o.append
a(text(10, 18, 'CP: refuse rather than lie', anchor='start', size=13, fill=VIOLET, ls='0'))
a(text(10, 178, 'AP: answer, reconcile later', anchor='start', size=13, fill=TEAL, ls='0'))
def column(y0, rows, col, react, rcol):
    for k, (name, use) in enumerate(rows):
        y = y0 + k * 44
        a(f'<rect x="10" y="{y}" width="380" height="40" rx="8" fill="{QCARD}" stroke="{col}" stroke-opacity="0.6"/>')
        a(text(20, y + 17, name, anchor='start', size=13, fill=col, ls='0'))
        a(text(20, y + 34, use, anchor='start', size=13, fill=QMUTED, ls='0'))
        a(f'<g opacity="0">{win(TR + 0.25 * k)}{text(380, y + 25, react, anchor="end", size=13, fill=rcol, ls="0")}</g>')
column(28, CP, VIOLET, 'write refused', QROSE)
column(188, AP, TEAL, 'keeps answering', QAMBER)
# the partition
a(f'<g class="fx" opacity="0">{pulse(TP)}<rect x="4" y="4" width="392" height="{188 + 3 * 44 - 4}" rx="12" fill="none" stroke="{QROSE}" stroke-width="2.5" stroke-dasharray="8 6"/></g>')
SY = 188 + 3 * 44 + 22
for t0, t1, s, col in ((0.31, TP, 'network healthy: all agree', QMUTED), (TP, None, 'partition: each picks its failure', QROSE)):
    vis = T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)]) if t1 else win(t0)
    a(f'<g opacity="0">{vis}{text(200, SY, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-21 svgd-part5-21">')
o.insert(1, '<title id="svgt-part5-21">Fig 17.8 · CAP in production · which database picked which corner</title>')
o.insert(2, '<desc id="svgd-part5-21">Systems that choose consistency: etcd and ZooKeeper, for leader election and cluster configuration; Spanner and CockroachDB, for ledgers and orders; MongoDB by default, whose primary steps down without a majority. '
  'Systems that choose availability: Cassandra, for telemetry and feeds; Dynamo-style stores, for shopping carts; DNS, where a stale name beats none. When a partition strikes, the first group refuses writes it cannot confirm and the second accepts them and reconciles later.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each production store picked the failure its users can bear. Coordination services and ledgers refuse writes they cannot confirm; carts, feeds and DNS keep answering and reconcile when the network heals.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reconciling.</b> AP stores settle diverged copies afterwards: last writer wins, vector clocks, or data types that merge by design (CRDTs).</li>
          <li><b>Tunable.</b> Many stores let each request choose: Cassandra's quorum reads and writes, DynamoDB's strongly consistent reads, at the cost of latency or availability.</li>
          <li><b>Spanner.</b> Google's TrueTime, GPS and atomic clocks bounding clock error, makes partitions rare and consistency cheap, but when one does happen it still chooses consistency.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-8">
      <div class="diagram-label">Fig 17.8 · CAP in production · which database picked which corner</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-8"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-8', cap, card.replace('CAPID', cap))
