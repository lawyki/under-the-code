"""Fig 1.9: the instruction cycle, shown on one real instruction (add eax, ebx = bytes 01 D8 at address 0x0A).
fetch: the program counter holds 0x0A, and the bytes there are copied into the CPU; decode: they become an
operation and two registers; execute: the ALU adds 5 and 3; writeback: 8 goes into eax and the counter moves on.
Round five: the program counter is a named box holding the address, the two earlier instructions say what they
did, and the registers and the ALU carry their names."""
from plate import *
D = 8.0
k = lambda t: t / D
BW = 18; MX, MY, MH = 20, 44, 24
b = []
# memory: fourteen bytes, three instructions
bytes_ = ['B8', '05', '00', '00', '00', 'BB', '03', '00', '00', '00', '01', 'D8', '', '']
for i, v in enumerate(bytes_):
    if i in (1, 2, 3, 4, 6, 7, 8, 9, 11): b.append(line(f'M {MX+i*BW} {MY+3} V {MY+MH-3}', INK, 1, ' stroke-opacity="0.45"'))
    if v: b.append(text(MX + i*BW + BW/2, MY + 16.5, v, 11.5, MUTE))
for start, n in ((0, 5), (5, 5), (10, 2), (12, 2)):
    b.append(f'<rect x="{MX+start*BW}" y="{MY}" width="{n*BW}" height="{MH}" rx="3" fill="none" stroke="{INK}" stroke-width="1.6"{' stroke-opacity="0.45"' if start == 12 else ''}/>')
# what the two earlier instructions did, in plain words
b.append(text(MX + 2.5*BW, MY - 9, 'put 5 in eax', 11.5, MUTE) + text(MX + 7.5*BW, MY - 9, 'put 3 in ebx', 11.5, MUTE))
# addresses under the first byte of each instruction
for start, a in ((0, '0x00'), (5, '0x05'), (10, '0x0A'), (12, '0x0C')):
    b.append(text(MX + start*BW + 1, MY + MH + 14, a, 11.5, MUTE, 'start'))
b.append(text(MX + 14*BW, MY - 9, 'memory', 13, MUTE, 'end'))
b.append(show(f'<rect x="{MX+10*BW}" y="{MY}" width="{2*BW}" height="{MH}" rx="3" fill="none" stroke="{GOLD}" stroke-width="2"/>', [(0, 2.0)], D))
# the CPU
CY = 116
b.append(f'<rect x="12" y="{CY}" width="276" height="210" rx="10" fill="none" stroke="{INK}" stroke-opacity="0.75" stroke-width="1.6"/>')
b.append(text(276, CY + 201, 'CPU', 13, MUTE, 'end'))
# program counter: a box in the CPU holding an address, and a pointer from it to that address in memory
PX0 = MX + 10*BW + 14; PBX, PBY, PBW, PBH = 190, CY + 10, 84, 24
b.append(text(PBX - 8, PBY + 17, 'program counter', 13, GOLD, 'end'))
b.append(f'<rect x="{PBX}" y="{PBY}" width="{PBW}" height="{PBH}" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.8"/>')
b.append(show(text(PBX + PBW/2, PBY + 17, '0x0A', 13, GOLD), [(0, 7.1)], D))
b.append(show(text(PBX + PBW/2, PBY + 17, '0x0C', 13, GOLD), [(7.1, D)], D))
ptr = line(f'M {PX0} {PBY} V {MY+MH+31}', GOLD, 1.8) + f'<path d="M {PX0} {MY+MH+19} l -6.5 11 h 13 Z" fill="{GOLD}"/>'
b.append(f'<g>{xform("translate", ["0 0", "0 0", "36 0", "36 0", "0 0"], [0, k(6.9), k(7.3), 0.999, 1], D)}{ptr}</g>')
# instruction slot
SX, SY = 30, CY + 44
b.append(f'<rect x="{SX}" y="{SY}" width="{2*BW+8}" height="{MH+4}" rx="4" fill="none" stroke="{INK}" stroke-opacity="0.6" stroke-width="1.4" stroke-dasharray="3 3"/>')
# fetch: the two bytes are copied down into the slot
chip = (f'<rect x="{MX+10*BW}" y="{MY}" width="{2*BW}" height="{MH}" rx="3" fill="{GOLD}"/>'
        + text(MX + 10*BW + 9, MY + 16.5, '01', 11.5, '#1a1408') + text(MX + 11*BW + 9, MY + 16.5, 'D8', 11.5, '#1a1408'))
dx, dy = SX + 4 - (MX + 10*BW), SY + 2 - MY
b.append(show(f'<g>{xform("translate", ["0 0", "0 0", f"{dx} {dy}", f"{dx} {dy}", "0 0"], [0, k(0.25), k(1.05), 0.999, 1], D)}{chip}</g>', [(0.52, D)], D))
# decode: the bytes read as an operation and two registers
dec = (line(f'M {SX+2*BW+14} {SY+14} h 16 m -5 -4.5 l 5 4.5 l -5 4.5', MUTE, 1.6)
       + text(SX + 2*BW + 40, SY + 19, 'add', 14, GOLD, 'start') + text(SX + 2*BW + 72, SY + 19, 'eax, ebx', 14, BLUE, 'start'))
