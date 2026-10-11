# Fig 17.4 · The reconcile loop · observe, diff, act, repeat (Pass 28, law 3). Quorum glass plate. Desired: 3 replicas.
# A loop of observe → diff → act runs round and round. A pod crashes, the next observe sees 2, the diff is +1, the act
# starts a new pod, and the next pass finds 3 = 3 and does nothing. Phase-synced: the loop marker steps on fixed beats.
# t=0 (shift): back at 3, the loop idling.
import math
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 12.0
T = Timeline(D, shift=11.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# the loop: three stations on a circle
CX, CY, R = 110, 130, 74
ST = [('observe', -90), ('diff', 30), ('act', 150)]
pos = lambda ang: (CX + R * math.cos(math.radians(ang)), CY + R * math.sin(math.radians(ang)))
a(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{VIOLET}" stroke-opacity="0.4" stroke-width="2"/>')
for lab, ang in ST:
    x, y = pos(ang)
    a(f'<rect x="{x - 36}" y="{y - 13}" width="72" height="26" rx="13" fill="{QCARD}" stroke="{VIOLET}" stroke-width="1.5"/>')
    a(text(x, y + 5, lab, anchor='middle', size=13, fill=VIOLET, ls='0'))
# the cluster on the right
a(text(232, 32, 'desired: 3', anchor='start', size=13, fill=QAMBER, ls='0'))
PX = [244, 292, 340]
PY = 60
TCRASH, TOBS, TDIFF, TACT, TOBS2 = 1.6, 3.0, 4.2, 5.4, 6.8
for k, x in enumerate(PX):
    a(f'<rect x="{x - 18}" y="{PY}" width="36" height="36" rx="7" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="0.5"/>')
    if k == 2:
        a(f'<g opacity="0">{first(TCRASH)}<rect x="{x - 14}" y="{PY + 4}" width="28" height="28" rx="5" fill="{TEAL}" fill-opacity="0.85"/></g>')
        a(f'<g opacity="0">{lit(TCRASH, TACT)}<path d="M{x - 10},{PY + 8} l20,20 M{x + 10},{PY + 8} l-20,20" stroke="{QROSE}" stroke-width="3"/></g>')
        a(f'<g opacity="0">{win(TACT)}<rect x="{x - 14}" y="{PY + 4}" width="28" height="28" rx="5" fill="{TEAL}" fill-opacity="0.85"/></g>')
        a(f'<g class="fx" opacity="0">{pulse(TACT)}<rect x="{x - 20}" y="{PY - 2}" width="40" height="40" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
    else:
        a(f'<rect x="{x - 14}" y="{PY + 4}" width="28" height="28" rx="5" fill="{TEAL}" fill-opacity="0.85"/>')
a(text(232, PY + 60, 'actual:', anchor='start', size=13, fill=QSOFT, ls='0'))
for t0, t1, s, col in ((0.31, TCRASH, '3', TEAL), (TCRASH, TACT, '2', QROSE), (TACT, None, '3', TEAL)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(300, PY + 60, s, anchor="start", size=13, fill=col, ls="0")}</g>')
# what each station says on this pass
SY = PY + 104
for t0, t1, s, col in ((0.31, TCRASH, 'idle: 3 = 3, nothing to do', QMUTED), (TCRASH, TOBS, 'a pod crashes', QROSE),
                       (TOBS, TDIFF, 'observe: 2 running', VIOLET), (TDIFF, TACT, 'diff: want 3, have 2: +1', VIOLET),
                       (TACT, TOBS2, 'act: start one pod', TEAL), (TOBS2, None, 'next pass: 3 = 3, nothing to do', QMUTED)):
    vis = first(t1) if t0 < 0.5 else (win(t0) if t1 is None else lit(t0, t1))
    a(f'<g opacity="0">{vis}{text(232, SY, s.split(": ", 1)[0] + (":" if ": " in s else ""), anchor="start", size=13, fill=col, ls="0")}'
      f'{text(232, SY + 18, s.split(": ", 1)[1] if ": " in s else "", anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
# the marker going round, stopping at each station on its beat
def ang_at(ang): return pos(ang)
mk = [(0.0, -90), (TOBS, -90), (TDIFF, 30), (TACT, 150), (TOBS2, 270), (D, 270)]
ox, oy = pos(-90)
kx, ky = [], []
for t, ang in mk:
    x, y = pos(ang)
    kx.append((t, x - ox)); ky.append((t, y - oy))
a(f'<g class="fx"><g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{ox:.1f}" cy="{oy - 22:.1f}" r="5" fill="#fff"/></g></g></g>')
H = int(max(SY + 30, CY + R + 14))
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-17 svgd-part5-17">')
o.insert(1, '<title id="svgt-part5-17">Fig 17.4 · The reconcile loop · observe, diff, act, repeat</title>')
o.insert(2, '<desc id="svgd-part5-17">A controller loops through observe, diff and act. The desired state is three replicas, and three pods are running. One pod crashes. On the next pass the controller observes two running, the difference is one, and it starts a new pod. The pass after finds three of three and does nothing.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A controller compares what was asked for with what is running and takes one step to close the gap, again and again. '
           'When a pod crashes the next pass sees two of three and starts one; the pass after sees nothing to do.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Level, not edge.</b> The controller acts on the current difference, not on remembered events, so a missed crash or a failed start is simply caught on the next pass.</li>
          <li><b>Idempotent.</b> A pass with nothing to fix changes nothing, so running the loop often is safe.</li>
          <li><b>Elsewhere.</b> Argo CD and Flux run the same loop over a Git repository; Terraform and Pulumi declare state too, but converge only when someone runs a plan and applies it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-4">
      <div class="diagram-label">Fig 17.4 · The reconcile loop · observe, diff, act, repeat</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-4"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-4', cap, card.replace('CAPID', cap))
