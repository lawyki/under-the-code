# Fig 8.9 · A MAC address, and the ARP cache that resolves it (Pass 28, law 3). Chart Room paper card.
# The 48-bit address split into maker and device halves; then an ARP exchange: a cache miss, the
# broadcast "who has 192.168.1.5?", the owner's reply, and the new cache row. t=0 (shift): resolved.
import figlib
from figlib import Timeline, text, splice, SPACE
figlib.FONT = SPACE

INK, INK_SOFT, ACC, ROUTE_D, GREEN = '#122a3f', 'rgba(18,42,63,0.62)', '#10719d', '#b4541f', '#2e7e4f'
BOX = '#f4f7f9'
W, H = 400, 336
D = 8.0
ASK, REPLY, CACHE = 1.0, 3.0, 4.6
T = Timeline(D, shift=7.0)
def win(t0, t1):
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (t1 - 0.008, 1.0), (t1 - 0.005, 0.0), (D, 0.0)])
def held(t0):
    return T.anim('opacity', [(0.0, 1.0), (0.4, 1.0), (0.405, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-10 svgd-part3-10">')
a('<title id="svgt-part3-10">Fig 8.9 · A MAC address, and the ARP cache that resolves it</title>')
a('<desc id="svgd-part3-10">The MAC address B8:27:EB:9C:DA:C7 is 48 bits in two halves: B8:27:EB names the maker, the Raspberry Pi Foundation, and 9C:DA:C7 names this one card. '
  'Below, a host at 192.168.1.10 wants to send to 192.168.1.5, which is not in its ARP cache. It broadcasts "who has 192.168.1.5?" to every host on the network; the owner replies with its MAC address, and the host adds the pair to its cache.</desc>')
a(text(20, 22, 'MAC ADDRESS · 48 BITS', size=13, fill=INK_SOFT))
for x, top, sub in ((20, 'B8:27:EB', 'Raspberry Pi'), (206, '9C:DA:C7', 'this card')):
    a(f'<rect x="{x}" y="32" width="174" height="48" rx="2" fill="{BOX}" stroke="{ACC}" stroke-opacity="0.6"/>')
    a(text(x + 12, 52, top, size=15, fill=INK, ls='0'))
    a(text(x + 12, 72, sub, size=13, fill=INK_SOFT, ls='0'))
# the network
a(text(20, 112, 'ARP', size=13, fill=INK_SOFT))
a(f'<rect x="20" y="140" width="110" height="40" rx="2" fill="{BOX}" stroke="{INK}" stroke-opacity="0.5"/>')
a(text(75, 156, 'me', anchor='middle', size=13, fill=INK_SOFT, ls='0'))
a(text(75, 172, '192.168.1.10', anchor='middle', size=13, fill=INK, ls='0'))
HOSTS = [('192.168.1.1', 116), ('192.168.1.5', 160), ('192.168.1.42', 204)]
for ip, y in HOSTS:
    a(f'<rect x="262" y="{y - 16}" width="118" height="32" rx="2" fill="{BOX}" stroke="{INK}" stroke-opacity="0.4"/>')
    a(text(321, y + 5, ip, anchor='middle', size=13, fill=INK, ls='0'))
    a(f'<line x1="130" y1="160" x2="262" y2="{y}" stroke="{INK}" stroke-opacity="0.15"/>')
    a(f'<line class="fx" x1="130" y1="160" x2="262" y2="{y}" stroke="{ROUTE_D}" stroke-width="2" stroke-dasharray="5 4" opacity="0">{win(ASK, REPLY)}</line>')
a(f'<path class="fx" d="M262 166 L136 166" stroke="{GREEN}" stroke-width="2.5" opacity="0">{win(REPLY, CACHE + 0.6)}</path>')
a(f'<polygon class="fx" points="138,161 130,166 138,171" fill="{GREEN}" opacity="0">{win(REPLY, CACHE + 0.6)}</polygon>')
# the cache
CY = 248
a(text(20, CY - 10, 'ARP CACHE ON 192.168.1.10', size=13, fill=INK_SOFT))
a(f'<rect x="20" y="{CY}" width="360" height="56" rx="2" fill="{BOX}" stroke="{ACC}" stroke-opacity="0.5"/>')
a(text(32, CY + 21, '192.168.1.1', size=13, fill=INK, ls='0'))
a(text(368, CY + 21, '8C:85:90:1F:33:42', anchor='end', size=13, fill=INK, ls='0'))
a(f'<g>{held(CACHE)}{text(32, CY + 44, "192.168.1.5", size=13, fill=GREEN, ls="0")}{text(368, CY + 44, "B8:27:EB:9C:DA:C7", anchor="end", size=13, fill=GREEN, ls="0")}</g>')
STAT = [(0.4, ASK, 'send to 192.168.1.5: not cached', INK), (ASK, REPLY, 'broadcast: who has 192.168.1.5?', ROUTE_D),
        (REPLY, CACHE, 'its owner replies with its MAC', GREEN), (CACHE, D - 0.2, 'cached; the next frame goes direct', INK)]
for t0, t1, s, col in STAT:
    a(f'<g opacity="0">{win(t0, t1)}{text(20, 328, s, size=13, fill=col, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('One MAC address split into maker and card, and the ARP exchange that finds it: broadcast the question, the owner replies, the answer is cached.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Expiry.</b> Entries age out after seconds to minutes, depending on the system, so a device that leaves or changes card is soon forgotten.</li>
          <li><b>No proof.</b> ARP checks nothing: any host on the link can answer for any address. <a href="part-4#ch15">Chapter 15</a> returns to what that allows.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card light-diagram fig-v2" id="fig-8-9">
      <div class="diagram-label">Fig 8.9 · A MAC address, and the ARP cache that resolves it</div>
      {svg}
      <p id="ch8-ethernet-p9" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-8-9', 'ch8-ethernet-p9', card)
