// --- Go deeper: optional outside videos beside the text (2026-10-12) ----------
// The book must teach on its own; these point to the best outside resources for
// readers who want more. Each one is an <aside class="deeper"> placed right
// after the passage it belongs to (markup and rules: README "Go deeper videos").
// Its static content is the no-script fallback and the single source of the
// data. With script, the aside becomes a tab at the right edge that shows while
// that passage (the element before the aside and the one after it) is on
// screen; hover (fine pointers) or a tap opens a small panel.
//
// Privacy: nothing is requested from Google until the reader presses play. The
// placeholder is drawn here (no i.ytimg.com thumbnail); the click inserts the
// player from www.youtube-nocookie.com. data-embed="off" (the creator disabled
// embedding) leaves only the plain "Watch on YouTube" link.
(function () {
  'use strict';
  const asides = document.querySelectorAll('aside.deeper[data-yt]');
  if (!asides.length) return;

  const hoverable = window.matchMedia('(hover: hover) and (pointer: fine)');
  const SVG = 'http://www.w3.org/2000/svg';
  const instances = [];
  let seq = 0;

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function icon(kind) {
    const s = document.createElementNS(SVG, 'svg');
    s.setAttribute('viewBox', '0 0 16 16');
    s.setAttribute('aria-hidden', 'true');
    s.setAttribute('focusable', 'false');
    const p = document.createElementNS(SVG, 'path');
    p.setAttribute('d', kind === 'play' ? 'M5 3.2v9.6L12.6 8z'
      : kind === 'close' ? 'M4 4l8 8M12 4l-8 8'
      : 'M6 3h7v7M13 3L6.5 9.5M11 9.5V13H3V5h3.5');   // out: an arrow leaving a box
    if (kind === 'play') p.setAttribute('fill', 'currentColor');
    else { p.setAttribute('fill', 'none'); p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '1.6'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round'); }
    s.appendChild(p);
    return s;
  }
  function outLink(cls, href, text) {
    const a = el('a', cls, text);
    a.href = href; a.target = '_blank'; a.rel = 'noopener';
    return a;
  }

  asides.forEach(aside => {
    const id = aside.getAttribute('data-yt') || '';
    const titleA = aside.querySelector('.deeper-title');
    const channelA = aside.querySelector('.deeper-channel');
    if (!/^[A-Za-z0-9_-]{11}$/.test(id) || !titleA || !channelA) return;   // malformed: keep the static fallback
    const n = ++seq;
    const d = {
      id,
      title: titleA.textContent.trim(),
      watch: titleA.href,
      creator: channelA.textContent.trim(),
      channel: channelA.href,
      length: aside.getAttribute('data-length') || '',
      intro: (aside.querySelector('.deeper-intro') || {}).textContent || '',
      about: (aside.querySelector('.deeper-about') || {}).textContent || '',
      embed: aside.getAttribute('data-embed') !== 'off'
    };

    // the tab
    const tab = el('button', 'deeper-tab');
    tab.type = 'button';
    tab.setAttribute('aria-expanded', 'false');
    tab.setAttribute('aria-controls', 'deeper-panel-' + n);
    tab.appendChild(icon('play'));
    tab.appendChild(el('span', 'deeper-tab-label', 'Go deeper'));
    if (d.length) tab.appendChild(el('span', 'deeper-tab-len', d.length));
    tab.setAttribute('aria-label', 'Go deeper: an outside video' + (d.length ? ', ' + d.length : ''));

    // the panel
    const panel = el('div', 'deeper-panel');
    panel.id = 'deeper-panel-' + n;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'false');
    panel.setAttribute('aria-labelledby', 'deeper-intro-' + n);

    const head = el('div', 'deeper-head');
    head.appendChild(el('span', 'deeper-kicker', 'Go deeper · outside video'));
    const close = el('button', 'deeper-close');
    close.type = 'button';
    close.setAttribute('aria-label', 'Close');
    close.appendChild(icon('close'));
    head.appendChild(close);
    panel.appendChild(head);

    const intro = el('div', 'deeper-intro', d.intro);
    intro.id = 'deeper-intro-' + n;
    panel.appendChild(intro);
    if (d.about) panel.appendChild(el('div', 'deeper-about', d.about));

    let stage = null, poster = null;
    if (d.embed) {
      stage = el('div', 'deeper-stage');
      poster = el('button', 'deeper-poster');
      poster.type = 'button';
      poster.setAttribute('aria-label', 'Play “' + d.title + '” by ' + d.creator + (d.length ? ', ' + d.length : '') + '. Loads YouTube.');
      const play = el('span', 'deeper-play');
      play.appendChild(icon('play'));
      poster.appendChild(play);
      poster.appendChild(el('span', 'deeper-poster-title', d.title));
      poster.appendChild(el('span', 'deeper-poster-meta', d.creator + (d.length ? ' · ' + d.length : '')));
      stage.appendChild(poster);
      panel.appendChild(stage);

      const consent = el('div', 'deeper-consent', 'Playing this loads YouTube, which may set cookies. ');
      const priv = el('a', '', 'Privacy');
      priv.href = '/account#privacy';
      consent.appendChild(priv);
      panel.appendChild(consent);
    }

    const credit = el('div', 'deeper-credit', '“' + d.title + '” by ');
    credit.appendChild(outLink('', d.channel, d.creator));
    panel.appendChild(credit);

    const foot = el('div', 'deeper-foot');
    const watch = outLink('deeper-watch', d.watch, 'Watch on YouTube');
    watch.appendChild(icon('out'));
    foot.appendChild(watch);
    foot.appendChild(el('span', 'deeper-legal', 'Not affiliated with this book or covered by its licence.'));
    panel.appendChild(foot);

    aside.appendChild(tab);
    aside.appendChild(panel);
    aside.classList.add('is-live');

    const zone = [aside.previousElementSibling, aside.nextElementSibling].filter(Boolean);
    const inst = { aside, tab, panel, d, zone, inView: false, state: 'closed', playing: false, timer: 0 };
    instances.push(inst);

    function setState(next, focusInside) {
      clearTimeout(inst.timer);
      if (next === 'closed' && inst.playing) stop();
      inst.state = next;
      const open = next !== 'closed';
      aside.classList.toggle('is-open', open);
      aside.classList.toggle('is-playing', inst.playing);
      tab.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open && focusInside) (poster || watch).focus({ preventScroll: true });
      refresh();
    }
    inst.setState = setState;
    function later(fn, ms) { clearTimeout(inst.timer); inst.timer = setTimeout(fn, ms); }

    function playNow() {
      const f = document.createElement('iframe');
      f.className = 'deeper-player';
      f.src = 'https://www.youtube-nocookie.com/embed/' + d.id + '?autoplay=1&rel=0';
      f.title = '“' + d.title + '” by ' + d.creator + ' (YouTube)';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      stage.replaceChildren(f);
      inst.playing = true;
      setState('pinned');
      f.focus({ preventScroll: true });
    }
    function stop() {
      inst.playing = false;
      stage.replaceChildren(poster);
    }

    tab.addEventListener('click', e => {
      if (inst.state === 'pinned') { setState('closed'); return; }
      setState('pinned', e.detail === 0);   // detail 0: keyboard, so move focus in
    });
    close.addEventListener('click', () => { setState('closed'); tab.focus({ preventScroll: true }); });
    if (poster) poster.addEventListener('click', playNow);

    // hover: a peek that closes when the pointer leaves; any click or focus inside pins it
    tab.addEventListener('pointerenter', e => {
      if (e.pointerType !== 'mouse' || !hoverable.matches || inst.state !== 'closed') return;
      later(() => setState('peek'), 120);
    });
    [tab, panel].forEach(n => n.addEventListener('pointerleave', e => {
      if (e.pointerType !== 'mouse') return;
      if (inst.state === 'peek') later(() => setState('closed'), 320);
      else if (inst.state === 'closed') clearTimeout(inst.timer);
    }));
    panel.addEventListener('pointerenter', () => { if (inst.state === 'peek') clearTimeout(inst.timer); });
    panel.addEventListener('pointerdown', () => { if (inst.state === 'peek') setState('pinned'); });
    panel.addEventListener('focusin', () => { if (inst.state === 'peek') setState('pinned'); });
    tab.addEventListener('focus', refresh);
    tab.addEventListener('blur', refresh);
  });
  if (!instances.length) return;

  // Escape closes; a click elsewhere closes a panel that is not playing
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    instances.forEach(i => {
      if (i.state === 'closed') return;
      const had = i.aside.contains(document.activeElement);
      i.setState('closed');
      if (had) i.tab.focus({ preventScroll: true });
    });
  });
  document.addEventListener('pointerdown', e => {
    instances.forEach(i => {
      if (i.state !== 'closed' && !i.playing && !i.aside.contains(e.target)) i.setState('closed');
    });
  });

  // the passage on screen: the middle 60 % of the viewport touches its zone
  if ('IntersectionObserver' in window) {
    const seen = new Map();
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => seen.set(en.target, en.isIntersecting));
      instances.forEach(i => {
        const was = i.inView;
        i.inView = i.zone.some(z => seen.get(z));
        if (was && !i.inView && i.state !== 'closed' && !i.playing) i.setState('closed');
      });
      refresh();
    }, { rootMargin: '-20% 0px -20% 0px' });
    instances.forEach(i => i.zone.forEach(z => io.observe(z)));
  } else {
    instances.forEach(i => { i.inView = true; });
  }

  // one tab at a time: an open panel first, else the first passage on screen
  function refresh() {
    const open = instances.find(i => i.state !== 'closed');
    const lead = open || instances.find(i => i.inView);
    instances.forEach(i => {
      const shown = i === lead || i.tab === document.activeElement;
      i.aside.classList.toggle('is-shown', shown);
    });
  }
  refresh();
})();
