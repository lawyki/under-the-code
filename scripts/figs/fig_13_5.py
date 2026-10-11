# Fig 13.5 · A bank transfer · atomicity: all of it or none of it (Pass 28, law 3). Strongroom dossier plate.
# Transfer €100 from Alice (200) to Bob (50), and the power fails between the two updates. Run twice, step by step:
# without a transaction the restart finds Alice at 100 and Bob at 50, €100 gone; inside BEGIN … COMMIT the restart
# finds no commit record in the log and undoes the debit, Alice back to 200. Lock-step: three shared steps light
# (debit Alice, power cut, restart), the balances stamp their new values. t=0 (shift): both outcomes shown.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
TS = [1.0, 2.6, 4.2]                               # debit Alice, power cut, restart
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
# the shared steps
STEPS = [(10, 'debit Alice', SEAL), (140, 'power cut', STAMP), (270, 'restart', BRASS)]
for k, (x, s, col) in enumerate(STEPS):
    w = 120
    body = f'<rect x="{x}" y="6" width="{w}" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.5"/>' + text(x + w / 2, 23, s, anchor='middle', size=13, fill=col, ls='0')
    a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(TS[k])}{body}</g>')
BW = 120
BX = [10, 140, 270]
def lane(y, head, hcol, vals, end_text, end_col):
    """vals: per account, list of (t_from, t_to or None, value, colour)."""
    a(text(10, y - 10, head, anchor='start', size=13, fill=hcol, ls='0'))
    for k, (name, seq) in enumerate(vals):
        x = BX[k]
        a(f'<rect x="{x}" y="{y}" width="{BW}" height="44" rx="3" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.6"/>')
        a(text(x + 10, y + 17, name, anchor='start', size=13, fill=PMUTED, ls='0'))
        for t0, t1, v, col in seq:
            body = text(x + 10, y + 37, v, anchor='start', size=16, fill=col, ls='0')
            a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{body}</g>')
            if t0 > 0.5:
                a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="{x - 2}" y="{y - 2}" width="{BW + 4}" height="48" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
    a(f'<g opacity="0">{win(TS[2] + 0.4)}{text(10, y + 66, end_text, anchor="start", size=13, fill=end_col, ls="0")}</g>')
Y1, Y2 = 62, 172
lane(Y1, 'no transaction', OXBLOOD,
     [('Alice', [(0.31, TS[0], '€200', PARCH), (TS[0], None, '€100', PARCH)]),
      ('Bob', [(0.31, None, '€50', PARCH)]),
      ('total', [(0.31, TS[0], '€250', PSOFT), (TS[0], None, '€150', OXBLOOD)])],
     'restart: €100 has vanished', OXBLOOD)
lane(Y2, 'BEGIN … COMMIT', SAGE,
     [('Alice', [(0.31, TS[0], '€200', PARCH), (TS[0], TS[2], '€100?', PMUTED), (TS[2], None, '€200', SAGE)]),
      ('Bob', [(0.31, None, '€50', PARCH)]),
      ('total', [(0.31, None, '€250', PSOFT)])],
     'no COMMIT in the log: undone', SAGE)
H = Y2 + 80
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-6 svgd-part4-6">')
o.insert(1, '<title id="svgt-part4-6">Fig 13.5 · A bank transfer · atomicity: all of it or none of it</title>')
o.insert(2, '<desc id="svgd-part4-6">A transfer of 100 euros from Alice, who has 200, to Bob, who has 50, interrupted by a power cut after Alice is debited and before Bob is paid. '
  'Without a transaction the restarted database shows Alice at 100 and Bob at 50: 100 euros have vanished. Inside BEGIN and COMMIT, the restart finds no commit record in the log and undoes the debit: Alice is back at 200 and the total is still 250.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A transfer is two updates. If the power fails between them, a database without transactions wakes up with Alice debited and Bob unpaid; '
           'inside a <span class="key-term">transaction</span>, <code>BEGIN</code> to <code>COMMIT</code>, recovery finds no commit record and undoes the debit, so the transfer happened in full or not at all.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>How recovery knows.</b> Every change goes to the write-ahead log before the table (Fig 13.6); at restart, the changes of any transaction with no commit record are undone.</li>
          <li><b>Who.</b> Jim Gray set out the transaction concept in 1981 (Turing Award 1998); Theo Härder and Andreas Reuter named it ACID in 1983.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-5">
      <div class="diagram-label">Fig 13.5 · A bank transfer · atomicity: all of it or none of it</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-5', cap, card.replace('CAPID', cap))
