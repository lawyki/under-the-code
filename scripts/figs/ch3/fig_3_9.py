"""Fig 3.9: ASLR. Three launches of one program side by side: the same four blocks, in the same order, at different
heights. One dashed red line runs across all three at the height of the libraries in the first launch: the address an
attacker learned there. Under each launch, in a word, what that address finds: a hit, then two misses.
Fixed from the old drawing: "~16 bits of randomness" (the 32-bit figure; the strip gives the one documented 64-bit
number, 28 bits for libraries, in place of the old caption's three unsourced ranges); the heap drawn above the program
with an address below it; "within seconds" against stamps minutes apart; the low-to-high axis that ran sideways."""
from card import *
b = []
W = 108
COLS = [(12, 'launch 1', dict(stack=62, libraries=112, heap=176, code=198), ('hit', RED)),
        (132, 'launch 2', dict(stack=86, libraries=150, heap=188, code=210), ('miss', GREEN)),
        (252, 'launch 3', dict(stack=56, libraries=90, heap=152, code=174), ('miss', GREEN))]
COL = dict(stack=GOLD, libraries=GREEN, heap=BLUE, code=INK)
AIM = 123
for x, name, ys, (res, rc) in COLS:
    b.append(cap(x + W / 2, 44, name, MUTE, 'middle'))
    b.append(f'<rect x="{x}" y="50" width="{W}" height="190" rx="{RX}" fill="none" stroke="{INK}" stroke-opacity="0.4" stroke-width="1"/>')
    for part, y in ys.items():
        b.append(f'<rect x="{x+6}" y="{y}" width="{W-12}" height="22" rx="{RX}" fill="none" stroke="{COL[part]}" stroke-width="{SW}"/>')
        b.append(text(x + W / 2, y + 15.5, part, FS, COL[part]))
    b.append(cap(x + W / 2, 258, res, rc, 'middle'))
# the attacker's one address, the same height in every launch: it reaches the libraries in the first only
dash = lambda x0, x1: b.append(line(f'M {x0} {AIM} H {x1}', RED, 1.3, ' stroke-dasharray="4 4"'))
dash(2, 16)
b.append(f'<circle cx="18" cy="{AIM}" r="3.5" fill="{RED}"/>')
dash(124, 180); dash(192, 300); dash(312, 368)
for cx in (186, 306):
    b.append(line(f'M {cx-4.5} {AIM-4.5} l 9 9 m 0 -9 l -9 9', RED, 1.8))
b.append(run(186, 280, [('- - -  the address the attacker aims at', RED)], 'middle'))
card('fig-3-9', 39, 'ch3-defenses-p7', '0 28 372 260',
     'Fig 3.9 · ASLR',
     'The same program, launched three times, each launch drawn as a tall column of memory with the highest addresses at the top. Every column holds the same four blocks in the same order: the stack at the top, then the libraries, then the heap resting on the program\'s code at the bottom. In each launch the blocks sit at different heights. A dashed red line, the one address an attacker aims at, crosses all three columns at the same height. In the first launch it lands on the libraries: a hit. In the second and third it passes through empty space: a miss, and the program crashes.',
     b,
     caption='An address learned in one launch points at nothing in the next.',
     strip=[('Each launch', 'The operating system loads the code, the libraries, the heap and the stack at fresh random addresses. Their order stays; their positions do not. Not to scale.'),
            ('How random', 'On 64-bit Linux a library can land in any of about 268 million places (28 random bits), and one wrong guess crashes the program.'),
            ('The limit', 'A library loads as one block, so a single leaked address locates all of it.')])
