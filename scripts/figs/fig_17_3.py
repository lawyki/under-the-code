# Fig 17.3 · Kubernetes architecture · control plane + workers (Pass 28, law 3). Quorum glass plate. One request
# traced: kubectl apply sends a pod to the API server, which stores it in etcd; the scheduler, watching the API server,
# picks node 2 and records it; node 2's kubelet, also watching, starts the pod. Every component talks only to the API
# server. The token's hops light each component in turn. t=0 (shift): the pod running on node 2.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

W = 400
D = 11.0
T = Timeline(D, shift=10.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
BOX = {'user': (10, 10, 120, 34, 'kubectl apply', QSOFT), 'api': (140, 72, 120, 40, 'API server', VIOLET),
       'etcd': (14, 72, 104, 40, 'etcd', QAMBER), 'sched': (282, 72, 104, 40, 'scheduler', VIOLET),
       'ctrl': (140, 126, 120, 34, 'controllers', VIOLET)}
NODES = [(14, 'node 1'), (144, 'node 2'), (274, 'node 3')]
NY = 206
a(f'<rect x="6" y="62" width="388" height="106" rx="12" fill="none" stroke="{VIOLET}" stroke-opacity="0.35"/>')
a(text(390, 182, 'control plane', anchor='end', size=13, fill=VIOLET, ls='0'))
for x, lab in NODES:
    a(f'<line x1="{x + 56}" y1="{NY}" x2="200" y2="112" stroke="{QMUTED}" stroke-opacity="0.25"/>')
for key in ('etcd', 'sched', 'ctrl'):
    x, y, w, h = BOX[key][:4]
    cx, cy = x + w / 2, y + h / 2
    a(f'<line x1="200" y1="92" x2="{cx}" y2="{cy}" stroke="{QMUTED}" stroke-opacity="0.25"/>')
for key, (x, y, w, h, lab, col) in BOX.items():
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{QCARD}" stroke="{col}" stroke-opacity="0.85"/>')
    a(text(x + w / 2, y + h / 2 + 5, lab, anchor='middle', size=13, fill=col, ls='0'))
for x, lab in NODES:
    a(f'<rect x="{x}" y="{NY}" width="112" height="68" rx="9" fill="{QCARD}" stroke="{TEAL}" stroke-opacity="0.6"/>')
    a(text(x + 10, NY + 18, lab, anchor='start', size=13, fill=TEAL, ls='0'))
    a(text(x + 10, NY + 36, 'kubelet', anchor='start', size=13, fill=QMUTED, ls='0'))
# the hops: (from centre, to centre, t0, t1, what lands, which box lights)
C = {k: (v[0] + v[2] / 2, v[1] + v[3] / 2) for k, v in BOX.items()}
N2 = (144 + 56, NY + 30)
HOPS = [(C['user'], C['api'], 0.8, 1.6, 'api'), (C['api'], C['etcd'], 1.8, 2.6, 'etcd'), (C['api'], C['sched'], 3.0, 3.8, 'sched'),
        (C['sched'], C['api'], 4.2, 5.0, 'api'), (C['api'], N2, 5.4, 6.4, 'node2')]
for (x0, y0), (x1, y1), t0, t1, tgt in HOPS:
    kx = [(0.0, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)]
    ky = [(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)]
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle cx="{x0}" cy="{y0}" r="6" fill="#fff" stroke="{TEAL}" stroke-width="2"/></g></g></g>')
    if tgt in BOX:
        x, y, w, h = BOX[tgt][:4]
        a(f'<g class="fx" opacity="0">{pulse(t1)}<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{h + 4}" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the pod lands on node 2
TP = 6.4
a(f'<g opacity="0">{win(TP)}<rect x="{144 + 10}" y="{NY + 44}" width="92" height="18" rx="4" fill="{TEAL}" fill-opacity="0.85"/>{text(200, NY + 57, "pod", anchor="middle", size=13, fill=QCARD, ls="0")}</g>')
SY = NY + 92
for t0, t1, s in ((0.8, 1.8, 'apply: the API server takes it'), (1.8, 3.0, 'stored in etcd'), (3.0, 4.2, 'scheduler picks node 2'),
                  (4.2, 5.4, 'choice recorded'), (5.4, None, 'kubelet on node 2 starts it')):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(10, SY, s, anchor="start", size=13, fill=QSOFT, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-16 svgd-part5-16">')
o.insert(1, '<title id="svgt-part5-16">Fig 17.3 · Kubernetes architecture · control plane + workers</title>')
o.insert(2, '<desc id="svgd-part5-16">A Kubernetes cluster: a control plane of API server, etcd, scheduler and controllers, above three worker nodes, each running a kubelet. One request traced: kubectl apply sends a pod to the API server, which stores it in etcd. '
  'The scheduler, watching the API server, picks node 2 and the choice is recorded; node 2\'s kubelet, also watching, starts the pod. Every component talks only to the API server.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every Kubernetes component talks only to the API server, which keeps the cluster\'s desired state in etcd. '
           'A new pod is stored there, the scheduler watching the API server picks it a node, and that node\'s kubelet, also watching, starts it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>etcd.</b> <span class="key-term">etcd</span> is a small replicated key-value store that keeps agreement with Raft (Fig 17.5); production control planes run three or five copies.</li>
          <li><b>Controllers.</b> Loops that watch one kind of object and act until reality matches it: a Deployment controller, a ReplicaSet controller and many more (Fig 17.4).</li>
          <li><b>On each node.</b> The kubelet runs the pods assigned to it through a <span class="key-term">container runtime</span> such as containerd, and kube-proxy routes service traffic to them.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-3">
      <div class="diagram-label">Fig 17.3 · Kubernetes architecture · control plane + workers</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-3"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-3', cap, card.replace('CAPID', cap))
