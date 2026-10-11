# Fig 12.5 · V8 · from source to optimised native code, with a feedback loop (Pass 28, law 3). Chart Room plate.
# V8's tiers top to bottom: the parser (source to bytecode), Ignition (runs bytecode at once, records the types it
# sees), Sparkplug (baseline machine code, 2021), Maglev (optimises for the types seen, 2023), TurboFan (optimises
# hardest). A function, add, climbs a tier at a time as it gets hot; then a string arrives where only numbers had,
# the optimised code's bet fails, and it deoptimises back to Ignition. t=0 (shift): back in Ignition, the deopt
# path lit, the feedback reading "a string".
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD, LOSS = '#9bd89b', '#d4a853', '#ec8d8d'
TIERS = [('parser', 'source to bytecode', CMUTED), ('Ignition', 'runs it, notes types', CYAN), ('Sparkplug', 'plain machine code', GREEN),
         ('Maglev', 'optimises for types', GOLD), ('TurboFan', 'optimises hardest', ROUTE)]
W = 400
BX0, BX1, BY0, BH, BG = 10, 300, 10, 42, 20
by = lambda i: BY0 + i * (BH + BG)
CX = 262                                         # the function chip's x
D = 10.0
T = Timeline(D, shift=9.5)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
for i, (name, desc, col) in enumerate(TIERS):
    y = by(i)
    a(f'<rect x="{BX0}" y="{y}" width="{BX1 - BX0}" height="{BH}" rx="5" fill="#0a1c2d" stroke="{col}" stroke-opacity="0.7"/>')
    a(text(BX0 + 10, y + 17, name, anchor='start', size=13, fill=col, ls='0'))
    a(text(BX0 + 10, y + 34, desc, anchor='start', size=13, fill=CMUTED, ls='0'))
    if i:
        a(f'<path d="M40,{y - BG + 2} V{y - 2} m-4,-5 l4,5 l4,-5" fill="none" stroke="{CMUTED}"/>')
a(text(52, by(2) - 5, 'hotter', anchor='start', size=13, fill=CMUTED, ls='0'))
# the deopt path: TurboFan (and Maglev) back to Ignition
yI, yT = by(1) + BH / 2, by(4) + BH / 2
dp = f'<path d="M{BX1},{yT} H{BX1 + 22} V{yI} H{BX1 + 6} m6,-5 l-6,5 l6,5" fill="none" stroke="{LOSS}" stroke-width="2"/>'
TD = 7.2                                         # the bet fails
a(f'<g opacity="0.3">{dp}</g><g class="fx" opacity="0">{win(TD)}{dp}</g>')
lab = text(BX1 + 30, (yI + yT) / 2 - 4, 'deopt', anchor='start', size=13, fill=LOSS, ls='0') + text(BX1 + 30, (yI + yT) / 2 + 13, 'back', anchor='start', size=13, fill=LOSS, ls='0')
a(f'<g opacity="0.3">{lab}</g><g class="fx" opacity="0">{win(TD)}{lab}</g>')
# what Ignition has seen add called with
FY = by(5) + 10
a(text(BX0, FY, 'add has seen:', anchor='start', size=13, fill=CMUTED, ls='0'))
a(f'<g opacity="0">{lit(0.31, TD)}{text(BX0 + 118, FY, "only numbers", anchor="start", size=13, fill=GREEN, ls="0")}</g>')
a(f'<g opacity="0">{win(TD)}{text(BX0 + 118, FY, "a string too", anchor="start", size=13, fill=LOSS, ls="0")}</g>')
# the function, climbing
STOPS = [(0.6, 0), (1.2, 1), (2.6, 2), (4.0, 3), (5.4, 4), (TD + 0.6, 1)]
cy0 = by(0) + BH / 2
ky = [(0.0, by(1) - by(0)), (0.3, by(1) - by(0)), (0.305, 0.0)]
for k, (t, i) in enumerate(STOPS):
    if k:
        ky.append((t - 0.5 if k < len(STOPS) - 1 else TD, ky[-1][1]))
    ky.append((t, by(i) - by(0)))
ky.append((D, by(1) - by(0)))
w = 38
a(f'<g class="fx"><g>{T.translate(ky, "y")}<rect x="{CX - w / 2}" y="{cy0 - 11}" width="{w}" height="22" rx="4" fill="#0a1c2d" stroke="#fff" stroke-width="1.5"/>'
  f'{text(CX, cy0 + 5, "add", anchor="middle", size=13, fill="#fff", ls="0")}</g></g>')
a(f'<g class="fx" opacity="0">{T.anim("opacity", [(0.0, 0.0), (TD - 0.002, 0.0), (TD, 1.0), (TD + 0.6, 0.0), (D, 0.0)])}'
  f'<rect x="{BX0}" y="{by(4)}" width="{BX1 - BX0}" height="{BH}" rx="5" fill="{LOSS}" fill-opacity="0.25" stroke="{LOSS}" stroke-width="2"/></g>')
H = FY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-60 svgd-part3-60">')
o.insert(1, '<title id="svgt-part3-60">Fig 12.5 · V8 · from source to optimised native code, with a feedback loop</title>')
o.insert(2, '<desc id="svgd-part3-60">V8\'s tiers, top to bottom: the parser turns source into bytecode; Ignition runs the bytecode at once and notes the types it sees; Sparkplug turns it into plain machine code; Maglev optimises for the types seen; TurboFan optimises hardest. '
  'A function called add moves down a tier at a time as it gets hotter, having seen only numbers. Then it is called with a string, the optimised code\'s assumption fails, and it drops back to Ignition.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('V8 runs every function first in its interpreter, which records the types it sees; as the function gets hotter it moves on to compilers that make ever faster code, betting on those types. '
           'Break the bet, a string where only numbers came, and the optimised code is thrown away: back to the interpreter.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The tiers.</b> Each costs more to compile and runs faster: Ignition interprets, Sparkplug (since 2021) translates bytecode straight to machine code, Maglev (since 2023) and TurboFan optimise. The optimising compilers, Maglev and TurboFan, work on background threads while the program runs.</li>
          <li><b>The bet.</b> Optimised code is built for the types seen so far, guarded by cheap checks. When a check fails, V8 rebuilds the interpreter's state and carries on there: <span class="key-term">deoptimisation</span>.</li>
          <li><b>Then and now.</b> The first V8, in 2008, had no interpreter and compiled everything straight to machine code. SpiderMonkey and JavaScriptCore also run tiers of interpreters and compilers today.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-5">
      <div class="diagram-label">Fig 12.5 · V8 · from source to optimised native code, with a feedback loop</div>
      {svg}
      <p id="ch12-node-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(ky)
    splice('part-3', 'fig-12-5', 'ch12-node-p2', card)
