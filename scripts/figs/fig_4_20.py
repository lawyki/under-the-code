# Fig 4.20 · Namespaces (Pass 28, law 3). One panel of five questions; the viewpoint steps from
# container A to container B to the host, and the one kernel's answers change with it.
# t=0: seen from container A.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 300
D = 9.0
T = Timeline(D, shift=0.0)
VIEWS = ['container A', 'container B', 'host']
SPAN = [(0.0, 3.0), (3.0, 6.0), (6.0, D)]
ROWS = [('PID 1 is', ['redis', 'nginx', 'systemd']),
        ('redis is PID', ['1', 'not visible', '8472']),
        ('hostname', ['redis-host', 'web-host', 'prod-01']),
        ('eth0', ['10.0.0.2', '10.0.0.3', '192.168.1.10']),
        ('/ is', ['redis image', 'nginx image', 'host disk'])]
def during(k):
    t0, t1 = SPAN[k]
    if t0 == 0.0:
        return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D - 0.008, 0.0), (D - 0.005, 1.0)])
    if t1 == D:
        return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D - 0.008, 1.0), (D - 0.005, 0.0)])
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-21 svgd-part2-21">')
a('<title id="svgt-part2-21">Fig 4.20 · Namespaces: each container sees its own world</title>')
a('<desc id="svgd-part2-21">Five questions asked from three places on one machine. From container A: PID 1 is redis, redis is PID 1, the hostname is redis-host, eth0 is 10.0.0.2 and the root filesystem is the redis image. '
  'From container B: PID 1 is nginx, redis is not visible at all, the hostname is web-host, eth0 is 10.0.0.3 and the root is the nginx image. '
  'From the host: PID 1 is systemd, redis is process 8472, the hostname is prod-01, eth0 is 192.168.1.10 and the root is the host disk. One kernel gives all three answers.</desc>')
TW = 116
for k, v in enumerate(VIEWS):
    x = 20 + k * (TW + 6)
    a(f'<rect x="{x}" y="14" width="{TW}" height="34" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.3)"/>')
    a(text(x + TW / 2, 36, v, anchor='middle', size=13, fill=MUTED, ls='0'))
    a(f'<g>{during(k)}<rect x="{x}" y="14" width="{TW}" height="34" rx="3" fill="{PHOS}" fill-opacity="0.22" stroke="{PHOS}" stroke-width="2"/>'
      f'{text(x + TW / 2, 36, v, anchor="middle", size=13, fill="#fff", ls="0")}</g>')
a(f'<rect x="20" y="58" width="360" height="{len(ROWS) * 34 + 8}" rx="3" fill="{PLATE}" stroke="rgba(132,255,178,0.25)"/>')
for r, (q, ans) in enumerate(ROWS):
    y = 66 + r * 34
    if r: a(f'<line x1="30" y1="{y - 2}" x2="370" y2="{y - 2}" stroke="rgba(132,255,178,0.1)"/>')
    a(text(34, y + 21, q, size=13, fill=MUTED, ls='0'))
    for k, v in enumerate(ans):
        col = RED if v == 'not visible' else (GOLD if k == 2 else PHOS)
        a(f'<g>{during(k)}{text(176, y + 21, v, size=14, fill=col, ls="0")}</g>')
yk = 66 + len(ROWS) * 34 + 16
a(f'<rect x="20" y="{yk}" width="360" height="32" rx="3" fill="{PANEL}" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(text(200, yk + 21, 'one kernel answers all three', anchor='middle', size=13, fill=GOLD, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ("Ask the same five questions from inside container A, inside B and on the host, and one kernel gives three sets of answers: each container sees its own PID 1, hostname, network and root filesystem. A PID namespace is a translation table, not a copy: to the host, A's PID 1 is just process 8472.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Eight kinds.</b> Mount, UTS (hostname), IPC, PID, network, user, cgroup and, since Linux 5.6, time. Each can be set separately.</li>
          <li><b>Making one.</b> <code>clone()</code> with a flag such as <code>CLONE_NEWPID</code> starts a new process in a fresh namespace; <code>unshare()</code> moves the caller itself into one (for PID, only its next children). Children inherit the namespace.</li>
          <li><b>The network.</b> A container's network namespace gets its own virtual network card, joined by a virtual cable to the host, which passes its traffic on. Part III opens up networking.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-20">
      <div class="diagram-label">Fig 4.20 · Namespaces: each container sees its own world</div>
      {svg}
      <p id="ch4-security-p12" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-20', 'ch4-security-p12', card)
