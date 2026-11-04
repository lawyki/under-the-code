# Fig 3.3 · The x86-64 register file (Pass 31, Part I, from an empty script). Job: function. Takeaway: each widening
# kept the older, smaller register inside the new one, so a 64-bit register holds its 32-bit half.
# Concept: RAX as eight byte cells with its names nested over it, each with its year (RAX 2003 over all eight, EAX 1985
# over the low four, AX 1978 over the low two, split into AH and AL). Below, two writes, each a row that lands in turn
# (Part I's step verb): mov al, 0xFF changes one byte; mov eax, 1 writes the low half and clears the upper half. The
# old panel of all sixteen names is the prose's table and is gone. t=0 shows both writes done.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, MUTED

W, H = 400, 330
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
X0, CW = 40, 40
CX = lambda i: X0 + i * CW + (CW - 4) / 2
D = 8.0
T = Timeline(D, shift=6.5)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-31 svgd-part1-31"{T.steps([(0.8, 'start'), (3.0, 'mov al'), (6.0, 'mov eax')])}>')
a('<title id="svgt-part1-31">Fig 3.3 · The x86-64 register file · one register, five names</title>')
a('<desc id="svgd-part1-31">RAX holds eight bytes. Its lower four bytes are also called EAX (1985), the lower two AX (1978), and those two '
  'bytes AH and AL; RAX itself dates from 2003. Starting from 11 22 33 44 55 66 77 88, mov al, 0xFF changes only the lowest byte '
  '(only AL changes). mov eax, 1 writes the lower half and clears the upper half too: 00 00 00 00 00 00 00 01.</desc>')

def bracket(i0, i1, y, label, col):
    x0, x1 = X0 + i0 * CW, X0 + i1 * CW + CW - 4
    a(f'<path d="M {x0} {y + 6} v -6 H {x1} v 6" fill="none" stroke="{col}" stroke-width="1.5"/>')
    a(text((x0 + x1) / 2, y - 6, label, anchor='middle', size=14, fill=col, ls='0'))
bracket(0, 7, 38, 'RAX · 2003', INK)
bracket(4, 7, 62, 'EAX · 1985', BLUE)
bracket(6, 7, 86, 'AX · 1978', GOLD)
a(text(CX(6), 104, 'AH', anchor='middle', size=14, fill=GOLD, ls='0')); a(text(CX(7), 104, 'AL', anchor='middle', size=14, fill=GOLD, ls='0'))

def row(y, vals, marks, t0):
    g = []
    for i, v in enumerate(vals):
        col = marks.get(i)
        g.append(f'<rect x="{X0 + i * CW}" y="{y}" width="{CW - 4}" height="34" rx="4" fill="none" stroke="{col or EDGE}" stroke-width="{2.2 if col else 1.4}"/>')
        g.append(text(CX(i), y + 22, v, anchor='middle', size=15, fill=col or INK, ls='0', role='object'))
    a(f'<g opacity="0">{vis([(t0, D)])}{"".join(g)}</g>' if t0 else ''.join(g))
row(112, ['11', '22', '33', '44', '55', '66', '77', '88'], {}, None)
a(f'<g opacity="0">{vis([(1.4, D)])}' + text(X0, 176, 'mov al, 0xFF', size=14, fill=GOLD, ls='0') + '</g>')
row(184, ['11', '22', '33', '44', '55', '66', '77', 'FF'], {7: GOLD}, 1.6)
a(f'<g opacity="0">{vis([(3.6, D)])}' + text(X0, 246, 'mov eax, 1', size=14, fill=RED, ls='0') + '</g>')
row(254, ['00', '00', '00', '00', '00', '00', '00', '01'], {0: RED, 1: RED, 2: RED, 3: RED, 4: GOLD, 5: GOLD, 6: GOLD, 7: GOLD}, 3.8)
a('</svg>')
svg = '\n'.join(o)

caption = 'One register, five names; a 32-bit write clears the upper half.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The names.</b> The 8086 had 16-bit AX, BX, CX, DX; 32-bit chips added an E for extended; AMD64, the 64-bit x86 that AMD shipped in 2003, replaced it with R and added R8 to R15, sixteen registers in all.</li>
          <li><b>The quirk.</b> 8- and 16-bit writes leave the rest of the register alone; 32-bit writes zero the top 32 bits.</li>
          <li><b>Two more.</b> RIP, the instruction pointer, and RFLAGS, the condition codes set by most arithmetic operations, are not general-purpose.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-3">
      <div class="diagram-label">Fig 3.3 · The x86-64 register file · one register, five names</div>
      {svg}
      <p id="ch3-registers-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-3', 'ch3-registers-p3', card)
