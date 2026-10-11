# Fig 18.5 · The reading list · grouped by part of this book (Pass 28, law 3). Quorum glass plate. Five shelves, one per
# part, each holding its books as spines laid flat, short title on each; the shelves light top to bottom as a marker
# steps down them. Full authors and titles are in the strip. t=0 (shift): every shelf lit.
import figlib
from figlib import Timeline, text, splice, JETBRAINS, VIOLET, TEAL, QSOFT, QMUTED, QROSE, QAMBER, QCARD
figlib.FONT = JETBRAINS

SHELVES = [('I · the physical world', TEAL, ['Code', 'Comp. Architecture']),
           ('II · the software layer', VIOLET, ['K&amp;R C', 'Modern OS', 'C++ (Stroustrup)']),
           ('III · the network', QAMBER, ['TCP/IP Illustrated', 'Comp. Networks']),
           ('IV · data and security', QROSE, ['DB Concepts', 'Crypto Engineering']),
           ('V · the modern machine', TEAL, ['Data-Intensive Apps'])]
W = 400
SY0, SS = 22, 62
D = 10.0
T = Timeline(D, shift=9.4)
TS = [0.8 + 1.2 * k for k in range(5)]
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
for k, (part, col, books) in enumerate(SHELVES):
    y = SY0 + k * SS
    a(text(10, y, f'Part {part}', anchor='start', size=13, fill=col, ls='0'))
    x = 10
    body = ''
    for b in books:
        w = len(b.replace('&amp;', '&')) * 7.8 + 18
        body += f'<rect x="{x}" y="{y + 8}" width="{w:.1f}" height="26" rx="3" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-opacity="0.8"/>'
        body += text(x + w / 2, y + 26, b, anchor='middle', size=13, fill=QSOFT, ls='0')
        x += w + 6
    assert x <= 396, (part, x)
    a(f'<g opacity="0.3">{body}</g><g opacity="0">{win(TS[k])}{body}</g>')
    a(f'<line x1="10" y1="{y + 36}" x2="390" y2="{y + 36}" stroke="{QMUTED}" stroke-opacity="0.5" stroke-width="2"/>')
H = SY0 + 4 * SS + 46
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part5-31 svgd-part5-31">')
o.insert(1, '<title id="svgt-part5-31">Fig 18.5 · The reading list · grouped by part of this book</title>')
o.insert(2, '<desc id="svgd-part5-31">Five shelves, one per part. Part I: Petzold\'s Code and Hennessy and Patterson\'s Computer Architecture. Part II: Kernighan and Ritchie\'s The C Programming Language, Tanenbaum and Bos\'s Modern Operating Systems, and Stroustrup\'s The C++ Programming Language. '
  'Part III: Stevens\'s TCP/IP Illustrated and Tanenbaum and Wetherall\'s Computer Networks. Part IV: Silberschatz and others\' Database System Concepts and Ferguson, Schneier and Kohno\'s Cryptography Engineering. Part V: Kleppmann\'s Designing Data-Intensive Applications.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One shelf for each part of the book, each holding the books that go deeper than its chapters did. Most have been the reference in their field for a decade or more.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Parts I and II.</b> Petzold, <cite>Code</cite>; Hennessy and Patterson, <cite>Computer Architecture: A Quantitative Approach</cite>; K&amp;R, <cite>The C Programming Language</cite>; Tanenbaum and Bos, <cite>Modern Operating Systems</cite>; Stroustrup, <cite>The C++ Programming Language</cite>. Also Ramalho, <cite>Fluent Python</cite>, and Kerrisk, <cite>The Linux Programming Interface</cite>.</li>
          <li><b>Parts III and IV.</b> Stevens, <cite>TCP/IP Illustrated</cite>; Tanenbaum and Wetherall, <cite>Computer Networks</cite>; Grigorik, <cite>High Performance Browser Networking</cite> (free online); Silberschatz, Korth and Sudarshan, <cite>Database System Concepts</cite>; Ferguson, Schneier and Kohno, <cite>Cryptography Engineering</cite>; Boneh and Shoup, <cite>A Graduate Course in Applied Cryptography</cite> (free draft).</li>
          <li><b>Part V.</b> Kleppmann, <cite>Designing Data-Intensive Applications</cite>, the modern reference on distributed data systems.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-18-5">
      <div class="diagram-label">Fig 18.5 · The reading list · grouped by part of this book</div>
      {svg}
      <p id="CAPID" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    import re
    s = open('/Users/yki/Documents/github/atheric/under-the-code/public/part-5.html').read()
    i = s.index('id="fig-18-5"'); cap = re.search(r'<p id="([^"]+)" class="diagram-caption"', s[i:]).group(1)
    splice('part-5', 'fig-18-5', cap, card.replace('CAPID', cap))
