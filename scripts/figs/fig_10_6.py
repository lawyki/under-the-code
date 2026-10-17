# Fig 10.6 · AIMD's fairness, in phase space (Pass 28, law 3). Chart Room paper card. Two flows, A and B,
# share a link of capacity 32 and lose together (Chiu and Jain's model). Start A 22, B 4. Additive
# increase moves the pair up the 45° direction until A + B reaches capacity (the gap A - B is kept);
# halving moves it toward the origin along its ray (the gap halves). A dot walks five cycles; the row of
# gaps lights one by one. t=0 (shift): the whole walk drawn, every gap lit.
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D, GREEN, RED = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f', '#2e7e4f', '#b3261e'
CAP, CYCLES = 32, 5
a_, b_ = 22.0, 4.0
PTS, GAPS = [(a_, b_)], [a_ - b_]
for _ in range(CYCLES):
    d = (CAP - a_ - b_) / 2
    a_, b_ = a_ + d, b_ + d; PTS.append((a_, b_))          # additive: both +d, gap kept
    a_, b_ = a_ / 2, b_ / 2; PTS.append((a_, b_))          # multiplicative: both halved, gap halved
    GAPS.append(a_ - b_)
assert [round(g, 2) for g in GAPS] == [18, 9, 4.5, 2.25, 1.12, 0.56]
GAPS = GAPS[:5]
AA, AB = 29, 19                               # axes: A to 29, B to 19, one scale for both (45° stays 45°)
W, X0, SC = 400, 54, 11.0
Y0 = 58 + AB * SC
H = int(Y0 + 36)
px = lambda a: X0 + a * SC
py = lambda b: Y0 - b * SC
D = 13.0
RISE, FALL, GAP0 = 1.3, 0.9, 0.5
T = Timeline(D, shift=12.3)
o = []; a = o.append
win = lambda t0, t1: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)]) if t1 is None else \
    T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-33 svgd-part3-33">')
a('<title id="svgt-part3-33">Fig 10.6 · AIMD\'s fairness, in phase space</title>')
a('<desc id="svgd-part3-33">Flow A\'s share across, flow B\'s share up, on a link of capacity 32. A dashed line marks the link full (A plus B equals 32), another marks A equals B. '
  'Starting at A 22, B 4, both flows add one per round trip, moving diagonally until the link is full, then both halve, moving toward the origin. '
  'The gap between them goes 18, 9, 4.5, 2.25, 1.1: the walk settles onto the fair line, its peaks on the capacity line creeping toward the point where the link is full and the shares are equal.</desc>')
# axes
a(f'<line x1="{X0}" y1="{Y0}" x2="{px(AA)}" y2="{Y0}" stroke="{INK_SOFT}"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{py(AB)}" stroke="{INK_SOFT}"/>')
a(text(X0 - 8, Y0 + 5, '0', anchor='end', size=13, fill=INK_SOFT, ls='0'))
a(text(px(AA), Y0 + 22, 'flow A', anchor='end', size=13, fill=INK_SOFT, ls='0'))
a(text(X0 - 8, py(AB) - 10, 'flow B', anchor='start', size=13, fill=INK_SOFT, ls='0'))
# capacity and fairness lines, the target where they cross
a(f'<line x1="{px(CAP - AB)}" y1="{py(AB)}" x2="{px(AA)}" y2="{py(CAP - AA)}" stroke="{ACC}" stroke-width="1.5" stroke-dasharray="5 4"/>')
a(text(px(AA), py(12.5), 'link full', anchor='end', size=13, fill=ACC, ls='0'))
a(f'<line x1="{px(0)}" y1="{py(0)}" x2="{px(AB)}" y2="{py(AB)}" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="5 4"/>')
a(text(px(10.3), py(11), 'A = B: fair', anchor='end', size=13, fill=GREEN, ls='0'))
a(f'<circle cx="{px(16)}" cy="{py(16)}" r="6" fill="none" stroke="{INK}" stroke-width="1.5"/>')
a(text(px(13.6), py(16.4), 'full and fair', anchor='end', size=13, fill=INK, ls='0'))
# the walk, drawn whole; each halving flashes its ray to the origin
a(f'<polyline points="{" ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in PTS)}" fill="none" stroke="{ROUTE_D}" stroke-width="2.2" stroke-linejoin="round"/>')
a(f'<circle cx="{px(PTS[0][0]):.1f}" cy="{py(PTS[0][1]):.1f}" r="4" fill="{ROUTE_D}"/>')
a(text(px(PTS[0][0]) + 8, py(PTS[0][1]) + 5, 'start', anchor='start', size=13, fill=ROUTE_D, ls='0'))
# times: cycle k rises from PTS[2k] to PTS[2k+1], halves to PTS[2k+2]
TS, t = [GAP0], GAP0
for k in range(CYCLES):
    t += RISE; TS.append(t); t += FALL; TS.append(t)
