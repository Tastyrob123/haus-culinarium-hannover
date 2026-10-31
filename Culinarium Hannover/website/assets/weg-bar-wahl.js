/* Culinarium · Der Weg, die Wand mit der Karte «Die Bar» in 20 Fassungen (nur Wahlseite).
   Am Scrollen: wandern (drift, quer), näher kommen (zoom), in den Gang hinein (tief), Streifen fügen sich (Jalousie), Bilder blenden über. Nur transform und opacity. */
(function () {
  'use strict';
  if (document.documentElement.classList.contains('ruhig')) return;
  var handy = matchMedia('(max-width:860px)'), lt = false;
  var els = [].slice.call(document.querySelectorAll('[data-wb]'));
  var jal = [].slice.call(document.querySelectorAll('[data-wb-jal]'));
  var blende = [].slice.call(document.querySelectorAll('[data-wb-blende]'));

  function sichtbar(el, r, vh) { return !el.closest('[hidden]') && r.bottom > -vh * .2 && r.top < vh * 1.2; }

  function bild() {
    lt = false;
    var vh = innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (!sichtbar(el, r, vh)) return;
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh + r.height))), f = +el.dataset.f || 0, art = el.dataset.wb;
      if (art === 'drift') el.style.transform = 'translate3d(0,' + ((p - .5) * f).toFixed(1) + 'px,0)';
      else if (art === 'quer') el.style.transform = 'translate3d(' + ((p - .5) * f).toFixed(1) + 'px,0,0)';
      else if (art === 'zoom') el.style.transform = 'scale(' + (1 + (1 - p) * f).toFixed(4) + ')';
      else if (art === 'tief') el.style.transform = handy.matches ? '' : 'translate3d(0,0,' + ((p - .5) * f).toFixed(1) + 'px)';
    });
    /* Jalousie: versetzt, in der Bildschirmmitte bündig */
    jal.forEach(function (j) {
      var r = j.getBoundingClientRect();
      if (!sichtbar(j, r, vh)) return;
      var mitte = r.top + r.height / 2, q = Math.min(1, Math.abs(mitte - vh / 2) / (vh * .55));
      j.querySelectorAll('.zb15-s').forEach(function (s) {
        s.style.transform = 'translate3d(0,' + (parseFloat(s.style.getPropertyValue('--o')) * q).toFixed(1) + 'px,0)';
      });
    });
    /* Überblendung: die Bühne steht, die Bilder wechseln mit dem Scrollen */
    blende.forEach(function (b) {
      var fs = [].slice.call(b.querySelectorAll('.zb17-f'));
      if (handy.matches) { fs.forEach(function (f) { f.style.opacity = ''; }); return; }
      var r = b.getBoundingClientRect();
      if (!sichtbar(b, r, vh)) return;
      var p = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height - vh))), t = p * (fs.length - 1);
      fs.forEach(function (f, i) { f.style.opacity = i === 0 ? 1 : Math.max(0, Math.min(1, t - i + 1)).toFixed(3); });
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(bild); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  document.addEventListener('click', function () { setTimeout(takt, 60); });
  addEventListener('keydown', function () { setTimeout(takt, 60); });
  takt();
})();
