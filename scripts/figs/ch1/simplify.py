"""Chapter 1, 2026-11-13 (owner: "simplify ... you don't need to repeat in text what the figure is already saying").
Titles lose the clause that restated the picture. Figs 1.1, 1.2, 1.3 and 1.7, which the owner praised, are not touched.
Idempotent; edits public/part-1.html."""
import re
from plate import PAGE
s = open(PAGE).read()
TITLES = {'fig-1-5': 'Fig 1.5 · Inside the switch', 'fig-1-6': 'Fig 1.6 · Moore\'s Law', 'fig-1-8': 'Fig 1.8 · Von Neumann architecture',
          'fig-1-12': 'Fig 1.12 · Speculative execution', 'fig-1-13': 'Fig 1.13 · Running a program in 1955', 'fig-1-15': 'Fig 1.15 · The hierarchy of forgetting'}
for fid, t in TITLES.items():
    a = s.index(f'id="{fid}"'); a = s.rindex('<div', 0, a); e = s.index('</svg>', a); c = s[a:e]
    c = re.sub(r'(<div class="diagram-label">)[\s\S]*?(</div>)', lambda m: m.group(1) + t.replace(' · ', '&nbsp;· ') + m.group(2), c, count=1)
    c = re.sub(r'(<title id="[^"]+">)[\s\S]*?(</title>)', lambda m: m.group(1) + t + m.group(2), c, count=1)
    s = s[:a] + c + s[e:]
open(PAGE, 'w').write(s); print('chapter 1 titles trimmed')
