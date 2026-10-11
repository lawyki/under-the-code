# Fig 18.3 · Three things the next decade will change (Pass 28, law 3). Quorum glass plate. The classical stack in the
# middle; three new substrates attach beside it, not in place of it: specialised chips (as general-purpose speed-ups
# slow), quantum processors (for a few structured problems), neuromorphic and analog accelerators (for neural networks).
# Below, two lists: what changes (RSA and elliptic-curve keys fade, single-thread clock scaling fades) and what stays
# (Boolean algebra, relational algebra, the layered model). t=0 (shift): all three attached, the transient items faded.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
fade = lambda t0: T.anim('opacity', [(0.0, 0.3), (0.3, 0.3), (0.305, 1.0), (t0 - 0.002, 1.0), (t0 + 0.6, 0.3), (D, 0.3)])
o = []; a = o.append
a(f'<rect x="10" y="14" width="112" height="190" rx="10" fill="{QCARD}" stroke="{QSOFT}" stroke-opacity="0.8"/>')
a(text(66, 104, 'classical', anchor='middle', size=13, fill=QSOFT, ls='0'))
a(text(66, 122, 'CPUs, GPUs', anchor='middle', size=13, fill=QMUTED, ls='0'))
NEW = [(14, 'specialised chips', 'as general speed-ups slow', TEAL, 1.2),
       (80, 'quantum', 'a few structured problems', VIOLET, 2.4),
       (146, 'neuromorphic, analog', 'for neural networks', QAMBER, 3.6)]
for y, l1, l2, col, t0 in NEW:
    body = (f'<rect x="142" y="{y}" width="248" height="58" rx="9" fill="{QCARD}" stroke="{col}" stroke-width="1.5"/>'
            + text(154, y + 24, l1, anchor='start', size=13, fill=col, ls='0') + text(154, y + 44, l2, anchor='start', size=13, fill=QMUTED, ls='0'))
    link = f'<line x1="122" y1="{y + 29}" x2="142" y2="{y + 29}" stroke="{col}" stroke-width="2" stroke-dasharray="3 3"/>'
    a(f'<g opacity="0.2">{link}{body}</g><g opacity="0">{win(t0)}{link}{body}</g>')
a(text(200, 236, 'added beside, not instead', anchor='middle', size=13, fill=QSOFT, ls='0'))
# what fades and what stays
LY = 272
a(text(10, LY, 'fades', anchor='start', size=13, fill=QROSE, ls='0'))
a(text(206, LY, 'stays', anchor='start', size=13, fill=TEAL, ls='0'))
for k, s in enumerate(('RSA, elliptic-curve keys', 'faster single threads')):
    a(f'<g opacity="1">{fade(5.0 + 0.6 * k)}{text(10, LY + 22 + k * 20, s, anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
for k, s in enumerate(('Boolean algebra', 'relational algebra', 'the layered model')):
    a(text(206, LY + 22 + k * 20, s, anchor='start', size=13, fill=QSOFT, ls='0'))
H = LY + 22 + 2 * 20 + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-29 svgd-part5-29">')
o.insert(1, '<title id="svgt-part5-29">Fig 18.3 · Three things the next decade will change</title>')
o.insert(2, '<desc id="svgd-part5-29">Classical CPUs and GPUs in the middle, with three new kinds of hardware attaching beside them, not replacing them: specialised chips, as general-purpose speed-ups slow; quantum processors, for a few structured problems; and neuromorphic and analog accelerators, for neural networks. '
  'Below, what fades: RSA and elliptic-curve keys, and ever-faster single threads. What stays: Boolean algebra, relational algebra and the layered model.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The next decade adds hardware beside the classical stack rather than replacing it: chips built for one job, quantum processors for a few structured problems, and accelerators shaped like neural networks. '
           'What changes is the machinery and the keys; the mathematics underneath, from Boolean algebra up, stays.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Specialised chips.</b> As shrinking transistors give less each generation, speed comes from silicon built for one task: tensor units for matrix multiplication, video encoders, network processors.</li>
          <li><b>Quantum.</b> Useful for factoring, simulating molecules and a few other structured problems; that is why public keys are moving to post-quantum algorithms now (Fig 14.13).</li>
          <li><b>What stays.</b> Each of these is still programmed through layers with promises at their boundaries, which is the model this book has followed from the transistor up.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-3">
      <div class="diagram-label">Fig 18.3 · Three things the next decade will change</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-3"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-3', cap, card.replace('CAPID', cap))
