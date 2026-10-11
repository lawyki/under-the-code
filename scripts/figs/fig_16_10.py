# Fig 16.10 · NUMA · two sockets, two memories, asymmetric latency (Pass 28, law 3). Quorum glass plate. Two sockets,
# each with four cores and its own memory, joined by an interconnect. Core 0 sends two reads on the same beat: one to
# its own memory, one to the other socket's, across the link. The local read is back while the remote one is still
# on its way; the remote round trip takes about 1.6 times as long here (platforms vary, typically 1.5 to 2).
# Phase-synced. t=0 (shift): both reads back, the gap marked.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
S0X, S1X, SW = 10, 214, 176
for x, name, col in ((S0X, 'socket 0', VIOLET), (S1X, 'socket 1', TEAL)):
    a(f'<rect x="{x}" y="10" width="{SW}" height="188" rx="12" fill="none" stroke="{col}" stroke-opacity="0.5"/>')
    a(text(x + 12, 30, name, anchor='start', size=13, fill=col, ls='0'))
    for k in range(4):
        cx = x + 12 + k * 40
        hl = (x == S0X and k == 0)
        a(f'<rect x="{cx}" y="42" width="34" height="34" rx="6" fill="{QCARD}" stroke="{col}" stroke-width="{2 if hl else 1}" stroke-opacity="{1 if hl else 0.6}"/>')
        a(text(cx + 17, 64, str(k + (0 if x == S0X else 4)), anchor='middle', size=13, fill=col if hl else QMUTED, ls='0'))
    a(f'<rect x="{x + 12}" y="130" width="{SW - 24}" height="52" rx="8" fill="{QCARD}" stroke="{QAMBER}" stroke-opacity="0.8"/>')
    a(text(x + SW / 2, 160, 'its memory', anchor='middle', size=13, fill=QAMBER, ls='0'))
a(f'<line x1="{S0X + SW}" y1="104" x2="{S1X}" y2="104" stroke="{QSOFT}" stroke-width="3" stroke-opacity="0.6"/>')
a(text(200, 92, 'link', anchor='middle', size=13, fill=QMUTED, ls='0'))
# the two reads: (path points, start, duration, colour)
C0 = (S0X + 29, 78)
LOCAL = [C0, (S0X + 29, 130), C0]
REMOTE = [C0, (S0X + 29, 104), (S1X + 60, 104), (S1X + 60, 130), (S1X + 60, 104), (S0X + 29, 104), C0]
T0, TL, TR = 1.2, 2.0, 3.2
def fly(pts, t0, dur, col):
    seg = [((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5 for i in range(len(pts) - 1)]
    tot = sum(seg); t, kx, ky = t0, [(0.0, 0.0), (t0, 0.0)], [(0.0, 0.0), (t0, 0.0)]
    for (x, y), L in zip(pts[1:], seg):
        t += dur * L / tot
        kx.append((t, x - pts[0][0])); ky.append((t, y - pts[0][1]))
    kx.append((D, 0.0)); ky.append((D, 0.0))
    a(f'<g class="fx" opacity="0">{lit(t0, t0 + dur + 0.01)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="6" fill="{col}"/></g></g></g>')
fly(LOCAL, T0, TL, VIOLET)
fly(REMOTE, T0, TR, TEAL)
# the clock: two bars that grow until each read returns
BY = 224
a(text(10, BY, 'round trip, from core 0', anchor='start', size=13, fill=QSOFT, ls='0'))
SC = 266 / TR
for k, (lab, dur, col) in enumerate((('local', TL, VIOLET), ('remote', TR, TEAL))):
    y = BY + 16 + k * 30
    a(text(10, y + 13, lab, anchor='start', size=13, fill=col, ls='0'))
    w = dur * SC
    a(f'<rect x="76" y="{y}" width="{w:.1f}" height="16" rx="3" fill="{col}" fill-opacity="0.85">'
      f'{T.anim("width", [(0.0, w), (0.3, w), (0.305, 0.0), (T0, 0.0), (T0 + dur, w), (D, w)])}</rect>')
a(f'<g opacity="0">{win(T0 + TR)}{text(390, BY + 16 + 30 + 13, "1.6×", anchor="end", size=13, fill=TEAL, ls="0")}</g>')
H = BY + 16 + 30 + 28
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-11 svgd-part5-11">')
o.insert(1, '<title id="svgt-part5-11">Fig 16.10 · NUMA · two sockets, two memories, asymmetric latency</title>')
o.insert(2, '<desc id="svgd-part5-11">Two processor sockets, each with four cores and its own memory, joined by a link. Core 0 sends two reads at the same moment: one to its own socket\'s memory, one across the link to the other socket\'s. The local read comes back first; the remote one takes about 1.6 times as long.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('In a two-socket server each socket has its own memory: a core reaches its own quickly and the other socket\'s only across the link, at roughly one and a half to two times the delay. '
           'The program sees one flat memory; only the clock shows where the data lives.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The link.</b> Intel calls it UPI, AMD Infinity Fabric; the ratio of remote to local delay depends on the platform.</li>
          <li><b>Keeping data near.</b> The operating system tries to run a thread on the socket that holds its memory and to allocate new memory there (first touch); <code>numactl</code> lets a program choose.</li>
          <li><b>When it bites.</b> A thread that drifts to the other socket, or one big allocation on the wrong node, can slow a program sharply while its results stay correct.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-10">
      <div class="diagram-label">Fig 16.10 · NUMA · two sockets, two memories, asymmetric latency</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-10"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-10', cap, card.replace('CAPID', cap))