b.append(show(dec, [(2.2, D)], D))
# registers
RX, RW, RH = 30, 86, 28; R1, R2 = CY + 104, CY + 142
b.append(text(RX, R1 - 9, 'registers', 13, MUTE, 'start'))
for name, y in (('eax', R1), ('ebx', R2)):
    b.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    b.append(text(RX + 10, y + 19, name, 13, MUTE, 'start'))
b.append(show(''.join(f'<rect x="{RX-3}" y="{y-3}" width="{RW+6}" height="{RH+6}" rx="7" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-opacity="0.7"/>' for y in (R1, R2)), [(2.2, 6.0)], D))
b.append(show(text(RX + RW - 12, R1 + 19.5, '5', 15, BLUE, 'end'), [(0, 6.9)], D))
b.append(show(text(RX + RW - 12, R1 + 19.5, '8', 15, GOLD, 'end'), [(6.9, D)], D))
b.append(text(RX + RW - 12, R2 + 19.5, '3', 15, BLUE, 'end'))
# wires and ALU
A1, A2, AM = R1 + 14, R2 + 14, (R1 + R2) / 2 + 14          # the two inputs and the output height
WB = R2 + RH + 14                                         # the way back runs under the registers
b.append(line(f'M {RX+RW} {A1} H 186', INK, 1.2, ' stroke-opacity="0.5"'))
b.append(line(f'M {RX+RW} {A2} H 186', INK, 1.2, ' stroke-opacity="0.5"'))
back = f'M 240 {AM} H 264 V {WB} H 20 V {A1} H 30'
b.append(line(back, INK, 1.2, ' stroke-opacity="0.5"'))
alu = f'M 186 {A1-12} V {AM-10} L 197 {AM} L 186 {AM+10} V {A2+12} L 240 {AM+16} V {AM-16} Z'
b.append(f'<path d="{alu}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
b.append(text(213, R1 - 9, 'ALU', 13, MUTE))
b.append(show(f'<path d="{alu}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linejoin="round"/>', [(2.2, 6.9)], D))
b.append(show(text(219, AM + 6, '+', 17, GOLD), [(2.2, 4.9)], D))
b.append(show(text(219, AM + 6, '8', 16, GOLD), [(4.9, 6.1)], D))
# execute: 5 and 3 travel into the ALU
def token(val, col, x0, y0, x1, y1, t0, t1, path=None):
    pill = f'<rect x="-11" y="-11" width="22" height="22" rx="6" fill="{col}"/>' + text(0, 5, val, 14, '#10131c')
    if path:
        mv = (f'<animateMotion path="{path}" keyPoints="0;0;1;1" keyTimes="0;{k(t0):.4f};{k(t1):.4f};1" calcMode="linear" dur="{D}s" repeatCount="indefinite"/>')
        g = f'<g>{mv}{pill}</g>'
    else:
        g = f'<g>{xform("translate", [f"{x0} {y0}", f"{x0} {y0}", f"{x1} {y1}", f"{x1} {y1}"], [0, k(t0), k(t1), 1], D)}{pill}</g>'
    return show(g, [(t0, t1)], D)
b.append(token('5', BLUE, RX + RW - 16, A1, 176, A1, 4.1, 4.9))
b.append(token('3', BLUE, RX + RW - 16, A2, 176, A2, 4.1, 4.9))
# writeback: 8 returns to eax
b.append(token('8', GOLD, 0, 0, 0, 0, 6.1, 6.9, path=f'M 240 {AM} H 264 V {WB} H 20 V {A1} H 40'))
put('fig-1-9', '4 22 292 310', [1.5, 3.2, 5.5, 7.6], ['fetch', 'decode', 'execute', 'writeback'],
    'Fig 1.9 · The instruction cycle',
    'A row of memory bytes holds three instructions, each with its address in hexadecimal beneath: five bytes at 0x00 that put 5 in eax, five at 0x05 that put 3 in ebx, and two, 01 D8, at 0x0A. Below is the CPU. Its program counter, a box holding the address 0x0A, points up at those two bytes. The CPU also has two registers, eax holding 5 and ebx holding 3, and an ALU. Fetch: the two bytes 01 D8 are copied from memory into the CPU. Decode: they are read as add eax, ebx; the ALU is set to add and the two registers are picked. Execute: 5 and 3 travel into the ALU, which shows 8. Writeback: the 8 travels back into eax, and the program counter changes to 0x0C, two bytes on.',
    b,
    caption='One instruction, the two bytes at 0x0A, goes through all four steps.',
    strip=[('Fetch', 'Copy the bytes at the address in the program counter into the CPU.'),
           ('Decode', 'Work out the operation and what it acts on from the bit pattern: 01 D8 means add eax, ebx (Fig 1.10 takes one apart).'),
           ('Execute', 'The ALU (arithmetic logic unit) or another unit does the work: here it adds 5 and 3.'),
           ('Writeback', 'Store the result, here 8 into eax, and move the counter on by the instruction\'s length, two bytes; a jump would set the counter instead.'),
           ('The addresses', 'Every byte has a number. 0x marks hexadecimal: 0x0A is ten, 0x0C twelve. The first two instructions take five bytes each, so the third starts at ten.')])
