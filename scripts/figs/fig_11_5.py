# Fig 11.5 · The DNS namespace · a tree, read right to left (Pass 28, law 3). Chart Room plate. The name
# www.example.com. above a slice of the tree: the root, four top-level domains, two names under com, two hosts
# under example.com. Read from the right, each label is one step down: the dot (root), com, example, www. The
# labels light right to left as the path lights top-down, and each level's operator lights with it.
# t=0 (shift): the whole path lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, BLUE = '#9bd89b', '#86a8ff'
W = 400
NY = 30                                          # the name
LV = [84, 152, 220, 288]                         # level y (box centres)
BH = 28
NODES = {'root': (110, 0, '.', CYAN), 'com': (50, 1, 'com', GREEN), 'org': (112, 1, 'org', GREEN), 'fi': (168, 1, 'fi', GREEN),
         'tlds': (220, 1, '…', CMUTED), 'example': (52, 2, 'example', BLUE), 'google': (140, 2, 'google', BLUE), 'sld': (210, 2, '…', CMUTED),
         'www': (34, 3, 'www', ROUTE), 'mail': (98, 3, 'mail', ROUTE)}
EDGES = [('root', 'com'), ('root', 'org'), ('root', 'fi'), ('root', 'tlds'), ('com', 'example'), ('com', 'google'), ('com', 'sld'),
         ('example', 'www'), ('example', 'mail')]
PATH = ['root', 'com', 'example', 'www']
OPS = [('root servers:', '12 operators'), ('com: VeriSign', 'fi: Traficom'), ('example.com:', 'its registrant'), ('www: one host', 'in that zone')]
OX = 254
bw = lambda s: max(34, len(s) * 8 + 20)
D = 9.0
TL = [0.8, 2.0, 3.2, 4.4]                       # the path, top-down
T = Timeline(D, shift=8.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
H = LV[3] + BH // 2 + 20
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-44 svgd-part3-44">')
a('<title id="svgt-part3-44">Fig 11.5 · The DNS namespace · a tree, read right to left</title>')
a('<desc id="svgd-part3-44">The name www.example.com. above a slice of the DNS tree. At the top the root, run by 12 operators; below it top-level domains such as com, org and fi; under com, names such as example and google; under example.com, hosts such as www and mail. '
  'Reading the name from the right walks the tree from the top: the final dot is the root, then com, run by VeriSign, then example, run by whoever registered it, then www, one host in that zone.</desc>')
# the name, label by label; each lights when its level is reached
parts = [('www', ROUTE, 3), ('.', CMUTED, None), ('example', BLUE, 2), ('.', CMUTED, None), ('com', GREEN, 1), ('.', CYAN, 0)]
dim = lambda t0: T.anim('fill-opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.35), (t0 - 0.002, 0.35), (t0, 1.0), (D, 1.0)])
spans = ''.join(f'<tspan fill="{col}">{lab}</tspan>' if lv is None else f'<tspan fill="{col}" fill-opacity="1">{dim(TL[lv])}{lab}</tspan>' for lab, col, lv in parts)
a(text(W / 2, NY, spans, anchor='middle', size=16, fill=CSOFT, ls='0'))
a(text(W / 2, NY + 22, 'read from the right', anchor='middle', size=13, fill=CMUTED, ls='0'))
# edges, then the path's edges lit
pos = lambda k: (NODES[k][0], LV[NODES[k][1]])
for p, c in EDGES:
    (x1, y1), (x2, y2) = pos(p), pos(c)
    a(f'<line x1="{x1}" y1="{y1 + BH / 2}" x2="{x2}" y2="{y2 - BH / 2}" stroke="{CMUTED}" stroke-opacity="0.6"/>')
for i in range(1, len(PATH)):
    (x1, y1), (x2, y2) = pos(PATH[i - 1]), pos(PATH[i])
    a(f'<g class="fx" opacity="0">{win(TL[i])}<line x1="{x1}" y1="{y1 + BH / 2}" x2="{x2}" y2="{y2 - BH / 2}" stroke="#fff" stroke-width="2.5"/></g>')
for k, (cx, lv, lab, col) in NODES.items():
    w = bw(lab)
    a(f'<rect x="{cx - w / 2}" y="{LV[lv] - BH / 2}" width="{w}" height="{BH}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(cx, LV[lv] + 5, lab, anchor='middle', size=13 if lab != '.' else 16, fill=col, ls='0'))
    if k in PATH:
        a(f'<g class="fx" opacity="0">{win(TL[PATH.index(k)])}<rect x="{cx - w / 2}" y="{LV[lv] - BH / 2}" width="{w}" height="{BH}" rx="5" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="2"/></g>')
# who runs each level
for lv, (l1, l2) in enumerate(OPS):
    y = LV[lv]
    a(f'<g opacity="0.45">{text(OX, y - 3, l1, anchor="start", size=13, fill=CSOFT, ls="0")}{text(OX, y + 14, l2, anchor="start", size=13, fill=CMUTED, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{win(TL[lv])}{text(OX, y - 3, l1, anchor="start", size=13, fill=CSOFT, ls="0")}{text(OX, y + 14, l2, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ("The bold path is the name read from the right. Beside each level stands who runs it, and <code>www</code> is only one host inside <code>example.com</code>'s zone.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The root.</b> Twelve organisations run it as thirteen named servers, <code>a.root-servers.net</code> to <code>m.root-servers.net</code>, each copied to many sites by anycast: well over a thousand instances.</li>
          <li><b>The levels.</b> <code>com</code> and <code>net</code> are run by VeriSign, <code>org</code> by Public Interest Registry, each country code by a national registry (<code>fi</code> by Traficom). Below that, the registrant runs its own zone or hands it to a host or CDN.</li>
          <li><b>The trust.</b> About 360 million registered names, and nobody below the root checks anyone else's answers: each operator is trusted for its own subtree, unless DNSSEC signatures are added.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-5">
      <div class="diagram-label">Fig 11.5 · The DNS namespace · a tree, read right to left</div>
      {svg}
      <p id="ch11-dns-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-5', 'ch11-dns-p4', card)
