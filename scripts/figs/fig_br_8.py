# Fig BR.8 · Direct memory access (Pass 31, Part I, from an empty script). Job: function. Takeaway: the device copies data
# into RAM by itself, so the CPU runs other work until an interrupt says done.
# Concept: CPU, SSD and RAM, and the read in its three steps, each lit as it happens (Part I's light verb): the kernel
# puts a command in the queue in RAM and rings the SSD's doorbell; the SSD streams the data into the buffer block by block
# by itself (flow) while the CPU runs process B; the SSD raises an interrupt and process A is woken. t=0 is the end.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 228
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=10.4)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
S1, S2, S3 = (0.4, 2.4), (2.6, 7.4), (7.6, D)
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-50 svgd-part1-50"{T.steps([(1.8, 'queue'), (5.5, 'fill'), (9.0, 'done')])}>')
a('<title id="svgt-part1-50">Fig BR.8 · Direct memory access · the device writes RAM by itself</title>')
a('<desc id="svgd-part1-50">A disk read by direct memory access. Process A asks for data; the kernel puts a small command in a queue in RAM '
  '(read these blocks into the buffer at 0x4a20_0000) and rings the SSD\'s doorbell register. The SSD then streams the data straight into '
  'RAM, filling the buffer block by block, while the CPU runs process B. When the transfer is finished the SSD raises an interrupt, the '
  'kernel completes the request and wakes process A. The CPU never copies the data during the transfer.</desc>')

# CPU and SSD
a(f'<rect x="20" y="16" width="164" height="62" rx="7" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
a(text(32, 38, 'CPU', size=15, fill=BLUE))
a(f'<g opacity="0">{vis([S1])}' + text(32, 62, 'kernel: queue it', size=14, fill=GOLD, ls='0') + '</g>')
a(f'<g opacity="0">{vis([S2])}' + text(32, 62, 'B runs', size=14, fill=GREEN, ls='0') + '</g>')
a(f'<g opacity="0">{vis([S3, (0.0, 0.4)])}' + text(32, 62, 'A woken', size=14, fill=BLUE, ls='0') + '</g>')
a(f'<rect x="216" y="16" width="164" height="62" rx="7" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
a(text(228, 38, 'NVMe SSD', size=15, fill=GOLD))
# the doorbell on the SSD, rung in step 1
bx, by = 352, 50
a(f'<path d="M {bx - 9} {by + 8} Q {bx - 9} {by - 10} {bx} {by - 10} Q {bx + 9} {by - 10} {bx + 9} {by + 8} Z M {bx - 3} {by + 11} h 6" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
a(f'<g opacity="0">{vis([(1.6, 2.6)])}<path d="M {bx - 16} {by - 10} l -5 -4 M {bx + 16} {by - 10} l 5 -4 M {bx - 18} {by} h -6 M {bx + 18} {by} h 6" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round"/></g>')
a(text(228, 62, 'doorbell', size=14, fill=MUTED))

# RAM: the command queue and the buffer
a(f'<rect x="20" y="110" width="360" height="104" rx="8" fill="none" stroke="{GREEN}" stroke-width="1.5"/>')
a(text(32, 132, 'RAM', size=15, fill=GREEN))
a(f'<rect x="230" y="118" width="140" height="28" rx="5" fill="none" stroke="{EDGE}" stroke-width="1.4"/>')
a(text(300, 137, 'command queue', anchor='middle', size=14, fill=MUTED))
a(f'<rect x="230" y="118" width="140" height="28" rx="5" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{vis([(1.2, D)])}</rect>')
a(text(32, 162, 'buffer', size=14, fill=INK, ls='0'))
for k in range(8):
    x = 32 + k * 43
    t = 3.0 + k * 0.5
    a(f'<rect x="{x}" y="172" width="38" height="30" rx="4" fill="none" stroke="{EDGE}" stroke-width="1.3"/>')
    a(f'<rect x="{x + 3}" y="175" width="32" height="24" rx="3" fill="{GREEN}" opacity="0">{vis([(t + 0.4, D), (0.0, 0.4)])}</rect>')
    # each block travels from the SSD down into the buffer
    dx, dy = x + 19 - 300, 187 - 78
    a(f'<g opacity="0">{vis([(t, t + 0.45)])}<g>{T.translate([(0.0, 0), (t, 0), (t + 0.4, dx), (D - 0.01, dx)], axis="x")}'
      f'<g>{T.translate([(0.0, 0), (t, 0), (t + 0.4, dy), (D - 0.01, dy)], axis="y")}<rect x="290" y="70" width="20" height="16" rx="3" fill="{GREEN}"/></g></g></g>')
# step 1: the command travels from the CPU to the queue
a(f'<g opacity="0">{vis([(0.4, 1.3)])}<g>{T.translate([(0.0, 0), (0.4, 0), (1.2, 160), (D - 0.01, 160)], axis="x")}'
  f'<g>{T.translate([(0.0, 0), (0.4, 0), (1.2, 52), (D - 0.01, 52)], axis="y")}<rect x="120" y="74" width="20" height="16" rx="3" fill="{GOLD}"/></g></g></g>')
# step 3: the interrupt, from the SSD to the CPU
a(f'<g opacity="0">{vis([(7.6, 9.6)])}<path d="M 214 34 H 188 m 7 -5 l -7 5 l 7 5" fill="none" stroke="{RED}" stroke-width="2.4"/></g>')
a(f'<path d="M 214 34 H 188" stroke="{EDGE}" stroke-dasharray="3 4"/>')
a(text(200, 96, 'interrupt', anchor='middle', size=14, fill=RED))

a('</svg>')
svg = '\n'.join(o)

caption = 'The drive fills RAM by itself while the CPU runs B; an interrupt says done.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Scattered buffers.</b> The buffer need not be one block of RAM: the command can list many separate pages (PRP or SGL entries), and the drive fills each in turn.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-8">
      <div class="diagram-label">Fig BR.8 · Direct memory access · the device writes RAM by itself</div>
      {svg}
      <p id="chBridge-io-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-8', 'chBridge-io-p5', card)
