# Fig 1.9 · The instruction cycle (Pass 28, law 3). Four stages on a ring; a packet goes
# round once per instruction. In the middle, the program counter and the instruction:
# mov eax, 5 (0x00, 5 bytes) · add eax, 3 (0x05, 3 bytes) · jmp 0x00 (0x08): the PC
# advances by each instruction's length, and the jump sends it back to the start.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 430
C, R = (200, 200), 120
CYC, N = 2.4, 3
T = Timeline(CYC * N, shift=0.0)
STAGES = [('Fetch', 'from memory', (200, 80)), ('Decode', 'what to do', (320, 200)),
          ('Execute', 'do it', (200, 320)), ('Writeback', 'store, move PC', (80, 200))]
PROG = [('0x00', 'mov eax, 5'), ('0x05', 'add eax, 3'), ('0x08', 'jmp 0x00')]
D = CYC * N
def window(t0, t1):           # on from t0 to t1 (snap), off otherwise
    end = D - 0.0005               # the loop's end must not land on its start (they are the same instant)
    # off a moment before the next one comes on, so two never show at once
    if t0 <= 0: return T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (end, 0.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (min(t1, end) - 0.002, 1.0), (min(t1, end) - 0.001, 0.0), (end, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-10 svgd-part1-10">')
a('<title id="svgt-part1-10">Fig 1.9 · The instruction cycle · fetch, decode, execute, writeback</title>')
a('<desc id="svgd-part1-10">Four stages on a ring: fetch, decode, execute, writeback. One instruction goes round per cycle. '
  'In the middle the program counter and the instruction: mov eax, 5 at 0x00, add eax, 3 at 0x05, jmp 0x00 at 0x08, which sends the counter back to 0x00.</desc>')
# the ring and the packet going round it (under the stage boxes); it starts 45 degrees back,
# so it sits on each stage in the middle of that stage's turn
a(f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="rgba(212,168,83,0.3)" stroke-width="2"/>')
for ang in (45, 135, 225, 315):   # direction arrows on the ring, clockwise
    import math
    r = math.radians(ang - 90); x, y = C[0] + R * math.cos(r), C[1] + R * math.sin(r)
    a(f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang})"><polygon points="-5,-5 6,0 -5,5" fill="rgba(212,168,83,0.6)"/></g>')
a(f'<g><animateTransform attributeName="transform" type="rotate" values="-45 {C[0]} {C[1]};315 {C[0]} {C[1]}" dur="{CYC}s" repeatCount="indefinite"/>'
  f'<circle cx="{C[0]}" cy="{C[1] - R}" r="8" fill="{GOLD}" stroke="#0e0e0e" stroke-width="2"/></g>')
# the stages; each lights while the instruction is in it
for k, (name, sub, (x, y)) in enumerate(STAGES):
    w = 124
    a(f'<rect x="{x - w / 2:g}" y="{y - 28}" width="{w}" height="56" rx="8" fill="#171717" stroke="rgba(255,255,255,0.3)"/>')
    pts = []
    for c in range(N):
        t0 = c * CYC + k * CYC / 4
        pts.append((t0, t0 + CYC / 4))
    for t0, t1 in pts:
        a(f'<rect x="{x - w / 2:g}" y="{y - 28}" width="{w}" height="56" rx="8" fill="{GOLD}" fill-opacity="0.16" stroke="{GOLD}" stroke-width="2" opacity="0">{window(t0, t1)}</rect>')
    a(text(x, y - 3, name, anchor='middle', size=17, fill='#fff', ls='0'))
    a(text(x, y + 17, sub, anchor='middle', size=13, fill=MUTED, ls='0'))
# the program counter and the instruction in flight
a(text(200, 168, 'PC', anchor='middle', size=13, fill=MUTED))
for c, (pc, ins) in enumerate(PROG):
    t0, t1 = c * CYC, (c + 1) * CYC
    a(f'<text x="200" y="192" text-anchor="middle" {MONO} font-size="18" fill="{BLUE}" opacity="0">{pc}{window(t0, t1)}</text>')
    a(f'<text x="200" y="226" text-anchor="middle" {MONO} font-size="16" fill="#fff" opacity="0">{ins}{window(t0, t1)}</text>')
# the program, all of it, with the current line marked
a(text(20, 368, 'THE PROGRAM', size=13, fill=MUTED))
for c, (pc, ins) in enumerate(PROG):
    x = 20 + c * 124
    a(f'<rect x="{x}" y="380" width="116" height="40" rx="5" fill="#141414" stroke="rgba(255,255,255,0.2)"/>')
    a(f'<rect x="{x}" y="380" width="116" height="40" rx="5" fill="none" stroke="{GOLD}" stroke-width="1.8" opacity="0">{window(c * CYC, (c + 1) * CYC)}</rect>')
    a(text(x + 8, 396, pc, size=13, fill=BLUE, ls='0'))
    a(text(x + 8, 413, ins, size=13, fill='#fff', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('Every core runs this loop: fetch the instruction the program counter names, decode it, execute it, write back the result, '
           'and move the counter on, billions of times a second.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Fetch.</b> Read the bytes at the address in the program counter.</li>
          <li><b>Decode.</b> Work out the operation and its operands from the bit pattern (Fig 1.10 takes one apart).</li>
          <li><b>Execute.</b> The ALU or another unit does the work: an addition, a comparison, an address.</li>
          <li><b>Writeback.</b> Store the result and move the counter on by the instruction's length: 5 bytes, then 3. A jump sets the counter instead, which is how this program loops.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-9">
      <div class="diagram-label">Fig 1.9 · The instruction cycle · fetch, decode, execute, writeback</div>
      {svg}
      <p id="ch1-cpu-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-9', 'ch1-cpu-p3', card)
