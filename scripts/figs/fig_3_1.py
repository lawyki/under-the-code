# Fig 3.1 · Same operation, three ISAs (Pass 31, Part I, from an empty script). Job: function. Takeaway: each
# instruction set encodes the same add in its own bits, so a program for one fails on another.
# Concept: each encoding as a 32-bit bar drawn to scale, its fields where its ISA puts them: the opcode (gold), the
# register (blue) and the number 5 (green), the rest grey. The bit strings themselves (unreadable at phone width) give
# way to the layout. Motion lights the three ingredients in turn across all three bars (Part I's light verb), so the
# eye sees the same thing land in three different places. The still has every field coloured.
from figlib import Timeline, text, splice, GOLD, BLUE, GREEN, MUTED

W, H = 400, 372
INK, GREY = '#ece6da', 'rgba(255,255,255,0.55)'
BX, BW = 24, 11                          # bar start, units per bit
T = Timeline(7.5, shift=0.0)
ROLE = {'op': GOLD, 'reg': BLUE, 'num': GREEN, 'x': GREY}
ISAS = [('x86-64', 'add rax, 5', '48 83 C0 05', [(8, 'x', '48'), (8, 'op', '83'), (8, 'reg', 'C0'), (8, 'num', '05')]),
        ('ARM64', 'add x0, x0, 5', '0x91001400', [(9, 'op', ''), (1, 'x', ''), (12, 'num', '5'), (5, 'reg', 'x0'), (5, 'reg', 'x0')]),
        ('RISC-V', 'addi a0, a0, 5', '0x00550513', [(12, 'num', '5'), (5, 'reg', 'a0'), (3, 'x', ''), (5, 'reg', 'a0'), (7, 'op', '')])]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-29 svgd-part1-29">')
a('<title id="svgt-part1-29">Fig 3.1 · Same operation · three ISAs · three encodings</title>')
a('<desc id="svgd-part1-29">"Add 5 to a register" in three instruction sets, each drawn as the 32 bits it uses, with its fields to scale. '
  'x86-64 add rax, 5 is the bytes 48 83 C0 05: a 64-bit prefix, the opcode, a byte naming the register rax, and 5. ARM64 add x0, x0, 5 '
  'is 0x91001400: the opcode first, then a shift bit, then 5, then the two register numbers. RISC-V addi a0, a0, 5 (addi: add a number) '
  'is 0x00550513: 5 first and the opcode last. The same three ingredients sit in different places, so another chip reads each pattern '
  'differently.</desc>')

def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0, 0.0), (t0 + 0.25, 1.0), (t1 - 0.25, 1.0), (t1, 0.0)])
SPANS = {'op': (0.6, 2.4), 'reg': (2.8, 4.6), 'num': (5.0, 6.8)}

# the legend: the three ingredients
LX = [24, 140, 262]
for x, (role, name) in zip(LX, (('op', 'opcode'), ('reg', 'register'), ('num', 'the 5'))):
    a(f'<rect x="{x}" y="18" width="16" height="16" rx="3" fill="{ROLE[role]}"/>')
    a(text(x + 24, 31, name, size=14, fill=ROLE[role]))
    a(f'<rect x="{x - 6}" y="12" width="{len(name) * 8.6 + 40:.0f}" height="28" rx="6" fill="none" stroke="{ROLE[role]}" stroke-width="1.8" opacity="0">{lit(*SPANS[role])}</rect>')

for k, (isa, asm, hexs, fields) in enumerate(ISAS):
    y = 74 + k * 96
    a(text(24, y, isa, size=15, fill=INK))
    a(text(376, y, asm, anchor='end', size=14, fill=MUTED, ls='0'))
    x = BX
    for bits, role, lab in fields:
        w = bits * BW
        col = ROLE[role]
        if role == 'x':
            a(f'<rect x="{x + 1}" y="{y + 10}" width="{w - 2}" height="34" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>')
        else:
            t0, t1 = SPANS[role]
            a(f'<rect x="{x + 1}" y="{y + 10}" width="{w - 2}" height="34" rx="3" fill="none" stroke="{col}" stroke-width="1.8">'
              f'{T.discrete("opacity", [(0.0, 1), (t0, 0), (t1, 1)])}</rect>')
            a(f'<rect x="{x + 1}" y="{y + 10}" width="{w - 2}" height="34" rx="3" fill="none" stroke="{col}" stroke-width="3.2" opacity="0">'
              f'{T.discrete("opacity", [(0.0, 0), (t0, 1), (t1, 0)])}</rect>')
        if lab:
            a(text(x + w / 2, y + 32, lab, anchor='middle', size=14, fill=INK if role == 'x' else col, ls='0', role='object'))
        x += w
    a(text(376, y + 64, hexs, anchor='end', size=14, fill=MUTED, ls='0'))
a(text(24, 362, '32 bits each, three different orders', size=14, fill=INK))
a('</svg>')
svg = '\n'.join(o)

caption = ('"Add 5 to a register" in the three instruction sets that run the world: the same three ingredients, an opcode, a register '
           'and the number 5, packed into 32 bits in three different orders.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>x86-64.</b> Variable length, 1 to 15 bytes. Here a prefix (64-bit), the opcode, a byte naming rax, and the 5 itself, an <em>immediate</em> (a number written into the instruction), in one byte. A number too big for one byte takes four; rax has a shorter form of its own with no register byte, so this add then grows to 6 bytes.</li>
          <li><b>ARM64.</b> Every instruction is exactly 32 bits; this one is opcode, a shift bit, the 12-bit immediate, then source and destination registers.</li>
          <li><b>RISC-V.</b> Also 32 bits, in another order: immediate first, opcode last. The base ISA has only six formats.</li>
          <li><b>The order of the bits.</b> x86 is shown byte by byte as stored; ARM64 and RISC-V as 32-bit words, high bit on the left. Grey fields hold other bits.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-1">
      <div class="diagram-label">Fig 3.1 · Same operation · three ISAs · three encodings</div>
      {svg}
      <p id="ch3-isa-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-1', 'ch3-isa-p3', card)
