# Fig 4.14 · Copy-on-write filesystem (Pass 28, law 3). Greenbar paper (a light card in Part II).
# Changing block 103 writes 103′, then a new parent, then a new root; one pointer switch makes it
# current, and the old root stays behind as a snapshot sharing block 102. t=0 (shift): both trees.
import figlib
from figlib import Timeline, text, splice, PLEX
figlib.FONT = PLEX

INK, INK_SOFT, GB = '#1d2b22', 'rgba(29,43,34,0.62)', '#2e6f52'
BOX, AMBER = '#f5f8f3', '#8a5a00'
W, H = 400, 290
D = 10.0
T = Timeline(D, shift=9.0)
NEW_BLOCK, NEW_NODE, NEW_ROOT, SWITCH = 1.0, 2.2, 3.4, 4.6
def on_from(t):
    return T.anim('opacity', [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
def node(cx, y, w, h, label, new=False, size=14):
    stroke, fill, op = (GB, 'rgba(46,111,82,0.14)', '2') if new else ('rgba(29,43,34,0.45)', BOX, '1.2')
    a(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{op}"/>')
    a(text(cx, y + h / 2 + 5, label, anchor='middle', size=size, fill=GB if new else INK, ls='0'))
def edge(x1, y1, x2, y2, new=False):
    col = GB if new else 'rgba(29,43,34,0.5)'
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2 - 6}" stroke="{col}" stroke-width="{2 if new else 1.4}"/>')
    import math
    ang = math.atan2(y2 - y1, x2 - x1); L = 7
    p = [(x2, y2), (x2 - L * math.cos(ang - 0.45), y2 - L * math.sin(ang - 0.45)), (x2 - L * math.cos(ang + 0.45), y2 - L * math.sin(ang + 0.45))]
    a('<polygon points="' + ' '.join(f'{px:.1f},{py:.1f}' for px, py in p) + f'" fill="{col}"/>')
OLD_C, NEW_C = 100, 300
RY, NY, BY = 48, 124, 200
RW, RH = 110, 34
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-15 svgd-part2-15">')
a('<title id="svgt-part2-15">Fig 4.14 · Copy-on-write filesystem: never overwrite, just re-point</title>')
a('<desc id="svgd-part2-15">A file\'s tree: a root points to a node, which points to blocks 102 and 103. To change block 103 the filesystem writes a new block 103′ elsewhere, '
  'then a new node pointing at 102 and 103′, then a new root. One pointer switch makes the new root current. Nothing was overwritten: the old root still points at the old node and block 103, '
  'so it is a snapshot of the file before the change, and block 102 is shared by both versions.</desc>')
# old tree (always there)
node(OLD_C, RY, RW, RH, 'root')
node(OLD_C, NY, RW, RH, 'node')
node(70, BY, 96, RH, '103')
node(200, BY, 96, RH, '102')
edge(OLD_C, RY + RH, OLD_C, NY)
edge(OLD_C - 14, NY + RH, 74, BY)
edge(OLD_C + 14, NY + RH, 192, BY)
# new tree, bottom up
a(f'<g>{on_from(NEW_BLOCK)}'); node(330, BY, 96, RH, '103′', new=True); a('</g>')
a(f'<g>{on_from(NEW_NODE)}'); node(NEW_C, NY, RW, RH, 'node′', new=True)
edge(NEW_C - 14, NY + RH, 208, BY, new=True); edge(NEW_C + 14, NY + RH, 326, BY, new=True); a('</g>')
a(f'<g>{on_from(NEW_ROOT)}'); node(NEW_C, RY, RW, RH, 'root′', new=True); edge(NEW_C, RY + RH, NEW_C, NY, new=True); a('</g>')
# the current marker: one pointer switch
TY = 28
a(f'<g>{T.anim("opacity", [(0.0, 1.0), (SWITCH - 0.008, 1.0), (SWITCH - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)])}'
  f'{text(OLD_C, TY, "current", anchor="middle", size=13, fill=GB, ls="0")}</g>')
a(f'<g>{on_from(SWITCH)}{text(NEW_C, TY, "current", anchor="middle", size=13, fill=GB, ls="0")}'
  f'{text(OLD_C, TY, "snapshot", anchor="middle", size=13, fill=AMBER, ls="0")}</g>')
a(f'<rect class="fx" x="{NEW_C - RW / 2 - 4}" y="{RY - 4}" width="{RW + 8}" height="{RH + 8}" rx="5" fill="none" stroke="{GB}" stroke-width="2.5" opacity="0">{lit(SWITCH, SWITCH + 0.8)}</rect>')
a(text(200, BY + RH + 20, 'shared', anchor='middle', size=13, fill=INK_SOFT, ls='0'))
# status
SY = 276
STAT = [(0.4, NEW_BLOCK, 'change block 103'), (NEW_BLOCK, NEW_NODE, 'write 103′ somewhere new'), (NEW_NODE, NEW_ROOT, 'write a new parent'),
        (NEW_ROOT, SWITCH, 'write a new root'), (SWITCH, 9.6, 'switch one pointer: done')]
for t0, t1, s in STAT:
    a(f'<g opacity="0">{lit(t0, t1)}{text(W / 2, SY, s, anchor="middle", size=13, fill=INK, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A copy-on-write filesystem never overwrites a block: changing 103 writes a new 103′, a new parent and a new root, and one pointer switch makes the change live. '
           'The old root still describes the old file, so a snapshot costs nothing until the versions diverge.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Crash safety.</b> Before the switch the old tree is whole; after it the new one is. A crash before the switch loses only the change, never the filesystem.</li>
          <li><b>Checksums.</b> Every block can carry a checksum checked on each read, so silent disk corruption is caught. ZFS and btrfs cover data too; APFS covers metadata.</li>
          <li><b>The cost.</b> One changed byte rewrites a block at every level up to the root: <span class="key-term">write amplification</span>. NetApp's WAFL made this trade in the early 1990s; ZFS, btrfs and APFS make it now.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-4-14">
      <div class="diagram-label">Fig 4.14 · Copy-on-write filesystem: never overwrite, just re-point</div>
      {svg}
      <p id="ch4-fs-p12" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-14', 'ch4-fs-p12', card)
