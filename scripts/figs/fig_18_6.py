# Fig 18.6 · The closing zoom-out · the inverse of where Chapter 1 began (Pass 28, law 3; the picture only). Quorum glass
# plate. The book's frames built outward from the centre, one ring at a time: a transistor, a CPU around it, a kernel,
# a network, a cloud, a civilization; the newest ring is outlined as it lands. The caption is the book's closing claim
# about itself, owner-authored (BRIDGE.md §1): it is read from the page and written back byte for byte, the one caption
# exempt from the two-sentence rule. t=0 (shift): every ring in place.
import re
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

PAGE = '/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html'
_s = open(PAGE).read()
_i = _s.index('id="fig-18-6"')
CAPTION = re.search(r'<p id="ch18-final-p6" class="diagram-caption">(.*?)</p>', _s[_i:], re.S).group(1)
assert CAPTION.startswith('Chapter 1 drew a single transistor.') and CAPTION.endswith('is what was inside the code.')
RINGS = [('CPU', TEAL), ('kernel', VIOLET), ('network', QAMBER), ('cloud', QROSE), ('civilization', TEAL)]
W = 400
CX, CY = 200, 196
R0, RB = 46, 26
D = 10.0
T = Timeline(D, shift=9.4)
TR = [0.8 + 1.3 * k for k in range(6)]        # the centre, then each ring
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.8, 0.0), (D, 0.0)])
o = []; a = o.append
# rings, outermost first so each inner one paints over its parent's fill
for k in range(len(RINGS), 0, -1):
    lab, col = RINGS[k - 1]
    r = R0 + RB * k
    body = (f'<rect x="{CX - r}" y="{CY - r}" width="{2 * r}" height="{2 * r}" rx="10" fill="{col}" fill-opacity="0.06" stroke="{col}" stroke-opacity="0.7"/>'
            + text(CX - r + 10, CY - r + 18, lab, size=13, fill=col, ls='0'))
    a(f'<g opacity="0">{win(TR[k])}{body}</g>')
for k in range(1, len(RINGS) + 1):
    r = R0 + RB * k
    a(f'<g class="fx" opacity="0">{pulse(TR[k])}<rect x="{CX - r - 2}" y="{CY - r - 2}" width="{2 * r + 4}" height="{2 * r + 4}" rx="11" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the centre: one transistor, where Chapter 1 began
centre = (f'<rect x="{CX - R0}" y="{CY - R0}" width="{2 * R0}" height="{2 * R0}" rx="8" fill="{QCARD}" stroke="{QSOFT}" stroke-opacity="0.8"/>'
          + text(CX, CY - 4, 'transistor', anchor='middle', size=13, fill=QSOFT, ls='0')
          + text(CX, CY + 16, 'Chapter 1', anchor='middle', size=13, fill=QMUTED, ls='0'))
a(f'<g opacity="0">{win(TR[0])}{centre}</g>')
ROUT = R0 + RB * len(RINGS)
a(f'<g opacity="0">{win(TR[-1])}{text(CX + ROUT - 10, CY + ROUT - 10, "Chapter 18", anchor="end", size=13, fill=QMUTED, ls="0")}</g>')
H = CY + ROUT + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-32 svgd-part5-32">')
o.insert(1, '<title id="svgt-part5-32">Fig 18.6 · The closing zoom-out · the inverse of where Chapter 1 began</title>')
o.insert(2, '<desc id="svgd-part5-32">A single transistor at the centre, where Chapter 1 began. Around it, one frame at a time, the layers built on it: a CPU, a kernel, a network, a cloud and, outermost, a civilization, reached in Chapter 18.</desc>')
a('</svg>')
svg = '\n'.join(o)

how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Where each frame was built.</b> The transistor and the CPU in Part I, the kernel in Part II, the network in Part III, the cloud in Part V.</li>
          <li><b>The other direction.</b> Chapter 1 started at the same centre, one switch, and worked outward chapter by chapter; this figure makes the whole climb at once.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-6">
      <div class="diagram-label"><span>Fig 18.6 · The closing zoom-out · the inverse of where <a href="part-1#ch1">Chapter 1</a> began</span></div>
      {svg}
      <p id="ch18-final-p6" class="diagram-caption">{CAPTION}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-5', 'fig-18-6', 'ch18-final-p6', card)
