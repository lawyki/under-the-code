# Fig 6.6 · qsort vs std::sort (Pass 28, law 3). The path one comparison takes in each: qsort calls
# the comparator through a pointer (call, load, cmp, ret, test); std::sort has it inlined (cmp, jge).
# A token steps through each path at the same rate; the shorter path comes round more often.
# t=0: both paths drawn, the first step lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 240
STEP = 0.4
QS = ['call', 'load', 'cmp', 'ret', 'test']
SS = ['cmp', 'jge']
D = STEP * 10            # 2 qsort comparisons, 5 std::sort comparisons
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def first(t1):
    return T.anim('opacity', [(0.0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-42 svgd-part2-42">')
a('<title id="svgt-part2-42">Fig 6.6 · qsort vs std::sort, same algorithm, different cost</title>')
a('<desc id="svgd-part2-42">The path of one comparison. C\'s qsort calls the comparison function through a pointer, so each comparison is five steps: call, load the two values, compare, return, test the result. '
  'C++\'s std::sort is compiled for the exact comparison, which is inlined into the loop: compare and branch, two steps. A marker stepping through both paths at the same rate completes two comparisons in qsort while std::sort completes five.</desc>')
def lane(y, title, code, steps, col, note):
    a(text(20, y, title, size=13, fill=MUTED, ls='0'))
    a(text(20, y + 20, code, size=13, fill='#fff', ls='0'))
    cy = y + 34
    n = len(steps)
    for k, s in enumerate(steps):
        x = 20 + k * 74
        a(f'<rect x="{x}" y="{cy}" width="64" height="32" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.6"/>')
        a(text(x + 32, cy + 21, s, anchor='middle', size=13, fill='#fff', ls='0'))
        if k < n - 1:
            a(f'<line x1="{x + 64}" y1="{cy + 16}" x2="{x + 74}" y2="{cy + 16}" stroke="{col}" stroke-opacity="0.5"/>')
        for c in range(int(round(D / (STEP * n)))):
            t0 = (c * n + k) * STEP
            g = f'<rect class="fx" x="{x}" y="{cy}" width="64" height="32" rx="3" fill="{col}" fill-opacity="0.3" stroke="{col}" stroke-width="2.5" opacity="0">'
            a(g + (first(t0 + STEP) if t0 == 0 else win(t0, t0 + STEP)) + '</rect>')
    a(text(20, cy + 54, note, size=13, fill=col, ls='0'))
lane(20, 'C · compiled once, in the library', 'qsort(v, n, sizeof(int), cmp);', QS, GOLD, 'every comparison is a call')
lane(140, 'C++ · compiled for this comparison', 'std::sort(v.begin(), v.end());', SS, PHOS, 'the comparison is inlined')
a('</svg>')
svg = '\n'.join(o)

caption = ('<code>qsort</code> reaches the comparison through a function pointer, so every comparison is a call the compiler cannot see into; <code>std::sort</code> is compiled for the exact comparison, which becomes two instructions in the loop. '
           'Same algorithm, a shorter path per comparison, paid for with a separate copy of the sort for each comparison type.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why C cannot inline.</b> <code>qsort</code> was compiled into the C library long before your comparison function existed, so it can only call it.</li>
          <li><b>Templates.</b> <code>std::sort</code> is compiled at your call site with the comparison's type known, so the optimiser folds it into the loop; on a million integers it typically runs about three times faster.</li>
          <li><b>A trap in C.</b> The usual comparator <code>return *(int*)a - *(int*)b;</code> overflows for large values; <code>(x &gt; y) - (x &lt; y)</code> is safe.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-6">
      <div class="diagram-label">Fig 6.6 · qsort vs std::sort, same algorithm, different cost</div>
      {svg}
      <p id="ch6-zerocost-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-6', 'ch6-zerocost-p3', card)
