/* Dirty Chicken · Wahlseite Zitate: Übersetzung (3), Satz für Satz (8), Untertitel (9), Rad (12), Lauter (14). Nur transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function p(el) { var r = el.getBoundingClientRect(), vh = innerHeight; return Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); }
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }

  /* 3 Die Übersetzung: antippen tauscht Berlinerisch gegen Hochdeutsch, noch einmal zurück */
  document.addEventListener('click', function (e) {
    var z = e.target.closest('.zt3-z'); if (!z) return;
    z.classList.toggle('an');
  });

  /* 8 Satz für Satz: der Satz in der Mitte des Schirms bestimmt das Bild links */
  if ('IntersectionObserver' in window) {
    var io8 = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var s = e.target, box = s.closest('.zt8').querySelector('.zt8-box');
        box.dataset.wahl = s.dataset.s;
        s.parentNode.querySelectorAll('.zt8-s').forEach(function (x) { x.classList.toggle('an', x === s); });
      });
    }, { rootMargin: '-42% 0px -42% 0px', threshold: 0 });
    document.querySelectorAll('.zt8-s').forEach(function (s) { io8.observe(s); });
  } else {
    document.querySelectorAll('.zt8-s').forEach(function (s) { s.classList.add('an'); });
  }

  /* 9 Die Untertitel: Pfeile schieben Bild und Untertitel seitwärts */
  function kino(k) {
    var n = +k.dataset.akt, m = k.querySelectorAll('.zt9-b').length;
    k.querySelector('.zt9-spur').style.transform = 'translate3d(' + (-n * 100) + '%,0,0)';
    k.querySelector('.zt9-ut-spur').style.transform = 'translate3d(' + (-n * 100) + '%,0,0)';
    k.querySelector('[data-zt9-nr]').textContent = (n + 1) + ' / ' + m;
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.zt9-k'); if (!b) return;
    var k = b.closest('.zt9-kino'), m = k.querySelectorAll('.zt9-b').length;
    k.dataset.akt = (+k.dataset.akt + (+b.dataset.r) + m) % m; kino(k);
  });

  /* Scroll-getrieben: das Rad dreht sich, die Sätze werden lauter */
  var RAD = [].slice.call(document.querySelectorAll('.zt12-dreh')), LAUT = [].slice.call(document.querySelectorAll('.zt14-q'));
  var lt = false;
  function rechnen() {
    lt = false;
    if (ruhig) return;
    RAD.forEach(function (d) { var b = d.closest('.zt12-buehne'); if (!drin(b)) return; d.style.transform = 'rotate(' + (p(b) * 140).toFixed(2) + 'deg)'; });
    LAUT.forEach(function (q) {
      var s = q.closest('.zt14-s'); if (!drin(s)) return;
      var r = s.getBoundingClientRect(), t = Math.max(0, Math.min(1, (innerHeight - r.top) / (innerHeight * .85)));   /* 0 = unten am Rand, 1 = angekommen */
      var e = 1 - Math.pow(1 - t, 3);
      q.style.transform = 'scale(' + (.3 + .7 * e).toFixed(4) + ')';
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  rechnen();
  /* Wahlseite: beim Umschalten neu stellen */
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); root.querySelectorAll('.zt9-kino').forEach(kino); setTimeout(takt, 50); };
})();
