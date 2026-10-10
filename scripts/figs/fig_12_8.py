# Fig 12.8 · Same-origin policy · scheme + host + port must all match (Pass 28, law 3). Chart Room plate. The
# reference origin https://www.example.com (port 443 by default) split into scheme, host and port; four URLs below,
# each split the same way and compared column by column: the same origin; http (scheme and default port 80 both
# differ); api.example.com (host); :8443 (port). Each row's marks light in turn, then its verdict.
# t=0 (shift): every row judged.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS = '#9bd89b', '#ec8d8d'
COLS = [(10, 78), (86, 270), (278, 336)]        # scheme, host, port chip spans
VX = 390                                         # verdict, right-aligned
REF = ('https', 'www.example.com', '443')
ROWS = [('https://www.example.com/page', ('https', 'www.example.com', '443')),
        ('http://www.example.com/', ('http', 'www.example.com', '80')),
        ('https://api.example.com/', ('https', 'api.example.com', '443')),
        ('https://www.example.com:8443/', ('https', 'www.example.com', '8443'))]
W = 400
D = 11.0
T = Timeline(D, shift=10.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
def chips(y, parts, cols, marks=None, t0=None):
    for k, ((x0, x1), s) in enumerate(zip(COLS, parts)):
        col = cols[k]
        a(f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="22" rx="4" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
        a(text((x0 + x1) / 2, y + 2, s, anchor='middle', size=13, fill=col, ls='0'))
        if marks is not None:
            ok = marks[k]
            mk = f'<rect x="{x0}" y="{y - 14}" width="{x1 - x0}" height="22" rx="4" fill="{GREEN if ok else LOSS}" fill-opacity="0.18" stroke="{GREEN if ok else LOSS}" stroke-width="2"/>'
            a(f'<g class="fx" opacity="0">{win(t0 + 0.35 * k)}{mk}</g>')
# the reference
for (x0, x1), h in zip(COLS, ('scheme', 'host', 'port')):
    a(text((x0 + x1) / 2, 16, h, anchor='middle', size=13, fill=CMUTED, ls='0'))
chips(40, REF, [CYAN] * 3)
a(text(VX, 42, 'origin', anchor='end', size=13, fill=CYAN, ls='0'))
a(f'<line x1="10" y1="62" x2="390" y2="62" stroke="{CMUTED}" stroke-opacity="0.4"/>')
for r, (url, parts) in enumerate(ROWS):
    y = 92 + r * 60
    t0 = 0.8 + 2.3 * r
    marks = [p == q for p, q in zip(parts, REF)]
    a(text(10, y, url, anchor='start', size=13, fill=CSOFT, ls='0'))
    chips(y + 26, parts, [CSOFT] * 3, marks, t0)
    same = all(marks)
    v = text(VX, y + 28, 'same' if same else 'other', anchor='end', size=13, fill=GREEN if same else LOSS, ls='0')
    a(f'<g opacity="0">{lit(0.31, t0 + 1.2)}{text(VX, y + 28, "?", anchor="end", size=13, fill=CMUTED, ls="0")}</g>')
    a(f'<g opacity="0">{win(t0 + 1.2)}{v}</g>')
H = 92 + 3 * 60 + 44
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-63 svgd-part3-63">')
o.insert(1, '<title id="svgt-part3-63">Fig 12.8 · Same-origin policy · scheme + host + port must all match</title>')
o.insert(2, '<desc id="svgd-part3-63">The origin https://www.example.com splits into scheme https, host www.example.com and port 443, the default for https. '
  'https://www.example.com/page matches in all three: the same origin. http://www.example.com differs in scheme and in port, 80 by default. https://api.example.com differs in host. https://www.example.com:8443 differs in port. Each of the last three is another origin.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('An origin is a scheme, a host and a port, and two URLs share one only if all three match; the path never counts. '
           'Change any one, <code>http</code> for <code>https</code>, <code>api</code> for <code>www</code>, 8443 for 443, and the browser treats the page as a stranger whose responses and DOM it may not read.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Default ports.</b> A URL without a port uses its scheme's default, 443 for https and 80 for http, so <code>http://www.example.com</code> differs in two places.</li>
          <li><b>The opt-ins.</b> A server can let named origins read its responses with CORS headers (<code>Access-Control-Allow-Origin</code>); two pages can agree to talk with <code>postMessage</code>.</li>
          <li><b>History.</b> The policy arrived with JavaScript itself, in Netscape 2.0 (1996). Cookies follow older, looser rules: they ignore the port, for one.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-8">
      <div class="diagram-label">Fig 12.8 · Same-origin policy · scheme + host + port must all match</div>
      {svg}
      <p id="ch12-security-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-8', 'ch12-security-p3', card)
