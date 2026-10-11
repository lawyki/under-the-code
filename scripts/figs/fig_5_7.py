# Fig 5.7 · Leak vs use-after-free (Pass 28, law 3, conceptual pass: the two bugs against the allocator, no exploit).
# Top, the leak: three times a pointer p gets a chunk and then goes out of scope; each chunk stays in use with nothing
# pointing at it, and the heap only grows. Bottom, use-after-free: p gets a chunk, free(p) returns it to the allocator
# while p still points there, the next malloc hands the same chunk to q, and a write through p overwrites q's data.
# t=0 (shift): three leaked chunks; q's data overwritten.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W = 400
D = 13.0
T = Timeline(D, shift=12.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
LINE = 'rgba(198,222,206,0.6)'
o = []; a = o.append
def ptr(x, y, name, col):
    a(f'<rect x="{x}" y="{y}" width="44" height="30" rx="4" fill="{PANEL}" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(x + 22, y + 20, name, anchor='middle', size=13, fill=col, ls='0'))
def chunk(x, y, w, h):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{PLATE}" stroke="rgba(132,255,178,0.5)"/>')
def state(x, y, spans):                       # [(t0, t1|None, text, colour)]
    for t0, t1, s, col in spans:
        vis = win(t0) if t1 is None else (first(t1) if t0 < 0.5 else lit(t0, t1))
        a(f'<g opacity="0">{vis}{text(x, y, s, size=13, fill=col, ls="0")}</g>')
# ── the leak ──
a(text(20, 24, 'leak: allocated, never freed', size=13, fill=GOLD, ls='0'))
LK = [1.0, 2.6, 4.2]                           # p = malloc(64) for the k-th time
GONE = 0.8                                     # p goes out of scope this long after
CX, CW, CH = 196, 184, 30
cy = lambda k: 40 + k * 40
pts = [(0.0, 0.3)]
for t0 in LK:
    pts += [(t0 - 0.002, 0.3), (t0, 1.0), (t0 + GONE - 0.002, 1.0), (t0 + GONE, 0.3)]
pts += [(D, 0.3)]
a(f'<g>{T.anim("opacity", pts)}')
ptr(20, cy(0), 'p', PHOS)
a('</g>')
for k, t0 in enumerate(LK):
    y = cy(k)
    chunk(CX, y, CW, CH)
    state(CX + 12, y + 20, [(0.31, t0, 'free', MUTED), (t0, t0 + GONE, 'in use', PHOS), (t0 + GONE, None, 'in use, no pointer', GOLD)])
    a(f'<g opacity="0">{lit(t0, t0 + GONE)}<path d="M64,{cy(0) + 15} H150 V{y + 15} H{CX}" fill="none" stroke="{PHOS}" stroke-width="2"/></g>')
    a(f'<g class="fx" opacity="0">{pulse(t0 + GONE)}<rect x="{CX - 2}" y="{y - 2}" width="{CW + 4}" height="{CH + 4}" rx="5" fill="none" stroke="{GOLD}" stroke-width="2"/></g>')
a(text(20, cy(1) + 20, 'returns, no free', size=13, fill=MUTED, ls='0'))
a(text(20, cy(3) + 4, 'the heap only grows', size=13, fill=MUTED, ls='0'))
# ── use-after-free ──
UY = 214
a(f'<line x1="20" y1="{UY - 22}" x2="380" y2="{UY - 22}" stroke="{MUTED}" stroke-opacity="0.4"/>')
a(text(20, UY, 'use-after-free: freed, still used', size=13, fill=RED, ls='0'))
TA, TF, TQ, TW = 6.0, 7.4, 8.8, 10.2
PY, QY, KY = UY + 16, UY + 62, UY + 36
ptr(20, PY, 'p', PHOS)
a(f'<g opacity="0">{win(TQ)}</g>')
a(f'<g opacity="0">{win(TQ)}<rect x="20" y="{QY}" width="44" height="30" rx="4" fill="{PANEL}" stroke="{PHOS}" stroke-opacity="0.7"/>{text(42, QY + 20, "q", anchor="middle", size=13, fill=PHOS, ls="0")}</g>')
chunk(CX, KY, CW, 38)
state(CX + 12, KY + 24, [(0.31, TA, 'free', MUTED), (TA, TF, "p's data", PHOS), (TF, TQ, 'free', MUTED), (TQ, TW, "q's data", PHOS), (TW, None, "q's data, overwritten", RED)])
pp = f'M64,{PY + 15} H150 V{KY + 12} H{CX}'
a(f'<g opacity="0">{lit(TA, TF)}<path d="{pp}" fill="none" stroke="{PHOS}" stroke-width="2"/></g>')
a(f'<g opacity="0">{win(TF)}<path d="{pp}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/></g>')
a(f'<g opacity="0">{win(TQ)}<path d="M64,{QY + 15} H150 V{KY + 26} H{CX}" fill="none" stroke="{PHOS}" stroke-width="2"/></g>')
a(f'<g class="fx" opacity="0">{pulse(TW)}<rect x="{CX - 2}" y="{KY - 2}" width="{CW + 4}" height="42" rx="5" fill="{RED}" fill-opacity="0.25" stroke="{RED}" stroke-width="2"/></g>')
SY = QY + 58
state(20, SY, [(0.31, TA, 'p = malloc(64)', '#fff'), (TA, TF, 'p = malloc(64)', '#fff'), (TF, TQ, 'free(p): p still points here', GOLD),
               (TQ, TW, 'q = malloc(64): the same chunk', PHOS), (TW, None, 'write through p: q is hit', RED)])
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-31 svgd-part2-31">')
o.insert(1, '<title id="svgt-part2-31">Fig 5.7 · Leak vs use-after-free</title>')
o.insert(2, '<desc id="svgd-part2-31">Two ways to get malloc and free wrong. A leak: three times, the pointer p is given a chunk and then goes out of scope without free; each chunk stays marked in use with nothing pointing at it, and the heap only grows. '
  'A use-after-free: p is given a chunk, free(p) hands it back to the allocator while p still points at it, the next malloc gives the same chunk to q, and a write through p overwrites q\'s data.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A leak loses the last pointer to memory that is still allocated, so the heap only grows until the OS ends the process. '
           'A use-after-free keeps a pointer to memory already given back: the allocator hands that chunk to the next caller, and every write through the old pointer overwrites their data.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why the same chunk.</b> Allocators reuse recently freed chunks of the right size first, because they are likely still in the cache, so the next <code>malloc(64)</code> often gets exactly the chunk just freed.</li>
          <li><b>Finding them.</b> Valgrind and AddressSanitizer track every allocation: they report leaks when the program exits and a use-after-free when it happens, as long as the freed chunk has not yet been reused.</li>
          <li><b>Defences.</b> Setting <code>p = NULL</code> after <code>free(p)</code> turns a later use into an immediate crash; hardened allocators delay reuse; in safe Rust, the ownership rules reject use-after-free at compile time.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-7">
      <div class="diagram-label">Fig 5.7 · Leak vs use-after-free</div>
      {svg}
      <p id="ch5-malloc-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-7', 'ch5-malloc-p6', card)
