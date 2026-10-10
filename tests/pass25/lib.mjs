// Shared helpers for the Pass 25 "Place and Marks" Playwright harness.
// Plain Node + playwright library API; no test runner.
//
//   reporter()       PASS/FAIL/SKIP/WARN lines + summary + exit code
//   FakeApi          in-memory /api/position + /api/marks + /api/auth/me
//   newContext()     context with routing: external -> abort+record,
//                    /api/* -> fake (or 404 + record), baseline -> git HEAD files
//   openPart()       seeded localStorage, optional page.clock, ?utc-debug
//   requireClient()  waits for window.__utcPlace; NoClientError when absent
//   snap/T/progress/marks readers, scroll + reading drivers
import { chromium, webkit } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { startServer, ROOT, PORT } from './serve.mjs';

export const BASE = 'http://localhost:' + PORT;
export const REPO = path.resolve(ROOT, '..');
export const PARTS = ['part-1', 'part-2', 'part-3', 'part-4', 'part-5'];
export const PAGES = [...PARTS, 'index', 'account', 'glossary'];
export const VIEWPORTS = {
  desktop: { width: 1440, height: 900 },
  phone: { width: 375, height: 667 },
  small: { width: 320, height: 568 },
};
export const ANCHOR_RE = /^(ch[0-9B][^ ]*|fig-[0-9]+-[0-9]+[a-z]?)$/;
export const PARA_RE = /^ch[0-9B][A-Za-z0-9]*-[A-Za-z0-9-]+-p\d+$/;
export const PROGRESS_KEY = 'under-the-code:progress';
export const MARKS_KEY = 'under-the-code:marks';
export const READING_LINE = 56;
// The commit the baseline (pre-Pass-25) files are read from, for the
// Tab-stop and runtime-id deltas. Override with UTC_BASELINE=<rev>.
export const BASELINE_REV = process.env.UTC_BASELINE || 'd1bbb42';

// ---------------------------------------------------------------- CLI args
export function args() {
  const out = { browsers: null, only: null, headed: false, verbose: false };
  for (const a of process.argv.slice(2)) {
    let m;
    if ((m = a.match(/^--browser=(.+)$/))) out.browsers = m[1].split(',');
    else if ((m = a.match(/^--only=(.+)$/))) out.only = new RegExp(m[1], 'i');
    else if (a === '--headed') out.headed = true;
    else if (a === '-v' || a === '--verbose') out.verbose = true;
  }
  return out;
}
export const ARGS = args();

// ---------------------------------------------------------------- reporter
export class NoClientError extends Error {}
export class SkipError extends Error {}
let CLIENT_MISSING = false;

export function reporter(suite) {
  const counts = { pass: 0, fail: 0, skip: 0, warn: 0 };
  const failures = [];
  const t0 = Date.now();
  function line(kind, name, detail) {
    const tag = { pass: 'PASS', fail: 'FAIL', skip: 'SKIP', warn: 'WARN', info: 'INFO' }[kind];
    if (kind in counts) counts[kind]++;
    if (kind === 'fail') failures.push(name + (detail ? ' — ' + detail : ''));
    const d = detail ? '  (' + String(detail).replace(/\s+/g, ' ').slice(0, 400) + ')' : '';
    console.log(tag.padEnd(4) + '  [' + suite + '] ' + name + d);
  }
  function scoped(prefix) {
    const n = s => (prefix ? prefix + ' › ' : '') + s;
    const api = {
      pass: (s, d) => line('pass', n(s), d),
      fail: (s, d) => line('fail', n(s), d),
      warn: (s, d) => line('warn', n(s), d),
      info: (s, d) => line('info', n(s), d),
      skip: (s, d) => line('skip', n(s), d),
      check(cond, s, d) { line(cond ? 'pass' : 'fail', n(s), d); return !!cond; },
      soft(cond, s, d) { line(cond ? 'pass' : 'warn', n(s), d); return !!cond; },
      eq(a, b, s, d) {
        const ok = JSON.stringify(a) === JSON.stringify(b);
        line(ok ? 'pass' : 'fail', n(s), (ok ? '' : 'got ' + JSON.stringify(a) + ' want ' + JSON.stringify(b)) + (d ? ' ' + d : ''));
        return ok;
      },
      near(a, b, tol, s, d) {
        const ok = typeof a === 'number' && typeof b === 'number' && Math.abs(a - b) <= tol;
        line(ok ? 'pass' : 'fail', n(s), 'got ' + a + ' want ' + b + ' ±' + tol + (d ? ' ' + d : ''));
        return ok;
      },
      // Abort the current test as skipped (thrown, caught by test()).
      skipTest(reason) { throw new SkipError(reason); },
    };
    return api;
  }
  const root = scoped('');
  return Object.assign(root, {
    scoped,
    // Run one named test with a timeout; never lets an error escape.
    async test(name, fn, { timeout = 240000, ignoreOnly = false } = {}) {
      if (!ignoreOnly && ARGS.only && !ARGS.only.test(name)) return;
      const t = scoped(name);
      let timer;
      try {
        await Promise.race([
          fn(t),
          new Promise((_, rej) => { timer = setTimeout(() => rej(new Error('test timeout ' + timeout + 'ms')), timeout); }),
        ]);
      } catch (e) {
        if (e instanceof SkipError) line('skip', name, e.message);
        else if (e instanceof NoClientError) line('fail', name, 'client missing: ' + e.message);
        else line('fail', name, 'error: ' + (e && e.stack ? e.stack.split('\n').slice(0, 3).join(' | ') : e));
      } finally { clearTimeout(timer); }
    },
    summary() {
      const s = ((Date.now() - t0) / 1000).toFixed(1);
      console.log('\nSUMMARY [' + suite + '] ' + counts.pass + ' pass, ' + counts.fail + ' fail, '
        + counts.skip + ' skip, ' + counts.warn + ' warn  (' + s + ' s)'
        + (CLIENT_MISSING ? '\nNOTE: window.__utcPlace was absent — the Pass 25 client is not built yet (or ?utc-debug is not wired).' : ''));
      if (failures.length) {
        console.log('Failures:');
        failures.slice(0, 60).forEach(f => console.log('  - ' + f.slice(0, 300)));
        if (failures.length > 60) console.log('  … ' + (failures.length - 60) + ' more');
      }
      return counts.fail ? 1 : 0;
    },
    counts,
  });
}

