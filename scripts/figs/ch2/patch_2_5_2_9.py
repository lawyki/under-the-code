"""Chapter 2, small changes to two Pass 28 figures whose pictures stay as they are (2026-11-12).
Fig 2.5: the reader starts the addition. It waits unsolved with the press-here mark on the first adder; one press
lets the carry ripple once and the answer stays (data-live="press", data-hold="end"). The line "carries ripple right
to left" inside the picture goes: the caption says it.
Fig 2.9: three step buttons (data-beats), so each of the bug's three moments can be held.
Idempotent; edits public/part-1.html in place."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE, hint
s = open(PAGE).read()
def svg_tag(fid):
    a = s.index(f'id="{fid}"'); m = re.compile(r'<svg\b[^>]*>').search(s, a); return m
# --- Fig 2.5
m = svg_tag('fig-2-5')
if 'data-live' not in m.group(0):
    s = s[:m.end()-1] + ' data-live="press" data-rest="1.1" data-run="1.1 5.2" data-hold="end" data-press-label="Add 5 and 3">' + s[m.end():]
a = s.index('id="fig-2-5"'); e = s.index('</svg>', a)
seg = s[a:e]
seg = re.sub(r'<text[^>]*>carries ripple right to left</text>\n?', '', seg)
if 'fig-hint' not in seg: seg = seg + hint(358, 164) + '\n'
s = s[:a] + seg.replace('viewBox="0 0 400 300"', 'viewBox="0 0 400 258"') + s[e:]
open(PAGE, 'w').write(s); print('patched 2.5')
