# Fig 4.6 · Little's Law and the cliff (Pass 28, law 3). For the simplest queue (M/M/1, service time 1):
# W = 1/(1 − ρ) and L = λW = ρ/(1 − ρ). Three loads in turn: 50% (L 1, W 2), 80% (L 4, W 5),
# 95% (L 19, W 20). The queue grows to match; a marker rides the curve. t=0: 95%.
# (The old caption said doubling the load at 50% "barely budges" the wait; doubling 50% is 100%.)
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, GOLD, MUTED
figlib.FONT = PLEX

W, H = 400, 400
LOADS = [0.5, 0.8, 0.95]
SPAN = 2.6
T = Timeline(SPAN * 3, shift=SPAN * 2 + 1.3)
D = SPAN * 3
def win(t0, t1):
    if t0 <= 0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D - 0.0005, 0.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (D - 0.0005, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-6 svgd-part2-6">')
a('<title id="svgt-part2-6">Fig 4.6 · Little\'s Law and the cliff at full utilisation</title>')
a('<desc id="svgd-part2-6">A queue in front of one server, at three loads. At 50% utilisation one request is in the system on average, waiting or being served, and each spends twice the service time there. '
  'At 80%, four are in the system and the time is five times the service time. At 95%, nineteen are in it and the time is twenty times. Below, the curve W = 1/(1 − ρ) climbs steeply toward 100%. Little\'s Law, L = λW, links the three numbers.</desc>')
# the queue and the server
a(text(20, 24, 'QUEUE → SERVER', size=13, fill=MUTED))
a(f'<rect x="334" y="36" width="46" height="46" rx="6" fill="{PANEL}" stroke="{PHOS}" stroke-width="1.8"/>')
a(f'<circle cx="357" cy="59" r="9" fill="{PHOS}"/>')
for k, rho in enumerate(LOADS):
    L = round(rho / (1 - rho)); Wt = round(1 / (1 - rho))
    t0, t1 = k * SPAN, (k + 1) * SPAN
    g = [f'<g opacity="0">{win(t0, t1)}']
    for i in range(L - 1):          # L counts the one in service too: L - 1 wait in line
        row, col = divmod(i, 10)
        x = 314 - col * 30 - (0 if row == 0 else 0)
        y = 48 + row * 30 if row == 0 else 84
        if row == 1: x = 314 - col * 30
        g.append(f'<rect x="{x}" y="{y if row == 0 else 84}" width="22" height="22" rx="3" fill="{GOLD}" fill-opacity="0.45" stroke="{GOLD}"/>')
    g.append(f'<text x="20" y="140" {PLEX} font-size="15" fill="#fff">ρ = {int(rho * 100)}%</text>')
    g.append(f'<text x="200" y="140" text-anchor="middle" {PLEX} font-size="15" fill="{GOLD}">L = {L}</text>')
    g.append(f'<text x="380" y="140" text-anchor="end" {PLEX} font-size="15" fill="{PHOS}">W = {Wt}</text>')
    g.append('</g>'); a(''.join(g))
# the curve W = 1/(1 − ρ), capped at 20 (ρ = 0.95)
X0, X1, Y0, Y1 = 64, 380, 352, 176
X = lambda r: X0 + r * (X1 - X0)
Y = lambda w: Y0 - w / 20 * (Y0 - Y1)
pts = [(r / 100, 1 / (1 - r / 100)) for r in range(0, 96)]
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="rgba(132,255,178,0.35)"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 6}" stroke="rgba(132,255,178,0.35)"/>')
a('<polyline points="' + ' '.join(f'{X(r):.1f},{Y(w):.1f}' for r, w in pts) + f'" fill="none" stroke="{PHOS}" stroke-width="2.4"/>')
a(f'<line x1="{X(1)}" y1="{Y1 - 6}" x2="{X(1)}" y2="{Y0}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
for w in (5, 20):
    a(text(X0 - 8, Y(w) + 5, str(w), anchor='end', size=13, fill=MUTED, ls='0'))
for r, lab in ((0, '0'), (0.5, '50%'), (0.8, '80%')):
    a(text(X(r), Y0 + 20, lab, anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(X(1), Y0 + 20, '100%', anchor='end', size=13, fill=MUTED, ls='0'))
a(text(X0 + 8, Y1 + 8, 'W = 1/(1 − ρ)', size=14, fill=PHOS, ls='0'))
a(text(X0, 394, 'utilisation ρ', size=13, fill='rgba(198,222,206,0.6)', ls='0'))
for k, rho in enumerate(LOADS):
    t0, t1 = k * SPAN, (k + 1) * SPAN
    a(f'<circle cx="{X(rho):.1f}" cy="{Y(1 / (1 - rho)):.1f}" r="5" fill="{GOLD}" fill-opacity="0.5"/>')
    a(f'<circle cx="{X(rho):.1f}" cy="{Y(1 / (1 - rho)):.1f}" r="8" fill="{GOLD}" stroke="{PLATE}" stroke-width="2" opacity="0">{win(t0, t1)}</circle>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Little\'s Law ties a queue\'s length to its arrival rate and wait: L = λW, for any stable queue. '
           'As utilisation nears 100% the time in the system grows like <span style="white-space:nowrap">1/(1 − ρ)</span>: five times the bare service time at 80% load, twenty times at 95%.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The law.</b> Average number in the system = arrival rate × average time in it. It needs no assumption about how arrivals or service times are distributed.</li>
          <li><b>The curve.</b> For the simplest queue (random arrivals, one server, called M/M/1) the time in the system is the service time divided by 1 − ρ.</li>
          <li><b>The cliff.</b> From 50% to 60% load the time in the system grows by a quarter; from 90% to 95% it doubles; at 100% (the dashed line) the queue never drains. That is why operators worry once a server stays above about 80%.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-6">
      <div class="diagram-label">Fig 4.6 · Little's Law and the cliff at full utilisation</div>
      {svg}
      <p id="ch4-scheduling-p11" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-6', 'ch4-scheduling-p11', card)
