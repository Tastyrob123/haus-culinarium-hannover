/* Culinarium · «Seit 2023.» Runde 2: Buch, Story, Teller als Uhr, Kapitel im Vollbild, langsamere Zahlen.
   Nur Klassen und transform, nativer Scroll. Antippen von [data-q] regelt chronik-wahl.js. */
(function () {
  'use strict';
  /* 5 Das Buch: Umblättern zeigt die nächste Doppelseite */
  document.querySelectorAll('[data-cz-buch]').forEach(function (b) {
    var S = b.querySelectorAll('.cz-05-seite'), n = 0;
    function zeige(i) { n = (i + S.length) % S.length; S.forEach(function (s, k) { s.classList.toggle('an', k === n); }); }
    b.querySelector('.cz-05-weiter').addEventListener('click', function () { zeige(n + 1); });
    b.querySelectorAll('.cz-05-r').forEach(function (r) { r.addEventListener('click', function () { zeige(n + 1); }); });
  });
  /* 6 Die Story: läuft von selbst, solange sie im Bild ist; antippen links zurück, rechts weiter */
  document.querySelectorAll('[data-cz-story]').forEach(function (st) {
    var F = st.querySelectorAll('.cz-06-f'), L = st.querySelectorAll('.cz-06-striche span'), n = 0, uhr = null, sichtbar = false;
    function zeige(i) {
      n = (i + F.length) % F.length;
      F.forEach(function (f, k) { f.classList.toggle('an', k === n); });
      L.forEach(function (l, k) { l.classList.remove('laeuft'); l.classList.toggle('voll', k < n); });
      void st.offsetWidth; if (sichtbar) L[n].classList.add('laeuft');
      clearTimeout(uhr); if (sichtbar) uhr = setTimeout(function () { zeige(n + 1); }, 5000);
    }
    st.querySelector('.cz-06-vor').addEventListener('click', function () { zeige(n + 1); });
    st.querySelector('.cz-06-zur').addEventListener('click', function () { zeige(n - 1); });
    new IntersectionObserver(function (es) {
      sichtbar = es[0].isIntersecting && !st.closest('[hidden]');
      if (sichtbar) zeige(n); else { clearTimeout(uhr); L.forEach(function (l) { l.classList.remove('laeuft'); }); }
    }, { threshold: .5 }).observe(st);
  });
  /* 12 Der Teller als Uhr: der gewählte Moment dreht nach oben */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('.cz-12-q'); if (!q) return;
    var box = q.closest('[data-cz-uhr]'), rad = box.querySelector('.cz-12-rad');
    var alt = +(rad.dataset.d || 0), ziel = -q.dataset.q * 72, diff = ((ziel - alt) % 360 + 540) % 360 - 180;
    rad.dataset.d = alt + diff;
    box.style.setProperty('--dreh', (alt + diff) + 'deg');
  });
  /* 13 Kapitel im Vollbild: die Marke in der Mitte des Bildschirms bestimmt Foto und Satz */
  document.querySelectorAll('[data-cz-kapitel]').forEach(function (box) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var m = e.target.dataset.m;
        box.querySelectorAll('.cz-13-f,.cz-13-s').forEach(function (x) { x.classList.toggle('an', x.dataset.m === m); });
      });
    }, { rootMargin: '-50% 0px -50% 0px' });
    box.querySelectorAll('.cz-13-marken span').forEach(function (s) { io.observe(s); });
  });
  /* 8 und 14: Zahl und Abspann wandern langsamer als die Seite */
  var P = [].slice.call(document.querySelectorAll('[data-cz-par]'));
  function wandern() {
    P.forEach(function (p) {
      if (p.closest('[hidden]')) return;
      var r = p.parentElement.getBoundingClientRect(), mitte = r.top + r.height / 2 - innerHeight / 2;
      p.style.transform = 'translate3d(0,' + (mitte * (p.classList.contains('cz-14-rolle') ? -0.08 : 0.18)).toFixed(1) + 'px,0)';
    });
  }
  if (P.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) { addEventListener('scroll', function () { requestAnimationFrame(wandern); }, { passive: true }); wandern(); }
})();
