"""Fig 1.9: the instruction cycle on one instruction. Simplified 2026-11-13 (owner: "simplify most of them ... you don't
need to repeat in text what the figure is already saying"). The hex bytes, their dividers, the decoded-form line, the
program-counter box and two labels are gone. Memory is a short program in plain words, each line at its address;
a gold pointer marks the line being run. fetch: the line is copied into the CPU; decode: the adder and the two
registers light; execute: 5 and 3 go into the adder, 8 comes out; writeback: 8 lands in eax, the pointer moves on."""
from plate import *
D = 8.0
k = lambda t: t / D
b = []
# memory: a program, one line an address
ROWS = [('0x00', 'put 5 in eax'), ('0x05', 'put 3 in ebx'), ('0x0A', 'add ebx to eax'), ('0x0C', '')]
RY = lambda i: 40 + i * 22
b.append(text(288, 29, 'memory', 13, MUTE, 'end'))
b.append(f'<rect x="12" y="{RY(0)-4}" width="276" height="{22*4+6}" rx="6" fill="none" stroke="{INK}" stroke-opacity="0.6" stroke-width="1.5"/>')
for i, (addr, ins) in enumerate(ROWS):
    b.append(text(40, RY(i) + 13, addr, 11.5, MUTE, 'start'))
    if ins: b.append(text(86, RY(i) + 13, ins, 13, INK, 'start'))
# the pointer: the line being run; it moves on at writeback
ptr = f'<path d="M 20 {RY(2)+3} l 11 6 l -11 6 Z" fill="{GOLD}"/>'
b.append(f'<g>{xform("translate", ["0 0", "0 0", "0 22", "0 22", "0 0"], [0, k(6.9), k(7.3), 0.999, 1], D)}{ptr}</g>')
# the CPU
CY = 140
b.append(f'<rect x="12" y="{CY}" width="276" height="150" rx="10" fill="none" stroke="{INK}" stroke-opacity="0.75" stroke-width="1.6"/>')
b.append(text(276, CY + 20, 'CPU', 13, MUTE, 'end'))
# fetch: the line is copied down into the CPU
CW = 126
chip = f'<rect x="80" y="{RY(2)-1}" width="{CW}" height="20" rx="4" fill="{GOLD}"/>' + text(86, RY(2) + 13, 'add ebx to eax', 13, '#1a1408', 'start')
dx, dy = 30 - 80, CY + 12 - (RY(2) - 1)
b.append(show(f'<g>{xform("translate", ["0 0", "0 0", f"{dx} {dy}", f"{dx} {dy}", "0 0"], [0, k(0.25), k(1.05), 0.999, 1], D)}{chip}</g>', [(0.3, D)], D))
# registers
RX, RW, RH = 30, 86, 28; R1, R2 = CY + 52, CY + 90
for name, y in (('eax', R1), ('ebx', R2)):
    b.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    b.append(text(RX + 10, y + 19, name, 13, MUTE, 'start'))
b.append(show(''.join(f'<rect x="{RX-3}" y="{y-3}" width="{RW+6}" height="{RH+6}" rx="7" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-opacity="0.7"/>' for y in (R1, R2)), [(2.2, 6.0)], D))
b.append(show(text(RX + RW - 12, R1 + 19.5, '5', 15, BLUE, 'end'), [(0, 6.9)], D))
b.append(show(text(RX + RW - 12, R1 + 19.5, '8', 15, GOLD, 'end'), [(6.9, D)], D))
b.append(text(RX + RW - 12, R2 + 19.5, '3', 15, BLUE, 'end'))
# wires and the adder
A1, A2, AM = R1 + 14, R2 + 14, (R1 + R2) / 2 + 14
WB = R2 + RH + 12
b.append(line(f'M {RX+RW} {A1} H 186', INK, 1.2, ' stroke-opacity="0.5"'))
b.append(line(f'M {RX+RW} {A2} H 186', INK, 1.2, ' stroke-opacity="0.5"'))
b.append(line(f'M 240 {AM} H 264 V {WB} H 20 V {A1} H 30', INK, 1.2, ' stroke-opacity="0.5"'))
alu = f'M 186 {A1-12} V {AM-10} L 197 {AM} L 186 {AM+10} V {A2+12} L 240 {AM+16} V {AM-16} Z'
b.append(f'<path d="{alu}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
b.append(show(f'<path d="{alu}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linejoin="round"/>', [(2.2, 6.9)], D))
b.append(show(text(219, AM + 6, '+', 18, GOLD), [(2.2, 4.9)], D))
b.append(show(text(219, AM + 6, '8', 16, GOLD), [(4.9, 6.1)], D))
def token(val, col, x0, y0, x1, y1, t0, t1, path=None):
    pill = f'<rect x="-11" y="-11" width="22" height="22" rx="6" fill="{col}"/>' + text(0, 5, val, 14, '#10131c')
    if path:
        g = f'<g><animateMotion path="{path}" keyPoints="0;0;1;1" keyTimes="0;{k(t0):.4f};{k(t1):.4f};1" calcMode="linear" dur="{D}s" repeatCount="indefinite"/>{pill}</g>'
    else:
        g = f'<g>{xform("translate", [f"{x0} {y0}", f"{x0} {y0}", f"{x1} {y1}", f"{x1} {y1}"], [0, k(t0), k(t1), 1], D)}{pill}</g>'
    return show(g, [(t0, t1)], D)
b.append(token('5', BLUE, RX + RW - 16, A1, 176, A1, 4.1, 4.9))
b.append(token('3', BLUE, RX + RW - 16, A2, 176, A2, 4.1, 4.9))
b.append(token('8', GOLD, 0, 0, 0, 0, 6.1, 6.9, path=f'M 240 {AM} H 264 V {WB} H 20 V {A1} H 40'))
put('fig-1-9', '4 10 292 286', [1.5, 3.2, 5.5, 7.6], ['fetch', 'decode', 'execute', 'writeback'],
    'Fig 1.9 · The instruction cycle',
    'Memory holds a short program, one instruction to a line, each at its address in hexadecimal: at 0x00, put 5 in eax; at 0x05, put 3 in ebx; at 0x0A, add ebx to eax; 0x0C is still empty. A gold pointer, the program counter, marks the line at 0x0A. Below is the CPU, with two registers, eax holding 5 and ebx holding 3, and an adder. Fetch: the line at 0x0A is copied from memory into the CPU. Decode: the adder is set to add and the two registers are picked. Execute: 5 and 3 travel into the adder, which shows 8. Writeback: the 8 travels back into eax, and the pointer moves down to 0x0C.',
    b,
    caption='The gold pointer is the program counter.',
    strip=[('Fetch', 'Copy the instruction at the address in the program counter into the CPU.'),
           ('Decode', 'Work out the operation and what it acts on. In memory the instruction is a bit pattern, not words: Fig 1.10 takes one apart.'),
           ('Execute', 'The ALU (arithmetic logic unit) or another unit does the work: here it adds 5 and 3.'),
           ('Writeback', 'Store the result, here 8 into eax, and move the counter on by the instruction\'s length; a jump would set the counter instead.'),
           ('The addresses', 'Every byte has a number. 0x marks hexadecimal: 0x0A is ten, 0x0C twelve. The first two instructions take five bytes each, so the third starts at ten, and it takes two.')])
