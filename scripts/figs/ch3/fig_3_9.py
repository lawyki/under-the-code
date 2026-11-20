"""Fig 3.9: ASLR. Three launches of one program side by side: the same four blocks, in the same order, at different
heights. One dashed red line runs across all three at the height of the libraries in the first launch: the address an
attacker learned there. In the other two it points at nothing.
Fixed: "~16 bits of randomness" (the 32-bit figure; the strip gives the one documented 64-bit number, 28 bits for
libraries, in place of the old caption's three unsourced ranges); the heap drawn above the program
with an address below it; "within seconds" against stamps minutes apart; the low-to-high axis that ran sideways."""
from card import *
b = []
COLS = [(14, 'launch 1', dict(stack=52, libraries=104, heap=168, code=192)),
        (128, 'launch 2', dict(stack=76, libraries=140, heap=178, code=202)),
        (242, 'launch 3', dict(stack=46, libraries=80, heap=140, code=164))]
COL = dict(stack=GOLD, libraries=GREEN, heap=BLUE, code=INK)
AIM, W = 116, 104
for x, name, ys in COLS:
    b.append(text(x + W / 2, 30, name, 14, MUTE))
    b.append(f'<rect x="{x}" y="40" width="{W}" height="192" rx="6" fill="none" stroke="{INK}" stroke-opacity="0.45" stroke-width="1.2"/>')
    for part, y in ys.items():
        b.append(f'<rect x="{x+5}" y="{y}" width="{W-10}" height="24" rx="4" fill="none" stroke="{COL[part]}" stroke-width="1.6"/>')
        b.append(text(x + W / 2, y + 17, part, 14, COL[part]))
# the attacker's one address, the same height in every launch: it reaches the libraries in the first only
dash = lambda x0, x1: b.append(line(f'M {x0} {AIM} H {x1}', RED, 2, ' stroke-dasharray="4 4"'))
dash(2, 14)                               # into launch 1's libraries
dash(113, 133); dash(137, 227)            # across launch 2: empty
dash(227, 247); dash(251, 356)            # across launch 3: empty
b.append(f'<circle cx="19" cy="{AIM}" r="5" fill="{RED}"/>')          # launch 1: it lands on the libraries
for cx in (180, 294):
    b.append(line(f'M {cx-6} {AIM-6} l 12 12 m 0 -12 l -12 12', RED, 2.4))
b.append(text(180, 252, 'the address the attacker aims at', 14, RED))
card('fig-3-9', 39, 'ch3-defenses-p7', '0 12 360 248',
     'Fig 3.9 · ASLR',
     'Three launches of the same program, side by side, each drawn as a tall column of memory with the highest addresses at the top. Every column holds the same four blocks in the same order: the stack at the top, then the libraries, then the heap resting on the program\'s code at the bottom. In each launch the blocks sit at different heights. A dashed red line, the one address an attacker aims at, crosses all three columns at the same height. In the first launch it lands on the libraries, marked with a dot. In the second and third it passes through empty space, marked with a cross.',
     b,
     caption='An address that worked in one launch points at nothing in the next.',
     strip=[('Each launch', 'The operating system loads the code, the libraries, the heap and the stack at fresh random addresses. Their order stays; their positions do not. Not to scale.'),
            ('How random', 'On 64-bit Linux a library can land in any of about 268 million places (28 random bits), and one wrong guess crashes the program.'),
            ('The limit', 'A library loads as one block, so a single leaked address locates all of it.')])
