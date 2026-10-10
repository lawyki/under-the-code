# Fig 7.2 · Python's slow conquest (Pass 28, law 3). A vertical timeline with two parallel bars:
# Python 1-2 and Python 3, overlapping from 2008 to 2020, the long split. A cursor steps the years.
# t=0 (shift): the whole line.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

EVENTS = [('1980s', 'ABC, a teaching language at CWI'),
          ('1989', 'van Rossum starts Python'),
          ('1991', '0.9.0 posted to Usenet'),
          ('1994', 'Python 1.0'),
          ('2000', '2.0: list comprehensions'),
          ('2008', '3.0 breaks compatibility'),
          ('2020', 'Python 2 retired'),
          ('2024', '3.13: optional build, no GIL')]
W = 400
AX = 76
Y0, P = 52, 34
D = 10.0
T = Timeline(D, shift=9.4)
RESET = 0.4
step = lambda i: 0.8 + 0.85 * i
ry = lambda i: Y0 + i * P
o = []; a = o.append
H = ry(len(EVENTS) - 1) + 30
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-48 svgd-part2-48">')
a('<title id="svgt-part2-48">Fig 7.2 · Python\'s slow conquest</title>')
a('<desc id="svgd-part2-48">A timeline of Python. 1980s: ABC, a teaching language at CWI in Amsterdam. 1989: Guido van Rossum starts Python over Christmas. 1991: version 0.9.0 is posted to Usenet. 1994: Python 1.0. '
  '2000: Python 2.0 adds list comprehensions. 2008: Python 3.0 breaks compatibility, and Python 2 and Python 3 run side by side for twelve years until Python 2 is retired in 2020. '
  '2024: Python 3.13 offers an optional build without the global interpreter lock.</desc>')
a(text(20, 22, 'Python', size=13, fill=MUTED, ls='0'))
a(f'<rect x="84" y="12" width="12" height="12" rx="2" fill="{GOLD}"/>')
a(text(102, 22, '1 and 2', size=13, fill=GOLD, ls='0'))
a(f'<rect x="184" y="12" width="12" height="12" rx="2" fill="{PHOS}"/>')
a(text(202, 22, '3', size=13, fill=PHOS, ls='0'))
def bar(x, i0, i1, col, end_pad=0):
    y0, y1 = ry(i0), ry(i1) + end_pad
    h = y1 - y0
    a(f'<rect x="{x - 3}" y="{y0}" width="6" height="{h}" rx="3" fill="{col}">'
      f'{T.anim("height", [(0.0, h), (RESET, h), (RESET + 0.005, 0.0), (step(i0), 0.0), (step(i1) + (0.3 if end_pad else 0.0), h), (D, h)])}</rect>')
a(f'<rect x="{AX - 3}" y="{ry(0) - 12}" width="6" height="{ry(3) - ry(0) + 12}" rx="3" fill="rgba(198,222,206,0.18)"/>')
bar(AX - 5, 3, 6, GOLD)
bar(AX + 5, 5, 7, PHOS, end_pad=8)
for i, (yr, ev) in enumerate(EVENTS):
    y = ry(i); t = step(i); hot = i == 5
    dim = T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.3), (t - 0.002, 0.3), (t, 1.0), (D, 1.0)])
    a(f'<g>{dim}')
    a(text(20, y + 5, yr, size=13, fill='#fff' if hot else MUTED, ls='0'))
    if hot:
        a(f'<rect x="96" y="{y - 15}" width="284" height="30" rx="3" fill="{PHOS}" fill-opacity="0.16" stroke="{PHOS}"/>')
    a(text(106 if hot else 100, y + 5, ev, size=14 if hot else 13, fill='#fff' if hot else PHOS_SOFT, ls='0'))
    a('</g>')
    a(f'<circle class="fx" cx="{AX}" cy="{y}" r="12" fill="none" stroke="#fff" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (t + 0.6, 0.0), (D, 0.0)])}</circle>')
a('</svg>')
svg = '\n'.join(o)

caption = ('From a project van Rossum began over Christmas 1989 to the everyday language of data science. '
           'The defining event is the split: Python 3 broke compatibility in 2008, and Python 2 lived beside it for twelve years before it was retired in 2020.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The name.</b> van Rossum (1996): "I chose Python as a working title for the project, being in a slightly irreverent mood (and a big fan of Monty Python's Flying Circus)."</li>
          <li><b>What 3.0 fixed.</b> Text became Unicode, <code>1/2</code> became 0.5, and <code>print</code> became a function: each one broke old code.</li>
          <li><b>The inheritance.</b> From ABC, Python took indentation as structure and a taste for being easy to read.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-2">
      <div class="diagram-label">Fig 7.2 · Python's slow conquest</div>
      {svg}
      <p id="ch7-vanrossum-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-2', 'ch7-vanrossum-p3', card)
