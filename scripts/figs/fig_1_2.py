# Fig 1.2 · Enigma (Pass 28, law 3). Phone-first: viewBox 400 wide, no label under 14 units.
# The drawing is generated from the six-contact model so every wire is true:
# press A three times; each press steps the fast rotor, then the current runs out
# through three rotors, turns in the reflector and comes back on another wire.
import math
from enigma_model import N, L, FAST, MID, SLOW, REFL, press

W, H = 400, 500
GOLD, BLUE = '#d4a853', '#86a8ff'
Y0, DY = 92, 44                        # contact rows
y = lambda i: Y0 + i * DY
KX = 34                                 # key/lamp column centre
R = [(84, 136), (166, 218), (248, 300)] # rotor boxes (x0, x1): fast, middle, slow
FX, FW = 330, 26                        # reflector box
DUR = 9.0
PH = 3.0                                # one press
SHIFT = 2.0                             # t=0 shows press 1 at tau=2.0: path drawn, lamp lit (the still)

def tmap(tau):                          # press-timeline time -> SMIL time
    return (tau - SHIFT) % DUR

def anim(attr, pts, extra=''):
    """pts: [(tau, value)] piecewise-linear over the 9 s loop; returns <animate>."""
    ev = sorted(((tmap(t), v) for t, v in pts), key=lambda p: p[0])
    def at(t):                           # value at SMIL time t (linear, wrapping)
        xs = ev + [(ev[0][0] + DUR, ev[0][1])]
        prev = (ev[-1][0] - DUR, ev[-1][1])
        for p in [prev] + xs:
            if p[0] >= t:
                a, b = prevp, p
                if b[0] == a[0]: return b[1]
                f = (t - a[0]) / (b[0] - a[0]); return a[1] + f * (b[1] - a[1])
            prevp = p
        return ev[-1][1]
    ts = sorted(set([0.0, DUR] + [p[0] for p in ev]))
    vals = [at(t) for t in ts]
    kt = ';'.join(f'{t / DUR:.4f}' for t in ts)
    vs = ';'.join(f'{v:.3f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v) for v in vals)
    return f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" dur="{DUR:g}s" repeatCount="indefinite"{extra}/>'

def path_pts(fw, bk):
    k, a, b, c = fw
    r, d, e, f = bk
    fwd = [(KX + 16, y(k)), (R[0][0], y(k)), (R[0][1], y(a)), (R[1][0], y(a)), (R[1][1], y(b)),
           (R[2][0], y(b)), (R[2][1], y(c)), (FX, y(c)), (FX + FW / 2, y(c))]
    ret = [(FX + FW / 2, y(r)), (FX, y(r)), (R[2][1], y(r)), (R[2][0], y(d)), (R[1][1], y(d)),
           (R[1][0], y(e)), (R[0][1], y(e)), (R[0][0], y(f)), (KX + 16, y(f))]
    turn = [(FX + FW / 2, y(c)), (FX + FW / 2, y(r))]
    return fwd, turn, ret

def plen(pts): return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
def d(pts): return 'M ' + ' L '.join(f'{x:g} {yy:g}' for x, yy in pts)

out = []
o = out.append
o(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-3 svgd-part1-3">')
o('<title id="svgt-part1-3">Fig 1.2 · Enigma · one key, a different lamp every press</title>')
o('<desc id="svgd-part1-3">The key A is pressed three times. Each press steps the fast rotor one position before the current flows, '
  'so the current takes a different path out through three rotors, turns in the reflector, and returns on another wire: '
  'the lamps F, then E, then C light. The reflector never sends a letter back to itself.</desc>')

# column heads
mono = 'font-family="DM Mono"'
o(f'<text x="{KX}" y="40" text-anchor="middle" {mono} font-size="14" letter-spacing="0.08em" fill="rgba(255,255,255,0.6)">KEY</text>')
o(f'<text x="{(R[0][0] + R[2][1]) / 2:g}" y="40" text-anchor="middle" {mono} font-size="14" letter-spacing="0.08em" fill="rgba(255,255,255,0.6)">ROTORS</text>')
o(f'<text x="{FX + FW / 2:g}" y="40" text-anchor="middle" {mono} font-size="14" letter-spacing="0.08em" fill="rgba(255,255,255,0.6)">REFLECTOR</text>')

# rotor windows: the letter each rotor shows; the fast one steps B, C, D (one per press)
for ri, (x0, x1) in enumerate(R):
    cx = (x0 + x1) / 2
    o(f'<rect x="{cx - 13:g}" y="52" width="26" height="22" rx="3" fill="#0f0f0f" stroke="rgba(212,168,83,0.55)"/>')
    if ri == 0:
        for p, ch in enumerate('BCD'):
            pts = []
            s, e = p * PH, p * PH + PH
            pts = [(0, 0.0), (max(s - 0.001, 0), 0.0), (s + 0.001, 1.0), (e - 0.002, 1.0), (e - 0.001, 0.0), (DUR, 0.0)] if p else [(0, 1.0), (e - 0.002, 1.0), (e - 0.001, 0.0), (DUR - 0.001, 0.0), (DUR, 1.0)]
            o(f'<text x="{cx:g}" y="68" text-anchor="middle" {mono} font-size="14" fill="{GOLD}" opacity="0">{ch}{anim("opacity", pts)}</text>')
    else:
        o(f'<text x="{cx:g}" y="68" text-anchor="middle" {mono} font-size="14" fill="rgba(212,168,83,0.75)">A</text>')

# straight wires between columns (the fixed wiring between the parts)
for i in range(N):
    for xa, xb in [(KX + 16, R[0][0]), (R[0][1], R[1][0]), (R[1][1], R[2][0]), (R[2][1], FX)]:
        o(f'<line x1="{xa}" y1="{y(i)}" x2="{xb}" y2="{y(i)}" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>')

# rotor bodies and their internal wiring (faint); the fast rotor's wiring changes with each step
def wiring(perm, k):
    return [(R_i, (perm[(i + k) % N] - k) % N) for R_i, i in [(i, i) for i in range(N)]]
for ri, (x0, x1) in enumerate(R):
    o(f'<rect x="{x0}" y="{Y0 - 22}" width="{x1 - x0}" height="{(N - 1) * DY + 44}" rx="8" fill="#151515" stroke="rgba(212,168,83,0.5)" stroke-width="1.5"/>')
    perm = [FAST, MID, SLOW][ri]
    if ri == 0:
        for p, k in enumerate((1, 2, 3)):
            s, e = p * PH, p * PH + PH
            pts = [(0, 0.0), (max(s - 0.001, 0), 0.0), (s + 0.001, 1.0), (e - 0.002, 1.0), (e - 0.001, 0.0), (DUR, 0.0)] if p else [(0, 1.0), (e - 0.002, 1.0), (e - 0.001, 0.0), (DUR - 0.001, 0.0), (DUR, 1.0)]
            g = [f'<g opacity="0">{anim("opacity", pts)}']
            for i in range(N):
                j = (perm[(i + k) % N] - k) % N
                g.append(f'<line x1="{x0}" y1="{y(i)}" x2="{x1}" y2="{y(j)}" stroke="rgba(212,168,83,0.28)" stroke-width="1.2"/>')
            g.append('</g>'); o(''.join(g))
    else:
        for i in range(N):
            j = perm[i]
            o(f'<line x1="{x0}" y1="{y(i)}" x2="{x1}" y2="{y(j)}" stroke="rgba(212,168,83,0.28)" stroke-width="1.2"/>')
    for i in range(N):
        o(f'<circle cx="{x0}" cy="{y(i)}" r="2.6" fill="rgba(212,168,83,0.7)"/><circle cx="{x1}" cy="{y(i)}" r="2.6" fill="rgba(212,168,83,0.7)"/>')
o(f'<text x="{(R[0][0] + R[0][1]) / 2:g}" y="{y(N - 1) + 46:g}" text-anchor="middle" {mono} font-size="14" fill="rgba(212,168,83,0.85)">steps</text>')
o(f'<text x="{(R[0][0] + R[0][1]) / 2:g}" y="{y(N - 1) + 62:g}" text-anchor="middle" {mono} font-size="14" fill="rgba(212,168,83,0.85)">each press</text>')

# reflector: a box whose wires pair contacts and turn the current back
o(f'<rect x="{FX}" y="{Y0 - 22}" width="{FW}" height="{(N - 1) * DY + 44}" rx="6" fill="#1a1200" stroke="rgba(212,168,83,0.6)" stroke-width="1.5"/>')
for a_, b_ in [(0, 4), (1, 3), (2, 5)]:
    xx = FX + FW / 2 + (a_ - 1) * 4
    o(f'<path d="M {FX} {y(a_)} H {xx:g} V {y(b_)} H {FX}" fill="none" stroke="rgba(212,168,83,0.3)" stroke-width="1.2"/>')

# keys / lamps: one circle per letter; the pressed key glows gold, the lit lamp blue
lamps = [press(0, k)[1][-1] for k in (1, 2, 3)]
for i in range(N):
    o(f'<circle cx="{KX}" cy="{y(i)}" r="16" fill="#0f0f0f" stroke="rgba(255,255,255,0.25)" stroke-width="1.2"/>')
    o(f'<text x="{KX}" y="{y(i) + 6:g}" text-anchor="middle" {mono} font-size="17" fill="rgba(255,255,255,0.55)">{L[i]}</text>')
# key A pressed in every press (down for most of each press)
pts = []
for p in range(3):
    s = p * PH
    pts += [(s, 0.25), (s + 0.12, 1.0), (s + 2.75, 1.0), (s + 2.95, 0.25)]
o(f'<circle cx="{KX}" cy="{y(0)}" r="16" fill="rgba(212,168,83,0.35)" stroke="{GOLD}" stroke-width="2">{anim("opacity", pts)}</circle>')
for p, li in enumerate(lamps):
    s = p * PH
    pts = [(s + 1.85, 0.0), (s + 2.0, 1.0), (s + 2.8, 1.0), (s + 2.95, 0.0)]
    pts = [(0, 0.0)] + pts + [(DUR, 0.0)] if p else pts + [(0.0, 0.0), (DUR, 0.0)]
    o(f'<g opacity="0">{anim("opacity", pts)}<circle cx="{KX}" cy="{y(li)}" r="16" fill="rgba(134,168,255,0.45)" stroke="{BLUE}" stroke-width="2"/>'
      f'<text x="{KX}" y="{y(li) + 6:g}" text-anchor="middle" {mono} font-size="17" fill="#fff">{L[li]}</text></g>')

# the current: drawn out (gold), through the reflector turn, and back (blue)
for p, k in enumerate((1, 2, 3)):
    fw, bk = press(0, k)
    fwd, turn, ret = path_pts(fw, bk)
    s = p * PH
    lf, lt, lr = plen(fwd), plen(turn), plen(ret)
    vis = [(s + 0.15, 0.0), (s + 0.2, 1.0), (s + 2.8, 1.0), (s + 2.95, 0.0)]
    def draw(a0, a1, ln):                  # hidden at ln + 2 (inside the gap, so no round-cap dot)
        return [(s + 0.15, ln + 2), (s + a0, ln + 2), (s + a1, 0.0), (s + 2.95, 0.0)]
    grp = [f'<g opacity="0">{anim("opacity", vis)}']
    grp.append(f'<path d="{d(fwd)}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="{lf:.1f} {lf + 4:.1f}">{anim("stroke-dashoffset", draw(0.25, 1.05, lf))}</path>')
    grp.append(f'<path d="{d(turn)}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-linecap="round" stroke-dasharray="{lt:.1f} {lt + 4:.1f}">{anim("stroke-dashoffset", draw(1.05, 1.2, lt))}</path>')
    grp.append(f'<path d="{d(ret)}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="{lr:.1f} {lr + 4:.1f}">{anim("stroke-dashoffset", draw(1.2, 1.95, lr))}</path>')
    grp.append('</g>')
    o(''.join(grp))

# results: all three presses, always visible; the current one is outlined
by = y(N - 1) + 116
o(f'<text x="20" y="{by - 12}" {mono} font-size="14" letter-spacing="0.08em" fill="rgba(255,255,255,0.6)">PRESS A THREE TIMES</text>')
for p, li in enumerate(lamps):
    bx = 20 + p * 124
    o(f'<rect x="{bx}" y="{by}" width="112" height="40" rx="6" fill="#0f0f0f" stroke="rgba(255,255,255,0.18)"/>')
    s = p * PH
    pts = [(s, 0.0), (s + 0.15, 1.0), (s + 2.8, 1.0), (s + 2.95, 0.0)]
    pts = [(0, 0.0)] + pts + [(DUR, 0.0)] if p else pts + [(0.0, 0.0), (DUR, 0.0)]
    o(f'<rect x="{bx}" y="{by}" width="112" height="40" rx="6" fill="rgba(212,168,83,0.12)" stroke="{GOLD}" stroke-width="1.5" opacity="0">{anim("opacity", pts)}</rect>')
    o(f'<text x="{bx + 56}" y="{by + 26}" text-anchor="middle" {mono} font-size="16" fill="rgba(255,255,255,0.9)">A <tspan fill="rgba(255,255,255,0.45)">→</tspan> <tspan fill="{BLUE}">{L[li]}</tspan></text>')
# legend: the colours are named, never the only cue
ly = by + 66
o(f'<line x1="20" y1="{ly - 5}" x2="38" y2="{ly - 5}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')
o(f'<text x="46" y="{ly}" {mono} font-size="14" fill="rgba(255,255,255,0.7)">out</text>')
o(f'<line x1="88" y1="{ly - 5}" x2="106" y2="{ly - 5}" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>')
o(f'<text x="114" y="{ly}" {mono} font-size="14" fill="rgba(255,255,255,0.7)">back</text>')
o(f'<text x="380" y="{ly}" text-anchor="end" {mono} font-size="14" fill="rgba(255,255,255,0.45)">6 of 26 contacts</text>')
o('</svg>')
svg = '\n'.join(out)

caption = ('The same key, pressed three times, lights three different lamps: each press steps the fast rotor, so the current '
           'takes a new path out and, after the reflector, a different one back. The reflector also guarantees that no letter '
           'is ever enciphered as itself, the flaw the Bombe exploited.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Press.</b> The fast rotor steps one position first, so its wiring meets the contacts differently every time.</li>
          <li><b>Out.</b> The current runs through the three rotors, each a fixed scramble of 26 wires.</li>
          <li><b>Turn.</b> The reflector pairs contacts and sends the current back through the rotors on another wire.</li>
          <li><b>Lamp.</b> It arrives at a different letter, and never at the one pressed.</li>
          <li><b>The settings.</b> Rotor order, start positions and plugboard pairs gave about 158 × 10<sup>18</sup> possible settings, changed daily.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-2">
      <div class="diagram-label">Fig 1.2 · Enigma · one key, a different lamp every press</div>
      {svg}
      <p id="ch1-context-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    from figlib import splice
    splice('part-1', 'fig-1-2', 'ch1-context-p9', card)
    raise SystemExit

    import re, sys
    p = '/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html'
    s = open(p).read()
    m = re.search(r'<div class="diagram-card[^"]*" id="fig-1-2">[\s\S]*?</svg>\s*<p id="ch1-context-p9"[\s\S]*?</p>\s*(?:<details class="fig-how">[\s\S]*?</details>\s*)?</div>', s)
    assert m, 'fig-1-2 not found'
    s = s[:m.start()] + card + s[m.end():]
    open(p, 'w').write(s); print('fig 1.2 written', len(svg), 'bytes svg')
