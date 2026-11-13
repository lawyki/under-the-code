"""Fig 2.9: one pattern of bits, read two ways. Redrawn 2026-11-13 (was a column of text in three numbered steps).
Eight ones. The check reads them with a sign: −1, and lets them pass. The copy reads them without: 255, and runs
out of the buffer. Eight bits stand for the 32 or 64 of a real length (the strip says so)."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 7.0
k = lambda t: t / D
b = []
for i in range(8):
    x = 110 + i * 20
    b.append(f'<circle cx="{x}" cy="52" r="8" fill="{GOLD}"/>' + text(x, 57, '1', 13, '#1a1408'))
b.append(show(text(52, 46, 'check', 13, GREEN) + text(52, 68, '−1', 19, GREEN), [(0.9, D)], D))
b.append(show(text(308, 46, 'copy', 13, RED) + text(308, 68, '255', 19, RED), [(2.2, D)], D))
# memory: the buffer and what lies after it
for i, (x, w) in enumerate(((40, 70), (114, 70), (188, 70), (262, 70))):
    b.append(f'<rect x="{x}" y="112" width="{w}" height="34" rx="4" fill="none" stroke="{INK}" stroke-opacity="{0.9 if i == 0 else 0.45}" stroke-width="1.6"/>')
b.append(text(75, 134, 'buffer', 14, INK))
# the copy: starts at the buffer and does not stop at its end
b.append(f'<path d="M 40 164 H 352" fill="none" stroke="{RED}" stroke-width="5" stroke-linecap="round" stroke-dasharray="312 312">'
         + anim('stroke-dashoffset', [312, 312, 0, 0], [0, k(3.2), k(5.4), 1], D) + '</path>')
b.append(show(f'<path d="M 362 164 l -12 -8 v 16 Z" fill="{RED}"/>', [(5.4, D)], D))
put('fig-2-9', '10 20 360 162', None, None,
    'Fig 2.9 · A signed length becomes a buffer overflow',
    'A row of eight bits, all ones. To the left, in green, how the length check reads them, with a sign: −1, small enough to pass. To the right, in red, how the copy reads the same bits, without a sign: 255. Below, a row of memory: a buffer and the cells after it. A red line, the copy, starts at the beginning of the buffer, runs past its end and on across everything after it.',
    b,
    caption='One pattern of bits, read two ways.',
    strip=[('The check', 'The length is a signed number, so all ones is −1 (Fig 2.8). −1 is not more than the buffer holds, and the check lets it through.'),
           ('Read as unsigned', 'The copying code takes its length as unsigned. The picture shows eight bits; a real length is widened to 64, and 64 ones read as unsigned are 2<sup>64</sup> − 1.'),
           ('The write', 'The copy overruns the buffer and smashes whatever lies after it, the start of the memory-corruption attacks of Chapter 3.'),
           ('The fix', 'Use an unsigned type for sizes, or check for a negative length as well as one that is too big.')])