// ---------------------------------------------------------------- browsers
const ENGINES = { chromium, webkit };
export async function withServer(fn) {
  const { server } = await startServer();
  try { return await fn(); } finally { if (server) server.close(); }
}
export async function launch(name) {
  return ENGINES[name].launch({ headless: !ARGS.headed });
}
export function browsersFor(defaults) {
  return (ARGS.browsers || defaults).filter(b => ENGINES[b]);
}

// ---------------------------------------------------------------- sources
const srcCache = new Map();
export function sourceHtml(pageName) {
  const file = path.join(ROOT, (pageName === 'index' ? 'index' : pageName) + '.html');
  if (!srcCache.has(file)) srcCache.set(file, fs.readFileSync(file, 'utf8'));
  return srcCache.get(file);
}
const gitCache = new Map();
export function baselineFile(rel) {
  if (gitCache.has(rel)) return gitCache.get(rel);
  let buf = null;
  try {
    buf = execFileSync('git', ['-C', REPO, 'show', BASELINE_REV + ':public/' + rel],
      { stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: 64 << 20 });
  } catch { buf = null; }
  gitCache.set(rel, buf);
  return buf;
}

function decode(s) {
  return s.replace(/<br\s*\/?>/gi, ' ').replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–').replace(/&rsquo;/g, '’').replace(/&lsquo;/g, '‘')
    .replace(/&ldquo;/g, '“').replace(/&rdquo;/g, '”').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
    .replace(/\s+/g, ' ').trim();
}
// Labels for a seeded progress record, parsed from the HTML source (close
// enough for seeding; tests that assert labels compute them in the browser).
export function sourceLabels(part, anchor) {
  const html = sourceHtml(part);
  const idx = html.indexOf('id="' + anchor + '"');
  if (idx < 0) throw new Error('anchor ' + anchor + ' not in ' + part);
  const secRe = /<section class="section[^"]*" id="([^"]+)"/g;
  let sec = null, secIdx = -1, m;
  while ((m = secRe.exec(html)) && m.index <= idx) { sec = m[1]; secIdx = m.index; }
  const section = sec || anchor;
  const chapterId = section.split('-')[0];
  const chIdx = html.indexOf('id="' + chapterId + '"');
  const h1 = chIdx >= 0 ? html.slice(chIdx).match(/<h1[^>]*>([\s\S]*?)<\/h1>/) : null;
  const tail = secIdx >= 0 ? html.slice(secIdx) : '';
  const sn = tail.match(/<div class="section-number">([\s\S]*?)<\/div>/);
  const h2 = tail.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);
  const n = chapterId.replace(/^ch/, '');
  return {
    section, chapterId,
    chapterNum: chapterId === 'chBridge' ? 'Bridge' : (/^\d+$/.test(n) ? 'Chapter ' + n : chapterId),
    chapterTitle: h1 ? decode(h1[1]) : '',
    sectionLabel: sn ? decode(sn[1]) : '',
    sectionTitle: h2 ? decode(h2[1]) : '',
  };
}
export function progressRecord(part, anchor, fraction = 0, extra = {}) {
  return Object.assign({ v: 2, part, anchor, fraction }, sourceLabels(part, anchor),
    { k: anchor, src: 'auto', timestamp: Date.now() - 60000 }, extra);
}

