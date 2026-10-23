# Fig 13.11 · Parameterised queries · code and data on separate wires (Pass 28, law 3, conceptual pass: the defence,
# shown with an honest apostrophe rather than an attack string). Strongroom dossier plate. Top, the code. Two lanes: the
# SQL text with its ? placeholder goes through the parser, once, into a plan; the value O'Brien goes around the parser
# and is bound into the plan's slot as plain data, apostrophe and all. Then a second value, Smith, reuses the plan with no
# second parse. t=0 (shift): the plan reused for Smith.
import figlib
from figlib import Timeline, text, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, OXBLOOD, BRASS, SAGE, DCARD
figlib.FONT = COURIER

W = 400
D = 10.0
T = Timeline(D, shift=9.4)
TP, TV1, TV2 = 0.8, 3.2, 6.4                 # parse, first value, second value
lit = lambda t0, t1: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
first = lambda t1: T.anim('opacity', [(0.0, 0.0), (0.3, 0.0), (0.305, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
pulse = lambda t0: T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t0 + 0.6, 0.0), (D, 0.0)])
o = []; a = o.append
def box(x, y, w, h, col, op=0.7):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{DCARD}" stroke="{col}" stroke-opacity="{op}"/>')
def phases(x, y, spans, anchor='start'):
    for t0, t1, s, col in spans:
        vis = win(t0) if t1 is None else (first(t1) if t0 < 0.5 else lit(t0, t1))
        a(f'<g opacity="0">{vis}{text(x, y, s, anchor=anchor, size=13, fill=col, ls="0")}</g>')
# the code
box(20, 12, 360, 74, PMUTED, 0.5)
a(text(32, 34, 'sql = "SELECT * FROM users', size=13, fill=PSOFT, ls='0'))
a(text(32 + 7 * 7.8, 54, 'WHERE name = ?"', size=13, fill=PSOFT, ls='0'))
a(text(32, 74, 'db.execute(sql, [name])', size=13, fill=PSOFT, ls='0'))
# lane heads
LX, RX = 20, 220
a(text(LX, 112, 'the SQL text', size=13, fill=BRASS, ls='0'))
a(text(RX, 112, 'the value', size=13, fill=SAGE, ls='0'))
box(LX, 122, 180, 32, BRASS); a(text(LX + 12, 143, 'name = ?', size=13, fill=PARCH, ls='0'))
box(RX, 122, 160, 32, SAGE)
phases(RX + 12, 143, [(0.31, TV2, "O'Brien", PARCH), (TV2, None, 'Smith', PARCH)])
# the parser: only the left lane passes through it
PY = 184
box(LX, PY, 180, 40, OXBLOOD, 0.8); a(text(LX + 12, PY + 25, 'parser', size=13, fill=PARCH, ls='0'))
phases(LX + 168, PY + 25, [(0.31, None, 'once', PMUTED)], anchor='end')
a(text(RX, PY + 25, 'never parsed', size=13, fill=PMUTED, ls='0'))
a(f'<g class="fx" opacity="0">{pulse(TP + 0.5)}<rect x="{LX - 3}" y="{PY - 3}" width="186" height="46" rx="3" fill="none" stroke="{OXBLOOD}" stroke-width="2.5"/></g>')
# the plan, with its slot
QY = 254
box(LX, QY, 360, 44, BRASS, 0.9)
a(text(LX + 12, QY + 27, 'plan: users,', size=13, fill=PARCH, ls='0'))
a(text(LX + 12 + 13 * 7.8, QY + 27, 'name =', size=13, fill=PARCH, ls='0'))
SX = 214
a(f'<rect x="{SX}" y="{QY + 8}" width="150" height="28" rx="2" fill="none" stroke="{SAGE}" stroke-dasharray="4 3"/>')
phases(SX + 12, QY + 27, [(0.31, TV1 + 0.9, '?', PMUTED), (TV1 + 0.9, TV2 + 0.9, "O'Brien", SAGE), (TV2 + 0.9, None, 'Smith', SAGE)])
a(f'<g opacity="0">{win(TP + 0.9)}</g>')
# the movements: dots down the lanes (the SQL text through the parser, the value beside it)
def drop(x, y0, y1, t0, t1, col):
    mv = T.translate([(0.0, 0.0), (t0, 0.0), (t1, y1 - y0), (D, y1 - y0)], 'y')
    a(f'<g class="fx" opacity="0">{lit(t0, t1 + 0.3)}<g>{mv}<circle cx="{x}" cy="{y0}" r="6" fill="{col}"/></g></g>')
drop(LX + 100, 154, QY - 6, TP, TP + 0.9, BRASS)
for t0 in (TV1, TV2):
    drop(RX + 140, 154, QY + 22, t0, t0 + 0.9, SAGE)
    a(f'<g class="fx" opacity="0">{pulse(t0 + 0.9)}<rect x="{SX - 3}" y="{QY + 5}" width="156" height="34" rx="3" fill="none" stroke="{SAGE}" stroke-width="2.5"/></g>')
SY = QY + 70
phases(20, SY, [(0.31, TV1, 'parse: once', BRASS), (TV1, TV2, "bound as data: O'Brien", SAGE),
                (TV2, None, 'new value, same statement', SAGE)])
H = SY + 14
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-12 svgd-part4-12">')
o.insert(1, '<title id="svgt-part4-12">Fig 13.11 · Parameterised queries · code and data on separate wires</title>')
o.insert(2, '<desc id="svgd-part4-12">The code sends the SQL text SELECT * FROM users WHERE name = ? and, separately, the value of name. The SQL text goes through the database\'s parser once and becomes a plan with an empty slot where the question mark was. '
  'The value O\'Brien never passes through the parser: it is bound into the slot as plain data, and its apostrophe is just a letter in a name. A second value, Smith, is bound into the same plan with no second parse.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('With a parameterised query the SQL text, with a placeholder where each value goes, is parsed once into a plan, and the values travel separately and are bound into it afterwards. Since a value never reaches the parser, nothing in it can change what the query does: an apostrophe is only a letter.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>On the wire.</b> PostgreSQL's extended query protocol and MySQL's prepared statements send the statement and its parameters as separate messages; a driver that only emulates this must escape every value correctly instead.</li>
          <li><b>Values only.</b> A placeholder can hold a value but not a table or column name, so code that varies those must pick from a fixed list.</li>
          <li><b>Reuse.</b> The parsed statement can be kept and run again for each new value, which saves the parse.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-13-11">
      <div class="diagram-label">Fig 13.11 · Parameterised queries · code and data on separate wires</div>
      {svg}
      <p id="ch13-injection-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-4', 'fig-13-11', 'ch13-injection-p5', card)
