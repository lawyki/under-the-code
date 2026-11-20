"""Chapter 3 and the Bridge, 2026-11-13 (owner: "simplify ... you don't need to repeat in text what the figure is
already saying"). Idempotent; edits public/part-1.html. Figs 3.7 to 3.11 (kept originals) are not touched.
- Fig 3.1: the three colour chips above the picture said what the three step buttons under it say, and the line of
  hex under each row repeated the row: both gone.
- Titles lose the clause that restated the picture.
- Fig 3.3: the years beside the three names move to the strip. Fig BR.7: the note under the picture moves to the strip."""
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
def fig33(c):                            # the years beside the three names: history, moved to the strip
    for name, year in (('RAX', '2003'), ('EAX', '1985'), ('AX', '1978')): c = c.replace(f'>{name} · {year}</text>', f'>{name}</text>')
    return c.replace('<li><b>The names.</b> The 8086 had 16-bit AX, BX, CX, DX; 32-bit chips added an E for extended;', '<li><b>The names.</b> The 8086 of 1978 had 16-bit AX, BX, CX, DX; 32-bit chips, from 1985, added an E for extended;')
edit('fig-3-3', fig33)
def figbr7(c):                           # the note under the picture: moved to the strip
    note = '<text x="20" y="374" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0" fill="rgba(255,255,255,0.6)">low addresses at the bottom, not to scale</text>'
    if note in c:
        c = c.replace(note + '\n', '').replace(note, '').replace('viewBox="0 0 400 384"', 'viewBox="0 0 400 356"')
        c = c.replace('<li><b>Who routes it.</b>', '<li><b>The map.</b> Low addresses are at the bottom; the regions are not drawn to scale.</li>\n          <li><b>Who routes it.</b>')
    return c
edit('fig-br-7', figbr7)
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
CAPS = {'fig-3-3': 'A 32-bit write clears the upper half.',                 # the title already says "one register, five names"
        'fig-br-2': 'One write call, time running down.'}
for fid, cap in CAPS.items():
    edit(fid, lambda c, cap=cap: re.sub(r'(<p id="[^"]+" class="diagram-caption">)[\s\S]*?(</p>)', lambda m: m.group(1) + cap + m.group(2), c, count=1))
open(PAGE, 'w').write(s); print('chapter 3 and bridge: 3.1 trimmed, titles')
