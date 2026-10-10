# Fig BR.1 · The privilege bit (Pass 28, law 3). Two lanes run the same three instructions:
# Ring 0 (CPL = 0) and Ring 3 (CPL = 3). Ordinary add runs in both; mov cr3 and hlt run in Ring 0
# and raise #GP in Ring 3, which hands control to the kernel's handler. t=0: all rows done.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 334
T = Timeline(8, shift=7.2)
def show(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (7.8, 1.0), (7.801, 0.0), (7.9995, 0.0)])
INS = [('add rax, rbx', False), ('mov cr3, rax', True), ('hlt', True)]
LANES = [(20, 'RING 0 · KERNEL', '00', GOLD, 0), (210, 'RING 3 · USER', '11', BLUE, 3)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-39 svgd-part1-39">')
a('<title id="svgt-part1-39">Fig BR.1 · The privilege bit · two worlds, one chip</title>')
a('<desc id="svgd-part1-39">The low two bits of the CS register hold the current privilege level: 00 in Ring 0, the kernel, and 11 in Ring 3, user programs. '
  'Both run the same three instructions. add runs in both. mov cr3, which changes the page tables, and hlt, which halts the processor, run in Ring 0; '
  'in Ring 3 the CPU stops each before it takes effect with a general-protection fault, #GP, and jumps to a handler the kernel registered in advance.</desc>')
for x, name, bits, col, cpl in LANES:
    a(f'<rect x="{x}" y="14" width="170" height="250" rx="8" fill="{col}" fill-opacity="0.05" stroke="{col}" stroke-opacity="0.45"/>')
    a(text(x + 12, 36, name, size=13, fill=col))
    a(text(x + 12, 64, 'CS bits 1–0', size=13, fill=MUTED, ls='0'))
    for k, b in enumerate(bits):
        a(f'<rect x="{x + 112 + k * 24}" y="48" width="22" height="24" rx="3" fill="{col}" fill-opacity="0.3" stroke="{col}"/>'
          f'<text x="{x + 123 + k * 24}" y="66" text-anchor="middle" {MONO} font-size="15" fill="#fff">{b}</text>')
    for i, (ins, priv) in enumerate(INS):
        y = 92 + i * 56
        t0 = 0.6 + i * 1.6
        ok = not (priv and cpl == 3)
        a(f'<rect x="{x + 10}" y="{y}" width="150" height="40" rx="5" fill="#151515" stroke="rgba(255,255,255,0.2)"/>')
        a(text(x + 20, y + 25, ins, size=13, fill='#fff', ls='0'))
        a(f'<rect class="fx" x="{x + 8}" y="{y - 2}" width="154" height="44" rx="6" fill="none" stroke="{GREEN if ok else RED}" stroke-width="2" opacity="0">'
          f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t0 + 0.9, 1.0), (t0 + 0.901, 0.0), (7.9995, 0.0)])}</rect>')
        mark = '✓' if ok else '#GP'
        a(f'<text x="{x + 150}" y="{y + 25}" text-anchor="end" {MONO} font-size="13" fill="{GREEN if ok else RED}" opacity="0">{mark}{show(t0 + 0.3)}</text>')
# the trap: from Ring 3 into the kernel's handler
a(f'<rect x="20" y="282" width="360" height="44" rx="6" fill="#1d1810" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(text(34, 309, 'kernel handler, registered at boot', size=14, fill=GOLD, ls='0'))
for i in (1, 2):
    y = 92 + i * 56 + 20
    t0 = 0.6 + i * 1.6 + 0.3
    a(f'<path d="M 380 {y} H 392 V 304 H 382" fill="none" stroke="{RED}" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t0 + 1.0, 1.0), (t0 + 1.2, 0.35), (7.8, 0.35), (7.801, 0.0), (7.9995, 0.0)])}</path>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Two bits in the CS register say which world the CPU is in: Ring 0 for the kernel, Ring 3 for everything else. '
           'In Ring 3 about thirty privileged instructions are refused by the silicon itself, which jumps to the kernel instead.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>CPL.</b> The current privilege level, held in the low two bits of CS: 00 for the kernel, 11 for user programs.</li>
          <li><b>Privileged.</b> Instructions that would let a program step past the operating system: loading the page tables (mov cr3), the interrupt table (lidt), model-specific registers, I/O ports, halting the CPU.</li>
          <li><b>#GP.</b> A general-protection fault. The instruction does not run and no error code comes back; the CPU jumps to the handler the kernel set up, and the kernel decides what happens to the program.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-1">
      <div class="diagram-label">Fig BR.1 · The privilege bit · two worlds, one chip</div>
      {svg}
      <p id="chBridge-mode-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-1', 'chBridge-mode-p5', card)
