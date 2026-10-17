# Fig 4.19 · VMs vs containers (Pass 28, law 3). Two stacks; pulses show whose kernel answers each
# app's system calls: each VM app its own guest kernel, every container app the one host kernel.
# t=0: both stacks, no pulse lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

W, H = 400, 296
D = 6.0
T = Timeline(D, shift=0.0)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
RH, Y_APP, Y_K, Y_HV, Y_HW = 30, 40, 92, 144, 182
def box(x, y, w, label, col='rgba(132,255,178,0.4)', fill=PANEL, tcol='#fff'):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" rx="3" fill="{fill}" stroke="{col}"/>')
    a(text(x + w / 2, y + 20, label, anchor='middle', size=13, fill=tcol, ls='0'))
def call(x0, y0, x1, y1, t):
    a(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="rgba(198,222,206,0.3)" stroke-width="1.2"/>')
    a(f'<line class="fx" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{PHOS}" stroke-width="3" opacity="0">{lit(t, t + 0.7)}</line>')
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-20 svgd-part2-20">')
a('<title id="svgt-part2-20">Fig 4.19 · VMs vs containers</title>')
a('<desc id="svgd-part2-20">Left, virtual machines: on the hardware runs a hypervisor; on it, each virtual machine runs its own guest kernel with its app above it, so each app\'s system calls go to its own kernel. '
  'Right, containers: on the hardware runs one host kernel; three apps sit on it, each fenced by namespaces and cgroups, and all of their system calls go to that one shared kernel. '
  'Virtual machines cost a kernel and gigabytes each and boot in seconds; containers share one kernel, cost megabytes and start like a process.</desc>')
# VMs
VX, CXL, CW = 20, 208, 176
a(text(VX, 24, 'VIRTUAL MACHINES', size=13, fill=MUTED))
for k in range(2):
    x = VX + k * 92
    box(x, Y_APP, 84, 'app')
    box(x, Y_K, 84, 'kernel', col=GOLD, tcol=GOLD)
    call(x + 42, Y_APP + RH, x + 42, Y_K, 0.5 + 0.5 * k)
box(VX, Y_HV, CW, 'hypervisor', col='rgba(198,222,206,0.5)')
# containers
a(text(CXL, 24, 'CONTAINERS', size=13, fill=MUTED))
for k in range(3):
    x = CXL + k * 60
    box(x, Y_APP, 56, 'app')
    a(f'<rect x="{x - 2}" y="{Y_APP - 3}" width="60" height="{RH + 6}" rx="4" fill="none" stroke="rgba(132,255,178,0.35)" stroke-dasharray="3 3"/>')
    call(x + 28, Y_APP + RH + 3, CXL + CW / 2 + (k - 1) * 30, Y_HV, 1.8 + 0.5 * k)
box(CXL, Y_HV, CW, 'one host kernel', col=GOLD, tcol=GOLD)
for x in (VX, CXL):
    box(x, Y_HW, CW, 'hardware', col='rgba(198,222,206,0.3)', fill=PLATE, tcol=MUTED)
for x, lines in ((VX, ['a kernel per VM', 'gigabytes each', 'boots in seconds']), (CXL, ['one kernel, fenced', 'megabytes each', 'starts like a process'])):
    for i, s in enumerate(lines):
        a(text(x, 238 + i * 20, s, size=13, fill=PHOS_SOFT, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('A virtual machine runs its own guest kernel on a hypervisor; a container is an ordinary process whose system calls go to the one host kernel, fenced by namespaces (what it can see) and cgroups (what it can use).')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Hypervisors.</b> KVM turns Linux into one; VMware ESXi, Xen and Hyper-V are others. CPU extensions (Intel VT-x, AMD-V) let guest kernels run directly on the processor.</li>
          <li><b>The fences.</b> Namespaces and cgroups are ordinary kernel features; the next two figures show each.</li>
          <li><b>The middle ground.</b> MicroVMs such as AWS Firecracker boot a minimal guest kernel in about 125 ms, giving each container its own kernel at nearly container cost.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-19">
      <div class="diagram-label">Fig 4.19 · VMs vs containers</div>
      {svg}
      <p id="ch4-security-p10" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-19', 'ch4-security-p10', card)
