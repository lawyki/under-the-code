# Fig 4.3 · A kernel module loading (Pass 28, law 3). Greenbar terminal: insmod, and the module steps
# down into Ring 0 beside the ones already loaded; its calls are linked against the kernel's symbol
# table and module_init() runs. Then rmmod takes it out again. t=0: loaded and linked.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 334
T = Timeline(10, shift=4.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (9.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-3 svgd-part2-3">')
a('<title id="svgt-part2-3">Fig 4.3 · A kernel module loading at runtime</title>')
a('<desc id="svgd-part2-3">A running Linux kernel with modules already loaded beside it: nvidia.ko, btrfs.ko, snd_hda_intel.ko. The command sudo insmod my_driver.ko brings a new module into Ring 0; '
  'its calls are linked against the kernel\'s symbol table and its module_init function runs. Later rmmod reverses it: module_exit runs and the module is removed.</desc>')
# terminal
a(f'<rect x="20" y="12" width="360" height="62" rx="4" fill="{PLATE}" stroke="rgba(132,255,178,0.4)"/>')
a(f'<g opacity="0">{win(0.3, 9.7)}{text(32, 36, "$ sudo insmod my_driver.ko", size=14, fill=PHOS, ls="0")}</g>')
a(f'<g opacity="0">{win(6.4, 9.7)}{text(32, 60, "$ sudo rmmod my_driver", size=14, fill=PHOS, ls="0")}</g>')
# the kernel
a(f'<rect x="20" y="100" width="360" height="226" rx="6" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
a(text(32, 120, 'KERNEL · Ring 0', size=13, fill=MUTED))
a(f'<rect x="32" y="134" width="150" height="176" rx="4" fill="#1b2a1f" stroke="{PHOS_SOFT}" stroke-opacity="0.6"/>')
a(text(44, 158, 'kernel image', size=14, fill='#fff', ls='0'))
a(text(44, 178, 'scheduler, VM,', size=13, fill=MUTED, ls='0'))
a(text(44, 196, 'syscall layer', size=13, fill=MUTED, ls='0'))
a(f'<rect x="44" y="240" width="126" height="56" rx="4" fill="{PLATE}" stroke="{PHOS}" stroke-opacity="0.6"/>')
a(text(56, 264, 'symbol', size=13, fill=PHOS, ls='0')); a(text(56, 282, 'table', size=13, fill=PHOS, ls='0'))
SLOTS = ['nvidia.ko', 'btrfs.ko', 'snd_hda_intel.ko']
for k, m in enumerate(SLOTS):
    y = 134 + k * 44
    a(f'<rect x="200" y="{y}" width="170" height="34" rx="4" fill="#1b2a1f" stroke="{PHOS_SOFT}" stroke-opacity="0.5"/>')
    a(text(212, y + 22, m, size=14, fill=PHOS_SOFT, ls='0'))
# the new module: snaps into the fourth slot (stepped, like the terminal), and out again on rmmod
a(f'<g opacity="0">{win(1.2, 7.2)}<rect x="200" y="266" width="170" height="34" rx="4" fill="{PHOS}" fill-opacity="0.22" stroke="{PHOS}" stroke-width="1.8"/>'
  f'<text x="212" y="288" {PLEX} font-size="14" fill="#fff">my_driver.ko</text></g>')
a(f'<rect class="fx" x="196" y="262" width="178" height="42" rx="6" fill="none" stroke="#fff" stroke-width="2" opacity="0">{win(1.2, 1.9)}</rect>')
# links to the symbol table, then module_init()
for k, yy in enumerate((276, 290)):
    a(f'<line x1="200" y1="{yy}" x2="170" y2="{yy - 6}" stroke="{PHOS}" stroke-width="2" opacity="0">{win(2.2 + k * 0.3, 7.0)}</line>')
a(f'<g opacity="0">{win(3.0, 6.4)}<rect x="200" y="306" width="170" height="16" rx="2" fill="none"/>{text(372, 318, "module_init()", anchor="end", size=13, fill=PHOS, ls="0")}</g>')
a(f'<g opacity="0">{win(6.6, 7.2)}{text(372, 318, "module_exit()", anchor="end", size=13, fill=RED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('insmod links a separately built module into the running kernel: its calls are resolved against the kernel\'s symbol table, its init function runs, and from then on it is part of Ring 0. '
           'rmmod takes it out again, so Linux stays monolithic in speed but modular in practice.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Load.</b> The kernel allocates memory for the module, copies its code in, and resolves every kernel function it calls by name in the symbol table.</li>
          <li><b>Start.</b> It calls the module's module_init(); a driver registers itself with the subsystem it serves.</li>
          <li><b>Still Ring 0.</b> A loaded module has the kernel's full power, so a buggy one can crash the machine (Fig 4.2).</li>
          <li><b>Unload.</b> rmmod calls module_exit(), frees the memory and forgets the module. lsmod lists what is loaded.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-3">
      <div class="diagram-label">Fig 4.3 · A kernel module loading at runtime</div>
      {svg}
      <p id="ch4-anatomy-p11" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-3', 'ch4-anatomy-p11', card)
