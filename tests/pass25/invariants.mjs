// Pass 25 invariants: every page (5 parts + index + account + glossary),
// Chromium + WebKit, 1440x900 / 375x667 / 320x568 signed out, plus 1440 and
// 375 signed in against the fake API.
//
//   node invariants.mjs [--browser=chromium] [--only=part-1] [-v]
//
// Checks per load: nav exactly 48.0px; anchor-id set identical to the HTML
// source; zero non-localhost requests; signed out -> zero /api requests; no
// console errors; no horizontal scroll; new runtime ids use the utc- prefix;
// (signed out) Tab-stop delta vs the pre-pass baseline (git BASELINE_REV):
// parts gain exactly one stop, .place-btn in the nav; other pages gain none;
// Pass 25 DOM contract (cue, place-btn, place bar, mark dots, live region).
// New-DOM checks SKIP with a message while the Pass 25 client is absent.
import {
  reporter, withServer, launch, browsersFor, newContext, watch, url, sourceHtml,
  FakeApi, VIEWPORTS, PAGES, PARTS, ANCHOR_RE, TABBABLE, BASELINE_REV, ARGS,
} from './lib.mjs';

const R = reporter('invariants');

const COLLECT = ([reSrc, html, tabbableSrc]) => {
  const re = new RegExp(reSrc);
  const anchorIds = root => [...root.querySelectorAll('[id]')]
    .filter(el => re.test(el.id) && !el.closest('svg')).map(el => el.id);
  const src = new DOMParser().parseFromString(html, 'text/html');
  const nav = document.querySelector('.book-nav');
  const tabbable = (0, eval)('(' + tabbableSrc + ')')();
  const q = s => document.querySelector(s);
  const vis = el => !!el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden' && getComputedStyle(el).display !== 'none';
  const cue = nav && nav.querySelector('span.reading-cue');
  const pb = nav && nav.querySelector('button.place-btn');
  const bar = q('#utc-placebar');
  const acc = nav && nav.querySelector('.book-account');
  const sns = [...document.querySelectorAll('.section-number')];
  const dots = sns.map(sn => sn.firstElementChild);
  const live = q('#utc-live');
  return {
    navH: nav ? nav.getBoundingClientRect().height : null,
    liveIds: anchorIds(document),
    srcIds: anchorIds(src),
    allIds: [...document.querySelectorAll('[id]')].map(e => e.id),
    srcAllIds: [...src.querySelectorAll('[id]')].map(e => e.id),
    scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth,
    clientWidth: document.documentElement.clientWidth,
    tabbable,
    tabInAriaHidden: tabbable.length ? [...document.querySelectorAll('[aria-hidden="true"] a[href], [aria-hidden="true"] button, [aria-hidden="true"] [tabindex]')]
      .filter(el => el.tabIndex >= 0 && !el.disabled && el.getClientRects().length).map(el => el.tagName + '.' + el.className).slice(0, 5) : [],
    newDom: {
      cue: !!cue, cueHidden: cue ? cue.getAttribute('aria-hidden') : null,
      cueHead: !!(cue && cue.querySelector('.cue-head')), cueMark: !!(cue && cue.querySelector('.cue-mark')),
      cueId: cue ? cue.id : null,
      pb: !!pb, pbExpanded: pb ? pb.getAttribute('aria-expanded') : null, pbControls: pb ? pb.getAttribute('aria-controls') : null,
      pbRect: pb ? pb.getBoundingClientRect().toJSON() : null, pbVisible: vis(pb),
      accRect: acc ? acc.getBoundingClientRect().toJSON() : null,
      bar: !!bar, barRole: bar ? bar.getAttribute('role') : null, barVisible: vis(bar),
      sections: sns.length,
      dotsOk: dots.filter(d => d && d.matches('button.mark-dot') && d.getAttribute('tabindex') === '-1' && d.getAttribute('aria-hidden') === 'true').length,
      anyDot: dots.some(d => d && d.matches && d.matches('.mark-dot')),
      live: !!live, liveAttr: live ? (live.getAttribute('aria-live') || live.getAttribute('role')) : null,
    },
  };
};

async function load(ctx, name, { debug = false } = {}) {
  const page = watch(await ctx.newPage());
  await page.goto(url(name, '', { debug }), { waitUntil: 'load' });
  try { await page.waitForLoadState('networkidle', { timeout: 6000 }); } catch {}
  await page.waitForTimeout(700);   // glossary tooltips + rail + cue injection
  const data = await page.evaluate(COLLECT, [ANCHOR_RE.source, sourceHtml(name), TABBABLE.toString()]);
  return { page, data };
}

