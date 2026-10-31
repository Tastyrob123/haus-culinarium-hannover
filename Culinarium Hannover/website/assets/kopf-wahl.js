/* Culinarium · Kopf von «Alle Abende» in 15 Fassungen, dritte Runde: Heros (nur Wahlseite). Überblende und Scroll-Züge; nur transform und opacity. */
(function () {
  var ruhig = document.documentElement.classList.contains('ruhig');
  var kopf = document.getElementById('kopf');
  if (ruhig) return;

  /* 2 Überblende: alle sechs Sekunden der nächste Moment, nur solange die Fassung zu sehen ist */
  var f2 = kopf.querySelector('.kh02');
  if (f2) setInterval(function () {
    if (f2.closest('.kwv').hidden || f2.getBoundingClientRect().bottom < 0) return;
    var bs = f2.querySelectorAll('.kh02-b'), i = [].indexOf.call(bs, f2.querySelector('.kh02-b.an'));
    bs[i].classList.remove('an'); bs[(i + 1) % bs.length].classList.add('an');
  }, 6000);

  var tick = false;
  function rechnen() {
    tick = false;
    var f = kopf.querySelector('.kwv:not([hidden])'); if (!f) return;
    var r = f.getBoundingClientRect(), h = innerHeight;
    if (r.bottom < 0 || r.top > h) return;
    var s = Math.max(0, -r.top), p = Math.min(1, s / (h * .8));   // wie weit über den Hero hinaus gescrollt
    f.querySelectorAll('[data-zieh]').forEach(function (el) {
      var art = el.dataset.zieh;
      if (art === 'innen') el.firstElementChild.style.transform = 'translate3d(0,' + (s * .2) + 'px,0)';
      else if (art === 'zurueck') el.style.transform = 'translate3d(0,' + (s * .4) + 'px,0)';
      else if (art === 'vor') el.style.transform = 'translate3d(0,' + (-s * .35) + 'px,0)';
      else if (art === 'hinein') el.style.transform = 'scale(' + (1 + p * .55) + ')';
      else if (art === 'weit') { var a = innerWidth < 860 ? .84 : .72; el.style.transform = 'scale(' + (a + (1 - a) * Math.min(1, s / (h * .55))) + ')'; }
    });
  }
  function anstoss() { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }
  addEventListener('scroll', anstoss, { passive: true });
  addEventListener('resize', anstoss);
  document.addEventListener('click', function () { setTimeout(anstoss, 30); });
  addEventListener('keydown', function () { setTimeout(anstoss, 30); });
  anstoss();
})();
