# Fig 5.10 · Where C still runs in 2026 (Pass 28, law 3). One request from a Python program travels
# down the layers beneath it, lit in turn; every layer below the program is written in C.
# t=0: the whole stack, nothing lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

LAYERS = [('app.py', 'your program', 'Python', BLUE),
          ('CPython', 'the interpreter running it', 'C', PHOS),
          ('OpenSSL · SQLite', 'libraries it calls', 'C', PHOS),
          ('libc', 'the system-call wrappers', 'C', PHOS),
          ('Linux', 'the kernel', 'C', PHOS),
          ('firmware', 'disk and network controllers', 'mostly C', PHOS)]
W = 400
LH, GAP, Y0 = 42, 8, 12
D = 8.0
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
ST = [0.6 + 0.8 * k for k in range(len(LAYERS))]
o = []; body = []; b = body.append
for k, (name, role, lang, col) in enumerate(LAYERS):
    y = Y0 + k * (LH + GAP)
    b(f'<rect x="20" y="{y}" width="272" height="{LH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.35)"/>')
    b(f'<rect class="fx" x="20" y="{y}" width="272" height="{LH}" rx="3" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2" opacity="0">{win(ST[k], ST[k] + 0.9)}</rect>')
    b(text(32, y + 18, name, size=14, fill='#fff', ls='0'))
    b(text(32, y + 35, role, size=13, fill=MUTED, ls='0'))
    b(f'<rect x="300" y="{y}" width="80" height="{LH}" rx="3" fill="{PLATE}" stroke="{col}" stroke-opacity="0.8"/>')
    b(text(340, y + 26, lang, anchor='middle', size=13, fill=col, ls='0'))
H = Y0 + len(LAYERS) * (LH + GAP) + 4
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-34 svgd-part2-34">')
o.append('<title id="svgt-part2-34">Fig 5.10 · Where C still runs in 2026</title>')
o.append('<desc id="svgd-part2-34">A request from a Python program, app.py, travels down the layers beneath it: the CPython interpreter, libraries such as OpenSSL and SQLite, libc, the Linux kernel, '
         'and the firmware of the disk and network controllers. The program is Python; every layer beneath it is written in C, the firmware mostly so.</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ('Underneath a Python program the work soon runs in C: its request passes through the CPython interpreter, OpenSSL and SQLite, libc and the Linux kernel, all written in C. '
           'C holds the layers where cycles and predictability matter most, and pays for it in memory-safety bugs.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why it stays.</b> No garbage collector, a simple calling convention every other language can call into, and a compiler for nearly every chip ever made.</li>
          <li><b>The price.</b> Microsoft and Google's Chromium team have each reported that about 70% of their serious security bugs are memory-safety bugs.</li>
          <li><b>The successor.</b> Rust has been accepted in the Linux kernel since 2022 and is entering Windows and Android, one layer at a time.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-10">
      <div class="diagram-label">Fig 5.10 · Where C still runs in 2026</div>
      {svg}
      <p id="ch5-survives-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-10', 'ch5-survives-p3', card)
