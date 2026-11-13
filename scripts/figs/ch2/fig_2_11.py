"""Fig 2.11: 0.1 + 0.2. Redrawn 2026-11-13 (was three number lines with a legend, an arc, a bracket and a print line,
in two steps). A ruler: its ticks are the only numbers a double can hold near 0.3. Typing 0.3 lands on one tick.
0.1 + 0.2 lands between two ticks and is moved to the next one up, which prints as 0.30000000000000004."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import *
D = 7.0
k = lambda t: t / D
CREAM = '#ece6da'
Y = 96
b = []
b.append(line(f'M 26 {Y} H 334', INK, 1.6, ' stroke-opacity="0.6"'))
for x in (60, 180, 300): b.append(line(f'M {x} {Y-13} V {Y+13}', INK, 2))
# typing 0.3 gives the lower tick
b.append(f'<circle cx="60" cy="{Y}" r="7" fill="{BLUE}"/>' + text(60, Y + 38, '0.3', 15, BLUE))
# 0.1 + 0.2 falls between two ticks, then is moved to the nearer storable number: here the one above
drop = xform('translate', ['0 -28', '0 -28', '0 0', '0 0', '60 0', '60 0'], [0, k(0.9), k(1.6), k(3.0), k(3.9), 1], D)
b.append(show(f'<g>{drop}<circle cx="120" cy="{Y}" r="7" fill="{GOLD}"/>' + text(120, Y - 22, '0.1 + 0.2', 15, GOLD) + '</g>', [(0.6, D)], D))
b.append(show(text(180, Y + 38, '0.30000000000000004', 15, GOLD), [(3.9, D)], D))
put('fig-2-11', '14 22 332 130', None, None,
    'Fig 2.11 · 0.1 + 0.2',
    'A ruler with three tick marks, the only numbers the computer can hold near 0.3. A blue dot sits on the first tick, labelled 0.3: what typing 0.3 stores. A gold dot labelled 0.1 + 0.2 drops onto the ruler between the first and second ticks, where no number can be held, then slides to the second tick, which is labelled 0.30000000000000004.',
    b,
    caption='The ticks are the only numbers a double can hold near 0.3.',
    strip=[('Why it repeats', '0.1 is 1/10, and 10 has a factor of 5 that no power of two can supply, just as 1/3 never ends in decimal.'),
           ('The ticks', 'Doubles are not continuous: the ticks are neighbouring doubles. Near 0.3 neighbours are 2⁻⁵⁴, about 5.6 × 10⁻¹⁷, apart; the true 0.3 falls between two of them.'),
           ('The result', '"0.3" is stored as the double just below it; the rounded 0.1 and 0.2 add up to a value exactly halfway between that double and the next, and the tie rounds up to the next. So in most languages 0.1 + 0.2 == 0.3 is false.'),
           ('Living with it', 'Compare floats within a tolerance, and count money in whole cents.')])
