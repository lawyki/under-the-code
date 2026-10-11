# Fig 17.10 · Service mesh and the sidecar · how a mesh moves one call (Pass 28, law 3). Quorum glass
# plate. Two pods, orders and auth, each an app beside a sidecar proxy. orders' app sends a plain request to its own
# sidecar; the sidecar encrypts it (mTLS) and sends it to auth's sidecar; the first attempt fails, the sidecar retries;
# auth's sidecar checks the caller's certificate and hands the plain request to its app. Above, the control plane pushes
# routes and certificates to both sidecars. The apps never see the failure. t=0 (shift): delivered.
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
# control plane
a(f'<rect x="80" y="10" width="240" height="34" rx="10" fill="{QCARD}" stroke="{VIOLET}" stroke-opacity="0.8"/>')
a(text(200, 32, 'control plane (Istio, Linkerd)', anchor='middle', size=13, fill=VIOLET, ls='0'))
# pods
PY = 96
PODS = [(10, 'orders'), (210, 'auth')]
for x, name in PODS:
    a(f'<path d="M{x + 90},44 V{PY + 78}" fill="none" stroke="{VIOLET}" stroke-opacity="0.3" stroke-dasharray="3 4"/>')
for x, name in PODS:
    a(f'<rect x="{x}" y="{PY}" width="180" height="128" rx="12" fill="none" stroke="{TEAL}" stroke-opacity="0.5"/>')
    a(text(x + 12, PY + 18, f'pod: {name}', anchor='start', size=13, fill=TEAL, ls='0'))
    a(f'<rect x="{x + 12}" y="{PY + 30}" width="156" height="34" rx="7" fill="{QCARD}" stroke="{QSOFT}" stroke-opacity="0.6"/>')
    a(text(x + 90, PY + 52, 'app', anchor='middle', size=13, fill=QSOFT, ls='0'))
    a(f'<rect x="{x + 12}" y="{PY + 80}" width="156" height="34" rx="7" fill="{QCARD}" stroke="{QAMBER}" stroke-opacity="0.85"/>')
    a(text(x + 90, PY + 102, 'sidecar proxy', anchor='middle', size=13, fill=QAMBER, ls='0'))
TPUSH = 0.8
for x, _ in PODS:
    a(f'<g class="fx" opacity="0">{lit(TPUSH, TPUSH + 1.0)}<g>{T.translate([(0.0, 0.0), (TPUSH, 0.0), (TPUSH + 1.0, PY + 70 - 50), (D, PY + 70 - 50)], "y")}<rect x="{x + 84}" y="46" width="12" height="10" rx="2" fill="{VIOLET}"/></g></g>')
def fly(p, q, t0, t1, col):
    (x0, y0), (x1, y1) = p, q
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, x1 - x0), (D, x1 - x0)], "x")}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)], "y")}<circle cx="{x0}" cy="{y0}" r="6" fill="{col}"/></g></g></g>')
OA, OS, AS, AA = (100, PY + 64), (100, PY + 80), (300, PY + 80), (300, PY + 64)
WY = PY + 140
fly(OA, OS, 2.2, 2.8, QSOFT)                                   # app → own sidecar, plain
fly((180, WY), (220, WY), 3.0, 3.8, QAMBER)                    # first attempt
a(f'<g opacity="0">{lit(3.8, 5.6)}<path d="M206,{WY - 7} l14,14 M220,{WY - 7} l-14,14" stroke="{QROSE}" stroke-width="2.5"/></g>')
fly((180, WY), (290, WY), 4.6, 5.8, QAMBER)                    # retry, delivered
fly(AS, AA, 6.2, 6.8, QSOFT)                                   # auth sidecar → app, plain
a(f'<line x1="100" y1="{PY + 114}" x2="100" y2="{WY}" stroke="{QAMBER}" stroke-opacity="0.4"/><line x1="100" y1="{WY}" x2="300" y2="{WY}" stroke="{QAMBER}" stroke-opacity="0.4" stroke-dasharray="5 4"/><line x1="300" y1="{WY}" x2="300" y2="{PY + 114}" stroke="{QAMBER}" stroke-opacity="0.4"/>')
a(text(200, WY + 22, 'mTLS between sidecars', anchor='middle', size=13, fill=QAMBER, ls='0'))
a(f'<g class="fx" opacity="0">{pulse(6.2)}<rect x="{210 + 10}" y="{PY + 78}" width="160" height="38" rx="8" fill="none" stroke="#fff" stroke-width="2"/></g>')
SY = WY + 50
for t0, t1, s, col in ((TPUSH, 2.2, 'control plane pushes routes, certificates', VIOLET), (2.2, 3.8, 'app sends plain HTTP to its own sidecar', QSOFT),
                       (3.8, 4.6, 'first try fails', QROSE), (4.6, 6.2, 'the sidecar retries, encrypted', QAMBER),
                       (6.2, None, 'delivered: the apps never saw the failure', TEAL)):
    a(f'<g opacity="0">{win(t0) if t1 is None else lit(t0, t1)}{text(200, SY, s, anchor="middle", size=13, fill=col, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-23 svgd-part5-23">')
o.insert(1, '<title id="svgt-part5-23">Fig 17.10 · Service mesh and the sidecar · how a mesh moves one call</title>')
o.insert(2, '<desc id="svgd-part5-23">Two pods, orders and auth, each holding an app and a sidecar proxy, and above them a control plane such as Istio or Linkerd that pushes routes and certificates to every sidecar. '
  'The orders app sends a plain request to its own sidecar. The sidecar sends it, encrypted with mutual TLS, to the auth pod\'s sidecar; the first attempt fails and the sidecar retries. The auth sidecar checks the caller and hands the plain request to its app. Neither app sees the failure.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each service gets a proxy beside it, and all its traffic goes through that proxy: encryption, retries, timeouts and metrics happen there, configured centrally, so a failed first attempt is retried before either app knows.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>mTLS.</b> Both sidecars present certificates, so each end knows which service it is talking to; the <span class="key-term">control plane</span> issues and rotates the certificates.</li>
          <li><b>What else the proxy does.</b> Timeouts and circuit breakers, gradual traffic shifts for new versions, and request metrics and traces for every call.</li>
          <li><b>The cost.</b> An extra hop on each side of every call, and a proxy per pod; newer meshes (Istio's ambient mode, Cilium) move some of this into a shared per-node proxy or the kernel.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-17-10">
      <div class="diagram-label">Fig 17.10 · Service mesh and the sidecar · how a mesh moves one call</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-17-10"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-17-10', cap, card.replace('CAPID', cap))
