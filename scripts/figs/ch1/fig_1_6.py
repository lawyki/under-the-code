"""Fig 1.6: Moore's Law as a zoom. 2,300 dots fill the square; every twenty years of doubling (x1,024)
the whole picture shrinks into one gold tile of the next; 2024 is twelve of the 2011 squares."""
from plate import *
D = 12.0
X, Y, S = 60, 86, 240
T = 0.9                                   # zoom time at the start of each step
k = lambda t: t / D
defs = (f'<defs>'
        f'<pattern id="f16-dots" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.45" fill="{INK}"/></pattern>'
        f'<pattern id="f16-tiles" width="7.5" height="7.5" patternUnits="userSpaceOnUse"><rect x="0.9" y="0.9" width="5.7" height="5.7" rx="0.8" fill="{INK}" fill-opacity="0.42"/></pattern>'
        f'<pattern id="f16-fine" width="7.5" height="7.5" patternUnits="userSpaceOnUse" patternTransform="translate({X} {Y+30}) scale(0.25)"><rect x="0.9" y="0.9" width="5.7" height="5.7" fill="{INK}" fill-opacity="0.42"/></pattern>'
        f'<pattern id="f16-tdots" width="4" height="4" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{INK}"/></pattern>'
        f'<pattern id="f16-ttiles" width="4" height="4" patternUnits="userSpaceOnUse"><rect x="0.6" y="0.6" width="2.8" height="2.8" fill="{INK}" fill-opacity="0.5"/></pattern>'
        f'</defs>')
def shrink(inner, t0, s, t_hide, dy=0):
    """inner (drawn in a 0..S box) sits at (X,Y); from t0 it shrinks toward its top-left corner to scale s (and slides down dy)."""
    slide = xform('translate', [f'{X} {Y}', f'{X} {Y}', f'{X} {Y+dy}', f'{X} {Y+dy}', f'{X} {Y}'], [0, k(t0), k(t0 + T), 0.999, 1], D) if dy else ''
    g = (f'<g transform="translate({X} {Y})">{slide}<g>'
         + xform('scale', ['1', '1', f'{s}', f'{s}', '1'], [0, k(t0), k(t0 + T), 0.999, 1], D) + inner + '</g></g>')
    return g
def fade(inner, t0, t1):
    """fades in over [t0, t0+T], stays until t1."""
    ks = [0, k(t0), k(t0 + T), k(t1) if t1 < D else 0.999, 1] ; vs = [0, 0, 1, 1, 0]
    return f'<g opacity="0">{anim("opacity", vs, ks, D)}{inner}</g>'
