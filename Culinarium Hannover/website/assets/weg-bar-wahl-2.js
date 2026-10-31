/* Culinarium · Der Weg, die Karte «Die Bar» in 20 weiteren Fassungen (nur Wahlseite).
   Am Scrollen: Fächer geht auf, Säule und Rund drehen, Flügel und Leporello öffnen, Karten wenden, Bilder hängen gerade, Platte und Sticker drehen,
   das Daumenkino blättert. Nur transform und opacity. Wandern und Näherkommen macht weg-bar-wahl.js. */
(function () {
  'use strict';
  if (document.documentElement.classList.contains('ruhig')) return;
  var handy = matchMedia('(max-width:860px)'), lt = false;
  var arten = ['dreh', 'faecher', 'saeule', 'rund', 'fluegel', 'wenden', 'gerade', 'leporello'];
  var els = [].slice.call(document.querySelectorAll('[data-wb]')).filter(function (e) { return arten.indexOf(e.dataset.wb) > -1; });
  var blocks = [].slice.call(document.querySelectorAll('[data-wb-blaettern]'));
  var kl = function (x) { return Math.max(0, Math.min(1, x)); };

  function sichtbar(el, r, vh) { return !el.closest('[hidden]') && r.bottom > -vh * .2 && r.top < vh * 1.2; }
  function alle(el, sel, fn) { [].forEach.call(el.querySelectorAll(sel), fn); }

  function bild() {
    lt = false;
    var vh = innerHeight;
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (!sichtbar(el, r, vh)) return;
      var p = kl((vh - r.top) / (vh + r.height)), f = +el.dataset.f || 0, art = el.dataset.wb, q = kl(p * 1.8);
      if (art === 'dreh') el.style.transform = 'rotate(' + ((p - .5) * f).toFixed(2) + 'deg)';
      else if (art === 'saeule') el.style.transform = 'rotateY(' + (-p * f).toFixed(2) + 'deg)';
      else if (art === 'rund') el.style.transform = 'rotateY(' + ((p - .5) * f).toFixed(2) + 'deg)';
      else if (art === 'faecher') alle(el, '.zc05-b', function (b) {
        b.style.transform = 'rotate(' + (b.style.getPropertyValue('--a') * (.55 + .45 * q)).toFixed(2) + 'deg)';
      });
      else if (art === 'fluegel') {
        var a = handy.matches ? 0 : 68 * (1 - q);
        alle(el, '.zc09-f', function (w) { w.style.transform = a ? 'rotateY(' + (w.classList.contains('l') ? a : -a).toFixed(2) + 'deg)' : ''; });
      } else if (art === 'leporello') {
        var b2 = handy.matches ? 0 : 40 * (1 - q);
        alle(el, '.zc19-p', function (w) { w.style.transform = b2 ? 'rotateY(' + (w.style.getPropertyValue('--s') * b2).toFixed(2) + 'deg)' : ''; });
      } else if (art === 'gerade') alle(el, '.zc13-r', function (w) {
        w.style.transform = 'rotate(' + (w.style.getPropertyValue('--r') * (1 - q)).toFixed(3) + 'deg)';
      });
      else if (art === 'wenden') alle(el, '.zc12-k', function (k) {
        var o = +k.style.getPropertyValue('--o') || 0, w = kl((p - .3 - o * .07) / .14) * 180;
        k.firstElementChild.style.transform = 'rotateY(' + w.toFixed(1) + 'deg)';
      });
    });
    /* Daumenkino: die Bühne steht, Blatt um Blatt klappt nach oben weg */
    blocks.forEach(function (b) {
      var bl = [].slice.call(b.querySelectorAll('.zc17-b:not(.zc17-letzt)'));
      if (handy.matches) { bl.forEach(function (x) { x.style.transform = ''; }); return; }
      var r = b.getBoundingClientRect();
      if (!sichtbar(b, r, vh)) return;
      var t = kl(-r.top / Math.max(1, r.height - vh)) * (bl.length + .4);
      bl.forEach(function (x, i) { x.style.transform = 'rotateX(' + (kl(t - i) * 180).toFixed(1) + 'deg)'; });
    });
  }
  function takt() { if (!lt) { lt = true; requestAnimationFrame(bild); } }
  addEventListener('scroll', takt, { passive: true });
  addEventListener('resize', takt, { passive: true });
  document.addEventListener('click', function () { setTimeout(takt, 60); });
  addEventListener('keydown', function () { setTimeout(takt, 60); });
  takt();
})();