// ---------------------------------------------------------------- fake API
// Implements the Pass 25 contract (mirrors functions/api/marks.js and the
// versioned position save). One instance may be attached to several contexts
// so two "devices" sync through it.
export class FakeApi {
  constructor(opts = {}) {
    this.signedIn = opts.signedIn !== false;
    this.owner = opts.owner || 'a1b2c3d4e5f60718';
    this.email = opts.email || 'reader@example.test';
    this.position = opts.position || null;
    this.updatedAt = opts.updatedAt || (this.position ? Date.now() - 3600e3 : 0);
    this.marks = new Map();       // "part|a" -> {part,a,c,x,t,v}
    this.vmax = 0;
    this.limit = 250;
    this.calls = [];              // every /api request seen by a route
    this.inflight = {};
    this.maxInflight = {};
    this.holds = [];
    this.failures = [];
    this.unknown = [];
  }
  key(m, p) { return m + ' ' + p; }
  // Hold the next request matching method+path prefix until release().
  hold(method, prefix) {
    let release, seenResolve;
    const h = { method, prefix, used: false };
    h.gate = new Promise(r => { release = r; });
    h.seen = new Promise(r => { seenResolve = r; });
    h.release = () => release();
    h._seen = seenResolve;
    this.holds.push(h);
    return h;
  }
  failNext(method, prefix, status, body = { error: 'fake_failure' }, times = 1) {
    this.failures.push({ method, prefix, status, body, times });
  }
  seedMark(part, a, c, extra = {}) {
    const v = this.nextV();
    const row = Object.assign({ part, a, c, x: c ? 0 : 1, t: Date.now() - 1000, v }, extra);
    this.marks.set(part + '|' + a, row);
    return row;
  }
  nextV() { this.vmax = Math.max(Date.now(), this.vmax + 1); return this.vmax; }
  liveCount() { let n = 0; for (const r of this.marks.values()) if (!r.x) n++; return n; }
  callsTo(method, prefix) { return this.calls.filter(c => c.method === method && c.path.startsWith(prefix)); }

  async handle(route, request, pageTag) {
    const url = new URL(request.url());
    const method = request.method();
    const p = url.pathname;
    let body = null;
    try { const raw = request.postData(); body = raw ? JSON.parse(raw) : null; } catch { body = '<unparsable>'; }
    const call = { method, path: p, query: url.search, body, type: request.resourceType(), at: Date.now(), page: pageTag, status: null };
    this.calls.push(call);
    const k = this.key(method, p);
    this.inflight[k] = (this.inflight[k] || 0) + 1;
    this.maxInflight[k] = Math.max(this.maxInflight[k] || 0, this.inflight[k]);
    try {
      const h = this.holds.find(x => !x.used && x.method === method && p.startsWith(x.prefix));
      if (h) { h.used = true; h.call = call; h._seen(call); await h.gate; }
      let res;
      const f = this.failures.find(x => x.times > 0 && x.method === method && p.startsWith(x.prefix));
      if (f) { f.times--; res = { status: f.status, json: f.body }; }
      else res = this.respond(method, p, url, body);
      call.status = res.status;
      call.response = res.json;
      await route.fulfill({ status: res.status, contentType: 'application/json', body: JSON.stringify(res.json) });
    } catch (e) {
      call.status = 'error:' + e.message;
      try { await route.abort(); } catch {}
    } finally { this.inflight[k]--; }
  }

