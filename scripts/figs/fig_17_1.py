# Fig 17.1 · Type 1 vs Type 2 hypervisors · bare metal vs hosted (Pass 28, law 3). Quorum glass plate. Two stacks: type
# 1, guests on a hypervisor on the hardware; type 2, guests on a hypervisor that is an application inside a host
# operating system. In each, a guest's ordinary instruction runs straight on the CPU, while a privileged one (here,
# switching page tables) traps down to the hypervisor, which does it on the guest's behalf and returns. Hardware
# support (VT-x, AMD-V) makes that trap reliable. Phase-synced in both stacks. t=0 (shift): both traps returned.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
o = []; a = o.append
def layer(x, y, w, h, lab, col, sub=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{QCARD}" stroke="{col}" stroke-opacity="0.85"/>')
    a(text(x + w / 2, y + (h / 2 + 5 if not sub else 18), lab, anchor='middle', size=13, fill=col, ls='0'))
    if sub:
        a(text(x + w / 2, y + 35, sub, anchor='middle', size=13, fill=QMUTED, ls='0'))
LX, RX, SW = 10, 206, 184
# type 1
a(text(LX, 18, 'type 1: bare metal', anchor='start', size=13, fill=VIOLET, ls='0'))
layer(LX, 30, 88, 40, 'guest A', QSOFT); layer(LX + 96, 30, 88, 40, 'guest B', QSOFT)
layer(LX, 116, SW, 44, 'hypervisor', VIOLET, 'KVM, ESXi, Hyper-V')
layer(LX, 206, SW, 36, 'hardware', QAMBER)
# type 2
a(text(RX, 18, 'type 2: hosted', anchor='start', size=13, fill=TEAL, ls='0'))
layer(RX, 30, 88, 40, 'guest A', QSOFT); layer(RX + 96, 30, 88, 40, 'browser', QMUTED)
layer(RX, 82, 88, 34, 'hypervisor', TEAL)
layer(RX, 128, SW, 44, 'host OS', QSOFT, 'macOS, Windows')
layer(RX, 206, SW, 36, 'hardware', QAMBER)
# instructions from guest A in each stack: ordinary goes to the CPU, privileged traps to the hypervisor
def fly(x0, y0, x1, y1, t0, t1, col, back=None):
    kx = [(0.0, 0.0), (t0, 0.0), (t1, x1 - x0)] + ([(back[0], x1 - x0), (back[1], 0.0)] if back else []) + [(D, 0.0)]
    ky = [(0.0, 0.0), (t0, 0.0), (t1, y1 - y0)] + ([(back[0], y1 - y0), (back[1], 0.0)] if back else []) + [(D, 0.0)]
    end = (back[1] if back else t1) + 0.01
    a(f'<g class="fx" opacity="0">{lit(t0, end)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{x0}" cy="{y0}" r="6" fill="{col}"/></g></g></g>')
TA0, TA1 = 0.8, 2.0                                    # ordinary instruction: straight to the CPU
TB0, TB1, TB2, TB3 = 3.0, 4.0, 5.2, 6.2                # privileged: trap, handled, returned
for gx, hy in ((LX + 44, 138), (RX + 44, 99)):
    fly(gx - 10, 72, gx - 10, 222, TA0, TA1, QSOFT)
    fly(gx + 10, 72, gx + 10, hy, TB0, TB1, QROSE, back=(TB2, TB3))
a(f'<g class="fx" opacity="0">{pulse(TB1)}<rect x="{LX - 2}" y="114" width="{SW + 4}" height="48" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(f'<g class="fx" opacity="0">{pulse(TB1)}<rect x="{RX - 2}" y="80" width="92" height="38" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
# what is happening
SY = 266
for t0, t1, s, col in ((TA0, TB0, 'add: runs straight on the CPU', QSOFT), (TB0, TB2, 'switch page tables: traps', QROSE),
                       (TB2, None, 'hypervisor does it, guest resumes', VIOLET)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, SY, s, anchor="start", size=13, fill=col, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-14 svgd-part5-14">')
o.insert(1, '<title id="svgt-part5-14">Fig 17.1 · Type 1 vs Type 2 hypervisors · bare metal vs hosted</title>')
o.insert(2, '<desc id="svgd-part5-14">Two stacks. Type 1: guest operating systems run on a hypervisor such as KVM, ESXi or Hyper-V, which runs directly on the hardware. Type 2: guests run on a hypervisor that is an application inside a host operating system such as macOS or Windows, beside ordinary apps. '
  'In both, a guest\'s ordinary instruction, such as an add, runs straight on the processor, while a privileged one, such as switching page tables, traps down to the hypervisor, which does it on the guest\'s behalf, and the guest resumes.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A guest\'s ordinary instructions run straight on the processor; only privileged ones, such as switching page tables, trap to the hypervisor, which does them on the guest\'s behalf. '
           'A type 1 hypervisor sits on the bare hardware, as in every public cloud; a type 2 runs as an application inside a desktop operating system.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The hardware help.</b> Intel VT-x and AMD-V (2005–2006) add a mode beneath the guest's own kernel mode, so every sensitive instruction traps cleanly to the hypervisor.</li>
          <li><b>Before that.</b> A few x86 instructions touched privileged state without trapping, so VMware rewrote guest code as it ran (binary translation) and Xen had guests call the hypervisor on purpose (paravirtualization).</li>
          <li><b>Examples.</b> Type 1: KVM, Xen, ESXi, Hyper-V. Type 2: VirtualBox, VMware Workstation, Parallels, each an application plus a kernel driver, which is where its traps land.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-1">
      <div class="diagram-label">Fig 17.1 · Type 1 vs Type 2 hypervisors · bare metal vs hosted</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-1"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-1', cap, card.replace('CAPID', cap))
