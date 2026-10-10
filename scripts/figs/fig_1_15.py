# Fig 1.15 · The hierarchy of forgetting (Pass 28, law 3).
# Bar length = size on a log scale (stated). Right column = access time at human
# scale: 0.3 ns (one register access) becomes 1 s, every ratio kept.
# Motion: read 1 misses every cache and finds the data in RAM, leaving copies on the
# way up; read 2 hits L1. The still (t=0) is the end state: copies in place, both results.
import math
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 500
X0, ROW, BH, Y0 = 20, 46, 36, 64
LEVELS = [  # name, bytes, ns, human, colour
    ('REGISTERS', 1e3, 0.3, '1 s', GOLD),
    ('L1 CACHE', 64e3, 1, '3 s', GOLD),
    ('L2 CACHE', 1e6, 4, '13 s', GOLD),
    ('L3 CACHE', 32e6, 13, '43 s', GOLD),
    ('RAM', 16e9, 60, '3 min', BLUE),
    ('SSD', 1e12, 50_000, '2 days', GREEN),
    ('HDD', 10e12, 5_000_000, '6 months', RED),
]
for name, b, ns, human, _ in LEVELS:      # the human column is the ns column ×(1 s / 0.3 ns)
    s = ns / 0.3
    assert {'1 s': 1, '3 s': 3.3, '13 s': 13.3, '43 s': 43.3, '3 min': 200, '2 days': 166_667, '6 months': 16_666_667}[human] == round(s, 1) or abs(math.log10(s) - math.log10({'1 s': 1, '3 s': 3, '13 s': 13, '43 s': 43, '3 min': 180, '2 days': 172_800, '6 months': 15_552_000}[human])) < 0.1, name
def width(b): return 124 + (math.log10(b) - 3) / 10 * 138      # 1 KB -> 124, 10 TB -> 262
def ry(i): return Y0 + i * ROW

