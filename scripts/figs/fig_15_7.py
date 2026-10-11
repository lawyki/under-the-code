# Fig 15.7 · Five generations of defence · firewall → IDS → SIEM → EDR → zero trust (Pass 28, law 3, conceptual pass:
# where each defence looks). Strongroom dossier plate. A small network: the internet above, a wall with one gap (the web
# port), four machines, traffic arriving through the gap. Era by era the map fills in where each generation looks: the
# firewall at the edge; the IDS on the traffic that got through; the SIEM gathering every machine's logs; an EDR agent on
# every machine; zero trust, a lock on every machine, so each request is checked wherever it comes from. The generations
# stack. t=0 (shift): all five in place.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 14.0
T = Timeline(D, shift=13.4)
TG = [0.8 + 2.5 * k for k in range(5)]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
o = []; a = o.append
def box(x, y, w, h, col, op=0.6):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{DCARD}" stroke="{col}" stroke-opacity="{op}"/>')
# the internet, the path in, the machines
box(20, 12, 360, 30, PMUTED, 0.4); a(text(200, 32, 'internet', anchor='middle', size=13, fill=PMUTED, ls='0'))
PX = 60
MY, MW, MH = 122, 80, 40
mx = lambda i: 20 + i * (MW + 13.33)
MACH = ['web', 'db', 'laptop', 'laptop']
a(f'<line x1="{PX}" y1="42" x2="{PX}" y2="{MY}" stroke="{PMUTED}" stroke-opacity="0.5" stroke-width="2"/>')
for i, name in enumerate(MACH):
    box(mx(i), MY, MW, MH, PSOFT, 0.6)
    a(text(mx(i) + MW / 2, MY + 25, name, anchor='middle', size=13, fill=PARCH, ls='0'))
# traffic through the gap, all the way through the loop
for k in range(9):
    s = 0.4 + 1.5 * k
    if s + 0.8 > D: break
    mv = T.translate([(0.0, 0.0), (s, 0.0), (s + 0.8, MY - 42), (D, MY - 42)], 'y')
    a(f'<g class="fx" opacity="0">{lit(s, s + 0.82)}<g>{mv}<circle cx="{PX}" cy="42" r="5" fill="{PSOFT}"/></g></g>')
# 1 · the firewall: a wall with one gap
WY = 62
wall = (f'<line x1="20" y1="{WY}" x2="{PX - 12}" y2="{WY}" stroke="{BRASS}" stroke-width="5"/>'
        f'<line x1="{PX + 12}" y1="{WY}" x2="380" y2="{WY}" stroke="{BRASS}" stroke-width="5"/>')
a(f'<g opacity="0">{win(TG[0])}{wall}{text(380, WY - 6, "1 · firewall", anchor="end", size=13, fill=BRASS, ls="0")}</g>')
# 2 · the IDS: a sensor on the traffic that got through
IX, IY = 92, 80
a(f'<g opacity="0">{win(TG[1])}<line x1="{PX}" y1="{IY + 13}" x2="{IX}" y2="{IY + 13}" stroke="{SEAL}" stroke-dasharray="3 3"/>'
  f'<rect x="{IX}" y="{IY}" width="84" height="26" rx="2" fill="{DCARD}" stroke="{SEAL}" stroke-opacity="0.9"/>{text(IX + 42, IY + 18, "2 · IDS", anchor="middle", size=13, fill=SEAL, ls="0")}</g>')
