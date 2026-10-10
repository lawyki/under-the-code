# Fig 1.14 · Protection rings (Pass 28, law 3). User programs (Ring 3) over the kernel (Ring 0)
# over the hardware. Act 1: a program reaches straight for the disk and the CPU stops it at the
# boundary. Act 2: it asks with a system call; the kernel does the work and returns.
# Both routes are drawn in the still; the motion runs them.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 352
T = Timeline(9, shift=8.4)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.999, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-15 svgd-part1-15">')
a('<title id="svgt-part1-15">Fig 1.14 · Protection rings · user programs, the kernel, the hardware</title>')
a('<desc id="svgd-part1-15">Three layers: user programs in Ring 3, the kernel in Ring 0, the hardware below. A program that reaches straight for the disk is stopped at the boundary by the CPU. '
  'The same request made as a system call traps into the kernel, which drives the disk and returns the result to the program.</desc>')
# bands
a(f'<rect x="10" y="12" width="380" height="112" rx="8" fill="rgba(134,168,255,0.06)" stroke="rgba(134,168,255,0.35)"/>')
a(text(22, 34, 'USER PROGRAMS · RING 3', size=13, fill='rgba(134,168,255,0.9)'))
a(f'<rect x="10" y="148" width="380" height="92" rx="8" fill="rgba(212,168,83,0.08)" stroke="rgba(212,168,83,0.5)"/>')
a(text(378, 170, 'KERNEL · RING 0', anchor='end', size=13, fill=GOLD))
a(f'<rect x="10" y="256" width="380" height="88" rx="8" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.25)"/>')
a(text(22, 278, 'HARDWARE', size=13, fill=MUTED))
# the boundary, enforced by the CPU
a(f'<line x1="10" y1="136" x2="390" y2="136" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="7 5"/>')
# programs
a(f'<rect x="22" y="46" width="168" height="44" rx="6" fill="#18202e" stroke="{BLUE}"/>')
a(text(106, 74, 'your program', anchor='middle', size=15, fill='#fff', ls='0'))
for x, name in ((202, 'browser'), (298, 'editor')):
    a(f'<rect x="{x}" y="46" width="88" height="44" rx="6" fill="#141414" stroke="rgba(255,255,255,0.2)"/>')
    a(text(x + 44, 73, name, anchor='middle', size=14, fill=MUTED, ls='0'))
# kernel parts and hardware
a(f'<rect x="110" y="184" width="98" height="40" rx="5" fill="#1d1810" stroke="rgba(212,168,83,0.6)"/>')
a(text(159, 209, 'driver', anchor='middle', size=14, fill='#f3e7cc', ls='0'))
a(f'<rect x="222" y="184" width="110" height="40" rx="5" fill="#1d1810" stroke="rgba(212,168,83,0.35)"/>')
a(text(277, 209, 'scheduler', anchor='middle', size=14, fill='rgba(243,231,204,0.6)', ls='0'))
for x, name, hi in ((110, 'disk', True), (222, 'network', False), (318, 'RAM', False)):
    w = 98 if name == 'disk' else (84 if name == 'network' else 64)
    a(f'<rect x="{x}" y="290" width="{w}" height="40" rx="5" fill="#1a1a1a" stroke="rgba(255,255,255,{0.5 if hi else 0.22})"/>')
    a(text(x + w / 2, 315, name, anchor='middle', size=14, fill='#fff' if hi else MUTED, ls='0'))
# route 1: straight for the disk, stopped at the boundary
a(f'<line x1="50" y1="90" x2="50" y2="130" stroke="{RED}" stroke-width="2" stroke-dasharray="3 3"/>')
a(f'<g transform="translate(50,136)"><circle r="10" fill="#2a1414" stroke="{RED}" stroke-width="2"/><path d="M -4 -4 L 4 4 M 4 -4 L -4 4" stroke="{RED}" stroke-width="2.2"/></g>')
a(text(66, 118, 'blocked', size=14, fill=RED))
# route 2: the system call, down and back
a(f'<path d="M 150 90 V 184 M 150 224 V 290" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="3 3"/>')
a(text(162, 118, 'system call', size=14, fill=GOLD))
# act 1: the red attempt
a(f'<circle cx="50" r="7" fill="{RED}" opacity="0">{T.anim("cy", [(0.0, 90), (0.4, 90), (1.2, 128), (2.6, 128), (9.0, 90)])}{win(0.4, 2.6)}</circle>')
a(f'<circle cx="50" cy="136" r="15" fill="none" stroke="{RED}" stroke-width="2.5" opacity="0">{win(1.2, 2.6)}</circle>')
# act 2: the trap, the work, the return
a(f'<circle cx="150" r="7" fill="{GOLD}" opacity="0">{T.anim("cy", [(0.0, 90), (3.2, 90), (4.0, 204), (4.6, 204), (5.2, 300), (5.8, 300)])}{win(3.2, 5.8)}</circle>')
a(f'<circle cx="150" r="7" fill="{BLUE}" opacity="0">{T.anim("cy", [(0.0, 300), (5.8, 300), (6.4, 204), (6.8, 204), (7.6, 90), (9.0, 90)])}{win(5.8, 7.8)}</circle>')
a(f'<rect x="108" y="288" width="102" height="44" rx="6" fill="none" stroke="#fff" stroke-width="2" opacity="0">{win(5.1, 6.0)}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Programs run in Ring 3 and cannot touch the hardware: a direct attempt is stopped by the CPU itself. '
           'To reach the disk a program makes a system call, a trap into the kernel in Ring 0, which does the work and returns, typically in under a microsecond.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rings.</b> x86 has four privilege levels; operating systems use two: Ring 0 for the kernel, Ring 3 for everything else.</li>
          <li><b>Enforced in silicon.</b> In Ring 3 the CPU itself refuses privileged instructions and the kernel's memory; no software stands in the way to be fooled.</li>
          <li><b>The way in.</b> A system call jumps to an entry point the kernel registered at boot, so a program can ask but never choose where it lands. The Bridge at the end of this Part opens the mechanism.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-14">
      <div class="diagram-label">Fig 1.14 · Protection rings · user programs, the kernel, the hardware</div>
      {svg}
      <p id="ch1-kernel-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-14', 'ch1-kernel-p5', card)
