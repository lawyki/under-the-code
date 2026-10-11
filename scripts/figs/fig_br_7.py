# Fig BR.7 · The physical address space · devices among the RAM (Pass 28, law 3, conceptual pass). The bottom 4 GiB of a
# typical PC's physical address map as a column (addresses vary by machine): RAM from 0, a PCIe window with the GPU's
# frame buffer and a network card's registers, the IO-APIC at 0xFEC0_0000, the local APIC at 0xFEE0_0000, firmware
# just below 4 GiB. The CPU issues the same store instruction four times with four addresses; each lands in a different
# region and does a different thing. t=0 (shift): all four effects shown.
from figlib import Timeline, text, splice, MONO, GOLD, BLUE, GREEN, RED, MUTED

REG = [  # (label, address shown, height, colour)
    ('firmware ROM', '0xFF00_0000', 46, MUTED), ('local APIC', '0xFEE0_0000', 46, GOLD), ('IO-APIC', '0xFEC0_0000', 46, GOLD),
    ('network card', '0xC010_0000', 46, BLUE), ('GPU frame buffer', '0xC000_0000', 46, BLUE), ('RAM', '0x0000_0000', 70, GREEN)]
STORES = [(5, '0x0040_1000', 'stored, nothing else', GREEN), (4, '0xC000_0400', 'a pixel changes', BLUE),
          (3, '0xC010_0018', 'a packet is sent', BLUE), (1, '0xFEE0_0380', 'timer rate set', GOLD)]
W = 400
D = 12.0
T = Timeline(D, shift=11.4)
TS = [1.0 + 2.4 * k for k in range(4)]
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
# the CPU and its instruction
a(f'<rect x="20" y="12" width="360" height="40" rx="6" fill="{BLUE}" fill-opacity="0.08" stroke="{BLUE}" stroke-opacity="0.6"/>')
a(text(32, 37, 'CPU:', size=13, fill=BLUE, ls='0'))
for k, (_, addr, _, _) in enumerate(STORES):
    t1 = TS[k + 1] if k + 1 < len(STORES) else None
    body = text(80, 37, f'mov [{addr}], x', size=13, fill='#fff', ls='0')
    vis = (first(t1) if k == 0 else lit(TS[k], t1)) if t1 else win(TS[k])
    a(f'<g opacity="0">{vis}{body}</g>')
# the map
MX, MW = 20, 196
y = 76
ys = []
for lab, addr, h, col in REG:
    a(f'<rect x="{MX}" y="{y}" width="{MW}" height="{h - 4}" rx="4" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>')
    a(text(MX + 10, y + h / 2 - 5, lab, size=13, fill='#fff', ls='0'))
    a(text(MX + 10, y + h / 2 + 12, 'from ' + addr, size=13, fill=MUTED, ls='0'))
    ys.append(y + (h - 4) / 2)
    y += h
a(text(MX, y + 16, 'low addresses at the bottom', size=13, fill=MUTED, ls='0'))
# effects beside the map; each store's token runs from the CPU down to its region
EX = MX + MW + 14
for k, (ri, addr, eff, col) in enumerate(STORES):
    ry = ys[ri]
    t0 = TS[k]
    a(f'<g opacity="0">{win(t0 + 0.8)}{text(EX, ry + 5, eff, size=13, fill=col, ls="0")}</g>')
    a(f'<g class="fx" opacity="0">{pulse(t0 + 0.8)}<rect x="{MX - 2}" y="{ry - REG[ri][2] / 2}" width="{MW + 4}" height="{REG[ri][2]}" rx="5" fill="none" stroke="#fff" stroke-width="2"/></g>')
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t0 + 0.8, ry - 52), (D, ry - 52)], 'y')
    a(f'<g class="fx" opacity="0">{lit(t0, t0 + 0.81)}<g>{mv}<circle cx="{MX + MW - 14}" cy="52" r="6" fill="#fff"/></g></g>')
H = y + 28
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-49 svgd-part1-49">')
o.insert(1, '<title id="svgt-part1-49">Fig BR.7 · The physical address space · devices among the RAM</title>')
o.insert(2, '<desc id="svgd-part1-49">The lowest 4 GiB of a typical PC\'s physical address map, top to bottom: firmware ROM just below 4 GiB, the local APIC at 0xFEE0_0000, the IO-APIC at 0xFEC0_0000, a network card\'s registers and the GPU\'s frame buffer in a PCIe window, and RAM from address zero. '
  'The CPU runs the same store instruction four times with four addresses: into RAM, where the value is simply stored; into the frame buffer, where a pixel changes; into the network card\'s registers, which sends a packet; and into the local APIC, which sets the timer\'s rate.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('To the CPU, physical memory is one flat range of addresses, but only some of it is RAM: other ranges belong to devices. '
           'The same store instruction saves a value, changes a pixel, sends a packet or sets the timer, depending only on the address.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Who routes it.</b> The memory controller and PCIe root complex send each access to RAM or to the device that claimed that range at boot; the addresses shown are typical, and every machine's map differs.</li>
          <li><b>Who may touch it.</b> Only the kernel maps device ranges into an address space (Fig BR.4), so a user program cannot reach a device's registers directly.</li>
          <li><b>Not cached.</b> Device ranges are marked uncacheable, so every store really reaches the device instead of waiting in a cache.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-br-7">
      <div class="diagram-label">Fig BR.7 · The physical address space · devices among the RAM</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-1.html').read()
    i = s.index('id="fig-br-7"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-1', 'fig-br-7', cap, card.replace('CAPID', cap))