frame = f'<rect x="0" y="0" width="{S}" height="{S}" rx="3" fill="none" stroke="{INK}" stroke-opacity="0.5" stroke-width="1.2"/>'
gold_tile = f'<rect x="0.9" y="0.9" width="5.7" height="5.7" rx="0.8" fill="{GOLD}"/>'
grid = f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#f16-tiles)"/>' + gold_tile + frame
body = [defs]
# 1971: the dots; they shrink into the first tile at 3 s
body.append(show(shrink(f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#f16-dots)"/>' + frame, 3.0, 1 / 32, 0), [(0, 3.0 + T)], D))
# 1991: a 32 x 32 grid of such squares; it shrinks into the first tile at 6 s
body.append(show(fade(shrink(grid, 6.0, 1 / 32, 0), 3.0, 6.0 + T), [(3.0, 6.0 + T)], D))
# 2011: again; it shrinks to a quarter at 9 s and eleven more join it
body.append(show(fade(shrink(grid, 9.0, 0.25, 0, 30), 6.0, D), [(6.0, D)], D))
others = ''
for i in range(1, 12):
    cx, cy = i % 4, i // 4
    others += (f'<rect x="{X + cx*60}" y="{Y + 30 + cy*60}" width="60" height="60" fill="url(#f16-fine)"/>'
               f'<rect x="{X + cx*60}" y="{Y + 30 + cy*60}" width="60" height="60" rx="1" fill="none" stroke="{INK}" stroke-opacity="0.5" stroke-width="1"/>')
body.append(show(fade(others, 9.0, D), [(9.0, D)], D))
body.append(show(f'<rect x="{X}" y="{Y+30}" width="60" height="60" rx="1" fill="none" stroke="{GOLD}" stroke-width="2"/>', [(9.0 + T, D)], D))
# the gold tile, magnified: a thumbnail of the picture before, joined to the tile by two fine lines
TH = 52; TY = Y - 70
def thumb(kind):
    if kind == 'dots':
        inner = f'<rect x="{X}" y="{TY}" width="{TH}" height="{TH}" fill="url(#f16-tdots)"/>'
    else:
        inner = f'<rect x="{X}" y="{TY}" width="{TH}" height="{TH}" fill="url(#f16-ttiles)"/><rect x="{X+1}" y="{TY+1}" width="3.4" height="3.4" fill="{GOLD}"/>'
    return (inner + f'<rect x="{X}" y="{TY}" width="{TH}" height="{TH}" rx="2" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
            + line(f'M {X} {TY+TH} L {X+0.9} {Y+0.9} M {X+TH} {TY+TH} L {X+6.6} {Y+0.9}', GOLD, 1))
for yr, kind, a, b_ in (('1971', 'dots', 3.0 + T, 6.0), ('1991', 'tiles', 6.0 + T, 9.0)):
    body.append(show(thumb(kind) + text(X + TH + 12, TY + 22, yr, 14, GOLD, 'start') + text(X + TH + 12, TY + 42, '×1,024', 14, MUTE, 'start'), [(a, b_)], D))
body.append(show(text(X, Y + 22, '2011', 14, GOLD, 'start') + text(X + S, Y + 22, '×12', 14, MUTE, 'end'), [(9.0 + T, D)], D))
labels = [('1971', '2,300', 0, 3.0), ('1991', '2.4 million', 3.0, 6.0), ('2011', '2.4 billion', 6.0, 9.0), ('2024', '28 billion', 9.0, D)]
for yr, n, a, b in labels:
    body.append(show(text(X, Y + S + 26, yr, 16, MUTE, 'start') + text(X + S, Y + S + 26, n, 16, GOLD if a else INK, 'end'), [(a, b)], D))
put('fig-1-6', f'{X-22} 8 {S+44} {S+114}', [1.5, 5.0, 8.0, 11.0], ['1971', '1991', '2011', '2024'],
    'Fig 1.6 · Moore\'s Law · transistors on one chip',
    'A square filled with 2,300 dots, one per transistor of the 1971 Intel 4004. Twenty years of doubling later, in 1991, the whole square has shrunk to a single small gold tile in a grid of 1,024 such tiles: about 2.4 million transistors. In 2011 that whole grid is again one gold tile among 1,024: about 2.4 billion. In 2024 the 2011 picture is one of twelve: the 28 billion transistors of the Apple M4.',
    body,
    caption='Each gold square is the whole picture before it.',
    strip=[('The dots', 'The first square holds 2,300 dots, one for each transistor of the Intel 4004 (1971).'),
           ('A thousandfold', 'Doubling every two years is ten doublings in twenty years: 2 × 2 × 2, ten times over, is 1,024. So each step packs 1,024 copies of the picture before it into the same square.'),
           ('On the line', 'Real chips kept close to it: about 1.2 million transistors in 1989 and 3.1 million in 1993; 2.3 to 2.6 billion in the largest processors of 2011.'),
           ('The slowdown', 'Thirteen more years at the old pace would have made 90 copies by 2024. The Apple M4 has 28 billion transistors: twelve.'),
           ('Not a law', 'Moore described what the industry was doing, and the industry then planned by it; nothing in physics promised it.')],
    label='Fig 1.6&nbsp;· Moore\'s Law&nbsp;· transistors on one chip')
