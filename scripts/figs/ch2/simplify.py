"""Chapter 2, 2026-11-13. Owner: "now just simplify most of them. You don't need to repeat in text what the figure
is already saying." Idempotent; edits public/part-1.html.
- 2.3, 2.4, 2.6: the row of cases drawn under the picture said what the step buttons under it already say: gone.
  2.3, 2.4: so are "A and B", "A or B" and "not A" beside gates already named AND, OR and NOT.
- titles: the third clause, which restated the picture, is cut.
- captions: what the picture cannot say for itself, or a few words."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
s = open(PAGE).read()
def span(fid):
    a = s.index(f'id="{fid}"'); a = s.rindex('<div', 0, a); return a, s.index('</details>', a)
def edit(fid, fn):
    global s
    a, e = span(fid); s = s[:a] + fn(s[a:e]) + s[e:]
def drop_row(text_y, rect_y, old_vb, new_vb):
    def fn(c):
        c = re.sub(r'<text[^>]* y="%s"[^>]*>(?:<animate[^>]*/>)?[^<]*</text>\n?' % text_y, '', c)
        c = re.sub(r'<rect[^>]* y="%s"[^>]*(?:/>|>(?:<animate[^>]*/>)*</rect>)\n?' % rect_y, '', c)
        return c.replace(f'viewBox="{old_vb}"', f'viewBox="{new_vb}"')
    return fn
edit('fig-2-3', drop_row('327', '307', '0 0 400 352', '0 0 400 296'))
edit('fig-2-4', drop_row('349', '329', '0 0 400 392', '0 0 400 326'))
edit('fig-2-6', drop_row('335', '316', '0 0 400 352', '0 0 400 296'))
def drop_names(c):                       # "A and B" beside the gate named AND, and so on: the row already carries its name
    return re.sub(r'<text[^>]*>(?:A and B|A or B|not A)</text>\n?', '', c)
edit('fig-2-3', drop_names); edit('fig-2-4', drop_names)
TITLES = {'fig-2-1': 'Fig 2.1 · Why binary survives noise', 'fig-2-2': 'Fig 2.2 · Boole\'s algebra · Shannon\'s switches', 'fig-2-3': 'Fig 2.3 · AND, OR, NOT',
          'fig-2-4': 'Fig 2.4 · Everything from NAND', 'fig-2-5': 'Fig 2.5 · Adding 5 + 3 in binary', 'fig-2-6': 'Fig 2.6 · Inside a full adder',
          'fig-2-7': 'Fig 2.7 · 7 − 5 with two\'s complement', 'fig-2-8': 'Fig 2.8 · The two\'s-complement wheel', 'fig-2-9': 'Fig 2.9 · A signed length becomes a buffer overflow',
          'fig-2-10': 'Fig 2.10 · A floating-point number', 'fig-2-11': 'Fig 2.11 · 0.1 + 0.2', 'fig-2-12': 'Fig 2.12 · The Patriot\'s clock'}
CAPS = {'fig-2-1': 'Each lamp is a voltage level; the flicker is noise.',
        'fig-2-2': 'The same AND, in algebra and in wire.',
        'fig-2-3': 'The three gates, in every case of their inputs.',
        'fig-2-4': 'NOT, AND and OR, each wired from NAND gates alone.',
        'fig-2-5': 'The carry ripples left, so the answer settles one bit at a time.',
        'fig-2-6': 'Two half adders and an OR.'}
def retitle(fid):
    def fn(c):
        c = re.sub(r'(<div class="diagram-label">)[\s\S]*?(</div>)', lambda m: m.group(1) + TITLES[fid].replace(' · ', '&nbsp;· ') + m.group(2), c, count=1)
        c = re.sub(r'(<title id="[^"]+">)[\s\S]*?(</title>)', lambda m: m.group(1) + TITLES[fid] + m.group(2), c, count=1)
        if fid in CAPS: c = re.sub(r'(<p id="[^"]+" class="diagram-caption">)[\s\S]*?(</p>)', lambda m: m.group(1) + CAPS[fid] + m.group(2), c, count=1)
        return c
    return fn
for fid in TITLES: edit(fid, retitle(fid))
open(PAGE, 'w').write(s); print('chapter 2 simplified: rows, titles, captions')
