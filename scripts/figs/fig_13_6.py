# Fig 13.6 · Write-ahead log · log first, mutate later, replay on crash (Pass 28, law 3). Strongroom dossier plate.
# Two transactions. T42 moves Alice from 200 to 100 and commits: the log records are forced to disk before the
# application hears OK, but the data page is not yet written. T43 moves Bob from 50 to 150 and has not committed,
# yet its dirty page reaches disk early. The power fails. Recovery reads the log: redo T42 (Alice back to 100),
# undo T43 (Bob back to 50). ARIES-style redo plus undo; PostgreSQL is redo-only (noted in the strip).
# t=0 (shift): recovered, consistent.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
TR = [0.6, 1.2, 2.2]                               # log records land
TOK, TLEAK, TCUT, TREDO, TUNDO, TDONE = 1.7, 2.8, 3.6, 4.8, 6.0, 7.0
o = []; a = o.append
# the log
a(text(10, 18, 'write-ahead log, forced to disk', anchor='start', size=13, fill=SEAL, ls='0'))
REC = [('T42  Alice 200 → 100', SEAL), ('T42  commit', SAGE), ('T43  Bob 50 → 150', OXBLOOD)]
RY = [28 + 26 * i for i in range(3)]
for (s, col), y, t0 in zip(REC, RY, TR):
    a(f'<rect x="10" y="{y}" width="240" height="22" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.45"/>')
    a(f'<g opacity="0">{win(t0)}{text(18, y + 16, s, anchor="start", size=13, fill=col, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="8" y="{y - 2}" width="244" height="26" rx="3" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
# the application
a(f'<rect x="266" y="28" width="124" height="48" rx="3" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.6"/>')
a(text(276, 46, 'application', anchor='start', size=13, fill=PMUTED, ls='0'))
a(f'<g opacity="0">{lit(0.31, TOK)}{text(276, 66, "waits…", anchor="start", size=13, fill=PMUTED, ls="0")}</g>')
a(f'<g opacity="0">{win(TOK)}{text(276, 66, "T42: OK", anchor="start", size=13, fill=SAGE, ls="0")}</g>')
# the data pages
PY = 134
a(text(10, PY - 10, 'data pages, written later', anchor='start', size=13, fill=BRASS, ls='0'))
PAGES = [(10, 'Alice', [(0.31, TREDO, '€200', PARCH, None), (TREDO, None, '€100', SAGE, 'redo')]),
         (210, 'Bob', [(0.31, TLEAK, '€50', PARCH, None), (TLEAK, TUNDO, '€150', OXBLOOD, None), (TUNDO, None, '€50', SAGE, 'undo')])]
for x, name, seq in PAGES:
    a(f'<rect x="{x}" y="{PY}" width="180" height="46" rx="3" fill="{DCARD}" stroke="{BRASS}" stroke-opacity="0.7"/>')
    a(text(x + 10, PY + 18, name, anchor='start', size=13, fill=PMUTED, ls='0'))
    for t0, t1, v, col, tag in seq:
        body = text(x + 10, PY + 38, v, anchor='start', size=16, fill=col, ls='0')
        if tag:
            body += text(x + 170, PY + 38, tag, anchor='end', size=13, fill=SAGE, ls='0')
        a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{body}</g>')
        if t0 > 0.5:
            a(f'<g class="fx" opacity="0">{stamp(t0)}<rect x="{x - 2}" y="{PY - 2}" width="184" height="50" rx="4" fill="none" stroke="{STAMP}" stroke-width="2.5"/></g>')
# recovery reads the record it acts on
for y, t0 in ((RY[0], TREDO), (RY[2], TUNDO)):
    a(f'<g class="fx" opacity="0">{lit(t0 - 0.4, t0 + 0.6)}<rect x="8" y="{y - 2}" width="244" height="26" rx="3" fill="none" stroke="{SAGE}" stroke-width="2.5"/></g>')
# the power cut, and what state we are in
CY = PY + 72
cut = f'<rect x="130" y="{CY - 14}" width="140" height="24" rx="12" fill="none" stroke="{STAMP}" stroke-width="2"/>' + text(200, CY + 3, 'power cut', anchor='middle', size=13, fill=STAMP, ls='0')
a(f'<g opacity="0.25">{cut}</g><g opacity="0">{win(TCUT)}{cut}</g>')
SY = CY + 36
for t0, t1, s, col in ((0.31, TCUT, 'running: log first, pages later', PSOFT), (TCUT, TREDO - 0.4, 'Alice\'s page stale, Bob\'s dirty', OXBLOOD),
                       (TREDO - 0.4, TDONE, 'recovery: redo T42, undo T43', SEAL), (TDONE, None, 'consistent: T42 kept, T43 gone', SAGE)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(200, SY, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-7 svgd-part4-7">')
o.insert(1, '<title id="svgt-part4-7">Fig 13.6 · Write-ahead log · log first, mutate later, replay on crash</title>')
o.insert(2, '<desc id="svgd-part4-7">A write-ahead log and two data pages. Transaction 42 moves Alice from 200 to 100 and commits; both records are forced to disk before the application is told OK, but Alice\'s page still says 200. '
  'Transaction 43 moves Bob from 50 to 150 without committing, and Bob\'s page is written early. The power fails. Recovery reads the log, redoes transaction 42 so Alice\'s page says 100, and undoes transaction 43 so Bob\'s says 50 again.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every change is written to the log and forced to disk before the commit is acknowledged; the data pages catch up later, whenever convenient. '
           'After a crash, recovery replays the log: committed changes the pages missed are redone, and uncommitted ones that reached them are undone.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it is fast.</b> Appending to one file is sequential; updating data pages means writes scattered across the disk. A commit costs one log flush, and the pages catch up in the background, at checkpoints.</li>
          <li><b>Redo and undo.</b> This is the ARIES scheme (IBM, 1992), used by DB2, SQL Server and InnoDB. PostgreSQL's log is redo-only: an aborted transaction's row versions simply stay invisible.</li>
          <li><b>The same idea elsewhere.</b> Journaling file systems (Chapter 4) and the replicated logs of Raft and Paxos (Chapter 17) write the intent before doing the deed.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-6">
      <div class="diagram-label">Fig 13.6 · Write-ahead log · log first, mutate later, replay on crash</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-13-6"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-13-6', cap, card.replace('CAPID', cap))
