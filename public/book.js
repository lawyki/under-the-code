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
    if (e.key === 'Escape' && activeCard) exitFullscreen();
  });

  document.addEventListener('click', e => {
    if (activeCard && !activeCard.contains(e.target)) exitFullscreen();
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
  }

  function paintActive() {
    rail.querySelectorAll('.rail-tick').forEach(t => {
      t.classList.toggle('active', t.dataset.target === activeId);
    });
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

// --- Reading progress + resume + cross-device sync -----------------------------
// Tracks the reader's exact position: the deepest stable element id at the
// reading line (chapter → section → paragraph/figure — paragraph ids are baked
// into the HTML by scripts/add-anchor-ids.js) plus a fractional offset within
// that element. Never raw scrollY, so the position survives viewport and font
// changes. localStorage is the always-on store; when the reader is signed in
// (detected by the JS-readable `under_signedin` hint cookie — no API call is
// ever made for signed-out readers), the same snapshot is mirrored to
// /api/position: debounced 2s after scrolling stops, flushed with sendBeacon
// on pagehide/visibilitychange. On load, a server position newer than local
// surfaces as a quiet, dismissible "on your other device" chip — never a modal.
(function () {
  'use strict';
  if (!('localStorage' in window)) return;

  const STORAGE_KEY = 'under-the-code:progress';
  const PENDING_KEY = 'under-the-code:pending-offset';
  const MAX_AGE_DAYS = 90;
  const SAVE_IDLE_MS = 2000;
  const READING_LINE = 56;   // px from viewport top: 48px fixed header + 8

  const signedIn = /(?:^|;\s*)under_signedin=1(?:;|$)/.test(document.cookie);
  const page = ((window.location.pathname.split('/').pop() || '')
    .toLowerCase().replace(/\.html$/, '')) || 'index';
  const isPart = /^part-[1-5]$/.test(page);

  function readProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data || !data.timestamp || !data.section || !data.part) return null;
      const ageDays = (Date.now() - data.timestamp) / (1000 * 60 * 60 * 24);
      if (ageDays > MAX_AGE_DAYS) {
        localStorage.removeItem(STORAGE_KEY);
        return null;
      }
      return data;
    } catch (e) { return null; }
  }
  function writeProgress(data) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) {}
  }

  function formatChapterNum(chapterId) {
    if (chapterId === 'chBridge') return 'Bridge';
    const n = chapterId.replace(/^ch/, '');
    return /^\d+$/.test(n) ? 'Chapter ' + n : chapterId;
  }

  // -------- ANCHOR MODEL --------------------------------------------------------
  // Candidates are baked ids only: chapters (ch7), sections (ch7-locks),
  // paragraphs (ch7-locks-p4), figures (fig-7-3). Runtime-assigned ids
  // (glossary term anchors) and ids inside SVGs are excluded — an anchor must
  // exist identically on every device that loads the same page.
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

  function snapshot() {
    const a = computeAnchor();
    if (!a) return null;
    const section = a.el.closest('section.section');
    const scopeId = (section && section.id) || a.el.id;
    const chapterId = scopeId.split('-')[0];
    const chapter = document.getElementById(chapterId);
    let chapterTitle = '';
    if (chapter) {
      const h1 = chapter.querySelector('.chapter-hero h1, h1');
      if (h1) chapterTitle = h1.textContent.trim();
    }
    const h2 = section ? section.querySelector('h2') : null;
    const sLabel = section ? section.querySelector('.section-number') : null;
    return {
      part: page,
      anchor: a.anchor,
      fraction: a.fraction,
      section: section ? section.id : scopeId,
      chapterId,
      chapterNum: formatChapterNum(chapterId),
      chapterTitle,
      sectionLabel: sLabel ? sLabel.textContent.trim() : '',
      sectionTitle: h2 ? h2.textContent.trim() : '',
      timestamp: Date.now()
    };
  }

  function scrollToAnchor(anchor, fraction, smooth) {
    const el = document.getElementById(anchor);
    if (!el) return false;
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
      done = true;
      if (ro) { ro.disconnect(); ro = null; }
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      detach.forEach(t => window.removeEventListener(t, cancel));
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
    const t0 = (window.performance && performance.now) ? performance.now() : Date.now();
    let stableFrames = 0, lastY = window.scrollY;
    (function tick() {
      if (done) return;
      repin();
      const y = window.scrollY;
      stableFrames = (Math.abs(y - lastY) < 0.5) ? stableFrames + 1 : 0;
      lastY = y;
      const elapsed = ((window.performance && performance.now) ? performance.now() : Date.now()) - t0;
      if (stableFrames >= 8 || elapsed > 2500) { stop(); return; }
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

  // -------- TRACKER (part pages) --------------------------------------------
  if (isPart) {
    let saveTimer = null;
    let lastLocalKey = '';
    let lastSentKey = '';

    // Bucket the fraction so micro-scrolls don't churn writes.
    function keyOf(s) { return s.part + '#' + s.anchor + '@' + Math.round(s.fraction * 20); }

    function doSave(flush) {
      const s = snapshot();
      if (!s) return;
      const key = keyOf(s);
      if (key !== lastLocalKey) {
        writeProgress(s);
        lastLocalKey = key;
      }
      if (!signedIn || key === lastSentKey) return;
      const body = JSON.stringify({
        part: s.part, anchor: s.anchor, fraction: s.fraction,
        section: s.section, chapterId: s.chapterId, chapterNum: s.chapterNum,
        chapterTitle: s.chapterTitle, sectionLabel: s.sectionLabel,
        sectionTitle: s.sectionTitle
      });
      if (flush && navigator.sendBeacon) {
        if (navigator.sendBeacon('/api/position', new Blob([body], { type: 'application/json' }))) {
          lastSentKey = key;
        }
      } else {
        fetch('/api/position', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body,
          keepalive: !!flush
        }).then(r => { if (r.ok) lastSentKey = key; }).catch(() => {});
      }
    }

    window.addEventListener('scroll', () => {
      if (saveTimer) clearTimeout(saveTimer);
      saveTimer = setTimeout(() => doSave(false), SAVE_IDLE_MS);
    }, { passive: true });

    function flush() {
      if (saveTimer) clearTimeout(saveTimer);
      doSave(true);
    }
    window.addEventListener('pagehide', flush);
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') flush();
    });

    // ---- Restore the exact offset within the anchored element ----------------
    const hash = (location.hash || '').slice(1);
    let pending = null;
    try {
      pending = JSON.parse(sessionStorage.getItem(PENDING_KEY) || 'null');
      sessionStorage.removeItem(PENDING_KEY);
    } catch (e) { /* ignore */ }
    const localAtLoad = readProgress();

    whenSettled(() => {
      if (pending && pending.anchor === hash) {
        scrollToAnchor(hash, pending.fraction, false);
      } else if (localAtLoad && localAtLoad.part === page && localAtLoad.anchor === hash) {
        scrollToAnchor(hash, localAtLoad.fraction, false);
      }
      // Record that the reader is here, even if they never scroll.
      setTimeout(() => doSave(false), 2500);
    });

    // ---- "On your other device" offer (signed in, server ahead of local) -----
    if (signedIn && 'fetch' in window) {
      fetch('/api/position').then(r => (r.ok ? r.json() : null)).then(data => {
        if (!data || !data.position || !data.position.anchor) return;
        const remote = data.position;
        const remoteTs = data.updated_at || 0;
        const localTs = (localAtLoad && localAtLoad.timestamp) || 0;
        if (remoteTs > localTs) {
          // Adopt the newer position so the index resume card stays current.
          writeProgress(Object.assign({}, remote, { timestamp: remoteTs }));
        }
        if (remoteTs <= localTs + 1500) return;          // not ahead of this device
        if (remote.part === page && remote.anchor === hash) return; // already going there
        whenSettled(() => {
          if (remote.part === page) {
            const el = document.getElementById(remote.anchor);
            if (el) {
              const target = window.scrollY + el.getBoundingClientRect().top;
              if (Math.abs(target - window.scrollY) < window.innerHeight * 0.75) return;
            }
          }
          showSyncChip(remote);
        });
      }).catch(() => {});
    }

    function showSyncChip(remote) {
      const chip = document.createElement('div');
      chip.className = 'sync-chip';
      chip.setAttribute('role', 'status');

      const eyebrow = document.createElement('span');
      eyebrow.className = 'sync-chip-eyebrow';
      eyebrow.textContent = 'On your other device';

      const link = document.createElement('a');
      link.className = 'sync-chip-link';
      const metaParts = [];
      if (remote.chapterNum) metaParts.push(remote.chapterNum);
      if (remote.sectionLabel) {
        const num = remote.sectionLabel.split('—')[0].trim();
        if (num) metaParts.push('§' + num);
      }
      link.textContent = (metaParts.length ? metaParts.join(' · ') + ' — ' : '')
        + (remote.sectionTitle || remote.chapterTitle || 'Continue reading') + ' →';
      link.href = remote.part + '#' + remote.anchor;
      link.addEventListener('click', e => {
        if (remote.part === page) {
          e.preventDefault();
          scrollToAnchor(remote.anchor, remote.fraction, true);
        } else {
          try {
            sessionStorage.setItem(PENDING_KEY,
              JSON.stringify({ anchor: remote.anchor, fraction: remote.fraction }));
          } catch (err) { /* ignore */ }
        }
        hide();
      });

      const dismiss = document.createElement('button');
      dismiss.type = 'button';
      dismiss.className = 'sync-chip-dismiss';
      dismiss.setAttribute('aria-label', 'Dismiss');
      dismiss.textContent = '×';
      dismiss.addEventListener('click', hide);

      function hide() {
        chip.classList.remove('visible');
        setTimeout(() => chip.remove(), 500);
      }

      chip.appendChild(eyebrow);
      chip.appendChild(link);
      chip.appendChild(dismiss);
      document.body.appendChild(chip);
      requestAnimationFrame(() => {
        requestAnimationFrame(() => chip.classList.add('visible'));
      });
    }
  }

  // -------- RESUME CARD (index page only) -------------------------------------
  const cover = document.querySelector('.cover');
  if (!cover) return;

  // Quiet footer entry point: reflect sync state on the account link.
  if (signedIn) {
    const accountLink = document.querySelector('.account-footer-link');
    if (accountLink) {
      accountLink.innerHTML = 'Reading sync · on <span aria-hidden="true">→</span>';
    }
  }

  function buildResumeCard(progress) {
    if (!progress) return;
    const card = document.createElement('a');
    card.className = 'resume-card';
    card.href = String(progress.part || '').replace(/\.html$/, '') + '#'
      + (progress.anchor || progress.section);
    card.setAttribute('aria-label', 'Resume reading where you left off');
    if (progress.anchor && typeof progress.fraction === 'number') {
      card.addEventListener('click', () => {
        try {
          sessionStorage.setItem(PENDING_KEY,
            JSON.stringify({ anchor: progress.anchor, fraction: progress.fraction }));
        } catch (e) { /* ignore */ }
      });
    }

    const eyebrow = document.createElement('div');
    eyebrow.className = 'resume-eyebrow';
    eyebrow.textContent = 'Where you left off';

    const body = document.createElement('div');
    body.className = 'resume-body';
    const metaParts = [];
    if (progress.chapterNum) metaParts.push(progress.chapterNum);
    if (progress.sectionLabel) {
      const num = progress.sectionLabel.split('—')[0].trim();
      if (num) metaParts.push('§' + num);
    }
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
  // card reflects wherever the reader last was on any device. Signed out:
  // local only, exactly as before.
  if (signedIn && 'fetch' in window) {
    fetch('/api/position').then(r => (r.ok ? r.json() : null)).then(data => {
      const local = readProgress();
      if (data && data.position && data.position.anchor) {
        const remoteTs = data.updated_at || 0;
        if (remoteTs > ((local && local.timestamp) || 0)) {
          const adopted = Object.assign({}, data.position, { timestamp: remoteTs });
          writeProgress(adopted);
          buildResumeCard(adopted);
          return;
        }
      }
      buildResumeCard(local);
    }).catch(() => buildResumeCard(readProgress()));
  } else {
    buildResumeCard(readProgress());
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
      .replace(/[^a-z0-9 -]/g, ' ')
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
      ? entry.section_label.split('—')[0].trim()
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
    activeAnchor = anchor;
    const tip = ensureTip();
    tip.innerHTML = buildTipContent(entry);
    placeTip(anchor);
    requestAnimationFrame(() => tip.classList.add('visible'));
  }

  function hideTip() {
    if (!tipEl) return;
    tipEl.classList.remove('visible');
    activeAnchor = null;
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
    tip.addEventListener('mouseleave', hideTip);
  }

  // -------- ATTACH TOOLTIPS ---------------------------------------------------
  function attachTooltips(glossary) {
    const entries = glossary.entries || {};
    const currentPart = ((window.location.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '')) || 'index';
    const candidates = document.querySelectorAll('strong, em, span.key-term');
    const anchored = new Set();  // keys that already have a first-use id

    candidates.forEach(el => {
      // Skip elements inside diagram SVGs / code blocks / nav.
      if (el.closest('svg, .diagram-card svg, code, pre, nav, .chapter-nav, .section-rail, .resume-card, .glossary-tip')) {
        return;
      }
      const text = el.textContent.trim();
      if (!text || text.length > 80) return;
      const key = normalizeKey(text);
      if (!key) return;
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
        openTimer = setTimeout(() => showTip(el, entry), 160);
      });
      el.addEventListener('mouseleave', () => {
        if (openTimer) { clearTimeout(openTimer); openTimer = null; }
        hideTip();
      });
      el.addEventListener('focus', () => showTip(el, entry));
      el.addEventListener('blur', hideTip);
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
        const sLabel = e.section_label ? e.section_label.split('—')[0].trim() : '';
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
