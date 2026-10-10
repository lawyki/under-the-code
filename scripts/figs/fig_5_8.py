# Fig 5.8 · How "trust the programmer" deletes your bug check (Pass 28, law 3). The source, the
# compiler's four deductions stepping in, the check struck out, and the -O2 output that remains.
# t=0 (shift): the whole deduction and the output.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 330
D = 10.0
T = Timeline(D, shift=9.0)
RESET = 0.4
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
STEPS = ['overflow is UB: it never happens', 'so i + 1 > i for every i', 'so (i + 1 < i) is always false', 'so abort() is dead code']
ST = [1.0 + 0.9 * k for k in range(4)]
STRIKE, OUT = ST[-1] + 0.7, ST[-1] + 1.5
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-32 svgd-part2-32">')
a('<title id="svgt-part2-32">Fig 5.8 · How &quot;trust the programmer&quot; deletes your bug check</title>')
a('<desc id="svgd-part2-32">A function int next(int i) checks if (i + 1 &lt; i) abort(); and then returns i + 1. The compiler reasons: signed overflow is undefined behaviour, so it never happens; '
  'so i + 1 is greater than i for every i; so the test is always false; so the call to abort is dead code. The check is deleted, and gcc at -O2 emits only lea eax,[rdi+1] and ret.</desc>')
a(f'<rect x="20" y="12" width="360" height="98" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
SRC = ['int next(int i) {', '  if (i + 1 &lt; i) abort();', '  return i + 1;', '}']
for k, l in enumerate(SRC):
    y = 34 + k * 21
    if k == 1:
        dim = T.anim('opacity', [(0.0, 0.4), (RESET, 0.4), (RESET + 0.005, 1.0), (STRIKE - 0.002, 1.0), (STRIKE, 0.4), (D, 0.4)])
        a(f'<g>{dim}{text(32, y, l.replace(" ", "&#160;"), size=13, fill=GOLD, ls="0")}</g>')
        a(f'<line x1="44" y1="{y - 4}" x2="236" y2="{y - 4}" stroke="{RED}" stroke-width="2.5">{held(STRIKE)}</line>'.replace('<line', '<line opacity="1"'))
    else:
        a(text(32, y, l.replace(' ', '&#160;'), size=13, fill='#fff', ls='0'))
a(text(20, 136, 'the compiler, at -O2:', size=13, fill=MUTED, ls='0'))
for k, s in enumerate(STEPS):
    y = 162 + k * 24
    a(f'<g>{held(ST[k])}{text(20, y, str(k + 1), size=13, fill=GOLD, ls="0")}{text(40, y, s.replace("<", "&lt;").replace(">", "&gt;"), size=13, fill=RED if k == 3 else PHOS_SOFT, ls="0")}</g>')
a(f'<g>{held(OUT)}<rect x="20" y="262" width="360" height="56" rx="3" fill="{PLATE}" stroke="{PHOS}" stroke-opacity="0.7"/>'
  f'{text(32, 284, "lea eax,[rdi+1]", size=14, fill=PHOS, ls="0")}{text(32, 306, "ret", size=14, fill=PHOS, ls="0")}'
  f'{text(368, 284, "no check left", anchor="end", size=13, fill=RED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Signed overflow is undefined behaviour, so the compiler may assume it never happens; from that, <code>i&nbsp;+&nbsp;1&nbsp;&lt;&nbsp;i</code> is always false and the check is dead code. '
           'At <code>-O2</code> gcc deletes it, leaving only an add and a return.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The safe test.</b> Check before adding, <code>if (i == INT_MAX)</code>, or use <code>__builtin_add_overflow</code> in gcc and clang.</li>
          <li><b>The kernel's answer.</b> Linux builds with <code>-fno-strict-overflow</code> and <code>-fno-delete-null-pointer-checks</code>, switching these deductions off.</li>
          <li><b>Not malice.</b> The standard lets the optimiser assume undefined behaviour never occurs; the same freedom is what lets it delete code that truly is dead.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-8">
      <div class="diagram-label">Fig 5.8 · How "trust the programmer" deletes your bug check</div>
      {svg}
      <p id="ch5-ub-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-8', 'ch5-ub-p4', card)
