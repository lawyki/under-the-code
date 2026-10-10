# Fig 8.2 · Three substrates, one job (Pass 28, law 3). Chart Room. One request's path: laptop -> router
# -> internet provider -> data centre across the ocean. Three hops, three media (radio, copper, glass),
# each with its card; a packet flows down continuously, the hop it is on lit. t=0 (shift): mid-copper.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

NODES = ['laptop', 'router', 'provider', 'data centre']
HOPS = [('radio', 'Wi-Fi, through shared air', '#c8a6ff'),
        ('copper', 'Ethernet runs up to 100 m', ROUTE),
        ('glass', 'loses about 0.2 dB per km', CYAN)]
W, H = 400, 330
NX, NW, NH = 20, 112, 34
Y = lambda i: 12 + i * 92
D = 6.0
T = Timeline(D, shift=2.6)
LEG = (D - 0.6) / 3
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-3 svgd-part3-3">')
a('<title id="svgt-part3-3">Fig 8.2 · Three substrates, one job</title>')
a('<desc id="svgd-part3-3">One request\'s path from a laptop to a data centre across the ocean. From laptop to router it travels as radio, Wi-Fi at 2.4, 5 or 6 GHz through shared air. '
  'From router to internet provider it travels on copper, twisted pair in runs of up to 100 m, or on fibre. From provider to data centre it travels as light in glass fibre, losing about 0.2 dB per km. Each hop encodes the bits its own way.</desc>')
for i, nm in enumerate(NODES):
    a(f'<rect x="{NX}" y="{Y(i)}" width="{NW}" height="{NH}" rx="3" fill="{CDEEP}" stroke="{CSOFT}" stroke-opacity="0.5"/>')
    a(text(NX + NW / 2, Y(i) + 22, nm, anchor='middle', size=13, fill='#fff', ls='0'))
CXL = NX + NW / 2
for k, (med, fact, col) in enumerate(HOPS):
    y0, y1 = Y(k) + NH, Y(k + 1)
    da = '3 5' if med == 'radio' else ('none' if med == 'copper' else '10 4')
    a(f'<line x1="{CXL}" y1="{y0}" x2="{CXL}" y2="{y1}" stroke="{col}" stroke-width="{3 if med != "radio" else 2}" stroke-opacity="0.75" stroke-dasharray="{da}">'
      + ('<animate attributeName="stroke-dashoffset" values="0;-14" dur="1.2s" repeatCount="indefinite"/>' if med == 'glass' else '') + '</line>')
    cy = (y0 + y1) / 2 - 22
    a(f'<rect x="150" y="{cy}" width="230" height="44" rx="2" fill="{CPLATE}" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(162, cy + 18, med, size=14, fill=col, ls='0'))
    a(text(162, cy + 36, fact, size=13, fill=CSOFT, ls='0'))
    t0, t1 = 0.3 + k * LEG, 0.3 + (k + 1) * LEG
    a(f'<rect class="fx" x="150" y="{cy}" width="230" height="44" rx="2" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])}</rect>')
# the packet
ys = [(0.0, Y(0) + NH), (0.3, Y(0) + NH)]
for k in range(3):
    ys.append((0.3 + (k + 1) * LEG - 0.01, Y(k + 1)))
    if k < 2: ys.append((0.3 + (k + 1) * LEG, Y(k + 1) + NH))
ys.append((D, Y(3)))
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (0.29, 0.0), (0.3, 1.0), (D - 0.31, 1.0), (D - 0.3, 0.0), (D, 0.0)])}'
  f'<g>{T.translate([(t, v - (Y(0) + NH)) for t, v in ys], "y")}<circle class="fx" cx="{CXL}" cy="{Y(0) + NH}" r="6" fill="#fff"/></g></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A request from a laptop to a distant server crosses all three substrates: radio to the router, copper or fibre to the internet provider, and glass across the ocean. '
           'Each hop encodes the bits its own way, and the layers above see none of it.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Copper.</b> Cheap and easy to connect, but it loses signal quickly at high frequencies: Cat 6 loses about 20 dB per 100 m at 100 MHz, so Ethernet runs stop at 100 m.</li>
          <li><b>Glass.</b> At 1550 nm fibre loses about 0.2 dB per km, so light travels tens of kilometres between amplifiers.</li>
          <li><b>Radio.</b> It shares the air with every neighbour; cellular networks use bands from below 1 GHz to tens of GHz, Wi-Fi 2.4, 5 and 6 GHz.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-8-2">
      <div class="diagram-label">Fig 8.2 · Three substrates, one job</div>
      {svg}
      <p id="ch8-substrates-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-2', 'ch8-substrates-p6', card)
