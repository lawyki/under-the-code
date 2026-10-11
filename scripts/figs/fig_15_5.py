# Fig 15.5 · SQL injection defence in depth · five layers, each independent (Pass 28, law 3, conceptual pass: the
# defence). Strongroom dossier plate. Five layers as bands, a bad input dropping through them. Run 1: everything in place,
# the input fails validation at layer 1. Run 2: the input passes validation, and one endpoint built its SQL by hand, so
# layers 2 and 3 have a gap; the input falls through both, the least-privileged database account refuses at layer 4,
# and monitoring at layer 5 raises an alert. t=0 (shift): run 2's end state.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

LAYERS = ['1 · validate input', '2 · parameterised queries', '3 · ORM by default', '4 · least-privilege account', '5 · monitoring']
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
R1, R2 = 0.8, 4.6
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
o = []; a = o.append
TX = 300                                      # the input's lane, through the gaps
GX0, GX1 = 278, 322                           # the gap in layers 2 and 3 during run 2
LY0, LH = 56, 52
ly = lambda k: LY0 + k * LH
a(text(20, 24, 'a bad input', size=13, fill=SEAL, ls='0'))
a(f'<line x1="{TX}" y1="30" x2="{TX}" y2="{ly(4) + 36}" stroke="{PMUTED}" stroke-opacity="0.25" stroke-dasharray="3 4"/>')
band = lambda k, x0, x1: f'<rect x="{x0}" y="{ly(k)}" width="{x1 - x0}" height="36" rx="2" fill="{DCARD}" stroke="{BRASS}" stroke-opacity="0.75"/>'
for k, lab in enumerate(LAYERS):
    if k in (1, 2):
        a(f'<g opacity="0">{first(R2 + 0.6)}{band(k, 20, 380)}</g>')
        a(f'<g opacity="0">{win(R2 + 0.6)}{band(k, 20, GX0)}{band(k, GX1, 380)}</g>')
    else:
        a(band(k, 20, 380))
    a(text(32, ly(k) + 23, lab, size=13, fill=PARCH, ls='0'))
# run 1: stopped at layer 1
def drop(t0, y1, col):
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t0 + 0.25 * (y1 - 24) / LH, y1 - 24), (D, y1 - 24)], 'y')
    return mv
a(f'<g class="fx" opacity="0">{lit(R1, R2 - 0.6)}<g>{drop(R1, ly(0) - 8, SEAL)}<circle cx="{TX}" cy="24" r="7" fill="{SEAL}"/></g></g>')
a(f'<g class="fx" opacity="0">{pulse(R1 + 0.3)}<rect x="17" y="{ly(0) - 3}" width="366" height="42" rx="3" fill="{SEAL}" fill-opacity="0.18" stroke="{SEAL}" stroke-width="2"/></g>')
# run 2: through the gaps in 2 and 3, refused at 4
T4 = R2 + 1.2 + 0.25 * (ly(3) - 8 - 24) / LH
a(f'<g class="fx" opacity="0">{lit(R2 + 1.2, D - 0.2)}<g>{drop(R2 + 1.2, ly(3) - 8, SEAL)}<circle cx="{TX}" cy="24" r="7" fill="{SEAL}"/></g></g>')
for k in (1, 2):
    a(f'<g class="fx" opacity="0">{pulse(R2 + 0.6)}<rect x="{GX0 - 2}" y="{ly(k) - 2}" width="{GX1 - GX0 + 4}" height="40" rx="2" fill="none" stroke="{SEAL}" stroke-width="2" stroke-dasharray="4 3"/></g>')
a(f'<g class="fx" opacity="0">{pulse(T4)}<rect x="17" y="{ly(3) - 3}" width="366" height="42" rx="3" fill="{SAGE}" fill-opacity="0.18" stroke="{SAGE}" stroke-width="2"/></g>')
a(f'<g opacity="0">{win(T4 + 0.4)}{text(368, ly(4) + 23, "alert", anchor="end", size=13, fill=SEAL, ls="0")}</g>')
SY = ly(5) + 6
for t0, t1, s, col in ((0.31, R2, 'fails validation: stopped at 1', SAGE), (R2, T4, 'hand-built SQL: 2 and 3 have a gap', SEAL),
                       (T4, None, 'no such right: refused at 4', SAGE)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(20, SY, s, size=13, fill=col, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-32 svgd-part4-32">')
o.insert(1, '<title id="svgt-part4-32">Fig 15.5 · SQL injection defence in depth · five layers, each independent</title>')
o.insert(2, '<desc id="svgd-part4-32">Five layers stand between a bad input and the data: input validation, parameterised queries, an ORM that parameterises by default, a database account with the least privilege it needs, and monitoring. '
  'First, with every layer in place, the input fails validation and stops at layer 1. Then an input passes validation, and one endpoint built its SQL by hand, leaving a gap in layers 2 and 3; it falls through both, the database account refuses it at layer 4 for lack of the right, and monitoring raises an alert.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Defence in depth stacks independent layers so that no single mistake is fatal: here one endpoint built its SQL by hand, opening a gap in two layers, and the least-privileged database account still refused while monitoring raised the alarm. '
           'Each layer is built as if the ones above it had failed.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The cure and the rest.</b> Layer 2 is the real fix (Fig 13.11); the others exist for the day it is missing.</li>
          <li><b>The same template.</b> Every web flaw has its own primary fix under the same supporting layers: output encoding for XSS, allow-lists for URLs a server fetches.</li>
          <li><b>Least privilege in practice.</b> The application's database account gets only the statements it needs on its own tables, never ownership or the right to drop them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-15-5">
      <div class="diagram-label">Fig 15.5 · SQL injection defence in depth · five layers, each independent</div>
      {svg}
      <p id="ch15-web-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-15-5', 'ch15-web-p3', card)