# 3 · the SIEM: every machine's logs in one place
SY = 202
siem = ''.join(f'<line x1="{mx(i) + MW / 2}" y1="{MY + MH}" x2="200" y2="{SY}" stroke="{SAGE}" stroke-opacity="0.7" stroke-dasharray="4 3"/>' for i in range(4))
siem += f'<rect x="130" y="{SY}" width="140" height="30" rx="2" fill="{DCARD}" stroke="{SAGE}" stroke-opacity="0.9"/>{text(200, SY + 20, "3 · SIEM", anchor="middle", size=13, fill=SAGE, ls="0")}'
a(f'<g opacity="0">{win(TG[2])}{siem}</g>')
# 4 · EDR: an agent on every machine
edr = ''.join(f'<circle cx="{mx(i) + MW - 9}" cy="{MY + 9}" r="4.5" fill="{STAMP}"/>' for i in range(4))
a(f'<g opacity="0">{win(TG[3])}{edr}</g>')
# 5 · zero trust: a lock on every machine
def lock(x, y):
    return (f'<rect x="{x}" y="{y + 4}" width="10" height="8" rx="1" fill="{BRASS}"/>'
            f'<path d="M{x + 2},{y + 4} v-2 a3,3 0 0 1 6,0 v2" fill="none" stroke="{BRASS}" stroke-width="1.6"/>')
a(f'<g opacity="0">{win(TG[4])}{"".join(lock(mx(i) + 5, MY + 3) for i in range(4))}</g>')
for k, (x, y, w, h) in enumerate(((18, WY - 4, 364, 8), (IX - 2, IY - 2, 88, 30), (128, SY - 2, 144, 34), (18, MY - 2, 364, MH + 4), (18, MY - 2, 364, MH + 4))):
    a(f'<g class="fx" opacity="0">{pulse(TG[k])}<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" stroke="#fff" stroke-width="2"/></g>')
# legend for the two marks on the machines, and the era line
LY = SY + 54
a(f'<g opacity="0">{win(TG[3])}<circle cx="25" cy="{LY - 4}" r="4.5" fill="{STAMP}"/>{text(38, LY, "4 · EDR agent on each machine", size=13, fill=PARCH, ls="0")}</g>')
a(f'<g opacity="0">{win(TG[4])}{lock(20, LY + 10)}{text(38, LY + 22, "5 · zero trust: every request checked", size=13, fill=BRASS, ls="0")}</g>')
ERAS = ['1990s: filter at the edge', 'early 2000s: inspect what got in', 'mid 2000s: all the logs together',
        'mid 2010s: watch every machine', 'late 2010s: trust no position']
EY = LY + 52
for k, s in enumerate(ERAS):
    t1 = TG[k + 1] if k + 1 < 5 else None
    vis = win(TG[k]) if t1 is None else lit(TG[k], t1)
    a(f'<g opacity="0">{vis}{text(20, EY, s, size=13, fill=PSOFT, ls="0")}</g>')
H = EY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-34 svgd-part4-34">')
o.insert(1, '<title id="svgt-part4-34">Fig 15.7 · Five generations of defence · firewall → IDS → SIEM → EDR → zero trust</title>')
o.insert(2, '<desc id="svgd-part4-34">A small network: the internet above, four machines (a web server, a database and two laptops) below, and traffic arriving through one opening to the web server. Five generations of defence are added in turn, each where it looks. '
  'In the 1990s a firewall walls off the edge, leaving the web port open. In the early 2000s an intrusion detection system inspects the traffic that got through. In the mid 2000s a SIEM gathers every machine\'s logs in one place. In the mid 2010s an EDR agent watches each machine. In the late 2010s zero trust puts a lock on every machine, so each request is checked wherever it comes from. All five remain in place together.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Each generation watches a different place: the edge, the traffic that got through, the logs of everything, the processes on each machine, and finally every single request, wherever it comes from. '
           'They stack rather than replace one another.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Examples.</b> iptables and cloud security groups as firewalls, Snort, Suricata and Zeek for intrusion detection, Splunk and Elastic as SIEMs, CrowdStrike and SentinelOne for EDR.</li>
          <li><b>Detect or prevent.</b> An intrusion detection system only raises alerts; an intrusion prevention system sits in the path and drops what matches.</li>
          <li><b>Zero trust on paper.</b> Google's BeyondCorp (described from 2014) and NIST SP 800-207 (2020): identity and the state of the device decide access, not where on the network a request comes from.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-15-7">
      <div class="diagram-label">Fig 15.7 · Five generations of defence · firewall → IDS → SIEM → EDR → zero trust</div>
      {svg}
      <p id="ch15-defense-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-15-7', 'ch15-defense-p2', card)
