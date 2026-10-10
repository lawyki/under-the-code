# Fig 1.12 · Speculative execution (Pass 28, law 3). One branch, played twice:
# act 1 the guess is right and the work is kept; act 2 it is wrong, the guessed path is thrown
# away and the other runs, but the speculative load's cache line stays: the trace Spectre reads.
# t=0: the end of act 2.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

W, H = 400, 356
T = Timeline(10, shift=9.0)
def win(t0, t1, lo=0.0, hi=1.0):
    return T.anim('opacity', [(0.0, lo), (t0 - 0.001, lo), (t0, hi), (t1 - 0.002, hi), (t1 - 0.001, lo), (9.999, lo)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-13 svgd-part1-13">')
a('<title id="svgt-part1-13">Fig 1.12 · Speculative execution · the CPU guesses, then checks</title>')
a('<desc id="svgd-part1-13">A branch, jne loop_start, whose condition is not known yet. The CPU guesses and runs the guessed path ahead: add, load, compare; the load brings a line into the cache. '
  'When the guess is right the work is kept. When it is wrong the guessed path is thrown away and the other path runs, but the cache line the load brought in is still there.</desc>')
# the branch
a(f'<rect x="96" y="14" width="208" height="40" rx="6" fill="#1a1200" stroke="{GOLD}" stroke-opacity="0.6"/>')
a(f'<text x="186" y="40" text-anchor="middle" {MONO} font-size="16" fill="#fff">jne loop_start</text>')
a('<circle cx="282" cy="34" r="11" fill="#222" stroke="rgba(255,255,255,0.4)"/>')
a(f'<text x="282" y="39" text-anchor="middle" {MONO} font-size="14" fill="#fff">?{T.anim("opacity", [(0.0, 0.0), (0.001, 1.0), (2.199, 1.0), (2.2, 0.0), (5.0, 0.0), (5.001, 1.0), (7.199, 1.0), (7.2, 0.0), (9.999, 0.0)])}</text>')
a(f'<text x="282" y="39" text-anchor="middle" {MONO} font-size="14" fill="{GREEN}" opacity="0">✓{win(2.2, 5.0)}</text>')
a(f'<text x="282" y="39" text-anchor="middle" {MONO} font-size="14" fill="{RED}" opacity="0">✗{T.anim("opacity", [(0.0, 1.0), (0.0005, 0.0), (7.2, 0.0), (7.201, 1.0), (9.999, 1.0)])}</text>')
a('<path d="M 200 54 V 66 M 105 76 V 66 H 295 V 76" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>')
# the two paths
a(text(20, 96, 'guessed path', size=14, fill=GOLD))
a(text(210, 96, 'other path', size=14, fill=MUTED))
G = ['add eax, 1', 'load [ebx]', 'cmp ecx, 0']
O = ['mov eax, 0', 'jmp exit']
for i, ins in enumerate(G):
    y = 106 + i * 36
    a(f'<rect x="20" y="{y}" width="170" height="30" rx="4" fill="#151515" stroke="rgba(255,255,255,0.18)"/>')
    # speculative (dashed) while the condition is unknown; solid when kept; struck when thrown away
    a(f'<rect x="20" y="{y}" width="170" height="30" rx="4" fill="{GOLD}" fill-opacity="0.08" stroke="{GOLD}" stroke-dasharray="4 3" opacity="0">'
      f'{T.anim("opacity", [(0.0, 0.0), (0.4 + i * 0.4, 0.0), (0.401 + i * 0.4, 1.0), (2.4, 1.0), (2.401, 0.0), (5.4 + i * 0.4, 0.0), (5.401 + i * 0.4, 1.0), (7.2, 1.0), (7.201, 0.0), (9.999, 0.0)])}</rect>')
    a(f'<rect x="20" y="{y}" width="170" height="30" rx="4" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}" opacity="0">{win(2.4, 4.8)}</rect>')
    a(f'<text x="34" y="{y + 20}" {MONO} font-size="14" fill="#fff">{ins}'
      f'{T.anim("opacity", [(0.0, 0.3), (0.4 + i * 0.4, 0.3), (0.401 + i * 0.4, 1.0), (4.8, 1.0), (4.801, 0.3), (5.4 + i * 0.4, 0.3), (5.401 + i * 0.4, 1.0), (7.2, 1.0), (7.201, 0.3), (9.999, 0.3)])}</text>')
    a(f'<line x1="30" y1="{y + 15}" x2="180" y2="{y + 15}" stroke="{RED}" stroke-width="2" opacity="0">'
      f'{T.anim("opacity", [(0.0, 1.0), (0.0005, 0.0), (7.2, 0.0), (7.201, 1.0), (9.999, 1.0)])}</line>')
for i, ins in enumerate(O):
    y = 106 + i * 36
    a(f'<rect x="210" y="{y}" width="170" height="30" rx="4" fill="#151515" stroke="rgba(255,255,255,0.18)"/>')
    a(f'<rect x="210" y="{y}" width="170" height="30" rx="4" fill="{BLUE}" fill-opacity="0.22" stroke="{BLUE}" opacity="0">'
      f'{T.anim("opacity", [(0.0, 1.0), (0.0005, 0.0), (7.5 + i * 0.4, 0.0), (7.501 + i * 0.4, 1.0), (9.999, 1.0)])}</rect>')
    a(f'<text x="224" y="{y + 20}" {MONO} font-size="14" fill="#fff">{ins}'
      f'{T.anim("opacity", [(0.0, 1.0), (0.0005, 0.35), (7.5 + i * 0.4, 0.35), (7.501 + i * 0.4, 1.0), (9.999, 1.0)])}</text>')
# the cache: the speculative load brings a line in; it stays when the work is thrown away
a(text(20, 232, 'CACHE', size=13, fill=MUTED))
for c in range(6):
    x = 20 + c * 61
    a(f'<rect x="{x}" y="240" width="55" height="26" rx="3" fill="#181818" stroke="rgba(255,255,255,0.2)"/>')
a(f'<rect x="142" y="240" width="55" height="26" rx="3" fill="{GOLD}" fill-opacity="0.75">'
  f'{T.anim("opacity", [(0.0, 1.0), (0.8, 0.0), (0.801, 1.0), (4.8, 1.0), (4.801, 0.0), (5.8, 0.0), (5.801, 1.0), (9.999, 1.0)])}</rect>')
a(f'<rect x="139" y="237" width="61" height="32" rx="5" fill="none" stroke="{RED}" stroke-width="2" opacity="0">{win(7.3, 9.999)}</rect>')
a(f'<text x="169" y="288" text-anchor="middle" {MONO} font-size="14" fill="{RED}" opacity="0">still there{win(7.3, 9.999)}</text>')
# the two outcomes, both always shown
for k, (head, sub, col, t0, t1) in enumerate((('right · ~95%', 'keep the work', GREEN, 2.4, 4.8), ('wrong · ~5%', 'throw it away', RED, 7.2, 9.999))):
    x = 20 + k * 184
    a(f'<rect x="{x}" y="300" width="176" height="50" rx="6" fill="#121212" stroke="rgba(255,255,255,0.18)"/>')
    a(f'<rect x="{x}" y="300" width="176" height="50" rx="6" fill="none" stroke="{col}" stroke-width="1.8" opacity="0">{win(t0, t1)}</rect>')
    a(text(x + 12, 320, head, size=14, fill=col, ls='0'))
    a(text(x + 12, 340, sub, size=14, fill='rgba(255,255,255,0.75)', ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('At a branch the CPU guesses which way it will go and runs ahead; a right guess keeps the work, a wrong one throws it away and takes the other path. '
           'Thrown-away work can still leave its mark in the cache: the trace that Spectre and Meltdown read.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Why guess.</b> Waiting for the condition would leave the pipeline idle for many cycles.</li>
          <li><b>The guess.</b> Made from the branch's history; modern CPUs are right about 95% of the time.</li>
          <li><b>The catch.</b> Throwing work away rolls back the registers, not the cache. A load that should never have run leaves its data behind, and an attacker can time the cache to find it.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-1-12">
      <div class="diagram-label">Fig 1.12 · Speculative execution · the CPU guesses, then checks</div>
      {svg}
      <p id="ch1-cpu-p10" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-1-12', 'ch1-cpu-p10', card)
