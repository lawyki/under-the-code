"""Fig 3.7: a buffer overflow. One frame, not two side by side: greet()'s frame as Fig 3.6 draws a stack (highest
address at the top): the return address, main's saved RBP, the 16-byte buffer as sixteen cells. "Tiger" fits. Then a
name too long: the A's fill the buffer and climb on through the saved RBP and the return address.
Fixed: "Tiger\\0" + 11 unused bytes (it is 10: the cells show it); the frame no longer runs the opposite way to
Figs 3.5, 3.6 and 3.8."""
from card import *
D = 9.0
T_OVER, STEP = 3.0, 0.11
t_cell = lambda k: T_OVER + 0.2 + k * STEP          # when the k-th copied byte lands (k = 0 .. 31)
Y_RET, Y_RBP, Y_B2, Y_B1 = 40, 74, 114, 144
b = []
# the two saved values above the buffer: as they should be, then overwritten
XS = X0 + 8 * CW + 12                   # names stand to the right of their rows
for y, col, name, was, k0 in ((Y_RET, GOLD, 'return: main', 'return address', 24), (Y_RBP, BLUE, "main's rbp", 'saved rbp', 16)):
    t = t_cell(k0)
    b.append(row(y, col, [(0, t)], D))
    b.append(show(text(X0 + 4 * CW, y + 20, name, 14, col), [(0, t)], D))
    b.append(show(row(y, RED, None, D, 2.2) + cells(y) + text(XS, y + 20, was, 14, RED, 'start'), [(t, D)], D))     # overwritten: its name moves outside
    for i in range(8): b.append(show(letter(i, y, 'A', RED), [(t_cell(k0 + i), D)], D))
# the buffer: sixteen bytes, lowest address at the bottom left
b.append(row(Y_B2, INK, None, D) + cells(Y_B2) + row(Y_B1, INK, None, D) + cells(Y_B1))
b.append(text(XS, Y_B2 + RH + 5, 'buffer', 14, MUTE, 'start'))
for i, ch in enumerate('Tiger'): b.append(show(letter(i, Y_B1, ch, INK), [(0, T_OVER)], D))
b.append(show(letter(5, Y_B1, '\\0', MUTE, 13), [(0, T_OVER)], D))
for k in range(16):
    y, i = (Y_B1, k) if k < 8 else (Y_B2, k - 8)
    b.append(show(letter(i, y, 'A', INK), [(t_cell(k), D)], D))
card('fig-3-7', 37, 'ch3-overflow-p4', '6 30 362 154',
     'Fig 3.7 · A buffer overflow',
     'The stack frame of greet(), drawn with the highest address at the top, as in Fig 3.6. From the top: a gold row holding the return address into main; a blue row holding main\'s saved RBP; and the buffer, sixteen byte cells in two rows, the lowest address at the bottom left. First the name Tiger is copied in: five letters and a zero byte fill six cells and ten stay empty; the two rows above are untouched. Then a name of thirty-two A\'s is copied in: the A\'s fill all sixteen cells of the buffer, then climb on, replacing the saved RBP and then the return address; those two rows turn red and their names, saved rbp and return address, appear beside them.',
     b,
     caption='On <code>ret</code>, the CPU jumps to whatever the return row holds.',
     strip=[('The frame', 'As in Fig 3.6: <code>call</code> pushed the return address, greet() saved main\'s RBP under it, and the 16-byte buffer sits below both, at the lowest addresses.'),
            ('The copy', '<code>strcpy</code> fills the buffer from its lowest address upward and stops only at a zero byte. "Tiger" and its zero take 6 bytes and leave 10 unused.'),
            ('Too long', 'Thirty-two A\'s: 16 fill the buffer, the next 8 replace the saved RBP, the last 8 the return address. An attacker writes chosen bytes where the A\'s are.')],
     beats=[1.0, 8.0], names=['fits', 'too long'])
