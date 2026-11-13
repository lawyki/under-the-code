"""Chapter 2, small fixes to Pass 28 figures, each confirmed by the 2026-11-12 screenshot scan and then by eye.
The pictures stay; one fault each goes. Idempotent; edits public/part-1.html in place.
(2.9 to 2.12 were redrawn on 2026-11-13, fig_2_9.py to fig_2_12.py; only the 2.7 fix is still applied here.)
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
open(PAGE, 'w').write(s); print('patched 2.7')
