# Fig 12.4 · The same fetch · three eras of async syntax (Pass 28, law 3). Chart Room plate. One job (get the user,
# then their orders, then the first invoice, then render it) spelled three ways: nested callbacks (from 1995),
# a promise chain (ES2015), async/await (ES2017). Each step lights its line in all three at once, so the same
# logic can be followed across the three shapes. t=0 (shift): every step lit.
import figlib
from figlib import Timeline, text, splice, SPACE, CYAN, ROUTE, CSOFT, CMUTED
figlib.FONT = SPACE

GREEN, GOLD = '#9bd89b', '#d4a853'
STEPS = [(CYAN, 1.0), (GREEN, 2.4), (GOLD, 3.8), (ROUTE, 5.2)]   # user, orders, invoice, render
ERAS = [('callbacks, from 1995', [
            ('getUser(id, function (user) {', 0),
            ('  getOrders(user, function (orders) {', 1),
            ('    getInvoice(orders[0], function (inv) {', 2),
            ('      render(inv);', 3),
            ('    });', None), ('  });', None), ('});', None)]),
        ('promises, ES2015', [
            ('getUser(id)', 0),
            ('  .then(getOrders)', 1),
            ('  .then(orders =&gt; getInvoice(orders[0]))', 2),
            ('  .then(render)', 3),
            ('  .catch(showError);', None)]),
        ('async/await, ES2017', [
            ('async function show(id) {', None),
            ('  try {', None),
            ('    const user = await getUser(id);', 0),
            ('    const orders = await getOrders(user);', 1),
            ('    render(await getInvoice(orders[0]));', (2, 3)),
            ('  } catch (err) { showError(err); }', None),
            ('}', None)])]
W = 400
LS = 18
D = 9.0
T = Timeline(D, shift=8.4)
win = lambda t0: T.anim('opacity', [(0.0, 1.0), (0.3, 1.0), (0.305, 0.0), (t0 - 0.002, 0.0), (t0, 1.0), (D, 1.0)])
o = []; a = o.append
y = 22
for head, lines in ERAS:
    a(text(10, y, head, anchor='start', size=13, fill=CSOFT, ls='0'))
    top = y + 10
    a(f'<rect x="10" y="{top}" width="380" height="{LS * len(lines) + 10}" rx="5" fill="#0a1c2d" stroke="{CMUTED}" stroke-opacity="0.45"/>')
    for i, (s, st) in enumerate(lines):
        ly = top + 19 + i * LS
        if st is not None:
            sts = st if isinstance(st, tuple) else (st,)
            col, t0 = STEPS[sts[0]]
            a(f'<g class="fx" opacity="0">{win(t0)}<rect x="12" y="{ly - 13}" width="376" height="{LS - 1}" rx="2" fill="{col}" fill-opacity="0.16"/>'
              f'<rect x="12" y="{ly - 13}" width="3" height="{LS - 1}" fill="{col}"/></g>')
        a(text(22, ly, s.replace(' ', '&#160;'), anchor='start', size=13, fill=CSOFT, ls='0'))
    y = top + LS * len(lines) + 10 + 34
H = y - 20
o.insert(0, f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="svgt-part3-59 svgd-part3-59">')
o.insert(1, '<title id="svgt-part3-59">Fig 12.4 · The same fetch · three eras of async syntax</title>')
o.insert(2, '<desc id="svgd-part3-59">The same job written three ways: get a user, then their orders, then the first invoice, then render it. '
  'With callbacks each step nests inside the previous one, the code stepping further right. With promises the steps form a flat chain of then calls with one catch at the end. '
  'With async and await the steps read like ordinary straight-line code inside a try block. The matching lines light together in all three.</desc>')
a('</svg>')
svg = '\n'.join(o)

caption = ('The same four steps (the user, then the orders, then the invoice, then render) spelled three ways: callbacks nested inside callbacks, a flat chain of promises, and async/await that reads like straight-line code.')
how = '''<details class="fig-how">
        <summary>How it works</summary>
        <ol>
          <li><b>Callbacks.</b> Each step nests inside the last, and every level needs its own error handling; forget one and the error is lost.</li>
          <li><b>Promises.</b> Each <code>.then</code> returns a new promise, so the chain stays flat and one <code>.catch</code> at the end catches a failure anywhere in it.</li>
          <li><b>async/await.</b> Each <code>await</code> pauses the function and lets the loop run other work; when the promise settles, the rest of the function continues as a microtask (Fig 12.3).</li>
        </ol>
      </details>'''
card = f'''<div class="diagram-card fig-v2" id="fig-12-4">
      <div class="diagram-label">Fig 12.4 · The same fetch · three eras of async syntax</div>
      {svg}
      <p id="ch12-loop-p5" class="diagram-caption">{caption}</p>
      {how}
    </div>'''
if __name__ == '__main__':
    splice('part-3', 'fig-12-4', 'ch12-loop-p5', card)
