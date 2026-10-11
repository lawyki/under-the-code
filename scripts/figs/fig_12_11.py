# Fig 12.11 · CSP · the server tells the browser which scripts to trust, the browser refuses the rest (Pass 28, law 3,
# conceptual pass: the defence). Chart Room. Top, the response header: script-src 'self' https://cdn.example.com.
# Below, four scripts the page asks to run, one at a time, each along its own lane to the browser's policy gate: the
# page's own /app.js and the listed CDN's lib.js pass and run; a script injected from another origin and an injected
# inline script stop at the gate, refused although the injection landed. t=0 (shift): all four verdicts shown.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CPLATE, CDEEP, CSOFT, CMUTED
figlib.FONT = SPACE

RED = '#ec6b6b'
W = 400
D = 10.5
T = Timeline(D, shift=10.0)
ROWS = [('/app.js', 'runs: own origin', True, False),
        ('cdn.example.com/lib.js', 'runs: listed', True, False),
        ('other.example/x.js', 'refused: unlisted', False, True),
        ('inline &lt;script&gt;', 'refused: inline', False, True)]
TR = [0.8 + 2.2 * k for k in range(4)]
GO = 0.8                                      # lane to the gate
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# the header
a(f'<rect x="20" y="12" width="360" height="74" rx="3" fill="{CDEEP}" stroke="{ROUTE}" stroke-opacity="0.7"/>')
a(text(32, 34, 'Content-Security-Policy:', size=13, fill=ROUTE, ls='0'))
a(text(32, 54, "script-src 'self'", size=13, fill='#fff', ls='0'))
a(text(48, 74, 'https://cdn.example.com', size=13, fill='#fff', ls='0'))
# the gate
GX = 222
RY0, RH = 126, 50
ry = lambda k: RY0 + k * RH
a(text(20, RY0 - 12, 'requested', size=13, fill=CMUTED, ls='0'))
a(f'<line x1="{GX}" y1="{RY0 - 4}" x2="{GX}" y2="{ry(4) - 6}" stroke="{ROUTE}" stroke-width="3" stroke-opacity="0.8"/>')
a(text(GX, RY0 - 12, 'browser checks', anchor='middle', size=13, fill=ROUTE, ls='0'))
for k, (lab, verdict, ok, injected) in enumerate(ROWS):
    y = ry(k); ly = y + 34
    a(text(20, y + 16, lab, size=13, fill=RED if injected else '#fff', ls='0'))
    a(f'<line x1="20" y1="{ly}" x2="380" y2="{ly}" stroke="{CSOFT}" stroke-opacity="0.25" stroke-width="2"/>')
    t0 = TR[k]
    a(f'<g opacity="0">{win(t0 + GO)}{text(380, y + 16, verdict, anchor="end", size=13, fill=CYAN if ok else RED, ls="0")}</g>')
    end = 372 if ok else GX - 8
    t1 = t0 + GO + (0.5 if ok else 0.0)
    pts = [(0.0, 0.0), (t0, 0.0), (t0 + GO, GX - 8 - 28)] + ([(t1, end - 28)] if ok else []) + [(D, end - 28)]
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.6)}<g>{T.translate(pts, "x")}<circle cx="28" cy="{ly}" r="6" fill="{CYAN if ok else RED}"/></g></g>')
    a(f'<g class="fx" opacity="0">{pulse(t0 + GO)}<rect x="{GX - 5}" y="{y + 22}" width="10" height="24" rx="2" fill="{CYAN if ok else RED}"/></g>')
SY = ry(4) + 18
for t0, t1, s, col in ((0.31, TR[2] + GO, 'each script checked on its own', CYAN), (TR[2] + GO, None, 'injected, yet refused', RED)):
    vis = first(t1) if t0 < 0.5 else win(t0)
    a(f'<g opacity="0">{vis}{text(20, SY, s, size=13, fill=col, ls="0")}</g>')
H = SY + 12
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-66 svgd-part3-66">')
o.insert(1, '<title id="svgt-part3-66">Fig 12.11 · CSP · the server tells the browser which scripts to trust, the browser refuses the rest</title>')
o.insert(2, '<desc id="svgd-part3-66">The server\'s response carries the header Content-Security-Policy: script-src \'self\' https://cdn.example.com. The page then asks the browser to run four scripts, one at a time, and the browser checks each against the policy. '
  'The site\'s own /app.js runs, being from the same origin; cdn.example.com/lib.js runs, being listed; a script injected from other.example is refused, not being listed; and an injected inline script is refused, since the policy does not allow inline code. The injections landed in the page, yet neither runs.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The browser checks each script against the header on its own: the page\'s own and the listed origin run, and everything else is refused, even when an <span class="key-term">XSS</span> injection has already put it in the page. '
           'Inline code counts as everything else unless the policy admits it by nonce or hash.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Nonces and hashes.</b> A strict policy admits chosen inline scripts by a fresh random nonce, sent in the header and repeated on each trusted script tag, or by the hash of the script's text.</li>
          <li><b>Reports.</b> A <code>report-to</code> directive names a reporting endpoint, and the browser sends it a report for each violation, so a refused injection shows up in the site's monitoring (the older <code>report-uri</code> still works).</li>
          <li><b>Rolling it out.</b> <code>Content-Security-Policy-Report-Only</code> applies a policy without enforcing it and reports what it would have blocked, so a site can see what would break before switching it on.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-11">
      <div class="diagram-label">Fig 12.11 · CSP · the server tells the browser which scripts to trust, the browser refuses the rest</div>
      {svg}
      <p id="ch12-security-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-11', 'ch12-security-p9', card)
