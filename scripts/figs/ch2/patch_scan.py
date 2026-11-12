"""Chapter 2, small fixes to Pass 28 figures, each confirmed by the 2026-11-12 screenshot scan and then by eye.
The pictures stay; one fault each goes. Idempotent; edits public/part-1.html in place.
2.7  "ninth bit" stood under nothing until the bit appeared: it now appears with the bit.
2.9  "no, so on" reads as a slip: "no: it passes".
2.10 nothing tied the stored mantissa to the digits in the boxes: the mantissa's digits are gold like their field,
     the hidden leading 1 sits in a dashed box, and the exponent line gives its result (= 2, = −1).
2.11 the rule over 5.6 × 10⁻¹⁷ measured nothing and the exponent was unreadably small: a bracket from the stored
     0.3 to the rounded sum, the exponent at label size.
2.12 "0.34 s" stood while the error was still 0: it shows when the error gets there; "window" moves with its box."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
s = open(PAGE).read()
def card(fid):
    a = s.index(f'id="{fid}"'); return a, s.index('</svg>', a)
def sub(fid, old, new, count=1):
    global s
    a, e = card(fid); c = s[a:e]
    if new in c and old not in c: return
    assert c.count(old) >= 1, (fid, old[:60])
    s = s[:a] + c.replace(old, new, count) + s[e:]
# 2.7
lab = '<text x="36" y="262" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#ec8d8d">ninth bit</text>'
sub('fig-2-7', lab, '<g opacity="0"><animate attributeName="opacity" values="1;0;0;1" keyTimes="0.000000;0.166611;0.166667;0.722222" calcMode="discrete" dur="9s" repeatCount="indefinite"/>' + lab + '</g>')
# 2.9
sub('fig-2-9', '>no, so on<', '>no: it passes<')
# 2.10
sub('fig-2-10', 'exponent 1025 − 1023</text>', 'exponent 1025 − 1023 = 2</text>')
sub('fig-2-10', 'exponent 1022 − 1023</text>', 'exponent 1022 − 1023 = −1</text>')
def box(x, d, kind):
    plain = f'<rect x="{x}" y="206" width="34" height="44" rx="5" fill="none" stroke="rgba(255,255,255,0.42)"/><text data-role="object" x="{x+17}" y="236" text-anchor="middle" font-family="DM Mono" font-size="20" letter-spacing="0" fill="#ece6da">{d}</text>'
    if kind == 'mantissa': new = f'<rect x="{x}" y="206" width="34" height="44" rx="5" fill="none" stroke="#d4a853" stroke-width="1.5"/><text data-role="object" x="{x+17}" y="236" text-anchor="middle" font-family="DM Mono" font-size="20" letter-spacing="0" fill="#d4a853">{d}</text>'
    else: new = f'<rect x="{x}" y="206" width="34" height="44" rx="5" fill="none" stroke="rgba(255,255,255,0.6)" stroke-dasharray="4 3"/><text data-role="object" x="{x+17}" y="236" text-anchor="middle" font-family="DM Mono" font-size="20" letter-spacing="0" fill="#ece6da">{d}</text>'
    return plain, new
a, e = card('fig-2-10'); c = s[a:e]
g1 = c.index('<rect x="112" y="206"'); g2 = c.index('<rect x="66" y="206"')          # 6.5's row, then −0.75's row
row1, row2 = c[g1:g2], c[g2:]
for x, d, kind in ((112, '1', 'hidden'), (158, '1', 'mantissa'), (204, '0', 'mantissa'), (250, '1', 'mantissa')):
    p, n = box(x, d, kind)
    if p in row1: row1 = row1.replace(p, n, 1)
for x, d, kind in ((112, '1', 'hidden'), (158, '1', 'mantissa')):
    p, n = box(x, d, kind)
    if p in row2: row2 = row2.replace(p, n, 1)
s = s[:a] + c[:g1] + row1 + row2 + s[e:]
# 2.11
sub('fig-2-11', '<path d="M 170 276 H 250" stroke="rgba(255,255,255,0.6)"/>', '<path d="M 160 269 V 276 H 260 V 269" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>')
sub('fig-2-11', '>5.6 × 10⁻¹⁷</text>', '>5.6 × 10<tspan dy="-6" font-size="13">−17</tspan></text>')
# 2.12
old = '<text x="350" y="48" text-anchor="end" font-family="DM Mono" font-size="16" letter-spacing="0.06em" fill="#ec8d8d">0.34 s</text>'
sub('fig-2-12', old, '<g opacity="1"><animate attributeName="opacity" values="1;0;1" keyTimes="0.000000;0.122222;0.911111" calcMode="discrete" dur="9s" repeatCount="indefinite"/>' + old + '</g>')
a, e = card('fig-2-12'); c = s[a:e]
win = '<text x="144" y="322" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#86a8ff">window</text>'
if win in c:
    c = c.replace(win, '')
    boxr = '<rect x="310" y="256" width="68" height="48" rx="6" fill="none" stroke="#86a8ff" stroke-width="2"/>'
    assert boxr in c
    c = c.replace(boxr, boxr + '<text x="344" y="342" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#86a8ff">window</text>')
    s = s[:a] + c + s[e:]
open(PAGE, 'w').write(s); print('patched 2.7 2.9 2.10 2.11 2.12')
