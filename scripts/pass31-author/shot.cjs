const { chromium } = require(process.argv[2] + '/tests/pass25/node_modules/playwright');
const fs = require('fs');
const [,, root, part, id, out, t] = process.argv;
(async () => {
  const html = fs.readFileSync(`${root}/public/${part}.html`, 'utf8');
  const i = html.indexOf(`id="${id}"`); const a = html.indexOf('<svg', i); const b = html.indexOf('</svg>', a) + 6;
  const br = await chromium.launch(); const pg = await br.newPage({ viewport: { width: 440, height: 560 }, deviceScaleFactor: 2 });
  await pg.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Space+Mono&display=swap" rel="stylesheet"></head><body style="margin:20px;background:#0d2740">${html.slice(a, b)}</body></html>`);
  await pg.waitForTimeout(800);
  await pg.evaluate((t) => { const s = document.querySelector('svg'); s.setAttribute('width', 400); s.pauseAnimations(); s.setCurrentTime(+t); }, t || 0);
  await pg.waitForTimeout(200);
  await pg.screenshot({ path: out, fullPage: true }); await br.close();
})();
