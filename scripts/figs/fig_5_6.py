# Fig 5.6 · The heap, as a free list (Pass 28, law 3). Five allocations, two frees, and a request for
# 300 bytes checked against each free chunk in turn: 400 bytes free, none of the pieces big enough.
# Every free piece is fenced by used chunks, so no coalescing could rescue it.
# t=0 (shift): the failed request, the whole story drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

CHUNKS = [('p1', 64), ('p2', 128), ('p3', 32), ('p4', 96), ('p5', 64), ('', 176)]
TOTAL = sum(n for _, n in CHUNKS)
assert TOTAL == 560
FREED = {'p2', 'p4'}
REQ = 300
free_sizes = [n for nm, n in CHUNKS if nm in FREED or nm == '']
assert sum(free_sizes) == 400 and max(free_sizes) < REQ
W, H = 400, 220
X0, S = 20, 360 / TOTAL
RY, RH = 64, 40
D = 12.0
T = Timeline(D, shift=9.2)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
ALLOC = [0.6 + 0.4 * k for k in range(5)]
FREE_T = {'p2': 3.2, 'p4': 3.8}
LIST_T = 4.4
CHECK = [5.2, 6.2, 7.2]
FAIL_T = 8.0
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-30 svgd-part2-30">')
a('<title id="svgt-part2-30">Fig 5.6 · The heap, as a free list</title>')
a('<desc id="svgd-part2-30">A heap of 560 bytes. Five allocations take 64, 128, 32, 96 and 64 bytes, leaving 176 free at the end. p2 and p4 are freed. '
  'The free list now links three chunks of 128, 96 and 176 bytes, 400 bytes in all, each separated from the next by memory still in use. '
  'A request for 300 bytes is checked against each free chunk in turn and fits none of them, so the allocator must ask the kernel for more.</desc>')
a(text(X0, 20, 'HEAP · 560 bytes', size=13, fill=MUTED))
a(f'<rect x="{X0}" y="{RY}" width="360" height="{RH}" fill="{PLATE}" stroke="rgba(132,255,178,0.3)"/>')
off = 0
cx = {}
free_idx = 0
for k, (nm, n) in enumerate(CHUNKS):
    x, w = X0 + off * S, n * S
    cx[k] = (x, w)
    if nm:
        ta = ALLOC[k]
        tf = FREE_T.get(nm)
        # used: from its malloc until its free (or the loop's end)
        a(f'<g>{win(ta, tf) if tf else held(ta)}<rect x="{x:.1f}" y="{RY}" width="{w:.1f}" height="{RH}" fill="{PHOS}" fill-opacity="0.3" stroke="{PHOS}"/>'
          f'{text(x + w / 2, RY + 17, nm, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
    a(text(x + w / 2, RY + 34, str(n), anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
    off += n
    if nm in FREED or nm == '':
        # free: dashed; the tail is free from the start
        t0 = FREE_T.get(nm, 0.0)
        fx = f'<rect x="{x + 1:.1f}" y="{RY + 1}" width="{w - 2:.1f}" height="{RH - 2}" fill="none" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="4 3"/>'
        a(f'<g>{held(t0) if t0 else T.anim("opacity", [(0.0, 1.0), (D, 1.0)])}{fx}</g>')
        if nm: a(f'<g>{held(t0)}{text(x + w / 2, RY + 17, "free", anchor="middle", size=13, fill=GOLD, ls="0")}</g>')
        else: a(text(x + w / 2, RY + 17, 'free', anchor='middle', size=13, fill=GOLD, ls='0'))
        # the check of a 300-byte request against this chunk
        t = CHECK[free_idx]; free_idx += 1
        a(f'<rect class="fx" x="{x:.1f}" y="{RY - 3}" width="{w:.1f}" height="{RH + 6}" fill="{RED}" fill-opacity="0.18" stroke="{RED}" stroke-width="2.5" opacity="0">{win(t, t + 0.9)}</rect>')
# free list links above the ribbon
fx_list = [k for k, (nm, _) in enumerate(CHUNKS) if nm in FREED or nm == '']
a(f'<g>{held(LIST_T)}')
a(text(X0, 46, 'free list', size=13, fill=GOLD, ls='0'))
for i0, i1 in zip(fx_list, fx_list[1:]):
    x0 = cx[i0][0] + cx[i0][1] / 2; x1 = cx[i1][0] + cx[i1][1] / 2
    a(f'<path d="M{x0:.1f} {RY - 2} C{x0:.1f} {RY - 22} {x1:.1f} {RY - 22} {x1:.1f} {RY - 6}" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
    a(f'<polygon points="{x1 - 4:.1f},{RY - 11} {x1 + 4:.1f},{RY - 11} {x1:.1f},{RY - 4}" fill="{GOLD}"/>')
a('</g>')
# the request, as a ruler
QY = 126
a(f'<g>{held(CHECK[0])}<rect x="{X0}" y="{QY}" width="{REQ * S:.1f}" height="26" rx="2" fill="{RED}" fill-opacity="0.15" stroke="{RED}"/>'
  f'{text(X0 + 10, QY + 18, "malloc(300)", size=13, fill="#fff", ls="0")}</g>')
STAT = [(0.4, 3.2, 'five mallocs', PHOS_SOFT), (3.2, 4.4, 'free(p2), free(p4)', GOLD), (4.4, 5.2, '400 bytes free, in three pieces', GOLD),
        (5.2, FAIL_T, 'checking each free chunk', RED), (FAIL_T, 11.6, 'none fits: ask the kernel for more', RED)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(X0, 182, s, size=13, fill=col, ls="0")}</g>')
a(f'<g>{held(FAIL_T)}{text(X0, 206, "largest free piece: 176 B", size=13, fill=MUTED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('After five allocations and two frees the heap holds 400 free bytes in three pieces, and a request for 300 fits none of them. '
           'The heap is <span class="key-term">fragmented</span>: free memory in pieces too small to use, so the allocator must ask the kernel for more.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The list.</b> Each free chunk stores, inside its own unused bytes, a pointer to the next free chunk; the allocator walks that list to find room.</li>
          <li><b>Coalescing.</b> Freeing a chunk next to free space merges the two. Here every free piece is fenced by a chunk still in use, so nothing can merge.</li>
          <li><b>Strategies.</b> First fit, best fit and size-class bins (glibc's ptmalloc, jemalloc) trade speed against fragmentation.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-6">
      <div class="diagram-label">Fig 5.6 · The heap, as a free list</div>
      {svg}
      <p id="ch5-malloc-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-6', 'ch5-malloc-p4', card)
