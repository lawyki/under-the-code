# Fig 6.5 · RAII (Pass 28, law 3). A C++ function with an execution cursor; each resource appears as
# its line runs. Run 1 returns normally, run 2 throws inside parse(); both unwind the same way, the
# destructors running in reverse: unlock, free, close. t=0 (shift): all three held, cursor at parse().
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 300
CODE = ['int do_thing() {', '  std::ifstream f{"x"};', '  std::vector&lt;char&gt; buf(1024);', '  std::lock_guard lock{m};',
        '  parse(buf, f);', '  write(buf);', '  return 0;', '}']
RES = [('ifstream f', 'file open', '~ifstream: close'), ('vector buf', '1024 bytes', '~vector: free'), ('lock_guard', 'm locked', '~lock_guard: unlock')]
LY = lambda i: 34 + i * 20
D = 12.0
T = Timeline(D, shift=2.42)
def win(t0, t1):
    assert t1 > t0 + 0.01, (t0, t1)
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
# run 1: lines 1..6 then return; run 2: lines 1..4, throw at line 4
R1 = [0.4 + 0.45 * k for k in range(1, 7)]           # cursor on lines 1..6
R1_UNW = [R1[-1] + 0.6 + 0.5 * k for k in range(3)]  # lock, buf, f
R2_0 = 6.6
R2 = [R2_0 + 0.45 * k for k in range(4)]             # lines 1..4
THROW = R2[-1]
R2_UNW = [THROW + 0.8 + 0.5 * k for k in range(3)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-41 svgd-part2-41">')
a('<title id="svgt-part2-41">Fig 6.5 · RAII: scope acquires, scope releases</title>')
a('<desc id="svgd-part2-41">A C++ function opens a file with std::ifstream, allocates a buffer with std::vector and locks a mutex with std::lock_guard, then calls parse and write and returns. '
  'Each object acquires its resource as its line runs. On return, the destructors run in reverse order: the lock is released, the buffer freed, the file closed. '
  'In a second run parse throws an exception, and the same three destructors run in the same reverse order as the exception leaves the function. No cleanup code is written.</desc>')
a(f'<rect x="20" y="14" width="360" height="{LY(len(CODE) - 1) + 12 - 14}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.4)"/>')
# cursor
def cursor(i, t0, t1, col=PHOS):
    a(f'<rect class="fx" x="24" y="{LY(i) - 14}" width="352" height="19" rx="2" fill="{col}" fill-opacity="0.2" opacity="0">{win(t0, t1)}</rect>')
for k in range(6):
    cursor(k + 1, R1[k], R1[k + 1] if k < 5 else R1_UNW[-1] + 0.4)
for k in range(3):                                   # line 4 is the throw, drawn red below
    cursor(k + 1, R2[k], R2[k + 1], PHOS)
cursor(4, THROW, R2_UNW[-1] + 0.4, RED)
for i, l in enumerate(CODE):
    a(text(32, LY(i), l.replace(' ', '&#160;'), size=13, fill='#fff' if i in (1, 2, 3) else PHOS_SOFT, ls='0'))
# resources
BY = 212
for k, (nm, state, dtor) in enumerate(RES):
    x = 20 + k * 124
    a(f'<rect x="{x}" y="{BY}" width="112" height="44" rx="3" fill="{PLATE}" stroke="rgba(198,222,206,0.2)" stroke-dasharray="3 3"/>')
    spans = [(R1[k], R1_UNW[2 - k]), (R2[k], R2_UNW[2 - k])]
    for t0, t1 in spans:
        a(f'<g opacity="0">{win(t0, t1)}<rect x="{x}" y="{BY}" width="112" height="44" rx="3" fill="{GOLD}" fill-opacity="0.2" stroke="{GOLD}"/>'
          f'{text(x + 56, BY + 18, nm, anchor="middle", size=13, fill="#fff", ls="0")}{text(x + 56, BY + 36, state, anchor="middle", size=13, fill=GOLD, ls="0")}</g>')
# status: which destructor is running
STAT = [(R1[-1] + 0.05, R1_UNW[0], 'return 0: leaving scope', PHOS_SOFT), (THROW, R2_UNW[0], 'parse() throws', RED)]
for k in range(3):
    for t0 in (R1_UNW[k], R2_UNW[k]):
        STAT.append((t0, t0 + 0.5, RES[2 - k][2], GOLD))
STAT.append((R1_UNW[-1] + 0.5, R2_0, 'all released, in reverse', PHOS))
STAT.append((R2_UNW[-1] + 0.5, D - 0.2, 'released the same way', PHOS))
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(20, 284, s, size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ("Each resource is held by an object on the stack (<code>buf</code>'s 1024 bytes sit on the heap; the vector on the stack owns them), acquired as its line runs and released by its destructor in reverse order. A normal return and an exception thrown by <code>parse()</code> unwind the same way.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The C version.</b> Every early return or error path must unlock, free and close by hand, usually through a shared <code>goto</code> label; one missed line leaks.</li>
          <li><b>Why reverse.</b> Later resources may depend on earlier ones, so the compiler destroys them in the opposite order to construction.</li>
          <li><b>What builds on it.</b> Containers, smart pointers and lock guards are all RAII types; it is also what makes exceptions safe to use.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-5">
      <div class="diagram-label">Fig 6.5 · RAII: scope acquires, scope releases</div>
      {svg}
      <p id="ch6-raii-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-5', 'ch6-raii-p4', card)
