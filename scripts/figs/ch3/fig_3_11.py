"""Fig 3.11: the arms race, as a two-sided timeline read downward: attacks on the left of the line, the defences that
answered them on the right, each with its year, its name and, in plain words, what it is. (The old figure's manner:
a fine line, small marks, three quiet lines to an entry. A first redraw as a column of big coloured dots and bare
acronyms was "worse design".)
Fixed from the old drawing: the dates ran 1998, 2003, 2001+, 2007 (ASLR, 2001, was drawn after the NX bit, 2003, so
the figure said ROP answered ASLR; it answers the NX bit); "1988 · stack overflow" (a buffer overflow); "2017+ ·
hardware-signed" (only pointer authentication signs, and it shipped in 2018)."""
from card import *
b = []
XC = 186
ROWS = [('1988', 'Morris worm', 'a buffer overflow', 'A'), ('1998', 'stack canary', 'a tripwire value', 'D'),
        ('2001', 'ASLR', 'random addresses', 'D'), ('2003', 'NX bit', 'no code on the stack', 'D'),
        ('2007', 'ROP', 'reuses existing code', 'A'), ('2018', 'PAC · shadow stack', 'checked returns', 'D')]
Y0, DY = 62, 44
b.append(cap(XC - 18, 30, 'attack', RED, 'end') + cap(XC + 18, 30, 'defence', GREEN))
b.append(line(f'M {XC} 40 V {Y0 + DY * (len(ROWS) - 1) + 22}', INK, 1, ' stroke-opacity="0.45"'))
for i, (year, name, what, side) in enumerate(ROWS):
    y = Y0 + i * DY
    col = RED if side == 'A' else GREEN
    sx, anchor, ox, oanchor = (XC - 18, 'end', XC + 18, 'start') if side == 'A' else (XC + 18, 'start', XC - 18, 'end')
    b.append(line(f'M {XC} {y} H {XC - 12 if side == "A" else XC + 12}', col, 1.2) + f'<circle cx="{XC}" cy="{y}" r="3.5" fill="{col}"/>')
    b.append(text(sx, y + 1, name, FS, INK, anchor) + text(sx, y + 17, what, FS, MUTE, anchor))
    b.append(text(ox, y + 1, year, FS, MUTE, oanchor))
card('fig-3-11', 41, 'ch3-defenses-p11', '0 14 372 298',
     'Fig 3.11 · The arms race',
     'A timeline read from top to bottom along a centre line, attacks to the left of it in red and defences to the right in green, each with its year. 1988, attack: the Morris worm, a buffer overflow. 1998, defence: the stack canary, a tripwire value. 2001, defence: ASLR, random addresses. 2003, defence: the NX bit, no code on the stack. 2007, attack: ROP, which reuses existing code. 2018, defence: PAC and the shadow stack, checked returns.',
     b,
     caption='Thirty years of move and answer.',
     strip=[('1988', 'One of the Morris worm\'s ways in is a buffer overflow in fingerd.'),
            ('1998 to 2003', 'StackGuard\'s canary; address randomisation, first in the PaX patch for Linux; the NX bit in x86 hardware, after software versions from 1997.'),
            ('2007', 'Return-oriented programming reuses code that is already there, which the NX bit cannot refuse.'),
            ('2018', 'Pointer authentication ships in Apple\'s chips; Intel\'s shadow stack (CET) follows in 2020.')])
