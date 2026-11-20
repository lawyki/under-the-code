"""Fig 3.8: the stack canary. Fig 3.7's frame with one row added: the canary, between the buffer and the saved values.
An overflow like Fig 3.7's runs (a longer name: forty A's, to reach the return address past the extra row); the A's cross the canary on their way up. Before ret the canary is checked: it has changed, and
the program stops. Fixed: the italic line drawn over both check boxes; the header that promised "the same overflow"
and drew a different one (buf[64], 200 bytes): it now is Fig 3.7's."""
from card import *
D = 10.0
T_OVER, STEP = 1.6, 0.11
t_cell = lambda k: T_OVER + 0.2 + k * STEP          # k = 0 .. 39: buffer 16, canary 8, rbp 8, return 8
T_CHECK = 7.0
Y_RET, Y_RBP, Y_CAN, Y_B2, Y_B1 = 40, 74, 108, 148, 178
b = []
XS = X0 + 8 * CW + 12
for y, col, name, was, k0 in ((Y_RET, GOLD, 'return: main', 'return address', 32), (Y_RBP, BLUE, "main's rbp", 'saved rbp', 24), (Y_CAN, GREEN, None, None, 16)):
    t = t_cell(k0)
    b.append(row(y, col, [(0, t)], D))
    if name: b.append(show(text(X0 + 4 * CW, y + 20, name, 14, col), [(0, t)], D))
    else:                                # the canary holds a random value: eight bytes that mean nothing
        b.append(show(''.join(letter(i, y, h, GREEN, 13) for i, h in enumerate(['3a', 'f1', '07', 'c9', '5e', 'b2', '8d', '64'])), [(0, t)], D))
    b.append(show(row(y, RED, None, D, 2.2) + cells(y) + (text(XS, y + 20, was, 14, RED, 'start') if was else ''), [(t, D)], D))
    for i in range(8): b.append(show(letter(i, y, 'A', RED), [(t_cell(k0 + i), D)], D))
b.append(row(Y_B2, INK, None, D) + cells(Y_B2) + row(Y_B1, INK, None, D) + cells(Y_B1))
b.append(text(XS, Y_B2 + RH + 5, 'buffer', 14, MUTE, 'start'))
for k in range(16):
    y, i = (Y_B1, k) if k < 8 else (Y_B2, k - 8)
    b.append(show(letter(i, y, 'A', INK), [(t_cell(k), D)], D))
# the canary's name, and the check that runs just before ret
b.append(show(text(XS, Y_CAN + 20, 'canary', 14, GREEN, 'start'), [(0, T_CHECK)], D))
b.append(show(text(XS, Y_CAN + 20, 'changed: stop', 14, RED, 'start'), [(T_CHECK, D)], D))
card('fig-3-8', 38, 'ch3-defenses-p4', '6 30 362 188',
     'Fig 3.8 · The stack canary',
     'The frame of Fig 3.7 with one row added. From the top: the return address into main, main\'s saved RBP, a green row labelled canary, holding eight random bytes, and the sixteen byte cells of the buffer. The same overlong name is copied in: the A\'s fill the buffer, then cross the canary, the saved RBP and the return address, and those three rows turn red. Then, beside the canary row, the result of the check that runs just before ret appears: changed, stop.',
     b,
     caption='The check runs just before <code>ret</code>, so the forged return address is never used.',
     strip=[('The canary', 'A random value, picked when the program starts (StackGuard, 1998). A function that holds a buffer keeps it just above its local variables, below the saved RBP and the return address.'),
            ('The check', 'Code the compiler adds before <code>ret</code> compares the canary with the original. If they differ, the program aborts.'),
            ('The limit', 'It holds only while the value stays secret: a separate bug that leaks memory can reveal the canary, and an attacker who knows it writes it back in place.')],
     beats=[0.8, 6.4, 9.0], names=['before', 'overflow', 'check'])
