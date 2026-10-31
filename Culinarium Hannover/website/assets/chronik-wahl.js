/* Culinarium · «Seit 2023.» zur Wahl: Jahre antippen, mitlaufendes Jahr, Messbecher, Querband, Damals und heute.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  /* Moment i zeigt Bild i: alles mit data-q / data-a im selben [data-ch] bekommt .an */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]'); if (!q) return;
    var box = q.closest('[data-ch]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
  });
  /* 1 Das mitlaufende Jahr: der Moment in der Bildschirmmitte rollt die Jahreszahl */
  document.querySelectorAll('[data-ch-lauf]').forEach(function (box) {
    var rolle = box.querySelector('.ch-01-rolle'), wann = box.querySelectorAll('.ch-01-wann span');
    wann[0].classList.add('an');
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var m = +e.target.dataset.m;
        rolle.style.setProperty('--m', m);
        wann.forEach(function (w, i) { w.classList.toggle('an', i === m); });
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    box.querySelectorAll('.ch-01-m').forEach(function (m) { io.observe(m); });
  });
  /* 12 Der Messbecher: füllt sich mit dem Scrollen, der erreichte Strich zeigt sein Bild */
  var becher = [].slice.call(document.querySelectorAll('[data-ch-becher]'));
  function fuellen() {
    becher.forEach(function (box) {
      if (box.closest('[hidden]')) return;
      var glas = box.querySelector('.ch-12-glas'), r = glas.getBoundingClientRect();
      var f = Math.min(1, Math.max(0.05, (innerHeight * .6 - r.top) / r.height));
      glas.style.setProperty('--f', f.toFixed(3));
      var n = 0;
      box.querySelectorAll('.ch-12-strich').forEach(function (s) { if (s.getBoundingClientRect().top < innerHeight * .6) n = Math.max(n, +s.dataset.m); });
      box.querySelectorAll('[data-m]').forEach(function (x) { x.classList.toggle('an', +x.dataset.m === n); });
    });
  }
  if (becher.length) { addEventListener('scroll', function () { requestAnimationFrame(fuellen); }, { passive: true }); fuellen(); }
  /* 14 Das Querband: Pfeile blättern um ein Bild */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ch-band]'); if (!b) return;
    var band = b.closest('.ch-14').querySelector('.ch-14-band'), k = band.firstElementChild;
    band.scrollBy({ left: +b.dataset.chBand * (k.offsetWidth + 20), behavior: 'smooth' });
  });
  /* 15 Damals und heute: der Griff schiebt die Grenze */
  document.querySelectorAll('[data-ch-schieber]').forEach(function (f) {
    var r = f.querySelector('input');
    r.addEventListener('input', function () { f.style.setProperty('--p', r.value); });
  });
})();
