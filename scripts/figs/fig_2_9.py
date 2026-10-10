# Fig 2.9 · A signed overflow becomes a buffer overflow (Pass 28, law 3). The code, then the
# three steps when it is called with n = −1: the check passes; the cast to size_t turns 32 ones
# into 64 ones, 2^64 − 1 bytes on a 64-bit machine; the copy runs out of the 256-byte buffer
# across its neighbours. (The old figure mixed this with 32-bit size_t's 4,294,967,295.)
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 440
T = Timeline(9, shift=8.2)
def show(t0, t1=8.9):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.999, 0.0)])
def hi(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (t1 - 0.002, 1.0), (t1 - 0.001, 0.0), (8.999, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-25 svgd-part1-25">')
a('<title id="svgt-part1-25">Fig 2.9 · How a signed overflow becomes a buffer overflow</title>')
a('<desc id="svgd-part1-25">A copy function checks that n is not more than 256, then calls memcpy with n. Called with n = −1, the check passes because −1 is less than 256. '
  'memcpy takes its length as an unsigned size_t, and on a 64-bit machine the 32 one-bits of −1 become 64 one-bits: 18,446,744,073,709,551,615. '
  'The copy runs out of the 256-byte buffer and over everything after it.</desc>')
# the code
a('<rect x="12" y="12" width="376" height="94" rx="6" fill="#141414" stroke="rgba(255,255,255,0.2)"/>')
CODE = [('int copy(char *dst, char *src, int n) {', 0), ('if (n > 256) return -1;', 1), ('memcpy(dst, src, n);', 1), ('}', 0)]
for i, (line, ind) in enumerate(CODE):
    a(f'<text x="{24 + ind * 18}" y="{34 + i * 20}" {MONO} font-size="13.5" fill="rgba(255,255,255,0.88)">{line.replace("<", "&lt;").replace(">", "&gt;")}</text>')
a(f'<rect x="38" y="40" width="200" height="20" rx="3" fill="none" stroke="{GOLD}" stroke-width="1.6" opacity="0">{hi(0.6, 2.4)}</rect>')
a(f'<rect x="38" y="60" width="176" height="20" rx="3" fill="none" stroke="{GOLD}" stroke-width="1.6" opacity="0">{hi(2.4, 5.6)}</rect>')
a(text(20, 132, 'called with  n = −1', size=15, fill=RED, ls='0'))
# step 1: the check
a(f'<circle cx="28" cy="164" r="11" fill="none" stroke="rgba(255,255,255,0.5)"/>'); a(text(28, 169, '1', anchor='middle', size=13, fill='#fff', ls='0'))
a(text(48, 169, 'the check: −1 > 256?', size=15, fill='#fff', ls='0'))
a(f'<text x="380" y="169" text-anchor="end" {MONO} font-size="15" fill="{GREEN}" opacity="0">no, so on{show(1.2)}</text>')
# step 2: the cast
a(f'<circle cx="28" cy="206" r="11" fill="none" stroke="rgba(255,255,255,0.5)"/>'); a(text(28, 211, '2', anchor='middle', size=13, fill='#fff', ls='0'))
a(text(48, 211, 'the cast to size_t', size=15, fill='#fff', ls='0'))
def bitbar(y, n, col, t0):
    w = 340 / 64
    for k in range(n):
        a(f'<rect x="{48 + k * w:.2f}" y="{y}" width="{w - 0.8:.2f}" height="16" fill="{col}" opacity="0">{show(t0 + k * 0.012)}</rect>')
a(text(48, 238, 'int: 32 ones = −1', size=14, fill=MUTED, ls='0'))
bitbar(244, 32, BLUE, 2.6)
a(text(48, 280, 'size_t: 64 ones =', size=14, fill=MUTED, ls='0'))
bitbar(286, 64, RED, 3.4)
a(f'<text x="48" y="324" {MONO} font-size="15" fill="{RED}" opacity="0">18,446,744,073,709,551,615{show(4.4)}</text>')
# step 3: the write, out of the buffer and over its neighbours
a(f'<circle cx="28" cy="352" r="11" fill="none" stroke="rgba(255,255,255,0.5)"/>'); a(text(28, 357, '3', anchor='middle', size=13, fill='#fff', ls='0'))
a(text(48, 357, 'the copy', size=15, fill='#fff', ls='0'))
MEM = [(20, 92, 'buffer'), (116, 80, 'next'), (200, 84, 'next'), (288, 92, '…')]
for x, w, lab in MEM:
    a(f'<rect x="{x}" y="374" width="{w}" height="40" rx="4" fill="#161616" stroke="rgba(255,255,255,{0.6 if lab == "buffer" else 0.25})"/>')
    a(text(x + w / 2, 399, lab, anchor='middle', size=14, fill='#fff' if lab == 'buffer' else MUTED, ls='0'))
a(text(20, 432, '256 bytes', size=13, fill=MUTED))
a(f'<rect class="fx" x="20" y="374" height="40" rx="4" fill="{RED}" fill-opacity="0.45" stroke="{RED}">'
  f'{T.anim("width", [(0.0, 360), (5.4, 0.0), (5.401, 2.0), (7.4, 360), (8.999, 360)])}'
  f'{T.anim("opacity", [(0.0, 1.0), (5.39, 1.0), (5.4, 0.0), (5.401, 1.0), (8.999, 1.0)])}</rect>')
a(f'<text x="380" y="432" text-anchor="end" {MONO} font-size="14" fill="{RED}" opacity="0">and on, over everything{show(6.6)}</text>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A length check that looks safe: called with −1, it passes, because −1 is less than 256. '
           'Then memcpy takes the length as an unsigned size_t, eighteen quintillion on a 64-bit machine, and copies far past the 256-byte buffer.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The check.</b> n is a signed int, so −1 &gt; 256 is false and the early return is skipped.</li>
          <li><b>The cast.</b> memcpy's length is a size_t, unsigned. On a 64-bit machine the 32-bit −1 is widened to 64 bits, all ones: 2<sup>64</sup> − 1.</li>
          <li><b>The write.</b> The copy overruns the buffer and smashes whatever lies after it, the start of the memory-corruption attacks of Chapter 3.</li>
          <li><b>The fix.</b> Use an unsigned type for sizes, or check n &lt; 0 as well as n &gt; 256.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-2-9">
      <div class="diagram-label">Fig 2.9 · How a signed overflow becomes a buffer overflow</div>
      {svg}
      <p id="ch2-twos-p11" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-2-9', 'ch2-twos-p11', card)
