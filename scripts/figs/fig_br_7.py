# Fig BR.7 · The physical address space (Pass 31, Part I, from an empty script). Job: function. Takeaway: devices sit at
# addresses among the RAM, so an ordinary store can change the screen or set a timer.
# Concept: the physical address map as one column, low addresses at the bottom, RAM and the device ranges stacked in it;
# beside each range what a store there does, drawn as the thing it touches (a value kept, a pixel, a packet, a clock).
# The CPU runs the same store four times with four addresses (Part I's step verb); the range it lands in gets the gold
# frame and its effect lights. t=0 is the store into the local APIC, which sets the timer.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 384
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
STEP = 2.5
D = STEP * 4
T = Timeline(D, shift=STEP * 3 + 1.2)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
MX, MW = 20, 170
REG = [('boot code', '0xFF00_0000', 66, 44), ('local APIC', '0xFEE0_0000', 110, 44), ('interrupt router', '0xFEC0_0000', 154, 44),
       ('network card', '0xD000_0000', 198, 44), ('GPU frame buffer', '0xC000_0000', 242, 44), ('RAM', '0x0000_0000', 286, 64)]
# the four stores: (region index, address, effect colour)
STORES = [(5, '0x0040_1000', GREEN), (4, '0xC000_2a00', BLUE), (3, '0xD000_0010', BLUE), (1, '0xFEE0_0380', GOLD)]
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-49 svgd-part1-49"{T.steps([(1.2, 'RAM'), (3.7, 'pixel'), (6.2, 'packet'), (8.7, 'timer')])}>')
a('<title id="svgt-part1-49">Fig BR.7 · The physical address space · devices among the RAM</title>')
a('<desc id="svgd-part1-49">The lowest 4 GiB of a typical PC\'s physical address map, top to bottom: the read-only boot code (firmware) just '
  'below 4 GiB, the local APIC at 0xFEE0_0000, the interrupt router (IO-APIC) that passes device interrupts to the cores at 0xFEC0_0000, '
  'a network card\'s registers and the GPU\'s frame buffer in a PCIe window, and RAM from address zero. The CPU runs the same store '
  'instruction four times with four addresses: into RAM, where the value is simply stored; into the frame buffer, where a pixel '
  'changes; into the network card\'s registers, which sends a packet; and into the local APIC, which sets the timer\'s rate.</desc>')

# the CPU and the store it runs
a(f'<rect x="20" y="14" width="360" height="38" rx="7" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
a(text(32, 38, 'CPU', size=15, fill=BLUE))
for k, (_, addr, _) in enumerate(STORES):
    a(f'<g opacity="0">{vis([(k * STEP, (k + 1) * STEP)])}' + text(84, 38, f'store x at {addr}', size=14, fill=INK, ls='0') + '</g>')
# the map
for name, addr, y, h in REG:
    a(f'<rect x="{MX}" y="{y}" width="{MW}" height="{h - 4}" rx="4" fill="none" stroke="{EDGE}" stroke-width="1.3"/>')
    a(text(MX + 10, y + 18, name, size=14, fill=INK, ls='0'))
for k, (i, _, col) in enumerate(STORES):
    _, _, y, h = REG[i]
    a(f'<rect x="{MX - 2}" y="{y - 2}" width="{MW + 4}" height="{h}" rx="5" fill="none" stroke="{GOLD}" stroke-width="2.6" opacity="0">{vis([(k * STEP + 0.2, (k + 1) * STEP)])}</rect>')
    a(f'<path d="M {MX + MW + 4} {y + h / 2 - 2} H {MX + MW + 18}" stroke="{GOLD}" stroke-width="2" opacity="0">{vis([(k * STEP + 0.2, (k + 1) * STEP)])}</path>')

# what each store does, drawn as what it touches
EX = 204
def effect(i, k, draw, words, col):
    _, _, y, h = REG[i]
    cy = y + h / 2 - 2
    on = vis([(k * STEP + 0.5, (k + 1) * STEP)])
    a(f'<g>{T.discrete("opacity", [(0.0, 1), (k * STEP + 0.5, 0), ((k + 1) * STEP, 1)])}{draw(cy)}' + text(EX + 40, cy + 5, words, size=14, fill=MUTED, ls='0') + '</g>')
    a(f'<g opacity="0">{on}{draw(cy, lit=True)}' + text(EX + 40, cy + 5, words, size=14, fill=col, ls='0') + '</g>')
def clock(cy, lit=False):
    c = GOLD
    return (f'<circle cx="{EX + 14}" cy="{cy}" r="12" fill="none" stroke="{c}" stroke-width="{2.2 if lit else 1.5}"/>'
            f'<path d="M {EX + 14} {cy} V {cy - 7} M {EX + 14} {cy} L {EX + 19} {cy + 3}" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>')
def packet(cy, lit=False):
    return (f'<rect x="{EX + 2}" y="{cy - 9}" width="22" height="18" rx="3" fill="none" stroke="{BLUE}" stroke-width="{2.2 if lit else 1.5}"/>'
            f'<path d="M {EX + 26} {cy} h 6 m -3 -3 l 3 3 l -3 3" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
def screen(cy, lit=False):
    s = f'<rect x="{EX}" y="{cy - 11}" width="30" height="22" rx="2" fill="none" stroke="{BLUE}" stroke-width="{2.2 if lit else 1.5}"/>'
    if lit: s += f'<rect x="{EX + 17}" y="{cy - 4}" width="6" height="6" fill="{GOLD}"/>'
    return s
def cell(cy, lit=False):
    s = f'<rect x="{EX + 2}" y="{cy - 11}" width="26" height="22" rx="3" fill="none" stroke="{GREEN}" stroke-width="{2.2 if lit else 1.5}"/>'
    if lit: s += text(EX + 15, cy + 5, 'x', anchor='middle', size=14, fill=GREEN, role='object')
    return s
effect(5, 0, cell, 'value', GREEN)
effect(4, 1, screen, 'pixel', BLUE)
effect(3, 2, packet, 'packet', BLUE)
effect(1, 3, clock, 'timer', GOLD)
a(text(20, 374, 'low addresses at the bottom, not to scale', size=14, fill=MUTED, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = 'One store instruction, four addresses: a value kept, a pixel, a packet, a timer.'
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Who routes it.</b> The CPU's address decoding sends each access to RAM, to a unit inside the CPU (the local APIC), or out to the device that claimed that range at boot; the addresses shown are typical, and every machine's map differs.</li>
          <li><b>Who may touch it.</b> These are physical addresses, after the MMU's translation (Fig BR.4); only the kernel maps device ranges into an address space, so a user program cannot reach a device's registers directly.</li>
          <li><b>Not cached.</b> Device registers are marked uncacheable, so every store really reaches the device; a frame buffer is write-combining, which batches stores but still sends them all.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-7">
      <div class="diagram-label">Fig BR.7 · The physical address space · devices among the RAM</div>
      {svg}
      <p id="chBridge-io-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-7', 'chBridge-io-p3', card)
