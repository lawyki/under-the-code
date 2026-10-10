# Fig 5.5 · a[i] ≡ *(a + i) (Pass 28, law 3). A stepped rewrite beside a memory ribbon: a[2] becomes
# *(a + 2), then *(0x100 + 2 × 4), then *(0x108), then 99, and the cell lights. Run 2: 2[a] reaches the
# same 99, because addition commutes. t=0 (shift): run 1 complete.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

W, H = 400, 268
VALS = ['17', '42', '99', '−7', '23', '8']
CW, RX, RY = 56, 32, 28
D = 12.0
T = Timeline(D, shift=5.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
E1 = [('a[2]', ''), ('= *(a + 2)', 'the definition'), ('= *(0x100 + 2 × 4)', 'scaled by sizeof'), ('= *(0x108)', ''), ('= 99', '')]
E2 = [('2[a]', ''), ('= *(2 + a)', 'same definition'), ('= *(a + 2)', 'addition commutes'), ('= 99', 'legal, never written')]
T1 = [0.6 + 0.8 * k for k in range(len(E1))]; END1 = 6.0
T2 = [6.4 + 0.8 * k for k in range(len(E2))]; END2 = 11.6
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-29 svgd-part2-29">')
a('<title id="svgt-part2-29">Fig 5.5 · a[i] ≡ *(a + i)</title>')
a('<desc id="svgd-part2-29">An int array a at address 0x100 holding 17, 42, 99, −7, 23, 8. The expression a[2] is rewritten step by step: by definition it is *(a + 2); '
  'the addition is scaled by the size of an int, so it is *(0x100 + 2 × 4), which is *(0x108), and the value there is 99. '
  'Then 2[a] is rewritten the same way: *(2 + a), and since addition commutes, *(a + 2), which is again 99.</desc>')
for k, v in enumerate(VALS):
    x = RX + k * CW
    a(f'<rect x="{x}" y="{RY}" width="{CW}" height="34" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
    a(text(x + CW / 2, RY + 22, v, anchor='middle', size=14, fill='#fff', ls='0'))
    a(text(x + CW / 2, RY + 52, f'0x{0x100 + 4 * k:X}', anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(RX, RY - 10, 'int a[6]', size=13, fill=PHOS_SOFT, ls='0'))
hx = RX + 2 * CW
for t0, t1 in ((T1[3], END1), (T2[3], END2)):
    a(f'<rect class="fx" x="{hx}" y="{RY}" width="{CW}" height="34" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}" stroke-width="2.5" opacity="0">{win(t0, t1)}</rect>')
def lines(E, TT, end):
    for k, (expr, note) in enumerate(E):
        y = 120 + k * 30
        col = GOLD if expr.endswith('99') else ('#fff' if k == 0 else PHOS)
        a(f'<g opacity="0">{win(TT[k], end)}{text(36, y, expr, size=15, fill=col, ls="0")}'
          + (text(380, y, note, anchor='end', size=13, fill=MUTED, ls='0') if note else '') + '</g>')
lines(E1, T1, END1)
lines(E2, T2, END2)
a('</svg>')
svg = '\n'.join(o)

caption = ('The C standard defines <code>a[i]</code> as <code>*(a&nbsp;+&nbsp;i)</code>: add <code>i</code> elements to the address, then read what is there. '
           'Because addition commutes, <code>2[a]</code> is the same expression and reads the same 99; arrays in C are a notation over pointer arithmetic.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rule.</b> C99 §6.5.2.1: "<code>E1[E2]</code> is identical to <code>(*((E1)+(E2)))</code>."</li>
          <li><b>The decay.</b> In most expressions an array's name turns into a pointer to its first element, which is why <code>a + 2</code> means an address at all.</li>
          <li><b>The cost.</b> Nothing in <code>*(a + i)</code> knows how long the array is, so <code>a[10]</code> on a six-element array reads whatever lies beyond it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-5">
      <div class="diagram-label">Fig 5.5 · <span class="nocase">a[i] ≡ *(a + i)</span></div>
      {svg}
      <p id="ch5-pointers-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-5', 'ch5-pointers-p6', card)
