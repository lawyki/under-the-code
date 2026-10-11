// Pass 30 bare capture (docs/pass-29-30-brief.md, BEFORE STARTING 5; the Gate 2 describers see these).
// The <svg> alone at a chosen SMIL time. Kept out: the figure number, <title>/<desc> (never painted),
// the label, caption, "How it works" strip, page chrome and prose. Kept in: the SVG's own text and the
// plate painted behind it, so the describer sees what the reader sees and nothing that explains it.
const USAGE = `node tests/pass30/bare.mjs --page=part-1 (--id=fig-1-2[,fig-1-3] | --selector='.chapter-hero-visual svg' [--index=N | --all])
    --out=<dir> [--width=375[,1440]] [--times=0,4,8 | --frames=3] [--browser=chromium|webkit] [--dsf=2]
    [--height=1000] [--click=<selector>[,<selector>]] [--json=<manifest.json>]
  --times   absolute SMIL seconds. --frames=N: N frames at k/N of the cycle (largest begin + dur).
            Default: static 1 frame at t=0; animated --frames=3; plays once (the cover) its end state.
  --dsf     deviceScaleFactor, default 2. Icons are 22 CSS px: use --dsf=6.
  --click   click these first (opens UI that holds an icon, e.g. --click=.place-btn for .pb-close svg).
  Heroes render above 768 px and the cover from 880 px: capture them at --width=1440.
  Files: <out>/<id | kind-index[-controlClass][-ancestorId]>-<width>-t<time>.png. --json merges into an existing manifest.
  A file another page, target or engine already wrote in <out> (owners in <out>/.bare-owners.json) is not
  overwritten: it prints COLLIDE and counts as a problem. Give each engine its own --out.`;
import { chromium, webkit } from '../pass25/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';

// split at the first '=' only: selectors may carry their own ([data-x="y"])
const ARGS = Object.fromEntries(process.argv.slice(2).map(a => { const m = a.match(/^--([^=]+)(?:=([\s\S]*))?$/) || [, a]; return [m[1], m[2] ?? true]; }));
if (ARGS.help || !ARGS.page || !ARGS.out || !(ARGS.id || ARGS.selector) || !['chromium', 'webkit', undefined].includes(ARGS.browser)) { console.log(USAGE); process.exit(ARGS.help ? 0 : 2); }
const ROOT = process.env.FIG_ROOT || new URL('../../public/', import.meta.url).pathname;
// a bare flag (--times) or an empty item (--times=0,,4) is not a number; Number() would read 1 or 0
const num = v => v === true || String(v).trim() === '' ? NaN : Number(v);
const WIDTHS = [...new Set(String(ARGS.width || '375').split(',').map(num))];
const ENG = ARGS.browser || 'chromium', DSF = num(ARGS.dsf || 2), H = num(ARGS.height || 1000);
const TIMES = ARGS.times !== undefined ? String(ARGS.times).split(',').map(num) : null;
const FRAMES = ARGS.frames ? Math.max(1, parseInt(ARGS.frames, 10)) : null;
const PICK = { ids: ARGS.id ? [...new Set(String(ARGS.id).split(','))] : null, selector: ARGS.selector || null, index: num(ARGS.index || 0), all: !!ARGS.all };
// a bad number would otherwise surface as a stack trace from setCurrentTime or Playwright
if (![...WIDTHS, DSF, H, PICK.index, ...(TIMES || []), ...(FRAMES === null ? [] : [FRAMES])].every(Number.isFinite) || ![...WIDTHS, DSF, H].every(x => x > 0)) { console.log(USAGE); process.exit(2); }
// page chrome that can sit over a figure (the brief's list, as shot.mjs hides it, plus the card's fullscreen buttons)
const CHROME = '.book-nav, .chapter-nav, .reading-cue, .cue-hit, .place-bar, .book-progress, .fs-button, .fs-close';
// a figure number drawn inside the svg; (?![a-z]) keeps words like "Fight" or "Figma" (the brief's /^\s*Fig(ure)?\.?\s*[0-9A-Z]/i, minus those)
const FIGNUM = '^\\s*Fig(?:ure)?(?![a-z])\\.?\\s*[0-9A-Z]';

