# Fig 1.13 · Running a program in 1955 (Pass 28, law 3). One illustrative hour on two lanes:
# you hand in your deck at 9:00 and wait; the machine runs one job at a time and sits idle
# between them while the operator loads the next deck. A cursor walks the hour. t=0: the hour done.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, MUTED

W, H = 400, 262
X0, X1 = 62, 378
X = lambda m: X0 + m / 60 * (X1 - X0)          # minutes after 9:00
JOBS = [(0, 9, None), (16, 24, None), (30, 40, 'yours'), (47, 55, None)]
SW0, SW1 = 0.5, 6.5                             # the sweep, in story time
tm = lambda m: SW0 + m / 60 * (SW1 - SW0)
T = Timeline(8, shift=7.2)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-14 svgd-part1-14">')
a('<title id="svgt-part1-14">Fig 1.13 · Running a program in 1955 · one job, one user, one machine</title>')
a('<desc id="svgd-part1-14">An illustrative hour. You hand in your deck of punched cards at 9:00 and wait. The machine runs one job at a time: '
  'four jobs, yours from 9:30 to 9:40, with idle gaps between them while the operator loads the next deck. At 10:00 you collect your printout.</desc>')
for m, lab in ((0, '9:00'), (30, '9:30'), (60, '10:00')):
    a(text(X(m), 26, lab, anchor='middle' if m != 60 else 'end', size=14, fill=MUTED, ls='0'))
    a(f'<line x1="{X(m):.1f}" y1="34" x2="{X(m):.1f}" y2="176" stroke="rgba(255,255,255,0.08)"/>')
# you
a(text(20, 70, 'you', size=14, fill='rgba(255,255,255,0.8)'))
a(f'<rect x="{X(0) - 6:.1f}" y="52" width="16" height="22" rx="2" fill="#efe3c8" stroke="#bfae8a"/>')        # the deck
a(f'<line x1="{X(0) + 16:.1f}" y1="63" x2="{X(60) - 22:.1f}" y2="63" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="3 5"/>')
a(text((X(0) + X(60)) / 2, 88, 'waiting', anchor='middle', size=13, fill=MUTED))
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (SW1 - 0.05, 0.0), (SW1, 1.0), (7.9, 1.0), (7.95, 0.0)])}'
  f'<path d="M {X(60) - 20:.1f} 52 h 18 v 22 l -4 -3 l -5 3 l -4 -3 l -5 3 z" fill="#f4f4f4"/></g>')       # the printout
# the machine
a(text(20, 136, 'CPU', size=14, fill='rgba(255,255,255,0.8)'))
a(f'<rect x="{X0}" y="116" width="{X1 - X0}" height="32" rx="3" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.15)"/>')
for m0, m1, lab in JOBS:
    col = GOLD
    a(f'<rect x="{X(m0):.1f}" y="116" width="{X(m1) - X(m0):.1f}" height="32" rx="3" fill="{col}" fill-opacity="{0.75 if lab else 0.4}" stroke="{col}">'
      f'{T.anim("opacity", [(0.0, 0.12), (tm(m0), 0.12), (tm(m0) + 0.1, 1.0), (7.9, 1.0), (7.95, 0.12)])}</rect>')
    if lab:
        a(text((X(m0) + X(m1)) / 2, 137, lab, anchor='middle', size=14, fill='#0e0e0e', ls='0'))
# your deck goes in at 9:30
a(f'<path d="M {X(0) + 2:.1f} 76 Q {X(0) + 2:.1f} 104 {X(30):.1f} 112" fill="none" stroke="rgba(239,227,200,0.5)" stroke-width="1.5" stroke-dasharray="3 3"/>')
# the cursor: the hour passing
a(f'<line y1="34" y2="176" stroke="#fff" stroke-width="2" opacity="0">'
  f'{T.anim("x1", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}{T.anim("x2", [(0.0, X0), (SW0, X0), (SW1, X1), (8.0, X1)])}'
  f'{T.anim("opacity", [(0.0, 0.0), (SW0 - 0.05, 0.0), (SW0, 1.0), (SW1, 1.0), (SW1 + 0.1, 0.0), (8.0, 0.0)])}</line>')
# legend
a(f'<rect x="20" y="196" width="18" height="14" rx="2" fill="{GOLD}" fill-opacity="0.6" stroke="{GOLD}"/>')
a(text(46, 208, 'running a job', size=14, fill=MUTED))
a('<rect x="20" y="222" width="18" height="14" rx="2" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.3)"/>')
a(text(46, 234, 'idle: the next deck loading', size=14, fill=MUTED))
a(text(380, 256, 'an illustrative hour', anchor='end', size=13, fill='rgba(255,255,255,0.4)'))
a('</svg>')
svg = '\n'.join(o)

caption = ('One program had the whole machine: you handed in your cards, the operator ran the jobs one by one, and you came back an hour later for the printout. '
           'Between jobs, while the next deck was loaded, the most expensive machine in the building sat idle.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>A job.</b> A deck of punched cards, roughly one line of program per card, carried to the machine room.</li>
          <li><b>The queue.</b> The operator loaded decks one after another; each job had the whole computer while it ran.</li>
          <li><b>The cost.</b> A bug meant new cards and another hour's wait, and the machine stood idle in the gaps: the waste time-sharing set out to remove.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-13">
      <div class="diagram-label">Fig 1.13 · Running a program in 1955 · one job, one user, one machine</div>
      {svg}
      <p id="ch1-kernel-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-13', 'ch1-kernel-p2', card)
