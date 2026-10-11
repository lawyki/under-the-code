# Fig 13.7 · The four isolation levels · what each one permits (Pass 28, law 3). Strongroom dossier plate. Top: the
# SQL standard's table, four levels against three anomalies (dirty read, non-repeatable read, phantom), each cell
# allows or blocks. Below, one anomaly run: T1 reads a balance of 100; T2 sets it to 50 and commits; T1 reads it
# again and gets 50 under read committed, 100 under repeatable read. The matching cells light as it happens.
# t=0 (shift): both answers shown.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
LEVELS = ['read uncommitted', 'read committed', 'repeatable read', 'serializable']
COLS = ['dirty', 're-read', 'phantom']
ALLOW = [(1, 1, 1), (0, 1, 1), (0, 0, 1), (0, 0, 0)]
CX = [196, 270, 348]                               # column centres
HY, R0, RS = 18, 42, 22
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
TS = [0.8, 2.2, 3.8]                               # T1 reads, T2 writes and commits, T1 reads again
TA = 4.6                                            # the two answers
o = []; a = o.append
for x, c in zip(CX, COLS):
    a(text(x, HY, c, anchor='middle', size=13, fill=PMUTED, ls='0'))
a(f'<line x1="10" y1="{HY + 8}" x2="390" y2="{HY + 8}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
for r, (lv, al) in enumerate(zip(LEVELS, ALLOW)):
    y = R0 + r * RS
    a(text(10, y, lv, anchor='start', size=13, fill=PSOFT, ls='0'))
    for x, v in zip(CX, al):
        a(text(x, y, 'allows' if v else 'blocks', anchor='middle', size=13, fill=OXBLOOD if v else SAGE, ls='0'))
# the cells the demo exercises: re-read under read committed (allows) and repeatable read (blocks)
for r in (1, 2):
    y = R0 + r * RS
    a(f'<g class="fx" opacity="0">{win(TA)}<rect x="{CX[1] - 34}" y="{y - 14}" width="68" height="18" rx="3" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
# the demo
DY = R0 + 4 * RS + 22
a(text(10, DY, 'a re-read, run:', anchor='start', size=13, fill=SEAL, ls='0'))
L1, L2 = DY + 30, DY + 64
a(text(10, L1 + 5, 'T1', anchor='start', size=13, fill=BRASS, ls='0'))
a(text(10, L2 + 5, 'T2', anchor='start', size=13, fill=OXBLOOD, ls='0'))
for y in (L1, L2):
    a(f'<line x1="40" y1="{y}" x2="390" y2="{y}" stroke="{PMUTED}" stroke-opacity="0.3"/>')
def chip(x, y, s, col, w):
    return (f'<rect x="{x}" y="{y - 12}" width="{w}" height="24" rx="3" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(x + w / 2, y + 5, s, anchor='middle', size=13, fill=col, ls='0'))
STEPS = [(44, L1, 'read: 100', BRASS, 100, TS[0]), (128, L2, 'set 50, commit', OXBLOOD, 132, TS[1]), (270, L1, 'read again', BRASS, 100, TS[2])]
for x, y, s, col, w, t0 in STEPS:
    body = chip(x, y, s, col, w)
    a(f'<g opacity="0.25">{body}</g><g opacity="0">{win(t0)}{body}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="{x - 3}" y="{y - 15}" width="{w + 6}" height="30" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
AY = L2 + 40
for k, (lv, v, col) in enumerate((('read committed:', '50', OXBLOOD), ('repeatable read:', '100', SAGE))):
    y = AY + k * 20
    a(f'<g opacity="0">{win(TA + 0.3 * k)}{text(170, y, lv, anchor="end", size=13, fill=PSOFT, ls="0")}{text(180, y, v, anchor="start", size=13, fill=col, ls="0")}</g>')
H = AY + 30
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-8 svgd-part4-8">')
o.insert(1, '<title id="svgt-part4-8">Fig 13.7 · The four isolation levels · what each one permits</title>')
o.insert(2, '<desc id="svgd-part4-8">The SQL standard\'s four isolation levels against three anomalies. Read uncommitted allows dirty reads, non-repeatable reads and phantoms; read committed blocks dirty reads; repeatable read also blocks non-repeatable reads; serializable blocks all three. '
  'Below, transaction 1 reads a balance of 100, transaction 2 sets it to 50 and commits, and transaction 1 reads it again: under read committed it sees 50, under repeatable read still 100.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each isolation level is defined by the anomalies it allows: a dirty read sees another transaction\'s uncommitted change, a non-repeatable read sees a row change between two reads, a phantom sees new rows appear. '
           'Run once, the same re-read returns 50 under read committed and 100 under repeatable read.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The defaults.</b> PostgreSQL runs at read committed, MySQL's InnoDB at repeatable read; serializable is kept for code where an anomaly costs more than lost throughput.</li>
          <li><b>The table is a minimum.</b> PostgreSQL's repeatable read is snapshot isolation and blocks phantoms too; snapshot isolation still allows write skew, which only serializable prevents.</li>
          <li><b>How.</b> Engines either lock what a transaction reads, or keep old versions of rows so each transaction reads its own snapshot (MVCC).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-7">
      <div class="diagram-label">Fig 13.7 · The four isolation levels · what each one permits</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-7"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-7', cap, card.replace('CAPID', cap))
