"""Part I plate helpers for hand-built figures (Chapter 1, round four).
A figure is a list of SVG strings; put() swaps it into public/part-1.html by card id."""
import re, sys
PAGE = '/home/user/under-the-code/public/part-1.html'
INK = '#e8e8e8'; MUTE = 'rgba(255,255,255,0.6)'; GOLD = '#d4a853'; BLUE = '#86a8ff'; RED = '#e2725b'; GREEN = '#7fc98f'; DARK = '#1a1a1a'
FONT = 'DM Mono'

def kt(xs): return ';'.join('%.4f' % x for x in xs)
def anim(attr, values, keytimes, dur, discrete=False, extra=''):
    return (f'<animate attributeName="{attr}" values="{";".join(str(v) for v in values)}" keyTimes="{kt(keytimes)}" '
            + ('calcMode="discrete" ' if discrete else '') + f'dur="{dur}s" repeatCount="indefinite"{extra}/>')
def xform(kind, values, keytimes, dur, additive=False):
    return (f'<animateTransform attributeName="transform" type="{kind}" values="{";".join(values)}" keyTimes="{kt(keytimes)}" '
            + ('additive="sum" ' if additive else '') + f'dur="{dur}s" repeatCount="indefinite"/>')
def show(inner, spans, dur):
    """Visible only inside the [start, end) spans (seconds) of a dur-second loop."""
    ks = [0.0]; vs = [0]
    for a, b in spans:
        if a <= 0: vs[0] = 1
        else: ks.append(a / dur); vs.append(1)
        if b < dur: ks.append(b / dur); vs.append(0)
    return f'<g opacity="{vs[0]}">{anim("opacity", vs, ks, dur, discrete=True)}{inner}</g>'
def line(d, stroke=INK, w=2, extra=''):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{extra}/>'
def text(x, y, s, size=14, fill=MUTE, anchor='middle', extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" fill="{fill}"{extra}>{s}</text>'

def hint(x, y):
    """The press-here mark (owner, 2026-11-12: a small modern pointer with a small animation, 'a pattern, not an
    exception'): a ring on the thing to press and a pointer whose tip is on it. book.css moves it (.fig-hint)
    and shows it only while the figure waits (card class is-armed, set by live-figures.js)."""
    return (f'<g class="fig-hint" transform="translate({x} {y})">'
            f'<circle class="fig-hint-ring" r="11" fill="none" stroke="{GOLD}" stroke-width="1.8"/>'
            f'<g class="fig-hint-cursor"><path d="M 0 0 V 18 L 4.9 13.8 L 8.2 21 L 11.4 19.5 L 8.2 12.5 L 14.4 12.3 Z" fill="#fff" stroke="{GOLD}" stroke-width="1.5" stroke-linejoin="round"/></g></g>')

def put(fig_id, viewbox, beats, names, title, desc, body, caption=None, strip=None, label=None, attrs=''):
    s = open(PAGE).read()
    a = s.index(f'id="{fig_id}"'); a = s.rindex('<div', 0, a)
    m = re.compile(r'<svg\b[^>]*>[\s\S]*?</svg>').search(s, a); assert m
    head = m.group(0)[:m.group(0).index('>') + 1]
    tid = re.search(r'aria-labelledby="(\S+) (\S+)"', head)
    new_head = (f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{tid.group(1)} {tid.group(2)}"'
                + (f' data-beats="{" ".join(str(b) for b in beats)}" data-beat-names="{"|".join(names)}"' if beats else '') + (' ' + attrs if attrs else '') + '>')
    svg = new_head + f'\n<title id="{tid.group(1)}">{title}</title>\n<desc id="{tid.group(2)}">{desc}</desc>\n' + '\n'.join(body) + '\n</svg>'
    s = s[:m.start()] + svg + s[m.end():]
    end = s.index('</details>', a)
    if label:
        lm = re.compile(r'<div class="diagram-label">[\s\S]*?</div>').search(s, a); s = s[:lm.start()] + f'<div class="diagram-label">{label}</div>' + s[lm.end():]
    if caption:
        cm = re.compile(r'(<p id="[^"]+" class="diagram-caption">)[\s\S]*?</p>').search(s, a); assert cm.start() < s.index('</details>', a)
        s = s[:cm.start()] + cm.group(1) + caption + '</p>' + s[cm.end():]
    if strip:
        om = re.compile(r'<ol>[\s\S]*?</ol>').search(s, a); assert om.start() < s.index('</details>', a)
        items = '\n'.join(f'          <li><b>{h}.</b> {t}</li>' for h, t in strip)
        s = s[:om.start()] + '<ol>\n' + items + '\n        </ol>' + s[om.end():]
    open(PAGE, 'w').write(s); print('put', fig_id, len(svg))
