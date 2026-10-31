/* Culinarium · «Wann und wie viel», zweite Runde: Bühne mit Tausch, Zoom, Drift und Kamerafahrt am Scrollen.
   Nur Klassen und transform, nativer Scroll, nur sichtbare Fassungen. */
(function () {
  'use strict';
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.classList.contains('ruhig');
  var lauf = false;
  function anteil(el, h) { var r = el.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return null; return Math.min(1, Math.max(0, (h - r.top) / (h + r.height))); }
  function takt() {
    lauf = false;
    var h = innerHeight;
    /* 3 Vier Bildschirme: Fortschritt durch die hohe Hülle bestimmt Satz und Foto (Tausch nur über Deckkraft) */
    document.querySelectorAll('.wv:not([hidden]) [data-tx-buehne]').forEach(function (b) {
      var r = b.getBoundingClientRect(), weg = r.height - h; if (weg <= 0) return;
      var p = Math.min(1, Math.max(0, -r.top / weg)), n = +getComputedStyle(b).getPropertyValue('--n') || 4;
      var i = Math.min(n - 1, Math.floor(p * n));
      if (b.dataset.i !== String(i)) {
        b.dataset.i = i;
        b.querySelectorAll('[data-s]').forEach(function (x) { x.classList.toggle('an', +x.dataset.s === i); });
      }
      b.style.setProperty('--p', p.toFixed(4));
    });
    if (ruhig) return;
    /* 1 Bildlegende: das Foto zieht langsam auf */
    document.querySelectorAll('.wv:not([hidden]) [data-tx-zoom] img').forEach(function (im) {
      var p = anteil(im.parentNode, h); if (p === null) return;
      im.style.transform = 'scale(' + (1.14 - p * .14).toFixed(4) + ')';
    });
    /* 6 Einladung: die zwei Fotos wandern gegenläufig */
    document.querySelectorAll('.wv:not([hidden]) [data-tx-drift]').forEach(function (f) {
      var p = anteil(f, h); if (p === null) return;
      f.style.transform = 'translate3d(0,' + ((p - .5) * 160 * +f.dataset.txDrift).toFixed(1) + 'px,0)';
    });
    /* 7 Leinwand: die Kamera fährt die Tafel entlang */
    document.querySelectorAll('.wv:not([hidden]) [data-tx-fahrt] img').forEach(function (im) {
      var p = anteil(im.parentNode, h); if (p === null) return;
      im.style.transform = 'translate3d(' + ((p - .5) * -14).toFixed(2) + '%,0,0)';
    });
  }
  function an() { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', an, { passive: true });
  addEventListener('resize', an);
  document.addEventListener('click', function () { setTimeout(an, 60); });
  an();
})();
