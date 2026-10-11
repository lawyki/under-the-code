# Fig 15.1 · STRIDE · the six classes of threat to enumerate (Pass 28, law 3, conceptual pass: the method). Strongroom
# dossier plate. Two parts of a design, a login service and a public image CDN, each walked through the six questions in
# turn, a cursor stepping down the letters; each row names the threat and the property it would break. For the login
# service all six apply; for the CDN, repudiation and disclosure do not (nothing to deny, nothing secret).
# t=0 (shift): the CDN's verdicts.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

ROWS = [('S', 'spoofing', 'authentication'), ('T', 'tampering', 'integrity'), ('R', 'repudiation', 'non-repudiation'),
        ('I', 'information disclosure', 'confidentiality'), ('D', 'denial of service', 'availability'),
        ('E', 'elevation of privilege', 'authorisation')]
PARTS = [('login service', [True] * 6), ('public image CDN', [True, True, False, False, True, True])]
W = 400
D = 11.0
T = Timeline(D, shift=10.4)
STEP = 0.55
TP = [0.8, 5.6]                               # each part's walk starts
tr = lambda p, k: TP[p] + STEP * k
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
# the two parts
BX = [20, 210]
for p, (name, _) in enumerate(PARTS):
    a(f'<rect x="{BX[p]}" y="12" width="170" height="40" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
    a(text(BX[p] + 85, 37, name, anchor='middle', size=13, fill=PARCH, ls='0'))
sel = [(0.0, BX[1] - BX[0]), (0.3, BX[1] - BX[0]), (0.305, 0.0), (TP[1] - 0.3, 0.0), (TP[1], BX[1] - BX[0]), (D, BX[1] - BX[0])]
a(f'<g>{T.translate(sel, "x")}<rect x="{BX[0] - 2}" y="10" width="174" height="44" rx="3" fill="none" stroke="{BRASS}" stroke-width="2.5"/></g>')
a(text(20, 80, 'ask of this part:', size=13, fill=PMUTED, ls='0'))
# the six rows
RY0, RH = 92, 46
ry = lambda k: RY0 + k * RH
for k, (L, threat, prop) in enumerate(ROWS):
    y = ry(k)
    a(text(20, y + 18, L, size=13, fill=SEAL, ls='0', extra=' font-weight="700"'))
    a(text(44, y + 18, threat, size=13, fill=PARCH, ls='0'))
    a(text(44, y + 36, f'breaks {prop}', size=13, fill=PMUTED, ls='0'))
    for p, (_, applies) in enumerate(PARTS):
        t0 = tr(p, k)
        t1 = TP[1] if p == 0 else None
        verdict = text(380, y + 18, 'applies' if applies[k] else 'not here', anchor='end', size=13, fill=SEAL if applies[k] else SAGE, ls='0')
        vis = win(t0) if t1 is None else lit(t0, t1)
        a(f'<g opacity="0">{vis}{verdict}</g>')
# the cursor stepping down the rows, once per part
pts = [(0.0, ry(5) - ry(0)), (0.3, ry(5) - ry(0)), (0.305, 0.0)]
for p in range(2):
    for k in range(6):
        pts.append((tr(p, k), ry(k) - ry(0)))
        if k < 5: pts.append((tr(p, k + 1) - 0.12, ry(k) - ry(0)))
    if p == 0: pts += [(TP[1] - 0.12, ry(5) - ry(0)), (TP[1], 0.0)]
pts.append((D, ry(5) - ry(0)))
a(f'<g class="fx">{T.translate(pts, "y")}<rect x="14" y="{ry(0) + 2}" width="372" height="{RH - 4}" rx="3" fill="{BRASS}" fill-opacity="0.08" stroke="{BRASS}" stroke-opacity="0.8"/></g>')
H = ry(6) + 6
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-28 svgd-part4-28">')
o.insert(1, '<title id="svgt-part4-28">Fig 15.1 · STRIDE · the six classes of threat to enumerate</title>')
o.insert(2, '<desc id="svgd-part4-28">STRIDE applied to two parts of one design. Each part is asked six questions in turn: spoofing, which breaks authentication; tampering, which breaks integrity; repudiation, which breaks non-repudiation; information disclosure, which breaks confidentiality; denial of service, which breaks availability; and elevation of privilege, which breaks authorisation. '
  'For a login service all six apply. For a public image CDN, repudiation and information disclosure do not, since there is nothing to deny and nothing secret, while the other four still apply.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('STRIDE turns threat modelling into six questions asked of every part of a design: could someone spoof, tamper, repudiate, disclose, deny service or elevate privilege here? '
           'The answers differ from part to part, and each yes names the property that part must defend.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The defences.</b> Each letter has its usual answer: authentication, integrity checks, audit logs, encryption and access control, rate limits and spare capacity, permission checks.</li>
          <li><b>Per element.</b> On a data-flow diagram, processes face all six, while data stores and the flows between them mainly face tampering, disclosure and denial.</li>
          <li><b>Least privilege.</b> A part that runs with only the rights it needs cannot hand the rest of the system over when it falls.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-15-1">
      <div class="diagram-label">Fig 15.1 · STRIDE · the six classes of threat to enumerate</div>
      {svg}
      <p id="ch15-mindset-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-15-1', 'ch15-mindset-p4', card)
