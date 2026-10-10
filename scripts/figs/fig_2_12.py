# Fig 2.12 · The Patriot clock (Pass 28, law 3). The drift grows in a straight line over the
# 100 hours the battery ran (3.6 million tenth-second ticks, each ~0.000000095 s short): 0.34 s.
# At a Scud's 1,676 m/s that is ~570 m, and the radar's window was looking there, not here.
# Sources: GAO/IMTEC-92-26. The tenth was held in a 24-bit fixed-point register, chopped.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, MUTED

W, H = 400, 392
T = Timeline(8, shift=7.2)
def show(t0):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (7.8, 1.0), (7.801, 0.0), (7.999, 0.0)])
X0, X1, Y0, Y1 = 62, 360, 186, 46            # hours 0..100, drift 0..0.34 s
X = lambda h: X0 + h / 100 * (X1 - X0)
Y = lambda s: Y0 - s / 0.34 * (Y0 - Y1)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-28 svgd-part1-28">')
a('<title id="svgt-part1-28">Fig 2.12 · The Patriot missile · a clock that lost a third of a second</title>')
a('<desc id="svgd-part1-28">A Patriot battery counted time in tenths of a second, but 0.1 rounded in binary made each tick about 0.000000095 seconds short. '
  'Over 100 hours, 3.6 million ticks, the clock fell 0.34 seconds behind. At a Scud\'s 1,676 metres per second that is about 570 metres: '
  'the radar looked for the missile where the clock said it should be, found nothing there, and the battery did not fire.</desc>')
a(text(20, 24, 'CLOCK ERROR · 100 HOURS POWERED ON', size=13, fill=MUTED))
a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="rgba(255,255,255,0.4)"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 6}" stroke="rgba(255,255,255,0.4)"/>')
for h in (0, 50, 100):
    a(text(X(h), Y0 + 22, f'{h} h', anchor='middle', size=14, fill=MUTED, ls='0'))
for s, lab in ((0, '0 s'), (0.34, '0.34 s')):
    a(text(X0 - 8, Y(s) + 5, lab, anchor='end', size=14, fill=MUTED, ls='0'))
a(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="rgba(255,255,255,0.08)"/>')
a(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(100)}" y2="{Y(0.34)}" stroke="{RED}" stroke-width="2.5"/>')
a(f'<circle r="7" fill="{RED}" stroke="#0e0e0e" stroke-width="2">{T.anim("cx", [(0.0, X(0)), (0.4, X(0)), (4.4, X(100)), (8.0, X(100))])}'
  f'{T.anim("cy", [(0.0, Y(0)), (0.4, Y(0)), (4.4, Y(0.34)), (8.0, Y(0.34))])}</circle>')
a(text(X(36), Y(0.075), '3.6 million ticks,', size=14, fill='rgba(255,255,255,0.75)', ls='0'))
a(text(X(36), Y(0.075) + 20, 'each 0.000000095 s short', size=14, fill='rgba(255,255,255,0.75)', ls='0'))
# the radar's window, and where the Scud really was
RY = 312
a(text(20, 252, 'WHERE THE RADAR LOOKED', size=13, fill=MUTED))
a(f'<line x1="20" y1="{RY}" x2="380" y2="{RY}" stroke="rgba(255,255,255,0.25)" stroke-dasharray="4 4"/>')
a(f'<g opacity="0">{show(4.6)}<rect x="66" y="{RY - 22}" width="76" height="44" rx="5" fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-width="2"/>'
  f'<text x="104" y="{RY + 40}" text-anchor="middle" {MONO} font-size="14" fill="{BLUE}">window: empty</text></g>')
a(f'<g opacity="0">{show(5.3)}<circle cx="330" cy="{RY}" r="9" fill="{RED}"/>'
  f'<text x="330" y="{RY + 40}" text-anchor="middle" {MONO} font-size="14" fill="{RED}">the Scud</text>'
  f'<path d="M 142 {RY - 34} H 330" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/><path d="M 142 {RY - 40} v 12 M 330 {RY - 40} v 12" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>'
  f'<text x="236" y="{RY - 42}" text-anchor="middle" {MONO} font-size="15" fill="#fff">≈ 570 m</text></g>')
a(f'<g opacity="0">{show(5.9)}<text x="20" y="384" {MONO} font-size="14" fill="rgba(255,255,255,0.75)">0.34 s × 1,676 m/s ≈ 570 m</text></g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A Patriot battery near Dhahran had run for 100 hours, counting time in tenths of a second, and 0.1 rounded in binary made every tick a hair short. '
           'The clock fell 0.34 s behind, about 570 m at a Scud\'s speed, so the radar looked in the wrong place and the battery never fired; 28 soldiers died.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The tick.</b> 0.1 repeats forever in binary (Fig 2.11). The system held it in a 24-bit fixed-point register, chopped, so each tick counted about 0.000000095 s too little.</li>
          <li><b>The sum.</b> 100 hours is 3.6 million ticks; 3.6 million × 0.000000095 s ≈ 0.34 s.</li>
          <li><b>The window.</b> The radar predicts where a target will be and looks only there. With the clock 0.34 s behind, the window was some 570 m from the Scud, on 25 February 1991.</li>
          <li><b>The fix.</b> Corrected software reached Dhahran the next day. Rebooting the battery would have reset the drift.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-12">
      <div class="diagram-label">Fig 2.12 · The Patriot missile · a clock that lost a third of a second</div>
      {svg}
      <p id="ch2-float-p12" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-12', 'ch2-float-p12', card)