function setDiff(a, b) {
  const sb = new Set(b); const sa = new Set(a);
  return { missing: b.filter(x => !sa.has(x)), extra: a.filter(x => !sb.has(x)) };
}
function multisetDiff(live, base) {
  const m = new Map();
  for (const x of base) m.set(x, (m.get(x) || 0) - 1);
  for (const x of live) m.set(x, (m.get(x) || 0) + 1);
  const added = [], removed = [];
  for (const [k, v] of m) { if (v > 0) added.push(k + (v > 1 ? ' ×' + v : '')); if (v < 0) removed.push(k + (v < -1 ? ' ×' + -v : '')); }
  return { added, removed };
}

function common(t, name, data, net, page, { signedOut }) {
  // 1 nav height
  if (data.navH === null) t.skip('nav 48.0px', 'no .book-nav on this page');
  else t.check(Math.abs(data.navH - 48) < 0.01, 'nav 48.0px', 'height ' + data.navH);
  // 2 anchor set
  const d = setDiff(data.liveIds, data.srcIds);
  t.check(!d.missing.length && !d.extra.length && data.liveIds.length === data.srcIds.length,
    'anchor-id set identical to source', data.liveIds.length + ' live / ' + data.srcIds.length + ' source'
      + (d.missing.length ? ' missing ' + d.missing.slice(0, 5).join(',') : '') + (d.extra.length ? ' extra ' + d.extra.slice(0, 5).join(',') : ''));
  // 3 external
  t.check(net.external.length === 0, 'zero non-localhost requests', net.external.slice(0, 3).join(' '));
  // 4 signed out -> zero api
  if (signedOut) {
    const reading = net.api.filter(a => !(name === 'account' && a.path.startsWith('/api/auth/')));
    t.check(reading.length === 0, name === 'account' ? 'signed out: zero /api requests (sign-in page: /api/auth/* exempt)' : 'signed out: zero /api requests',
      reading.map(a => a.method + ' ' + a.path).slice(0, 5).join(', '));
  }
  // 5 console
  t.check(page.__errors.length === 0, 'no console errors', page.__errors.slice(0, 3).join(' | '));
  // 6 h-scroll
  t.check(data.scrollWidth <= data.innerWidth, 'no horizontal scroll', 'scrollWidth ' + data.scrollWidth + ' innerWidth ' + data.innerWidth + ' clientWidth ' + data.clientWidth);
}

