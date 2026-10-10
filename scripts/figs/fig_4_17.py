# Fig 4.17 · A signal arrives mid-execution (Pass 28, law 3). Three lanes, a time cursor.
# Run 1: Ctrl+C marks SIGINT pending; main runs on to its next kernel return, is diverted into its
# handler, and sigreturn resumes it. Run 2: SIGKILL; the kernel ends the process, no handler runs.
# t=0 (shift): run 1 drawn complete.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 236
X0, X1 = 90, 384
LANES = {'main': 70, 'kernel': 130, 'handler': 190}
BH = 24
D = 13.0
T = Timeline(D, shift=6.5)
E1, E1_END = 1.0, 6.0
E2 = 7.2
def tx(x, start):  # story time at which the cursor reaches x
    return start + (x - X0) / (X1 - X0) * (E1_END - E1)
def vis(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
def bar(x0, x1, lane, col, start, label=None, op=0.35):
    y = LANES[lane] - BH / 2
    w = x1 - x0
    t0, t1 = tx(x0, start), tx(x1, start)
    a(f'<rect x="{x0}" y="{y}" width="{w}" height="{BH}" rx="2" fill="{col}" fill-opacity="{op}" stroke="{col}">'
      f'{T.anim("width", [(0.0, 0.0), (t0, 0.0), (t1, w), (D, w)])}</rect>')
    if label:
        a(f'<g>{T.anim("opacity", [(0.0, 0.0), (t1 - 0.002, 0.0), (t1, 1.0), (D, 1.0)])}{text((x0 + x1) / 2, LANES[lane] + 5, label, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
def link(x, l0, l1, col, start):
    t = tx(x, start)
    y0, y1 = LANES[l0] + (BH / 2 if LANES[l1] > LANES[l0] else -BH / 2), LANES[l1] + (-BH / 2 if LANES[l1] > LANES[l0] else BH / 2)
    a(f'<g>{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])}<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{col}" stroke-width="1.5" stroke-dasharray="3 3"/></g>')
def bolt(x, start, name, col):
    t = tx(x, start)
    a(f'<g>{T.anim("opacity", [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (D, 1.0)])}'
      f'<path d="M{x + 5} 26 L{x - 3} {LANES["kernel"] - 22} L{x + 3} {LANES["kernel"] - 22} L{x - 2} {LANES["kernel"] - 4}" fill="none" stroke="{col}" stroke-width="2"/>'
      f'{text(x + 10, 30, name, size=13, fill=col, ls="0")}</g>')

a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-18 svgd-part2-18">')
a('<title id="svgt-part2-18">Fig 4.17 · A signal arrives mid-execution</title>')
a('<desc id="svgd-part2-18">Three lanes over time: the program\'s main code, the kernel, and the program\'s signal handler. Pressing Ctrl+C makes the kernel mark SIGINT as pending; '
  'the program keeps running until its next return from the kernel, where the kernel diverts it into the handler; when the handler returns, a sigreturn call restores the saved state and main resumes where it stopped. '
  'In a second run SIGKILL arrives instead: the kernel ends the process at once, and the handler never runs.</desc>')
for name, y in LANES.items():
    a(text(20, y + 5, name, size=13, fill=MUTED, ls='0'))
    a(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="rgba(132,255,178,0.14)" stroke-width="1"/>')
# run 1
a(f'<g>{vis(0.3, 6.9)}')
bar(X0, 206, 'main', PHOS, E1)
bolt(150, E1, 'Ctrl+C', GOLD)
pt = tx(150, E1)
a(f'<g>{T.anim("opacity", [(0.0, 0.0), (pt - 0.002, 0.0), (pt, 1.0), (D, 1.0)])}'
  f'<rect x="{146}" y="{LANES["kernel"] - 6}" width="12" height="12" fill="{GOLD}" transform="rotate(45 152 {LANES["kernel"]})"/>'
  f'{text(138, LANES["kernel"] + 5, "pending", anchor="end", size=13, fill=GOLD, ls="0")}</g>')
link(206, 'main', 'kernel', PHOS_SOFT, E1)
bar(206, 222, 'kernel', PHOS_SOFT, E1, op=0.5)
link(222, 'kernel', 'handler', PHOS_SOFT, E1)
bar(222, 300, 'handler', GOLD, E1, 'handler')
link(300, 'handler', 'kernel', PHOS_SOFT, E1)
bar(300, 316, 'kernel', PHOS_SOFT, E1, op=0.5)
link(316, 'kernel', 'main', PHOS_SOFT, E1)
bar(316, X1, 'main', PHOS, E1)
a(f'<g>{T.anim("opacity", [(0.0, 0.0), (tx(316, E1) - 0.002, 0.0), (tx(316, E1), 1.0), (D, 1.0)])}{text(324, LANES["kernel"] + 5, "sigreturn", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a('</g>')
# run 2
a(f'<g opacity="0">{vis(7.0, 12.8)}')
bar(X0, 200, 'main', PHOS, E2)
bolt(156, E2, 'SIGKILL', RED)
link(200, 'main', 'kernel', RED, E2)
bar(200, 216, 'kernel', RED, E2, op=0.5)
tk = tx(216, E2)
a(f'<g>{T.anim("opacity", [(0.0, 0.0), (tk - 0.002, 0.0), (tk, 1.0), (D, 1.0)])}'
  f'{text(226, LANES["kernel"] + 5, "process ended", size=13, fill=RED, ls="0")}'
  f'{text(234, LANES["handler"] + 5, "never runs", size=13, fill="rgba(198,222,206,0.6)", ls="0")}</g>')
a('</g>')
# cursor
for s0, x_end in ((E1, X1), (E2, 216)):
    t0, t1 = tx(X0, s0), tx(x_end, s0)
    a(f'<line y1="{LANES["main"] - 22}" y2="{LANES["handler"] + 18}" stroke="#fff" stroke-width="1.2" opacity="0">'
      f'{T.anim("x1", [(0.0, X0), (t0, X0), (t1, x_end), (D, x_end)])}{T.anim("x2", [(0.0, X0), (t0, X0), (t1, x_end), (D, x_end)])}'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 0.6), (t1, 0.6), (t1 + 0.1, 0.0), (D, 0.0)])}</line>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Ctrl+C makes the kernel mark SIGINT pending; the program runs on until its next return from the kernel, where it is diverted into its handler and then resumed where it stopped. '
           'SIGKILL never reaches the program: the kernel ends the process without running any of its code.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Three reactions.</b> A process can handle a signal with its own function, ignore it, or take the default action: terminate, stop, or nothing.</li>
          <li><b>Uncatchable.</b> <code>SIGKILL</code> and <code>SIGSTOP</code> can be neither handled nor ignored, so an administrator can always stop a process that has trapped everything else.</li>
          <li><b>Crude by design.</b> A signal is just a number. A second signal of the same kind arriving while the first is still pending merges with it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-17">
      <div class="diagram-label">Fig 4.17 · A signal arrives mid-execution</div>
      {svg}
      <p id="ch4-ipc-p10" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-17', 'ch4-ipc-p10', card)
