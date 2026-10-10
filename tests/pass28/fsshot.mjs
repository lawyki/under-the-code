// Fullscreen view of a figure: node fsshot.mjs <part> <fig-id> <outdir> [--widths=375,1440] [--browser=webkit]
import { chromium, webkit } from '/Users/yki/.npm/_npx/361ceb562f3b3235/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const [part, fig, outdir] = process.argv.slice(2);
const ARGS = Object.fromEntries(process.argv.slice(5).map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const ROOT = new URL('../../public/', import.meta.url).pathname;
const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };
const server = http.createServer((q, r) => { let u = decodeURIComponent(new URL(q.url, 'http://x').pathname); if (u.startsWith('/api/')) { r.writeHead(404); return r.end('{}'); }
  let f = path.join(ROOT, u === '/' ? 'index.html' : u); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html'; if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': T[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
await new Promise(r => server.listen(0, r)); fs.mkdirSync(outdir, { recursive: true });
const b = await (ARGS.browser === 'webkit' ? webkit : chromium).launch();
for (const w of String(ARGS.widths || '375,1440').split(',').map(Number)) {
  const h = w < 600 ? 780 : 900;
  const page = await (await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 })).newPage();
  await page.goto(`http://localhost:${server.address().port}/${part}#${fig}`); await page.waitForTimeout(1200);
  await page.click(`#${fig} .fs-button`); await page.waitForTimeout(900);
  const m = await page.evaluate(id => { const s = document.querySelector('#' + id + ' svg'); const r = s.getBoundingClientRect(); s.pauseAnimations(); s.setCurrentTime(0);
    return { svgW: Math.round(r.width), svgH: Math.round(r.height), inView: r.top >= 0 && r.bottom <= innerHeight + 1 }; }, fig);
  await page.screenshot({ path: `${outdir}/${fig}-fs-${ARGS.browser || 'chromium'}-${w}.png` });
  console.log(w, JSON.stringify(m));
}
await b.close(); server.close();
