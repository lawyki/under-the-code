"""Fig 3.8: the stack canary. Fig 3.7's frame with one row added, the canary, and the check that runs before ret,
told as the old figure told it: normal against overflow, each row saying what it holds, the check answering yes or no.
Fixed from the old drawing: the italic line drawn over both check boxes; a header that promised "the same overflow"
and drew another (buf[64], 200 bytes): this is Fig 3.7's frame and Fig 3.7's attack, eight bytes longer."""
from card import *
D = 10.0
TA = 4.0
T_BUF, T_CAN, T_RBP, T_RET, T_OUT = TA + 0.6, TA + 1.4, TA + 2.2, TA + 3.0, TA + 3.8
Y_RET, Y_RBP, Y_CAN, Y_BUF, Y_CHK = 44, 86, 128, 170, 222
b = []
b.append(show(run(FX, 32, [('NORMAL', GREEN), (' · canary intact', MUTE)]), [(0, TA)], D))
b.append(show(run(FX, 32, [('OVERFLOW', RED), (' · canary overwritten', MUTE)]), [(TA, D)], D))
def flips(y, name, normal, col, attack, t, name_col=MUTE):
    b.append(show(frow(y, name, normal, col, name_col), [(0, t)], D))
    b.append(show(frow(y, name, attack, RED), [(t, D)], D))
flips(Y_RET, 'return address', [('back to main', GOLD)], GOLD, [('the address of the buffer', RED)], T_RET)
flips(Y_RBP, 'saved rbp', [("main's frame pointer", BLUE)], BLUE, [('BBBBBBBB', RED), ('  overwritten', MUTE)], T_RBP)
flips(Y_CAN, 'canary', [('3a f1 07 c9 5e b2 8d 64', GREEN), ('  random', MUTE)], GREEN, [('AAAAAAAA', RED), ('  no longer matches', MUTE)], T_CAN, GREEN)
flips(Y_BUF, 'buffer · 16 bytes', [('Tiger\\0', INK), ('  + 10 unused', MUTE)], INK, [('AAAAAAAAAAAAAAAA', RED), ('  full', MUTE)], T_BUF)
b.append(upward(Y_BUF + FH, Y_RET, 'the copy runs upward', [(T_BUF, D)], D))
Q = 'before ret: is the canary unchanged?'
b.append(show(verdict(Y_CHK, Q, 'yes  →  return to main', GREEN), [(0, TA)], D))
b.append(show(verdict(Y_CHK, Q, 'no  →  the program stops', RED), [(T_OUT, D)], D))
card('fig-3-8', 38, 'ch3-defenses-p4', '0 14 372 256',
     'Fig 3.8 · The stack canary',
     'The frame of Fig 3.7 with one row added, and under it the check that runs before ret. First the normal case. From the top: the return address holds: back to main. The saved RBP holds main\'s frame pointer. The canary holds eight random bytes. The buffer holds Tiger and a zero byte, with 10 bytes unused. The check asks: is the canary unchanged? Yes: return to main. Then the overflow. The copy runs upward: the buffer fills with sixteen A\'s; the canary is overwritten with eight more A\'s and no longer matches; the saved RBP is overwritten with B\'s; the return address is replaced with the address of the buffer. The check asks again: is the canary unchanged? No: the program stops.',
     b,
     caption='To reach the return address, the overflow has to cross the canary.',
     strip=[('The canary', 'A random value, picked when the program starts (StackGuard, 1998). A function that holds a buffer keeps it just above its local variables, below the saved RBP and the return address.'),
            ('The check', 'Code the compiler adds before <code>ret</code> compares the canary with the original. If they differ, the program aborts, and the forged return address is never used.'),
            ('The limit', 'It holds only while the value stays secret: a separate bug that leaks memory can reveal the canary, and an attacker who knows it writes it back in place.')],
     beats=[2.0, 9.2], names=['normal', 'overflow'])
