// Live figures (owner, 2026-11-12: "it should be interactable, this sort of game of a transistor, how it actually
// works"). A figure whose <svg> carries data-live is driven by the reader, not by a clock: a slider under the
// picture sets one quantity and the picture answers. The resting picture is plain SVG and reads without this file.
// Nothing moves until the reader acts: a press-here mark (.fig-hint) shows what to touch. Motion runs only while the
// figure is on screen; under reduced motion the picture answers in still states.
(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));

  // The slider row under a slider figure, with the press-here mark on its thumb until the reader takes it.
  function slider(svg, o) {
    const row = document.createElement('div');
    row.className = 'fig-live is-armed';
    row.innerHTML = '<span aria-hidden="true">' + o.left + '</span>'
      + '<span class="fig-live-track"><input type="range" min="0" max="' + o.max + '" step="' + o.step + '" value="0" aria-label="' + o.label + '">'
      + '<svg class="fig-hint fig-live-hint" viewBox="-13 -13 30 37" aria-hidden="true" focusable="false"><circle class="fig-hint-ring" r="11" fill="none" stroke="#d4a853" stroke-width="1.8"/>'
      + '<g class="fig-hint-cursor"><path d="M 0 0 V 18 L 4.9 13.8 L 8.2 21 L 11.4 19.5 L 8.2 12.5 L 14.4 12.3 Z" fill="#fff" stroke="#d4a853" stroke-width="1.5" stroke-linejoin="round"/></g></svg></span>'
      + '<span aria-hidden="true">' + o.right + '</span>';
    const input = row.querySelector('input');
    const take = () => row.classList.remove('is-armed');          // the mark goes at the first touch
    input.addEventListener('pointerdown', take);
    input.addEventListener('keydown', take);
    input.addEventListener('input', take);
    svg.insertAdjacentElement('afterend', row);
    return { row, input };
  }

  const LIVE = {
    // Fig 1.5: the gate voltage of a field-effect transistor. Charge gathers on the gate, the holes under it sink,
    // electrons come in from both wells; at the threshold the two rows meet and current runs round the loop.
    mosfet(svg, card) {
      const VT = 0.7, VMAX = 1.5;
      const q = s => svg.querySelector(s), qa = s => Array.from(svg.querySelectorAll(s));
      const gate = q('.lv-gate'), holes = q('.lv-holes'), stream = q('.lv-stream'), lamp = q('.lv-lamp');
      const wire = q('.lv-wire'), readout = q('.lv-v'), gname = q('.lv-gname');
      const charges = qa('.lv-q'), els = qa('.lv-e');
      if (!gate || !stream || !readout || !wire) return;

      const { row, input } = slider(svg, { max: VMAX, step: 0.05, label: 'Gate voltage', left: '0 V', right: VMAX + ' V' });

      let shown = 0, target = 0, offset = 0, raf = 0, last = 0, visible = !('IntersectionObserver' in window);

      function render(v) {
        const on = v >= VT - 0.004;
        gate.setAttribute('opacity', clamp(v / 1.2, 0, 1).toFixed(3));
        const n = Math.round(clamp(v / 1.4, 0, 1) * charges.length);
        charges.forEach(c => c.setAttribute('opacity', +c.dataset.n < n ? 1 : 0));
        holes.setAttribute('transform', 'translate(0 ' + (30 * clamp(v / VT, 0, 1)).toFixed(1) + ')');
        els.forEach(e => {
          const p = clamp(v / VT * 4 - +e.dataset.rank, 0, 1);
          const home = +e.dataset.home, slot = +e.dataset.slot;
          e.setAttribute('cx', (home + (slot - home) * p).toFixed(1));
          e.setAttribute('opacity', p > 0.03 && !on ? 1 : 0);   // once whole, the running stream stands for the bridge
        });
        stream.setAttribute('opacity', on ? 1 : 0);
        wire.setAttribute('opacity', on ? 1 : 0);
        lamp.setAttribute('opacity', on ? (0.55 + 0.45 * (v - VT) / (VMAX - VT)).toFixed(3) : 0);
        const lit = v > 0.02 ? '#d4a853' : 'rgba(255,255,255,0.6)';
        readout.textContent = v.toFixed(2) + ' V';
        readout.setAttribute('fill', lit);
        gname.setAttribute('fill', lit);
      }

      function frame(now) {
        raf = 0;
        const dt = Math.min(0.05, (now - last) / 1000); last = now;
        shown += (target - shown) * Math.min(1, dt * 9);
        if (Math.abs(target - shown) < 0.002) shown = target;
        if (shown >= VT) {                             // the electrons run, faster as the voltage rises
          offset -= dt * (26 + 120 * (shown - VT) / (VMAX - VT));
          stream.setAttribute('stroke-dashoffset', offset.toFixed(1));
        }
        render(shown);
        if (visible && (shown !== target || shown >= VT)) tick();
      }
      function tick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); } }

      function set(v) {
        target = clamp(v, 0, VMAX);
        input.setAttribute('aria-valuetext', target.toFixed(2) + ' volts, ' + (target >= VT ? 'current flows, lamp lit' : 'no current'));
        if (reduce.matches) { shown = target; render(shown); } else tick();
      }
      input.addEventListener('input', () => set(parseFloat(input.value)));

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(es => es.forEach(en => { visible = en.isIntersecting; if (visible) tick(); })).observe(card);
      }
      render(0);
    }
  };

  // Fig 2.1: noise on a wire. The slider sets how hard both levels are shaken (by the same amount); a digit is misread
  // while its level is past a threshold. Ternary's margin is 50 units, binary's 100, and the noise tops out at 62.
  LIVE.noise = function (svg, card) {
    const dots = Array.from(svg.querySelectorAll('.lv-dot')), bad = Array.from(svg.querySelectorAll('.lv-bad'));
    const ok = svg.querySelector('.lv-ok'), read = svg.querySelector('.lv-read-t'), arrow = svg.querySelector('.lv-arrow');
    if (dots.length < 2 || !read || !arrow) return;
    const TOP = 62, MARGIN = 50;
    const W = [1, 0.55, 0.7, 0.25, 0.4, 0.1, 0.3, 0.05, 0.35, 0.6, 0.45, 0.85, 0.7, 0.95];   // one shake, six seconds
    const { input } = slider(svg, { max: 1, step: 0.02, label: 'Noise', left: 'quiet', right: 'noisy' });
    let amp = 0, raf = 0, visible = !('IntersectionObserver' in window), wrong = null, wrongUntil = 0;
    function render(now) {
      let w = 1;                                                // still pictures show the noise at its largest
      if (!reduce.matches) { const p = (now / 6000 * W.length) % W.length, i = Math.floor(p); w = W[i] + (W[(i + 1) % W.length] - W[i]) * (p - i); }
      const lift = amp * TOP * w;
      dots.forEach(d => d.setAttribute('transform', 'translate(0 ' + (-lift).toFixed(1) + ')'));
      if (lift > MARGIN && !reduce.matches) wrongUntil = now + 1100;              // a misread digit stays misread long enough to be seen
      const is = lift > MARGIN || now < wrongUntil;
      if (is !== wrong) {
        wrong = is;
        bad.forEach(el => el.setAttribute('opacity', is ? 1 : 0));
        ok.setAttribute('opacity', is ? 0 : 1);
        read.textContent = is ? '+1' : '0';
        read.setAttribute('fill', is ? '#ec8d8d' : '#ece6da');
      }
      const top = 164 - amp * TOP;
      arrow.setAttribute('opacity', amp > 0.12 ? 1 : 0);
      arrow.setAttribute('d', 'M 200 164 V ' + top.toFixed(1) + ' m -5 6 l 5 -6 l 5 6');
    }
    function frame(now) { raf = 0; render(now); if (visible && !reduce.matches && (amp > 0 || now < wrongUntil)) raf = requestAnimationFrame(frame); }
    const tick = () => { if (!raf) raf = requestAnimationFrame(frame); };
    input.addEventListener('input', () => {
      amp = parseFloat(input.value);
      input.setAttribute('aria-valuetext', Math.round(amp * 100) + ' percent noise');
      tick();
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(es => es.forEach(en => { visible = en.isIntersecting; if (visible) tick(); })).observe(card);
    }
    render(0);
  };

  // A figure the reader starts with one press (owner, 2026-11-12: "the animation is started by the user, only one
  // press"). It rests at its first moment with the press-here mark showing (.fig-hint in the picture, card class
  // is-armed); a click, a tap or the key button plays data-run="start end" (SMIL seconds) once, then it rests again
  // (data-rest: the waiting moment; data-hold="end": it stays on its result, and a press plays it again).
  // While it runs it is an ordinary playing figure to book.js, which still holds it off screen and while scrolling.
  LIVE.press = function (svg, card) {
    if (typeof svg.setCurrentTime !== 'function') return;
    const [t0, t1] = (svg.dataset.run || '0.05 10').trim().split(/\s+/).map(Number);
    const tRest = +(svg.dataset.rest || 0);                    // the moment it waits at before the first press
    const hold = svg.dataset.hold === 'end';                   // stay on the last moment (a result), or go back to rest
    let running = false, timer = 0;
    const key = document.createElement('button');
    key.type = 'button';
    key.className = 'fig-press';
    key.textContent = svg.dataset.pressLabel || 'Play the figure';
    svg.insertAdjacentElement('afterend', key);
    function rest(t) {
      running = false; clearInterval(timer);
      card.dataset.userPaused = '1'; delete card.dataset.userPlayed;
      svg.pauseAnimations(); svg.setCurrentTime(t);
      card.classList.add('is-armed'); card.classList.remove('is-running');
      key.disabled = false;
    }
    function run() {
      if (running) return;
      running = true;
      card.classList.remove('is-armed'); card.classList.add('is-running');
      key.disabled = true;
      svg.setCurrentTime(t0);
      delete card.dataset.userPaused;
      if (reduce.matches) card.dataset.userPlayed = '1';      // asked for, so it plays (the book's rule for reduced motion)
      svg.unpauseAnimations();
      timer = setInterval(() => {
        if (svg.getCurrentTime() < t1) return;
        if (hold) { rest(t1); return; }
        rest(tRest);
        svg.classList.remove('fig-cut'); void svg.getBoundingClientRect(); svg.classList.add('fig-cut');
      }, 80);
    }
    svg.addEventListener('click', run);
    key.addEventListener('click', run);
    rest(tRest);
  };

  // Switches the reader works (Fig 2.2): each press area (data-sw="A") flips its switch. A part with data-when="A&B"
  // (also "!A", and "|" for or) shows while that holds; a lever with data-turn="A" turns; a press-here mark with
  // data-hint="A" shows on the first switch not yet tried. Key buttons give the keyboard the same switches.
  LIVE.switches = function (svg, card) {
    const names = (svg.dataset.switches || 'A B').trim().split(/\s+/);
    const state = {}, tried = {}, keys = {};
    names.forEach(n => { state[n] = false; });
    const holds = expr => expr.split('|').some(alt => alt.split('&').every(t => t[0] === '!' ? !state[t.slice(1)] : !!state[t]));
    const parts = Array.from(svg.querySelectorAll('[data-when]'));
    const levers = Array.from(svg.querySelectorAll('[data-turn]'));
    const hints = Array.from(svg.querySelectorAll('[data-hint]'));
    function render() {
      parts.forEach(el => el.setAttribute('opacity', holds(el.dataset.when) ? 1 : 0));
      levers.forEach(el => el.classList.toggle('is-on', !!state[el.dataset.turn]));
      const next = names.find(n => !tried[n]);
      hints.forEach(el => { el.style.display = el.dataset.hint === next ? '' : 'none'; });
      card.classList.toggle('is-armed', !!next);
      names.forEach(n => keys[n].setAttribute('aria-pressed', state[n] ? 'true' : 'false'));
    }
    function flip(n) { state[n] = !state[n]; tried[n] = true; render(); }
    let after = svg;
    names.forEach(n => {
      const k = document.createElement('button');
      k.type = 'button'; k.className = 'fig-press'; k.textContent = 'Switch ' + n;
      k.addEventListener('click', () => flip(n));
      after.insertAdjacentElement('afterend', k); after = k; keys[n] = k;
    });
    svg.querySelectorAll('[data-sw]').forEach(el => el.addEventListener('click', () => flip(el.dataset.sw)));
    render();
  };

  document.querySelectorAll('svg[data-live]').forEach(svg => {
    const run = LIVE[svg.dataset.live], card = svg.closest('.diagram-card, .light-diagram');
    if (run && card) run(svg, card);
  });
})();
