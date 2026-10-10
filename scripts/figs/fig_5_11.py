# Fig 5.11 · The C family tree (Pass 28, law 3). C at the root and three waves of descendants; a year
# counter sweeps 1972 to 2016 and each language appears in its year. t=0 (shift): the whole tree.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, GOLD, BLUE, MUTED
figlib.FONT = PLEX

WAVES = [('keep the speed, add objects', GOLD, [('Objective-C', 1984), ('C++', 1985)]),
         ('keep the syntax, add a managed runtime', BLUE, [('Perl', 1987), ('Java', 1995), ('JavaScript', 1995), ('PHP', 1995), ('C#', 2000), ('Kotlin', 2011)]),
         ('keep the speed, add memory safety', PHOS, [('Go', 2009), ('Rust', 2010), ('Swift', 2014), ('Zig', 2016)])]
W = 400
CX0, CWD, CH, CG = 40, 108, 40, 8
D = 12.0
T = Timeline(D, shift=11.2)
RESET = 0.4
Y0, Y1 = 1972, 2016
yt = lambda yr: 1.0 + (yr - Y0) / (Y1 - Y0) * 8.0
def appear(t0):
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; body = []; b = body.append
b(f'<rect x="20" y="12" width="360" height="38" rx="3" fill="{PLATE}" stroke="{PHOS}" stroke-width="1.5"/>')
b(text(32, 36, 'C · 1972 · Bell Labs', size=14, fill='#fff', ls='0'))
years = sorted({yr for _, _, ls in WAVES for _, yr in ls})
for i, yr in enumerate(years):
    t0 = yt(yr); t1 = yt(years[i + 1]) if i + 1 < len(years) else None
    if t1 is None:
        pts = [(0.0, 1.0), (RESET, 1.0), (RESET + 0.005, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)]
    else:
        pts = [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)]
    b(f'<g>{T.anim("opacity", pts)}{text(368, 36, str(yr), anchor="end", size=14, fill=GOLD, ls="0")}</g>')
y = 76
trunk_end = 0
for title, col, langs in WAVES:
    b(text(CX0, y, title, size=13, fill=col, ls='0'))
    b(f'<line x1="26" y1="{y - 5}" x2="34" y2="{y - 5}" stroke="rgba(198,222,206,0.4)" stroke-width="1.5"/>')
    trunk_end = y - 5
    y += 10
    for i, (nm, yr) in enumerate(langs):
        r, c = divmod(i, 3)
        x, cy = CX0 + c * (CWD + 5), y + r * (CH + CG)
        b(f'<g>{appear(yt(yr))}<rect x="{x}" y="{cy}" width="{CWD}" height="{CH}" rx="3" fill="{PANEL}" stroke="{col}" stroke-opacity="0.7"/>'
          f'{text(x + 10, cy + 17, nm, size=14, fill="#fff", ls="0")}{text(x + 10, cy + 33, str(yr), size=13, fill=MUTED, ls="0")}</g>')
        b(f'<rect class="fx" x="{x}" y="{cy}" width="{CWD}" height="{CH}" rx="3" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="2" opacity="0">'
          f'{T.anim("opacity", [(0.0, 0.0), (yt(yr) - 0.002, 0.0), (yt(yr), 1.0), (yt(yr) + 0.5, 0.0), (D, 0.0)])}</rect>')
    rows = (len(langs) + 2) // 3
    y += rows * (CH + CG) + 20
b(f'<line x1="26" y1="50" x2="26" y2="{trunk_end}" stroke="rgba(198,222,206,0.4)" stroke-width="1.5"/>')
H = y - 14
o.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-35 svgd-part2-35">')
o.append('<title id="svgt-part2-35">Fig 5.11 · The C family tree · half a century of descendants</title>')
o.append('<desc id="svgd-part2-35">C, from Bell Labs in 1972, at the root of three waves of descendants. Keeping C\'s speed and adding objects: Objective-C (1984) and C++ (1985). '
         'Keeping C\'s syntax on a managed runtime: Perl (1987), Java, JavaScript and PHP (all 1995), C# (2000) and Kotlin (2011). '
         'Keeping C\'s speed and adding memory safety: Go (2009), Rust (2010), Swift (2014) and Zig (2016).</desc>')
o.extend(body)
o.append('</svg>')
svg = '\n'.join(o)

caption = ('Most major languages since 1972 grew out of C or were built as answers to it, in three waves: objects on top of C\'s speed, C\'s syntax on a managed runtime, and C\'s speed with memory safety. '
           'The braces, semicolons and <code>for</code> loops of much of today\'s code are C\'s.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>First wave.</b> Objective-C is a strict superset of C, and C++ nearly one: both compile C code almost unchanged.</li>
          <li><b>Second wave.</b> Java, C# and Kotlin run on virtual machines with garbage collection; Perl, JavaScript and PHP borrowed C's look for scripting.</li>
          <li><b>Third wave.</b> Rust proves memory safety at compile time through ownership; Go and Swift manage memory for you; Zig keeps manual control with fewer traps.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-5-11">
      <div class="diagram-label">Fig 5.11 · The C family tree · half a century of descendants</div>
      {svg}
      <p id="ch5-survives-p4" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-5-11', 'ch5-survives-p4', card)
