/* Culinarium · Hero von «Das Haus» in 15 Fassungen (nur Wahlseite). Scroll-Züge und Tausch; nur transform und opacity. */
(function () {
  var kopf = document.getElementById('kopf');

  /* 11 Drei Seiten der Bar: Zeigen oder Tippen tauscht das Bild an derselben Stelle */
  var f11 = kopf.querySelector('.bk11');
  if (f11) {
    var waehle = function (b) {
      if (!b) return;
      var n = b.dataset.seite;
      f11.querySelectorAll('[data-seite]').forEach(function (x) { x.classList.toggle('an', x.dataset.seite === n); });
    };
    f11.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('mouseenter', function () { waehle(b); });
      b.addEventListener('click', function () { waehle(b); });
    });
  }

  if (document.documentElement.classList.contains('ruhig')) return;
  var tick = false;
  function rechnen() {
    tick = false;
    var f = kopf.querySelector('.bkv:not([hidden])'); if (!f) return;
    var r = f.getBoundingClientRect(), h = innerHeight;
    if (r.bottom < 0 || r.top > h) return;
    var s = Math.max(0, -r.top), p = Math.min(1, s / (h * .6));
    f.querySelectorAll('[data-zieh]').forEach(function (el) {
      var art = el.dataset.zieh;
      if (art === 'nacht' || art === 'nachtwort') el.style.opacity = p;
      else if (art === 'fenster') { el.style.transform = 'scale(' + (1 + p * 1.6) + ')'; el.style.opacity = 1 - Math.max(0, (p - .45) / .45); }
      else if (art === 'innen') el.style.opacity = Math.min(1, Math.max(0, (p - .3) / .5));
      else if (art === 'wort') el.style.transform = 'scale(' + (1 + p * .22) + ')';
      else if (art === 'band') el.style.transform = 'translate3d(' + (-s * .9) + 'px,0,0)';
      else if (art === 'saeule') el.style.transform = 'translate3d(0,' + (-s * .3) + 'px,0)';
      else if (art === 'drift') el.firstElementChild.style.transform = 'translate3d(0,' + (s * .22) + 'px,0)';
      else if (art === 'hoch') el.firstElementChild.style.transform = 'translate3d(0,' + (-s * .28) + 'px,0)';
    });
  }
  function anstoss() { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', anstoss, { passive: true });
  addEventListener('resize', anstoss);
  document.addEventListener('click', function () { setTimeout(anstoss, 30); });
  addEventListener('keydown', function () { setTimeout(anstoss, 30); });
  anstoss();
})();
