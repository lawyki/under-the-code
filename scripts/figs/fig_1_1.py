# Fig 1.1 · A Turing machine (Pass 28, law 3). A real program, not placeholder states:
# "add one" on binary 1011. State carry: read 1 -> write 0, move left; read 0 or blank
# -> write 1, halt. 1011 (11) becomes 1100 (12). t=0 is the finished run.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 422
TAPE0 = ['_', '1', '0', '1', '1', '_', '_']
CX = lambda i: 40 + i * 46 + 22               # cell centres
TY = 116                                       # tape top
T = Timeline(9, shift=7.0)
# the run: (tau of the read, cell, writes, moves to, rule row)
STEPS = [(0.8, 4, '0', 3, 0), (2.6, 3, '0', 2, 0), (4.4, 2, '1', None, 1)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-2 svgd-part1-2">')
a('<title id="svgt-part1-2">Fig 1.1 · A Turing machine · adding one</title>')
a('<desc id="svgd-part1-2">A tape holds the binary number 1011. The head starts on the last digit in state carry. '
  'Reading 1 it writes 0 and moves left, twice; reading 0 it writes 1 and halts. The tape now reads 1100: 11 plus one is 12. '
  'Below, the whole program: two rules, the one in use highlighted.</desc>')

# the tape
a(f'<text x="18" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.35)">…</text>')
a(f'<text x="382" y="{TY + 31}" text-anchor="middle" {MONO} font-size="16" fill="rgba(255,255,255,0.35)">…</text>')
for i, ch in enumerate(TAPE0):
    x = 40 + i * 46
    a(f'<rect x="{x}" y="{TY}" width="44" height="48" rx="3" fill="#1c1c1c" stroke="rgba(255,255,255,0.18)"/>')
    step = next((s for s in STEPS if s[1] == i), None)
    if step:
        t_w = step[0] + 0.6
        a(f'<text x="{CX(i)}" y="{TY + 32}" text-anchor="middle" {MONO} font-size="22" fill="rgba(255,255,255,0.75)">{ch}'
          f'{T.anim("opacity", [(0.0, 1.0), (t_w - 0.05, 1.0), (t_w, 0.0), (8.5, 0.0), (8.7, 1.0)])}</text>')
        a(f'<text x="{CX(i)}" y="{TY + 32}" text-anchor="middle" {MONO} font-size="22" font-weight="500" fill="{GOLD}">{step[2]}'
          f'{T.anim("opacity", [(0.0, 0.0), (t_w - 0.05, 0.0), (t_w, 1.0), (8.5, 1.0), (8.7, 0.0)])}</text>')
    else:
        a(f'<text x="{CX(i)}" y="{TY + 32}" text-anchor="middle" {MONO} font-size="22" fill="rgba(255,255,255,{0.35 if ch == "_" else 0.75})">{ch}</text>')

# the head: a box with its state, and a pointer to the cell under it
hx = [(0.0, CX(4)), (1.6, CX(4)), (2.2, CX(3)), (3.4, CX(3)), (4.0, CX(2)), (8.5, CX(2)), (8.8, CX(4)), (9.0, CX(4))]
# build the head motion with explicit keyframes in SMIL time (sorted, with 0 and 1 endpoints)
pts = sorted((T.t(t), v - CX(4)) for t, v in hx)
def head_at(t):
    seq = [(pts[-1][0] - 9, pts[-1][1])] + pts + [(pts[0][0] + 9, pts[0][1])]
    for p, q in zip(seq, seq[1:]):
        if p[0] <= t <= q[0]:
            return p[1] if q[0] == p[0] else p[1] + (t - p[0]) / (q[0] - p[0]) * (q[1] - p[1])
ts = sorted(set([0.0, 9.0] + [p[0] for p in pts]))
a(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"{head_at(t):.2f} 0" for t in ts)}" '
  f'keyTimes="{";".join(f"{t / 9:.4f}" for t in ts)}" dur="9s" repeatCount="indefinite"/>')