  respond(method, p, url, body) {
    const ok = j => ({ status: 200, json: j });
    const err = (s, e, extra = {}) => ({ status: s, json: Object.assign({ error: e }, extra) });
    if (p === '/api/position') {
      if (!this.signedIn) return err(401, 'signed_out');
      if (method === 'GET') return ok(this.position ? { position: this.position, updated_at: this.updatedAt } : { position: null });
      if (method === 'POST') {
        if (!body || typeof body !== 'object' || !/^part-[1-5]$/.test(body.part || '') || typeof body.anchor !== 'string') return err(400, 'bad_request');
        const cid = typeof body.cid === 'string' ? body.cid : null;
        const seq = Number.isSafeInteger(body.seq) ? body.seq : null;
        if (cid && seq != null && this.position && this.position.cid === cid
            && typeof this.position.seq === 'number' && seq <= this.position.seq) {
          return err(409, 'stale', { updated_at: this.updatedAt });
        }
        const clean = {};
        for (const f of ['part', 'anchor', 'fraction', 'section', 'chapterId', 'chapterNum', 'chapterTitle', 'sectionLabel', 'sectionTitle']) {
          if (body[f] !== undefined) clean[f] = body[f];
        }
        if (body.src === 'auto' || body.src === 'set') clean.src = body.src;
        if (cid && seq != null) { clean.cid = cid; clean.seq = seq; }
        this.position = clean;
        this.updatedAt = Math.max(Date.now(), this.updatedAt + 1);
        return ok(seq != null ? { ok: true, updated_at: this.updatedAt, seq } : { ok: true, updated_at: this.updatedAt });
      }
    }
    if (p === '/api/marks') {
      if (!this.signedIn) return err(401, 'signed_out');
      if (method === 'GET') {
        const since = /^\d{1,16}$/.test(url.searchParams.get('since') || '') ? Number(url.searchParams.get('since')) : 0;
        const rows = [...this.marks.values()].filter(r => r.v > since).sort((a, b) => a.v - b.v).map(r => Object.assign({}, r));
        const all = [...this.marks.values()].map(r => r.v);
        return ok({ owner: this.owner, cursor: rows.length ? rows[rows.length - 1].v : (all.length ? Math.max(...all) : since), rows });
      }
      if (method === 'POST') {
        if (!body || body.v !== 1 || !Array.isArray(body.ops) || body.ops.length < 1 || body.ops.length > 50) return err(400, 'bad_ops');
        const ops = new Map();
        for (const op of body.ops) {
          if (!op || !/^part-[1-5]$/.test(op.part || '') || !/^ch[0-9B][A-Za-z0-9-]{0,95}$/.test(op.a || '')
              || !Number.isInteger(op.c) || op.c < 0 || op.c > 5) return err(400, 'bad_op');
          const key = op.part + '|' + op.a; ops.delete(key); ops.set(key, op);
        }
        const live = new Set([...this.marks.values()].filter(r => !r.x).map(r => r.part + '|' + r.a));
        const before = live.size;
        for (const [key, op] of ops) { if (op.c > 0) live.add(key); else live.delete(key); }
        if (live.size > this.limit && live.size > before) return err(409, 'mark_limit', { limit: this.limit });
        const now = Date.now(), rows = [];
        for (const [key, op] of ops) {
          const old = this.marks.get(key);
          const t = old ? Math.max(now, old.t + 1) : now;
          const row = op.c > 0
            ? { part: op.part, a: op.a, c: op.c, x: 0, t, v: this.nextV() }
            : { part: op.part, a: op.a, c: old ? old.c : 0, x: 1, t, v: this.nextV() };
          this.marks.set(key, row); rows.push(Object.assign({}, row));
        }
        return ok({ ok: true, rows });
      }
    }
    if (p === '/api/auth/me') {
      if (!this.signedIn) return err(401, 'signed_out');
      return ok({ email: this.email, hasPassword: true, passkeyCount: 0, recent: false });
    }
    if (p === '/api/auth/credentials') return this.signedIn ? ok({ passkeys: [] }) : err(401, 'signed_out');
    if (p === '/api/auth/passkey/login-options') {
      // Pre-existing account-page conditional-UI request (signed out); a
      // plausible options object so the page stays quiet.
      return ok({ challenge: 'dGVzdC1jaGFsbGVuZ2UtMDAwMDAwMDAwMDAwMDAwMDA', timeout: 60000, rpId: 'localhost', allowCredentials: [], userVerification: 'preferred' });
    }
    if (p === '/api/auth/logout') { this.signedIn = false; return ok({ ok: true }); }
    this.unknown.push(method + ' ' + p);
    return err(404, 'not_found');
  }
}

