# Fig BR.3 · The interrupt descriptor table (Pass 31, Part I, from an empty script; it replaces a kept original that was
# hand-written SVG at 720 wide). Job: function. Takeaway: a vector number picks an entry in the kernel's table, and the
# CPU jumps to that entry's handler.
# Concept: who raises a vector on the left (the CPU itself, a device, a program's int 0x80), the table in the middle
# found through IDTR, the kernel's handlers on the right. One at a time a vector number travels in, its row lights and
# the CPU jumps along that row to the handler (Part I's flow and light verbs). The facts follow the owner-calls
# correction (UNDER.md 4af): SYSCALL is not an IDT source; devices use vectors 32 and up. t=0 is a page fault taken.
from figlib import Timeline, text, splice, GOLD, BLUE, RED, GREEN, MUTED

W, H = 400, 372
INK, EDGE = '#ece6da', 'rgba(255,255,255,0.55)'
D = 12.0
T = Timeline(D, shift=2.6)
def vis(spans):
    pts = [(0.0, 0)]
    for t0, t1 in spans: pts += [(t0, 1), (t1, 0)]
    return T.discrete('opacity', sorted(pts))
ROWS = [('0', 'divide error'), ('13', 'protection'), ('14', 'page fault'), ('⋮', None), ('32+', 'devices'), ('⋮', None), ('128', 'int 0x80')]
RY = lambda i: 96 + i * 34                     # row top
TX, TW = 118, 154                              # the table
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part1-45 svgd-part1-45">')
a('<title id="svgt-part1-45">Fig BR.3 · The interrupt descriptor table · 256 doors into the kernel</title>')
a('<desc id="svgd-part1-45">The interrupt descriptor table: 256 entries the kernel wrote at boot, found through the IDTR register. Each '
  'entry holds the address of a kernel handler. A vector number picks the entry. The CPU itself raises vectors 0 to 31 for its '
  'exceptions, such as 0 for a divide error, 13 for a protection fault and 14 for a page fault; devices raise vectors 32 and up; '
  'on legacy x86 a program\'s int 0x80 raises vector 128. In turn a page fault, a device interrupt and an int 0x80 arrive, each '
  'lighting its row, and the CPU jumps to the handler that row names.</desc>')

# IDTR points at the table
a(f'<rect x="{TX}" y="18" width="{TW}" height="34" rx="5" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
a(text(TX + TW / 2, 40, 'IDTR', anchor='middle', size=15, fill=BLUE))
a(f'<path d="M {TX + TW / 2} 52 V {RY(0) - 22} m -5 -6 l 5 6 l 5 -6" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
a(text(TX + TW / 2 - 10, 72, 'where the table is', anchor='end', size=14, fill=MUTED))
# the table
a(f'<rect x="{TX}" y="{RY(0) - 10}" width="{TW}" height="{RY(len(ROWS)) - RY(0) + 4}" rx="6" fill="none" stroke="{INK}" stroke-width="1.4"/>')
for i, (v, name) in enumerate(ROWS):
    y = RY(i)
    if name is None:
        a(text(TX + TW / 2, y + 16, '⋮', anchor='middle', size=16, fill=MUTED)); continue
    a(text(TX + 10, y + 18, v, size=14, fill=GOLD, ls='0', role='object'))
    a(text(TX + 46, y + 18, name, size=14, fill=INK, ls='0'))
# the handlers
HX = 296
a(text(HX + 40, RY(0) - 26, 'kernel', anchor='middle', size=14, fill=GOLD))
a(text(HX + 40, RY(0) - 10, 'handlers', anchor='middle', size=14, fill=GOLD))
for i, (v, name) in enumerate(ROWS):
    if name is None: continue
    a(f'<rect x="{HX}" y="{RY(i) + 4}" width="80" height="22" rx="4" fill="none" stroke="rgba(212,168,83,0.75)" stroke-width="1.4"/>')
# who raises each vector
SRC = [(2, 'the CPU', RED, '14', 0.6), (4, 'a device', GREEN, '33', 4.6), (6, 'a program', BLUE, '128', 8.6)]
for i, name, col, vec, t0 in SRC:
    y = RY(i) + 15
    a(text(20, y + 5, name, size=14, fill=col))
    a(f'<path d="M 100 {y} H {TX - 6}" stroke="{EDGE}" stroke-width="1.4" stroke-dasharray="3 4"/>')
    # the source raises its vector: its line lights
    a(f'<path d="M 100 {y} H {TX - 6}" stroke="{col}" stroke-width="2.6" opacity="0">{vis([(t0, t0 + 1.6)])}</path>')
    # its row lights, and the CPU jumps along it to the handler
    a(f'<rect x="{TX + 3}" y="{RY(i) - 1}" width="{TW - 6}" height="30" rx="4" fill="none" stroke="{GOLD}" stroke-width="2.4" opacity="0">{vis([(t0 + 1.0, t0 + 3.6)])}</rect>')
    a(f'<g opacity="0">{vis([(t0 + 1.6, t0 + 3.6)])}<path d="M {TX + TW + 2} {RY(i) + 15} H {HX - 4} m -7 -5 l 7 5 l -7 5" fill="none" stroke="{GOLD}" stroke-width="2.2"/>'
      f'<rect x="{HX}" y="{RY(i) + 4}" width="80" height="22" rx="4" fill="none" stroke="{GOLD}" stroke-width="2.6"/></g>')
a(text(200, 362, 'the vector number picks the row', anchor='middle', size=14, fill=MUTED))
a('</svg>')
svg = '\n'.join(o)

caption = ('When any trap fires, the CPU reads the IDT base address from its <code>IDTR</code> register, indexes by vector number, and '
           'jumps to the handler the kernel registered for that vector. The same table dispatches CPU exceptions (vectors 0–31), '
           'hardware interrupts from devices (vectors 32 and up), and on legacy x86 the <code>int 0x80</code> system call. Exactly the '
           'same machinery underlies every involuntary entry into the kernel.')
card = f'''<div class="diagram-card fig-v2" id="fig-br-3">
      <div class="diagram-label">Fig BR.3 · The interrupt descriptor table · 256 doors into the kernel</div>
      {svg}
      <p id="chBridge-trap-p5" class="diagram-caption">{caption}</p>
    </div>'''
if __name__ == '__main__':
    splice('part-1', 'fig-br-3', 'chBridge-trap-p5', card)
