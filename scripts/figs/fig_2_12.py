# Fig 2.12 · The Patriot missile (Pass 31, Part I, from an empty script). Job: function. Takeaway: each tick of a tenth
# of a second ran slightly short, so the error grew until the radar missed.
# Concept: one clock running for 100 hours, in two linked pictures. Above, the clock's error growing tick by tick in a
# straight line to 0.34 s. Below, the radar's search window, placed by that clock, drifting off the Scud as the error
# grows, until it looks some 570 m away and finds nothing. Both move together (Part I's flow verb). t=0 is hour 100.
from figlib import Timeline, text, splice, BLUE, RED, GOLD, MUTED

W, H = 400, 372
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D, RUN = 9.0, 6.5                         # 100 hours pass in RUN seconds, then hold
T = Timeline(D, shift=RUN + 1.2)
X0, X1, YB, YT = 48, 360, 160, 52          # chart: 0..100 h across, 0..0.34 s up
SCUD, DRIFT = 344, 200                     # the Scud's x on the track; 570 m drawn as DRIFT units
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-28 svgd-part1-28"{T.steps([(0.2, 'hour 0'), (3.65, 'hour 50'), (8.5, 'hour 100')])}>')
a('<title id="svgt-part1-28">Fig 2.12 · The Patriot missile · a clock that lost a third of a second</title>')
a('<desc id="svgd-part1-28">A Patriot battery counted time in tenths of a second, but 0.1 chopped in binary made each tick about 0.000000095 '
  'seconds short. Above, the clock\'s error grows in a straight line over 100 hours, 3.6 million ticks, to 0.34 seconds. Below, the '
  'radar\'s search window, placed by that clock, drifts off the Scud as the error grows: at a Scud\'s 1,676 metres per second, 0.34 '
  'seconds is about 570 metres. The radar looked where the clock said the missile should be, found nothing there, and the battery '
  'did not fire.</desc>')

a(text(20, 30, 'clock error', size=14, fill=INK))
a(f'<path d="M {X0} {YT - 8} V {YB} H {X1 + 8}" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
a(text(X0, YB + 22, '0 h', anchor='middle', size=14, fill=MUTED)); a(text(X1, YB + 22, '100 h', anchor='middle', size=14, fill=MUTED))
a(text(X0 - 8, YB + 5, '0', anchor='end', size=14, fill=MUTED))
a(text(X1 - 10, YT - 4, '0.34 s', anchor='end', size=16, fill=RED))
a(text(X0 + 14, YT + 18, 'each tick', size=14, fill=MUTED, ls='0'))
a(text(X0 + 14, YT + 36, '0.000000095 s short', size=14, fill=MUTED, ls='0'))
# the growing error: a solid line drawn along the dashed one, and its tip
grow = [(0.0, 0.0), (0.4, 0.0), (0.4 + RUN, 1.0), (D - 0.2, 1.0), (D - 0.01, 0.0)]
L = ((X1 - X0) ** 2 + (YB - YT) ** 2) ** 0.5
a(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YT}" stroke="{RED}" stroke-width="3" stroke-dasharray="{L:.1f} {L:.1f}">'
  f'{T.anim("stroke-dashoffset", [(t, L * (1 - v)) for t, v in grow])}</line>')
a(f'<g>{T.translate([(t, (X1 - X0) * v) for t, v in grow], axis="x")}<g>{T.translate([(t, -(YB - YT) * v) for t, v in grow], axis="y")}'
  f'<circle cx="{X0}" cy="{YB}" r="6" fill="{RED}"/></g></g>')

# the radar track: the Scud stays put, the search window drifts off it
TY = 280
a(text(20, 206, 'where the radar looked', size=14, fill=INK))
a(f'<line x1="20" y1="{TY}" x2="380" y2="{TY}" stroke="{EDGE}" stroke-dasharray="3 5"/>')
a(f'<circle cx="{SCUD}" cy="{TY}" r="8" fill="{RED}"/>')
a(text(SCUD, TY + 42, 'the Scud', anchor='middle', size=14, fill=RED))
a(f'<g>{T.translate([(t, -DRIFT * v) for t, v in grow], axis="x")}'
  f'<rect x="{SCUD - 34}" y="{TY - 24}" width="68" height="48" rx="6" fill="none" stroke="{BLUE}" stroke-width="2"/>'
  f'</g>')
a(text(SCUD - DRIFT, TY + 42, 'window', anchor='middle', size=14, fill=BLUE))
a(f'<path d="M {SCUD - DRIFT} {TY - 34} v -8 H {SCUD} v 8" fill="none" stroke="{INK}" stroke-width="1.4"/>')
a(text((2 * SCUD - DRIFT) / 2, TY - 48, '0.34 s × 1,676 m/s ≈ 570 m', anchor='middle', size=14, fill=INK, ls='0'))
a(text(200, 360, 'the window was empty: the battery never fired', anchor='middle', size=14, fill=GOLD, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('After 100 hours of tenth-of-a-second ticks the clock was 0.34 s behind, about 570 m at a Scud\'s speed, so the radar '
           'looked in the wrong place and the battery never fired.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The tick.</b> 0.1 repeats forever in binary (Fig 2.11). The system held it in a 24-bit fixed-point register, chopped, so each tick counted about 0.000000095 s too little.</li>
          <li><b>The sum.</b> 100 hours is 3.6 million ticks; 3.6 million × 0.000000095 s ≈ 0.34 s.</li>
          <li><b>The window.</b> The radar predicts where a target will be and looks only there. With the clock 0.34 s behind, the window was some 570 m (at Mach 5) from the Scud, on 25 February 1991.</li>
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
