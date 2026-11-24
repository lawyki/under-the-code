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

# --- one drawing manner for the five (owner, 2026-11-24: the first redraws were "not understandable by anyone" and
# "look toys"). What the old drawings did right and the first redraws threw away: every box says in plain words what
# it is, what it holds and what happens to it, and a normal case stands against an attack case. Kept here, at a
# size a phone can show: fine lines, square corners, 13-unit type in a 372-wide viewBox, names in small capitals.
FS, SW, RX = 13, 1.2, 2
def cap(x, y, s_, col=MUTE, anchor='start'):
    return text(x, y, s_.upper(), FS, col, anchor, ' letter-spacing="0.08em"')
def run(x, y, parts, anchor='start'):
    """One line of text in several colours: parts = [(words, colour), ...]."""
    spans = ''.join(f'<tspan fill="{c}">{w}</tspan>' for w, c in parts)
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DM Mono" font-size="{FS}" xml:space="preserve">{spans}</text>'
FX, FW, FH = 14, 300, 38                 # a frame row: its name above, what it holds below
def frow(y, name, parts, col, name_col=MUTE):
    return (f'<rect x="{FX}" y="{y}" width="{FW}" height="{FH}" rx="{RX}" fill="none" stroke="{col}" stroke-width="{SW}"/>'
            + cap(FX + 12, y + 15, name, name_col) + run(FX + 12, y + 31, parts))
def verdict(y, question, answer, col):
    return (f'<rect x="{FX}" y="{y}" width="{FW}" height="{FH}" rx="{RX}" fill="none" stroke="{col}" stroke-width="{SW}" stroke-dasharray="5 3"/>'
            + text(FX + 12, y + 15, question, FS, MUTE, 'start') + text(FX + 12, y + 31, answer, FS, col, 'start'))
def upward(y0, y1, words, spans, D):
    """The copy runs up the page: an arrow beside the frame, named along its length."""
    x = FX + FW + 22
    g = (line(f'M {x} {y0} V {y1+8}', RED, 1.3, ' stroke-dasharray="5 4"') + f'<path d="M {x} {y1} l -5 9 h 10 Z" fill="{RED}"/>'
         + f'<text transform="translate({x+20} {(y0+y1)/2}) rotate(90)" text-anchor="middle" font-family="DM Mono" font-size="{FS}" letter-spacing="0.08em" fill="{RED}">{words.upper()}</text>')
    return show(g, spans, D)
