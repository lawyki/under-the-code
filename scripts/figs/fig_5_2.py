# Fig 5.2 · UNIX's rewrite, in time (Pass 28, law 3). A vertical timeline; the axis is coloured by the
# language UNIX's own source was written in: assembly to 1973, then C. A cursor steps year by year;
# 1977 shows the payoff, a port to a different machine. t=0 (shift): the whole timeline.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

EVENTS = [('1969', 'UNIX on a PDP-7, in assembly', 'asm'),
          ('1969', 'B: Thompson\'s typeless language', None),
          ('1970', 'PDP-11 arrives: byte-addressed', None),
          ('1971', 'First Edition: PDP-11 assembly', 'asm'),
          ('1972', 'C: B plus types', None),
          ('1973', 'UNIX rewritten in C', 'c'),
          ('1977', 'ported to the Interdata 8/32', 'c'),
          ('1978', 'K&amp;R: the C book, 228 pages', None)]
W = 400
AX = 74
Y0, P = 52, 34
REWRITE = 5
D = 10.0
T = Timeline(D, shift=9.4)
RESET = 0.4
step = lambda i: 0.8 + 0.85 * i
ry = lambda i: Y0 + i * P
o = []; a = o.append
H = ry(len(EVENTS) - 1) + 30
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-26 svgd-part2-26">')
a('<title id="svgt-part2-26">Fig 5.2 · UNIX\'s rewrite, in time</title>')
a('<desc id="svgd-part2-26">A timeline from 1969 to 1978, coloured by the language UNIX itself was written in. 1969: UNIX on a PDP-7, in assembly; Thompson\'s typeless language B. '
  '1970: the byte-addressed PDP-11 arrives. 1971: the First Edition, in PDP-11 assembly. 1972: C, which is B plus types. '
  '1973: UNIX is rewritten in C, and the colour changes from assembly to C. 1977: UNIX is ported to the Interdata 8/32. 1978: Kernighan and Ritchie\'s book on C, 228 pages.</desc>')
a(text(20, 22, 'UNIX source in:', size=13, fill=MUTED, ls='0'))
a(f'<rect x="150" y="12" width="12" height="12" rx="2" fill="{GOLD}"/>')
a(text(168, 22, 'assembly', size=13, fill=GOLD, ls='0'))
a(f'<rect x="250" y="12" width="12" height="12" rx="2" fill="{PHOS}"/>')
a(text(268, 22, 'C', size=13, fill=PHOS, ls='0'))
# axis, coloured by language, filling with the cursor
ya, yb, yc = ry(0) - 12, ry(REWRITE), ry(len(EVENTS) - 1) + 8
a(f'<rect x="{AX - 3}" y="{ya}" width="6" height="{yc - ya}" rx="3" fill="rgba(198,222,206,0.12)"/>')
def grow(y_top, y_bot, col, t0, t1):
    h = y_bot - y_top
    a(f'<rect x="{AX - 3}" y="{y_top}" width="6" height="{h}" rx="3" fill="{col}">'
      f'{T.anim("height", [(0.0, h), (RESET, h), (RESET + 0.005, 0.0), (t0, 0.0), (t1, h), (D, h)])}</rect>')
grow(ya, yb, GOLD, step(0), step(REWRITE))
grow(yb, yc, PHOS, step(REWRITE), step(len(EVENTS) - 1) + 0.3)
for i, (yr, ev, lang) in enumerate(EVENTS):
    y = ry(i)
    t = step(i)
    dim = T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.3), (t - 0.002, 0.3), (t, 1.0), (D, 1.0)])
    hot = i == REWRITE
    a(f'<g>{dim}')
    a(text(20, y + 5, yr, size=13, fill='#fff' if hot else MUTED, ls='0'))
    a(f'<circle cx="{AX}" cy="{y}" r="{7 if hot else 5}" fill="{PLATE}" stroke="{PHOS if hot else PHOS_SOFT}" stroke-width="{2.5 if hot else 1.5}"/>')
    if hot:
        a(f'<rect x="88" y="{y - 15}" width="292" height="30" rx="3" fill="{PHOS}" fill-opacity="0.16" stroke="{PHOS}"/>')
    a(text(98 if hot else 92, y + 5, ev, size=14 if hot else 13, fill='#fff' if hot else PHOS_SOFT, ls='0'))
    a('</g>')
    a(f'<circle class="fx" cx="{AX}" cy="{y}" r="11" fill="none" stroke="#fff" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (t + 0.6, 0.0), (D, 0.0)])}</circle>')
a('</svg>')
svg = '\n'.join(o)

caption = ('UNIX began in 1969 as PDP-7 assembly and moved to the PDP-11 still in assembly; in 1973, with C ready, Ritchie and Thompson rewrote the kernel in it. Four years later it ran on an Interdata 8/32, a machine of a different design, carried over largely by recompiling.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why C.</b> B had one type, the machine word. The PDP-11 addressed bytes, so the language needed types; Ritchie added them, and structs, to make C.</li>
          <li><b>The rewrite.</b> The 1973 Fourth Edition was the first UNIX with its kernel mostly in C; a small machine-dependent part stayed in assembly.</li>
          <li><b>The book.</b> Kernighan and Ritchie's <em>The C Programming Language</em> (1978) served as the language's definition until the ANSI standard of 1989.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-2">
      <div class="diagram-label">Fig 5.2 · UNIX's rewrite, in time</div>
      {svg}
      <p id="ch5-bell-labs-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-2', 'ch5-bell-labs-p4', card)
