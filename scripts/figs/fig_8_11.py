# Fig 8.11 · The OSI seven-layer cake (Pass 28, law 3). Chart Room. The seven layers as rows; beside each,
# the packet as that layer passes it down: GET / wrapped by TLS, then TCP, IP, and an Ethernet header and
# checksum, until layer 1 sends signals. A cursor lights the descent row by row. t=0: every row drawn.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

LAYERS = ['Application', 'Presentation', 'Session', 'Transport', 'Network', 'Data link', 'Physical']
W = 400
RY0, RH = 16, 38
PX = 160
D = 8.0
ST = [0.6 + 0.8 * k for k in range(7)]
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
SEG = {'data': ('GET /', 60, CYAN), 'tls': ('TLS', 44, '#c8a6ff'), 'tcp': ('TCP', 40, ROUTE), 'ip': ('IP', 32, '#9bd89b'),
       'eth': ('Eth', 38, '#d4a853'), 'fcs': ('FCS', 38, '#d4a853')}
ROWS = [['data'], ['tls'], ['tls'], ['tcp', 'tls'], ['ip', 'tcp', 'tls'], ['eth', 'ip', 'tcp', 'tls', 'fcs'], None]
o = []; body = []; b = body.append
for k, (nm, segs) in enumerate(zip(LAYERS, ROWS)):
    y = RY0 + k * RH
    b(f'<rect x="20" y="{y}" width="360" height="{RH - 6}" rx="2" fill="{CPLATE}" stroke="rgba(79,196,230,0.2)"/>')
    b(f'<rect class="fx" x="20" y="{y}" width="360" height="{RH - 6}" rx="2" fill="{CYAN}" fill-opacity="0.12" stroke="{CYAN}" stroke-width="2" opacity="0">{win(ST[k], ST[k] + 0.8)}</rect>')
    b(text(30, y + 21, f'{7 - k}', size=13, fill=CMUTED, ls='0'))
    b(text(50, y + 21, nm, size=13, fill='#fff', ls='0'))
    x = PX
    if segs is None:
        b(text(PX + 4, y + 21, '0110 1001 0011…', size=13, fill=CYAN, ls='0'))
        continue
    for sname in segs:
        lab, w, col = SEG[sname]
        if sname == 'tls':
            w = 52 if len(segs) > 1 else 104
            lab = 'TLS · GET /' if len(segs) == 1 else 'TLS'
        b(f'<rect x="{x}" y="{y + 5}" width="{w - 2}" height="{RH - 16}" rx="2" fill="{col}" fill-opacity="0.25" stroke="{col}"/>')
        b(text(x + (w - 2) / 2, y + 21, lab, anchor='middle', size=13, fill='#fff', ls='0'))
        x += w
H = RY0 + 7 * RH + 4
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-12 svgd-part3-12">')
o.append('<title id="svgt-part3-12">Fig 8.11 · The OSI seven-layer cake</title>')
o.append('<desc id="svgd-part3-12">The seven layers of the OSI model, from Application at the top to Physical at the bottom, and a request passing down through them. '
         'At the application layer it is GET /. Presentation encrypts it with TLS. Transport adds a TCP header, Network an IP header, and Data link an Ethernet header in front and a checksum, FCS, behind. '
         'The physical layer sends the whole frame as a stream of bits on the wire.</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ('Each layer serves the one above and adds its own wrapping on the way down: TLS around the request, then a TCP header, an IP header, and an Ethernet header and checksum, until layer 1 sends it as signals. '
           'In practice the top three blur into the application, which is why the internet runs on the four layers of TCP/IP.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Examples.</b> 7: HTTP, DNS, SSH. 6: TLS, compression. 5: session handling. 4: TCP, UDP. 3: IP, ICMP. 2: Ethernet, Wi-Fi. 1: copper, fibre, radio.</li>
          <li><b>On arrival.</b> The receiver works upward, each layer removing its own header and handing the rest up, in the reverse order.</li>
          <li><b>The standard.</b> ISO published the model in 1984 as ISO 7498; its protocols lost to TCP/IP, but its layer numbers stayed in engineers' vocabulary.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-11">
      <div class="diagram-label">Fig 8.11 · The OSI seven-layer cake</div>
      {svg}
      <p id="ch8-layers-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-11', 'ch8-layers-p4', card)