async function run() {
  const browsers = browsersFor(['chromium', 'webkit']);
  for (const bname of browsers) {
    const browser = await launch(bname);
    try {
      // ---------------- signed out, 3 viewports, with baseline deltas
      for (const [vname, viewport] of Object.entries(VIEWPORTS)) {
        await R.test(`${bname} ${vname} signed-out`, async () => {
          const live = await newContext(browser, { viewport, fake: new FakeApi({ signedIn: false }), signedIn: false });
          const base = await newContext(browser, { viewport, baseline: true, fake: new FakeApi({ signedIn: false }), signedIn: false });
          try {
            for (const name of PAGES) {
              const t = R.scoped(`${bname} ${viewport.width}x${viewport.height} out ${name}`);
              if (ARGS.only && !ARGS.only.test(name) && !ARGS.only.test(bname)) continue;
              live.net.api.length = 0; live.net.external.length = 0;
              const { page, data } = await load(live.ctx, name);
              common(t, name, data, live.net, page, { signedOut: true });
              await page.close();
              const { page: bp, data: bd } = await load(base.ctx, name);
              await bp.close();
              // runtime ids: new ones (vs source and vs baseline runtime) carry utc-
              const srcAll = new Set(data.srcAllIds), baseAll = new Set(bd.allIds);
              // glossary first-use anchors (term-*) follow the glossary, which later passes change by design
              const newIds = data.allIds.filter(id => !srcAll.has(id) && !baseAll.has(id) && !id.startsWith('term-'));
              t.check(newIds.every(id => id.startsWith('utc-')), 'injected ids use the utc- prefix only', newIds.filter(id => !id.startsWith('utc-')).slice(0, 5).join(','));
              t.check(!newIds.some(id => ANCHOR_RE.test(id)), 'no injected id matches the anchor regex');
              // Tab stops
              // Glossary terms and index entries are tab stops that follow the glossary (Pass 26 changed it by design).
              // Plain prose links (bare `a`, outside the nav) follow the text, which Pass 27 cuts by design.
              const gloss = d => /glossary-ref|glossary-entry-anchor/.test(d) || d === 'a';
              const diff = multisetDiff(data.tabbable.map(x => (x.inNav ? 'nav:' : '') + x.d).filter(d => !gloss(d)), bd.tabbable.map(x => (x.inNav ? 'nav:' : '') + x.d).filter(d => !gloss(d)));
              const detail = `live ${data.tabbable.length} vs baseline@${BASELINE_REV} ${bd.tabbable.length}; +[${diff.added.join(', ')}] -[${diff.removed.join(', ')}]`;
              const isPart = PARTS.includes(name);
              if (isPart && !data.newDom.pb) {
                t.skip('Tab-stop delta = +1 (place-btn)', 'new DOM absent (no .book-nav .place-btn) — ' + detail);
              } else if (isPart) {
                t.check(diff.added.length === 1 && diff.added[0] === 'nav:button.place-btn' && diff.removed.length === 0, 'Tab-stop delta = +1 (place-btn in the nav)', detail);
              } else {
                t.check(diff.added.length === 0 && diff.removed.length === 0, 'Tab-stop delta = 0 (non-part page)', detail);
              }
              t.check(data.tabInAriaHidden.length === 0, 'no focusable element inside aria-hidden (axe aria-hidden-focus)', data.tabInAriaHidden.join(', '));
              // Pass 25 DOM contract
              const n = data.newDom;
              if (!isPart || name === 'glossary') continue;
              if (!n.cue && !n.pb && !n.anyDot) {
                t.skip('Pass 25 DOM contract', 'new DOM absent (no span.reading-cue / button.place-btn / .mark-dot) — client not built yet');
                continue;
              }
              t.check(n.cue && n.cueHidden === 'true' && n.cueHead && n.cueMark && !n.cueId, 'span.reading-cue[aria-hidden] with .cue-head + .cue-mark, no id', JSON.stringify({ cue: n.cue, hid: n.cueHidden, head: n.cueHead, mark: n.cueMark, id: n.cueId }));
              t.check(n.pb && /^(true|false)$/.test(n.pbExpanded || '') && n.pbControls === 'utc-placebar', 'button.place-btn aria-expanded + aria-controls=utc-placebar', JSON.stringify({ exp: n.pbExpanded, ctl: n.pbControls }));
              t.check(n.bar && n.barRole === 'group' && !n.barVisible, '#utc-placebar role=group, hidden while closed', JSON.stringify({ bar: n.bar, role: n.barRole, visible: n.barVisible }));
              t.check(n.sections > 0 && n.dotsOk === n.sections, 'every .section-number starts with button.mark-dot[tabindex=-1][aria-hidden=true]', n.dotsOk + '/' + n.sections);
              t.check(n.live && /polite|status/.test(n.liveAttr || ''), '#utc-live polite live region', String(n.liveAttr));
              if (viewport.width <= 620 && n.pbRect && n.accRect) {
                const gap = n.accRect.left - n.pbRect.right;
                t.check(n.pbVisible && gap >= -0.5 && gap < 24, 'place-btn immediately left of the account mark (≤620px)', 'gap ' + gap.toFixed(1) + 'px');
              }
            }
          } finally { await live.ctx.close(); await base.ctx.close(); }
        }, { timeout: 900000, ignoreOnly: true });
      }
      // ---------------- signed in with the fake API (1440, 375)
      for (const vname of ['desktop', 'phone']) {
        const viewport = VIEWPORTS[vname];
        await R.test(`${bname} ${vname} signed-in`, async () => {
          const fake = new FakeApi();
          const live = await newContext(browser, { viewport, fake });
          try {
            for (const name of PAGES) {
              if (ARGS.only && !ARGS.only.test(name) && !ARGS.only.test(bname)) continue;
              const t = R.scoped(`${bname} ${viewport.width}x${viewport.height} in ${name}`);
              live.net.external.length = 0;
              const before = fake.unknown.length;
              const { page, data } = await load(live.ctx, name);
              common(t, name, data, live.net, page, { signedOut: false });
              t.check(fake.unknown.length === before, 'only known /api endpoints called', fake.unknown.slice(before).join(', '));
              await page.close();
            }
            const kinds = [...new Set(fake.calls.map(c => c.method + ' ' + c.path))];
            R.info(`${bname} ${vname} signed-in api calls`, kinds.join(', ') || 'none');
          } finally { await live.ctx.close(); }
        }, { timeout: 900000, ignoreOnly: true });
      }
    } finally { await browser.close(); }
  }
}

await withServer(run);
process.exit(R.summary());
