# Fig 5.3 · PDP-7 to PDP-11 (Pass 28, law 3). The difference that shaped C: on the PDP-7 an address
# names an 18-bit word holding two characters; on the PDP-11 every byte has its own address. A
# pointer steps through "UNIX" on each: by word on the PDP-7; by 1 for char* and by 2 for int* on the
# PDP-11, which is why C's pointers needed types. t=0: all pointers at their start, both machines drawn.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 390
D = 9.0
T = Timeline(D, shift=0.0)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-27 svgd-part2-27">')
a('<title id="svgt-part2-27">Fig 5.3 · PDP-7 to PDP-11 · the machines that shaped C</title>')
a('<desc id="svgd-part2-27">The string UNIX in the memory of two machines. On the PDP-7 of 1964, memory is 18-bit words and an address names a whole word: "UN" sits in word 100 and "IX" in word 101, and a pointer steps a word at a time. '
  'On the PDP-11 of 1970, words are 16 bits but every byte has its own address: U, N, I and X sit at 1000 to 1003. A char pointer steps by 1 byte, an int pointer by 2. '
  'Pointer arithmetic that depends on what is pointed at is why C gave its pointers types.</desc>')
def panel(y, title, spec):
    a(text(20, y, title, size=14, fill=PHOS, ls='0'))
    a(text(20, y + 20, spec, size=13, fill=MUTED, ls='0'))
def pointer(label, xs, y, col, times, above=True):
    # a stepping marker: positions xs at story times
    pts = []
    for i, (x, t) in enumerate(zip(xs, times)):
        if i == 0: pts.append((0.0, x))
        else: pts += [(t - 0.2, xs[i - 1]), (t, x)]
    pts.append((D, xs[-1]))
    # back to the start at the loop's end
    pts = [(0.0, xs[0])] + [p for p in pts[1:]]
    back = [(D - 0.6, xs[-1]), (D - 0.3, xs[0]), (D, xs[0])]
    pts = [p for p in pts if p[0] < D - 0.6] + back
    if above:
        g = f'<polygon points="-6,{y - 18} 6,{y - 18} 0,{y - 6}" fill="{col}"/>' + text(0, y - 24, label, anchor='middle', size=13, fill=col, ls='0')
    else:   # below the cells, pointing up
        g = f'<polygon points="-6,{y + 10} 6,{y + 10} 0,{y}" fill="{col}"/>' + text(0, y + 28, label, anchor='middle', size=13, fill=col, ls='0')
    a(f'<g>{T.translate(pts, "x")}{g}</g>')
# PDP-7
panel(22, 'PDP-7 · 1964', '18-bit words; an address names a word')
WY = 82
for k, (addr, chars) in enumerate(((100, 'U N'), (101, 'I X'))):
    x = 60 + k * 140
    a(f'<rect x="{x}" y="{WY}" width="136" height="34" rx="2" fill="{PANEL}" stroke="{GOLD}" stroke-opacity="0.8"/>')
    a(text(x + 68, WY + 23, chars, anchor='middle', size=16, fill='#fff', ls='0.2em'))
    a(f'<line x1="{x + 68}" y1="{WY + 6}" x2="{x + 68}" y2="{WY + 28}" stroke="rgba(212,168,83,0.35)" stroke-dasharray="2 2"/>')
    a(text(x + 68, WY + 54, str(addr), anchor='middle', size=13, fill=GOLD, ls='0'))
pointer('p', [128, 268], WY, GOLD, [0.0, 2.0])
# PDP-11
panel(174, 'PDP-11 · 1970', '16-bit words; every byte has an address')
BY = 244
for k, ch in enumerate('UNIX'):
    x = 60 + k * 70
    a(f'<rect x="{x}" y="{BY}" width="68" height="34" rx="2" fill="{PANEL}" stroke="{PHOS}" stroke-opacity="0.7"/>')
    a(text(x + 34, BY + 23, ch, anchor='middle', size=16, fill='#fff', ls='0'))
    a(text(x + 34, BY + 54, str(1000 + k), anchor='middle', size=13, fill=PHOS_SOFT, ls='0'))
for k in range(2):  # the 16-bit words: pairs of bytes
    a(f'<rect x="{58 + k * 140}" y="{BY - 3}" width="140" height="40" rx="3" fill="none" stroke="rgba(198,222,206,0.3)" stroke-dasharray="3 3"/>')
pointer('char *c', [94, 164, 234, 304], BY, PHOS, [0.0, 3.4, 4.6, 5.8])
pointer('int *i', [94, 234], BY + 64, BLUE, [0.0, 4.6], above=False)
a(text(380, BY + 118, 'c + 1: next byte', anchor='end', size=13, fill=PHOS_SOFT, ls='0'))
a(text(380, BY + 136, 'i + 1: next word', anchor='end', size=13, fill=BLUE, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('On the PDP-7 an address named a whole 18-bit word, two characters at a time; on the PDP-11 every byte had its own address. A pointer to a character must then step by 1 and a pointer to an integer by 2, which is why C, unlike B, gave its pointers types.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The PDP-7.</b> Bell Labs' machine had 8K words of 18 bits. B, its language, had a single type, the word; reaching one character meant shifting and masking.</li>
          <li><b>The PDP-11.</b> A 16-bit design with byte addresses, eight registers and regular addressing modes. Its bytes are what forced types into the language.</li>
          <li><b>The legacy.</b> Flat byte-addressed memory and pointers that scale by the size of what they point at are C's model, and nearly every processor since provides it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-3">
      <div class="diagram-label">Fig 5.3 · PDP-7 to PDP-11 · the machines that shaped C</div>
      {svg}
      <p id="ch5-bell-labs-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-3', 'ch5-bell-labs-p8', card)
