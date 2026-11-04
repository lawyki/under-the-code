# Fig BR.1 · The privilege bit (Pass 31, Part I, from an empty script). Job: function. Takeaway: the CPU checks a
# privilege bit, so in Ring 3 a privileged instruction never runs; the kernel takes over.
# Concept: the check as a gate on the instruction path, the bit (CS's low two bits, the CPL) shown on it. The same three
# instructions go through it twice, in two lanes at once (Part I's step verb): in Ring 0 (CPL 00) all three pass and
# run; in Ring 3 (CPL 11) add passes, and the two privileged ones stop dead at the gate with #GP while the CPU jumps to
# the handler the kernel registered. t=0 is the end: every instruction where it finished.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 352
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 10.0
T = Timeline(D, shift=8.4)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
INS = [('add rax, rbx', False), ('mov cr3, rax', True), ('hlt', True)]
PW, X_START, X_END, GX = 122, 18, 246, 172          # pill width, start x, end x, gate x
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-br-1 svgd-part1-br-1">')
a('<title id="svgt-part1-br-1">Fig BR.1 · The privilege bit · two worlds, one chip</title>')
a('<desc id="svgd-part1-br-1">The low two bits of the CS register hold the current privilege level: 00 in Ring 0, the kernel, and 11 in '
  'Ring 3, user programs. The CPU checks it on every instruction, drawn as a gate. The same three instructions go through in each '
  'ring. add runs in both. mov cr3, which changes the page tables, and hlt, which halts the processor, run in Ring 0; in Ring 3 the '
  'CPU stops each at the gate with a general-protection fault, #GP, and jumps to a handler the kernel registered in advance.</desc>')

def lane(y0, ring, cpl, col, user):
    a(text(18, y0 - 14, ring, size=14, fill=col))
    # the gate, with the bit on it
    a(f'<line x1="{GX}" y1="{y0 - 4}" x2="{GX}" y2="{y0 + 92}" stroke="{col}" stroke-width="3"/>')
    a(f'<rect x="{GX + 8}" y="{y0 - 30}" width="64" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.6"/>')
    a(text(GX + 40, y0 - 13, f'CPL {cpl}', anchor='middle', size=14, fill=col, ls='0', role='object'))
    for k, (ins, priv) in enumerate(INS):
        y = y0 + k * 32
        t0 = 1.0 + 2.0 * k
        stop = user and priv
        x1 = GX - PW - 6 if stop else X_END
        xs = [(0.0, 0), (t0, 0), (t0 + 0.8, x1 - X_START), (D - 0.3, x1 - X_START), (D - 0.01, 0)]
        base_vis = f' opacity="0">{vis([(0.0, t0 + 0.8), (D - 0.3, D)])}</rect>' if stop else '/>'
        body = (f'<rect x="{X_START}" y="{y}" width="{PW}" height="26" rx="5" fill="none" stroke="{EDGE}" stroke-width="1.4"{base_vis}'
                + text(X_START + 10, y + 18, ins, size=14, fill=INK, ls='0', role='object'))
        if stop:
            body += (f'<rect x="{X_START}" y="{y}" width="{PW}" height="26" rx="5" fill="none" stroke="{RED}" stroke-width="2.2" opacity="0">'
                     f'{vis([(t0 + 0.8, D - 0.3)])}</rect>')
        a(f'<g>{T.translate(xs, axis="x")}{body}</g>')
        if stop:
            a(f'<g opacity="0">{vis([(t0 + 0.8, D - 0.3)])}' + text(GX + 10, y + 18, '#GP', size=14, fill=RED, ls='0') + '</g>')
            # the CPU jumps to the kernel's handler
            a(f'<path d="M {GX + 46} {y + 13} H 300 V 300" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 4" opacity="0">{vis([(t0 + 0.9, D - 0.3)])}</path>')
        else:
            a(f'<g opacity="0">{vis([(t0 + 0.8, D - 0.3)])}<path d="M {X_END + PW + 6} {y + 13} l 4 5 l 8 -10" fill="none" stroke="{GREEN}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')
lane(46, 'Ring 0 · kernel', '00', GOLD, False)
lane(186, 'Ring 3 · user', '11', BLUE, True)
a(f'<rect x="216" y="300" width="168" height="34" rx="6" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
a(text(300, 322, "kernel's handler", anchor='middle', size=14, fill=GOLD))
a('</svg>')
svg = '\n'.join(o)

caption = ('The same three instructions in each ring: <code>add</code> runs in both, while in Ring 3 the two privileged ones stop at '
           '<code>#GP</code> and the CPU jumps to the handler the kernel registered.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>CPL.</b> The current privilege level, held in the low two bits of CS: 00 for the kernel, 11 for user programs. The CPU checks it on every instruction.</li>
          <li><b>Privileged.</b> Instructions that would let a program step past the operating system: loading the page tables (mov cr3), the interrupt table (lidt), model-specific registers, I/O ports, halting the CPU.</li>
          <li><b>#GP.</b> A general-protection fault. The instruction does not run and the program gets no result; the CPU jumps to the handler the kernel set up, and the kernel decides what happens to the program.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-1">
      <div class="diagram-label">Fig BR.1 · The privilege bit · two worlds, one chip</div>
      {svg}
      <p id="chBridge-mode-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-1', 'chBridge-mode-p5', card)
