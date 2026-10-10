# Fig 4.2 · Monolithic vs microkernel (Pass 28, law 3). Two acts on two panels. Speed: one file read
# crosses the user/kernel boundary twice in a monolithic kernel and eight times in a microkernel
# (app → IPC → file-system server → IPC → driver, and back). Safety: a driver bug takes the whole
# monolithic kernel down; in the microkernel only the driver process fails and restarts.
# Greenbar: stepped motion. t=0: both reads done, crossings counted.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 410
T = Timeline(12, shift=5.6)
def snap_seq(points, t_end=5.8):
    """stepped motion: a list of (tau, x, y); returns cx, cy anims holding each stop."""
    xs, ys = [(0.0, points[0][1])], [(0.0, points[0][2])]
    for k, (t, x, y) in enumerate(points):
        if k: xs.append((t - 0.001, points[k - 1][1])); ys.append((t - 0.001, points[k - 1][2]))
        xs.append((t, x)); ys.append((t, y))
    return T.anim('cx', xs + [(11.9995, points[-1][1])]), T.anim('cy', ys + [(11.9995, points[-1][2])])
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (11.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-2 svgd-part2-2">')
a('<title id="svgt-part2-2">Fig 4.2 · Monolithic vs microkernel · speed against safety</title>')
a('<desc id="svgd-part2-2">Two kernels serve the same file read. In the monolithic kernel the program crosses into the kernel once, the file system and the disk driver run inside it, and the answer crosses back: two crossings. '
  'In the microkernel the file system and the driver are separate user programs, so the request hops through the kernel\'s message passing four times each way: eight crossings. '
  'Then a driver bug: in the monolithic kernel it brings down the whole machine; in the microkernel only the driver process fails and is restarted.</desc>')

def panel(y0, title):
    a(text(20, y0 + 16, title, size=14, fill=PHOS, ls='0'))
    a(f'<rect x="20" y="{y0 + 26}" width="360" height="62" rx="4" fill="{PLATE}" stroke="rgba(132,255,178,0.3)"/>')
    a(text(28, y0 + 42, 'user', size=13, fill=MUTED, ls='0'))
    a(f'<line x1="20" y1="{y0 + 94}" x2="380" y2="{y0 + 94}" stroke="{PHOS}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    a(f'<rect x="20" y="{y0 + 100}" width="360" height="62" rx="4" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
    a(text(28, y0 + 116, 'kernel · Ring 0', size=13, fill=MUTED, ls='0'))
def box(x, y, w, lab, col=PHOS_SOFT):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="4" fill="#1b2a1f" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(x + 8, y + 20, lab, size=13, fill='#fff', ls='0'))
    return (x + w - 12, y + 15)            # where a packet stops: the box's empty right end

# panel A: monolithic
A0 = 6
panel(A0, 'MONOLITHIC · Linux')
app_a = box(40, A0 + 48, 76, 'app')
fs_a = box(144, A0 + 124, 66, 'FS')
drv_a = box(222, A0 + 124, 84, 'driver')
box(316, A0 + 124, 60, 'sched')
# panel B: microkernel
B0 = 214
panel(B0, 'MICROKERNEL · seL4')
app_b = box(40, B0 + 48, 76, 'app')
fs_b = box(136, B0 + 48, 118, 'FS server')
drv_b = box(270, B0 + 48, 100, 'driver')
a(text(370, B0 + 152, 'IPC', anchor='end', size=13, fill=PHOS, ls='0'))
ipc_b = (0, B0 + 134)
# act 1: the read, stepped
STEP = 0.55
seqA = [app_a, fs_a, drv_a, fs_a, app_a]
cA = snap_seq([(0.3 + k * STEP * 2, x, y) for k, (x, y) in enumerate(seqA)])
a(f'<circle class="fx" r="7" fill="{PHOS}" stroke="{PLATE}" stroke-width="2">{cA[0]}{cA[1]}{win(0.3, 5.9)}</circle>')
ipcA = lambda x: (x, ipc_b[1])
seqB = [app_b, ipcA(app_b[0]), fs_b, ipcA(fs_b[0]), drv_b, ipcA(drv_b[0]), fs_b, ipcA(fs_b[0]), app_b]
cB = snap_seq([(0.3 + k * STEP, x, y) for k, (x, y) in enumerate(seqB)])
a(f'<circle class="fx" r="7" fill="{PHOS}" stroke="{PLATE}" stroke-width="2">{cB[0]}{cB[1]}{win(0.3, 5.9)}</circle>')
# crossings, counted as they happen
for k, (t0, t1) in enumerate(((0.3 + 2 * STEP, 0.3 + 6 * STEP), (0.3 + 6 * STEP, 11.9)), 1):   # in at FS, back out at app
    a(f'<text x="380" y="{A0 + 16}" text-anchor="end" {PLEX} font-size="14" fill="{PHOS}" opacity="0">crossings: {k}{win(t0, t1)}</text>')
for k in range(1, 9):
    t0 = 0.3 + k * STEP
    a(f'<text x="380" y="{B0 + 16}" text-anchor="end" {PLEX} font-size="14" fill="{PHOS}" opacity="0">crossings: {k}{win(t0, 11.9 if k == 8 else t0 + STEP)}</text>')
# act 2: a driver bug
CR = 6.4
a(f'<g opacity="0">{win(CR, 11.6)}<rect class="fx" x="20" y="{A0 + 100}" width="360" height="62" rx="4" fill="{RED}" fill-opacity="0.35" stroke="{RED}" stroke-width="2"/>'
  f'</g>')
a(f'<g opacity="0">{win(CR, 11.6)}{text(200, A0 + 186, "one driver bug: the whole machine down", anchor="middle", size=13, fill=RED, ls="0")}</g>')
a(f'<g opacity="0">{win(CR, 8.6)}<rect class="fx" x="270" y="{B0 + 48}" width="100" height="30" rx="4" fill="{RED}" fill-opacity="0.45" stroke="{RED}" stroke-width="2"/></g>')
a(f'<g opacity="0">{win(8.6, 11.6)}{text(320, B0 + 42, "restarted", anchor="middle", size=13, fill=PHOS, ls="0")}</g>')
a(f'<g opacity="0">{win(CR, 8.6)}{text(320, B0 + 42, "driver fails", anchor="middle", size=13, fill=RED, ls="0")}</g>')
a(text(20, 402, 'speed: fewer crossings · safety: smaller blast', size=13, fill='rgba(198,222,206,0.6)', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('A monolithic kernel runs everything in Ring 0, so a file read crosses the boundary twice; a microkernel runs file systems and drivers as separate programs, so the same read crosses eight times. '
           'The price buys safety: a driver bug takes down one process, not the machine.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Monolithic.</b> Scheduler, memory, file systems, drivers and network stack share one address space in Ring 0 and call each other directly.</li>
          <li><b>Microkernel.</b> Ring 0 keeps only message passing, basic memory protection and scheduling; everything else is a user process that talks by IPC.</li>
          <li><b>The trade.</b> Every crossing costs time, so microkernels are slower; every component outside Ring 0 is a bug that cannot corrupt the kernel, so they are safer.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-2">
      <div class="diagram-label">Fig 4.2 · Monolithic vs microkernel · speed against safety</div>
      {svg}
      <p id="ch4-anatomy-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-2', 'ch4-anatomy-p9', card)