a(f'<rect x="{CX(4) - 34}" y="56" width="68" height="40" rx="6" fill="#1a1200" stroke="{GOLD}" stroke-width="1.5"/>')
a(f'<text x="{CX(4)}" y="81" text-anchor="middle" {MONO} font-size="15" fill="{GOLD}">carry'
  f'{T.anim("opacity", [(0.0, 1.0), (5.3, 1.0), (5.4, 0.0), (8.6, 0.0), (8.7, 1.0)])}</text>')
a(f'<text x="{CX(4)}" y="81" text-anchor="middle" {MONO} font-size="15" fill="#fff">halt'
  f'{T.anim("opacity", [(0.0, 0.0), (5.3, 0.0), (5.4, 1.0), (8.6, 1.0), (8.7, 0.0)])}</text>')
a(f'<polygon points="{CX(4) - 7},98 {CX(4) + 7},98 {CX(4)},108" fill="{GOLD}"/>')
a('</g>')
a(text(20, 40, 'HEAD · ITS STATE', fill=MUTED))

# what the tape means, before and after
a(text(20, 200, 'before', fill=MUTED))
a(text(20, 222, '1011 = 11', size=17, fill='rgba(255,255,255,0.8)'))
a(text(210, 200, 'after', fill=MUTED))
a(f'<text x="210" y="222" {MONO} font-size="17" fill="{GOLD}">1100 = 12{T.anim("opacity", [(0.0, 0.25), (5.0, 0.25), (5.3, 1.0), (8.5, 1.0), (8.7, 0.25)])}</text>')

# the program: two rules (three lines), the one firing highlighted
a(text(20, 262, 'THE WHOLE PROGRAM', fill=MUTED))
cols = [('STATE', 20), ('READ', 108), ('WRITE', 166), ('MOVE', 238), ('NEXT', 310)]
for name, x in cols: a(text(x, 290, name, size=13, fill='rgba(255,255,255,0.45)'))
RULES = [('carry', '1', '0', '←', 'carry'), ('carry', '0', '1', 'none', 'halt'), ('carry', '_', '1', 'none', 'halt')]
for r, row in enumerate(RULES):
    y = 300 + r * 32
    a(f'<rect x="14" y="{y}" width="372" height="28" rx="4" fill="#161616"/>')
    fires = [s for s in STEPS if s[4] == r]
    if fires:
        pts_ = [(0.0, 0.0)]
        for s in fires: pts_ += [(s[0] - 0.1, 0.0), (s[0], 1.0), (s[0] + 1.2, 1.0), (s[0] + 1.4, 0.0)]
        pts_ += [(9.0, 0.0)]
        a(f'<rect x="14" y="{y}" width="372" height="28" rx="4" fill="rgba(212,168,83,0.16)" stroke="{GOLD}" stroke-width="1.5" opacity="0">{T.anim("opacity", pts_)}</rect>')
    for (name, x), v in zip(cols, row):
        a(text(x, y + 19, v, size=15, fill='rgba(255,255,255,0.88)' if name != 'STATE' else 'rgba(212,168,83,0.9)'))
a(text(20, 414, '_ is a blank cell', size=13, fill='rgba(255,255,255,0.45)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('The machine adds one to binary 1011: at each step the head reads a cell, finds the rule for its state and that symbol, '
           'writes, moves, and changes state. Anything that can be computed can be computed by a machine like this.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tape.</b> An endless row of cells, one symbol in each; the head sees one cell at a time.</li>
          <li><b>Rule.</b> For the current state and the symbol under the head, a rule says what to write, where to move and which state comes next.</li>
          <li><b>This program.</b> A 1 plus a carry is 0 with the carry passed left; the first 0 or blank takes the carry as a 1, and the machine halts.</li>
          <li><b>Universal.</b> A machine whose rules read another machine's rules from its tape can run any of them: the universal machine of the text.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-1">
      <div class="diagram-label">Fig 1.1 · A Turing machine · adding one</div>
      {svg}
      <p id="ch1-context-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-1', 'ch1-context-p6', card)
