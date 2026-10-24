# Fig 1.5 · Inside the switch (Pass 31 exemplar for Part I, from an empty script). Intent: electrons gather under the
# oxide into a channel when the gate goes positive, because the gate's field pulls them in from the n-type source and
# drain over the p-type body, without touching them, so current flows only while the gate is on.
# Concept chosen of three (ledger): the same cross-section twice, gate at 0 V above and positive below, so the still
# alone shows the switch. The lower panel switches on each cycle: electrons slide in from both wells, holes are pushed
# down, the lamp lights. t=0 is the finished on state.
from figlib import Timeline, text, obj, splice, GOLD, BLUE, RED, MUTED

W, H = 400, 404
INK = '#ece6da'
WIRE = 'rgba(255,255,255,0.45)'
T = Timeline(9, shift=6.0)
ON = T.beat(1.2, 'the gate goes positive')
IN = T.beat(3.0, 'the channel is complete')
T.beat(3.4, 'current flows, the lamp lights')
OFF = T.beat(8.2, 'the gate goes back to 0 V')

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-6 svgd-part1-6"{T.beats_attr()}>')
a('<title id="svgt-part1-6">Fig 1.5 · Inside the switch · a field-effect transistor in cross-section</title>')
a('<desc id="svgd-part1-6">The same transistor twice, cut open. A slab of p-type silicon holds two n-type wells, the source and the '
  'drain, full of free electrons; above the gap between them a gate sits on a thin insulating oxide, and a wire with a lamp and a '
  'battery joins source to drain. Top, the gate at 0 V: the electrons stay in their wells, nothing joins them, and the lamp is dark. Bottom, '
  'the gate switched each cycle from 0 V to a positive voltage (1 V): its pull reaches through the oxide, electrons slide in from both wells into a thin channel '
  'under it while the holes are pushed down, current flows round the wire and the lamp lights. The gate never touches the '
  'electrons.</desc>')

SL, SR = 20, 380                 # slab
WL, WR = 116, 284                # well inner edges = gate ends
GATE_Y, OX_Y = 74, 100           # gate top, oxide top (panel coordinates)
ST = 110                         # slab top
SB = 190                         # slab bottom

def e(cx, cy, extra=''):
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="4.6" fill="{BLUE}"{extra}/>'
def hole(cx, cy, extra=''):
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="4.2" fill="none" stroke="{RED}" stroke-width="1.7"{extra}/>'

def lamp(cx, cy, lit_pts=None):
    """Fig 1.4's lamp. lit_pts: an opacity timeline for the lit layer (None: dark)."""
    g = [f'<circle cx="{cx}" cy="{cy}" r="12" fill="#111" stroke="rgba(255,255,255,0.62)" stroke-width="2"/>',
         f'<path d="M {cx - 6} {cy + 4} L {cx - 2} {cy - 5} L {cx + 2} {cy + 4} L {cx + 6} {cy - 5}" fill="none" stroke="rgba(255,255,255,0.62)" stroke-width="1.6"/>']
    if lit_pts:
        rays = ''.join(f'<line x1="{cx + dx * 17:g}" y1="{cy + dy * 17:g}" x2="{cx + dx * 23:g}" y2="{cy + dy * 23:g}" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>'
                       for dx, dy in ((0, -1), (0.71, -0.71), (-0.71, -0.71), (1, 0), (-1, 0)))
        g.append(f'<g opacity="0">{T.anim("opacity", lit_pts)}'
                 f'<circle cx="{cx}" cy="{cy}" r="12" fill="rgba(212,168,83,0.38)" stroke="{GOLD}" stroke-width="2"/>'
                 f'<path d="M {cx - 6} {cy + 4} L {cx - 2} {cy - 5} L {cx + 2} {cy + 4} L {cx + 6} {cy - 5}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>{rays}</g>')
    return ''.join(g)

