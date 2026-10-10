# Fig 6.3 · A class, an object, and a vtable (Pass 28, law 3). Object -> vtable -> function, with the
# two instructions underneath. A call to s->area() lights each hop with its instruction: load the vptr,
# read slot 0, jump to Circle::area. t=0: everything drawn, nothing lit.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

W, H = 400, 300
D = 7.0
T = Timeline(D, shift=0.0)
S1, S2, S3, END = 1.0, 2.2, 3.4, 5.4
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def glow(x, y, w, h, t0, t1=END, col=GOLD):
    return f'<rect class="fx" x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}" fill-opacity="0.2" stroke="{col}" stroke-width="2" opacity="0">{win(t0, t1)}</rect>'
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-39 svgd-part2-39">')
a('<title id="svgt-part2-39">Fig 6.3 · A class, an object, and a vtable</title>')
a('<desc id="svgd-part2-39">Shape* s = new Circle{2.0}; then s-&gt;area(). The object holds a hidden vptr and its field r = 2.0. The vptr points to Circle\'s vtable, one per class, whose slot 0 points to Circle::area and slot 1 to Circle::draw. '
  'The call compiles to two instructions: mov rax, [rdi] loads the vptr, and call [rax] jumps through slot 0 to Circle::area.</desc>')
a(text(20, 22, 'Shape* s = new Circle{2.0};  s-&gt;area();', size=13, fill='#fff', ls='0'))
# object
a(text(20, 52, 'the object', size=13, fill=MUTED, ls='0'))
a(f'<rect x="20" y="60" width="130" height="64" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
a(f'<line x1="20" y1="92" x2="150" y2="92" stroke="rgba(132,255,178,0.25)"/>')
a(text(32, 81, 'vptr', size=13, fill=GOLD, ls='0'))
a(text(32, 113, 'r = 2.0', size=13, fill=PHOS_SOFT, ls='0'))
a(glow(20, 60, 130, 32, S1, S2))
# vtable
a(text(200, 52, "Circle's vtable", size=13, fill=MUTED, ls='0'))
a(f'<rect x="200" y="60" width="180" height="64" rx="3" fill="{PLATE}" stroke="{GOLD}" stroke-opacity="0.7"/>')
a(f'<line x1="200" y1="92" x2="380" y2="92" stroke="rgba(212,168,83,0.3)"/>')
a(text(212, 81, '0: Circle::area', size=13, fill='#fff', ls='0'))
a(text(212, 113, '1: Circle::draw', size=13, fill=PHOS_SOFT, ls='0'))
a(glow(200, 60, 180, 32, S2, S3))
# vptr -> vtable
a(f'<path d="M150 76 L194 76" stroke="{GOLD}" stroke-width="1.5"/><polygon points="192,71 200,76 192,81" fill="{GOLD}"/>')
# function
a(f'<rect x="200" y="152" width="180" height="50" rx="3" fill="{PANEL}" stroke="rgba(132,255,178,0.45)"/>')
a(text(212, 172, 'Circle::area()', size=13, fill='#fff', ls='0'))
a(text(212, 192, 'return π·r·r;', size=13, fill=PHOS_SOFT, ls='0'))
a(glow(200, 152, 180, 50, S3, END, PHOS))
a(f'<path d="M380 76 H392 V177 H388" fill="none" stroke="{GOLD}" stroke-width="1.5"/><polygon points="389,172 389,182 381,177" fill="{GOLD}"/>')
# the code
a(text(20, 232, 'what s-&gt;area() compiles to', size=13, fill=MUTED, ls='0'))
a(f'<rect x="20" y="240" width="360" height="52" rx="3" fill="{PLATE}" stroke="rgba(198,222,206,0.25)"/>')
for k, (ins, note, t0, t1) in enumerate((('mov rax, [rdi]', 'load the vptr', S1, S2), ('call [rax]', 'through slot 0', S2, END))):
    y = 260 + k * 22
    a(text(32, y, ins, size=13, fill=BLUE, ls='0'))
    a(text(368, y, note, anchor='end', size=13, fill=MUTED, ls='0'))
    a(f'<rect class="fx" x="24" y="{y - 15}" width="352" height="21" rx="2" fill="{BLUE}" fill-opacity="0.18" opacity="0">{win(t0, t1)}</rect>')
a('</svg>')
svg = '\n'.join(o)

caption = ('A class with virtual functions gives each object one hidden pointer, the vptr, to a table shared by the whole class. '
           'Calling <code>s-&gt;area()</code> loads the vptr, reads slot 0, and jumps there: two instructions, the second an indirect call.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Who sets it.</b> The constructor writes the vptr, so a <code>Circle</code> always points at <code>Circle</code>'s table, whatever type of pointer holds it.</li>
          <li><b>The cost.</b> One extra load and an indirect call; when the processor predicts the target, that is close to a direct call.</li>
          <li><b>The C version.</b> A struct of function pointers, kept by hand, is the same design: the Linux kernel's <code>file_operations</code> is one.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-6-3">
      <div class="diagram-label">Fig 6.3 · A class, an object, and a vtable</div>
      {svg}
      <p id="ch6-classes-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-6-3', 'ch6-classes-p4', card)
