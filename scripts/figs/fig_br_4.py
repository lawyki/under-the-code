# Fig BR.4 · The MMU · silicon between the CPU and the RAM (Pass 28, law 3, conceptual pass). Two accesses through the
# MMU, top to bottom (each to its own page, so each misses the TLB). A load of 0x7fff_a3c4_0010: the TLB misses, the walker reads the four page-table levels from CR3
# down, the permission bits allow it, and the physical address 0x4_a200_0010 (same low 12 bits, the offset in the page)
# goes to RAM. Then a store to a read-only page: the walk succeeds but the check fails, and the MMU raises a page fault
# for the kernel instead of touching RAM. t=0 (shift): both outcomes shown.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

VA, PA = 0x7fffa3c40010, 0x4a2000010
assert VA & 0xfff == PA & 0xfff == 0x010
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
T1 = dict(ask=0.8, tlb=1.4, walk=[2.0, 2.4, 2.8, 3.2], ok=3.8, ram=4.4)      # the load
T2 = dict(ask=6.0, tlb=6.5, walk=[6.9, 7.2, 7.5, 7.8], bad=8.3)              # the store
o = []; a = o.append
def box(x, y, w, h, col, op=0.6):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="{op}"/>')
# CPU
box(20, 14, 360, 54, BLUE)
a(text(32, 36, 'CPU', size=13, fill=BLUE, ls='0'))
a(f'<g opacity="0">{lit(0.31, T2["ask"])}{text(32, 56, "load  0x7fff_a3c4_0010", size=13, fill="#fff", ls="0")}</g>')
a(f'<g opacity="0">{win(T2["ask"])}{text(32, 56, "store 0x7fff_a3c5_0010", size=13, fill="#fff", ls="0")}</g>')
# MMU
MY = 90
box(20, MY, 360, 196, GOLD, 0.8)
a(text(32, MY + 22, 'MMU · a circuit, no code', size=13, fill=GOLD, ls='0'))
box(32, MY + 34, 336, 30, MUTED, 0.5)
a(text(44, MY + 54, 'TLB: recent translations', size=13, fill='#fff', ls='0'))
for t0 in (T1['tlb'], T2['tlb']):
    a(f'<g class="fx" opacity="0">{lit(t0, t0 + 0.5)}{text(356, MY + 54, "miss", anchor="end", size=13, fill=RED, ls="0")}</g>')
a(text(44, MY + 90, 'walk from CR3:', size=13, fill=MUTED, ls='0'))
LX = [44, 128, 212, 296]
for k, (lx, lab) in enumerate(zip(LX, ('L4', 'L3', 'L2', 'L1'))):
    a(f'<rect x="{lx}" y="{MY + 100}" width="72" height="30" rx="5" fill="none" stroke="{GOLD}" stroke-opacity="0.6"/>')
    a(text(lx + 36, MY + 120, lab, anchor='middle', size=13, fill='#fff', ls='0'))
    for t0 in (T1['walk'][k], T2['walk'][k]):
        a(f'<g class="fx" opacity="0">{lit(t0, t0 + 0.4)}<rect x="{lx}" y="{MY + 100}" width="72" height="30" rx="5" fill="{GOLD}" fill-opacity="0.35" stroke="{GOLD}" stroke-width="2"/></g>')
    if k < 3:
        a(f'<path d="M{lx + 72},{MY + 115} h12 m-5,-4 l5,4 l-5,4" fill="none" stroke="{MUTED}"/>')
a(text(44, MY + 162, 'check: present, user, writable?', size=13, fill=MUTED, ls='0'))
a(f'<g opacity="0">{lit(T1["ok"], T2["ask"])}{text(44, MY + 182, "load allowed", size=13, fill=GREEN, ls="0")}</g>')
a(f'<g opacity="0">{win(T2["bad"])}{text(44, MY + 182, "store to a read-only page: no", size=13, fill=RED, ls="0")}</g>')
# the two exits: RAM, or a fault to the kernel
EY = MY + 216
box(20, EY, 170, 52, GREEN)
a(text(32, EY + 21, 'RAM', size=13, fill=GREEN, ls='0'))
a(f'<g opacity="0">{win(T1["ram"])}{text(32, EY + 41, "0x4_a200_0010", size=13, fill="#fff", ls="0")}</g>')
box(210, EY, 170, 52, RED)
a(text(222, EY + 21, 'page fault', size=13, fill=RED, ls='0'))
a(f'<g opacity="0">{win(T2["bad"] + 0.3)}{text(222, EY + 41, "kernel decides", size=13, fill="#fff", ls="0")}</g>')
a(f'<g class="fx" opacity="0">{pulse(T1["ram"])}<rect x="18" y="{EY - 2}" width="174" height="56" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(f'<g class="fx" opacity="0">{pulse(T2["bad"] + 0.3)}<rect x="208" y="{EY - 2}" width="174" height="56" rx="7" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(text(20, EY + 76, 'offset 0x010 unchanged: only the page moves', size=13, fill=MUTED, ls='0'))
H = EY + 88
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-46 svgd-part1-46">')
o.insert(1, '<title id="svgt-part1-46">Fig BR.4 · The MMU · silicon between the CPU and the RAM</title>')
o.insert(2, '<desc id="svgd-part1-46">Two memory accesses through the MMU. A load from virtual address 0x7fff_a3c4_0010 misses the TLB, so the walker reads the four page-table levels starting from CR3; the permission bits allow the load, and the physical address 0x4_a200_0010 goes to RAM, keeping the same offset within the page. '
  'Then a store to the next page up, 0x7fff_a3c5_0010: it misses the TLB too, the walk succeeds, but that page is read-only, so instead of touching RAM the MMU raises a page fault and the kernel decides what happens next.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every load, store and instruction fetch goes through the MMU, which turns the virtual address into a physical one by walking the page tables the kernel wrote, then checks the permission bits. '
           'If the check fails, nothing reaches RAM: the MMU raises a page fault and the kernel takes over.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The walk.</b> On x86-64, CR3 holds the top table; nine bits of the address pick an entry at each of four levels, and the last twelve are the offset inside the 4 KiB page.</li>
          <li><b>The bits.</b> Each entry carries present, user/supervisor, writable and no-execute flags; a failed check raises a page fault (vector 14).</li>
          <li><b>The shortcut.</b> The <span class="key-term">TLB</span> keeps recent answers, so a second access to the same page skips the walk (Fig BR.5).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-4">
      <div class="diagram-label">Fig BR.4 · The MMU · silicon between the CPU and the RAM</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-4"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-4', cap, card.replace('CAPID', cap))
