/* Culinarium · «Die Plakate» zur Wahl: Abend antippen, Plakat zeigen; Stapel, Litfasssäule, Durchblättern.
   Nur Klassen und transform, nativer Scroll. */
(function () {
  'use strict';
  /* Abend i zeigt Plakat i: alles mit data-q / data-a im selben [data-pk] bekommt .an */
  function waehle(q) {
    var box = q.closest('[data-pk]'); if (!box) return;
    var i = q.dataset.q;
    box.querySelectorAll('[data-q],[data-a]').forEach(function (x) {
      x.classList.toggle('an', (x.dataset.q !== undefined ? x.dataset.q : x.dataset.a) === i);
    });
  }
  document.addEventListener('click', function (e) { var q = e.target.closest('[data-q]'); if (q) waehle(q); });
  /* 4 Das Heft: Überfahren der Zeile reicht */
  document.addEventListener('mouseover', function (e) { var q = e.target.closest('.pk-04-z'); if (q && !q.classList.contains('an')) waehle(q); });

  /* 3 Der Stapel: das oberste Plakat geht nach hinten */
  document.querySelectorAll('[data-pk-stapel]').forEach(function (s) {
    var K = [].slice.call(s.children), n = K.length, r = s.parentNode;
    s.addEventListener('click', function (e) {
      if (!e.target.closest('.pk-03-p')) return;
      var neu;
      K.forEach(function (k) {
        var p = +k.style.getPropertyValue('--p');
        if (p === 0) { k.classList.add('weg'); setTimeout(function () { k.classList.remove('weg'); }, 380); }
        if (p === 1) neu = k;
        k.style.setProperty('--p', (p - 1 + n) % n);
      });
      r.querySelector('[data-pk-lang]').textContent = neu.dataset.lang;
      r.querySelector('[data-pk-preis]').textContent = neu.dataset.preis;
    });
  });

  /* 10 Litfasssäule und 11 Durchblättern hängen am Scroll */
  var saeulen = [].slice.call(document.querySelectorAll('[data-pk-saeule]'));
  var blaetter = [].slice.call(document.querySelectorAll('[data-pk-blaettern]'));
  var plan = false;
  function takt() {
    plan = false;
    var h = innerHeight;
    saeulen.forEach(function (s) {
      var r = s.getBoundingClientRect(); if (!r.height || r.bottom < -200 || r.top > h + 200) return;
      var p = (h - r.top) / (h + r.height);
      s.querySelector('.pk-10-ring').style.setProperty('--dreh', (40 - p * 220).toFixed(2) + 'deg');
    });
    blaetter.forEach(function (b) {
      var r = b.getBoundingClientRect(); if (!r.height) return;
      var weg = Math.min(Math.max((90 - r.top) / (r.height - h + 40), 0), 1);
      var B = b.querySelectorAll('[data-a]'), n = +b.style.getPropertyValue('--n');
      var i = String(Math.min(n - 1, Math.floor(weg * n)));
      B.forEach(function (x) { x.classList.toggle('an', x.dataset.a === i); });
      b.querySelector('.pk-11-strich').style.setProperty('--lauf', ((+i + 1) / n).toFixed(3));
    });
  }
  function los() { if (!plan) { plan = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true });
  addEventListener('resize', los);
  /* beim Wechsel der Fassung neu messen */
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (el) { if (alt) alt(el); los(); };
  los();
})();
