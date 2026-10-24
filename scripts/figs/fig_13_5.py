# Fig 13.6 · A bank transfer, and the log that saves it (Pass 31 exemplar for Part IV, from an empty script: the merge
# of Figs 13.5 and 13.6 into one merged card, which keeps the higher number). Takeaway (ledger, round 4): changes reach the log before the pages,
# so recovery after a crash replays committed work, rolls back the rest.
# Concept chosen of three (ledger). Top, the failure: a transfer with no transaction, cut by a power failure after
# Alice is debited, and EUR 100 is gone. Below, the same transfer inside a transaction: every change is stamped into
# the log before the data pages; an earlier deposit committed but never reached its page, and the transfer was
# cut before its commit. Recovery redoes the deposit and undoes the transfer. Strongroom's lock-step motion: records land like stamps.
# t=0 is the recovered state. The merged card is Fig 13.6 (the higher half keeps its number, id and slot); Fig 13.5's
# card leaves the page and its ids are aliased in book.js to ch13-acid-p2.
import re
import figlib
from figlib import Timeline, text, obj, splice, COURIER, PARCH, PSOFT, PMUTED, SEAL, STAMP, BRASS, SAGE
figlib.FONT = COURIER

W, H = 400, 470
D = 10.0
T = Timeline(D, shift=9.6)
RESET = 0.3
def held(t):
    return T.anim('opacity', [(0.0, 1.0), (RESET, 1.0), (RESET + 0.001, 0.0), (t - 0.001, 0.0), (t, 1.0), (D, 1.0)])
def until(t):
    return T.anim('opacity', [(0.0, 0.0), (RESET, 0.0), (RESET + 0.001, 1.0), (t - 0.001, 1.0), (t, 0.0), (D, 0.0)])
P1_DEBIT, P1_CUT, P1_GONE = T.beat(0.6, 'no transaction: Alice is debited'), T.beat(1.3, 'the power fails'), T.beat(2.0, 'EUR 100 is gone')
L1, L2, L3 = T.beat(3.0, 'the deposit logged'), T.beat(3.6, 'the deposit commits'), T.beat(4.3, 'the transfer logged: Alice debited')
EARLY, CUT = T.beat(4.8, "Alice's page written early"), T.beat(5.5, 'the power fails before the transfer commits')
REDO, UNDO, DONE = T.beat(6.6, 'recovery redoes the deposit'), T.beat(7.5, 'and undoes the transfer'), T.beat(8.3, 'nothing half done')

o = []; a = o.append
a(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part4-6 svgd-part4-6"{T.beats_attr()}>')
a('<title id="svgt-part4-6">Fig 13.6 · A bank transfer · the failure, and the log that prevents it</title>')
a('<desc id="svgd-part4-6">Two parts. Top, a transfer of 100 euros from Alice to Bob with no transaction: Alice is debited, the '
  'power fails before Bob is credited, and at restart Alice holds 100, Bob 50, and 100 euros are gone. Below, the same '
  'transfer inside a transaction. Every change is written to the log first: an earlier deposit raising Dan from 20 to 70, '
  'and its commit; then the transfer, debiting Alice from 200 to 100. Dan\'s data page has not been written yet, while '
  'Alice\'s was written early. The power fails before the transfer commits. Recovery reads the log: the deposit has a '
  'commit, so it is redone and Dan holds 70; the transfer has none, so it is undone and Alice holds 200 again. Nothing is '
  'left half done.</desc>')

def card(x, y, w, name, value='', col=PARCH, layers=()):
    """An account's data card: its name, and either a fixed value or value layers that change over time."""
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="3" fill="none" stroke="{PSOFT}" stroke-width="1.3"/>',
             text(x + 10, y + 18, name, size=14, fill=PMUTED, ls='0')]
    if value:
        parts.append(text(x + w - 10, y + 38, value, anchor='end', size=16, fill=col, ls='0'))
    return obj(*parts, *layers)

def stamp(x, y, word, col, t):
    """A word that lands like a rubber stamp, boxed, at t; held to the end of the loop."""
    w = len(word) * 9 + 18
    return (f'<g opacity="1">{held(t)}' +
            obj(f'<rect x="{x - w / 2}" y="{y - 15}" width="{w}" height="21" rx="2" fill="none" stroke="{col}" stroke-width="2"/>',
                text(x, y + 1, word, anchor='middle', size=14, fill=col, ls='0.04em')) + '</g>')