T = Timeline(10, shift=8.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-16 svgd-part1-16">')
a('<title id="svgt-part1-16">Fig 1.15 · The hierarchy of forgetting · bigger and slower at every step</title>')
a('<desc id="svgd-part1-16">Seven levels from registers to hard disk, each bar longer (more capacity, log scale) and slower. '
  'If a register access took one second, L1 would take 3 seconds, L2 13, L3 43, RAM 3 minutes, an SSD 2 days and a hard disk 6 months. '
  'A first read misses every cache and fetches from RAM, leaving copies in L3, L2 and L1; a second read of the same data stops at L1.</desc>')
a(text(X0, 34, 'SIZE →', fill=MUTED))
a(text(380, 34, '0.3 ns = 1 s', anchor='end', fill=GOLD))
for i, (name, b, ns, human, col) in enumerate(LEVELS):
    y = ry(i); w = width(b)
    a(f'<rect x="{X0}" y="{y}" width="{w:.1f}" height="{BH}" rx="4" fill="{col}" fill-opacity="{0.42 - i * 0.03:.2f}" stroke="{col}" stroke-opacity="0.8"/>')
    a(text(X0 + 26, y + 24, name, size=14, fill='#fff', ls='0.04em'))
    a(text(380, y + 24, human, anchor='end', size=15, fill='rgba(255,255,255,0.85)' if i < 5 else 'rgba(255,255,255,0.95)'))
a(text(X0, ry(6) + BH + 26, 'bar length: size, log scale', fill='rgba(255,255,255,0.45)'))

# copies of the data in L3, L2, L1: drawn in the still; they appear on the way up in read 1
for i, lvl in ((3, 2.7), (2, 3.0), (1, 3.3)):
    y = ry(i); x = X0 + width(LEVELS[i][1]) - 20
    a(f'<rect x="{x:.1f}" y="{y + 11}" width="14" height="14" rx="2" fill="#fff">{T.anim("opacity", [(0.0, 0.0), (lvl, 0.0), (lvl + 0.15, 1.0), (9.4, 1.0), (9.8, 0.0)])}</rect>')
a(f'<rect x="{X0 + width(LEVELS[4][1]) - 20:.1f}" y="{ry(4) + 11}" width="14" height="14" rx="2" fill="#fff"/>')   # the data lives in RAM

# miss / hit outlines
def ring(i, t0, t1, col):          # the outline, and the word: colour is never the only cue
    y = ry(i); w = width(LEVELS[i][1])
    op = T.anim("opacity", [(0.0, 0.0)] + T.pulse(t0, t1, 0.1) + [(10.0, 0.0)])
    word = 'miss' if col == RED else 'found'
    return (f'<rect x="{X0 - 3}" y="{y - 3}" width="{w + 6:.1f}" height="{BH + 6}" rx="6" fill="none" stroke="{col}" stroke-width="2.5" opacity="0">{op}</rect>'
            f'<text x="{X0 + w + 12:.1f}" y="{y + 24}" {MONO} font-size="14" fill="{col}" opacity="0">{word}{op}</text>')
for i, t0 in ((1, 0.7), (2, 1.0), (3, 1.3)): a(ring(i, t0, t0 + 0.5, RED))
a(ring(4, 1.7, 2.6, GREEN))
a(ring(1, 5.9, 6.8, GREEN))

# the request: a dot that runs down the left edge until it finds the data, then back
DX = X0 + 12
def dot(pts):                       # pts: [(tau, y)] ; visible between first and last
    on = [(0.0, 0.0), (pts[0][0] - 0.05, 0.0), (pts[0][0], 1.0), (pts[-1][0], 1.0), (pts[-1][0] + 0.05, 0.0), (10.0, 0.0)]
    cy = [(0.0, pts[0][1])] + pts + [(10.0, pts[0][1])]
    return f'<circle cx="{DX}" r="5" fill="#fff" opacity="0">{T.anim("cy", cy)}{T.anim("opacity", on)}</circle>'
a(dot([(0.4, ry(0) + 18), (0.7, ry(1) + 18), (1.0, ry(2) + 18), (1.3, ry(3) + 18), (1.7, ry(4) + 18), (2.6, ry(4) + 18), (3.4, ry(0) + 18)]))
a(dot([(5.5, ry(0) + 18), (5.9, ry(1) + 18), (6.5, ry(1) + 18), (6.8, ry(0) + 18)]))

# results: both reads, always shown; the current one is outlined
by = ry(6) + BH + 52
for k, (head, where, col, t0, t1) in enumerate((('1st read', 'RAM · 3 min', BLUE, 1.7, 5.3), ('2nd read', 'L1 · 3 s', GOLD, 5.9, 9.4))):
    bx = X0 + k * 184
    a(f'<rect x="{bx}" y="{by}" width="176" height="56" rx="6" fill="#0f0f0f" stroke="rgba(255,255,255,0.18)"/>')
    a(f'<rect x="{bx}" y="{by}" width="176" height="56" rx="6" fill="none" stroke="{col}" stroke-width="1.8" opacity="0">{T.anim("opacity", [(0.0, 0.0)] + T.pulse(t0, t1) + [(10.0, 0.0)])}</rect>')
    a(text(bx + 14, by + 22, head, fill=MUTED))
    a(text(bx + 14, by + 44, where, size=16, fill=col))
a('</svg>')
svg = '\n'.join(o)

caption = ('Each level down is bigger and far slower: at a scale where a register answers in one second, a hard disk takes six months. '
           'A cache keeps a copy of what was just read, so reading it again costs seconds, not minutes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The scale.</b> One register access, about 0.3 ns, becomes one second; every other time keeps its ratio to it. Bar length is size on a log scale.</li>
          <li><b>A miss.</b> The first read looks in L1, L2 and L3, finds nothing, and waits for RAM: about 60 ns.</li>
          <li><b>A copy.</b> On the way back each cache keeps a copy of the data and its neighbours.</li>
          <li><b>A hit.</b> The next read of the same data, or of data next to it, stops at L1: about 1 ns.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-15">
      <div class="diagram-label">Fig 1.15 · The hierarchy of forgetting · bigger and slower at every step</div>
      {svg}
      <p id="ch1-memory-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-15', 'ch1-memory-p3', card)