// ---------------------------------------------------------------- contexts
// net: {all:[url], external:[url], api:[{method,path,type}]} recorded from
// the context's 'request' event (sees beacons even if a route doesn't).
export async function newContext(browser, opts = {}) {
  const {
    viewport = VIEWPORTS.desktop, fake = null, signedIn = !!fake,
    // UTC_FORCE_BASELINE=1 serves the pre-pass files everywhere (proves the
    // suites fail cleanly when the client / __utcPlace is absent).
    baseline = process.env.UTC_FORCE_BASELINE === '1',
    reducedMotion, forcedColors, colorScheme, hasTouch, isMobile, deviceScaleFactor,
    initScripts = [],
  } = opts;
  const ctxOpts = { viewport };
  if (reducedMotion) ctxOpts.reducedMotion = reducedMotion;
  if (forcedColors) ctxOpts.forcedColors = forcedColors;
  if (colorScheme) ctxOpts.colorScheme = colorScheme;
  if (hasTouch) ctxOpts.hasTouch = true;
  if (isMobile && browser.browserType().name() === 'chromium') ctxOpts.isMobile = true;
  if (deviceScaleFactor) ctxOpts.deviceScaleFactor = deviceScaleFactor;
  const ctx = await browser.newContext(ctxOpts);
  const net = { all: [], external: [], api: [], unstubbed: [] };
  ctx.on('request', r => {
    const u = r.url();
    net.all.push(u);
    let url; try { url = new URL(u); } catch { return; }
    if (url.protocol === 'data:' || url.protocol === 'blob:' || url.protocol === 'about:') return;
    if (url.hostname !== 'localhost' && url.hostname !== '127.0.0.1') net.external.push(u);
    else if (url.pathname.startsWith('/api/')) net.api.push({ method: r.method(), path: url.pathname, type: r.resourceType(), at: Date.now() });
  });
  let pageSeq = 0;
  const pageTags = new WeakMap();
  ctx.on('page', p => pageTags.set(p, 'p' + (++pageSeq)));
  await ctx.route('**/*', async (route, request) => {
    let url;
    try { url = new URL(request.url()); } catch { return route.continue(); }
    if (url.hostname !== 'localhost' && url.hostname !== '127.0.0.1') return route.abort();
    if (url.pathname.startsWith('/api/')) {
      let tag = null;
      try { tag = pageTags.get(request.frame().page()) || null; } catch {}
      if (fake) return fake.handle(route, request, tag);
      net.unstubbed.push(request.method() + ' ' + url.pathname);
      return route.fulfill({ status: 404, contentType: 'application/json', body: '{"error":"no_fake"}' });
    }
    if (baseline && request.method() === 'GET') {
      let rel = decodeURIComponent(url.pathname).replace(/^\//, '');
      if (rel === '') rel = 'index';
      if (!/\.[a-z0-9]+$/i.test(rel)) rel += '.html';
      if (/\.(html|js|css|json)$/.test(rel)) {
        const buf = baselineFile(rel);
        if (buf) {
          const type = rel.endsWith('.html') ? 'text/html; charset=utf-8' : rel.endsWith('.js') ? 'text/javascript'
            : rel.endsWith('.css') ? 'text/css' : 'application/json';
          return route.fulfill({ status: 200, contentType: type, body: buf });
        }
      }
    }
    return route.continue();
  });
  if (signedIn) {
    await ctx.addCookies([{ name: 'under_signedin', value: '1', domain: 'localhost', path: '/', sameSite: 'Lax' }]);
  }
  for (const s of initScripts) await ctx.addInitScript(s);
  return { ctx, net, fake };
}
export async function setSignedIn(ctx, on) {
  if (on) await ctx.addCookies([{ name: 'under_signedin', value: '1', domain: 'localhost', path: '/', sameSite: 'Lax' }]);
  else await ctx.clearCookies({ name: 'under_signedin' });
}

// Console errors + page errors, per page.
export function watch(page) {
  page.__errors = [];
  page.on('console', m => { if (m.type() === 'error') page.__errors.push('console: ' + m.text()); });
  page.on('pageerror', e => page.__errors.push('pageerror: ' + e.message));
  return page;
}

// Instrumentation shared by suites (init script; runs before page scripts).
export const INSTRUMENT = () => {
  window.__rectReads = 0;
  window.__countRects = false;
  const orig = Element.prototype.getBoundingClientRect;
  Element.prototype.getBoundingClientRect = function () {
    if (window.__countRects) window.__rectReads++;
    return orig.apply(this, arguments);
  };
  window.__longtasks = [];
  try {
    new PerformanceObserver(l => { for (const e of l.getEntries()) window.__longtasks.push({ d: e.duration, t: e.startTime }); })
      .observe({ type: 'longtask', buffered: true });
  } catch (e) { window.__longtaskUnsupported = true; }
  window.__live = [];
  const hook = () => {
    const el = document.getElementById('utc-live');
    if (!el || el.__hooked) return;
    el.__hooked = true;
    new MutationObserver(() => { const s = el.textContent.trim(); if (s) window.__live.push(s); })
      .observe(el, { childList: true, characterData: true, subtree: true });
  };
  // #utc-live may be injected late; watch for it, then watch its text.
  const seek = new MutationObserver(() => { if (document.getElementById('utc-live')) { hook(); seek.disconnect(); } });
  seek.observe(document, { childList: true, subtree: true });
};

// ---------------------------------------------------------------- pages
export function url(pageName, hash = '', { debug = true, query = '' } = {}) {
  const p = pageName === 'index' ? '/' : '/' + pageName;
  const q = [debug ? 'utc-debug' : '', query].filter(Boolean).join('&');
  return BASE + p + (q ? '?' + q : '') + (hash ? '#' + hash : '');
}
// Write localStorage on the origin without running book.js (robots.txt).
export async function seed(page, { progress, marks, raw } = {}) {
  await page.goto(BASE + '/robots.txt');
  await page.evaluate(([pk, mk, p, m, r]) => {
    if (p !== undefined) { if (p === null) localStorage.removeItem(pk); else localStorage.setItem(pk, JSON.stringify(p)); }
    if (m !== undefined) { if (m === null) localStorage.removeItem(mk); else localStorage.setItem(mk, JSON.stringify(m)); }
    if (r) for (const [k, v] of Object.entries(r)) localStorage.setItem(k, v);
  }, [PROGRESS_KEY, MARKS_KEY, progress, marks, raw]);
}
// Open a part page. opts: {hash, seedProgress, seedMarks, clock, debug, waitReading}
export async function openPart(ctx, part, opts = {}) {
  const page = watch(await ctx.newPage());
  if (opts.clock) { try { await page.clock.install(); } catch (e) { if (!/already/i.test(e.message)) throw e; } }
  if (opts.seedProgress !== undefined || opts.seedMarks !== undefined) {
    await seed(page, { progress: opts.seedProgress, marks: opts.seedMarks });
  }
  await page.goto(url(part, opts.hash || '', { debug: opts.debug !== false }), { waitUntil: 'load' });
  await parkPointer(page);
  if (opts.debug !== false) await requireClient(page);
  if (opts.waitReading) await waitState(page, 'READING', 8000);
  return page;
}

export async function requireClient(page, timeout) {
  const ms = timeout || (CLIENT_MISSING ? 300 : 6000);
  try {
    await page.waitForFunction(() => !!(window.__utcPlace && typeof window.__utcPlace.snapshot === 'function'), null, { timeout: ms });
  } catch {
    CLIENT_MISSING = true;
    throw new NoClientError('window.__utcPlace absent on ' + page.url() + ' after ' + ms + ' ms');
  }
}
export function clientMissing() { return CLIENT_MISSING; }

export const snap = page => page.evaluate(() => window.__utcPlace.snapshot());
export const setT = (page, o) => page.evaluate(o => Object.assign(window.__utcPlace.T, o), o);
export const getT = page => page.evaluate(() => Object.assign({}, window.__utcPlace.T));
export const readLS = (page, key) => page.evaluate(k => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } }, key);
export const progress = page => readLS(page, PROGRESS_KEY);
export const marksLS = page => readLS(page, MARKS_KEY);

