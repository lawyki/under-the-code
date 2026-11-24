"""Fig 3.10: return-oriented programming, told as the old figure told it but as an idea only: on the left the smashed
stack, a list of return addresses the attacker wrote; on the right, fragments of code that were already in the program,
each ending in ret; each address points at its fragment, and they run in the order listed. The fragments are the three
kinds the prose names (load a register, increment a counter, write a byte). No real addresses, no payload.
Fixed from the old drawing: its chain put its argument in the wrong register and a string where its address belongs,
mixed two different calls, and said RIP "reads down" the stack (the list is headed by its order of use, not as a stack)."""
from card import *
D = 6.0
b = []
YS = [80, 130, 180]
OPS = ['load a register', 'add 1', 'write a byte']
b.append(run(8, 26, [('NO NEW CODE', RED), (' · only fragments already there', MUTE)]))
b.append(cap(82, 52, 'smashed stack', RED, 'middle') + text(82, 68, 'in order of use', FS, MUTE))
b.append(cap(282, 52, 'existing code', GOLD, 'middle') + text(282, 68, 'each ends in ret', FS, MUTE))
for i, (y, op) in enumerate(zip(YS, OPS)):
    on = [(i * 2.0, i * 2.0 + 2.0)]
    off = [(0, i * 2.0), (i * 2.0 + 2.0, D)] if i else [(2.0, D)]
    b.append(show(f'<rect x="8" y="{y}" width="148" height="{FH}" rx="{RX}" fill="none" stroke="{RED}" stroke-opacity="0.8" stroke-width="{SW}"/>', off, D))
    b.append(show(f'<rect x="8" y="{y}" width="148" height="{FH}" rx="{RX}" fill="none" stroke="{RED}" stroke-width="2"/>', on, D))
    b.append(cap(20, y + 15, 'return address', MUTE) + text(20, y + 31, f'→ fragment {i+1}', FS, INK, 'start'))
    b.append(show(f'<rect x="204" y="{y}" width="160" height="{FH}" rx="{RX}" fill="none" stroke="{GOLD}" stroke-opacity="0.8" stroke-width="{SW}"/>', off, D))
    b.append(show(f'<rect x="204" y="{y}" width="160" height="{FH}" rx="{RX}" fill="none" stroke="{GOLD}" stroke-width="2"/>', on, D))
    b.append(text(216, y + 15, op, FS, INK, 'start') + text(216, y + 31, 'ret', FS, GOLD, 'start'))      # a listing: one instruction to a line
    b.append(show(line(f'M 160 {y+19} H 192', GOLD, 1.2, ' stroke-dasharray="4 3" stroke-opacity="0.7"') + f'<path d="M 200 {y+19} l -8 -4 v 8 Z" fill="{GOLD}" fill-opacity="0.7"/>', off, D))
    b.append(show(line(f'M 160 {y+19} H 192', GOLD, 2) + f'<path d="M 200 {y+19} l -8 -4 v 8 Z" fill="{GOLD}"/>', on, D))
card('fig-3-10', 40, 'ch3-defenses-p10', '0 10 372 216',
     'Fig 3.10 · Return-oriented programming',
     'Headed: no new code, only fragments already there. Two columns. On the left, the smashed stack: three return addresses the attacker wrote, in order of use, pointing at fragment 1, fragment 2 and fragment 3. On the right, existing code: three short fragments that were already in the program, each ending in ret. Fragment 1 loads a register, fragment 2 adds 1, fragment 3 writes a byte. A dashed arrow runs from each return address to its fragment, and the pairs light one after another from the top.',
     b,
     caption='Every fragment ends in <code>ret</code>, and each <code>ret</code> takes the next address: the stack is the program.',
     strip=[('The stack', 'After the overflow, the attacker\'s bytes sit where return addresses belong. They are addresses, not code, so the NX bit has nothing to refuse.'),
            ('A gadget', 'A few instructions that already exist in the program or its libraries and happen to end in <code>ret</code>.'),
            ('The chain', 'Each <code>ret</code> pops the next address off the stack and jumps to it, so the gadgets run in the order the stack lists them (Hovav Shacham, 2007).'),
            ('The answer', 'A shadow stack (Intel CET) or pointer authentication (ARM PAC) checks a return address before <code>ret</code> uses it.')])
