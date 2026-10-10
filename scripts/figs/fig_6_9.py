# Fig 6.9 · C++ standards (Pass 28, law 3). One task, summing a vector, in three eras: an explicit
# iterator loop (C++98), a range-for (C++11), a fold with no loop (C++23). A highlight steps through
# the eras and lights each one's standard on a strip of all seven. t=0: all three shown, C++98 lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

ERAS = [('C++98', ['int total = 0;', 'for (vector&lt;int&gt;::iterator i = v.begin();', '     i != v.end(); ++i) total += *i;'], GOLD),
        ('C++11', ['int total = 0;', 'for (int x : v) total += x;'], BLUE),
        ('C++23', ['auto total = std::ranges::fold_left(', '    v, 0, std::plus{});'], PHOS)]
STDS = ['98', '03', '11', '14', '17', '20', '23']
W = 400
D = 9.0
T = Timeline(D, shift=0.0)
SPAN = [(0.0, 3.0), (3.0, 6.0), (6.0, D)]
def during(k):
    t0, t1 = SPAN[k]
    if t0 == 0.0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)])
    if t1 == D:
        return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; body = []; b = body.append
b(text(20, 22, 'one task, three eras: add up a vector', size=13, fill=MUTED, ls='0'))
y = 34
for k, (std, lines, col) in enumerate(ERAS):
    h = 12 + len(lines) * 20
    b(f'<rect x="20" y="{y}" width="360" height="{h}" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.5"/>')
    b(f'<rect class="fx" x="20" y="{y}" width="360" height="{h}" rx="3" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-width="2.2" opacity="0">{during(k)}</rect>')
    b(text(368, y + 18, std, anchor='end', size=13, fill=col, ls='0'))
    for i, l in enumerate(lines):
        b(text(30, y + 20 + i * 20, l.replace(' ', '&#160;'), size=13, fill='#fff', ls='0'))
    y += h + 10
SY = y + 8
b(text(20, SY, 'the standards', size=13, fill=MUTED, ls='0'))
for i, s in enumerate(STDS):
    x = 20 + i * 52
    b(f'<rect x="{x}" y="{SY + 10}" width="46" height="28" rx="3" fill="{PLATE}" stroke="rgba(198,222,206,0.3)"/>')
    b(text(x + 23, SY + 29, s, anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
    for k, (std, _, col) in enumerate(ERAS):
        if std.endswith(s):
            b(f'<rect class="fx" x="{x}" y="{SY + 10}" width="46" height="28" rx="3" fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="2" opacity="0">{during(k)}</rect>')
H = SY + 50
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-45 svgd-part2-45">')
o.append('<title id="svgt-part2-45">Fig 6.9 · C++ standards · the language eating its own complexity</title>')
o.append('<desc id="svgd-part2-45">Adding up a vector in three eras of C++. C++98: an explicit iterator loop over three lines. C++11: a range-for, for (int x : v) total += x. '
         'C++23: auto total = std::ranges::fold_left(v, 0, std::plus{}), with no loop at all. Beneath, the seven standards: 98, 03, 11, 14, 17, 20 and 23.</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ('Seven standards in twenty-five years, and the same task keeps getting shorter: an iterator loop in C++98, a range-for in C++11, a single fold with no loop in C++23. '
           'The old forms still compile, so the language keeps growing while the recommended way to write it shrinks.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The two big ones.</b> C++11 (<code>auto</code>, lambdas, move semantics, smart pointers) and C++20 (concepts, modules, ranges, coroutines) each changed what "modern C++" means.</li>
          <li><b>The books.</b> Scott Meyers wrote <em>Effective Modern C++</em> (2014) because C++11 had overtaken much of his <em>Effective C++</em>.</li>
          <li><b>Little is removed.</b> <code>auto_ptr</code>, gone in C++17, is a rare exception; that is why the language only grows.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-9">
      <div class="diagram-label">Fig 6.9 · C++ standards · the language eating its own complexity</div>
      {svg}
      <p id="ch6-modern-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-9', 'ch6-modern-p6', card)
