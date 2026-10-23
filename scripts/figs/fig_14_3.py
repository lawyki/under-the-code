# Fig 14.3 · Three hash properties · three different attacks (Pass 28, law 3, conceptual pass: the properties and the
# arithmetic, no attack). Strongroom dossier plate. Top: the three properties for SHA-256, each with the work it takes to
# break it, drawn to scale in the exponent (2^256, 2^256, 2^128). Below: why collision is the cheap one. The birthday
# effect, simulated: people are dropped onto a 365-day strip one at a time (fixed seed) until two share a day; with
# person 23 the strip holds 253 pairs and the first match lands (person 5's day). t=0 (shift): the match shown.
import random
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

r = random.Random(64)
DAYS, seen = [], {}
while True:
    d = r.randrange(365); DAYS.append(d)
    if d in seen: break
    seen[d] = len(DAYS)
N = len(DAYS); MATCH = seen[DAYS[-1]]
assert (N, MATCH, DAYS[-1]) == (23, 5, 206) and N * (N - 1) // 2 == 253
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
T0, STEP = 1.0, 0.36
tk = lambda k: T0 + STEP * k                   # person k+1 lands
TM = tk(N - 1)
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.7, 0.0), (D, 0.0)])
pw = lambda e: f'2<tspan dy="-6">{e}</tspan>'
o = []; a = o.append
# the three properties, the work to break each for SHA-256, to scale in the exponent
a(text(20, 20, 'work to break SHA-256 (bar = exponent)', size=13, fill=PMUTED, ls='0'))
PROPS = [('preimage', 'given a hash, find an input', 256, OXBLOOD), ('second preimage', 'given an input, find another', 256, OXBLOOD),
         ('collision', 'any two with one hash', 128, BRASS)]
BX, BWMAX = 20, 290
for k, (name, what, e, col) in enumerate(PROPS):
    y = 34 + k * 56
    a(text(20, y + 14, name, size=13, fill=PARCH, ls='0'))
    a(text(380, y + 14, what, anchor='end', size=13, fill=PMUTED, ls='0'))
    w = BWMAX * e / 256
    a(f'<rect x="{BX}" y="{y + 22}" width="{w:.1f}" height="16" rx="2" fill="{col}" fill-opacity="0.55"/>')
    a(text(BX + w + 8, y + 35, pw(e), size=13, fill=col, ls='0'))
# the birthday effect
SY = 222
a(f'<line x1="20" y1="{SY - 20}" x2="380" y2="{SY - 20}" stroke="{PMUTED}" stroke-opacity="0.35"/>')
a(text(20, SY, 'why collisions are cheap: birthdays', size=13, fill=BRASS, ls='0'))
STRIP_Y = SY + 30
xd = lambda d: 20 + d * 360 / 364
a(f'<rect x="20" y="{STRIP_Y}" width="360" height="6" rx="2" fill="{DCARD}" stroke="{PMUTED}" stroke-opacity="0.5"/>')
for lab, d in (('Jan', 0), ('Jul', 181), ('Dec', 364)):
    a(text(xd(d), STRIP_Y + 24, lab, anchor='start' if d == 0 else ('end' if d == 364 else 'middle'), size=13, fill=PMUTED, ls='0'))
for k, d in enumerate(DAYS):
    hitk = (k == N - 1 or k == MATCH - 1)
    tick = f'<rect x="{xd(d) - 1.5:.1f}" y="{STRIP_Y - 22}" width="3" height="20" rx="1" fill="{PSOFT}"/>'
    a(f'<g opacity="0">{win(tk(k))}{tick}</g>')
    if hitk:
        a(f'<g opacity="0">{win(TM)}<rect x="{xd(d) - 2.5:.1f}" y="{STRIP_Y - 26}" width="5" height="26" rx="1" fill="{SEAL}"/></g>')
a(f'<g class="fx" opacity="0">{pulse(TM)}<circle cx="{xd(DAYS[-1]):.1f}" cy="{STRIP_Y - 12}" r="14" fill="none" stroke="{SEAL}" stroke-width="2"/></g>')
# the counters, one state per person
CY = STRIP_Y + 54
for k in range(N):
    t1 = tk(k + 1) if k + 1 < N else None
    vis = win(tk(k)) if t1 is None else lit(tk(k), t1)
    body = text(20, CY, f'people {k + 1}', size=13, fill=PARCH, ls='0') + text(380, CY, f'pairs {(k + 1) * k // 2}', anchor='end', size=13, fill=BRASS, ls='0')
    a(f'<g opacity="0">{vis}{body}</g>')
a(f'<g opacity="0">{T.anim("opacity", [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (TM - 0.002, 0.0), (TM, 1.0), (D, 1.0)])}{text(20, CY + 24, "one run: 23 shares a day with 5", size=13, fill=SEAL, ls="0")}</g>')
a(f'<g opacity="0">{lit(T0, TM)}{text(20, CY + 24, "count the pairs, not the people", size=13, fill=PMUTED, ls="0")}</g>')
H = CY + 36
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-16 svgd-part4-16">')
o.insert(1, '<title id="svgt-part4-16">Fig 14.3 · Three hash properties · three different attacks</title>')
o.insert(2, '<desc id="svgd-part4-16">The work needed to break each property of SHA-256, drawn to scale in the exponent: finding an input for a given hash (preimage) takes about 2 to the 256; finding a second input with the same hash as a given one also takes about 2 to the 256; finding any two inputs with one hash (a collision) takes only about 2 to the 128. '
  'Below, the birthday effect explains why: people are placed one at a time on a strip of the 365 days of the year, the count of pairs growing as the square of the people, and the 23rd person shares a birthday with the 5th; 23 people make 253 pairs.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A collision needs only some pair of inputs to match, and pairs grow as the square of the inputs: 23 people make 253 pairs and better than even odds of a shared birthday. A match is likely once the pairs rival the possible hashes, so a 256-bit hash falls to about 2<sup>128</sup> inputs, against 2<sup>256</sup> tries for either preimage.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>SHA-1.</b> A 160-bit hash: collisions were produced in practice in 2017 (<span class="key-term">SHAttered</span>, about 2<sup>63</sup> computations), while a preimage still costs about 2<sup>160</sup>.</li>
          <li><b>No shortcut for a second preimage.</b> The target is one fixed hash, not any pair, so the birthday effect does not help.</li>
          <li><b>Choosing a size.</b> Collision resistance is half the output size in bits, which is why 128-bit security calls for a 256-bit hash.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-14-3">
      <div class="diagram-label">Fig 14.3 · Three hash properties · three different attacks</div>
      {svg}
      <p id="ch14-hashing-p2" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-14-3', 'ch14-hashing-p2', card)
