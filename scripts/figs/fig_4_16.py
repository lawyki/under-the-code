# Fig 4.16 · The UNIX philosophy, in five processes (Pass 28, law 3). A vertical pipeline with real
# log lines: cat streams them, grep passes ERROR lines as they arrive, sort waits for the end of
# input and then emits all at once, uniq drops the repeat, wc prints 2. t=0 (shift): all outputs.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, MUTED
figlib.FONT = PLEX

LOG = ['INFO start', 'ERROR disk', 'ERROR net', 'WARN cpu', 'ERROR disk']
CAT_T = [0.6 + 0.5 * i for i in range(len(LOG))]
EOF_T = CAT_T[-1] + 0.4
GREP = [(l, t + 0.25) for l, t in zip(LOG, CAT_T) if l.startswith('ERROR')]
SORT = [(l, EOF_T + 0.5) for l in sorted(l for l, _ in GREP)]
UNIQ, last = [], None
for i, (l, t) in enumerate(SORT):
    if l != last: UNIQ.append((l, t + 0.4 + 0.25 * len(UNIQ)))
    last = l
WC = [(str(len(UNIQ)), UNIQ[-1][1] + 0.6)]
STAGES = [('cat server.log', 'read the file', [(l, t) for l, t in zip(LOG, CAT_T)]),
          ('grep ^ERROR', 'keep matches', GREP),
          ('sort', 'waits for end', SORT),
          ('uniq', 'drop repeats', UNIQ),
          ('wc -l', 'count', WC)]
W = 400
BX, BW, BH = 20, 140, 46
LX, LW, LH, PAD, GAP = 176, 204, 18, 8, 24
D = 8.0
T = Timeline(D, shift=7.4)
def on_from(t):
    return T.anim('opacity', [(0.0, 0.0), (t - 0.002, 0.0), (t, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
def lit(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
body = []
y = 12
tops = []
for k, (cmd, job, outs) in enumerate(STAGES):
    rh = max(BH, len(outs) * LH + 2 * PAD)
    tops.append((y, rh))
    body.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
    body.append(text(BX + 10, y + 19, cmd, size=14, fill='#fff', ls='0'))
    body.append(text(BX + 10, y + 37, job, size=13, fill=GOLD if cmd == 'sort' else MUTED, ls='0'))
    body.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{rh}" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.18)"/>')
    body.append(f'<line x1="{BX + BW}" y1="{y + BH / 2}" x2="{LX}" y2="{y + BH / 2}" stroke="rgba(132,255,178,0.55)" stroke-width="1.2"/>')
    for i, (l, t) in enumerate(outs):
        col = PHOS if (l.startswith('ERROR') or l.isdigit()) else 'rgba(198,222,206,0.6)'
        body.append(f'<g>{on_from(t)}{text(LX + 12, y + PAD + 13 + i * LH, l, size=13 if not l.isdigit() else 15, fill=col, ls="0")}</g>')
    if k < len(STAGES) - 1:
        py0, py1 = y + BH, y + rh + GAP
        body.append(f'<line x1="{BX + 30}" y1="{py0}" x2="{BX + 30}" y2="{py1 - 2}" stroke="rgba(132,255,178,0.5)" stroke-width="2"/>')
        body.append(f'<polygon points="{BX + 25},{py1 - 8} {BX + 35},{py1 - 8} {BX + 30},{py1}" fill="rgba(132,255,178,0.5)"/>')
        body.append(text(BX + 40, (py0 + py1) / 2 + 5, 'pipe', size=13, fill='rgba(132,255,178,0.6)', ls='0'))
        # each item crossing the pipe lights it
        for l, t in outs:
            body.append(f'<line class="fx" x1="{BX + 30}" y1="{py0}" x2="{BX + 30}" y2="{py1 - 2}" stroke="{PHOS}" stroke-width="3.5" opacity="0">{lit(t, t + 0.22)}</line>')
    y += rh + GAP
H = y - GAP + 12
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-17 svgd-part2-17">')
a('<title id="svgt-part2-17">Fig 4.16 · The UNIX philosophy, in five processes</title>')
a('<desc id="svgd-part2-17">Five processes joined by pipes: cat server.log, grep ^ERROR, sort, uniq, wc -l. cat streams five log lines; grep passes the three ERROR lines as each arrives; '
  'sort must wait until its input ends and then prints all three in order; uniq drops the repeated "ERROR disk"; wc -l prints 2.</desc>')
o.extend(body)
a('</svg>')
svg = '\n'.join(o)

caption = ('Five small programs joined by four pipes run at once, each reading standard input and writing standard output with no idea what is on the other end. Lines stream through as they arrive, except at <code>sort</code>, which must see the last line before it can print the first.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The wiring.</b> The shell calls <code>pipe()</code> four times and <code>fork()</code> five, then points each program's standard output at the next one's standard input.</li>
          <li><b>Streaming.</b> <code>grep</code> and <code>uniq</code> work a line at a time; <code>sort</code> and <code>wc</code> must reach the end of their input before they can answer.</li>
          
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-16">
      <div class="diagram-label">Fig 4.16 · The UNIX philosophy, in five processes</div>
      {svg}
      <p id="ch4-ipc-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print('H', H, 'wc at', WC[0][1])
    splice('part-2', 'fig-4-16', 'ch4-ipc-p7', card)
