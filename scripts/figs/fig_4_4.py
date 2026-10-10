# Fig 4.4 · CFS picks the leftmost node (Pass 28, law 3). Runnable processes in a balanced search
# tree keyed by virtual runtime. The leftmost, the furthest behind, leaves the tree and runs; its
# virtual runtime grows from 3.2 to 13.0; it goes back in on the right, and 8.1 is now leftmost.
# Drawn as a balanced binary search tree (the red-black colouring is described, not drawn).
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, MUTED
figlib.FONT = PLEX

W, H = 400, 330
T = Timeline(10, shift=0.6)
POS = [(200, 44), (110, 104), (290, 104), (60, 164), (160, 164), (240, 164), (340, 164)]   # heap order
def tree(vals):              # vals sorted -> balanced BST in heap order
    v = sorted(vals); return [v[3], v[1], v[5], v[0], v[2], v[4], v[6]]
A = tree([3.2, 8.1, 10.0, 12.4, 15.5, 17.2, 19.8])
B = tree([8.1, 10.0, 12.4, 13.0, 15.5, 17.2, 19.8])
def win(t0, t1):
    if t0 <= 0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (9.4, 0.0), (9.401, 1.0), (9.9995, 1.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (9.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-4 svgd-part2-4">')
a('<title id="svgt-part2-4">Fig 4.4 · CFS chooses the leftmost node of a red-black tree</title>')
a('<desc id="svgd-part2-4">Seven runnable processes in a balanced search tree, keyed by how much CPU time each has had, its virtual runtime. The leftmost, 3.2, is the furthest behind, so it runs next. '
  'While it runs its virtual runtime grows to 13.0; when its turn ends it goes back into the tree on the right, and the new leftmost, 8.1, runs next.</desc>')
EDGES = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
def draw_tree(vals, leftmost_skip=False, t0=0.0, t1=10.0, hilite=None):
    g = [f'<g opacity="0">{win(t0, t1)}']
    for p, c in EDGES:
        (x1, y1), (x2, y2) = POS[p], POS[c]
        if leftmost_skip and c == 3: continue
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(132,255,178,0.4)" stroke-width="1.5"/>')
    for i, v in enumerate(vals):
        if leftmost_skip and i == 3: continue
        x, y = POS[i]
        lead = (i == 3)
        g.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{PHOS if lead else "#1b2a1f"}" fill-opacity="{0.3 if lead else 1}" stroke="{PHOS if lead else PHOS_SOFT}" stroke-width="{2 if lead else 1.2}"/>'
                 f'<text x="{x}" y="{y + 5}" text-anchor="middle" {PLEX} font-size="14" fill="#fff">{v:.1f}</text>')
    g.append('</g>'); a(''.join(g))
# act: A with 3.2 leftmost; 3.2 leaves to run; B with 13.0 inserted, 8.1 leftmost
draw_tree(A, t0=0.0, t1=1.6)
draw_tree(A, leftmost_skip=True, t0=1.6, t1=5.4)
draw_tree(B, t0=5.4, t1=9.4)
a(f'<g opacity="0">{win(0.0, 1.6)}{text(20, 208, "leftmost: runs next", size=13, fill=PHOS, ls="0")}</g>')
a(f'<g opacity="0">{win(5.4, 9.4)}{text(20, 208, "leftmost: runs next", size=13, fill=PHOS, ls="0")}</g>')
# the CPU, where the leftmost process runs and its virtual runtime grows
a(f'<rect x="20" y="230" width="360" height="86" rx="6" fill="{PLATE}" stroke="rgba(132,255,178,0.45)"/>')
a(text(32, 252, 'ON THE CPU', size=13, fill=MUTED))
VR = [3.2, 5.2, 7.1, 9.1, 11.0, 13.0]
for k, v in enumerate(VR):
    t0 = 1.6 + k * 0.6
    t1 = t0 + 0.6 if k < len(VR) - 1 else 5.4
    a(f'<g opacity="0">{win(t0, t1)}<circle cx="70" cy="286" r="22" fill="{PHOS}" fill-opacity="0.3" stroke="{PHOS}" stroke-width="2"/>'
      f'<text x="70" y="291" text-anchor="middle" {PLEX} font-size="14" fill="#fff">{v:.1f}</text></g>')
a(f'<g opacity="0">{win(1.6, 5.4)}{text(108, 291, "virtual runtime grows", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a(f'<g opacity="0">{win(5.4, 9.4)}{text(32, 291, "13.0 goes back in on the right", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a(f'<g opacity="0">{win(0.0, 1.6)}{text(32, 291, "idle for an instant", size=13, fill=MUTED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('CFS keeps runnable processes in a tree ordered by virtual runtime, the CPU time each has had. '
           'The leftmost is the furthest behind, so it runs next; as it runs its virtual runtime grows, and it goes back in further right.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Virtual runtime.</b> CPU time received, weighted by priority. Whoever has had least is owed the CPU.</li>
          <li><b>The tree.</b> A red-black tree, kept balanced, so finding the leftmost, removing it and inserting a process are all O(log N), even with thousands runnable.</li>
          <li><b>Since 6.6.</b> Linux's default is now EEVDF, which keeps the same bookkeeping and adds a deadline per task so latency-sensitive work runs on time.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-4">
      <div class="diagram-label">Fig 4.4 · CFS chooses the leftmost node of a red-black tree</div>
      {svg}
      <p id="ch4-scheduling-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-4', 'ch4-scheduling-p6', card)
