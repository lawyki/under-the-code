# Fig BR.2 · The trap (Pass 28, law 3). One write(1, "hello\n", 6) as a sequence, time flowing down:
# user steps on the left, kernel steps on the right, the boundary between. SYSCALL saves RIP in RCX
# and RFLAGS in R11, sets CPL 0 and jumps to MSR_LSTAR; the kernel dispatches on RAX (1 = write on
# x86-64 Linux), puts the result in RAX, and SYSRET returns. t=0: the round trip complete.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, MUTED

W, H = 400, 452
T = Timeline(9, shift=8.2)
UX, KX, CW = 20, 214, 166
ROWS = [('u', 'mov rax, 1'), ('u', 'syscall'), ('k', 'entry · MSR_LSTAR'), ('k', 'table[1] → write'), ('k', 'write; rax = 6'), ('k', 'sysret'), ('u', 'next instruction')]
row_y = lambda i: 48 + i * 40
def show(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (8.8, 1.0), (8.801, 0.0), (8.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-40 svgd-part1-40">')
a('<title id="svgt-part1-40">Fig BR.2 · The trap mechanism · one round trip across the boundary</title>')
a('<desc id="svgd-part1-40">A write system call, step by step, time flowing down. In user mode the program puts 1, the number of write, in RAX and executes SYSCALL. '
  'The CPU saves RIP in RCX and RFLAGS in R11, switches to Ring 0 and jumps to the entry point the kernel stored in MSR_LSTAR. '
  'The kernel looks up entry 1 in its syscall table, runs write, puts the result, 6 bytes written, in RAX, and executes SYSRET, which restores user mode at the next instruction.</desc>')
a(text(UX, 24, 'USER · RING 3', size=13, fill=BLUE))
a(text(KX, 24, 'KERNEL · RING 0', size=13, fill=GOLD))
a(f'<line x1="200" y1="32" x2="200" y2="{row_y(6) + 34}" stroke="{GOLD}" stroke-width="2" stroke-dasharray="6 5"/>')
times = []
for i, (side, lab) in enumerate(ROWS):
    x = UX if side == 'u' else KX
    col = BLUE if side == 'u' else GOLD
    y = row_y(i)
    t0 = 0.4 + i * 1.05
    times.append(t0)
    a(f'<rect x="{x}" y="{y}" width="{CW}" height="32" rx="5" fill="{col}" fill-opacity="0.1" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(x + 12, y + 21, lab, size=14, fill='#fff', ls='0'))
    a(f'<rect class="fx" x="{x - 2}" y="{y - 2}" width="{CW + 4}" height="36" rx="6" fill="none" stroke="#fff" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t0 + 1.0, 1.0), (t0 + 1.001, 0.0), (8.9995, 0.0)])}</rect>')
# the two crossings
a(f'<path d="M {UX + CW} {row_y(1) + 16} C 200 {row_y(1) + 16} 200 {row_y(2) + 16} {KX} {row_y(2) + 16}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
  f'<polygon points="{KX},{row_y(2) + 16} {KX - 8},{row_y(2) + 11} {KX - 8},{row_y(2) + 21}" fill="{GOLD}"/>')
a(f'<path d="M {KX} {row_y(5) + 16} C 200 {row_y(5) + 16} 200 {row_y(6) + 16} {UX + CW} {row_y(6) + 16}" fill="none" stroke="{BLUE}" stroke-width="2"/>'
  f'<polygon points="{UX + CW},{row_y(6) + 16} {UX + CW + 8},{row_y(6) + 11} {UX + CW + 8},{row_y(6) + 21}" fill="{BLUE}"/>')
# registers: what the CPU saved and what RAX means
RY = row_y(7) + 20
a(text(UX, RY, 'REGISTERS', size=13, fill=MUTED))
REG = [('RAX', [('1 · write', times[0], times[4]), ('6 · bytes written', times[4], 8.8)]),
       ('RCX', [('saved RIP', times[1] + 0.3, 8.8)]), ('R11', [('saved RFLAGS', times[1] + 0.3, 8.8)])]
for k, (name, vals) in enumerate(REG):
    y = RY + 14 + k * 30
    a(f'<rect x="{UX}" y="{y}" width="360" height="26" rx="4" fill="#141414" stroke="rgba(255,255,255,0.18)"/>')
    a(text(UX + 12, y + 18, name, size=14, fill=GREEN, ls='0'))
    for lab, t0, t1 in vals:
        a(f'<text x="{UX + 70}" y="{y + 18}" {MONO} font-size="14" fill="#fff" opacity="0">{lab}'
          f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.9995, 0.0)])}</text>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One system call, start to finish: the program names the call in RAX and executes SYSCALL; the CPU saves where it was, switches to Ring 0 and jumps to the entry point the kernel registered. '
           'The kernel does the work and SYSRET brings it back, typically in under a microsecond.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The number.</b> RAX names the call (1 is write on x86-64 Linux); the arguments sit in the ABI registers.</li>
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