const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.png': 'image/png' };
const server = http.createServer((q, r) => { let u = decodeURIComponent(new URL(q.url, 'http://x').pathname); if (u.startsWith('/api/')) { r.writeHead(404); return r.end('{}'); }
  let f = path.join(ROOT, u === '/' ? 'index.html' : u); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f += '.html'; if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': T[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
await new Promise(r => server.listen(0, r));
fs.mkdirSync(ARGS.out, { recursive: true });

// in the page: find each target's <svg>, mark it data-bare=k, say whether it renders at this width
function resolve({ ids, selector, index, all }) {
  const pick = el => !el ? null : el instanceof SVGSVGElement ? el : el instanceof SVGElement ? el.ownerSVGElement
    : el.querySelector(':scope > svg') || [...el.querySelectorAll('svg')].find(s => !s.closest('.fs-button, .fs-close')) || null;
  let list;
  if (ids) list = ids.map(id => ({ target: id, name: id, svg: pick(document.getElementById(id)) }));
  else { const m = [...document.querySelectorAll(selector)]; list = (all ? m.map((_, i) => i) : [index]).map(i => ({ target: `${selector}[${i}]`, i, svg: pick(m[i]) })); }
  return list.map((t, k) => {
    const s = t.svg; if (!s) return { k, target: t.target, missing: true };
    s.setAttribute('data-bare', k);
    const kind = s.matches('.cover-exhibit-svg') ? 'cover' : s.closest('.chapter-hero-visual') ? 'hero' : s.closest('.insight-icon') ? 'insight'
      : s.closest('button, a, [role="button"], [role="menuitem"]') ? 'icon' : s.closest('.diagram-card, .light-diagram') ? 'fig' : 'svg';
    // an icon is named by its control too: the expand and close svgs of one card are both index 0 under that card's id
    const anc = (s.closest('[id]') || {}).id, ctl = kind === 'icon' && s.closest('button, a, [role="button"], [role="menuitem"]');
    // opacity 0 (a menu still fading in) would shoot a bare plate and pass, so it counts as not rendered
    const r = s.getBoundingClientRect(), vis = s.checkVisibility ? s.checkVisibility({ visibilityProperty: true, opacityProperty: true }) : true;
    return { k, target: t.target, kind, name: t.name || `${kind}-${t.i}${ctl && ctl.classList[0] ? '-' + ctl.classList[0] : ''}${anc ? '-' + anc : ''}`, rendered: r.width >= 1 && r.height >= 1 && vis, size: `${Math.round(r.width)}x${Math.round(r.height)}${vis ? '' : ', hidden or opacity 0'}` };
  });
}

// in the page: hide what could explain or cover the target; read its animation clock
function prepare([k, chrome, fignum]) {
  const svg = document.querySelector(`[data-bare="${k}"]`); let root = svg; while (root.ownerSVGElement) root = root.ownerSVGElement;
  const hide = el => el.setAttribute('data-bare-hide', '');
  document.querySelectorAll('[data-bare-hide]').forEach(e => e.removeAttribute('data-bare-hide'));   // the previous target's set
  document.querySelectorAll(chrome).forEach(el => { if (!el.contains(svg)) hide(el); });           // an icon's own bar or button stays
  const card = svg.closest('.diagram-card, .light-diagram');
  if (card) card.querySelectorAll('.diagram-label, .diagram-caption, details.fig-how').forEach(hide);
  const rx = new RegExp(fignum, 'i'), figNum = [...svg.querySelectorAll('text')].filter(t => rx.test(t.textContent)).map(t => (hide(t), t.textContent.trim()));
  svg.scrollIntoView({ block: 'center' });
  // clock values: 8s, 500ms, 1.5min, 0:08, bare seconds; events, syncbases, 'indefinite' are not clocks
  const clock = v => { let m; v = v.trim();
    if ((m = v.match(/^([-+]?[\d.]+)(h|min|s|ms)?$/))) return +m[1] * { h: 3600, min: 60, s: 1, ms: 0.001 }[m[2] || 's'];
    if ((m = v.match(/^(?:(\d+):)?(\d+):([\d.]+)$/))) return (+m[1] || 0) * 3600 + +m[2] * 60 + +m[3];
    return null; };
  let cycle = 0, forever = false; const smil = [...svg.querySelectorAll('animate, animateTransform, animateMotion, set')];
  for (const a of smil) {
    const b = (a.getAttribute('begin') || '0').split(';').map(clock).filter(x => x !== null);
    cycle = Math.max(cycle, (b.length ? Math.max(...b) : 0) + (clock(a.getAttribute('dur') || '') ?? 0));
    if (/indefinite/.test((a.getAttribute('repeatCount') || '') + (a.getAttribute('repeatDur') || ''))) forever = true;
  }
  // CSS animations inside the svg (the cover's rise, ignition, bloom): their end counts toward a play-once end state
  let cssEnd = 0, cssLoop = 0; const css = document.getAnimations().filter(a => a.effect && a.effect.target && svg.contains(a.effect.target));
  for (const a of css) { const t = a.effect.getComputedTiming();
    if (t.endTime === Infinity) { forever = true; cssLoop = Math.max(cssLoop, (t.delay + t.duration) / 1000); } else cssEnd = Math.max(cssEnd, t.endTime / 1000); }
  return { animated: smil.length + css.length > 0, forever, cycle: cycle || cssLoop, end: Math.max(cycle, cssEnd), figNum };
}

// in the page: freeze SMIL (on the outermost svg, the time container) and the svg's CSS animations at t
function freeze([k, t]) {
  let root = document.querySelector(`[data-bare="${k}"]`); while (root.ownerSVGElement) root = root.ownerSVGElement;
  root.pauseAnimations(); root.setCurrentTime(t);
  for (const a of document.getAnimations()) if (a.effect && a.effect.target && root.contains(a.effect.target)) { a.pause(); a.currentTime = t * 1000; }
  return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => r())));
}
// book.js's off-screen pauser may unpause a figure on an intersection change: confirm the frame held
const held = ([k, t]) => { let root = document.querySelector(`[data-bare="${k}"]`); while (root.ownerSVGElement) root = root.ownerSVGElement; return root.animationsPaused() && Math.abs(root.getCurrentTime() - t) < 0.02; };

