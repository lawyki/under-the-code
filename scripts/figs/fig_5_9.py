# Fig 5.9 · A NULL dereference, traced (Pass 28, law 3). Five stages down the stack, lit in turn as the
# fault travels: user code, MMU, kernel, signal, default action; the shell's message at the end.
# t=0: the whole chain, nothing lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

STAGES = [('user code', "*p = 'a';  with p == NULL", '#fff'),
          ('MMU', 'no page maps address 0: fault', GOLD),
          ('kernel', "0 is in none of the process's regions", GOLD),
          ('signal', 'SIGSEGV, number 11', RED),
          ('default action', 'terminate, dump core', RED)]
W = 400
CH, GAP, Y0 = 46, 14, 12
D = 9.0
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
ST = [0.6 + 1.0 * k for k in range(len(STAGES))]
o = []; a = o.append
body = []; b = body.append
for k, (who, what, col) in enumerate(STAGES):
    y = Y0 + k * (CH + GAP)
    b(f'<rect x="20" y="{y}" width="360" height="{CH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.35)"/>')
    b(f'<rect class="fx" x="20" y="{y}" width="360" height="{CH}" rx="3" fill="{col if col != "#fff" else PHOS}" fill-opacity="0.16" stroke="{col if col != "#fff" else PHOS}" stroke-width="2" opacity="0">{win(ST[k], ST[k] + 1.0)}</rect>')
    b(text(32, y + 18, who, size=13, fill=MUTED, ls='0'))
    b(text(32, y + 37, what, size=13, fill=col, ls='0'))
    if k < len(STAGES) - 1:
        ay = y + CH
        b(f'<line x1="200" y1="{ay + 1}" x2="200" y2="{ay + GAP - 3}" stroke="rgba(198,222,206,0.5)" stroke-width="1.5"/>')
        b(f'<polygon points="195,{ay + GAP - 7} 205,{ay + GAP - 7} 200,{ay + GAP - 1}" fill="rgba(198,222,206,0.5)"/>')
yt = Y0 + len(STAGES) * (CH + GAP) + 4
b(f'<rect x="20" y="{yt}" width="360" height="34" rx="3" fill="{PLATE}" stroke="rgba(198,222,206,0.3)"/>')
b(text(32, yt + 22, '$', size=13, fill=PHOS, ls='0'))
b(f'<g>{T.anim("opacity", [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (ST[-1] + 0.8 - 0.002, 0.0), (ST[-1] + 0.8, 1.0), (D, 1.0)])}'
  f'{text(48, yt + 22, "Segmentation fault (core dumped)", size=13, fill="#fff", ls="0")}</g>')
H = yt + 46
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-33 svgd-part2-33">')
a('<title id="svgt-part2-33">Fig 5.9 · A NULL dereference, traced</title>')
a("<desc id=\"svgd-part2-33\">User code writes through a NULL pointer: *p = 'a' with p equal to NULL. The MMU finds no page mapping address 0 and raises a page fault. "
  'The kernel\'s fault handler finds that address 0 lies in no region the process owns, so the access is illegal, and it sends the process SIGSEGV, signal number 11. '
  'The default action for that signal terminates the process and dumps core, and the shell prints Segmentation fault (core dumped).</desc>')
o.extend(body)
a('</svg>')
svg = '\n'.join(o)

caption = ("One write through NULL, followed from user code through the MMU, the kernel and the signal to the shell's message.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why address 0 faults.</b> Operating systems leave the lowest pages unmapped on purpose (Linux's <code>mmap_min_addr</code>), so a NULL access that reaches the processor traps instead of reading data.</li>
          <li><b>The same path.</b> This is the "invalid" exit of the page-fault tree in Fig 4.9; only the outcome differs from a minor fault.</li>
          <li><b>The core file.</b> "Core dumped" appears only when the system allows it; the dump is a snapshot of memory for a debugger to open.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-9">
      <div class="diagram-label">Fig 5.9 · A NULL dereference, traced</div>
      {svg}
      <p id="ch5-ub-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-9', 'ch5-ub-p6', card)
