# Fig 4.21 · Cgroups (Pass 28, law 3). Greenbar paper card. Two panels, CPU and memory; each group's
# limit is an outlined track, its use a fill. The batch job wants 12 CPUs (dashed ghost) and gets its
# 4: throttled. Then it outgrows its 16 GB and is OOM-killed; web and db never move.
# t=0 (shift): batch throttled, wanting 12.
import figlib
from figlib import Timeline, text, splice, PLEX
figlib.FONT = PLEX

INK, INK_SOFT, GB, AMBER, RED = '#1d2b22', 'rgba(29,43,34,0.62)', '#2e6f52', '#8a5a00', '#b3261e'
W, H = 400, 262
TX, TW = 84, 240
D = 10.0
T = Timeline(D, shift=3.0)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
GROUPS = ['web', 'db', 'batch']
CAP_CPU, CAP_MEM = {'web': 4, 'db': 8, 'batch': 4}, {'web': 16, 'db': 32, 'batch': 16}
USE_CPU, USE_MEM = {'web': 2, 'db': 6}, {'web': 6, 'db': 24}
cpu_w, mem_w = TW / 16, TW / 64
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-22 svgd-part2-22">')
a('<title id="svgt-part2-22">Fig 4.21 · Cgroups: quotas as taps on the resource flow</title>')
a('<desc id="svgd-part2-22">A host with 16 CPUs and 64 GB of memory runs three cgroups. web is limited to 4 CPUs and 16 GB, db to 8 CPUs and 32 GB, batch to 4 CPUs and 16 GB. '
  'web and db use part of their share. The batch job asks for 12 CPUs; the kernel throttles it at its 4. Its memory then grows to its 16 GB limit and the kernel kills it; '
  'web and db carry on untouched.</desc>')
def panel(y0, title):
    a(text(20, y0, title, size=13, fill=INK_SOFT))
def row(y, name, cap_units, unit_w, base_w=None):
    a(text(20, y + 14, name, size=14, fill=INK, ls='0'))
    a(f'<rect x="{TX}" y="{y}" width="{TW}" height="18" rx="2" fill="rgba(29,43,34,0.05)" stroke="rgba(29,43,34,0.15)"/>')
    a(f'<rect x="{TX}" y="{y}" width="{cap_units * unit_w:.1f}" height="18" rx="2" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    a(text(TX + TW + 8, y + 14, f'{cap_units}', size=13, fill=INK, ls='0'))
CPU_Y, MEM_Y, PITCH = [34, 60, 86], [146, 172, 198], 26
panel(20, 'CPU · host has 16 · limit outlined')
panel(132, 'MEMORY · host has 64 GB')
for k, g in enumerate(GROUPS):
    row(CPU_Y[k], g, CAP_CPU[g], cpu_w)
    row(MEM_Y[k], g, CAP_MEM[g], mem_w)
    if g != 'batch':
        a(f'<rect x="{TX}" y="{CPU_Y[k] + 3}" width="{USE_CPU[g] * cpu_w:.1f}" height="12" fill="{GB}" fill-opacity="0.75"/>')
        a(f'<rect x="{TX}" y="{MEM_Y[k] + 3}" width="{USE_MEM[g] * mem_w:.1f}" height="12" fill="{GB}" fill-opacity="0.75"/>')
# batch CPU: demand ghost and capped use
yb = CPU_Y[2]
dem = [(0.0, 1), (1.0, 1), (2.0, 12), (7.0, 12), (7.01, 0), (8.0, 1), (D, 1)]
use = [(0.0, 1), (1.0, 1), (1.27, 4), (7.0, 4), (7.01, 0), (8.0, 1), (D, 1)]
a(f'<rect x="{TX}" y="{yb + 1}" width="{cpu_w:.1f}" height="16" fill="none" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="4 3">{T.anim("width", [(t, v * cpu_w) for t, v in dem])}</rect>')
a(f'<rect x="{TX}" y="{yb + 3}" width="{cpu_w:.1f}" height="12" fill="{GB}" fill-opacity="0.75">{T.anim("width", [(t, v * cpu_w) for t, v in use])}</rect>')
a(f'<rect x="{TX}" y="{yb + 3}" width="{4 * cpu_w:.1f}" height="12" fill="{AMBER}" fill-opacity="0.8" opacity="0">{lit(1.3, 7.0)}</rect>')
a(f'<g opacity="0">{lit(1.3, 7.0)}{text(TX + 4 * cpu_w + 10, yb + 14, "wants 12", size=13, fill=AMBER, ls="0")}</g>')
# batch memory: climbs, hits 16 GB, killed, restarts small
ym = MEM_Y[2]
mem = [(0.0, 4), (4.0, 4), (6.4, 16), (6.6, 16), (6.61, 0), (7.4, 0), (8.4, 2), (D, 2)]
a(f'<rect x="{TX}" y="{ym + 3}" width="{4 * mem_w:.1f}" height="12" fill="{GB}" fill-opacity="0.75">{T.anim("width", [(t, v * mem_w) for t, v in mem])}</rect>')
a(f'<rect class="fx" x="{TX - 2}" y="{ym - 2}" width="{16 * mem_w + 4:.1f}" height="22" rx="3" fill="{RED}" fill-opacity="0.25" stroke="{RED}" stroke-width="2" opacity="0">{lit(6.4, 7.0)}</rect>')
a(f'<g opacity="0">{lit(6.6, 7.6)}{text(TX + 16 * mem_w + 8, ym + 14, "killed", size=13, fill=RED, ls="0")}</g>')
# status
STAT = [(0.3, 1.3, 'batch asks for more CPU', INK), (1.3, 4.0, 'wants 12 CPUs, gets 4: throttled', AMBER),
        (4.0, 6.4, 'batch memory grows toward 16 GB', INK), (6.4, 7.6, 'over its limit: OOM-killed', RED),
        (7.6, 9.7, 'web and db never noticed', GB)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{lit(t0, t1)}{text(W / 2, 248, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Namespaces decide what a process can see; cgroups decide what it can use, with a CPU and a memory limit per group that the kernel enforces. A runaway batch job wanting 12 CPUs is held to its 4, and when it outgrows its 16 GB the kernel kills it, while web and db never notice.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The interface.</b> Cgroup v2 is a filesystem at <code>/sys/fs/cgroup</code>. Writing <code>400000 100000</code> to <code>cpu.max</code> allows 4 CPUs' worth of time in every 100 ms period.</li>
          <li><b>Memory.</b> Past <code>memory.max</code> the kernel first reclaims the group's own pages; if that fails, the OOM killer picks a process inside the group.</li>
          <li><b>Who writes them.</b> Docker's <code>--cpus</code> and <code>--memory</code>, Kubernetes resource limits and systemd's services all write these files; <code>io.max</code> and <code>pids.max</code> are further files, for disk and process counts.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-4-21">
      <div class="diagram-label">Fig 4.21 · Cgroups: quotas as taps on the resource flow</div>
      {svg}
      <p id="ch4-security-p13" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-21', 'ch4-security-p13', card)
