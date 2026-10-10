# Fig 11.1 · March 1989 to August 1991 · a quiet two and a half years (Pass 28, law 3). Chart Room plate. A
# vertical timeline drawn to scale, 1989 to 1994, so the quiet is a long empty stretch and the take-off a
# cluster: the proposal (Mar 1989, Sendall's "vague but exciting"), the first server (Dec 1990, info.cern.ch on
# a NeXT), the announcement (6 Aug 1991, alt.hypertext), SLAC (12 Dec 1991, first in North America), the
# public-domain release (30 Apr 1993), more than 500 known servers (late 1993, CERN timeline). A marker walks
# down the years; each event lights as it is reached. t=0 (shift): every event lit, the marker at the end.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN = '#9bd89b'
Y89, PY = 44, 80                               # y of 1 Jan 1989, px per year
yy = lambda yr: Y89 + (yr - 1989) * PY
AX, LX = 76, 96                                # axis x, label x
EV = [(1989 + 2.5 / 12, 'Mar 1989', 'the proposal', 'Sendall: “vague but exciting”', CYAN),
      (1990 + 11.5 / 12, 'Dec 1990', 'first server', 'info.cern.ch, on a NeXT cube', CYAN),
      (1991 + 7.2 / 12, 'Aug 1991', 'the announcement', 'posted to alt.hypertext', CYAN),
      (1991 + 11.4 / 12, 'Dec 1991', 'SLAC, California', 'first server in North America', GREEN),
      (1993 + 4.0 / 12, 'Apr 1993', 'public domain', 'CERN gives the software away', GREEN),
      (1993 + 10.5 / 12, 'late 1993', '500+ servers', None, GREEN)]
LG = 40                                        # minimum step between label blocks
ly, prev = [], -1e9
for yr, *_ in EV:
    y = max(yy(yr) + 5, prev + LG); ly.append(y); prev = y
W = 400
H = int(max(yy(1994), ly[-1]) + 24)
D = 10.0
S0, S1 = 0.5, 8.0
T = Timeline(D, shift=9.4)
ts = lambda yr: S0 + (yr - 1989) / 5 * (S1 - S0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-40 svgd-part3-40">')
a('<title id="svgt-part3-40">Fig 11.1 · March 1989 to August 1991 · a quiet two and a half years</title>')
a('<desc id="svgd-part3-40">A timeline from 1989 to 1994, drawn to scale. March 1989, Berners-Lee\'s proposal, which his manager marked “vague but exciting”. '
  'December 1990, the first server, info.cern.ch, on a NeXT cube. August 1991, the announcement on alt.hypertext. December 1991, SLAC in California runs the first server in North America. '
  'Then a gap until April 1993, when CERN puts the software in the public domain, and by late 1993 there are more than 500 web servers.</desc>')
a(f'<line x1="{AX}" y1="{yy(1989)}" x2="{AX}" y2="{yy(1994)}" stroke="{CMUTED}"/>')
for y in range(1989, 1995):
    a(f'<line x1="{AX - 5}" y1="{yy(y)}" x2="{AX + 5}" y2="{yy(y)}" stroke="{CMUTED}"/>')
    a(text(AX - 22, yy(y) + 5, str(y), anchor='end', size=13, fill=CMUTED, ls='0'))
# the quiet: proposal to announcement, one machine and no public
a(f'<line x1="{AX}" y1="{yy(EV[0][0]):.1f}" x2="{AX}" y2="{yy(EV[2][0]):.1f}" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="7" stroke-linecap="round"/>')
a(text(LX, yy(1990.25), '2½ quiet years, one machine', anchor='start', size=13, fill=CYAN, ls='0'))
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
for (yr, when, what, more, col), y in zip(EV, ly):
    ey = yy(yr)
    if y - 5 - ey > 2:
        a(f'<path d="M{AX + 6},{ey:.1f} L{LX - 6},{y - 5:.1f}" fill="none" stroke="{col}" stroke-opacity="0.6"/>')
    else:
        a(f'<line x1="{AX + 6}" y1="{ey:.1f}" x2="{LX - 6}" y2="{ey:.1f}" stroke="{col}" stroke-opacity="0.6"/>')
    a(f'<circle cx="{AX}" cy="{ey:.1f}" r="5" fill="{CMUTED}"/>')
    lab = text(LX, y, f'{when} · ', anchor='start', size=13, fill=CMUTED, ls='0').replace('</text>', f'<tspan fill="{col}">{what}</tspan></text>')
    a(f'<g opacity="0.7">{lab}</g>')
    lit = f'<circle cx="{AX}" cy="{ey:.1f}" r="5" fill="{col}"/>' + text(LX, y, f'{when} · ', anchor='start', size=13, fill=CSOFT, ls='0').replace('</text>', f'<tspan fill="{col}">{what}</tspan></text>')
    if more:
        a(f'<g opacity="0.7">{text(LX, y + 17, more, anchor="start", size=13, fill=CMUTED, ls="0")}</g>')
        lit += text(LX, y + 17, more, anchor='start', size=13, fill=CSOFT, ls='0')
    a(f'<g class="fx" opacity="0">{win(ts(yr))}{lit}</g>')
# the marker walks down the years
a(f'<g class="fx"><g>{T.translate([(0.0, yy(1994) - yy(1989)), (0.3, yy(1994) - yy(1989)), (0.305, 0.0), (S0, 0.0), (S1, yy(1994) - yy(1989)), (D, yy(1994) - yy(1989))], "y")}'
  f'<path d="M{AX - 16},{yy(1989) - 6} L{AX - 8},{yy(1989)} L{AX - 16},{yy(1989) + 6} Z" fill="#fff"/></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('For two and a half years the web was one project on one machine at CERN: a proposal, a server running by December 1990, an announcement in August 1991. '
           'It took off after CERN gave the software away in April 1993; by the end of that year there were more than 500 servers.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> Each dot sits at its date: the long empty stretch is the quiet, the cluster at the bottom is the take-off.</li>
          <li><b>The machine.</b> A NeXT cube in Berners-Lee's office ran the server, <code>httpd</code>, and his browser-editor, WorldWideWeb. A label on it read <em>“This machine is a server. DO NOT POWER IT DOWN!!”</em></li>
          <li><b>The first page.</b> <code>info.cern.ch/hypertext/WWW/TheProject.html</code> described the project itself. Paul Kunz brought the software from CERN to SLAC, whose server went live on 12 December 1991.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-1">
      <div class="diagram-label">Fig 11.1 · March 1989 to August 1991 · a quiet two and a half years</div>
      {svg}
      <p id="ch11-bernerslee-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(ly)
    splice('part-3', 'fig-11-1', 'ch11-bernerslee-p6', card)
