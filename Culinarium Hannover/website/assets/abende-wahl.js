/* Culinarium · «Alle Abende» zur Wahl: Weinkarte, roter Faden, Jahresreihen, Planschrank, Eins nach dem anderen.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  /* Abend i zeigen: alles mit data-q / data-a im selben [data-aw] bekommt .an */
  function zeige(box, i) {
    i = String(i);
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
    box.dataset.akt = i;
  }
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-aw] [data-q]');
    if (q) { zeige(q.closest('[data-aw]'), q.dataset.q); return; }
    var s = e.target.closest('[data-schritt]');
    if (s) { var b = s.closest('[data-aw]'), n = b.querySelectorAll('[data-q]').length; zeige(b, ((+b.dataset.akt || 0) + +s.dataset.schritt + n) % n); return; }
    var r = e.target.closest('[data-reihe]');
    if (r) { var band = r.closest('.aw10-r').querySelector('.aw10-band'); band.scrollBy({ left: +r.dataset.reihe * band.clientWidth * .8, behavior: 'smooth' }); return; }
    /* 14 Planschrank: Schublade auf und zu */
    var l = e.target.closest('[data-lade]');
    if (l) {
      var auf = l.getAttribute('aria-expanded') !== 'true', innen = l.nextElementSibling;
      l.setAttribute('aria-expanded', auf); innen.hidden = !auf; l.parentNode.classList.toggle('offen', auf);
      if (auf && window.culinariumNeu) window.culinariumNeu(innen);
    }
  });
  /* 3 Weinkarte: mit der Maus reicht Überfahren, beim Scrollen zeigt die Zeile in der Mitte ihr Plakat */
  if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
    document.addEventListener('mouseover', function (e) { var q = e.target.closest('.aw03-z'); if (q && !q.classList.contains('an')) zeige(q.closest('[data-aw]'), q.dataset.q); });
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) zeige(e.target.closest('[data-aw]'), e.target.dataset.q); });
    }, { rootMargin: '-48% 0px -48% 0px' });
    document.querySelectorAll('.aw03-z').forEach(function (z) { io.observe(z); });
  }
  /* 5 Roter Faden: die Linie läuft mit dem Scrollen nach unten */
  var faeden = [].slice.call(document.querySelectorAll('[data-aw-faden]')), plan = false;
  function takt() {
    plan = false;
    faeden.forEach(function (f) {
      if (!f.offsetParent) return;
      var r = f.getBoundingClientRect(), p = (innerHeight * .62 - r.top) / r.height;
      f.querySelector('.aw05-linie i').style.transform = 'scaleY(' + Math.max(0, Math.min(1, p)).toFixed(4) + ')';
    });
  }
  function bald() { if (!plan) { plan = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', bald, { passive: true });
  addEventListener('resize', bald);
  document.addEventListener('click', bald);
  addEventListener('keydown', bald);
  takt();
})();
