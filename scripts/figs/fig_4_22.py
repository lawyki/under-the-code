# Fig 4.22 · eBPF and the verifier (Pass 28, law 3). Two programs go through bpf() into the verifier.
# "count packets" is proven to end and stay in bounds: JIT-compiled, attached, and it runs on each
# packet. "while (1) { }" cannot be proven to end: refused with EINVAL. t=0 (shift): both outcomes.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 330
D = 11.0
T = Timeline(D, shift=9.4)
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
o = []; a = o.append
LINE = 'rgba(198,222,206,0.3)'
def path(d, col, t0, t1):
    a(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    a(f'<path class="fx" d="{d}" fill="none" stroke="{col}" stroke-width="3" opacity="0">{lit(t0, t1)}</path>')
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-23 svgd-part2-23">')
a('<title id="svgt-part2-23">Fig 4.22 · eBPF: untrusted code in the kernel, made safe by proof</title>')
a('<desc id="svgd-part2-23">Two eBPF programs are submitted from user space with the bpf() system call. The kernel\'s verifier checks each one. '
  'The first, which counts packets, is proven to end and to stay within its memory bounds; it is compiled to native code and attached to the packet-arrival hook, where it runs once per packet. '
  'The second, an endless while loop, cannot be proven to end; the verifier refuses it with the error EINVAL and it never runs in the kernel.</desc>')
a(text(20, 20, 'USER SPACE', size=13, fill=MUTED))
for x, l1, l2 in ((20, 'prog A', 'count packets'), (210, 'prog B', 'while (1) { }')):
    a(f'<rect x="{x}" y="28" width="170" height="46" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.4)"/>')
    a(text(x + 12, 46, l1, size=13, fill=MUTED, ls='0'))
    a(text(x + 12, 65, l2, size=14, fill='#fff', ls='0'))
a(f'<line x1="20" y1="100" x2="380" y2="100" stroke="rgba(198,222,206,0.35)" stroke-dasharray="6 5"/>')
a(text(20, 95, 'bpf()', size=13, fill=PHOS_SOFT, ls='0'))
a(text(20, 118, 'KERNEL', size=13, fill=MUTED))
# verifier
VY = 126
a(f'<rect x="40" y="{VY}" width="320" height="50" rx="3" fill="{PLATE}" stroke="{GOLD}" stroke-width="1.5"/>')
a(text(200, VY + 20, 'verifier', anchor='middle', size=14, fill=GOLD, ls='0'))
V2 = [(None, 'proves: it ends, stays in bounds', PHOS_SOFT), ((1.6, 2.8), 'A: ends, in bounds: accept', PHOS), ((6.6, 7.8), 'B: no proof it ends: refuse', RED)]
for span, s, col in V2:
    if span is None:
        pts = [(0.0, 1.0), (1.6 - 0.008, 1.0), (1.6 - 0.005, 0.0), (2.8 - 0.002, 0.0), (2.8, 1.0), (6.6 - 0.008, 1.0), (6.6 - 0.005, 0.0), (7.8 - 0.002, 0.0), (7.8, 1.0), (D, 1.0)]
        a(f'<g>{T.anim("opacity", pts)}{text(200, VY + 40, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
    else:
        a(f'<g opacity="0">{lit(*span)}{text(200, VY + 40, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
for (t0, t1), col in (((1.6, 2.8), PHOS), ((6.6, 7.8), RED)):
    a(f'<rect class="fx" x="40" y="{VY}" width="320" height="50" rx="3" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-width="2" opacity="0">{lit(t0, t1)}</rect>')
path(f'M105 74 L105 {VY}', PHOS, 1.0, 2.8)
path(f'M295 74 L295 {VY}', RED, 6.0, 7.8)
# outcomes
OY = 214
path(f'M105 {VY + 50} L105 {OY}', PHOS, 2.8, 3.6)
path(f'M295 {VY + 50} L295 {OY}', RED, 7.8, 8.6)
a(f'<rect x="20" y="{OY}" width="170" height="46" rx="3" fill="{PANEL}" stroke="{PHOS}" stroke-opacity="0.7"/>')
a(text(32, OY + 19, 'JIT to native', size=13, fill=PHOS, ls='0'))
a(text(32, OY + 37, 'attached', size=13, fill=PHOS_SOFT, ls='0'))
a(f'<rect x="210" y="{OY}" width="170" height="46" rx="3" fill="{PANEL}" stroke="{RED}" stroke-opacity="0.7"/>')
a(text(222, OY + 19, 'refused: EINVAL', size=13, fill=RED, ls='0'))
a(text(222, OY + 37, 'never runs', size=13, fill=PHOS_SOFT, ls='0'))
for (x, t0), col in (((20, 2.8), PHOS), ((210, 7.8), RED)):
    a(f'<rect class="fx" x="{x}" y="{OY}" width="170" height="46" rx="3" fill="{col}" fill-opacity="0.15" stroke="{col}" stroke-width="2" opacity="0">{lit(t0, t0 + 0.8)}</rect>')
# the hook: A runs on each packet
HY = 290
a(text(20, HY + 4, 'packet in', size=13, fill=MUTED, ls='0'))
a(f'<line x1="104" y1="{HY}" x2="380" y2="{HY}" stroke="{LINE}" stroke-width="1.5"/>')
PKT = [3.6, 4.2, 4.8, 5.4]
for k, t in enumerate(PKT):
    x = 120 + k * 34
    a(f'<rect x="{x}" y="{HY - 7}" width="14" height="14" rx="2" fill="{PHOS}" fill-opacity="0.4" stroke="{PHOS}" opacity="0">{held(t)}</rect>')
    a(f'<circle class="fx" cx="{x + 7}" cy="{HY}" r="12" fill="none" stroke="{PHOS}" stroke-width="2" opacity="0">{lit(t, t + 0.35)}</circle>')
for k in range(len(PKT) + 1):
    t0 = 0.0 if k == 0 else PKT[k - 1]
    t1 = PKT[k] if k < len(PKT) else D
    if k == 0:
        pts = [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)]
    elif k == len(PKT):
        pts = [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)]
    else:
        pts = [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)]
    a(f'<g>{T.anim("opacity", pts)}{text(380, HY + 26, f"A ran {k}×", anchor="end", size=13, fill=PHOS, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Program A, a packet counter, is proven to end and stay in bounds, so it is compiled to native code and runs on every packet; program B, an endless loop, is refused and never runs.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The toolchain.</b> <code>clang</code> compiles restricted C to eBPF bytecode, and the <code>bpf()</code> system call hands it to the kernel.</li>
          <li><b>The proof.</b> The verifier walks every path through the program, tracking the range of every register. Loops pass only when it can bound them (allowed since Linux 5.3), and its effort is capped.</li>
          
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-22">
      <div class="diagram-label">Fig 4.22 · eBPF: untrusted code in the kernel, made safe by proof</div>
      {svg}
      <p id="ch4-security-p16" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-22', 'ch4-security-p16', card)
