# Fig 4.11 · Dirty COW: the race that broke Linux (Pass 28, law 3, conceptual pass: the promise and the bug's life,
# not the attack). Top: copy-on-write's one promise, a write lands in a private copy and never in the file underneath.
# Below, a vertical timeline swept from 2005 to 2017: Linus's first fix of the race (2005) is undone; from Linux 2.6.22
# (2007) the flaw is in every kernel, a red bar growing for nine years; October 2016, seen in use, patched within
# hours (author date 2016-10-13, §4g); 2017, a related flaw in the huge-page path (CVE-2017-1000405).
# t=0 (shift): the whole timeline drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
Y = {2005: 128, 2007: 172, 2016: 368, 2017: 404}
ty = lambda y: 1.0 + (y - Y[2005]) / (Y[2017] - Y[2005]) * 7.0    # the sweep's time at height y
TT = {yr: ty(y) for yr, y in Y.items()}
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# the promise
a(f'<rect x="20" y="14" width="360" height="72" rx="6" fill="{PANEL}" stroke="rgba(132,255,178,0.5)"/>')
a(text(32, 36, 'copy-on-write promises:', size=13, fill=PHOS, ls='0'))
a(text(32, 56, 'a write lands in a private copy,', size=13, fill='#fff', ls='0'))
a(text(32, 74, 'never in the file underneath', size=13, fill='#fff', ls='0'))
# the axis
AX = 70
a(f'<line x1="{AX}" y1="{Y[2005] - 14}" x2="{AX}" y2="{Y[2017] + 10}" stroke="{MUTED}"/>')
EV = [(2005, 'a first fix, later undone', MUTED), (2007, 'Linux 2.6.22: flaw ships', GOLD),
      (2016, 'seen in use: patched in hours', PHOS), (2017, 'a related flaw, huge pages', GOLD)]
for yr, s, col in EV:
    y = Y[yr]
    a(text(20, y + 5, str(yr), size=13, fill=MUTED, ls='0'))
    a(f'<circle cx="{AX}" cy="{y}" r="4" fill="{MUTED}"/>')
    a(f'<g opacity="0">{win(TT[yr])}<circle cx="{AX}" cy="{y}" r="6" fill="{col}"/>{text(AX + 18, y + 5, s, size=13, fill=col, ls="0")}</g>')
# nine years exposed: a red bar grows from 2007 to 2016, then stops
BX, B0, B1 = AX + 18, Y[2007] + 18, Y[2016] - 18
a(f'<rect x="{BX}" y="{B0}" width="10" height="{B1 - B0}" rx="3" fill="none" stroke="{RED}" stroke-opacity="0.4"/>')
grow = T.anim('height', [(0.0, B1 - B0), (0.3, B1 - B0), (0.305, 0.0), (ty(B0), 0.0), (ty(B1), B1 - B0), (D, B1 - B0)])
a(f'<rect x="{BX}" y="{B0}" width="10" height="{B1 - B0}" rx="3" fill="{RED}" fill-opacity="0.8">{grow}</rect>')
MY = (B0 + B1) / 2
a(text(BX + 24, MY - 4, 'nine years in', size=13, fill=RED, ls='0'))
a(text(BX + 24, MY + 14, 'every kernel after', size=13, fill=RED, ls='0'))
# the sweep
mv = T.translate([(0.0, 0.0), (0.3, 0.0), (0.305, 0.0), (TT[2005], 0.0), (TT[2017], Y[2017] - Y[2005]), (D, Y[2017] - Y[2005])], 'y')
a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (TT[2005] - 0.002, 0.0), (TT[2005], 1.0), (TT[2017] + 0.3, 1.0), (TT[2017] + 0.32, 0.0), (D, 0.0)])}'
  f'<g>{mv}<rect x="{AX - 8}" y="{Y[2005] - 2}" width="16" height="4" rx="2" fill="#fff"/></g></g>')
H = Y[2017] + 26
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-12 svgd-part2-12">')
o.insert(1, '<title id="svgt-part2-12">Fig 4.11 · Dirty COW: the race that broke Linux</title>')
o.insert(2, '<desc id="svgd-part2-12">Copy-on-write promises that a write lands in a private copy and never in the file underneath. A timeline from 2005 to 2017: in 2005 a first fix for the race is made and later undone; from Linux 2.6.22 in 2007 the flaw ships in every kernel, for nine years; in October 2016 it is seen in use and patched within hours; in 2017 a related flaw turns up in the huge-page code.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Dirty COW broke copy-on-write\'s one promise, that a write lands in a private copy and never in the file. '
           'It shipped in Linux for nine years, was patched within hours of being seen in use in October 2016, and a related flaw followed in the huge-page code a year later.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The fix.</b> The kernel now remembers that it made the private copy and allows the write only if the page-table entry is still that private copy, instead of retrying the look-up as a plain read.</li>
          <li><b>The class.</b> A check, then an action that relies on it, with a moment between them in which something else can change: time-of-check to time-of-use, closed by making the two one step or checking again.</li>
          <li><b>Getting the patch out.</b> A fix protects only machines that install it; distributions shipped it within days, Android in its December 2016 security bulletin.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-11">
      <div class="diagram-label">Fig 4.11 · Dirty COW: the race that broke Linux</div>
      {svg}
      <p id="ch4-vm-p18" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-11', 'ch4-vm-p18', card)
