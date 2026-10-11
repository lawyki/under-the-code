# Fig 18.1 · The full stack · sand to web service · math at every layer (Pass 28, law 3). Quorum glass plate. Eleven
# layers, transistor at the bottom, distributed systems at the top; each row names the layer and the mathematics it
# realises. A pulse climbs the stack one layer per beat, lighting each row and its chapter as it passes, so the reader
# watches one structure built on the next. t=0 (shift): every layer lit.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

LAYERS = [('transistor', 'solid-state physics', 'Ch 1'), ('logic gates', 'Boolean algebra', 'Ch 1'), ('arithmetic', "two's complement, IEEE 754", 'Ch 2'),
          ('instruction set', 'state machines', 'Ch 3'), ('kernel', 'queueing, scheduling', 'Ch 4'), ('languages', 'types, lambda calculus', 'Ch 5–7'),
          ('networks', 'information, control', 'Ch 8–10'), ('the web', 'graphs, request–response', 'Ch 11–12'), ('databases', 'relational algebra', 'Ch 13'),
          ('cryptography', 'number theory, curves', 'Ch 14'), ('distributed', 'consensus, CAP', 'Ch 16–17')]
W = 400
RH, Y0 = 30, 18
ry = lambda k: Y0 + (len(LAYERS) - 1 - k) * RH          # bottom layer at the bottom
D = 12.0
T = Timeline(D, shift=11.4)
TS = [0.8 + 0.8 * k for k in range(len(LAYERS))]
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
o = []; a = o.append
for k, (layer, math_, ch) in enumerate(LAYERS):
    y = ry(k)
    col = TEAL if k < 4 else (VIOLET if k < 8 else QAMBER)
    a(f'<rect x="10" y="{y}" width="380" height="{RH - 4}" rx="6" fill="{QCARD}" stroke="{col}" stroke-opacity="0.35"/>')
    lit = (text(20, y + 18, layer, anchor='start', size=13, fill=col, ls='0') + text(158, y + 18, math_, anchor='start', size=13, fill=QSOFT, ls='0'))
    a(f'<g opacity="0.3">{lit}</g><g opacity="0">{win(TS[k])}{lit}</g>')
    a(f'<g class="fx" opacity="0">{pulse(TS[k])}<rect x="8" y="{y - 2}" width="384" height="{RH}" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
H = Y0 + len(LAYERS) * RH + 4
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-26 svgd-part5-26">')
o.insert(1, '<title id="svgt-part5-26">Fig 18.1 · The full stack · sand to web service · math at every layer</title>')
o.insert(2, '<desc id="svgd-part5-26">The book\'s eleven layers, bottom to top, each with the mathematics it realises: transistors, solid-state physics; logic gates, Boolean algebra; arithmetic, two\'s complement and IEEE 754; the instruction set, state machines; '
  'the kernel, queueing and scheduling; languages, types and the lambda calculus; networks, information and control theory; the web, graphs and request and response; databases, relational algebra; cryptography, number theory and elliptic curves; distributed systems, consensus and CAP.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each layer is a piece of mathematics made real in the layer beneath it, from the physics of a transistor to the consensus of a thousand machines. '
           'The remarkable thing is not that any one layer works; it\'s that all of them work at once.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Reading it.</b> Bottom to top is the order of the book: Part I builds the machine, II the software on it, III the network, IV data and secrets, V the machines working as one.</li>
          <li><b>Each boundary is a contract.</b> A layer depends only on what the one below promises: gates, which make <span class="key-term">Boolean algebra</span> physical, on voltages; the kernel on the instruction set, TCP on IP's best effort.</li>
          <li><b>Where it leaks.</b> The bugs the book kept returning to (overflow, races, side channels) are places where a lower layer shows through a promise.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-1">
      <div class="diagram-label">Fig 18.1 · The full stack · sand to web service · math at every layer</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-1"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-1', cap, card.replace('CAPID', cap))
