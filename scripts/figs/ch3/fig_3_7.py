"""Fig 3.7: a buffer overflow, told as the old figure told it: a normal call against an attack, every row saying what
it is and what it holds, and a line saying what ret then does. One frame, switched between the two cases (a phone
cannot hold two side by side), drawn as Fig 3.6 draws a stack: highest address at the top.
Fixed from the old drawing: "Tiger\\0" + 11 unused bytes (10); the frame ran the opposite way to Figs 3.5, 3.6, 3.8."""
from card import *
D = 10.0
TA = 4.0                                  # the attack begins
T_BUF, T_RBP, T_RET, T_OUT = TA + 0.6, TA + 1.5, TA + 2.4, TA + 3.3
Y_RET, Y_RBP, Y_BUF, Y_OUT = 44, 86, 128, 188
b = []
b.append(show(run(FX, 32, [('NORMAL', GREEN), (' · name = "Tiger"', MUTE)]), [(0, TA)], D))
b.append(show(run(FX, 32, [('ATTACK', RED), (' · a name of 32 chosen bytes', MUTE)]), [(TA, D)], D))
def flips(y, name, normal, col, attack, t):
    b.append(show(frow(y, name, normal, col), [(0, t)], D))
    b.append(show(frow(y, name, attack, RED), [(t, D)], D))
flips(Y_RET, 'return address', [('back to main', GOLD)], GOLD, [('the address of the buffer', RED)], T_RET)
flips(Y_RBP, 'saved rbp', [("main's frame pointer", BLUE)], BLUE, [('BBBBBBBB', RED), ('  overwritten', MUTE)], T_RBP)
flips(Y_BUF, 'buffer · 16 bytes', [('Tiger\\0', INK), ('  + 10 unused', MUTE)], INK, [('AAAAAAAAAAAAAAAA', RED), ('  full', MUTE)], T_BUF)
b.append(upward(Y_BUF + FH, Y_RET, 'the copy runs upward', [(T_BUF, D)], D))
b.append(show(run(FX, Y_OUT, [('ret', INK), ('  →  returns to main', GREEN)]), [(0, TA)], D))
b.append(show(run(FX, Y_OUT, [('ret', INK), ('  →  runs the attacker\'s bytes', RED)]), [(T_OUT, D)], D))
card('fig-3-7', 37, 'ch3-overflow-p4', '0 14 372 186',
     'Fig 3.7 · A buffer overflow',
     'The stack frame of greet(), highest address at the top, as in Fig 3.6: three rows, each naming what it is and what it holds. First the normal case, the name Tiger. The return address holds: back to main. The saved RBP holds main\'s frame pointer. The buffer, 16 bytes, holds Tiger and a zero byte, with 10 bytes unused. Below, what ret does: it returns to main. Then the attack, a name of 32 chosen bytes. The copy runs upward: the buffer fills with sixteen A\'s; the saved RBP is overwritten with eight B\'s; the return address is replaced with the address of the buffer. Below, what ret does now: it runs the attacker\'s bytes.',
     b,
     caption='No bounds check: <code>strcpy</code> keeps writing, and a return address is only bytes.',
     strip=[('The frame', 'As in Fig 3.6: <code>call</code> pushed the return address, greet() saved main\'s RBP under it, and the 16-byte buffer sits below both, at the lowest addresses.'),
            ('The copy', '<code>strcpy</code> fills the buffer from its lowest address upward and stops only at a zero byte. "Tiger" and its zero take 6 bytes and leave 10 unused.'),
            ('The attack', 'Thirty-two bytes: 16 fill the buffer (the A\'s, where the attacker\'s own code would go), 8 run over the saved RBP, and the last 8 replace the return address with the address of the buffer.')],
     beats=[2.0, 9.0], names=['normal', 'attack'])
