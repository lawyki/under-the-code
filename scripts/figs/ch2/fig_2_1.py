"""Fig 2.1: why binary survives noise. The Pass 28 figure, kept: two gauges, two steps (a little noise, a lot).
One fault fixed: the read row showed ternary's wrong +1, boxed in red, even while the level was nowhere near its
threshold. The digit and its box now follow the level: 0 in gold until it crosses, +1 in red while it is over.
(A noise slider with continuous shaking stood here for a few hours on 2026-11-12 and was taken out again, owner:
"do not replace a working simple figure with a complex one".)
Idempotent: takes the card from origin/main and applies the fix."""
import re, subprocess, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
old = subprocess.run(['git', 'show', 'origin/main:public/part-1.html'], capture_output=True, text=True, check=True, cwd=PAGE.rsplit('/', 2)[0]).stdout
def card_span(t):
    a = t.index('id="fig-2-1"'); a = t.rindex('<div', 0, a); return a, t.index('</details>', a) + len('</details>')
a, e = card_span(old); card = old[a:e]
m = re.search(r'<rect x="277" y="55.0" width="82" height="59.0" fill="none" stroke="#ec8d8d" stroke-width="2.4"><animate attributeName="opacity" values="([^"]*)" keyTimes="([^"]*)"', card)
on, kt = m.group(1).split(';'), m.group(2)
off = ['%.1f' % (1 - float(v)) for v in on]
anim = lambda vs: f'<animate attributeName="opacity" values="{";".join(vs)}" keyTimes="{kt}" calcMode="discrete" dur="6s" repeatCount="indefinite"/>'
T = '<text x="348" y="340" text-anchor="middle" font-family="DM Mono" font-size="15" letter-spacing="0" fill="%s" opacity="%s">%s%s</text>'
R = '<rect x="331.0" y="294" width="34" height="56" rx="5" fill="none" stroke="%s" stroke-width="1.6" opacity="%s">%s</rect>'
txt = '<text x="348" y="340" text-anchor="middle" font-family="DM Mono" font-size="15" letter-spacing="0" fill="#ec8d8d">+1</text>'
box = '<rect x="331.0" y="294" width="34" height="56" rx="5" fill="none" stroke="#ec8d8d" stroke-width="1.6"/>'
assert txt in card and box in card
card = card.replace(txt, T % ('#ece6da', off[0], '0', anim(off)) + T % ('#ec8d8d', on[0], '+1', anim(on)))
card = card.replace(box, R % ('#d4a853', off[0], anim(off)) + R % ('#ec8d8d', on[0], anim(on)))
card = card.replace('binary\'s level stays in its band, ternary\'s crosses a threshold and the 0 is read as +1.', 'binary\'s level stays in its band, ternary\'s crosses a threshold and, while it is over, the 0 is read as +1 and boxed in red.')
s = open(PAGE).read(); a, e = card_span(s)
open(PAGE, 'w').write(s[:a] + card + s[e:]); print('fig-2-1 restored, read row follows the level')
