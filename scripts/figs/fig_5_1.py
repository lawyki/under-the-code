# Fig 5.1 · One C source, many targets (Pass 28, law 3). One function, three compilers. Each target's
# instructions are drawn with their real encodings as cells whose width is the byte length: x86's
# variable 3 + 1 bytes against the fixed 4-byte words of ARM64 and RISC-V. Cells appear as each target
# is compiled (stepped). t=0 (shift): all three compiled.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

# encodings checked by hand: lea eax,[rdi+rsi] = 8D 04 37 (ModRM 04, SIB 37); ret = C3
# ARM64 add w0,w0,w1 = 0x0B010000, ret = 0xD65F03C0; RV64 addw a0,a0,a1 = 0x00B5053B, ret = 0x00008067
assert (11 << 20 | 10 << 15 | 10 << 7 | 0x3B) == 0x00B5053B
assert (0x0B000000 | 1 << 16) == 0x0B010000
TARGETS = [('x86-64', 'gcc -O2', [('lea eax,[rdi+rsi]', '8D 04 37', 3), ('ret', 'C3', 1)], GOLD),
           ('ARM64', 'gcc -O2', [('add w0,w0,w1', '0B010000', 4), ('ret', 'D65F03C0', 4)], PHOS),
           ('RISC-V · RV64G', 'gcc -O2', [('addw a0,a0,a1', '00B5053B', 4), ('ret', '00008067', 4)], BLUE)]
W = 400
U = 24                     # units per byte
CX0 = 196
D = 8.0
T = Timeline(D, shift=7.4)
def from_t(t):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])
o = []; a = o.append
body = []
b = body.append
b(f'<rect x="20" y="12" width="360" height="52" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
b(text(32, 31, 'main.c', size=13, fill=MUTED, ls='0'))
b(text(32, 52, 'int add(int a, int b) { return a + b; }', size=13, fill='#fff', ls='0'))
y = 84
for k, (arch, cc, ins, col) in enumerate(TARGETS):
    h = 30 + len(ins) * 28 + 6
    b(f'<rect x="20" y="{y}" width="360" height="{h}" rx="3" fill="{PLATE}" stroke="{col}" stroke-opacity="0.6"/>')
    b(text(32, y + 21, arch, size=14, fill=col, ls='0'))
    b(text(368, y + 21, cc, anchor='end', size=13, fill=MUTED, ls='0'))
    t0 = 0.8 + 1.2 * k
    for i, (asm, hexs, n) in enumerate(ins):
        ry = y + 32 + i * 28
        b(text(32, ry + 16, asm, size=13, fill=PHOS_SOFT, ls='0'))
        w = n * U
        b(f'<rect x="{CX0}" y="{ry}" width="{4 * U}" height="22" rx="2" fill="none" stroke="rgba(198,222,206,0.12)" stroke-dasharray="2 3"/>')
        b(f'<g>{from_t(t0 + 0.3 * i)}<rect x="{CX0}" y="{ry}" width="{w}" height="22" rx="2" fill="{col}" fill-opacity="0.22" stroke="{col}"/>'
          f'{text(CX0 + w / 2, ry + 16, hexs, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
        b(f'<g>{from_t(t0 + 0.3 * i)}{text(CX0 + 4 * U + 10, ry + 16, f"{n} B", size=13, fill=MUTED, ls="0")}</g>')
    y += h + 10
H = y
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-25 svgd-part2-25">')
a('<title id="svgt-part2-25">Fig 5.1 · One C source, many targets</title>')
a('<desc id="svgd-part2-25">The C function int add(int a, int b) { return a + b; } compiled for three processors. '
  'x86-64: lea eax,[rdi+rsi] then ret, encoded as the 3 bytes 8D 04 37 and the 1 byte C3. '
  'ARM64: add w0,w0,w1 then ret, two fixed 4-byte words, 0B010000 and D65F03C0. '
  'RISC-V: addw a0,a0,a1 then ret, two 4-byte words, 00B5053B and 00008067. Different instructions, registers and encodings; identical behaviour.</desc>')
o.extend(body)
a('</svg>')
svg = '\n'.join(o)

caption = ('One C function compiled for three processors: different instructions, different registers (<code>eax</code>, <code>w0</code>, <code>a0</code>) and different encodings, x86\'s variable-length bytes against the fixed 4-byte words of ARM and RISC-V. '
           'The behaviour is identical, which is what portable means for C: not one binary everywhere, but one source that compiles to each.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Calling conventions.</b> Each platform's ABI says where arguments arrive (<code>edi</code>/<code>esi</code>, <code>w0</code>/<code>w1</code>, <code>a0</code>/<code>a1</code>) and where the result goes back.</li>
          <li><b>The <code>lea</code> trick.</b> x86 compilers borrow <code>lea</code>, an address-arithmetic instruction, to add two registers into a third in one step.</li>
          <li><b>The <code>w</code> in <code>addw</code>.</b> On 64-bit RISC-V it adds 32-bit <code>int</code>s. With the compressed extension both instructions shrink to 2 bytes each.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-1">
      <div class="diagram-label">Fig 5.1 · One C source, many targets</div>
      {svg}
      <p id="ch5-portability-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-1', 'ch5-portability-p4', card)
