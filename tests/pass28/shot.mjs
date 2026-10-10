// Screenshot one figure card: node shot.mjs <part> <fig-id> <outdir> [--widths=375,1440] [--times=0,1,4] [--browser=webkit] [--open]
import { chromium, webkit } from '/Users/yki/.npm/_npx/361ceb562f3b3235/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const [part, fig, outdir] = process.argv.slice(2);
const ARGS = Object.fromEntries(process.argv.slice(5).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = process.env.FIG_ROOT || new URL('../../public/', import.meta.url).pathname;
const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.png': 'image/png' };
const server = http.createServer((q, r) => { let u = decodeURIComponent(new URL(q.url, 'http://x').pathname); if (u.startsWith('/api/')) { r.writeHead(404); return r.end('{}'); }
  let f = path.join(ROOT, u === '/' ? 'index.html' : u); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html'; if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': T[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
await new Promise(r => server.listen(0, r));
fs.mkdirSync(outdir, { recursive: true });
const widths = String(ARGS.widths || '375,1440').split(',').map(Number);
const times = String(ARGS.times || '0').split(',').map(Number);
const b = await (ARGS.browser === 'webkit' ? webkit : chromium).launch();
for (const w of widths) {
  const page = await (await b.newContext({ viewport: { width: w, height: 1000 }, deviceScaleFactor: 2 })).newPage();
  await page.goto(`http://localhost:${server.address().port}/${part}#${fig}`); await page.waitForTimeout(1200);
  await page.addStyleTag({ content: '.book-nav, .chapter-nav, .reading-cue, .cue-hit, .place-bar, .book-progress { visibility: hidden !important; }' });
  if (ARGS.open) await page.evaluate(id => { const d = document.querySelector('#' + id + ' details'); if (d) d.open = true; }, fig);
  for (const t of times) {
    await page.evaluate(([id, t]) => { const s = document.querySelector('#' + id + ' svg'); s.pauseAnimations(); s.setCurrentTime(t); }, [fig, t]);
    await page.waitForTimeout(150);
    const el = await page.$('#' + fig); await el.scrollIntoViewIfNeeded();
    await el.screenshot({ path: `${outdir}/${fig}-${ARGS.browser || 'chromium'}-${w}-t${t}${ARGS.open ? '-open' : ''}.png` });
  }
}
await b.close(); server.close(); console.log('shots in', outdir);
