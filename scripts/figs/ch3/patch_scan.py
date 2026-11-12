"""Chapter 3, small fixes to Pass 28 figures, each confirmed by the 2026-11-12 screenshot scan and then by eye.
Idempotent; edits public/part-1.html in place. Figs 3.7 to 3.11 are kept originals (owner ground) and untouched.
3.1 the ARM64 and RISC-V opcode boxes were empty while x86's showed 83: each now shows its bits; the "register"
    chip's frame clears its word.
3.2 "register w8" hung off the instruction column: it sits under its box.
3.4 two step moments fell while the next argument was already in flight (a stray d, a g over RDX): both moved
    to the settled moment just before.
3.6 the dashed return line ran through the RSP mark: it leaves the return box above the mark."""
import sys; sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/ch1')
from plate import PAGE
s = open(PAGE).read()
def sub(fid, old, new):
    global s
    a = s.index(f'id="{fid}"'); e = s.index('</svg>', a); c = s[a:e]
    if old not in c:
        assert new in c, (fid, old[:70]); return
    s = s[:a] + c.replace(old, new, 1) + s[e:]
T = lambda x, y, t: f'<text data-role="object" x="{x}" y="{y}" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0" fill="#d4a853">{t}</text>'
five_arm = '<text data-role="object" x="200" y="202" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0" fill="#9bd89b">5</text>'
five_rv = '<text data-role="object" x="90" y="298" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0" fill="#9bd89b">5</text>'
sub('fig-3-1', five_arm, T(73.5, 202, '100100010') + five_arm)
sub('fig-3-1', five_rv, T(337.5, 298, '0010011') + five_rv)
sub('fig-3-1', '<rect x="134" y="12" width="109" height="28"', '<rect x="134" y="12" width="116" height="28"')
sub('fig-3-2', '<text x="266" y="362" text-anchor="end" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="rgba(255,255,255,0.6)">register w8</text>',
    '<text x="324" y="396" text-anchor="middle" font-family="DM Mono" font-size="14" letter-spacing="0.06em" fill="rgba(255,255,255,0.6)">register w8</text>')
sub('fig-3-4', 'data-beats="4.8 7.6 8.6 10.4"', 'data-beats="4.6 7.3 8.6 10.4"')
sub('fig-3-6', '<path d="M 236 140 C 196 140 200 86 176 86"', '<path d="M 236 129 C 204 129 202 86 176 86"')
open(PAGE, 'w').write(s); print('patched 3.1 3.2 3.4 3.6')
