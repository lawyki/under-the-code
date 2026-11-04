# Fig BR.5 · The TLB (Pass 31, Part I, from an empty script). Job: function. Takeaway: programs reuse the same few
# pages, so the TLB answers most translations and the slow walk runs rarely.
# Concept: a program's twelve memory accesses, by page, stepping in one at a time (Part I's step verb) against a TLB of
# four entries. A page already there lights its entry (a hit, green) and is done at once; a new page (red) pays the
# four-read walk, and its translation replaces the entry used longest ago, tagged "oldest". The count runs below.
# t=0 is the end: ten hits, two misses.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 332
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
SEQ = [4, 4, 5, 4, 5, 6, 4, 6, 7, 7, 4, 5]
FRAME = {2: '51e0', 3: '7d10', 4: 'a200', 5: 'b731', 6: '0907', 7: 'c152'}
STEP, T0 = 0.75, 0.6
D = T0 + STEP * len(SEQ) + 2.4
T = Timeline(D, shift=D - 1.2)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
# simulate the TLB, least recently used out
slots = [2, 3, 4, 5]; last = {2: -4, 3: -3, 4: -2, 5: -1}
hist = []                                   # per step: (page, hit, slot index, slots after, oldest index after)
for k, p in enumerate(SEQ):
    if p in slots:
        i = slots.index(p); hit = True
    else:
        i = min(range(4), key=lambda j: last[slots[j]]); slots[i] = p; hit = False
    last[p] = k
    oldest = min(range(4), key=lambda j: last[slots[j]])
    hist.append((p, hit, i, list(slots), oldest))
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-47 svgd-part1-47"{T.steps([(1.75, 'a hit'), (4.75, 'a miss'), (9.35, 'the end')])}>')
a('<title id="svgt-part1-47">Fig BR.5 · The TLB · why the walk usually doesn\'t happen</title>')
a('<desc id="svgd-part1-47">A program\'s twelve memory accesses, by page (a3c4, a3c4, a3c5, a3c4, a3c5, a3c6, a3c4, a3c6, a3c7, a3c7, a3c4, '
  'a3c5), against a TLB of four entries holding recent page translations. A page already in the TLB is a hit, answered at once. A new '
  'page is a miss: the MMU pays the four-read page-table walk, and the new translation replaces the entry used longest ago. Ten hits, '
  'two misses; real programs reach well over 99% hits.</desc>')

# the accesses
a(text(20, 26, 'pages', size=14, fill=MUTED))
for k, p in enumerate(SEQ):
    x = 20 + k * 30
    _, hit, _, _, _ = hist[k]
    t = T0 + k * STEP
    a(f'<rect x="{x}" y="36" width="26" height="30" rx="4" fill="none" stroke="{EDGE}" stroke-width="1.3"/>')
    a(text(x + 13, 56, str(p), anchor='middle', size=15, fill=INK, ls='0', role='object'))
    a(f'<g opacity="0">{vis([(t + 0.3, D - 0.2)])}<rect x="{x}" y="70" width="26" height="5" rx="2" fill="{GREEN if hit else RED}"/></g>')
# the current access: a gold frame stepping along
xs = [(0.0, 0)] + [p for k in range(len(SEQ)) for p in ((T0 + k * STEP, k * 30), (T0 + k * STEP + 0.6, k * 30))] + [(D - 0.01, (len(SEQ) - 1) * 30)]
a(f'<g opacity="0">{vis([(T0, D - 0.2)])}<g>{T.translate(xs, axis="x")}<rect x="17" y="33" width="32" height="36" rx="6" fill="none" stroke="{GOLD}" stroke-width="2.4"/></g></g>')

# the TLB: four entries
a(f'<rect x="20" y="112" width="218" height="176" rx="8" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
a(text(34, 134, 'TLB', size=14, fill=GOLD))
SY = lambda i: 146 + i * 34
def spans_for(pred):
    out, start = [], None
    for k in range(len(SEQ) + 1):
        on = pred(k)
        t = 0.0 if k == 0 else T0 + (k - 1) * STEP + 0.35
        if on and start is None: start = t
        if not on and start is not None: out.append((start, t)); start = None
    if start is not None: out.append((start, D))
    return out
init = [2, 3, 4, 5]
for i in range(4):
    a(f'<rect x="32" y="{SY(i)}" width="194" height="28" rx="4" fill="none" stroke="{EDGE}" stroke-width="1.3"/>')
    for p in FRAME:
        sp = spans_for(lambda k, p=p, i=i: (init if k == 0 else hist[k - 1][3])[i] == p)
        if sp:
            a(f'<g opacity="0">{vis(sp)}' + text(42, SY(i) + 19, f'a3c{p} → {FRAME[p]}', size=14, fill=INK, ls='0', role='object') + '</g>')
    # a hit lights the entry
    hits = [(T0 + k * STEP + 0.3, T0 + k * STEP + 0.7) for k, (p, hit, j, _, _) in enumerate(hist) if hit and j == i]
    a(f'<rect x="32" y="{SY(i)}" width="194" height="28" rx="4" fill="none" stroke="{GREEN}" stroke-width="2.4" opacity="0">{vis(hits)}</rect>')
    # the entry used longest ago
    olds = spans_for(lambda k, i=i: (0 if k == 0 else hist[k - 1][4]) == i)
    a(f'<g opacity="0">{vis(olds)}' + text(220, SY(i) + 19, 'oldest', anchor='end', size=14, fill=MUTED, ls='0') + '</g>')
# the walk, paid only on a miss
a(f'<rect x="252" y="146" width="128" height="96" rx="8" fill="none" stroke="rgba(255,255,255,0.5)" stroke-dasharray="4 4"/>')
a(text(316, 172, 'page-table', anchor='middle', size=14, fill=INK))
a(text(316, 190, 'walk', anchor='middle', size=14, fill=INK))
miss = [(T0 + k * STEP + 0.1, T0 + k * STEP + 0.7) for k, (_, hit, _, _, _) in enumerate(hist) if not hit]
a(f'<rect x="252" y="146" width="128" height="96" rx="8" fill="none" stroke="{RED}" stroke-width="2.4" opacity="0">{vis(miss)}</rect>')
# the count
nh = sum(1 for h in hist if h[1]); nm = len(hist) - nh
a(text(252, 268, f'hits {nh}', size=15, fill=GREEN)); a(text(252, 290, f'misses {nm}', size=15, fill=RED))
a('</svg>')
svg = '\n'.join(o)

caption = 'Most accesses hit the TLB; only a miss pays for the walk.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Sizes.</b> From 64 entries to a few thousand per core, in one or two levels; one entry can also cover a 2 MiB or 1 GiB huge page.</li>
          <li><b>Tags.</b> On x86 the address-space tag is the PCID, so a switch of <code>CR3</code> need not empty the TLB.</li>
          <li><b>The pages.</b> The strip shows each page by its last hex digit (a3c4, a3c5 and so on); a miss costs four more memory reads.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-5">
      <div class="diagram-label">Fig BR.5 · The TLB · why the walk usually doesn't happen</div>
      {svg}
      <p id="chBridge-mmu-p6" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-5', 'chBridge-mmu-p6', card)
