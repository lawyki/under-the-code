# Fig 18.4 · CS intersections · the disciplines that now run on the substrate (Pass 28, law 3). Quorum glass plate.
# Computing at the hub, six fields around it; a spoke lights to each in turn and the field shows one concrete thing it
# now does with computation: biology (protein structures predicted, AlphaFold 2, 2020), economics (trades decided in
# microseconds), governance (digital identity), art (generative images and music), education (tutoring by language
# models), physics (climate models on supercomputers). t=0 (shift): every spoke lit.
import math
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

FIELDS = [('biology', ('protein shapes', 'predicted'), TEAL), ('economics', ('trades in', 'microseconds'), QAMBER),
          ('governance', ('digital', 'identity'), VIOLET), ('art', ('generative', 'images, music'), QROSE),
          ('education', ('tutoring by', 'language models'), TEAL), ('physics', ('climate on', 'supercomputers'), QAMBER)]
W = 400
CX, CY = 200, 150
D = 10.0
T = Timeline(D, shift=9.4)
TS = [0.8 + 1.0 * k for k in range(6)]
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# nodes: left and right columns, three each
import math as _m
BW2, R = 68, 44
POS = [(78, 46), (322, 46), (78, 150), (322, 150), (78, 254), (322, 254)]
for (x, y), (name, (l1, l2), col), t0 in zip(POS, FIELDS, TS):
    ex = x + BW2 if x < CX else x - BW2
    ang = _m.atan2(y - CY, ex - CX)
    hx, hy = CX + R * _m.cos(ang), CY + R * _m.sin(ang)
    a(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{ex}" y2="{y}" stroke="{QMUTED}" stroke-opacity="0.25"/>')
    a(f'<g opacity="0">{win(t0)}<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{ex}" y2="{y}" stroke="{col}" stroke-width="2"/></g>')
    a(f'<rect x="{x - BW2}" y="{y - 32}" width="{2 * BW2}" height="64" rx="10" fill="{QCARD}" stroke="{col}" stroke-opacity="0.8"/>' + text(x, y - 10, name, anchor='middle', size=13, fill=col, ls='0'))
    exb = text(x, y + 8, l1, anchor='middle', size=13, fill=QSOFT, ls='0') + text(x, y + 24, l2, anchor='middle', size=13, fill=QSOFT, ls='0')
    a(f'<g opacity="0.25">{exb}</g><g opacity="0">{win(t0)}{exb}</g>')
    a(f'<g class="fx" opacity="0">{pulse(t0)}<rect x="{x - BW2 - 2}" y="{y - 34}" width="{2 * BW2 + 4}" height="68" rx="11" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{QCARD}" stroke="{QSOFT}" stroke-width="1.5"/>')
a(text(CX, CY - 2, 'computing', anchor='middle', size=13, fill=QSOFT, ls='0'))
a(text(CX, CY + 15, 'beneath', anchor='middle', size=13, fill=QMUTED, ls='0'))
H = 296
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-30 svgd-part5-30">')
o.insert(1, '<title id="svgt-part5-30">Fig 18.4 · CS intersections · the disciplines that now run on the substrate</title>')
o.insert(2, '<desc id="svgd-part5-30">Computing at the centre, joined to six fields, each with one thing it now does by computation: biology predicts protein structures; economics trades in microseconds; governance runs digital identity; art makes generative images and music; education tutors with language models; physics runs climate models on supercomputers.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Six fields that now run on the machinery of this book: predicting a protein\'s shape, trading in microseconds, issuing digital identities, generating images, tutoring and simulating the climate are all programs on processors, networks and stores like the ones the chapters built. '
           'A reader who has finished the book can follow any of them down to the transistor.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Biology.</b> The Human Genome Project finished in 2003; AlphaFold 2 (2020) predicts protein structures well enough to change how biologists work.</li>
          <li><b>Two directions.</b> In some fields computing is a tool for asking questions; in others, markets, identity and media, the software is now the thing itself.</li>
          <li><b>The same parts.</b> Each runs on the stack of Fig 18.1: a model training on GPUs (Chapter 16), a trading system on a low-latency network (Part III), records in databases (Chapter 13).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-4">
      <div class="diagram-label">Fig 18.4 · CS intersections · the disciplines that now run on the substrate</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-4"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-4', cap, card.replace('CAPID', cap))
