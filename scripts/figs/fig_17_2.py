# Fig 17.2 · Docker image layers · copy-on-write filesystems for software distribution (Pass 28, law 3). Quorum glass
# plate. A Dockerfile's five steps beside the image's layers, one per step, each named by the hash of its contents.
# Edit app.py and rebuild: the four layers below it come from cache unchanged, only the app layer is rebuilt and
# pushed; a second image built on the same base shares the bottom layer, stored once. Phase-synced.
# t=0 (shift): the rebuild done, the shared base marked.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

LAYERS = [('FROM ubuntu:24.04', 'base'), ('RUN apt install python3', 'python'), ('COPY requirements.txt', 'reqs'),
          ('RUN pip install -r …', 'packages'), ('COPY app.py', 'your code')]
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
a(text(10, 18, 'image A, layers bottom up', anchor='start', size=13, fill=QSOFT, ls='0'))
LY0, LH = 186, 34                                     # bottom layer y, layer pitch
ly = lambda k: LY0 - k * LH
TE = 1.0                                               # app.py edited
TC = [1.8 + 0.5 * k for k in range(4)]                 # layers 0..3 come from cache
TB, TP = TC[-1] + 0.8, TC[-1] + 1.8                    # layer 4 rebuilt, pushed
for k, (step, name) in enumerate(LAYERS):
    y = ly(k)
    col = QAMBER if k == 0 else (TEAL if k == 4 else VIOLET)
    a(f'<rect x="10" y="{y - 22}" width="262" height="28" rx="6" fill="{QCARD}" stroke="{col}" stroke-opacity="0.8"/>')
    a(text(20, y - 3, step, anchor='start', size=13, fill=QSOFT, ls='0'))
    if k < 4:
        a(f'<g opacity="0">{win(TC[k])}{text(266, y - 3, "cached", anchor="end", size=13, fill=QMUTED, ls="0")}</g>')
    else:
        a(f'<g opacity="0">{lit(TE, TB)}{text(266, y - 3, "edited", anchor="end", size=13, fill=QROSE, ls="0")}</g>')
        a(f'<g opacity="0">{win(TB)}{text(266, y - 3, "rebuilt", anchor="end", size=13, fill=TEAL, ls="0")}</g>')
        a(f'<g class="fx" opacity="0">{pulse(TB)}<rect x="8" y="{y - 24}" width="266" height="32" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the push: only the top layer travels
RX = 284
a(f'<rect x="{RX}" y="{ly(4) - 26}" width="108" height="36" rx="8" fill="none" stroke="{QMUTED}" stroke-dasharray="4 3"/>')
a(text(RX + 54, ly(4) - 3, 'registry', anchor='middle', size=13, fill=QMUTED, ls='0'))
mv = T.translate([(0.0, 0.0), (TB, 0.0), (TP, RX + 20 - 274), (D, RX + 20 - 274)], 'x')
a(f'<g class="fx" opacity="0">{lit(TB, TP + 0.01)}<g>{mv}<rect x="266" y="{ly(4) - 14}" width="16" height="12" rx="2" fill="{TEAL}"/></g></g>')
a(f'<g opacity="0">{win(TP)}{text(RX + 54, ly(4) + 28, "only this layer", anchor="middle", size=13, fill=TEAL, ls="0")}{text(RX + 54, ly(4) + 46, "is sent", anchor="middle", size=13, fill=TEAL, ls="0")}</g>')
# image B shares the base
BY = LY0 + 40
a(text(10, BY, 'image B, another service:', anchor='start', size=13, fill=QSOFT, ls='0'))
a(f'<rect x="10" y="{BY + 12}" width="262" height="28" rx="6" fill="{QCARD}" stroke="{QAMBER}" stroke-opacity="0.8" stroke-dasharray="4 3"/>')
a(text(20, BY + 31, 'same base layer', anchor='start', size=13, fill=QAMBER, ls='0'))
a(text(282, BY + 31, 'stored once', anchor='start', size=13, fill=QAMBER, ls='0'))
H = BY + 52
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-15 svgd-part5-15">')
o.insert(1, '<title id="svgt-part5-15">Fig 17.2 · Docker image layers · rebuild and ship only what changed</title>')
o.insert(2, '<desc id="svgd-part5-15">An image built from five Dockerfile steps, one layer each, bottom up: the ubuntu base, installing Python, copying the requirements file, installing packages, and copying app.py. '
  'After app.py is edited and the image rebuilt, the four layers below come from the cache unchanged and only the top layer is rebuilt, and only that layer is sent to the registry. A second image built on the same base shares the bottom layer, stored once.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A Dockerfile is the recipe an image is built from: each of its steps produces one read-only layer holding the files that step added or changed, named by a hash of its contents. Change app.py and only its layer is rebuilt and pushed to the registry; images that share a base store it once.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Order matters.</b> A changed step invalidates its layer and every layer above it, so Dockerfiles put what changes least (the base, the packages) first and the code last.</li>
          <li><b>At run time.</b> The layers are stacked into one read-only file system, with a thin writable layer on top for the running container; a write to a lower file copies it up first (copy-on-write).</li>
          <li><b>The idea.</b> Name things by the hash of their contents and share them by reference, as Git stores its objects.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-2">
      <div class="diagram-label">Fig 17.2 · Docker image layers · copy-on-write filesystems for software distribution</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-2"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-2', cap, card.replace('CAPID', cap))
