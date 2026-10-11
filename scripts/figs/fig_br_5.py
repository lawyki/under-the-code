# Fig BR.5 · The TLB · why the walk usually doesn't happen (Pass 28, law 3, conceptual pass). Twelve accesses from a
# program working through a few pages, through a four-entry TLB (least recently used is evicted), simulated here. Each
# access names its virtual page; a hit returns the frame at once, a miss runs the four-level walk and loads the entry,
# evicting the oldest. Hits and misses are counted as they happen: 10 hits, 2 misses here; real programs, with far longer
# runs and larger TLBs, usually hit more than 99% of the time. t=0 (shift): all twelve done.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

PAGES = ['a3c4', 'a3c4', 'a3c5', 'a3c4', 'a3c5', 'a3c6', 'a3c4', 'a3c6', 'a3c7', 'a3c7', 'a3c4', 'a3c5']
FRAME = {'a3c4': 'a200', 'a3c5': 'b731', 'a3c6': '0907', 'a3c7': 'c152'}       # a3c4 → a200 as in Fig BR.4
INIT = ['a3c4', 'a3c5', 'b210', 'b211']
# simulate LRU
tlb, events, slots_hist = INIT[:], [], []
last = {p: -1 for p in tlb}
for i, p in enumerate(PAGES):
    if p in tlb:
        events.append(('hit', None)); last[p] = i
    else:
        victim = min(tlb, key=lambda q: last[q])
        k = tlb.index(victim); tlb[k] = p; last[p] = i
        events.append(('miss', k))
    slots_hist.append(tlb[:])
HITS = sum(e == 'hit' for e, _ in events)
assert (HITS, len(PAGES) - HITS) == (10, 2)
W = 400
D = 14.0
T = Timeline(D, shift=13.4)
STEP, T0 = 0.9, 0.8
ts = lambda i: T0 + STEP * i
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# the access stream
a(text(20, 22, 'virtual pages the program touches', size=13, fill=MUTED, ls='0'))
CW = 30
for i, p in enumerate(PAGES):
    x = 20 + i * CW
    hit = events[i][0] == 'hit'
    a(f'<rect x="{x}" y="32" width="{CW - 4}" height="26" rx="4" fill="none" stroke="{BLUE}" stroke-opacity="0.5"/>')
    a(text(x + (CW - 4) / 2, 50, p[-1], anchor='middle', size=13, fill='#fff', ls='0'))
    mark = f'<rect x="{x}" y="62" width="{CW - 4}" height="6" rx="2" fill="{GREEN if hit else RED}"/>'
    a(f'<g opacity="0">{win(ts(i))}{mark}</g>')
    a(f'<g class="fx" opacity="0">{lit(ts(i), ts(i) + STEP)}<rect x="{x - 2}" y="30" width="{CW}" height="30" rx="5" fill="none" stroke="#fff" stroke-width="2"/></g>')
a(text(20, 88, 'page a3c? (last digit shown)', size=13, fill=MUTED, ls='0'))
# the TLB
TY = 112
a(f'<rect x="20" y="{TY}" width="360" height="152" rx="6" fill="{GOLD}" fill-opacity="0.06" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(text(32, TY + 22, 'TLB · four entries', size=13, fill=GOLD, ls='0'))
SY = lambda k: TY + 34 + k * 28
for k in range(4):
    a(f'<rect x="32" y="{SY(k)}" width="200" height="24" rx="4" fill="none" stroke="{MUTED}" stroke-opacity="0.6"/>')
    # value over time: before the first access, then after each access
    seq = [INIT[k]] + [h[k] for h in slots_hist]
    spans, cur, start = [], seq[0], 0.31
    for i in range(1, len(seq)):
        if seq[i] != cur:
            spans.append((cur, start, ts(i - 1))); cur, start = seq[i], ts(i - 1)
    spans.append((cur, start, None))
    for p, t0, t1 in spans:
        lab = f'{p} → {FRAME.get(p, "51e" + p[-1])}'
        body = text(42, SY(k) + 17, lab, size=13, fill='#fff', ls='0')
        vis = win(t0) if t1 is None else (first(t1) if t0 < 0.5 else lit(t0, t1))
        a(f'<g opacity="0">{vis}{body}</g>')
for i, (e, k) in enumerate(events):
    if e == 'miss':
        a(f'<g class="fx" opacity="0">{pulse(ts(i))}<rect x="30" y="{SY(k) - 2}" width="204" height="28" rx="5" fill="none" stroke="{RED}" stroke-width="2"/></g>')
# the walk, lit on each miss
a(f'<rect x="250" y="{SY(0)}" width="118" height="108" rx="5" fill="none" stroke="{MUTED}" stroke-opacity="0.5" stroke-dasharray="4 3"/>')
a(text(309, SY(0) + 22, 'page-table', anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(309, SY(0) + 40, 'walk', anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(309, SY(0) + 70, '4 extra', anchor='middle', size=13, fill=MUTED, ls='0'))
a(text(309, SY(0) + 88, 'memory reads', anchor='middle', size=13, fill=MUTED, ls='0'))
for i, (e, k) in enumerate(events):
    if e == 'miss':
        a(f'<g class="fx" opacity="0">{lit(ts(i), ts(i) + 0.7)}<rect x="250" y="{SY(0)}" width="118" height="108" rx="5" fill="{RED}" fill-opacity="0.18" stroke="{RED}" stroke-width="2"/></g>')
# the tally
RY = TY + 182
h = m = 0
for i, (e, _) in enumerate(events):
    h += e == 'hit'; m += e == 'miss'
    t1 = ts(i + 1) if i + 1 < len(events) else None
    body = text(20, RY, f'hits {h}', size=13, fill=GREEN, ls='0') + text(120, RY, f'misses {m}', size=13, fill=RED, ls='0')
    vis = win(ts(i)) if t1 is None else lit(ts(i), t1)
    a(f'<g opacity="0">{vis}{body}</g>')
a(text(20, RY + 22, 'real programs: well over 99% hits', size=13, fill=MUTED, ls='0'))
H = RY + 34
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-47 svgd-part1-47">')
o.insert(1, '<title id="svgt-part1-47">Fig BR.5 · The TLB · why the walk usually doesn\'t happen</title>')
o.insert(2, '<desc id="svgd-part1-47">Twelve memory accesses from a program working through a few pages, run through a four-entry TLB. Most name a page the TLB already holds and are translated at once. '
  'Two name a page it does not hold: each of those runs the page-table walk, four extra memory reads, and loads the translation into the TLB, replacing the entry used longest ago. The count ends at ten hits and two misses; real programs usually hit well over 99% of the time.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Programs touch the same few pages again and again, so the TLB, a small cache of recent translations, can answer most accesses at once. '
           'Only a miss pays for the four-read walk, and then the new translation replaces the entry used longest ago.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Sizes.</b> From 64 entries to a few thousand per core, in one or two levels; one entry can also cover a 2 MiB or 1 GiB huge page.</li>
          <li><b>Keeping it true.</b> When the kernel changes a page-table entry it must drop the stale translation (<code>INVLPG</code> on x86), on every core that might hold it.</li>
          <li><b>Switching processes.</b> Each process has its own tables; tagging entries with an address-space ID (PCID on x86) lets the TLB keep them through a switch.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-5">
      <div class="diagram-label">Fig BR.5 · The TLB · why the walk usually doesn't happen</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-5', cap, card.replace('CAPID', cap))
