# Fig 1.10 · From assembly to binary (Pass 31, Part I, from an empty script). Job: function. Takeaway: the
# assembler swaps each written name for its fixed number code, one for one, the form the processor runs.
# Concept: Fig 1.9's own three-line loop, written on the left and assembled on the right, one line at a time
# (Part I's step verb), the operation in gold and its operand in blue on both sides, so the one-for-one swap is
# seen by colour. Below, the first byte opened: B8 is five bits that say "move a value into a register" and three
# that name EAX. t=0 is the finished translation.
from figlib import Timeline, text, splice, GOLD, BLUE, MUTED

W, H = 400, 340
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
T = Timeline(9, shift=8.0)
ROWS = [('mov eax,', ' 5', ['B8'], ['05', '00', '00', '00']),
        ('add eax,', ' 3', ['83', 'C0'], ['03']),
        ('jmp', ' 0x00', ['EB'], ['F6'])]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-11 svgd-part1-11"{T.steps([(2.2, 'mov'), (3.8, 'add'), (6.6, 'jmp')])}>')
a('<title id="svgt-part1-11">Fig 1.10 · From assembly to binary · one instruction decoded</title>')
a('<desc id="svgd-part1-11">The three-line loop of Fig 1.9, written on the left and assembled on the right, one line at a time: mov eax, 5 '
  'becomes B8 05 00 00 00; add eax, 3 becomes 83 C0 03; jmp 0x00 becomes EB F6. Each operation name becomes its fixed code and each '
  'operand its number, one for one. Below, the first byte opened: B8 is 10111 000 in binary; the top five bits mean move a value '
  'into a register, the bottom three name the register, 000 for EAX. The value 5 is stored lowest byte first, as 05 00 00 00.</desc>')

for k, (op, arg, obytes, abytes) in enumerate(ROWS):
    y = 46 + k * 46
    t0 = 1.0 + k * 1.6
    a(f'<rect x="16" y="{y}" width="118" height="34" rx="5" fill="none" stroke="{EDGE}"/>')
    a(f'<text x="26" y="{y + 22}" font-family="DM Mono" font-size="15" letter-spacing="0">'
      f'<tspan fill="{GOLD}">{op}</tspan><tspan fill="{BLUE}">{arg}</tspan></text>')
    # the assembler's arrow
    a(f'<path d="M 142 {y + 17} H 180 M 174 {y + 11} L 180 {y + 17} L 174 {y + 23}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    # the bytes, landing one line at a time
    cells = [(b, GOLD) for b in obytes] + [(b, BLUE) for b in abytes]
    show = T.anim('opacity', [(0.0, 0.0), (t0 - 0.01, 0.0), (t0 + 0.3, 1.0), (8.8, 1.0), (8.99, 0.0)])
    g = []
    for j, (b, col) in enumerate(cells):
        x = 192 + j * 38
        g.append(f'<rect x="{x}" y="{y}" width="34" height="34" rx="4" fill="none" stroke="{col}" stroke-width="1.5"/>')
        g.append(text(x + 17, y + 22, b, anchor='middle', size=14, fill=col, ls='0', role='object'))
    a(f'<g opacity="0">{show}{"".join(g)}</g>')
    # the line being assembled gets the gold frame
    a(f'<rect x="12" y="{y - 4}" width="126" height="42" rx="7" fill="none" stroke="{GOLD}" stroke-width="2.2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.4, 0.0), (t0 - 0.3, 1.0), (t0 + 1.2, 1.0), (t0 + 1.3, 0.0)])}</rect>')

# ---------- B8, opened ----------
a(text(20, 224, 'B8', size=14, fill=GOLD))
BITS = '10111000'
for j, b in enumerate(BITS):
    x = 58 + j * 36
    col = GOLD if j < 5 else BLUE
    a(f'<rect x="{x}" y="238" width="32" height="34" rx="4" fill="none" stroke="{col}" stroke-width="1.5"/>')
    a(text(x + 16, 261, b, anchor='middle', size=16, fill=col, ls='0', role='object'))
a(f'<path d="M 58 282 v 6 H {58 + 5 * 36 - 4} v -6" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
a(text(58 + (5 * 36 - 4) / 2, 308, 'operation', anchor='middle', size=14, fill=GOLD))
a(f'<path d="M {58 + 5 * 36} 282 v 6 H {58 + 8 * 36 - 4} v -6" fill="none" stroke="{BLUE}" stroke-width="1.4"/>')
a(text(58 + 5 * 36 + (3 * 36 - 4) / 2, 308, 'EAX', anchor='middle', size=14, fill=BLUE))
a('</svg>')
svg = '\n'.join(o)

caption = "Each name becomes its code, one for one; B8's bits name the operation and the register."
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Opcode.</b> B8 is 10111 000. The top five bits mean “move a 32-bit value into a register”; the bottom three name the register, and 000 is EAX.</li>
          <li><b>Value.</b> x86 is little-endian: it stores the lowest byte first, so 5 sits in memory as 05&nbsp;00&nbsp;00&nbsp;00.</li>
          <li><b>The jump.</b> F6 is not an address but a distance: minus ten bytes, counted from the end of the jump, which lands back on 0x00.</li>
          <li><b>Decode.</b> The decoder is a circuit that recognises these bit patterns and routes them to the right units; nothing is looked up by name.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-10">
      <div class="diagram-label">Fig 1.10 · From assembly to binary · one instruction decoded</div>
      {svg}
      <p id="ch1-cpu-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-10', 'ch1-cpu-p6', card)
