"""Fig 3.10: return-oriented programming, as an idea: the overflowed stack holds a list of return addresses; each
points at a fragment of code that is already in the program and ends in ret; each ret takes the next address. The
fragments are the three kinds the prose names (load a register, add, write a byte). No addresses, no payload.
Fixed: the old chain put its argument in the wrong register and a string where its address belongs, mixed two
different calls, and said RIP "reads down" the stack (it is RSP that walks it)."""
from card import *
D = 6.0
b = []
YS = [152, 104, 56]                      # as every stack in this chapter: highest address at the top, so the first to be used is lowest
OPS = ['load a register', 'add 1', 'write a byte']
b.append(text(108, 38, 'stack', 14, MUTE) + text(286, 38, 'code already there', 14, MUTE))
for i, (y, op) in enumerate(zip(YS, OPS)):
    on = [(i * 2.0, i * 2.0 + 2.0)]
    off = [(0, i * 2.0), (i * 2.0 + 2.0, D)] if i else [(2.0, D)]
    # the return address the attacker wrote
    b.append(show(f'<rect x="56" y="{y}" width="104" height="32" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.6"/>', off, D))
    b.append(show(f'<rect x="56" y="{y}" width="104" height="32" rx="5" fill="none" stroke="{GOLD}" stroke-width="3"/>', on, D))
    b.append(text(108, y + 21, f'return: {i+1}', 14, GOLD))
    # RSP, as in Fig 3.6: each ret moves it up to the next address
    b.append(show(text(40, y + 21, 'RSP', 13, INK, 'end') + f'<path d="M 52 {y+16} l -8 -5 v 10 Z" fill="{INK}"/>', on, D))
    # the fragment it points at
    b.append(show(f'<rect x="202" y="{y}" width="168" height="32" rx="5" fill="none" stroke="{INK}" stroke-opacity="0.7" stroke-width="1.5"/>', off, D))
    b.append(show(f'<rect x="202" y="{y}" width="168" height="32" rx="5" fill="none" stroke="{GOLD}" stroke-width="2.6"/>', on, D))
    b.append(text(212, y + 21, op, 13, INK, 'start') + text(360, y + 21, 'ret', 14, GOLD, 'end'))
    b.append(show(line(f'M 164 {y+16} H 190', INK, 1.5, ' stroke-opacity="0.6"') + f'<path d="M 198 {y+16} l -9 -5 v 10 Z" fill="{INK}" fill-opacity="0.6"/>', off, D))
    b.append(show(line(f'M 164 {y+16} H 190', GOLD, 2.6) + f'<path d="M 198 {y+16} l -9 -5 v 10 Z" fill="{GOLD}"/>', on, D))
card('fig-3-10', 40, 'ch3-defenses-p10', '8 18 370 176',
     'Fig 3.10 · Return-oriented programming',
     'Two columns. On the left, the stack after an overflow, highest address at the top: three gold slots, each a return address the attacker wrote, numbered 1 at the bottom to 3 at the top. On the right, three short fragments of code that already exist in the program: one loads a register, one adds 1, one writes a byte, and each ends in ret. An arrow runs from each return address to its fragment. The pairs light one after another from the bottom, and the stack pointer, RSP, steps up with them: return 1 and its fragment, then return 2 and its fragment, then return 3 and its fragment.',
     b,
     caption='No new code: each return address borrows a fragment that is already there.',
     strip=[('The stack', 'After the overflow, the attacker\'s bytes sit where return addresses belong. They are addresses, not code, so the NX bit has nothing to refuse.'),
            ('A gadget', 'A few instructions that already exist in the program or its libraries and happen to end in <code>ret</code>.'),
            ('The chain', 'Each <code>ret</code> pops the next address off the stack and jumps to it, so the gadgets run in the order the stack lists them (Hovav Shacham, 2007).'),
            ('The answer', 'A shadow stack (Intel CET) or pointer authentication (ARM PAC) checks a return address before <code>ret</code> uses it.')])
