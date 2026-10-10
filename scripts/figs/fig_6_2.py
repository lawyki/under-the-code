# Fig 6.2 · C++, in time (Pass 28, law 3). A vertical timeline from Simula 67 to C++23; the axis turns
# from classic to modern at C++11, and a cursor steps through the years. t=0 (shift): the whole line.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

EVENTS = [('1967', 'Simula 67: the first classes'),
          ('1979', 'C with Classes, over C'),
          ('1985', 'C++ 1.0: Cfront, compiles to C'),
          ('1998', 'C++98: ISO standard, the STL'),
          ('2011', 'C++11: move, lambdas, auto'),
          ('2017', 'C++17: structured bindings'),
          ('2020', 'C++20: concepts, modules'),
          ('2023', 'C++23: std::print')]
W = 400
AX = 74
Y0, P = 52, 34
PIVOT = 4
D = 10.0
T = Timeline(D, shift=9.4)
RESET = 0.4
step = lambda i: 0.8 + 0.85 * i
ry = lambda i: Y0 + i * P
o = []; a = o.append
H = ry(len(EVENTS) - 1) + 30
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-38 svgd-part2-38">')
a('<title id="svgt-part2-38">Fig 6.2 · C++, in time</title>')
a('<desc id="svgd-part2-38">A timeline of C++. 1967: Simula 67 introduces classes. 1979: Stroustrup\'s C with Classes, translated into C. 1985: C++ 1.0, whose compiler Cfront produced C. '
  '1998: C++98, the first ISO standard, with the Standard Template Library. 2011: C++11 adds move semantics, lambdas and auto, and the language\'s style turns modern. '
  '2017: C++17 adds structured bindings. 2020: C++20 adds concepts and modules. 2023: C++23 adds std::print.</desc>')
a(text(20, 22, 'C++ style:', size=13, fill=MUTED, ls='0'))
a(f'<rect x="110" y="12" width="12" height="12" rx="2" fill="{GOLD}"/>')
a(text(128, 22, 'classic', size=13, fill=GOLD, ls='0'))
a(f'<rect x="210" y="12" width="12" height="12" rx="2" fill="{PHOS}"/>')
a(text(228, 22, 'modern', size=13, fill=PHOS, ls='0'))
ya, yb, yc = ry(0) - 12, ry(PIVOT), ry(len(EVENTS) - 1) + 8
a(f'<rect x="{AX - 3}" y="{ya}" width="6" height="{yc - ya}" rx="3" fill="rgba(198,222,206,0.12)"/>')
def grow(y_top, y_bot, col, t0, t1):
    h = y_bot - y_top
    a(f'<rect x="{AX - 3}" y="{y_top}" width="6" height="{h}" rx="3" fill="{col}">'
      f'{T.anim("height", [(0.0, h), (RESET, h), (RESET + 0.005, 0.0), (t0, 0.0), (t1, h), (D, h)])}</rect>')
grow(ya, yb, GOLD, step(0), step(PIVOT))
grow(yb, yc, PHOS, step(PIVOT), step(len(EVENTS) - 1) + 0.3)
for i, (yr, ev) in enumerate(EVENTS):
    y = ry(i); t = step(i); hot = i == PIVOT
    dim = T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.3), (t - 0.002, 0.3), (t, 1.0), (D, 1.0)])
    a(f'<g>{dim}')
    a(text(20, y + 5, yr, size=13, fill='#fff' if hot else MUTED, ls='0'))
    a(f'<circle cx="{AX}" cy="{y}" r="{7 if hot else 5}" fill="{PLATE}" stroke="{PHOS if hot else PHOS_SOFT}" stroke-width="{2.5 if hot else 1.5}"/>')
    if hot:
        a(f'<rect x="88" y="{y - 15}" width="292" height="30" rx="3" fill="{PHOS}" fill-opacity="0.16" stroke="{PHOS}"/>')
    a(text(98 if hot else 92, y + 5, ev, size=14 if hot else 13, fill='#fff' if hot else PHOS_SOFT, ls='0'))
    a('</g>')
    a(f'<circle class="fx" cx="{AX}" cy="{y}" r="11" fill="none" stroke="#fff" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (t + 0.6, 0.0), (D, 0.0)])}</circle>')
a('</svg>')
svg = '\n'.join(o)

caption = ('From Simula\'s classes to C++23: Stroustrup\'s C with Classes (1979) became C++, standardised in 1998. '
           'C++11 is the pivot, adding move semantics, lambdas, <code>auto</code> and smart pointers, and every standard since has added more while keeping almost all older code compiling.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The aim.</b> Stroustrup (1993): "C++ was designed to provide Simula's facilities for program organization together with C's efficiency and flexibility for systems programming."</li>
          <li><b>Early compilers.</b> C with Classes and Cfront, the first C++ compiler, translated programs into C, so C++ could run wherever a C compiler did.</li>
          <li><b>The rhythm.</b> Since 2011 a new standard has arrived every three years: 14, 17, 20, 23.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-2">
      <div class="diagram-label">Fig 6.2 · C++, in time</div>
      {svg}
      <p id="ch6-stroustrup-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-2', 'ch6-stroustrup-p4', card)
