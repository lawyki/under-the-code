(function () {
  'use strict';

  const ICON_EXPAND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>';
  const ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>';

  let activeCard = null;

  function withTransition(card, mutate) {
    if (document.startViewTransition) {
      card.classList.add('transitioning');
      const tx = document.startViewTransition(mutate);
      tx.finished.finally(() => card.classList.remove('transitioning'));
      return tx.finished;
    } else {
      mutate();
      return Promise.resolve();
    }
  }

  function enterFullscreen(card) {
    if (activeCard) return;
    activeCard = card;
    document.dispatchEvent(new CustomEvent('utc:overlay', { detail: { name: 'fs', open: true } }));
    // Run the morph transition uncluttered — no rainbow during the snap-to-fullscreen.
    const done = withTransition(card, () => {
      card.classList.add('is-fullscreen');
      document.body.classList.add('has-fullscreen');
    });
    // After the card has landed, light up the rainbow. The liquid-bg is
    // already in the DOM and painted; only opacity transitions, so this is
    // a single GPU-composited animation — no first-paint cost, no filter
    // chain interpolation, no staggered start times.
    done.then(() => {
      if (activeCard !== card) return;
      document.body.classList.add('liquid-active');
    }).catch(() => {});
  }

  function exitFullscreen() {
    if (!activeCard) return;
    const card = activeCard;
    activeCard = null;
    document.dispatchEvent(new CustomEvent('utc:overlay', { detail: { name: 'fs', open: false } }));
    // Snap the rainbow off instantly — base style has no transition, so this
    // applies in the same frame as the click. The View Transition then
    // snapshots a clean (rainbow-free) state, eliminating the close lag.
    document.body.classList.remove('liquid-active');
    // Flag the html element so the close transition runs at 0.32s instead
    // of the default 0.5s — feels immediate rather than luxurious.
    document.documentElement.classList.add('is-closing-fullscreen');
    withTransition(card, () => {
      card.classList.remove('is-fullscreen');
      document.body.classList.remove('has-fullscreen');
    }).finally(() => {
      document.documentElement.classList.remove('is-closing-fullscreen');
    });
  }

  document.querySelectorAll('.diagram-card, .light-diagram').forEach(card => {
    const expandBtn = document.createElement('button');
    expandBtn.className = 'fs-button';
    expandBtn.type = 'button';
    expandBtn.setAttribute('aria-label', 'View diagram fullscreen');
    expandBtn.innerHTML = ICON_EXPAND;
    expandBtn.addEventListener('click', e => {
      e.stopPropagation();
      enterFullscreen(card);
    });
    card.appendChild(expandBtn);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'fs-close';
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', 'Exit fullscreen');
    closeBtn.innerHTML = ICON_CLOSE;
    closeBtn.addEventListener('click', e => {
      e.stopPropagation();
      exitFullscreen();
    });
    card.appendChild(closeBtn);
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && activeCard && !e.defaultPrevented) exitFullscreen();
  });

  document.addEventListener('click', e => {
    if (activeCard && !activeCard.contains(e.target)) exitFullscreen();
  });
})();

// --- Account corner -----------------------------------------------------------
// A quiet way to find the account page: a bookmark at the right end of the top
// bar on part pages, and in the cover's top-right corner. Outline when signed
// out; filled gold when this browser holds a session (the JS-readable hint
// cookie — no request is made, so signed-out readers still generate zero API
// traffic).
(function () {
  'use strict';
  const nav = document.querySelector('.book-nav');
  const cover = document.querySelector('.cover');
  const host = nav || cover;
  if (!host) return;
  const signedIn = /(?:^|;\s*)under_signedin=1(?:;|$)/.test(document.cookie);
  const a = document.createElement('a');
  a.className = 'book-account' + (signedIn ? ' is-signed-in' : '');
  a.href = '/account';
  const label = signedIn ? 'Your account: your place is kept across devices' : 'Account: keep your place across devices';
  a.setAttribute('aria-label', label);
  a.title = label;
  a.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M4 2.5h8v11l-4-3-4 3z"/></svg>'
    + '<span class="book-account-label">' + (signedIn ? 'Account' : 'Sign in') + '</span>';
  if (nav) nav.classList.add('has-account');
  host.appendChild(a);
  // A 401 seen by the place module is more truthful than the hint cookie.
  document.addEventListener('utc:signedout', () => {
    a.classList.remove('is-signed-in');
    const out = 'Account: keep your place across devices';
    a.setAttribute('aria-label', out);
    a.title = out;
    const l = a.querySelector('.book-account-label');
    if (l) l.textContent = 'Sign in';
  });
})();

// --- Section progress rail ----------------------------------------------------
(function () {
  'use strict';

  const sections = Array.from(document.querySelectorAll('section.section[id^="ch"]'));
  if (!sections.length) return;

  const rail = document.createElement('aside');
  rail.className = 'section-rail';
  rail.setAttribute('aria-label', 'Section navigation');
  document.body.appendChild(rail);

  const visibleSet = new Set();
  let currentChapter = null;
  let activeId = null;

  function buildRailFor(chapter) {
    if (chapter === currentChapter) return;
    currentChapter = chapter;
    rail.innerHTML = '';
    const navItems = chapter.querySelectorAll('.chapter-nav .nav-item');
    navItems.forEach(item => {
      const href = item.getAttribute('href');
      if (!href) return;
      const tick = document.createElement('a');
      tick.className = 'rail-tick';
      tick.href = href;
      tick.dataset.target = href.slice(1);
      const label = document.createElement('span');
      label.className = 'rail-label';
      label.textContent = item.textContent.trim();
      tick.appendChild(label);
      rail.appendChild(tick);
    });
    paintActive();
    document.dispatchEvent(new CustomEvent('utc:rail'));
  }

  function paintActive() {
    rail.querySelectorAll('.rail-tick').forEach(t => {
      t.classList.toggle('active', t.dataset.target === activeId);
    });
    paintChapterNav();
  }

  // Pass 22: the horizontal .chapter-nav shows the same active section the
  // rail tracks (one observer, two readouts). When the active tab is outside
  // the nav's visible strip it is brought into view with an instant scroll —
  // no smooth chase while the reader scrolls, so nothing moves under the eye
  // and reduced-motion needs no special case.
  function paintChapterNav() {
    if (!currentChapter || !activeId) return;
    // Only the chapter in view asserts a current location.
    document.querySelectorAll('.chapter-nav [aria-current]').forEach(el => {
      if (!currentChapter.contains(el)) el.removeAttribute('aria-current');
    });
    const nav = currentChapter.querySelector('.chapter-nav');
    if (!nav) return;
    let activeItem = null;
    nav.querySelectorAll('.nav-item').forEach(item => {
      const on = item.getAttribute('href') === '#' + activeId;
      item.classList.toggle('active', on);
      if (on) { item.setAttribute('aria-current', 'location'); activeItem = item; }
      else item.removeAttribute('aria-current');
    });
    if (!activeItem || nav.scrollWidth <= nav.clientWidth + 1) return;
    const left = activeItem.offsetLeft - nav.offsetLeft;
    const right = left + activeItem.offsetWidth;
    const pad = 24;   // keep clear of the edge fade
    if (left < nav.scrollLeft + pad) nav.scrollLeft = Math.max(0, left - pad);
    else if (right > nav.scrollLeft + nav.clientWidth - pad) nav.scrollLeft = right - nav.clientWidth + pad;
  }

  function recompute() {
    if (visibleSet.size === 0) {
      rail.classList.remove('visible');
      return;
    }
    let topmost = null;
    let topmostY = Infinity;
    visibleSet.forEach(s => {
      const y = s.getBoundingClientRect().top;
      if (y < topmostY) {
        topmostY = y;
        topmost = s;
      }
    });
    if (!topmost) return;
    const chapterId = topmost.id.split('-')[0];
    const chapter = document.getElementById(chapterId);
    if (chapter) buildRailFor(chapter);
    if (topmost.id !== activeId) {
      activeId = topmost.id;
      paintActive();
    }
    rail.classList.add('visible');
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) visibleSet.add(entry.target);
      else visibleSet.delete(entry.target);
    });
    recompute();
  }, { rootMargin: '0px 0px -50% 0px' });

  sections.forEach(s => observer.observe(s));
})();

// --- Chapter-nav overflow affordance ------------------------------------------
// The horizontal .chapter-nav scrolls when a chapter has more section tabs than
// fit the width (always on mobile). A hidden scrollbar (macOS/iOS) left the last
// tab clipped with no hint that more exists. We flag which edges have off-screen
// content via [data-navscroll~="more-left|more-right"]; book.css fades that edge.
(function () {
  'use strict';

  const navs = document.querySelectorAll('.chapter-nav');
  if (!navs.length) return;

  function update(nav) {
    const max = nav.scrollWidth - nav.clientWidth;
    if (max <= 1) { nav.dataset.navscroll = 'none'; return; }
    const x = nav.scrollLeft;
    const state = (x > 1 ? 'more-left ' : '') + (x < max - 1 ? 'more-right' : '');
    nav.dataset.navscroll = state.trim() || 'none';
  }

  navs.forEach(nav => {
    update(nav);
    nav.addEventListener('scroll', () => update(nav), { passive: true });
  });

  const updateAll = () => navs.forEach(update);
  window.addEventListener('resize', updateAll, { passive: true });
  window.addEventListener('load', updateAll);
  if (window.ResizeObserver) {
    const ro = new ResizeObserver(updateAll);
    navs.forEach(n => ro.observe(n));
  }
})();

// --- Pause SMIL on off-screen figures + honor prefers-reduced-motion ----------
// Every <animate> in every figure SVG ticks continuously by default. With ~50
// figures in Part I alone, that's a real CPU/battery cost on mobile when
// scrolling through the book — even when 95% of those figures are nowhere near
// the viewport. SVG ships with pauseAnimations() / unpauseAnimations() on each
// <svg> element; we just drive them from an IntersectionObserver.
//
// Figures that are in fullscreen are excluded — they should always animate
// regardless of where the original card sits in the page.
//
// Accessibility: when the user has set `prefers-reduced-motion: reduce` at the
// OS level, we pause every SVG and never unpause. CSS animations/transitions are
// handled by the matching @media block in book.css; SMIL is JS-only because it
// ignores the CSS media query.
(function () {
  'use strict';
  if (!('IntersectionObserver' in window)) return;

  const allSvgs = document.querySelectorAll('svg');
  const figures = document.querySelectorAll('.diagram-card > svg, .light-diagram > svg');
  if (!figures.length) return;

  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  function pauseAll() {
    allSvgs.forEach(svg => {
      if (typeof svg.pauseAnimations === 'function') svg.pauseAnimations();
    });
  }

  // If the user prefers reduced motion: pause every SVG and do nothing else.
  if (motionQuery.matches) {
    pauseAll();
    // If they later change their preference at runtime, fall back to the
    // intersection-observer behavior by reloading.
    if (motionQuery.addEventListener) {
      motionQuery.addEventListener('change', e => { if (!e.matches) location.reload(); });
    }
    return;
  }

  // Start figures paused; the observer unpauses what's actually near the viewport.
  figures.forEach(svg => {
    if (typeof svg.pauseAnimations === 'function') svg.pauseAnimations();
  });

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const svg = entry.target;
      const card = svg.closest('.diagram-card, .light-diagram');
      const forcePlay = card && card.classList.contains('is-fullscreen');
      if (entry.isIntersecting || forcePlay) {
        if (typeof svg.unpauseAnimations === 'function') svg.unpauseAnimations();
      } else {
        if (typeof svg.pauseAnimations === 'function') svg.pauseAnimations();
      }
    });
  }, {
    rootMargin: '300px 0px',
    threshold: 0
  });

  figures.forEach(svg => io.observe(svg));

  // When a figure is opened fullscreen its inline counterpart may not be in
  // view, but we still want SMIL running for the user.
  const cards = document.querySelectorAll('.diagram-card, .light-diagram');
  const mo = new MutationObserver((mutations) => {
    mutations.forEach(m => {
      const card = m.target;
      const svg = card.querySelector(':scope > svg');
      if (!svg) return;
      if (card.classList.contains('is-fullscreen')) {
        if (typeof svg.unpauseAnimations === 'function') svg.unpauseAnimations();
      }
    });
  });
  cards.forEach(c => mo.observe(c, { attributes: true, attributeFilter: ['class'] }));

  // If the user toggles their preference to "reduce" at runtime, pause everything.
  if (motionQuery.addEventListener) {
    motionQuery.addEventListener('change', e => {
      if (e.matches) pauseAll();
    });
  }
})();

// --- Scroll-reveal entrance animation -----------------------------------------
// Diagram cards, pull-quotes, math callouts, and insight strips lift into view
// as the reader scrolls. Prose paragraphs are intentionally excluded — text
// should simply be there; only structural "furniture" earns an entrance.
// Staggered 90ms per batch so simultaneous entries don't snap in as a block.
// Fully respects prefers-reduced-motion (skipped entirely if set).
(function () {
  'use strict';
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const targets = document.querySelectorAll(
    '.diagram-card, .pull-quote, .math-callout, .insight-strip'
  );
  if (!targets.length) return;

  targets.forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver((entries) => {
    const entering = entries
      .filter(e => e.isIntersecting && !e.target.classList.contains('revealed'))
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

    entering.forEach((entry, i) => {
      const el = entry.target;
      setTimeout(() => {
        el.classList.add('revealed');
        observer.unobserve(el);
      }, i * 90);
    });
  }, {
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.05
  });

  targets.forEach(el => observer.observe(el));
})();