END = TS[-1]
assert END < 12.0
for k in range(CYCLES):
    (pa, pb), t0, t1 = PTS[2 * k + 1], TS[2 * k + 1], TS[2 * k + 2]
    a(f'<g class="fx" opacity="0">{win(t0, t1 + 0.4)}<line x1="{px(0)}" y1="{py(0)}" x2="{px(pa):.1f}" y2="{py(pb):.1f}" stroke="{ROUTE_D}" stroke-width="1" stroke-dasharray="2 3"/></g>')
# the dot
ex, ey = px(PTS[-1][0]) - px(PTS[0][0]), py(PTS[-1][1]) - py(PTS[0][1])
kx = [(0.0, ex), (0.3, ex), (0.305, 0.0)] + [(TS[i], px(PTS[i][0]) - px(PTS[0][0])) for i in range(len(PTS))] + [(D, ex)]
ky = [(0.0, ey), (0.3, ey), (0.305, 0.0)] + [(TS[i], py(PTS[i][1]) - py(PTS[0][1])) for i in range(len(PTS))] + [(D, ey)]
a(f'<g>{T.translate(kx, "x")}<g>{T.translate(ky, "y")}<circle class="fx" cx="{px(PTS[0][0]):.1f}" cy="{py(PTS[0][1]):.1f}" r="7" fill="{RED}" stroke="#fff" stroke-width="1.5"/></g></g>')
# labels on the first cycle's two moves
a(text(px(25.3), py(8.6), '+1 each', anchor='start', size=13, fill=ROUTE_D, ls='0'))
a(text(px(18), py(2.2), 'both ×½', anchor='middle', size=13, fill=ROUTE_D, ls='0'))
# the gaps, lit as each halving lands
GY = 22
a(text(X0 - 8, GY, 'gap A − B:', anchor='start', size=13, fill=INK_SOFT, ls='0'))
gx = X0 - 8 + 11 * 8
for k, g in enumerate(GAPS):
    s = ('18', '9', '4.5', '2.25', '1.1')[k]
    assert abs(float(s) - g) < 0.06
    a(text(gx, GY, s, anchor='start', size=13, fill=INK_SOFT, ls='0'))
    lit_at = GAP0 if k == 0 else TS[2 * k]
    a(f'<g class="fx" opacity="0">{win(lit_at, None)}{text(gx, GY, s, anchor="start", size=13, fill=RED, ls="0", extra=" font-weight=\"700\"")}</g>')
    gx += len(s) * 8 + 16
a('</svg>')
svg = '\n'.join(o)

caption = ('Adding one segment to each flow per round trip keeps the gap between them; halving both on a loss halves it. Every loss brings the pair closer to equal shares while each peak still fills the link, though neither flow knows the other exists.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The plane.</b> Flow A's window across, flow B's up. On the blue line the link is exactly full; on the green line the two are equal. The target is where they cross: AIMD ends up oscillating along the green line, its peaks closing in on the target.</li>
          <li><b>The two moves.</b> <em>Additive increase</em> adds the same amount to both, so the point moves at 45° and the gap stays. <em>Multiplicative decrease</em> halves both, so the point slides toward the origin along its own ray and the gap halves.</li>
          <li><b>This run.</b> Capacity 32, start A 22 and B 4, both flows losing at the same moment, as in Chiu and Jain's model. Real flows with different round-trip times converge less neatly.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-10-6">
      <div class="diagram-label">Fig 10.6 · AIMD's fairness, in phase space</div>
      {svg}
      <p id="ch10-aimd-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    print(PTS, GAPS, TS)
    splice('part-3', 'fig-10-6', 'ch10-aimd-p9', card)