export async function waitState(page, state, timeout = 6000) {
  const end = Date.now() + timeout;
  let s = null;
  while (Date.now() < end) {
    s = await snap(page);
    if (s && (Array.isArray(state) ? state.includes(s.state) : s.state === state)) return s;
    await page.waitForTimeout(100);
  }
  throw new Error('state ' + JSON.stringify(state) + ' not reached in ' + timeout + ' ms (last: ' + JSON.stringify(s && { state: s.state, C: s.C && s.C.anchor }) + ')');
}
export async function waitFor(page, fn, arg, timeout = 5000) {
  try { await page.waitForFunction(fn, arg, { timeout }); return true; } catch { return false; }
}

// Time: page.clock when installed (fast-forward, fires timers), else real.
export async function advance(page, ms) {
  try { await page.clock.runFor(ms); } catch (e) {
    if (/install/i.test(String(e.message))) await page.waitForTimeout(ms); else throw e;
  }
}
export const settle = (page, ms = 500) => page.waitForTimeout(ms);
export async function blurAll(page) { await page.evaluate(() => document.activeElement && document.activeElement.blur && document.activeElement.blur()); }

export async function wheel(page, dy, after = 500) {
  await page.mouse.wheel(0, dy);
  await settle(page, after);
}
// Many wheel events inside `ms` real milliseconds (a fling / burst).
export async function burst(page, total, ms = 300, n = 10) {
  for (let i = 0; i < n; i++) { await page.mouse.wheel(0, total / n); await page.waitForTimeout(ms / n); }
}
export async function key(page, k, after = 800) { await page.keyboard.press(k); await settle(page, after); }
export async function scriptedJump(page, dy) {
  await page.evaluate(dy => window.scrollTo({ top: window.scrollY + dy, behavior: 'instant' }), dy);
  await settle(page, 600);
}
// Reading: every `every` ms of (fake) time, one small forward wheel step.
export async function read(page, ms, { step = 120, every = 8000 } = {}) {
  let left = ms;
  while (left > 0) {
    const d = Math.min(every, left);
    await advance(page, d);
    left -= d;
    if (left >= 0 && d === every) await wheel(page, step, 450);
  }
}
// Keep "input in the last 120 s" true without scrolling.
// The pointer rests in the right page margin (wheel events scroll the
// document; no glossary term sits under it, so no hover tooltips open).
export async function parkPointer(page) {
  const v = page.viewportSize();
  await page.mouse.move(v.width - 8, Math.round(v.height * 0.6));
}
export async function nudgePointer(page) {
  const v = page.viewportSize();
  await page.mouse.move(v.width - 11, Math.round(v.height * 0.6));
  await page.mouse.move(v.width - 8, Math.round(v.height * 0.6));
}
// Idle without scrolling (pointer nudged every 60 s so tracking stays live).
export async function idle(page, ms, { nudge = false } = {}) {
  let left = ms;
  while (left > 0) {
    const d = Math.min(60000, left);
    await advance(page, d); left -= d;
    if (nudge) await nudgePointer(page);
  }
}

