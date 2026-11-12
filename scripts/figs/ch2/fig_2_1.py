"""Fig 2.1: why binary survives noise, with the noise in the reader's hand (data-live="noise").
The Pass 28 picture is kept: two gauges of the same height, binary with one threshold, ternary with two, both
sending 0 as their fourth digit. New: a slider sets how much noise shakes both levels. Ternary's level crosses its
threshold and its 0 is read as +1 while binary's stays in its band. (Before, the wrong +1 stood in the read row
even while the level was nowhere near the threshold.)"""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
CREAM = '#ece6da'; BAD = '#ec8d8d'
b = []
def gauge(x, name, levels, thresholds, rail):
    b.append(text(x + 42, 40, name, 15, CREAM, 'middle', ' letter-spacing="0.06em"'))
    b.append(f'<rect x="{x}" y="54" width="84" height="220" rx="5" fill="none" stroke="rgba(255,255,255,0.42)" stroke-width="1.4"/>')
    for lab, y in levels: b.append(text(x - 10, y, lab, 14, MUTE, 'end'))
    for y in thresholds: b.append(f'<line x1="{x}" y1="{y}" x2="{x+84}" y2="{y}" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    b.append(f'<line x1="{x+8}" y1="{rail}" x2="{x+76}" y2="{rail}" stroke="{BLUE}" stroke-width="1.5" opacity="0.6"/>')
def digits(x0, sent, read, k, cls):
    for i, (s_, r_) in enumerate(zip(sent, read)):
        x = x0 + i * 30
        b.append(text(x, 312, s_, 14, MUTE))
        if i == k: b.append(text(x, 340, r_, 15, CREAM, 'middle', f' class="{cls}"'))
        else: b.append(text(x, 340, r_, 15, CREAM))
# binary
gauge(66, 'binary', [('0', 219), ('1', 119)], [164], 264)
b.append(f'<g class="lv-dot"><circle cx="108" cy="264" r="7" fill="{BLUE}" stroke="#111" stroke-width="1.5"/></g>')
digits(48, ['0', '1', '1', '0', '1'], ['0', '1', '1', '0', '1'], 3, 'lv-read-b')
b.append(f'<rect x="121" y="294" width="34" height="56" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
# ternary
gauge(276, 'ternary', [('−1', 244), ('0', 169), ('+1', 94)], [214, 114], 164)
b.append(f'<rect class="lv-bad" x="277" y="55" width="82" height="59" fill="none" stroke="{BAD}" stroke-width="2.4" opacity="0"/>')
b.append(f'<g class="lv-dot"><circle cx="318" cy="164" r="7" fill="{BLUE}" stroke="#111" stroke-width="1.5"/></g>')
digits(258, ['0', '+1', '−1', '0', '+1'], ['0', '+1', '−1', '0', '+1'], 3, 'lv-read-t')
b.append(f'<rect class="lv-ok" x="331" y="294" width="34" height="56" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
b.append(f'<rect class="lv-bad" x="331" y="294" width="34" height="56" rx="5" fill="none" stroke="{BAD}" stroke-width="1.6" opacity="0"/>')
# the noise, as big as the slider says (the script draws the arrow to that height)
b.append(f'<path class="lv-arrow" d="M 200 164 V 164" fill="none" stroke="{CREAM}" stroke-width="1.6" opacity="0"/>')
b.append(text(200, 186, 'same', 14, CREAM, 'middle', ' letter-spacing="0.06em"') + text(200, 203, 'noise', 14, CREAM, 'middle', ' letter-spacing="0.06em"'))
b.append(text(213, 312, 'sent', 14, MUTE, 'middle', ' letter-spacing="0.06em"') + text(213, 340, 'read', 14, MUTE, 'middle', ' letter-spacing="0.06em"'))
put('fig-2-1', '0 0 400 362', None, None,
    'Fig 2.1 · Why binary survives noise · one threshold against two',
    'Two wires with the same voltage span, drawn as two gauges of the same height. The binary wire has one threshold and two wide bands; the ternary wire squeezes three levels into the same span with two thresholds. Both send 0 as their fourth digit. A slider under the picture sets how much noise shakes both levels, by the same amount. With little noise both digits are read correctly. With more, the ternary level crosses its upper threshold and its 0 is read as +1, shown in red, while the binary level, shaken just as much, stays inside its band and is still read as 0. Binary reads all five bits 0 1 1 0 1 right.',
    b,
    attrs='data-live="noise"')
