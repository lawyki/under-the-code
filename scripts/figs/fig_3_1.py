# Fig 3.1 · One operation, three ISAs (Pass 28, law 3). "Add 5 to a register" as real encodings:
# x86-64 add rax, 5 = 48 83 C0 05 (what an assembler emits); ARM64 add x0, x0, #5 = 0x91001400;
# RISC-V addi a0, a0, 5 = 0x00550513. Bits drawn, fields coloured by role; a highlight walks the
# roles so the 5, the register and the opcode can be seen landing in different places.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, MUTED

W, H = 400, 376
GRAY = '#9a9a9a'
ROLE = {'op': (GOLD, 'opcode'), 'reg': (BLUE, 'register'), 'imm': (GREEN, 'the 5'), 'misc': (GRAY, 'other')}
# (name, asm, hex shown, [(bits, role, label)]) ; x86 in byte order, the others as 32-bit words, high bit left
ROWS = [
    ('x86-64', 'add rax, 5', '48 83 C0 05',
     [('01001000', 'misc', 'prefix'), ('10000011', 'op', 'opcode'), ('11000000', 'reg', 'rax'), ('00000101', 'imm', '5')]),
    ('ARM64', 'add x0, x0, #5', '0x91001400',
     [('100100010', 'op', 'opcode'), ('0', 'misc', ''), ('000000000101', 'imm', '5'), ('00000', 'reg', 'x0'), ('00000', 'reg', 'x0')]),
    ('RISC-V', 'addi a0, a0, 5', '0x00550513',
     [('000000000101', 'imm', '5'), ('01010', 'reg', 'a0'), ('000', 'misc', ''), ('01010', 'reg', 'a0'), ('0010011', 'op', 'opcode')]),
]
assert int(''.join(b for b, _, _ in ROWS[1][3]), 2) == 0x91001400
assert int(''.join(b for b, _, _ in ROWS[2][3]), 2) == 0x00550513
assert ' '.join(f'{int(b, 2):02X}' for b, _, _ in ROWS[0][3]) == '48 83 C0 05'
PITCH, X0 = 11, 24
T = Timeline(9, shift=0.0)
ORDER = ['imm', 'reg', 'op']
def role_hi(role):
    k = ORDER.index(role); t0, t1 = 0.5 + k * 2.8, 0.5 + k * 2.8 + 2.4
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.999, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-29 svgd-part1-29">')
a('<title id="svgt-part1-29">Fig 3.1 · Same operation · three ISAs · three encodings</title>')
a('<desc id="svgd-part1-29">"Add 5 to a register" in three instruction sets, as the 32 bits each one uses. x86-64 add rax, 5 is the bytes 48 83 C0 05: a prefix, the opcode, a byte naming rax, and 5. '
  'ARM64 add x0, x0, #5 is 0x91001400: the opcode first, then 5, then the two register numbers. RISC-V addi a0, a0, 5 is 0x00550513: 5 first and the opcode last. '
  'The same three ingredients sit in different places, so each pattern means nothing to the other two chips.</desc>')
for r, (name, asm, hx, fields) in enumerate(ROWS):
    y = 20 + r * 112
    a(text(20, y + 14, name, size=15, fill='#fff', ls='0'))
    a(text(380, y + 14, asm, anchor='end', size=14, fill='rgba(255,255,255,0.8)', ls='0'))
    x = X0
    for bits, role, lab in fields:
        col = ROLE[role][0]
        w = len(bits) * PITCH
        a(f'<rect x="{x}" y="{y + 26}" width="{w - 2}" height="30" rx="3" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-opacity="0.75"/>')
        if role in ORDER:
            a(f'<rect class="fx" x="{x - 2}" y="{y + 24}" width="{w + 2}" height="34" rx="4" fill="{col}" fill-opacity="0.35" stroke="#fff" stroke-width="2" opacity="0">{role_hi(role)}</rect>')
        for k, b in enumerate(bits):
            a(f'<text x="{x + k * PITCH + PITCH / 2 - 1}" y="{y + 46}" text-anchor="middle" {MONO} font-size="13" fill="#fff">{b}</text>')
        if lab and w >= 40:
            a(text(x + w / 2 - 1, y + 76, lab, anchor='middle', size=13, fill=col, ls='0'))
        x += w
    a(text(380, y + 98, hx, anchor='end', size=13, fill=MUTED, ls='0'))
# legend
for k, role in enumerate(['op', 'reg', 'imm']):
    col, lab = ROLE[role]
    a(f'<rect x="{20 + k * 120}" y="{H - 22}" width="14" height="14" rx="2" fill="{col}" fill-opacity="0.5" stroke="{col}"/>')
    a(text(40 + k * 120, H - 10, lab, size=13, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('"Add 5 to a register" in the three instruction sets that run the world: the same three ingredients, an opcode, a register and the number 5, packed into 32 bits in three different orders. '
           'Each pattern is meaningless to the other two chips.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>x86-64.</b> Variable length, 1 to 15 bytes. Here a prefix (64-bit), the opcode, a byte naming rax, and the 5 in one byte. With a 32-bit immediate it would be 7 bytes.</li>
          <li><b>ARM64.</b> Every instruction is exactly 32 bits; this one is opcode, a shift bit, the 12-bit immediate, then source and destination registers.</li>
          <li><b>RISC-V.</b> Also 32 bits, in another order: immediate first, opcode last. The base ISA has only six formats.</li>
          <li><b>The order of the bits.</b> x86 is shown byte by byte as stored; ARM64 and RISC-V as 32-bit words, high bit on the left.</li>
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
