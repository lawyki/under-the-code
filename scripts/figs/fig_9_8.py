# Fig 9.8 · IPv4 ran out, then CGNAT papered over it (Pass 28, law 3). Chart Room. Homes in the
# 100.64.0.0/10 shared space go out through one public address; each outgoing connection gets a port in
# the translation table. A connection started from outside matches no entry and is dropped.
# t=0 (shift): two mappings made, the outside attempt refused.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W, H = 400, 326
PUB = '203.0.113.5'
HOMES = [('home A', '100.64.0.11', 40), ('home B', '100.64.0.12', 100), ('home C', '100.64.0.13', 160)]
GX, GY, GW, GH = 166, 82, 70, 64
SRV, STR = (276, 40), (276, 150)
D = 10.0
OUT = [(0.8, 0, '5000', '40001'), (2.6, 1, '5000', '40002')]
INC = 4.6
T = Timeline(D, shift=INC + 1.6)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-22 svgd-part3-22">')
a('<title id="svgt-part3-22">Fig 9.8 · IPv4 ran out, then CGNAT papered over it</title>')
a(f'<desc id="svgd-part3-22">Three homes with addresses in the shared 100.64.0.0/10 range sit behind a carrier-grade NAT that owns one public address, {PUB}. '
  f'When home A connects to a server, the NAT records 100.64.0.11 port 5000 as {PUB} port 40001; home B gets port 40002. A connection started from outside to {PUB} matches no entry in the table and is dropped.</desc>')
for nm, ip, y in HOMES:
    a(f'<rect x="12" y="{y}" width="124" height="44" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.5"/>')
    a(text(24, y + 18, nm, size=13, fill=CMUTED, ls='0'))
    a(text(24, y + 36, ip, size=13, fill='#fff', ls='0'))
    a(f'<line x1="136" y1="{y + 22}" x2="{GX}" y2="{GY + GH / 2}" stroke="{CSOFT}" stroke-opacity="0.25"/>')
a(f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" rx="3" fill="{CPLATE}" stroke="{ROUTE}" stroke-width="2"/>')
a(text(GX + GW / 2, GY + 28, 'CGNAT', anchor='middle', size=13, fill=ROUTE, ls='0'))
a(text(GX + GW / 2, GY + 48, 'one IP', anchor='middle', size=13, fill=CMUTED, ls='0'))
for (x, y), lab in ((SRV, 'server'), (STR, 'outsider')):
    a(f'<rect x="{x}" y="{y}" width="112" height="40" rx="2" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.5"/>')
    a(text(x + 56, y + 25, lab, anchor='middle', size=13, fill='#fff', ls='0'))
    a(f'<line x1="{GX + GW}" y1="{GY + GH / 2}" x2="{x}" y2="{y + 20}" stroke="{CSOFT}" stroke-opacity="0.25"/>')
# outgoing connections
for t0, h, ip_port, pub_port in OUT:
    _, ip, y = HOMES[h]
    a(f'<polyline class="fx" points="136,{y + 22} {GX},{GY + GH / 2} {GX + GW},{GY + GH / 2} {SRV[0]},{SRV[1] + 20}" fill="none" stroke="{CYAN}" stroke-width="3" opacity="0">{win(t0, t0 + 1.4)}</polyline>')
# incoming attempt, refused
a(f'<line class="fx" x1="{STR[0]}" y1="{STR[1] + 20}" x2="{GX + GW + 4}" y2="{GY + GH / 2 + 8}" stroke="{RED}" stroke-width="3" opacity="0">{win(INC, INC + 2.0)}</line>')
cx, cy = GX + GW + 10, GY + GH / 2 + 12
a(f'<g>{held(INC + 0.6)}<line x1="{cx - 7}" y1="{cy - 7}" x2="{cx + 7}" y2="{cy + 7}" stroke="{RED}" stroke-width="3"/><line x1="{cx + 7}" y1="{cy - 7}" x2="{cx - 7}" y2="{cy + 7}" stroke="{RED}" stroke-width="3"/></g>')
# the table
TY = 238
a(text(12, TY - 10, f'TRANSLATION TABLE · {PUB}', size=13, fill=CMUTED))
a(f'<rect x="12" y="{TY}" width="376" height="54" rx="2" fill="{CPLATE}" stroke="{ROUTE}" stroke-opacity="0.4"/>')
for k, (t0, h, ip_port, pub_port) in enumerate(OUT):
    _, ip, _ = HOMES[h]
    a(f'<g>{held(t0 + 0.6)}{text(24, TY + 21 + k * 22, f"{ip}:{ip_port}", size=13, fill=CSOFT, ls="0")}{text(376, TY + 21 + k * 22, f"port {pub_port}", anchor="end", size=13, fill=CYAN, ls="0")}</g>')
a(f'<g>{held(INC + 0.6)}{text(12, TY + 78, "from outside: no entry, dropped", size=13, fill=RED, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Since the free pool of IPv4 addresses ran out in 2011, many ISPs put customers behind carrier-grade NAT (<span class="key-term">CGNAT</span>): thousands of homes share one public address, each outgoing connection given its own port in a translation table. '
           'A connection started from outside matches no entry and is dropped, so hosting anything from behind it fails.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The dates.</b> IANA handed out its last blocks of IPv4 addresses on 3 February 2011; the regional registries ran dry over the following years.</li>
          <li><b>The shared range.</b> 100.64.0.0/10 was set aside in 2012 for exactly this layer, so it never collides with home networks' own 192.168 addresses.</li>
          <li><b>The real fix.</b> IPv6 gives every device its own public address; by 2025 close to half of Google's users reached it over IPv6.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-9-8">
      <div class="diagram-label">Fig 9.8 · IPv4 ran out, then CGNAT papered over it</div>
      {svg}
      <p id="ch9-v6-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-8', 'ch9-v6-p2', card)