// --- Reading place: tracking, the cue, section marks, sync (Pass 25) ----------
// One saved place per reader, and it is the place they were READING, not
// wherever the page happens to be scrolled (UNDER.md §4y).
//
// The encoding is Pass 3's, unchanged: the deepest stable element id at the
// 56px reading line plus a fraction inside it, so a restore is pixel-exact on
// any viewport and old clients still read the record. What changed is WHEN a
// place is committed:
//   · An offset table (document tops of every anchor, paragraph character
//     counts) is built once per layout; the scroll listener only stores
//     scrollY and a timestamp.
//   · Scroll events group into bursts. A burst that looks like reading (small,
//     explained by input, within a characters-per-second budget) commits the
//     place 400ms after it ends. A burst that looks like seeking (a fling,
//     skipped text, a link, find-in-page, a long jump) starts an EXCURSION
//     that remembers where the reader was (R). Coming back costs nothing; only
//     sustained reading somewhere else promotes the excursion to the new
//     place — slowly for look-ups (links, other parts, going back), quickly
//     for a reader who skipped ahead on purpose.
//   · Labels (chapter, §, ¶) come from K, the anchor at the attention line a
//     third of the way down the reading area, never from the 56px line.
//
// The cue: a 2px line on the bar's bottom edge — chapter progress and a mark
// at the saved place (hollow = this device, solid = synced). Under a slow
// mouse it widens to show the chapter's sections and marks; the mark can be
// dragged. Everywhere, the place button opens the place bar. Section marks:
// five colours per volume, each with its own glyph and texture, on the
// section dot, the chapter tab and the rail.
//
// Privacy: signed-out readers make zero API calls (the JS-readable hint
// cookie gates every request); place and marks then live in localStorage
// only. Signed in, the place mirrors to /api/position and marks to /api/marks
// (the latter only once the server enables it).
(function () {
  'use strict';
  // Storage can throw on access (cookies blocked, sandboxed frames): resolve it
  // once, inside a try, so the rest of book.js (tooltips) still runs.
  const getStore = name => { try { const st = window[name]; st.getItem('utc'); return st; } catch (e) { return null; } };
  const LS = getStore('localStorage'), SS = getStore('sessionStorage');
  if (!LS) return;

  const STORAGE_KEY = 'under-the-code:progress';
  const PENDING_KEY = 'under-the-code:pending-offset';
  const MARKS_KEY = 'under-the-code:marks';
  const TAB_KEY = 'under-the-code:place-tab';          // sessionStorage: this tab's excursion
  const DETOUR_KEY = 'under-the-code:detour';          // sessionStorage: arrived by an in-book link
  const BEFORE_KEY = 'under-the-code:before-detour';   // localStorage, never synced, 24 h
  const MARKS_OFF_KEY = 'under-the-code:marks-off';    // sessionStorage: the server has marks off
  const MAX_AGE_DAYS = 90;
  const READING_LINE = 56;   // px from viewport top: 48px fixed header + 8

  // Thresholds — tuned on paper; re-tune after the owner's read (?utc-debug).
  const T = {
    BURST_END_MS: 250,        // a burst ends 250ms after its last scroll event (or on scrollend)
    BURST_MAX_MS: 3000,       // …or after 3 s of unbroken scrolling (slow continuous reading)
    BAR_CLOSE_B: 0.5,         // the place bar closes on a scroll longer than this
    IH_IGNORE_MS: 100,        // scrolls this soon after an innerHeight change are the browser's
    SKIP_FRAC: 0.25,          // skipped-text gap, in B
    UNEXPLAINED_B: 1.25,      // a jump this long with no input is find-in-page, a fragment, history
    INPUT_WINDOW_MS: 300,
    CPS: 60,                  // reading budget: characters per second of reading time
    FIG_CPPX: 1.2,            // a figure's drawing counts as reading: characters' worth per pixel of its height (Pass 28)
    CAP_FLOOR: 600,
    OVERSPEND: 0.25,          // below −cap/4 the reader is outrunning their eyes
    BACK_B: 0.5,              // going back up to 0.5B is a re-read; more is seeking
    FWD_B: 1.5,
    STEP_COMMIT_MS: 400,
    SETTLE_QUIET_MS: 1500,
    FS_SETTLE_MS: 400,
    IDLE_STOP_MS: 120000,     // reading time stops 120 s after the last input
    RETURN_B: 0.5, RETURN_MIN_PX: 80,
    PROMOTE_SOFT_MS: 25000, PROMOTE_SOFT_CHARS: 300,
    PROMOTE_HARD_MS: 180000, PROMOTE_HARD_PARAS: 5,
    DWELL_MS: 90000,
    PIN_RELEASE_B: 1,
    UNDO_MS: 600000,
    BEFORE_KEEP_MS: 86400000,
    DETOUR_FRESH_MS: 60000,
    FIRST_VISIT_MS: 8000,
    POST_DEBOUNCE_MS: 2000,
    MARKS_DEBOUNCE_MS: 1000,
    TIP_PAUSE_CAP_MS: 30000,
    READOUT_MIN_MS: 10000,
    BAR_IDLE_MS: 30000,
    HOVER_DWELL_MS: 120, HOVER_SPEED: 0.5, HOVER_CLOSE_MS: 300,
    DRAG_PX: 4,
    TOAST_MS: 6000,
    SYNC_FAILS: 2, SYNC_BACKLOG_MS: 10000,
    MARK_LIMIT: 250,
  };

  const now = () => ((window.performance && performance.now) ? performance.now() : Date.now());
  let signedIn = /(?:^|;\s*)under_signedin=1(?:;|$)/.test(document.cookie);
  const page = ((window.location.pathname.split('/').pop() || '')
    .toLowerCase().replace(/\.html$/, '')) || 'index';
  const isPart = /^part-[1-5]$/.test(page);
  const partNum = p => { const m = /^part-([1-5])$/.exec(p || ''); return m ? +m[1] : 0; };
  const debug = /(?:^|[?&])utc-debug(?:[=&]|$)/.test(window.location.search);
  const motionQ = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  let reduceMotion = !!(motionQ && motionQ.matches);
  if (motionQ && motionQ.addEventListener) motionQ.addEventListener('change', e => { reduceMotion = e.matches; });

  // -------- STORES ------------------------------------------------------------
  function readJSON(store, key) {
    if (!store) return null;
    try { return JSON.parse(store.getItem(key) || 'null'); } catch (e) { return null; }
  }
  function writeJSON(store, key, value) {
    if (!store) return;
    try {
      if (value == null) store.removeItem(key); else store.setItem(key, JSON.stringify(value));
    } catch (e) { /* full or blocked: the book still works */ }
  }

  // v1 records (before Pass 25) carry no `v`; they read as an automatic place.
  function readProgress() {
    const data = readJSON(LS, STORAGE_KEY);
    if (!data || !data.timestamp || !data.part || !(data.section || data.anchor)) return null;
    if ((Date.now() - data.timestamp) / 86400000 > MAX_AGE_DAYS) {
      writeJSON(LS, STORAGE_KEY, null);
      return null;
    }
    if (data.src !== 'set') data.src = 'auto';
    return data;
  }
  function writeProgress(data) { writeJSON(LS, STORAGE_KEY, data); }

  function formatChapterNum(chapterId) {
    if (chapterId === 'chBridge') return 'Bridge';
    const n = String(chapterId || '').replace(/^ch/, '');
    return /^\d+$/.test(n) ? 'Chapter ' + n : chapterId;
  }
  // "03 · The Architecture" (and older stored "03 — …" labels) → "03"
  function labelNum(label) { return String(label || '').split(/\s[\u2014·]\s/)[0].trim(); }
  function sectionNum(rec) {
    return rec && rec.sectionLabel ? labelNum(rec.sectionLabel) : '';
  }

  // -------- ANCHOR MODEL --------------------------------------------------------
  // Candidates are baked ids only: chapters (ch7), sections (ch7-locks),
  // paragraphs (ch7-locks-p4), figures (fig-7-3). Runtime-assigned ids
  // (glossary term anchors, the utc- ids below) and ids inside SVGs are
  // excluded — an anchor must exist identically on every device.
  let anchorEls = null;
  function candidates() {
    if (!anchorEls) {
      anchorEls = Array.prototype.filter.call(
        document.querySelectorAll('[id]'),
        el => /^(ch[0-9B][^ ]*|fig-[0-9]+-[0-9]+[a-z]?)$/.test(el.id) && !el.closest('svg')
      );
    }
    return anchorEls;
  }

  // The deepest candidate whose box contains the reading line; if the line
  // falls in a margin, the nearest candidate above it (fraction may exceed 1).
  // Live rects: used only at a commit.
  function computeAnchor() {
    let containing = null, containingRect = null;
    let above = null, aboveRect = null;
    candidates().forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.height === 0 && r.width === 0) return;      // hidden
      if (r.top > READING_LINE) return;
      if (r.bottom > READING_LINE) { containing = el; containingRect = r; }
      else { above = el; aboveRect = r; }
    });
    // Prefer whichever is later in document order — a paragraph fully above
    // the line pins the position tighter than the section that contains it.
    let el = containing, rect = containingRect, cap = 1;
    if (above && (!containing ||
        (containing.compareDocumentPosition(above) & Node.DOCUMENT_POSITION_FOLLOWING))) {
      el = above; rect = aboveRect; cap = 2;
    }
    if (!el) return null;
    const fraction = (READING_LINE - rect.top) / Math.max(rect.height, 1);
    return {
      el,
      anchor: el.id,
      fraction: Math.round(Math.max(0, Math.min(cap, fraction)) * 1000) / 1000
    };
  }

  // Headings break lines with <br> ("The Machine<br>Beneath<br>Everything");
  // textContent drops those breaks and glues the words together. Read the
  // heading with each <br> as a space, whitespace collapsed.
  function headingText(el) {
    const c = el.cloneNode(true);
    c.querySelectorAll('br').forEach(br => br.replaceWith(' '));
    return c.textContent.replace(/\s+/g, ' ').trim();
  }

  // Anchors that later prose edits merged away. Stored positions (server +
  // localStorage) may still carry them; resolve to the surviving paragraph
  // so no reader loses their place.
  const ANCHOR_ALIASES = {
    'ch1-kernel-p9': 'ch1-kernel-p8',
    // Pass 27 (the cut), Part I
    'ch2-arithmetic-p2': 'ch2-arithmetic-p1',
    'ch2-binary-p7': 'ch2-binary-p6',
    'ch2-boole-p8': 'ch2-boole-p7',
    'ch3-call-p1': 'ch3-call-p2',
    'ch3-overflow-p2': 'ch3-overflow-p1',
    'chBridge-synthesis-p8': 'chBridge-synthesis-p7',
    // Part II
    'ch4-anatomy-p3': 'ch4-anatomy-p4',
    'ch4-security-p7': 'ch4-security-p6'
  };
  const resolveId = id => (document.getElementById(id) ? id : (ANCHOR_ALIASES[id] || id));

  // onDone(), when given, runs once the restore has let go (settled, timed
  // out, or the reader took over).
  function scrollToAnchor(anchor, fraction, smooth, onDone) {
    const el = document.getElementById(anchor) ||
               document.getElementById(ANCHOR_ALIASES[anchor] || '');
    if (!el) { if (onDone) onDone(); return false; }
    function apply(behavior) {
      const r = el.getBoundingClientRect();
      const top = window.scrollY + r.top + (fraction || 0) * r.height - READING_LINE;
      window.scrollTo({ top: Math.max(0, top), behavior });
    }
    apply(smooth ? 'smooth' : 'instant');

    let done = false;
    let ro = null, raf = 0;
    const detach = ['wheel', 'touchstart', 'keydown'];
    function stop() {
      if (done) return;
      done = true;
      if (ro) { ro.disconnect(); ro = null; }
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      detach.forEach(t => window.removeEventListener(t, cancel));
      if (onDone) onDone();
    }
    const cancel = () => stop();               // the reader takes over → let go
    detach.forEach(t => window.addEventListener(t, cancel, { once: true, passive: true }));

    if (smooth) {
      // A smooth scroll animates; don't fight it. Re-apply once, after it ends.
      const settle = () => { if (done) return; apply('instant'); stop(); };
      if ('onscrollend' in window) window.addEventListener('scrollend', settle, { once: true });
      setTimeout(settle, 1800);
      return true;
    }

    // Instant restore: content above the anchor can still shrink or grow after
    // the first apply — a webfont whose off-screen headings reserve a taller
    // line box and collapse to the CSS line-height once scrolled into view, a
    // late image, a reflow. Keep the anchor pinned to its exact offset while
    // that settles. A ResizeObserver fires after layout and before paint, so a
    // shift above the anchor is absorbed in the same frame it happens and never
    // paints out of place; a short rAF loop stops once the position holds.
    function repin() {
      if (done) return;
      const r = el.getBoundingClientRect();
      const drift = r.top - (READING_LINE - (fraction || 0) * r.height);
      if (Math.abs(drift) > 0.5) window.scrollBy({ top: drift, behavior: 'instant' });
    }
    if ('ResizeObserver' in window) {
      ro = new ResizeObserver(repin);
      ro.observe(document.body);
    }
    const t0 = now();
    let stableFrames = 0, lastY = window.scrollY;
    (function tick() {
      if (done) return;
      repin();
      const y = window.scrollY;
      stableFrames = (Math.abs(y - lastY) < 0.5) ? stableFrames + 1 : 0;
      lastY = y;
      if (stableFrames >= 8 || now() - t0 > 2500) { stop(); return; }
      raf = requestAnimationFrame(tick);
    })();
    return true;
  }

  // Layout is only trustworthy once the webfonts have applied.
  function whenSettled(fn) {
    const go = () => requestAnimationFrame(() => requestAnimationFrame(fn));
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(go, go);
    } else { go(); }
  }

  // A 401 means the hint cookie lies: clear it, stop calling, and tell the
  // account mark (it follows the more truthful of the two signals).
  let onSignedOut = null;
  function signedOutDetected() {
    if (!signedIn) return;
    signedIn = false;
    try {
      document.cookie = 'under_signedin=; Max-Age=0; Path=/; Secure; SameSite=Lax';
      document.cookie = 'under_signedin=; Max-Age=0; Path=/';
    } catch (e) { /* ignore */ }
    document.dispatchEvent(new CustomEvent('utc:signedout'));
    if (onSignedOut) onSignedOut();
  }

  // -------- VOLUMES: marker palettes and glyphs --------------------------------
  // One hue family per slot in every volume (1 amber, 2 red, 3 blue, 4 green,
  // 5 violet/neutral), so a reader's own colour code means the same thing in
  // every part; each volume keeps its own tint, names and glyphs. Colours live
  // in CSS (--mk-1…--mk-5 per part stylesheet); glyphs are 10×10 SVG drawn in
  // currentColor. Ratios and the colour-blind check: UNDER.md §4y.
  const SVG_OPEN = '<svg viewBox="0 0 10 10" aria-hidden="true" focusable="false">';
  const VOLUMES = /*VOLUMES*/{
    'part-1': { names: ['Sienna', 'Madder', 'Smalt', 'Verdigris', 'Murex'], glyphs: [
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5 1.4V8.6M1.9 3.2L8.1 6.8M1.9 6.8L8.1 3.2"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5 1.2V8.8M2.3 3.6H7.7"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5 1.2V8.8M2.4 3H7.6M2.4 7H7.6"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M3.4 1.4V8.6M6.6 1.4V8.6"/>',
      '<path fill="currentColor" d="M5.6 1.3V5.9H4.7A2.3 2.3 0 0 1 4.7 1.3Z"/><path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5.6 1.3V8.8M7.9 1.3V8.8M4.7 1.3H8.4"/>' ] },
    'part-2': { names: ['P3 amber', 'Ribbon red', '3270 blue', 'P1 green', 'Carbon'], glyphs: [
      '<path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter" d="M2.6 1.9L7.2 5L2.6 8.1"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter" shape-rendering="crispEdges" d="M3.6 1.6V8.4M6.4 1.6V8.4M1.6 3.6H8.4M1.6 6.4H8.4"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter" shape-rendering="crispEdges" d="M1.9 3.3H8.1M1.9 6.7H8.1"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter" d="M2.4 8.4L7.6 1.6"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="square" stroke-linejoin="miter" d="M5 1.8V8.2M2.2 3.4L7.8 6.6M2.2 6.6L7.8 3.4"/>' ] },
    'part-3': { names: ['Route', 'Port', 'Prussian', 'Starboard', 'Sounding'], glyphs: [
      '<path fill="currentColor" d="M1.4 1.6L8.9 5L1.4 8.4L3.5 5Z"/>',
      '<path fill="currentColor" d="M5 1L9 5L5 9L1 5Z"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M0.9 5C2 2.4 3.6 2.4 4.9 5S7.9 7.6 9.1 5"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5 1.5L8.7 8.1H1.3Z"/>',
      '<circle fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" cx="5" cy="5" r="3.3"/>' ] },
    'part-4': { names: ['Ochre', 'Sealing wax', 'Registry ink', 'Baize', 'Graphite'], glyphs: [
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M1.6 5.3L4 7.8L8.5 2.3"/>',
      '<rect fill="currentColor" x="0.9" y="3.2" width="8.2" height="3.6" rx="0.3"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-linecap="butt" d="M1.2 2.9H8.8M1.2 7.1H8.8"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M5 0.9L7.7 5L5 9.1L2.3 5Z"/>',
      '<path fill="currentColor" d="M1.2 1.2H8.8L1.2 8.8Z"/>' ] },
    'part-5': { names: ['Candidate', 'Heartbeat', 'Replica', 'Follower', 'Commit'], glyphs: [
      '<circle fill="none" stroke="currentColor" stroke-width="1.2" cx="5" cy="5" r="3.5"/><path fill="currentColor" d="M5 1.5A3.5 3.5 0 0 0 5 8.5Z"/>',
      '<path fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" d="M0.9 6.6L3 3.4L5 6.6L7 3.4L9.1 6.6"/>',
      '<circle fill="none" stroke="currentColor" stroke-width="1.1" cx="5" cy="5" r="3.9"/><circle fill="none" stroke="currentColor" stroke-width="1.1" cx="5" cy="5" r="1.5"/>',
      '<circle fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" cx="5" cy="5" r="3.3"/>',
      '<rect fill="currentColor" x="2" y="2" width="6" height="6" rx="0.5"/>' ] },
  }/*/VOLUMES*/;
  const VOL = VOLUMES[isPart ? page : 'part-1'];
  const glyphSvg = (part, c) => SVG_OPEN + (VOLUMES[part] || VOLUMES['part-1']).glyphs[c - 1] + '</svg>';
  const slotName = (part, c) => (VOLUMES[part] || VOLUMES['part-1']).names[c - 1];

  // -------- MARKS (shared by part pages; the account page has its own reader) --
  // {v:1, owner, cursor, m:{"part|sectionId":{c, t, s, x, o, st}}}
  //   c 1..5 slot · t last change (ms; server time once synced) · s 1 = the
  //   server holds this state · x 1 = removed (a tombstone waiting to sync)
  //   · o the account it belongs to (null = made signed out) · st the server
  //   time of the last synced state (present = the server has seen it).
  function readMarks() {
    const d = readJSON(LS, MARKS_KEY);
    if (d && d.v === 1 && d.m && typeof d.m === 'object') return d;
    return { v: 1, owner: null, cursor: 0, m: {} };
  }
  function writeMarks(d) { writeJSON(LS, MARKS_KEY, d); }

  // ==========================================================================
  // PART PAGES
  // ==========================================================================
  if (isPart) initPart();
  else initOther();

  function initPart() {
    const nav = document.querySelector('.book-nav');
    document.documentElement.dataset.vol = page;   // the volume's marker palette (book.css)

    // ---- the deadline queue: every timer in this module goes through one ----
    const timers = new Map();
    let tHandle = 0, tAt = Infinity;
    function at(name, ms, fn) { timers.set(name, { due: now() + ms, fn }); arm(); }
    function cancelT(name) { if (timers.delete(name)) arm(); }
    function pendingT(name) { return timers.has(name); }
    function arm() {
      let min = Infinity;
      timers.forEach(t => { if (t.due < min) min = t.due; });
      if (min === tAt) return;
      clearTimeout(tHandle);
      tAt = min;
      if (min < Infinity) tHandle = setTimeout(fire, Math.max(0, min - now()));
    }
    function fire() {
      tAt = Infinity;
      const n = now() + 1;
      const due = [];
      timers.forEach((t, k) => { if (t.due <= n) due.push([k, t]); });
      due.sort((a, b) => a[1].due - b[1].due);
      due.forEach(([k, t]) => { if (timers.get(k) === t) { timers.delete(k); t.fn(); } });
      arm();
    }

    // ---- GEOMETRY: the offset table -------------------------------------------
    // Document tops as computeAnchor sees them, with the reveal and
    // scroll-driven entrance transforms factored out (see buildTable).
    let G = null;
    let navB = 48 + 59, B = 600, Lpx = 200;
    const secMeta = new Map();   // section id → {label, title, num} (text never changes)

    function docTop(el) {
      let y = 0, n = el;
      while (n) { y += n.offsetTop; n = n.offsetParent; if (n) y += n.clientTop; }
      return y;
    }
    function measureConsts() {
      const cn = document.querySelector('.chapter-nav');
      navB = 48 + (cn ? cn.offsetHeight : 0);                 // constant (review M7)
      B = Math.max(200, window.innerHeight - navB);
      Lpx = navB + 0.3 * B;
    }
    function buildTable() {
      measureConsts();
      const anchors = [], byId = Object.create(null);
      const sy = window.scrollY;
      candidates().forEach((el, i) => {
        const r = el.getBoundingClientRect();
        const hidden = r.width === 0 && r.height === 0;
        // Rect geometry (sub-pixel, as computeAnchor sees it), unless an
        // entrance transform has moved the box: then the transform-free
        // offset chain, which is where it comes to rest.
        let top = 0, h = 0;
        if (!hidden) {
          const off = docTop(el);
          top = Math.abs(r.top + sy - off) > 2 ? off : r.top + sy;
          h = Math.abs(r.top + sy - off) > 2 ? el.offsetHeight : r.height;
        }
        const isPara = el.tagName === 'P' && /-p\d+$/.test(el.id);
        const a = { el, id: el.id, i, hidden, top, h, bottom: top + h, isPara,
          chars: isPara ? el.textContent.replace(/\s+/g, ' ').length : 0, sec: -1, ch: -1 };
        anchors.push(a);
        byId[el.id] = a;
      });
      const chapters = [];
      anchors.forEach(a => {
        if (/^ch(\d+|Bridge)$/.test(a.id) && !a.hidden) {
          chapters.push({ id: a.id, idx: chapters.length, top: a.top, bottom: a.bottom, secs: [] });
        }
      });
      const sections = [];
      document.querySelectorAll('section.section[id^="ch"]').forEach(el => {
        const a = byId[el.id];
        if (!a || a.hidden) return;
        const chId = el.id.split('-')[0];
        const ch = chapters.find(c => c.id === chId) || null;
        if (!secMeta.has(el.id)) {
          const sn = el.querySelector('.section-number');
          const h2 = el.querySelector('h2');
          const label = sn ? sn.textContent.replace(/\s+/g, ' ').trim() : '';
          secMeta.set(el.id, { label, title: h2 ? headingText(h2) : '', num: labelNum(label) });
        }
        const s = { id: el.id, el, idx: sections.length, top: a.top, bottom: a.bottom, ch: chId,
          chIdx: ch ? ch.idx : -1, paras: [], meta: secMeta.get(el.id) };
        sections.push(s);
        if (ch) ch.secs.push(s.idx);
      });
      const secById = Object.create(null);
      sections.forEach(s => { secById[s.id] = s; });
      anchors.forEach(a => {
        const sEl = a.el.closest('section.section');
        const s = sEl ? secById[sEl.id] : null;
        if (s) { a.sec = s.idx; if (a.isPara && !a.hidden) s.paras.push(a.i); }
        const chId = (s ? s.id : a.id).split('-')[0];
        const ch = chapters.find(c => c.id === chId);
        a.ch = ch ? ch.idx : -1;
      });
      // Sorted by top (ties keep document order) for the binary searches.
      const order = anchors.filter(a => !a.hidden).sort((p, q) => (p.top - q.top) || (p.i - q.i));
      const paras = order.filter(a => a.isPara);
      // Figures are read too (Pass 28: the picture carries it). Their drawings join
      // the character count by height; captions are paragraphs already.
      const figs = order.filter(a => /^fig-/.test(a.id)).map(a => {
        const svg = a.el.querySelector(':scope > svg');
        if (!svg) return null;
        const r = svg.getBoundingClientRect(), top = a.top + (r.top - a.el.getBoundingClientRect().top);
        return { top, bottom: top + r.height, h: r.height, chars: r.height * T.FIG_CPPX };
      }).filter(Boolean);
      G = { anchors, byId, chapters, sections, secById, order, paras, figs,
        docH: document.documentElement.scrollHeight };
      onTableBuilt();
    }

    // Deepest anchor whose top is at or above y (document px).
    function kAt(y) {
      if (!G || !G.order.length) return null;
      let lo = 0, hi = G.order.length - 1, ans = -1;
      while (lo <= hi) {
        const mid = (lo + hi) >> 1;
        if (G.order[mid].top <= y + 0.5) { ans = mid; lo = mid + 1; } else hi = mid - 1;
      }
      return ans < 0 ? null : G.order[ans];
    }
    // The pure twin of computeAnchor(): the same containing/above/cap rules
    // at document line y, from the table. Parity is a verified invariant.
    function anchorAt(y) {
      if (!G) return null;
      let containing = null, above = null;
      for (const a of G.anchors) {
        if (a.hidden || a.top > y) continue;
        if (a.bottom > y) containing = a; else above = a;
      }
      let a = containing, cap = 1;
      if (above && (!containing || above.i > containing.i)) { a = above; cap = 2; }
      if (!a) return null;
      const f = (y - a.top) / Math.max(a.h, 1);
      return { a, anchor: a.id, fraction: Math.round(Math.max(0, Math.min(cap, f)) * 1000) / 1000 };
    }
    function chapterAt(y) {
      if (!G) return null;
      for (const c of G.chapters) if (c.top <= y && y < c.bottom) return c;
      return null;
    }
    // Characters of paragraph text between document lines y0 < y1.
    function charsBetween(y0, y1) {
      if (!G || y1 <= y0) return 0;
      let sum = 0;
      for (const list of [G.paras, G.figs]) for (const p of list) {
        if (p.bottom <= y0) continue;
        if (p.top >= y1) break;
        const ov = Math.min(p.bottom, y1) - Math.max(p.top, y0);
        if (ov > 0) sum += p.chars * ov / Math.max(p.h, 1);
      }
      return sum;
    }
    function bandCap(scrollY) {
      return Math.max(T.CAP_FLOOR, charsBetween(scrollY + navB, scrollY + window.innerHeight));
    }
    // A paragraph that sat entirely between the old viewport's bottom and the
    // new reading area's top was never on screen: text was skipped.
    function skipped(y0, y1) {
      const oldBottom = y0 + window.innerHeight, newTop = y1 + navB;
      if (newTop - oldBottom <= T.SKIP_FRAC * B) return false;
      for (const p of G.paras) {
        if (p.top < oldBottom) continue;
        if (p.top >= newTop) break;
        if (p.bottom <= newTop) return true;
      }
      return false;
    }
    function parasCrossed(yA, yB) {   // paragraphs whose end the attention line passed
      const out = [];
      if (!G) return out;
      for (const p of G.paras) {
        if (p.bottom <= yA) continue;
        if (p.bottom > yB) break;
        out.push(p.id);
      }
      return out;
    }
    function paraOrdinal(k) {   // {n, of} of the paragraph at or before anchor k in its section
      if (!G || !k || k.sec < 0) return null;
      const s = G.sections[k.sec];
      let n = 0;
      s.paras.forEach(i => { if (G.anchors[i].top <= k.top) n++; });
      return { n, of: s.paras.length };
    }
    // The document y of a saved place's attention line on this viewport.
    function placeY(rec) {
      if (!G || !rec || rec.part !== page) return null;
      const a = G.byId[resolveId(rec.anchor)];
      if (!a || a.hidden) return null;
      return a.top + (rec.fraction || 0) * a.h - READING_LINE + Lpx;
    }
    const nearBand = () => Math.max(T.RETURN_B * B, T.RETURN_MIN_PX);
    function nearPlace(rec, yL) {
      const py = placeY(rec);
      return py != null && Math.abs(yL - py) <= nearBand();
    }

    // ---- records ---------------------------------------------------------------
    function makeRecord(anc, k, src) {
      const s = k && k.sec >= 0 ? G.sections[k.sec] : null;
      const chapterId = s ? s.ch : (k ? k.id.split('-')[0] : anc.anchor.split('-')[0]);
      const chEl = document.getElementById(chapterId);
      let chapterTitle = '';
      if (chEl) {
        const h1 = chEl.querySelector('.chapter-hero h1, h1');
        if (h1) chapterTitle = headingText(h1);
      }
      return {
        v: 2,
        part: page,
        anchor: anc.anchor,
        fraction: anc.fraction,
        section: s ? s.id : chapterId,
        chapterId,
        chapterNum: formatChapterNum(chapterId),
        chapterTitle,
        sectionLabel: s ? s.meta.label : '',
        sectionTitle: s ? s.meta.title : '',
        k: k ? k.id : anc.anchor,
        pn: (k && paraOrdinal(k) || { n: 0 }).n,   // ¶ ordinal, so the readout is exact before the table exists
        src: src || 'auto',
        end: s && s.idx === G.sections.length - 1 ? 1 : 0,
        timestamp: Date.now()
      };
    }
    const bucket = r => r ? r.part + '#' + r.anchor + '@' + Math.round(r.fraction * 100) + ':' + r.src : '';
    const bucket5 = r => r ? r.part + '#' + r.anchor + '@' + Math.round(r.fraction * 20) + ':' + r.src : '';

    // ---- STATE ---------------------------------------------------------------
    let state = 'SETTLING';
    let C = readProgress();            // the committed place — the only thing saved, synced or drawn
    let R = null, exc = null;          // excursion: where to return to, and its counters
    let pinAway = null;                // PINNED: reading elsewhere (release counters)
    let gate = null;                   // first visit / reading on: commits wait for 8 s past the opener
    let before = readJSON(LS, BEFORE_KEY);   // {rec, at}: back to before the detour
    if (before && (!before.rec || Date.now() - before.at > T.BEFORE_KEEP_MS)) { before = null; writeJSON(LS, BEFORE_KEY, null); }
    let undoPrev = null;               // the place before a hand-set place (Undo, until the next commit)
    let budget = 0, cap = T.CAP_FLOOR;
    let writes = 0, posts = 0;
    let restY = window.scrollY;
    let lastInputAt = now(), lastAccrue = now(), pauses = new Map();   // opening the page counts as input
    let navFlag = null, ihChangeAt = -Infinity, selfUntil = 0;
    let lastW = window.innerWidth, lastH = window.innerHeight, lastDPR = window.devicePixelRatio || 1;
    let viewAnchor = null;             // the line-56 anchor of the last rest position (re-pins on reflow)
    let burst = null;
    let prevState = null, undoDetourUntil = 0, lost401 = false, acctOwner = null;
    let touched = false, recheckView = null;   // the reader's own input since load; a view to re-check after a reload
    const hover = { open: false, lastX: 0, lastY: 0, lastT: 0, armed: true };
    let drag = null, cancelDrag = null, cueW = window.innerWidth;

    const navEntry0 = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || null;
    const detour = (function () {
      const d = readJSON(SS, DETOUR_KEY);
      writeJSON(SS, DETOUR_KEY, null);
      if (d && Date.now() - d.at < T.DETOUR_FRESH_MS) return d;
      // Middle-click, "open in new tab", cmd-click: no click reached this tab,
      // but the referrer still says a part page or the glossary sent the reader.
      if (navEntry0 && navEntry0.type !== 'navigate') return null;
      if (readJSON(SS, PENDING_KEY)) return null;
      try {
        const ref = new URL(document.referrer);
        const from = (ref.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '');
        if (ref.origin === window.location.origin && from !== page && /^(part-[1-5]|glossary)$/.test(from)) return { from, at: Date.now() };
      } catch (e) { /* no referrer */ }
      return null;
    })();
    const tabPrev = readJSON(SS, TAB_KEY);
    function saveTab() {
      writeJSON(SS, TAB_KEY, { R: exc ? R : null, kind: exc ? exc.kind : null,
        view: viewAnchor ? { anchor: viewAnchor.anchor, fraction: viewAnchor.fraction } : null, at: Date.now() });
    }

    // ---- reading time ----------------------------------------------------------
    // Time counts while the page is visible, no overlay pauses it, and the
    // last input was under 120 s ago. Overlays pause the clock only; scroll
    // steps are never discarded (review H5). A tooltip pauses at most 30 s.
    function paused() { return pauses.size > 0 || document.visibilityState !== 'visible'; }
    function accrue() {
      const t = now();
      const from = lastAccrue;
      lastAccrue = t;
      if (paused()) return;
      const end = Math.min(t, lastInputAt + T.IDLE_STOP_MS);
      const ms = end - from;
      if (!(ms > 0)) return;
      budget = Math.min(cap, budget + ms / 1000 * T.CPS);
      if (exc) { exc.readMs += ms; exc.spotMs += ms; }
      if (pinAway) pinAway.readMs += ms;
      if (gate) { const k = kAt(window.scrollY + Lpx); if (k && k.ch >= 0) gate.ms += ms; }
    }
    function setPause(name, on) {
      accrue();
      if (on) pauses.set(name, now()); else pauses.delete(name);
      lastAccrue = now();
      if (name === 'tip') {
        if (on) at('tipcap', T.TIP_PAUSE_CAP_MS, () => setPause('tip', false));
        else cancelT('tipcap');
      }
    }
    function input() { lastInputAt = now(); }

    // ---- STATE TRANSITIONS -------------------------------------------------------
    function enterSettling(quietMs) {
      if (state !== 'SETTLING') prevState = state;
      state = 'SETTLING';
      cancelT('commit');
      at('settle', quietMs == null ? T.SETTLE_QUIET_MS : quietMs, endSettling);
      debugPaint();
    }
    function endSettling() {
      cancelT('settle');
      if (state !== 'SETTLING') return;
      restY = window.scrollY;
      if (!G) return;
      if (recheckView && !touched) {
        // WebKit re-applies a stale #fragment after load, after our restore:
        // if the reader hasn't moved, put this tab's view back, once.
        const want = recheckView, v = anchorAt(restY + READING_LINE);
        recheckView = null;
        if (!v || v.anchor !== want.anchor || Math.abs(v.fraction - want.fraction) > 0.05) {
          selfScrollToAnchor(want.anchor, want.fraction, false);
          return;
        }
      }
      recheckView = null;
      freshTable(kAt(restY + READING_LINE));      // a reflow (rotation, fonts) may have outrun the rebuild
      viewAnchor = anchorAt(restY + READING_LINE);
      decideState();
    }
    // Where does the reader stand relative to their place, now the page is still?
    function decideState() {
      const yL = window.scrollY + Lpx;
      cap = bandCap(window.scrollY);
      if (budget <= 0) budget = cap / 2;
      if (!C) { state = 'READING'; exc = null; R = null; gate = gate || { ms: 0 }; armChecks(); return paintAll(); }
      if (C.src === 'set') { state = 'PINNED'; exc = null; R = null; pinAway = nearPlace(C, yL) ? null : freshAway(); saveTab(); armChecks(); return paintAll(); }
      if (C.part === page && nearPlace(C, yL)) { state = 'READING'; exc = null; R = null; saveTab(); return paintAll(); }
      // Reading on: the place is at the end of the previous part and this
      // part opened at its opener — that is reading, not a detour.
      if (C.part !== page && C.end && partNum(C.part) + 1 === partNum(page) && !chapterAt(yL)) {
        state = 'READING'; gate = { ms: 0 }; armChecks(); return paintAll();
      }
      if (prevState === 'EXCURSION' && exc && R) { state = 'EXCURSION'; return paintAll(); }
      const carried = tabPrev && tabPrev.R && C && tabPrev.R.part === C.part && tabPrev.R.anchor === C.anchor ? tabPrev.kind : null;
      startExcursion(detour ? 'hard' : (carried || 'soft'), detour ? 'link' : 'arrival');
    }
    function freshAway() { return { readMs: 0, paras: new Set() }; }
    function freshExc(kind, reason) {
      const k = kAt(window.scrollY + Lpx);
      return { kind, reason, readMs: 0, spotMs: 0, chars: 0, paras: new Set(),
        startSec: k ? k.sec : -1, pastEnd: false };
    }
    function startExcursion(kind, reason) {
      cancelT('commit');
      cap = bandCap(window.scrollY);
      budget = cap / 2;
      if (state === 'PINNED') { pinAway = freshAway(); armChecks(); return paintAll(); }
      if (!C) { state = 'READING'; gate = { ms: 0 }; armChecks(); return paintAll(); }   // nothing to return to
      if (state === 'EXCURSION' && exc) {
        // Still seeking: the clock restarts, the return point stays.
        const harder = exc.kind === 'hard' || kind === 'hard';
        exc = freshExc(harder ? 'hard' : 'soft', reason);
      } else {
        state = 'EXCURSION';
        R = C;
        exc = freshExc(kind, reason);
      }
      saveTab();
      armChecks();
      paintAll();
    }
    function endExcursion() {   // back at the place: nothing is written
      state = C && C.src === 'set' ? 'PINNED' : 'READING';
      exc = null; R = null; pinAway = null;
      saveTab();
      cancelT('check');
      paintAll();
    }
    function promote() {
      if (R) {
        before = { rec: R, at: Date.now() };
        writeJSON(LS, BEFORE_KEY, before);
        undoDetourUntil = now() + T.UNDO_MS;
      }
      state = 'READING'; exc = null; R = null; pinAway = null;
      saveTab();
      cancelT('check');
      commitNow('auto');
    }
    function restoreBefore() {   // one reading step back at the old place restores it (1 write)
      const rec = before.rec;
      before = null; undoDetourUntil = 0;
      writeJSON(LS, BEFORE_KEY, null);
      state = rec.src === 'set' ? 'PINNED' : 'READING';
      exc = null; R = null; saveTab(); cancelT('check');
      commit(Object.assign({}, rec, { timestamp: Date.now(), sa: undefined }));
    }

    // Promotion and gate checks run on a slow tick only while something waits.
    function armChecks() {
      if (state === 'EXCURSION' || (state === 'PINNED' && pinAway) || gate) at('check', 2500, check);
      else cancelT('check');
    }
    function check() {
      if (burst) return armChecks();     // decide between bursts, never mid-scroll
      accrue();
      if (state === 'EXCURSION' && exc) {
        if (exc.kind === 'soft') {
          if ((exc.readMs >= T.PROMOTE_SOFT_MS && exc.chars >= T.PROMOTE_SOFT_CHARS) ||
              (exc.spotMs >= T.DWELL_MS && now() - lastInputAt <= T.IDLE_STOP_MS)) return promote();
        } else if ((exc.readMs >= T.PROMOTE_HARD_MS && exc.paras.size >= T.PROMOTE_HARD_PARAS) || exc.pastEnd) {
          return promote();
        }
      }
      if (state === 'PINNED' && pinAway && pinAway.readMs >= T.PROMOTE_HARD_MS && pinAway.paras.size >= T.PROMOTE_HARD_PARAS) {
        pinAway = null;
        if (C) C = Object.assign({}, C, { src: 'auto' });
        state = 'READING';
        return commitNow('auto');
      }
      if (gate && gate.ms >= T.FIRST_VISIT_MS && state === 'READING') {
        const k = kAt(window.scrollY + Lpx);
        if (k && k.ch >= 0) { gate = null; commitNow('auto'); }
      }
      armChecks();
      debugPaint();
    }

    // ---- BURSTS ------------------------------------------------------------------
    function onScroll() {
      const t = now();
      if (burst && t - burst.t0 > T.BURST_MAX_MS) endBurst();   // a slow, unbroken scroll is read in steps
      if (!burst) {
        burst = { y0: restY, t0: t, self: t < selfUntil, nav: navFlag && t - navFlag.at < 1500 ? navFlag : null,
          input: t - lastInputAt < T.INPUT_WINDOW_MS };
        closeMenu();
      }
      if (t - lastInputAt < T.INPUT_WINDOW_MS) burst.input = true;
      if (t < selfUntil) burst.self = true;
      burst.last = t;
      if (!pendingT('burst')) at('burst', T.BURST_END_MS, burstTimer);
      queueCue();
      if (hover.open && !drag) closeWide(true);
    }
    function burstTimer() {   // the scroll listener never re-arms a timer; this re-checks
      if (!burst) return;
      const left = burst.last + T.BURST_END_MS - now();
      if (left > 1) at('burst', left, burstTimer); else endBurst();
    }
    function endBurst() {
      cancelT('burst');
      const b = burst;
      burst = null;
      if (!b) return;
      const y0 = b.y0, y1 = window.scrollY;
      restY = y1;
      if (!G) return;
      viewAnchor = anchorAt(y1 + READING_LINE);
      if (state === 'SETTLING' || b.self || now() < selfUntil) {
        if (state === 'SETTLING' && pendingT('settle') && !b.self) at('settle', T.SETTLE_QUIET_MS, endSettling);
        return;
      }
      if (b.t0 >= ihChangeAt && b.t0 - ihChangeAt < T.IH_IGNORE_MS) return;   // the URL bar, not the reader
      const d = y1 - y0;
      if (Math.abs(d) < 2) return;
      accrue();
      if (Math.abs(d) > T.BAR_CLOSE_B * B) closePlaceBar(false);
      navFlag = b.nav ? null : navFlag;
      const c = classify(b, y0, y1, d);
      step(c, y0, y1, d);
      if (!c.seeking && d > 0) lastInputAt = now();   // read-all / browse mode moves the page with no input (H6)
      debugPaint();
    }
    function classify(b, y0, y1, d) {
      const res = { seeking: false, kind: 'soft', reason: '', crossed: 0 };
      const hard = r => { res.seeking = true; res.kind = 'hard'; res.reason = r; return res; };
      const soft = r => { res.seeking = true; res.reason = r; return res; };
      if (b.nav) return hard('nav');
      if (d < -T.BACK_B * B) return hard('back');
      if (d > T.FWD_B * B) return soft('long');
      if (Math.abs(d) > T.UNEXPLAINED_B * B && !b.input) return soft('unexplained');
      if (d > 0 && skipped(y0, y1)) return soft('skipped');
      if (d > 0) {
        // Text the reader must have read to move on: what was on screen and
        // has now left the top of the reading area. (Charging text that crossed
        // the attention line counted lines a page-sized step had not yet shown
        // — measured, Pass 25.)
        res.crossed = charsBetween(y0 + navB, Math.min(y1 + navB, y0 + window.innerHeight));
        budget -= res.crossed;
        if (budget < -cap * T.OVERSPEND) return soft('budget');
      }
      return res;
    }
    function step(c, y0, y1, d) {
      const yL = y1 + Lpx;
      if (state === 'READING') {
        if (c.seeking) return startExcursion(c.kind, c.reason);
        if (d < 0) return;                     // a re-read changes nothing
        if (gate) return armChecks();          // first visit: the clock decides
        if (undoDetourUntil > now() && before && nearPlace(before.rec, yL)) return restoreBefore();
        at('commit', T.STEP_COMMIT_MS, () => commitNow('auto'));
        return;
      }
      if (state === 'EXCURSION' && exc) {
        if (R && nearPlace(R, yL)) return endExcursion();
        if (undoDetourUntil > now() && before && nearPlace(before.rec, yL)) return restoreBefore();
        if (c.seeking) return startExcursion(c.kind, c.reason);
        exc.spotMs = 0;
        if (d > 0) {
          exc.chars += c.crossed;
          parasCrossed(y0 + Lpx, yL).forEach(id => exc.paras.add(id));
          const k = kAt(yL);
          if (k && exc.startSec >= 0 && k.sec > exc.startSec) exc.pastEnd = true;
        }
        saveTab();
        return check();
      }
      if (state === 'PINNED') {
        const py = placeY(C);
        if (!c.seeking && d > 0 && py != null && Math.abs((y0 + Lpx) - py) <= T.PIN_RELEASE_B * B) {
          // Reading on from the pin: the book tracks again.
          pinAway = null;
          C = Object.assign({}, C, { src: 'auto' });
          state = 'READING';
          at('commit', T.STEP_COMMIT_MS, () => commitNow('auto'));
          return;
        }
        if (py != null && Math.abs(yL - py) <= nearBand()) { pinAway = null; return paintAll(); }
        if (c.seeking) { pinAway = freshAway(); return armChecks(); }
        if (!pinAway) pinAway = freshAway();
        if (d > 0) parasCrossed(y0 + Lpx, yL).forEach(id => pinAway.paras.add(id));
        return check();
      }
    }

    // ---- COMMIT -----------------------------------------------------------------
    function atPageEnd() {
      return window.scrollY >= document.documentElement.scrollHeight - window.innerHeight - 4;
    }
    // Late layout (an off-screen heading's line box collapsing, an image) moves
    // anchors before the body ResizeObserver's debounced rebuild: check one.
    function freshTable(k) {
      if (!G || !k || k.hidden) return;
      const r = k.el.getBoundingClientRect();
      if (Math.abs(r.top + window.scrollY - k.top) > 1.5 && Math.abs(docTop(k.el) - k.top) > 1.5) buildTable();
    }
    function commitNow(src) {
      cancelT('commit');
      if (!G || state === 'SETTLING' || pauses.has('fs')) return;
      if (burst) { at('commit', T.STEP_COMMIT_MS, () => commitNow(src)); return; }   // never mid-scroll
      freshTable(kAt(window.scrollY + Lpx));
      const anc = computeAnchor();           // the only live rect reads: at a commit
      if (!anc) return;
      let k = kAt(window.scrollY + Lpx);
      if (atPageEnd()) {                     // the last paragraph whose top is visible
        const vis = G.paras.filter(p => p.top < window.scrollY + window.innerHeight);
        if (vis.length) k = vis[vis.length - 1];
      }
      commit(makeRecord(anc, k, src || 'auto'));
      cap = bandCap(window.scrollY);
    }
    function commit(rec, opts) {
      const prev = C;
      rec.sb = prev ? (prev.sa || prev.sb || 0) : 0;   // the server time this place builds on
      if (signedIn) rec.acct = 1;                       // made signed in: sign-out forgets it (H12)
      if (signedIn && acctOwner) rec.own = acctOwner;
      if (prev && bucket(prev) === bucket(rec)) { C = Object.assign(rec, { sa: prev.sa, acct: rec.acct || prev.acct, own: rec.own || prev.own }); return; }
      C = rec;
      writeProgress(rec);
      writes++;
      if (!(opts && opts.keepUndo)) undoPrev = null;
      markDirty();
      schedulePost(opts && opts.now ? 0 : T.POST_DEBOUNCE_MS);
      paintAll();
    }

    // ---- POSITION SYNC: one POST at a time, latest wins (review H4) ---------------
    const cid = Math.random().toString(36).slice(2, 10).padEnd(8, '0');
    let seq = 0, inflight = false, queued = false, lastSentKey = '';
    let dirty = false, dirtySince = 0, confirmed = false, fails = 0;
    function markDirty() {
      if (!dirty) dirtySince = now();
      dirty = true;
      at('synceval', T.SYNC_BACKLOG_MS + 50, paintSync);
    }
    function schedulePost(ms) {
      if (!signedIn || !('fetch' in window)) return paintSync();
      at('post', ms, sendPost);
    }
    function postBody(rec, s) {
      return JSON.stringify({
        part: rec.part, anchor: rec.anchor, fraction: rec.fraction,
        section: rec.section, chapterId: rec.chapterId, chapterNum: rec.chapterNum,
        chapterTitle: rec.chapterTitle, sectionLabel: rec.sectionLabel,
        sectionTitle: rec.sectionTitle, k: rec.k, end: rec.end ? 1 : 0, src: rec.src, cid, seq: s
      });
    }
    function sendPost(keepalive) {
      cancelT('post');
      if (!signedIn || !C || !dirty) return;
      if (inflight) { queued = true; return; }
      const rec = C;
      if (bucket5(rec) === lastSentKey && rec.sa) { dirty = false; return paintSync(); }
      const mySeq = ++seq;
      inflight = true;
      posts++;
      fetch('/api/position', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: postBody(rec, mySeq), keepalive: !!keepalive, credentials: 'same-origin'
      }).then(r => {
        if (r.status === 401) { signedOutDetected(); return null; }
        if (r.status === 409) return { stale: true };   // a newer save from this tab already landed
        if (!r.ok) throw new Error('http ' + r.status);
        return r.json().catch(() => ({}));
      }).then(data => {
        if (!data) return;
        fails = 0;
        lastSentKey = bucket5(rec);
        const same = C === rec || (C && bucket(C) === bucket(rec));
        if (data.updated_at && same) { C.sa = data.updated_at; writeProgress(C); }
        if (mySeq === seq && same) { dirty = false; confirmed = true; }
      }).catch(() => { fails++; }).then(() => {
        inflight = false;
        paintSync();
        if (queued || (dirty && C !== rec)) { queued = false; schedulePost(0); }
      });
    }
    function flush(viaBeacon) {
      if (burst) endBurst();
      if (pendingT('commit')) commitNow('auto');
      saveTab();
      if (pendingT('marks')) pushMarks(true);
      if (!signedIn || !dirty || !C) return;
      if (viaBeacon && navigator.sendBeacon) {
        const body = postBody(C, ++seq);
        if (navigator.sendBeacon('/api/position', new Blob([body], { type: 'application/json' }))) {
          posts++;
          lastSentKey = bucket5(C);
        }
      } else {
        sendPost(true);
      }
    }
    function syncState() {
      if (!signedIn) return 'signedout';
      if (fails >= T.SYNC_FAILS) return 'paused';
      if (confirmed && (!dirty || now() - dirtySince < T.SYNC_BACKLOG_MS)) return 'synced';
      return 'local';
    }

    // ---- another tab, another device -------------------------------------------
    // Tabs share localStorage: a newer place written elsewhere is adopted, so a
    // stale tab never sends its old place over the reader's real one (H3).
    function adoptLocal() {
      const d = readProgress();
      if (!d || (C && d.timestamp <= C.timestamp)) return;
      C = d;
      dirty = false;
      cancelT('commit'); cancelT('post');
      if (state !== 'SETTLING') reconsider();
      paintAll();
    }
    function reconsider(kindHint) {
      const yL = window.scrollY + Lpx;
      if (!C) { state = 'READING'; exc = null; R = null; pinAway = null; gate = gate || { ms: 0 }; }
      else if (C.src === 'set') { state = 'PINNED'; exc = null; R = null; pinAway = nearPlace(C, yL) ? null : freshAway(); }
      else if (C.part === page && nearPlace(C, yL)) { state = 'READING'; exc = null; R = null; }
      else {
        const hard = kindHint === 'hard' || (exc && exc.kind === 'hard') || (detour && C.part !== page);
        exc = null; state = 'READING';
        startExcursion(hard ? 'hard' : 'soft', hard ? 'link' : 'elsewhere');
      }
      saveTab();
      armChecks();
    }
    window.addEventListener('storage', e => {
      if (e.key === STORAGE_KEY) adoptLocal();
      else if (e.key === MARKS_KEY) { marks = readMarks(); paintMarks(); }
      else if (e.key === BEFORE_KEY) { before = readJSON(LS, BEFORE_KEY); paintBar(); }
    });

    function fetchRemote() {
      if (!signedIn || !('fetch' in window)) return;
      fetch('/api/position', { credentials: 'same-origin' }).then(r => {
        if (r.status === 401) { signedOutDetected(); return null; }
        if (!r.ok) { fails++; paintSync(); return null; }
        return r.json();
      }).then(data => {
        if (!data) return;
        fails = 0;
        if (data.owner) acctOwner = data.owner;
        if (C && C.own && data.owner && C.own !== data.owner) {   // left by another account on this device
          C = null; writeProgress(null); dirty = false; cancelT('commit'); cancelT('post');
          if (state !== 'SETTLING') reconsider();
          paintAll();
        }
        const remote = data.position && data.position.anchor ? data.position : null;
        const remoteTs = data.updated_at || 0;
        if (!remote) { if (C) { markDirty(); schedulePost(0); } return paintSync(); }
        const local = C;
        let adopt;
        if (!local) adopt = true;
        else if (local.v !== 2) adopt = remoteTs > (local.timestamp || 0) + 1500;   // a v1 record: the old rule
        else if (!local.sa) adopt = false;     // never over a place this device has not synced (M4)
        else adopt = remoteTs > local.sa;
        if (adopt && local && local.src === 'set' && remote.src !== 'set') {
          // Nothing but the reader moves a pin (spec §5): offer the other device's place.
          adopt = false;
          offerRemote(Object.assign({}, remote, { v: 2, src: 'auto', sa: remoteTs, sb: remoteTs, own: data.owner }), true);
        }
        if (adopt) {
          C = Object.assign({}, remote, { v: 2, src: remote.src === 'set' ? 'set' : 'auto', sa: remoteTs, sb: remoteTs, acct: 1, own: data.owner, timestamp: Date.now() });
          writeProgress(C);
          dirty = false; confirmed = true; cancelT('commit'); cancelT('post');
          if (state !== 'SETTLING') reconsider();
          paintAll();
          offerRemote(C);
        } else {
          const neutral = r => bucket5(Object.assign({}, r, { src: 'auto' }));
          const own = local.v === 2 && !local.sa && neutral(remote) === neutral(local);
          if (local.sa && remoteTs === local.sa) { dirty = false; confirmed = true; }
          else if (own) { local.sa = remoteTs; writeProgress(local); dirty = false; confirmed = true; }   // this device's beacon landed
          else if (local.sa ? remoteTs < local.sa : remoteTs <= (local.sb || 0)) { markDirty(); schedulePost(0); }
          // else: another device wrote after this place's base — offer, never overwrite; the next commit here pushes.
          if (local.v === 2 && !local.sa && !own && remoteTs > (local.sb || 0)) {
            offerRemote(Object.assign({}, remote, { v: 2, src: remote.src === 'set' ? 'set' : 'auto', sa: remoteTs, sb: remoteTs }), true);
          }
          paintSync();
        }
      }).catch(() => { fails++; paintSync(); });
    }

    // ---- MARKS ---------------------------------------------------------------------
    let marks = readMarks();
    let marksServer = signedIn && readJSON(SS, MARKS_OFF_KEY) !== 1;
    let marksInflight = false, marksAgain = false, limitShown = false;
    const mkKey = (part, a) => part + '|' + a;
    function markOf(secId) {
      const e = marks.m[mkKey(page, secId)];
      return e && !e.x ? e.c : 0;
    }
    function setMark(secId, c) {
      marks = readMarks();
      const key = mkKey(page, secId);
      const e = marks.m[key];
      const owner = signedIn && marksServer ? (marks.owner || 'acct') : null;   // flag off: plain device marks
      if (!c) {
        if (!e) return;
        if (e.st) marks.m[key] = { c: e.c, t: Date.now(), s: 0, x: 1, o: e.o || owner, st: e.st };   // H11
        else delete marks.m[key];
      } else {
        if (e && !e.x && e.c === c) return;
        const live = Object.keys(marks.m).filter(k => !marks.m[k].x).length;
        if ((!e || e.x) && live >= T.MARK_LIMIT) {
          if (!limitShown) { limitShown = true; announce('You have marked ' + T.MARK_LIMIT + ' sections, the most there can be. Remove one to mark this.'); }
          return false;
        }
        marks.m[key] = { c, t: Date.now(), s: 0, x: 0, o: e && e.o ? e.o : owner, st: e ? e.st : undefined };
      }
      writeMarks(marks);
      paintMarks();
      if (marksServer) at('marks', T.MARKS_DEBOUNCE_MS, pushMarks);
      return true;
    }
    function pullMarks(since) {
      if (!signedIn || !marksServer || !('fetch' in window)) return;
      fetch('/api/marks?since=' + (since || 0), { credentials: 'same-origin' }).then(r => {
        if (r.status === 401) { signedOutDetected(); return null; }
        if (r.status === 404) { marksOff(); return null; }
        if (!r.ok) return null;
        return r.json();
      }).then(data => {
        if (!data || !Array.isArray(data.rows)) return;
        marks = readMarks();
        if (marks.owner && data.owner && marks.owner !== data.owner) {
          // Another account signed in on this device: its marks are not ours.
          Object.keys(marks.m).forEach(k => { if (marks.m[k].o) delete marks.m[k]; });
          marks.owner = data.owner; marks.cursor = 0;
          writeMarks(marks);
          if (since) return pullMarks(0);
        }
        if (since && typeof data.cursor === 'number' && data.cursor < since) {
          // The server is behind this device's cursor: the cursor is bad. Start over.
          marks.cursor = 0; writeMarks(marks);
          return pullMarks(0);
        }
        marks.owner = data.owner || marks.owner;
        Object.keys(marks.m).forEach(k => { if (marks.m[k].o === 'acct') marks.m[k].o = marks.owner; });
        data.rows.forEach(row => applyRow(row));
        if (typeof data.cursor === 'number') marks.cursor = data.cursor;
        writeMarks(marks);
        paintMarks();
        if (data.more) return pullMarks(marks.cursor);
        if (Object.keys(marks.m).some(k => !marks.m[k].s && (!marks.m[k].o || marks.m[k].o === marks.owner))) pushMarks();
      }).catch(() => {});
    }
    function marksOff() {   // the server keeps no marks: anything tagged but never sent is a device mark
      marksServer = false;
      writeJSON(SS, MARKS_OFF_KEY, 1);
      marks = readMarks();
      Object.keys(marks.m).forEach(k => { const e = marks.m[k]; if (e.o && !e.s && !(e.st > 0)) { e.o = null; if (e.st < 0) delete e.st; } });
      writeMarks(marks);
    }
    function applyRow(row) {
      const key = mkKey(row.part, row.a);
      const e = marks.m[key];
      if (e && !e.s && (!e.o || e.o === marks.owner)) return;   // a local change waits to be sent
      if (row.x) delete marks.m[key];
      else marks.m[key] = { c: row.c, t: row.t, s: 1, x: 0, o: marks.owner, st: row.t };
    }
    function pushMarks(keepalive) {
      cancelT('marks');
      if (!signedIn || !marksServer) return;
      if (marksInflight) { marksAgain = true; return; }
      marks = readMarks();
      const sent = {};
      const ops = [];
      Object.keys(marks.m).forEach(k => {
        const e = marks.m[k];
        if (e.s || (e.o && marks.owner && e.o !== marks.owner) || ops.length >= 50) return;
        const [part, a] = k.split('|');
        ops.push({ part, a, c: e.x ? 0 : e.c });
        sent[k] = e.t;
        if (!e.st) e.st = -1;                  // possibly on the server from now on (H11)
      });
      if (!ops.length) return;
      writeMarks(marks);
      marksInflight = true;
      fetch('/api/marks', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin',
        keepalive: !!keepalive, body: JSON.stringify({ v: 1, ops })
      }).then(r => {
        if (r.status === 401) { signedOutDetected(); return null; }
        if (r.status === 404) { marksOff(); return null; }
        if (r.status === 409) {
          if (!limitShown) { limitShown = true; announce('Marks are full: ' + T.MARK_LIMIT + ' sections. The newest stay on this device only.'); }
          return null;
        }
        return r.ok ? r.json() : null;
      }).then(data => {
        if (!data || !Array.isArray(data.rows)) return;
        marks = readMarks();
        const got = {};
        data.rows.forEach(row => {
          const key = mkKey(row.part, row.a);
          got[key] = 1;
          const e = marks.m[key];
          if (!e) return;
          if (e.t !== sent[key]) { if (!(e.st > 0)) e.st = row.t; return; }   // changed again meanwhile: send that next
          if (row.x) delete marks.m[key];
          else marks.m[key] = { c: row.c, t: row.t, s: 1, x: 0, o: marks.owner, st: row.t };
        });
        // A removal the server never held comes back without a row: nothing to sync.
        Object.keys(sent).forEach(key => { const e = marks.m[key]; if (!got[key] && e && e.x && e.t === sent[key]) delete marks.m[key]; });
        writeMarks(marks);
        paintMarks();
        if (data.rows.length >= 50 || Object.keys(sent).length >= 50) marksAgain = true;   // more than one batch waiting
      }).catch(() => {}).then(() => {
        marksInflight = false;
        if (marksAgain) { marksAgain = false; pushMarks(); }
      });
    }

    // ==========================================================================
    // UI
    // ==========================================================================
    const h = (tag, cls, attrs) => {
      const e = document.createElement(tag);
      if (cls) e.className = cls;
      if (attrs) Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
      return e;
    };
    const live = h('div', 'utc-sr', { id: 'utc-live', 'aria-live': 'polite' });
    document.body.appendChild(live);
    function announce(text) {   // only ever after the reader's own action
      live.textContent = '';
      at('live', 60, () => { live.textContent = text; at('livecl', 4000, () => { live.textContent = ''; }); });
    }

    // ---- the cue, the place button, the place bar -----------------------------------
    let cue = null, head = null, ticks = null, segs = null, ghost = null, mark = null, hit = null;
    let btn = null, readout = null, staticText = '', desc = null, bar = null;
    const fineHover = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (nav) {
      cue = h('span', 'reading-cue is-idle', { 'aria-hidden': 'true' });
      cue.innerHTML = '<span class="cue-rail"><span class="cue-track"></span><span class="cue-head"></span>'
        + '<span class="cue-ticks"></span></span><span class="cue-segs"></span>'
        + '<span class="cue-ghost"><span class="utc-shape"><b></b></span></span>'
        + '<span class="cue-mark"><span class="utc-shape"><b></b></span></span>';
      head = cue.querySelector('.cue-head');
      ticks = cue.querySelector('.cue-ticks');
      segs = cue.querySelector('.cue-segs');
      ghost = cue.querySelector('.cue-ghost');
      mark = cue.querySelector('.cue-mark');
      nav.appendChild(cue);
      if (fineHover) {
        hit = h('span', 'cue-hit', { 'aria-hidden': 'true' });
        nav.insertBefore(hit, nav.firstChild);
      }

      readout = nav.querySelector('.book-progress');
      staticText = readout ? readout.textContent : '';
      btn = h('button', 'place-btn', { type: 'button', 'aria-expanded': 'false',
        'aria-controls': 'utc-placebar', 'aria-describedby': 'utc-place-desc' });
      if (readout) btn.appendChild(readout);
      btn.insertAdjacentHTML('beforeend', '<span class="place-glyph" aria-hidden="true"><span class="utc-shape"><b></b></span></span>'
        + '<span class="utc-sr"> Reading place</span>');
      const account = nav.querySelector('.book-account');
      nav.insertBefore(btn, account || null);
      desc = h('span', null, { id: 'utc-place-desc', hidden: '' });
      nav.appendChild(desc);

      bar = h('div', 'place-bar', { id: 'utc-placebar', role: 'group', 'aria-label': 'Reading place', hidden: '' });
      bar.innerHTML = ''
        + '<div class="pb-row pb-head">'
        +   '<span class="pb-info"><span class="pb-where"></span><span class="pb-sync"></span></span>'
        +   '<button type="button" class="pb-close" aria-label="Close the place bar">' + '<svg viewBox="0 0 10 10" aria-hidden="true" focusable="false"><path d="M2 2l6 6M8 2L2 8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>' + '</button>'
        + '</div>'
        + '<div class="pb-row pb-actions">'
        +   '<span class="pb-nudge">'
        +     '<button type="button" class="pb-step pb-prev" tabindex="-1" aria-hidden="true" title="Previous paragraph">◀¶</button>'
        +     '<span class="pb-slider" role="slider" tabindex="0" aria-label="Reading line, by paragraph" aria-valuemin="1" aria-valuemax="1" aria-valuenow="1"></span>'
        +     '<button type="button" class="pb-step pb-next" tabindex="-1" aria-hidden="true" title="Next paragraph">¶▶</button>'
        +   '</span>'
        +   '<button type="button" class="pb-btn pb-set">Set to where I’m reading</button>'
        +   '<button type="button" class="pb-btn pb-go">Go to saved place</button>'
        +   '<button type="button" class="pb-btn pb-mark" aria-haspopup="menu" aria-expanded="false">Mark this section</button>'
        +   '<button type="button" class="pb-btn pb-back" hidden>Back to before the detour</button>'
        +   '<button type="button" class="pb-btn pb-track" hidden>Let the book track</button>'
        +   '<button type="button" class="pb-btn pb-undo" hidden>Undo</button>'
        + '</div>';
      btn.insertAdjacentElement('afterend', bar);
    }
    const q = sel => (bar ? bar.querySelector(sel) : null);

    // Section dots: a mark button replaces each section's pulsing dot. Not a
    // tab stop and hidden from assistive tech (review H7): the keyboard and
    // screen-reader path is the place button → "Mark this section".
    const dots = new Map();
    document.querySelectorAll('section.section[id^="ch"]').forEach(sec => {
      const sn = sec.querySelector('.section-number');
      if (!sn) return;
      const d = h('button', 'mark-dot', { type: 'button', tabindex: '-1', 'aria-hidden': 'true' });
      d.dataset.sec = sec.id;
      sn.insertBefore(d, sn.firstChild);
      sn.classList.add('has-dot');
      dots.set(sec.id, d);
      d.addEventListener('click', e => {
        e.preventDefault();
        if (menuOpen && menuOpener === d) { closeMenu(false); return; }
        openMenu(sec.id, d, false);
      });
    });
    const tabDescs = h('div', null, { hidden: '' });
    document.body.appendChild(tabDescs);

    // ---- painting --------------------------------------------------------------------
    let curCh = null, cueRaf = 0, lastReadout = '', lastReadoutAt = -Infinity, lastReadoutSec = '';
    function queueCue() {
      if (cueRaf || !cue) return;
      cueRaf = requestAnimationFrame(() => { cueRaf = 0; paintHead(); });
    }
    function cueWidth() { return cueW; }
    function paintHead() {
      if (!cue || !G) return;
      const yL = window.scrollY + Lpx;
      const ch = chapterAt(yL);
      if (ch !== curCh) return swapChapter(ch);
      if (!ch) return;
      const p = Math.max(0, Math.min(1, (yL - ch.top) / Math.max(1, ch.bottom - ch.top)));
      cue.style.setProperty('--cue-p', p.toFixed(4));
    }
    function swapChapter(ch) {
      curCh = ch;
      cue.dataset.ch = ch ? ch.id : '';
      if (reduceMotion) { layoutChapter(); return; }
      cue.classList.add('is-swapping');
      at('cueswap', 160, () => { layoutChapter(); cue.classList.remove('is-swapping'); });
    }
    function layoutChapter() {
      const ch = curCh;
      cue.classList.toggle('is-idle', !ch);
      ticks.innerHTML = '';
      segs.innerHTML = '';
      if (!ch) { paintMark(); return; }
      const span = Math.max(1, ch.bottom - ch.top);
      ch.secs.forEach((si, n) => {
        const s = G.sections[si];
        const x0 = (s.top - ch.top) / span, x1 = ((n + 1 < ch.secs.length ? G.sections[ch.secs[n + 1]].top : ch.bottom) - ch.top) / span;
        if (n > 0) {
          const t = h('i', 'cue-tick');
          t.style.left = (x0 * 100).toFixed(3) + '%';
          ticks.appendChild(t);
        }
        const g = h('i', 'cue-seg');
        g.style.left = (x0 * 100).toFixed(3) + '%';
        g.style.width = ((x1 - x0) * 100).toFixed(3) + '%';
        g.style.setProperty('--n', n);
        g.dataset.sec = s.id;
        segs.appendChild(g);
      });
      paintHead();
      paintMark();
      paintMarks();
    }
    function markX(rec) {   // {x (0..1), dock: 'left'|'right'|null}
      if (!rec || !curCh) return null;
      if (rec.part !== page) return { x: partNum(rec.part) < partNum(page) ? 0 : 1, dock: true };
      const y = placeY(rec);
      if (y == null) return null;
      const span = Math.max(1, curCh.bottom - curCh.top);
      const x = (y - curCh.top) / span;
      if (x < 0) return { x: 0, dock: true };
      if (x > 1) return { x: 1, dock: true };
      return { x, dock: false };
    }
    let markW = 3;
    function setMx(el, px) {   // left edge on a whole pixel, the shape kept inside the track
      const W = cueWidth();
      const c = Math.max(markW / 2, Math.min(W - markW / 2, px));
      el.style.setProperty('--mx', Math.round(c - markW / 2) + 'px');
    }
    function paintMark() {
      if (!mark) return;
      const m = drag ? null : markX(C);
      mark.classList.toggle('is-none', !m && !drag);
      if (m) {
        setMx(mark, m.x * cueWidth());
        mark.classList.toggle('is-docked', m.dock);
      }
      mark.classList.toggle('is-pinned', !!(C && C.src === 'set'));
      paintSync();
    }
    function paintSync() {
      cancelT('synceval');
      if (dirty && syncState() === 'synced') at('synceval', Math.max(50, T.SYNC_BACKLOG_MS - (now() - dirtySince) + 50), paintSync);
      const st = syncState();
      [mark, btn].forEach(el => {
        if (!el) return;
        el.classList.toggle('is-synced', st === 'synced');
        el.classList.toggle('is-paused', st === 'paused');
      });
      if (desc) desc.textContent = describe(C) + ' ' + syncWords(st);
      paintBar();
      debugPaint();
    }
    function syncWords(st) {
      return st === 'synced' ? 'Synced across your devices.'
        : st === 'paused' ? 'Saved on this device; sync is paused.'
        : st === 'signedout' ? 'Saved on this device.' : 'Saved on this device.';
    }
    function shortText(rec) {
      if (!rec || rec.part !== page) return staticText;
      const chap = rec.chapterId === 'chBridge' ? 'BRIDGE' : 'CH ' + String(rec.chapterId || '').replace(/^ch/, '');
      const parts = [chap];
      const n = sectionNum(rec);
      if (n) parts.push('§' + n);
      const k = G && rec.k ? G.byId[rec.k] : null;
      const o = k ? paraOrdinal(k) : (rec.pn ? { n: rec.pn } : null);
      if (o && o.n) parts.push('¶' + o.n);
      return parts.join(' · ');
    }
    function describe(rec) {
      if (!rec) return 'No saved place yet.';
      const parts = [rec.chapterNum || ''];
      const n = sectionNum(rec);
      if (n) parts.push('section ' + n + (rec.sectionTitle ? ' ' + rec.sectionTitle.replace(/[.!?…]+$/, '') : ''));
      const k = G && rec.part === page && rec.k ? G.byId[rec.k] : null;
      const o = k ? paraOrdinal(k) : null;
      if (o && o.n) parts.push('paragraph ' + o.n + ' of ' + o.of);
      const where = parts.filter(Boolean).join(', ');
      return (rec.part !== page ? 'Part ' + ['', 'I', 'II', 'III', 'IV', 'V'][partNum(rec.part)] + ', ' : '') + where + '.';
    }
    // The readout shows location only, and changes at most on a section
    // change or every 10 s — nothing flickers at the edge of vision (H8/H9).
    function paintReadout(force, preview) {
      if (!readout) return;
      const text = preview || shortText(C);
      if (text === lastReadout) return;
      const sec = preview ? '' : (C && C.part === page ? C.section : '');
      if (!force && !preview && sec === lastReadoutSec && now() - lastReadoutAt < T.READOUT_MIN_MS) {
        at('readout', T.READOUT_MIN_MS - (now() - lastReadoutAt) + 20, () => paintReadout(true));
        return;
      }
      readout.textContent = text;
      lastReadout = text;
      if (!preview) { lastReadoutAt = now(); lastReadoutSec = sec; }
    }
    // The readout box keeps the width of the part's static line, right-aligned,
    // so its text can change without moving anything (zero layout shift).
    function reserveReadout() {
      if (!readout || readout.style.minWidth) return;
      const w = readout.offsetWidth;
      if (w > 0) readout.style.minWidth = Math.ceil(w) + 'px';
    }
    function paintAll() {
      paintMark();
      paintReadout(false);
      paintBar();
      debugPaint();
    }

    // Marks paint onto the section dot, the chapter tab and the rail tick.
    function paintMarks() {
      dots.forEach((d, secId) => {
        const c = markOf(secId);
        const was = d.classList.contains('is-marked') ? +d.dataset.c : 0;
        d.classList.toggle('is-marked', !!c);
        if (c) d.dataset.c = c; else delete d.dataset.c;
        if (c !== was) d.innerHTML = c ? glyphSvg(page, c) : '';
      });
      document.querySelectorAll('.chapter-nav .nav-item[href^="#"]').forEach(tab => {
        const secId = tab.getAttribute('href').slice(1);
        const c = markOf(secId);
        tab.classList.toggle('is-marked', !!c);
        const did = 'utc-mk-' + secId;
        let span = document.getElementById(did);
        if (c) {
          tab.dataset.c = c;
          if (!span) { span = h('span', null, { id: did }); tabDescs.appendChild(span); }
          span.textContent = 'Marked ' + slotName(page, c);
          tab.setAttribute('aria-describedby', did);
        } else {
          delete tab.dataset.c;
          if (tab.getAttribute('aria-describedby') === did) tab.removeAttribute('aria-describedby');
        }
      });
      paintRail();
      if (segs) segs.querySelectorAll('.cue-seg').forEach(g => {
        const c = markOf(g.dataset.sec);
        g.classList.toggle('is-marked', !!c);
        if (c) g.dataset.c = c; else delete g.dataset.c;
      });
    }
    function paintRail() {
      document.querySelectorAll('.section-rail .rail-tick').forEach(t => {
        const c = markOf(t.dataset.target);
        t.classList.toggle('is-marked', !!c);
        if (c) t.dataset.c = c; else delete t.dataset.c;
      });
    }
    document.addEventListener('utc:rail', paintRail);

    // ---- the place bar ---------------------------------------------------------------
    let barOpen = false, barTarget = null, barOrigin = null;
    function paintBar() {
      if (!bar) return;
      const st = syncState();
      q('.pb-where').textContent = C ? describe(C).replace(/\.$/, '') : 'No saved place yet';
      const sync = q('.pb-sync');
      sync.classList.toggle('is-synced', st === 'synced');
      sync.classList.toggle('is-paused', st === 'paused');
      if (st === 'signedout' && lost401) {
        sync.innerHTML = '<a href="/account">Reading sync · sign in</a>';
      } else {
        sync.textContent = st === 'synced' ? 'SYNCED' : st === 'paused' ? 'SAVED HERE · SYNC PAUSED' : 'SAVED ON THIS DEVICE';
      }
      const yL = window.scrollY + Lpx;
      const there = C && C.part === page && nearPlace(C, yL);
      const go = q('.pb-go');
      go.disabled = !C || !!there;
      q('.pb-back').hidden = !before;
      q('.pb-track').hidden = !(C && C.src === 'set');
      q('.pb-undo').hidden = !undoPrev;
      paintSlider();
    }
    function paintSlider() {
      if (!bar || !G) return;
      const k = barTarget || kAt(window.scrollY + Lpx);
      const sl = q('.pb-slider');
      if (!k || k.sec < 0) {
        sl.setAttribute('aria-valuenow', '1'); sl.setAttribute('aria-valuemax', '1');
        sl.setAttribute('aria-valuetext', 'Not in a section');
        sl.textContent = '¶ –';
        return;
      }
      const s = G.sections[k.sec];
      const o = paraOrdinal(k) || { n: 0, of: s.paras.length };
      sl.setAttribute('aria-valuemin', '1');
      sl.setAttribute('aria-valuemax', String(Math.max(1, o.of)));
      sl.setAttribute('aria-valuenow', String(Math.max(1, o.n)));
      sl.setAttribute('aria-valuetext', '§' + s.meta.num + ' ' + s.meta.title + ', paragraph ' + Math.max(1, o.n) + ' of ' + o.of);
      sl.textContent = '§' + s.meta.num + ' ¶' + Math.max(1, o.n);
    }
    function openPlaceBar(focusFirst) {
      if (!bar || barOpen) return;
      barOpen = true;
      barOrigin = { y: window.scrollY };
      bar.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      setPause('bar', true);
      paintBar();
      requestAnimationFrame(() => bar.classList.add('is-open'));
      barIdle();
      if (focusFirst) (q('.pb-set') || bar).focus();
    }
    // 30 s idle closes the bar (H5) — but never from under the reader's focus.
    function barIdle() {
      at('baridle', T.BAR_IDLE_MS, () => {
        const a = document.activeElement;
        if (menuOpen || (a && (bar.contains(a) || menu.contains(a)))) barIdle();
        else closePlaceBar(false);
      });
    }
    const keepBarFocus = () => {   // an action that hides or disables its own button hands focus on
      const a = document.activeElement;
      if (barOpen && a && bar.contains(a) && (a.hidden || a.disabled)) q('.pb-set').focus({ preventScroll: true });
    };
    function closePlaceBar(returnFocus) {
      if (!bar || !barOpen) return;
      const had = bar.contains(document.activeElement) || (menuOpen && menu.contains(document.activeElement));
      if (menuOpen && bar.contains(menuOpener)) closeMenu(false);
      barOpen = false;
      barTarget = null;
      clearOutline();
      cancelT('baridle');
      bar.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
      setPause('bar', false);
      at('barhide', reduceMotion ? 0 : 160, () => { if (!barOpen) bar.hidden = true; });
      if (returnFocus || had) btn.focus({ preventScroll: true });
    }
    if (btn) btn.addEventListener('click', () => (barOpen ? closePlaceBar(false) : openPlaceBar(false)));
    if (bar) {
      bar.addEventListener('pointerdown', barIdle);
      bar.addEventListener('keydown', barIdle);
      bar.addEventListener('focusin', barIdle);
      // Tabbing out of the bar (not into its menu or button) closes it.
      const keepBar = el => el && (bar.contains(el) || el === btn || menu.contains(el));
      [bar, btn].forEach(n => n.addEventListener('focusout', e => {
        if (barOpen && e.relatedTarget && !keepBar(e.relatedTarget)) closePlaceBar(false);
      }));
      q('.pb-close').addEventListener('click', () => closePlaceBar(true));
      q('.pb-set').addEventListener('click', () => {
        const k = kAt(window.scrollY + Lpx);
        if (k) { flashOutline(k); setPlace(k, 'here'); }
      });
      q('.pb-go').addEventListener('click', () => { goToPlace(C); });
      q('.pb-mark').addEventListener('click', e => {
        const k = kAt(window.scrollY + Lpx);
        if (k && k.sec >= 0) openMenu(G.sections[k.sec].id, e.currentTarget, true);
        else announce('Scroll into a section to mark it.');
      });
      q('.pb-back').addEventListener('click', () => {
        if (!before) return;
        const rec = before.rec;
        before = null; undoDetourUntil = 0;
        writeJSON(LS, BEFORE_KEY, null);
        commit(Object.assign({}, rec, { timestamp: Date.now(), sa: undefined }), { now: true });
        state = rec.src === 'set' ? 'PINNED' : 'READING';
        exc = null; R = null; saveTab();
        goToPlace(rec);
        announce('Back to ' + describe(rec));
      });
      q('.pb-track').addEventListener('click', () => {
        if (!C) return;
        commit(Object.assign({}, C, { src: 'auto', timestamp: Date.now() }), { now: true });
        reconsider();
        announce('The book tracks your place again.');
        paintBar();
        keepBarFocus();
      });
      q('.pb-undo').addEventListener('click', undoSet);
      // Nudge by paragraph: the reading line moves, the page follows (SETTLING),
      // so "Set to where I'm reading" is literally true afterwards (review M15).
      q('.pb-prev').addEventListener('click', () => nudge(-1, 'para'));
      q('.pb-next').addEventListener('click', () => nudge(1, 'para'));
      q('.pb-slider').addEventListener('keydown', e => {
        const map = { ArrowLeft: [-1, 'para'], ArrowDown: [-1, 'para'], ArrowRight: [1, 'para'], ArrowUp: [1, 'para'],
          PageUp: [-1, 'sec'], PageDown: [1, 'sec'], Home: [-1, 'edge'], End: [1, 'edge'] };
        if (map[e.key]) { e.preventDefault(); e.stopPropagation(); nudge(map[e.key][0], map[e.key][1]); }
        else if (e.key === 'Enter') {
          e.preventDefault();
          const k = barTarget || kAt(window.scrollY + Lpx);
          if (k) setPlace(k, 'here');
        }
      });
    }
    function nudge(dir, unit) {
      if (!G) return;
      const cur = barTarget || kAt(window.scrollY + Lpx);
      if (!cur) return;
      let target = null;
      if (unit === 'para') {
        const list = G.paras;
        let i = -1;
        list.forEach((p, n) => { if (p.top <= cur.top + 0.5) i = n; });
        const j = i < 0 ? (dir > 0 ? 0 : -1) : i + dir;
        if (j >= 0 && j < list.length) target = list[j];
      } else if (unit === 'sec') {
        let si;
        if (cur.sec >= 0) si = Math.max(0, Math.min(G.sections.length - 1, cur.sec + dir));
        else if (dir > 0) si = G.sections.findIndex(x => x.top > cur.top);
        else { si = -1; G.sections.forEach((x, n) => { if (x.top < cur.top) si = n; }); }
        if (si < 0) return;
        const s = G.sections[si];
        target = s.paras.length ? G.anchors[s.paras[0]] : G.byId[s.id];
      } else if (unit === 'edge') {   // the slider's own range: this section's first / last paragraph
        const sec = cur.sec >= 0 ? G.sections[cur.sec] : null;
        const ps = sec ? sec.paras : [];
        if (ps.length) target = G.anchors[dir < 0 ? ps[0] : ps[ps.length - 1]];
      } else {
        const ch = G.chapters[cur.ch];
        if (ch) {
          const ss = ch.secs.map(i => G.sections[i]);
          const s = dir < 0 ? ss[0] : ss[ss.length - 1];
          const ps = s ? s.paras : [];
          target = ps.length ? G.anchors[dir < 0 ? ps[0] : ps[ps.length - 1]] : null;
        }
      }
      if (!target) return;
      barTarget = target;
      selfScrollTo(target.top - Lpx);
      flashOutline(target);
      paintSlider();
    }
    let outlined = null;
    function flashOutline(k) {
      clearOutline();
      outlined = k.el;
      outlined.classList.add('utc-target');
      at('outline', 1600, clearOutline);
    }
    function clearOutline() {
      if (outlined) outlined.classList.remove('utc-target');
      outlined = null;
      cancelT('outline');
    }

    // ---- set my place ------------------------------------------------------------------
    function setPlace(k, how) {
      if (!G || !k) return;
      cancelT('commit'); cancelT('post');           // H4: nothing scheduled earlier may land after this
      const kid = k.id;
      freshTable(k);
      k = G.byId[kid] || k;
      const vY = Math.max(0, k.top - Lpx);          // the scroll that puts k on the attention line
      const anc = anchorAt(vY + READING_LINE);
      if (!anc) return;
      barTarget = null; barOrigin = { y: window.scrollY };   // Esc after Set only closes the bar
      const prev = C;
      const rec = makeRecord(anc, k, 'set');
      if (prev && bucket(prev) === bucket(rec)) { announce('Your place is already here.'); return; }
      const prevKind = exc ? exc.kind : null;
      exc = null; R = null; pinAway = null; gate = null;
      saveTab();
      commit(rec, { now: true, keepUndo: true });
      undoPrev = { rec: prev || null, kind: prevKind };
      state = 'PINNED';
      if (mark && !reduceMotion) { mark.classList.add('is-gliding'); at('glide', 260, () => mark.classList.remove('is-gliding')); }
      replay(mark);
      showToast(rec);
      announce('Place set: ' + describe(rec));
      paintBar();
      armChecks();
    }
    function undoSet() {
      if (!undoPrev) return;
      const prev = undoPrev.rec, prevKind = undoPrev.kind;
      undoPrev = null;
      barTarget = null; barOrigin = { y: window.scrollY };
      cancelT('commit'); cancelT('post');
      hideToast();
      if (prev) commit(Object.assign({}, prev, { timestamp: Date.now(), sa: undefined }), { now: true });
      else {
        C = null; writeProgress(null); writes++; dirty = false;
        if (signedIn && 'fetch' in window) {
          fetch('/api/position', { method: 'DELETE', credentials: 'same-origin', keepalive: true })
            .then(r => { if (r.status === 401) signedOutDetected(); }).catch(() => {});
        }
      }
      reconsider(prevKind);
      paintAll();
      keepBarFocus();
      announce('Undone. ' + (prev ? 'Your place is ' + describe(prev) : 'No saved place.'));
    }
    function goToPlace(rec) {
      if (!rec) return;
      if (rec.part === page) {
        closePlaceBar(!!(bar && bar.contains(document.activeElement)));
        selfScrollToAnchor(rec.anchor, rec.fraction);
      } else {
        writeJSON(SS, PENDING_KEY, { anchor: rec.anchor, fraction: rec.fraction, place: 1 });
        window.location.href = rec.part + '#' + rec.anchor;
      }
    }
    function selfScrollTo(top) {
      selfUntil = now() + 900;
      enterSettling(T.SETTLE_QUIET_MS);
      window.scrollTo({ top: Math.max(0, top), behavior: 'instant' });
    }
    function selfScrollToAnchor(anchor, fraction, smooth) {
      selfUntil = now() + (smooth ? 2600 : 2700);
      enterSettling(T.SETTLE_QUIET_MS);
      scrollToAnchor(anchor, fraction, smooth && !reduceMotion, () => {
        selfUntil = now() + 120;
        at('settle', T.SETTLE_QUIET_MS, endSettling);
      });
    }

    // ---- toast in the chip slot -----------------------------------------------------------
    let toast = null;
    function showToast(rec) {
      hideToast(true);
      toast = h('div', 'sync-chip place-toast');   // the live region already says it: announce once
      const n = sectionNum(rec);
      const k = G && rec.k ? G.byId[rec.k] : null;
      const o = k ? paraOrdinal(k) : null;
      toast.innerHTML = '<span class="sync-chip-eyebrow">Place set</span>'
        + '<span class="place-toast-where"></span>'
        + '<button type="button" class="place-toast-undo">Undo</button>';
      toast.querySelector('.place-toast-where').textContent = (n ? '§' + n : rec.chapterNum) + (o && o.n ? ' ¶' + o.n : '');
      toast.querySelector('.place-toast-undo').addEventListener('click', undoSet);
      let hold = false;
      const release = () => { hold = false; at('toast', T.TOAST_MS, hideToast); };
      toast.addEventListener('pointerenter', () => { hold = true; cancelT('toast'); });
      toast.addEventListener('pointerleave', release);
      toast.addEventListener('focusin', () => { hold = true; cancelT('toast'); });
      toast.addEventListener('focusout', release);
      document.querySelectorAll('.sync-chip:not(.place-toast)').forEach(c => c.classList.add('is-waiting'));
      document.body.appendChild(toast);
      requestAnimationFrame(() => requestAnimationFrame(() => toast && toast.classList.add('visible')));
      at('toast', T.TOAST_MS, () => { if (!hold) hideToast(); });
    }
    function hideToast(instant) {
      cancelT('toast');
      if (!toast) return;
      const t = toast;
      toast = null;
      t.classList.remove('visible');
      setTimeout(() => t.remove(), instant ? 0 : 500);
      document.querySelectorAll('.sync-chip.is-waiting').forEach(c => c.classList.remove('is-waiting'));
    }

    // ---- "On your other device" ------------------------------------------------------------
    function offerRemote(remote, adoptOnClick) {
      whenSettled(() => {
        if (remote.part === page && nearPlace(remote, window.scrollY + Lpx)) return;
        if (remote.part === page && pending && pending.anchor === remote.anchor) return;
        const chip = h('div', 'sync-chip', { role: 'status' });
        const eyebrow = h('span', 'sync-chip-eyebrow');
        eyebrow.textContent = 'On your other device';
        const link = h('a', 'sync-chip-link');
        const metaParts = [];
        if (remote.chapterNum) metaParts.push(remote.chapterNum);
        const num = sectionNum(remote);
        if (num) metaParts.push('§' + num);
        link.textContent = (metaParts.length ? metaParts.join(' · ') + ': ' : '')
          + (remote.sectionTitle || remote.chapterTitle || 'Continue reading') + ' →';
        link.href = remote.part + '#' + remote.anchor;
        link.addEventListener('click', e => {
          if (adoptOnClick) {
            C = remote; writeProgress(C); dirty = false;
          }
          if (remote.part === page) {
            e.preventDefault();
            selfScrollToAnchor(remote.anchor, remote.fraction, true);
          } else {
            writeJSON(SS, PENDING_KEY, { anchor: remote.anchor, fraction: remote.fraction, place: 1 });
          }
          hide();
        });
        const dismiss = h('button', 'sync-chip-dismiss', { type: 'button', 'aria-label': 'Dismiss' });
        dismiss.textContent = '×';
        dismiss.addEventListener('click', hide);
        function hide() {
          chip.classList.remove('visible');
          setTimeout(() => chip.remove(), 500);
        }
        chip.appendChild(eyebrow);
        chip.appendChild(link);
        chip.appendChild(dismiss);
        if (toast) chip.classList.add('is-waiting');
        document.body.appendChild(chip);
        requestAnimationFrame(() => requestAnimationFrame(() => chip.classList.add('visible')));
      });
    }

    // ---- the mark menu -------------------------------------------------------------------------
    const usePopover = typeof HTMLElement !== 'undefined' && 'popover' in HTMLElement.prototype;
    const menu = h('div', 'mark-menu', { id: 'utc-markmenu', role: 'menu' });
    if (usePopover) menu.setAttribute('popover', 'manual');
    else menu.hidden = true;
    let menuSec = null, menuOpener = null, menuOpen = false, menuKbd = false;
    function buildMenu(secId, fromBar) {
      const c = markOf(secId);
      const meta = secMeta.get(secId) || { num: '', title: '' };
      menu.setAttribute('aria-label', 'Mark section ' + meta.num + ' ' + meta.title);
      let html = '<div class="mm-title" aria-hidden="true">§' + meta.num + ' · mark</div>';
      html += '<button type="button" role="menuitemradio" class="mm-item" data-c="0" aria-checked="' + (c === 0) + '" tabindex="-1">'
        + '<span class="mm-glyph mm-none" aria-hidden="true"></span><span>None</span></button>';
      for (let s = 1; s <= 5; s++) {
        html += '<button type="button" role="menuitemradio" class="mm-item" data-c="' + s + '" aria-checked="' + (c === s) + '" tabindex="-1">'
          + '<span class="mm-glyph" data-c="' + s + '" aria-hidden="true">' + glyphSvg(page, s) + '</span><span>' + slotName(page, s) + '</span></button>';
      }
      if (!fromBar) html += '<div class="mm-sep" role="separator"></div>'
        + '<button type="button" role="menuitem" class="mm-item mm-place" tabindex="-1">Set my place here</button>';
      menu.innerHTML = html;
    }
    function menuItems() { return Array.prototype.slice.call(menu.querySelectorAll('.mm-item')); }
    function openMenu(secId, opener, viaKeyboard) {
      if (menuOpen) closeMenu(false);
      menuSec = secId; menuOpener = opener; menuKbd = !!viaKeyboard;
      buildMenu(secId, !!(bar && bar.contains(opener)));
      if (!menu.isConnected) document.body.appendChild(menu);
      const r = opener.getBoundingClientRect();
      menu.style.left = '0px'; menu.style.top = '0px';
      if (usePopover) { try { menu.showPopover(); } catch (e) { /* already open */ } } else menu.hidden = false;
      menu.scrollTop = 0;
      const mw = menu.offsetWidth, mh = Math.min(menu.offsetHeight, window.innerHeight - 64);
      let left = Math.min(window.innerWidth - mw - 12, Math.max(12, r.left - 8));
      let top = r.bottom + 8;
      if (top + mh > window.innerHeight - 8) top = Math.max(56, r.top - mh - 8);
      top = Math.max(56, Math.min(top, window.innerHeight - mh - 8));
      menu.style.left = left + 'px';
      menu.style.top = top + 'px';
      menuOpen = true;
      opener.setAttribute('aria-expanded', 'true');
      setPause('menu', true);
      requestAnimationFrame(() => menu.classList.add('is-open'));
      const items = menuItems();
      const cur = items.find(b => b.getAttribute('aria-checked') === 'true') || items[0];
      items.forEach(b => { b.tabIndex = b === cur ? 0 : -1; });
      cur.focus({ preventScroll: true });
    }
    function closeMenu(returnFocus) {
      if (!menuOpen) return;
      menuOpen = false;
      menu.classList.remove('is-open');
      if (usePopover) { try { menu.hidePopover(); } catch (e) { /* closed */ } } else menu.hidden = true;
      if (menuOpener) {
        if (bar && bar.contains(menuOpener)) menuOpener.setAttribute('aria-expanded', 'false');
        else menuOpener.removeAttribute('aria-expanded');
        // Opened from the place bar: focus goes back to its button. Opened by
        // pointer from a section dot (hidden from assistive tech): let go.
        if (returnFocus && menuKbd && menuOpener.isConnected) menuOpener.focus({ preventScroll: true });
        else if (menu.contains(document.activeElement)) document.activeElement.blur();
      }
      setPause('menu', false);
    }
    menu.addEventListener('click', e => {
      const item = e.target.closest('.mm-item');
      if (!item) return;
      const secId = menuSec;
      if (item.classList.contains('mm-place')) {
        const s = G && G.secById[secId];
        const k = s ? (s.paras.length ? G.anchors[s.paras[0]] : G.byId[s.id]) : null;
        closeMenu(true);
        if (k) setPlace(k, 'section');
        return;
      }
      const c = +item.dataset.c;
      const meta = secMeta.get(secId) || { num: '', title: '' };
      const ok = setMark(secId, c) !== false;
      closeMenu(true);
      if (!ok) return;
      const d = dots.get(secId);
      if (c && d) replay(d);
      announce(c ? 'Marked §' + meta.num + ' ' + meta.title + ': ' + slotName(page, c) + '.' : 'Mark removed from §' + meta.num + '.');
    });
    menu.addEventListener('pointerdown', () => { if (barOpen && bar.contains(menuOpener)) barIdle(); });
    menu.addEventListener('keydown', e => {
      if (barOpen && bar.contains(menuOpener)) barIdle();
      const items = menuItems();
      const i = items.indexOf(document.activeElement);
      let j = -1;
      if (e.key === 'ArrowDown') j = (i + 1) % items.length;
      else if (e.key === 'ArrowUp') j = (i - 1 + items.length) % items.length;
      else if (e.key === 'Home') j = 0;
      else if (e.key === 'End') j = items.length - 1;
      else if (e.key === 'Tab') { closeMenu(menuKbd); return; }
      if (j >= 0) {
        e.preventDefault();
        items.forEach((b, n) => { b.tabIndex = n === j ? 0 : -1; });
        items[j].focus({ preventScroll: true });
      }
    });
    document.addEventListener('pointerdown', e => {
      if (menuOpen && !menu.contains(e.target) && !(menuOpener && menuOpener.contains(e.target))) closeMenu(false);
    }, true);
    function replay(el) {   // the volume's set motion, once
      if (!el || reduceMotion) return;
      el.classList.remove('mk-anim');
      void el.offsetWidth;
      el.classList.add('mk-anim');
      at('anim-' + (el.dataset.sec || 'mark'), 700, () => el.classList.remove('mk-anim'));
    }

    // ---- hover: the cue widens under a slow mouse -------------------------------------------
    function openWide() {
      if (!cue || hover.open || !curCh) return;
      hover.open = true;
      cue.classList.add('is-wide');
      paintMarks();
    }
    function closeWide(untilMove) {
      cancelT('hoveropen'); cancelT('hoverclose');
      if (untilMove) hover.armed = false;
      if (!hover.open || drag) return;
      hover.open = false;
      cue.classList.remove('is-wide');
      paintReadout(true);
    }
    function segAt(clientX) {
      if (!segs || !curCh) return null;
      const x = clientX / cueWidth();
      const span = curCh.bottom - curCh.top;
      const y = curCh.top + x * span;
      let found = null;
      curCh.secs.forEach(i => { if (G.sections[i].top <= y) found = G.sections[i]; });
      return found;
    }
    if (hit) {
      hit.addEventListener('pointermove', e => {
        if (e.pointerType !== 'mouse') return;
        if (e.clientX === hover.lastX && e.clientY === hover.lastY) return;   // a synthetic move after scrolling
        hover.lastY = e.clientY;
        const t = now();
        const speed = hover.lastT ? Math.abs(e.clientX - hover.lastX) / Math.max(1, t - hover.lastT) : 0;
        hover.lastX = e.clientX; hover.lastT = t;
        hover.armed = true;
        cancelT('hoverclose');
        if (!hover.open) {
          if (speed > T.HOVER_SPEED) cancelT('hoveropen');
          else if (!pendingT('hoveropen')) at('hoveropen', T.HOVER_DWELL_MS, () => {
            // still moving, slowly: a pointer parked after a sweep does not open it (review M8)
            if (hover.armed && hover.lastT && now() - hover.lastT < 80) openWide();
          });
          return;
        }
        if (drag) return;
        const s = segAt(e.clientX);
        if (s) paintReadout(true, '§' + s.meta.label.replace(/\s[\u2014·]\s/, ' · '));
      });
      hit.addEventListener('pointerleave', () => {
        hover.lastT = 0;
        cancelT('hoveropen');
        if (hover.open && !drag) at('hoverclose', T.HOVER_CLOSE_MS, () => closeWide(false));
      });
      hit.addEventListener('click', e => {
        if (!hover.open || drag) return;
        const s = segAt(e.clientX);
        if (!s) return;
        navFlag = { at: now(), kind: 'cue' };
        window.scrollTo({ top: Math.max(0, s.top - navB), behavior: 'instant' });
      });
      window.addEventListener('wheel', () => { if (hover.open && !drag) closeWide(true); }, { passive: true });

      // Drag the mark to correct the place: snaps to paragraphs from the table,
      // never reads layout, never scrolls the page. Esc cancels; release sets.
      mark.addEventListener('pointerdown', e => {
        if (e.pointerType !== 'mouse' || !hover.open || !C) return;
        const m = markX(C);
        if (m && m.dock) return;
        e.preventDefault();
        mark.setPointerCapture(e.pointerId);
        drag = { id: e.pointerId, x0: e.clientX, active: false, target: null };
      });
      mark.addEventListener('click', () => {
        const m = markX(C);
        if (m && m.dock && !drag) goToPlace(C);
      });
      mark.addEventListener('pointermove', e => {
        if (!drag || e.pointerId !== drag.id) return;
        if (!drag.active) {
          if (Math.abs(e.clientX - drag.x0) < T.DRAG_PX) return;
          drag.active = true;
          cue.classList.add('is-dragging');
          ghost.style.setProperty('--mx', mark.style.getPropertyValue('--mx'));
        }
        const x = Math.max(0, Math.min(1, e.clientX / cueWidth()));
        const y = curCh.top + x * (curCh.bottom - curCh.top);
        let best = null;
        curCh.secs.forEach(si => G.sections[si].paras.forEach(pi => {
          const p = G.anchors[pi];
          if (!best || Math.abs(p.top - y) < Math.abs(best.top - y)) best = p;
        }));
        if (!best) return;
        drag.target = best;
        setMx(mark, ((best.top - curCh.top) / (curCh.bottom - curCh.top)) * cueWidth());
        const s = G.sections[best.sec];
        const o = paraOrdinal(best);
        paintReadout(true, '§' + s.meta.num + ' · ¶' + (o ? o.n : 1) + ', release to set');
      });
      const endDrag = commitIt => {
        if (!drag) return;
        const d = drag;
        drag = null;
        cue.classList.remove('is-dragging');
        try { mark.releasePointerCapture(d.id); } catch (e) { /* released */ }
        if (commitIt && d.active && d.target) setPlace(d.target, 'drag');
        else paintMark();
        paintReadout(true);
      };
      mark.addEventListener('pointerup', e => { if (drag && e.pointerId === drag.id) endDrag(true); });
      mark.addEventListener('pointercancel', () => endDrag(false));
      cancelDrag = () => endDrag(false);
      // The widened cue stays open while the pointer is on the mark itself.
      mark.addEventListener('pointerenter', () => cancelT('hoverclose'));
      mark.addEventListener('pointerleave', () => {
        if (hover.open && !drag) at('hoverclose', T.HOVER_CLOSE_MS, () => closeWide(false));
      });
    }

    // ---- one owner for Esc (review M17): drag → menu → tooltip → place bar → fullscreen
    window.addEventListener('keydown', e => {
      if (e.key !== 'Escape' || e.defaultPrevented) return;
      if (drag && cancelDrag) { cancelDrag(); e.preventDefault(); e.stopImmediatePropagation(); return; }
      if (menuOpen) { closeMenu(true); e.preventDefault(); e.stopImmediatePropagation(); return; }
      if (pauses.has('tip')) return;
      if (barOpen) {
        if (barTarget && barOrigin) { selfScrollTo(barOrigin.y); barTarget = null; paintSlider(); }
        closePlaceBar(true);
        e.preventDefault(); e.stopImmediatePropagation();
      } else if (hover.open) {
        closeWide(true);
        e.preventDefault(); e.stopImmediatePropagation();
      }
    }, true);

    // ---- inputs, navigation, visibility --------------------------------------------------------
    const markInput = () => {
      input(); touched = true;
      if (state === 'SETTLING' && now() > selfUntil) endSettling();
    };
    ['wheel', 'touchstart', 'touchmove', 'pointerdown'].forEach(t => window.addEventListener(t, markInput, { passive: true, capture: true }));
    window.addEventListener('pointermove', input, { passive: true });
    document.addEventListener('focusin', input);               // screen-reader browse moves focus (H6)
    document.addEventListener('selectionchange', input);
    window.addEventListener('keydown', e => {
      markInput();
      if (e.key === 'Home' || e.key === 'End') {
        const tgt = e.target;
        if (!(tgt && (tgt.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(tgt.tagName) || tgt.getAttribute('role') === 'slider'))) navFlag = { at: now(), kind: 'key' };
      }
    }, true);
    window.addEventListener('hashchange', () => { navFlag = { at: now(), kind: 'hash' }; });
    document.addEventListener('click', e => {
      const a = e.target.closest && e.target.closest('a[href]');
      if (!a || e.defaultPrevented) return;
      const url = new URL(a.getAttribute('href'), window.location.href);
      if (url.origin !== window.location.origin) return;
      const target = (url.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '') || 'index';
      if (target === page && url.hash) navFlag = { at: now(), kind: 'link' };
      else if (/^part-[1-5]$/.test(target) && target !== page) writeJSON(SS, DETOUR_KEY, { from: page, at: Date.now() });
    }, true);
    window.addEventListener('scroll', onScroll, { passive: true });
    if ('onscrollend' in window) window.addEventListener('scrollend', () => { if (burst) endBurst(); });

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') { accrue(); flush(false); }
      else {
        lastAccrue = now(); input();
        adoptLocal();
        marks = readMarks(); paintMarks();
      }
    });
    window.addEventListener('pagehide', () => flush(true));
    window.addEventListener('pageshow', e => {
      if (!e.persisted) return;
      lastAccrue = now();
      C = readProgress() || C;
      marks = readMarks(); paintMarks();
      enterSettling(T.SETTLE_QUIET_MS);
    });

    // Overlays from the other modules: glossary tooltip, fullscreen figure.
    document.addEventListener('utc:overlay', e => {
      const d = e.detail || {};
      if (d.name === 'tip') setPause('tip', !!d.open);
      if (d.name === 'fs') {
        if (d.open && pendingT('commit')) commitNow('auto');
        setPause('fs', !!d.open);
        if (d.open) { closePlaceBar(false); closeMenu(false); }
        else { selfUntil = now() + T.FS_SETTLE_MS; enterSettling(T.FS_SETTLE_MS); }
      }
    });

    // Rotation, zoom, window resize: re-pin the view; a height-only change
    // (the mobile URL bar) only moves the attention line (review M6).
    let roTimer = 0;
    window.addEventListener('resize', () => {
      const w = window.innerWidth, hgt = window.innerHeight, dpr = window.devicePixelRatio || 1;
      if (w !== lastW || dpr !== lastDPR) {
        lastW = w; lastH = hgt; lastDPR = dpr;
        // Reading at the place: the place holds (review M6). Elsewhere: the view.
        const atPlace = (state === 'READING' || state === 'PINNED' || (state === 'SETTLING' && prevState !== 'EXCURSION'))
          && C && C.part === page && nearPlace(C, restY + Lpx);
        const keep = atPlace ? { anchor: C.anchor, fraction: C.fraction } : viewAnchor;
        if (pendingT('commit')) cancelT('commit');
        enterSettling(T.SETTLE_QUIET_MS);
        requestAnimationFrame(() => {
          buildTable();
          if (keep) selfScrollToAnchor(keep.anchor, keep.fraction, false);
        });
      } else if (hgt !== lastH) {
        lastH = hgt;
        ihChangeAt = now();
        measureConsts();
        queueCue();
      }
    }, { passive: true });
    if ('ResizeObserver' in window) {
      new ResizeObserver(() => {
        clearTimeout(roTimer);
        roTimer = setTimeout(() => { if (state !== 'SETTLING' || !pendingT('settle')) buildTable(); else at('rebuild', 160, buildTable); }, 150);
      }).observe(document.body);
    }
    onSignedOut = () => { fails = 0; lost401 = true; marksServer = false; dirty = false; paintSync(); };

    function onTableBuilt() {
      if (cue) {
        cueW = cue.clientWidth || window.innerWidth;
        markW = (mark && mark.firstElementChild && mark.firstElementChild.offsetWidth) || markW;
        reserveReadout();
        cancelT('cueswap');
        cue.classList.remove('is-swapping');
        curCh = chapterAt(window.scrollY + Lpx);
        cue.dataset.ch = curCh ? curCh.id : '';
        layoutChapter();
      }
      paintAll();
    }

    // ---- RESTORE ------------------------------------------------------------------------------
    const hash = (window.location.hash || '').slice(1);
    let pending = readJSON(SS, PENDING_KEY);
    writeJSON(SS, PENDING_KEY, null);
    const navEntry = (performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || null;
    const navType = navEntry ? navEntry.type : 'navigate';
    paintMarks();
    reserveReadout();
    paintReadout(true);   // the saved place's text replaces the static line before first paint
    whenSettled(() => {
      buildTable();
      let target = null;
      if (pending && pending.anchor === hash) target = pending;                         // an explicit hand-off
      else if (navType === 'navigate' && C && C.part === page && (C.anchor === hash || !hash)) target = C;   // G4; reload/history keep their scroll (M5)
      else if (navType !== 'navigate' && tabPrev && tabPrev.view && (recheckView = tabPrev.view)) {
        // Reload / history: the browser restores its own scroll — except WebKit,
        // which jumps back to a stale #fragment. Return to this tab's last view.
        const v = anchorAt(window.scrollY + READING_LINE);
        if (!v || v.anchor !== tabPrev.view.anchor || Math.abs(v.fraction - tabPrev.view.fraction) > 0.05) target = tabPrev.view;
      }
      if (target) selfScrollToAnchor(target.anchor, target.fraction, false);
      else enterSettling(T.SETTLE_QUIET_MS);
      if (signedIn) { fetchRemote(); pullMarks(marks.owner ? marks.cursor || 0 : 0); }
      paintAll();
    });

    // ---- DEBUG: ?utc-debug — a local overlay for re-tuning; no network ---------------------------
    let dbg = null;
    function snapshotState() {
      const yL = window.scrollY + Lpx;
      const k = kAt(yL);
      const cy = placeY(C);
      return {
        state, paused: paused(),
        C: C ? { part: C.part, anchor: C.anchor, fraction: C.fraction, k: C.k, src: C.src, y: cy } : null,
        K: k ? k.id : null,
        R: R ? { part: R.part, anchor: R.anchor, fraction: R.fraction, k: R.k, src: R.src, y: placeY(R) } : null,
        Rprev: before ? { part: before.rec.part, anchor: before.rec.anchor, k: before.rec.k, at: before.at } : null,
        budget: Math.round(budget), cap: Math.round(cap),
        excursion: exc ? { kind: exc.kind, reason: exc.reason, readMs: Math.round(exc.readMs), spotMs: Math.round(exc.spotMs), chars: Math.round(exc.chars), paras: exc.paras.size, pastEnd: exc.pastEnd } : null,
        pinAway: pinAway ? { readMs: Math.round(pinAway.readMs), paras: pinAway.paras.size } : null,
        gate: gate ? { ms: Math.round(gate.ms) } : null,
        writes, posts, sync: syncState(), dirty, seq
      };
    }
    function debugPaint() {
      if (!debug) return;
      if (!dbg) {
        dbg = h('pre', 'utc-debug', { 'aria-hidden': 'true' });
        document.body.appendChild(dbg);
      }
      const s = snapshotState();
      dbg.textContent = s.state + (s.paused ? ' (paused)' : '') + '  sync:' + s.sync
        + '\nK ' + s.K + '\nC ' + (s.C ? s.C.anchor + ' @' + s.C.fraction + ' k=' + s.C.k + ' ' + s.C.src : 'none')
        + '\nR ' + (s.R ? s.R.anchor : 'none') + '   before ' + (s.Rprev ? s.Rprev.anchor : 'none')
        + '\nbudget ' + s.budget + ' / ' + s.cap
        + (s.excursion ? '\nexc ' + s.excursion.kind + '/' + s.excursion.reason + ' ' + (s.excursion.readMs / 1000).toFixed(1) + 's ' + s.excursion.chars + 'ch ' + s.excursion.paras + '¶' + (s.excursion.pastEnd ? ' past-end' : '') : '')
        + (s.pinAway ? '\npin-away ' + (s.pinAway.readMs / 1000).toFixed(1) + 's ' + s.pinAway.paras + '¶' : '')
        + (s.gate ? '\ngate ' + (s.gate.ms / 1000).toFixed(1) + 's' : '')
        + '\nwrites ' + s.writes + '  posts ' + s.posts;
    }
    if (debug) {
      window.__utcPlace = {
        T,
        snapshot: snapshotState,
        anchorAt: y => { const r = anchorAt(y); return r ? { anchor: r.anchor, fraction: r.fraction } : null; },
        liveAnchor: () => { const r = computeAnchor(); return r ? { anchor: r.anchor, fraction: r.fraction } : null; },
        table: () => (G ? G.anchors.map(a => ({ id: a.id, top: a.top, bottom: a.bottom, isPara: a.isPara, chars: a.chars,
          section: a.sec >= 0 ? G.sections[a.sec].id : null, chapter: a.ch >= 0 ? G.chapters[a.ch].id : null })) : []),
        L: () => Lpx,
        navB: () => navB,
        chars: (y0, y1) => Math.round(charsBetween(y0, y1)),
        rebuild: buildTable
      };
      debugPaint();
    }
  }

  // ==========================================================================
  // INDEX, GLOSSARY
  // ==========================================================================
  function initOther() {
    // A link from the glossary into a part is a look-up: the arrival is a detour.
    if (page === 'glossary') {
      document.addEventListener('click', e => {
        const a = e.target.closest && e.target.closest('a[href]');
        if (!a) return;
        const url = new URL(a.getAttribute('href'), window.location.href);
        const target = (url.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '');
        if (url.origin === window.location.origin && /^part-[1-5]$/.test(target)) {
          writeJSON(SS, DETOUR_KEY, { from: page, at: Date.now() });
        }
      }, true);
    }

    // -------- RESUME CARD (index page only) -------------------------------------
    const cover = document.querySelector('.cover');
    if (!cover) return;
    const accountLink = document.querySelector('.account-footer-link');

    function buildResumeCard(progress) {
      if (!progress) return;
      const card = document.createElement('a');
      card.className = 'resume-card';
      card.href = String(progress.part || '').replace(/\.html$/, '') + '#'
        + (progress.anchor || progress.section);
      card.setAttribute('aria-label', 'Resume reading where you left off');
      if (progress.anchor && typeof progress.fraction === 'number') {
        card.addEventListener('click', () => {
          writeJSON(SS, PENDING_KEY, { anchor: progress.anchor, fraction: progress.fraction, place: 1 });
        });
      }

      const eyebrow = document.createElement('div');
      eyebrow.className = 'resume-eyebrow';
      eyebrow.textContent = 'Where you left off';

      const body = document.createElement('div');
      body.className = 'resume-body';
      const metaParts = [];
      if (progress.chapterNum) metaParts.push(progress.chapterNum);
      const num = sectionNum(progress);
      if (num) metaParts.push('§' + num);
      if (metaParts.length) {
        const meta = document.createElement('span');
        meta.className = 'resume-meta';
        meta.textContent = metaParts.join(' · ');
        body.appendChild(meta);
      }
      const title = document.createElement('span');
      title.className = 'resume-title';
      title.textContent = progress.sectionTitle || progress.chapterTitle || 'Continue reading';
      body.appendChild(title);

      const arrow = document.createElement('span');
      arrow.className = 'resume-arrow';
      arrow.textContent = '→';
      arrow.setAttribute('aria-hidden', 'true');

      const dismiss = document.createElement('button');
      dismiss.type = 'button';
      dismiss.className = 'resume-dismiss';
      dismiss.setAttribute('aria-label', 'Dismiss');
      dismiss.textContent = '×';
      dismiss.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        card.classList.remove('visible');
        setTimeout(() => card.remove(), 720);
      });

      card.appendChild(eyebrow);
      card.appendChild(body);
      card.appendChild(arrow);
      card.appendChild(dismiss);

      cover.insertAdjacentElement('afterend', card);

      requestAnimationFrame(() => {
        requestAnimationFrame(() => card.classList.add('visible'));
      });
    }

    // Signed in: adopt a newer server position before building the card, so the
    // card reflects wherever the reader last was on any device — but never over
    // a place this device has not synced yet. Signed out: local only. The
    // footer says "on" only after the server answered (a 401 says "sign in").
    if (signedIn && 'fetch' in window) {
      fetch('/api/position', { credentials: 'same-origin' }).then(r => {
        if (r.status === 401) { signedOutDetected(); return { out: true }; }
        return r.ok ? r.json() : null;
      }).then(data => {
        const local = readProgress();
        if (data && data.out) {
          if (accountLink) accountLink.innerHTML = 'Reading sync · sign in <span aria-hidden="true">→</span>';
          return buildResumeCard(local);
        }
        if (data && accountLink) accountLink.innerHTML = 'Reading sync · on <span aria-hidden="true">→</span>';
        if (data && data.position && data.position.anchor) {
          const remoteTs = data.updated_at || 0;
          const adopt = !local ? true
            : local.v !== 2 ? remoteTs > (local.timestamp || 0)
            : !!local.sa && remoteTs > local.sa && !(local.src === 'set' && data.position.src !== 'set');
          if (adopt) {
            const p = data.position;
            const adopted = Object.assign({}, p, { v: 2, src: p.src === 'set' ? 'set' : 'auto', sa: remoteTs, sb: remoteTs, acct: 1, timestamp: Date.now() });
            writeProgress(adopted);
            return buildResumeCard(adopted);
          }
        }
        buildResumeCard(local);
      }).catch(() => buildResumeCard(readProgress()));
    } else {
      buildResumeCard(readProgress());
    }
  }
})();

