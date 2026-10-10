# Fig 3.3 · One register, four names (Pass 28, law 3). RAX's eight bytes with EAX, AX, AH, AL
# nested inside. Two real instructions: mov al, 0xFF changes only the lowest byte; mov eax, 1
# clears the whole upper half (x86-64 zero-extends 32-bit writes). Below, the sixteen names by era.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 404
X0, BW = 20, 45
STATES = [('', ['11', '22', '33', '44', '55', '66', '77', '88']),
          ('mov al, 0xFF', ['11', '22', '33', '44', '55', '66', '77', 'FF']),
          ('mov eax, 1', ['00', '00', '00', '00', '00', '00', '00', '01'])]
SPANS = [(0.0, 1.4), (1.4, 4.6), (4.6, 8.6)]
T = Timeline(9, shift=3.0)
def win(t0, t1):
    if t0 <= 0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.6, 0.0), (8.601, 1.0), (9.0, 1.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (9.0, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-31 svgd-part1-31">')
a('<title id="svgt-part1-31">Fig 3.3 · The x86-64 register file · one register, four names</title>')
a('<desc id="svgd-part1-31">RAX holds eight bytes. Its lower four bytes are also called EAX (1985), the lower two AX (1978), and those two bytes AH and AL. '
  'Starting from 11 22 33 44 55 66 77 88, mov al, 0xFF changes only the lowest byte. mov eax, 1 writes the lower half and clears the upper half too: 00 00 00 00 00 00 00 01. '
  'Below, the sixteen general-purpose registers: eight 8086 names widened twice, and eight added by AMD64 in 2003.</desc>')
a(text(20, 22, 'RAX · 64 BITS · 2003', size=13, fill=MUTED))
for k, (ins, bytes_) in enumerate(STATES):
    t0, t1 = SPANS[k]
    g = [f'<g opacity="0">{win(t0, t1)}']
    for i, b in enumerate(bytes_):
        changed = k > 0 and b != STATES[k - 1][1][i]
        g.append(f'<rect x="{X0 + i * BW}" y="32" width="{BW - 3}" height="34" rx="3" fill="{GOLD if changed else BLUE}" fill-opacity="{0.35 if changed else 0.15}" stroke="{GOLD if changed else BLUE}" stroke-opacity="0.8"/>'
                 f'<text x="{X0 + i * BW + (BW - 3) / 2}" y="55" text-anchor="middle" {MONO} font-size="16" fill="#fff">{b}</text>')
    if ins:
        g.append(f'<text x="200" y="196" text-anchor="middle" {MONO} font-size="17" fill="{GOLD}">{ins}</text>')
    g.append('</g>'); a(''.join(g))
# the nested names, as brackets under the bytes
def bracket(i0, i1, y, label, col):
    x0, x1 = X0 + i0 * BW, X0 + i1 * BW - 3
    a(f'<path d="M {x0} {y - 8} V {y} H {x1} V {y - 8}" fill="none" stroke="{col}" stroke-width="1.5"/>')
    a(text((x0 + x1) / 2, y + 17, label, anchor='middle', size=14, fill=col, ls='0'))
bracket(0, 8, 82, 'RAX', BLUE)
bracket(4, 8, 112, 'EAX · 1985', BLUE)
bracket(6, 8, 142, 'AX · 1978', BLUE)
bracket(6, 7, 172, 'AH', 'rgba(134,168,255,0.8)')
bracket(7, 8, 172, 'AL', 'rgba(134,168,255,0.8)')
a(text(20, 196, 'write:', size=13, fill=MUTED))
# the sixteen
a(text(20, 232, 'THE SIXTEEN', size=13, fill=MUTED))
OLD = ['RAX', 'RBX', 'RCX', 'RDX', 'RSI', 'RDI', 'RBP', 'RSP']
NEW = [f'R{i}' for i in range(8, 16)]
for k, name in enumerate(OLD + NEW):
    r, c = divmod(k, 4)
    x, y = 20 + c * 92, 242 + r * 32
    col = BLUE if k < 8 else GREEN
    a(f'<rect x="{x}" y="{y}" width="86" height="27" rx="4" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(x + 43, y + 19, name, anchor='middle', size=14, fill='#fff', ls='0'))
a(f'<rect x="20" y="380" width="14" height="14" rx="2" fill="{BLUE}" fill-opacity="0.4" stroke="{BLUE}"/>')
a(text(40, 392, '8086 names, widened', size=13, fill=MUTED))
a(f'<rect x="210" y="380" width="14" height="14" rx="2" fill="{GREEN}" fill-opacity="0.4" stroke="{GREEN}"/>')
a(text(230, 392, 'added by AMD64', size=13, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('One register, four names: RAX (2003) contains EAX (1985), which contains AX (1978), split into AH and AL. '
           'Writing AL changes only that byte; writing EAX also clears the upper half, a rule of x86-64.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The names.</b> The 8086 had 16-bit AX, BX, CX, DX; 32-bit chips added an E for extended; AMD64 replaced it with R and added R8 to R15.</li>
          <li><b>The quirk.</b> 8- and 16-bit writes leave the rest of the register alone; 32-bit writes zero the top 32 bits.</li>
          <li><b>Two more.</b> RIP, the instruction pointer, and RFLAGS, the condition codes set by every arithmetic operation, are not general-purpose.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-3-3">
      <div class="diagram-label">Fig 3.3 · The x86-64 register file · one register, four names</div>
      {svg}
      <p id="ch3-registers-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-3-3', 'ch3-registers-p3', card)
