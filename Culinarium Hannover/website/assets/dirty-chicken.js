/* Dirty Chicken · Drei Worte (die Bühne steht, Bilder und Worte wechseln beim Scrollen) und die schwebenden Sätze am Opening.
   Nur transform, nativer Scroll; ein Takt für beides, nur gerechnet, solange etwas davon im Bild ist. */
(function () {
  'use strict';
  var html = document.documentElement, ruhig = html.classList.contains('ruhig');
  var lauf = document.querySelector('.dr-lauf'), buehne = lauf && lauf.querySelector('.dr-buehne');
  var n = buehne ? buehne.querySelectorAll('.dr-bild').length : 0, akt = -1;
  var Q = [].slice.call(document.querySelectorAll('.op-q,.op-plakat'));
  var qAn = false, dAn = false, lt = false;
  if ('IntersectionObserver' in window) {
    if (lauf) new IntersectionObserver(function (es) { dAn = es[0].isIntersecting; takt(); }, { rootMargin: '30% 0px' }).observe(lauf);
    var op = document.querySelector('.op-raster');
    if (op) new IntersectionObserver(function (es) { qAn = es[0].isIntersecting; takt(); }, { rootMargin: '20% 0px' }).observe(op);
  } else { dAn = true; qAn = true; }
  function rechnen() {
    lt = false;
    var vh = innerHeight;
    if (buehne && dAn) {
      var r = lauf.getBoundingClientRect();
      var p = (-r.top) / (r.height - vh);
      p = Math.max(0, Math.min(.9999, p));
      var s = Math.floor(p * n);
      if (s !== akt) { akt = s; buehne.dataset.schritt = s; }
    }
    if (qAn && !ruhig) Q.forEach(function (q) {
      var b = q.getBoundingClientRect(), c = Math.max(-1, Math.min(1, (b.top + b.height / 2 - vh / 2) / vh));
      var f = parseFloat(q.style.getPropertyValue('--g0')) || 0;
      q.style.setProperty('--g', (c * f * 64).toFixed(1) + 'px');
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  rechnen();
})();
