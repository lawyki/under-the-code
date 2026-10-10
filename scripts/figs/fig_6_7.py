# Fig 6.7 · Three pointer flavours (Pass 28, law 3). Three lifecycles: a unique_ptr's object dies with
# its one owner; a shared_ptr's object counts 2, 1, 0 as owners go; a weak_ptr watches its object die
# without keeping it alive, and reads expired. t=0: every owner alive.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 314
D = 10.0
T = Timeline(D, shift=0.0)
RESET = 9.6
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def until(t1):   # on from the start, off at t1, back on at the reset
    return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (RESET - 0.002, 0.0), (RESET, 1.0), (D, 1.0)])
def after(t0):
    return win(t0, RESET)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-43 svgd-part2-43">')
a('<title id="svgt-part2-43">Fig 6.7 · Three pointer flavours, three ownership semantics</title>')
a('<desc id="svgd-part2-43">Three lifecycles. unique_ptr: one owner, p; when p goes out of scope the object is freed. shared_ptr: two owners, a and b, and a count of 2; when a goes the count is 1, when b goes it is 0 and the object is freed. '
  'weak_ptr: an owner s and a weak observer w; when s goes the object is destroyed even though w is still watching it, and w reports that it has expired.</desc>')
def chip(x, y, w, label, col, dashed=False):
    da = ' stroke-dasharray="4 3"' if dashed else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="3" fill="{PANEL}" stroke="{col}"{da}/>' + text(x + w / 2, y + 22, label, anchor='middle', size=13, fill='#fff', ls='0')
def ghost(x, y, w):
    return f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="3" fill="none" stroke="rgba(198,222,206,0.25)" stroke-dasharray="3 3"/>'
def arrow(x1, x2, y, col, dashed=False):
    da = ' stroke-dasharray="4 3"' if dashed else ''
    return f'<line x1="{x1}" y1="{y}" x2="{x2 - 6}" y2="{y}" stroke="{col}" stroke-width="1.5"{da}/><polygon points="{x2 - 7},{y - 4} {x2},{y} {x2 - 7},{y + 4}" fill="{col}"/>'
OX, OW = 262, 118
def obj(y, states):
    a(ghost(OX, y, OW))
    for t0, t1, line2, col in states:
        g = until(t1) if t0 == 0 else (after(t0) if t1 == RESET else win(t0, t1))
        a(f'<g>{g}<rect x="{OX}" y="{y}" width="{OW}" height="34" rx="3" fill="{col}" fill-opacity="0.15" stroke="{col}"/>'
          f'{text(OX + OW / 2, y + 22, line2, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
    a(f'<g>{after(states[-1][1])}{text(OX + OW / 2, y + 22, "freed", anchor="middle", size=13, fill=RED, ls="0")}</g>')
# unique_ptr
y = 30
a(text(20, y - 10, 'unique_ptr · one owner', size=13, fill=MUTED, ls='0'))
FREE_U = 2.0
a(ghost(20, y, 130)); a(f'<g>{until(FREE_U)}{chip(20, y, 130, "owner p", PHOS)}{arrow(150, OX, y + 17, PHOS)}</g>')
obj(y, [(0, FREE_U, 'object', PHOS)])
# shared_ptr: two owners stacked, each with its own arrow
def obj2(y, states):  # object centred on a two-owner panel
    obj(y, states)
y = 112
a(text(20, y - 10, 'shared_ptr · counted owners', size=13, fill=MUTED, ls='0'))
A_GO, B_GO = 3.6, 5.2
OY = y + 20
a(ghost(20, y, 130)); a(f'<g>{until(A_GO)}{chip(20, y, 130, "owner a", GOLD)}<path d="M150 {y + 17} L{OX - 6} {OY + 12}" stroke="{GOLD}" stroke-width="1.5"/><polygon points="{OX - 7},{OY + 7} {OX},{OY + 13} {OX - 8},{OY + 16}" fill="{GOLD}"/></g>')
a(ghost(20, y + 40, 130)); a(f'<g>{until(B_GO)}{chip(20, y + 40, 130, "owner b", GOLD)}<path d="M150 {y + 57} L{OX - 6} {OY + 22}" stroke="{GOLD}" stroke-width="1.5"/><polygon points="{OX - 8},{OY + 18} {OX},{OY + 21} {OX - 6},{OY + 27}" fill="{GOLD}"/></g>')
obj(OY, [(0, A_GO, 'count 2', GOLD), (A_GO, B_GO, 'count 1', GOLD)])
# weak_ptr
y = 228
a(text(20, y - 10, 'weak_ptr · watches, does not own', size=13, fill=MUTED, ls='0'))
S_GO = 7.2
OY = y + 20
a(ghost(20, y, 130)); a(f'<g>{until(S_GO)}{chip(20, y, 130, "owner s", PHOS)}<path d="M150 {y + 17} L{OX - 6} {OY + 12}" stroke="{PHOS}" stroke-width="1.5"/><polygon points="{OX - 7},{OY + 7} {OX},{OY + 13} {OX - 8},{OY + 16}" fill="{PHOS}"/></g>')
a(f'<g>{until(S_GO)}{chip(20, y + 40, 130, "weak w", BLUE, dashed=True)}<path d="M150 {y + 57} L{OX - 6} {OY + 22}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="4 3"/><polygon points="{OX - 8},{OY + 18} {OX},{OY + 21} {OX - 6},{OY + 27}" fill="{BLUE}"/></g>')
a(f'<g>{after(S_GO)}<rect x="20" y="{y + 40}" width="130" height="34" rx="3" fill="{PANEL}" stroke="{RED}" stroke-dasharray="4 3"/>'
  f'{text(85, y + 62, "w: expired", anchor="middle", size=13, fill=RED, ls="0")}</g>')
obj(OY, [(0, S_GO, 'object', PHOS)])
a(text(20, 258, '', size=13))
a('</svg>')
svg = '\n'.join(o).replace(text(20, 258, '', size=13), '')

caption = ('Ownership is part of the type: behind a <code>unique_ptr</code> the object dies with its single owner, behind a <code>shared_ptr</code> when its count of owners reaches zero. '
           'A <code>weak_ptr</code> watches without keeping its object alive, and afterwards reports that it has expired.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The costs.</b> A <code>unique_ptr</code> is as cheap as a raw pointer; a <code>shared_ptr</code> pays for an atomic count updated on every copy.</li>
          <li><b>Moving, not copying.</b> A <code>unique_ptr</code> cannot be copied, only moved, so there is never more than one owner.</li>
          <li><b>Breaking cycles.</b> Two objects holding <code>shared_ptr</code>s to each other never reach zero; making one link a <code>weak_ptr</code> lets both be freed.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-7">
      <div class="diagram-label">Fig 6.7 · Three pointer flavours, three ownership semantics</div>
      {svg}
      <p id="ch6-modern-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-7', 'ch6-modern-p3', card)