// Simulated tab hide / show (document.visibilityState override + events).
export async function setHidden(page, hidden) {
  await page.evaluate(h => {
    Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => (h ? 'hidden' : 'visible') });
    Object.defineProperty(document, 'hidden', { configurable: true, get: () => h });
    document.dispatchEvent(new Event('visibilitychange'));
    if (h) window.dispatchEvent(new PageTransitionEvent('pagehide', { persisted: true }));
    else window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true }));
  }, hidden);
}

// Anchor geometry in the live page.
export async function anchorScrollY(page, anchor, fraction = 0) {
  return page.evaluate(([a, f, line]) => {
    const el = document.getElementById(a);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return Math.max(0, window.scrollY + r.top + f * r.height - line);
  }, [anchor, fraction, READING_LINE]);
}
export async function anchorDrift(page, anchor, fraction = 0) {
  return page.evaluate(([a, f, line]) => {
    const el = document.getElementById(a);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return r.top + f * r.height - line;
  }, [anchor, fraction, READING_LINE]);
}

// Place-bar helpers (contract strings).
// Straight or typographic apostrophe both accepted.
export const PLACE_LABELS = {
  set: /Set to where I['’]m reading/, go: /Go to saved place/, mark: /Mark this section/,
  back: /Back to before the detour/, track: /Let the book track/, undo: /^\s*Undo\b/,
};
export async function openPlaceBar(page) {
  const btn = page.locator('.book-nav .place-btn');
  if (!(await btn.count())) throw new Error('.place-btn missing');
  if ((await btn.getAttribute('aria-expanded')) !== 'true') await btn.click();
  await page.locator('#utc-placebar').waitFor({ state: 'visible', timeout: 3000 });
}
export async function placeAction(page, which) {
  await openPlaceBar(page);
  const b = page.locator('#utc-placebar button:visible', { hasText: PLACE_LABELS[which] || which }).first();
  if (!(await b.count())) throw new Error('place bar button ' + (PLACE_LABELS[which] || which) + ' missing or hidden');
  await b.click();
  await settle(page, 300);
}
export async function placeBarHas(page, which) {
  const b = page.locator('#utc-placebar button', { hasText: PLACE_LABELS[which] || which });
  return (await b.count()) > 0 && (await b.first().isVisible());
}

// Tab stops (tabbable, visible) described as short selectors.
export const TABBABLE = () => {
  const sel = 'a[href], area[href], button, input, select, textarea, iframe, summary, [tabindex], [contenteditable=""], [contenteditable="true"], audio[controls], video[controls]';
  const out = [];
  for (const el of document.querySelectorAll(sel)) {
    if (el.disabled) continue;
    if (el.tabIndex < 0) continue;
    if (el.closest('[inert]')) continue;
    if (el.closest('details:not([open])') && el.tagName !== 'SUMMARY') continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (!el.getClientRects().length) continue;
    if (el.closest('[hidden]')) continue;
    if (el.matches('[popover]:not(:popover-open), [popover]:not(:popover-open) *')) continue;
    const cls = (typeof el.className === 'string' ? el.className.trim().split(/\s+/)[0] : '') || '';
    out.push({ d: el.tagName.toLowerCase() + (cls ? '.' + cls : ''), inNav: !!el.closest('.book-nav') });
  }
  return out;
};

// ---------------------------------------------------------------- geometry
// B and L as the spec defines them, measured in the page (navB = 48 + the
// chapter nav's offsetHeight).
export async function geom(page) {
  return page.evaluate(() => {
    const cn = document.querySelector('.chapter-nav');
    const navB = 48 + (cn ? cn.offsetHeight : 0);
    const B = Math.max(200, innerHeight - navB);
    return { navB, B, L: navB + 0.3 * B, innerHeight, scrollY, max: document.documentElement.scrollHeight - innerHeight };
  });
}
export function sameC(a, b, tol = 0.011) {
  return !!(a && b && a.part === b.part && a.anchor === b.anchor && Math.abs((a.fraction || 0) - (b.fraction || 0)) <= tol);
}
export function cAdvanced(prev, cur) {
  if (!prev || !cur) return false;
  if (typeof prev.y === 'number' && typeof cur.y === 'number') return cur.y > prev.y + 0.5;
  return prev.anchor !== cur.anchor || (cur.fraction || 0) > (prev.fraction || 0);
}
export const brief = c => (c ? c.part + '#' + c.anchor + '@' + (typeof c.fraction === 'number' ? c.fraction.toFixed(3) : c.fraction) + (c.src ? ' ' + c.src : '') : 'null');

// Start state for every trace: C0 = part-1#ch1-kernel-p2 (seeded, restored).
export const C0 = { part: 'part-1', anchor: 'ch1-kernel-p2' };
export async function startC0(browser, opts = {}) {
  const fake = opts.fake || (opts.signedIn ? new FakeApi() : null);
  const { ctx, net } = await newContext(browser, {
    viewport: opts.viewport || VIEWPORTS.desktop, fake, signedIn: !!(opts.signedIn || opts.fake),
    reducedMotion: opts.reducedMotion, hasTouch: opts.hasTouch, isMobile: opts.isMobile,
    initScripts: [INSTRUMENT],
  });
  const anchor = opts.anchor || C0.anchor, part = opts.part || C0.part;
  const page = await openPart(ctx, part, {
    hash: opts.noHash ? '' : anchor, seedProgress: progressRecord(part, anchor, opts.fraction || 0),
    clock: opts.clock !== false, seedMarks: opts.seedMarks,
  });
  const s0 = await waitState(page, ['READING', 'PINNED'], 8000);
  return { ctx, net, fake, page, s0 };
}

// Two short traces used for reduced-motion / viewport identity comparisons.
export async function traceWheel(page) {
  const s0 = await snap(page); const out = [];
  for (let i = 0; i < 3; i++) {
    await advance(page, 8000); await wheel(page, 120, 450); await advance(page, 600);
    const s = await snap(page);
    out.push({ anchor: s.C && s.C.anchor, f: s.C && Math.round(s.C.fraction * 100), dw: s.writes - s0.writes, state: s.state });
  }
  return out;
}
export async function traceFling(page) {
  const s0 = await snap(page); const g = await geom(page);
  await burst(page, 3 * g.B, 300); await settle(page, 300);
  await burst(page, -3 * g.B, 300); await settle(page, 900);
  const s = await snap(page);
  return { dw: s.writes - s0.writes, same: sameC(s.C, s0.C), state: s.state };
}

// Cross-page navigation drops ?utc-debug; rewrite an in-book link so the
// destination page also exposes __utcPlace. Returns the original href.
export async function clickInBookLink(page, selectorOrFn) {
  const href = await page.evaluate(sel => new Promise(resolve => {
    const a = typeof sel === 'string' ? document.querySelector(sel) : null;
    if (!a) return resolve(null);
    const h = a.getAttribute('href');
    a.setAttribute('href', h.replace(/^(\/?part-[1-5]|\/?index|\/)(?=#|$)/, m => m + '?utc-debug'));
    resolve(h);
    setTimeout(() => a.click(), 0);   // after evaluate returns (navigation destroys the context)
  }), selectorOrFn).catch(() => null);
  return href;
}
