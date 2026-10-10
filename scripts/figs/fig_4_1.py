# Fig 4.1 · The Tanenbaum–Torvalds debate (Pass 28, law 3). Greenbar: the thread as a newsreader
# prints it, line by line (stepped, like a terminal), then where each side's design ended up.
import figlib
from figlib import Timeline, text, splice, PLEX, PHOS, PHOS_SOFT, PLATE, PANEL, RED, MUTED
figlib.FONT = PLEX

W, H = 400, 402
T = Timeline(10, shift=9.0)
def line_at(t0):              # stepped reveal: on at t0, held to the loop's end
    return T.anim('opacity', [(0.0, 0.0), (t0 - 0.001, 0.0), (t0, 1.0), (9.7, 1.0), (9.701, 0.0), (9.9995, 0.0)])
o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part2-1 svgd-part2-1">')
a('<title id="svgt-part2-1">Fig 4.1 · The Tanenbaum–Torvalds debate, January 1992</title>')
a('<desc id="svgd-part2-1">A newsgroup thread on comp.os.minix, 29 January 1992. Andrew Tanenbaum posts "LINUX is obsolete": a monolithic kernel is a giant step back into the 1970s. '
  'Linus Torvalds replies: "Your job is being a professor and researcher: that\'s one hell of a good excuse for some of the brain-damages of minix." '
  'Below, where the two designs ended up: microkernels such as seL4 and QNX in safety-critical systems, the monolithic Linux nearly everywhere else.</desc>')
a(text(20, 22, '$ comp.os.minix · 29 Jan 1992', size=14, fill=PHOS))
# post 1
a(f'<rect x="20" y="34" width="360" height="110" rx="4" fill="{PLATE}" stroke="rgba(132,255,178,0.4)"/>')
L1 = [(58, 'From: ast (Andrew Tanenbaum)', 13, PHOS_SOFT), (84, 'Subject: LINUX is obsolete', 16, '#fff'),
      (112, '"a giant step back', 15, PHOS), (132, ' into the 1970s"', 15, PHOS)]
for k, (y, s, size, col) in enumerate(L1):
    a(f'<g opacity="0">{line_at(0.4 + k * 0.5)}{text(32, y, s, size=size, fill=col, ls="0")}</g>')
# post 2, a reply, indented
a(f'<rect x="40" y="156" width="340" height="150" rx="4" fill="{PLATE}" stroke="rgba(132,255,178,0.4)"/>')
a('<path d="M 30 150 V 230 H 40" fill="none" stroke="rgba(132,255,178,0.4)"/>')
L2 = [(180, 'From: torvalds (Linus Torvalds)', 13, PHOS_SOFT), (204, 'Re: LINUX is obsolete', 15, '#fff'),
      (230, '"Your job is being a professor', 14, PHOS), (250, ' and researcher: that\'s one hell', 14, PHOS),
      (270, ' of a good excuse for some of', 14, PHOS), (290, ' the brain-damages of minix."', 14, PHOS)]
for k, (y, s, size, col) in enumerate(L2):
    a(f'<g opacity="0">{line_at(2.8 + k * 0.5)}{text(52, y, s.replace(chr(39), "&#39;"), size=size, fill=col, ls="0")}</g>')
# the block cursor, blinking at the end of the thread
a(f'<rect x="300" y="280" width="9" height="14" fill="{PHOS}" opacity="0">'
  f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.5;0.51" dur="1s" repeatCount="indefinite"/></rect>')
# where each design went
a(text(20, 332, 'THIRTY YEARS ON', size=13, fill=MUTED))
for k, (head, sub) in enumerate((('microkernels', 'seL4, QNX: safety-critical'), ('monolithic', 'Linux: nearly everywhere'))):
    y = 342 + k * 30
    a(f'<g opacity="0">{line_at(6.4 + k * 0.6)}<rect x="20" y="{y}" width="360" height="26" rx="4" fill="{PANEL}" stroke="rgba(132,255,178,0.35)"/>'
      f'{text(30, y + 18, head, size=14, fill=PHOS, ls="0")}{text(370, y + 18, sub, anchor="end", size=13, fill=PHOS_SOFT, ls="0")}</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('In January 1992 Andrew Tanenbaum told comp.os.minix that Linux\'s monolithic design was obsolete; Linus Torvalds, twenty-two, answered at length. '
           'Three decades on both were right: microkernels are strong in safety-critical systems, and Linux runs nearly everything else.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Tanenbaum's case.</b> Theory: a microkernel keeps drivers and services out of the kernel, so one bug cannot take the machine down. He also predicted Linux, tied to the 386, would not last.</li>
          <li><b>Torvalds's case.</b> Running code: a monolithic kernel is simpler and faster, and Linux was free and worked on the machines people had.</li>
          <li><b>The outcome.</b> Microkernels such as seL4 (formally verified) and QNX are used where one kernel bug is unacceptable; Linux runs servers, phones and supercomputers.</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-4-1">
      <div class="diagram-label">Fig 4.1 · The Tanenbaum–Torvalds debate, January 1992</div>
      {svg}
      <p id="ch4-anatomy-p7" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-2', 'fig-4-1', 'ch4-anatomy-p7', card)
