# Fig 9.9 · The shape of an IPv4 vs an IPv6 address (Pass 28, law 3). Chart Room paper card. IPv4's 32
# bits as four octets; IPv6's 128 bits as eight groups, then shortened in two legal steps (drop leading
# zeros, collapse one run of zero groups into ::), with the /64 split marked. t=0: all steps shown.
import ipaddress
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D, GREEN = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f', '#2e7e4f'
BOX = '#f4f7f9'
FULL = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
STEP2 = ':'.join(g.lstrip('0') or '0' for g in FULL.split(':'))
STEP3 = str(ipaddress.IPv6Address(FULL))
assert STEP2 == '2001:db8:85a3:0:0:8a2e:370:7334' and STEP3 == '2001:db8:85a3::8a2e:370:7334'
W, H = 400, 312
D = 8.0
ST = [0.6, 2.4, 4.2]
T = Timeline(D, shift=0.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-23 svgd-part3-23">')
a('<title id="svgt-part3-23">Fig 9.9 · The shape of an IPv4 vs an IPv6 address</title>')
a(f'<desc id="svgd-part3-23">An IPv4 address, 192.0.2.42, is 32 bits written as four decimal octets; there are about 4.3 billion. An IPv6 address is 128 bits written as eight groups of four hexadecimal digits, {FULL}; there are about 3.4 × 10^38. '
  f'It may be shortened in two steps: drop each group\'s leading zeros, giving {STEP2}, then replace one run of zero groups with a double colon, giving {STEP3}. The first 64 bits name the network, the last 64 the device.</desc>')
a(text(20, 22, 'IPv4 · 32 bits · about 4.3 billion', size=13, fill=INK_SOFT))
for k, octet in enumerate(['192', '0', '2', '42']):
    x = 20 + k * 92
    a(f'<rect x="{x}" y="32" width="86" height="34" rx="2" fill="{BOX}" stroke="{ACC}" stroke-opacity="0.6"/>')
    a(text(x + 43, 54, octet, anchor='middle', size=15, fill=INK, ls='0'))
    a(text(x + 43, 84, '8 bits', anchor='middle', size=13, fill=INK_SOFT, ls='0'))
a(text(20, 120, 'IPv6 · 128 bits · about 3.4 × 10³⁸', size=13, fill=INK_SOFT))
ROWS = [(FULL, 'eight 16-bit groups, in hex'), (STEP2, 'drop leading zeros'), (STEP3, 'one run of zeros becomes ::')]
for k, (addr, note) in enumerate(ROWS):
    y = 140 + k * 46
    a(f'<rect x="12" y="{y}" width="376" height="40" rx="2" fill="{BOX}" stroke="{GREEN if k == 2 else ACC}" stroke-opacity="0.5"/>')
    a(text(20, y + 17, addr, size=13, fill=GREEN if k == 2 else INK, ls='0'))
    a(text(20, y + 34, f'{k + 1} · {note}', size=13, fill=INK_SOFT, ls='0'))
    a(f'<rect class="fx" x="12" y="{y}" width="376" height="40" rx="2" fill="{ROUTE_D}" fill-opacity="0.12" stroke="{ROUTE_D}" stroke-width="2" opacity="0">{win(ST[k], ST[k] + 1.8)}</rect>')
# the /64 split under the full form
y = 140 + 3 * 46 + 4
mid = 20 + 19.5 * 8.0       # after "2001:0db8:85a3:0000" (19 characters)
a(f'<line x1="20" y1="{y}" x2="{mid - 6}" y2="{y}" stroke="{ACC}" stroke-width="2"/><line x1="{mid + 6}" y1="{y}" x2="372" y2="{y}" stroke="{ROUTE_D}" stroke-width="2"/>')
a(text(20, y + 18, 'network · 64 bits', size=13, fill=ACC, ls='0'))
a(text(372, y + 18, 'device · 64 bits', anchor='end', size=13, fill=ROUTE_D, ls='0'))
a('</svg>')
svg = '\n'.join(o)

caption = ('IPv4 writes its 32 bits as four decimal octets; IPv6 writes 128 bits as eight hexadecimal groups, shortened by dropping leading zeros and collapsing one run of zero groups into <code>::</code>. '
           'The first 64 bits name the network and the last 64 the device, a split the abundance makes affordable.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Scale.</b> 2<sup>32</sup> is about 4.3 billion, fewer than the people alive; 2<sup>128</sup> is about 3.4 × 10<sup>38</sup>, so even every 64-bit subnet has room for 1.8 × 10<sup>19</sup> devices.</li>
          <li><b>One :: only.</b> It may appear once per address, or a reader could not tell how many zero groups each stood for.</li>
          <li><b>The price.</b> Every router, operating system, firewall and networking library had to change, which is why, nearly thirty years on, the move is still unfinished.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-9-9">
      <div class="diagram-label">Fig 9.9 · The shape of an IPv4 vs an IPv6 address</div>
      {svg}
      <p id="ch9-v6-p3" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-9-9', 'ch9-v6-p3', card)
