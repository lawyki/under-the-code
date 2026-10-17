# Fig 7.7 · Why Python is slow (Pass 28, law 3). The work behind a + b. C: one add instruction.
# CPython's generic path: a list of steps, lit in turn, each of them several machine instructions.
# t=0 (shift): every step lit once, the comparison complete.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

STEPS = ['dispatch to the opcode handler', 'pop two object pointers', 'find the type\'s add function',
         'check both are ints', 'read the digits out of both', 'add them', 'make an int object for the result',
         'update reference counts', 'push the result']
W = 400
D = 10.0
ST = [0.6 + 0.8 * k for k in range(len(STEPS))]
DONE = ST[-1] + 0.8
T = Timeline(D, shift=DONE + 0.3)
RESET = 0.4
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; body = []; b = body.append
b(text(20, 22, 'the work behind  a + b', size=13, fill=MUTED, ls='0'))
b(text(20, 48, 'C', size=14, fill=GOLD, ls='0'))
b(f'<rect x="60" y="32" width="320" height="26" rx="3" fill="{PANEL}" stroke="{GOLD}" stroke-opacity="0.7"/>')
b(text(72, 50, 'add eax, esi', size=13, fill='#fff', ls='0'))
b(text(368, 50, '1 instruction', anchor='end', size=13, fill=GOLD, ls='0'))
b(f'<rect class="fx" x="60" y="32" width="320" height="26" rx="3" fill="{GOLD}" fill-opacity="0.25" stroke="{GOLD}" stroke-width="2" opacity="0">{win(ST[0], ST[0] + 0.8)}</rect>')
b(text(20, 92, 'CPython', size=14, fill=BLUE, ls='0'))
for k, s in enumerate(STEPS):
    y = 100 + k * 26
    b(f'<rect x="60" y="{y}" width="320" height="22" rx="2" fill="{PLATE}" stroke="rgba(134,168,255,0.25)"/>')
    b(f'<g>{held(ST[k])}<rect x="60" y="{y}" width="320" height="22" rx="2" fill="{BLUE}" fill-opacity="0.18" stroke="{BLUE}" stroke-opacity="0.6"/></g>')
    b(f'<rect class="fx" x="60" y="{y}" width="320" height="22" rx="2" fill="none" stroke="#fff" stroke-width="2" opacity="0">{win(ST[k], ST[k] + 0.8)}</rect>')
    b(text(72, y + 16, s.replace("'", '&#8217;'), size=13, fill='#fff', ls='0'))
    b(text(42, y + 16, str(k + 1), anchor='end', size=13, fill=MUTED, ls='0'))
yb = 100 + len(STEPS) * 26 + 18
b(f'<g>{held(DONE)}{text(20, yb, "each step is several instructions, every time", size=13, fill=BLUE, ls="0")}</g>')
H = yb + 12
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-53 svgd-part2-53">')
o.append('<title id="svgt-part2-53">Fig 7.7 · Why Python is slow (and why nobody minds)</title>')
o.append('<desc id="svgd-part2-53">The work behind a + b. In C, where the compiler knows both are ints, it is one instruction: add eax, esi. '
         'In CPython\'s generic path it is a list of steps, each several machine instructions: dispatch to the opcode handler, pop two object pointers, find the type\'s add function, '
         'check both are ints, read the digits out of both, add them, make an int object for the result, update reference counts, push the result.</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ("C's compiler knows both values are ints and emits one add; CPython learns what they are only at runtime, so every <code>+</code> unpacks two objects, checks their types, adds, and packs a new object. Many programs spend most of their time waiting on disks, networks or libraries written in C, and there the gap does not show.")
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Boxes.</b> Every Python value is an object on the heap with a type and a reference count; even a small int is a pointer to one.</li>
          <li><b>Since 3.11.</b> The interpreter notices that a <code>+</code> keeps seeing ints and swaps in a specialised instruction that skips the lookup, though not the boxes.</li>
          <li><b>JIT compilers.</b> PyPy compiles hot loops to machine code with the types it has observed, removing most of the steps.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-7-7">
      <div class="diagram-label">Fig 7.7 · Why Python is slow (and why nobody minds)</div>
      {svg}
      <p id="ch7-cpython-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-7-7', 'ch7-cpython-p4', card)
