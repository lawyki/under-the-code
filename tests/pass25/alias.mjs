// Anchor-ID law: a stored place on a removed id must land exactly where the surviving id lands.
import { webkit, chromium } from '/Users/yki/.npm/_npx/361ceb562f3b3235/node_modules/playwright/index.mjs';
const [part, port, ...pairs] = process.argv.slice(2);
let bad = 0;
for (const bt of [chromium, webkit]) for (const vw of [375, 1440]) {
  const b = await bt.launch();
  for (const pr of pairs) { const [oldId, newId] = pr.split('=');
    for (const fr of [0, 0.5]) {
      const ys = [];
      for (const id of [oldId, newId]) {
        const ctx = await b.newContext({ viewport: { width: vw, height: 850 } });
        await ctx.addInitScript(([p, a, f]) => { try { localStorage.setItem('under-the-code:progress', JSON.stringify({ v: 1, part: p, anchor: a, fraction: f, timestamp: Date.now(), src: 'set' })); } catch (e) {} }, [part, id, fr]);
        const page = await ctx.newPage();
        await page.goto(`http://localhost:${port}/${part}`); await page.waitForTimeout(2200);
        ys.push(await page.evaluate(() => Math.round(scrollY))); await ctx.close();
      }
      const ok = ys[0] === ys[1] && ys[1] > 0; if (!ok) bad++;
      console.log(`${bt.name()} ${vw} ${oldId}->${newId} f=${fr} ${ys.join(' vs ')} ${ok ? 'ok' : 'FAIL'}`);
    }
  }
  await b.close();
}
console.log(bad ? `${bad} FAIL` : 'aliases: all zero delta'); process.exit(bad ? 1 : 0);
