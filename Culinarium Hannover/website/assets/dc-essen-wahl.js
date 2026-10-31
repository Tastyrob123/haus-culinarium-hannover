/* Dirty Chicken · Wahlseite Essen: Tippen tauscht (Fassung 4), Zoom am Scrollen (9), die Luke (11). Nur transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  /* 4 Chunks oder Sandwich: das Bild an derselben Stelle tauschen, nichts springt */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.e04-w'); if (!b) return;
    var r = b.closest('.e04'); r.dataset.wahl = b.dataset.s;
    r.querySelectorAll('.e04-w').forEach(function (x) { var an = x === b; x.classList.toggle('an', an); x.setAttribute('aria-pressed', an ? 'true' : 'false'); });
  });
  /* 9 und 11: Scroll-Fortschritt eines Elements zwischen -1 (unten) und 1 (oben), nur solange es im Bild ist */
  var Z = [].slice.call(document.querySelectorAll('.e09-zoom')), L = [].slice.call(document.querySelectorAll('.e11-glas'));
  if (ruhig || (!Z.length && !L.length)) return;
  var lt = false;
  function p(el) { var r = el.getBoundingClientRect(), vh = innerHeight; return Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); }
  function sichtbar(el) { var r = el.getBoundingClientRect(); return r.bottom > -200 && r.top < innerHeight + 200; }
  function rechnen() {
    lt = false;
    Z.forEach(function (z) { if (!sichtbar(z) || z.closest('[hidden]')) return; z.style.setProperty('--z', (1.02 + (1 - p(z)) * .06).toFixed(4)); });
    L.forEach(function (g) { if (!sichtbar(g) || g.closest('[hidden]')) return; g.style.setProperty('--g', (p(g) * -70).toFixed(1) + 'px'); });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  rechnen();
})();
