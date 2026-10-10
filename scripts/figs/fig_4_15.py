# Fig 4.15 · A pipe is a kernel ring buffer (Pass 28, law 3). Eight cells in a ring; the write
# pointer and the read pointer step around it (stepped, the Greenbar idiom). cat fills the ring until
# it is full and blocks; grep drains it, cat resumes, then grep empties it and blocks.
# t=0 (shift): the ring full, the writer blocked.
import math
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 462
CX, CY, RAD, CELL = 200, 231, 84, 40
N = 8
STEP, T0 = 0.36, 0.5
OPS = 'wwww' + 'r' + 'wwwww' + 'bbb' + 'rrr' + 'ww' + 'rrrrrrr' + 'eee'
STREAM = 'ERROR: disk full '
# simulate
events, wptr, rptr, count, nw = [], 0, 0, 0, 0
cells = {}                      # write index -> (cell, char, t_write, t_read)
writes = []                     # [cell, char, tw, tr]
wpos, rpos, blocked_w, blocked_r = [(0.0, 0)], [(0.0, 0)], [], []
for s, op in enumerate(OPS):
    t = T0 + s * STEP
    if op == 'w':
        assert count < N
        writes.append([wptr, STREAM[nw % len(STREAM)], t, None]); nw += 1
        wptr = (wptr + 1) % N; count += 1; wpos.append((t, wptr))
    elif op == 'r':
        assert count > 0
        w = next(x for x in writes if x[3] is None)
        w[3] = t; rptr = (rptr + 1) % N; count -= 1; rpos.append((t, rptr))
    elif op == 'b':
        assert count == N; blocked_w.append(t)
    elif op == 'e':
        assert count == 0; blocked_r.append(t)
END = T0 + len(OPS) * STEP
D = round(END + 1.2, 2)
SHIFT = blocked_w[1]
T = Timeline(D, shift=SHIFT)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def intervals(pos, k):
    out = []
    for (t0, p), nxt in zip(pos, pos[1:] + [(D, None)]):
        if p == k: out.append((t0, nxt[0]))
    return out
def ang(k): return math.radians(-90 + 360 / N * k)
def cxy(k): return CX + RAD * math.cos(ang(k)), CY + RAD * math.sin(ang(k))

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-16 svgd-part2-16">')
a('<title id="svgt-part2-16">Fig 4.15 · A pipe is a kernel ring buffer with two ends</title>')
a('<desc id="svgd-part2-16">A pipe drawn as a ring of eight cells in the kernel. The writer, cat server.log, puts bytes in at the write pointer, which steps round the ring; '
  'the reader, grep ERROR, takes them out at the read pointer, which follows it. When the ring is full the writer is blocked until the reader frees a cell; '
  'when the ring is empty the reader is blocked until the writer adds one. A real pipe on Linux holds 64 KB by default.</desc>')
# processes
for y, who, cmd in ((14, 'writer', 'cat server.log'), (H - 62, 'reader', 'grep ERROR')):
    a(f'<rect x="96" y="{y}" width="208" height="46" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.4)"/>')
    a(text(110, y + 19, who, size=13, fill=MUTED, ls='0'))
    a(text(110, y + 37, cmd, size=14, fill='#fff', ls='0'))
for t in blocked_w:
    pass
def blocked_tag(y, word, ts):
    a(f'<g opacity="0">{lit(ts[0], ts[-1] + STEP)}<rect x="312" y="{y}" width="76" height="46" rx="3" fill="{RED}" fill-opacity="0.15" stroke="{RED}"/>'
      f'{text(350, y + 19, "blocked", anchor="middle", size=13, fill=RED, ls="0")}{text(350, y + 37, word, anchor="middle", size=13, fill=RED, ls="0")}</g>')
blocked_tag(14, 'full', blocked_w)
blocked_tag(H - 62, 'empty', blocked_r)
# ring
a(f'<circle cx="{CX}" cy="{CY}" r="{RAD}" fill="none" stroke="rgba(132,255,178,0.18)" stroke-width="1.5"/>')
a(text(CX, CY - 2, 'kernel', anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(CX, CY + 16, 'buffer', anchor='middle', size=13, fill=MUTED, ls='0'))
for k in range(N):
    x, y = cxy(k)
    a(f'<rect x="{x - CELL / 2:.1f}" y="{y - CELL / 2:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.3)"/>')
for cell, ch, tw, tr in writes:
    x, y = cxy(cell)
    tr = tr if tr is not None else D
    glyph = '·' if ch == ' ' else ch
    a(f'<g opacity="0">{lit(tw, tr)}<rect x="{x - CELL / 2:.1f}" y="{y - CELL / 2:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{PHOS}" fill-opacity="0.3" stroke="{PHOS}"/>'
      f'{text(x, y + 6, glyph, anchor="middle", size=17, fill="#fff", ls="0")}</g>')
# pointers, just outside the ring, write a little ahead of read
for name, pos, off, col in (('write', wpos, -16, PHOS), ('read', rpos, 16, PHOS_SOFT)):
    for k in range(N):
        th, tc = ang(k) + math.radians(off), ang(k)
        lx, ly = CX + 162 * math.cos(th), CY + 158 * math.sin(th)
        x1, y1 = CX + 134 * math.cos(th), CY + 134 * math.sin(th)
        x2, y2 = CX + 110 * math.cos(tc), CY + 110 * math.sin(tc)
        al = math.atan2(y2 - y1, x2 - x1)
        hd = [(x2, y2), (x2 - 7 * math.cos(al - 0.5), y2 - 7 * math.sin(al - 0.5)), (x2 - 7 * math.cos(al + 0.5), y2 - 7 * math.sin(al + 0.5))]
        g = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.5"/>'
             '<polygon points="' + ' '.join(f'{px:.1f},{py:.1f}' for px, py in hd) + f'" fill="{col}"/>'
             + text(lx, ly + 5, name, anchor='middle', size=13, fill=col, ls='0'))
        for t0, t1 in intervals(pos, k):
            pts = [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)] if t0 > 0 else \
                  [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)]
            a(f'<g opacity="0">{T.anim("opacity", pts)}{g}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A pipe is a ring buffer in the kernel with a write end and a read end. '
           'When the ring is full the writer blocks until the reader frees space, and when it is empty the reader blocks until bytes arrive: flow control with no locks in either program.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Two descriptors.</b> <code>pipe()</code> returns one file descriptor for each end; the shell wires the writer's standard output to one and the reader's standard input to the other.</li>
          <li><b>The size.</b> A Linux pipe holds 64 KB by default, so a fast writer runs ahead of a slow reader by at most that much.</li>
          <li><b>The lineage.</b> Doug McIlroy pressed for pipes for years; Ken Thompson added them to UNIX in 1973, and every shell pipeline since runs on this mechanism.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-15">
      <div class="diagram-label">Fig 4.15 · A pipe is a kernel ring buffer with two ends</div>
      {svg}
      <p id="ch4-ipc-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print('D', D, 'shift', SHIFT, 'writes', len(writes))
    splice('part-2', 'fig-4-15', 'ch4-ipc-p4', card)
