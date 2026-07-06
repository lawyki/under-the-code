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

// --- Reading progress + resume -----------------------------------------------
// Tracks the reader's position through the book. On the index page, surfaces
// a quiet "where you left off" card between the cover and the part shelves.
// All state lives in localStorage; it never leaves the device. Stale progress
// (>90 days) is silently dropped so the card doesn't haunt forever.
(function () {
  'use strict';
  if (!('IntersectionObserver' in window)) return;
  if (!('localStorage' in window)) return;

  const STORAGE_KEY = 'under-the-code:progress';
  const MAX_AGE_DAYS = 90;
  const SAVE_DEBOUNCE_MS = 1200;

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

  // -------- TRACKER (runs on every part-N.html page) ---------------------------
  const sections = Array.from(document.querySelectorAll('section.section[id^="ch"]'));
  if (sections.length) {
    const visibleSet = new Set();
    let saveTimer = null;
    let lastSavedId = null;

    function formatChapterNum(chapterId) {
      if (chapterId === 'chBridge') return 'Bridge';
      const n = chapterId.replace(/^ch/, '');
      return /^\d+$/.test(n) ? 'Chapter ' + n : chapterId;
    }

    function snapshot(section) {
      const id = section.id;
      const chapterId = id.split('-')[0];
      const chapter = document.getElementById(chapterId);
      let chapterTitle = '';
      if (chapter) {
        const h1 = chapter.querySelector('.chapter-hero h1, h1');
        if (h1) chapterTitle = h1.textContent.trim();
      }
      const h2 = section.querySelector('h2');
      const sLabel = section.querySelector('.section-number');
      const part = (window.location.pathname.split('/').pop() || '').toLowerCase().replace(/\.html$/, '');
      return {
        part: part || 'index',
        section: id,
        chapterId,
        chapterNum: formatChapterNum(chapterId),
        chapterTitle,
        sectionLabel: sLabel ? sLabel.textContent.trim() : '',
        sectionTitle: h2 ? h2.textContent.trim() : '',
        timestamp: Date.now()
      };
    }

    function scheduleSave(section) {
      if (section.id === lastSavedId) return;
      if (saveTimer) clearTimeout(saveTimer);
      saveTimer = setTimeout(() => {
        writeProgress(snapshot(section));
        lastSavedId = section.id;
      }, SAVE_DEBOUNCE_MS);
    }

    function recompute() {
      if (visibleSet.size === 0) return;
      let topmost = null;
      let topmostY = Infinity;
      visibleSet.forEach(s => {
        const y = s.getBoundingClientRect().top;
        if (y < topmostY) { topmostY = y; topmost = s; }
      });
      if (topmost) scheduleSave(topmost);
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) visibleSet.add(entry.target);
        else visibleSet.delete(entry.target);
      });
      recompute();
    }, { rootMargin: '0px 0px -50% 0px' });

    sections.forEach(s => observer.observe(s));
  }

  // -------- RESUME CARD (index page only) -------------------------------------
  const cover = document.querySelector('.cover');
  if (!cover) return;

  const progress = readProgress();
  if (!progress) return;

  const card = document.createElement('a');
  card.className = 'resume-card';
  card.href = String(progress.part || '').replace(/\.html$/, '') + '#' + progress.section;
  card.setAttribute('aria-label', 'Resume reading where you left off');

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
