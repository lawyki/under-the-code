# Fig 8.12 · OSI vs TCP/IP (Pass 28, law 3). Chart Room. Seven OSI rows beside four TCP/IP boxes that
# span the rows they absorb; a highlight pairs each TCP/IP layer with its OSI rows in turn.
# t=0: both columns drawn, nothing lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

OSI = ['7 Application', '6 Presentation', '5 Session', '4 Transport', '3 Network', '2 Data link', '1 Physical']
TCPIP = [('Application', 'HTTP, DNS, SSH', 0, 3), ('Transport', 'TCP, UDP', 3, 1), ('Internet', 'IP', 4, 1), ('Link', 'Ethernet, Wi-Fi', 5, 2)]
W = 400
Y0, RH = 40, 34
LX, LW, RX, RW = 20, 172, 204, 176
D = 8.0
SPAN = 1.8
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; body = []; b = body.append
b(text(LX, 26, 'OSI', size=13, fill=CMUTED, ls='0'))
b(text(RX, 26, 'TCP/IP', size=13, fill=CMUTED, ls='0'))
for i, nm in enumerate(OSI):
    y = Y0 + i * RH
    b(f'<rect x="{LX}" y="{y}" width="{LW}" height="{RH - 4}" rx="2" fill="{CPLATE}" stroke="rgba(79,196,230,0.3)"/>')
    b(text(LX + 12, y + 20, nm, size=13, fill=CSOFT, ls='0'))
for k, (nm, ex, i0, n) in enumerate(TCPIP):
    y, h = Y0 + i0 * RH, n * RH - 4
    t0 = 0.6 + k * SPAN
    b(f'<rect x="{RX}" y="{y}" width="{RW}" height="{h}" rx="2" fill="{CDEEP}" stroke="{CYAN}" stroke-opacity="0.7"/>')
    if n >= 2:
        b(text(RX + 12, y + h / 2 - 2, nm, size=14, fill='#fff', ls='0'))
        b(text(RX + 12, y + h / 2 + 16, ex, size=13, fill=CMUTED, ls='0'))
    else:
        b(text(RX + 12, y + 20, nm, size=14, fill='#fff', ls='0'))
        b(text(RX + RW - 12, y + 20, ex, anchor='end', size=13, fill=CMUTED, ls='0'))
    b(f'<rect class="fx" x="{RX}" y="{y}" width="{RW}" height="{h}" rx="2" fill="{ROUTE}" fill-opacity="0.18" stroke="{ROUTE}" stroke-width="2" opacity="0">{win(t0, t0 + SPAN)}</rect>')
    b(f'<rect class="fx" x="{LX}" y="{y}" width="{LW}" height="{h}" rx="2" fill="{ROUTE}" fill-opacity="0.12" stroke="{ROUTE}" stroke-width="2" opacity="0">{win(t0, t0 + SPAN)}</rect>')
H = Y0 + 7 * RH + 6
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-13 svgd-part3-13">')
o.append('<title id="svgt-part3-13">Fig 8.12 · OSI vs TCP/IP, side by side</title>')
o.append('<desc id="svgd-part3-13">The seven OSI layers beside the four TCP/IP layers. TCP/IP\'s Application layer, home of HTTP, DNS and SSH, covers OSI\'s Application, Presentation and Session. '
         'Its Transport layer, TCP and UDP, matches OSI Transport; its Internet layer, IP, matches OSI Network; and its Link layer, Ethernet and Wi-Fi, covers OSI\'s Data link and Physical.</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ('TCP/IP folds OSI\'s top three layers into one Application layer, because protocols such as HTTP manage their own sessions and formats, and its bottom two into one Link layer, because IP only needs a frame delivered to the next hop. '
           'OSI says where a feature belongs; TCP/IP describes what is on the wire.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>HTTP as an example.</b> It handles its own connections, content negotiation and compression, the jobs OSI gave to Session and Presentation.</li>
          <li><b>The names.</b> TCP/IP's layers come from RFC 1122 (1989): link, internet, transport, application.</li>
          <li><b>Where TLS sits.</b> It encrypts between the application and TCP, which is one reason neither model places it cleanly.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-12">
      <div class="diagram-label">Fig 8.12 · OSI vs TCP/IP, side by side</div>
      {svg}
      <p id="ch8-layers-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-12', 'ch8-layers-p5', card)
