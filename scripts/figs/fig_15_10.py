# Fig 15.10 · The security ecosystem · learning, working, meeting (Pass 28, law 3). Strongroom dossier plate. Top: the
# three rings of the field as one row, learn (CTFs) → work (red team, blue team, bug bounty) → meet (DEF CON, CCC,
# Black Hat). Below, what holds it together, the disclosure clock, run twice on one 0–120 day axis under Project Zero's
# 90+30 policy (since 2021): a bug reported on day 0 and fixed on day 60 is published 30 days later, on day 90; a bug
# still unfixed at day 90 is published then. A cursor walks the days. t=0 (shift): both runs complete.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
stamp = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
# the three rings
RINGS = [(6, 'learn', 'CTF games', SAGE), (140, 'work', 'attack, defend', BRASS), (274, 'meet', 'DEF CON, CCC', SEAL)]
for k, (x, l1, l2, col) in enumerate(RINGS):
    a(f'<rect x="{x}" y="10" width="122" height="48" rx="4" fill="{DCARD}" stroke="{col}" stroke-width="1.5"/>')
    a(text(x + 61, 30, l1, anchor='middle', size=13, fill=col, ls='0'))
    a(text(x + 61, 48, l2, anchor='middle', size=13, fill=PSOFT, ls='0'))
    if k < 2:
        a(f'<path d="M{x + 123},34 H{x + 133} m-5,-4 l5,4 l-5,4" fill="none" stroke="{PMUTED}"/>')
# the disclosure clock
a(text(10, 92, 'the disclosure clock (Project Zero, 90+30)', anchor='start', size=13, fill=SEAL, ls='0'))
X0, X1, DMAX = 20, 380, 120
xd = lambda d: X0 + d / DMAX * (X1 - X0)
TD0, TD1 = 1.0, 9.0                                # story time for day 0 and day 120
td = lambda d: TD0 + d / DMAX * (TD1 - TD0)
AY = 270
a(f'<line x1="{X0}" y1="{AY}" x2="{X1}" y2="{AY}" stroke="{PMUTED}"/>')
for d in (0, 30, 60, 90, 120):
    a(f'<line x1="{xd(d):.1f}" y1="{AY - 4}" x2="{xd(d):.1f}" y2="{AY + 4}" stroke="{PMUTED}"/>')
    a(text(xd(d), AY + 20, str(d), anchor='middle' if 0 < d < DMAX else ('start' if d == 0 else 'end'), size=13, fill=PMUTED, ls='0'))
a(text(X1, AY + 40, 'days after the report', anchor='end', size=13, fill=PMUTED, ls='0'))
a(f'<line x1="{xd(90):.1f}" y1="110" x2="{xd(90):.1f}" y2="{AY}" stroke="{STAMP}" stroke-opacity="0.6" stroke-dasharray="4 3"/>')
a(text(xd(90) + 6, 116, 'day 90', anchor='start', size=13, fill=STAMP, ls='0'))
def lane(y, head, events, bar_to, col):
    a(text(X0, y - 12, head, anchor='start', size=13, fill=PSOFT, ls='0'))
    a(f'<rect x="{X0}" y="{y}" width="{xd(bar_to) - X0:.1f}" height="14" rx="2" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-opacity="0.6"/>')
    for d, lab, c in events:
        x = xd(d)
        mark = f'<path d="M{x:.1f},{y - 3} V{y + 17}" stroke="{c}" stroke-width="3"/>' + text(x + (6 if d < 100 else -6), y + 34, lab, anchor='start' if d < 100 else 'end', size=13, fill=c, ls='0')
        a(f'<g opacity="0.25">{mark}</g><g opacity="0">{win(td(d))}{mark}</g>')
        a(f'<g class="fx" opacity="0">{stamp(td(d))}<circle cx="{x:.1f}" cy="{y + 7}" r="11" fill="none" stroke="{STAMP}" stroke-width="2"/></g>')
lane(144, 'fixed on day 60', [(0, 'report', PSOFT), (60, 'fix', SAGE), (90, 'publish', SEAL)], 90, SAGE)
lane(222, 'never fixed', [(0, 'report', PSOFT), (90, 'publish', SEAL)], 90, OXBLOOD)
# the cursor walking the days
a(f'<g class="fx"><g>{T.translate([(0.0, xd(DMAX) - X0), (0.3, xd(DMAX) - X0), (0.305, 0.0), (TD0, 0.0), (TD1, xd(DMAX) - X0), (D, xd(DMAX) - X0)], "x")}'
  f'<path d="M{X0 - 6},{AY - 14} L{X0},{AY - 4} L{X0 + 6},{AY - 14} Z" fill="{PARCH}"/></g></g>')
H = AY + 50
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-37 svgd-part4-37">')
o.insert(1, '<title id="svgt-part4-37">Fig 15.10 · The security ecosystem · learning, working, meeting</title>')
o.insert(2, '<desc id="svgd-part4-37">The field as three rings: people learn on capture-the-flag games and wargames, work on red teams, blue teams or bug bounties, and meet at conferences such as DEF CON and CCC. '
  'What holds it together is the disclosure clock, under Project Zero\'s 90 plus 30 policy. A bug reported on day 0 and fixed on day 60 is published 30 days later, on day 90. A bug the vendor never fixes is published on day 90 anyway.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('People learn on capture-the-flag games, work on red teams, blue teams or bug bounties, and meet at conferences; the norm holding it together is coordinated disclosure. '
           'A researcher reports a bug privately and the vendor gets a fixed window to ship a fix, after which the details are published whether or not it did.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>90+30.</b> Google's Project Zero gives a vendor 90 days to fix; if it does, details follow 30 days after the fix, so users have time to update. Others use similar windows.</li>
          <li><b>The rings.</b> Learning: PicoCTF, OverTheWire, Hack The Box. Working: internal red teams, blue teams (incident response, threat intelligence), and bounty platforms such as HackerOne and Bugcrowd. Meeting: DEF CON and Black Hat in Las Vegas each August, CCC in Hamburg each December, USENIX Security.</li>
          <li><b>Why it holds.</b> Nothing enforces the norm but reputation, and the alternatives, silence or publishing with no warning, are worse for everyone.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-15-10">
      <div class="diagram-label">Fig 15.10 · The security ecosystem · learning, working, meeting</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html').read()
    i = s.index('id="fig-15-10"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-4', 'fig-15-10', cap, card.replace('CAPID', cap))
