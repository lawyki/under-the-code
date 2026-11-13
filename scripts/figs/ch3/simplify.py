"""Chapter 3 and the Bridge, 2026-11-13 (owner: "simplify ... you don't need to repeat in text what the figure is
already saying"). Idempotent; edits public/part-1.html. Figs 3.7 to 3.11 (kept originals) are not touched.
- Fig 3.1: the three colour chips above the picture said what the three step buttons under it say, and the line of
  hex under each row repeated the row: both gone.
- Titles lose the clause that restated the picture."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
s = open(PAGE).read()
def edit(fid, fn):
    global s
    a = s.index(f'id="{fid}"'); a = s.rindex('<div', 0, a); e = s.index('</details>', a); s = s[:a] + fn(s[a:e]) + s[e:]
def fig31(c):
    c = re.sub(r'<rect x="(?:24|140|262)" y="18" width="16" height="16"[^>]*/>\n?', '', c)
    c = re.sub(r'<text x="(?:48|164|286)" y="31"[^>]*>(?:opcode|register|the 5)</text>\n?', '', c)
    c = re.sub(r'<rect x="(?:18|134|256)" y="12"[^>]*>(?:<animate[^>]*/>)*</rect>\n?', '', c)
    c = re.sub(r'<text x="376" y="\d+" text-anchor="end"[^>]*>(?:48 83 C0 05|0x91001400|0x00550513)</text>\n?', '', c)
    return c.replace('viewBox="0 0 400 372"', 'viewBox="0 52 400 276"')
edit('fig-3-1', fig31)
TITLES = {'fig-3-1': 'Fig 3.1 · One operation, three encodings', 'fig-3-2': 'Fig 3.2 · Rosetta 2', 'fig-3-3': 'Fig 3.3 · One register, five names',
          'fig-3-4': 'Fig 3.4 · Which register holds which argument',
          'fig-br-1': 'Fig BR.1 · The privilege bit', 'fig-br-2': 'Fig BR.2 · The trap mechanism', 'fig-br-3': 'Fig BR.3 · The interrupt descriptor table',
          'fig-br-4': 'Fig BR.4 · The MMU', 'fig-br-5': 'Fig BR.5 · The TLB', 'fig-br-6': 'Fig BR.6 · The timer interrupt',
          'fig-br-7': 'Fig BR.7 · Devices among the RAM', 'fig-br-8': 'Fig BR.8 · Direct memory access'}
def retitle(fid):
    def fn(c):
        c = re.sub(r'(<div class="diagram-label">)[\s\S]*?(</div>)', lambda m: m.group(1) + TITLES[fid].replace(' · ', '&nbsp;· ') + m.group(2), c, count=1)
        return re.sub(r'(<title id="[^"]+">)[\s\S]*?(</title>)', lambda m: m.group(1) + TITLES[fid] + m.group(2), c, count=1)
    return fn
for fid in TITLES: edit(fid, retitle(fid))
open(PAGE, 'w').write(s); print('chapter 3 and bridge: 3.1 trimmed, titles')
