// Live figures (owner, 2026-11-12: "it should be interactable, this sort of game of a transistor, how it actually
// works"). A figure whose <svg> carries data-live is driven by the reader, not by a clock: a slider under the
// picture sets one quantity and the picture answers. The resting picture is plain SVG and reads without this file.
// Motion runs only while the figure is on screen; under reduced motion the picture answers the slider in still
// states (no demonstration sweep, no running stream).
(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));

  const LIVE = {
    // Fig 1.5: the gate voltage of a field-effect transistor. Charge gathers on the gate, the holes under it sink,
    // electrons come in from both wells; at the threshold the two rows meet and current runs round the loop.
    mosfet(svg, card) {
      const VT = 0.7, VMAX = 1.5;
      const q = s => svg.querySelector(s), qa = s => Array.from(svg.querySelectorAll(s));
      const gate = q('.lv-gate'), holes = q('.lv-holes'), stream = q('.lv-stream'), lamp = q('.lv-lamp');
      const arrow = q('.lv-arrow'), readout = q('.lv-v'), gname = q('.lv-gname');
      const charges = qa('.lv-q'), els = qa('.lv-e');
      if (!gate || !stream || !readout) return;

      const row = document.createElement('div');
      row.className = 'fig-live';
      row.innerHTML = '<span aria-hidden="true">0 V</span>'
        + '<input type="range" min="0" max="' + VMAX + '" step="0.05" value="0" aria-label="Gate voltage">'
        + '<span aria-hidden="true">' + VMAX + ' V</span>';
      const input = row.querySelector('input');
      svg.insertAdjacentElement('afterend', row);

      let shown = 0, target = 0, offset = 0, raf = 0, last = 0, visible = false, demo = 0, touched = false;

      function render(v) {
        const on = v >= VT - 0.004;
        gate.setAttribute('opacity', clamp(v / 1.2, 0, 1).toFixed(3));
        const n = Math.round(clamp(v / 1.4, 0, 1) * charges.length);
        charges.forEach(c => c.setAttribute('opacity', +c.dataset.n < n ? 1 : 0));
        holes.setAttribute('transform', 'translate(0 ' + (34 * clamp(v / VT, 0, 1)).toFixed(1) + ')');
        els.forEach(e => {
          const p = clamp(v / VT * 4 - +e.dataset.rank, 0, 1);
          const home = +e.dataset.home, slot = +e.dataset.slot;
          e.setAttribute('cx', (home + (slot - home) * p).toFixed(1));
          e.setAttribute('opacity', p > 0.03 && !on ? 1 : 0);   // once whole, the running stream stands for the bridge
        });
        stream.setAttribute('opacity', on ? 1 : 0);
        arrow.setAttribute('opacity', on ? 1 : 0);
        lamp.setAttribute('opacity', on ? (0.55 + 0.45 * (v - VT) / (VMAX - VT)).toFixed(3) : 0);
        const lit = v > 0.02 ? '#d4a853' : 'rgba(255,255,255,0.6)';
        readout.textContent = v.toFixed(2) + ' V';
        readout.setAttribute('fill', lit);
        gname.setAttribute('fill', lit);
      }

      function frame(now) {
        raf = 0;
        const dt = Math.min(0.05, (now - last) / 1000); last = now;
        if (demo) {                                   // one sweep up and back, so the reader sees what the slider does
          const t = (now - demo) / 1000;
          const v = t < 0.6 ? 0 : t < 3.4 ? 1.2 * (t - 0.6) / 2.8 : t < 5.2 ? 1.2 : t < 7.2 ? 1.2 * (7.2 - t) / 2 : 0;
          target = v; input.value = (Math.round(v * 20) / 20).toFixed(2);
          if (t >= 7.4) demo = 0;
        }
        shown += (target - shown) * Math.min(1, dt * 9);
        if (Math.abs(target - shown) < 0.002) shown = target;
        if (shown >= VT) {
          offset -= dt * (26 + 120 * (shown - VT) / (VMAX - VT));
          stream.setAttribute('stroke-dashoffset', offset.toFixed(1));
        }
        render(shown);
        if (visible && (demo || shown !== target || shown >= VT)) tick();
      }
      function tick() { if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); } }

      function set(v) {
        target = clamp(v, 0, VMAX);
        input.setAttribute('aria-valuetext', target.toFixed(2) + ' volts, ' + (target >= VT ? 'current flows, lamp lit' : 'no current'));
        if (reduce.matches) { shown = target; render(shown); } else tick();
      }
      function take() { touched = true; demo = 0; }
      input.addEventListener('pointerdown', take);
      input.addEventListener('keydown', take);
      input.addEventListener('input', () => { take(); set(parseFloat(input.value)); });

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(es => es.forEach(en => {
          visible = en.isIntersecting;
          if (!visible) return;
          if (!touched && !demo && !reduce.matches && en.intersectionRatio >= 0.6 && !card.dataset.liveShown) {
            card.dataset.liveShown = '1'; demo = performance.now();
          }
          tick();
        }), { threshold: [0, 0.6] }).observe(card);
      } else { visible = true; }
      render(0);
    }
  };

  document.querySelectorAll('svg[data-live]').forEach(svg => {
    const run = LIVE[svg.dataset.live], card = svg.closest('.diagram-card, .light-diagram');
    if (run && card) run(svg, card);
  });
})();
