# Fig 16.11 · MESI · how four cores keep one cache line consistent (Pass 28, law 3). Quorum glass plate. Four cores,
# one cache line, each core's copy in one of four states. A reads: E (the only copy). B reads: both S. A writes: it
# broadcasts an invalidate, B drops to I, A becomes M (memory now stale). C reads: A supplies the new data and writes
# it back, A and C become S; B stays I until it reads again; D never touched the line. Each event lights its bus
# message and the states change on the same beat. t=0 (shift): A S, B I, C S, D I.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

COL = {'M': QROSE, 'E': VIOLET, 'S': TEAL, 'I': QMUTED}
EVENTS = [('A reads', 'no one else has it', 'AEBICIDI'), ('B reads', 'copies shared', 'ASBSCIDI'),
          ('A writes', 'invalidate the others', 'AMBICIDI'), ('C reads', 'A supplies, writes back', 'ASBICSDI')]
def states(s): return {s[i]: s[i + 1] for i in range(0, 8, 2)}
# the protocol's own rules, checked: at most one M or E; M or E excludes any S
for _, _, st in EVENTS:
    v = list(states(st).values())
    assert v.count('M') + v.count('E') <= 1 and not ((('M' in v) or ('E' in v)) and 'S' in v)
W = 400
D = 10.0
T = Timeline(D, shift=9.4)
TS = [0.8 + 1.8 * k for k in range(len(EVENTS))]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
CX = [56, 152, 248, 344]
for k, core in enumerate('ABCD'):
    x = CX[k]
    a(f'<rect x="{x - 42}" y="14" width="84" height="94" rx="10" fill="{QCARD}" stroke="{QMUTED}" stroke-opacity="0.5"/>')
    a(text(x, 34, f'core {core}', anchor='middle', size=13, fill=QSOFT, ls='0'))
    seq = [('I', 0.31, TS[0])] + [(states(st)[core], TS[j], TS[j + 1] if j + 1 < len(EVENTS) else None) for j, (_, _, st) in enumerate(EVENTS)]
    for j, (stt, t0, t1) in enumerate(seq):
        vis = first(t1) if j == 0 else (win(t0) if t1 is None else lit(t0, t1))
        a(f'<g opacity="0">{vis}<rect x="{x - 22}" y="48" width="44" height="44" rx="8" fill="{COL[stt]}" fill-opacity="{0.25 if stt == "I" else 0.85}"/>'
          f'{text(x, 77, stt, anchor="middle", size=16, fill=QCARD if stt != "I" else QSOFT, ls="0")}</g>')
        if j and seq[j - 1][0] != stt:
            a(f'<g class="fx" opacity="0">{pulse(t0)}<rect x="{x - 25}" y="45" width="50" height="50" rx="9" fill="none" stroke="#fff" stroke-width="2"/></g>')
# the bus and the event
BY = 132
a(f'<line x1="14" y1="{BY}" x2="386" y2="{BY}" stroke="{QSOFT}" stroke-width="3" stroke-opacity="0.4"/>')
a(text(386, BY + 20, 'bus', anchor='end', size=13, fill=QMUTED, ls='0'))
for j, (ev, why, _) in enumerate(EVENTS):
    t1 = TS[j + 1] if j + 1 < len(EVENTS) else None
    body = text(14, BY + 46, ev, anchor='start', size=13, fill=QAMBER, ls='0') + text(14, BY + 66, why, anchor='start', size=13, fill=QSOFT, ls='0')
    a(f'<g opacity="0">{win(TS[j]) if t1 is None else lit(TS[j], t1)}{body}</g>')
    a(f'<g class="fx" opacity="0">{pulse(TS[j])}<line x1="14" y1="{BY}" x2="386" y2="{BY}" stroke="{QAMBER}" stroke-width="3"/></g>')
LY = BY + 96
for k, (s_, lab) in enumerate((('M', 'modified'), ('E', 'exclusive'), ('S', 'shared'), ('I', 'invalid'))):
    x = (14, 120, 236, 320)[k]
    a(f'<rect x="{x}" y="{LY - 12}" width="16" height="16" rx="3" fill="{COL[s_]}" fill-opacity="{0.25 if s_ == "I" else 0.85}"/>' + text(x + 22, LY + 1, lab, anchor='start', size=13, fill=QMUTED, ls='0'))
H = LY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-12 svgd-part5-12">')
o.insert(1, '<title id="svgt-part5-12">Fig 16.11 · MESI · how four cores keep one cache line consistent</title>')
o.insert(2, '<desc id="svgd-part5-12">Four cores and one cache line; each core\'s copy is modified, exclusive, shared or invalid. Core A reads it and holds the only copy, exclusive. Core B reads it, and both copies become shared. '
  'Core A writes: it sends an invalidate on the bus, B\'s copy becomes invalid and A\'s modified. Core C reads: A supplies the new data and writes it back, and A and C become shared, while B stays invalid and D never held the line.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Every core\'s copy of a cache line is modified, exclusive, shared or invalid. A core may write only once every other copy is invalid, so a write broadcasts an invalidate and a later reader must fetch the new value.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The rule.</b> Many readers or one writer, never both: at most one copy is M or E, and then no other copy is valid.</li>
          <li><b>Ping-pong.</b> Two cores writing the same line take turns invalidating each other, and every write waits for the line to move. If the two values are unrelated but share one 64-byte line, that is <span class="key-term">false sharing</span>; padding them apart fixes it.</li>
          <li><b>Variants.</b> AMD adds an Owned state (MOESI) and Intel a Forward state (MESIF), so a shared line can be passed between cores without going through memory.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-16-11">
      <div class="diagram-label">Fig 16.11 · MESI · how four cores keep one cache line consistent</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-16-11"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-16-11', cap, card.replace('CAPID', cap))