// --- Glossary tooltips + index page ------------------------------------------
// Loads glossary.json (generated by scripts/build-glossary.js). For every
// <strong>, <em>, and <span class="key-term"> element on the page that matches
// a glossary entry, attaches a hover/focus tooltip showing the definition and
// linking back to the first-use location. Skips the term's own first-use
// element so the definition isn't tooltipped on top of itself.
//
// On glossary.html, populates the .glossary-content container with an
// alphabetical index built from the same JSON.
(function () {
  'use strict';
  if (!('fetch' in window)) return;

  const STORAGE_KEY = 'under-the-code:glossary';
  const STORAGE_VER_KEY = 'under-the-code:glossary-ver';

  function normalizeKey(s) {
    return s.toLowerCase()
      .replace(/<[^>]+>/g, ' ')
      .replace(/[^a-z0-9 +-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function fromCache(version) {
    try {
      if (localStorage.getItem(STORAGE_VER_KEY) !== version) return null;
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }
  function toCache(version, data) {
    try {
      localStorage.setItem(STORAGE_VER_KEY, version);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {}
  }

  // Resolve glossary.json relative to the current document.
  function loadGlossary() {
    return fetch('glossary.json')
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (!data || !data.entries) return null;
        const cached = fromCache(data.generated || '0');
        if (cached) return cached;
        toCache(data.generated || '0', data);
        return data;
      })
      .catch(() => null);
  }

  // -------- TOOLTIP -----------------------------------------------------------
  let tipEl = null;
  let hideTimer = null;
  let activeAnchor = null;

  function ensureTip() {
    if (tipEl) return tipEl;
    tipEl = document.createElement('div');
    tipEl.className = 'glossary-tip';
    tipEl.setAttribute('role', 'tooltip');
    document.body.appendChild(tipEl);
    return tipEl;
  }

  function buildTipContent(entry) {
    const currentPart = ((window.location.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '')) || 'index';
    const entryPart = (entry.part || '').toLowerCase().replace(/\.html$/, '');
    const here = entryPart === currentPart;
    const href = (here ? '' : entryPart) + '#' + entry.section;
    const sectionLabel = entry.section_label
      ? entry.section_label.split(/\s[\u2014·]\s/)[0].trim()
      : '';
    const meta = [entry.chapter_num, sectionLabel ? '§' + sectionLabel : '']
      .filter(Boolean).join(' · ');
    return ''
      + '<div class="glossary-tip-term">' + escapeHtml(entry.term) + '</div>'
      + '<div class="glossary-tip-def">' + escapeHtml(entry.definition) + '</div>'
      + '<a class="glossary-tip-link" href="' + href + '">'
      + escapeHtml(meta) + ' →</a>';
  }

  function placeTip(anchor) {
    const tip = tipEl;
    tip.style.visibility = 'hidden';
    tip.style.display = 'block';
    tip.classList.remove('below');
    const ar = anchor.getBoundingClientRect();
    const tr = tip.getBoundingClientRect();
    let top = ar.top + window.scrollY - tr.height - 12;
    let left = ar.left + window.scrollX + (ar.width / 2) - (tr.width / 2);
    if (top < window.scrollY + 8) {
      top = ar.bottom + window.scrollY + 12;
      tip.classList.add('below');
    }
    const minLeft = window.scrollX + 12;
    const maxLeft = window.scrollX + window.innerWidth - tr.width - 12;
    left = Math.max(minLeft, Math.min(left, maxLeft));
    tip.style.top = top + 'px';
    tip.style.left = left + 'px';
    tip.style.visibility = 'visible';
  }

  function showTip(anchor, entry) {
    if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
    openedByTouch = false;   // the touch path sets it again after this call
    activeAnchor = anchor;
    const tip = ensureTip();
    tip.innerHTML = buildTipContent(entry);
    placeTip(anchor);
    requestAnimationFrame(() => tip.classList.add('visible'));
    tipScrollY = window.scrollY;
    document.dispatchEvent(new CustomEvent('utc:overlay', { detail: { name: 'tip', open: true } }));
  }

  // Pass 22 — touch. A tap on a term toggles its tooltip; a second tap, a tap
  // anywhere else, or Esc dismisses it; scrolling leaves it open; rotating
  // re-places it. Mouse hover and keyboard focus behave exactly as before:
  // the touch path only engages for ~800 ms after a touch/pen pointerdown,
  // which suppresses the emulated mouseenter/focus/blur a tap generates.
  let lastTouch = 0;
  let openedByTouch = false;   // a touch-opened tip ignores mouse-leave/blur (WebKit
                              // fires them after a scroll moves text under the old tap point)
  const touchRecent = () => Date.now() - lastTouch < 800;
  // Dismiss on the END of a tap outside (little movement, not cancelled):
  // a swipe to keep reading becomes a scroll (pointercancel) and leaves the
  // tooltip open.
  let downAt = null;
  document.addEventListener('pointerdown', e => {
    if (e.pointerType !== 'touch' && e.pointerType !== 'pen') {
      downAt = null;
      // Hybrid devices: a mouse click elsewhere closes a touch-opened tip.
      if (openedByTouch && activeAnchor && !activeAnchor.contains(e.target) && !(tipEl && tipEl.contains(e.target))) hideTip();
      return;
    }
    lastTouch = Date.now();
    downAt = { x: e.clientX, y: e.clientY };
  }, { passive: true, capture: true });
  document.addEventListener('pointercancel', () => { downAt = null; }, { passive: true, capture: true });
  // A real mouse moving (pointer events never come from a tap's emulated mouse
  // events) hands a touch-opened tip back to ordinary hover rules.
  document.addEventListener('pointermove', e => {
    if (e.pointerType === 'mouse' && openedByTouch && !touchRecent()) openedByTouch = false;
  }, { passive: true });
  document.addEventListener('pointerup', e => {
    if (e.pointerType !== 'touch' && e.pointerType !== 'pen') return;
    lastTouch = Date.now();
    const start = downAt; downAt = null;
    if (!activeAnchor || !start) return;
    if (Math.hypot(e.clientX - start.x, e.clientY - start.y) > 10) return;
    const t = e.target;
    if (activeAnchor.contains(t) || (tipEl && tipEl.contains(t))) return;
    hideTip();
  }, { passive: true, capture: true });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && activeAnchor && !e.defaultPrevented) hideTip();
  });
  // Pass 25 (review H5): a tooltip opened by hover or keyboard focus closes
  // once the reader scrolls on, so a focused term never holds the reading
  // clock. Touch-opened tooltips keep Pass 22's rule: scrolling leaves them open.
  let tipScrollY = 0;
  window.addEventListener('scroll', () => {
    if (activeAnchor && !openedByTouch && Math.abs(window.scrollY - tipScrollY) > 48) hideTip();
  }, { passive: true });
  window.addEventListener('resize', () => {
    if (activeAnchor && tipEl && tipEl.classList.contains('visible')) placeTip(activeAnchor);
  }, { passive: true });

  function hideTip() {
    if (!tipEl) return;
    if (activeAnchor) document.dispatchEvent(new CustomEvent('utc:overlay', { detail: { name: 'tip', open: false } }));
    tipEl.classList.remove('visible');
    activeAnchor = null;
    openedByTouch = false;
    if (hideTimer) clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      if (tipEl) tipEl.style.display = 'none';
    }, 220);
  }

  // Allow the cursor to enter the tooltip itself without dismissing.
  function bindTipPersistence() {
    const tip = ensureTip();
    tip.addEventListener('mouseenter', () => {
      if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
    });
    tip.addEventListener('mouseleave', () => { if (!openedByTouch) hideTip(); });
    tip.addEventListener('click', e => { if (e.target.closest('.glossary-tip-link')) hideTip(); });
  }

  // -------- ATTACH TOOLTIPS ---------------------------------------------------
  function attachTooltips(glossary) {
    const entries = glossary.entries || {};
    const currentPart = ((window.location.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '')) || 'index';
    const candidates = document.querySelectorAll('strong, em, span.key-term');
    const anchored = new Set();  // keys that already have a first-use id

    candidates.forEach(el => {
      // Skip elements inside diagram SVGs / code blocks / nav.
      if (el.closest('svg, .diagram-card svg, code, pre, nav, .chapter-nav, .section-rail, .resume-card, .glossary-tip, .place-bar, .mark-menu, .sync-chip, [popover]')) {
        return;
      }
      const text = el.textContent.trim();
      if (!text || text.length > 80) return;
      const key = normalizeKey(text);
      if (!key) return;
      if (key.length === 1 && el.tagName === 'EM') return;   // a variable (the RSA ciphertext c), not a term
      const entry = entries[key];
      if (!entry) return;

      const section = el.closest('section.section');
      const inFirstUseSection = (entry.part || '').toLowerCase().replace(/\.html$/, '') === currentPart
        && section !== null
        && section.id === entry.section;

      if (inFirstUseSection) {
        // The first matching element in document order gets the anchor id;
        // every subsequent occurrence in the same section is silent (the
        // reader is reading the definition itself).
        if (!anchored.has(key)) {
          if (!el.id) el.id = 'term-' + key.replace(/\s+/g, '-');
          anchored.add(key);
        }
        return;
      }

      el.classList.add('glossary-ref');
      el.setAttribute('tabindex', '0');

      let openTimer = null;
      el.addEventListener('mouseenter', () => {
        if (touchRecent()) return;
        openTimer = setTimeout(() => showTip(el, entry), 160);
      });
      el.addEventListener('mouseleave', () => {
        if (openTimer) { clearTimeout(openTimer); openTimer = null; }
        if (touchRecent() || openedByTouch) return;
        hideTip();
      });
      el.addEventListener('focus', () => { if (!touchRecent()) showTip(el, entry); });
      el.addEventListener('blur', () => { if (!touchRecent() && !openedByTouch) hideTip(); });
      el.addEventListener('click', () => {
        if (!touchRecent()) return;
        if (activeAnchor === el) hideTip(); else { showTip(el, entry); openedByTouch = true; }
      });
    });

    bindTipPersistence();
  }

  // -------- GLOSSARY INDEX PAGE -----------------------------------------------
  function renderIndex(glossary) {
    const container = document.querySelector('.glossary-content');
    if (!container) return;

    const entries = Object.values(glossary.entries || {});
    entries.sort((a, b) => {
      const at = a.term.toLowerCase().replace(/^[^a-z0-9]+/, '');
      const bt = b.term.toLowerCase().replace(/^[^a-z0-9]+/, '');
      return at.localeCompare(bt);
    });

    const groups = new Map();
    entries.forEach(e => {
      const first = e.term.replace(/^[^A-Za-z0-9]+/, '').charAt(0).toUpperCase();
      const letter = /[A-Z]/.test(first) ? first : (/[0-9]/.test(first) ? '#' : '·');
      if (!groups.has(letter)) groups.set(letter, []);
      groups.get(letter).push(e);
    });

    const letters = Array.from(groups.keys()).sort();
    let html = '<nav class="glossary-jump">';
    letters.forEach(L => {
      html += '<a href="#letter-' + L + '">' + L + '</a>';
    });
    html += '</nav>';

    letters.forEach(L => {
      html += '<section class="glossary-group" id="letter-' + L + '">';
      html += '<div class="glossary-letter">' + L + '</div>';
      html += '<div class="glossary-list">';
      groups.get(L).forEach(e => {
        const sLabel = e.section_label ? e.section_label.split(/\s[\u2014·]\s/)[0].trim() : '';
        const meta = [e.chapter_num, sLabel ? '§' + sLabel : ''].filter(Boolean).join(' · ');
        const href = (e.part || '').replace(/\.html$/, '') + '#' + e.section;
        html += '<article class="glossary-entry">'
          + '<a class="glossary-entry-anchor" href="' + href + '">'
          +   '<div class="glossary-entry-term">' + escapeHtml(e.term) + '</div>'
          +   '<div class="glossary-entry-def">' + escapeHtml(e.definition) + '</div>'
          +   '<div class="glossary-entry-loc">' + escapeHtml(meta) + ' →</div>'
          + '</a>'
          + '</article>';
      });
      html += '</div></section>';
    });

    container.innerHTML = html;

    const counter = document.querySelector('.glossary-count');
    if (counter) counter.textContent = entries.length + ' terms';
  }

  // -------- INDEX FOOTER LINK -------------------------------------------------
  // On index.html: add a small "Glossary" link to the footer if the glossary
  // loaded successfully. Self-disabling — never shows if glossary.json is
  // missing or empty.
  function maybeAddIndexLink(glossary) {
    if (!document.querySelector('.cover')) return;  // not the index page
    const footer = document.querySelector('.footer');
    if (!footer) return;
    if (footer.querySelector('.glossary-footer-link')) return;

    const link = document.createElement('a');
    link.className = 'glossary-footer-link';
    link.href = 'glossary';
    const count = (glossary.entries && Object.keys(glossary.entries).length) || 0;
    link.innerHTML = 'Glossary · ' + count + ' terms <span aria-hidden="true">→</span>';
    footer.appendChild(link);
  }

  // -------- INIT --------------------------------------------------------------
  loadGlossary().then(glossary => {
    if (!glossary || !glossary.entries) return;
    if (document.querySelector('.glossary-content')) {
      renderIndex(glossary);
    } else {
      attachTooltips(glossary);
      maybeAddIndexLink(glossary);
    }
  });
})();
