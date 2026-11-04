# Fig 1.14 · Protection rings (Pass 31, Part I, from an empty script). Job: function. Takeaway: programs share
# the machine, so the kernel owns the disk; a program must ask it, and it checks first.
# Concept: three layers, programs over the kernel over the hardware, with one wall between programs and kernel and
# one door in it. Two paths from your program, both always drawn so the still teaches: the direct reach for the
# disk stops dead at the wall (the CPU refuses it); the request goes through the door, the kernel checks it, drives
# the disk, and the data comes back up. Labels by role, as the ledger asks: Ring 0, Ring 3 and system call stay in
# the caption and the strip.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, MUTED

W, H = 400, 340
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.42)'
T = Timeline(9, shift=0.0)
WALL = 128
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-15 svgd-part1-15">')
a('<title id="svgt-part1-15">Fig 1.14 · Protection rings · user programs, the kernel, the hardware</title>')
a('<desc id="svgd-part1-15">Three layers: programs on top, the kernel in the middle, the hardware below, with a wall between programs '
  'and kernel that has one door. Your program reaching straight for the disk is stopped at the wall by the CPU. The same request '
  'made through the door, a system call, reaches the kernel, which checks it, drives the disk and sends the data back up to the '
  'program.</desc>')

# the three layers
a(f'<rect x="16" y="16" width="368" height="88" rx="8" fill="none" stroke="rgba(134,168,255,0.55)" stroke-width="1.4"/>')
a(text(30, 38, 'programs', size=14, fill=BLUE))
a(f'<rect x="16" y="152" width="368" height="76" rx="8" fill="none" stroke="rgba(212,168,83,0.6)" stroke-width="1.4"/>')
a(text(30, 174, 'kernel', size=14, fill=GOLD))
a(f'<rect x="16" y="244" width="368" height="80" rx="8" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.4"/>')
a(text(30, 266, 'hardware', size=14, fill=MUTED))
# the programs
a(f'<rect x="40" y="48" width="170" height="40" rx="6" fill="none" stroke="{INK}" stroke-width="1.6"/>')
a(text(125, 73, 'your program', anchor='middle', size=15, fill=INK))
a(f'<rect x="232" y="48" width="130" height="40" rx="6" fill="none" stroke="rgba(255,255,255,0.35)"/>')
a(text(297, 73, 'another', anchor='middle', size=14, fill=MUTED))
# the wall, with its one door
DX0, DX1 = 156, 194
a(f'<path d="M 16 {WALL} H {DX0} M {DX1} {WALL} H 384" stroke="{GOLD}" stroke-width="2.4" stroke-dasharray="7 4"/>')
a(f'<path d="M {DX0} {WALL - 7} V {WALL + 7} M {DX1} {WALL - 7} V {WALL + 7}" stroke="{GOLD}" stroke-width="2.4"/>')
# the disk, drawn as a drive: a stack of platters
cx, cy = 175, 288
a(f'<ellipse cx="{cx}" cy="{cy + 12}" rx="34" ry="9" fill="#151515" stroke="{INK}" stroke-opacity="0.7"/>')
a(f'<path d="M {cx - 34} {cy} V {cy + 12} M {cx + 34} {cy} V {cy + 12}" stroke="{INK}" stroke-opacity="0.7"/>')
a(f'<rect x="{cx - 34}" y="{cy}" width="68" height="12" fill="#151515"/>')
a(f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="9" fill="#1d1d1d" stroke="{INK}" stroke-opacity="0.8"/>')
a(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}" opacity="0.7"/>')
a(text(cx + 46, cy + 10, 'disk', size=14, fill=INK))

# path 1: the direct reach, stopped at the wall
a(f'<path d="M 82 88 V {WALL - 6}" stroke="{RED}" stroke-width="2.4"/>')
a(f'<path d="M 74 {WALL - 8} l 16 16 m 0 -16 l -16 16" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>')
a(text(98, WALL + 19, 'blocked', size=14, fill=RED))
# path 2: through the door, checked by the kernel, to the disk
a(f'<path d="M {cx} 88 V 183 M {cx} 209 V {cy - 12}" stroke="{GOLD}" stroke-width="2.4"/>')
a(text(cx + 14, WALL - 8, 'asks the kernel', size=14, fill=GOLD))
a(f'<circle cx="{cx}" cy="196" r="13" fill="none" stroke="{GOLD}" stroke-width="2"/>')
a(f'<path d="M {cx - 6} 196 l 4 5 l 8 -10" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
a(text(cx + 22, 201, 'checks first', size=14, fill=INK))

# motion: the reach flashes and dies at the wall; the request travels down, the data travels back up
a(f'<circle cx="82" cy="0" r="5" fill="{RED}" opacity="0">'
  f'{T.anim("opacity", [(0.3, 0.0), (0.4, 1.0), (1.3, 1.0), (1.6, 0.0)])}'
  f'<animate attributeName="cy" values="{88};{WALL - 8};{WALL - 8}" keyTimes="0;0.11;1" dur="9s" begin="-8.7s" repeatCount="indefinite"/></circle>')
def travel(col, y0, y1, t0, t1):
    pts_y = [(0.0, y0), (t0, y0), (t1, y1), (8.99, y1)]
    a(f'<g opacity="0">{T.anim("opacity", [(t0 - 0.1, 0.0), (t0, 1.0), (t1, 1.0), (t1 + 0.2, 0.0)])}'
      f'<g>{T.translate([(t, v - y0) for t, v in pts_y], axis="y")}<circle cx="{cx}" cy="{y0}" r="5.5" fill="{col}"/></g></g>')
travel(GOLD, 88, 196, 2.4, 3.6)          # the request, through the door to the kernel's check
travel(GOLD, 196, cy - 12, 4.1, 5.0)     # checked: on to the disk
travel(BLUE, cy - 12, 88, 5.6, 7.4)      # the data, back up to the program
a('</svg>')
svg = '\n'.join(o)

caption = ('The CPU runs each program at a privilege level, or ring: Ring 3 for programs, Ring 0 for the kernel. The red path, a '
           'program reaching straight for the disk, is blocked; the gold one, a request to the kernel called a system call, is let through.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rings.</b> x86 has four privilege levels; operating systems use two: Ring 0 for the kernel, Ring 3 for everything else.</li>
          <li><b>Enforced in silicon.</b> In Ring 3 the CPU itself refuses privileged instructions and the kernel's memory; no software stands in the way to be fooled.</li>
          <li><b>The door.</b> A system call enters the kernel at one fixed place the kernel chose, never wherever the program likes; there the kernel checks the request before it touches the disk.</li>
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
