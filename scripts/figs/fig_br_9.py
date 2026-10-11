# Fig BR.9 · Hardware features → kernel → abstractions (Pass 28, law 3, conceptual pass). Five rows, silicon on the
# left, what programs get on the right, the kernel between them. First the kernel connects each row in turn; then each
# feature is taken away in turn, its row breaks, its abstraction dims, and one line says what is lost. t=0 (shift): all
# five rows connected, with the rule beneath.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

ROWS = [('privilege bit', 'root vs user', 'no privilege: any program can do anything'),
        ('traps', 'system calls', 'no traps: no safe way into the kernel'),
        ('MMU · TLB', 'processes', 'no MMU: every program reads every other'),
        ('timer', 'multitasking', 'no timer: a stuck loop keeps the CPU'),
        ('MMIO · DMA', 'files, network', 'no MMIO or DMA: no disk, no network')]
W = 400
D = 14.0
T = Timeline(D, shift=13.4)
TB = [0.8 + 0.5 * k for k in range(5)]                 # build: the kernel connects row k
R0, RS = 4.2, 1.8
TR = [R0 + RS * k for k in range(5)]                   # remove feature k
TE = R0 + RS * 5
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
dim = lambda t0, t1: T.anim('opacity', [(0.0, 1.0), (t0 - 0.002, 1.0), (t0, 0.3), (t1 - 0.008, 0.3), (t1 - 0.005, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.5, 0.0), (D, 0.0)])
o = []; a = o.append
HX, HW, KX, KW, AX, AW = 20, 120, 156, 72, 244, 136
a(text(HX, 24, 'silicon', size=13, fill=BLUE, ls='0'))
a(text(KX + KW / 2, 24, 'kernel', anchor='middle', size=13, fill=GOLD, ls='0'))
a(text(AX + AW, 24, 'what you get', anchor='end', size=13, fill=GREEN, ls='0'))
Y0, RH, GAP = 40, 40, 12
ry = lambda k: Y0 + k * (RH + GAP)
a(f'<rect x="{KX}" y="{Y0 - 4}" width="{KW}" height="{5 * RH + 4 * GAP + 8}" rx="6" fill="{GOLD}" fill-opacity="0.10" stroke="{GOLD}" stroke-opacity="0.6"/>')
for k, (hw, ab, _) in enumerate(ROWS):
    y = ry(k); cy = y + RH / 2
    t0, t1 = TR[k], TR[k] + RS
    a(f'<rect x="{HX}" y="{y}" width="{HW}" height="{RH}" rx="5" fill="{BLUE}" fill-opacity="0.10" stroke="{BLUE}" stroke-opacity="0.6"/>')
    a(f'<g>{dim(t0, t1)}{text(HX + 10, cy + 5, hw, size=13, fill="#fff", ls="0")}</g>')
    a(f'<rect x="{AX}" y="{y}" width="{AW}" height="{RH}" rx="5" fill="{GREEN}" fill-opacity="0.10" stroke="{GREEN}" stroke-opacity="0.6"/>')
    a(f'<g>{dim(t0 + 0.3, t1)}{text(AX + 10, cy + 5, ab, size=13, fill="#fff", ls="0")}</g>')
    # the joins, through the kernel
    a(f'<g>{dim(t0, t1)}<line x1="{HX + HW}" y1="{cy}" x2="{KX}" y2="{cy}" stroke="{MUTED}"/><line x1="{KX + KW}" y1="{cy}" x2="{AX}" y2="{cy}" stroke="{MUTED}"/>'
      f'<circle cx="{KX + KW / 2}" cy="{cy}" r="4" fill="{GOLD}"/></g>')
    # build: a token runs the row, the abstraction lights on arrival
    mv = T.translate([(0.0, 0.0), (TB[k], 0.0), (TB[k] + 0.6, AX - HX - HW), (D, AX - HX - HW)], 'x')
    a(f'<g class="fx" opacity="0">{lit(TB[k], TB[k] + 0.61)}<g>{mv}<circle cx="{HX + HW}" cy="{cy}" r="6" fill="#fff"/></g></g>')
    a(f'<g class="fx" opacity="0">{pulse(TB[k] + 0.6)}<rect x="{AX - 2}" y="{y - 2}" width="{AW + 4}" height="{RH + 4}" rx="6" fill="none" stroke="#fff" stroke-width="2"/></g>')
    # removal: red outlines on both ends
    for x, w in ((HX, HW), (AX, AW)):
        a(f'<g class="fx" opacity="0">{lit(t0, t1)}<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{RH + 4}" rx="6" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/></g>')
LY = ry(5) + 22
for k, (_, _, loss) in enumerate(ROWS):
    a(f'<g opacity="0">{lit(TR[k], TR[k] + RS)}{text(HX, LY, loss, size=13, fill=RED, ls="0")}</g>')
rule = T.anim('opacity', [(0.0, 1.0), (R0 - 0.002, 1.0), (R0, 0.0), (TE - 0.008, 0.0), (TE - 0.005, 1.0), (D, 1.0)])
a(f'<g>{rule}{text(HX, LY, "take a feature away, its abstraction goes", size=13, fill=MUTED, ls="0")}</g>')
H = LY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-51 svgd-part1-51">')
o.insert(1, '<title id="svgt-part1-51">Fig BR.9 · Hardware features → kernel → abstractions</title>')
o.insert(2, '<desc id="svgd-part1-51">Five hardware features on the left, the abstractions programs rely on at the right, and the kernel joining each pair: the privilege bit gives root versus user, traps give system calls, the MMU and TLB give separate processes, the timer gives multitasking, and MMIO and DMA give files and networking. '
  'Each feature is then taken away in turn and its abstraction goes with it: without privilege any program can do anything, without traps there is no safe way into the kernel, without the MMU every program can read every other, without the timer a stuck loop keeps the CPU, and without MMIO and DMA there is no disk and no network.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each abstraction programs rely on rests on a hardware feature that the kernel sets up at boot and then manages. '
           'Take a feature away and its abstraction goes with it: without the timer there is no multitasking, without the MMU no separate processes.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why the kernel.</b> Only code running with full privilege can program these features, so one program does it and every other program asks it through system calls.</li>
          <li><b>Not strictly one to one.</b> A process needs the MMU, traps and the timer together; each row shows the feature its abstraction cannot do without.</li>
          <li><b>What comes next.</b> The silicon asks for little: page tables, a trap handler, a timer. Everything else a kernel contains, Part II takes up.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-9">
      <div class="diagram-label">Fig BR.9 · Hardware features → kernel → abstractions</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-9"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-9', cap, card.replace('CAPID', cap))