def panel(py, live):
    """One cross-section at panel top py. live: the lower panel, which switches on."""
    a(f'<g data-panel="{"on" if live else "off"}" transform="translate(0 {py})">')
    # the circuit: source contact up, across through the lamp, down to the drain contact
    a(f'<path d="M 40 {ST} V 26 H 66 M 75 26 H 360 V {ST}" fill="none" stroke="{WIRE}" stroke-width="1.6"/>')
    for x in (40, 360):
        a(f'<rect x="{x - 12}" y="{ST - 6}" width="24" height="7" rx="1.5" fill="#8d8d8d"/>')
    lit = T.pulse(IN + 0.2, OFF, ramp=0.25) if live else None
    a(lamp(118, 26, lit))
    # the battery that drives the current (long plate +, short plate -)
    a(f'<line x1="66" y1="13" x2="66" y2="39" stroke="rgba(255,255,255,0.75)" stroke-width="2.2"/>'
      f'<line x1="75" y1="19" x2="75" y2="33" stroke="rgba(255,255,255,0.75)" stroke-width="3.4"/>')
    # the slab, the two wells, the oxide, the gate
    a(f'<rect x="{SL}" y="{ST}" width="{SR - SL}" height="{SB - ST}" rx="4" fill="none" stroke="{RED}" stroke-opacity="0.8" stroke-width="1.4"/>')
    for x0 in (SL, WR):
        a(f'<path d="M {x0} {ST} V {ST + 40} Q {x0} {ST + 48} {x0 + 8} {ST + 48} H {x0 + 88} Q {x0 + 96} {ST + 48} {x0 + 96} {ST + 40} V {ST} Z" '
          f'fill="none" stroke="{BLUE}" stroke-opacity="0.85" stroke-width="1.4"/>')
    a(f'<rect x="{WL}" y="{OX_Y}" width="{WR - WL}" height="{ST - OX_Y}" fill="#cfdde6" fill-opacity="0.55"/>')
    if live:
        lit_g = T.pulse(ON, OFF, ramp=0.2)
        dark_g = [(t, 1.0 - v) for t, v in lit_g]
        def word(fill, pts, start):
            return text(200, GATE_Y + 19, 'gate', anchor='middle', size=15, fill=fill, extra=f' opacity="{start}"', role='label').replace('</text>', f'{T.anim("opacity", pts)}</text>')
        # 'gate' is a name, so a label (brief section 15), not object text
        a(f'<rect x="{WL}" y="{GATE_Y}" width="{WR - WL}" height="{OX_Y - GATE_Y}" rx="3" fill="{GOLD}" fill-opacity="0" stroke="{GOLD}" stroke-width="1.8">'
          f'{T.anim("fill-opacity", lit_g)}</rect>' + word('#f3e7cc', dark_g, 0) + word('#16120a', lit_g, 1))
    else:
        a(f'<rect x="{WL}" y="{GATE_Y}" width="{WR - WL}" height="{OX_Y - GATE_Y}" rx="3" fill="none" stroke="rgba(212,168,83,0.6)" stroke-width="1.4"/>'
          + text(200, GATE_Y + 19, 'gate', anchor='middle', size=15, fill='#f3e7cc', role='label'))
    # the gate's lead and its voltage
    a(f'<line x1="200" y1="{GATE_Y}" x2="200" y2="60" stroke="{GOLD if live else "rgba(255,255,255,0.6)"}" stroke-width="2"/>')
    if live:
        snap_on = [(0.0, 0.0), (ON - 0.001, 0.0), (ON, 1.0), (OFF - 0.001, 1.0), (OFF, 0.0)]
        snap_off = [(t, 1.0 - v) for t, v in snap_on]
        def word(s, fill, pts, start):
            return (text(200, 55, s, anchor='middle', size=15, fill=fill, extra=f' opacity="{start}"')
                    .replace('</text>', f'{T.anim("opacity", pts)}</text>'))
        a(obj(f'<rect x="170" y="38" width="60" height="24" rx="12" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>',
              f'<rect x="170" y="38" width="60" height="24" rx="12" fill="none" stroke="{GOLD}" stroke-width="1.8" opacity="0">{T.anim("opacity", snap_on)}</rect>',
              word('0 V', MUTED, snap_off, 1), word('1 V', GOLD, snap_on, 0)))
    else:
        a(obj('<rect x="170" y="38" width="60" height="24" rx="12" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.4"/>',
              text(200, 55, '0 V', anchor='middle', size=15, fill=MUTED)))
    # holes in the body; the positive gate pushes the ones under it down
    for k, x in enumerate((140, 170, 200, 230, 260)):
        y_up, y_dn = ST + 22 + (k % 2) * 14, ST + 52 + (k % 2) * 8
        if live:
            a(f'<circle cx="{x}" r="4.2" fill="none" stroke="{RED}" stroke-width="1.7">{T.anim("cy", [(0.0, y_up), (ON + 0.3, y_up), (IN, y_dn), (OFF, y_dn), (OFF + 0.6, y_up)])}</circle>')
        else:
            a(hole(x, y_up))
    for x in (300, 336, 366) if not live else (40, 72, 300, 336, 366):
        a(hole(x, ST + 66))
    # free electrons: eight in each well; below, five from each slide in under the oxide
    for side, x0 in ((-1, SL), (1, WR)):
        spots = [(x0 + 14 + c * 23, ST + 13 + r * 20) for r in range(2) for c in range(4)]
        movers = sorted(spots, key=lambda p: -p[0] if side < 0 else p[0])[:5] if live else []
        for p in spots:
            if p in movers:
                j = movers.index(p)
                cx_end = (WL + 10 + j * 16.5) if side < 0 else (WR - 10 - j * 16.5)
                d0 = ON + 0.25 + j * 0.18
                a(f'<circle r="4.6" fill="{BLUE}">{T.anim("opacity", [(0.0, 1.0), (IN + 0.15, 1.0), (IN + 0.25, 0.0), (OFF - 0.05, 0.0), (OFF, 1.0)])}'
                  f'{T.anim("cx", [(0.0, p[0]), (d0, p[0]), (d0 + 1.0, cx_end), (OFF, cx_end), (OFF + 0.5, p[0])])}'
                  f'{T.anim("cy", [(0.0, p[1]), (d0, p[1]), (d0 + 1.0, ST + 7), (OFF, ST + 7), (OFF + 0.5, p[1])])}</circle>')
            else:
                a(e(*p))
    if live:
        # current: the channel's own electrons stream from source to drain, and on round the wire back to the source
        flow = T.anim("opacity", [(0.0, 0.0), (IN + 0.15, 0.0), (IN + 0.25, 1.0), (OFF - 0.05, 1.0), (OFF, 0.0)])
        g = [f'<g opacity="0">{flow}']
        for k in range(10):
            g.append(f'<circle r="4.6" fill="{BLUE}"><animateMotion path="M {WL - 6} {ST + 7} H {WR + 6}" dur="2s" begin="-{k * 0.2:.1f}s" repeatCount="indefinite"/></circle>')
        for k in range(7):
            g.append(f'<circle r="2.8" fill="#fff"><animateMotion path="M 360 {ST - 8} V 26 H 40 V {ST - 8}" dur="4.2s" begin="-{k * 0.6:.1f}s" repeatCount="indefinite"/></circle>')
        g.append('</g>'); a(''.join(g))
        a(f'<g opacity="0">{T.anim("opacity", T.pulse(IN + 0.2, OFF, ramp=0.25))}' +
          text(200, ST + 34, 'bridge', anchor='middle', size=14, fill=BLUE, role='label') +
          text(380, 17, 'current flows', anchor='end', size=15, fill=GOLD, role='label') + '</g>')
    else:
        a(text(380, 17, 'no current', anchor='end', size=15, fill=MUTED, role='label'))
        a(text(200, ST + 72, 'p-type', anchor='middle', size=14, fill=RED, role='label'))
        a(text(80, ST - 12, 'source', anchor='middle', size=14, fill=BLUE, role='label'))
        a(text(322, ST - 12, 'drain', anchor='middle', size=14, fill=BLUE, role='label'))
        # above 'source', clear of the p-type body, so it names the well
        a(text(80, ST - 28, 'n-type', anchor='middle', size=14, fill='rgba(134,168,255,0.85)', role='label'))
    a('</g>')

