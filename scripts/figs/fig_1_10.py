# Fig 1.10 · From assembly to binary (Pass 28, law 3). Phone-first, viewBox 400 wide,
# no label under 14 units. Everything is drawn in the still; the motion is a highlight
# that walks the decode in order: what you write, the bytes, the opcode's bits, the value.
W, H = 400, 600
GOLD, BLUE, RED = '#d4a853', '#86a8ff', '#ec8d8d'
MUTED = 'rgba(255,255,255,0.6)'
mono = 'font-family="DM Mono"'
DUR = 8.0
o = []; a = o.append

def glow(x, y, w, h, t0, t1, color=GOLD, rx=6):
    kt = [0, t0 / DUR, (t0 + 0.2) / DUR, (t1 - 0.2) / DUR, t1 / DUR, 1]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{color}" stroke-width="3" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{";".join(f"{k:.4f}" for k in kt)}" dur="{DUR:g}s" repeatCount="indefinite"/></rect>')
def label(x, y, s, anchor='start', size=14, fill=MUTED, extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {mono} font-size="{size}" letter-spacing="0.06em" fill="{fill}"{extra}>{s}</text>'

a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-11 svgd-part1-11">')
a('<title id="svgt-part1-11">Fig 1.10 · From assembly to binary · one instruction decoded</title>')
a('<desc id="svgd-part1-11">mov eax, 5 assembles to five bytes, B8 05 00 00 00. The first byte, B8, is 10111 000 in binary: '
  'the top five bits mean move a 32-bit value into a register, the bottom three name the register, 000 for EAX. '
  'The next four bytes are the value 5, stored lowest byte first; read in reverse they are 00 00 00 05. Result: EAX holds 5.</desc>')

# 1 · what you write
a(label(20, 30, 'YOU WRITE'))
a('<rect x="20" y="42" width="360" height="52" rx="6" fill="#1a1200" stroke="rgba(212,168,83,0.55)"/>')
a(f'<text x="200" y="77" text-anchor="middle" {mono} font-size="24" fill="#fff">mov eax, 5</text>')
a(glow(20, 42, 360, 52, 0.2, 1.4))
# assembler arrow
a('<line x1="200" y1="100" x2="200" y2="128" stroke="rgba(212,168,83,0.6)" stroke-width="1.5"/><polygon points="194,126 200,136 206,126" fill="rgba(212,168,83,0.8)"/>')
a(label(214, 122, 'assembler', size=14, fill='rgba(255,255,255,0.5)', extra=' font-style="italic"'))

# 2 · the bytes the CPU reads
a(label(20, 160, 'IN MEMORY · 5 BYTES'))
bytes_ = ['B8', '05', '00', '00', '00']
for i, b in enumerate(bytes_):
    x = 20 + i * 74
    op = i == 0
    a(f'<rect x="{x}" y="172" width="64" height="56" rx="6" fill="{"rgba(212,168,83,0.28)" if op else "rgba(134,168,255,0.18)"}" stroke="{GOLD if op else BLUE}" stroke-width="1.5"/>')
    a(f'<text x="{x + 32}" y="209" text-anchor="middle" {mono} font-size="24" fill="{GOLD if op else BLUE}">{b}</text>')
    a(glow(x - 3, 169, 70, 62, 1.5 + i * 0.25, 2.3 + i * 0.25, GOLD if op else BLUE))

# 3 · the opcode byte, bit by bit
a('<path d="M 52 232 L 52 258" stroke="rgba(212,168,83,0.6)" stroke-width="1.5"/>')
a(label(66, 254, 'B8, BIT BY BIT', fill='rgba(212,168,83,0.85)'))
bits = '10111000'
for i, bt in enumerate(bits):
    x = 20 + i * 36 + (8 if i >= 5 else 0)
    gold = i < 5
    a(f'<rect x="{x}" y="268" width="32" height="36" rx="3" fill="{"rgba(212,168,83,0.5)" if gold else "rgba(236,141,141,0.42)"}" stroke="{GOLD if gold else RED}"/>')
    a(f'<text x="{x + 16}" y="293" text-anchor="middle" {mono} font-size="18" fill="#0a0a0a" font-weight="500">{bt}</text>')
a('<path d="M 20 312 V 318 H 196 V 312" fill="none" stroke="rgba(212,168,83,0.8)" stroke-width="1.5"/>')
a('<path d="M 208 312 V 318 H 312 V 312" fill="none" stroke="rgba(236,141,141,0.85)" stroke-width="1.5"/>')
a(label(108, 342, 'MOV', anchor='middle', size=18, fill=GOLD))
a(label(108, 362, 'a value into', anchor='middle', fill=MUTED))
a(label(108, 380, 'a register', anchor='middle', fill=MUTED))
a(label(260, 342, 'EAX', anchor='middle', size=18, fill=RED))
a(label(260, 362, 'register 000', anchor='middle', fill=MUTED))
a(glow(16, 264, 186, 44, 3.0, 4.0))
a(glow(204, 264, 112, 44, 3.4, 4.4, RED))

# 4 · the value, stored lowest byte first
a(label(20, 414, 'THE VALUE · LOW BYTE FIRST'))
xs_stored = [20 + i * 62 for i in range(4)]      # 05 00 00 00 as stored
xs_read = [20 + i * 62 for i in range(4)]        # 00 00 00 05 as a number
for i, b in enumerate(['05', '00', '00', '00']):
    a(f'<rect x="{xs_stored[i]}" y="426" width="54" height="36" rx="4" fill="rgba(134,168,255,0.18)" stroke="{BLUE}"/>')
    a(f'<text x="{xs_stored[i] + 27}" y="451" text-anchor="middle" {mono} font-size="18" fill="{BLUE}">{b}</text>')
for i in range(4):                                # each byte to its mirrored place
    x1 = xs_stored[i] + 27; x2 = xs_read[3 - i] + 27
    a(f'<line x1="{x1}" y1="464" x2="{x2}" y2="500" stroke="rgba(134,168,255,0.55)" stroke-width="1.5"/>')
for i, b in enumerate(['00', '00', '00', '05']):
    a(f'<rect x="{xs_read[i]}" y="502" width="54" height="36" rx="4" fill="rgba(134,168,255,0.3)" stroke="{BLUE}"/>')
    a(f'<text x="{xs_read[i] + 27}" y="527" text-anchor="middle" {mono} font-size="18" fill="#fff">{b}</text>')
a(f'<text x="284" y="529" {mono} font-size="24" fill="{BLUE}">= 5</text>')
a(glow(16, 422, 250, 120, 4.5, 5.6, BLUE))

# 5 · the result
a(f'<text x="200" y="584" text-anchor="middle" {mono} font-size="22" fill="#fff">EAX <tspan fill="{GOLD}">←</tspan> 5</text>')
a(glow(120, 558, 160, 38, 5.7, 7.4))
a('</svg>')
svg = '\n'.join(o)

caption = ('One instruction as the CPU sees it: the first byte says what to do and to which register, '
           'the next four hold the value, lowest byte first.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Opcode.</b> B8 is 10111 000. The top five bits mean “move a 32-bit value into a register”; the bottom three name the register, and 000 is EAX.</li>
          <li><b>Value.</b> x86 is little-endian: it stores the lowest byte first, so 5 sits in memory as 05&nbsp;00&nbsp;00&nbsp;00.</li>
          <li><b>Decode.</b> The decoder is a circuit that recognises these bit patterns and routes them to the right units; nothing is looked up by name.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-10">
      <div class="diagram-label">Fig 1.10 · From assembly to binary · one instruction decoded</div>
      {svg}
      <p id="ch1-cpu-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    from figlib import splice
    splice('part-1', 'fig-1-10', 'ch1-cpu-p6', card)
    raise SystemExit

    import re
    p = '/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html'
    s = open(p).read()
    m = re.search(r'<div class="diagram-card[^"]*" id="fig-1-10">[\s\S]*?</svg>\s*<p id="ch1-cpu-p6"[\s\S]*?</p>\s*(?:<details class="fig-how">[\s\S]*?</details>\s*)?</div>', s)
    assert m, 'fig-1-10 not found'
    s = s[:m.start()] + card + s[m.end():]
    open(p, 'w').write(s); print('fig 1.10 written', len(svg), 'bytes svg')
