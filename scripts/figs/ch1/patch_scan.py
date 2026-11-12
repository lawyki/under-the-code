"""Chapter 1, small fixes confirmed by the 2026-11-12 screenshot scan (idempotent, edits public/part-1.html).
Fig 1.12: the cross and the tick sat on the branch stems, so the line showed through each mark (the fault the
owner pointed at on the loop's arrows). They now stand beside their stems."""
from plate import PAGE
s = open(PAGE).read()
a = s.index('id="fig-1-12"'); e = s.index('</svg>', a); c = s[a:e]
c = c.replace('M 121 58 l 14 14 M 135 58 l -14 14', 'M 98 58 l 14 14 M 112 58 l -14 14').replace('M 264 66 l 5 6 l 11 -13', 'M 284 66 l 5 6 l 11 -13')
open(PAGE, 'w').write(s[:a] + c + s[e:]); print('patched 1.12')
