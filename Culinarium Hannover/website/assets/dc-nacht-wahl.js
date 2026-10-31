/* Dirty Chicken · Wahlseite Nacht: Filmstreifen (2), Stories (5), Buchstaben (6), Liste am Handy (7), Prost (14). Nur transform, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function p(el) { var r = el.getBoundingClientRect(), vh = innerHeight; return Math.max(-1, Math.min(1, (r.top + r.height / 2 - vh / 2) / vh)); }
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }

  /* 5 Stories: Karten stehen nach ihrem Abstand zur gewählten, antippen holt sie in die Mitte */
  function stories(b) {
    var akt = +b.dataset.akt, karten = [].slice.call(b.querySelectorAll('.nx5-k'));
    var breit = karten[0] ? karten[0].offsetWidth : 300, luft = Math.min(28, innerWidth * .02);
    karten.forEach(function (k, i) {
      var d = i - akt, s = d === 0 ? 1 : .86;
      k.style.transform = 'translate(' + (d * (breit + luft)).toFixed(1) + 'px,0) scale(' + s + ')';
      k.classList.toggle('an', d === 0);
      k.style.zIndex = String(10 - Math.abs(d));
    });
  }
  var buehnen = [].slice.call(document.querySelectorAll('.nx5-buehne'));
  buehnen.forEach(stories);
  document.addEventListener('click', function (e) {
    var k = e.target.closest('.nx5-k'); if (!k) return;
    var b = k.closest('.nx5-buehne'); b.dataset.akt = k.dataset.i; stories(b);
  });
  /* 7 Die Liste am Handy: tippen tauscht das Bild oben */
  document.addEventListener('click', function (e) {
    var z = e.target.closest('.nx7-z'); if (!z) return;
    var r = z.closest('.nx7-rechts'), h = r && r.querySelector('.nx7-handy'); if (!h) return;
    e.preventDefault(); h.dataset.wahl = z.dataset.s;
    r.querySelectorAll('.nx7-z').forEach(function (x) { x.classList.toggle('an', x === z); });
  });

  /* Scroll-getrieben: Filmstreifen zieht seitwärts, Buchstabenbild driftet, Gläser stossen an */
  var SP = [].slice.call(document.querySelectorAll('.nx2-spur')), BU = [].slice.call(document.querySelectorAll('.nx6-bild')), PR = [].slice.call(document.querySelectorAll('.nx14-paar'));
  var lt = false;
  function rechnen() {
    lt = false;
    if (ruhig) return;
    SP.forEach(function (s) { if (!drin(s)) return; var q = (1 - p(s)) / 2; s.style.transform = 'translate3d(' + (-(s.scrollWidth - s.parentNode.clientWidth) * Math.max(0, Math.min(1, q))).toFixed(1) + 'px,0,0)'; });
    BU.forEach(function (b) { var w = b.closest('.nx6-wort'); if (!drin(w)) return; b.setAttribute('transform', 'translate(0 ' + (p(w) * 90).toFixed(1) + ')'); });
    PR.forEach(function (pa) {
      if (!drin(pa)) return;
      var r = pa.getBoundingClientRect(), q = Math.max(0, Math.min(1, (innerHeight - r.top) / (innerHeight * .75)));   /* 0 = unten am Rand, 1 = angekommen */
      var e = 1 - Math.pow(1 - q, 3), weg = (1 - e) * 46;
      pa.querySelector('.nx14-g.l').style.transform = 'translate3d(' + (-weg).toFixed(2) + '%,0,0)';
      pa.querySelector('.nx14-g.r').style.transform = 'translate3d(' + weg.toFixed(2) + '%,0,0)';
      pa.classList.toggle('prost', q >= .96);
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', function () { buehnen.forEach(stories); takt(); }, { passive: true });
  rechnen();
  /* Filme der Wahlseite: nur die gezeigte Fassung bekommt ihre Quelle, spielt, solange sie zu sehen ist (17 Filme auf einmal wären 85 MB) */
  var fio = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { var v = e.target.querySelector('video'); if (!v) return; if (e.isIntersecting) { if (!v.src) v.src = v.dataset.film; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else if (v.src) v.pause(); });
  }, { threshold: .3 }) : null;
  function filme(root) {
    (root || document).querySelectorAll('.filmw').forEach(function (f) { if (f.closest('[hidden]')) return; if (fio) fio.observe(f); else { var v = f.querySelector('video'); v.src = v.dataset.film; v.play(); } });
  }
  filme();
  /* Wahlseite: beim Umschalten neu stellen */
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); root.querySelectorAll('.nx5-buehne').forEach(stories); filme(root); setTimeout(takt, 50); };
})();
