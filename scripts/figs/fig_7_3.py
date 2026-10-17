# Fig 7.3 · Duck typing (Pass 28, law 3). Greenbar paper card. announce(thing) is called with a Duck, a
# Robot, then an int; each time Python looks up speak on the object itself, at the call: quack, BEEP,
# then AttributeError. t=0 (shift): the Duck call, answered.
import figlib
from figlib import Timeline, text, splice, PLEX
figlib.FONT = PLEX

INK, INK_SOFT, GB, AMBER, RED = '#1d2b22', 'rgba(29,43,34,0.62)', '#2e6f52', '#8a5a00', '#b3261e'
BOX = '#f5f8f3'
OBJS = [('class Duck', 'speak()', '"quack"', True), ('class Robot', 'speak()', '"BEEP"', True), ('42, an int', 'no speak', '', False)]
OUT = ['quack', 'BEEP', 'AttributeError']
W, H = 400, 220
CX = [20, 142, 264]; CW = 116
D = 9.0
T = Timeline(D, shift=2.0)
ST = [0.6 + 2.8 * k for k in range(3)]
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-49 svgd-part2-49">')
a('<title id="svgt-part2-49">Fig 7.3 · Duck typing: behaviour, not lineage</title>')
a('<desc id="svgd-part2-49">A function announce(thing) prints thing.speak(). It is called three times. With a Duck, Python finds a speak method on the object and prints quack. '
  'With a Robot, an unrelated class with no shared parent, it finds speak again and prints BEEP. With the integer 42, there is no speak, and the call fails at that moment with AttributeError.</desc>')
a(f'<rect x="20" y="12" width="360" height="54" rx="3" fill="{BOX}" stroke="rgba(29,43,34,0.45)"/>')
a(text(32, 34, 'def announce(thing):', size=13, fill=INK, ls='0'))
a(text(32, 54, '    print(thing.speak())'.replace(' ', '&#160;'), size=13, fill=INK, ls='0'))
for k, out in enumerate(OUT):
    t0 = ST[k] + 1.0; t1 = ST[k + 1] if k < 2 else D - 0.3
    col = RED if k == 2 else GB
    a(f'<g opacity="0">{win(t0, t1)}{text(368, 34, out, anchor="end", size=13, fill=col, ls="0")}</g>')
for k, (l1, l2, l3, ok) in enumerate(OBJS):
    x = CX[k]; cx = x + CW / 2
    a(f'<rect x="{x}" y="96" width="{CW}" height="78" rx="3" fill="{BOX}" stroke="rgba(29,43,34,0.35)"/>')
    a(text(cx, 116, l1, anchor='middle', size=13, fill=INK, ls='0'))
    a(f'<line x1="{x + 8}" y1="126" x2="{x + CW - 8}" y2="126" stroke="rgba(29,43,34,0.12)"/>')
    a(text(cx, 146, l2, anchor='middle', size=13, fill=GB if ok else INK_SOFT, ls='0'))
    if l3: a(text(cx, 164, l3, anchor='middle', size=13, fill=INK_SOFT, ls='0'))
    t0 = ST[k] + 0.5; t1 = ST[k + 1] if k < 2 else D - 0.3
    col = GB if ok else RED
    a(f'<rect class="fx" x="{x + 4}" y="131" width="{CW - 8}" height="{38 if l3 else 22}" rx="2" fill="{col}" fill-opacity="0.15" stroke="{col}" stroke-width="2" opacity="0">{win(t0, t1)}</rect>')
a(text(20, 204, 'no shared parent class, no declared interface', size=13, fill=INK_SOFT, ls='0'))
# thing: the argument, moving across the objects
xs = [x + CW / 2 for x in CX]
pts = [(0.0, 0.0)]
for k in (1, 2):
    pts += [(ST[k] - 0.3, xs[k - 1] - xs[0]), (ST[k], xs[k] - xs[0])]
pts += [(D - 0.4, xs[2] - xs[0]), (D - 0.1, 0.0), (D, 0.0)]
a(f'<g>{T.translate(pts, "x")}<line x1="{xs[0]}" y1="66" x2="{xs[0]}" y2="88" stroke="{AMBER}" stroke-width="2"/>'
  f'<polygon points="{xs[0] - 5},86 {xs[0] + 5},86 {xs[0]},95" fill="{AMBER}"/>{text(xs[0] + 8, 84, "thing", size=13, fill=AMBER, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('<code>announce</code> works on any object that has a <code>speak</code> method: Python looks the name up on the object, at the moment of the call. A Duck and an unrelated Robot both answer; an int has no <code>speak</code>, and the mistake surfaces only when that call runs, as <code>AttributeError</code>.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The strength.</b> Any object with the right method fits, including ones from libraries written after the function was.</li>
          <li><b>The weakness.</b> The contract "must have <code>speak()</code>" is checked by running the code, not by a compiler beforehand.</li>
          <li><b>The middle way.</b> Type hints with <code>typing.Protocol</code> let a checker such as mypy verify the contract before the program runs, without any shared parent class.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-7-3">
      <div class="diagram-label">Fig 7.3 · Duck typing: behaviour, not lineage</div>
      {svg}
      <p id="ch7-types-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-3', 'ch7-types-p4', card)
