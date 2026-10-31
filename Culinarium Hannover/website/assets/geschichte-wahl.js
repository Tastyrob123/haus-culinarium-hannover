/* Culinarium · Bar-Seite «Seit 2017 in Linden.» · dritte Runde: Scroll-Momente der Wand (randlos zoomen, atmen, seitwärts ziehen).
   Nur transform/scale/translate, nativer Scroll. Umschalten der Fassungen regelt wahl.js, Auftritte, Zahlen und Filme culinarium.js. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (ruhig) return;
  var box = document.getElementById('geschichte');
  function versteckt(el) { return !!el.closest('[hidden]'); }
  var RAND = [].slice.call(box.querySelectorAll('.g3-randlos'));
  var GLEIT = [].slice.call(box.querySelectorAll('[data-g3-gleit]'));
  var ZUG = [].slice.call(box.querySelectorAll('[data-g3-zug]'));
  function lage(el) { var r = el.getBoundingClientRect(), h = innerHeight; return { r: r, p: (r.top + r.height / 2 - h / 2) / h }; }
  function rahmen() {
    var h = innerHeight;
    RAND.forEach(function (w) {
      if (versteckt(w)) return;
      var r = w.getBoundingClientRect(), p = Math.max(0, Math.min(1, (h - r.top) / (h + r.height * .6)));
      w.style.setProperty('--z', (1.2 - p * .2).toFixed(4));
    });
    GLEIT.forEach(function (z) {
      if (versteckt(z)) return;
      var p = Math.max(-1, Math.min(1, lage(z).p));
      z.style.setProperty('--g', (p * +z.dataset.g3Gleit * Math.min(60, z.offsetHeight * .08)).toFixed(1) + 'px');
    });
    ZUG.forEach(function (w) {
      if (versteckt(w)) return;
      var r = w.getBoundingClientRect(), p = Math.max(0, Math.min(1, (h - r.top) / (h + r.height)));
      var band = w.firstElementChild, weg = Math.max(0, band.scrollWidth - w.clientWidth);
      w.style.setProperty('--x', (-p * weg).toFixed(1) + 'px');
    });
  }
  var wartet = false;
  addEventListener('scroll', function () { if (!wartet) { wartet = true; requestAnimationFrame(function () { wartet = false; rahmen(); }); } }, { passive: true });
  addEventListener('resize', rahmen);
  new MutationObserver(rahmen).observe(box, { attributes: true, subtree: true, attributeFilter: ['hidden'] });
  rahmen();
})();
