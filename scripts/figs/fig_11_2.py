# Fig 11.2 · A complete HTTP exchange · request and response, byte for byte (Pass 28, law 3). Chart Room plate.
# An HTTP/1.1 request and its response as the lines that cross the wire, each ending in CR LF (shown as \r\n):
# request line, headers, the blank line that ends them; status line, headers, blank line, body. Brackets name
# the parts. The lines light in the order they are sent, the request, then the response. t=0 (shift): all lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN = '#9bd89b'
W = 400
BX, BW = 20, 250                               # message box
LX = BX + 10
KX = BX + BW + 8                               # bracket x
STEP = 20
def ln(*parts):
    """[(text, colour)] -> tspans, then the line ending."""
    return ''.join(f'<tspan fill="{c}">{s}</tspan>' for s, c in parts) + f'<tspan fill="{CMUTED}"> \\r\\n</tspan>'
REQ = [ln(('GET', CYAN), (' /index.html ', CSOFT), ('HTTP/1.1', GREEN)),
       ln(('Host: ', CSOFT), ('example.com', CMUTED)),
       ln(('User-Agent: ', CSOFT), ('curl/8.4.0', CMUTED)),
       ln(('Accept: ', CSOFT), ('*/*', CMUTED)),
       f'<tspan fill="{CMUTED}">\\r\\n</tspan>']
REQ_K = [(0, 0, 'request line'), (1, 3, 'headers'), (4, 4, 'blank line')]
RES = [ln(('HTTP/1.1 ', GREEN), ('200', GREEN), (' OK', CSOFT)),
       ln(('Content-Type: ', CSOFT), ('text/html', CMUTED)),
       ln(('Content-Length: ', CSOFT), ('1256', CMUTED)),
       f'<tspan fill="{CMUTED}">\\r\\n</tspan>',
       f'<tspan fill="{CYAN}">&lt;!doctype html&gt;</tspan>',
       f'<tspan fill="{CYAN}">&lt;html&gt;…&lt;/html&gt;</tspan>']
RES_K = [(0, 0, 'status line'), (1, 2, 'headers'), (3, 3, 'blank line'), (4, 5, 'body')]
Y1 = 26                                        # request heading
B1 = Y1 + 10
L1 = B1 + 22
Y2 = L1 + STEP * (len(REQ) - 1) + 12 + 56      # response heading
B2 = Y2 + 10
L2 = B2 + 22
H = L2 + STEP * (len(RES) - 1) + 12 + 12
D = 10.0
T = Timeline(D, shift=9.5)
TQ = [0.8 + 0.5 * i for i in range(len(REQ))]
TR = [4.4 + 0.5 * i for i in range(len(RES))]
fade = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.28), (t0 - 0.002, 0.28), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-41 svgd-part3-41">')
a('<title id="svgt-part3-41">Fig 11.2 · A complete HTTP exchange · request and response, byte for byte</title>')
a('<desc id="svgd-part3-41">An HTTP/1.1 request, line by line, each line ending in carriage return and line feed: GET /index.html HTTP/1.1, then the headers Host: example.com, User-Agent: curl/8.4.0 and Accept: */*, then an empty line. '
  'The response: HTTP/1.1 200 OK, the headers Content-Type: text/html and Content-Length: 1256, an empty line, then the body, an HTML document.</desc>')
def message(title, col, by, ly, lines, kinds, times):
    a(text(BX, by - 10, title, anchor='start', size=13, fill=col, ls='0'))
    a(f'<rect x="{BX}" y="{by}" width="{BW}" height="{STEP * (len(lines) - 1) + 34}" rx="4" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.55"/>')
    for i, s in enumerate(lines):
        a(f'<g opacity="1">{fade(times[i])}{text(LX, ly + i * STEP, s, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
    for i0, i1, lab in kinds:
        y0, y1 = ly + i0 * STEP - 12, ly + i1 * STEP + 4
        a(f'<g opacity="1">{fade(times[i0])}<path d="M{KX},{y0} h4 V{y1} h-4" fill="none" stroke="{CMUTED}"/>'
          f'{text(KX + 12, (y0 + y1) / 2 + 5, lab, anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
message('request · client to server', GREEN, B1, L1, REQ, REQ_K, TQ)
# the wire between them
wy0, wy1 = B1 + STEP * (len(REQ) - 1) + 34 + 8, B2 - 28
a(f'<line x1="{BX + 40}" y1="{wy0}" x2="{BX + 40}" y2="{wy1}" stroke="{CMUTED}" stroke-dasharray="3 4"/>')
a(text(BX + 54, (wy0 + wy1) / 2 + 5, 'one TCP connection, port 80', anchor='start', size=13, fill=CMUTED, ls='0'))
tw = TQ[-1] + 0.4
a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (tw - 0.002, 0.0), (tw, 1.0), (tw + 0.792, 1.0), (tw + 0.795, 0.0), (D, 0.0)])}'
  f'<g>{T.translate([(0.0, 0.0), (tw, 0.0), (tw + 0.8, wy1 - wy0), (D, wy1 - wy0)], "y")}<circle cx="{BX + 40}" cy="{wy0}" r="5" fill="{GREEN}"/></g></g>')
message('response · server to client', ROUTE, B2, L2, RES, RES_K, TR)
a('</svg>')
svg = '\n'.join(o)

caption = ('One request and its response, byte for byte; every line ends in a carriage return and a line feed, drawn as <code>\\r\\n</code>.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Status codes.</b> The first digit is the class: 1xx informational, 2xx success, 3xx redirection, 4xx the client's error (404: no such document), 5xx the server's (500: it failed while answering).</li>
          <li><b>Where the body ends.</b> The blank line ends the headers; <code>Content-Length</code> says how many bytes of body follow (here 1,256), so the same connection can carry the next request.</li>
          <li><b>HTTP/2 and HTTP/3.</b> The same methods, headers and status codes, but sent as binary frames with compressed headers instead of these lines of text.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-11-2">
      <div class="diagram-label">Fig 11.2 · A complete HTTP exchange · request and response, byte for byte</div>
      {svg}
      <p id="ch11-http-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-11-2', 'ch11-http-p3', card)