// in the page: hide any other text painted inside the svg's box (prose under a hero, a chip, a tooltip)
function guard(k) {
  const svg = document.querySelector(`[data-bare="${k}"]`), R = svg.getBoundingClientRect(), hit = [], rg = document.createRange();
  const meets = b => b.width > 0 && b.right > R.left && b.left < R.right && b.bottom > R.top && b.top < R.bottom;
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: n => n.data.trim() && !svg.contains(n) ? 1 : 3 });
  for (let n; (n = tw.nextNode());) {
    const p = n.parentElement; if (!p || p.contains(svg) || !meets(p.getBoundingClientRect())) continue;
    const cs = getComputedStyle(p); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    rg.selectNodeContents(n); if (![...rg.getClientRects()].some(meets)) continue;
    p.setAttribute('data-bare-hide', ''); hit.push(n.data.trim().slice(0, 40));
  }
  return hit;
}

const t0 = Date.now(), round = x => Math.round(x * 1000) / 1000, manifest = []; let bad = 0;
// who wrote each file in --out (by basename, so a relative or absolute --out agree): the registry kept there, plus
// any --json row for this dir. A rerun of the same page, target and engine replaces its file; anything else is refused.
const OUT = path.resolve(ARGS.out), REG = path.join(OUT, '.bare-owners.json'), owner = new Map();
const own = m => owner.set(path.basename(m.file), { file: path.basename(m.file), page: m.page, target: m.target, browser: m.browser });
try { JSON.parse(fs.readFileSync(REG, 'utf8')).forEach(own); } catch {}
if (ARGS.json) try { JSON.parse(fs.readFileSync(ARGS.json, 'utf8')).filter(m => path.dirname(path.resolve(m.file)) === OUT).forEach(own); } catch {}
const browser = await (ENG === 'webkit' ? webkit : chromium).launch();
for (const w of WIDTHS) {
  // reducedMotion 'no-preference': the page force-pauses nothing; only this script stops the clock
  const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: DSF, reducedMotion: 'no-preference' });
  const page = await ctx.newPage();
  await page.goto(`http://localhost:${server.address().port}/${ARGS.page}`, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts && document.fonts.ready); await page.waitForTimeout(500);
  // .reveal cards wait for a scroll to fade in: show them as revealed; [data-bare-hide] is this script's hiding
  await page.addStyleTag({ content: '.reveal { opacity: 1 !important; transform: none !important; transition: none !important; } [data-bare-hide] { visibility: hidden !important; }' });
  for (const sel of ARGS.click ? String(ARGS.click).split(',') : []) { await page.click(sel); await page.waitForTimeout(400); }
  for (const tg of await page.evaluate(resolve, PICK)) {
    if (tg.missing) { console.log(`MISS ${ARGS.page} ${tg.target}: no element or no <svg> in it`); bad++; continue; }
    if (!tg.rendered) { console.log(`MISS ${ARGS.page} ${tg.target}: not rendered at ${w} px (${tg.size}). Heroes render above 768 px, the cover from 880 px: try --width=1440`); bad++; continue; }
    const info = await page.evaluate(prepare, [tg.k, CHROME, FIGNUM]);
    await page.waitForTimeout(350);   // let the scroll's intersection callbacks (pauser, reading place) settle before the clock stops
    // a loop is sampled over its cycle; a play-once svg (the cover) over its real end, SMIL and CSS together
    const span = info.forever ? info.cycle : info.end;
    const times = TIMES ? [...new Set(TIMES.map(t => round(Math.max(0, t))))]   // a repeated time is one file, one row
      : !info.animated || !span ? [0]
      : !info.forever && !FRAMES ? [round(info.end)]   // plays once (the cover): its end state
      : Array.from({ length: FRAMES || 3 }, (_, i) => round(i / (FRAMES || 3) * span));
    let hiddenOverlap = null;
    for (const [i, t] of times.entries()) {
      const base = `${tg.name.replace(/[^\w.-]+/g, '_')}-${w}-t${t}.png`, file = path.join(ARGS.out, base), loc = page.locator(`[data-bare="${tg.k}"]`);
      const was = owner.get(base);
      if (was && (was.page !== ARGS.page || was.target !== tg.target || was.browser !== ENG)) {
        console.log(`COLLIDE ${file} (was ${was.page} ${was.target} ${was.browser}; now ${ARGS.page} ${tg.target} ${ENG}): not overwritten, use another --out`); bad++; continue; }
      await page.evaluate(freeze, [tg.k, t]);
      if (hiddenOverlap === null) hiddenOverlap = await page.evaluate(guard, tg.k);
      await loc.screenshot({ path: file });
      own({ file: base, page: ARGS.page, target: tg.target, browser: ENG }); fs.writeFileSync(REG, JSON.stringify([...owner.values()], null, 1));   // per shot: a crash mid-run still leaves the owners
      let ok = await page.evaluate(held, [tg.k, t]);
      if (!ok) { await page.evaluate(freeze, [tg.k, t]); await loc.screenshot({ path: file }); ok = await page.evaluate(held, [tg.k, t]); }
      console.log(`${ok ? 'shot' : 'DRIFT'} ${ENG} ${ARGS.page} ${tg.target} ${w} t${t} (${i + 1}/${times.length}${!info.animated ? ', static' : info.forever ? ', cycle ' + round(info.cycle) + 's' : ', plays once, ends ' + round(info.end) + 's'})${info.figNum.length ? ' hid fig number [' + info.figNum.join('; ') + ']' : ''}${hiddenOverlap.length ? ' hid overlapping text [' + hiddenOverlap.slice(0, 3).join('; ') + ']' : ''} -> ${file}`);
      if (!ok) bad++;
      manifest.push({ page: ARGS.page, target: tg.target, kind: tg.kind, browser: ENG, width: w, dsf: DSF, time: t, frame: i + 1, of: times.length, file, hiddenFigNumber: info.figNum.length ? info.figNum : false, hiddenOverlap, held: ok });
    }
  }
  await ctx.close();
}
await browser.close(); server.close();
if (ARGS.json) {   // merge: a chapter batch is built from several runs (one per page)
  let old = []; try { old = JSON.parse(fs.readFileSync(ARGS.json, 'utf8')); } catch {}
  // only a same-owner rerun reaches here with a file already listed (the guard refused the rest): its new row replaces the old
  const mine = new Set(manifest.map(m => path.resolve(m.file))); fs.writeFileSync(ARGS.json, JSON.stringify([...old.filter(m => !mine.has(path.resolve(m.file))), ...manifest], null, 1));
}
console.log(`bare: ${manifest.length} shots, ${bad} problems, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(bad ? 1 : 0);