# ---- top: the failure ------------------------------------------------------------------------------------------
a('<g data-panel="failure">')
a(text(20, 22, 'no transaction', size=14, fill=PMUTED, role='label'))
steps = [('debit Alice', PARCH, P1_DEBIT), ('power cut', SEAL, P1_CUT), ('credit Bob', PMUTED, None)]
x = 20
for name, col, t in steps:
    w = len(name) * 8.6 + 20
    chip = obj(f'<rect x="{x}" y="34" width="{w:.0f}" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.5"/>',
               text(x + w / 2, 51, name, anchor='middle', size=14, fill=col, ls='0', role='label'))
    if t is None:  # never happens: struck through
        chip += f'<line x1="{x + 6}" y1="46" x2="{x + w - 6:.0f}" y2="46" stroke="{STAMP}" stroke-width="2"/>'
        a(f'<g opacity="1">{held(P1_CUT)}{chip}</g>')
    else:
        a(f'<g opacity="1">{held(t)}{chip}</g>')
    x += w + 10
a(card(20, 72, 112, 'Alice', '€100'))
a(card(144, 72, 112, 'Bob', '€50'))
a(f'<g opacity="1">{held(P1_GONE)}' + card(268, 72, 112, 'total', '€150', SEAL) +
  text(380, 136, '€100 gone', anchor='end', size=15, fill=SEAL, ls='0', role='label') + '</g>')
a('</g>')
a(f'<line x1="20" y1="156" x2="380" y2="156" stroke="{PSOFT}" stroke-width="1" stroke-dasharray="2 4"/>')

# ---- below: the log that prevents it ----------------------------------------------------------------------------
a('<g data-panel="log">')
a(text(20, 182, 'the log, written first', size=14, fill=PMUTED, role='label'))
recs = [('deposit: Dan 20 → 70', PARCH, L1), ('deposit commits', SAGE, L2), ('transfer: Alice 200 → 100', PARCH, L3)]
for i, (s, col, t) in enumerate(recs):
    y = 192 + i * 26
    a(f'<g opacity="1">{held(t)}' + obj(f'<rect x="20" y="{y}" width="262" height="22" rx="2" fill="none" stroke="{PSOFT}" stroke-width="1.2"/>',
                                        text(30, y + 16, s, size=14, fill=col, ls='0', role='label')) + '</g>')
a(stamp(338, 261, 'power cut', SEAL, CUT))
a(text(20, 294, 'data pages after the cut', size=14, fill=PMUTED, role='label'))
# Dan: stale 20 on the page, redone to 70
a(card(20, 304, 112, 'Dan', layers=(
    f'<g opacity="1">{until(REDO)}' + text(122, 342, '€20', anchor='end', size=16, fill=PARCH, ls='0', role='object') + '</g>',
    f'<g opacity="1">{held(REDO)}' + text(76, 342, '€20', anchor='end', size=14, fill=PMUTED, ls='0', role='object') +
    f'<line x1="44" y1="337" x2="78" y2="337" stroke="{PMUTED}" stroke-width="1.5"/>' +
    text(122, 342, '€70', anchor='end', size=16, fill=SAGE, ls='0', role='object') + '</g>')))
# Alice: 200 on the page until the transfer's debit reaches it early, undone back to 200
a(card(144, 304, 112, 'Alice', layers=(
    f'<g opacity="1">{until(EARLY)}' + text(246, 342, '€200', anchor='end', size=16, fill=PARCH, ls='0', role='object') + '</g>',
    f'<g opacity="0">{T.anim("opacity", [(0.0, 0.0), (EARLY - 0.001, 0.0), (EARLY, 1.0), (UNDO - 0.001, 1.0), (UNDO, 0.0), (D, 0.0)])}' +
    text(246, 342, '€100', anchor='end', size=16, fill=PARCH, ls='0', role='object') + '</g>',
    f'<g opacity="1">{held(UNDO)}' + text(196, 342, '€100', anchor='end', size=14, fill=PMUTED, ls='0', role='object') +
    f'<line x1="158" y1="337" x2="198" y2="337" stroke="{PMUTED}" stroke-width="1.5"/>' +
    text(246, 342, '€200', anchor='end', size=16, fill=SAGE, ls='0', role='object') + '</g>')))
