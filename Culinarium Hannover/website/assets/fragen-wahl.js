/* Culinarium · «Gut zu wissen» zur Wahl: Fragen antippen, Antwort zeigen; Kartenstapel, Fotoband, Drehteller.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  /* Frage i zeigt Antwort i: alles mit data-q / data-a im selben [data-fw] bekommt .an */
  document.addEventListener('click', function (e) {
    var q = e.target.closest('[data-q]'); if (!q) return;
    var box = q.closest('[data-fw]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
    /* 13 Drehteller: der Kranz dreht die gewählte Frage nach oben */
    if (box.hasAttribute('data-fw-dreh-teller')) {
      var rad = box.querySelector('.fw-13-rad'), alt = +(rad.dataset.d || 0), ziel = -i * 360 / 7;
      var diff = ((ziel - alt) % 360 + 540) % 360 - 180;
      rad.dataset.d = alt + diff;
      rad.style.setProperty('--dreh', (alt + diff) + 'deg');
    }
  });
  /* 6 Fotoband: antippen dreht das Bild um */
  document.addEventListener('click', function (e) {
    var k = e.target.closest('.fw-06-k1'); if (k) k.classList.toggle('um');
  });
  /* 10 Kartenstapel: die oberste Karte geht nach hinten */
  document.querySelectorAll('[data-fw-stapel]').forEach(function (s) {
    var K = [].slice.call(s.children), n = K.length;
    s.addEventListener('click', function (e) {
      if (!e.target.closest('.fw-10-karte')) return;
      K.forEach(function (k) {
        var p = +k.style.getPropertyValue('--p');
        if (p === 0) { k.classList.add('weg'); setTimeout(function () { k.classList.remove('weg'); }, 420); }
        k.style.setProperty('--p', (p - 1 + n) % n);
      });
    });
  });
})();
