# Fig 18.2 · The civilization timeline · seven moments that made the rest possible (Pass 28, law 3). Quorum glass plate.
# A thin to-scale axis, 1850 to 2026, beside an evenly spaced column of the seven moments joined by non-crossing leaders:
# Boole (1854, Cork), Turing (1936, Cambridge), the transistor (1947, Bell Labs), ARPANET and UNIX (1969), Diffie and
# Hellman (1976, Stanford), Berners-Lee (1989, CERN), Torvalds (1991, Helsinki). The axis shows the long gap after Boole and
# the crowding after 1947. A marker walks the years. t=0 (shift): every moment lit.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

EV = [(1854, 'Boole, the algebra', 'Cork, Ireland', TEAL), (1936, 'Turing, the machine', 'Cambridge', TEAL),
      (1947, 'the transistor', 'Bell Labs, New Jersey', TEAL), (1969, 'ARPANET and UNIX', 'UCLA, Bell Labs', VIOLET),
      (1976, 'public-key cryptography', 'Diffie, Hellman, Stanford', VIOLET), (1989, 'the web', 'Berners-Lee, CERN', QAMBER),
      (1991, 'Linux', 'Torvalds, Helsinki', QAMBER)]
assert 2026 - 1854 == 172
W = 400
AX, Y0, Y1 = 46, 26, 350
YR0, YR1 = 1850, 2026
yy = lambda yr: Y0 + (yr - YR0) / (YR1 - YR0) * (Y1 - Y0)
LX, L0, LS = 96, 34, 46
D = 11.0
T = Timeline(D, shift=10.4)
ts = lambda yr: 0.8 + (yr - YR0) / (YR1 - YR0) * 7.6
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<line x1="{AX}" y1="{Y0}" x2="{AX}" y2="{Y1}" stroke="{QMUTED}"/>')
for yr in (1850, 1900, 1950, 2000):
    a(f'<line x1="{AX - 5}" y1="{yy(yr):.1f}" x2="{AX}" y2="{yy(yr):.1f}" stroke="{QMUTED}"/>')
    a(text(AX - 8, yy(yr) + 5, str(yr), anchor='end', size=13, fill=QMUTED, ls='0'))
for k, (yr, l1, l2, col) in enumerate(EV):
    ly, dy = L0 + k * LS, yy(yr)
    a(f'<path d="M{AX + 5},{dy:.1f} L{LX - 8},{ly - 5}" fill="none" stroke="{col}" stroke-opacity="0.5"/>')
    a(f'<circle cx="{AX}" cy="{dy:.1f}" r="4" fill="{QMUTED}"/>')
    a(f'<g class="fx" opacity="0">{win(ts(yr))}<circle cx="{AX}" cy="{dy:.1f}" r="5" fill="{col}"/></g>')
    lab = text(LX, ly, f'{yr} · {l1}', anchor='start', size=13, fill=col, ls='0') + text(LX, ly + 17, l2, anchor='start', size=13, fill=QSOFT, ls='0')
    a(f'<g opacity="0.3">{lab}</g><g opacity="0">{win(ts(yr))}{lab}</g>')
span = Y1 - Y0
a(f'<g class="fx"><g>{T.translate([(0.0, span), (0.3, span), (0.305, 0.0), (0.8, 0.0), (8.4, span), (D, span)], "y")}'
  f'<path d="M{AX - 16},{Y0 - 6} L{AX - 8},{Y0} L{AX - 16},{Y0 + 6} Z" fill="#fff"/></g></g>')
H = max(L0 + LS * 6 + 30, Y1 + 14)
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-28 svgd-part5-28">')
o.insert(1, '<title id="svgt-part5-28">Fig 18.2 · The civilization timeline · seven moments that made the rest possible</title>')
o.insert(2, '<desc id="svgd-part5-28">A timeline drawn to scale from 1850 to 2026 with seven moments. 1854: Boole\'s algebra of logic, written in Cork. 1936: Turing\'s universal machine, Cambridge. 1947: the transistor, Bell Labs. 1969: ARPANET and UNIX. 1976: public-key cryptography, Diffie and Hellman at Stanford. 1989: the web, Berners-Lee at CERN. 1991: Linux, Torvalds in Helsinki. After Boole the line is empty for eighty years; everything else crowds into the fifty-five years from 1936.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Seven moments, a few rooms and a few people: Boole\'s algebra in 1854, then no entry for eighty years, then Turing\'s machine, the transistor, the network and the kernel, public keys, the web and Linux in the fifty-five years that followed. '
           'Everything in this book is built on them.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> Dots sit at their years on a line from 1850 to 2026; the labels are spaced evenly so they can be read.</li>
          <li><b>1969, twice.</b> ARPANET's first message (UCLA) and the first UNIX (Bell Labs) came within months of each other, years before either met the other.</li>
          <li><b>Not the only seven.</b> Shannon's information theory (1948) and the integrated circuit (1958) have as good a claim; these are the ones the book's chapters keep returning to.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-2">
      <div class="diagram-label">Fig 18.2 · The civilization timeline · seven moments that made the rest possible</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-2"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-2', cap, card.replace('CAPID', cap))
