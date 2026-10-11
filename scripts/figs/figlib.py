# Shared helpers for Pass 28 figures (law 3). Figures are drawn phone-first in a
# viewBox about 400 wide; no label under 14 units (11 CSS px from 360 px up).
import re

MONO = 'font-family="DM Mono"'
GOLD, BLUE, RED, GREEN = '#d4a853', '#86a8ff', '#ec8d8d', '#9bd89b'
MUTED = 'rgba(255,255,255,0.6)'

class Timeline:
    """A looping SMIL timeline written in 'story time' tau. SHIFT picks which
    story moment is t=0, the frame a reduced-motion reader sees: make it the
    complete one."""
    def __init__(self, dur, shift=0.0):
        self.dur, self.shift = float(dur), float(shift)
    def t(self, tau):
        return (tau - self.shift) % self.dur
    def anim(self, attr, pts, extra=''):
        D = self.dur
        # tau = dur is the same instant as tau = 0. A point there means "hold this to the end of the
        # loop": move it a hair earlier, so the hold survives and never shares an instant with tau = 0.
        pts = [(min(t, D - 0.0005), v) for t, v in pts]
        ev = sorted(((self.t(t), v) for t, v in pts), key=lambda p: p[0])
        def at(t):
            seq = [(ev[-1][0] - D, ev[-1][1])] + ev + [(ev[0][0] + D, ev[0][1])]
            for a, b in zip(seq, seq[1:]):
                if a[0] <= t <= b[0]:
                    if b[0] == a[0]: return b[1]
                    f = (t - a[0]) / (b[0] - a[0]); return a[1] + f * (b[1] - a[1])
            return ev[-1][1]
        ts = sorted(set([0.0, D] + [p[0] for p in ev]))
        kt = ';'.join(f'{t / D:.6f}' for t in ts)
        vs = ';'.join(f'{at(t):.3f}'.rstrip('0').rstrip('.') for t in ts)
        return f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" dur="{D:g}s" repeatCount="indefinite"{extra}/>'
    def translate(self, pts, axis='y'):
        """animateTransform translate along one axis from [(tau, offset)] keyframes."""
        D = self.dur
        pts = [(min(t, D - 0.0005), v) for t, v in pts]
        ev = sorted(((self.t(t), v) for t, v in pts), key=lambda p: p[0])
        def at(t):
            seq = [(ev[-1][0] - D, ev[-1][1])] + ev + [(ev[0][0] + D, ev[0][1])]
            for a, b in zip(seq, seq[1:]):
                if a[0] <= t <= b[0]:
                    return a[1] if b[0] == a[0] else a[1] + (t - a[0]) / (b[0] - a[0]) * (b[1] - a[1])
            return ev[-1][1]
        ts = sorted(set([0.0, D] + [p[0] for p in ev]))
        vals = ';'.join((f'0 {at(t):.2f}' if axis == 'y' else f'{at(t):.2f} 0') for t in ts)
        kt = ';'.join(f'{t / D:.6f}' for t in ts)
        return f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" dur="{D:g}s" repeatCount="indefinite"/>'
    def pulse(self, t0, t1, ramp=0.2, lo=0.0, hi=1.0):
        """opacity points: off, on from t0 to t1, off."""
        return [(t0, lo), (t0 + ramp, hi), (t1 - ramp, hi), (t1, lo)]

# Part II · Greenbar (the printed listing): IBM Plex Mono, phosphor green on a dark green plate.
PLEX = 'font-family="IBM Plex Mono"'
PHOS, PHOS_SOFT, LISTING, PLATE, PANEL = '#84ffb2', 'rgba(198,222,206,0.85)', 'rgba(132,255,178,0.55)', '#0c120e', '#152016'
FONT = MONO                     # the face text() uses; a part's script may set figlib.FONT = PLEX

def text(x, y, s, anchor='start', size=14, fill=MUTED, extra='', ls='0.06em'):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" {FONT} font-size="{size}" letter-spacing="{ls}" fill="{fill}"{extra}>{s}</text>'

def splice(part, fig_id, caption_id, card):
    """Replace a figure card (label, svg, caption, optional how-it-works) in public/<part>.html."""
    p = f'/Users/yki/Documents/github/atheric/under-the-code/public/{part}.html'
    s = open(p).read()
    m = re.search(r'<div class="(?:diagram-card|light-diagram)[^"]*" id="' + re.escape(fig_id) + r'">[\s\S]*?</svg>\s*<p id="'
                  + re.escape(caption_id) + r'"[\s\S]*?</p>\s*(?:<details class="fig-how">[\s\S]*?</details>\s*)?</div>', s)
    assert m, fig_id + ' not found'
    # a wrapped label keeps its separator with the word before it, never alone at a line end
    card = re.sub(r'(<div class="diagram-label">)([^<]*)(</div>)', lambda g: g.group(1) + g.group(2).replace(' · ', '&nbsp;· ') + g.group(3), card, count=1)
    s = s[:m.start()] + card + s[m.end():]
    open(p, 'w').write(s)
    print(fig_id, 'written')

# Part III · Chart Room (the cable chart): Space Mono labels, signal cyan and route orange on Prussian
# plates; continuous-flow motion. A part's script sets figlib.FONT = SPACE.
SPACE = 'font-family="Space Mono"'
CYAN, ROUTE, CPLATE, CDEEP = '#4fc4e6', '#e07a3f', '#0d2740', '#081b2e'
CSOFT, CMUTED = 'rgba(223,234,242,0.85)', 'rgba(223,234,242,0.6)'

# Part IV · Strongroom (the sealed dossier): Courier Prime labels, parchment on a dark dossier plate, seal and
# stamp reds, brass; lock-step motion (things land like stamps). A part's script sets figlib.FONT = COURIER.
COURIER = 'font-family="Courier Prime"'
PARCH, PSOFT, PMUTED = '#e6d9bd', 'rgba(230,217,189,0.85)', 'rgba(230,217,189,0.6)'
SEAL, STAMP, OXBLOOD, BRASS, SAGE = '#cf8d78', '#b8372f', '#c05a48', '#c9a25a', '#a9bf8e'
DOSSIER, DCARD = '#171008', '#241a10'

# Part V · Quorum (many machines as one): JetBrains Mono labels, violet and teal in phase on a void-indigo glass
# plate; motion is phase-synced (things move together, in step). A part's script sets figlib.FONT = JETBRAINS.
JETBRAINS = 'font-family="JetBrains Mono"'
VIOLET, TEAL, QSOFT, QMUTED = '#a08cff', '#4fd8c2', 'rgba(232,229,244,0.85)', 'rgba(232,229,244,0.58)'
QROSE, QAMBER, QVOID, QCARD = '#f08aa8', '#f2c46d', '#14111f', '#1d1930'
