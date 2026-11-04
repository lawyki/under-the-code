# Fig BR.2 · The trap mechanism (Pass 31, Part I, from an empty script). Job: function. Takeaway: SYSCALL jumps to an
# address the kernel chose, so a program picks the service, never the destination.
# Concept: the round trip as one journey across a wall, time running down: the program (Ring 3) on the left, the kernel
# (Ring 0) on the right. A dot (Part I's flow verb) follows the CPU: the program puts the service number in RAX and runs
# syscall; the CPU saves where to come back and jumps to the one entry the kernel stored in MSR_LSTAR; the kernel looks
# the number up, runs write, puts the result in RAX and runs sysret, back to the next instruction. The registers that
# carry the trip sit below. t=0 is the trip done: RAX holds 6.
from figlib import Timeline, text, splice, GOLD, BLUE, GREEN, MUTED

W, H = 400, 376
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 11.0
T = Timeline(D, shift=9.6)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-br-2 svgd-part1-br-2"{T.steps([(2.4, 'syscall'), (5.0, 'kernel'), (7.4, 'sysret'), (9.6, 'back')])}>')
a('<title id="svgt-part1-br-2">Fig BR.2 · The trap mechanism · one round trip across the boundary</title>')
a('<desc id="svgd-part1-br-2">A write system call, step by step, time flowing down. In user mode, Ring 3, the program puts 1, the number of '
  'write, in RAX and executes SYSCALL. The CPU saves RIP, the return address, in RCX and RFLAGS, its status bits, in R11 (a spare '
  'register), switches to Ring 0 and jumps to the entry point the kernel stored in MSR_LSTAR. The kernel looks up entry 1 in its '
  'syscall table, runs write, puts the result, 6 bytes written, in RAX, and executes SYSRET, which restores user mode at the next '
  'instruction. The program chose the service number, never where the CPU jumped.</desc>')

a(text(20, 26, 'program · Ring 3', size=14, fill=BLUE))
a(text(216, 26, 'kernel · Ring 0', size=14, fill=GOLD))
a(f'<line x1="200" y1="14" x2="200" y2="284" stroke="{GOLD}" stroke-width="2" stroke-dasharray="6 5"/>')
def box(x, y, w, label, col, sub=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="5" fill="none" stroke="{col}" stroke-width="1.5"/>')
    a(text(x + 10, y + 20, label, size=14, fill=INK, ls='0'))
BL = [(42, 'mov rax, 1'), (82, 'syscall'), (250, 'next instruction')]
BR = [(116, 'entry: MSR_LSTAR'), (152, 'table[1]: write'), (188, 'write runs'), (224, 'sysret')]
for y, s in BL: box(18, y, 166, s, BLUE)
for y, s in BR: box(216, y, 166, s, GOLD)
a(text(222, 108, 'set by the kernel', size=14, fill=MUTED))
# the two crossings
a(f'<path d="M 184 97 C 200 97 200 131 214 131" fill="none" stroke="{EDGE}" stroke-width="1.6"/>')
a(f'<path d="M 216 239 C 200 239 200 265 186 265" fill="none" stroke="{EDGE}" stroke-width="1.6"/>')

# the dot: the CPU's path through the trip
PATH = [(0.4, 101, 57), (1.6, 101, 57), (2.0, 101, 97), (2.8, 101, 97), (3.4, 299, 131), (4.2, 299, 131), (4.6, 299, 167),
        (5.4, 299, 167), (5.8, 299, 203), (6.6, 299, 203), (7.0, 299, 239), (7.8, 299, 239), (8.4, 101, 265), (D - 0.01, 101, 265)]
xs = [(0.0, 0)] + [(t, x - 101) for t, x, _ in PATH]
ys = [(0.0, 0)] + [(t, y - 57) for t, _, y in PATH]
a(f'<g opacity="0">{vis([(0.4, D)])}<g>{T.translate(xs, axis="x")}<g>{T.translate(ys, axis="y")}'
  f'<circle cx="101" cy="57" r="7" fill="none" stroke="{GOLD}" stroke-width="2.4"/></g></g></g>')

# the registers that carry it
RY = 300
REGS = [(18, 'RAX'), (146, 'RCX'), (274, 'R11')]
for x, name in REGS:
    a(f'<rect x="{x}" y="{RY}" width="108" height="56" rx="6" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
    a(text(x + 10, RY + 20, name, size=14, fill=GREEN, ls='0'))
def rv(x, s, spans, col=INK):
    a(f'<text data-role="object" x="{x + 10}" y="{RY + 44}" font-family="DM Mono" font-size="14" fill="{col}" opacity="0">{vis(spans)}{s}</text>')
rv(18, '1 · write', [(1.0, 6.4)]); rv(18, '6 · bytes', [(6.4, D)], GOLD)
rv(146, 'return addr', [(2.8, 8.4)]); rv(274, 'status bits', [(2.8, 8.4)])
rv(146, 'restored', [(8.4, D)], MUTED); rv(274, 'restored', [(8.4, D)], MUTED)
for x, _ in REGS[1:]:
    a(f'<rect x="{x}" y="{RY}" width="108" height="56" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{vis([(2.8, 3.6), (7.8, 8.6)])}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One <code>write</code> system call, time running down: the program in Ring 3 on the left, the kernel in Ring 0 on the '
           'right, and below them the registers that carry the request and the way back. The round trip typically takes under a microsecond.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The number.</b> RAX names the call (1 is write on x86-64 Linux); the arguments sit in RDI, RSI, RDX, R10, R8 and R9: Fig 3.4's order, with R10 in place of RCX, which <code>SYSCALL</code> overwrites.</li>
          <li><b>SYSCALL.</b> In one instruction the CPU saves RIP in RCX and RFLAGS in R11, sets CPL to 0, masks interrupts, and loads RIP from MSR_LSTAR, a register only the kernel can set.</li>
          <li><b>Dispatch.</b> The entry stub indexes the syscall table with RAX and runs that handler; the result comes back in RAX.</li>
          <li><b>SYSRET.</b> Restores RIP and RFLAGS from RCX and R11 and drops back to Ring 3. No scheduling is involved.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-2">
      <div class="diagram-label">Fig BR.2 · The trap mechanism · one round trip across the boundary</div>
      {svg}
      <p id="chBridge-trap-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-2', 'chBridge-trap-p3', card)
