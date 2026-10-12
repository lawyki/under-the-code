// --- Go deeper: optional outside videos beside the text (2026-10-12) ----------
// The book teaches on its own; these point to the best outside resources for
// readers who want more. Each is an <aside class="deeper"> placed just before
// the passage it belongs to (rules: README "Go deeper videos"). Its static
// content is the no-script fallback and the single source of the data.
//
// Wide screens: a note in the right margin, beside the passage.
// Narrower: a small pill at the bottom right while the passage is on screen.
// Either opens a viewer (a modal <dialog>) with the play button.
//
// Privacy: nothing is requested from Google until the reader presses play. The
// picture is drawn here (no i.ytimg.com thumbnail); play inserts the player
// from www.youtube-nocookie.com. data-embed="off" (embedding disabled by the
// creator) leaves only the plain "Watch on YouTube" link.
(function () {
  'use strict';
  const asides = document.querySelectorAll('aside.deeper[data-yt]');
  if (!asides.length) return;
  const NS = 'http://www.w3.org/2000/svg';

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function svg(viewBox, cls) {
    const s = document.createElementNS(NS, 'svg');
    s.setAttribute('viewBox', viewBox);
    s.setAttribute('aria-hidden', 'true');
    s.setAttribute('focusable', 'false');
    if (cls) s.setAttribute('class', cls);
    return s;
  }
  function add(parent, tag, attrs) {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    parent.appendChild(n);
    return n;
  }
  function icon(kind) {
    const s = svg('0 0 16 16');
    if (kind === 'play') add(s, 'path', { d: 'M5.5 3.5v9l7-4.5z', fill: 'currentColor' });
    else add(s, 'path', { d: kind === 'close' ? 'M4 4l8 8M12 4l-8 8' : 'M6 3h7v7M13 3L6.5 9.5M11 9.5V13H3V5h3.5',
      fill: 'none', stroke: 'currentColor', 'stroke-width': '1.6', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' });
    return s;
  }
  function link(cls, href, text) {
    const a = el('a', cls, text);
    a.href = href; a.target = '_blank'; a.rel = 'noopener';
    return a;
  }

  // The picture: drawn in the book's figure style, never the video's thumbnail.
  // "enigma": a key, three rotors, the reflector, the path out and back to a lamp.
  function art(kind) {
    const s = svg('0 0 320 180', 'deeper-art');
    if (kind !== 'enigma') return s;
    const line = 'rgba(236,230,218,0.42)', faint = 'rgba(236,230,218,0.16)', gold = '#d4a853';
    [90, 160, 230].forEach((cx, i) => {
      const g = add(s, 'g', { class: i === 0 ? 'deeper-rotor is-fast' : 'deeper-rotor' });
      add(g, 'circle', { cx, cy: 90, r: 32, fill: 'none', stroke: line, 'stroke-width': 1.5 });
      add(g, 'circle', { cx, cy: 90, r: 24, fill: 'none', stroke: faint });
      for (let k = 0; k < 26; k++) {
        const t = k / 26 * Math.PI * 2, c = Math.cos(t), n = Math.sin(t);
        add(g, 'line', { x1: cx + 26 * c, y1: 90 + 26 * n, x2: cx + 30 * c, y2: 90 + 30 * n, stroke: faint });
      }
      add(g, 'line', { x1: cx, y1: 58, x2: cx, y2: 66, stroke: gold, 'stroke-width': 2, 'stroke-linecap': 'round' });
      add(g, 'circle', { cx, cy: 90, r: 4, fill: faint });
    });
    add(s, 'rect', { x: 280, y: 48, width: 12, height: 84, rx: 3, fill: 'none', stroke: line, 'stroke-width': 1.5 });
    add(s, 'circle', { cx: 30, cy: 70, r: 8, fill: 'none', stroke: line, 'stroke-width': 1.5 });
    add(s, 'circle', { cx: 30, cy: 110, r: 8, fill: gold, class: 'deeper-lamp' });
    const path = { fill: 'none', stroke: gold, 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
    add(s, 'path', Object.assign({ d: 'M38 70 H60 L124 62 L192 80 L280 74' }, path));
    add(s, 'path', Object.assign({ d: 'M280 106 L192 100 L124 120 L60 110 H38', opacity: 0.6 }, path));
    return s;
  }

  // one shared viewer
  const dlg = el('dialog', 'deeper-viewer');
  dlg.setAttribute('aria-labelledby', 'deeper-viewer-title');
  const card = el('div', 'dv-card');
  const head = el('div', 'dv-head');
  head.appendChild(el('span', 'dv-kicker', 'Go deeper · outside video'));
  const closeBtn = el('button', 'dv-close');
  closeBtn.type = 'button';
  closeBtn.setAttribute('aria-label', 'Close');
  closeBtn.appendChild(icon('close'));
  head.appendChild(closeBtn);
  const stage = el('div', 'dv-stage');
  const credit = el('div', 'dv-credit');
  credit.id = 'deeper-viewer-title';
  const about = el('div', 'dv-about');
  const foot = el('div', 'dv-foot');
  [head, stage, credit, about, foot].forEach(n => card.appendChild(n));
  dlg.appendChild(card);
  document.body.appendChild(dlg);

  let current = null, opener = null;

  function open(d, from) {
    current = d; opener = from;
    stage.replaceChildren();
    credit.replaceChildren(el('span', 'dv-title', '“' + d.title + '”'), document.createTextNode(' by '), link('', d.channel, d.creator));
    about.textContent = d.about;
    foot.replaceChildren();
    if (d.embed) {
      stage.appendChild(art(d.art));
      const play = el('button', 'dv-play');
      play.type = 'button';
      play.setAttribute('aria-label', 'Play “' + d.title + '” by ' + d.creator + ', ' + d.length + '. Loads YouTube.');
      const disc = el('span', 'dv-play-disc');
      disc.appendChild(icon('play'));
      play.appendChild(disc);
      play.appendChild(el('span', 'dv-play-len', d.length));
      play.addEventListener('click', () => playNow(d));
      stage.appendChild(play);
      const consent = el('span', 'dv-consent', 'Playing loads YouTube, which may set cookies. ');
      const priv = el('a', '', 'Privacy');
      priv.href = '/account#privacy';
      consent.appendChild(priv);
      foot.appendChild(consent);
    } else {
      stage.classList.add('is-off');
    }
    const watch = link('dv-watch', d.watch, 'Watch on YouTube');
    watch.appendChild(icon('out'));
    foot.appendChild(watch);
    document.documentElement.classList.add('deeper-lock');
    dlg.showModal();
    (stage.querySelector('.dv-play') || watch).focus();
  }
  function playNow(d) {
    const f = document.createElement('iframe');
    f.className = 'dv-player';
    f.src = 'https://www.youtube-nocookie.com/embed/' + d.id + '?autoplay=1&rel=0';
    f.title = '“' + d.title + '” by ' + d.creator + ' (YouTube)';
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    stage.replaceChildren(f);
    f.focus();
  }
  dlg.addEventListener('close', () => {
    stage.replaceChildren();               // stops the video
    stage.classList.remove('is-off');
    document.documentElement.classList.remove('deeper-lock');
    if (opener && opener.isConnected) opener.focus({ preventScroll: true });
    current = null;
  });
  closeBtn.addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });   // the backdrop

  const pills = [];
  asides.forEach(aside => {
    const id = aside.getAttribute('data-yt') || '';
    const titleA = aside.querySelector('.deeper-title');
    const channelA = aside.querySelector('.deeper-channel');
    if (!/^[A-Za-z0-9_-]{11}$/.test(id) || !titleA || !channelA) return;   // malformed: keep the fallback
    const length = aside.getAttribute('data-length') || '';
    const mins = /^(\d+):(\d\d)$/.exec(length);
    const d = {
      id, length,
      short: mins ? Math.max(1, Math.round(+mins[1] + mins[2] / 60)) + ' min' : length,
      title: titleA.textContent.trim(), watch: titleA.href,
      creator: channelA.textContent.trim(), channel: channelA.href,
      about: ((aside.querySelector('.deeper-about') || {}).textContent || '').trim(),
      art: aside.getAttribute('data-art') || '',
      embed: aside.getAttribute('data-embed') !== 'off'
    };

    // the margin note (wide screens)
    const note = el('button', 'deeper-note');
    note.type = 'button';
    note.setAttribute('aria-haspopup', 'dialog');
    note.appendChild(el('span', 'dn-kicker', 'Go deeper'));
    const thumb = el('span', 'dn-thumb');
    thumb.appendChild(art(d.art));
    const badge = el('span', 'dn-badge');
    badge.appendChild(icon('play'));
    thumb.appendChild(badge);
    note.appendChild(thumb);
    note.appendChild(el('span', 'dn-title', d.title));
    note.appendChild(el('span', 'dn-meta', d.creator + ' · ' + d.short));
    note.addEventListener('click', () => open(d, note));

    // the pill (narrow screens)
    const pill = el('button', 'deeper-pill');
    pill.type = 'button';
    pill.setAttribute('aria-haspopup', 'dialog');
    pill.setAttribute('aria-label', 'Go deeper: “' + d.title + '” by ' + d.creator + ', ' + d.short);
    const pd = el('span', 'dp-disc');
    pd.appendChild(icon('play'));
    pill.appendChild(pd);
    pill.appendChild(el('span', 'dp-label', 'Go deeper'));
    pill.appendChild(el('span', 'dp-meta', d.short));
    pill.addEventListener('click', () => open(d, pill));

    aside.appendChild(note);
    aside.appendChild(pill);
    aside.classList.add('is-live');
    pills.push({ aside, zone: [aside.nextElementSibling].filter(Boolean), seen: false });
  });

  // the pill shows while its passage crosses the middle of the screen
  if (!('IntersectionObserver' in window)) { pills.forEach(p => p.aside.classList.add('is-near')); return; }
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => pills.forEach(p => { if (p.zone[0] === en.target) p.seen = en.isIntersecting; }));
    let shown = false;   // one at a time
    pills.forEach(p => { const on = p.seen && !shown; if (on) shown = true; p.aside.classList.toggle('is-near', on); });
  }, { rootMargin: '-25% 0px -25% 0px' });
  pills.forEach(p => p.zone.forEach(z => io.observe(z)));
})();
