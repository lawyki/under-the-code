"""Fig 3.11: the arms race, as a plain timeline read downward: year, dot, name; attacks red, defences green.
Fixed: the dates ran 1998, 2003, 2001+, 2007 (ASLR, 2001, was drawn after the NX bit, 2003, so the figure said ROP
answered ASLR; it answers the NX bit); "1988 · stack overflow" (a buffer overflow); "2017+ · hardware-signed" (only
pointer authentication signs, and it shipped in 2018)."""
from card import *
b = []
ROWS = [('1988', 'buffer overflow', RED), ('1998', 'stack canary', GREEN), ('2001', 'ASLR', GREEN),
        ('2003', 'NX bit', GREEN), ('2007', 'ROP', RED), ('2018', 'checked returns', GREEN)]
Y0, DY, XL = 36, 34, 96
b.append(line(f'M {XL} {Y0} V {Y0 + DY * (len(ROWS) - 1)}', INK, 1.4, ' stroke-opacity="0.5"'))
for i, (year, name, col) in enumerate(ROWS):
    y = Y0 + i * DY
    b.append(text(XL - 16, y + 5, year, 14, MUTE, 'end'))
    b.append(f'<circle cx="{XL}" cy="{y}" r="6.5" fill="{col}"/>')
    b.append(text(XL + 18, y + 5, name, 14, col, 'start'))
card('fig-3-11', 41, 'ch3-defenses-p11', '20 14 300 208',
     'Fig 3.11 · The arms race',
     'A timeline read from top to bottom, each entry a year, a dot and a name. 1988, in red: buffer overflow. 1998, in green: stack canary. 2001, in green: ASLR. 2003, in green: NX bit. 2007, in red: ROP. 2018, in green: checked returns.',
     b,
     caption='Attacks in red, the defences that answered them in green.',
     strip=[('1988', 'One of the Morris worm\'s ways in is a buffer overflow in fingerd.'),
            ('1998 to 2003', 'StackGuard\'s canary; address randomisation, first in the PaX patch for Linux; the NX bit in x86 hardware, after software versions from 1997.'),
            ('2007', 'Return-oriented programming reuses code that is already there, which the NX bit cannot refuse.'),
            ('2018', 'Pointer authentication ships in Apple\'s chips; Intel\'s shadow stack (CET) follows in 2020.')])
