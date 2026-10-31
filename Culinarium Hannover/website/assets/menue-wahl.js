/* Culinarium · «Was auf den Tisch kommt» zur Wahl: antippen tauscht, Karte wenden, durchs Glas ziehen, Band, angeheftete Karte, Drift und Zoom.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* Teil i zeigt Inhalt i: alles mit data-q / data-a im selben [data-mw] bekommt .an */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]'); if (!q) return;
    var box = q.closest('[data-mw]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
    /* 5 Zwei Seiten: die Karte wendet sich */
    var w = box.querySelector('[data-mw-wende]'); if (w) w.classList.toggle('um', i === '1');
  });
  /* 6 Durchs Glas: der Regler schiebt die Grenze */
  document.querySelectorAll('[data-mw-zieh]').forEach(function (b) {
    var r = b.querySelector('input');
    r.addEventListener('input', function () { b.style.setProperty('--x', r.value); b.classList.add('gezogen'); });
  });
  /* 8 Band: Pfeile blättern um eine Bildbreite */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-mw-band]'); if (!b) return;
    var band = b.closest('.mw08').querySelector('.mw08-band');
    band.scrollBy({ left: +b.dataset.mwBand * band.clientWidth * .6, behavior: 'smooth' });
  });
  /* 9 Die Karte bleibt stehen: das Foto in der Mitte des Fensters bestimmt die leuchtende Zeile */
  if ('IntersectionObserver' in window) document.querySelectorAll('[data-mw-buehne]').forEach(function (b) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var g = e.target.dataset.g;
        b.querySelectorAll('.mw-gang').forEach(function (x) { x.classList.toggle('an', x.dataset.g === g); });
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    b.querySelectorAll('.mw09-f').forEach(function (f) { io.observe(f); });
  });
  /* 12 Drift und 15 Zoom: an die Scroll-Zeitachse gebunden, nur sichtbare Fassungen */
  if (ruhig) return;
  var lauf = false;
  function takt() {
    lauf = false;
    var h = innerHeight;
    document.querySelectorAll('.wv:not([hidden]) [data-mw-drift] img').forEach(function (im) {
      var r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = (r.top + r.height / 2 - h / 2) / h;
      im.style.transform = 'translate3d(0,' + (p * -14).toFixed(2) + '%,0) scale(1.3)';
    });
    document.querySelectorAll('.wv:not([hidden]) [data-mw-zoom] img').forEach(function (im) {
      var r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > h) return;
      var p = Math.min(1, Math.max(0, (h - r.top) / (h + r.height)));
      im.style.transform = 'scale(' + (1.22 - p * .22).toFixed(4) + ')';
    });
  }
  function an() { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', an, { passive: true });
  addEventListener('resize', an);
  document.addEventListener('click', function () { setTimeout(an, 60); });
  an();
})();
