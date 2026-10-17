# Fig 7.1 · The two pipelines (Pass 28, law 3). Two lanes across three runs. C: compile and link once,
# then every run is native. Python: the first run parses and compiles to bytecode, later runs load it
# from the .pyc cache, and every run goes through the eval loop. t=0 (shift): run 3, the full story.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 236
D = 12.0
T = Timeline(D, shift=8.9)
RUNS = [2.0, 5.0, 8.0]
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-47 svgd-part2-47">')
a('<title id="svgt-part2-47">Fig 7.1 · The two pipelines, side by side</title>')
a('<desc id="svgd-part2-47">Two programs, each run three times. The C program is compiled and linked once, on the developer\'s machine, and every run executes native machine code. '
  'The Python module is parsed and compiled to bytecode the first time it is imported, and the bytecode is saved in a .pyc file; later runs load it from the cache, but every run, the first and the later ones, '
  'goes through CPython\'s eval loop, which interprets the bytecode one instruction at a time.</desc>')
for k, t in enumerate(RUNS):
    t1 = RUNS[k + 1] if k < 2 else D - 0.3
    a(f'<g opacity="0">{win(t, t1)}{text(380, 22, f"run {k + 1} of 3", anchor="end", size=13, fill="#fff", ls="0")}</g>')
def chip(x, y, w, label, col):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(x + w / 2, y + 22, label, anchor='middle', size=13, fill='#fff', ls='0'))
def glow(x, y, w, col, t0, t1):
    a(f'<rect class="fx" x="{x}" y="{y}" width="{w}" height="34" rx="3" fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="2.2" opacity="0">{win(t0, t1)}</rect>')
# C lane
y = 60
a(text(20, y - 14, 'C · main.c', size=13, fill=GOLD, ls='0'))
chip(20, y, 88, 'compile', GOLD); chip(116, y, 72, 'link', GOLD); chip(222, y, 158, 'native code', GOLD)
glow(20, y, 88, GOLD, 0.6, 1.4); glow(116, y, 72, GOLD, 1.0, 1.6)
for t in RUNS:
    glow(222, y, 158, GOLD, t + 0.4, t + 1.4)
a(f'<line x1="205" y1="{y - 6}" x2="205" y2="{y + 40}" stroke="rgba(198,222,206,0.4)" stroke-dasharray="3 3"/>')
a(text(20, y + 54, 'once, before shipping', size=13, fill=MUTED, ls='0'))
a(text(380, y + 54, 'every run', anchor='end', size=13, fill=MUTED, ls='0'))
# Python lane
y = 160
a(text(20, y - 14, 'Python · an imported module', size=13, fill=BLUE, ls='0'))
CACHE = [(t, t + 1.6) for t in RUNS[1:]]
pts = [(0.0, 1.0)]
for t0, t1 in CACHE:
    pts += [(t0 - 0.008, 1.0), (t0 - 0.005, 0.0), (t1 - 0.002, 0.0), (t1, 1.0)]
pts += [(D, 1.0)]
a(f'<g>{T.anim("opacity", pts)}'); chip(20, y, 80, 'parse', BLUE); chip(108, y, 88, 'bytecode', BLUE); a('</g>')
chip(222, y, 158, 'eval loop', BLUE)
glow(20, y, 80, BLUE, RUNS[0], RUNS[0] + 0.6); glow(108, y, 88, BLUE, RUNS[0] + 0.3, RUNS[0] + 0.9)
for t in RUNS[1:]:
    a(f'<g opacity="0">{win(t, t + 1.6)}<rect x="20" y="{y}" width="176" height="34" rx="3" fill="{PLATE}" stroke="{BLUE}" stroke-dasharray="4 3"/>'
      f'{text(108, y + 22, "from .pyc cache", anchor="middle", size=13, fill=BLUE, ls="0")}</g>')
for t in RUNS:
    glow(222, y, 158, BLUE, t + 0.4 + (0.5 if t == RUNS[0] else 0), t + 1.6)
a(f'<line x1="205" y1="{y - 6}" x2="205" y2="{y + 40}" stroke="rgba(198,222,206,0.4)" stroke-dasharray="3 3"/>')
a(text(20, y + 54, 'first run, then cached', size=13, fill=MUTED, ls='0'))
a(text(380, y + 54, 'every run', anchor='end', size=13, fill=MUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ("C pays for translation once, on the developer's machine, and every run executes native code; Python translates on the user's machine, caches an imported module's bytecode in a <code>.pyc</code> file, and interprets it on every run. Python ships source that runs wherever there is an interpreter, and pays in cycles each time it runs.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>C.</b> The compiler parses, optimises and emits machine code; the linker joins the pieces into one executable for one kind of machine.</li>
          <li><b>Python.</b> CPython parses a module to a syntax tree, compiles it to bytecode and caches that in <code>__pycache__</code> when it is imported (a script run directly is recompiled each time); its eval loop runs one bytecode instruction at a time.</li>
          <li><b>In between.</b> Just-in-time compilers (PyPy, and CPython 3.13's experimental JIT) turn hot bytecode into machine code while the program runs.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-1">
      <div class="diagram-label">Fig 7.1 · The two pipelines, side by side</div>
      {svg}
      <p id="ch7-interpret-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-1', 'ch7-interpret-p4', card)
