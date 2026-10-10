# Fig 4.18 · Two processes, one region, one gate (Pass 28, law 3). A and B map the same physical page;
# a semaphore holding 1 lets one in at a time. A takes the 1 and writes; B finds 0 and sleeps; A's
# sem_post wakes B, which enters. t=0 (shift): A in the page, B blocked at the gate, value 0.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 304
D = 12.0
T = Timeline(D, shift=3.0)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-19 svgd-part2-19">')
a('<title id="svgt-part2-19">Fig 4.18 · Two processes, one region, one gate</title>')
a('<desc id="svgd-part2-19">Process A maps physical page 0x4000 at its virtual address 0x7f2a1000; process B maps the same page at 0x55e0c000. Between them and the page stands a semaphore holding 1. '
  'A calls sem_wait, takes the 1 (the value drops to 0) and writes to the page. B calls sem_wait, finds 0 and sleeps. A calls sem_post, the value returns to 1, B wakes, takes it and writes. '
  'When B calls sem_post the gate is open again.</desc>')
for x, who, addr in ((20, 'process A', 'at 0x7f2a1000'), (220, 'process B', 'at 0x55e0c000')):
    a(f'<rect x="{x}" y="14" width="160" height="50" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.4)"/>')
    a(text(x + 12, 34, who, size=13, fill='#fff', ls='0'))
    a(text(x + 12, 53, addr, size=13, fill=MUTED, ls='0'))
# mapping lines to the shared page
a(f'<path d="M40 64 L118 196" stroke="rgba(198,222,206,0.35)" stroke-width="1.5" stroke-dasharray="4 4"/>')
a(f'<path d="M360 64 L282 196" stroke="rgba(198,222,206,0.35)" stroke-width="1.5" stroke-dasharray="4 4"/>')
# gate
a(text(200, 98, 'semaphore', anchor='middle', size=13, fill=GOLD, ls='0'))
a(f'<rect x="140" y="106" width="120" height="44" rx="3" fill="{PLATE}" stroke="{GOLD}" stroke-opacity="0.7"/>')
VALS = [(0.0, 1.0, '1'), (1.0, 3.6, '0'), (3.6, 4.0, '1'), (4.0, 6.0, '0'), (6.0, D, '1')]
for t0, t1, v in VALS:
    pts = [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)] if t0 == 0.0 else \
          [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)]
    if t1 == D: pts = [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)]
    a(f'<g opacity="0">{T.anim("opacity", pts)}{text(200, 135, v, anchor="middle", size=18, fill=GOLD, ls="0")}</g>')
# shared page
a(f'<rect x="110" y="196" width="180" height="54" rx="3" fill="{PLATE}" stroke="{PHOS}" stroke-opacity="0.7"/>')
a(text(200, 270, 'shared page 0x4000', anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
# B blocked
a(f'<circle class="fx" cx="230" cy="128" r="17" fill="none" stroke="{RED}" stroke-width="2.5" opacity="0">{lit(2.25, 4.0)}</circle>')
# tokens: home -> gate -> page -> home, short slides
def moves(home, gate, page, t_gate, t_page, t_home):
    S = 0.25
    xs = [(0.0, home[0]), (t_gate, home[0]), (t_gate + S, gate[0]), (t_page, gate[0]), (t_page + S, page[0]), (t_home, page[0]), (t_home + S, home[0]), (D, home[0])]
    ys = [(0.0, home[1]), (t_gate, home[1]), (t_gate + S, gate[1]), (t_page, gate[1]), (t_page + S, page[1]), (t_home, page[1]), (t_home + S, home[1]), (D, home[1])]
    return T.translate(xs, 'x'), T.translate(ys, 'y')
for name, home, gate, page, tg, tp, th in (('A', (100, 82), (168, 128), (168, 223), 0.6, 1.4, 3.6), ('B', (300, 82), (230, 128), (232, 223), 2.0, 4.2, 6.0)):
    mx, my = moves(home, gate, page, tg, tp, th)
    a(f'<g class="fx">{mx}<g>{my}<circle r="13" fill="{PHOS}" fill-opacity="0.3" stroke="{PHOS}" stroke-width="1.5"/>'
      f'{text(0, 5, name, anchor="middle", size=14, fill="#fff", ls="0")}</g></g>')
# status
STAT = [(0.4, 1.4, 'A: sem_wait() takes the 1'), (1.4, 2.0, 'A writes the shared page'), (2.0, 3.6, 'B: sem_wait() finds 0, sleeps'),
        (3.6, 4.2, 'A: sem_post(); B wakes'), (4.2, 6.0, 'B writes the shared page'), (6.0, 11.6, 'B: sem_post(); the gate is open')]
for t0, t1, s in STAT:
    a(f'<g opacity="0">{lit(t0, t1)}{text(200, 294, s, anchor="middle", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Both processes map the same physical page at different virtual addresses, so what one stores the other can load, with no copy and no system call. '
           'A semaphore holding 1 lets one in at a time: A takes the 1, B finds 0 and sleeps, and A\'s <code>sem_post()</code> wakes it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The mapping.</b> <code>shm_open()</code> and <code>mmap()</code> put the same physical pages into both address spaces; after that the region is ordinary memory.</li>
          <li><b>The fast path.</b> On Linux, <code>sem_wait()</code> and <code>sem_post()</code> are atomic instructions on a counter in shared memory; the kernel is called only when someone must sleep or be woken.</li>
          <li><b>Counting.</b> A semaphore started at N admits N at once, a pool rather than a lock. The idea is Dijkstra's, from 1965.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-18">
      <div class="diagram-label">Fig 4.18 · Two processes, one region, one gate</div>
      {svg}
      <p id="ch4-ipc-p13" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-18', 'ch4-ipc-p13', card)
