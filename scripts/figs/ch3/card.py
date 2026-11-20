"""Chapter 3, Figs 3.7 to 3.11 (2026-11-20). They were the 18 kept originals' first five: desktop drawings scaled to
4 to 6 px on a phone, with known errors (docs/audit/owner-calls.md, Chapter 3). Owner, 2026-11-20: "fix errors and
simplify the one's. I have repeatedly only given two rules: understandable & simple."
card() replaces a whole card, old form or new, keeping the card id and the caption's anchor id."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE, kt, anim, xform, show, line, text
INK = '#ece6da'; MUTE = 'rgba(255,255,255,0.6)'; GOLD = '#d4a853'; BLUE = '#86a8ff'; GREEN = '#9bd89b'; RED = '#ec8d8d'    # Figs 3.5 and 3.6's palette

def card(fig_id, n, cap_id, viewbox, title, desc, body, caption, strip, beats=None, names=None):
    s = open(PAGE).read()
    a = s.index(f'<div class="diagram-card', s.index(f'id="{fig_id}"') - 60)
    cm = re.compile(r'<p id="%s" class="diagram-caption">[\s\S]*?</p>' % cap_id).search(s, a)
    e = cm.end()
    dm = re.compile(r'\s*<details class="fig-how">[\s\S]*?</details>').match(s, e)
    if dm: e = dm.end()
    e = s.index('</div>', e) + len('</div>')
    steps = f' data-beats="{" ".join(str(b) for b in beats)}" data-beat-names="{"|".join(names)}"' if beats else ''
    items = '\n'.join(f'          <li><b>{h}.</b> {t}</li>' for h, t in strip)
    new = f'''<div class="diagram-card fig-v2" id="{fig_id}">
      <div class="diagram-label">{title.replace(' · ', '&nbsp;· ')}</div>
      <svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-{n} svgd-part1-{n}"{steps}>
<title id="svgt-part1-{n}">{title}</title>
<desc id="svgd-part1-{n}">{desc}</desc>
{chr(10).join(body)}
</svg>
      <p id="{cap_id}" class="diagram-caption">{caption}</p>
      <details class="fig-how">
        <summary>How it works</summary>
        <ol>
{items}
        </ol>
      </details>
    </div>'''
    open(PAGE, 'w').write(s[:a] + new + s[e:]); print('card', fig_id, len(new))

# --- the stack frame of greet(), drawn as Fig 3.6 draws a stack: highest address at the top
X0, CW, RH = 22, 26, 30                 # eight byte cells to a row
def row(y, col, spans, D, w=1.6):
    r = f'<rect x="{X0}" y="{y}" width="{8*CW}" height="{RH}" rx="5" fill="none" stroke="{col}" stroke-width="{w}"/>'
    return show(r, spans, D) if spans else r
def cells(y):
    return ''.join(line(f'M {X0+i*CW} {y+4} V {y+RH-4}', INK, 1, ' stroke-opacity="0.45"') for i in range(1, 8))
def letter(i, y, ch, col, size=14): return text(X0 + i * CW + CW / 2, y + 20, ch, size, col)