a(card(268, 304, 112, 'Bob', '€50'))
a(stamp(76, 382, 'redo', SAGE, REDO))
a(stamp(200, 382, 'undo', BRASS, UNDO))
a(f'<g opacity="1">{held(DONE)}' + text(20, 432, 'deposit kept, transfer undone:', size=15, fill=SAGE, ls='0', role='label') +
  text(20, 454, 'nothing half done', size=15, fill=SAGE, ls='0', role='label') + '</g>')
a('</g>')
a('</svg>')
svg = '\n'.join(o)

caption = ('Top, a transfer with no transaction: the power fails after Alice is debited, and €100 vanishes. Below, every '
           'change reaches the log before the data pages, so recovery redoes the committed deposit that never reached its '
           'page and undoes the unfinished transfer.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>The transaction.</b> BEGIN and COMMIT fence the transfer: both updates count, or neither does.</li>
          <li><b>The log first.</b> Each change is appended to the write-ahead log and forced to disk (<code>fsync()</code>) before the commit is acknowledged.</li>
          <li><b>Pages later.</b> The data pages are written when convenient, so at a crash some committed changes are missing from them and some uncommitted ones are already there.</li>
          <li><b>Recovery.</b> It reads the log: a transaction with a commit record is redone, one without is undone. One mechanism gives both durability and atomicity.</li>
          <li><b>Variants.</b> This is the idea behind ARIES (IBM, 1992), which first repeats every logged change and then undoes the unfinished transactions; PostgreSQL only redoes, and its row versions keep uncommitted changes from ever being seen.</li>
        </ol>
      </details>'''
card_html = f'''<div class="diagram-card fig-v2" id="fig-13-6">
      <div class="diagram-label">Fig 13.6 · A bank transfer · the failure, and the log that prevents it</div>
      {svg}
      <p id="ch13-acid-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''

def place_merged_card():
    """Brief section 12 (round 4): a merged card keeps the HIGHER half's number, id and slot, after every paragraph between
    the halves. Here that is Fig 13.6 after ch13-acid-p4 (the log, lazy data pages, redo and undo), so the drawing uses
    only words taught before it; fig-13-5 and its caption ch13-acid-p3 are aliased in book.js to ch13-acid-p2, the
    paragraph before the lower half's old slot, so a stored reading position resumes before text not yet read."""
    from figlib import splice  # noqa: F401 (kept for symmetry with the other scripts)
    p = '/Users/yki/Documents/github/atheric/under-the-code/public/part-4.html'
    s = open(p).read()
    pat = lambda fid: re.compile(r'\n\s*<div class="diagram-card[^"]*" id="' + fid + r'">[\s\S]*?</details>\s*</div>')
    global card_html
    # the same label rule as figlib.splice: a separator keeps to the word before it, never alone at a line end
    card_html = re.sub(r'(<div class="diagram-label">)([^<]*)(</div>)', lambda g: g.group(1) + g.group(2).replace(' · ', '&nbsp;· ') + g.group(3), card_html, count=1)
    lower, higher = pat('fig-13-5').search(s), pat('fig-13-6').search(s)
    if lower and higher:          # the page before any merge: drop the lower card, replace the higher one
        s = s[:lower.start()] + s[lower.end():]
        higher = pat('fig-13-6').search(s)
        s = s[:higher.start()] + '\n    ' + card_html + s[higher.end():]
    elif lower or higher:         # an earlier merge left one card: replace it
        m = lower or higher
        s = s[:m.start()] + s[m.end():]
        p4 = re.search(r'<p id="ch13-acid-p4"[\s\S]*?</p>', s)
        s = s[:p4.end()] + '\n    ' + card_html + s[p4.end():]
    else:
        raise SystemExit('no Fig 13.5 or 13.6 card found')
    card = pat('fig-13-6').search(s); p4 = re.search(r'<p id="ch13-acid-p4"[\s\S]*?</p>', s)
    assert card and p4 and p4.end() <= card.start(), 'the merged card must sit after ch13-acid-p4'
    open(p, 'w').write(s)
    print('fig-13-6 written as the merged card, after ch13-acid-p4')

if __name__ == '__main__':
    place_merged_card()
