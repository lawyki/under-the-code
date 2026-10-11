# Fig 12.7 · Critical rendering path · five stages, one ~16 ms frame (Pass 28, law 3). Chart Room plate. The five
# stages across the top; four changes below, each lighting only the stages it re-runs: first load (all five), a new
# width (style, layout, paint, composite), a new colour (style, paint, composite), an animated transform on its own
# layer (composite only). A sweep plays each row in turn; skipped stages stay dark. t=0 (shift): every row shown.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD, LOSS = '#9bd89b', '#d4a853', '#ec8d8d'
STAGES = [('parse', ROUTE), ('style', GOLD), ('layout', LOSS), ('paint', GREEN), ('composite', CYAN)]
ROWS = [('first load', {0, 1, 2, 3, 4}), ('width: 300px', {1, 2, 3, 4}), ('color: red', {1, 3, 4}), ('animate transform', {4})]
W = 400
SW, SG, SX0 = 77, 1, 8
sx = lambda i: SX0 + i * (SW + SG)
HY = 12
RY0, RS = 74, 48                                 # first row label baseline, row step
D = 12.0
T = Timeline(D, shift=11.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.35, 0.0), (D, 0.0)])
o = []; a = o.append
for i, (name, col) in enumerate(STAGES):
    a(f'<rect x="{sx(i)}" y="{HY}" width="{SW}" height="30" rx="4" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.8"/>')
    a(text(sx(i) + SW / 2, HY + 20, name, anchor='middle', size=13, fill=col, ls='0'))
for r, (lab, run) in enumerate(ROWS):
    ly = RY0 + r * RS
    a(text(SX0 + 1, ly, lab, anchor='start', size=13, fill=CSOFT, ls='0'))
    t0 = 0.6 + 2.7 * r
    for i, (name, col) in enumerate(STAGES):
        cy = ly + 8
        if i in run:
            ti = t0 + 0.4 * i
            a(f'<rect x="{sx(i) + 4}" y="{cy}" width="{SW - 8}" height="16" rx="3" fill="none" stroke="{col}" stroke-opacity="0.35"/>')
            a(f'<g opacity="0">{win(ti)}<rect x="{sx(i) + 4}" y="{cy}" width="{SW - 8}" height="16" rx="3" fill="{col}" fill-opacity="0.75"/></g>')
            a(f'<g class="fx" opacity="0">{pulse(ti)}<rect x="{sx(i) + 2}" y="{cy - 2}" width="{SW - 4}" height="20" rx="4" fill="none" stroke="#fff" stroke-width="2"/></g>')
        else:
            a(f'<line x1="{sx(i) + 14}" y1="{cy + 8}" x2="{sx(i) + SW - 14}" y2="{cy + 8}" stroke="{CMUTED}" stroke-opacity="0.45" stroke-dasharray="2 4"/>')
H = RY0 + 3 * RS + 36
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-62 svgd-part3-62">')
o.insert(1, '<title id="svgt-part3-62">Fig 12.7 · Critical rendering path · five stages, one ~16 ms frame</title>')
o.insert(2, '<desc id="svgd-part3-62">The five stages of drawing a page: parse, style, layout, paint, composite. A first load runs all five. Changing an element\'s width re-runs style, layout, paint and composite. '
  'Changing its colour re-runs style, paint and composite but skips layout. Animating a transform on its own layer re-runs only composite.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A change re-runs only the stages it touches: a new width means style, layout, paint and composite again; a new colour skips layout; an animated transform on its own layer needs only composite. '
           'That is why smooth animations move transform and opacity, not width or height.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The stages.</b> Parse turns HTML and CSS into the DOM and CSSOM; style matches rules to elements; layout works out every box's size and position; paint draws each layer's pixels; composite stacks the layers into the frame.</li>
          <li><b>The budget.</b> At 60 frames a second each frame has about 16 ms for style, layout, paint and composite, your JavaScript included (Fig 12.3); parse runs when HTML or CSS arrives.</li>
          <li><b>The fast path.</b> A CSS animation of <code>transform</code> or <code>opacity</code> on its own layer runs on the compositor thread, so it stays smooth even while the main thread is busy.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-7">
      <div class="diagram-label">Fig 12.7 · Critical rendering path · five stages, one ~16 ms frame</div>
      {svg}
      <p id="ch12-dom-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-7', 'ch12-dom-p2', card)
