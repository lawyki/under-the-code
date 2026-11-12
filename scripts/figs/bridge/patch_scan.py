"""The Bridge, small fixes to Pass 28 figures (2026-11-12 scan, then by eye). Idempotent; edits public/part-1.html.
BR.4 the arriving address covered the word RAM: the word now heads its box from above.
BR.6 a gold square stood alone under the time line, a key whose word had been cut: it says "kernel" again, which
     names the gold slivers. The tick arrows' heads were dashed chevrons that ran into the slivers: solid heads now,
     ending clear of them.
BR.2 the step marker was a ring drawn over the words of each row: it is now a frame round the row. "return addr" and
     "status bits" touched their boxes: one size down (13).
BR.3 the three step moments sat on the instant each handler arrow appears, so two steps showed no arrow: each moved
     inside its arrow's time. The row names move 4 left to clear the table's edge; "a program" clears its leader.
BR.5 "hits 10 · misses 2" stood from the first access: the two counts now run with the accesses.
BR.8 "interrupt" stood in every step: it shows with its arrow."""
import re, sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
s = open(PAGE).read()
def sub(fid, old, new):
    global s
    a = s.index(f'id="{fid}"'); e = s.index('</svg>', a); c = s[a:e]
    if old not in c:
        assert new in c, (fid, old[:70]); return
    s = s[:a] + c.replace(old, new) + s[e:]
sub('fig-br-4', '<text x="214" y="350" text-anchor="start" font-family="DM Mono" font-size="15" letter-spacing="0.06em" fill="#9bd89b">RAM</text>',
    '<text x="202" y="313" text-anchor="start" font-family="DM Mono" font-size="15" letter-spacing="0.06em" fill="#9bd89b">RAM</text>')
key = '<rect x="36" y="224" width="12" height="12" rx="2" fill="#d4a853"/>'
sub('fig-br-6', key + '\n', key + '<text x="56" y="235" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#d4a853">kernel</text>\n')
for x in (120, 204, 288):
    sub('fig-br-6', f'<path d="M {x} 62 V 104 m -5 -7 l 5 7 l 5 -7" fill="none" stroke="#d4a853" stroke-width="1.6" stroke-dasharray="3 3"/>',
        f'<path d="M {x} 62 V 95" fill="none" stroke="#d4a853" stroke-width="1.6" stroke-dasharray="3 3"/><path d="M {x} 104 l -5.5 -9 h 11 Z" fill="#d4a853"/>')
# BR.2
ring = '<circle cx="101" cy="57" r="7" fill="none" stroke="#d4a853" stroke-width="2.4"/>'
sub('fig-br-2', ring, '<rect x="13.5" y="37.5" width="175" height="39" rx="8" fill="none" stroke="#ece6da" stroke-width="2.2"/>')
for x, w in ((156, 'return addr'), (284, 'status bits')):
    a_ = s.index('id="fig-br-2"'); e_ = s.index('</svg>', a_); c_ = s[a_:e_]
    c_ = re.sub(r'(<text data-role="object" x="%d" y="344" [^>]*?)font-size="14"([^>]*>(?:<animate[^>]*/>)?%s</text>)' % (x, w), r'\1font-size="13"\2', c_)
    s = s[:a_] + c_ + s[e_:]
# BR.3
sub('fig-br-3', 'data-beats="11.6 3.6 7.6"', 'data-beats="11.8 4.4 8.4"')
for y, w in ((114, 'divide error'), (148, 'protection'), (182, 'page fault'), (250, 'devices'), (318, 'int 0x80')):
    sub('fig-br-3', f'<text x="164" y="{y}" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0" fill="#ece6da">{w}</text>',
        f'<text x="160" y="{y}" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0" fill="#ece6da">{w}</text>')
sub('fig-br-3', '<text x="20" y="320" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#86a8ff">a program</text>',
    '<text x="13" y="320" text-anchor="start" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#86a8ff">a program</text>')
# BR.5: running counts. Twelve accesses 0.75 s apart from 0.6 s on a 12 s clock that the page shows 1.2 s late.
SEQ_HIT = [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
def counter(x, y, word, col, events):
    out = []
    times = [0.0] + events + [12.0]
    for n in range(len(events) + 1):
        t0, t1 = (times[n] + 1.2) % 12, (times[n + 1] + 1.2) % 12 or 12.0
        if t0 < t1: ks, vs = ([0, t0, t1] if t1 < 12 else [0, t0]), ([0, 1, 0] if t1 < 12 else [0, 1])
        else: ks, vs = [0, t1, t0], [1, 0, 1]                      # wraps past the end of the clock
        if ks[1] == 0: ks, vs = ks[1:], vs[1:]
        kt = ';'.join('%.6f' % (k / 12) for k in ks); vv = ';'.join(str(v) for v in vs)
        out.append(f'<text x="{x}" y="{y}" text-anchor="start" font-family="DM Mono" font-size="15" letter-spacing="0.06em" fill="{col}" opacity="{vs[0]}">'
                   f'<animate attributeName="opacity" values="{vv}" keyTimes="{kt}" calcMode="discrete" dur="12s" repeatCount="indefinite"/>{word} {n}</text>')
    return ''.join(out)
hit_t = [0.6 + 0.75 * k for k, h in enumerate(SEQ_HIT) if h]; miss_t = [0.6 + 0.75 * k for k, h in enumerate(SEQ_HIT) if not h]
sub('fig-br-5', '<text x="252" y="268" text-anchor="start" font-family="DM Mono" font-size="15" letter-spacing="0.06em" fill="#9bd89b">hits 10</text>', counter(252, 268, 'hits', '#9bd89b', hit_t))
sub('fig-br-5', '<text x="252" y="290" text-anchor="start" font-family="DM Mono" font-size="15" letter-spacing="0.06em" fill="#ec8d8d">misses 2</text>', counter(252, 290, 'misses', '#ec8d8d', miss_t))
# BR.8
lab = '<text x="200" y="96" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="#ec8d8d">interrupt</text>'
sub('fig-br-8', lab, '<g opacity="0"><animate attributeName="opacity" values="0;0;1;0" keyTimes="0.000000;0.133333;0.766667;0.933333" calcMode="discrete" dur="12s" repeatCount="indefinite"/>' + lab + '</g>')
open(PAGE, 'w').write(s); print('patched BR.4 BR.6')
