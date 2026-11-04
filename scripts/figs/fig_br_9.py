# Fig BR.9 · Hardware features to abstractions (Pass 31, Part I, from an empty script). Job: function. Takeaway: each
# abstraction rests mainly on one hardware feature the kernel sets up, so removing it removes the abstraction.
# Concept: the ledger's redesign, not a redraw: five features on the left, the kernel joining each to its abstraction on
# the right, and then each feature taken away in turn (Part I's light verb, in red): the feature is struck out, its link
# goes dark, and its abstraction breaks, with the consequence written below. t=0 is the whole, before any is removed.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 346
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
ROWS = [('privilege bit', 'kernel vs user', 'any program can do anything'),
        ('traps', 'system calls', 'no safe way into the kernel'),
        ('MMU · TLB', 'processes', 'every program reads every other'),
        ('timer', 'multitasking', 'a stuck loop keeps the CPU'),
        ('MMIO · DMA', 'files, network', 'no disk and no network')]
STEP = 2.4
D = 1.6 + STEP * len(ROWS) + 0.6
T = Timeline(D, shift=0.6)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
RY = lambda k: 46 + k * 46
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-51 svgd-part1-51"{T.steps([(1.0, 'whole'), (2.6, 'privilege'), (5.0, 'traps'), (7.4, 'MMU'), (9.799999999999999, 'timer'), (12.2, 'MMIO')])}>')
a('<title id="svgt-part1-51">Fig BR.9 · Hardware features → kernel → abstractions</title>')
a('<desc id="svgd-part1-51">Five hardware features on the left, the abstractions programs rely on at the right, and the kernel joining each '
  'pair: the privilege bit gives a protected kernel apart from user programs, traps give system calls, the MMU and TLB give separate '
  'processes, the timer gives multitasking, and MMIO and DMA give files and networking. Each feature is then taken away in turn and '
  'its abstraction goes with it: without privilege any program can do anything, without traps there is no safe way into the kernel, '
  'without the MMU every program can read every other, without the timer a stuck loop keeps the CPU, and without MMIO and DMA there is '
  'no disk and no network.</desc>')

a(text(20, 26, 'silicon', size=14, fill=BLUE))
a(text(200, 26, 'kernel', anchor='middle', size=14, fill=GOLD))
a(text(380, 26, 'what you get', anchor='end', size=14, fill=GREEN))
a(f'<rect x="176" y="{RY(0) - 6}" width="48" height="{RY(4) - RY(0) + 44}" rx="8" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
for k, (feat, abst, loss) in enumerate(ROWS):
    y = RY(k)
    t0 = 1.6 + k * STEP
    off = (t0, t0 + STEP - 0.2)
    # the intact row, hidden while it is broken
    on = T.discrete('opacity', [(0.0, 1), (t0, 0), (t0 + STEP - 0.2, 1)])
    a(f'<g>{on}<rect x="20" y="{y}" width="140" height="32" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.5"/>'
      + text(32, y + 21, feat, size=14, fill=INK, ls='0')
      + f'<path d="M 160 {y + 16} H 240" stroke="{GOLD}" stroke-width="1.6"/><circle cx="200" cy="{y + 16}" r="4" fill="{GOLD}"/>'
      + f'<rect x="240" y="{y}" width="140" height="32" rx="5" fill="none" stroke="{GREEN}" stroke-width="1.5"/>'
      + text(252, y + 21, abst, size=14, fill=INK, ls='0') + '</g>')
    # the same row with its feature taken away
    a(f'<g opacity="0">{vis([off])}<rect x="20" y="{y}" width="140" height="32" rx="5" fill="none" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 4"/>'
      + text(32, y + 21, feat, size=14, fill=MUTED, ls='0')
      + f'<path d="M 26 {y + 16} H 154" stroke="{RED}" stroke-width="2"/>'
      + f'<rect x="240" y="{y}" width="140" height="32" rx="5" fill="none" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 4"/>'
      + text(252, y + 21, abst, size=14, fill=MUTED, ls='0')+ '</g>')
    a(f'<g opacity="0">{vis([off])}' + text(20, 302, ['without the privilege bit:', 'without traps:', 'without the MMU:', 'without the timer:', 'without MMIO and DMA:'][k], size=14, fill=RED, ls='0')
      + text(20, 324, loss, size=14, fill=INK, ls='0') + '</g>')
a(f'<g opacity="0">{vis([(0.0, 1.6), (1.6 + STEP * len(ROWS) - 0.2, D)])}' + text(20, 302, 'take a feature away,', size=14, fill=MUTED, ls='0')
  + text(20, 324, 'and its abstraction goes with it', size=14, fill=MUTED, ls='0') + '</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each hardware feature on the left becomes, through the kernel, the abstraction on the right. Take the feature away and the '
           'abstraction goes with it: without the MMU there are no separate processes, and without the timer nothing can take the CPU '
           'from a program that never yields.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why the kernel.</b> Only code running with full privilege can program these features, so one program does it and every other program asks it through system calls.</li>
          <li><b>Not strictly one to one.</b> A process needs the MMU, traps and the timer together; each row shows the feature its abstraction cannot do without.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-9">
      <div class="diagram-label">Fig BR.9 · Hardware features → kernel → abstractions</div>
      {svg}
      <p id="chBridge-synthesis-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-9', 'chBridge-synthesis-p3', card)
