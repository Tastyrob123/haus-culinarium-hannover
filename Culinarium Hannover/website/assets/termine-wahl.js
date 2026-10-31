/* Culinarium · «Wann und wie viel» zur Wahl: antippen tauscht, Untersetzer wenden, Kerze, Zoom und Drift am Scrollen.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.classList.contains('ruhig');
  /* 14 Freitag oder Samstag: Teil i zeigt Inhalt i, alles im selben [data-tw] */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]'); if (!q) return;
    var box = q.closest('[data-tw]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
  });
  /* 16 Untersetzer: antippen wendet */
  document.addEventListener('click', function (e) {
    var w = e.target.closest('[data-tw-wende]'); if (w) w.classList.toggle('um');
  });
  if (ruhig) return;
  /* 9 Kerze, 12 Zoom, 15 Drift: an die Scroll-Zeitachse gebunden, nur sichtbare Fassungen */
  var lauf = false;
  function anteil(el, h) { var r = el.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return null; return Math.min(1, Math.max(0, (h - r.top) / (h + r.height))); }
  function takt() {
    lauf = false;
    var h = innerHeight;
    document.querySelectorAll('.wv:not([hidden]) [data-tw-kerze]').forEach(function (k) {
      var p = anteil(k, h); if (p === null) return;
      var b = Math.min(1, Math.max(0, (p - .25) / .55));
      k.style.setProperty('--brand', b.toFixed(4));
      k.querySelector('.tw09-wachs').style.transform = 'scaleY(' + (1 - b * .42).toFixed(4) + ')';
      k.querySelector('.tw09-flamme').style.transform = 'translate3d(-50%,' + (b * .42 * k.querySelector('.tw09-kerze').clientHeight * .86).toFixed(1) + 'px,0)';
    });
    document.querySelectorAll('.wv:not([hidden]) [data-tw-zoom] img').forEach(function (im) {
      var p = anteil(im.parentNode, h); if (p === null) return;
      im.style.transform = 'scale(' + (1.12 - p * .12).toFixed(4) + ')';
    });
    document.querySelectorAll('.wv:not([hidden]) [data-tw-drift]').forEach(function (im) {
      var p = anteil(im.closest('svg'), h); if (p === null) return;
      im.style.transform = 'translate3d(0,' + ((p - .5) * 220).toFixed(1) + 'px,0)';
    });
  }
  function an() { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', an, { passive: true });
  addEventListener('resize', an);
  document.addEventListener('click', function () { setTimeout(an, 60); });
  an();
})();
/* Runde 2: 21 Vier Ecken (Foto wächst), 24 Bühne mit Tausch, 28 Band, 31 Drift der Abzüge */
(function () {
  'use strict';
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.classList.contains('ruhig');
  /* 24: der Schritt in der Mitte des Fensters bestimmt Foto und Angabe */
  if ('IntersectionObserver' in window) document.querySelectorAll('[data-tw-buehne]').forEach(function (b) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var s = e.target.dataset.s;
        b.querySelectorAll('[data-a]').forEach(function (x) { x.classList.toggle('an', x.dataset.a === s); });
      });
    }, { rootMargin: '-50% 0px -49% 0px' });
    b.querySelectorAll('[data-s]').forEach(function (s) { io.observe(s); });
  });
  /* 28: Pfeile blättern */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-tw-band]'); if (!b) return;
    var band = b.closest('.tw28').querySelector('.tw28-band');
    band.scrollBy({ left: +b.dataset.twBand * band.clientWidth * .6, behavior: 'smooth' });
  });
  var lauf = false;
  function takt() {
    lauf = false;
    var h = innerHeight;
    document.querySelectorAll('.wv:not([hidden]) [data-tw-ecken]').forEach(function (b) {
      var r = b.getBoundingClientRect(), f = b.querySelector('.tw21-f');
      if (ruhig) { f.style.transform = 'none'; return; }
      if (r.bottom < 0 || r.top > h) return;
      var p = Math.min(1, Math.max(0, -r.top / (h * .7)));
      f.style.transform = 'scale(' + (.42 + .58 * p).toFixed(4) + ')';
    });
    if (ruhig) return;
    document.querySelectorAll('.wv:not([hidden]) [data-tw-drift-h]').forEach(function (f) {
      var r = f.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = (r.top + r.height / 2 - h / 2) / h;
      f.style.transform = 'translate3d(0,' + (p * +f.dataset.twDriftH * 260).toFixed(1) + 'px,0)';
    });
  }
  function an() { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', an, { passive: true });
  addEventListener('resize', an);
  document.addEventListener('click', function () { setTimeout(an, 60); });
  an();
})();
