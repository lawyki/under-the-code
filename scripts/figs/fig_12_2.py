# Fig 12.2 · May 1995 to ECMAScript 2026 · the slow legitimisation (Pass 28, law 3). Chart Room plate. A thin axis
# drawn to scale, 1995 to 2026, shows the rhythm: a crowded start, a decade's stall after ES3 (ES4 abandoned in
# 2008), then one edition a year from 2016. Labels sit in an evenly spaced column to the right, joined to their
# dots by leaders that never cross. A marker walks the years; each dot and label lights as it is reached.
# t=0 (shift): every event lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
W = 400
AX, Y95, PY = 58, 34, 10                         # axis x, y of 1995.0, px per year
yy = lambda yr: Y95 + (yr - 1995) * PY
EV = [(1995.4, '1995 · written in 10 days', 'Mocha, LiveScript, JavaScript', ROUTE),
      (1996.6, '1996 · Microsoft\'s JScript', 'in Internet Explorer 3', ROUTE),
      (1997.45, '1997 · ECMA-262', 'standardised as ECMAScript', CYAN),
      (1999.95, '1999 · ES3', 'regular expressions, try/catch', CYAN),
      (2008.6, '2008 · ES4 abandoned', 'too big to agree on', LOSS),
      (2009.95, '2009 · ES5', 'strict mode, JSON', CYAN),
      (2015.45, '2015 · ES2015', 'classes, modules, Promises', CYAN),
      (2021.45, '2016 to 2026 · one a year', 'ES2016 … ES2026, each June', GREEN)]
YEARLY = [2016.45 + k for k in range(11)]
LX, L0, LS = 100, 44, 40                         # label column x, first label baseline, step
D = 10.0
S0, S1 = 0.5, 8.0
T = Timeline(D, shift=9.4)
ts = lambda yr: S0 + (yr - 1995) / 31 * (S1 - S0)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
H = int(max(L0 + LS * (len(EV) - 1) + 30, yy(2026.9) + 14))
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-57 svgd-part3-57">')
a('<title id="svgt-part3-57">Fig 12.2 · May 1995 to ECMAScript 2026 · the slow legitimisation</title>')
a('<desc id="svgd-part3-57">A timeline from 1995 to 2026. In 1995 the language is written in ten days and named Mocha, then LiveScript, then JavaScript. 1996, Microsoft ships JScript in Internet Explorer 3. 1997, it is standardised as ECMA-262, ECMAScript. 1999, ES3. '
  'Then a decade without an edition: ES4 is abandoned in 2008, and ES5 arrives in 2009 with strict mode and JSON. ES2015 brings classes, modules and promises, and from 2016 to 2026 a new edition ships every June.</desc>')
a(f'<line x1="{AX}" y1="{yy(1995)}" x2="{AX}" y2="{yy(2026.9)}" stroke="{CMUTED}"/>')
for y in (1995, 2005, 2015, 2025):
    a(f'<line x1="{AX - 5}" y1="{yy(y)}" x2="{AX}" y2="{yy(y)}" stroke="{CMUTED}"/>')
    a(text(AX - 10, yy(y) + 5, str(y), anchor='end', size=13, fill=CMUTED, ls='0'))
# the yearly train
for yr in YEARLY:
    a(f'<circle cx="{AX}" cy="{yy(yr):.1f}" r="3" fill="{CMUTED}"/>')
    a(f'<g class="fx" opacity="0">{win(ts(yr))}<circle cx="{AX}" cy="{yy(yr):.1f}" r="3.5" fill="{GREEN}"/></g>')
for i, (yr, l1, l2, col) in enumerate(EV):
    ly = L0 + i * LS
    dy = yy(yr)
    a(f'<path d="M{AX + 6},{dy:.1f} L{LX - 8},{ly - 5}" fill="none" stroke="{col}" stroke-opacity="0.45"/>')
    if i < len(EV) - 1:
        a(f'<circle cx="{AX}" cy="{dy:.1f}" r="4.5" fill="{CMUTED}"/>')
        a(f'<g class="fx" opacity="0">{win(ts(yr))}<circle cx="{AX}" cy="{dy:.1f}" r="5" fill="{col}"/></g>')
    t0 = ts(yr) if i < len(EV) - 1 else ts(YEARLY[0])
    lab = text(LX, ly, l1, anchor='start', size=13, fill=col, ls='0') + text(LX, ly + 17, l2, anchor='start', size=13, fill=CSOFT, ls='0')
    a(f'<g opacity="0.4">{lab}</g><g class="fx" opacity="0">{win(t0)}{lab}</g>')
# the marker
span = yy(2026.9) - yy(1995)
a(f'<g class="fx"><g>{T.translate([(0.0, span), (0.3, span), (0.305, 0.0), (S0, 0.0), (S1, span), (D, span)], "y")}'
  f'<path d="M{AX - 14},{yy(1995) - 6} L{AX - 6},{yy(1995)} L{AX - 14},{yy(1995) + 6} Z" fill="#fff"/></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('JavaScript was written in ten days in 1995 and renamed twice for marketing; a standard followed in 1997, then a decade\'s stall when the ambitious ES4 was abandoned. '
           'ES2015 finally brought classes and modules, and since then the language has shipped one edition a year.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The axis.</b> Dots sit at their dates on a scale of 31 years; the labels are spaced evenly so they can be read.</li>
          <li><b>The names.</b> Mocha in May, LiveScript in September, JavaScript in December 1995, after Netscape's deal with Sun, which held the Java trademark. The standard had to be called ECMAScript for the same reason.</li>
          <li><b>The stall and the cadence.</b> ES4 grew to include classes, static types and packages; Microsoft and Yahoo objected, and it was dropped in 2008 for the smaller ES5. Since 2015 the TC39 committee ships whatever proposals are ready each June.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-2">
      <div class="diagram-label">Fig 12.2 · May 1995 to ECMAScript 2026 · the slow legitimisation</div>
      {svg}
      <p id="ch12-eich-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-2', 'ch12-eich-p4', card)
