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
        ev = sorted(((self.t(t), v) for t, v in pts), key=lambda p: p[0])
        def at(t):
            seq = [(ev[-1][0] - D, ev[-1][1])] + ev + [(ev[0][0] + D, ev[0][1])]
            for a, b in zip(seq, seq[1:]):
                if a[0] <= t <= b[0]:
                    if b[0] == a[0]: return b[1]
                    f = (t - a[0]) / (b[0] - a[0]); return a[1] + f * (b[1] - a[1])
            return ev[-1][1]
        ts = sorted(set([0.0, D] + [p[0] for p in ev]))
        kt = ';'.join(f'{t / D:.4f}' for t in ts)
        vs = ';'.join(f'{at(t):.3f}'.rstrip('0').rstrip('.') for t in ts)
        return f'<animate attributeName="{attr}" values="{vs}" keyTimes="{kt}" dur="{D:g}s" repeatCount="indefinite"{extra}/>'
    def pulse(self, t0, t1, ramp=0.2, lo=0.0, hi=1.0):
        """opacity points: off, on from t0 to t1, off."""
        return [(t0, lo), (t0 + ramp, hi), (t1 - ramp, hi), (t1, lo)]

def text(x, y, s, anchor='start', size=14, fill=MUTED, extra='', ls='0.06em'):
    return f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" {MONO} font-size="{size}" letter-spacing="{ls}" fill="{fill}"{extra}>{s}</text>'

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
