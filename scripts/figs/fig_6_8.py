# Fig 6.8 · A move (Pass 28, law 3). Greenbar paper card. Two vector headers over one heap buffer.
# std::move copies v1's three pointers into v2, points v2 at the buffer and nulls v1: the million
# ints never move. t=0 (shift): after the move.
import figlib
from figlib import Timeline, text, splice, PLEX
figlib.FONT = PLEX

INK, INK_SOFT, GB, AMBER, RED = '#1d2b22', 'rgba(29,43,34,0.62)', '#2e6f52', '#8a5a00', '#b3261e'
BOX = '#f5f8f3'
W, H = 400, 288
D = 8.0
T = Timeline(D, shift=6.0)
RESET = 7.6
FIELDS = [('begin', '0xA000'), ('end', 'begin+1M'), ('cap', 'begin+1M')]
CP = [0.8, 1.3, 1.8]; V2ARROW = 2.4; NULLED = 3.0
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def until(t1):
    return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (RESET - 0.002, 0.0), (RESET, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-44 svgd-part2-44">')
a('<title id="svgt-part2-44">Fig 6.8 · A move is &quot;I\'m done with this, take it&quot;</title>')
a('<desc id="svgd-part2-44">auto v2 = std::move(v1); Two vector objects, each three pointers: begin, end and capacity. Before the move, v1\'s pointers lead to a heap buffer of one million ints, 4 MB, and v2 is empty. '
  'The move copies v1\'s three pointers into v2 one by one, so v2 now leads to the same buffer, then sets v1\'s pointers to null. No int is copied and nothing is allocated; v1 is left empty but valid.</desc>')
a(text(20, 24, 'auto v2 = std::move(v1);', size=14, fill=INK, ls='0'))
def header(x, name):
    a(text(x, 52, name, size=14, fill=INK, ls='0'))
    a(f'<rect x="{x}" y="60" width="160" height="96" rx="3" fill="{BOX}" stroke="rgba(29,43,34,0.4)"/>')
    for k in (1, 2):
        a(f'<line x1="{x}" y1="{60 + 32 * k}" x2="{x + 160}" y2="{60 + 32 * k}" stroke="rgba(29,43,34,0.15)"/>')
for x, nm in ((20, 'v1'), (220, 'v2')):
    header(x, nm)
for k, (f, val) in enumerate(FIELDS):
    y = 81 + 32 * k
    # v1: value until nulled, then null
    a(f'<g>{until(NULLED)}{text(30, y, f"{f} = {val}", size=13, fill=INK, ls="0")}</g>')
    a(f'<g opacity="0">{win(NULLED, RESET)}{text(30, y, f"{f} = null", size=13, fill=RED, ls="0")}</g>')
    # v2: null until copied, then the value
    a(f'<g>{until(CP[k])}{text(230, y, f"{f} = null", size=13, fill=INK_SOFT, ls="0")}</g>')
    a(f'<g opacity="0">{win(CP[k], RESET)}{text(230, y, f"{f} = {val}", size=13, fill=GB, ls="0")}</g>')
    a(f'<rect class="fx" x="220" y="{60 + 32 * k}" width="160" height="32" fill="{GB}" fill-opacity="0.18" opacity="0">{win(CP[k], CP[k] + 0.5)}</rect>')
# the heap buffer
a(f'<rect x="20" y="206" width="360" height="40" rx="3" fill="rgba(46,111,82,0.12)" stroke="{GB}"/>')
a(text(200, 231, 'heap: 1,000,000 ints, 4 MB', anchor='middle', size=13, fill=INK, ls='0'))
def arrow(x1, x2, col):
    return (f'<line x1="{x1}" y1="156" x2="{x2}" y2="198" stroke="{col}" stroke-width="2"/>'
            f'<polygon points="{x2 - 5},{196} {x2 + 5},{196} {x2},{205}" fill="{col}"/>')
a(f'<g>{until(NULLED)}{arrow(100, 150, INK)}</g>')
a(f'<g opacity="0">{win(V2ARROW, RESET)}{arrow(300, 250, GB)}</g>')
# result line
a(f'<g opacity="0">{win(NULLED + 0.4, RESET)}{text(20, 276, "3 pointers copied, 3 nulled, 0 ints moved", size=13, fill=GB, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Moving a vector copies its three pointers into the new owner and nulls the old ones; the million ints stay exactly where they are. '
           'The cost is the same for ten elements or ten million, and <code>v1</code> is left empty but still valid.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A copy instead.</b> <code>auto v2 = v1;</code> would allocate another 4 MB and copy every int into it.</li>
          <li><b><code>std::move</code> moves nothing.</b> It only marks <code>v1</code> as finished with, so the compiler picks the moving constructor over the copying one.</li>
          <li><b>Returning by value.</b> A local vector returned from a function is moved out, or built in place, so returning large containers is cheap.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-6-8">
      <div class="diagram-label">Fig 6.8 · A move is "I'm done with this, take it"</div>
      {svg}
      <p id="ch6-modern-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-8', 'ch6-modern-p5', card)