panel(0, False)
panel(SB + 14, True)
a('</svg>')
svg = '\n'.join(o)

caption = ('At 0 V (top) the electrons stay in the source and drain and the lamp is dark; at 1 V (bottom) the gate draws them '
           'under the oxide into a channel and current flows. The gate never touches them: it pulls through the insulator, as a '
           'rubbed balloon lifts hair, and that pull across a gap is an electric field.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The silicon.</b> The source and drain are n-type, full of free electrons (dots); the body between them is p-type, with holes (rings). Where the two kinds meet, electrons fill the nearby holes and leave a thin barrier, so nothing joins source to drain.</li>
          <li><b>Gate on.</b> A positive voltage on the gate pulls through the oxide. It draws electrons in from both wells and pushes the holes away beneath it.</li>
          <li><b>The channel.</b> The gathered electrons form a thin bridge under the oxide, and the battery drives a current round the circuit: the lamp lights.</li>
          <li><b>Gate off.</b> At 0 V the pull stops, the electrons go back, the channel is gone and the lamp goes dark.</li>
          <li><b>The name.</b> MOSFET: metal-oxide-semiconductor field-effect transistor, the kind a modern chip holds billions of.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-5">
      <div class="diagram-label">Fig 1.5 · Inside the switch · a field-effect transistor in cross-section</div>
      {svg}
      <p id="ch1-transistor-p8" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-5', 'ch1-transistor-p8', card)
