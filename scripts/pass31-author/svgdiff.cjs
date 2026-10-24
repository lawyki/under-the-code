const { chromium } = require(process.argv[2] + '/tests/pass25/node_modules/playwright');
const fs = require('fs');
const [,, root, S] = process.argv;
const pick = (html, id) => { const i = html.indexOf(`id="${id}"`); const a = html.indexOf('<svg', i); const b = html.indexOf('</svg>', a) + 6; return html.slice(a, b); };
(async () => {
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 420, height: 500 }, deviceScaleFactor: 2 });
  for (const [part, id] of [['part-2', 'fig-4-8'], ['part-4', 'fig-13-6']]) {
    const old = pick(fs.readFileSync(`${S}/old-${part}.html`, 'utf8'), id), neu = pick(fs.readFileSync(`${root}/public/${part}.html`, 'utf8'), id);
    const dur = +(neu.match(/data-dur="([\d.]+)"/) || [, 10])[1];
    const times = []; for (let t = 0; t < dur; t += 0.05) times.push(+t.toFixed(2));
    let worst = 0, worstT = null;
    const shot = async (svg, t) => { await pg.setContent(`<body style="margin:0;background:#111">${svg}</body>`); return pg.evaluate(async (t) => { const s = document.querySelector('svg'); s.pauseAnimations(); s.setCurrentTime(t); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, t).then(() => pg.screenshot()); };
    for (const t of times) {
      const a = await shot(old, t), b = await shot(neu, t);
      if (!a.equals(b)) { const n = Math.abs(a.length - b.length) + 1; if (n > worst) { worst = n; worstT = t; } }
      if (!a.equals(b) && worstT === t) fs.writeFileSync(`${S}/diff-${id}-${t}-old.png`, a), fs.writeFileSync(`${S}/diff-${id}-${t}-new.png`, b);
    }
    const diffs = [];
    for (const t of times) { const a = await shot(old, t), b = await shot(neu, t); if (!a.equals(b)) diffs.push(t); }
    console.log(id, 'frames', times.length, 'differing', diffs.length, diffs.slice(0, 20).join(' '));
  }
  await br.close();
})();
