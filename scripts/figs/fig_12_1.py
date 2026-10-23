# Fig 12.1 · The web of 1994–95 · static documents and a tab-out to Java (Pass 28, law 3). Chart Room plate. Two
# small browser windows. HTML form: "abc" typed into an age field, Send; the request goes to the server, the
# whole page goes blank while a new one loads, and the answer comes back as a new page with the error. Java
# applet: a box in the page shows "starting Java…" while a bar fills, then the applet runs, walled off from the
# page text beside it. t=0 (shift): both settled (error shown, applet running).
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, LOSS, GOLD = '#9bd89b', '#ec8d8d', '#d4a853'
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
def window(x0, y0, x1, y1, title, col):
    a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
    a(f'<line x1="{x0}" y1="{y0 + 22}" x2="{x1}" y2="{y0 + 22}" stroke="{col}" stroke-opacity="0.4"/>')
    a(text(x0 + 10, y0 + 16, title, anchor='start', size=13, fill=col, ls='0'))
# window 1: the HTML form, and the server
X0, X1, Y0, Y1 = 10, 290, 10, 128
window(X0, Y0, X1, Y1, 'HTML form', ROUTE)
TS, TB, TR = 1.4, 2.2, 4.4                      # Send; the page goes blank; the new page arrives
form = (text(X0 + 14, Y0 + 52, 'age:', anchor='start', size=13, fill=CSOFT, ls='0')
        + f'<rect x="{X0 + 60}" y="{Y0 + 36}" width="96" height="24" rx="3" fill="none" stroke="{CMUTED}"/>'
        + text(X0 + 68, Y0 + 52, 'abc', anchor='start', size=13, fill=CSOFT, ls='0')
        + f'<rect x="{X0 + 168}" y="{Y0 + 36}" width="60" height="24" rx="3" fill="{ROUTE}" fill-opacity="0.25" stroke="{ROUTE}"/>'
        + text(X0 + 198, Y0 + 52, 'Send', anchor='middle', size=13, fill=CSOFT, ls='0'))
a(f'<g opacity="0">{lit(0.31, TB)}{form}</g>')
a(f'<g class="fx" opacity="0">{lit(TB, TR)}{text((X0 + X1) / 2, Y0 + 62, "loading a new page…", anchor="middle", size=13, fill=CMUTED, ls="0")}</g>')
a(f'<g opacity="0">{win(TR)}{form}{text(X0 + 14, Y0 + 88, "age must be a number", anchor="start", size=13, fill=LOSS, ls="0")}</g>')
a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (TS - 0.002, 0.0), (TS, 1.0), (TS + 0.5, 0.0), (D, 0.0)])}'
  f'<rect x="{X0 + 168}" y="{Y0 + 36}" width="60" height="24" rx="3" fill="none" stroke="#fff" stroke-width="2"/></g>')
SX0, SX1 = 318, 390
SY = (Y0 + Y1) / 2
a(f'<rect x="{SX0}" y="{SY - 20}" width="{SX1 - SX0}" height="40" rx="5" fill="#0a1c2d" stroke="{CMUTED}"/>')
a(text((SX0 + SX1) / 2, SY + 5, 'server', anchor='middle', size=13, fill=CSOFT, ls='0'))
a(f'<line x1="{X1 + 4}" y1="{SY}" x2="{SX0 - 4}" y2="{SY}" stroke="{CMUTED}" stroke-dasharray="3 3"/>')
for t0, t1, xa, xb, col in ((TS, TB + 0.4, X1 + 4, SX0 - 4, CSOFT), (TR - 1.2, TR, SX0 - 4, X1 + 4, LOSS)):
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.01)}<g>{T.translate([(0.0, 0.0), (t0, 0.0), (t1, xb - xa), (D, xb - xa)], "x")}'
      f'<circle cx="{xa}" cy="{SY}" r="5" fill="{col}"/></g></g>')
# window 2: the applet, an island in the page
Y2, Y3 = 150, 290
window(X0, Y2, 390, Y3, 'Java applet', CYAN)
AX0, AX1, AY0, AY1 = X0 + 14, 214, Y2 + 36, Y3 - 14
a(f'<rect x="{AX0}" y="{AY0}" width="{AX1 - AX0}" height="{AY1 - AY0}" rx="3" fill="#081624" stroke="{CYAN}" stroke-dasharray="5 3"/>')
TJ0, TJ1 = 0.6, 6.0
a(f'<g opacity="0">{lit(0.31, TJ1)}{text(AX0 + 12, AY0 + 32, "starting Java…", anchor="start", size=13, fill=CMUTED, ls="0")}'
  f'<rect x="{AX0 + 12}" y="{AY0 + 46}" width="{AX1 - AX0 - 24}" height="8" rx="2" fill="none" stroke="{CMUTED}"/></g>')
bw = AX1 - AX0 - 24
a(f'<g class="fx" opacity="0">{lit(TJ0, TJ1)}<rect x="{AX0 + 12}" y="{AY0 + 46}" width="0" height="8" rx="2" fill="{CYAN}">'
  f'{T.anim("width", [(0.0, 0.0), (TJ0, 0.0), (TJ1, bw), (D, bw)])}</rect></g>')
a(f'<g opacity="0">{win(TJ1)}{text(AX0 + 12, AY0 + 32, "the applet runs", anchor="start", size=13, fill=CYAN, ls="0")}'
  f'{text(AX0 + 12, AY0 + 54, "in its own box", anchor="start", size=13, fill=CSOFT, ls="0")}</g>')
# the page around it, which the applet cannot reach
PX = AX1 + 16
for i, s in enumerate(('page text', 'the applet', "can't reach", 'or change')):
    a(text(PX, AY0 + 18 + i * 20, s, anchor='start', size=13, fill=CSOFT if i == 0 else CMUTED, ls='0'))
H = Y3 + 10
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-56 svgd-part3-56">')
o.insert(1, '<title id="svgt-part3-56">Fig 12.1 · The web of 1994–95 · static documents and a tab-out to Java</title>')
o.insert(2, '<desc id="svgd-part3-56">Two browser windows from 1995. In the first, an HTML form: abc is typed into an age field and Send is pressed. The request goes to the server, the whole page goes blank while a new one loads, and the new page says age must be a number. '
  'In the second, a Java applet sits in a box on the page: it shows starting Java while a bar fills, and only then runs, inside its box, unable to reach or change the page text around it.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('In 1995 a page could only send a form to the server and wait for a whole new page, or hand a box to a Java applet that took seconds to start and could not touch the page around it. What was missing was a small language that ran inside the page itself, at once.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The form.</b> Every check, even "is this a number?", meant a request to the server and a whole new page back.</li>
          <li><b>The applet.</b> Java ran in its own virtual machine, sandboxed from the computer and walled off from the page; the machine had to start before the first pixel.</li>
          <li><b>What came next.</b> JavaScript (Fig 12.2) shipped inside the page in Netscape 2.0. Applets faded, and browsers had dropped the plugin interface they needed by 2017.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-1">
      <div class="diagram-label">Fig 12.1 · The web of 1994–95 · static documents and a tab-out to Java</div>
      {svg}
      <p id="ch12-browser-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-1', 'ch12-browser-p4', card)
