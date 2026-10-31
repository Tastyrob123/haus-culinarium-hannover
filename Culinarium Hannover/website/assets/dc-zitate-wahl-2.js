/* Dirty Chicken · Wahlseite Zitate, Runde 2: Schallplatte (3), Tonspur (6), Postkarten (7), Einschlagpapier (10), Abreisskalender (13). Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  function drin(el) { if (el.closest('[hidden]')) return false; var r = el.getBoundingClientRect(); return r.bottom > -300 && r.top < innerHeight + 300; }
  function ankunft(el, weit) { var r = el.getBoundingClientRect(); return Math.max(0, Math.min(1, (innerHeight - r.top) / (innerHeight * (weit || .8)))); }

  /* 7 Postkarten: antippen dreht zurück aufs Bild, noch einmal auf den Satz */
  document.addEventListener('click', function (e) { var k = e.target.closest('.zu7-k'); if (k) k.classList.toggle('um'); });

  /* 13 Abreisskalender: antippen reisst das oberste Blatt ab; nach dem letzten liegt der Block wieder voll da */
  function reissen(b) {
    var blaetter = [].slice.call(b.querySelectorAll('.zu13-blatt')), n = +b.dataset.akt;
    if (n >= blaetter.length - 1) { blaetter.forEach(function (x) { x.classList.remove('weg'); }); n = 0; }
    else { blaetter[n].classList.add('weg'); n++; }
    b.dataset.akt = n;
    var box = b.closest('.zu13').querySelector('.zu13-box'); if (box) box.dataset.wahl = n;
  }
  document.addEventListener('click', function (e) { var b = e.target.closest('.zu13-block'); if (b) reissen(b); });
  document.addEventListener('keydown', function (e) { var b = e.target.closest && e.target.closest('.zu13-block'); if (b && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); reissen(b); } });

  /* Scroll-getrieben: Platte zieht heraus und dreht, Papier geht auf, Tonspur läuft */
  var PL = [].slice.call(document.querySelectorAll('.zu3-spieler')), PA = [].slice.call(document.querySelectorAll('.zu10')), SP = [].slice.call(document.querySelectorAll('.zu6-spur'));
  var handy = innerWidth < 860, lt = false;
  function rechnen() {
    lt = false;
    PL.forEach(function (s) {
      if (!drin(s)) return;
      var t = ruhig ? 1 : ankunft(s, .9), e = 1 - Math.pow(1 - t, 3);
      s.querySelector('.zu3-platte').style.transform = 'translate3d(' + (8 + e * 40).toFixed(2) + '%,0,0) rotate(' + (t * 300).toFixed(1) + 'deg)';
    });
    if (!handy) PA.forEach(function (p) {
      if (!drin(p)) return;
      var t = ruhig ? 1 : ankunft(p, .75), e = 1 - Math.pow(1 - t, 3), w = (1 - e) * 72;
      p.querySelector('.zu10-p.l').style.transform = 'translate3d(' + w.toFixed(2) + '%,0,0)';
      p.querySelector('.zu10-p.r').style.transform = 'translate3d(' + (-w).toFixed(2) + '%,0,0)';
    });
    SP.forEach(function (s) {
      if (!drin(s)) return;
      var r = s.getBoundingClientRect(), t = ruhig ? 1 : Math.max(0, Math.min(1, (innerHeight * .78 - r.top) / (innerHeight * .42)));
      if (s.__t === t) return; s.__t = t;
      var welle = s.querySelector('.zu6-welle'), balken = s.__b || (s.__b = [].slice.call(welle.querySelectorAll('i')).filter(function (i) { return i.offsetWidth; }));
      var w = s.__w || (s.__w = [].slice.call(s.querySelectorAll('.zu6-text span')));
      var nb = Math.round(t * balken.length), nw = Math.round(t * w.length);
      balken.forEach(function (b, i) { b.classList.toggle('an', i < nb); });
      w.forEach(function (x, i) { x.classList.toggle('an', i < nw); });
      s.querySelector('.zu6-kopfl').style.transform = 'translate3d(' + (t * welle.clientWidth).toFixed(1) + 'px,0,0)';
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', function () { handy = innerWidth < 860; SP.forEach(function (s) { s.__b = null; s.__t = -1; }); takt(); }, { passive: true });
  rechnen();
  /* Wahlseite: beim Umschalten neu stellen */
  var alt = window.culinariumNeu;
  window.culinariumNeu = function (root) { if (alt) alt(root); SP.forEach(function (s) { s.__b = null; s.__t = -1; }); setTimeout(takt, 50); };
})();
