# Fig BR.4 · The MMU (Pass 31, Part I, from an empty script). Job: function. Takeaway: the MMU translates every address
# and checks its permissions, so a forbidden access never reaches memory.
# Concept: the order of the steps, seen: an address leaves the CPU as two parts, page number and offset; inside the MMU
# the page tables swap the page number for a physical one (the offset passes through unchanged), then the permission
# check lets it on to RAM or stops it. Two accesses run in turn (Part I's flow verb): a load that reaches RAM, then a
# store to the next page up, read-only, stopped at the check as a page fault for the kernel. As the ledger asks, no TLB
# is drawn (chBridge-mmu-p5 teaches it after the card) and each access runs the walk. t=0 is the store stopped.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 400
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=10.0)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-46 svgd-part1-46"{T.steps([(4.6, 'load'), (10.4, 'store')])}>')
a('<title id="svgt-part1-46">Fig BR.4 · The MMU · silicon between the CPU and the RAM</title>')
a('<desc id="svgd-part1-46">Two memory accesses through the MMU, each as an address in two parts, the page number and the offset within the '
  'page. A load from virtual address 0x7fff_fa3c_4010: the MMU walks the page tables the kernel wrote and swaps the page number for the '
  'physical page 0x4a200, the offset 010 passing through unchanged; the permission check allows the load, and 0x4a20_0010 goes to RAM. '
  'Then a store to the next page up, 0x7fff_fa3c_5010: the walk succeeds, but that page is read-only, so the store never reaches RAM: '
  'the MMU raises a page fault and the kernel decides what happens next.</desc>')

# CPU, MMU, RAM
a(f'<rect x="20" y="16" width="360" height="46" rx="7" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
a(text(34, 44, 'CPU', size=15, fill=BLUE))
a(f'<rect x="20" y="96" width="360" height="176" rx="8" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
a(text(34, 120, 'MMU', size=15, fill=GOLD))
a(f'<rect x="200" y="322" width="180" height="46" rx="7" fill="none" stroke="{GREEN}" stroke-width="1.5"/>')
a(text(214, 350, 'RAM', size=15, fill=GREEN))
a(f'<rect x="20" y="322" width="150" height="60" rx="7" fill="none" stroke="{RED}" stroke-width="1.5"/>')
a(text(95, 345, 'page fault', anchor='middle', size=14, fill=RED))
a(text(95, 365, 'kernel decides', anchor='middle', size=14, fill=MUTED))
# the two stages inside the MMU, on the left; the address travels down the lane on the right
a(f'<rect x="40" y="134" width="180" height="52" rx="6" fill="none" stroke="{EDGE}"/>')
a(text(52, 155, 'page tables', size=14, fill=INK, ls='0'))
a(text(52, 175, 'page → physical', size=14, fill=MUTED, ls='0'))
a(f'<rect x="40" y="204" width="180" height="52" rx="6" fill="none" stroke="{EDGE}"/>')
a(text(52, 225, 'check the bits', size=14, fill=INK, ls='0'))
a(text(52, 245, 'user? writable?', size=14, fill=MUTED, ls='0'))
a(f'<path d="M 222 160 H 232 M 222 230 H 232" stroke="{EDGE}"/>')

def token(page, off, col, x, y):
    return (f'<rect x="{x}" y="{y}" width="88" height="26" rx="4" fill="none" stroke="{col}" stroke-width="1.6"/>'
            + text(x + 44, y + 18, page, anchor='middle', size=14, fill=col, ls='0', role='object')
            + f'<rect x="{x + 92}" y="{y}" width="46" height="26" rx="4" fill="none" stroke="{INK}" stroke-width="1.6"/>'
            + text(x + 115, y + 18, off, anchor='middle', size=14, fill=INK, ls='0', role='object'))
# which access, named in the CPU
a(f'<g opacity="0">{vis([(0.0, 6.0)])}' + text(90, 44, 'load  0x7fff_fa3c_4010', size=14, fill=INK, ls='0') + '</g>')
a(f'<g opacity="0">{vis([(6.0, D)])}' + text(90, 44, 'store 0x7fff_fa3c_5010', size=14, fill=INK, ls='0') + '</g>')
LX = 238
def run(t0, vpage, ppage, ok):
    """an access: down from the CPU past the tables (page swapped), past the check, then to RAM or stopped"""
    ys = [(0.0, 0), (t0, 0), (t0 + 0.8, 79), (t0 + 1.8, 79), (t0 + 2.4, 149), (t0 + 3.2, 149)]
    if ok: ys += [(t0 + 4.0, 264), (D - 0.01, 264)]
    else: ys += [(D - 0.01, 149)]
    end = t0 + 5.6 if ok else D
    a(f'<g opacity="0">{vis([(t0, end)])}<g>{T.translate(ys, axis="y")}'
      f'<g opacity="0">{vis([(t0, t0 + 1.4)])}{token(vpage, "010", BLUE, LX, 68)}</g>'
      f'<g opacity="0">{vis([(t0 + 1.4, end)])}{token(ppage, "010", GREEN, LX, 68)}</g></g></g>')
    if ok:
        a(f'<g opacity="0">{vis([(t0 + 3.0, t0 + 5.6)])}<path d="M 196 236 l 4 5 l 9 -10" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></g>')
    else:
        a(f'<g opacity="0">{vis([(t0 + 3.0, D)])}<path d="M 194 224 l 12 12 m 0 -12 l -12 12" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>'
          f'<path d="M 200 246 V 306 H 95 V 318 m -5 -7 l 5 7 l 5 -7" fill="none" stroke="{RED}" stroke-width="1.8"/>'
          + text(30, 290, 'read-only: stop', size=14, fill=RED, ls='0') + '</g>')
run(0.4, '…a3c4', '4a200', True)
run(6.2, '…a3c5', '4a201', False)
a(f'<g opacity="0">{vis([(0.0, 6.2)])}' + text(30, 290, 'offset unchanged', size=14, fill=MUTED, ls='0') + '</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every load, store and instruction fetch goes through the MMU, which swaps the page number for a physical one using the '
           'page tables the kernel wrote, then checks the permission bits. If the check fails, nothing reaches RAM: the MMU raises a '
           'page fault and the kernel takes over.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The walk.</b> On x86-64, CR3 holds the top table; nine bits of the address pick an entry at each of four levels, and the last twelve are the offset inside the 4 KiB page.</li>
          <li><b>The bits.</b> Each entry carries present, user/supervisor, writable and no-execute flags; a failed check raises a page fault (vector 14).</li>
          <li><b>The shortcut.</b> Most accesses skip the walk, because recent translations are kept close at hand (Fig BR.5).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-4">
      <div class="diagram-label">Fig BR.4 · The MMU · silicon between the CPU and the RAM</div>
      {svg}
      <p id="chBridge-mmu-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-4', 'chBridge-mmu-p3', card)
